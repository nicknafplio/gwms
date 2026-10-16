# 06 · Preview test results

Run on 16 October 2026 with Playwright 1.56 / Chromium and axe-core 4.x against the local preview server. Re-run with `tools/test_preview.cjs` (see README).

## Measured
| Check | Result |
|---|---|
| axe-core (WCAG 2.0/2.1/2.2 A+AA + best-practice rules) — Home and ASK fund page, desktop 1440 and mobile 390, with menus closed, Funds open, About open | **12 of 12 scans: 0 violations** |
| Horizontal overflow at 1440 and 390 | none |
| Browser console errors / failed requests (all captured states) | none |
| Content comparison vs live baseline — Home (24 words), ASK fund page (242 words, side navigation excluded) | **identical** (`tools/compare_content.py`; output in `preview/content-check.txt`) |
| Keyboard: skip link first; Tab reaches Funds after logo + Platforms; Enter/Space open and close; Tab enters panel; Escape closes and returns focus; ArrowDown opens and focuses first link; tabbing past the last panel link closes it; opening a second panel closes the first; click outside closes | all pass |
| Hover alone does not open a panel | pass (by design) |
| Mobile: menu hidden until opened; toggle sets `aria-expanded`; section accordion opens on tap; Escape collapses section, then menu | all pass |
| JavaScript disabled: all 19 desktop navigation links visible and usable | pass |
| Third-party requests made by the preview | **none** (all fonts, images, scripts local) |
| Contrast (computed): link blue 6.9:1, muted text 6.3:1, body text 12.7:1, footer text 10.9:1 on navy | all ≥ 4.5:1 |
| Payload (preview home, uncompressed): HTML 6.8 KB, CSS 17.8 KB (≈4 KB gzip for components.css), JS 4.1 KB, fonts 150 KB, hero image 30–153 KB depending on screen | |

## Not yet done / could not be measured
- Lighthouse / performance timings (no Lighthouse in this environment); no real-device or Safari/Firefox testing; no screen-reader (NVDA/VoiceOver) testing; no print-layout check; link checking across the full site (only 2 of 22 pages exist so far); axe cannot judge reading order or whether alt text is *meaningful*.
- Axe does not test colour contrast of text over the photographic hero: the hero title is white on a dark image under a navy gradient; I judge it adequate visually but have not measured it.
