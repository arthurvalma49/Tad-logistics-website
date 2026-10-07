"""Site content shared by all pages: UI strings, navigation, products.

All product data comes from the product pages of the old tadlogistics.ee (2016).
"""

SITE = 'https://tadlogistics.ee'

# Page keys -> file name per language
PAGES = {
    'en': {'home': 'index.html', 'trading': 'trading.html', 'production': 'production.html',
           'contact': 'contact.html', 'privacy': 'privacy.html'},
    'et': {'home': 'et/index.html', 'trading': 'et/tooted.html', 'production': 'et/tootmine.html',
           'contact': 'et/kontakt.html', 'privacy': 'et/privaatsus.html'},
}

STRINGS = {
    'en': {
        'skip': 'Skip to content',
        'home_label': 'TAD Logistics home',
        'nav_label': 'Main',
        'menu': 'Menu',
        'nav': {'trading': 'Products', 'production': 'Production', 'contact': 'Contact'},
        'other_lang': 'Eesti', 'other_lang_code': 'et',
        'addresses': 'Addresses', 'contact': 'Contact',
        'production_site': 'Production', 'office': 'Office',
        'sales': 'Sales', 'purchasing': 'Purchasing', 'general': 'General',
        'privacy': 'Privacy notice',
        'ask': 'Ask for an offer',
        'group_all': 'All',
    },
    'et': {
        'skip': 'Liigu sisu juurde',
        'home_label': 'TAD Logistics avaleht',
        'nav_label': 'Peamenüü',
        'menu': 'Menüü',
        'nav': {'trading': 'Tooted', 'production': 'Tootmine', 'contact': 'Kontakt'},
        'other_lang': 'English', 'other_lang_code': 'en',
        'addresses': 'Aadressid', 'contact': 'Kontakt',
        'production_site': 'Tootmine', 'office': 'Kontor',
        'sales': 'Müük', 'purchasing': 'Ost', 'general': 'Üldine',
        'privacy': 'Privaatsusteade',
        'ask': 'Küsi pakkumist',
        'group_all': 'Kõik',
    },
}

GROUPS = {
    'en': {'fabrics': 'Fabrics', 'filling': 'Filling & foam', 'hardware': 'Hardware',
           'accessories': 'Packaging & accessories'},
    'et': {'fabrics': 'Kangad', 'filling': 'Täidised ja poroloon', 'hardware': 'Furnituur',
           'accessories': 'Pakend ja tarvikud'},
}

# id, group, image, {lang: (name, [specs])}
PRODUCTS = [
    ('nonwoven-fabric', 'fabrics', 'kiudkangas', {
        'en': ('Nonwoven fabric (PP spunbond)', ['Colours: black and white from stock, other colours on order', 'Weight: 14–120 g/m²', 'Widths: 31–280 cm']),
        'et': ('Kiudkangas', ['Värvus: must ja valge laokaubana, värvilised eritellimusena', 'Tihedus: 14–120 g/m²', 'Laiused: 31–280 cm'])}),
    ('fibertex', 'fabrics', 'fibertex', {
        'en': ('Fibertex', ['Needle-punched material', 'Colour: brown', 'Weight: 100 g/m²', 'Width: 160 cm']),
        'et': ('Fibertex', ['Nõeltöödeldud materjal', 'Värvus: pruun', 'Tihedus: 100 g/m²', 'Laius: 160 cm'])}),
    ('down-proof-fabric', 'fabrics', 'sulekangas', {
        'en': ('Down-proof fabric', ['135 g/m², 100% cotton', '150 g/m², 57% cotton / 43% polyester']),
        'et': ('Sulekangas', ['135 g/m², 100% puuvill (sulekindel)', '150 g/m², 57% puuvill / 43% polüester (sulekindel)'])}),
    ('leather', 'fabrics', 'nahk', {
        'en': ('Leather', ['TEXAS black 100, 138 cm', 'TEXAS brown 110, 138 cm', 'Torello black 201']),
        'et': ('Nahk', ['TEXAS must 100, 138 cm', 'TEXAS pruun 110, 138 cm', 'Torello must 201'])}),
    ('polyester-fiber', 'filling', 'poluester-kiud', {
        'en': ('Polyester fibre', ['7D/32 mm HCS, A-grade, virgin', '7D/64 mm HCS, A-grade, virgin', 'Bale weight: 271 kg']),
        'et': ('Polüesterkiud', ['7D/32 mm HCS, A-grade, virgin', '7D/64 mm HCS, A-grade, virgin', 'Paki kaal: 271 kg'])}),
    ('polyester-wadding', 'filling', 'mahuline-vatiin', {
        'en': ('Polyester wadding', ['Weight: 50–500 g/m²', 'Various sizes available']),
        'et': ('Mahuline vatiin', ['Tihedus: 50–500 g/m²', 'Saadaval erinevad mõõdud'])}),
    ('latex', 'filling', 'latex', {
        'en': ('Latex', ['Sheets 90–1100 × 200–210 cm, 3–5 cm thick', 'Talalay natural 100% N5, 79–179 × 199 × 4.5 cm', 'Talalay natural 100% N7, 89–104 × 199 × 3 cm']),
        'et': ('Latex', ['Lehed 90–1100 × 200–210 cm, paksus 3–5 cm', 'Talalay naturaalne 100% N5, 79–179 × 199 × 4,5 cm', 'Talalay naturaalne 100% N7, 89–104 × 199 × 3 cm'])}),
    ('laminated-foam', 'filling', 'lamineeritud-poroloon', {
        'en': ('Laminated foam', ['3 mm / 160 cm, white', '5 mm / 160 cm', '5 mm / 160 cm, black + black', '5 mm / 160 cm, black + white']),
        'et': ('Lamineeritud poroloon', ['3 mm / 160 cm, valge', '5 mm / 160 cm', '5 mm / 160 cm, must + must', '5 mm / 160 cm, must + valge'])}),
    ('duck-feathers', 'filling', 'pardisuled', {
        'en': ('Duck feathers', ['White, 10% down + 90% feathers, 2–3 cm', 'White, 10% down + 90% feathers, 4–6 cm', 'Bag weight: 50 kg']),
        'et': ('Pardisuled', ['Valge, 10% + 90%, 2–3 cm', 'Valge, 10% + 90%, 4–6 cm', 'Paki kaal: 50 kg'])}),
    ('motors', 'hardware', 'mootorid-ja-puldid', {
        'en': ('Motors and remote controls', ['Motor Okimat IPS 6000N', 'Remote control Smartline 1.87']),
        'et': ('Mootorid ja puldid', ['Mootor Okimat IPS 6000N', 'Pult Smartline 1.87'])}),
    ('metal-connectors', 'hardware', 'metallist-kinnitused', {
        'en': ('Metal fasteners', ['Fastening brackets for sofas', 'HF-001, HF-002, HF-012, HF-012A, HF-012A-S, HF-012B', 'Zamac bracket']),
        'et': ('Metallist kinnitused', ['Kinnitusklambrid diivanitele', 'HF-001, HF-002, HF-012, HF-012A, HF-012A-S, HF-012B', 'Kinnitusklamber Zamac'])}),
    ('steel-wire', 'hardware', 'terasest-traat', {
        'en': ('Steel wire', ['For pocket and bonnell springs', 'Diameter: 1.8 mm and 2.0 mm', 'Roll weight: 750 kg']),
        'et': ('Terasest traat', ['Pocket- ja bonnell-vedrude valmistamiseks', 'Läbimõõt: 1,8 mm ja 2,0 mm', 'Kaal: 750 kg/rull'])}),
    ('legs', 'hardware', 'jalad', {
        'en': ('Bed legs', ['Champagne, 12 cm and 19 cm, M8, aluminium', 'Cylinder, 12 cm and 19 cm, M8, aluminium']),
        'et': ('Jalad', ['Voodijala kompl. Champagne, 12 cm ja 19 cm, M8, alumiinium', 'Voodijala kompl. silinder, 12 cm ja 19 cm, M8, alumiinium'])}),
    ('plastic-washers', 'hardware', 'plastikust-seibid', {
        'en': ('Plastic washers', ['40 × 2.0, white']),
        'et': ('Plastikust seibid', ['40 × 2,0, valge'])}),
    ('zippers', 'accessories', 'meetrilukud-ja-lukukelgud', {
        'en': ('Zippers by the metre and sliders', ['Sizes: 4 mm and 6 mm', 'Colours: white, black, grey, beige']),
        'et': ('Meetrilukud ja lukukelgud', ['Mõõdud: 4 mm ja 6 mm', 'Värvid: valge, must, hall, beež'])}),
    ('corrugated-cardboard', 'accessories', 'lainepapp', {
        'en': ('Corrugated cardboard rolls', ['Widths: 0.3, 0.5, 0.75, 1, 1.2, 1.6 and 2 m', 'Length: 75 m (1 m width also 100 m)']),
        'et': ('Lainepapp', ['Laiused: 0,3; 0,5; 0,75; 1; 1,2; 1,6 ja 2 m', 'Pikkus: 75 m (1 m laiusega ka 100 m)'])}),
    ('cushioning-film', 'accessories', 'pehmenduskile', {
        'en': ('Cushioning film', ['1200 × 300 × 0.8 mm', '600 × 300 × 0.8 mm']),
        'et': ('Pehmenduskile', ['1200 × 300 × 0,8 mm', '600 × 300 × 0,8 mm'])}),
]

PARTNERS = [
    ('kungsangen.webp', 'Kungsängen', 'wide'),
    ('hilding-baltic.webp', 'Hilding Baltic', ''),
    ('hastens.webp', 'Hästens', ''),
    ('bellus.webp', 'Bellus', 'inv'),
    ('wendre.webp', 'Wendre', 'tall'),
]
