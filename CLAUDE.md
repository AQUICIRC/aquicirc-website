# AQUICIRC website — project facts

Public project website for AQUICIRC (Water4All, 2026–2028; deliverable D6.3, task 6.3 in
the proposal). Ordinary software — the analysis-repo rules in `~/code/CLAUDE.md` do not
apply.

## Stack and hosting
- Hugo **0.167.0**, pinned only in pixi.toml / pixi.lock; CI installs it through prefix-dev/setup-pixi.
- Starter: **Hugobricks v2** (MIT), vendored (not a submodule) from
  `jhvanderschee/hugobricks_v2` @ `0f7ae0a`. Only the engine was copied (layouts, i18n,
  static/css|fonts|img|js, config); demo content and the 93 MB of demo uploads were not.
  Changes vs upstream: Usecue CMS `home.json` output and its iframe-monitor script removed.
- Repo `AQUICIRC/aquicirc-website` is **public** (decided deliberately: static site, no
  secrets; open-science fit). GitHub Pages via Actions. Custom domain from GoDaddy.
- Custom domain **aquicirc.eu** (apex primary; www CNAME → aquicirc.github.io), verified for
  the org. Templates use root-relative paths (`/css/…`), so the site only renders at a
  domain root — never serve it from a subpath.
- Not derived from the Project GROW website repo; GROW was only a reference for page types.

## Decisions taken
- English-only launch; structure ready for more languages (proposal promises EN, NL, FR,
  IT, ES, AR — Arabic needs RTL work).
- Maintainers: the site owner plus partners via GitHub PRs. **Decap CMS may be added
  later** → keep partner-edited content (news, case sites, people, publications,
  deliverables) as front matter / YAML data / plain Markdown, no shortcodes.
- Agreed sitemap: Home · About · Case studies (one page per site) · Consortium · News ·
  Outputs; funding acknowledgement in the footer. Dashboard and serious game not in nav
  until they exist.
- Proposed visual direction (not yet built): logo-derived palette (navy #0F2A3F, flow
  blue #2471A1, cyan #32B8D9, pore-water #EAF4F7, sediment #C9B38A), Archivo headings +
  Source Serif 4 body, signature north–south site transect, strata-band motif.

## Never commit
`.env*`, `aquicirc gmail com Za.txt` (account credentials), the grant proposal PDF and
other root-level PDFs — all gitignored.

## Browser support policy
Baseline Widely available features are used freely. Newer features only as feature-detected
progressive enhancement that degrades to a complete page. No polyfills; if a newer feature
would be required for core functionality, redesign instead.

## Testing
`pixi run test` builds the site and checks the HTML (runs in CI before deploy).
`pixi run test-browser` runs the Playwright behaviour tests locally
(`pixi run install-browsers` once).

## Changes vs upstream Hugobricks v2
- `hugo.yaml`: Usecue `json` home output removed. `layouts/home.json` deleted.
- `layouts/baseof.html`: Usecue iframe-monitor script removed.
- `static/css/variables.css`: AQUICIRC colour/type tokens; v2 names mapped onto them; colour themes removed. v2's spacing token `--flow` renamed `--flow-space` (3 uses in `style.css`) because `--flow` is the AQUICIRC flow-blue colour.
- `static/css/fonts.css`, `static/fonts/`: Archivo + Source Serif 4 (OFL, `OFL-*.txt`) replace Signika + Heebo.
- `static/css/style.css`: `[hidden]` rule excludes `hidden="until-found"`; `var(--flow)` → `var(--flow-space)`.
- `layouts/_partials/site/styles.html`: bundles `css/aquicirc.css`.
- `layouts/baseof.html`: Archivo preload, `<link rel="expect" href="#main" blocking="render">`.
- `data/settings.yaml`: `intersectionobserver: false`.
- `layouts/_partials/site/footer.html`: contact email, funding statement wrapper + `funders` logo list from `data/en/footer.yaml`.
- `static/css/sections/features.css`: feature cards left-aligned (was centred).
- `static/js/site.js`: Escape dismissal for `[data-reveal]` hosts.
- `static/css/sections/intro.css`: page openers left-aligned on the wide column (was centred, small).
- `layouts/_shortcodes/team.html`: optional `group` filter and empty state.
- `static/css/sections/small.css`, `static/css/sections/team.css`: left-aligned (were centred).
- `layouts/_shortcodes/blog.html`: `limit` parameter (no filter, no paging) and empty state.
- `layouts/_partials/sections/post.html`: tag links to `/news/`, featured image uses `image_alt`, build fails without it.
- `static/css/sections/post.css`: post header left-aligned (was centred).
- `hugo.yaml`: posts published under `/news/`.
- Post front matter uses `case_sites` (not `sites`, which Hugo reserves).
- `static/js/site.js`: timeline "today" marker.
- `static/js/site.js`: inactive tab panels use `hidden="until-found"`; `beforematch` selects the tab.
- `static/css/sections/wide.css`: page h1 left-aligned (was centred).
