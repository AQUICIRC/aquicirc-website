# AQUICIRC website — design spec

Date: 2026-10-06 · Revision 3 · Status: approved, revised after preview · Owner: Mateusz Zawadzki

Written with these skills applied: **frontend-design** (identity, layout, copy),
**dataviz** (transect, timeline, status), **modern-web-guidance** (each interactive pattern,
with the guide id cited), **chrome-devtools a11y-debugging** and **debug-optimize-lcp**
(verification, §11).

## Revision 3 — owner feedback after the first preview (2026-10-06)

These supersede the sections they name; everything else stands.

- **Home hero (§4):** carries the former About opener ("Recharging aquifers with water we
  used to waste" + two paragraphs). Buttons *See the six sites* and *See outputs*, stacked on
  the right of the text (below it on phones). About opens with "About AQUICIRC" instead.
- **Sites map replaces the transect (§6.1, §7.3):** an OpenStreetMap map of all sites
  (`sitesmap` brick) on Home and Case studies, beside a plain list of site links (keyboard,
  screen-reader and no-JS route). It loads automatically after the page's `load` event once
  it nears the viewport (owner chose this over click-to-load; a note under the map says the
  tiles come from openstreetmap.org). Markers closer than 22px merge into a numbered marker;
  each popup gives the site name, a one-sentence `teaser` (new required site front-matter
  field) and a link to the site page. Markers are keyboard-focusable. The transect, its
  scroll-driven animation and the page-to-page morph are removed; the root cross-fade stays.
- **About (§6.2, §6.3):** no timeline. Work-package panels show 2–3 plain sentences each
  (`summary` in `workpackages.yaml`); no tasks, dates or deliverables there. Deliverables
  with due dates remain on Outputs.
- **Advisory board:** Consortium only.

## 1. Purpose and success

The public website of AQUICIRC (Water4All, Jan 2026 – Dec 2028), deliverable D6.3. It must:

- explain in under a minute what the project does and why: managed aquifer recharge (MAR)
  with unconventional water, and the contaminants of emerging concern (CECs) it carries;
- show **where** the work happens: six case-study sites from the Netherlands to South Africa;
- let operators, regulators, scientists and funders find outputs (publications,
  deliverables, data) without hunting;
- stay maintainable for three years by the site owner plus partners sending GitHub pull
  requests, and be ready for Decap CMS and more languages without restructuring.

Audience, in order: MAR operators and water managers, regulators and policymakers,
researchers, funders; the interested public second.

**Done means:** every page in §4 is live on https://aquicirc.eu with proposal-derived content;
a partner can add a news post or update a site page by editing one Markdown or YAML file;
the build has zero warnings; the checks in §11 pass.

## 2. Scope

**In:** English-only launch; pages Home, About, Case studies (index + 6 site pages),
Consortium, News, Outputs, 404; the visual identity; the custom bricks in §6; deploy on push.

**Out (each later gets its own spec):** other languages (the proposal promises EN, NL, FR,
IT, ES, AR; Arabic needs RTL), Decap CMS, the results dashboard, the serious game, contact
form, site search, newsletter, dark mode. The data model in §5 is shaped so none of these
forces a restructure.

## 3. Foundations and rules

### 3.1 Already in place
Hugo 0.167.0 + Hugobricks v2 engine (vendored); GitHub Pages via Actions; `aquicirc.eu` with
enforced HTTPS. Templates use root-relative asset paths, so the site is always served at a
domain root.

### 3.2 How Hugobricks v2 builds a page
A page is Markdown split on `---`. Each section is routed to a brick
(`layouts/_partials/sections/<name>.html`) by the rules in `hugo.yaml` `params.sections`,
or forced with a named divider `---.<name>`. A named divider that opens an empty section
includes `content/en/bricks/<name>.md`. Brick CSS lives in `static/css/sections/<name>.css`
and is concatenated into the single bundle automatically (no `@import` chains).

### 3.3 Content rule (Decap readiness)
Anything partners edit (news, site pages, people, partners, publications, deliverables,
datasets) is front matter, YAML data or plain Markdown, with **no shortcodes and no `---`
dividers in the body**. Shortcodes and named dividers appear only in the structural pages the
owner edits (Home, About, Case studies index, Consortium, Outputs).

### 3.4 Browser-support policy
Recorded in `CLAUDE.md` as the project policy:

> **Baseline Widely available** features are used freely. Newer features are used only as
> **feature-detected progressive enhancement** that degrades to a complete, usable page.
> **No polyfills.** If a newer feature would be required for core functionality, redesign
> instead.

Every interactive element below names its modern-web-guidance guide. The implementer
retrieves that guide before writing the element and checks the result against it.

### 3.5 Vendored files
Vendored Hugobricks files change only where §9 lists them, and every such change goes into
`CLAUDE.md` so a later upstream merge knows what diverged.

## 4. Sitemap and page composition

Menu: **About · Case studies · Consortium · News · Outputs**. The logo links Home.

| Page | File | Composition (top → bottom) |
|---|---|---|
| Home | `content/en/_index.md` | `hero` (navy; headline, two-line description, buttons *See the six sites* / *About the project*; strata band on its lower edge) · `features` (three objectives) · `transect` (signature) · latest 3 news (`blog` with a limit) · partner logo strip · footer with funding statement |
| About | `content/en/about.md` | intro (the problem: MAR + CECs) · aim and the three objectives · `workpackages` flow · `timeline` · advisory board (`team`, group = advisory) |
| Case studies | `content/en/sites/_index.md` | intro · `transect` · `sitecompare` table (proposal Table 1) |
| Site page ×6 | `content/en/sites/<slug>.md` | own layout (§6.4) |
| Consortium | `content/en/consortium.md` | intro · `partners` (grouped by country, coordinator first) · team (`team`, group = team) · advisory board |
| News | `content/en/posts/_index.md`, `content/en/posts/*.md` | `blog` grid with v2's tag filter; posts render with v2's `post` brick |
| Outputs | `content/en/outputs.md` | intro · `tabs`: Publications · Deliverables · Data & models · Media |
| 404 | `content/en/404.md` | v2 `error404` brick |

In `hugo.yaml`, `permalinks` publish the posts section at `/news/` and each post at
`/news/:slug/`, so there is one list page and no stray `/posts/`.

Each page has one `<h1>` and headings that never skip a level. v2's landmarks (`header`,
`nav`, `main`, `footer`) and skip link are kept.

### 4.1 The six sites
The site pages follow the proposal's Table 1, where Atlantis and Cape Flats share one row.
(The proposal text counts seven locations in places.) Ordered north → south:

| Slug | Site | Country | ≈ lat, lon (to confirm with partners) | MAR system |
|---|---|---|---|---|
| `lieshout` | Swinkels Family Brewery, Lieshout | NL | 51.52, 5.60 | subsurface irrigation, treated industrial wastewater |
| `kinrooi` | GROW pilot, Kinrooi | BE | 51.15, 5.74 | subsurface irrigation, treated domestic wastewater |
| `besos` | Besòs river basin | ES | 41.44, 2.19 | direct injection |
| `llobregat` | Llobregat river basin | ES | 41.38, 2.02 | infiltration basins |
| `wadi-khairat` | Wadi Khairat, Sousse | TN | 36.13, 10.38 | check dams, recharge basins, injection wells |
| `cape-town` | Atlantis & Cape Flats | ZA | −33.57, 18.49 / −34.03, 18.55 | infiltration (Atlantis), planned injection (Cape Flats) |

## 5. Data model

Everything here is partner-editable. Language-specific files live under `data/en/` (v2
resolves `data/<lang>/` per language); language-independent facts live under `data/`.

**`content/en/sites/<slug>.md`**, front matter:
```yaml
title: Wadi Khairat
country: Tunisia
location: Sousse governorate
coordinates: [[36.13, 10.38]]        # one or more [lat, lon]
climate: Semi-arid, episodic floods
aquifer: Shallow fractured and alluvial system
mar_system: Check dams, recharge basins, injection wells
source_water: Hill-dam releases
expected_cecs: [Pesticides, Trace metals]
partners: [inat]                      # ids from partners.yaml
image: /uploads/sites/wadi-khairat.jpg   # optional
image_alt: Check dam on the Wadi Khairat after a flood release   # required with image
references:
  - text: Chekirbane et al., 2022
    doi: 10.1007/s12517-022-09484-7
```
- **Body:** plain Markdown prose.
- **Order:** by latitude, computed, never a `weight`.
- **Multi-location sites:** the first coordinate places the site on the transect (one entry,
  "Atlantis & Cape Flats"); the locator map shows all of them.

**`content/en/posts/<slug>.md`:** `title`, `date`, `image` + `image_alt` (optional), `tags`,
`case_sites` (site slugs; `sites` is reserved by Hugo ≥ 0.153), `wps` (e.g. `[WP3]`). Plain Markdown body.

**`data/en/partners.yaml`:** `id`, `name`, `short`, `country`, `city`, `url`, `logo`, `role`
(`coordinator` | `wp-lead` | `partner`), `wps` (the WPs it leads). Seeded from the proposal:
WU (coordinator, WP1), SU + UWC (WP2), IoT + VUB (WP3), UNIPD (WP4), UPC (WP5), INAT (WP6),
CSIR, Umvoto.

**`data/en/people.yaml`:** v2's `team` fields (`name`, `function`, `image`, `description`,
`email`, `linkedin`, `website`) plus `affiliation` (a partner id) and `group` (`team` |
`advisory`).

**`data/en/workpackages.yaml`:** `id`, `title`, `leads` (partner ids), `summary`,
`tasks: [{id, title, start: Y1Q1, end: Y2Q2}]`. Seeded from proposal §h.

**`data/en/deliverables.yaml`:** `id`, `title`, `wp`, `due` (`Y1Q2`), `status` (`planned` |
`submitted` | `public`), `url` (once public). Seeded with D1.1 – D6.3.

**`data/en/publications.yaml`:** `authors`, `year`, `title`, `venue`, `doi`, `type`
(`article` | `preprint` | `conference` | `report`). Starts empty.

**`data/en/datasets.yaml`:** `title`, `description`, `url`, `kind` (`data` | `model` |
`code`), `wps`, `sites`. Starts empty.

**`data/project.yaml`:** `start: 2026-01-01`, `months: 36`.

**`data/en/footer.yaml`** (v2's own file, extended): `footer_text` = the funding statement;
`socials` (LinkedIn, Bluesky); a new `funders` list (`name`, `logo`, `url`).
**`data/en/general.yaml`:** `contact.email`.

**Empty lists** render an explicit empty state that says what will appear and when
("No publications yet. The first are expected in 2027."), never a blank section.

## 6. Custom bricks and layouts

Each brick is `layouts/_partials/sections/<name>.html` + `static/css/sections/<name>.css`,
placed with a named divider (`---.transect`). Its optional include
`content/en/bricks/<name>.md` holds the section's heading and intro. Data-driven bricks read
pages and data, not the section content.

### 6.1 `transect`, the signature element
A vertical meridian from 52°N to 35°S. Each site sits at a height set by its latitude. The
span over the Sahara and the equator is compressed into a marked break ("≈ 7,000 km"), so
the northern cluster and the Cape don't leave a dead middle. Each site shows its name,
country and climate band, and the line carries latitude ticks.

- **Markup first.** An ordered list of links, north → south, that reads and works with no
  CSS or JS. CSS places each item with a `--y` custom property the template computes.
- **Marks (dataviz).**
  - The meridian is a 2px line in `--flow`.
  - Each site is a filled dot ≥ 8px (r ≥ 4) in `--flow` with a 2px surface ring.
  - `--flow` clears 3:1 on white and on pore-water. Cyan fails at 2.1–2.3:1 and is never a
    data mark.
  - Latitude ticks are solid 1px hairlines in `--borderMedium`.
  - Labels use text tokens, never the mark colour.
  - One series, so no legend: the section heading names what is plotted.
- **One orchestrated motion, the only automatic animation on the site** (guide
  `scrollytelling`).
  - As the section scrolls into view, the line draws north → south and the sites appear in
    that order.
  - Built as a native CSS scroll-driven animation (`animation-timeline: view()`), gated by
    `@supports ((animation-timeline: scroll()) and (animation-range: 0% 100%))`.
  - It is decorative, so there is **no JS fallback**: Firefox shows the finished transect.
  - Under `prefers-reduced-motion: reduce` it is static.
- **Details on hover or focus.**
  - Hovering or focusing a site reveals its key facts (MAR system, source water) **in place,
    inside the item's own box**, with plain CSS (`:hover`, `:focus-within`).
  - Not a popover: `popover="hint"` + `interestfor` (guide `interest-triggered-tooltips`) is
    Chrome/Edge-only and would need two polyfills, which §3.4 rules out. Revisit when it
    reaches Baseline.
  - WCAG 1.4.13: the reveal stays open while the pointer is over it (it is part of the
    hovered box), persists, and closes with Escape (a few lines of JS).
  - Each hit target is ≥ 24px tall and covers dot plus label. Keyboard focus shows exactly
    what hover shows.
  - The same facts are always reachable without hover, on the site page and in the
    `sitecompare` table, which is the transect's table view.
- **Forced colours.** Marks fall back to `CanvasText`/`LinkText` through SVG `currentColor`.
  No state or separation relies on `background-image` or `box-shadow`.
- **Narrow screens.** The transect stays vertical and the intro text stacks above it.

### 6.2 `workpackages`
- **Layout.** The six WPs as a flow: WP2 → WP3 → WP4 → WP5 in sequence, with WP1
  (management) and WP6 (knowledge transfer) drawn as bands across it. Numbers are used
  because the content really is a sequence.
- **Each WP is a native `<details>`** (guide `search-hidden-content`).
  - No `name` grouping, so readers can open two WPs to compare.
  - Content inside stays findable with Ctrl+F.
  - The summary shows the WP's number, title and lead. Opened, it shows the tasks and the
    WP's deliverables (joined from `deliverables.yaml`).
- **Opening animates its height** (guide `animate-element-entry-exit`; `details::details-content`
  per guide `html`): `transition-behavior: allow-discrete` as its own declaration,
  `interpolate-size: allow-keywords` under `@supports`. Elsewhere it opens instantly. No
  animation under reduced motion.

### 6.3 `timeline`
A CSS-grid Gantt of 36 months (12 quarters): one row per WP, bars from the task spans, and
deliverable markers.

- **Marks (dataviz).**
  - One series, so every bar is `--flow`, ≤ 24px thick, with 4px rounded ends and a 2px
    surface gap between a WP's adjacent task bars.
  - WP identity comes from the row label, in text tokens.
  - Deliverables are a different shape (≥ 8px diamond in `--aquifer` with a 2px surface
    ring), so shape rather than hue separates them from tasks.
  - Gridlines are solid 1px hairlines; years are labelled and quarters ticked.
- **"Today"** is a 1px `--aquifer` rule with a text label. A few lines of JS place it from
  the current date, so it stays right between builds. Without JS it is absent rather than
  wrong.
- **Tooltips.** Each bar and diamond is focusable and shows the task or deliverable, its id
  and its start–end or due quarter on hover and focus. They use the same in-place CSS
  technique and Escape dismissal as §6.1, and text is set with `textContent`. They never
  gate anything: the WP `<details>` and the Outputs deliverables table are the table view.
- **Small screens.** The grid scrolls horizontally inside its own frame, with the WP labels
  pinned (sticky). The scroll frame is a labelled, focusable region (`role="region"`,
  `aria-labelledby`, `tabindex="0"`) so keyboard users can scroll it. The container grows
  with its content, axis band included.

### 6.4 Site page layout, `layouts/sites/page.html`
It renders the page whole, like v2 posts, and bypasses `section_map`. Top to bottom:

- **Header:** title and country.
- **Key facts box** in the sediment tint, as a `<dl>`: climate, aquifer, MAR system, source
  water, expected CECs, and partners linked to Consortium.
- **Body prose.**
- **Locator map** (below).
- **News from this site:** posts whose `case_sites` contains this slug, newest 3, or an empty
  state.
- **References** with DOI links.
- **Previous / next site,** north → south.

**Locator map.**
- A `<button>` labelled "Show map" loads **Leaflet, self-hosted in `static/vendor/leaflet/`**
  (guide `performance`: self-host third-party code, no extra origin), then OpenStreetMap
  tiles, and shows the site's markers.
- Nothing goes to a third party until the visitor clicks. After the click, the only
  third-party request is the tiles, with OSM attribution shown.
- The map frame reserves its height before loading, so nothing shifts (CLS).
- Without JS there is a plain link to the location on openstreetmap.org.

**Page-to-page morph** (guides `cross-document-transitions`,
`consistent-cross-document-transitions`).
- Each transect label and the matching site page `<h1>` share
  `view-transition-name: site-<slug>`, so the name glides into place when you open a site.
  The rest of the page cross-fades.
- `@view-transition { navigation: auto; }` is inside
  `@media (prefers-reduced-motion: no-preference)` in the global stylesheet.
- Pages carry `<link rel="expect" href="#main" blocking="render">` so the transition never
  animates to a half-parsed page.
- Progressive enhancement: Chrome, Edge and Safari 18.2+ animate; Firefox navigates
  instantly.

### 6.5 Tables, tabs and smaller bricks
- **`sitecompare`** (guide `responsive-table`).
  - Proposal Table 1 as a real `<table>` built from site front matter, with `<caption>`,
    `<thead>` and `<th scope>`.
  - Sticky column headers and site-name row headers.
  - A `@container` query under 600px turns rows into stacked cards with visible field
    labels, using DOM text rather than `content:` (guide `css`).
  - The same component renders the Outputs deliverables table.
- **Outputs tabs.**
  - Keep v2's accessible tabs (role="tab", roving tabindex).
  - Change inactive panels from `hidden` to `hidden="until-found"`, plus a `beforematch`
    listener that selects the matching tab (guide `search-hidden-content`), so Ctrl+F and
    deep links reach a publication in a closed tab.
  - Shortcodes: `publications`, `deliverables`, `datasets`.
- **Deliverable status** (planned / submitted / public) is state, so it is always a text
  label plus a small icon. Colour may reinforce it but never carries it alone (dataviz).
- **`partners`.** Partners grouped by country, coordinator first, each with logo, name and
  role, linking out.
- **Partner logo strip on Home.** Static: no carousel, no auto-motion.

## 7. Visual identity

### 7.1 Colour, from the logo
| Token | Hex | Use |
|---|---|---|
| `--aquifer` | `#0F2A3F` | text, hero and footer backgrounds |
| `--flow` | `#2471A1` | links, buttons, focus ring, data marks (≥ 4.5:1 on white) |
| `--recharge` | `#32B8D9` | decorative water lines (strata band), accents on the navy hero; never text, never a data mark on light surfaces (2.3:1) |
| `--porewater` | `#EAF4F7` | tinted section bands |
| `--sediment` | `#C9B38A` | strata band, key-facts box, sparingly |
| `--page` | `#FFFFFF` | base |

- These map onto v2's tokens in `variables.css` (`--accent` = flow, `--textDark` = aquifer,
  …).
- Checked with the dataviz validator: flow vs recharge ΔE 20 under normal and CVD vision.
  On the navy hero only one cyan may carry meaning (the logo's lighter cyan is ΔE 7.6 from
  it).
- Text on tinted bands is re-checked for ≥ 4.5:1.
- The site is light-only (v2 ships no dark mode). A dark theme would get its own validated
  steps (guide `dark-mode`), not an inversion.

### 7.2 Type
- **Archivo** (variable, width axis) for headings, menu and buttons, set semi-expanded to
  echo the wide, tracked wordmark in the logo.
- **Source Serif 4** (variable) for body: long reading for a scientific audience.
  Line-height 1.6, measure ≤ 68ch.
- **Font files:** self-hosted woff2, subset to latin + latin-ext (covers NL, FR, ES, IT).
  `font-display: swap`. Arabic later: IBM Plex Sans Arabic.
- **Avoiding layout shift as fonts arrive:** `font-size-adjust: from-font` on body and
  headings (guide `visually-stable-font-fallbacks`; Baseline 2024).
- **The hero `<h1>` is text, so it is the likely LCP element.** The Archivo file it uses gets
  `<link rel="preload" as="font" crossorigin>`, and nothing else is preloaded
  (debug-optimize-lcp).
- **Scale:** `rem` steps at a 1.25 ratio from a 1.0625rem body. Display sizes use `clamp()`
  mixing `rem` and `vw`, never `vw` alone, never `px` (guide `css`).
- **Wrapping:** `text-wrap: balance` on h1–h3 only; `text-wrap: pretty` on body paragraphs
  (guide `improve-text-layout-and-legibility`).
- **Copy rules (frontend-design):** sentence case everywhere; no all-caps labels; no eyebrow
  labels over headings; no "→" appended to buttons; buttons say exactly what they do.

### 7.3 Motifs, layout, motion
- **Strata band.** A thin horizontal band: land surface, unsaturated zone, water table (a
  recharge-cyan line), aquifer. It forms the hero's lower edge and appears at most twice
  more per page as a divider. Inline SVG with `aria-hidden="true"`, hidden in forced-colours
  mode.
- **Layout.** Left-aligned content; v2's measures kept (`--measure-medium` for prose).
- **Motion budget.**
  - v2's per-section fade-ins are **off** (`intersectionobserver: false`).
  - Automatic motion: the transect draw only.
  - Motion that answers the visitor:
    - the page-to-page morph
    - `<details>` opening
    - map loading
    - tab switching
    - `scroll-behavior: smooth` for in-page links
  - Each is short (≤ 300ms), shows what changed, and is wrapped in
    `prefers-reduced-motion: no-preference`.
- **Interaction quality floor** (guides `accessibility`, `css`):
  - responsive down to 360px with no horizontal page scroll
  - a visible `:focus-visible` ring in `--flow` with 3:1 contrast
  - tap targets ≥ 24px, and ≥ 44px for primary navigation and buttons
  - zoom never disabled
  - no `user-select: none` on content

### 7.4 Checked against generic defaults
- **Kept: navy + cyan.** It's common for water sites, but here the latitude transect, the
  strata motif and the sediment colour all come from the project's own subject (aquifers, a
  north–south consortium).
- **Rejected: a stat strip in the hero** ("6 sites · 6 countries · 36 months"). It's the
  default treatment, and the transect carries that information with meaning.
- **Rejected: numbered markers on the objectives**, which aren't a sequence. They're kept on
  the WPs, which are.
- **Rejected: uniform rounded cards with drop shadows.** Cards appear only where the content
  is a set of peers (news teasers, partners).
- **Rejected: a partner logo carousel.** A static strip is calmer and nothing moves on its
  own.

## 8. Performance budget

- **No hero image.** The LCP element is the hero `<h1>` text.
- **CSS and JS.** One concatenated, minified, fingerprinted stylesheet (v2 already does
  this). JS is `defer`red. The only things in `<head>` beyond the stylesheet are the one
  font preload and `link rel="expect"`; there are no scripts there.
- **Images** go through Hugo image processing: WebP derivatives with `srcset`/`sizes`,
  explicit `width`/`height`, and `loading="lazy"` below the fold. Logos are SVG when
  partners supply SVG.
- **Leaflet** (~40 kB gzipped) loads only on click (§6.4).
- **Targets**, measured with DevTools emulating Fast 3G and 4× CPU throttling:
  - LCP ≤ 2.5 s, CLS < 0.1
  - Lighthouse Performance ≥ 95 on mobile
  - Accessibility, Best Practices and SEO = 100

## 9. Changes to vendored Hugobricks files
- `static/css/variables.css`, `static/css/fonts.css`: AQUICIRC tokens and faces.
- `layouts/_partials/site/styles.html`: append `css/aquicirc.css` (global motifs, view
  transitions, focus ring, text wrapping).
- `layouts/baseof.html`: font preload, `<link rel="expect">`.
- `layouts/_partials/site/footer.html`: render the `funders` logos next to the funding
  statement.
- `layouts/_shortcodes/team.html`: optional `group` filter.
- `layouts/_shortcodes/blog.html`: optional `limit` (Home shows 3).
- `static/js/site.js`:
  - tab panels use `hidden="until-found"` + `beforematch` (§6.5)
  - Escape closes in-place reveals (§6.1, §6.3)
  - the timeline's "today" marker (§6.3)
- `data/settings.yaml`: `intersectionobserver: false`.
- `hugo.yaml`: `permalinks` for posts; routing rules only where a named divider is not
  enough.
- New: `static/img/bluesky.svg`, `static/vendor/leaflet/`.

v2's unused webshop, checkout and payment templates stay (disabled, harmless) to keep the
upstream diff small.

## 10. Content to collect (owner)
Placeholders are allowed while building. Each is marked `TODO(content)` so they can all be
found with grep before launch.
- Funders and their logos for the acknowledgement (Water4All + the EU emblem; national
  agencies).
- Project contact email; LinkedIn and Bluesky URLs.
- Partner logos (SVG preferred); the team list with consent for names and photos; advisory
  board consent (R. Murray, S. Garré).
- One photo per site (optional, with alt text); confirmed coordinates.

## 11. Verification

Run per build phase, not only at the end.

**Build**
- `pixi run build` completes with **zero warnings**. v2 warns on unrouted sections and
  missing includes, which are content errors. CI builds with `--panicOnWarning`, so a
  warning fails the deploy.
- Templates fail loudly (`errorf`) when a site page lacks a required field (`country`,
  `coordinates`, `mar_system`) or has an `image` without `image_alt`.

**Browser checks, with Chrome DevTools MCP (a11y-debugging skill) on every page**
1. Lighthouse in navigation mode. Failing audits are pulled from the saved JSON report
   with a filter, not read whole.
2. `list_console_messages` (type `issue`) for native low-contrast, ARIA and label issues.
3. `take_snapshot`: one `<h1>`, no skipped heading levels, landmarks present, and DOM order
   matches visual order (compared against a screenshot).
4. Keyboard pass with `press_key` Tab / Shift+Tab / Escape, through the menu, transect,
   WP details, timeline, tabs and map button. Focus is always visible, there are no traps,
   and Escape closes reveals.
5. Tap target sizes and spot contrast checks with the skill's snippets.

**Performance, with DevTools (debug-optimize-lcp skill) on Home and one site page**
- A performance trace with reload under Fast 3G + 4× CPU. Check `LCPBreakdown` and
  `RenderBlocking`: resource-load and render delay each < 10% of LCP.

**Visual, with Playwright**
- Screenshots at 375, 768 and 1280px for every page, and a reduced-motion run.
- Forced-colours spot check on the transect and timeline.

**Design and data**
- The transect and timeline are checked against the dataviz anti-pattern list. Any new
  colour on a data mark goes through the palette validator first.
- Each interactive element is checked against its modern-web-guidance guide (§3.4).

**Launch gate**
- `grep -r "TODO(content)"` comes back empty.
