#!/usr/bin/env python3
"""Final internal pages correction pass — editorial, factual, footer, and copy sync."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HOME_FOOTER = """    <footer class="site-footer site-footer--home">
    <div class="container">
      <div class="footer-grid footer-grid--home">
        <div class="footer-brand">
          <div class="logo-name">Michael Kofman</div>
          <p data-i18n="home.footerHomeDesc">Technology executive, founder, and board advisor.</p>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.navigation">Navigation</h4>
          <ul>
            <li><a href="about.html" data-i18n="nav.about">About</a></li>
            <li><a href="career.html" data-i18n="nav.career">The Record</a></li>
            <li><a href="ventures.html" data-i18n="nav.ventures">Ventures</a></li>
            <li><a href="insights.html" data-i18n="nav.insights">Insights</a></li>
            <li><a href="contact.html" data-i18n="nav.contact">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.connect">Connect</h4>
          <ul>
            <li><a href="mailto:mkofman@mkofman.com">mkofman@mkofman.com</a></li>
            <li><a href="https://www.linkedin.com/in/michael-kofman-0509176/" target="_blank" rel="noopener">LinkedIn</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <a href="privacy.html" class="footer-privacy" data-i18n="footer.privacy">Privacy Policy</a>
        <span data-i18n="footer.copyright">&copy; 2026 Michael Kofman. All Rights Reserved.</span>
        <div class="footer-social">
          <a href="https://www.linkedin.com/in/michael-kofman-0509176/" target="_blank" rel="noopener" aria-label="LinkedIn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          </a>
        </div>
      </div>
    </div>
  </footer>"""

# Global factual / promotional string replacements (all langs)
GLOBAL_REPLACEMENTS = [
    (
        "Founded and scaled Digital Invest from inception through a successful IPO. The company is dedicated to the bio-mathematical sphere, transforming medicine through AI, ML, and DNA technologies.",
        "Bio-mathematical medicine, genomic data, and clinical intelligence — AI, machine learning, and DNA technologies applied to clinical and research workflows.",
    ),
    (
        "Founded and scaled Digital Invest Inc. from inception through a successful IPO. Led the full public offering process — legal structuring, financial compliance, investor roadshows, and SEC coordination. Directed design, construction, and operations of multiple data centers in the U.S. and Europe.",
        "Founded Digital Invest Inc. in 2021. Leads bio-mathematical medicine, genomic intelligence, and clinical data platforms.",
    ),
    (
        "Founded Digital Invest Inc. in 2021. Leads bio-mathematical medicine, genomic intelligence, and clinical data platforms; directed data-center and enterprise software operations in the U.S. and Europe.",
        "Founded Digital Invest Inc. in 2021. Leads bio-mathematical medicine, genomic intelligence, and clinical data platforms.",
    ),
    (
        "Founded Digital Invest Inc. in 2021. Leads bio-mathematical medicine, genomic intelligence, and clinical data platforms. Directed data-center and enterprise software operations in the U.S. and Europe. Featured in Healthcare Tech Outlook (2023).",
        "Founded Digital Invest Inc. in 2021. Leads bio-mathematical medicine, genomic intelligence, and clinical data platforms. Featured in Healthcare Tech Outlook (2023).",
    ),
    (
        "With Digital Invest Inc., founded in 2021, we are dedicated to the bio-mathematical sphere — transforming outdated approaches in medicine using science, DNA technologies, AI, and ML. The company was scaled from inception through a successful IPO and recognized among America's Top 10 Best Companies in Precision Medicine and Digital Health in 2023.",
        "Digital Invest Inc., founded in 2021, focuses on bio-mathematical medicine — applying science, DNA technologies, AI, and ML to clinical and research workflows. Featured in Healthcare Tech Outlook (2023).",
    ),
    (
        "These principles reflect decades of leadership.",
        "",
    ),
    (
        "These principles reflect more than three decades of founding companies, engineering critical systems, advising boards, and leading through market cycles.",
        "",
    ),
    (
        "Fill out the form below and I'll get back to you promptly.",
        "",
    ),
    (
        "Moments Across the Journey",
        "Selected Photographs",
    ),
    (
        "Selected photographs from company building, infrastructure, and leadership — from the 9 Net Avenue years to today.",
        "Authentic material from company building, infrastructure, and leadership.",
    ),
    (
        "Board advisory, strategic technology leadership, and building the next generation of digital health and infrastructure companies.",
        "Digital Invest Inc., AGRON Inc., and board advisory work.",
    ),
    (
        "Honors, credentials, and references from existing archives.",
        "Selected professional recognition and documented industry references.",
    ),
    (
        "Professional Record",
        "The Record",
    ),
    (
        "Documented activity across engineering, infrastructure, public markets, life sciences, and autonomous systems.",
        "Technology, companies, and operating experience across successive periods of technological change.",
    ),
    (
        '"periodCurrent": "Current"',
        '"periodCurrent": "Autonomous Systems"',
    ),
    (
        '"periodCurrentLead": "Principal companies and projects in active development."',
        '"periodCurrentLead": "AI, robotics, autonomous operations, geospatial systems, and related current infrastructure."',
    ),
    (
        "Build and scale a Data Storage company in a rapidly consolidating technology market.",
        "Build and scale a hosting and internet infrastructure company.",
    ),
    (
        "world's largest Data Storage companies",
        "hosting and internet infrastructure",
    ),
    (
        "$19.5",
        "",
    ),
    (
        "19.5 billion",
        "",
    ),
    (
        "Peak Value $19.5",
        "Acquired · Concentric Networks, 2000",
    ),
    (
        "technology visionary",
        "technology executive",
    ),
    (
        "Technological visionary",
        "Technology executive",
    ),
    (
        "A Legacy of Innovation",
        "Background",
    ),
    (
        "Recognition of Excellence",
        "Recognition",
    ),
    (
        "Decades of exceptional achievements",
        "Selected professional recognition and documented industry references.",
    ),
]

IPO_PATTERNS = [
    r"from inception through a successful IPO[^\"]*",
    r"from inception to a successful IPO[^\"]*",
    r"от старта до успешного IPO[^\"]*",
    r"до успешного IPO[^\"]*",
    r"scaled from inception through a successful IPO[^\"]*",
    r"introduction en bourse réussie[^\"]*",
    r"IPO & Financial Scaling",
    r"IPO und finanzielle Skalierung",
    r"IPO и финансовое масштабирование",
    r"IPO та фінансове масштабування",
    r"IPO 与财务规模化",
]


def patch_js_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in GLOBAL_REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
    for pat in IPO_PATTERNS:
        text = re.sub(pat, "", text, flags=re.IGNORECASE)
    # Remove empty thesis intro line if present
    text = re.sub(r'"intro": "",\n', "", text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"patched {path.relative_to(ROOT)}")


def replace_footers() -> None:
    footer_re = re.compile(
        r"<footer class=\"site-footer[^\"]*\">.*?</footer>",
        re.DOTALL,
    )
    for html in ROOT.glob("*.html"):
        if html.name == "index.html":
            continue
        text = html.read_text(encoding="utf-8")
        # Fix contact calendly nested in footer
        text = re.sub(
            r"</div>\s*\n\s*<section class=\"section section-white\">.*?</section>\s*\n\s*</footer>",
            "</div>\n    </div>\n  </footer>",
            text,
            flags=re.DOTALL,
        )
        new_text, n = footer_re.subn(HOME_FOOTER, text, count=1)
        if n:
            html.write_text(new_text, encoding="utf-8")
            print(f"footer {html.name}")


def patch_nav(html_path: Path) -> None:
    text = html_path.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        '<a href="consulting.html" data-i18n="nav.consulting">Consulting</a>',
        '<a href="board.html" data-i18n="nav.board">Board & Advisory</a>',
    )
    # Mobile: add board if missing, remove duplicate consulting pattern
    if "board.html" not in text.split("main-nav-mobile")[1].split("</nav>")[0]:
        text = text.replace(
            '<a href="insights.html" data-i18n="nav.insights">Insights</a>\n      <a href="contact.html"',
            '<a href="insights.html" data-i18n="nav.insights">Insights</a>\n      <a href="board.html" data-i18n="nav.board">Board & Advisory</a>\n      <a href="contact.html"',
        )
    if text != original:
        html_path.write_text(text, encoding="utf-8")
        print(f"nav {html_path.name}")


def patch_consulting_page() -> None:
    path = ROOT / "consulting.html"
    body = """  <section class="page-hero">
    <div class="container">
      <span class="eyebrow" data-i18n="consulting.eyebrow">Advisory</span>
      <h1 data-i18n="consulting.title">Consulting</h1>
      <div class="gold-line"></div>
    </div>
  </section>

  <section class="section section-cream">
    <div class="container container-narrow">
      <div class="consulting-intro fade-in">
        <p class="lead" data-i18n="consulting.redirectLead">Board and strategic advisory work is documented on the Board & Advisory page. For professional inquiries, use Contact.</p>
        <p style="margin-top: 2rem;"><a href="board.html" class="text-link" data-i18n="consulting.redirectLink">Board & Advisory →</a></p>
        <p style="margin-top: 1rem;"><a href="contact.html?topic=advisory" class="text-link" data-i18n="nav.contact">Contact →</a></p>
      </div>
    </div>
  </section>
"""
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"<section class=\"page-hero\">.*?</section>\s*<section class=\"section section-cream\">.*?</section>\s*<section class=\"section section-white\">.*?</section>",
        body.strip(),
        text,
        flags=re.DOTALL,
    )
    path.write_text(text, encoding="utf-8")
    print("consulting.html simplified")


def patch_insights_page() -> None:
    path = ROOT / "insights.html"
    text = path.read_text(encoding="utf-8")
    # Keep hero + briefs + articles only; add related links section
    related = """
  <section class="section section-cream">
    <div class="container container-narrow">
      <p class="fade-in" data-i18n="insights.relatedLead">Recognition, press coverage, and patents are documented separately.</p>
      <p class="fade-in" style="margin-top: 1rem;">
        <a href="recognition.html" class="text-link" data-i18n="nav.recognition">Recognition →</a>
        &nbsp;·&nbsp;
        <a href="press.html" class="text-link" data-i18n="nav.press">Press →</a>
      </p>
    </div>
  </section>
"""
    text = re.sub(
        r"\n  <section class=\"section section-cream\">\n    <div class=\"container\">\n      <article class=\"insights-featured",
        related + "\n  <!-- removed duplicate recognition/press/patents/reading -->",
        text,
        count=1,
    )
    # Remove everything from removed comment through last section before footer
    text = re.sub(
        r"<!-- removed duplicate recognition/press/patents/reading -->.*?(?=\n    <footer)",
        "",
        text,
        flags=re.DOTALL,
    )
    # Add lead to hero if missing
    if 'data-i18n="insights.lead"' not in text:
        text = text.replace(
            '<div class="gold-line"></div>\n    </div>\n  </section>\n\n  \n  <section class="section section-white">',
            '<div class="gold-line"></div>\n      <p class="lead" data-i18n="insights.lead">Substantive writing and executive briefs.</p>\n    </div>\n  </section>\n\n  <section class="section section-white">',
        )
    path.write_text(text, encoding="utf-8")
    print("insights.html trimmed")


def patch_career_page() -> None:
    path = ROOT / "career.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        'data-i18n="career.eyebrow">Professional Record',
        'data-i18n="career.eyebrow">The Record',
    )
    text = text.replace(
        'data-i18n="career.lead">Documented activity across engineering, infrastructure, public markets, life sciences, and autonomous systems.',
        'data-i18n="career.lead">Technology, companies, and operating experience across successive periods of technological change.',
    )
    text = text.replace(
        'data-i18n="career.periodCurrent">Current',
        'data-i18n="career.periodCurrent">Autonomous Systems',
    )
    text = text.replace(
        'data-i18n="career.periodCurrentLead">Principal companies and projects in active development.',
        'data-i18n="career.periodCurrentLead">AI, robotics, autonomous operations, geospatial systems, and related current infrastructure.',
    )
    # Move Digital Invest from Current to Life Sciences — remove second article from current block
    current_block = """      <div class="record-period record-period--current fade-in">
        <h2 class="record-period-title" data-i18n="career.periodCurrent">Autonomous Systems</h2>
        <p class="record-period-lead" data-i18n="career.periodCurrentLead">AI, robotics, autonomous operations, geospatial systems, and related current infrastructure.</p>
        <article class="record-entry">
          <div class="record-entry-meta" data-i18n="career.t0year">2026 — Present</div>
          <h3 class="record-entry-title">AGRON Inc.</h3>
          <div class="record-entry-role" data-i18n="career.t0role">Founder</div>
          <p data-i18n="career.t0desc">Founded AGRON Inc. for autonomous aerial-ground operations, UAV capability development, geospatial systems, and maritime intelligence infrastructure.</p>
        </article>
      </div>"""
    text = re.sub(
        r'<div class="record-period record-period--current fade-in">.*?</div>\n\n      <div class="record-period fade-in">\n        <h2 class="record-period-title" data-i18n="career\.period4title">',
        current_block + '\n\n      <div class="record-period fade-in">\n        <h2 class="record-period-title" data-i18n="career.period4title">',
        text,
        flags=re.DOTALL,
    )
    # Add Digital Invest at start of Life Sciences section
    di_entry = """        <article class="record-entry">
          <div class="record-entry-meta" data-i18n="career.t1year">2021 — Present</div>
          <h3 class="record-entry-title">Digital Invest Inc.</h3>
          <div class="record-entry-role" data-i18n="career.t1role">Founder & CEO</div>
          <p data-i18n="career.t1desc">Founded Digital Invest Inc. in 2021. Leads bio-mathematical medicine, genomic intelligence, and clinical data platforms. Featured in Healthcare Tech Outlook (2023).</p>
        </article>
"""
    if "Digital Invest Inc." not in text.split("period4title")[1].split("period5title")[0]:
        text = text.replace(
            '<p class="record-period-lead" data-i18n="career.period4lead">',
            di_entry + '        <p class="record-period-lead" data-i18n="career.period4lead">',
            1,
        )
    path.write_text(text, encoding="utf-8")
    print("career.html restructured")


def patch_vercel_redirect() -> None:
    path = ROOT / "vercel.json"
    import json

    data = json.loads(path.read_text(encoding="utf-8"))
    redirects = data.setdefault("redirects", [])
    entry = {
        "source": "/consulting.html",
        "destination": "/board.html",
        "permanent": True,
    }
    if not any(r.get("source") == entry["source"] for r in redirects):
        redirects.append(entry)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print("vercel.json consulting redirect")


def patch_translations_consulting_insights() -> None:
    path = ROOT / "js" / "translations.js"
    text = path.read_text(encoding="utf-8")
    if "redirectLead" not in text:
        text = text.replace(
            '"consulting": {\n      "eyebrow": "Advisory Services",',
            '"consulting": {\n      "redirectLead": "Board and strategic advisory work is documented on the Board & Advisory page. For professional inquiries, use Contact.",\n      "redirectLink": "Board & Advisory →",\n      "eyebrow": "Advisory",',
            1,
        )
    if '"lead": "Substantive writing and executive briefs."' not in text:
        text = text.replace(
            '"insights": {\n      "eyebrow": "Perspectives",',
            '"insights": {\n      "lead": "Substantive writing and executive briefs.",\n      "relatedLead": "Recognition, press coverage, and patents are documented separately.",\n      "eyebrow": "Perspectives",',
            1,
        )
    path.write_text(text, encoding="utf-8")
    print("translations.js consulting/insights keys")


def main() -> None:
    for name in ("translations.js", "page-content.js"):
        patch_js_file(ROOT / "js" / name)
    for lang in (ROOT / "js" / "langs").glob("*.js"):
        patch_js_file(lang)
    replace_footers()
    for html in ROOT.glob("*.html"):
        if html.name != "index.html":
            patch_nav(html)
    patch_consulting_page()
    patch_insights_page()
    patch_career_page()
    patch_vercel_redirect()
    patch_translations_consulting_insights()
    print("final internal pass complete")


if __name__ == "__main__":
    main()
