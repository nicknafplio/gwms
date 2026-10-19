# GWMS static website — redesign

Replacement for https://globalwms.com (Joomla), built as ordinary static HTML/CSS/JS. **Nothing here has been deployed; production is untouched.**

**Built so far (in `dist/`, ready to upload to a staging site — see `DEPLOY.md`):** Home, Funds, ASK Indian Entrepreneur Fund, 404, robots.txt, sitemap.xml, `.htaccess`. The other 19 pages are not built yet.

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

## Preview (no install needed)
Open `preview/index.html` in a browser by double-clicking it. The ASK page is `preview/ask-capital-india-entrepreneur-fund/index.html`. Plain HTML/CSS/JS; Python is only used by the optional generator.

## Preview via local server (optional)
```
python3 -m http.server 8765 --directory preview     # then open http://localhost:8765/
```
Only Home (`/`) and the ASK fund page (`/ask-capital-india-entrepreneur-fund/`) exist in the preview; other links will 404 until the full build.

## Tools (`tools/`)
| Script | Purpose |
|---|---|
| `make_preview.py` | Generates the preview pages from one shared header/nav/footer definition |
| `compare_content.py` | Word-for-word comparison of a built page against `audit/baseline/text/` |
| `test_preview.cjs` | axe + keyboard + mobile + no-JS tests (needs Playwright and axe-core; set `AXE_PATH`) |
| `shoot_preview.cjs` | Regenerates `preview/screenshots/` |
| `crawl.py`, `extract.py`, `shoot_live.cjs` (in `audit/tools/`) | The audit crawl and live-site screenshots |

## Layout
`audit/baseline/` live-site snapshot (HTML, text, assets, PDF, screenshots) · `design-assets/supplied/` files you supplied · `preview/` the preview site · `docs/` review documents.
