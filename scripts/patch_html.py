#!/usr/bin/env python3
"""Add favicon, seo.js, and fix mobile nav duplicate class attributes."""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")

HEAD_INSERT = """  <link rel="icon" href="favicon.svg" type="image/svg+xml">"""

SEO_SCRIPT = """  <script src="js/seo.js"></script>"""


def patch_head(html):
    if "favicon.svg" not in html:
        html = html.replace(
            '<meta name="viewport"',
            f"{HEAD_INSERT}\n  <meta name=\"viewport\"",
            1,
        )
    if "js/seo.js" not in html:
        html = html.replace(
            '<script src="js/main.js"></script>',
            f"{SEO_SCRIPT}\n  <script src=\"js/main.js\"></script>",
            1,
        )
    return html


def fix_mobile_nav_classes(html):
    return re.sub(
        r'class="active" data-i18n="([^"]+)" class="mobile-nav-secondary"',
        r'class="mobile-nav-secondary active" data-i18n="\1"',
        html,
    )


def main():
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(ROOT, name)
        html = open(path, encoding="utf-8").read()
        html = patch_head(html)
        html = fix_mobile_nav_classes(html)
        open(path, "w", encoding="utf-8").write(html)
        print(f"patched {name}")


if __name__ == "__main__":
    main()
