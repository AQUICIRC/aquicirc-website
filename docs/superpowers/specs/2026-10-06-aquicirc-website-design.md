# AQUICIRC website — design spec

Date: 2026-10-06 · Status: draft for review · Owner: Mateusz Zawadzki

## 1. Purpose and success

The public website of AQUICIRC (Water4All, Jan 2026 – Dec 2028), deliverable D6.3. It must:

- explain in under a minute what the project does and why — managed aquifer recharge (MAR)
  with unconventional water, and the contaminants of emerging concern (CECs) that come with it;
- show **where** the work happens — six case-study sites from the Netherlands to South Africa;
- let operators, regulators, scientists and funders find outputs (publications,
  deliverables, data) without hunting;
- be maintainable for three years by the site owner plus partners sending GitHub pull
  requests, and be ready for Decap CMS and more languages later without restructuring.

Audience, in order: MAR operators and water managers, regulators and policymakers,
researchers, funders; the interested public second.

Success = all six pages below are live on https://aquicirc.eu with real proposal-derived
content, a partner can add a news post or update a site page by editing one Markdown or YAML
file, and the build has zero warnings.

## 2. Scope

**In:** English-only launch; pages Home, About, Case studies (index + 6 site pages),
Consortium, News, Outputs, 404; visual identity; the custom bricks in §6; deploy on push.

**Out (later, each its own spec):** other languages (EN, NL, FR, IT, ES, AR promised — Arabic
needs RTL), Decap CMS, the results dashboard, the serious game, contact form, site search,
newsletter. The data model in §5 is shaped so none of these forces a restructure.

## 3. Constraints and foundations (already in place)

- Hugo 0.167.0 + Hugobricks v2 engine, vendored; GitHub Pages via Actions; `aquicirc.eu`
  with HTTPS. Root-relative asset paths → the site must be served at a domain root.
- Hugobricks v2 page model: a page is Markdown split on `---`; each section is routed to a
  brick (`layouts/_partials/sections/<name>.html`) by the rules in `hugo.yaml`
  `params.sections`, or forced with a named divider `---.<name>`. A named divider that opens
  an empty section includes `content/en/bricks/<name>.md`. Brick CSS lives in
  `static/css/sections/<name>.css` and is bundled automatically.
- **Content rule (Decap-readiness):** anything partners edit — news, site pages, people,
  partners, publications, deliverables, datasets — is front matter, YAML data or plain
  Markdown with **no shortcodes and no `---` dividers in the body**. Shortcodes and named
  dividers appear only in the owner-edited structural pages (Home, About, Case studies index,
  Consortium, Outputs).
- Vendored files are edited only where noted in §8, and every such edit is listed in
  `CLAUDE.md` so a future upstream merge knows what diverged.

## 4. Sitemap and page composition

Menu: **About · Case studies · Consortium · News · Outputs** (logo links Home).

| Page | File | Composition (top → bottom) |
|---|---|---|
| Home | `content/en/_index.md` | `hero` (navy, headline, two-line description, buttons *See the six sites* / *About the project*, strata band bottom edge) · `features` (three objectives) · `transect` (signature) · latest 3 news (`blog` limited) · partner logo strip · funding statement (footer) |
| About | `content/en/about.md` | intro (the problem: MAR + CECs) · aim and three objectives · `workpackages` flow diagram · `timeline` · advisory board (`team`, group = advisory) |
| Case studies | `content/en/sites/_index.md` | intro · `transect` · `sitecompare` table (proposal Table 1) |
| Site page ×6 | `content/en/sites/<slug>.md` | custom layout (§6.4): title + country, key-facts box, body prose, click-to-load locator map, related news, previous/next site (north → south) |
| Consortium | `content/en/consortium.md` | intro · `partners` (grouped by country, coordinator first) · team (`team`, group = team) · advisory board |
| News | `content/en/posts/_index.md` + `content/en/posts/*.md` | `blog` grid with the existing tag filter; posts render with the v2 `post` brick |
| Outputs | `content/en/outputs.md` | intro · `tabs`: Publications · Deliverables · Data & models · Media |
| 404 | `content/en/404.md` | existing `error404` brick |

Posts keep v2's `posts` section; `permalinks` in `hugo.yaml` publish the section at `/news/`
and each post at `/news/:slug/`, so there is one list page and no stray `/posts/`.

### The six sites

Following the proposal's Table 1 (Atlantis and Cape Flats share one page; the proposal text
counts seven locations in places — the site pages follow the table). Ordered north → south:

| Slug | Site | Country | ≈ lat, lon (to confirm with partners) | MAR system |
|---|---|---|---|---|
| `lieshout` | Swinkels Family Brewery, Lieshout | NL | 51.52, 5.60 | subsurface irrigation, treated industrial wastewater |
| `kinrooi` | GROW pilot, Kinrooi | BE | 51.15, 5.74 | subsurface irrigation, treated domestic wastewater |
| `besos` | Besòs river basin | ES | 41.44, 2.19 | direct injection |
| `llobregat` | Llobregat river basin | ES | 41.38, 2.02 | infiltration basins |
| `wadi-khairat` | Wadi Khairat, Sousse | TN | 36.13, 10.38 | check dams, recharge basins, injection wells |
| `cape-town` | Atlantis & Cape Flats | ZA | −33.57, 18.49 / −34.03, 18.55 | infiltration (Atlantis), planned injection (Cape Flats) |

## 5. Data model

All partner-editable. Language-specific files live under `data/en/` (v2 resolves
`data/<lang>/` per language); language-independent facts under `data/`.

**`content/en/sites/<slug>.md`** front matter:
```yaml
title: Wadi Khairat
country: Tunisia
location: Sousse governorate
coordinates: [36.13, 10.38]          # [[lat, lon], …] allowed for multi-location sites
climate: Semi-arid, episodic floods
aquifer: Shallow fractured and alluvial system
mar_system: Check dams, recharge basins, injection wells
source_water: Hill-dam releases
expected_cecs: [Pesticides, Trace metals]
partners: [inat]                      # ids from partners.yaml
image: /uploads/sites/wadi-khairat.jpg   # optional
references:
  - text: Chekirbane et al., 2022
    doi: 10.1007/s12517-022-09484-7
```
Body: plain Markdown prose. Ordering everywhere is by latitude, computed — no `weight`.
For a multi-location site the first coordinate places it on the transect (one entry,
"Atlantis & Cape Flats"); the locator map shows all of them.

**`content/en/posts/<slug>.md`**: `title`, `date`, `image` (optional), `tags`, `sites`
(list of site slugs), `wps` (list, e.g. `[WP3]`). Plain Markdown body.

**`data/en/partners.yaml`**: `id`, `name`, `short`, `country`, `city`, `url`, `logo`,
`role` (`coordinator` | `wp-lead` | `partner`), `wps` (led). Seeded from the proposal:
WU (coordinator, WP1), SU + UWC (WP2), IoT + VUB (WP3), UNIPD (WP4), UPC (WP5), INAT
(WP6), CSIR, Umvoto.

**`data/en/people.yaml`**: v2 `team` fields (`name`, `function`, `image`, `description`,
`email`, `linkedin`, `website`) plus `affiliation` (partner id) and `group`
(`team` | `advisory`). The v2 `team` shortcode gets a `group` filter (§8).

**`data/en/workpackages.yaml`**: `id`, `title`, `leads` (partner ids), `summary`,
`tasks: [{id, title, start: Y1Q1, end: Y2Q2}]`. Seeded from proposal §h.

**`data/en/deliverables.yaml`**: `id`, `title`, `wp`, `due` (`Y1Q2`), `status`
(`planned` | `submitted` | `public`), `url` (when public). Seeded with D1.1 – D6.3.

**`data/en/publications.yaml`**: `authors`, `year`, `title`, `venue`, `doi`, `type`
(`article` | `preprint` | `conference` | `report`). Starts empty.

**`data/en/datasets.yaml`**: `title`, `description`, `url`, `kind` (`data` | `model` |
`code`), `wps`, `sites`. Starts empty.

**`data/project.yaml`** (language-independent): `start: 2026-01-01`, `months: 36`.

**`data/en/footer.yaml`** (v2's own file, extended): `footer_text` = funding statement,
`socials` (LinkedIn, Bluesky), new `funders` list (`name`, `logo`, `url`).
**`data/en/general.yaml`**: `contact.email`.

Empty lists render an explicit empty state ("No publications yet — the first are expected
in 2027."), never a blank section.

## 6. Custom bricks and layouts

Each is `layouts/_partials/sections/<name>.html` + `static/css/sections/<name>.css`, placed
with a named divider (`---.transect`) whose optional include file
`content/en/bricks/<name>.md` holds the section's heading and intro text. Data-driven bricks
read pages/data, not the section content.

### 6.1 `transect` — the signature element
A vertical meridian from 52°N to 35°S. Each site sits at a vertical position from its
latitude; the Sahara/equator span is compressed into a marked break ("≈ 7,000 km"), so the
northern cluster and the Cape do not leave a dead middle. Each site shows name, country and
climate band; the line is labelled with latitude ticks.

- **Markup first:** an ordered list of links (north → south) — readable and navigable with
  no CSS/JS. CSS places each item with a `--y` custom property computed in the template.
- **One orchestrated motion, the only automatic animation on the site:** on first scroll into
  view the line draws north → south and sites appear in that order (IntersectionObserver
  adds a class; CSS does the animation). `prefers-reduced-motion`: everything static.
- Hover/focus on a site reveals its key facts (MAR system, source water) in place; the
  link opens the site page.
- Narrow screens: stays vertical; the intro text stacks above.

### 6.2 `workpackages`
The six WPs as a flow: WP2 → WP3 → WP4 → WP5 in sequence, with WP1 (management) and WP6
(knowledge transfer) drawn as bands spanning the sequence. Numbering is used because the
content really is a sequence. Each WP is a native `<details>`: summary shows number, title,
lead; open shows tasks and the WP's deliverables (joined from `deliverables.yaml`).

### 6.3 `timeline`
A CSS-grid Gantt of 36 months / 12 quarters with one row per WP (bars from task spans) and
deliverable ticks. A "today" marker is placed by a few lines of JS from the current date,
so it stays right between builds; without JS it is absent rather than wrong.

### 6.4 Site page layout — `layouts/sites/page.html`
Renders the page whole (like v2 posts, bypassing `section_map`): header with title and
country; key-facts box in sediment tint (climate, aquifer, MAR system, source water,
expected CECs, partners linked to Consortium); body prose; locator map; "News from this
site" (posts whose `sites` contains this slug, newest 3; empty state otherwise); references
with DOI links; previous/next site in north → south order.

**Locator map:** a button "Show map" loads Leaflet (cdnjs) and OpenStreetMap tiles only on
click, then shows the site's marker(s). No third-party request on page load (privacy: no
visitor IP sent to OSM without an action). Without JS: a plain link to the location on
openstreetmap.org.

### 6.5 Smaller data bricks and shortcodes
- `sitecompare` — Table 1 as a real `<table>` built from site front matter; on narrow
  screens each row becomes a stacked card.
- `partners` — partners grouped by country, coordinator first, logo + name + role; links out.
- Shortcodes for Outputs tabs: `publications`, `deliverables` (status shown as text with a
  restrained colour, not a badge soup), `datasets`.
- Partner logo strip on Home: static, greyscale-to-colour only on hover/focus.

## 7. Visual identity

Plan (frontend-design pass; reviewed against generic defaults — see §7.4).

### 7.1 Colour — from the logo
| Token | Hex | Use |
|---|---|---|
| `--aquifer` | `#0F2A3F` | text, hero and footer backgrounds |
| `--flow` | `#2471A1` | links, buttons, focus ring (≥ 4.5:1 on white) |
| `--recharge` | `#32B8D9` | water lines, transect, graphics — never text on white |
| `--porewater` | `#EAF4F7` | tinted section bands |
| `--sediment` | `#C9B38A` | strata band, key-facts box, sparingly |
| `--page` | `#FFFFFF` | base |

Mapped onto v2's tokens in `variables.css` (`--accent` = flow, `--textDark` = aquifer, …).

### 7.2 Type
- **Archivo** (variable, width axis) for headings, menu and buttons — set semi-expanded to
  echo the wide, tracked wordmark in the logo. **Source Serif 4** (variable) for body: long
  reading for a scientific audience; line-height 1.6, measure ≤ 68ch.
- Self-hosted woff2, latin + latin-ext (covers NL/FR/ES/IT). Arabic later: IBM Plex Sans
  Arabic. Scale: 1.25 ratio from 1.0625rem body.
- Sentence case everywhere; no all-caps labels, no eyebrow labels over headings, no "→"
  appended to buttons; buttons say exactly what they do.

### 7.3 Motifs, layout, motion
- **Strata band:** a thin horizontal band — land surface, unsaturated zone, water table
  (recharge cyan line), aquifer — as the hero's lower edge and, at most twice per page, as
  a section divider. Inline SVG, decorative (`aria-hidden`).
- Left-aligned content; v2 measures kept (`--measure-medium` for prose).
- Motion: v2's per-section fade-ins **off** (`intersectionobserver: false`); the transect
  draw is the one automatic motion. User-triggered motion (details opening, map loading,
  tab switching) is short and shows what changed.
- Quality floor: responsive to 360 px, visible keyboard focus, reduced motion respected,
  WCAG AA contrast.

### 7.4 Review against generic defaults
- Navy + cyan is common for "water" sites; what makes this one specific is the
  latitude transect, the strata motif and the sediment colour — all from the project's own
  subject (aquifers, a north–south consortium). Kept.
- Rejected: a stat strip ("6 sites · 6 countries · 36 months") in the hero — the
  default treatment; the transect carries that information with meaning.
- Rejected: numbered markers on the objectives (not a sequence); kept on WPs (a sequence).
- Rejected: uniform rounded cards with drop shadows everywhere; cards only where the
  content is a set of peers (news teasers, partners).

## 8. Changes to vendored Hugobricks files
- `static/css/variables.css`, `static/css/fonts.css`: AQUICIRC tokens and faces.
- `layouts/_partials/site/styles.html`: append `css/aquicirc.css` (global motifs).
- `layouts/_partials/site/footer.html`: render the new `funders` logos from
  `data/en/footer.yaml` next to the funding statement.
- `layouts/_shortcodes/team.html`: optional `group` filter.
- `layouts/_shortcodes/blog.html`: optional `limit` (Home shows 3).
- `hugo.yaml`: routing rules for new bricks only if a named divider is not enough;
  `permalinks` for posts; `sites` section.
- New bluesky icon in `static/img/`.
Unused v2 webshop/checkout/payment templates stay (harmless, disabled) to keep the upstream
diff small.

## 9. Content to collect (owner)
Placeholders are allowed at build time; each is marked `TODO(content)` in the file so it can
be grepped before launch.
- Funders and logos for the acknowledgement (Water4All + EU emblem; national agencies).
- Project contact email; LinkedIn and Bluesky URLs.
- Partner logos; team list with consent for names/photos; advisory board consent
  (R. Murray, S. Garré).
- One photo per site (optional); confirmed coordinates.

## 10. Verification
- `pixi run build` completes with **zero warnings** (v2 warns on unrouted sections and
  missing includes — these are content errors). CI fails the deploy on warnings
  (`--panicOnWarning`).
- Templates fail loudly (`errorf`) on a site page missing a required field
  (`country`, `coordinates`, `mar_system`).
- Before each phase is called done: Playwright screenshots of every page at 375 px and
  1280 px, keyboard-only pass through menu, transect, WP details, tabs and map button;
  reduced-motion check.
- `grep -r "TODO(content)"` is empty before announcing the site.
