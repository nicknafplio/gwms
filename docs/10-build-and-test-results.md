# 10 · Build of Home, Funds and ASK pages — results

Built 19 Oct 2026 into `dist/` by `tools/make_preview.py`. Tested against a local static server with Playwright/Chromium + axe-core.

## What `dist/` contains
`index.html` (Home) · `funds/` · `ask-capital-india-entrepreneur-fund/` · `404.html` (existing 404 wording; `noindex`) · `robots.txt` · `sitemap.xml` (3 URLs) · `.htaccess` · `css/ js/ fonts/ img/` (824 KB total; images only if referenced).

**Design decisions applied:** Home = approved concept home. Funds = the v2 list page. ASK = the originally built layout (white page, grouped side list, article, footnote) with the new header/mega menus and the new footer; ASK logo is the supplied dark SVG. Levendi keeps its existing name and uses the Causeway logo. ASK is labelled "ASK Indian Entrepreneur Fund" everywhere. Entry notice kept (existing wording, DECLINE → https://google.com).

## Measured
| Check | Result |
|---|---|
| axe-core (WCAG 2.0–2.2 A/AA + best-practice): Home, Funds, ASK, 404 × desktop 1440 / mobile 390 | **8/8 pages: 0 violations**; also 0 with the entry notice open |
| Console errors, failed requests, broken images, horizontal overflow | none on any page |
| Third-party requests | **none** (only the local server) |
| Cookies set | **0** |
| Navigation tests (keyboard, Escape, focus, mobile accordion, no-JS, header hide) | all pass (22 checks) |
| Entry notice | shown first visit; ACCEPT closes and is remembered for the browser session; Escape does not dismiss; DECLINE → https://google.com |
| Content vs live baseline | ASK page body text **identical** (242 words, `docs/dist-content-check.txt`); Home: all original sentences present |
| Pages open directly from disk (`file://`) | yes, no errors |

## Not measured / not done
- Lighthouse timings, Safari/Firefox/real devices, screen readers, print layout, hero-text contrast over the photo.
- **19 pages are not built**: 20 distinct links on the built pages go to them (About, Team, Contact, Platforms, IMS, Structured Products, six other funds, five regions, three policy pages) and 404 until built.
- Browser-tab icon is still the PNG GW tile; touch-icon sizes and `manifest.json` not regenerated.
- Policy text is **unchanged**; the entry notice's "Cookie Statement" paragraph says the site uses cookies although the new site sets none — kept verbatim pending the policy review (`04-policy-inventory.md`); `sessionStorage` use should be covered there.

## Update 19 Oct (later): home link, overlay animation, strapline
- **Home, under the statement:** a text link "Funds" → `/funds`, styled like the "About GWMS" link (existing label, no new copy).
- **Overlay animation (hero and Funds panel, plus the Funds-page hero which shares the hero component):** three layers, all `ease-in-out`, `alternate`, `infinite`: the wide light band drifts toward the top-right and back (22 s per leg), the narrow band (26 s), and the navy→blue gradient shifts (30 s). Only `clip-path` / `background-position` change. Durations differ so the motion never repeats mechanically. The footer panel is **not** animated. Verified by computed style and by freezing the animations at 0 / 11 s / 22 s (`preview/screenshots/anim-hero-sequence.png`, `anim-funds-sequence.png`). The animation runs for everyone (reduced-motion handling discarded by owner decision).
- **Home hero strapline:** 15% smaller (measured 96 → 81.6 px at 1440 wide; ratio 0.850 at 1440, 1100 and 390 wide). The Funds-page title is unchanged.
- Re-tested after the changes: navigation/keyboard/mobile/no-JS/header-hide checks and the dist checks (axe 0 violations on all pages, no errors, no third-party requests, no cookies) all pass.

## Animation speed (19 Oct, later)
Overlay animation 5% faster (durations ×0.95): wide band 22 → 20.9 s, narrow band 26 → 24.7 s, gradient 30 → 28.5 s per leg. Still ease-in-out, alternating, infinite. Hero, Funds panel and the Funds-page hero (shared component).

## EPIC logo (home Funds section)
EPIC logo a further 5% smaller (height 6.75rem → 6.41rem). The Funds page no longer uses cards, so only the home carousel is affected.

## Mobile home refinements (below 52rem only)
Hero text centred; decorative square on its own line; arrow anchor link (`#statement`) added; Funds panel vertical padding reduced; Funds logos ~40% smaller. Desktop CSS unchanged. Measured: no horizontal overflow at 390px; screenshot `preview/screenshots/dist-home-mobile.jpg`.


## Full site build (all 23 pages)
**Structure:** all pages are flat `.html` files at the root; assets in `css/ js/ fonts/ img/ img/funds/ img/platforms/ img/investment/ img/team/ vcards/`, each folder with a blank `index.html`. Old extensionless URLs are 301-redirected by `.htaccess`; `docs/url-map.csv` regenerated.

**Page layouts:** fund pages (1OAK, EPIC, Levendi/Causeway, Pecora x3) follow the ASK page (Funds side navigation, heading, dark logo, prose). About, Meet the Team and the five regions use the same layout with an About-us side navigation. Platforms (Veritas Life logo), Investment Management Solutions (Resilience logo), Structured Products, Contact and the three policy pages use the same frame without a side navigation. Meet the Team keeps the original list layout (photo, name, role, bio) in the new design.

**Measured (Chromium 1.56 via Playwright, local server):** `tools/test_dist.cjs`: 60 checks passed - axe (WCAG 2.0/2.1/2.2 A/AA + best practice) 0 violations on all 24 pages at 1440 and 390 px; no console/network errors; no horizontal overflow; no broken images; no third-party requests; no cookies; 0 broken internal links/assets across the 24 pages; every folder has an index.html.
**Content comparison (`tools/compare_content.py` against the captured live text):** identical word-for-word for the 7 fund pages, About, IMS, Structured Products, Disclaimer and Cookie Information. Only expected differences: (a) e-mail addresses (see below), (b) added page headings "Platforms" and "Meet the Team" (the live pages had none; labels are the existing menu labels), (c) the "vCard" links on Meet the Team.
**Not measured:** other browsers, screen readers, Lighthouse, real-device touch, no-JS pass on the new pages.

**Changes needing your confirmation**
1. **Team photos / vCards are placeholders:** every person uses `img/team/duffprofile.jpg` and a blank `vcards/<name>.vcf` (0 bytes). Replace the files, same names. The "vCard" download link is new (requested).
2. **Dawn Parker** removed from Meet the Team (page, vCard, old URL now 410). She is still listed on the Contact page (existing content) - say if she should go from there too.
3. **Individual team-member pages** captured from the live site and built (`team-<name>.html`; word-for-word identical, checked). Photos/vCards on them are the placeholders.
4. **E-mail:** shown everywhere as `name [at] globalwms.com`; no address or `mailto:` target exists in the served HTML or rendered DOM; the link's `mailto:` is assembled in `js/mail.js` only when activated (click/tap/Enter). Without JavaScript the same text is shown (no link).
5. **Privacy Notice:** the two broken links ("/about", "/cookie-information.") now point to About GWMS and Cookie Information; wording unchanged. Policy wording is still the live text, unreviewed; the Cookie page still describes Google Analytics although the new site has none (policy review stage 2).
6. **Logos:** Veritas Life and Resilience SVGs used as supplied (the Resilience file is a traced bitmap, ~50 KB; Veritas has empty space under the wordmark).
7. Region pages: phone numbers that were links on the live site remain links.

## Update: team-member pages, e-mail, entry-notice cookie
- 5 team-member pages added (28 pages in total). Test run: 76 checks passed (axe 0 violations on every page at 1440 and 390 px, no broken links, no third-party requests).
- **Entry notice:** wording unchanged (verbatim from the live site). ACCEPT now sets one first-party cookie, `gwms_notice=1` (30 days, `SameSite=Lax`, `Secure` on https), which matches the Cookie Information page ("a cookie is created that tells whether or not to display the popup"). Nothing is set before ACCEPT or on DECLINE. If cookies are unavailable (blocked, or opened from disk) it falls back to `sessionStorage`. **The 30-day lifetime is my choice, not a stated GWMS fact** - change `DAYS` in `js/notice.js`.
- Note: the Cookie Information page still describes Google Analytics and a CMS session cookie, which the new site does not use (policy review stage 2).

## Update: Mike Kew, number edits
- **Mike Kew** (International Sales Director) added to Meet the Team below David Parker, with his own page `team-mike-kew.html`, the supplied bio, the photo placeholder and a blank `vcards/mike-kew.vcf`. His contact details are **placeholders**: e-mail and mobile read "[… to be confirmed]" (I did not invent an address); the website line is the existing company one. The vCard link and bio wording are new content supplied by the owner and are not part of the live-site comparison.
- Simon Voysey's page: job title "Partner" -> "International Sales Director".
- Numbers removed/replaced on team-member pages (owner instruction): David Parker 01525 862420 removed; Simon Voysey 01525 863774 removed; Sarah Crow 01525 62420 -> +44(0)7876 757253; Jessica French 01525 863780 -> +44(0)7788 205487. (Contact page numbers are unchanged.) These edits are held in `MEMBER_EDITS` in `tools/extract_bodies.py` so a re-extract keeps them.
- Test run: all checks pass on 29 pages.

## Update: banners, portrait style, Contact
- Banners (same framed gradient banner as the Funds page, page title as the h1) added to Meet the Team, Contact, Platforms, Investment Management Solutions and Structured Products. On Platforms and Investment Management Solutions the partner logo now sits below the banner.
- Portrait style (team list and team-member pages): rounded corners, hairline edge and soft drop shadow, 3:4 portrait crop; the dark-blue left border is removed from photos (and from the team list rows).
- Contact page: Emily Karavla and Asma Choudhary removed (`REMOVED_PEOPLE` in `tools/extract_bodies.py`). Dawn Parker remains on the Contact page.
- Test run: 78 checks pass on 29 pages.

## Update: Mike Kew list entry, Dawn Parker on Contact
- Mike Kew's bio now appears only on his personal page; the team list shows name, photo and title only.
- Dawn Parker removed from the Contact page (she is now removed everywhere on the site).

## Update: team photos
Photos supplied by the owner added for David Parker, James Bottomley, Simon Voysey, Sarah Crow and Jessica French (matched to the live-site portraits by image comparison). The Meet the Team list uses a square crop to face and shoulders (`img/team/<name>-square.jpg`); each personal page uses the full 3:4 portrait (`img/team/<name>.jpg`). Mike Kew still uses the placeholder. Crops were set by eye; tell me if any should be re-framed.

## Update: team thumbnails, personal-page photo, Mike Kew photo
- Meet the Team thumbnails now mirror the GW icon (photo square over an offset grey `#C6C5C7` rounded square, via CSS `box-shadow`); they are grayscale (CSS `filter`) and fade to colour over 0.5 s on hover or keyboard focus within the row. Personal-page portraits are 75% larger (8rem to 14rem wide). Mike Kew's photo added (full portrait and square crop).
- Team thumbnail grey offset reduced to 8px (all widths).

## Update: Mike Kew contact details; partner-logo column
- Mike Kew: title "UK Sales Consultant" (list, page, card); mobile +44(0) 07802 949751 (as supplied); e-mail michael.kew [at] globalwms.com (same obfuscation as elsewhere); `vcards/mike-kew.vcf` is now a real vCard 3.0 (name, organisation, title, mobile, e-mail, website) and downloads from his card and the team list. Note: an address inside a downloadable .vcf is plain text. The other vCards are still blank placeholders.
- Platforms and Investment Management Solutions: partner logo moved to a right-hand column on desktop (>= 60rem) at 80% of the column width; above the text on smaller screens.

## Update: vCards for everyone, Simon Voysey's title in regions, personal-page layout
- **vCards:** each person now has a real vCard 3.0 (`vcards/<name>.vcf`: name, organisation, job title, mobile, e-mail, website) generated at build time from the contact details on their page, so the two cannot drift apart. Phone numbers are normalised to +44 international form (the "(0)" is dropped). Dawn Parker's file was removed earlier. As noted, e-mail addresses inside a downloadable vCard are plain text.
- **Regions:** Simon Voysey's "Partner" replaced by "International Sales Director" on the Europe and Middle East pages (Asia already used it). Held in `TEXT_EDITS` in `tools/extract_bodies.py`.
- **Personal pages (desktop, >= 60rem):** text in the left column, portrait in a right-hand column; stacked on smaller screens as before.

## Update: region maps, Mike Kew in Europe
- Region pages (Africa, Americas & Caribbean, Asia, Europe, Middle East) now show the supplied region map above the contact cards: the supplied cropped SVGs (Natural Earth 1:110m, public domain), shown as `<img alt="">` (decorative; the page heading names the region), 10px corner radius with a pale background and hairline border. Files: `img/regions/*.svg`. The map's highlighted countries are the supplied illustrative assignments (see the zip's README: e.g. Europe excludes Russia and Turkey), not statements of GWMS coverage - **please confirm the assignments before publishing**.
- Europe: added "Mike Kew, UK Sales Consultant - United Kingdom" with mobile and e-mail, in the same format as the other entries (`ADDED_PARAS` in `tools/extract_bodies.py`).
- Region maps: all five now share one 16:9 frame (same height at every width). Each supplied viewBox was widened/re-centred to 16:9 around its region (as the zip's README allows), so the whole region stays visible with neighbouring land as context. Edited copies are in `img/regions/`; the originals are unchanged in the zip.
- About GWMS: in the "Locations" paragraph the existing region names (Europe, Africa, Asia, The Middle East, Caribbean Islands, South America) are now links to the regional pages; wording unchanged (compare: identical). Caribbean Islands and South America both go to Americas & Caribbean.
- Region maps cropped to a wide 14:5 band (centred crop, `object-fit: cover`) for a more panoramic look, as requested.
- Region maps: the SVG files themselves are now cropped to 14:5 (not only via CSS) and span the full article width under the heading rule. CSS/JS/map URLs carry a ?v=<hash> so browsers pick up updates instead of showing a cached copy.

## Update: home, team list, About banner, Contact, bio cards
- Home: "Providing access to best of breed financial products since 2003." now in the serif heading font. Carousel logos 25% smaller on tablet/desktop (logo area 7.5rem to 5.625rem; 1OAK and EPIC scaled likewise); mobile sizes unchanged.
- Meet the Team: vCard link removed from the list; each entry is a card (whole row links to the personal page, hover lift/border/shadow, photo fades to colour).
- About GWMS: banner added (title is the existing h1 text).
- Contact: two columns on desktop (>= 60rem), full article width.
- Personal pages: the whole business card is the vCard download (stretched link) with hover/focus state; the e-mail link inside stays separately clickable.
- Overlay fade animation 5% faster on the home hero, Funds panel and all banners (durations 20.9/24.7/28.5 s to 19.86/23.47/27.08 s).
- Fund pages (all seven): title on the left (may wrap onto two lines), partner logo in a right-hand column on desktop (>= 60rem); stacked on smaller screens.
- Jessica French photos replaced with the colourised versions (square crop and full portrait).

## Update: hero GW outline and typewriter word
- **GW outline:** inline SVG tracing the logo's own G and W glyph outlines (paths from the supplied icon), stroke only, bottom-right of the home hero and cropped by the hero's bottom edge. CSS animation draws each outline slowly, holds, then undraws (17 s loop, the W starts 1.6 s after the G), echoing the line animation in the reference recording; it is original geometry and timing, not a copy of that site's artwork. Decorative (`aria-hidden`).
- **Typewriter:** the last word of "Creating long-term value" types letter by letter (95 ms/letter), stays complete for 3 s, deletes letter by letter (55 ms/letter), then "relationships", then "objectives", then loops back to "value" (`js/typed.js`). Screen readers get the static headline "Creating long-term value"; the animated text is `aria-hidden`; without JavaScript the headline reads "Creating long-term value". On phones the changing word sits on its own line so the headline height never changes. The reduced-motion preference is not handled, as decided earlier.
- **Content note:** "relationships" and "objectives" are new headline wording supplied by the owner; they are not on the live site.
- Home Funds carousel logos a further 10% smaller on tablet/desktop (logo area 5.0625rem, 1OAK 2.97rem, EPIC 4.33rem).
- Home Funds carousel logos (tablet/desktop): logo area 4rem; 1OAK 2.7rem (+15% on the proportional size); EPIC 3.76rem (+10%).
- Home Funds carousel: 1OAK logo set to 3rem (final sizes: area 4rem, 1OAK 3rem, EPIC 3.76rem).
- Page banners (Funds, About, Meet the Team, Platforms, Investment Management Solutions, Structured Products, Contact): same traced GW outline animation as the home hero, larger and pushed off the right edge so only the top of the G shows (per the supplied layout).
- Open Graph / Twitter card tags on every page: og:title 'Global Wealth Management Solutions — <page>' (home: '— Creating long-term value'), og:description = the existing site description, og:url, and a 1200x630 preview image (img/og-image.jpg: hero photo, white logo, strapline). URLs point at https://globalwms.com, so previews only work once the site is live on that domain.

## Lighthouse (measured 20 Oct 2026, local server, headless Chromium, Lighthouse run via its Node API; 5 pages)
Scores are performance / accessibility / best practices / SEO. Local-server numbers; production hosting (compression, caching headers, HTTP/2) will change performance.
| Page | Mobile (simulated slow 4G, 4x CPU) | Desktop |
|---|---|---|
| Home | 90 / 100 / 100 / 100 (LCP 3.2 s, CLS 0.001) | 99 / 100 / 100 / 100 (LCP 0.8 s, CLS 0.073) |
| Funds | 94 / 100 / 100 / 100 | 98 / 100 / 100 / 100 |
| Levendi fund page | 99 / 100 / 100 / 100 | 99 / 100 / 100 / 100 |
| Meet the Team | 93 / 100 / 100 / 100 | 99 / 100 / 100 / 100 |
| Europe | 91 / 100 / 100 / 100 | 98 / 100 / 100 / 100 |
Open items from the reports (all minor): fund logo images on the home carousel lack width/height attributes; CSS is not minified and ~half unused per page (shared stylesheets); the home hero shifts layout slightly (CLS 0.07-0.08 on desktop, under the 0.1 "good" threshold); caching headers and compression depend on the host (not set by `.htaccess` yet). Not measured: real-device performance, other browsers, screen readers.
- Home carousel fund logos now carry width/height attributes (Lighthouse 'unsized images'); displayed sizes unchanged. CSS deliberately left unminified (owner decision).
- Diagonal-stripe/overlay drift 10% faster on the home hero, Funds carousel panel and all banners (19.86/23.47/27.08 s to 17.87/21.12/24.37 s). The GW outline animation (17 s) is unchanged.
- Overlay stripe/fade animations now start at the midpoint position and run B-A-B (animation-direction: alternate-reverse) on the home hero, Funds carousel panel and all banners; the GW outline is unchanged.

## Update: Structured Products content
Page text replaced with owner-supplied copy (four headed sections plus the closing line); the live wording ('GWMS have partnered with key structured product providers who focus on providing the very best outcome...') no longer appears, so the word-for-word comparison against the live page is intentionally retired for this page. Same 640 px text column as Platforms (measured). The copy contains risk wording ('capital remains at risk', issuer obligations) that belongs in the policy/compliance review. Held in tools/content/structured-products.html (not re-extracted).
- Structured Products: closing line 'Connecting expertise with investment opportunity.' moved to a right-hand pull quote (serif, dark blue, font-size clamp(1.75rem, 0.9rem + 1.8vw, 3.25rem), blue left rule, sticky on desktop; below the text on small screens).

## Update: content offset and Legal menu
- Pages without a left-hand menu that have a banner (Platforms, Investment Management Solutions, Structured Products, Contact) are offset on desktop (>= 52rem) so the content's left edge lines up with the banner heading text (padding-left = gutter + 0.39 x banner title size; measured within 0.1 px at 840 and 1440 px widths).
- Privacy Notice, Disclaimer and Cookie Information now have a left-hand 'Legal' menu listing the three pages (so are excluded from the offset). 'Legal' as the group label is new (it matches the footer list's accessible name).
- Legal pages (Privacy Notice, Disclaimer, Cookie Information): heading and rule moved to their own row offset by the menu column, so the Legal menu and the text start level (both at the same top, measured); the menu stays sticky on scroll (measured: sits 112 px from the viewport top).
- Meet the Team: Mike Kew's list card shows a short edited bio line (owner-supplied wording); his full bio stays on his own page.

## Update: mobile section menu
All left-hand menus (Funds, About us/Regions/Team, Legal) become, below 52rem, a sticky, collapsed-by-default disclosure labelled 'Explore this section' (button with aria-expanded/aria-controls, Esc and tap-outside close it, panel scrolls if taller than the screen). Groups are preserved and the current page stays highlighted. Desktop sidebar unchanged (measured: toggle hidden, panel visible, same position). Without JavaScript the full list shows. Measured on a 390 px viewport: collapsed on load, opens on tap, Esc closes, bar stays at the top while scrolling.
- Mobile section menu now slides open and closed (row-height transition, 0.3 s; measured heights animate 0 to 389 px and back; closed content is hidden from keyboard and screen readers).
- Contact: Sarah Crow and Jessica French no longer shown as 'Partner'; Jessica's title now 'Head of Accounting & Audit' to match her bio (Sarah's already matched).
- 'Partner' removed from Sarah Crow's and Jessica French's names on Meet the Team and their personal pages.
- Jessica French: new photo (grey studio background) cropped to a 3:4 portrait for her page and a square face-and-shoulders crop for Meet the Team (both saved at 2x).

## Update: policy text corrections, titles, numbers (owner instructions)
- **Cookie Information:** removed the sentence "We use a disclaimer in line with compliance to make sure that you agree to the Disclaimer of using darwinpim.com" (it named a different domain). Policy wording change by the owner; to be recorded in the policy review (docs/04).
- **Privacy Notice:** registered address changed from "Wrest Park, Silsoe, Bedfordshire MK45 4HR, United Kingdom" to "2 Furl Close, Maids Moreton, Buckingham, MK18 1EF" (the trailing "United Kingdom" is dropped because the new address was supplied without it). The notice's other contact detail is the privacy e-mail address (obfuscated); no other postal address appears on the site.
- **Addresses found elsewhere, not changed:** the retired Investment Tracking Form PDF (not on the new site) carries "Sunnyhill House, Little Horwood Road, Great Horwood, MK17 0NZ · t: +44 (0)1525 862420" (docs/01). The live Joomla site's own footer is not reproduced in the new build.
- **Jessica French:** job title is now "Head of Accounts" on Meet the Team, her page, the Contact page and her vCard.
- **Contact numbers:** landlines replaced by mobiles, shown as "M: +44 (0)7876 757253" (Sarah) and "M: +44 (0)7788 205487" (Jessica); label changed from T: to M:.
- Cookie Information: removed the 'Content Management System Session Cookie' section (heading and its two paragraphs) because the new site has no CMS. The page still describes a Google Analytics cookie, which the new site does not use, and does not yet mention the site's one first-party cookie (gwms_notice, which remembers acceptance of the entry notice for 30 days); both are for the policy review.

## Update: cookie bar and cookie choices (DRAFT for policy review - not legal advice, not approved)
**What the site does now** (measured, 94 checks): nothing is set before the visitor chooses. After the entry notice is accepted a dark-blue cookie bar appears at the bottom with **Accept**, **Decline** (equal weight) and **More info** (links to Cookie Information).
- **Accept:** stores `gwms_cookies=accepted` (12 months) and `gwms_notice=1` (30 days, remembers acceptance of the entry notice). First-party, SameSite=Lax, Secure on https.
- **Decline:** stores only `gwms_cookies=declined` (12 months), deletes any `gwms_notice`; acceptance of the entry notice is then remembered for the browser tab only (sessionStorage), so a new visit shows the notice again.
- **Change of mind:** the Cookie Information page has a "Review your cookie choice" button that reopens the bar (needs JavaScript; without JavaScript no cookie is ever set).
- No analytics, advertising or third-party cookies exist on the site. If an optional script is ever added it must load only after `gwms_cookies=accepted`.
- Bar appears only after the notice is closed (no stacked dialogs); axe: 0 violations with the bar visible.

**Wording changes (all mine, for review):**
1. Entry notice: the "Cookie Statement" heading and paragraph were removed (as instructed).
2. Cookie bar text: "We use a cookie to remember that you have accepted our notice, so you are not asked again on every visit. Accept to allow it, or decline to be asked each visit. We do not use analytics or advertising cookies."  (Your reference bar used "By browsing this website, you agree to our use of cookies"; I did not copy that because consent by browsing is not valid consent for non-essential cookies under UK PECR/UK GDPR guidance. The retention periods 30 days / 12 months are my choices, not GWMS facts.)
3. Cookie Information rewritten: kept the existing sentences about the pop-up cookie and the allaboutcookies.org paragraph; removed the Analytics section and the CMS section; replaced the "By continuing to browse... you are agreeing" line (implied consent); added the two cookie names and durations, a "no analytics or advertising cookies" statement and the review button.
**Open for the policy review:** the Privacy Notice still says Cookies are used "to collect and use personal information about you" and refers to the cookie page; it should be aligned with the above. Whether the notice-acceptance cookie needs consent at all (it may count as strictly necessary) is a legal question for your adviser; the build is conservative (opt-in for the 30-day cookie).

## Update: Privacy Notice cookie wording (owner instruction; DRAFT for review)
- 'Some of this information may be collected using cookies and similar tracking technology...' now reads 'The cookies used on this Website do not collect any of this information...'.
- The 'Cookies and similar tracking technology' paragraph no longer says cookies 'collect and use personal information about you'; it states they are used only to remember the visitor's choices (notice accepted; cookies accepted or declined) and do not collect personal information.
- Left unchanged: the 'Information that we collect automatically' text (IP address, device type, pages visited). The cookies do not store that, but the web host's server logs normally do, so it may still be true; confirm with the host and your adviser. Headings unchanged.

## Update: Google Analytics 4 behind cookie consent (reverses the earlier "analytics dropped" decision; owner instruction)
- Measurement ID `G-4F1S9L903X`. Loaded by `js/cookie-bar.js` **only after Accept** (and on later visits while the saved choice is "accepted"); never loaded before a choice or after Decline. Configured with Google signals and ad personalisation signals off (my setting; GA4 anonymises IP addresses by default). Decline / change to Decline sets `ga-disable-G-4F1S9L903X` and removes `_ga` and `_ga_4F1S9L903X` where the browser allows it (cookies set by Google on the site's own domain).
- Cookie bar text now: "We use cookies to remember that you have accepted our notice and, if you accept, Google Analytics cookies to see how the site is used. If you decline, we set only a cookie that records your choice."
- **Cookie Information** (draft): new "Analytics Cookies" section (cookie names, up to 2 years, random identifier, Google signals off, may be processed outside the UK/EEA, Google privacy policy and opt-out links restored), "Advertising: this website does not use advertising cookies".
- **Privacy Notice** (draft): the 'collected automatically' sentence and the Cookies paragraph now say that, only if the visitor accepts Cookies, information about use of the Website is collected through Google Analytics and may include the personal information described, processed by Google possibly outside the UK/EEA; choice can be changed at any time. The previous "cookies do not collect personal information" wording was replaced.
- Tests: Google requests are intercepted in the test run; checks confirm no Google request before a choice or after Decline, and the GA4 script URL with the ID after Accept and on a later visit.
- **Not measured / for you:** that GA4 receives data (needs the live domain and your GA4 property; confirm the data stream's domain and enable Consent/IP settings in the GA admin as you prefer); whether GA4 data-retention is set (default 2 months, can be raised to 14); whether a data-processing agreement with Google is in place; the legal wording above (drafts, not approved).
- Cookie bar: 'Decline' button relabelled 'Only essentials' and the sentence now reads 'If you choose Only essentials, we set just the cookie that records your choice.' (behaviour unchanged). The Cookie Information and Privacy Notice pages still say 'decline'; align wording if you want the same term there.
- Desktop navigation: hover/focus underline is now the palette silver grey (--gw-grey) and slides in from the left (0.3 s) and out to the right; the current-page navy underline and the open-menu blue are unchanged.

## Update: 404 / .htaccess
`ErrorDocument 404 /404.html` only works when the site is at the web root of its host name. Fixed/documented in DEPLOY.md: build with `SITE_BASE=/folder` for sub-folder deployments (ErrorDocument, redirect targets and the 404 page's own links are prefixed), and the extension-less redirect test now uses `%{REQUEST_FILENAME}.html` instead of `%{DOCUMENT_ROOT}`. Not testable here (no Apache in this environment): please re-test on the host. A test now checks that the ErrorDocument target exists in dist.

## Update: "For more information ... link to the website HERE" on every fund page
Same sentence pattern, link opening in a new tab (with screen-reader text), right-arrow icon after HERE that turns palette grey and drifts right over 0.7 s on hover/focus. Added to: 1OAK (existing sentence, now with the icon; wording unchanged), EPIC Wealth Fund, Levendi Thornbridge Defined Return Fund, ASK Indian Entrepreneur Fund, the three Pecora pages and Investment Management Solutions (Resilience Asset Management). Links as supplied: 1oakgroup.com, whirelandplc.com (WHI Wealth Fund page), causeway-securities.com (Levendi page), askfinancials.com, pecoracapital.com, resilience.im.
Review points: (1) EPIC has been rebranded to WH Ireland per your note, but the EPIC page text, logo and menu still say EPIC; say if they should change. (2) The Levendi page still also carries its existing "For more information: www.levendi-im.com/..." line; remove if the Causeway link replaces it. (3) The sentence wording for the funds other than 1OAK is mine, following your template.

## Update: Platforms
Added 'For more information on Veritas Life Guernsey link to the website HERE.' (same format, arrow icon and hover as the fund pages) and the Veritas Life logo is now a link, both to https://veritaslifeguernsey.com/about-us/ (new tab, with screen-reader text). Sentence wording is mine following the fund-page template.
- 'link to the website' removed from the 'For more information' lines on every page: they now read 'For more information on X, click HERE →.' (one-word choice, easy to change). For 1OAK this edits an existing live sentence, so its word-for-word comparison with the live page now differs by that phrase (intentional).
- Full stop removed after the arrow on every 'For more information ... click HERE' line (the icon keeps a little room on the right so it does not run to the edge when it drifts).

## Update: EPIC logo replaced by the WH Ireland wordmark
From the SVG supplied by the owner (original colour #845873 stored as `wh-ireland-original.svg`), I made `wh-ireland-dark.svg` (black) and `wh-ireland-white.svg` (white): same paths and viewBox (711.3 x 70.8), fill set inline so they work in `<img>`. Files are in `img/funds/` and `design-assets/supplied/fund-logos/`. Used on the home carousel (white, 80% of card width) and the EPIC fund page (black, in the right-hand logo column). The old epic-*.svg/png were removed from the build assets (still in design-assets). Alt text is "WH Ireland". The EPIC page text and menu labels still say EPIC; names/copy not changed without your instruction.
