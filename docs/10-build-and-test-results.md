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
