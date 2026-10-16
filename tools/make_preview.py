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
    ("About GWMS", [("About GWMS", "/about-gwms"), ("Meet the team", "/meet-the-team"),
                    ("Documents", "/investment-notification-form")]),
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
    <a class="brand" href="/"><img src="/img/logo-gwms.png" width="752" height="164" alt="Global Wealth Management Solutions — home"></a>
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
    <img class="site-footer__mark" src="/img/gw-icon.png" width="171" height="171" alt="">
    <p class="site-footer__reg">{e(REG)}</p>
    <ul class="site-footer__links" aria-label="Legal">
      <li><a href="/privacy-notice">Privacy Notice</a></li>
      <li><a href="/disclaimer">Disclaimer</a></li>
      <li><a href="/cookie-information">Cookie Information</a></li>
    </ul>
  </div>
</footer>'''


def page(title, path, body, section=None, extra_head=""):
    return f'''<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" type="image/png" sizes="32x32" href="/img/gw-icon.png">
<link rel="preload" href="/fonts/source-serif-4-latin-opsz.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/source-sans-3-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/tokens.css">
<link rel="stylesheet" href="/css/base.css">
<link rel="stylesheet" href="/css/components.css">
<script src="/js/init.js"></script>
{extra_head}</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header(path, section)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="/js/nav.js" defer></script>
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


def write(rel, content):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


write("index.html", page("Home page", "/", HOME))
write("ask-capital-india-entrepreneur-fund/index.html",
      page("ASK Indian Entrepreneur Fund", ASK_PATH, ASK, section="funds"))
print("wrote preview pages")
