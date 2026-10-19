# 08 · Concept home page (DRAFT — not approved)

Files: `preview/concept-home/index.html` · screenshots `preview/screenshots/concept-home-desktop.jpg`, `concept-home-mobile.jpg`.
Sections: framed hero → statement + index (Platforms added) → About band (photo + reworded text) → Funds carousel → expanded footer with navigation.

## New / reworded copy (needs your approval — the only text not copied verbatim from the live site)
| Where | Text | Derived from (existing About page) |
|---|---|---|
| About statement | "Providing access to best of breed financial products since 2003." | "Established in 2003, … provides access to a suite of best of breed financial products." |
| About paragraph (20 words) | "Trusted by banks, institutions, captives, trust companies, family offices and boutique fund managers for market knowledge, service and track record." | "We are trusted by banks, institutions, captives, trust companies, family offices and boutique fund managers, who value our exceptional market knowledge, excellent service levels and strong track record." Adjectives (exceptional / excellent / strong) are dropped, nothing added. |
| Link | "About GWMS" → `/about-gwms` | existing label |

Everything else is an existing label: "About us", "Funds", "Platforms", group names, fund names, footer headings, "Regions" (still the pending N3 label).

## Decisions this concept needs from you
1. Index order — I put **Platforms first** (matches the main nav); alternatives: after Funds, or last.
2. Fund cards — the cards are links showing logo, group and fund name; **no "learn more" buttons** (CTA rule). The three Pecora cards share one logo and differ only by name.
3. **ASK logo** is the only 250×74 px raster (soft when enlarged) and the Levendi logo is square; better originals would sharpen the cards.
4. Photo (supplied, Unsplash): teal in the original is shifted to blue with CSS (`hue-rotate`) and a navy tint to fit the brand — say if you prefer it untinted.
5. Gradient band: static here. Planned slow drift toward the top-right and back (see `07-decisions-log.md`) once approved.
6. Carousel: manual arrows only, no autoplay, scroll-snap, works without JavaScript as a swipeable list. Tested only visually so far — accessibility/keyboard scans not yet run on this page.
7. Hero uses the existing walkway photo with a navy veil; the white-on-photo contrast has not been measured.

## Revision 2 (per your feedback)
- Order is now: hero → statement + index → **Funds** → **About** → footer.
- Footer navigation is only Platforms · Funds · Investment Management Solutions · Structured Products, plus a LinkedIn icon (links to the existing https://www.linkedin.com/company/gwms/, opens in a new tab).
- The FCA statement sits underneath in small type. I kept the **Privacy Notice / Disclaimer / Cookie Information** links on that bottom line, because the policy pages must stay reachable from every page — say if you want them removed or moved.
- Fund logos are placeholders until you supply updated ones.

## Revision 3
Footer is four columns: (1) full logo, (2) navigation, (3) legal links (Privacy Notice, Disclaimer, Cookie Information), (4) LinkedIn icon without a circle. The FCA statement stays underneath in small type. The logo sits on a white plate because the supplied logo has dark lettering that would disappear on the navy gradient; a reversed (white) logo would need your approval as a brand change.

## Revision 4
Footer uses your white single-colour logo (`design-assets/supplied/logo-final-white.svg`, delivered with an `.ai` extension but actually an SVG) directly on the gradient, with the existing line "Creating long-term value" as the strapline underneath. The white-plate version is retired.

## Revision 5
- Second section: statement text aligned to the top with the small offset-square marker above it (as in the other sections); index links reduced to 17 px with smaller arrows.
- Footer: a "Back to top" link (`#top`) under the LinkedIn icon, drawn as a white tile with a grey offset shadow and an up-chevron, echoing the logo mark. "Back to top" is new functional UI text (not marketing copy).

## Revision 6
Footer "Back to top" → **"Top"** (screen readers announce "Top of page"), with a plain white up-chevron and no tile behind it.

## Revision 7
About-band photo swapped to the warm sunlit version of the glass corridor (`design-assets/supplied/photo-glass-corridor-warm.jpg`). The earlier blue colour-shift was removed (it turned the orange to yellow); only a faint navy tint remains at the top-left. This is a deliberate warm accent against the navy/blue palette — say if you want it cooled toward blue instead.

## Revision 8
The offset-square marker is now inline with the first line of text in every section: hero headline, second-section statement, Funds heading and About label (it was above the text in the first two).

## Revision 9
Hero diagonal band: opacity raised by 10 points (white 13%→23% at the top, 7%→17% at the bottom) and drawn above the photo veil, where it was previously hidden. Other gradient panels (Funds, footer) are unchanged.

## Revision 10
Hero band rolled back 5 points: white 18% at the top, 12% at the bottom (10 points above the original 13%/7% minus 5).

## Revision 12 (replaces Revision 11)
Revision 11 is rolled back: the Funds panel is again plain gradient + two bands (no photo). Instead the **hero overlay now mirrors the Funds panel**: the same navy→blue gradient (translucent, so the walkway photo still shows through) and the same two diagonal bands, at the Funds opacity (13% / 7%).

## Revision 13
Hero veil 5 points more transparent at every stop (navy 90→85%, mid 76→71%, blue 62→57%) so the photo shows slightly more. The diagonal bands are unchanged.

## Revision 14
Hero headline is vertically centred in the banner (was bottom-aligned).

## Revision 15 — fund logos
Five white fund logos supplied and stored in `design-assets/supplied/fund-logos/` (also copied to `preview/img/funds/`): 1OAK, ASK, EPIC, Levendi-Thornbridge, Pecora Capital.
- Applied now to the three visible home cards: **1OAK, EPIC, ASK**, shown directly on the gradient (no white plate).
- **Needs your check:** the file named *Levendi-Thornbridge-causeway* actually shows the **Causeway Securities** logo, not Levendi's. Not used anywhere yet.
- The ASK file reads "ASK Investment Managers" (the live site uses an "ASK Capital" logo and text says ASK Capital is a subsidiary of ASK Investment Managers).
- The remaining cards (Pecora ×3, Levendi) still show the old logos on white plates, so the carousel is mixed until you confirm; Pecora's white logo is ready to apply.

## Revision 16 — fund logos
Per owner: Levendi was acquired by Causeway, so the **Causeway Securities** logo is used for the Levendi card, and the supplied ASK logo ("ASK Investment Managers") stays. The three Pecora cards now use the white Pecora Capital logo, so all seven cards are consistent. Not changed: the fund name on the card ("Levendi Thornbridge Defined Return Fund") and the Levendi fund page text, which still describe Levendi — the page text should be reviewed against this acquisition (content and compliance wording, not changed here).

## Revision 17
1OAK logo scaled down (height 4.4rem, was filling the 7.5rem logo area) so it no longer outweighs the other fund logos.

## Revision 18
EPIC logo 10% smaller (height 6.75rem, was the full 7.5rem logo area).

## Revision 19 — second-section links
Arrows are now a bold, short silver (`#BCBDBF`) arrow in a blue (`#065AA7`) rounded square. On hover/keyboard focus the colours reverse (silver square, blue arrow) and the square slides left 0.7rem over 0.28s. Silver-on-blue and blue-on-silver are both ≈3.6:1 (meets the 3:1 needed for graphical controls; the link text itself is unchanged). Animation runs for everyone (reduced-motion handling discarded by owner decision).

## Revision 20 — About photo scroll crossfade
The About photo is now two stacked images: the original teal photo with the blue tint (underneath) and the new warm/orange photo (on top). `js/photo-fade.js` sets `--p` (0→1) from scroll position and the warm image's opacity follows it: 0 when the photo's top edge is at 90% of the viewport height, 1 when it reaches 30%. The navy tint fades as the orange comes in. Plain JS, passive scroll listener with requestAnimationFrame. Without JavaScript the warm photo shows. `preview/screenshots/concept-photo-fade-sequence.png` shows progress 0 / 0.5 / 1.

## Revision 21 — navigation motion
- **Dropdowns slide down/up on click.** One generic function (`slide()` in `js/nav.js`) animates the height of the panel controlled by *any* `button[aria-controls]` inside `#site-nav`, on desktop (mega panel) and mobile (accordion). To add a dropdown, add the button + panel markup; no new JS or CSS. Duration is `--slide-duration` (default 0.3s). Interrupting an animation reverses it from its current height.
- **Header slides up out of view when the footer is reached** (`js/header-hide.js`, generic: it only needs `.site-header` and `.site-footer`). It returns when scrolling back up, and never hides: at the top of a short page, while the mobile menu is open, or while keyboard focus is inside the header. Open dropdowns are closed as it hides.
- Both run for everyone (reduced-motion handling discarded by owner decision).
- Tests (`tools/test_preview.cjs`) updated for animation timing: 12 axe scans 0 violations; keyboard/mobile/no-JS checks and 4 new header checks pass. Measured on desktop: opening Funds went 13px → 68 → 177 → 387 → 389px over the sampled frames; closing 376 → 211 → 63 → 0px (sampling times are approximate).
