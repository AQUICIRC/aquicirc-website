# AQUICIRC website — project facts

Public project website for AQUICIRC (Water4All, 2026–2028; deliverable D6.3, task 6.3 in
the proposal). Ordinary software — the analysis-repo rules in `~/code/CLAUDE.md` do not
apply.

## Stack and hosting
- Hugo **0.167.0**, pinned in two places that must agree: `pixi.toml` and
  `HUGO_VERSION` in `.github/workflows/pages.yml`.
- Starter: **Hugobricks v2** (MIT), vendored (not a submodule) from
  `jhvanderschee/hugobricks_v2` @ `0f7ae0a`. Only the engine was copied (layouts, i18n,
  static/css|fonts|img|js, config); demo content and the 93 MB of demo uploads were not.
  Changes vs upstream: Usecue CMS `home.json` output and its iframe-monitor script removed.
- Repo `AQUICIRC/aquicirc-website` is **public** (decided deliberately: static site, no
  secrets; open-science fit). GitHub Pages via Actions. Custom domain from GoDaddy.
- Custom domain **aquicirc.eu** (apex primary; www CNAME → aquicirc.github.io), verified for the org.
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
