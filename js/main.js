document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initCtaBand();
  initHeader();
  initMobileNav();
  initQuoteCarousel();
  initScrollAnimations();
  initSiteForms();
  initLanguageSwitcher().catch(err => console.warn('Language init failed:', err));
});

function initHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 50);
  });
}

function initMobileNav() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav-mobile');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', () => {
    toggle.classList.toggle('active');
    nav.classList.toggle('open');
    document.body.classList.toggle('nav-open', nav.classList.contains('open'));
  });

  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      toggle.classList.remove('active');
      nav.classList.remove('open');
      document.body.classList.remove('nav-open');
    });
  });

  document.addEventListener('click', e => {
    if (!nav.classList.contains('open')) return;
    if (e.target.closest('.site-header')) return;
    toggle.classList.remove('active');
    nav.classList.remove('open');
    document.body.classList.remove('nav-open');
  });
}

function initQuoteCarousel() {
  const slides = document.querySelectorAll('.quote-slide');
  const dots = document.querySelectorAll('.quote-dot');
  if (!slides.length) return;

  let current = 0;
  let interval;

  function showSlide(index) {
    slides.forEach(s => s.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));
    slides[index].classList.add('active');
    if (dots[index]) dots[index].classList.add('active');
    current = index;
  }

  function nextSlide() {
    showSlide((current + 1) % slides.length);
  }

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      showSlide(i);
      resetInterval();
    });
  });

  function resetInterval() {
    clearInterval(interval);
    interval = setInterval(nextSlide, 6000);
  }

  showSlide(0);
  resetInterval();
}

function initScrollAnimations() {
  const elements = document.querySelectorAll('.fade-in');
  if (!elements.length) return;

  const reveal = el => el.classList.add('visible');

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) reveal(entry.target);
      });
    },
    { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
  );

  elements.forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight * 0.92 && rect.bottom > 0) {
      reveal(el);
    } else {
      observer.observe(el);
    }
  });
}

function submitFormFeedback(btn, i18nKey) {
  if (!btn) return;
  const lang = localStorage.getItem('lang') || 'en';
  const originalText = t(i18nKey, lang) || btn.textContent;
  btn.textContent = t('ui.messageSent', lang) || 'Message Sent';
  btn.style.background = 'var(--gold-dark)';
  btn.style.borderColor = 'var(--gold-dark)';
  setTimeout(() => {
    btn.textContent = originalText;
    btn.style.background = '';
    btn.style.borderColor = '';
  }, 3000);
}
