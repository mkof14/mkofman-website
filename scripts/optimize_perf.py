#!/usr/bin/env python3
"""Bundle CSS/JS and rewrite HTML for fewer network requests."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FONT_HREF = (
    "https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600&display=swap"
)

CSS_PARTS = ["styles.css", "expansion.css", "controls.css"]
JS_RUNTIME_PARTS = ["forms.js", "cta.js", "analytics.js", "features.js", "main.js"]


def bundle_css() -> None:
    chunks = []
    for name in CSS_PARTS:
        chunks.append(f"/* === {name} === */\n")
        chunks.append((ROOT / "css" / name).read_text(encoding="utf-8"))
        chunks.append("\n")
    out = ROOT / "css" / "site.css"
    out.write_text("".join(chunks), encoding="utf-8")
    print(f"bundled {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")


def bundle_js() -> None:
    # Prepend generated site-config so runtime has SITE_CONFIG
    config = (ROOT / "js" / "site-config.js").read_text(encoding="utf-8")
    chunks = [config, "\n"]
    for name in JS_RUNTIME_PARTS:
        chunks.append(f"\n/* === {name} === */\n")
        chunks.append((ROOT / "js" / name).read_text(encoding="utf-8"))
    out = ROOT / "js" / "app.js"
    out.write_text("".join(chunks), encoding="utf-8")
    print(f"bundled {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")


def normalize_image_paths(html: str) -> str:
    """Root-absolute image URLs — reliable on www/apex and all pages."""
    html = re.sub(r'\bsrc="images/', 'src="/images/', html)
    html = re.sub(r"\bsrc='images/", "src='/images/", html)
    html = re.sub(r'srcset="images/', 'srcset="/images/', html)
    html = re.sub(
        r'href="images/([^"]+\.(?:jpg|jpeg|webp|png|gif))"',
        r'href="/images/\1"',
        html,
    )
    html = html.replace('href="images/', 'href="/images/')
    return html


def patch_html_assets(html: str) -> str:
    # Slim Google Fonts
    html = re.sub(
        r"https://fonts\.googleapis\.com/css2\?family=Cormorant\+Garamond:[^\"']+",
        FONT_HREF,
        html,
    )

    # Single CSS bundle — root-absolute path avoids redirect loops on custom domains
    html = re.sub(
        r'\s*<link rel="stylesheet" href="css/(?:styles|expansion|controls|site)\.css">',
        "",
        html,
    )
    if 'href="/css/site.css"' not in html and 'href="css/site.css"' not in html:
        # after preload or before theme
        if 'rel="preload" as="image"' in html:
            html = html.replace(
                'rel="preload" as="image" href="images/portrait-hero.webp" type="image/webp">',
                'rel="preload" as="image" href="/images/portrait-hero-480.webp" type="image/webp" media="(max-width: 768px)">\n'
                '  <link rel="preload" as="image" href="/images/portrait-hero.webp" type="image/webp" media="(min-width: 769px)">\n'
                '  <link rel="stylesheet" href="/css/site.css">',
                1,
            )
        else:
            html = html.replace(
                '<script src="js/theme.js"></script>',
                '<link rel="stylesheet" href="/css/site.css">\n  <script src="/js/theme.js"></script>',
                1,
            )
    html = html.replace('href="css/site.css"', 'href="/css/site.css"')

    # Hero PNG → JPG fallback
    html = html.replace("images/portrait-hero.png", "images/portrait-hero.jpg")

    # Press clipping uses small display asset (full scan stays on href)
    html = html.replace(
        'srcset="images/archive/press-datapeer-interview.webp"',
        'srcset="images/archive/press-datapeer-interview-sm.webp"',
    )
    html = re.sub(
        r'<img[^>]*src="images/archive/press-datapeer-interview(?:-sm)?\.jpg"[^>]*>',
        '<img src="images/archive/press-datapeer-interview-sm.jpg" alt="State of the Storage Industry — DataPeer interview with Michael Kofman" width="640" height="816" loading="lazy" decoding="async">',
        html,
        count=1,
    )

    # Collapse many defer scripts → boot chain
    # Remove individual runtime scripts; keep i18n + app
    for name in ("site-config.js", "forms.js", "cta.js", "analytics.js", "features.js", "main.js"):
        html = re.sub(rf'\s*<script src="(?:/)?js/{re.escape(name)}"[^>]*></script>', "", html)

    if 'src="/js/app.js"' not in html and 'src="js/app.js"' not in html:
        # after i18n.js
        if "i18n.js" in html:
            html = re.sub(
                r'(<script src="(?:/)?js/i18n\.js[^"]*"[^>]*></script>)',
                r'\1\n  <script src="/js/app.js" defer></script>',
                html,
                count=1,
            )
        else:
            html = html.replace(
                "</body>",
                '  <script src="/js/app.js" defer></script>\n</body>',
                1,
            )

    # Ensure i18n-bootstrap present once before i18n
    if "i18n-bootstrap.js" not in html and "i18n.js" in html:
        html = html.replace(
            '<script src="/js/i18n.js',
            '<script src="/js/i18n-bootstrap.js" defer></script>\n  <script src="/js/i18n.js',
            1,
        )
        html = html.replace(
            '<script src="js/i18n.js',
            '<script src="/js/i18n-bootstrap.js" defer></script>\n  <script src="/js/i18n.js',
            1,
        )

    html = html.replace('src="js/app.js"', 'src="/js/app.js"')
    html = html.replace('src="js/i18n-bootstrap.js"', 'src="/js/i18n-bootstrap.js"')
    html = html.replace('src="js/i18n.js', 'src="/js/i18n.js')
    html = html.replace('src="js/theme.js"', 'src="/js/theme.js"')

    return normalize_image_paths(html)


def css_cache_version() -> str:
    return str(int((ROOT / "css" / "site.css").stat().st_mtime))


def stamp_css_href(html: str, version: str) -> str:
    href = f'/css/site.css?v={version}'
    html = re.sub(r'href="/css/site\.css(?:\?v=[^"]*)?"', f'href="{href}"', html)
    return html


def patch_all_html(css_version: str | None = None) -> None:
    version = css_version or css_cache_version()
    for path in sorted(ROOT.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        new = stamp_css_href(patch_html_assets(html), version)
        if new != html:
            path.write_text(new, encoding="utf-8")
            print(f"assets patched {path.name}")


def main() -> None:
    bundle_css()
    css_version = css_cache_version()
    bundle_js()
    patch_all_html(css_version)
    print("perf bundle complete")


if __name__ == "__main__":
    main()
