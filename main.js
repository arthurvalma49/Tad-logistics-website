/* ============================================================
   TAD Logistics — main.js
   - Mobile navigation
   - Mega-menu (desktop hover, mobile tap)
   - Scroll reveal
   - Contact form
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ─── Mobile nav ─────────────────────────────────────── */
  const burger  = document.querySelector('.site-nav__burger');
  const mobileNav = document.querySelector('.mobile-nav');
  const body = document.body;

  if (burger && mobileNav) {
    burger.addEventListener('click', () => {
      const isOpen = burger.classList.toggle('is-open');
      mobileNav.classList.toggle('is-open', isOpen);
      body.style.overflow = isOpen ? 'hidden' : '';
      burger.setAttribute('aria-expanded', String(isOpen));
    });

    // Close on backdrop click
    mobileNav.addEventListener('click', (e) => {
      if (e.target === mobileNav) closeMobileNav();
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeMobileNav();
    });
  }

  function closeMobileNav() {
    burger?.classList.remove('is-open');
    mobileNav?.classList.remove('is-open');
    body.style.overflow = '';
    burger?.setAttribute('aria-expanded', 'false');
  }

  /* ─── Mega-menu ──────────────────────────────────────── */
  const navItems = document.querySelectorAll('.site-nav__item');

  navItems.forEach(item => {
    const link = item.querySelector('.site-nav__link--has-dropdown');
    if (!link) return;

    // Touch devices: toggle on click instead of hover
    link.addEventListener('click', (e) => {
      const isTouchDevice = window.matchMedia('(hover: none)').matches;
      if (isTouchDevice) {
        e.preventDefault();
        const isOpen = item.classList.toggle('is-open');
        // Close others
        navItems.forEach(other => {
          if (other !== item) other.classList.remove('is-open');
        });
      }
    });
  });

  // Close mega-menu on outside click
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.site-nav__item')) {
      navItems.forEach(item => item.classList.remove('is-open'));
    }
  });

  /* ─── Active nav link ────────────────────────────────── */
  const currentPage = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.site-nav__link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && (href === currentPage || (currentPage === '' && href === 'index.html'))) {
      link.classList.add('is-active');
    }
  });

  /* ─── Scroll reveal ──────────────────────────────────── */
  const revealEls = document.querySelectorAll('.reveal');

  if (revealEls.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px',
    });

    revealEls.forEach(el => observer.observe(el));
  }

  /* ─── Contact form ───────────────────────────────────── */
  const form = document.querySelector('.contact-form');
  const successEl = document.querySelector('.form-success');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const btn = form.querySelector('.form-submit');
      btn.textContent = 'Sending…';
      btn.disabled = true;

      // Simulate send (replace with real endpoint)
      setTimeout(() => {
        form.style.display = 'none';
        if (successEl) successEl.classList.add('is-visible');
      }, 900);
    });
  }

  /* ─── Smooth stat counter animation ─────────────────── */
  const statValues = document.querySelectorAll('.stats-bar__value[data-count]');

  if (statValues.length > 0) {
    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || '';
        const duration = 1200;
        const start = performance.now();

        function tick(now) {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          // ease-out-quart
          const eased = 1 - Math.pow(1 - progress, 4);
          el.textContent = Math.round(eased * target) + suffix;
          if (progress < 1) requestAnimationFrame(tick);
        }

        requestAnimationFrame(tick);
        countObserver.unobserve(el);
      });
    }, { threshold: 0.5 });

    statValues.forEach(el => countObserver.observe(el));
  }

});
