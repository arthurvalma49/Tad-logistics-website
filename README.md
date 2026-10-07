# TAD Logistics website

Static site, plain HTML, CSS and JavaScript, deployed as-is on Vercel. English at `/`, Estonian at `/et/`.

## Editing

The HTML pages are **generated**. Edit the sources in `src/`, then run:

```
python src/build.py
```

| Source | What it holds |
|---|---|
| `src/build.py` | Layout (head, header, footer), page titles/descriptions, sitemap generation |
| `src/content.py` | UI strings for both languages, the 17 products with specs, partner logos |
| `src/pages/en/*.html`, `src/pages/et/*.html` | Body of each page |
| `src/pages/404.html` | Bilingual 404 page |

The build also adds `width`/`height` to every image automatically. Python 3.12+, no packages needed.

## Other files

- `style.css`: all styles (fonts are self-hosted in `assets/fonts/`)
- `main.js`: menu, hero carousel, partner strip, inquiry form, subject dropdown, click-to-load maps, product filter, photo lightbox
- `vercel.json`: redirects from the old WordPress URLs, security headers, caching
- `.vercelignore`: keeps `src/` and project notes out of the deployment
- `assets/og/`: JPEG images used for link previews

## Preview locally

```
python -m http.server 8000
```

then open http://localhost:8000. (Redirects and security headers only apply on Vercel.)
