#!/usr/bin/env python3
"""Generate the two representative preview pages from one shared definition of
header / navigation / footer. All page text below is copied verbatim from the
live site (audit/baseline/text/*.txt); tools/verify_preview.py checks that."""
import html, pathlib, sys

OUT = pathlib.Path(__file__).resolve().parent.parent / "preview"
SITE = "https://globalwms.com"
DESC = "Global investors deserve better - now you can provide it"  # existing, unchanged

# --- navigation (labels verbatim from the live menus) -------------------------------------
FUNDS_MENU = [  # group order: Multi Asset, Equities, Fixed Interest, Alternative Strategies
    ("Multi Asset", [
        ("1OAK Multi Asset (MA80) Fund (Growth)", "/1oak-multi-asset-funds-guided-by-blackrock"),
        ("EPIC Wealth Fund (Balanced)", "/epic-investment-partners")]),
    ("Equities", [
        ("ASK Indian Entrepreneur Fund", "/ask-capital-india-entrepreneur-fund"),
        ("Pecora Chatrier Equity (Value)", "/pecora-chatrier-equity-value")]),
    ("Fixed Interest", [
        ("Pecora Manning & Napier High Yield Bond Strategy", "/pecora-manning-napier-high-yield-bond-strategy")]),
    ("Alternative Strategies", [
        ("Levendi Thornbridge Defined Return Fund", "/levendi-thornbridge-defined-return-fund"),
        ("Pecora QMS", "/pecora-qms")]),
]
ABOUT_MENU = [
    ("About GWMS", [("About GWMS", "/about-gwms"), ("Meet the team", "/meet-the-team")]),
    ("Regions", [("Africa", "/africa"), ("Americas & Caribbean", "/americas-caribbean"), ("Asia", "/asia"),
                 ("Europe", "/europe"), ("Middle East", "/middle-east")]),
]
# Fund-page side navigation (labels verbatim from the live side menu)
SIDE_NAV = [
    ("Multi Asset", [("1OAK Multi Asset (MA80) Fund (Growth)", "/1oak-multi-asset-funds-guided-by-blackrock"),
                     ("EPIC Wealth Fund (Balanced)", "/epic-investment-partners")]),
    ("Equities", [("ASK Capital India Entrepreneur Fund", "/ask-capital-india-entrepreneur-fund"),
                  ("Pecora Chatrier Equity (Value)", "/pecora-chatrier-equity-value")]),
    ("Fixed Interest", [("Pecora Manning & Napier High Yield Bond Strategy", "/pecora-manning-napier-high-yield-bond-strategy")]),
    ("Alternative Strategies", [("Levendi Thornbridge Defined Return Fund", "/levendi-thornbridge-defined-return-fund"),
                                ("Pecora QMS", "/pecora-qms")]),
]
REG = "GLOBAL WEALTH MANAGEMENT SOLUTIONS LLP IS AUTHORISED AND REGULATED BY THE FINANCIAL CONDUCT AUTHORITY REF:678746."
e = html.escape


def links(items, current):
    out = []
    for label, href in items:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'<li><a href="{href}"{cur}>{e(label, quote=False)}</a></li>')
    return "\n".join(out)


def panel(pid, title, groups, current):
    gs = []
    for i, (label, items) in enumerate(groups):
        gid = f"{pid}-g{i}"
        gs.append(f'''<div class="mega__group">
  <p class="mega__label" id="{gid}"><span class="motif" aria-hidden="true"></span>{e(label, quote=False)}</p>
  <ul class="mega__list" aria-labelledby="{gid}">
{links(items, current)}
  </ul>
</div>''')
    return f'''<div class="mega" id="{pid}" role="group" aria-labelledby="{pid}-btn">
  <div class="mega__inner">
    <p class="mega__title" aria-hidden="true"><span class="motif"></span>{e(title)}</p>
    <div class="mega__groups">
{chr(10).join(gs)}
    </div>
  </div>
</div>'''


def header(current, section=None):
    def top_link(label, href):
        cur = ' aria-current="page"' if href == current else ""
        return f'<li class="site-nav__item"><a class="site-nav__link" href="{href}"{cur}>{label}</a></li>'

    def top_panel(pid, label, groups):
        sec = ' data-section="current"' if section == pid else ""
        return f'''<li class="site-nav__item">
  <button type="button" class="site-nav__link" id="{pid}-btn" aria-expanded="false" aria-controls="{pid}"{sec}>{label}<span class="chev" aria-hidden="true"></span></button>
{panel(pid, label, groups, current)}
</li>'''

    return f'''<header class="site-header">
  <div class="site-header__bar container">
    <a class="brand" href="/"><img src="/img/logo-gwms.svg" width="376" height="89" alt="Global Wealth Management Solutions — home"></a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span>Menu</span><span class="nav-toggle__icon" aria-hidden="true"></span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul class="site-nav__list">
        <li class="site-nav__item site-nav__item--home"><a class="site-nav__link" href="/"{' aria-current="page"' if current == "/" else ""}>Home</a></li>
        {top_link("Platforms", "/platforms")}
        {top_panel("funds", "Funds", FUNDS_MENU)}
        {top_link("Investment Management Solutions", "/investment-management-solutions")}
        {top_link("Structured Products", "/structured-products")}
        {top_panel("about", "About us", ABOUT_MENU)}
        {top_link("Contact", "/contact")}
      </ul>
    </nav>
  </div>
</header>'''


FOOTER = f'''<footer class="site-footer on-dark">
  <div class="container site-footer__inner">
    <img class="site-footer__mark" src="/img/gw-icon.svg" width="78" height="83" alt="">
    <p class="site-footer__reg">{e(REG)}</p>
    <ul class="site-footer__links" aria-label="Legal">
      <li><a href="/privacy-notice">Privacy Notice</a></li>
      <li><a href="/disclaimer">Disclaimer</a></li>
      <li><a href="/cookie-information">Cookie Information</a></li>
    </ul>
  </div>
</footer>'''


def page(title, path, body, section=None, extra_head="", footer=None, extra_scripts=""):
    return f'''<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" type="image/png" sizes="32x32" href="/img/gw-icon.png">
<link rel="stylesheet" href="/css/tokens.css">
<link rel="stylesheet" href="/css/base.css">
<link rel="stylesheet" href="/css/components.css">
<script src="/js/init.js"></script>
{extra_head}</head>
<body id="top">
<a class="skip-link" href="#main">Skip to main content</a>
{header(path, section)}
<main id="main">
{body}
</main>
{footer or FOOTER}
<script src="/js/nav.js" defer></script>
{extra_scripts}
</body>
</html>
'''


HOME = '''<section class="hero on-dark" aria-labelledby="home-title">
  <picture class="hero__media">
    <source type="image/webp" srcset="/img/hero-800.webp 800w, /img/hero-1280.webp 1280w, /img/hero-1920.webp 1920w" sizes="100vw">
    <img src="/img/hero-1280.webp" width="1280" height="928" alt="" fetchpriority="high">
  </picture>
  <div class="container hero__inner">
    <span class="motif" aria-hidden="true"></span>
    <h1 class="hero__title" id="home-title">Creating <br>long-term value</h1>
  </div>
</section>
<section class="statement">
  <div class="container statement__grid">
    <h2 class="statement__lead">Our portfolio comprises ‘best-of-breed’ solutions to meet the needs of discerning intermediaries and their investors.</h2>
    <ul class="index">
      <li><a href="/levendi-thornbridge-defined-return-fund"><span>Funds</span></a></li>
      <li><a href="/investment-management-solutions"><span>Investment Management Solutions</span></a></li>
      <li><a href="/structured-products"><span>Structured Products</span></a></li>
    </ul>
  </div>
</section>'''


def side_nav(current):
    parts = []
    for label, items in SIDE_NAV:
        parts.append(f'<p class="side-nav__label"><span class="motif" aria-hidden="true"></span>{e(label)}</p>\n<ul>\n{links(items, current)}\n</ul>')
    return '<nav class="side-nav" aria-label="Funds">\n' + "\n".join(parts) + "\n</nav>"


ASK_PATH = "/ask-capital-india-entrepreneur-fund"
ASK = f'''<div class="container page">
  <div class="page__layout">
{side_nav(ASK_PATH)}
    <article>
      <header class="page-header">
        <h1>ASK Indian Entrepreneur Fund</h1>
        <img class="page-header__logo" src="/img/fund-ask-web.png" width="250" height="74" alt="ASK Capital">
      </header>
      <div class="prose">
<p>ASK Capital, a subsidiary of ASK Investment Managers (“ASK”), is a boutique India-specialist investment manager. ASK is one of the leading asset and wealth management companies in India, with an AUM of ~USD 10.1 billion<a class="fn-ref" href="#_ftn1" id="_ftnref1"><sup>[1]</sup></a>. </p>
<p>ASK is a portfolio company of Blackstone owned funds, who bought a majority stake in the firm in February 2022 <a href="https://www.blackstone.com/news/press/blackstone-acquires-a-majority-stake-in-ask-investment-managers-indias-leading-asset-and-wealth-management-company/" target="_blank" rel="noopener"><strong>(LINK).</strong><span class="sr-only"> External site: blackstone.com. Opens in a new tab.</span></a></p>
<h2>Why India?</h2>
<p>India is one of the most exciting long-term markets for any global investor today. The country is not just the 5<sup>th</sup> largest in the world by GDP, but also the 5<sup>th</sup> largest by market-cap. With a population of over 1.4 billion people, a median age of just 29 years, several crucial structural reforms already implemented, a per-capita GDP over the inflection point of USD 2,000, a stable democracy, and a potent combination of under-penetration across sectors and high-aspirations across citizens, the opportunity is undeniable.</p>
<h2>ASK Indian Entrepreneur Strategy</h2>
<ul>
<li>USD 2.4 billion in AUM, across multiple vehicles, including a UCITS</li>
<li>Track record of over 13 years.</li>
<li>Portfolio Highlights
<ul>
<li>Low turnover (~20-25%)</li>
<li>High conviction (~4-5% position weights),</li>
<li>Concentrated (~20-25 stocks)</li>
</ul>
</li>
<li>ASK invests into Indian entrepreneurial businesses with large size of opportunity, superior quality (capital efficiency) and high growth at fair valuations.</li>
<li>Entrepreneur-run companies are among the largest wealth creators in India. This makes such a portfolio an excellent way to access the country’s growth potential.</li>
<li>ASK Indian Entrepreneur Fund is a Dublin based daily dealing ICAV.</li>
</ul>
      </div>
      <section class="footnotes" aria-labelledby="fn-title">
        <h2 class="sr-only" id="fn-title">Footnotes</h2>
        <p id="_ftn1"><a class="fn-ref" href="#_ftnref1"><sup>[1]</sup></a> as of 31 July 2023</p>
      </section>
    </article>
  </div>
</div>'''


def portable(content, depth):
    """Rewrite root-relative URLs so the pages open straight from disk (file://) and on any host.
    Assets -> relative path; page links -> relative path to <page>/index.html."""
    import re
    up = "../" * depth
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"/(css|js|img|fonts)/", url):
            return f'{attr}="{up}{url[1:]}"'
        if url == "/":
            return f'{attr}="{up}index.html"'
        return f'{attr}="{up}{url.strip("/")}/index.html"'
    content = re.sub(r'\b(href|src)="(/[^"/][^"]*|/)"', fix, content)
    return re.sub(r'(/img/[^ ",]+)( \d+w)', lambda m: up + m.group(1)[1:] + m.group(2), content)


def write(rel, content):
    content = portable(content, rel.count("/"))
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------------------
# CONCEPT HOME (draft for approval; not the approved design). New copy is marked in
# docs/08-concept-home.md. Everything else is existing GWMS text/labels.
# ---------------------------------------------------------------------------------------
CARDS = [  # (group, name as in menu, url, logo file, logo alt)
    ("Multi Asset", "1OAK Multi Asset (MA80) Fund (Growth)", "/1oak-multi-asset-funds-guided-by-blackrock", "1oak-white.svg", "1OAK"),
    ("Multi Asset", "EPIC Wealth Fund (Balanced)", "/epic-investment-partners", "epic-white.svg", "EPIC Investment Partners"),
    ("Equities", "ASK Indian Entrepreneur Fund", "/ask-capital-india-entrepreneur-fund", "ask-white.svg", "ASK Investment Managers"),
    ("Equities", "Pecora Chatrier Equity (Value)", "/pecora-chatrier-equity-value", "pecora-capital-white.svg", "Pecora Capital"),
    ("Fixed Interest", "Pecora Manning & Napier High Yield Bond Strategy", "/pecora-manning-napier-high-yield-bond-strategy", "pecora-capital-white.svg", "Pecora Capital"),
    ("Alternative Strategies", "Levendi Thornbridge Defined Return Fund", "/levendi-thornbridge-defined-return-fund", "levendi-thornbridge-white.svg", "Causeway Securities"),
    ("Alternative Strategies", "Pecora QMS", "/pecora-qms", "pecora-capital-white.svg", "Pecora Capital"),
]
cards_html = "\n".join(
    f'''<li><a class="card" href="{u}"><span class="card__logo{' card__logo--mark' if lg.endswith('.svg') else ''}"><img src="/img/funds/{lg}" alt="{e(alt)}" loading="lazy"></span>
<span class="card__group">{e(g)}</span><span class="card__name">{e(n, quote=False)}</span></a></li>'''
    for g, n, u, lg, alt in CARDS)

CONCEPT = f'''<div class="frame">
<section class="hero hero--framed gradient on-dark" aria-labelledby="home-title">
  <picture class="hero__media">
    <source type="image/webp" srcset="/img/hero-800.webp 800w, /img/hero-1280.webp 1280w, /img/hero-1920.webp 1920w" sizes="100vw">
    <img src="/img/hero-1280.webp" width="1280" height="928" alt="" fetchpriority="high">
  </picture>
  <div class="container hero__inner">
    <h1 class="hero__title" id="home-title"><span class="motif" aria-hidden="true"></span>Creating <br>long-term value</h1>
  </div>
</section>
</div>
<section class="statement statement--plain">
  <div class="container statement__grid">
    <div class="statement__text">
      <h2 class="statement__lead"><span class="motif" aria-hidden="true"></span>Our portfolio comprises ‘best-of-breed’ solutions to meet the needs of discerning intermediaries and their investors.</h2>
    </div>
    <ul class="index">
      <li><a href="/platforms"><span>Platforms</span></a></li>
      <li><a href="/levendi-thornbridge-defined-return-fund"><span>Funds</span></a></li>
      <li><a href="/investment-management-solutions"><span>Investment Management Solutions</span></a></li>
      <li><a href="/structured-products"><span>Structured Products</span></a></li>
    </ul>
  </div>
</section>
<section class="funds" aria-labelledby="funds-title">
  <div class="frame">
    <div class="funds__panel gradient on-dark">
      <div class="funds__head">
        <h2 class="funds__title" id="funds-title"><span class="motif" aria-hidden="true"></span>Funds</h2>
        <div class="funds__controls">
          <button type="button" class="carousel-btn carousel-btn--prev" data-carousel-prev aria-label="Previous funds"><span class="chev" aria-hidden="true"></span></button>
          <button type="button" class="carousel-btn carousel-btn--next" data-carousel-next aria-label="Next funds"><span class="chev" aria-hidden="true"></span></button>
        </div>
      </div>
      <ul class="cards" data-carousel tabindex="0" aria-label="Funds, scrollable list">
{cards_html}
      </ul>
    </div>
  </div>
</section>
<section class="about" aria-labelledby="about-title">
  <div class="container about__grid">
    <div class="about__photo"><img src="/img/about-glass-1200.webp" srcset="/img/about-glass-700.webp 700w, /img/about-glass-1200.webp 1200w" sizes="(min-width: 60rem) 45vw, 100vw" width="1200" height="800" alt="" loading="lazy"></div>
    <div>
      <p class="label about__label"><span class="motif" aria-hidden="true"></span><span id="about-title">About us</span></p>
      <p class="about__statement">Providing access to best of breed financial products since 2003.</p>
      <p class="about__text">Trusted by banks, institutions, captives, trust companies, family offices and boutique fund managers for market knowledge, service and track record.</p>
      <a class="text-link" href="/about-gwms">About GWMS</a>
    </div>
  </div>
</section>'''


def foot_col(title, groups):
    out = [f'<div class="footer-col"><h2><span class="motif" aria-hidden="true"></span>{e(title)}</h2>']
    for label, items in groups:
        if label:
            out.append(f'<h3>{e(label)}</h3>')
        out.append("<ul>" + "".join(f'<li><a href="{h}">{e(t, quote=False)}</a></li>' for t, h in items) + "</ul>")
    return "\n".join(out) + "</div>"


CONCEPT_FOOTER = f'''<footer class="site-footer site-footer--wide on-dark">
  <div class="frame">
    <div class="footer-panel gradient">
      <div class="footer-top">
        <div class="footer-brand"><a class="footer-logo" href="/"><img src="/img/logo-gwms-white.svg" width="2362" height="495" alt="Global Wealth Management Solutions — home"></a>
          <p class="footer-strap">Creating long-term value</p></div>
        <nav class="footer-nav" aria-label="Footer">
          <ul>
            <li><a href="/platforms">Platforms</a></li>
            <li><a href="/levendi-thornbridge-defined-return-fund">Funds</a></li>
            <li><a href="/investment-management-solutions">Investment Management Solutions</a></li>
            <li><a href="/structured-products">Structured Products</a></li>
          </ul>
        </nav>
        <ul class="footer-legal" aria-label="Legal">
          <li><a href="/privacy-notice">Privacy Notice</a></li>
          <li><a href="/disclaimer">Disclaimer</a></li>
          <li><a href="/cookie-information">Cookie Information</a></li>
        </ul>
        <div class="footer-side">
        <a class="footer-social" href="https://www.linkedin.com/company/gwms/" target="_blank" rel="noopener" aria-label="LinkedIn (opens in a new tab)">
          <svg viewBox="0 0 24 24" width="28" height="28" aria-hidden="true" focusable="false"><path fill="currentColor" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.063 2.063 0 1 1 0-4.126 2.063 2.063 0 0 1 0 4.126zM7.119 20.452H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0z"/></svg>
        </a>
        <a class="to-top" href="#top"><span class="to-top__tile" aria-hidden="true"></span><span class="to-top__label">Top<span class="sr-only"> of page</span></span></a>
        </div>
      </div>
      <div class="footer-small">
        <p class="footer-reg">{e(REG)}</p>
      </div>
    </div>
  </div>
</footer>'''

write("index.html", page("Home page", "/", HOME))
write("concept-home/index.html", page("Home page (concept)", "/", CONCEPT,
      extra_head='<link rel="stylesheet" href="/css/concept.css">\n', footer=CONCEPT_FOOTER,
      extra_scripts='<script src="/js/carousel.js" defer></script>'))
write("ask-capital-india-entrepreneur-fund/index.html",
      page("ASK Indian Entrepreneur Fund", ASK_PATH, ASK, section="funds"))
print("wrote preview pages")
