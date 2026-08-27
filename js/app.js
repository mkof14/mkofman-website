const SITE_CONFIG = {
  url: 'https://mkofman.com',
  email: 'mkofman@mkofman.com',
  /**
   * Formspree endpoint — set FORMSPREE_ENDPOINT in Vercel or .env locally.
   * Example: https://formspree.io/f/xyzabcde
   * Leave empty to use mailto: fallback.
   */
  formspreeEndpoint: '',
  /**
   * Calendly scheduling URL — set CALENDLY_URL in Vercel or .env.
   * Example: https://calendly.com/your-name/intro
   */
  calendlyUrl: '',
  ogImage: '/images/portrait-hero.webp',
  /**
   * Analytics — set ANALYTICS_PROVIDER=plausible|ga4 in Vercel or .env.
   */
  analytics: {
    provider: '',
    plausibleDomain: 'mkofman.com',
    ga4Id: '',
  },
};


/* === forms.js === */
function getFormStrings(lang) {
  return {
    sending: t('ui.sending', lang) || 'Sending…',
    sent: t('ui.messageSent', lang) || 'Message Sent',
    error: t('ui.formError', lang) || 'Could not send. Please email directly.',
    send: t('ui.sendMessage', lang) || 'Send Message',
  };
}

function buildMailtoLink(form) {
  const email = SITE_CONFIG.email;
  const data = new FormData(form);
  const subject = data.get('subject')
    || data.get('topic')
    || data.get('_subject')
    || `Website inquiry from ${data.get('firstName') || ''} ${data.get('lastName') || ''}`.trim()
    || 'Website inquiry';
  const lines = [];
  if (data.get('firstName') || data.get('lastName')) {
    lines.push(`Name: ${[data.get('firstName'), data.get('lastName')].filter(Boolean).join(' ')}`);
  }
  if (data.get('email')) lines.push(`Email: ${data.get('email')}`);
  if (data.get('company')) lines.push(`Company: ${data.get('company')}`);
  if (data.get('topic')) lines.push(`Topic: ${data.get('topic')}`);
  lines.push('');
  lines.push(String(data.get('message') || '').trim());
  const body = lines.join('\n');
  return `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

function ensureFormspreeFields(form) {
  const endpoint = SITE_CONFIG.formspreeEndpoint;
  if (!endpoint) return false;

  form.action = endpoint;
  form.method = 'POST';

  if (!form.querySelector('input[name="_replyto"]')) {
    const reply = document.createElement('input');
    reply.type = 'hidden';
    reply.name = '_replyto';
    form.appendChild(reply);
  }

  if (!form.querySelector('input[name="_subject"]')) {
    const subj = document.createElement('input');
    subj.type = 'hidden';
    subj.name = '_subject';
    subj.value = 'Michael Kofman website inquiry';
    form.appendChild(subj);
  }

  if (!form.querySelector('input[name="_gotcha"]')) {
    const honeypot = document.createElement('input');
    honeypot.type = 'text';
    honeypot.name = '_gotcha';
    honeypot.tabIndex = -1;
    honeypot.autocomplete = 'off';
    honeypot.setAttribute('aria-hidden', 'true');
    honeypot.style.cssText = 'position:absolute;left:-9999px;height:0;width:0;opacity:0;';
    form.appendChild(honeypot);
  }

  const emailField = form.querySelector('[name="email"]');
  const replyField = form.querySelector('[name="_replyto"]');
  if (emailField && replyField) {
    const syncReply = () => { replyField.value = emailField.value || ''; };
    emailField.addEventListener('input', syncReply);
    syncReply();
  }

  return true;
}

async function submitSiteForm(form, button) {
  const lang = localStorage.getItem('lang') || 'en';
  const strings = getFormStrings(lang);
  const endpoint = SITE_CONFIG.formspreeEndpoint;
  const usesFormspree = Boolean(endpoint);

  if (button) {
    button.disabled = true;
    button.dataset.originalText = button.textContent;
    button.textContent = strings.sending;
  }

  try {
    if (usesFormspree) {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' },
      });
      if (!response.ok) throw new Error('formspree failed');
      return true;
    }

    window.location.href = buildMailtoLink(form);
    return true;
  } catch {
    if (usesFormspree) {
      window.location.href = buildMailtoLink(form);
      return true;
    }
    if (button) {
      button.textContent = strings.error;
      setTimeout(() => {
        button.disabled = false;
        button.textContent = button.dataset.originalText || strings.send;
      }, 3500);
    }
    return false;
  } finally {
    if (button && usesFormspree) {
      button.disabled = false;
      button.textContent = button.dataset.originalText || strings.send;
    }
  }
}

function showFormSuccess(wrapper) {
  if (!wrapper) return;
  wrapper.classList.add('success');
  setTimeout(() => wrapper.classList.remove('success'), 5000);
}

function initSiteForms() {
  document.querySelectorAll('.contact-form form, .footer-form form, .insights-connect-form form').forEach(form => {
    if (form.dataset.bound === 'true') return;
    form.dataset.bound = 'true';

    const usesFormspree = ensureFormspreeFields(form);

    form.addEventListener('submit', async e => {
      e.preventDefault();
      const button = form.querySelector('button[type="submit"]');
      const wrapper = form.closest('.footer-form, .insights-connect-form, .contact-form');
      const ok = await submitSiteForm(form, button);

      if (ok && usesFormspree) {
        if (wrapper) showFormSuccess(wrapper);
        else submitFormFeedback(button, 'ui.sendMessage');
        form.reset();
        const replyField = form.querySelector('[name="_replyto"]');
        if (replyField) replyField.value = '';
      }
    });
  });
}

/* === cta.js === */
function initCtaBand() {
  if (document.body.classList.contains('page-home') || document.querySelector('.site-cta-band')) return;

  const footer = document.querySelector('.site-footer');
  if (!footer) return;

  const band = document.createElement('section');
  band.className = 'section section-cta-band site-cta-band';
  band.innerHTML = `
    <div class="container">
      <div class="cta-band-inner fade-in visible">
        <div class="cta-band-text">
          <span class="eyebrow" data-i18n="cta.eyebrow">Work Together</span>
          <h2 data-i18n="cta.title">Request Advisory or a Speaking Engagement</h2>
          <p class="lead" data-i18n="cta.lead">For advisory roles, board positions, speaking engagements, and strategic partnerships.</p>
        </div>
        <a href="contact.html" class="hero-cta" data-i18n="cta.button">Get in Touch</a>
      </div>
    </div>
  `;

  footer.parentNode.insertBefore(band, footer);

  const lang = localStorage.getItem('lang') || 'en';
  band.querySelectorAll('[data-i18n]').forEach(el => {
    const val = t(el.dataset.i18n, lang);
    if (val) el.textContent = val;
  });
}

/* === analytics.js === */
function initAnalytics() {
  const cfg = SITE_CONFIG.analytics;
  if (!cfg || !cfg.provider) return;

  if (cfg.provider === 'plausible' && cfg.plausibleDomain) {
    const s = document.createElement('script');
    s.defer = true;
    s.dataset.domain = cfg.plausibleDomain;
    s.src = 'https://plausible.io/js/script.js';
    document.head.appendChild(s);
    return;
  }

  if (cfg.provider === 'ga4' && cfg.ga4Id) {
    const g = document.createElement('script');
    g.async = true;
    g.src = `https://www.googletagmanager.com/gtag/js?id=${cfg.ga4Id}`;
    document.head.appendChild(g);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function gtag() { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', cfg.ga4Id, { anonymize_ip: true });
  }
}

document.addEventListener('DOMContentLoaded', initAnalytics);

/* === features.js === */
/** Career filters, Calendly embed, inquiry deep-links */
(function () {
  function initCareerFilters() {
    const bar = document.querySelector('.filter-bar[data-filter-target]');
    if (!bar) return;
    const targetSel = bar.dataset.filterTarget;
    const items = document.querySelectorAll(targetSel);
    if (!items.length) return;

    bar.addEventListener('click', (e) => {
      const btn = e.target.closest('.filter-btn');
      if (!btn) return;
      const filter = btn.dataset.filter || 'all';
      bar.querySelectorAll('.filter-btn').forEach((b) => {
        b.classList.toggle('is-active', b === btn);
      });
      items.forEach((item) => {
        const tags = (item.dataset.tags || '').split(/\s+/);
        const show = filter === 'all' || tags.includes(filter);
        item.classList.toggle('is-hidden', !show);
      });
    });
  }

  function initCalendly() {
    const slot = document.getElementById('calendly-embed');
    if (!slot || typeof SITE_CONFIG === 'undefined') return;
    const url = SITE_CONFIG.calendlyUrl;
    if (!url) {
      slot.innerHTML =
        '<div class="calendly-placeholder"><p data-i18n="contact.calendlyPlaceholder">Schedule a brief introductory call — booking link available on request via contact form.</p><p><a href="contact.html" class="text-link" data-i18n="contact.calendlyCta">Request a meeting →</a></p></div>';
      return;
    }
    const script = document.createElement('script');
    script.src = 'https://assets.calendly.com/assets/external/widget.js';
    script.async = true;
    script.onload = () => {
      if (window.Calendly) {
        window.Calendly.initInlineWidget({
          url,
          parentElement: slot,
          resize: true,
        });
      }
    };
    document.head.appendChild(script);
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://assets.calendly.com/assets/external/widget.css';
    document.head.appendChild(link);
  }

  function initInquiryFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const topic = params.get('topic');
    const select = document.getElementById('inquiryType');
    if (!topic || !select) return;
    const map = {
      board: 'Advisory',
      speaking: 'Speaking',
      press: 'Press',
      partnership: 'Partnership',
    };
    const val = map[topic.toLowerCase()] || topic;
    for (const opt of select.options) {
      if (opt.value === val) {
        select.value = val;
        break;
      }
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    initCareerFilters();
    initCalendly();
    initInquiryFromUrl();
  });
})();

/* === main.js === */
document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  try {
    await initLanguageSwitcher();
  } catch (err) {
    console.warn('Language init failed:', err);
  }
  initCtaBand();
  initHeader();
  initMobileNav();
  initQuoteCarousel();
  initScrollAnimations();
  initSiteForms();
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
