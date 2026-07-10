const LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇺🇸', dir: 'ltr' },
  { code: 'es', name: 'Español', flag: '🇪🇸', dir: 'ltr' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪', dir: 'ltr' },
  { code: 'fr', name: 'Français', flag: '🇫🇷', dir: 'ltr' },
  { code: 'ru', name: 'Русский', flag: '🇷🇺', dir: 'ltr' },
  { code: 'uk', name: 'Українська', flag: '🇺🇦', dir: 'ltr' },
  { code: 'zh', name: '中文', flag: '🇨🇳', dir: 'ltr' },
  { code: 'ar', name: 'العربية', flag: '🇸🇦', dir: 'rtl' },
  { code: 'he', name: 'עברית', flag: '🇮🇱', dir: 'rtl' }
];

function t(key, lang) {
  const parts = key.split('.');
  let node = TRANSLATIONS[lang] || TRANSLATIONS.en;
  for (const p of parts) {
    node = node?.[p];
    if (node === undefined) break;
  }
  if (node === undefined && lang !== 'en') {
    node = TRANSLATIONS.en;
    for (const p of parts) node = node?.[p];
  }
  return typeof node === 'string' ? node : null;
}

function getPageId() {
  return document.body.dataset.page || 'home';
}

function getInitialLang() {
  const params = new URLSearchParams(window.location.search);
  const fromUrl = params.get('lang');
  if (fromUrl && LANGUAGES.some(l => l.code === fromUrl)) {
    localStorage.setItem('lang', fromUrl);
    return fromUrl;
  }
  return localStorage.getItem('lang') || 'en';
}

async function setLang(lang) {
  await ensureLangs('en', lang);
  localStorage.setItem('lang', lang);
  applyTranslations(lang);
  const url = new URL(window.location.href);
  if (lang === 'en') url.searchParams.delete('lang');
  else url.searchParams.set('lang', lang);
  history.replaceState(null, '', url);
}

function applyTranslations(lang) {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const val = t(el.dataset.i18n, lang);
    if (val) {
      el.textContent = val;
      if (val.includes('\n')) el.style.whiteSpace = 'pre-line';
    }
  });

  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const val = t(el.dataset.i18nHtml, lang);
    if (val) el.innerHTML = val;
  });

  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const val = t(el.dataset.i18nPlaceholder, lang);
    if (val) el.placeholder = val;
  });

  document.querySelectorAll('[data-i18n-aria]').forEach(el => {
    const val = t(el.dataset.i18nAria, lang);
    if (val) el.setAttribute('aria-label', val);
  });

  document.querySelectorAll('[data-i18n-alt]').forEach(el => {
    const val = t(el.dataset.i18nAlt, lang);
    if (val) el.alt = val;
  });

  document.querySelectorAll('select option[data-i18n]').forEach(el => {
    const val = t(el.dataset.i18n, lang);
    if (val) el.textContent = val;
  });

  const page = getPageId();
  const title = t(`meta.${page}.title`, lang);
  const desc = t(`meta.${page}.description`, lang);
  if (title) document.title = title;
  if (desc) {
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.content = desc;
  }

  const langMeta = LANGUAGES.find(l => l.code === lang) || LANGUAGES[0];
  document.documentElement.lang = lang;
  document.documentElement.dir = langMeta.dir;

  const flagEl = document.querySelector('.lang-trigger .lang-flag');
  if (flagEl) flagEl.textContent = langMeta.flag;

  document.querySelectorAll('.lang-option').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
}

async function initLanguageSwitcher() {
  const switcher = document.querySelector('.lang-switcher');
  if (!switcher) return;

  const trigger = switcher.querySelector('.lang-trigger');
  const panel = switcher.querySelector('.lang-panel');
  if (!panel) return;

  panel.innerHTML = LANGUAGES.map(lang => `
    <li>
      <button type="button" class="lang-option" data-lang="${lang.code}" role="option">
        <span class="lang-option-flag">${lang.flag}</span>
        <span class="lang-option-name">${lang.name}</span>
      </button>
    </li>
  `).join('');

  const saved = getInitialLang();
  try {
    await ensureLangs('en', saved);
  } catch (err) {
    console.warn('Language pack load failed:', err);
  }
  applyTranslations(saved);

  trigger.addEventListener('click', e => {
    e.stopPropagation();
    switcher.classList.toggle('open');
  });

  panel.addEventListener('click', async e => {
    const btn = e.target.closest('.lang-option');
    if (!btn) return;
    await setLang(btn.dataset.lang);
    switcher.classList.remove('open');
  });

  document.addEventListener('click', () => switcher.classList.remove('open'));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') switcher.classList.remove('open');
  });
}
