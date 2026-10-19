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
    ("Equities", [("ASK Indian Entrepreneur Fund", "/ask-capital-india-entrepreneur-fund"),
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


def page(title, path, body, section=None, extra_head="", footer=None, extra_scripts="", notice=False, robots=None):
    return f'''<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(DESC)}">
{"" if robots else f'<link rel="canonical" href="{SITE}{path}">'}
{f'<meta name="robots" content="{robots}">' if robots else ""}
<link rel="icon" type="image/png" sizes="32x32" href="/img/gw-icon.png">
<link rel="stylesheet" href="/css/tokens.css">
<link rel="stylesheet" href="/css/base.css">
<link rel="stylesheet" href="/css/components.css">
<script src="/js/init.js"></script>
{extra_head}{'<link rel="stylesheet" href="/css/notice.css">' + chr(10) if notice else ""}</head>
<body id="top">
<a class="skip-link" href="#main">Skip to main content</a>
{header(path, section)}
<main id="main">
{body}
</main>
{footer or FOOTER}
<script src="/js/nav.js" defer></script>
<script src="/js/header-hide.js" defer></script>
{extra_scripts}
{NOTICE_HTML + chr(10) + '<script src="/js/notice.js" defer></script>' if notice else ""}
</body>
</html>
'''



# Entry notice: wording copied verbatim from the live site's modal (audit/baseline/pages/home.html).
NOTICE_HTML = '''<dialog class="notice" id="entry-notice" aria-labelledby="notice-title">
  <div class="notice__body">
    <h2 id="notice-title">Notice</h2>
    <p>Global Wealth Management Solutions deals exclusively with Intermediaries.</p>
    <p>It does not provide advice to Private Clients or the Public in general; therefore in the event of any part or all of the website being accessed by or coming into the hands of Private Clients or the Public in general, none of its content should be construed as explicit or implicit advice of any kind.</p>
    <h3>Cookie Statement</h3>
    <p>Please note that this site uses cookies for the essential running of the website. Please make sure to read the cookie statement to find out how globalwms.com uses cookies.</p>
    <div class="notice__actions">
      <button type="button" class="notice__accept" data-notice-accept autofocus>ACCEPT</button>
      <a class="notice__decline" href="https://google.com">DECLINE</a>
    </div>
  </div>
</dialog>'''

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
        <img class="page-header__logo page-header__logo--wide" src="/img/funds/ask-dark.svg" width="1000" height="159" alt="ASK Investment Managers">
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


def write(rel, content, root=None, raw=False):
    root = root or OUT
    if not raw:
        content = portable(content, rel.count("/"))
    p = root / rel
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
    f'''<li><a class="card" href="{u}"><span class="card__logo{' card__logo--mark' if lg.endswith('.svg') else ''}{' card__logo--oak' if lg.startswith('1oak') else ''}{' card__logo--epic' if lg.startswith('epic') else ''}"><img src="/img/funds/{lg}" alt="{e(alt)}" loading="lazy"></span>
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
      <a class="text-link statement__more" href="/funds">Funds</a>
    </div>
    <ul class="index">
      <li><a href="/platforms"><span>Platforms</span></a></li>
      <li><a href="/funds"><span>Funds</span></a></li>
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
    <div class="about__photo" data-photo-fade>
      <img class="about__img about__img--blue" src="/img/about-glass-blue-1200.webp" srcset="/img/about-glass-blue-700.webp 700w, /img/about-glass-blue-1200.webp 1200w" sizes="(min-width: 60rem) 45vw, 100vw" width="1200" height="800" alt="" loading="lazy">
      <img class="about__img about__img--warm" src="/img/about-glass-1200.webp" srcset="/img/about-glass-700.webp 700w, /img/about-glass-1200.webp 1200w" sizes="(min-width: 60rem) 45vw, 100vw" width="1200" height="800" alt="" loading="lazy">
    </div>
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
            <li><a href="/funds">Funds</a></li>
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


# ---------------------------------------------------------------------------------------
# FUNDS INDEX PAGE (new page: lists the existing funds, existing group names only)
# ---------------------------------------------------------------------------------------
def fund_card(g, n, u, lg, alt):
    cls = "card__logo card__logo--mark" + (" card__logo--oak" if lg.startswith("1oak") else "") + (" card__logo--epic" if lg.startswith("epic") else "")
    return (f'<li><a class="card card--solid" href="{u}"><span class="{cls}"><img src="/img/funds/{lg}" alt="{e(alt)}" loading="lazy"></span>'
            f'<span class="card__group">{e(g)}</span><span class="card__name">{e(n, quote=False)}</span></a></li>')

GROUP_ORDER = ["Multi Asset", "Equities", "Fixed Interest", "Alternative Strategies"]
groups_html = []
for gi, g in enumerate(GROUP_ORDER):
    items = [c for c in CARDS if c[0] == g]
    rows = "\n".join(f'          <li><a href="{u}"><span>{e(n, quote=False)}</span></a></li>' for _, n, u, _, _ in items)
    groups_html.append(f'''<section class="fund-group" aria-labelledby="fg{gi}">
        <h2 class="fund-group__label" id="fg{gi}"><span class="motif" aria-hidden="true"></span>{e(g)}</h2>
        <ul class="index">
{rows}
        </ul>
      </section>''')

FUNDS_PAGE = f'''<div class="frame">
<section class="hero hero--framed hero--page gradient on-dark" aria-labelledby="page-title">
  <picture class="hero__media">
    <source type="image/webp" srcset="/img/hero-800.webp 800w, /img/hero-1280.webp 1280w, /img/hero-1920.webp 1920w" sizes="100vw">
    <img src="/img/hero-1280.webp" width="1280" height="928" alt="" fetchpriority="high">
  </picture>
  <div class="container hero__inner">
    <h1 class="hero__title" id="page-title"><span class="motif" aria-hidden="true"></span>Funds</h1>
  </div>
</section>
</div>
<div class="container fund-groups">
  <p class="fund-intro statement__lead"><span class="motif" aria-hidden="true"></span>Our portfolio comprises ‘best-of-breed’ solutions to meet the needs of discerning intermediaries and their investors.</p>
  <div class="fund-groups__lists">
      {chr(10).join(groups_html)}
  </div>
</div>'''

write("funds/index.html", page("Funds", "/funds", FUNDS_PAGE, section="funds",
      extra_head='<link rel="stylesheet" href="/css/concept.css">\n', footer=CONCEPT_FOOTER))

write("index.html", page("Home page", "/", HOME))
write("concept-home/index.html", page("Home page (concept)", "/", CONCEPT,
      extra_head='<link rel="stylesheet" href="/css/concept.css">\n', footer=CONCEPT_FOOTER,
      extra_scripts='<script src="/js/carousel.js" defer></script>\n<script src="/js/photo-fade.js" defer></script>'))
write("ask-capital-india-entrepreneur-fund/index.html",
      page("ASK Indian Entrepreneur Fund", ASK_PATH, ASK, section="funds"))
print("wrote preview pages")

# =======================================================================================
# DEPLOYABLE SITE  ->  dist/   (home, funds, ASK fund page + 404, robots, sitemap, .htaccess)
# Only pages that are built are included; every other link is still dead until built.
# =======================================================================================
import re, shutil
DIST = OUT.parent / "dist"
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()
ASSET_SRC = OUT
BUILT = ["/", "/funds", ASK_PATH]
FOOT_HEAD = '<link rel="stylesheet" href="/css/concept.css">\n'
HOME_JS = '<script src="/js/photo-fade.js" defer></script>'

write("index.html", page("Home page", "/", CONCEPT, extra_head=FOOT_HEAD, footer=CONCEPT_FOOTER,
      extra_scripts='<script src="/js/carousel.js" defer></script>\n' + HOME_JS, notice=True), root=DIST)
write("funds/index.html", page("Funds", "/funds", FUNDS_PAGE, section="funds", extra_head=FOOT_HEAD,
      footer=CONCEPT_FOOTER, notice=True), root=DIST)
write(ASK_PATH.strip("/") + "/index.html", page("ASK Indian Entrepreneur Fund", ASK_PATH, ASK, section="funds",
      extra_head=FOOT_HEAD, footer=CONCEPT_FOOTER, notice=True), root=DIST)

# 404: served by the host at any URL depth, so it uses root-absolute asset paths (written raw).
NOT_FOUND = '''<div class="container page">
  <h1>404 Not Found</h1>
  <div class="prose">
    <p>The document has not been found on this server.</p>
    <p>Either the link is broken or it is temporarily unavailable.</p>
  </div>
</div>'''
write("404.html", page("404 Not Found", "/404", NOT_FOUND, extra_head=FOOT_HEAD, footer=CONCEPT_FOOTER,
      notice=True, robots="noindex"), root=DIST, raw=True)

write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: " + SITE + "/sitemap.xml\n", root=DIST, raw=True)
urls = "".join(f"  <url><loc>{SITE}{u if u != '/' else '/'}</loc></url>\n" for u in BUILT)
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n", root=DIST, raw=True)
write(".htaccess", """# Apache (SiteGround). Plain static site: no PHP/CMS is required.
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
AddType image/svg+xml .svg
AddType font/woff2 .woff2

RewriteEngine On
# Joomla-era duplicates of the home page and of every page
RewriteRule ^index\\.php/?$ / [R=301,L]
RewriteRule ^home/?$ / [R=301,L]
RewriteRule ^index\\.php/(.+)$ /$1 [R=301,L]
# Retired (owner decision): Investment Notification page and its PDF, Joomla login and feeds
RewriteRule ^investment-notification-form/?$ - [G]
RewriteRule ^images/documents/ - [G]
RewriteRule ^component/ - [G]
""", root=DIST, raw=True)

# assets: css/js/fonts whole (small); images only if referenced
for d in ("css", "js", "fonts"):
    shutil.copytree(ASSET_SRC / d, DIST / d)
text = "".join(f.read_text(encoding="utf-8", errors="ignore") for f in DIST.rglob("*") if f.suffix in (".html", ".css", ".js"))
used = sorted(set(re.findall(r"img/[A-Za-z0-9_\-./]+\.(?:webp|png|jpg|svg)", text)))
for rel in used:
    src = ASSET_SRC / rel
    if src.exists():
        (DIST / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, DIST / rel)
    else:
        print("MISSING ASSET:", rel)
print(f"wrote dist/ ({len(used)} images)")
