#!/usr/bin/env python3
"""Build static SEO blocks, patch HTML, split i18n, optimize assets."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://mkofman.com"
LANGS = ["en", "es", "de", "fr", "ru", "uk", "zh", "ar", "he"]

PAGES = [
    ("index.html", "home", ""),
    ("about.html", "about", "about.html"),
    ("ventures.html", "ventures", "ventures.html"),
    ("career.html", "career", "career.html"),
    ("recognition.html", "recognition", "recognition.html"),
    ("contact.html", "contact", "contact.html"),
    ("consulting.html", "consulting", "consulting.html"),
    ("insights.html", "insights", "insights.html"),
    ("speaking.html", "speaking", "speaking.html"),
    ("case-studies.html", "caseStudies", "case-studies.html"),
    ("media-kit.html", "mediaKit", "media-kit.html"),
    ("article-data-infrastructure.html", "article1", "article-data-infrastructure.html"),
    ("article-precision-medicine.html", "article2", "article-precision-medicine.html"),
    ("privacy.html", "privacy", "privacy.html"),
]

OG_IMAGE = f"{SITE_URL}/images/portrait-hero.webp"


def load_meta() -> dict:
    raw = (ROOT / "js" / "translations.js").read_text(encoding="utf-8")
    start, end = raw.find("{"), raw.rfind("}")
    data = json.loads(raw[start : end + 1])
    return {lang: data[lang].get("meta", {}) for lang in data}


def page_url(path: str, lang: str | None = None) -> str:
    base = SITE_URL if not path else f"{SITE_URL}/{path}"
    if lang and lang != "en":
        sep = "&" if "?" in base else "?"
        return f"{base}{sep}lang={lang}"
    return base


def seo_block(page_key: str, path: str, meta_en: dict) -> str:
    m = meta_en.get(page_key, {})
    title = m.get("title", "Michael Kofman")
    desc = m.get("description", "")
    canonical = page_url(path)

    lines = [
        f'  <link rel="canonical" href="{canonical}">',
    ]
    for lang in LANGS:
        lines.append(
            f'  <link rel="alternate" hreflang="{lang}" href="{page_url(path, lang)}">'
        )
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{page_url(path, "en")}">')
    lines.extend([
        f'  <meta property="og:type" content="website">',
        f'  <meta property="og:site_name" content="Michael Kofman">',
        f'  <meta property="og:title" content="{title}">',
        f'  <meta property="og:description" content="{desc}">',
        f'  <meta property="og:url" content="{canonical}">',
        f'  <meta property="og:image" content="{OG_IMAGE}">',
        f'  <meta name="twitter:card" content="summary_large_image">',
        f'  <meta name="twitter:title" content="{title}">',
        f'  <meta name="twitter:description" content="{desc}">',
        f'  <meta name="twitter:image" content="{OG_IMAGE}">',
    ])
    return "\n".join(lines)


def json_ld_block(page_key: str, path: str, meta_en: dict) -> str:
    m = meta_en.get(page_key, {})
    title = m.get("title", "Michael Kofman")
    desc = m.get("description", "")
    url = page_url(path)
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Michael Kofman",
        "url": SITE_URL,
        "image": OG_IMAGE,
        "jobTitle": "CEO & Strategic Technologist",
        "worksFor": {"@type": "Organization", "name": "Digital Invest Inc."},
        "email": "mailto:mkofman@mkofman.com",
        "sameAs": ["https://www.linkedin.com/in/michael-kofman-0509176/"],
    }
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Michael Kofman",
        "url": SITE_URL,
        "description": desc or "Official website of Michael Kofman",
        "inLanguage": LANGS,
    }
    webpage = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "url": url,
        "isPartOf": {"@type": "WebSite", "url": SITE_URL, "name": "Michael Kofman"},
    }
    payload = json.dumps([person, website, webpage], ensure_ascii=False)
    return f'  <script type="application/ld+json">{payload}</script>'


def font_links() -> str:
    return """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@300;400;500;600&display=swap" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@300;400;500;600&display=swap"></noscript>"""


def head_extras(page_key: str, path: str, meta_en: dict) -> str:
    return "\n".join([font_links(), seo_block(page_key, path, meta_en), json_ld_block(page_key, path, meta_en)])


def patch_html_head(html: str, page_key: str, path: str, meta_en: dict) -> str:
    extras = head_extras(page_key, path, meta_en)
    # Remove old dynamic SEO if re-running
    html = re.sub(r"\n  <link rel=\"canonical\".*?</script>\n(?=  <link rel=\"stylesheet\")", "\n", html, flags=re.S)
    html = re.sub(r"\n  <link rel=\"preconnect\".*?</noscript>\n", "\n", html, flags=re.S)
    html = re.sub(
        r'(<meta name="description" content="[^"]*">)\n',
        r"\1\n" + extras + "\n",
        html,
        count=1,
    )
    # defer scripts except theme (only in head)
    html = re.sub(
        r'<script src="js/(?!theme\.js)([^"]+\.js[^"]*)"></script>',
        r'<script src="js/\1" defer></script>',
        html,
    )
    html = re.sub(r'\n\s*<script src="js/theme\.js"></script>\s*(?=<script src="js/(?:site-config|i18n))', '\n', html)
    # lazy below-fold images (not hero cutout)
    html = re.sub(
        r'(<img(?![^>]*portrait-hero)[^>]*)(>)',
        lambda m: m.group(1) + (' loading="lazy"' if 'loading=' not in m.group(1) else '') + m.group(2),
        html,
    )
    # Ensure analytics + structured data scripts present once
    if "js/analytics.js" not in html:
        html = html.replace(
            '<script src="js/main.js" defer></script>',
            '<script src="js/analytics.js" defer></script>\n  <script src="js/main.js" defer></script>',
        )
    return html


def patch_footer_privacy(html: str) -> str:
    if "privacy.html" in html:
        return html
    return html.replace(
        '<span data-i18n="footer.copyright">',
        '<a href="privacy.html" class="footer-privacy" data-i18n="footer.privacy">Privacy Policy</a>\n        <span data-i18n="footer.copyright">',
        1,
    )


def patch_index_hero(html: str, hero_w: int = 1131, hero_h: int = 1608) -> str:
    picture = (
        '<picture><source srcset="images/portrait-hero.webp" type="image/webp">'
        f'<img src="images/portrait-hero.png" alt="Michael Kofman" data-i18n-alt="home.heroAlt" '
        f'width="{hero_w}" height="{hero_h}" fetchpriority="high" decoding="async"></picture>'
    )
    if "portrait-hero.webp" in html:
        html = re.sub(
            r'<picture>.*?portrait-hero\.png.*?</picture>',
            picture,
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        html = html.replace(
            '<img src="images/portrait-hero.png" alt="Michael Kofman" data-i18n-alt="home.heroAlt">',
            picture,
        )
    if 'rel="preload" as="image"' not in html:
        html = html.replace(
            '<link rel="stylesheet" href="css/styles.css">',
            '  <link rel="preload" as="image" href="images/portrait-hero.webp" type="image/webp">\n  <link rel="stylesheet" href="css/styles.css">',
        )
    return html


def optimize_hero_images() -> tuple[int, int]:
    png = ROOT / "images" / "portrait-hero.png"
    webp = ROOT / "images" / "portrait-hero.webp"
    if not png.exists():
        return 1131, 1608
    try:
        from PIL import Image
    except ImportError:
        print("PIL not available — skipping hero image optimization")
        return 1131, 1608

    img = Image.open(png)
    max_w = 800
    if img.width > max_w:
        ratio = max_w / img.width
        new_size = (max_w, int(img.height * ratio))
        resample = getattr(Image, "Resampling", Image).LANCZOS
        img = img.resize(new_size, resample)

    if img.mode == "RGBA":
        r, g, b, a = img.split()
        rgb = Image.merge("RGB", (r, g, b))
        quantize = getattr(Image, "Quantize", Image).MEDIANCUT
        pal = rgb.quantize(colors=192, method=quantize).convert("RGBA")
        pal.putalpha(a)
        pal.save(png, "PNG", optimize=True, compress_level=9)
    else:
        if img.mode not in ("RGB",):
            img = img.convert("RGB")
        img.save(png, "PNG", optimize=True, compress_level=9)

    img = Image.open(png)
    img.save(webp, "WEBP", quality=82, method=6)
    print(
        f"hero assets: png {png.stat().st_size // 1024} KB, "
        f"webp {webp.stat().st_size // 1024} KB"
    )
    return img.width, img.height


def update_sitemap():
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    entry = '  <url><loc>https://mkofman.com/privacy.html</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>\n'
    if "privacy.html" not in text:
        text = text.replace("</urlset>", entry + "</urlset>")
        path.write_text(text, encoding="utf-8")
        print("updated sitemap.xml")


PRIVACY_I18N = {
    "ru": {
        "meta": {
            "privacy": {
                "title": "Политика конфиденциальности — Michael Kofman",
                "description": "Политика конфиденциальности mkofman.com — обработка данных форм и аналитика.",
            }
        },
        "footer": {"privacy": "Конфиденциальность"},
        "privacy": {
            "eyebrow": "Правовая информация",
            "title": "Политика конфиденциальности",
            "lead": "Как mkofman.com обрабатывает информацию при посещении сайта и отправке сообщений.",
            "updated": "Обновлено: июль 2026",
            "s1title": "Какие данные собираются",
            "s1text": "При отправке формы мы получаем указанные вами поля (имя, email, сообщение). При включённой аналитике — обезличенные данные о посещениях.",
            "s2title": "Как используются данные",
            "s2text": "Для ответа на запросы и улучшения сайта. Мы не продаём персональные данные.",
            "s3title": "Сторонние сервисы",
            "s3text": "Формы могут обрабатываться Formspree. Аналитика — Plausible или Google Analytics при настройке.",
            "s4title": "Ваши права",
            "s4text": "Запрос доступа, исправления или удаления данных: mkofman@mkofman.com.",
            "s5title": "Контакты",
            "s5text": "Вопросы по политике: mkofman@mkofman.com",
        },
    }
}


def merge_privacy_i18n(translations: dict) -> None:
    for lang, patch in PRIVACY_I18N.items():
        if lang in translations:
            deep_merge(translations[lang], patch)


def split_i18n():
    trans_path = ROOT / "js" / "translations.js"
    content_path = ROOT / "js" / "page-content.js"
    langs_dir = ROOT / "js" / "langs"
    langs_dir.mkdir(exist_ok=True)

    def parse_js_const(path: Path) -> dict:
        raw = path.read_text(encoding="utf-8")
        start, end = raw.find("{"), raw.rfind("}")
        return json.loads(raw[start : end + 1])

    translations = parse_js_const(trans_path)
    merge_privacy_i18n(translations)
    page_content = parse_js_const(content_path)

    for lang in LANGS:
        merged = json.loads(json.dumps(translations.get(lang, translations["en"])))
        if lang in page_content:
            deep_merge(merged, page_content[lang])
        out = f"window.__LANG_{lang} = {json.dumps(merged, ensure_ascii=False, indent=2)};\n"
        (langs_dir / f"{lang}.js").write_text(out, encoding="utf-8")

    bootstrap = """const TRANSLATIONS = {};
const LANG_FILES = %s;

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
    script.src = new URL(`js/langs/${lang}.js?v=2`, document.baseURI).href;
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
""" % json.dumps(LANGS)
    (ROOT / "js" / "i18n-bootstrap.js").write_text(bootstrap, encoding="utf-8")
    print(f"split i18n → {len(LANGS)} lang files")


def deep_merge(target: dict, source: dict) -> None:
    for k, v in source.items():
        if isinstance(v, dict) and isinstance(target.get(k), dict):
            deep_merge(target[k], v)
        else:
            target[k] = v


def patch_all_html(hero_dims: tuple[int, int] = (1131, 1608)):
    meta_by_lang = load_meta()
    meta_en = meta_by_lang["en"]
    hero_w, hero_h = hero_dims
    for filename, page_key, path in PAGES:
        fpath = ROOT / filename
        if not fpath.exists():
            continue
        html = fpath.read_text(encoding="utf-8")
        html = patch_html_head(html, page_key, path, meta_en)
        html = patch_footer_privacy(html)
        if filename == "index.html":
            html = patch_index_hero(html, hero_w, hero_h)
        # Update script tags for lazy i18n
        html = re.sub(r'<script src="js/translations\.js"[^>]*></script>\s*', "", html)
        html = re.sub(r'<script src="js/page-content\.js[^"]*"[^>]*></script>\s*', "", html)
        html = re.sub(r'<script src="js/seo\.js"[^>]*></script>\s*', "", html)
        html = re.sub(r'<script src="js/og-meta\.js"[^>]*></script>\s*', "", html)
        if "i18n-bootstrap.js" not in html:
            html = html.replace(
                '<script src="js/i18n.js',
                '<script src="js/i18n-bootstrap.js" defer></script>\n  <script src="js/i18n.js',
            )
        fpath.write_text(html, encoding="utf-8")
        print(f"patched {filename}")


def strip_font_import_from_css():
    css = ROOT / "css" / "styles.css"
    text = css.read_text(encoding="utf-8")
    text = re.sub(
        r"@import url\('https://fonts\.googleapis\.com[^']+'\);\n?",
        "/* Fonts loaded via <link> in HTML for non-blocking render */\n",
        text,
    )
    css.write_text(text, encoding="utf-8")
    print("stripped @import fonts from styles.css")


def main():
    hero_dims = optimize_hero_images()
    split_i18n()
    strip_font_import_from_css()
    patch_all_html(hero_dims)
    update_sitemap()
    cleanup_unused_images()
    print("build complete")


def cleanup_unused_images():
    unused = [
        "portrait-hero-opt.jpg",
        "portrait-bw.jpg",
        "portrait-hero-2.png",
        "portrait-hero-4.png",
    ]
    for name in unused:
        p = ROOT / "images" / name
        if p.exists():
            p.unlink()
            print(f"removed unused {name}")


if __name__ == "__main__":
    main()
