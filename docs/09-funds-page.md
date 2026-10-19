# 09 · Funds index page (new page, DRAFT)

`preview/funds/index.html` (URL `/funds`) · screenshots `preview/screenshots/funds-page-desktop.jpg`, `funds-page-mobile.jpg`.

**Purpose:** the plain index of the existing funds agreed earlier (it replaces the home-page "Funds" link that pointed at the Levendi fund page). **No new copy:** the only text is the page title "Funds", the four existing group names and the existing fund names; each card links to its existing fund page.

**Layout:** framed hero (same photo/veil/band recipe as the home page, shorter) → four groups in order Multi Asset, Equities, Fixed Interest, Alternative Strategies (N2, still pending your approval) → each group a responsive grid of dark gradient cards with the white fund logo → expanded footer.

**Changes elsewhere:** the concept home page "Funds" index link and footer "Funds" link now go to `/funds`.

**Measured:** axe-core (WCAG 2.0–2.2 A/AA + best-practice), desktop 1440 and mobile 390: 0 violations, no horizontal overflow, no console errors.

**Open points for development**
1. Groups with two funds leave the third column empty on desktop; alternatives: one continuous grid with group labels inline, or a left-hand group list.
2. The three Pecora cards share one logo and differ only by name/group.
3. Nothing on the page says what each fund is. That needs existing text; the fund pages have it, but I have not excerpted it here.
4. Whether the Funds nav button should also link to this page (today it only opens the dropdown).
5. The Levendi card shows the Causeway logo while its name is still "Levendi Thornbridge Defined Return Fund" (see `08` rev. 16).
