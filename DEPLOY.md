# Deploying `dist/`

`dist/` is the complete, ready-to-upload static output: **plain HTML/CSS/JS/fonts/images. No PHP, CMS, database or build step is needed on the server.** Upload the *contents* of `dist/` to the web root.

## Status
All 23 pages are built (Home, Funds, the 7 fund pages, About, Meet the Team, 5 regional pages, Platforms, Investment Management Solutions, Structured Products, Contact, 3 policy pages) plus 404. **Still hold off deploying over the live site** until you have approved the open items in `docs/10-build-and-test-results.md` (placeholders: team photos and vCards; policy wording review; contact e-mail handling). Nothing has been deployed and DNS is untouched. Use a staging URL first.

## Structure
Every page is a flat `.html` file in the web root (`about-gwms.html`, `funds.html`, …). Assets sit in their own folders: `css/ js/ fonts/ img/ img/funds/ img/platforms/ img/investment/ img/team/ vcards/`, each with a blank `index.html`. Old extensionless URLs (`/about-gwms`) are 301-redirected to the `.html` file by `.htaccess`.

## SiteGround (Apache)
1. Upload `dist/*` (including the hidden `.htaccess`) to `public_html/` of a **staging** subdomain first.
2. `.htaccess` provides: custom 404 (`/404.html`), no directory listing, 301s from the old `/index.php`, `/home` and `/index.php/<page>`, and 410 Gone for the retired Investment Notification page, its PDF and Joomla's `/component/…`.
3. Old extensionless URLs (`/funds`, `/about-gwms`, `/about`, …) are 301-redirected to `<name>.html` by the last rules in `.htaccess`.
4. HTTPS and `www` → non-`www` redirects are host settings (SiteGround → Site Tools → Security → HTTPS Enforce); not part of this folder.

## Portability
| Host | What to use |
|---|---|
| Apache / SiteGround | `dist/.htaccess` (included) |
| Nginx | `error_page 404 /404.html; location / { try_files $uri $uri.html $uri/ =404; } location = /index.php { return 301 /; } location = /home { return 301 /; } location ~ ^/index\.php/(.+)$ { return 301 /$1; } location = /investment-notification-form { return 410; } location ^~ /images/documents/ { return 410; } location ^~ /component/ { return 410; }` |
| Netlify / Cloudflare Pages | `/index.php /  301` · `/home /  301` · `/index.php/*  /:splat  301` · `/investment-notification-form  /404.html  410` · `/images/documents/*  /404.html  410` · `/component/*  /404.html  410` in a `_redirects` file |
| Anything else | Serve `dist/` as static files; set the 404 document to `/404.html` |

Pages use **relative** URLs (they open straight from disk) except `404.html`, which uses root-absolute paths because hosts serve it at any URL depth; if the site is ever served from a sub-folder rather than a domain root, only `404.html` needs its paths adjusted.

## What the site does and does not do
No third-party requests until a visitor clicks Accept in the cookie bar; then Google Analytics 4 (G-4F1S9L903X) loads from googletagmanager.com. No external fonts or CDNs. First-party cookies: `gwms_cookies` (choice, 12 months) and `gwms_notice` (notice acceptance, 30 days, only if accepted). Google Analytics sets `_ga` and `_ga_4F1S9L903X` only after Accept. Outbound links: LinkedIn, the Blackstone press release (ASK page) and `https://google.com` (Decline on the entry notice).

## Rebuild
`python3 tools/extract_bodies.py` (only if the captured live text is re-extracted) and `python3 tools/make_preview.py` regenerate `dist/` from one shared definition (nav, footer, pages) plus `tools/content/*.html` (page text) and the asset sources in `preview/css|js|img|fonts|vcards`. Not needed to deploy; only to change the site.
