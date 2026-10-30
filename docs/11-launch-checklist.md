# Launch checklist (production)

Status: **built and tested = [x]**, **needs a decision or action from you = [ ]**.  Not legal advice; the policy items are drafts for your advisers.

## A. In the build (done)
- [x] Single launch build in `dist/` (default addresses https://globalwms.com); staging build is separate (`dist-staging/`, noindex).
- [x] 404 page + `.htaccess` ErrorDocument; old Joomla URLs 301-redirected to the new `.html` pages; retired pages return 410.
- [x] sitemap.xml and robots.txt (production addresses).
- [x] Open Graph / Twitter tags + 1200x630 preview image on every page; canonical links.
- [x] Favicons (ico, 16/32 png), Apple touch icon, 192/512 icons, `site.webmanifest`, theme colour (new).
- [x] Security headers in `.htaccess` (new): X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy and a Content-Security-Policy limited to this site plus Google Analytics. `tools/test_csp.cjs` serves every page with the policy and reports no violations (Google calls were stubbed, so test with real Analytics on staging, see B).
- [x] Compression and browser caching rules (new); CSS/JS/map links carry a version tag so updates are picked up.
- [x] Cookie bar; Google Analytics 4 (G-4F1S9L903X) only after Accept; accessibility checks (axe) clean on every page; Lighthouse 98-99 desktop, 90-99 mobile (local).

## B. Before you switch (checks on the staging site)
- [ ] Open staging with the browser developer console. Accept cookies and browse: there must be **no red "Content Security Policy" errors**. If Google Analytics is blocked, note the blocked address and tell me; I'll add it.
- [ ] In Google Analytics (Admin > Realtime), confirm hits arrive after Accept and none after "Only essentials". Check the data stream's website address is globalwms.com, set data retention (default 2 months; up to 14), and confirm a data processing agreement with Google is accepted.
- [ ] Test the redirects on the host (not testable here): `/about-gwms`, `/about`, `/meet-the-team/25-david-parker`, `/investment-notification-form` (should be 410), a made-up address (custom 404 page).
- [ ] Test link previews with real links (WhatsApp, LinkedIn): see DEPLOY.md.
- [ ] Open the site on a real phone and in Safari/Firefox (only Chromium was tested).

## C. Hosting actions (SiteGround)
- [ ] Back up the current live Joomla site and database before replacing it. Keep the backup.
- [ ] Lower the DNS TTL a day before if DNS changes are involved. **No DNS or deployment change is made by me.**
- [ ] HTTPS: certificate active for globalwms.com and www; enable the HTTPS redirect (Site Tools > Security > HTTPS Enforce, or uncomment the https rule in `.htaccess`).
- [ ] Choose one address (www or non-www) and redirect the other to it (host setting or `.htaccess`).
- [ ] After https works everywhere, enable HSTS (line left commented in `.htaccess`).
- [ ] Upload `dist/` contents to the web root (hidden `.htaccess` included). Do not upload `dist-staging/`. Remove any old Joomla files, `administrator/`, `configuration.php` etc. from the web root so they cannot be reached.
- [ ] SiteGround caching (SG Optimizer): flush the cache after upload; disable HTML minify/combine features that could rewrite the pages.
- [ ] Submit sitemap.xml in Google Search Console and Bing Webmaster Tools; check the old URLs redirect (Coverage report) in the following weeks.
- [ ] Optional: `/.well-known/security.txt` with a security contact (needs a mailbox you choose).

## D. Content and legal (owner decisions)
- [ ] **Policy review stage 2** (docs/04): Privacy Notice, Cookie Information, Disclaimer and the entry notice are drafts or client text; get your compliance adviser's sign-off. Open facts still needed: legal entity details, hosting country, the Privacy Notice statements on servers/transfers, whether the notice-acceptance cookie needs consent, retention periods (30 days / 12 months were my choices).
- [ ] FCA financial-promotion check of the fund pages and the factsheet/ US-persons wording (the Pecora Arena factsheet says it is not suitable for US investors).
- [ ] Contact page / team: confirm region allocations; real vCards and photos for team members still placeholders where noted (Mike Kew's contact vCard is real; other vCards were generated from page data); Mike Kew full details.
- [ ] Unique meta descriptions: all pages currently share "Global investors deserve better - now you can provide it". Better for search results to have one sentence per page; I can draft them for your approval.
- [ ] Optional: structured data (Organization schema) and an accessibility statement.

## E. After launch
- [ ] Re-test cookie bar and entry notice on the live domain; flush WhatsApp/Facebook previews (Sharing Debugger).
- [ ] Watch Search Console and Analytics for 404s; add redirects for any old address that still gets traffic.
- [ ] Remove `dist-staging/` from the repository when no longer needed.
