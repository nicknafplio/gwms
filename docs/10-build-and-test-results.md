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
