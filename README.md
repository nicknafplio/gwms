# GWMS static website — redesign (stage 1: audit, direction, preview)

Replacement for https://globalwms.com (Joomla), built as ordinary static HTML/CSS/JS. **Nothing here has been deployed; production is untouched.**

| Read first | |
|---|---|
| `docs/05-decisions-and-questions.md` | What I need you to decide |
| `docs/01-audit-inventory.md` | Pages, navigation, documents, assets, dependencies, access gaps |
| `docs/02-navigation-proposal.md` | Proposed mega menus; every non-existing label flagged |
| `docs/03-visual-direction.md` | Reference study and the GWMS design system |
| `docs/04-policy-inventory.md` | Disclaimers/policies inventory and issues (no redrafting yet) |
| `docs/06-preview-test-results.md` | Measured vs not-yet-measured |
| `docs/url-map.csv` | Old → new URL map (all existing URLs preserved) |

## Preview locally
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
