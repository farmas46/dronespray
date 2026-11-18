# Prerender every page of the built site (dist/) into static HTML, one folder per language and page:
#   dist/index.html (Greek home), dist/ds600/index.html, dist/en/index.html, dist/en/ds600/index.html, ...
# Also writes dist/sitemap.xml with every page and its language versions.
# Needs Microsoft Edge (Windows). Run after tools/prod.py:   powershell -File tools\prerender.ps1
param([int]$Port = 8137)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$dist = Join-Path $root 'dist'
$SITE = 'https://www.dronespray-premixingsystems.com'
$langs = 'el', 'en', 'es', 'it', 'fr', 'de'
$views = @('home', 'ds600', 'ds500', 'ds420', 'ds400', 'ds300', 'ds200', 'ds200c', 'ds110', 'pm20', 'accessories', 'dealers', 'network', 'contact', 'privacy') +
         @('pm2637', 'pm2545', 'fm1', 'pdr', 'reel', 'panel', 'led', 'nozzle', 'lidmix', 'dpump', 'bracket', 'wsp', 'lid', 'herbkit', 'pnozzle', 'rinse' | ForEach-Object { "acc-$_" })
function PathOf([string]$v, [string]$l) { (($(if ($l -eq 'el') { '' } else { "/$l" })) + $(if ($v -eq 'home') { '' } else { "/$v" })) + '/' }
$edge = @("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $edge) { throw 'Microsoft Edge not found' }

# The app template every page starts from (kept as 404.html so unknown URLs still load the app).
$tpl = [IO.File]::ReadAllText((Join-Path $dist 'index.html'))
if ($tpl -notmatch '<base href="/">') { throw 'dist/index.html needs <base href="/"> in <head>' }
[IO.File]::WriteAllText((Join-Path $dist '404.html'), $tpl, (New-Object Text.UTF8Encoding $false))

# Tiny static server for dist/: real files as they are, any other path gets the template.
$server = Start-Job -ArgumentList $dist, $Port -ScriptBlock {
  param($dist, $port)
  $mime = @{ '.html' = 'text/html; charset=utf-8'; '.js' = 'text/javascript; charset=utf-8'; '.css' = 'text/css; charset=utf-8'; '.webp' = 'image/webp'; '.png' = 'image/png'; '.jpg' = 'image/jpeg'; '.svg' = 'image/svg+xml'; '.woff2' = 'font/woff2'; '.json' = 'application/json'; '.xml' = 'application/xml'; '.txt' = 'text/plain; charset=utf-8'; '.pdf' = 'application/pdf' }
  $l = [Net.HttpListener]::new(); $l.Prefixes.Add("http://localhost:$port/"); $l.Start()
  while ($l.IsListening) {
    $c = $l.GetContext(); $rel = [Uri]::UnescapeDataString($c.Request.Url.AbsolutePath).TrimStart('/')
    $f = Join-Path $dist $rel
    if (Test-Path $f -PathType Container) { $f = Join-Path $f 'index.html' }
    if (-not (Test-Path $f -PathType Leaf)) { $f = Join-Path $dist '404.html' }
    $b = [IO.File]::ReadAllBytes($f); $ext = [IO.Path]::GetExtension($f).ToLower()
    $c.Response.ContentType = $(if ($mime[$ext]) { $mime[$ext] } else { 'application/octet-stream' })
    $c.Response.OutputStream.Write($b, 0, $b.Length); $c.Response.Close()
  }
}
Start-Sleep 2
$out = Join-Path $env:TEMP ('prerender-' + [guid]::NewGuid()); New-Item -ItemType Directory $out | Out-Null
$prof = Join-Path $env:TEMP ('prerender-edge-' + [guid]::NewGuid())
$done = 0; $failed = @()
try {
  foreach ($l in $langs) { foreach ($v in $views) {
    $p = PathOf $v $l
    # Edge prints harmless warnings on stderr; do not let them stop the script.
    $ErrorActionPreference = 'Continue'
    $html = & $edge --headless=new --disable-gpu --no-first-run --log-level=3 --user-data-dir="$prof" --virtual-time-budget=2500 --dump-dom "http://localhost:$Port$p`?prerender" 2>$null | Out-String
    $ErrorActionPreference = 'Stop'
    if ($html -notmatch '<main id="view">\s*<' -or $html -notmatch 'rel="canonical"') { $failed += $p; continue }
    $html = '<!doctype html>' + "`n" + $html.Trim() + "`n"
    $dir = Join-Path $out ($p.Trim('/')); New-Item -ItemType Directory -Force $dir | Out-Null
    [IO.File]::WriteAllText((Join-Path $dir 'index.html'), $html, (New-Object Text.UTF8Encoding $false))
    $done++
  } }
} finally {
  Stop-Job $server; Remove-Job $server -Force
  Remove-Item -Recurse -Force $prof -ErrorAction SilentlyContinue
}
if ($failed.Count) { throw "Prerender failed for: $($failed -join ', ') (nothing was copied)" }
Copy-Item (Join-Path $out '*') $dist -Recurse -Force
Remove-Item -Recurse -Force $out

# Sitemap: every page, with its language versions.
$today = (Get-Date).ToString('yyyy-MM-dd')
$sb = [Text.StringBuilder]::new()
[void]$sb.Append('<?xml version="1.0" encoding="UTF-8"?>' + "`n" + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">' + "`n")
foreach ($v in $views) { foreach ($l in $langs) {
  [void]$sb.Append("<url><loc>$SITE$(PathOf $v $l)</loc><lastmod>$today</lastmod>")
  foreach ($a in $langs) { [void]$sb.Append("<xhtml:link rel=`"alternate`" hreflang=`"$a`" href=`"$SITE$(PathOf $v $a)`"/>") }
  [void]$sb.Append("<xhtml:link rel=`"alternate`" hreflang=`"x-default`" href=`"$SITE$(PathOf $v 'en')`"/></url>`n")
} }
[void]$sb.Append('</urlset>' + "`n")
[IO.File]::WriteAllText((Join-Path $dist 'sitemap.xml'), $sb.ToString(), (New-Object Text.UTF8Encoding $false))
"Prerendered $done pages; sitemap has $($views.Count * $langs.Count) URLs."
