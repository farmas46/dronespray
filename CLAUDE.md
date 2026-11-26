# DroneSpray website

Static, multilingual catalogue site for DroneSpray pre-mixing systems for agricultural drones. The maker is FARMA Κυράτσας, Larissa. The owner talks in Greek; answer in Greek.

## Working with the owner (read first, every session, every computer)

- Address the owner as **KING**. Answer in Greek.
- The owner works from more than one computer and more than one Claude conversation. GitHub (`farmas46/dronespray`, branch `main`) is the only shared copy, so:
  - **Before any change:** `git pull` (or fetch and compare with `origin/main`). Never start from an old local copy.
  - **After every change the owner asks for:** commit and push right away, so the other computer sees it.
  - If the push is rejected because GitHub has newer commits: pull them first; never force-push and never overwrite the other work. Ask the owner if the two changes overlap.
- Every text change goes into **all site languages** (currently el, en, es, it, fr, de, ro).
- Bigger visual changes: show a **preview first** (2–3 options when it is a design choice) and push only after the owner approves.
- On Windows with a long folder path, set `git config core.longpaths true` or fetch/push fails with "Filename too long".

## Layout

- `src.html`: the whole site, one file. **Always edit this file.** It has one `<style>` block, the static header/footer markup and one `<script>` block.
- `img/`: product photos (transparent WebP), logos (SVG).
- `fonts/`: self-hosted WOFF (Manrope, Inter Tight, Commissioner), Greek + Latin subset.
- `files/DroneSpray-Catalogue-2026.pdf`: catalogue offered for download.
- `tools/prod.py`: **production build** → `dist/`. This is what goes online (GitHub / Netlify).
  - Re-encodes images to WebP with 400/800 px versions for `srcset`.
  - Converts fonts to WOFF2.
  - Minifies CSS/JS with esbuild into hashed `assets/` files.
  - Writes `config.js`, favicon, og-image, robots, sitemap, CNAME, `_headers`, `.nojekyll`.
  - Settings come from `tools/site.json` (`url`, `gaId`, `formEndpoint`, `formEmail`).
  - Image results are cached in `.cache/`.
- SEO / GEO files, read by `prod.py` (`{URL}` = `site.json` url):
  - `tools/seo-head.html`: robots, og:locale, geo tags, JSON-LD graph (LocalBusiness, Brand, WebSite, WebPage for the home page, ItemList of the 9 model pages). Update it when models or contact details change.
    - The model list is plain `ListItem`s (name + url). **Do not use `"@type":"Product"`**: without a price, review or rating Google reports every one as an invalid "Product snippet" (27 errors in Search Console, removed 2026-11-21).
    - Google result icon and thumbnail: `favicon-48.png`, `favicon-192.png`, `favicon.ico` and `logo-square.jpg` (yellow square with the DroneSpray logo, the owner's choice) live in `tools/static/`. `logo-square.jpg` is the business/brand logo and the home page's `primaryImageOfPage`. `og-image.jpg` (wide, logo + machine) stays for social links.
  - `tools/seo-body.html`: crawlable static content inside `<main id="view">` for crawlers without JavaScript; the app replaces it on load.
  - `tools/llms.txt`: English summary for AI assistants, published at `/llms.txt`.
  - `prod.py` also writes an image sitemap.
- `tools/build.py`: single-file preview build → `index.html`, with images and fonts embedded as base64. Used for the claude.ai artifact preview only.
- `tools/privacy.py`: privacy policy text (EL/EN). After editing it, regenerate the `const PRIV=...;` line in `src.html` from `privacy.js()`.

Requirements:
- Python 3 with `pip install pillow fonttools brotli`.
- Node.js, for `npx esbuild`.

Build:

```
python tools/prod.py
```

Optionally also run `python tools/build.py`.

## How the app works (inside the script in src.html)

- Real URLs (router block just before `render(false);ckInit();`):
  - Greek at the root: `/`, `/ds600/`, `/contact/`; other languages under a prefix: `/en/`, `/de/ds600/`, `/it/acc-reel/`.
  - views: `home`, model ids `ds600 ds500 ds420 ds400 ds300 ds200 ds200c ds110 pm20`, `accessories`, `acc-<id>`, `why`, `dealers`, `network`, `contact`, `privacy`. `products` is the home page scrolled to `#products`.
  - `why` = "Why DroneSpray" page (menu link after Accessories): `whyPage()`, texts in `WHY[lang]` (all 7 languages), icons in `WHYI`. Owner's text, approved 2026-11-24. Do not call the piping "hydraulic" (υδραυλικές): the machines have no hydraulic system.
  - Templates still write `href="#ds600"`; `fixLinks()` turns them into real paths after every render and marks them `data-r`. Old `#ds600` links still work.
  - `seoHead()` sets title, description, canonical, og tags and hreflang (x-default = English) per page. `SITE` holds the live URL.
  - Google titles and descriptions come from `SEOT[lang]` (home title `home`, home description `hd`, model title `m(cap)`, prefix `pre` before each model's intro, accessories title `acc`). They use the words people search: «σταθμός ανάδευσης», «ανεφοδιασμός» (el), "pre-mixing/refill station" (en), "estación de premezcla", "stazione di premiscelazione", "station de prémélange", "Mischstation", "stație de premixare". The visible page texts (h1 etc.) are separate and unchanged. Owner-approved 2026-11-23.
  - `<base href="/">` in the head keeps relative asset paths working in sub-folders.
  - `render()` builds `#view`; `chrome()` builds the nav, mega menu and footer.
- Static pages: after a build, run `powershell -File tools\prerender.ps1` on Windows, or `python3 tools/prerender.py` on Mac (uses Google Chrome; keep its `LANGS`/`VIEWS` lists in step with the .ps1). It serves `dist/` locally, opens every page × language in headless Edge, saves `dist/<lang>/<view>/index.html`, copies the template to `404.html` and writes the full sitemap with hreflang. New views or languages must be added to the lists in the router block, `prerender.ps1` and `prerender.py`.
- Languages `el en es it fr de ro`:
  - Main text: `T[lang]`.
  - Other per-language objects: `PZ` (model tiles, `nw` = "New" label, `na` = "Temporarily unavailable"), `NLT` (newsletter), `NEWST`, `GALT`, `PRIV`, `CATT`, `ACCX`, `PT` (production texts: forms, cookie banner), `HX`, `HWT`, `PRIVL`, `CO.addr`/`CO.hours`, `ACC[].name`, `NEWS[]`.
  - German (`de`) and Romanian (`ro`) each live in one block (`T.de=…`, `T.ro=…`, `PZ.ro=…`, …) just before `for(const l in PT)`; `PRIV` exists in el, en, de and ro; es/it/fr fall back to English.
  - Romanian letters ă ș ț are not in the main font files: `fonts/*-ro.woff` hold just those glyphs, loaded with `unicode-range`.
  - **Every text change must be made in all 7 languages.**
  - Company name: `coName()` gives the Greek name on `el`, "FARMA KYRATSAS AGRICULTURAL MACHINERY" on every other language.
- Model data:
  - `IMG`, `GAL` (extra photos), `NAME`, `FULL`, `CAPS`, `PZK` (filter keys), `SPEC`.
  - `SPEC` holds capacity and dimensions in cm and kg. Missing `SPEC` means the page shows "data coming soon".
  - Model order arrays appear in several places: search `'ds420','ds400','ds300'`.
  - The comparison uses `M` and `SH` in `cmpTable`.
  - New-model badge: `NEWM=['ds400']`.
- Accessories: `ACC` array.
- Spray calculator on the home page, below the models (owner's approved design, 2026-11-19: dark card, sliders, brand tabs, yellow model card with a slanted dark panel, tappable model bars).
  - `calcSec()` builds it, `calcRun()` (called in `render()`) fills it; state in `CS`; clicks and inputs handled by delegated listeners.
  - Area × dose → total mix, drone refills, drone fill time (drone tank ÷ model flow; 80 L/min is the real field flow, DS110 19 L/min).
  - Recommends the smallest DS that holds the whole job in one fill, else DS600; DS110 only for drones with tanks up to 30 L. The bars of all models can be tapped to choose another one.
  - The quote button opens the contact form with the model selected and the calculation in the message (`form.msg`).
  - Greek uses στρέμματα and L/στρέμμα; the other languages use ha and L/ha. Texts in `CALCT` (all 7 languages).
  - `CALCM`: DS models (tank, flow, weight, alternative with the same tank). `CALCD`: DJI / EAVision / XAG spray-tank volumes from the makers' official spec pages (ag.dji.com, xa.com, eavision.com), checked Nov 2026. No maker photos (copyright).
- Videos on the home page, after the models (`vidSec()`, owner-approved 2026-11-24): vertical videos in a row (`.vid-car`, swipe or arrows like the gallery; side by side with the arrows hidden when they all fit), titles under each, one «DS600 →» button. `VIDS` lists them: `files/dronespray-field.mp4` «Παράδοση DS600 στο οινοποιείο La Tour Melas» `files/ds600-presentation.mp4` «Παρουσίαση DS600» `files/dealer-spain-opening.mp4` «Στιγμιότυπα από τα εγκαίνια του dealer μας στην Ισπανία» and `files/deserve2fly-platform.mp4` «Κατασκευή αποσπώμενης πλατφόρμας … DS300 … DESERVE2FLY» (37 s, encoded at 2.3 Mbit/s), `files/ds400-new-model.mp4` «Νέο μοντέλο – DS400» (37 s, 2.3 Mbit/s), `files/ds420-cone-new-model.mp4` «Νέο μοντέλο – DS420 Cone Series», `files/paldron-palencia.mp4` «PALDRON | Παλένθια, Ισπανία», posters in `img/`. Titles in `VIDT[lang]` (`h` … `h7`, eyebrow `ve`; all 7 languages). 720×1280 H.264, a few MB, **no sound** (the owner wants none). They play muted in a loop only while on screen (`vidRun()`, called in `render()`). A yellow ▶ on each opens it in the `#vbox` window (`vopen()`), from the start, with controls and prev/next, so visitors can watch it whole. Video titles (under each video and in the window) are Inter Tight 600, normal case — the owner's choice 2026-11-24 over Manrope capitals. New videos: re-encode the same way (on the Mac: `swift ~/.local/video-tools/compress.swift <in> <out.mp4> 720 1280 2300000`, drops the sound) and add them to `VIDS` and `VIDT`.
- `SS(path, sizes)` adds `srcset`. It is empty in src and filled by `prod.py`. Every new `<img>` template should use `${SS(x,'sizes')}`, plus `loading="lazy"` when below the fold.
- Production block, near the end of the script:
  - `window.DS_CONFIG` (from `config.js`).
  - Cookie consent: GA4 loads only after "Αποδοχή"; localStorage key `ds-consent`.
  - `track()` and `pageView()` on hashchange.
  - `sendForm()`: POSTs JSON to `formEndpoint` (Formspree-compatible), or falls back to `mailto:`.

## Owner's style decisions (keep them)

- Yellow `#f6b70b` buttons. Rounded corners on buttons, fields and boxes. Lists use line style with a yellow dot.
- Model names in Inter Tight light, CLAAS-like.
- Slogan "Engineered for drone spraying" in lowercase.
- Language switcher is plain text `ΕΛ | EN | ES | IT | FR` with a yellow underline.
- Every machine's specs show CE | UKCA.
- Do not add "how it works" sections or hero stats; the owner removed them as clutter.
- Home top (approved 2026-11-23, after several rejected tries: text bullets, a centered layout): title left in Manrope 800 capitals, 2 lines; the short `HX[lang].lead` line under it on screens ≥1100 px; under the buttons the CE | UKCA marks (`.hb-cert`, drawn as inline SVG + text, not an image). On mobile only the marks are added, centred.
- Wording the owner chose:
  - «μάνικα 3/4"» (not λάστιχο)
  - «φιαλών σκευασμάτων»
  - «Σύστημα διάσπασης για σκόνες»
  - «Ψηφιακός μετρητής ροής»
  - «Μοντέλα» (not Προϊόντα)
  - © line: «© DRONESPRAY | PRE-MIXING SYSTEMS»

## Open items

- Warranty: 1 year; delivery usually 3–4 weeks depending on availability (`WD` in src.html, side box on model pages).
- Missing data:
  - DS110 dimensions and weight.
  - DS200 Cone outlets (3 or 4).
- Site settings:
  - Domain: goes in `tools/site.json` → `url`.
  - GA4 measurement ID.
  - Formspree endpoint.
- Hosting: public repo `farmas46/dronespray` on GitHub Pages (`.github/workflows/pages.yml` publishes `dist/`), domain www.dronespray-premixingsystems.com.
  - Keep upload and deploy as **two separate jobs** (upload-pages-artifact@v5, then deploy-pages@v5 with `needs: upload`). In one job deploy-pages often fails with "No artifacts named github-pages were found" (GitHub race, Nov 2026); re-running does not help.
