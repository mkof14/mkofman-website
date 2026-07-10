const SEO_LANGS = ['en', 'es', 'de', 'fr', 'ru', 'uk', 'zh', 'ar', 'he'];

function pagePathForSeo() {
  const path = window.location.pathname.replace(/^\//, '');
  if (!path || path === 'index.html') return '';
  return path;
}

function buildPageUrl(lang) {
  const base = SITE_CONFIG.url.replace(/\/$/, '');
  const path = pagePathForSeo();
  const url = new URL(path ? `${base}/${path}` : `${base}/`);
  if (lang && lang !== 'en') url.searchParams.set('lang', lang);
  return url.toString();
}

function upsertLink(rel, extra = {}) {
  const { hreflang } = extra;
  let el = hreflang
    ? document.head.querySelector(`link[rel="${rel}"][hreflang="${hreflang}"]`)
    : document.head.querySelector(`link[rel="${rel}"]:not([hreflang])`);
  if (!el) {
    el = document.createElement('link');
    el.rel = rel;
    if (hreflang) el.hreflang = hreflang;
    document.head.appendChild(el);
  }
  return el;
}

function initSeo() {
  const lang = localStorage.getItem('lang') || 'en';
  upsertLink('canonical').href = buildPageUrl(lang).replace(/\?lang=en(?:&|$)/, '').replace(/\?$/, '');

  SEO_LANGS.forEach(code => {
    upsertLink('alternate', { hreflang: code }).href = buildPageUrl(code);
  });

  upsertLink('alternate', { hreflang: 'x-default' }).href = buildPageUrl('en');
}

function updateSeoOnLangChange(lang) {
  const link = document.querySelector('link[rel="canonical"]');
  if (link) {
    link.href = buildPageUrl(lang).replace(/\?lang=en(?:&|$)/, '').replace(/\?$/, '');
  }
}
