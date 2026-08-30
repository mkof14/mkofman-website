#!/usr/bin/env python3
"""Apply site expansion: merge translations, generate pages, patch existing HTML."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "scripts" / "expansion_content.json"
TRANSLATIONS = ROOT / "js" / "translations.js"

HEADER_STUB = """    <header class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="logo"><span class="logo-name">Michael Kofman</span></a>
    </div>
  </header>"""

FOOTER = """    <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <div class="logo-name">Michael Kofman</div>
          <p data-i18n="footer.desc">CEO, strategic technologist, and award-winning entrepreneur.</p>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.navigation">Navigation</h4>
          <ul>
            <li><a href="about.html" data-i18n="nav.about">About</a></li>
            <li><a href="consulting.html" data-i18n="nav.consulting">Consulting</a></li>
            <li><a href="insights.html" data-i18n="nav.insights">Insights</a></li>
            <li><a href="ventures.html" data-i18n="nav.ventures">Ventures</a></li>
            <li><a href="contact.html" data-i18n="nav.contact">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.more">More</h4>
          <ul>
            <li><a href="board.html" data-i18n="nav.board">Board Advisory</a></li>
            <li><a href="thesis.html" data-i18n="nav.thesis">Leadership Thesis</a></li>
            <li><a href="press.html" data-i18n="nav.press">Press</a></li>
            <li><a href="case-studies.html" data-i18n="nav.caseStudies">Case Studies</a></li>
            <li><a href="career.html" data-i18n="nav.career">Career</a></li>
            <li><a href="recognition.html" data-i18n="nav.recognition">Recognition</a></li>
            <li><a href="brief-ipo.html" data-i18n="nav.briefIpo">Brief: IPO</a></li>
            <li><a href="brief-genetic.html" data-i18n="nav.briefGenetic">Brief: Genetic Data</a></li>
            <li><a href="brief-ai.html" data-i18n="nav.briefAi">Brief: AI Strategy</a></li>
            <li><a href="article-data-infrastructure.html" data-i18n="nav.articleInfra">Data Infrastructure</a></li>
            <li><a href="article-precision-medicine.html" data-i18n="nav.articleHealth">Precision Medicine</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.ventures">Ventures</h4>
          <ul>
            <li><a href="ventures.html">Digital Invest Inc.</a></li>
            <li><a href="ventures.html">Biotechnology Group</a></li>
            <li><a href="ventures.html">XIBI Group</a></li>
            <li><a href="ventures.html">DataPeer Inc.</a></li>
          </ul>
        </div>
        <div class="footer-col footer-write">
          <h4 data-i18n="footer.writeTitle">Write to Me</h4>
          <div class="footer-form">
            <form>
              <input type="email" name="email" required data-i18n-placeholder="footer.writeEmail" placeholder="Your email">
              <textarea name="message" required data-i18n-placeholder="footer.writeMessage" placeholder="Your message"></textarea>
              <button type="submit" class="footer-form-btn" data-i18n="footer.writeSend">Send</button>
            </form>
            <p class="footer-form-success" data-i18n="footer.writeSuccess">Thank you.</p>
          </div>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.connect">Connect</h4>
          <ul>
            <li><a href="contact.html" data-i18n="nav.contact">Contact</a></li>
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

SCRIPTS = """    <script src="js/site-config.js" defer></script>
  <script src="js/i18n-bootstrap.js" defer></script>
  <script src="js/i18n.js?v=2" defer></script>
  <script src="js/forms.js" defer></script>
  <script src="js/cta.js" defer></script>
  <script src="js/analytics.js" defer></script>
  <script src="js/features.js" defer></script>
  <script src="js/main.js" defer></script>
</body>
</html>"""


def deep_merge(target: dict, source: dict) -> None:
    for k, v in source.items():
        if isinstance(v, dict) and isinstance(target.get(k), dict):
            deep_merge(target[k], v)
        else:
            target[k] = v


def merge_translations() -> None:
    expansion = json.loads(EXPANSION.read_text(encoding="utf-8"))
    raw = TRANSLATIONS.read_text(encoding="utf-8")
    start, end = raw.find("{"), raw.rfind("}")
    data = json.loads(raw[start : end + 1])
    for lang in ("en", "ru", "uk"):
        if lang in expansion:
            deep_merge(data.setdefault(lang, {}), expansion[lang])
    out = "const TRANSLATIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    TRANSLATIONS.write_text(out, encoding="utf-8")
    print("merged expansion translations (en, ru, uk)")


def page_head(title: str, desc: str, extra: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="stylesheet" href="css/styles.css">
  <link rel="stylesheet" href="css/expansion.css">
  <link rel="stylesheet" href="css/controls.css">
{extra}  <script src="js/theme.js"></script>
  <script>initThemeEarly();</script>
</head>"""


def wrap_page(page_id: str, body: str, title: str, desc: str, extra_head: str = "") -> str:
    return (
        page_head(title, desc, extra_head)
        + f'\n<body data-page="{page_id}">\n\n'
        + HEADER_STUB
        + "\n"
        + body
        + "\n"
        + FOOTER
        + "\n"
        + SCRIPTS
    )


def board_page() -> str:
    body = """
  <section class="page-hero">
    <div class="container">
      <span class="eyebrow" data-i18n="board.eyebrow">Board & Strategic Advisory</span>
      <h1 data-i18n="board.title">Independent Judgment for Consequential Decisions</h1>
      <div class="gold-line"></div>
      <p class="lead" data-i18n="board.lead">I work with boards, founders, and executive teams.</p>
    </div>
  </section>
  <section class="section section-cream">
    <div class="container">
      <div class="section-header fade-in">
        <span class="eyebrow" data-i18n="board.rolesEyebrow">Ways to Engage</span>
        <h2 data-i18n="board.rolesTitle">Board-Level Partnership</h2>
      </div>
      <div class="expertise-grid">
        <div class="expertise-card fade-in">
          <h3 data-i18n="board.role1title">Independent Director</h3>
          <p data-i18n="board.role1desc">Constructive oversight and long-range perspective.</p>
        </div>
        <div class="expertise-card fade-in">
          <h3 data-i18n="board.role2title">Advisory Board Member</h3>
          <p data-i18n="board.role2desc">Practical guidance on emerging technologies.</p>
        </div>
        <div class="expertise-card fade-in">
          <h3 data-i18n="board.role3title">CEO & Founder Advisor</h3>
          <p data-i18n="board.role3desc">Confidential counsel for leaders at inflection points.</p>
        </div>
        <div class="expertise-card fade-in">
          <h3 data-i18n="board.role4title">Special Committee Advisor</h3>
          <p data-i18n="board.role4desc">Focused support for transactions and diligence.</p>
        </div>
      </div>
    </div>
  </section>
  <section class="section section-white">
    <div class="container container-narrow">
      <div class="section-header-left fade-in">
        <span class="eyebrow" data-i18n="board.valueEyebrow">Perspective</span>
        <h2 data-i18n="board.valueTitle">What I Bring to the Table</h2>
        <div class="gold-line"></div>
      </div>
      <div class="insights-list fade-in">
        <article class="insights-list-item">
          <h3 data-i18n="board.value1title">Operator's Discipline</h3>
          <p data-i18n="board.value1desc">Experience from inception through public markets.</p>
        </article>
        <article class="insights-list-item">
          <h3 data-i18n="board.value2title">Technical Fluency</h3>
          <p data-i18n="board.value2desc">Translate complex systems into board decisions.</p>
        </article>
        <article class="insights-list-item">
          <h3 data-i18n="board.value3title">Cross-Market Judgment</h3>
          <p data-i18n="board.value3desc">Technology, defense, data, and precision medicine.</p>
        </article>
        <article class="insights-list-item">
          <h3 data-i18n="board.value4title">Governance Mindset</h3>
          <p data-i18n="board.value4desc">Fiduciary responsibility and durable value.</p>
        </article>
      </div>
      <p class="lead" style="margin-top:2rem;text-align:center" data-i18n="board.availability">Select engagements considered.</p>
      <p style="text-align:center;margin-top:1.5rem">
        <a href="contact.html?topic=board" class="hero-cta" data-i18n="board.cta">Discuss a Board Mandate</a>
      </p>
    </div>
  </section>"""
    return wrap_page(
        "board",
        body,
        "Board Advisory — Michael Kofman",
        "Board service and strategic advisory from Michael Kofman.",
    )


def thesis_page() -> str:
    items = "".join(
        f"""        <li>
          <span class="thesis-num">{i}</span>
          <div>
            <h3 data-i18n="thesis.b{i}title">Principle</h3>
            <p data-i18n="thesis.b{i}text">Text</p>
          </div>
        </li>\n"""
        for i in range(1, 8)
    )
    rejects = "".join(
        f"""        <article class="insights-list-item">
          <h3 data-i18n="thesis.r{i}title">Reject</h3>
          <p data-i18n="thesis.r{i}text">Text</p>
        </article>\n"""
        for i in range(1, 4)
    )
    body = f"""
  <section class="page-hero">
    <div class="container">
      <span class="eyebrow" data-i18n="thesis.eyebrow">Leadership Thesis</span>
      <h1 data-i18n="thesis.title">Build for the Long Term</h1>
      <div class="gold-line"></div>
      <p class="lead" data-i18n="thesis.lead">Technology changes quickly; leadership obligations do not.</p>
    </div>
  </section>
  <section class="section section-cream">
    <div class="container container-narrow">
      <p class="lead fade-in" data-i18n="thesis.intro">These principles reflect decades of leadership.</p>
      <div class="section-header-left fade-in" style="margin-top:2.5rem">
        <span class="eyebrow" data-i18n="thesis.believeEyebrow">What I Believe</span>
        <h2 data-i18n="thesis.believeTitle">Seven Principles</h2>
        <div class="gold-line"></div>
      </div>
      <ul class="thesis-list fade-in">
{items}      </ul>
    </div>
  </section>
  <section class="section section-white">
    <div class="container container-narrow">
      <div class="section-header-left fade-in">
        <span class="eyebrow" data-i18n="thesis.rejectEyebrow">What I Reject</span>
        <h2 data-i18n="thesis.rejectTitle">Short-Term Thinking</h2>
        <div class="gold-line"></div>
      </div>
      <div class="insights-list fade-in">
{rejects}      </div>
    </div>
  </section>
  <section class="section section-dark">
    <div class="container container-narrow" style="text-align:center">
      <span class="eyebrow" data-i18n="thesis.horizonEyebrow">Looking Ahead</span>
      <h2 data-i18n="thesis.horizonTitle">2026–2030</h2>
      <p class="lead" data-i18n="thesis.horizonText">The convergence of biomathematics, AI, and secure infrastructure.</p>
      <a href="insights.html" class="hero-cta" style="margin-top:1.5rem" data-i18n="nav.insights">Read Insights</a>
    </div>
  </section>"""
    return wrap_page(
        "thesis",
        body,
        "Leadership Thesis — Michael Kofman",
        "Michael Kofman's principles for building durable companies.",
    )


def press_page() -> str:
    body = """
  <section class="page-hero">
    <div class="container">
      <span class="eyebrow" data-i18n="press.eyebrow">Press & Media</span>
      <h1 data-i18n="press.title">Press Archive</h1>
      <div class="gold-line"></div>
      <p class="lead" data-i18n="press.lead">Selected coverage and industry recognition.</p>
      <p style="margin-top:1.25rem"><a href="contact.html?topic=press" class="text-link" data-i18n="contact.inquiryPress">Press inquiries →</a></p>
    </div>
  </section>
  <section class="section section-cream">
    <div class="container container-narrow">
      <div class="press-archive fade-in">
        <div class="press-year-group">
          <h3>2023</h3>
          <div class="press-entry">
            <span class="press-entry-type" data-i18n="press.y2023type">Feature</span>
            <div>
              <h4 data-i18n="press.y2023title">Healthcare Tech Outlook</h4>
              <p data-i18n="press.y2023desc">Digital Invest featured in precision medicine.</p>
              <a href="https://www.healthcaretechoutlook.com/digital-invest-inc" target="_blank" rel="noopener" class="text-link" data-i18n="press.y2023link">Read →</a>
            </div>
          </div>
        </div>
        <div class="press-year-group">
          <h3>2001</h3>
          <div class="press-entry">
            <span class="press-entry-type" data-i18n="press.y2001type">Award</span>
            <div>
              <h4 data-i18n="press.y2001title">Entrepreneur of the Year</h4>
              <p data-i18n="press.y2001desc">Entrepreneur Magazine recognition.</p>
            </div>
          </div>
        </div>
        <div class="press-year-group">
          <h3>1999</h3>
          <div class="press-entry">
            <span class="press-entry-type" data-i18n="press.y1999type">Profile</span>
            <div>
              <h4 data-i18n="press.y1999title">Who's Who in America</h4>
              <p data-i18n="press.y1999desc">National biographical recognition.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>"""
    return wrap_page(
        "press",
        body,
        "Press Archive — Michael Kofman",
        "Press coverage and media references.",
    )


def ip_page() -> str:
    body = """
  <section class="page-hero">
    <div class="container">
      <span class="eyebrow" data-i18n="ip.eyebrow">Intellectual Property</span>
      <h1 data-i18n="ip.title">Patents & Research</h1>
      <div class="gold-line"></div>
      <p class="lead" data-i18n="ip.lead">Innovation across communications, computing, and digital health.</p>
    </div>
  </section>
  <section class="section section-cream">
    <div class="container container-narrow">
      <div class="insights-list fade-in">
        <article class="insights-list-item">
          <div class="insights-list-meta"><span data-i18n="recognition.ip1year">Patent</span></div>
          <h3 data-i18n="recognition.ip1title">Digital Satellite HDTV Systems</h3>
          <p data-i18n="ip.patentIntro">Patent subsequently acquired by Sony Corporation.</p>
        </article>
        <article class="insights-list-item">
          <div class="insights-list-meta"><span data-i18n="recognition.ip2year">Publications</span></div>
          <h3 data-i18n="recognition.ip2title">Technical Papers</h3>
          <p data-i18n="ip.publicationsIntro">Satellite and optical systems for data transmission.</p>
        </article>
        <article class="insights-list-item">
          <div class="insights-list-meta"><span data-i18n="recognition.ip3year">Research</span></div>
          <h3 data-i18n="recognition.ip3title">International Collaborations</h3>
          <p data-i18n="ip.researchIntro">Harvard, Stanford, and cross-industry R&D.</p>
        </article>
      </div>
      <p style="margin-top:2rem;text-align:center"><a href="recognition.html" class="hero-cta" data-i18n="nav.recognition">Full Recognition</a></p>
    </div>
  </section>"""
    return wrap_page(
        "ip",
        body,
        "Intellectual Property — Michael Kofman",
        "Patents and publications by Michael Kofman.",
    )


def deck_page() -> str:
    body = """
  <section class="deck-page">
    <p class="eyebrow">Executive Overview</p>
    <h1 data-i18n="deck.title">Michael Kofman</h1>
    <p class="deck-meta" data-i18n="deck.subtitle">CEO · Board Advisor · Strategic Technologist</p>
    <p class="lead" data-i18n="deck.thesis">Building and advising technology-driven enterprises across the U.S. and Europe.</p>
    <div class="deck-stat-row">
      <div class="deck-stat"><strong>30+</strong><span data-i18n="deck.stat1">Years Leadership</span></div>
      <div class="deck-stat"><strong>$19.5B</strong><span data-i18n="deck.stat2">Peak Acquisition Value</span></div>
      <div class="deck-stat"><strong>8+</strong><span data-i18n="deck.stat3">Companies Founded</span></div>
    </div>
    <p data-i18n="deck.contact">mkofman@mkofman.com · mkofman.com</p>
  </section>"""
    return wrap_page(
        "deck",
        body,
        "Executive Overview — Michael Kofman",
        "Private executive overview.",
        '  <meta name="robots" content="noindex, nofollow">\n',
    )


def brief_page(page_id: str, prefix: str, title: str, desc: str) -> str:
    paras = "".join(
        f'      <p data-i18n="{prefix}.p{i}">Paragraph</p>\n' for i in range(1, 5)
    )
    body = f"""
  <section class="page-hero">
    <div class="container container-narrow">
      <a href="insights.html" class="text-link" data-i18n="articles.backLink">← Back to Insights</a>
      <span class="eyebrow" style="display:block;margin-top:1rem" data-i18n="{prefix}.eyebrow">Executive Brief</span>
      <h1 data-i18n="{prefix}.title">{title}</h1>
      <div class="gold-line"></div>
    </div>
  </section>
  <section class="section section-cream">
    <div class="container container-narrow article-body fade-in">
{paras}    </div>
  </section>"""
    return wrap_page(page_id, body, title, desc)


def generate_pages() -> None:
    pages = {
        "board.html": board_page(),
        "thesis.html": thesis_page(),
        "press.html": press_page(),
        "deck.html": deck_page(),
        "brief-ipo.html": brief_page(
            "briefIpo",
            "briefIpo",
            "What an IPO Changes — Michael Kofman",
            "Executive brief on IPO readiness.",
        ),
        "brief-genetic.html": brief_page(
            "briefGenetic",
            "briefGenetic",
            "Genetic Data to Clinical Decisions — Michael Kofman",
            "Executive brief on genomic intelligence.",
        ),
        "brief-ai.html": brief_page(
            "briefAi",
            "briefAi",
            "AI Strategy Beyond the Pilot — Michael Kofman",
            "Executive brief on enterprise AI.",
        ),
    }
    for name, html in pages.items():
        (ROOT / name).write_text(html, encoding="utf-8")
        print(f"generated {name}")


def ensure_assets(html: str) -> str:
    if "expansion.css" not in html:
        html = html.replace(
            '<link rel="stylesheet" href="css/styles.css">',
            '<link rel="stylesheet" href="css/styles.css">\n  <link rel="stylesheet" href="css/expansion.css">',
            1,
        )
    if "features.js" not in html and "main.js" in html:
        html = html.replace(
            '<script src="js/main.js"',
            '<script src="js/features.js" defer></script>\n  <script src="js/main.js"',
            1,
        )
    if 'rel="alternate" type="application/rss+xml"' not in html and "<head>" in html:
        html = html.replace(
            "<head>",
            '<head>\n  <link rel="alternate" type="application/rss+xml" title="Michael Kofman Insights" href="/feed.xml">',
            1,
        )
    return html


def patch_index(html: str) -> str:
    if "testimonials-grid" in html:
        return html
    testimonials = """
  <section class="section section-white">
    <div class="container">
      <div class="section-header fade-in">
        <span class="eyebrow" data-i18n="home.testimonialsEyebrow">Endorsements</span>
        <h2 data-i18n="home.testimonialsTitle">What Leaders Say</h2>
      </div>
      <div class="testimonials-grid">
        <article class="testimonial-card fade-in">
          <blockquote data-i18n="testimonials.t1quote">Quote</blockquote>
          <footer><strong data-i18n="testimonials.t1name">Name</strong><span data-i18n="testimonials.t1role">Role</span></footer>
        </article>
        <article class="testimonial-card fade-in">
          <blockquote data-i18n="testimonials.t2quote">Quote</blockquote>
          <footer><strong data-i18n="testimonials.t2name">Name</strong><span data-i18n="testimonials.t2role">Role</span></footer>
        </article>
        <article class="testimonial-card fade-in">
          <blockquote data-i18n="testimonials.t3quote">Quote</blockquote>
          <footer><strong data-i18n="testimonials.t3name">Name</strong><span data-i18n="testimonials.t3role">Role</span></footer>
        </article>
      </div>
    </div>
  </section>"""
    board_cta = """
  <section class="section section-dark board-cta-strip">
    <div class="container container-narrow fade-in">
      <span class="eyebrow" data-i18n="home.boardCtaEyebrow">Board & Advisory</span>
      <h2 data-i18n="home.boardCtaTitle">Available for Select Board Mandates</h2>
      <p class="lead" data-i18n="home.boardCtaLead">Independent director and strategic advisory roles.</p>
      <a href="board.html" class="hero-cta" data-i18n="home.boardCtaBtn">Learn More</a>
    </div>
  </section>"""
    video = """
  <section class="section section-cream">
    <div class="container container-narrow" style="text-align:center">
      <span class="eyebrow" data-i18n="home.videoEyebrow">Executive Perspective</span>
      <h2 data-i18n="home.videoTitle">Vision & Leadership</h2>
      <p class="lead" data-i18n="home.videoLead">A message on technology, medicine, and building for the long term.</p>
      <div class="video-hero-slot">
        <img src="images/portrait-hero-3.png" alt="" loading="lazy" width="800" height="600">
      </div>
      <p style="margin-top:1rem"><a href="thesis.html" class="text-link" data-i18n="home.videoCta">Read Leadership Thesis →</a></p>
    </div>
  </section>"""
    # Insert board CTA after press-band
    if 'class="press-band"' in html and "board-cta-strip" not in html:
        html = html.replace(
            '</section>\n\n  <section class="section section-cream">\n    <div class="container">\n      <div class="about-preview',
            '</section>\n' + board_cta + '\n  <section class="section section-cream">\n    <div class="container">\n      <div class="about-preview',
            1,
        )
    # Before footer: testimonials + video
    if "testimonials-grid" not in html:
        html = html.replace("    <footer class=\"site-footer\">", testimonials + video + '\n    <footer class="site-footer">', 1)
    return html


def patch_career(html: str) -> str:
    if "filter-bar" in html:
        return html
    filters = """
      <div class="filter-bar fade-in" data-filter-target=".timeline-item">
        <button type="button" class="filter-btn is-active" data-filter="all" data-i18n="career.filterAll">All</button>
        <button type="button" class="filter-btn" data-filter="healthcare" data-i18n="career.filterHealthcare">Healthcare</button>
        <button type="button" class="filter-btn" data-filter="infrastructure" data-i18n="career.filterInfrastructure">Infrastructure</button>
        <button type="button" class="filter-btn" data-filter="defense" data-i18n="career.filterDefense">Defense & Gov</button>
        <button type="button" class="filter-btn" data-filter="telecom" data-i18n="career.filterTelecom">Telecom</button>
      </div>"""
    html = html.replace('<div class="timeline fade-in">', filters + '\n      <div class="timeline fade-in">', 1)
    tag_map = [
        ("career.t1year", "healthcare infrastructure"),
        ("career.t2year", "defense infrastructure"),
        ("career.t3year", "healthcare"),
        ("career.t4year", "telecom infrastructure"),
        ("career.t5year", "infrastructure"),
        ("career.t6year", "infrastructure"),
        ("career.t7year", "infrastructure telecom"),
        ("career.t8year", "infrastructure"),
        ("career.t9year", "telecom defense"),
        ("career.t10year", "defense"),
    ]
    for key, tags in tag_map:
        needle = f'<div class="timeline-item">\n          <div class="timeline-year" data-i18n="{key}"'
        repl = f'<div class="timeline-item" data-tags="{tags}">\n          <div class="timeline-year" data-i18n="{key}"'
        html = html.replace(needle, repl, 1)
    return html


def patch_ventures(html: str) -> str:
    if "ecosystem-map" in html:
        return html
    ecosystem = """
  <section class="section section-white">
    <div class="container">
      <div class="section-header fade-in">
        <span class="eyebrow" data-i18n="ventures.ecosystemEyebrow">Portfolio Ecosystem</span>
        <h2 data-i18n="ventures.ecosystemTitle">Connected Innovation</h2>
        <p class="lead" data-i18n="ventures.ecosystemLead">How ventures align across precision medicine, data, and robotics.</p>
      </div>
      <div class="ecosystem-map fade-in" aria-hidden="true">
        <svg viewBox="0 0 400 320" role="img" aria-label="Venture ecosystem">
          <line class="ecosystem-line" x1="200" y1="160" x2="200" y2="60"/>
          <line class="ecosystem-line" x1="200" y1="160" x2="80" y2="220"/>
          <line class="ecosystem-line" x1="200" y1="160" x2="320" y2="220"/>
          <line class="ecosystem-line" x1="200" y1="160" x2="120" y2="100"/>
          <line class="ecosystem-line" x1="200" y1="160" x2="280" y2="100"/>
          <circle class="ecosystem-node ecosystem-node--hub" cx="200" cy="160" r="36"/>
          <text class="ecosystem-label" x="200" y="165">Digital Invest</text>
          <circle class="ecosystem-node" cx="200" cy="60" r="28"/>
          <text class="ecosystem-label" x="200" y="64" fill="#0c1829">BioMath</text>
          <circle class="ecosystem-node" cx="80" cy="220" r="28"/>
          <text class="ecosystem-label" x="80" y="224" fill="#0c1829">Human Model</text>
          <circle class="ecosystem-node" cx="320" cy="220" r="28"/>
          <text class="ecosystem-label" x="320" y="224" fill="#0c1829">Aero-Ground</text>
          <circle class="ecosystem-node" cx="120" cy="100" r="22"/>
          <text class="ecosystem-label" x="120" y="104" fill="#0c1829" font-size="9">XIBI</text>
          <circle class="ecosystem-node" cx="280" cy="100" r="22"/>
          <text class="ecosystem-label" x="280" y="104" fill="#0c1829" font-size="9">Biotech</text>
        </svg>
      </div>
    </div>
  </section>"""
    html = html.replace(
        '<span class="venture-highlight" data-i18n="ventures.v1highlight">',
        '<span class="venture-highlight" data-i18n="ventures.v1highlight">',
        1,
    )
    if "ventures.v1lesson" not in html:
        html = html.replace(
            '</span>\n          </div>\n        </article>\n\n        <article class="venture-card fade-in">\n          <div class="venture-card-header">\n            <div class="venture-year" data-period-start="2008"',
            '</span>\n            <p class="venture-lesson" data-i18n="ventures.v1lesson">Lesson</p>\n          </div>\n        </article>\n\n        <article class="venture-card fade-in" data-tags="healthcare">\n          <span class="venture-status" data-i18n="ventures.statusLegacy">Legacy</span>\n          <div class="venture-card-header">\n            <div class="venture-year" data-period-start="2008"',
            1,
        )
        html = html.replace(
            '<article class="venture-card fade-in">\n          <div class="venture-card-header">\n            <div class="venture-year" data-period-start="2021"',
            '<article class="venture-card fade-in" data-tags="healthcare infrastructure">\n          <span class="venture-status" data-i18n="ventures.statusActive">Active</span>\n          <div class="venture-card-header">\n            <div class="venture-year" data-period-start="2021"',
            1,
        )
        html = html.replace(
            'data-i18n="ventures.v2highlight">Harvard Medical School & Stanford Biomath Partner</span>\n          </div>\n        </article>',
            'data-i18n="ventures.v2highlight">Harvard Medical School & Stanford Biomath Partner</span>\n            <p class="venture-lesson" data-i18n="ventures.v2lesson">Lesson</p>\n          </div>\n        </article>',
            1,
        )
        html = html.replace(
            '<article class="venture-card fade-in">\n          <div class="venture-card-header">\n            <div class="venture-year" data-period-start="1996"',
            '<article class="venture-card fade-in" data-tags="infrastructure telecom">\n          <span class="venture-status" data-i18n="ventures.statusExited">Exited</span>\n          <div class="venture-card-header">\n            <div class="venture-year" data-period-start="1996"',
            1,
        )
        html = html.replace(
            'data-i18n="ventures.v5highlight">Acquired · Peak Value $19.5 Billion</span>\n          </div>\n        </article>',
            'data-i18n="ventures.v5highlight">Acquired · Peak Value $19.5 Billion</span>\n            <p class="venture-lesson" data-i18n="ventures.v5lesson">Lesson</p>\n          </div>\n        </article>',
            1,
        )
    html = html.replace("</section>\n\n    <footer", ecosystem + "\n  </section>\n\n    <footer", 1)
    return html


def patch_speaking(html: str) -> str:
    if "topic-catalog" in html:
        return html
    rows = "".join(
        f"""        <div class="topic-row fade-in">
          <h3 data-i18n="speaking.t{i}title">Topic</h3>
          <span class="topic-audience" data-i18n="speaking.t{i}audience">Audience</span>
          <span class="topic-format" data-i18n="speaking.t{i}format">Keynote</span>
        </div>\n"""
        for i in range(1, 9)
    )
    block = f"""
  <section class="section section-white">
    <div class="container">
      <div class="section-header fade-in">
        <span class="eyebrow" data-i18n="speaking.catalogEyebrow">Speaking Catalog</span>
        <h2 data-i18n="speaking.catalogTitle">Topics & Formats</h2>
        <p class="lead" data-i18n="speaking.catalogLead">Keynotes, panels, and executive workshops.</p>
      </div>
      <div class="topic-catalog fade-in">
{rows}      </div>
      <p style="text-align:center;margin-top:2rem">
        <a href="contact.html?topic=speaking" class="hero-cta" data-i18n="consulting.cta">Contact Michael Kofman</a>
        <a href="media-kit.html" class="text-link" style="margin-left:1.5rem" data-i18n="nav.mediaKit">Media Kit</a>
      </p>
    </div>
  </section>"""
    return html.replace("</footer>", block + "\n  </footer>", 1)


def patch_insights(html: str) -> str:
    if "brief-card" in html:
        return html
    briefs = """
  <section class="section section-white">
    <div class="container">
      <div class="section-header fade-in">
        <span class="eyebrow" data-i18n="insights.briefsEyebrow">Executive Briefs</span>
        <h2 data-i18n="insights.briefsTitle">Short-Form Perspectives</h2>
        <p class="lead" data-i18n="insights.briefsLead">Concise analysis for boards and executive teams.</p>
      </div>
      <div class="insights-grid insights-grid--2">
        <article class="brief-card fade-in">
          <span class="brief-tag" data-i18n="insights.brief1tag">Capital Markets</span>
          <h3 data-i18n="insights.brief1title">What an IPO Changes</h3>
          <p data-i18n="insights.brief1desc">Operating discipline before and after going public.</p>
          <a href="brief-ipo.html" class="text-link">Read →</a>
        </article>
        <article class="brief-card fade-in">
          <span class="brief-tag" data-i18n="insights.brief2tag">Digital Health</span>
          <h3 data-i18n="insights.brief2title">Genetic Data to Decisions</h3>
          <p data-i18n="insights.brief2desc">Responsible clinical intelligence from genomic data.</p>
          <a href="brief-genetic.html" class="text-link">Read →</a>
        </article>
        <article class="brief-card fade-in">
          <span class="brief-tag" data-i18n="insights.brief3tag">Enterprise AI</span>
          <h3 data-i18n="insights.brief3title">AI Beyond the Pilot</h3>
          <p data-i18n="insights.brief3desc">Governed, measurable AI at enterprise scale.</p>
          <a href="brief-ai.html" class="text-link">Read →</a>
        </article>
      </div>
    </div>
  </section>"""
    reading = """
  <section class="section section-cream">
    <div class="container container-narrow">
      <div class="section-header-left fade-in">
        <span class="eyebrow" data-i18n="insights.readingEyebrow">Reading List</span>
        <h2 data-i18n="insights.readingTitle">Books That Shape My Thinking</h2>
        <div class="gold-line"></div>
      </div>
      <ul class="reading-list fade-in">
        <li><span data-i18n="insights.r1title">Book</span><span class="reading-author" data-i18n="insights.r1author">Author</span></li>
        <li><span data-i18n="insights.r2title">Book</span><span class="reading-author" data-i18n="insights.r2author">Author</span></li>
        <li><span data-i18n="insights.r3title">Book</span><span class="reading-author" data-i18n="insights.r3author">Author</span></li>
        <li><span data-i18n="insights.r4title">Book</span><span class="reading-author" data-i18n="insights.r4author">Author</span></li>
        <li><span data-i18n="insights.r5title">Book</span><span class="reading-author" data-i18n="insights.r5author">Author</span></li>
      </ul>
    </div>
  </section>"""
    newsletter = """
  <section class="section section-white">
    <div class="container container-narrow">
      <div class="newsletter-box fade-in">
        <span class="eyebrow" data-i18n="insights.newsletterEyebrow">Stay Informed</span>
        <h2 data-i18n="insights.newsletterTitle">Executive Updates</h2>
        <p class="lead" data-i18n="insights.newsletterLead">Occasional perspectives on technology, health, and leadership.</p>
        <a href="contact.html" class="hero-cta" data-i18n="insights.newsletterCta">Request Updates</a>
      </div>
    </div>
  </section>"""
    html = html.replace(
        '<section class="section section-cream">\n    <div class="container container-narrow">\n      <div class="insights-intro',
        briefs
        + '\n  <section class="section section-cream">\n    <div class="container container-narrow">\n      <div class="insights-intro',
        1,
    )
    html = html.replace("</footer>", reading + newsletter + "\n  </footer>", 1)
    return html


def patch_about(html: str) -> str:
    if "principles-grid" in html:
        return html
    block = """
  <section class="section section-white">
    <div class="container">
      <div class="section-header fade-in">
        <span class="eyebrow" data-i18n="about.principlesEyebrow">Personal Principles</span>
        <h2 data-i18n="about.principlesTitle">How I Lead</h2>
      </div>
      <div class="principles-grid">
        <article class="principle-card fade-in">
          <h3 data-i18n="about.p1title">Principle</h3>
          <p data-i18n="about.p1text">Text</p>
        </article>
        <article class="principle-card fade-in">
          <h3 data-i18n="about.p2title">Principle</h3>
          <p data-i18n="about.p2text">Text</p>
        </article>
        <article class="principle-card fade-in">
          <h3 data-i18n="about.p3title">Principle</h3>
          <p data-i18n="about.p3text">Text</p>
        </article>
      </div>
      <p style="text-align:center;margin-top:2rem"><a href="thesis.html" class="text-link" data-i18n="nav.thesis">Full Leadership Thesis →</a></p>
    </div>
  </section>"""
    return html.replace("</footer>", block + "\n  </footer>", 1)


def patch_contact(html: str) -> str:
    if "calendly-embed" in html:
        return html
    block = """
  <section class="section section-white">
    <div class="container container-narrow">
      <div class="section-header fade-in">
        <span class="eyebrow" data-i18n="contact.calendlyEyebrow">Schedule</span>
        <h2 data-i18n="contact.calendlyTitle">Book an Introductory Call</h2>
        <p class="lead" data-i18n="contact.calendlyLead">For board, speaking, and advisory inquiries.</p>
      </div>
      <div id="calendly-embed" class="calendly-embed fade-in"></div>
    </div>
  </section>"""
    return html.replace("</footer>", block + "\n  </footer>", 1)


def patch_media_kit(html: str) -> str:
    if "brand-swatches" in html:
        return html
    block = """
  <section class="section section-white">
    <div class="container container-narrow">
      <div class="section-header-left fade-in">
        <span class="eyebrow" data-i18n="mediaKit.brandEyebrow">Brand Assets</span>
        <h2 data-i18n="mediaKit.brandTitle">Logo & Colors</h2>
        <p class="lead" data-i18n="mediaKit.brandLead">Official palette for press and event materials.</p>
        <div class="gold-line"></div>
      </div>
      <div class="brand-swatches fade-in">
        <div class="brand-swatch brand-swatch--navy" title="Navy #0c1829"></div>
        <div class="brand-swatch brand-swatch--gold" title="Gold #c4a265"></div>
        <div class="brand-swatch brand-swatch--cream" title="Cream #f8f6f2"></div>
      </div>
      <p data-i18n="mediaKit.brandColors">Navy · Gold · Cream</p>
      <p style="margin-top:1rem"><a href="favicon.svg" download class="text-link" data-i18n="mediaKit.brandLogo">Download logo (SVG)</a></p>
      <p><a href="downloads/michael-kofman-media-kit.pdf" download class="hero-cta" style="margin-top:1rem;display:inline-block" data-i18n="mediaKit.brandDownload">Download Media Kit PDF</a></p>
    </div>
  </section>"""
    return html.replace(
        '<section class="section section-cream">\n    <div class="container container-narrow">\n      <div class="consulting-intro',
        block
        + '\n  <section class="section section-cream">\n    <div class="container container-narrow">\n      <div class="consulting-intro',
        1,
    )


PATCHERS = {
    "index.html": patch_index,
    "career.html": patch_career,
    "ventures.html": patch_ventures,
    "insights.html": patch_insights,
    "about.html": patch_about,
    "contact.html": patch_contact,
}


def patch_existing() -> None:
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".html"):
            continue
        path = ROOT / name
        html = path.read_text(encoding="utf-8")
        html = ensure_assets(html)
        if name in PATCHERS:
            html = PATCHERS[name](html)
        path.write_text(html, encoding="utf-8")
    print("patched existing HTML pages")


def main() -> None:
    merge_translations()
    generate_pages()
    patch_existing()
    print("expansion applied — run fix_nav.py and build_site.py next")


if __name__ == "__main__":
    main()
