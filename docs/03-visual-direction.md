# 03 · Visual direction

## What I studied in the Saxenhammer reference (rendered, not just its source)

| Observed | Adapt for GWMS? |
|---|---|
| One confident geometric sans at very large sizes, set against small, quiet body text — hierarchy comes from scale, not decoration | **Yes**, as a serif/sans pairing with the same scale contrast |
| A single graphic device derived from the brand (a chevron line) repeated through the page | **Yes**, using GWMS's own device: the offset square from the GW logo mark |
| Navigation that shows hierarchy at a glance: large parent labels, lighter child links, generous spacing | **Yes**, in a restrained desktop panel with quiet group labels and hairline-ruled links |
| Full-bleed tonal photography integrated with the brand colour | **Yes**, using your supplied dark walkway photograph, left monochrome |
| Disciplined vertical rhythm and one container width | **Yes** |
| Gradients, rounded gradient hero frame, chevron animation, carousels, stats counters, news cards | **No** — promotional |
| Persistent "Contact" button, contact form, "Learn more" buttons | **No** — CTAs (excluded by the brief) |
| Cookiebot, Tailwind, search, language toggle | **No** |

Nothing from the reference — colours, text, imagery, graphic device — is copied.

## The GWMS system

**Character:** quiet, exact, institutional. Dark photography and navy for gravity; white space and hairline rules for clarity. No promotional language in the design.

**Colour** (sampled from your swatches and logo)
| Token | Value | Use |
|---|---|---|
| `--gw-navy` | `#1A3D6C` | Headings, labels |
| `--gw-blue` | `#065AA7` | Links, focus, current state (6.9:1 on white) |
| `--gw-grey` | `#BCBDBF` | Decoration only (offset square, rules) — never text |
| `--navy-900` | `#0F2742` | Footer |
| `--ink` / `--text` / `--muted` | `#14202E` / `#28343F` / `#55616D` | Text (muted = 6.3:1) |
| `--mist` / `--rule` | `#F2F5F8` / `#D6DCE3` | Panels, hairlines |

**Type** — both OFL-licensed, self-hosted as variable WOFF2 (150 KB total), no external requests
- **Source Serif 4** (optical-size axis): headings, panel titles, home statement — an editorial serif that echoes the serif headings used on the current site.
- **Source Sans 3**: body, navigation, labels. Humanist, close in spirit to the logo's wordmark.
- Body 18 px / 1.6, reading measure ≈ 68 characters (40 rem). Nav and labels: 13 px, semibold, +0.1em tracking, uppercase — echoing the spaced capitals in "MANAGEMENT SOLUTIONS".

**Brand device:** the logo's offset square (blue tile + grey shadow) used at small size as group markers, the hero accent, and the footer mark. It appears nowhere as decoration beyond that.

**Layout:** 76 rem container; 4 px spacing scale; fund pages use a 16.5 rem side navigation + 40 rem reading column; footnotes sit directly beneath the text they qualify, separated by a rule, with two-way anchors (`[1]` ↔ footnote) and a highlighted target.

**Imagery:** your dark walkway photo (hero, 800/1280/1920 px WebP, 30–153 KB) and the pale rotunda (veiled to 34% as a texture behind the home statement). Logos, portraits and the PDF are used unaltered.

## Representative layouts (actual GWMS content)

Open `preview/` via the instructions in `README.md`, or see `preview/screenshots/`:

| Screenshot | Shows |
|---|---|
| `home-desktop-full.png`, `home-mobile-full.png`, `home-tablet.png` | Home |
| `megamenu-funds-desktop.png`, `megamenu-about-desktop.png` | Open mega menus, desktop |
| `megamenu-funds-mobile.png`, `menu-mobile-closed-sections.png` | Open mobile menu |
| `fund-desktop-full.png`, `fund-mobile-full.png` | Fund page (ASK) with nested list, external link and footnote |
| `home-no-js.png` | No-JavaScript fallback |

## Honest limits of this preview
- The home page has only 24 words of content, so it is deliberately sparse; I have not padded it.
- The logo is the supplied PNG. A vector master would give a crisper header; I have not redrawn it.
- Panel links to pages not yet built (everything except Home and the ASK page) are live-site paths and will 404 in the preview server.
