# 01 · Audit and inventory of globalwms.com

Captured **16 October 2026** from the public site over HTTPS. Raw HTML, extracted text, assets and screenshots are in `audit/baseline/` and are the reference for every later content comparison. The production Joomla site was only read, never changed.

## 1. Method and access gaps

| Done | Detail |
|---|---|
| Followed every internal link from the home page, recursively (pages, documents, images) | 22 content pages + 1 PDF + the 404 page |
| Probed ~45 guessable URLs (`/about`, `/funds`, `/news`, `/terms`, `/complaints`, `/sitemap.xml`, …) | All redirect to `/error404`; no hidden content pages found |
| Rendered the live site in Chromium (desktop + mobile), recorded cookies and third-party requests | Screenshots in `audit/baseline/shots/` |
| Read the fillable PDF's form fields | See §4 |

**What I could not see — the crawl may be incomplete:**
- Joomla administrator (`/administrator` → 401), the database, unpublished/archived articles, menu items that are hidden or access-restricted, and anything not linked from a public page.
- Server/hosting configuration, redirects defined at server level, the Google Analytics account, who hosts the site and where (needed for the privacy notice).
- `www.globalwms.com` (blocked by this session's network allow-list; not tested).
- Whether the Accept/Decline entry notice actually appears to visitors: the markup and script are present on every page, but it did not render in my headless Chromium run. The separate cookie bar *did* render.

## 2. Pages (22) — all return HTTP 200

| URL | `<title>` (existing) | Where it is reached from | Notes |
|---|---|---|---|
| `/` | Home page | Logo, "Home" | `/index.php` and `/home` also return the same page (duplicates). |
| `/about-gwms` | Exceptional wealth management solutions | About us → About GWMS | Contains LinkedIn link, FCA reference, professional connections. |
| `/meet-the-team` | Meet the Team | About us → Meet the team | 6 portraits (3 named with titles only, 3 Partners). |
| `/investment-notification-form` | Investment Notification | About us → **Documents** | Menu label ≠ page title. Hosts the PDF (§4). |
| `/contact` | Contact | Contact | Names, phone numbers, cloaked e-mail links. **No contact form.** |
| `/africa` `/americas-caribbean` `/asia` `/europe` `/middle-east` | region names | Side list on About pages only | Not in the main menu; each lists regional contacts. |
| `/platforms` | Platforms | Platforms | Veritas Life Guernsey. |
| `/1oak-multi-asset-funds-guided-by-blackrock` | 1OAK Multi Asset (MA80) Fund | Funds → Multi Asset | |
| `/epic-investment-partners` | EPIC Investment Partners | Funds → Multi Asset | Menu label "EPIC Wealth Fund (Balanced)". |
| `/ask-capital-india-entrepreneur-fund` | ASK Indian Entrepreneur Fund | Funds → Equities | Has footnote [1]. |
| `/pecora-chatrier-equity-value` | Pecora Chatrier Equity (Value) | Funds → Equities | |
| `/pecora-manning-napier-high-yield-bond-strategy` | Pecora Manning & Napier High Yield Bond Strategy | Funds → Fixed Interest | |
| `/levendi-thornbridge-defined-return-fund` | Levendi Thornbridge Defined Return Fund | Funds → Alternative Strategies | Home-page "Funds" link points here. |
| `/pecora-qms` | Pecora QMS | Funds → Alternative Strategies | |
| `/investment-management-solutions` | Investment Management Solutions | Main menu | Resilience Asset Management. |
| `/structured-products` | Structured Products | Main menu | One sentence only. |
| `/cookie-information` `/disclaimer` `/privacy-notice` | as named | Footer | See `04-policy-inventory.md`. |
| `/error404` | 404 Not Found | any unknown URL (302) | Returns **200**, not 404 (soft-404). |

**Metadata:** every page has the identical description *"Global investors deserve better - now you can provide it"*; no canonical URLs, no Open Graph tags; `<meta name="generator" content="MYOB">`; viewport has `maximum-scale=1` (blocks pinch-zoom — an accessibility failure); Joomla JSON-LD (Organization/WebSite/WebPage/Article) is present; RSS/Atom feed links exist at `/meet-the-team?format=feed&type=rss|atom`.

**Other reachable Joomla endpoints:** `/component/users/` (a public login page), `/index.php/<alias>` duplicates of each page. No `sitemap.xml`; `robots.txt` is the Joomla default (blocks only system folders).

## 3. Navigation as it exists today

- **Primary bar:** Home · About us ▾ (About GWMS, Meet the team, Documents) · Contact
- **Secondary bar:** Platforms · Funds ▾ · Investment Management Solutions · Structured Products
- **Funds ▾** (hover dropdown with logo thumbnails): Multi Asset (1OAK Multi Asset (MA80) Fund (Growth); EPIC Wealth Fund (Balanced)) · Alternative Strategies (Levendi Thornbridge Defined Return Fund; Pecora QMS) · Equities (ASK Indian Entrepreneur Fund; Pecora Chatrier Equity (Value)) · Fixed Interest (Pecora Manning & Napier High Yield Bond Strategy)
- **Side lists:** on fund pages the same funds in a different group order (Multi Asset, Equities, Fixed Interest, Alternative Strategies) and with a different label for ASK ("ASK Capital India Entrepreneur Fund"); on About/Team/region pages: About GWMS, Meet the Team, Africa, Americas & Caribbean, Asia, Europe, Middle East, Investment notification.
- **Footer:** regulatory statement + Cookie Information · Disclaimer · Privacy Notice.

**Defects observed in the current menu** (measured, `audit/baseline/shots/live-home-desktop-first-visit.png`): the open dropdown covers the logo; "About us" and "Funds" are non-link separators so they cannot be reached without JavaScript or hover; hover-only; the submenu intercepts pointer events from its own trigger.

## 4. Documents

| File | Size | Details |
|---|---|---|
| `/images/documents/GWMS-Investment-Tracking-Form-2023.pdf` | 3.1 MB | One A4 page, fillable AcroForm (95 fields, embedded JavaScript, "Send" button), created 2011, last modified 19 Oct 2023, form version "23v11". It is the **only** downloadable document found. |

Findings inside the PDF (the file will be preserved byte-for-byte; I will not edit it):
1. Its fund drop-downs list share classes of funds **not shown on the website**: *Darwin L D/L P Fund*, *Fortunis II VC Fund*, *Leibniz Edge 2X*.
2. Its footer gives a different address and numbers from the site: *Sunnyhill House, Little Horwood Road, Great Horwood, MK17 0NZ · t: +44 (0)1525 862420* versus the privacy notice (*Wrest Park, Silsoe, Bedfordshire MK45 4HR*) and Contact page (*+44 (0)1525 863772*).
3. It states "commission payments cannot be processed without this form" — operational, kept as is.

## 5. Assets

Local: 6 team portraits, 8 logos, 4 fund thumbnails, 13 favicon/touch-icon files + `manifest.json` — all resolve (one `<!-- commented-out -->` image, `/images/logo-veritas.png`, is a 404 but is not live content). Stored in `audit/baseline/assets/`. The live logo (775×177) is not byte-identical to the logo you supplied (752×164); the build uses **your supplied file**.

## 6. Third-party and functional dependencies on the live site (measured)

| Dependency | Observed |
|---|---|
| Google Tag Manager / Analytics (`G-4F1S9L903X`) | Hard-coded in every page; **requests fire on first load, before any Accept click** |
| Google Fonts (Cinzel, Open Sans) | Requested from `fonts.googleapis.com` / `fonts.gstatic.com` |
| jQuery 3.2.1, Fancybox 3.1.25 | From `cdnjs.cloudflare.com` |
| Web357 "Cookies Policy Notification Bar" (Joomla plugin) | Cookie bar shown with *"Ok, I've understood! / Decline / More Info"*; its consent categories contain only placeholder scripts, so **Decline does not stop the analytics tag** (the tag is outside the plugin's control) |
| Entry notice (Fancybox modal) | Text *"Notice … deals exclusively with Intermediaries … Cookie Statement …"* with **ACCEPT** and **DECLINE** (Decline → `https://google.com`) |
| Cookies set on first visit | `aa75833e…` (Joomla session, secure, HttpOnly) and `popupGWMS=Disclaimer`; plus Google's cookies once the tag runs |
| Forms | None. No contact form exists, although the Privacy Notice says one does. |
| External links | linkedin.com/company/gwms, 1oakgroup.com, levendi-im.com, blackstone.com (press release), resilience.im, allaboutcookies.org, Google opt-out/analytics pages |

**New build default:** none of the above third-party items is carried over (no analytics, no external fonts, no CDN scripts) unless you approve — see decisions D5 and D6 in `05-decisions-and-questions.md`.
