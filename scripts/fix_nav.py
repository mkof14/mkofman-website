#!/usr/bin/env python3
"""Unify site navigation and headers across all HTML pages."""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")

CONTROLS = """          <div class="header-controls">
            <button class="theme-toggle" type="button" data-i18n-aria="ui.toggleTheme" aria-label="Toggle theme">
              <svg class="icon-sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
              <svg class="icon-moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
            </button>
            <div class="lang-switcher">
              <button class="lang-trigger" type="button" data-i18n-aria="ui.selectLanguage" aria-label="Select language">
                <span class="lang-flag">🇺🇸</span>
                <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
              </button>
              <ul class="lang-panel" role="listbox"></ul>
            </div>
          </div>
          <button class="nav-toggle" type="button" data-i18n-aria="ui.toggleNav" aria-label="Toggle navigation">
            <span></span><span></span><span></span>
          </button>"""

NAV_LINKS = [
    ("index.html", "nav.home", "Home"),
    ("about.html", "nav.about", "About"),
    ("consulting.html", "nav.consulting", "Consulting"),
    ("insights.html", "nav.insights", "Insights"),
    ("ventures.html", "nav.ventures", "Ventures"),
    ("contact.html", "nav.contact", "Contact"),
]

MOBILE_EXTRA = []  # Additional pages live in footer only — keep header/mobile nav short

FOOTER_MORE = [
    ("board.html", "nav.board", "Board Advisory"),
    ("thesis.html", "nav.thesis", "Leadership Thesis"),
    ("press.html", "nav.press", "Press"),
    ("case-studies.html", "nav.caseStudies", "Case Studies"),
    ("career.html", "nav.career", "Career"),
    ("recognition.html", "nav.recognition", "Recognition"),
    ("brief-ipo.html", "nav.briefIpo", "Brief: IPO"),
    ("brief-genetic.html", "nav.briefGenetic", "Brief: Genetic Data"),
    ("brief-ai.html", "nav.briefAi", "Brief: AI Strategy"),
    ("article-data-infrastructure.html", "nav.articleInfra", "Data Infrastructure"),
    ("article-precision-medicine.html", "nav.articleHealth", "Precision Medicine"),
]

SKIP_HTML = {"speaking.html", "ip.html", "media-kit.html"}


def nav_links(active_file, desktop_only=False):
    lines = []
    for href, key, label in NAV_LINKS:
        if desktop_only and href == "index.html":
            continue
        cls = ' class="active"' if href == active_file else ""
        lines.append(f'        <a href="{href}"{cls} data-i18n="{key}">{label}</a>')
    return "\n".join(lines)


def mobile_nav(active_file):
    primary = []
    for href, key, label in NAV_LINKS:
        cls = ' class="active"' if href == active_file else ""
        primary.append(f'      <a href="{href}"{cls} data-i18n="{key}">{label}</a>')
    return (
        '    <nav class="main-nav main-nav-mobile" aria-label="Mobile">\n'
        + "\n".join(primary)
        + "\n    </nav>"
    )


def inner_header(active_file):
    return f"""    <header class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="logo">
        <span class="logo-name">Michael Kofman</span>
      </a>
      <div class="header-right">
        <nav class="main-nav" aria-label="Primary">
{nav_links(active_file, desktop_only=True)}
        </nav>
{CONTROLS}
      </div>
    </div>
{mobile_nav(active_file)}
  </header>"""


def home_nav_left(active_file):
    left = [
        ("index.html", "nav.home", "Home"),
        ("about.html", "nav.about", "About"),
        ("ventures.html", "nav.ventures", "Ventures"),
    ]
    lines = []
    for href, key, label in left:
        cls = ' class="active"' if href == active_file else ""
        lines.append(f'            <a href="{href}"{cls} data-i18n="{key}">{label}</a>')
    return "\n".join(lines)


def home_nav_right(active_file):
    right = [
        ("career.html", "nav.career", "Career"),
        ("recognition.html", "nav.recognition", "Recognition"),
        ("contact.html", "nav.contact", "Contact"),
    ]
    lines = []
    for href, key, label in right:
        cls = ' class="active"' if href == active_file else ""
        lines.append(f'            <a href="{href}"{cls} data-i18n="{key}">{label}</a>')
    return "\n".join(lines)


def home_header():
    mobile = mobile_nav("index.html")
    return f"""    <header class="site-header site-header--split">
    <div class="header-split">
      <div class="header-zone header-zone-left">
        <div class="header-zone-inner">
          <a href="index.html" class="logo logo--hero">
            <span class="logo-name">Michael Kofman</span>
          </a>
          <nav class="main-nav main-nav-left" aria-label="Primary">
{home_nav_left("index.html")}
          </nav>
        </div>
      </div>
      <div class="header-zone header-zone-gap" aria-hidden="true"></div>
      <div class="header-zone header-zone-right">
        <div class="header-zone-inner header-zone-inner-right">
          <nav class="main-nav main-nav-right" aria-label="Secondary">
{home_nav_right("index.html")}
          </nav>
{CONTROLS}
        </div>
      </div>
    </div>
{mobile}
  </header>"""


def footer_more_block() -> str:
    lines = [
        '          <h4 data-i18n="footer.more">More</h4>',
        "          <ul>",
    ]
    for href, key, label in FOOTER_MORE:
        lines.append(f'            <li><a href="{href}" data-i18n="{key}">{label}</a></li>')
    lines.append("          </ul>")
    return "\n".join(lines)


def patch_footer(html: str) -> str:
    return re.sub(
        r'<h4 data-i18n="footer\.more">More</h4>\s*<ul>.*?</ul>',
        footer_more_block(),
        html,
        count=1,
        flags=re.S,
    )


def patch_file(path):
    name = os.path.basename(path)
    html = open(path, encoding="utf-8").read()
    if name == "index.html":
        new_header = home_header()
    else:
        new_header = inner_header(name)

    html = re.sub(
        r"<header class=\"site-header.*?</header>",
        new_header,
        html,
        count=1,
        flags=re.S,
    )

    # Featured strip upgrade on home
    if name == "index.html":
        html = re.sub(
            r'<section class="featured-strip section section-white">.*?</section>',
            """  <section class="press-band" aria-label="Press">
    <div class="container">
      <p class="press-band-label" data-i18n="home.featuredEyebrow">As Featured In</p>
      <div class="press-band-track" role="list">
        <span role="listitem">Entrepreneur Magazine</span>
        <span class="press-band-sep" aria-hidden="true"></span>
        <span role="listitem">Healthcare Tech Outlook</span>
        <span class="press-band-sep" aria-hidden="true"></span>
        <span role="listitem">Who's Who in America</span>
        <span class="press-band-sep" aria-hidden="true"></span>
        <span role="listitem">Who's Who in Science &amp; Engineering</span>
        <span class="press-band-sep" aria-hidden="true"></span>
        <span role="listitem">Sony</span>
      </div>
    </div>
  </section>""",
            html,
            count=1,
            flags=re.S,
        )

    html = patch_footer(html)

    open(path, "w", encoding="utf-8").write(html)
    print(f"patched {name}")


def main():
    for name in sorted(os.listdir(ROOT)):
        if name.endswith(".html") and name not in SKIP_HTML:
            patch_file(os.path.join(ROOT, name))


if __name__ == "__main__":
    main()
