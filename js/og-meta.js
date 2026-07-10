function initOgMeta() {
  const title = document.title;
  const desc = document.querySelector('meta[name="description"]')?.content || '';
  const url = SITE_CONFIG.url.replace(/\/$/, '') + window.location.pathname.replace(/index\.html$/, '');
  const image = SITE_CONFIG.url.replace(/\/$/, '') + SITE_CONFIG.ogImage;

  const tags = [
    ['property', 'og:type', 'website'],
    ['property', 'og:title', title],
    ['property', 'og:description', desc],
    ['property', 'og:url', url],
    ['property', 'og:image', image],
    ['name', 'twitter:card', 'summary_large_image'],
    ['name', 'twitter:title', title],
    ['name', 'twitter:description', desc],
    ['name', 'twitter:image', image],
  ];

  tags.forEach(([attr, key, value]) => {
    if (!value) return;
    let el = document.head.querySelector(`meta[${attr}="${key}"]`);
    if (!el) {
      el = document.createElement('meta');
      el.setAttribute(attr, key);
      document.head.appendChild(el);
    }
    el.setAttribute('content', value);
  });
}
