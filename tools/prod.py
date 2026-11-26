"""Production build: src.html -> dist/ (static site for GitHub Pages / Netlify).

Images become separate optimised files with 400/800 px versions for srcset,
fonts become WOFF2, CSS and JS are minified into hashed files, and SEO files,
favicon, social image and host config are written.  Settings: tools/site.json.
"""
import re, os, sys, json, shutil, hashlib, subprocess, datetime
try:
    import brotli  # real module if installed (pip install brotli)
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shim'))  # falls back to Node's brotli
from PIL import Image
from fontTools.ttLib import TTFont

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
OUT = D + 'dist/'
ESB = os.environ.get('ESBUILD') or shutil.which('esbuild') or ('/opt/npm-tools/node_modules/esbuild/bin/esbuild' if os.path.exists('/opt/npm-tools/node_modules/esbuild/bin/esbuild') else None)
CFG = json.load(open(D + 'tools/site.json', encoding='utf8'))
URL = (CFG.get('url') or '').rstrip('/')

src = open(D + 'src.html', encoding='utf8').read()
css = src[src.index('<style>') + 7:src.index('</style>')]
body = src[src.index('</style>') + 8:src.index('<script>')]
js = src[src.index('<script>') + 8:src.rindex('</script>')]
body = re.sub(r'<title>.*?</title>|<meta name="claude:[^>]*>', '', body).strip()

if os.path.exists(OUT):
    shutil.rmtree(OUT)
for d in ('img', 'fonts', 'assets', 'files'):
    os.makedirs(OUT + d)

# ---------- images ----------
names = sorted(set(re.findall(r'img/([\w.-]+\.(?:webp|jpg|png|svg))', src)))
VAR, DIM, ren, before, after = {}, {}, {}, 0, 0
for n in names:
    p = D + 'img/' + n
    if not os.path.exists(p):
        print('missing image', n); continue
    before += os.path.getsize(p)
    stem, ext = n.rsplit('.', 1)
    if ext == 'svg':
        t = open(p, encoding='utf8').read()
        t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
        t = re.sub(r'(\d+\.\d{3})\d+', r'\1', t)          # trim coordinate precision
        t = re.sub(r'>\s+<', '><', t).strip()
        open(OUT + 'img/' + n, 'w', encoding='utf8').write(t)
        after += os.path.getsize(OUT + 'img/' + n); continue
    C = D + '.cache/' + str(int(os.path.getmtime(p))) + '-'
    M = C + 'meta-' + stem + '.json'
    if os.path.exists(M):
        meta = json.load(open(M))
        for f in meta['files']:
            shutil.copy(C + f, OUT + 'img/' + f)
        if meta['out'] != n: ren['img/' + n] = 'img/' + meta['out']
        if meta['var']: VAR['img/' + meta['out']] = meta['var']
        DIM['img/' + meta['out']] = meta.get('dim') or list(Image.open(OUT + 'img/' + meta['out']).size)
        after += os.path.getsize(OUT + 'img/' + meta['out']); continue
    im = Image.open(p)
    im.load()
    alpha = im.mode in ('RGBA', 'LA') or 'transparency' in im.info
    im = im.convert('RGBA' if alpha else 'RGB')
    if max(im.size) > 1600:
        im.thumbnail((1600, 1600), Image.LANCZOS)
    q = 82 if ext == 'jpg' else 80
    out = stem + '.webp'
    im.save(OUT + 'img/' + out, 'WEBP', quality=q, method=6)
    if ext == 'webp' and os.path.getsize(OUT + 'img/' + out) > os.path.getsize(p):
        shutil.copy(p, OUT + 'img/' + out)                 # keep the original if re-encoding is no smaller
    if out != n:
        ren['img/' + n] = 'img/' + out
    after += os.path.getsize(OUT + 'img/' + out)
    w = im.size[0]
    DIM['img/' + out] = list(im.size)
    sets = []
    for tw in (400, 800):
        if w > tw * 1.25:
            v = im.resize((tw, round(im.size[1] * tw / w)), Image.LANCZOS)
            vn = f'{stem}-{tw}.webp'
            v.save(OUT + 'img/' + vn, 'WEBP', quality=78, method=6)
            sets.append([f'img/{vn}', tw])
    if sets:
        VAR['img/' + out] = sets + [['img/' + out, w]]
    os.makedirs(D + '.cache', exist_ok=True)
    for f in [out] + [x[0][4:] for x in sets]:
        shutil.copy(OUT + 'img/' + f, C + f)
    json.dump({'out': out, 'files': [out] + [x[0][4:] for x in sets], 'var': VAR.get('img/' + out), 'dim': DIM['img/' + out]}, open(C + 'meta-' + stem + '.json', 'w'))
print(f'images: {len(names)} files, {before/1024/1024:.1f} MB -> {after/1024/1024:.1f} MB (+ small versions)')
for a, b in ren.items():
    js = js.replace(a, b); body = body.replace(a, b); css = css.replace(a, b)

# ---------- fonts ----------
fonts = sorted(set(re.findall(r'url\(fonts/([\w.-]+)\.woff\)', css)))
for f in fonts:
    t = TTFont(D + f'fonts/{f}.woff'); t.flavor = 'woff2'; t.save(OUT + f'fonts/{f}.woff2')
css = re.sub(r"url\(fonts/([\w.-]+)\.woff\) format\('woff'\)", r"url(../fonts/\1.woff2) format('woff2')", css)
css = css.replace('url(img/', 'url(../img/')

# ---------- JS: responsive images ----------
# SS also writes width/height (intrinsic size) so the browser knows each image's shape;
# CSS ':where(img[width][height]){width:auto;height:auto}' keeps the layout as before.
js = js.replace("const SS=(p,z)=>'';",
    "const VAR=" + json.dumps(VAR, separators=(',', ':')) +
    ",DIM=" + json.dumps(DIM, separators=(',', ':')) +
    ";const SS=(p,z)=>{const v=VAR[p],d=DIM[p];return(v?` srcset=\"${v.map(x=>x[0]+' '+x[1]+'w').join(', ')}\" sizes=\"${z||'100vw'}\"`:'')+(d?` width=\"${d[0]}\" height=\"${d[1]}\"`:'')};", 1)

def esb(code, loader):
    cmd = [ESB] if ESB else ['npx', '--yes', 'esbuild']
    r = subprocess.run(cmd + ['--minify', f'--loader={loader}', '--target=es2020'],
                       input=code.encode(), capture_output=True, shell=(os.name == 'nt'))
    if r.returncode:
        sys.exit(r.stderr.decode())
    return r.stdout.decode()

def put(code, ext):
    h = hashlib.sha1(code.encode()).hexdigest()[:8]
    name = f'assets/app.{h}.{ext}'
    open(OUT + name, 'w', encoding='utf8').write(code)
    return name

cssf = put(esb(css, 'css'), 'css')
jsf = put(esb(js, 'js'), 'js')

# ---------- favicon + social image ----------
logo = Image.open(D + 'img/logo.png').convert('RGBA')
icon = logo.crop((0, 0, 640, 257))  # whole drone mark (arms + drop), without the text
def fav(size, pad):
    bg = Image.new('RGBA', (size, size), (246, 183, 11, 255))
    m = Image.new('L', (size, size), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), radius=size // 5, fill=255)
    ic = icon.copy(); ic.thumbnail((size - 2 * pad, size - 2 * pad), Image.LANCZOS)
    bg.alpha_composite(ic, ((size - ic.size[0]) // 2, (size - ic.size[1]) // 2))
    bg.putalpha(m); return bg
fav(32, 2).save(OUT + 'favicon-32.png')
fav(180, 16).convert('RGB').save(OUT + 'apple-touch-icon.png')
fav(512, 44).save(OUT + 'icon-512.png')
og = Image.new('RGB', (1200, 630), (243, 244, 240))
lg = Image.open(D + 'img/logo.png').convert('RGBA'); lg.thumbnail((330, 330), Image.LANCZOS)
og.paste(lg, (90, (630 - lg.size[1]) // 2), lg)
mc = Image.open(D + 'img/ds400.webp').convert('RGBA'); mc.thumbnail((640, 560), Image.LANCZOS)
og.paste(mc, (1200 - mc.size[0] - 70, (630 - mc.size[1]) // 2), mc)
og.save(OUT + 'og-image.jpg', quality=86)

# ---------- copy files ----------
for f in os.listdir(D + 'files'):
    shutil.copy(D + 'files/' + f, OUT + 'files/' + f)

# ---------- config.js (editable on GitHub without rebuilding) ----------
open(OUT + 'config.js', 'w', encoding='utf8').write(f"""/* DroneSpray settings. You can edit this file directly on GitHub. */
window.DS_CONFIG = {{
  /* Google Analytics 4 measurement ID, e.g. "G-AB12CD34EF", or a Tag Manager container "GTM-XXXXXXX". Leave "" to switch analytics and the cookie notice off. */
  gaId: {json.dumps(CFG.get('gaId', ''))},
  /* Where the contact, dealer and newsletter forms are sent (e.g. a Formspree endpoint "https://formspree.io/f/xxxxxxx").
     Leave "" and the forms open the visitor's email app with the message ready, addressed to formEmail. */
  formEndpoint: {json.dumps(CFG.get('formEndpoint', ''))},
  formEmail: {json.dumps(CFG.get('formEmail', 'info@farma.com.gr'))}
}};
""")

# ---------- HTML ----------
desc = 'DroneSpray: συστήματα ανάδευσης και ανεφοδιασμού ψεκαστικού υγρού για γεωργικά drones, 110 έως 600 λίτρων. Κατασκευή FARMA Κυράτσας, Λάρισα.'
title = 'DroneSpray | Pre-mixing systems for agricultural drones'
abs_ = (lambda p: URL + '/' + p) if URL else (lambda p: p)
ld = {"@context": "https://schema.org", "@type": "Organization", "name": "DroneSpray",
      "legalName": "FARMA Κυράτσας Γεωργικά Μηχανήματα Ε.Ε.", "logo": abs_('icon-512.png'),
      "email": "info@farma.com.gr", "telephone": "+30 2410 622500",
      "address": {"@type": "PostalAddress", "streetAddress": "3ο χλμ. Λάρισας – Καρδίτσας",
                  "postalCode": "41500", "addressLocality": "Λάρισα", "addressCountry": "GR"},
      "sameAs": ["https://www.instagram.com/farma_kyratsas_agrimachinery"]}
if URL:
    ld["url"] = URL + '/'
# LCP: the big DS600 of the first hero slide. imagesizes must match hsSz() in src.html.
lcp = VAR.get('img/ds600.webp')
lcppre = (f'<link rel="preload" as="image" href="img/ds600.webp" imagesrcset="{", ".join(f"{a} {b}w" for a, b in lcp)}" '
          f'imagesizes="min(56vw, 392px)" fetchpriority="high">') if lcp else ''
# SEO / GEO: extra head tags with the JSON-LD graph (tools/seo-head.html) and crawlable static
# content shown before the app renders (tools/seo-body.html). {URL} is replaced with the site URL.
def tool_text(name):
    p = D + 'tools/' + name
    return open(p, encoding='utf8').read().replace('{URL}', URL).strip() if os.path.exists(p) else ''
seohead, seobody = tool_text('seo-head.html'), tool_text('seo-body.html')
ldtag = '' if seohead else f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
fontpre = ''.join(f'<link rel="preload" href="fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>'
                  for f in ('InterTight-300', 'Manrope-700', 'Commissioner-400') if f in fonts)
head = f'''<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<base href="/">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f6b70b">
{f'<link rel="canonical" href="{URL}/">' if URL else ''}
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="48x48" href="favicon-48.png">
<link rel="icon" type="image/png" sizes="192x192" href="favicon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DroneSpray">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{abs_('og-image.jpg')}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
{f'<meta property="og:url" content="{URL}/">' if URL else ''}
<meta name="twitter:card" content="summary_large_image">
{seohead}
{fontpre}
{lcppre}
<link rel="stylesheet" href="{cssf}">
<script src="config.js"></script>
<script src="{jsf}" defer></script>
{ldtag}
</head>
<body>
<noscript><p style="padding:24px;font:16px Arial,sans-serif">Η ιστοσελίδα χρειάζεται JavaScript. This website needs JavaScript. Τηλ. 2410 622500 · info@farma.com.gr</p></noscript>
'''
html = head + re.sub(r'\n\s*\n', '\n', body) + '\n</body>\n</html>\n'
html = re.sub(r'>\n\s+<', '>\n<', html)
if seobody:
    html = html.replace('<main id="view"></main>', '<main id="view">' + seobody + '</main>', 1)
open(OUT + 'index.html', 'w', encoding='utf8').write(html)
# 404.html is the app itself: the router reads the path, so /en/ds600/ works even before prerendering.
# Then run tools/prerender.ps1 to write a static page for every language and page.
open(OUT + '404.html', 'w', encoding='utf8').write(html)

# ---------- host files ----------
open(OUT + '.nojekyll', 'w').write('')
open(OUT + 'robots.txt', 'w').write('User-agent: *\nAllow: /\n' + (f'Sitemap: {URL}/sitemap.xml\n' if URL else ''))
if URL:
    today = datetime.date.today().isoformat()
    simg = ['og-image.jpg'] + [f'img/{n}.webp' for n in ('ph6', 'ph7', 'ph8', 'ph9', 'ph1', 'ph3', 'ph4', 'ph5', 'ds600', 'ds500', 'ds420', 'ds400', 'ds300', 'ds200', 'ds200c', 'ds110', 'pm20')]
    simg = ''.join(f'<image:image><image:loc>{URL}/{i}</image:loc></image:image>' for i in simg if os.path.exists(OUT + i))
    open(OUT + 'sitemap.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><url><loc>{URL}/</loc><lastmod>{today}</lastmod>{simg}</url></urlset>\n')
    if tool_text('llms.txt'):
        open(OUT + 'llms.txt', 'w', encoding='utf8').write(tool_text('llms.txt') + '\n')
    host = URL.split('://', 1)[1].split('/')[0]
    if not host.endswith('github.io') and not host.endswith('netlify.app'):
        open(OUT + 'CNAME', 'w').write(host + '\n')
open(OUT + '_headers', 'w').write('''/assets/*
  Cache-Control: public, max-age=31536000, immutable
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/img/*
  Cache-Control: public, max-age=2592000
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
''')
shutil.copy(D + 'tools/README-site.md', OUT + 'README.md')
# Files published as-is at the site root (search engine verification files etc.). Do not delete them.
if os.path.isdir(D + 'tools/static'):
    for f in os.listdir(D + 'tools/static'):
        shutil.copy(D + 'tools/static/' + f, OUT + f)

tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print('css', os.path.getsize(OUT + cssf) // 1024, 'KB  js', os.path.getsize(OUT + jsf) // 1024, 'KB  html',
      os.path.getsize(OUT + 'index.html') // 1024, 'KB  total dist', round(tot / 1024 / 1024, 1), 'MB')
