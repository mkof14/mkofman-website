function initTheme() {
  const toggle = document.querySelector('.theme-toggle');
  if (!toggle) return;

  const saved = localStorage.getItem('theme') || 'dark';
  setTheme(saved, false);

  toggle.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(next, true);
  });
}

function setTheme(theme, save) {
  document.documentElement.dataset.theme = theme;
  if (save) localStorage.setItem('theme', theme);
}

function initThemeEarly() {
  const theme = localStorage.getItem('theme') || 'dark';
  document.documentElement.dataset.theme = theme;
  const lang = localStorage.getItem('lang') || 'en';
  document.documentElement.lang = lang;
  const rtl = lang === 'ar' || lang === 'he';
  document.documentElement.dir = rtl ? 'rtl' : 'ltr';
}
