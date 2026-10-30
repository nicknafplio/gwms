#!/usr/bin/env python3
"""Extract the article body of each captured live page (audit/baseline/pages) into a
cleaned HTML fragment in tools/content/<slug>.html.

Only presentation is removed (inline styles, Joomla/TinyMCE classes, layout rows and
columns, empty spacer paragraphs, images). Words, order, lists, bold/italic and links are
kept as captured. Joomla's e-mail obfuscation is replaced by <span class="mail"> (see
js/mail.js); the decoded address is data-user@data-domain. Verified afterwards with
tools/compare_content.py."""
import base64, pathlib, re, sys
from bs4 import BeautifulSoup, Comment, NavigableString

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "audit/baseline/pages"
OUT = pathlib.Path(__file__).resolve().parent / "content"
SLUGS = ["1oak-multi-asset-funds-guided-by-blackrock", "epic-investment-partners", "levendi-thornbridge-defined-return-fund",
         "pecora-chatrier-equity-value", "pecora-manning-napier-high-yield-bond-strategy", "pecora-qms",
         "investment-management-solutions", "structured-products", "platforms", "contact",
         "africa", "americas-caribbean", "asia", "europe", "middle-east",
         "privacy-notice", "disclaimer", "cookie-information"]
OWNER_SUPPLIED = {"structured-products", "cookie-information"}   # tools/content/structured-products.html replaces the live wording
REMOVED_PEOPLE = {"contact": ["Dawn Parker", "Asma Choudhary", "Emily Karavla"]}
TEXT_EDITS = {   # owner-requested wording corrections: Simon Voysey's title; Contact page job titles follow the bios
    "contact": [("Sarah Crow - Partner<br/>Head of Commissions &amp; Client Services<br/>T: +44 (0)1525 863772", "Sarah Crow<br/>Head of Commissions &amp; Client Services<br/>M: +44 (0)7876 757253"),
                ("Jessica French - Partner<br/>Audit and Accounting<br/>T: +44 (0)1525 863772", "Jessica French<br/>Head of Accounts<br/>M: +44 (0)7788 205487")],
    "europe": [("Simon Voysey – Partner, Iberia, Channel Islands &amp; UK", "Simon Voysey – International Sales Director, Iberia")],
    "middle-east": [("Simon Voysey, Partner - Middle East", "Simon Voysey, International Sales Director - Middle East")],
}
TEXT_EDITS_MORE = {   # owner-requested policy/text corrections (see docs/10-build-and-test-results.md)
    "privacy-notice": [("registered at Wrest Park, Silsoe, Bedfordshire MK45 4HR, United Kingdom", "registered at 2 Furl Close, Maids Moreton, Buckingham, MK18 1EF"),
                       ('Some of this information may be collected using cookies and similar tracking technology, as explained further under the heading "Cookies and similar tracking technology" below.',
                        'If you accept cookies, some of this information is collected using Google Analytics cookies, as explained further under the heading "Cookies and similar tracking technology" below.'),
                       ('We use cookies and similar tracking technology (collectively, "<strong>Cookies</strong>") to collect and use personal information about you. For further information about the types of Cookies we use, why, and how you can control Cookies, please see our Cookie Policy ',
                        'We use cookies (collectively, "<strong>Cookies</strong>") to remember your choices on this Website (whether you have accepted our notice and whether you have accepted or declined Cookies) and, only if you accept Cookies, to collect information about how you use the Website through Google Analytics. This information may include the personal information described above. Google may process it outside the United Kingdom and the European Economic Area. You can decline Cookies or change your choice at any time. For further information about the Cookies we use, why, and how you can control them, please see our Cookie Policy ')],
    "cookie-information": [("<h2>Content Management System Session Cookie</h2>\n<p>The cookie performs a custom session function for this website. The cookie is created by this (globalwms.com) website’s content management system upon a visitor's arrival. The purpose of the cookie is so that viewing behaviour can be collected in an anonymous form and statistics are displayed in the administrator area.</p>\n<p>This cookie is then removed when a user closes their browser.</p>\n", ""),
                           ("<p>We use a disclaimer in line with compliance to make sure that you agree to the Disclaimer of using darwinpim.com</p>\n", "")],
}
ADDED_PARAS = {}   # (Mike Kew now lives on the United Kingdom page, tools/content/united-kingdom.html)
d = lambda s: base64.b64decode(s).decode()


def clean(slug):
    soup = BeautifulSoup((SRC / f"{slug}.html").read_text(encoding="utf-8"), "html.parser")
    body = soup.select_one(".com-content-article__body")
    for c in body.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for img in body.find_all("img"):
        img.decompose()
    for jm in body.find_all("joomla-hidden-mail"):
        user, dom = d(jm["first"]), d(jm["last"])
        shown = d(jm["text"])
        attrs = {"class": "mail", "data-user": user, "data-domain": dom}
        if shown != f"{user}@{dom}":
            attrs["data-label"] = shown       # display case differs from the address
        span = soup.new_tag("span", attrs=attrs)
        span.string = shown.replace("@", " [at] ")
        jm.replace_with(span)
    for a in body.find_all("a"):          # empty mailto stubs left behind by the CMS
        if not a.get_text(strip=True) and not a.find_all(True):
            a.decompose()
    for div in body.find_all("div"):      # layout rows/columns carry no content
        div.unwrap()
    for t in body.find_all(True):
        for attr in list(t.attrs):
            if attr not in ("href", "data-user", "data-domain", "class") or (attr == "class" and t.name != "span"):
                del t.attrs[attr]
        if t.name == "a" and t.get("href", "").startswith("tel:"):
            t["href"] = "tel:" + re.sub(r"[^\d+]", "", re.sub(r"%20", "", t["href"][4:]))
    # direct text/inline children of the body (structured products, 1OAK footer line) -> paragraphs
    inline = []
    for ch in list(body.children):
        blockish = getattr(ch, "name", None) in ("p", "ul", "ol", "h2", "h3", "h4", "table", "section")
        if blockish or (isinstance(ch, NavigableString) and not ch.strip()):
            if inline:
                p = soup.new_tag("p")
                inline[0].insert_before(p)
                for n in inline: p.append(n.extract())
                inline = []
            continue
        if getattr(ch, "name", None) == "br":
            continue
        inline.append(ch)
    if inline:
        p = soup.new_tag("p"); inline[0].insert_before(p)
        for n in inline: p.append(n.extract())
    for br in body.find_all("br", recursive=False):
        br.decompose()
    for p in body.find_all("p"):          # empty / nbsp-only spacer paragraphs
        if not p.get_text().replace("\xa0", "").strip() and not p.find(["a", "span"]):
            p.decompose()
    for u in body.find_all("ul"):         # CMS emitted one <ul> per bullet
        nxt = u.find_next_sibling()
        while nxt is not None and nxt.name == "ul" and u.find_next_sibling() is nxt:
            for li in list(nxt.find_all("li", recursive=False)):
                u.append(li.extract())
            gone, nxt = nxt, nxt.find_next_sibling()
            gone.decompose()
    for sp in body.find_all("span"):      # empty spans left by the CMS
        if not sp.attrs and not sp.get_text(strip=True):
            sp.decompose()
    for p in body.find_all("p"):          # a paragraph that is only bold in the blue name colour -> heading
        kids = [c for c in p.children if not (isinstance(c, NavigableString) and not c.strip())]
        if len(kids) == 1 and kids[0].name == "strong" and slug == "epic-investment-partners":
            p.name = "h3"; kids[0].unwrap()
    for a in body.find_all("a", href=re.compile(r"^https?://")):
        a["target"] = "_blank"; a["rel"] = "noopener"
        host = re.sub(r"^https?://(www\.)?", "", a["href"]).split("/")[0]
        s = soup.new_tag("span", attrs={"class": "sr-only"}); s.string = f" External site: {host}. Opens in a new tab."
        a.append(s)
    # two links in the Privacy Notice point at pages that never existed ("/about", "/cookie-information.");
    # the link text is untouched, only the target is pointed at the page the text names.
    for a in body.find_all("a", href=True):
        a["href"] = {"/about": "/about-gwms", "/cookie-information.": "/cookie-information"}.get(a["href"], a["href"])
    for who in REMOVED_PEOPLE.get(slug, []):      # owner decision: people removed from the site
        for p_ in body.find_all("p"):
            if p_.get_text().strip().startswith(who):
                p_.decompose()
    h1 = soup.select_one(".page-header h1")
    html = body.decode_contents().replace("\xa0", " ")
    for extra in ADDED_PARAS.get(slug, []):
        html += "\n" + extra
    for old, new in TEXT_EDITS.get(slug, []) + TEXT_EDITS_MORE.get(slug, []):
        assert old in html, (slug, old)
        html = html.replace(old, new)
    html = re.sub(r"\n{2,}", "\n", html).strip()
    return (h1.get_text(strip=True) if h1 else None), html


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for slug in SLUGS:
        if slug in OWNER_SUPPLIED:      # text written/supplied by the owner; not re-extracted from the live site
            continue
        h1, html = clean(slug)
        (OUT / f"{slug}.html").write_text(html + "\n", encoding="utf-8")
        print(f"{slug}: h1={h1!r} {len(html)} bytes")


MEMBERS = {"david-parker": "25-david-parker", "james-bottomley": "61-james-bottomley", "simon-voysey": "28-simon-voysey",
           "sarah-crow": "32-sarah-crow-partner", "jessica-french": "34-jessica-french"}


# Owner-requested edits to the captured member pages (applied after extraction so a re-run keeps them).
MEMBER_EDITS = {
    "david-parker": [("34 years of experience", "40 years of experience"), ('<li class="bizcard__detail"><span class="bizcard__key">t:</span> +44(0)1525 862420</li>', "")],
    "simon-voysey": [('<li class="bizcard__job">Partner</li>', '<li class="bizcard__job">International Sales Director</li>'),
                     ('<li class="bizcard__detail"><span class="bizcard__key">t:</span> +44 (0) 1525 863774</li>', "")],
    "sarah-crow": [("+44 (01525) 62420", "+44(0)7876 757253")],
    "jessica-french": [("+44 (01525) 863780", "+44(0)7788 205487"), ("Head of Accounting & Audit", "Head of Accounts")],
}


def member(slug):
    """Individual team-member page (captured from /meet-the-team/<id>-<name>): role, biography,
    the vCard lead-in sentence, the business-card details and (David Parker) the LinkedIn sentence."""
    soup = BeautifulSoup((SRC / "team" / f"{MEMBERS[slug]}.html").read_text(encoding="utf-8"), "html.parser")
    body = soup.select_one(".item-page .com-content-article__body")
    for c in body.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    out = [f'<p class="member__role">{body.find("h3").get_text(strip=True)}</p>']
    for el in body.find_all(["p", "div"], recursive=False):
        if el.name == "div":                       # the business card
            items = []
            for li in el.find_all("li"):
                jm = li.find("joomla-hidden-mail")
                if jm:
                    user, dom, shown = d(jm["first"]), d(jm["last"]), d(jm["text"])
                    lab = f' data-label="{shown}"' if shown != f"{user}@{dom}" else ""
                    val = f'<span class="mail" data-user="{user}" data-domain="{dom}"{lab}>{shown.replace("@", " [at] ")}</span>'
                else:
                    val = "".join(str(c) for c in li.children if getattr(c, "name", None) != "span").strip()
                key = li.find("span")
                cls = (li.get("class") or [""])[0]
                items.append((cls, key.get_text(strip=True) if key else "", val))
            lis = "".join(f'<li class="bizcard__{c}">' + (f'<span class="bizcard__key">{k}</span> ' if k else "") + v + "</li>" for c, k, v in items)
            out.append(f'<div class="bizcard"><ul>{lis}</ul></div>')
            continue
        for a in el.find_all("a", href=re.compile("^https?://")):
            for i in a.find_all("i"): i.decompose()
            a["target"] = "_blank"; a["rel"] = "noopener"
            sp = soup.new_tag("span", attrs={"class": "sr-only"}); sp.string = " External site: linkedin.com. Opens in a new tab."
            a.append(sp)
            a.string = a.get_text().strip() if False else a.contents[0].strip() if isinstance(a.contents[0], NavigableString) else a.contents[0]
        for t in [el] + el.find_all(True):
            for attr in list(t.attrs):
                if attr not in ("href", "target", "rel", "class"): del t.attrs[attr]
        txt = el.get_text(strip=True)
        if txt:
            out.append(str(el).replace("\xa0", " "))
    html = "\n".join(out)
    for old, new in MEMBER_EDITS.get(slug, []):
        assert old in html, (slug, old)
        html = html.replace(old, new)
    return html


if __name__ == "__main__":
    for slug in MEMBERS:
        (OUT / f"team-{slug}.html").write_text(member(slug) + "\n", encoding="utf-8")
        print("team-" + slug)
