# 07 · Decisions log (answers received)

| Date | Item | Decision |
|---|---|---|
| 2026-10-16 | Analytics (D5) | **Dropped.** No Google Analytics/GTM in the new site. |
| | Entry notice (D6) | **Kept.** Text unchanged; **Decline → https://google.com**. Acceptance remembered per browser session only (`sessionStorage`, no cookie) — to be covered in the policy review. |
| | Contact e-mail handling (D9) | Left for now (default: plain `mailto:` links). |
| | Policy facts / approver (04 §3, B5) | Left for now. Existing policy wording stays unchanged in the build. |
| | PDF and `/investment-notification-form` | **Removed from scope.** Page, PDF and its menu/side-nav entries are not rebuilt. Old URLs → 410 Gone (or a redirect if you prefer). Consequence: the site has no downloadable documents. |
| | Hidden/unpublished Joomla pages | Not needed. |
| | Photographs | Owned by GWMS (bought long ago). |
| | Typo "a institutional" | **Corrected** to "an institutional" (EPIC page). "Resilience’ focus" left as is. Other typos unchanged. |
| | Hosting | **SiteGround now, must stay portable:** plain static files; redirects supplied as `.htaccess` (Apache, SiteGround), plus `_redirects` (Netlify/Cloudflare) and an nginx snippet. No host-specific features. |
| | ASK label | **"ASK Indian Entrepreneur Fund"** everywhere (menu and side list). |
| | Home "Funds" link | **Add a plain Funds index page** listing the existing fund links (no new copy beyond existing labels and group names). |
| | Visual direction / nav N1–N4 | **Not approved — design changes requested; details awaited.** |
| 2026-10-16 | Reduced motion | **Owner decision: `prefers-reduced-motion` is discarded** (no reduced-motion handling for any future scroll-reveal/parallax). Accessibility risk noted to owner. |
| 2026-10-16 | Animated gradient (for the full build, not yet implemented) | Recreate the diagonal translucent light-band over a dark-to-mid gradient in GWMS navy `#1A3D6C` and blue `#065AA7`, using CSS only. Add a **slow looping drift toward the top-right and back again** (deliberately the mirror of the reference's top-left motion, to emulate and not copy). Keep to `transform` / `background-position`. Applies to hero (and optionally menu panel/footer); not to stats counters or sliders. White text over the lighter band must stay ≥4.5:1. Runs for all users (reduced-motion handling discarded by owner). |
| 2026-10-16 | Scroll-reveal and parallax | Technically feasible (plain CSS/JS, no library); contradicts the original "no decorative animation" brief, so only to be added when you explicitly confirm in the full build. |
| 2026-10-19 | Build scope | Build and push Home, Funds and ASK pages. **ASK and Funds keep the layout built for them** (not restyled to the concept look), with the new navigation and footer. Individual fund pages use the supplied **dark** logos (stored in `design-assets/supplied/fund-logos/dark/`; 1OAK file cropped from an A4 artboard). **Levendi keeps its old text; Causeway logo used.** Home becomes the concept home. Entry notice implemented (existing wording; Decline → google.com; remembered per browser session via sessionStorage, no cookie). |
