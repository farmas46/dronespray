# DroneSpray website

Static, multilingual catalogue site for DroneSpray pre-mixing systems for agricultural drones. The maker is FARMA Κυράτσας, Larissa. The owner talks in Greek; answer in Greek.

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

- Hash routing:
  - `#home`, `#products`
  - model ids: `ds600 ds500 ds420 ds400 ds300 ds200 ds200c ds110 pm20`
  - `#accessories`, `#acc-<id>`
  - `#dealers`, `#network`, `#contact`, `#privacy`
  - `render()` builds `#view`; `chrome()` builds the nav, mega menu and footer.
- Languages `el en es it fr de`:
  - Main text: `T[lang]`.
  - Other per-language objects: `PZ` (model tiles, `nw` = "New" label, `na` = "Temporarily unavailable"), `NLT` (newsletter), `NEWST`, `GALT`, `PRIV`, `CATT`, `ACCX`, `PT` (production texts: forms, cookie banner), `HX`, `HWT`, `PRIVL`, `CO.addr`/`CO.hours`, `ACC[].name`, `NEWS[]`.
  - German (`de`) lives in one block (`T.de=…`, `PZ.de=…`, …) just before `for(const l in PT)`; `PRIV` exists in el, en and de; es/it/fr fall back to English.
  - **Every text change must be made in all 6 languages.**
  - Company name: `coName()` gives the Greek name on `el`, "FARMA KYRATSAS AGRICULTURAL MACHINERY" on every other language.
- Model data:
  - `IMG`, `GAL` (extra photos), `NAME`, `FULL`, `CAPS`, `PZK` (filter keys), `SPEC`.
  - `SPEC` holds capacity and dimensions in cm and kg. Missing `SPEC` means the page shows "data coming soon".
  - Model order arrays appear in several places: search `'ds420','ds400','ds300'`.
  - The comparison uses `M` and `SH` in `cmpTable`.
  - New-model badge: `NEWM=['ds400']`.
- Accessories: `ACC` array.
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
- Wording the owner chose:
  - «μάνικα 3/4"» (not λάστιχο)
  - «φιαλών σκευασμάτων»
  - «Σύστημα διάσπασης για σκόνες»
  - «Ψηφιακός μετρητής ροής»
  - «Μοντέλα» (not Προϊόντα)
  - © line: «© DRONESPRAY | PRE-MIXING SYSTEMS»

## Open items

- Missing data:
  - DS110 dimensions and weight.
  - DS200 Cone outlets (3 or 4).
  - Warranty text.
- Site settings:
  - Domain: goes in `tools/site.json` → `url`.
  - GA4 measurement ID.
  - Formspree endpoint.
- Hosting plan: private GitHub repo + Netlify (publish directory `dist`), or a public repo with GitHub Pages.
