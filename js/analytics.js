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
