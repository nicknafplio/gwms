# GWMS static website — redesign

Replacement for https://globalwms.com (Joomla), built as ordinary static HTML/CSS/JS. **Nothing here has been deployed; production is untouched.**

**Built (in `dist/`, ready for a staging site — see `DEPLOY.md`):** all 23 pages as flat `.html` files in the root, 404, robots.txt, sitemap.xml, `.htaccess`.

| Read first | |
|---|---|
| `DEPLOY.md` | How to deploy `dist/` (SiteGround/Apache, nginx, Netlify) and why not to deploy it over the live site yet |
| `docs/10-build-and-test-results.md` | What `dist/` contains and what was measured |
| `docs/05-decisions-and-questions.md` | What I need you to decide |
| `docs/01-audit-inventory.md` | Pages, navigation, documents, assets, dependencies, access gaps |
| `docs/02-navigation-proposal.md` | Proposed mega menus; every non-existing label flagged |
| `docs/03-visual-direction.md` | Reference study and the GWMS design system |
| `docs/04-policy-inventory.md` | Disclaimers/policies inventory and issues (no redrafting yet) |
| `docs/06-preview-test-results.md` | Measured vs not-yet-measured |
| `docs/url-map.csv` | Old → new URL map (all existing URLs preserved) |

## View the site (no install needed)
Open `dist/index.html` in a browser (links are relative, so it works from disk), or serve it:
```
python3 -m http.server 8766 --directory dist
```
`preview/` now holds only the asset sources (css, js, fonts, img, vcards) and screenshots; pages are generated into `dist/`.

## Tools (`tools/`)
| Script | Purpose |
|---|---|
| `extract_bodies.py` | Cleans the captured live page text into `tools/content/*.html` |
| `make_preview.py` | Builds `dist/` (all pages, header/nav/footer shared, 404, sitemap, `.htaccess`) |
| `compare_content.py` | Word-for-word comparison of a built page against `audit/baseline/text/` |
| `test_preview.cjs` | axe + keyboard + mobile + no-JS tests (needs Playwright and axe-core; set `AXE_PATH`) |
| `shoot_preview.cjs` | Regenerates `preview/screenshots/` |
| `crawl.py`, `extract.py`, `shoot_live.cjs` (in `audit/tools/`) | The audit crawl and live-site screenshots |

## Layout
`audit/baseline/` live-site snapshot (HTML, text, assets, PDF, screenshots) · `design-assets/supplied/` files you supplied · `preview/` the preview site · `docs/` review documents.
