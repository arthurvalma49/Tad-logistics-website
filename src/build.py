"""Builds the static site.

Usage (from the project root):  python src/build.py

Reads page bodies from src/pages/<lang>/<page>.html, wraps them in the shared
layout (head, header, footer) and writes the finished HTML files to the project
root (English) and et/ (Estonian). Edit the files in src/, not the generated HTML.
"""
import html
import json
import re
import struct
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
from content import GROUPS, PAGES, PARTNERS, PRODUCTS, SITE, STRINGS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
YEAR = date.today().year
esc = html.escape


def url(lang, key):
    path = '/' + PAGES[lang][key]
    return path[:-len('index.html')] if path.endswith('index.html') else path


def other(lang):
    return 'et' if lang == 'en' else 'en'


# ── Page metadata ────────────────────────────────────────────
META = {
    'en': {
        'home': ('TAD Logistics | Materials for soft furniture manufacturers',
                 'TAD Logistics supplies materials and accessories to soft furniture manufacturers, produces beds on a project basis and delivers across Estonia. Rummu, Estonia, since 2005.',
                 'hero-warehouse.jpg'),
        'trading': ('Products | TAD Logistics',
                    'Nonwoven fabric, Fibertex, latex, polyester fibre and wadding, duck feathers, steel wire, bed legs, zippers and other materials for soft furniture and bed manufacturers.',
                    'kiudkangas.jpg'),
        'production': ('Production | TAD Logistics',
                       'Project-based production of beds, headboards, top mattresses, mattress covers, pillows, duvets and bed legs in Rummu, Estonia. Most production is exported to Scandinavia.',
                       'prod-3.jpg'),
        'contact': ('Contact | TAD Logistics',
                    'Contact TAD Logistics sales and purchasing. Production and logistics centre in Rummu, office in Assaku, Estonia.',
                    'truck.jpg'),
        'privacy': ('Privacy notice | TAD Logistics',
                    'How TAD Logistics OÜ handles personal data sent through this website.', 'hero-warehouse.jpg'),
    },
    'et': {
        'home': ('TAD Logistics | Materjalid ja tarvikud pehme mööbli tootjatele',
                 'TAD Logistics varustab pehmemööblitootjaid materjalide ja tarvikutega, toodab voodeid projektipõhiselt ja pakub transporti. Rummu, alates 2005.',
                 'hero-warehouse.jpg'),
        'trading': ('Tooted | TAD Logistics',
                    'Kiudkangas, Fibertex, latex, polüesterkiud ja vatiin, pardisuled, terasest traat, voodijalad, lukud ja muud materjalid pehme mööbli ja voodite tootjatele.',
                    'kiudkangas.jpg'),
        'production': ('Tootmine | TAD Logistics',
                       'Voodite, voodiotste, kattemadratsite, madratsikatete, patjade, tekkide ja voodijalgade projektipõhine tootmine Rummus. Enamus toodangust eksporditakse Skandinaaviasse.',
                       'prod-3.jpg'),
        'contact': ('Kontakt | TAD Logistics',
                    'TAD Logistics müügi- ja ostukontaktid. Tootmis- ja logistikakeskus Rummus, kontor Assakus.',
                    'truck.jpg'),
        'privacy': ('Privaatsusteade | TAD Logistics',
                    'Kuidas TAD Logistics OÜ selle veebilehe kaudu saadetud isikuandmeid käsitleb.', 'hero-warehouse.jpg'),
    },
}

JSON_LD = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    'name': 'TAD Logistics OÜ',
    'url': SITE + '/',
    'logo': SITE + '/assets/logo.png',
    'foundingDate': '2005',
    'email': 'info@tadlogistics.ee',
    'telephone': '+372 5340 0308',
    'address': {'@type': 'PostalAddress', 'streetAddress': 'Haapsalu mnt 12A', 'addressLocality': 'Rummu',
                'postalCode': '76102', 'addressRegion': 'Harjumaa', 'addressCountry': 'EE'},
    'location': [
        {'@type': 'Place', 'name': 'Production and logistics centre',
         'address': {'@type': 'PostalAddress', 'streetAddress': 'Haapsalu mnt 12A', 'addressLocality': 'Rummu',
                     'postalCode': '76102', 'addressRegion': 'Harjumaa', 'addressCountry': 'EE'}},
        {'@type': 'Place', 'name': 'Office',
         'address': {'@type': 'PostalAddress', 'streetAddress': 'Graniidi tee 19', 'addressLocality': 'Assaku',
                     'postalCode': '75310', 'addressRegion': 'Harjumaa', 'addressCountry': 'EE'}},
    ],
}


# ── Layout parts ─────────────────────────────────────────────
def head(lang, key):
    title, desc, og_img = META[lang][key]
    canon = SITE + url(lang, key)
    alt = SITE + url(other(lang), key)
    en_url = SITE + url('en', key)
    ld = ''
    if key == 'home':
        ld = '\n  <script type="application/ld+json">' + json.dumps(JSON_LD, ensure_ascii=False) + '</script>'
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{canon}">
  <link rel="alternate" hreflang="{lang}" href="{canon}">
  <link rel="alternate" hreflang="{other(lang)}" href="{alt}">
  <link rel="alternate" hreflang="x-default" href="{en_url}">
  <link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="TAD Logistics">
  <meta property="og:locale" content="{'en_GB' if lang == 'en' else 'et_EE'}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{SITE}/assets/og/{og_img}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preload" href="/assets/fonts/hanken-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/style.css">{ld}
</head>
<body>
'''


def header(lang, key):
    s = STRINGS[lang]
    links = '\n'.join(
        f'      <a href="{url(lang, k)}"{" aria-current=\"page\"" if k == key else ""}>{esc(label)}</a>'
        for k, label in s['nav'].items())
    o = other(lang)
    switch = f'href="{url(o, key)}" lang="{o}" hreflang="{o}"'
    return f'''<a class="skip" href="#main">{s["skip"]}</a>

<header class="site-header">
  <div class="wrap nav">
    <a class="nav__logo" href="{url(lang, "home")}" aria-label="{s["home_label"]}"><img src="/assets/logo.png" alt="TAD Logistics" width="164" height="110"></a>
    <nav class="nav__links" id="nav-links" aria-label="{s["nav_label"]}">
{links}
      <a class="lang-mobile" {switch}>{s["other_lang"]}</a>
    </nav>
    <a class="lang" {switch}>{s["other_lang"]}</a>
    <button class="burger" aria-label="{s["menu"]}" aria-expanded="false" aria-controls="nav-links"><span></span><span></span><span></span></button>
  </div>
</header>
'''


def footer(lang):
    s = STRINGS[lang]
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div><img src="/assets/logo.png" alt="TAD Logistics" width="164" height="110"></div>
      <div>
        <h2>{s["addresses"]}</h2>
        <p class="row"><span class="role">{s["production_site"]}</span><span class="v"><span>Haapsalu mnt 12A, Rummu, Vasalemma vald, 76102 Harjumaa</span></span></p>
        <p class="row"><span class="role">{s["office"]}</span><span class="v"><span>Graniidi tee 19, 75310 Assaku</span></span></p>
      </div>
      <div>
        <h2>{s["contact"]}</h2>
        <p class="row"><span class="role">{s["sales"]}</span><span class="v"><span class="name">Taavi Tavaste</span><a href="tel:+37253400308">+372 5340 0308</a><span class="sep" aria-hidden="true">·</span><a href="mailto:taavi@tadlogistics.ee">taavi@tadlogistics.ee</a></span></p>
        <p class="row"><span class="role">{s["purchasing"]}</span><span class="v"><span class="name">Tanel Kimalane</span><a href="tel:+37256985363">+372 5698 5363</a><span class="sep" aria-hidden="true">·</span><a href="mailto:tanel@tadlogistics.ee">tanel@tadlogistics.ee</a></span></p>
        <p class="row"><span class="role">{s["general"]}</span><span class="v"><a href="mailto:info@tadlogistics.ee">info@tadlogistics.ee</a></span></p>
      </div>
    </div>
    <div class="copy"><span>© <span class="year">{YEAR}</span> TAD Logistics OÜ</span><span class="sep" aria-hidden="true">·</span><a href="{url(lang, "privacy")}">{s["privacy"]}</a></div>
  </div>
</footer>

<script src="/main.js"></script>
</body>
</html>
'''


# ── Generated blocks ─────────────────────────────────────────
def partners():
    imgs = lambda hidden: '\n'.join(
        f'          <img{f" class=\"{c}\"" if c else ""} src="/assets/partners/{f}" alt="{"" if hidden else esc(n)}">'
        for f, n, c in PARTNERS)
    return f'''<div class="marquee__set">
{imgs(False)}
        </div>
        <div class="marquee__set" aria-hidden="true">
{imgs(True)}
        </div>'''


def products(lang):
    s = STRINGS[lang]
    groups = GROUPS[lang]
    counts = {g: sum(1 for p in PRODUCTS if p[1] == g) for g in groups}
    btns = [f'        <button type="button" aria-pressed="true" data-group="all">{s["group_all"]} ({len(PRODUCTS)})</button>']
    btns += [f'        <button type="button" aria-pressed="false" data-group="{g}">{esc(n)} ({counts[g]})</button>'
             for g, n in groups.items()]
    cards = []
    for pid, g, img, t in PRODUCTS:
        name, specs = t[lang]
        # "Weight: 14–120 g/m²" becomes a label/value row; lines without a label span the full row
        def row(x):
            if ': ' in x:
                k, v = x.split(': ', 1)
                v = v[:1].upper() + v[1:]
                return f'<li><span class="spec__k">{esc(k)}</span><span class="spec__v">{esc(v)}</span></li>'
            return f'<li class="spec--plain"><span class="spec__v">{esc(x)}</span></li>'
        lis = ''.join(row(x) for x in specs)
        ask = f'{url(lang, "contact")}?subject={quote(name)}#inquiry'
        cards.append(f'''        <article class="product" id="{pid}" data-group="{g}">
          <div class="product__img"><img src="/assets/img/{img}.webp" alt="{esc(name)}" loading="lazy"></div>
          <div class="product__body">
            <p class="product__group">{esc(groups[g])}</p>
            <h2>{esc(name)}</h2>
            <ul class="specs">{lis}</ul>
            <a class="product__ask" href="{esc(ask)}">{s["ask"]}<span class="sr-only">: {esc(name)}</span> <span aria-hidden="true">→</span></a>
          </div>
        </article>''')
    return f'''<div class="filters" role="group" aria-label="{"Filter by group" if lang == "en" else "Filtreeri rühma järgi"}">
{chr(10).join(btns)}
      </div>
      <div class="product-grid">
{chr(10).join(cards)}
      </div>'''


# ── Image dimensions (width/height attributes prevent layout shift) ──
def image_size(path):
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', data[16:24])
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        chunk = data[12:16]
        if chunk == b'VP8 ':
            w, h = struct.unpack('<HH', data[26:30])
            return w & 0x3fff, h & 0x3fff
        if chunk == b'VP8L':
            b = data[21:25]
            return 1 + (((b[1] & 0x3f) << 8) | b[0]), 1 + (((b[3] & 0xf) << 10) | (b[2] << 2) | ((b[1] & 0xc0) >> 6))
        if chunk == b'VP8X':
            return 1 + int.from_bytes(data[24:27], 'little'), 1 + int.from_bytes(data[27:30], 'little')
    if data[:2] == b'\xff\xd8':
        i = 2
        while i < len(data):
            marker, size = data[i + 1], struct.unpack('>H', data[i + 2:i + 4])[0]
            if 0xc0 <= marker <= 0xcf and marker not in (0xc4, 0xc8, 0xcc):
                h, w = struct.unpack('>HH', data[i + 5:i + 9])
                return w, h
            i += 2 + size
    raise ValueError(f'Unknown image format: {path}')


def add_image_sizes(page):
    def fix(m):
        tag = m.group(0)
        if ' width=' in tag:
            return tag
        src = re.search(r'src="(/assets/[^"]+)"', tag)
        if not src:
            return tag
        w, h = image_size(ROOT / src.group(1).lstrip('/'))
        return tag[:-1] + f' width="{w}" height="{h}">'
    return re.sub(r'<img\b[^>]*>', fix, page)


# ── Build ────────────────────────────────────────────────────
def build():
    written = []
    for lang in PAGES:
        for key, out in PAGES[lang].items():
            body = (SRC / 'pages' / lang / f'{key}.html').read_text(encoding='utf-8')
            body = body.replace('<!--@partners-->', partners()).replace('<!--@products-->', products(lang))
            for k in PAGES[lang]:
                body = body.replace('{{' + k + '}}', url(lang, k))
            page = head(lang, key) + '\n' + header(lang, key) + '\n<main id="main">\n' + body.strip('\n') + '\n</main>\n\n' + footer(lang)
            page = add_image_sizes(page)
            target = ROOT / out
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(page, encoding='utf-8', newline='\n')
            written.append(out)
    notfound = (SRC / 'pages' / '404.html').read_text(encoding='utf-8')
    (ROOT / '404.html').write_text(add_image_sizes(notfound.replace('{{year}}', str(YEAR))), encoding='utf-8', newline='\n')
    written.append('404.html')

    urls = [(SITE + url(lang, k), k) for lang in PAGES for k in PAGES[lang]]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for lang in PAGES:
        for k in PAGES[lang]:
            sitemap.append(f'  <url>\n    <loc>{SITE + url(lang, k)}</loc>\n    <lastmod>{date.today().isoformat()}</lastmod>')
            for l2 in PAGES:
                sitemap.append(f'    <xhtml:link rel="alternate" hreflang="{l2}" href="{SITE + url(l2, k)}"/>')
            sitemap.append('  </url>')
    sitemap.append('</urlset>\n')
    (ROOT / 'sitemap.xml').write_text('\n'.join(sitemap), encoding='utf-8', newline='\n')
    print('Built:', ', '.join(written), f'+ sitemap.xml ({len(urls)} URLs)')


if __name__ == '__main__':
    build()
