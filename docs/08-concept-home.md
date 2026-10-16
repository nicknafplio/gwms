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
