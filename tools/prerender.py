"""Prerender every page of the built site (dist/) into static HTML, one folder per language and page.

Mac / Linux version of tools/prerender.ps1 (same pages, same output), using headless Google Chrome.
  dist/index.html (Greek home), dist/ds600/index.html, dist/en/index.html, dist/en/ds600/index.html, ...
Also writes dist/sitemap.xml with every page and its language versions.

Run after tools/prod.py:   python3 tools/prerender.py
Keep LANGS and VIEWS in step with tools/prerender.ps1 and the router block in src.html.
"""
import datetime, functools, http.server, os, re, shutil, subprocess, sys, tempfile, threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
SITE = 'https://www.dronespray-premixingsystems.com'
PORT = 8137
LANGS = ['el', 'en', 'es', 'it', 'fr', 'de', 'ro']
VIEWS = ['home', 'ds600', 'ds500', 'ds420', 'ds400', 'ds300', 'ds200', 'ds200c', 'ds110', 'pm20',
         'accessories', 'dealers', 'network', 'contact', 'privacy', 'why'] + ['acc-' + a for a in (
         'pm2637', 'pm2545', 'pm2540', 'fm1', 'pdr', 'reel', 'panel', 'led', 'nozzle', 'lidmix', 'dpump',
         'bracket', 'wsp', 'lid', 'herbkit', 'pnozzle', 'rinse', 'fillkit', 'doccase', 'tankwash')]


def path_of(v, l):
    return ('' if l == 'el' else '/' + l) + ('' if v == 'home' else '/' + v) + '/'


def find_chrome():
    for c in (os.environ.get('CHROME'),
              '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
              '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
              '/Applications/Chromium.app/Contents/MacOS/Chromium',
              shutil.which('google-chrome'), shutil.which('chromium'), shutil.which('chromium-browser')):
        if c and os.path.exists(c):
            return c
    sys.exit('Google Chrome not found (set CHROME=/path/to/chrome)')


# The app template every page starts from (kept as 404.html so unknown URLs still load the app).
tpl = open(os.path.join(DIST, 'index.html'), encoding='utf-8').read()
if '<base href="/">' not in tpl:
    sys.exit('dist/index.html needs <base href="/"> in <head>')
open(os.path.join(DIST, '404.html'), 'w', encoding='utf-8').write(tpl)


class Handler(http.server.SimpleHTTPRequestHandler):
    """Real files as they are; pages (paths ending in "/") and unknown paths get the current template."""
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
                      '.css': 'text/css; charset=utf-8', '.webp': 'image/webp', '.woff2': 'font/woff2'}

    def translate_path(self, path):
        rel = path.split('?', 1)[0].split('#', 1)[0]
        f = super().translate_path(rel)
        if rel.endswith('/') or not os.path.isfile(f):
            return os.path.join(DIST, '404.html')
        return f

    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(Handler, directory=DIST))
threading.Thread(target=srv.serve_forever, daemon=True).start()

chrome = find_chrome()
out = tempfile.mkdtemp(prefix='prerender-')
prof = tempfile.mkdtemp(prefix='prerender-chrome-')
done, failed = 0, []
try:
    for l in LANGS:
        for v in VIEWS:
            p = path_of(v, l)
            r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-first-run', '--log-level=3',
                                f'--user-data-dir={prof}', '--virtual-time-budget=2500', '--dump-dom',
                                f'http://localhost:{PORT}{p}?prerender'],
                               capture_output=True, timeout=120)
            html = r.stdout.decode('utf-8', 'replace')
            if not re.search(r'<main id="view">\s*<', html) or 'rel="canonical"' not in html:
                failed.append(p)
                continue
            d = os.path.join(out, p.strip('/'))
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write('<!doctype html>\n' + html.strip() + '\n')
            done += 1
            print(f'\r{done} pages', end='', flush=True)
finally:
    srv.shutdown()
    shutil.rmtree(prof, ignore_errors=True)
print()
if failed:
    shutil.rmtree(out, ignore_errors=True)
    sys.exit('Prerender failed for: ' + ', '.join(failed) + ' (nothing was copied)')
shutil.copytree(out, DIST, dirs_exist_ok=True)
shutil.rmtree(out, ignore_errors=True)

# Sitemap: every page, with its language versions.
today = datetime.date.today().isoformat()
sb = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n']
for v in VIEWS:
    for l in LANGS:
        sb.append(f'<url><loc>{SITE}{path_of(v, l)}</loc><lastmod>{today}</lastmod>')
        sb += [f'<xhtml:link rel="alternate" hreflang="{a}" href="{SITE}{path_of(v, a)}"/>' for a in LANGS]
        sb.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{path_of(v, "en")}"/></url>\n')
sb.append('</urlset>\n')
open(os.path.join(DIST, 'sitemap.xml'), 'w', encoding='utf-8').write(''.join(sb))
print(f'Prerendered {done} pages; sitemap has {len(VIEWS) * len(LANGS)} URLs.')
