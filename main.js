const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Current year in the footer
document.querySelectorAll('.year').forEach((el) => { el.textContent = new Date().getFullYear(); });

// Pause / play buttons
function setPaused(btn, paused) {
  btn.setAttribute('aria-pressed', paused);
  btn.setAttribute('aria-label', paused ? btn.dataset.labelPlay : btn.dataset.labelPause);
}

// Language switch: keep the reading position (and product filter) on the other language's page.
// Positions are stored per section, since Estonian text is longer and pixel offsets would drift.
{
  const KEY = 'tad-lang-scroll';
  // Anchors: page sections, plus any element with an id (product cards, projects…) that exists in both languages
  const blocks = () => [...document.querySelectorAll('main > section, main [id], .site-footer')].filter((b) => b.offsetParent);
  const headerH = () => document.querySelector('.site-header')?.offsetHeight || 0;

  document.querySelectorAll('.lang, .lang-mobile').forEach((a) => a.addEventListener('click', () => {
    const url = new URL(a.href);
    const group = new URLSearchParams(location.search).get('group');
    if (group) { url.searchParams.set('group', group); a.href = url; }
    if (window.scrollY === 0) return;
    const top = headerH();
    // The smallest anchor crossing the top edge of the viewport is the most precise
    const list = blocks();
    const hit = list.filter((b) => { const r = b.getBoundingClientRect(); return r.top <= top && r.bottom > top; })
      .sort((x, y) => x.offsetHeight - y.offsetHeight)[0];
    if (!hit) return;
    const r = hit.getBoundingClientRect();
    try {
      sessionStorage.setItem(KEY, JSON.stringify({ path: url.pathname, id: hit.id || null, idx: list.indexOf(hit), frac: (top - r.top) / r.height }));
    } catch (e) { /* storage unavailable: page opens at the top */ }
  }));

  let saved = null;
  try { saved = JSON.parse(sessionStorage.getItem(KEY)); sessionStorage.removeItem(KEY); } catch (e) { /* ignore */ }
  if (saved && saved.path === location.pathname && !location.hash) {
    if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
    // Wait until the rest of this script has run (e.g. the product filter changes the layout)
    document.addEventListener('DOMContentLoaded', () => {
      const b = (saved.id && document.getElementById(saved.id)) || blocks()[saved.idx];
      if (b) window.scrollTo(0, b.getBoundingClientRect().top + window.scrollY + saved.frac * b.offsetHeight - headerH());
    });
  }
}

// Mobile menu
const burger = document.querySelector('.burger');
const links = document.querySelector('.nav__links');
if (burger && links) {
  const setMenu = (open) => {
    links.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', open);
  };
  burger.addEventListener('click', () => setMenu(!links.classList.contains('is-open')));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && links.classList.contains('is-open')) { setMenu(false); burger.focus(); }
  });
  document.addEventListener('click', (e) => {
    if (links.classList.contains('is-open') && !links.contains(e.target) && !burger.contains(e.target)) setMenu(false);
  });
}

// Hero photo carousel (home)
const hero = document.querySelector('.hero');
if (hero) {
  const slides = [...hero.querySelectorAll('.hero__slide')];
  const bars = hero.querySelector('.hero__bars');
  const pauseBtn = hero.querySelector('.pause');
  const DELAY = 6000;
  let i = 0, timer, paused = reducedMotion;

  bars.innerHTML = slides.map((_, n) => `<button type="button" aria-label="${bars.dataset.label} ${n + 1} / ${slides.length}"></button>`).join('');
  const dots = [...bars.children];

  function schedule() {
    clearTimeout(timer);
    hero.classList.toggle('is-stopped', paused);
    if (!paused) timer = setTimeout(() => show(i + 1), DELAY);
  }
  function show(n) {
    slides[i].classList.remove('is-active');
    dots[i].removeAttribute('aria-current');
    i = (n + slides.length) % slides.length;
    slides[i].classList.add('is-active');
    void dots[i].offsetWidth; // restart the bar fill animation
    dots[i].setAttribute('aria-current', 'true');
    schedule();
  }

  hero.querySelector('.hero__next').addEventListener('click', () => show(i + 1));
  dots.forEach((d, n) => d.addEventListener('click', () => show(n)));
  setPaused(pauseBtn, paused);
  pauseBtn.addEventListener('click', () => {
    paused = !paused;
    setPaused(pauseBtn, paused);
    if (paused) schedule(); else show(i); // resuming gives the current photo a full turn again
  });

  // Swipe on touch screens
  let startX = null;
  hero.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
  hero.addEventListener('touchend', (e) => {
    if (startX === null) return;
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1));
    startX = null;
  });

  show(0);
}

// Inquiry form (contact). No backend yet: opens the visitor's email app with the inquiry filled in.
const form = document.querySelector('#inquiry');
if (form) {
  const fields = [...form.querySelectorAll('[required]')];
  const validate = (f) => {
    const err = document.getElementById(f.getAttribute('aria-describedby'));
    const msg = f.validity.valueMissing ? f.dataset.missing : f.validity.typeMismatch ? f.dataset.invalid : '';
    f.setAttribute('aria-invalid', !!msg);
    err.textContent = msg;
    err.hidden = !msg;
    return !msg;
  };

  // Subject from "Ask for an offer" links (?subject=Latex)
  const preset = new URLSearchParams(location.search).get('subject');
  if (preset) form.querySelector('#subject').value = preset;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const invalid = fields.filter((f) => !validate(f));
    if (invalid.length) { invalid[0].focus(); return; }

    const d = Object.fromEntries(new FormData(form));
    const body = [d.message, '', d.name, d.email].join('\n');
    const subject = (document.documentElement.lang === 'et' ? 'Päring: ' : 'Inquiry: ') + (d.subject.trim() || (document.documentElement.lang === 'et' ? 'Üldine' : 'General'));
    location.href = `mailto:info@tadlogistics.ee?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
  // Errors appear on submit (not on blur, which would shift the button under the cursor) and clear as they are fixed
  fields.forEach((f) => {
    f.addEventListener('input', () => { if (f.getAttribute('aria-invalid') === 'true') validate(f); });
  });
}

// Subject field: preset options, hidden as soon as the visitor types their own
const combo = document.querySelector('.combo');
if (combo) {
  const input = combo.querySelector('input');
  const list = combo.querySelector('.combo__list');
  const options = [...list.children];
  let active = -1;

  function setOpen(open) {
    list.hidden = !open;
    combo.classList.toggle('is-open', open);
    input.setAttribute('aria-expanded', open);
    setActive(-1);
  }
  function setActive(n) {
    options.forEach((o, i) => {
      o.classList.toggle('is-active', i === n);
      o.setAttribute('aria-selected', i === n);
    });
    active = n;
    if (n >= 0) input.setAttribute('aria-activedescendant', options[n].id);
    else input.removeAttribute('aria-activedescendant');
  }
  function choose(o) { input.value = o.textContent; setOpen(false); }
  const openIfEmpty = () => setOpen(input.value === '');

  input.addEventListener('focus', openIfEmpty);
  input.addEventListener('input', openIfEmpty);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      if (list.hidden) setOpen(true);
      const n = options.length;
      setActive(e.key === 'ArrowDown' ? (active + 1) % n : (active - 1 + n) % n);
    } else if (e.key === 'Enter' && !list.hidden && active >= 0) {
      e.preventDefault();
      choose(options[active]);
    } else if (e.key === 'Escape' && !list.hidden) {
      e.stopPropagation();
      setOpen(false);
    }
  });
  const toggle = combo.querySelector('.combo__toggle');
  toggle.addEventListener('mousedown', (e) => e.preventDefault());
  toggle.addEventListener('click', () => {
    const open = list.hidden;
    input.focus();
    setOpen(open);
  });
  list.addEventListener('mousedown', (e) => {
    const o = e.target.closest('li');
    if (o) { e.preventDefault(); choose(o); }
  });
  input.addEventListener('blur', () => setOpen(false));
}

// Maps load only after a click (Google receives data when they load)
document.querySelectorAll('.map').forEach((map) => {
  map.querySelector('button').addEventListener('click', () => {
    const frame = document.createElement('iframe');
    frame.src = map.dataset.src;
    frame.title = map.dataset.title;
    frame.loading = 'lazy';
    map.replaceChildren(frame);
    map.classList.add('is-loaded');
    frame.focus();
  });
});

// Copy buttons next to phone numbers and emails (contact)
const copyGrid = document.querySelector('.contact__grid');
if (copyGrid) {
  const buttons = copyGrid.querySelectorAll('.copy-btn');
  if (!navigator.clipboard) buttons.forEach((b) => { b.hidden = true; });
  const toast = document.querySelector('.copy-toast');
  let hideTimer;
  buttons.forEach((b) => b.addEventListener('click', async () => {
    let ok = true;
    try { await navigator.clipboard.writeText(b.dataset.copy); } catch (e) { ok = false; }
    toast.textContent = ok ? `${copyGrid.dataset.copied}: ${b.dataset.copy}` : copyGrid.dataset.copyFailed;
    toast.classList.add('is-visible');
    buttons.forEach((x) => x.classList.toggle('is-done', ok && x === b));
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
      toast.classList.remove('is-visible');
      buttons.forEach((x) => x.classList.remove('is-done'));
    }, 2000);
  }));
}

// Product group filter, kept in the URL (?group=hardware)
const filters = document.querySelector('.filters');
if (filters) {
  const products = document.querySelectorAll('.product');
  const apply = (group) => {
    const btn = filters.querySelector(`[data-group="${group}"]`) || filters.querySelector('[data-group="all"]');
    filters.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', b === btn));
    products.forEach((p) => { p.hidden = btn.dataset.group !== 'all' && p.dataset.group !== btn.dataset.group; });
    return btn.dataset.group;
  };
  apply(new URLSearchParams(location.search).get('group'));
  filters.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const group = apply(btn.dataset.group);
    const u = new URL(location.href);
    if (group === 'all') u.searchParams.delete('group'); else u.searchParams.set('group', group);
    u.hash = '';
    history.replaceState(null, '', u);
  });
}

// Photo lightbox (production)
const gallery = document.querySelector('.gallery__grid');
if (gallery && window.HTMLDialogElement) {
  const items = [...gallery.querySelectorAll('button')];
  const d = gallery.dataset;
  const box = document.createElement('dialog');
  box.className = 'lightbox';
  box.innerHTML = `<img alt="">
    <button type="button" class="lightbox__btn lightbox__close" aria-label="${d.close}">✕</button>
    <button type="button" class="lightbox__btn lightbox__prev" aria-label="${d.prev}">‹</button>
    <button type="button" class="lightbox__btn lightbox__next" aria-label="${d.next}">›</button>`;
  document.body.append(box);
  const img = box.querySelector('img');
  let cur = 0;
  const open = (n) => {
    cur = (n + items.length) % items.length;
    const src = items[cur].querySelector('img');
    img.src = src.currentSrc || src.src;
    img.alt = src.alt;
    if (!box.open) box.showModal();
  };
  items.forEach((b, n) => b.addEventListener('click', () => open(n)));
  box.querySelector('.lightbox__close').addEventListener('click', () => box.close());
  box.querySelector('.lightbox__prev').addEventListener('click', () => open(cur - 1));
  box.querySelector('.lightbox__next').addEventListener('click', () => open(cur + 1));
  box.addEventListener('click', (e) => { if (e.target === box) box.close(); });
  box.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') open(cur + 1);
    if (e.key === 'ArrowLeft') open(cur - 1);
  });
}
