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
    ("case-studies.html", "caseStudies", "case-studies.html"),
    ("article-data-infrastructure.html", "article1", "article-data-infrastructure.html"),
    ("article-precision-medicine.html", "article2", "article-precision-medicine.html"),
    ("privacy.html", "privacy", "privacy.html"),
    ("board.html", "board", "board.html"),
    ("thesis.html", "thesis", "thesis.html"),
    ("press.html", "press", "press.html"),
    ("deck.html", "deck", "deck.html"),
    ("brief-ipo.html", "briefIpo", "brief-ipo.html"),
    ("brief-genetic.html", "briefGenetic", "brief-genetic.html"),
    ("brief-ai.html", "briefAi", "brief-ai.html"),
]

OG_IMAGE = f"{SITE_URL}/images/portrait-hero.webp"
SITE_START_YEAR = 2026

ARTICLE_PAGES = {
    "article1": {"datePublished": "2024-06-01", "author": "Michael Kofman"},
    "article2": {"datePublished": "2024-08-15", "author": "Michael Kofman"},
    "briefIpo": {"datePublished": "2025-03-01", "author": "Michael Kofman"},
    "briefGenetic": {"datePublished": "2025-04-01", "author": "Michael Kofman"},
    "briefAi": {"datePublished": "2025-05-01", "author": "Michael Kofman"},
}

BREADCRUMB_LABELS = {
    "home": "Home",
    "about": "About",
    "ventures": "Ventures",
    "career": "Career",
    "recognition": "Recognition",
    "contact": "Contact",
    "consulting": "Consulting",
    "insights": "Insights",
    "caseStudies": "Case Studies",
    "article1": "Data Infrastructure",
    "article2": "Precision Medicine",
    "privacy": "Privacy",
    "board": "Board Advisory",
    "thesis": "Leadership Thesis",
    "press": "Press",
    "deck": "Executive Overview",
    "briefIpo": "Brief: IPO",
    "briefGenetic": "Brief: Genetic Data",
    "briefAi": "Brief: AI Strategy",
}


def meta_basics_block() -> str:
    return "\n".join([
        '  <meta name="theme-color" content="#0c1829">',
        '  <meta name="color-scheme" content="dark light">',
        '  <meta name="format-detection" content="telephone=no">',
        '  <meta name="author" content="Michael Kofman">',
        '  <meta property="og:locale" content="en_US">',
        '  <meta name="apple-mobile-web-app-capable" content="yes">',
        '  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">',
    ])


def breadcrumb_ld(path: str, page_key: str) -> dict | None:
    if page_key == "home" or not path:
        return None
    items = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL},
        {
            "@type": "ListItem",
            "position": 2,
            "name": BREADCRUMB_LABELS.get(page_key, page_key),
            "item": page_url(path),
        },
    ]
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def article_ld(page_key: str, path: str, meta_en: dict) -> dict | None:
    info = ARTICLE_PAGES.get(page_key)
    if not info:
        return None
    m = meta_en.get(page_key, {})
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": m.get("title", "Michael Kofman"),
        "description": m.get("description", ""),
        "url": page_url(path),
        "datePublished": info["datePublished"],
        "dateModified": info["datePublished"],
        "author": {"@type": "Person", "name": info["author"], "url": SITE_URL},
        "publisher": {
            "@type": "Person",
            "name": "Michael Kofman",
            "url": SITE_URL,
            "logo": {"@type": "ImageObject", "url": OG_IMAGE},
        },
        "image": OG_IMAGE,
        "inLanguage": "en",
    }


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
        "publisher": {"@type": "Person", "name": "Michael Kofman"},
    }
    webpage = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "url": url,
        "isPartOf": {"@type": "WebSite", "url": SITE_URL, "name": "Michael Kofman"},
    }
    blocks = [person, website, webpage]
    crumb = breadcrumb_ld(path, page_key)
    if crumb:
        blocks.append(crumb)
    article = article_ld(page_key, path, meta_en)
    if article:
        blocks.append(article)
    payload = json.dumps(blocks, ensure_ascii=False)
    return f'  <script type="application/ld+json">{payload}</script>'


FONT_HREF = (
    "https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600&display=swap"
)


def font_links() -> str:
    return f"""  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FONT_HREF}" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="{FONT_HREF}"></noscript>"""


def head_extras(page_key: str, path: str, meta_en: dict) -> str:
    basics = meta_basics_block()
    if page_key == "deck":
        return "\n".join([basics, font_links()])
    return "\n".join([basics, font_links(), seo_block(page_key, path, meta_en), json_ld_block(page_key, path, meta_en)])


def strip_seo_blocks(html: str) -> str:
    """Remove all injected SEO/OG/JSON-LD/font blocks so rebuild is idempotent."""
    # Repeated canonical → JSON-LD clusters (may appear many times)
    html = re.sub(
        r"(?:\n\s*)?<link rel=\"canonical\" href=\"[^\"]*\">"
        r"(?:\n\s*<link rel=\"alternate\"[^>]*>)*"
        r"(?:\n\s*<meta property=\"og:[^>]*>)*"
        r"(?:\n\s*<meta name=\"twitter:[^>]*>)*"
        r"(?:\n\s*<script type=\"application/ld\+json\">.*?</script>)+",
        "",
        html,
        flags=re.S,
    )
    html = re.sub(
        r"(?:\n\s*)?<link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\">"
        r"(?:\n\s*<link rel=\"preconnect\"[^>]*>)?"
        r"(?:\n\s*<link rel=\"stylesheet\" href=\"https://fonts\.googleapis\.com[^>]*>)?"
        r"(?:\n\s*<noscript><link rel=\"stylesheet\" href=\"https://fonts\.googleapis\.com[^>]*></noscript>)?",
        "",
        html,
        flags=re.S,
    )
    html = re.sub(
        r"(?:\n\s*)?<meta name=\"theme-color\"[^>]*>",
        "",
        html,
    )
    html = re.sub(
        r"(?:\n\s*)?<meta name=\"(?:color-scheme|format-detection|author|apple-mobile-web-app-capable|apple-mobile-web-app-status-bar-style)\"[^>]*>",
        "",
        html,
    )
    html = re.sub(
        r"(?:\n\s*)?<meta property=\"og:locale\"[^>]*>",
        "",
        html,
    )
    # RSS alternate may be injected repeatedly by expansion patches
    html = re.sub(
        r"(?:\n\s*)?<link rel=\"alternate\" type=\"application/rss\+xml\"[^>]*>",
        "",
        html,
    )
    # Keep a single RSS link near the top of <head>
    if "<head>" in html:
        html = html.replace(
            "<head>",
            '<head>\n  <link rel="alternate" type="application/rss+xml" title="Michael Kofman Insights" href="/feed.xml">',
            1,
        )
    return html


def patch_html_head(html: str, page_key: str, path: str, meta_en: dict) -> str:
    extras = head_extras(page_key, path, meta_en)
    html = strip_seo_blocks(html)
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
    return html


def patch_footer_privacy(html: str) -> str:
    if "privacy.html" in html:
        return html
    return html.replace(
        '<span data-i18n="footer.copyright">',
        '<a href="privacy.html" class="footer-privacy" data-i18n="footer.privacy">Privacy Policy</a>\n        <span data-i18n="footer.copyright">',
        1,
    )


def patch_footer_copyright(html: str) -> str:
    from datetime import datetime

    year = datetime.now().year
    html = re.sub(
        r'(<span data-i18n="footer\.copyright">)[^<]*(</span>)',
        rf"\1&copy; {year} Michael Kofman. All Rights Reserved.\2",
        html,
    )
    return html


def patch_index_hero(html: str, hero_w: int = 720, hero_h: int = 1022) -> str:
    picture = (
        '<picture>'
        '<source srcset="/images/portrait-hero-480.webp" type="image/webp" media="(max-width: 768px)">'
        '<source srcset="/images/portrait-hero.webp" type="image/webp">'
        f'<img src="/images/portrait-hero.jpg" alt="Michael Kofman" data-i18n-alt="home.heroAlt" '
        f'width="{hero_w}" height="{hero_h}" fetchpriority="high" decoding="async"></picture>'
    )
    if "portrait-hero.webp" in html or "portrait-hero.jpg" in html or "portrait-hero.png" in html:
        html = re.sub(
            r'<picture>.*?portrait-hero\.(?:png|jpg|webp).*?</picture>',
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
    html = html.replace("images/portrait-hero.png", "/images/portrait-hero.jpg")
    html = html.replace('src="images/portrait-hero.jpg"', 'src="/images/portrait-hero.jpg"')
    html = re.sub(
        r'\s*<link rel="preload" as="image" href="/images/portrait-hero(?:-480)?\.webp"[^>]*>\n?',
        "\n",
        html,
    )
    html = re.sub(
        r'(<link rel="stylesheet" href="/css/site\.css">)',
        '  <link rel="preload" as="image" href="/images/portrait-hero-480.webp" type="image/webp" media="(max-width: 768px)">\n'
        '  <link rel="preload" as="image" href="/images/portrait-hero.webp" type="image/webp" media="(min-width: 769px)">\n'
        r"\1",
        html,
        count=1,
    )
    return html


def optimize_hero_images() -> tuple[int, int]:
    """Emit lean WebP (alpha) + JPEG (navy bake) — no heavy PNG in the deploy."""
    webp = ROOT / "images" / "portrait-hero.webp"
    jpg = ROOT / "images" / "portrait-hero.jpg"
    sources = [
        ROOT / "images" / "portrait-hero-source.png",
        ROOT / "images" / "portrait-hero.png",
        webp,
        jpg,
    ]
    src = next((p for p in sources if p.exists()), None)
    if src is None:
        return 720, 1022
    try:
        from PIL import Image
    except ImportError:
        print("PIL not available — skipping hero image optimization")
        return 720, 1022

    img = Image.open(src).convert("RGBA")
    max_w = 720
    if img.width > max_w:
        ratio = max_w / img.width
        resample = getattr(Image, "Resampling", Image).LANCZOS
        img = img.resize((max_w, int(img.height * ratio)), resample)

    img.save(webp, "WEBP", quality=78, method=6)
    navy = (12, 24, 41, 255)
    composed = Image.alpha_composite(Image.new("RGBA", img.size, navy), img).convert("RGB")
    composed.save(jpg, "JPEG", quality=82, optimize=True, progressive=True)

    # Mobile variant (~480px wide)
    mobile_w = 480
    if img.width > mobile_w:
        ratio = mobile_w / img.width
        resample = getattr(Image, "Resampling", Image).LANCZOS
        mobile = img.resize((mobile_w, int(img.height * ratio)), resample)
    else:
        mobile = img
    mobile_webp = ROOT / "images" / "portrait-hero-480.webp"
    mobile_jpg = ROOT / "images" / "portrait-hero-480.jpg"
    mobile.save(mobile_webp, "WEBP", quality=76, method=6)
    mobile_composed = Image.alpha_composite(Image.new("RGBA", mobile.size, navy), mobile).convert("RGB")
    mobile_composed.save(mobile_jpg, "JPEG", quality=80, optimize=True, progressive=True)

    # Drop legacy PNG from deploy tree if present
    legacy_png = ROOT / "images" / "portrait-hero.png"
    if legacy_png.exists():
        legacy_png.unlink()

    print(
        f"hero assets: webp {webp.stat().st_size // 1024} KB, "
        f"jpg {jpg.stat().st_size // 1024} KB, "
        f"mobile webp {mobile_webp.stat().st_size // 1024} KB "
        f"({img.width}x{img.height})"
    )
    return img.width, img.height


def optimize_archive_images() -> None:
    """Recompress archive WebP/JPEG pairs for faster mobile loads."""
    archive = ROOT / "images" / "archive"
    if not archive.is_dir():
        return
    try:
        from PIL import Image
    except ImportError:
        print("PIL not available — skipping archive optimization")
        return

    resample = getattr(Image, "Resampling", Image).LANCZOS
    max_display_w = 960
    for path in sorted(archive.glob("*.jpg")) + sorted(archive.glob("*.jpeg")):
        max_w_file = 520 if path.stem.endswith("-sm") else max_display_w
        jpg_quality = 72 if path.stem.endswith("-sm") else 80
        webp_quality = 68 if path.stem.endswith("-sm") else 74
        try:
            img = Image.open(path)
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            if img.width > max_w_file:
                ratio = max_w_file / img.width
                img = img.resize((max_w_file, int(img.height * ratio)), resample)
            webp_path = path.with_suffix(".webp")
            img.save(webp_path, "WEBP", quality=webp_quality, method=6)
            img.save(path, "JPEG", quality=jpg_quality, optimize=True, progressive=True)
            print(
                f"archive {path.name}: jpg {path.stat().st_size // 1024} KB, "
                f"webp {webp_path.stat().st_size // 1024} KB"
            )
        except OSError as err:
            print(f"skip archive {path.name}: {err}")


def update_sitemap():
    from datetime import datetime, timezone

    path = ROOT / "sitemap.xml"
    lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entries = [
        ("", "monthly", "1.0"),
        ("about.html", "monthly", "0.9"),
        ("consulting.html", "monthly", "0.8"),
        ("board.html", "monthly", "0.85"),
        ("thesis.html", "monthly", "0.8"),
        ("insights.html", "weekly", "0.8"),
        ("ventures.html", "monthly", "0.8"),
        ("career.html", "monthly", "0.7"),
        ("recognition.html", "monthly", "0.7"),
        ("press.html", "monthly", "0.7"),
        ("contact.html", "yearly", "0.8"),
        ("case-studies.html", "monthly", "0.7"),
        ("article-data-infrastructure.html", "yearly", "0.6"),
        ("article-precision-medicine.html", "yearly", "0.6"),
        ("brief-ipo.html", "monthly", "0.65"),
        ("brief-genetic.html", "monthly", "0.65"),
        ("brief-ai.html", "monthly", "0.65"),
        ("privacy.html", "yearly", "0.3"),
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page, freq, pri in entries:
        loc = SITE_URL if not page else f"{SITE_URL}/{page}"
        mtime = lastmod
        fpath = ROOT / page if page else ROOT / "index.html"
        if fpath.exists():
            mtime = datetime.fromtimestamp(fpath.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d")
        lines.append(
            f"  <url><loc>{loc}</loc><lastmod>{mtime}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{pri}</priority></url>"
        )
    lines.append("</urlset>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("updated sitemap.xml")


def generate_feed():
    meta_en = load_meta()["en"]
    items = [
        ("article-data-infrastructure.html", "article1"),
        ("article-precision-medicine.html", "article2"),
        ("brief-ipo.html", "briefIpo"),
        ("brief-genetic.html", "briefGenetic"),
        ("brief-ai.html", "briefAi"),
    ]
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        "<channel>",
        "<title>Michael Kofman — Insights</title>",
        f"<link>{SITE_URL}/insights.html</link>",
        "<description>Executive perspectives from Michael Kofman</description>",
        f"<lastBuildDate>{now}</lastBuildDate>",
    ]
    for path, key in items:
        m = meta_en.get(key, {})
        title = m.get("title", "Michael Kofman")
        desc = m.get("description", "")
        link = page_url(path)
        parts.extend(
            [
                "<item>",
                f"<title>{title}</title>",
                f"<link>{link}</link>",
                f"<guid>{link}</guid>",
                f"<description>{desc}</description>",
                "</item>",
            ]
        )
    parts.extend(["</channel>", "</rss>"])
    (ROOT / "feed.xml").write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("generated feed.xml")


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
        html = patch_footer_copyright(html)
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
    optimize_archive_images()
    split_i18n()
    strip_font_import_from_css()
    patch_all_html(hero_dims)
    update_sitemap()
    generate_feed()
    cleanup_unused_images()
    finalize_deploy_assets()
    print("build complete")


def finalize_deploy_assets() -> None:
    """Generate runtime config, bundle CSS/JS, and wire HTML for Vercel deploy."""
    import subprocess
    import sys

    py = sys.executable
    scripts = ROOT / "scripts"
    subprocess.run([py, str(scripts / "generate_config.py")], check=True, cwd=ROOT)
    subprocess.run([py, str(scripts / "optimize_perf.py")], check=True, cwd=ROOT)
    print("deploy assets ready (site-config, site.css, app.js)")


def cleanup_unused_images():
    unused = [
        "portrait-hero-opt.jpg",
        "portrait-bw.jpg",
        "portrait-hero-2.png",
        "portrait-hero-4.png",
        "portrait-color.jpg",
        "portrait-color-2.jpg",
        "portrait-hero-3.png",
        "portrait-hero-3.jpg",
        "portrait-hero-3.webp",
        "portrait-hero.png",
    ]
    for name in unused:
        p = ROOT / "images" / name
        if p.exists():
            p.unlink()
            print(f"removed unused {name}")


if __name__ == "__main__":
    main()
