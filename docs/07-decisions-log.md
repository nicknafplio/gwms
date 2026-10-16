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
