# 02 · Proposed mega-menu structure

Rule applied: **every label below is an existing label**. Anything new, reordered or merged is marked ⚑ and needs your approval before the full build.

## Structure

```
[Logo → Home]   Platforms   Funds ▾   Investment Management Solutions   Structured Products   About us ▾   Contact
```

### Funds ▾ — panel with four groups (existing groupings)
| Group | Links (existing menu labels) |
|---|---|
| Multi Asset | 1OAK Multi Asset (MA80) Fund (Growth) · EPIC Wealth Fund (Balanced) |
| Equities | ASK Indian Entrepreneur Fund · Pecora Chatrier Equity (Value) |
| Fixed Interest | Pecora Manning & Napier High Yield Bond Strategy |
| Alternative Strategies | Levendi Thornbridge Defined Return Fund · Pecora QMS |

### About us ▾ — panel with two groups
| Group | Links |
|---|---|
| About GWMS | About GWMS · Meet the team |
| Regions ⚑ | Africa · Americas & Caribbean · Asia · Europe · Middle East |

### Direct links
Platforms · Investment Management Solutions · Structured Products · Contact. "Home" is the logo on desktop and the first item on mobile.

## ⚑ Items needing your approval (none applied silently)

| # | Change | Why | Alternative |
|---|---|---|---|
| N1 | One merged bar instead of today's two bars (primary + secondary) | Two stacked bars are hard to scan; order kept: Platforms, Funds, IMS, Structured Products, then About us, Contact | Keep two bars |
| N2 | Fund group order: Multi Asset → Equities → Fixed Interest → Alternative Strategies | The live dropdown and the live side list disagree; this order matches the side list and two of three sources. | Dropdown order (Multi Asset → Alternative Strategies → Equities → Fixed Interest) |
| N3 | New group label **"Regions"** over the five region pages | The region pages (contact details by territory) are currently reachable only from a side list on the About pages — easy to miss. The label is new text. | Leave them out of the menu; or label "Contacts by region" |
| N4 | Fund links drop the logo thumbnails | Thumbnails are 150×54 px rasters, inconsistent, and make the panel heavy. Logos remain on each fund page. | Keep thumbnails in the panel |
| N5 | ASK label: menu says "ASK Indian Entrepreneur Fund" (matches the page title); side list says "ASK Capital India Entrepreneur Fund" | Same page, two names. Preview keeps each label where it is today. | Pick one everywhere |
| N6 | "Documents" (menu) vs "Investment notification" (side list) vs page title "Investment Notification" | Three names for one page that holds one form. Menu label kept as is. | Use "Investment notification" |
| N7 | Home-page "Funds" link goes to the **Levendi** fund page, not to a Funds overview | Looks like a placeholder; preserved as is. A Funds overview page would be new content. | Link "Funds" to open the Funds panel; or approve a plain index page listing the existing fund links |
| N8 | Page titles kept (e.g. "Home page"), same description on every page | Preserving per brief. I recommend page-specific titles — flagged, not changed. | |

## Behaviour (implemented in the preview and tested — see `06-preview-test-results.md`)

- `<nav aria-label="Main">`; each panel opens from a real `<button aria-expanded aria-controls>`; links are ordinary `<a>`; current page = `aria-current="page"`.
- Opens by **click / tap / Enter / Space** only. Deliberately **not on hover**, so mouse, touch and keyboard behave identically and nothing flickers. ArrowDown on a button opens it and moves to the first link.
- **Escape** closes and returns focus to the button. Opening one panel closes the other. Click outside, or tabbing out of the open item, closes it.
- **Mobile (< 70rem):** a "Menu" button reveals a full-width list; Funds and About us are accordion sections (independent). Escape collapses a section first, then the menu.
- **No JavaScript:** the whole list renders expanded and every link works (tested with JS disabled).
- Visible focus rings (3px, ≥3:1), no motion, honours `prefers-reduced-motion`.
- The nav is generated from one data definition (`tools/make_preview.py`) so the header is never hand-duplicated.
