# 09 · Funds index page (new page, DRAFT) — version 2

`preview/funds/index.html` (URL `/funds`) · screenshots `preview/screenshots/funds-page-desktop.jpg`, `funds-page-mobile.jpg`.

**v2 (per owner):** an enlarged version of the grouped fund list from the old side navigation, replacing the v1 card grid.
- Framed hero titled "Funds" (same photo/veil/band recipe as home).
- At the top, the existing sentence: *"Our portfolio comprises ‘best-of-breed’ solutions to meet the needs of discerning intermediaries and their investors."* (verbatim, home-page text).
- Four groups (Multi Asset, Equities, Fixed Interest, Alternative Strategies) in two columns on desktop, one on mobile: bold navy group label with the offset-square marker, then large ruled rows (22 px serif) with the same blue-square/silver-arrow links (and hover) as the home page.
- Fund names are the main-menu labels ("ASK Indian Entrepreneur Fund" everywhere, per decision). No logos on this page for now; the v1 card version is in git history (commit `a1d81e1`) if you want to compare or combine.

**Measured:** axe-core (WCAG 2.0–2.2 A/AA + best-practice), desktop 1440 and mobile 390: 0 violations, no horizontal overflow, no console errors.

**Open points**
1. The Levendi row still reads "Levendi Thornbridge Defined Return Fund" although the fund was acquired by Causeway (see `08` rev. 16); wording to confirm.
2. Fund logos could return as small marks beside each row — say if wanted.
3. The Funds nav button still only opens the dropdown; it could also link to this page.
