const TRANSLATIONS = {};
const LANG_FILES = ["en", "es", "de", "fr", "ru", "uk", "zh", "ar", "he"];

function deepMerge(target, source) {
  if (!source) return target;
  for (const key of Object.keys(source)) {
    const val = source[key];
    if (val && typeof val === 'object' && !Array.isArray(val)) {
      if (!target[key] || typeof target[key] !== 'object') target[key] = {};
      deepMerge(target[key], val);
    } else {
      target[key] = val;
    }
  }
  return target;
}

const langLoadPromises = {};

function loadLangFile(lang) {
  if (TRANSLATIONS[lang]) return Promise.resolve(TRANSLATIONS[lang]);
  if (langLoadPromises[lang]) return langLoadPromises[lang];
  langLoadPromises[lang] = new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = `/js/langs/${lang}.js?v=2`;
    script.onload = () => {
      const data = window[`__LANG_${lang}`];
      if (data) TRANSLATIONS[lang] = data;
      resolve(TRANSLATIONS[lang]);
    };
    script.onerror = reject;
    document.head.appendChild(script);
  });
  return langLoadPromises[lang];
}

async function ensureLangs(...langs) {
  const unique = [...new Set(langs.filter(Boolean))];
  await Promise.all(unique.map(loadLangFile));
}

function mergePageContent() {}
