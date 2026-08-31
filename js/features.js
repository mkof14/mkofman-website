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
    // initCalendly disabled
    initInquiryFromUrl();
  });
})();
