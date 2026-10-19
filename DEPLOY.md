# Deploying `dist/`

`dist/` is the complete, ready-to-upload static output: **plain HTML/CSS/JS/fonts/images. No PHP, CMS, database or build step is needed on the server.** Upload the *contents* of `dist/` to the web root.

## ⚠ Do not deploy this over the live Joomla site yet
Only **3 pages are built** (Home, Funds, ASK Indian Entrepreneur Fund) plus the 404 page. The live site has 22 pages. Deploying now would turn the other 19 (About, Team, Contact, Platforms, the other six funds, Investment Management Solutions, Structured Products, the five regional pages and the three policy pages) into 404s, and the menu, footer and home page already link to them. Deploy only to a staging URL until the remaining pages are built. Nothing here has been deployed and DNS is untouched.

## SiteGround (Apache)
1. Upload `dist/*` (including the hidden `.htaccess`) to `public_html/` of a **staging** subdomain first.
2. `.htaccess` provides: custom 404 (`/404.html`), no directory listing, 301s from the old `/index.php`, `/home` and `/index.php/<page>`, and 410 Gone for the retired Investment Notification page, its PDF and Joomla's `/component/…`.
3. Apache adds the trailing slash to folder URLs itself (`/funds` → `/funds/`).
4. HTTPS and `www` → non-`www` redirects are host settings (SiteGround → Site Tools → Security → HTTPS Enforce); not part of this folder.

## Portability
| Host | What to use |
|---|---|
| Apache / SiteGround | `dist/.htaccess` (included) |
| Nginx | `error_page 404 /404.html; location = /index.php { return 301 /; } location = /home { return 301 /; } location ~ ^/index\.php/(.+)$ { return 301 /$1; } location = /investment-notification-form { return 410; } location ^~ /images/documents/ { return 410; } location ^~ /component/ { return 410; }` |
| Netlify / Cloudflare Pages | `/index.php /  301` · `/home /  301` · `/index.php/*  /:splat  301` · `/investment-notification-form  /404.html  410` · `/images/documents/*  /404.html  410` · `/component/*  /404.html  410` in a `_redirects` file |
| Anything else | Serve `dist/` as static files; set the 404 document to `/404.html` |

Pages use **relative** URLs (they open straight from disk) except `404.html`, which uses root-absolute paths because hosts serve it at any URL depth; if the site is ever served from a sub-folder rather than a domain root, only `404.html` needs its paths adjusted.

## What the site does and does not do
No analytics, trackers, cookies, external fonts, CDNs or third-party requests (measured). The entry notice uses `sessionStorage` (cleared when the tab closes). Outbound links only: LinkedIn, the Blackstone press release (ASK page) and `https://google.com` (Decline).

## Rebuild
`python3 tools/make_preview.py` regenerates `preview/` and `dist/` from one shared definition (nav, footer, pages). Not needed to deploy; only to change the site.
