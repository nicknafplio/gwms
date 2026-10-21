#!/usr/bin/env python3
"""Generate the two representative preview pages from one shared definition of
header / navigation / footer. All page text below is copied verbatim from the
live site (audit/baseline/text/*.txt); tools/verify_preview.py checks that."""
import html, pathlib, re, sys

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


SITE_NAME = "Global Wealth Management Solutions"


def og_tags(title, path):
    """Open Graph / Twitter card tags so links shared in social and messaging apps show a title,
    the existing site description and a preview image. URLs are absolute (the live domain)."""
    t = f"{SITE_NAME} — " + ("Creating long-term value" if path == "/" else title)
    url = SITE + ("/" if path == "/" else path + ".html")
    return "\n".join([
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{e(t)}">',
        f'<meta property="og:description" content="{e(DESC)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{SITE}/img/og-image.jpg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{SITE_NAME}: Creating long-term value">',
        '<meta property="og:locale" content="en_GB">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(t)}">',
        f'<meta name="twitter:description" content="{e(DESC)}">',
        f'<meta name="twitter:image" content="{SITE}/img/og-image.jpg">',
    ])


def page(title, path, body, section=None, extra_head="", footer=None, extra_scripts="", notice=False, robots=None):
    return f'''<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(DESC)}">
{og_tags(title, path)}
{"" if robots else f'<link rel="canonical" href="{SITE}{"/" if path == "/" else path + ".html"}">'}
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
{'<script src="/js/side-nav.js" defer></script>' + chr(10) if 'class="side-nav"' in body else ''}{extra_scripts}
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


def side_nav(current, groups=None, label="Funds"):
    """Left-hand section menu. Desktop: always-visible sidebar. Mobile (with JS): a sticky, collapsed
    'Explore this section' disclosure (see js/side-nav.js and the .side-nav rules in concept.css);
    without JS the full list simply shows."""
    parts = []
    for glabel, items in (groups or SIDE_NAV):
        parts.append(f'<p class="side-nav__label"><span class="motif" aria-hidden="true"></span>{e(glabel)}</p>\n<ul>\n{links(items, current)}\n</ul>')
    return (f'<nav class="side-nav" aria-label="{label}">\n'
            f'<button type="button" class="side-nav__toggle" aria-expanded="false" aria-controls="side-nav-panel"><span>Explore this section</span><span class="chev" aria-hidden="true"></span></button>\n'
            f'<div class="side-nav__panel" id="side-nav-panel">\n' + "\n".join(parts) + "\n</div>\n</nav>")


ASK_PATH = "/ask-capital-india-entrepreneur-fund"
ASK = f'''<div class="container page">
  <div class="page__layout">
{side_nav(ASK_PATH)}
    <article>
      <div class="member-layout fund-layout">
      <header class="page-header"><h1>ASK Indian Entrepreneur Fund</h1></header>
      <img class="page-header__logo page-header__logo--wide" src="/img/funds/ask-dark.svg" width="1000" height="159" alt="ASK Investment Managers">
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
      </div>
      <section class="footnotes" aria-labelledby="fn-title">
        <h2 class="sr-only" id="fn-title">Footnotes</h2>
        <p id="_ftn1"><a class="fn-ref" href="#_ftnref1"><sup>[1]</sup></a> as of 31 July 2023</p>
      </section>
    </article>
  </div>
</div>'''


ASSET_DIRS = "css|js|img|fonts|vcards"


def _asset_version():
    """Short hash of the css/js/map files, appended as ?v= so browsers never show a stale copy after an update."""
    import hashlib
    h = hashlib.sha1()
    for sub in ("css", "js", "img/regions"):
        for f in sorted((OUT / sub).glob("*")):
            if f.is_file():
                h.update(f.read_bytes())
    return h.hexdigest()[:8]


ASSET_V = _asset_version()


def page_href(url):
    """Internal page path -> flat file at the site root: '/about-gwms' -> 'about-gwms.html'."""
    return "index.html" if url == "/" else url.strip("/") + ".html"


def portable(content):
    """Pages sit at the site root, so every internal URL becomes a plain relative path and the
    site opens straight from disk (file://) as well as on any host."""
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(rf"/({ASSET_DIRS})/", url):
            bust = f"?v={ASSET_V}" if re.match(r"/(css|js|img/regions)/", url) else ""
            return f'{attr}="{url[1:]}{bust}"'
        return f'{attr}="{page_href(url)}"'
    content = re.sub(r'\b(href|src)="(/[^"/][^"]*|/)"', fix, content)
    return re.sub(r'(/img/[^ ",]+)( \d+w)', lambda m: m.group(1)[1:] + m.group(2), content)


def absolute(content):
    """For 404.html, which a host serves at any URL: keep root-absolute paths, add '.html' to page links."""
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(rf"/({ASSET_DIRS})/", url) or url == "/":
            return m.group(0)
        return f'{attr}="/{page_href(url)}"'
    return re.sub(r'\b(href|src)="(/[^"/][^"]*|/)"', fix, content)


def write(rel, content, root=None, raw=False):
    root = root or OUT
    if rel.endswith(".html"):
        content = absolute(content) if raw else portable(content)
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
LOGO_DIMS = {"1oak-white.svg": (892, 368), "epic-white.svg": (515, 193), "ask-white.svg": (1000, 159),
             "pecora-capital-white.svg": (761, 121), "levendi-thornbridge-white.svg": (287, 55)}   # intrinsic sizes, avoids layout shift
cards_html = "\n".join(
    f'''<li><a class="card" href="{u}"><span class="card__logo{' card__logo--mark' if lg.endswith('.svg') else ''}{' card__logo--oak' if lg.startswith('1oak') else ''}{' card__logo--epic' if lg.startswith('epic') else ''}"><img src="/img/funds/{lg}" width="{LOGO_DIMS[lg][0]}" height="{LOGO_DIMS[lg][1]}" alt="{e(alt)}" loading="lazy"></span>
<span class="card__group">{e(g)}</span><span class="card__name">{e(n, quote=False)}</span></a></li>'''
    for g, n, u, lg, alt in CARDS)

CONCEPT = f'''<div class="frame">
<section class="hero hero--framed gradient on-dark" aria-labelledby="home-title">
  <picture class="hero__media">
    <source type="image/webp" srcset="/img/hero-800.webp 800w, /img/hero-1280.webp 1280w, /img/hero-1920.webp 1920w" sizes="100vw">
    <img src="/img/hero-1280.webp" width="1280" height="928" alt="" fetchpriority="high">
  </picture>
  <div class="container hero__inner">
    <h1 class="hero__title" id="home-title"><span class="motif" aria-hidden="true"></span>Creating <br>long-term <span class="typed" data-words="value,relationships,objectives"><span class="sr-only">value</span><span class="typed__text" aria-hidden="true">value</span><span class="typed__caret" aria-hidden="true"></span></span></h1>
  </div>
  <div class="hero__outline" aria-hidden="true">
    <svg viewBox="15 41 41 22" focusable="false">
      <path pathLength="1" d="M31.8,61.2c-1.1,0.4-3.3,1.1-5.9,1.1c-2.9,0-5.3-0.7-7.2-2.6c-1.7-1.6-2.7-4.2-2.7-7.2c0-5.8,4-10,10.5-10c2.2,0,4,0.5,4.8,0.9l-0.6,2c-1-0.5-2.3-0.8-4.3-0.8c-4.7,0-7.8,2.9-7.8,7.8c0,4.9,3,7.8,7.5,7.8c1.6,0,2.8-0.2,3.3-0.5v-5.8h-3.9v-2h6.4V61.2z"/>
      <path pathLength="1" d="M38.8,62l-4.9-19.3h2.6l2.3,9.8c0.6,2.4,1.1,4.8,1.4,6.7h0.1c0.3-1.9,0.9-4.2,1.6-6.7l2.6-9.8h2.6l2.4,9.8c0.5,2.3,1.1,4.6,1.3,6.6h0.1c0.4-2.1,0.9-4.3,1.6-6.7l2.6-9.8h2.6L52,62h-2.6L46.9,52c-0.6-2.5-1-4.4-1.3-6.3h-0.1c-0.3,1.9-0.8,3.8-1.5,6.3L41.4,62H38.8z"/>
    </svg>
  </div>
  <a class="hero__next" href="#statement" aria-label="Skip to next section"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false"><path d="M12 4v15M5.5 12.5 12 19l6.5-6.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="square"/></svg></a>
</section>
</div>
<section class="statement statement--plain" id="statement">
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


OUTLINE_HTML = re.search(r'<div class="hero__outline".*?</div>', CONCEPT, re.S).group(0)   # traced GW outline, shared by hero and banners


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
  {OUTLINE_HTML}
</section>
</div>
<div class="container fund-groups">
  <p class="fund-intro statement__lead"><span class="motif" aria-hidden="true"></span>Our portfolio comprises ‘best-of-breed’ solutions to meet the needs of discerning intermediaries and their investors.</p>
  <div class="fund-groups__lists">
      {chr(10).join(groups_html)}
  </div>
</div>'''



# =======================================================================================
# INNER PAGES.  Page bodies come from tools/content/*.html (cleaned captures of the live
# pages, see extract_bodies.py); only the frame around them is new.
# =======================================================================================
import shutil
CONTENT = pathlib.Path(__file__).resolve().parent / "content"


def body_of(slug):
    return (CONTENT / f"{slug}.html").read_text(encoding="utf-8").strip()


def logo(file, alt, w, h, wide=True):
    cls = "page-header__logo" + (" page-header__logo--wide" if wide else "")
    return f'<img class="{cls}" src="/img/{file}" width="{w}" height="{h}" alt="{e(alt)}">'


def banner(title):
    """Framed gradient banner with the page title (same as the Funds page)."""
    return f'''<div class="frame">
<section class="hero hero--framed hero--page gradient on-dark" aria-labelledby="page-title">
  <picture class="hero__media">
    <source type="image/webp" srcset="/img/hero-800.webp 800w, /img/hero-1280.webp 1280w, /img/hero-1920.webp 1920w" sizes="100vw">
    <img src="/img/hero-1280.webp" width="1280" height="928" alt="" fetchpriority="high">
  </picture>
  <div class="container hero__inner">
    <h1 class="hero__title" id="page-title"><span class="motif" aria-hidden="true"></span>{e(title, quote=False)}</h1>
  </div>
  {OUTLINE_HTML}
</section>
</div>
'''


def article(h1, content, side=None, logo_html="", footnotes="", banner_title=None, lead="", aside_html="", head_above=False):
    """With banner_title the page title lives in the banner (h1) and the page header keeps only the logo."""
    if side and head_above and not banner_title:    # heading + rule in their own row, offset so the menu and the text start level
        return (f'<div class="container page">\n  <div class="page__layout page__layout--headed">\n'
                f'    <header class="page-header page__head"><h1>{e(h1, quote=False)}</h1></header>\n{side}\n'
                f'    <article>\n      <div class="prose">\n{content}\n      </div>{footnotes}\n    </article>\n  </div>\n</div>')
    if side and logo_html and not banner_title:   # fund pages: title left (may wrap), logo in a right-hand column on desktop
        art = (f'<article>\n      <div class="member-layout fund-layout">\n        <header class="page-header"><h1>{e(h1, quote=False)}</h1></header>\n'
               f'        {logo_html}\n        <div class="prose">\n{content}\n        </div>\n      </div>{footnotes}\n    </article>')
    elif banner_title and aside_html:           # text left, pull quote in a right-hand column
        art = (f'<article>\n      <div class="split">\n        <div class="prose">\n{content}\n        </div>\n'
               f'        <aside class="split__quote" aria-label="Pull quote">{aside_html}</aside>\n      </div>{footnotes}\n    </article>')
    elif banner_title and logo_html:      # partner logo in a right-hand column on desktop (above the text on mobile)
        art = (f'<article>\n      <div class="split">\n        <div class="prose">\n{content}\n        </div>\n'
               f'        <aside class="split__logo" aria-label="Partner">{logo_html}</aside>\n      </div>{footnotes}\n    </article>')
    else:
        if banner_title:
            head = ""
        else:
            head = f'<header class="page-header">\n        <h1>{e(h1, quote=False)}</h1>\n        {logo_html}\n      </header>\n      '
        art = f'<article>\n      {head}{lead}<div class="prose">\n{content}\n      </div>{footnotes}\n    </article>'
    if side:
        inner = f'<div class="container page">\n  <div class="page__layout">\n{side}\n    {art}\n  </div>\n</div>'
    else:
        inner = f'<div class="container page page--single">\n  {art}\n</div>'
    if banner_title and not side:       # no left-hand menu: content is offset to line up with the banner heading
        inner = inner.replace('class="container page page--single"', 'class="container page page--single page--aligned"', 1)
    return (banner(banner_title) if banner_title else "") + inner


def people(content):
    """Contact / region pages: the first heading (if any) stays above; each person is a card."""
    m = re.match(r"(<h2>.*?</h2>\s*)?(.*)", content, re.S)
    return (m.group(1) or "") + '<div class="people">\n' + m.group(2) + "\n</div>"


ABOUT_SIDE = lambda cur: side_nav(cur, ABOUT_MENU, "About us")
FUND_PAGES = [  # slug, h1, header logo
    ("1oak-multi-asset-funds-guided-by-blackrock", "1OAK Multi Asset (MA80) Fund", logo("funds/1oak-dark.svg", "1OAK", 515, 193, wide=False)),
    ("epic-investment-partners", "EPIC Investment Partners", logo("funds/epic-dark.svg", "EPIC Investment Partners", 515, 193, wide=False)),
    ("levendi-thornbridge-defined-return-fund", "Levendi Thornbridge Defined Return Fund", logo("funds/causeway-dark.svg", "Causeway Securities", 1000, 193)),
    ("pecora-chatrier-equity-value", "Pecora Chatrier Equity (Value)", logo("funds/pecora-capital-dark.svg", "Pecora Capital", 761, 121)),
    ("pecora-manning-napier-high-yield-bond-strategy", "Pecora Manning & Napier High Yield Bond Strategy", logo("funds/pecora-capital-dark.svg", "Pecora Capital", 761, 121)),
    ("pecora-qms", "Pecora QMS", logo("funds/pecora-capital-dark.svg", "Pecora Capital", 761, 121)),
]

PAGES = {}   # path -> (title, html, section)


def add(path, title, html, section=None):
    PAGES[path] = (title, html, section)


add("/", "Home page", CONCEPT)
add("/funds", "Funds", FUNDS_PAGE, "funds")
add(ASK_PATH, "ASK Indian Entrepreneur Fund", ASK, "funds")
for slug, h1, lg in FUND_PAGES:
    path = "/" + slug
    add(path, h1, article(h1, body_of(slug), side_nav(path), lg), "funds")

ABOUT = '''<p>Established in 2003, Global Wealth Management Solutions (GWMS) provides access to a suite of best of breed financial products. We are trusted by banks, institutions, captives, trust companies, family offices and boutique fund managers, who value our exceptional market knowledge, excellent service levels and strong track record.</p>
<p>Our management team has over 150 years of financial services experience and provides the highest levels of support, professionalism and integrity. Most of our Partners and senior staff have been with us for more than 10 years. As a result, we have developed a sustainable and successful business, based on longevity, experience, security and value.</p>
<h2>Locations</h2>
<p>We offer a global reach combined with local knowledge, transacting business in over 80 countries. GWMS is headquartered in the UK but reaches a global audience through our teams operating in Offshore Islands and throughout <a href="/europe">Europe</a>, <a href="/africa">Africa</a>, <a href="/asia">Asia</a>, <a href="/middle-east">The Middle East</a>, <a href="/americas-caribbean">Caribbean Islands</a> and <a href="/americas-caribbean">South America</a>. We understand each marketplace, its nuances, challenges and opportunities, utilising the deep insights of our country specialists.</p>
<p>Global Wealth Managent Solutions on <a href="https://www.linkedin.com/company/gwms/" target="_blank" rel="noopener">LinkedIn<span class="sr-only"> External site: linkedin.com. Opens in a new tab.</span></a>.</p>'''
CREDENTIALS = '''<aside class="credentials" aria-labelledby="cred-title">
  <h2 id="cred-title">Credentials</h2>
  <p>Global Wealth Management Solutions LLP is authorised and regulated by the Financial Conduct Authority (ref 678746).</p>
  <p>Professional Connections</p>
  <ul>
    <li>Bank: NatWest</li>
    <li>Lawyers: BDB Pitmans LLP</li>
    <li>Compliance Advisers: FM Consult</li>
    <li>Regulators: FCA</li>
  </ul>
</aside>'''
add("/about-gwms", "Exceptional wealth management solutions",
    article("Exceptional wealth management solutions", ABOUT + "\n" + CREDENTIALS, ABOUT_SIDE("/about-gwms"), banner_title="Exceptional wealth management solutions"), "about")

TEAM = [  # name, role, bio (verbatim), slug
    ("David Parker", "Chief Executive Officer", "David has 34 years of experience marketing wealth management products to institutions and professional intermediaries.", "david-parker"),
    ("Mike Kew", "UK Sales Consultant", "Mike has over 40 years' experience across stockbroking, private wealth, fund management, and alternative investments.", "mike-kew"),
    ("James Bottomley", "Head of Institutional Sales Asia", "James has 30 years experience in the Financial Services sector.", "james-bottomley"),
    ("Simon Voysey", "International Sales Director", "As an IFA for 10 years in the Middle East I was initially attracted by the best of breed fund range, providing key client solutions for IFAs and Wealth Managers.", "simon-voysey"),
    ("Sarah Crow - Partner", "Head of Commissions & Client Services", "", "sarah-crow"),
    ("Jessica French - Partner", "Head of Accounting & Audit", "", "jessica-french"),
]
def make_vcard(fragment):
    """vCard 3.0 built from the business-card details on the person's page (single source of truth)."""
    def li(cls):
        m = re.search(rf'<li class="bizcard__{cls}">(.*?)</li>', fragment)
        return m.group(1) if m else ""
    name = html.unescape(re.sub("<[^>]+>", "", li("name"))).strip()
    job = html.unescape(re.sub("<[^>]+>", "", li("job"))).strip()
    if not job:
        job = html.unescape(re.search(r'<p class="member__role">(.*?)</p>', fragment).group(1))
    lines = ["BEGIN:VCARD", "VERSION:3.0"]
    first, _, last = name.partition(" ")
    lines += [f"N:{last};{first};;;", f"FN:{name}", "ORG:Global Wealth Management Solutions", f"TITLE:{job}"]
    for m in re.finditer(r'<li class="bizcard__detail">(.*?)</li>', fragment):
        d_ = m.group(1)
        mm = re.search(r'data-user="([^"]+)" data-domain="([^"]+)"', d_)
        txt = html.unescape(re.sub("<[^>]+>", "", d_)).strip()
        if mm:
            lines.append("EMAIL;TYPE=INTERNET,WORK:" + f"{mm.group(1)}@{mm.group(2)}".lower())
        elif txt.startswith("m:") or txt.startswith("t:"):
            digits = re.sub(r"\D", "", txt[2:].replace("(0)", ""))
            if digits.startswith("440"):
                digits = "44" + digits[3:]
            lines.append(f"TEL;TYPE={'CELL' if txt[0] == 'm' else 'WORK'},VOICE:+{digits}")
        elif txt.startswith("w:"):
            lines.append("URL:https://" + txt[2:].strip())
    return "\r\n".join(lines + ["END:VCARD", ""])


vcards_out = {}
PHOTOS = {"mike-kew", "david-parker", "james-bottomley", "simon-voysey", "sarah-crow", "jessica-french"}   # others: placeholder
team_items = []
for name, role, bio, vc in TEAM:
    list_img = f"/img/team/{vc}-square.jpg" if vc in PHOTOS else "/img/team/duffprofile.jpg"
    page_img = f"/img/team/{vc}.jpg" if vc in PHOTOS else "/img/team/duffprofile.jpg"
    short = name.split(" - ")[0]
    team_items.append(f'''<li class="member">
  <img class="member__photo" src="{list_img}" width="300" height="300" alt="" loading="lazy">
  <div class="member__text">
    <h2 class="member__name"><a href="/team-{vc}">{e(name)}</a></h2>
    <p class="member__role">{e(role, quote=False)}</p>
    {f'<p class="member__bio">{e(bio, quote=False)}</p>' if bio else ""}
  </div>
</li>''')
    mc = body_of("team-" + vc).replace('</ul></div>', f'</ul><a class="member__vcard" href="/vcards/{vc}.vcf" download>vCard<span class="sr-only"> for {e(short)}</span></a></div>')
    role_html, rest = mc.split("\n", 1)
    photo = f'<img class="page-header__photo" src="{page_img}" width="300" height="405" alt="">'
    add("/team-" + vc, short, f'''<div class="container page">
  <div class="page__layout">
{ABOUT_SIDE("/meet-the-team")}
    <article>
      <div class="member-layout">
        <header class="page-header"><h1>{e(name)}</h1></header>
        {photo}
        <div class="prose">
{role_html}
{rest}
        </div>
      </div>
    </article>
  </div>
</div>''', "about")
    vcards_out[vc] = make_vcard(mc)
TEAM_HTML = '<ul class="team">\n' + "\n".join(team_items) + "\n</ul>"
add("/meet-the-team", "Meet the Team",
    banner("Meet the Team") + f'<div class="container page">\n  <div class="page__layout">\n{ABOUT_SIDE("/meet-the-team")}\n    <article>\n{TEAM_HTML}\n    </article>\n  </div>\n</div>', "about")

for slug, h1 in [("africa", "Africa"), ("americas-caribbean", "Americas & Caribbean"), ("asia", "Asia"),
                 ("europe", "Europe"), ("middle-east", "Middle East")]:
    vb = re.search(r'viewBox="([\d. ]+)"', (OUT / "img/regions" / f"{slug}.svg").read_text(encoding="utf-8")).group(1).split()
    w_, h_ = float(vb[2]), float(vb[3])
    region_map = (f'<img class="region-map" src="/img/regions/{slug}.svg" width="{round(w_ * 2)}" '
                  f'height="{round(h_ * 2)}" alt="">\n')      # decorative: the page heading already names the region
    add("/" + slug, h1, article(h1, people(body_of(slug)), ABOUT_SIDE("/" + slug), lead=region_map), "about")

add("/platforms", "Platforms", article("Platforms", body_of("platforms"), None,
    logo("platforms/veritas-life.svg", "Veritas Life", 296, 114), banner_title="Platforms"), None)
add("/investment-management-solutions", "Investment Management Solutions",
    article("Investment Management Solutions", body_of("investment-management-solutions"), None,
            logo("investment/resilience-asset-management.svg", "Resilience Asset Management", 1024, 229),
            banner_title="Investment Management Solutions"), None)
add("/structured-products", "Structured Products", article("Structured Products", body_of("structured-products"), banner_title="Structured Products",
            aside_html='<p class="pullquote">Connecting expertise with investment opportunity.</p>'), None)
add("/contact", "Contact", article("Contact", people(body_of("contact")), banner_title="Contact"), None)
LEGAL_MENU = [("Legal", [("Privacy Notice", "/privacy-notice"), ("Disclaimer", "/disclaimer"), ("Cookie Information", "/cookie-information")])]
for slug, h1 in [("privacy-notice", "Privacy Notice"), ("disclaimer", "Disclaimer"), ("cookie-information", "Cookie Information")]:
    add("/" + slug, h1, article(h1, body_of(slug), side_nav("/" + slug, LEGAL_MENU, "Legal"), head_above=True), None)

# =======================================================================================
# DEPLOYABLE SITE  ->  dist/   Every page is a plain .html file at the site root; assets live
# in their own folders (css, js, fonts, img/*, vcards), each with a blank index.html.
# =======================================================================================
DIST = OUT.parent / "dist"
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()
FOOT_HEAD = '<link rel="stylesheet" href="/css/concept.css">\n'
HOME_JS = '<script src="/js/carousel.js" defer></script>\n<script src="/js/photo-fade.js" defer></script>\n<script src="/js/typed.js" defer></script>'

for path, (title, html_, section) in PAGES.items():
    scripts = HOME_JS if path == "/" else ""
    if 'class="mail"' in html_:
        scripts += '\n<script src="/js/mail.js" defer></script>'
    write(page_href(path), page(title, path, html_, section=section, extra_head=FOOT_HEAD,
          footer=CONCEPT_FOOTER, extra_scripts=scripts, notice=True), root=DIST)

# 404: served by the host at any URL depth, so it uses root-absolute asset paths.
NOT_FOUND = '''<div class="container page page--single">
  <h1>404 Not Found</h1>
  <div class="prose">
    <p>The document has not been found on this server.</p>
    <p>Either the link is broken or it is temporarily unavailable.</p>
  </div>
</div>'''
write("404.html", page("404 Not Found", "/404", NOT_FOUND, extra_head=FOOT_HEAD, footer=CONCEPT_FOOTER,
      notice=True, robots="noindex"), root=DIST, raw=True)

write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: " + SITE + "/sitemap.xml\n", root=DIST, raw=True)
urls = "".join(f"  <url><loc>{SITE}{'/' if u == '/' else u + '.html'}</loc></url>\n" for u in PAGES)
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n", root=DIST, raw=True)
write(".htaccess", """# Apache (SiteGround). Plain static site: no PHP/CMS is required.
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
AddType image/svg+xml .svg
AddType font/woff2 .woff2
AddType text/vcard .vcf

RewriteEngine On
# Joomla-era duplicates of the home page and of every page
RewriteRule ^index\\.php/?$ / [R=301,L]
RewriteRule ^home/?$ / [R=301,L]
RewriteRule ^index\\.php/(.+)$ /$1 [R=301,L]
# Retired (owner decision): Investment Notification page and its PDF, Joomla login and feeds
RewriteRule ^investment-notification-form/?$ - [G]
RewriteRule ^images/documents/ - [G]
RewriteRule ^component/ - [G]
# Individual team-member pages (old Joomla URLs); Dawn Parker's page is retired (owner decision)
RewriteRule ^meet-the-team/25-david-parker/?$ /team-david-parker.html [R=301,L]
RewriteRule ^meet-the-team/61-james-bottomley/?$ /team-james-bottomley.html [R=301,L]
RewriteRule ^meet-the-team/28-simon-voysey/?$ /team-simon-voysey.html [R=301,L]
RewriteRule ^meet-the-team/32-sarah-crow-partner/?$ /team-sarah-crow.html [R=301,L]
RewriteRule ^meet-the-team/34-jessica-french/?$ /team-jessica-french.html [R=301,L]
RewriteRule ^meet-the-team/57-dawn-parker/?$ - [G]
# Old extensionless page URLs -> the same page as <name>.html
RewriteRule ^about/?$ /about-gwms.html [R=301,L]
RewriteRule ^cookie-information\\.$ /cookie-information.html [R=301,L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^([A-Za-z0-9-]+)/?$ /$1.html [R=301,L]
""", root=DIST, raw=True)

for vc, card in vcards_out.items():      # real vCards replace the placeholders in the source folder
    (OUT / "vcards" / f"{vc}.vcf").write_text(card, encoding="utf-8", newline="")
# assets: css/js/fonts/vcards whole (small); images only if referenced
for d in ("css", "js", "fonts", "vcards"):
    shutil.copytree(OUT / d, DIST / d)
text = "".join(f.read_text(encoding="utf-8", errors="ignore") for f in DIST.rglob("*") if f.suffix in (".html", ".css", ".js"))
used = sorted(set(["img/og-image.jpg"] + re.findall(r"img/[A-Za-z0-9_\-./]+\.(?:webp|png|jpg|svg)", text)))
for rel in used:
    src = OUT / rel
    if src.exists():
        (DIST / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, DIST / rel)
    else:
        print("MISSING ASSET:", rel)
BLANK = '<!doctype html>\n<meta charset="utf-8">\n<title></title>\n'
for folder in sorted({d for d in DIST.rglob("*") if d.is_dir()}):
    (folder / "index.html").write_text(BLANK, encoding="utf-8")
print(f"wrote dist/: {len(PAGES)} pages, {len(used)} images")
