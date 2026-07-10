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
