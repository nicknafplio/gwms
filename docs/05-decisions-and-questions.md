# 05 · Decisions and questions needed

## A. Approvals requested at this gate
| ID | Decision | My recommendation |
|---|---|---|
| A1 | **Visual direction** (`03-visual-direction.md`; previews in `preview/screenshots/`) | Approve, or tell me what to change |
| A2 | **Navigation structure** (`02-navigation-proposal.md`, items N1–N8) | Approve N1–N4; decide N5–N7 |
| A3 | **Fonts:** self-hosted Source Serif 4 + Source Sans 3 (OFL, 150 KB, no external requests) | Approve |
| A4 | **Build tooling:** plain Python 3 generator (already used for the preview) producing ordinary static files, no Node/framework needed to maintain | Approve; no JS framework or CSS framework is used |
| A5 | **URL style:** keep today's extensionless URLs (`/platforms`). Needs the host to serve `/platforms` → `platforms/index.html` (almost all static hosts do) | Approve; confirm host in B1 |

## B. Questions that change the work
| ID | Question |
|---|---|
| B1 | Where will the static site be hosted (and by whom)? Determines redirect syntax, security headers, privacy-notice wording. |
| B2 | Can you supply a **vector (SVG/AI/EPS) logo**? The supplied PNG (752×164) is used as-is until then. |
| B3 | Permission/licence to use the two supplied photographs (assumed yes). |
| B4 | Do you have the source/exports of the Joomla site (database, unpublished articles, menu items hidden from the public)? My crawl cannot see them. |
| B5 | Who approves policy changes (compliance adviser / legal)? |

## C. Existing elements that may conflict with the "no new CTA" rule — flagged, **nothing deleted**
| ID | Element | Why flagged | Default in the build |
|---|---|---|---|
| C1 | Meta description on every page: "Global investors deserve better - now you can provide it" | Promotional / sales-prompt wording | Kept unchanged |
| C2 | Home hero text "Creating long-term value" and section "Why EPIC Wealth Fund?" / "Why India?" | Promotional tone, but it is existing content | Kept verbatim, styled neutrally |
| C3 | Investment Notification page and PDF ("Send" button, "commission payments cannot be processed without this form") | A functional operational document, not lead generation | Kept; the PDF is served byte-for-byte unaltered |
| C4 | Entry notice **ACCEPT / DECLINE** buttons | Functional gate, not a sales prompt | Kept as a plain dialog if you want it (see D6) |
| C5 | "Contact" menu item and contact details | Factual contact information | Kept as an ordinary nav link, not styled as a button |
| C6 | "(LINK)" and "HERE" link text | Not CTAs but non-descriptive links | Visible text unchanged; screen-reader context added |

## D. Items where the new build would differ from the live site (all need a yes/no)
| ID | Difference | Default until you decide |
|---|---|---|
| D1 | **Soft-404 fix:** unknown URLs return a real HTTP 404 with a useful page (no 302 → 200) | Yes |
| D2 | `/index.php`, `/home` → 301 to `/`. `/component/users/` (login page) and RSS/Atom feeds not carried over | Yes |
| D3 | Add canonical URLs, `sitemap.xml`, `robots.txt` (allow all + sitemap), per-page `<title>` kept as is | Yes |
| D4 | Fix viewport (remove `maximum-scale=1`), logo alt text (live: "The Global Wealth Account" → "Global Wealth Management Solutions"), descriptive alt text on portraits/fund logos (live: "fund ask web", "logo pecora" on non-Pecora pages) | Yes — metadata only, no visible content |
| D5 | **Google Analytics/GTM:** not included in the new build | Omitted until you approve a plan (see `04` §3.1) |
| D6 | **Entry notice and cookie bar:** if the build uses no cookies and no analytics, the cookie bar has nothing to ask. The entry notice text can stay as an accessible dialog (shown once per session, no cookie). | Entry notice kept (text unchanged); cookie bar dropped; Decline wording for you to decide |
| D7 | **Typos and wording in existing content are preserved**, e.g. "Global Wealth Managent Solutions on LinkedIn", "a institutional risk framework", "Resilience’ focus", "(iv)" numbering. I will list all of them for your approval rather than fix them. | Preserve; list for approval |
| D8 | Disclaimer says "buying any product from this site" — see `04` item 10 | Preserve until policy review |
| D9 | Contact e-mail addresses are cloaked by Joomla JavaScript; in the new site they are real `mailto:` links, which expose addresses to scrapers | Needs your choice: plain `mailto:` links, or a tiny script that assembles them (links then absent without JavaScript) |
| D10 | Team and contact pages carry personal data (names, mobiles). Preserved as is. | Preserve |
