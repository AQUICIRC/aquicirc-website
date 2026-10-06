# AQUICIRC website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the English launch of https://aquicirc.eu: six content pages plus six site pages, the AQUICIRC visual identity, and the custom bricks (transect, work packages, timeline, tables, locator map), all on the existing Hugo + Hugobricks v2 scaffold.

**Architecture:**
- Hugobricks v2 stacks Markdown sections into bricks. New bricks are `layouts/_partials/sections/<name>.html` + `static/css/sections/<name>.css`, placed with named dividers (`---.<name>`).
- Partner-editable content is YAML data and plain-Markdown pages; structural pages carry the shortcodes.
- Tests build the site once per session and assert on the generated HTML (pytest + BeautifulSoup). A small Playwright suite covers the JS behaviours.

**Tech Stack:** Hugo 0.167.0 (extended), Hugobricks v2 (vendored), vanilla CSS/JS, Leaflet 1.9.4 (self-hosted, loaded on click), pixi (conda-forge), pytest + beautifulsoup4 + pyyaml, Playwright for Python, GitHub Actions → GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-10-06-aquicirc-website-design.md` (revision 2). Read it before starting any task; section numbers below (§) refer to it.

## Global Constraints

**Stack and process**
- Hugo version **0.167.0**, pinned **only** through `pixi.toml`/`pixi.lock`. CI uses pixi too (Task 1 removes the second pin).
- Build must pass `hugo --panicOnWarning`: **zero warnings**.
- Browser policy (§3.4): Baseline Widely available freely; newer features only as feature-detected progressive enhancement; **no polyfills**.
- Content rule (§3.3): partner-edited files (`content/en/sites/*.md`, `content/en/posts/*.md`, `data/en/*.yaml`) contain **no shortcodes and no `---` body dividers**.
- Every change to a vendored Hugobricks file is listed in `CLAUDE.md` under "Changes vs upstream".
- Every placeholder for owner-supplied content contains the literal marker `TODO(content)`.
- Before writing any interactive element, run `npx -y modern-web-guidance@latest retrieve "<guide-id>"` for the guide the task names, and check the result against it.

**Visual tokens**
- Colours exactly: `--aquifer #0F2A3F`, `--flow #2471A1`, `--recharge #32B8D9`, `--porewater #EAF4F7`, `--sediment #C9B38A`, `--page #FFFFFF`.
- `--recharge` is **never** text and **never** a data mark on a light surface.
- Data marks: 2px lines; dots/diamonds ≥ 8px with a 2px surface ring; bars ≤ 24px with 4px rounded ends; solid 1px hairline gridlines (never dashed).
- Type: **Archivo** (variable, `wdth` axis) for headings, menu and buttons; **Source Serif 4** (variable) for body. Self-hosted woff2, latin + latin-ext.
- Font sizes in `rem`/`clamp()`, never `px`; body line-height 1.6; measure ≤ 68ch.

**Copy**
- Sentence case everywhere.
- No all-caps labels and no eyebrow labels over headings.
- No "→" appended to links or buttons.
- No meta strings joined with middle dots; use commas or separate elements.
- Buttons say exactly what they do.

**Motion and interaction**
- One automatic animation: the transect draw.
- All motion ≤ 300ms and wrapped in `prefers-reduced-motion: no-preference`.
- Tap targets ≥ 24px; ≥ 44px for primary navigation and buttons.
- No request to any third-party origin until the visitor acts. The only one is OpenStreetMap tiles, after "Show map".

## Review Focus

These failure modes are implied by the spec but no feature test naturally exercises them. Each has a test in the task named.

1. **A site with more than one coordinate (Atlantis & Cape Flats):** the transect uses the first coordinate; the map shows a marker for every coordinate. Tests in Task 7 and Task 13.
2. **A 360px-wide phone:** no page scrolls horizontally, even with the longest site, partner and deliverable names. Test in Task 15.
3. **JavaScript off:** all tab panels are readable (stacked), the map degrades to an OpenStreetMap link, and the transect is complete and static. Tests in Task 12 and Task 13.
4. **A partner's typo in a post's `sites:` slug or a partner id:** the build/test run fails with a message naming the bad id, instead of the post silently not appearing. Test in Task 3.
5. **`prefers-reduced-motion: reduce`:** no transect animation and no view transition. Test in Task 7.

---

## File structure

```
pixi.toml, pixi.lock                       # + test feature (python, pytest, bs4, pyyaml, playwright)
.github/workflows/pages.yml                # pixi-based: test, then build + deploy
CLAUDE.md                                  # + browser policy, "Changes vs upstream" list
hugo.yaml                                  # + permalinks for posts
data/project.yaml                          # start, months
data/settings.yaml                         # intersectionobserver: false
data/en/{general,header,footer}.yaml       # contact, menu, funding/socials/funders
data/en/{partners,people,workpackages,deliverables,publications,datasets,features}.yaml
content/en/_index.md, about.md, consortium.md, outputs.md, 404.md
content/en/sites/_index.md, sites/<6 slugs>.md
content/en/posts/_index.md, posts/2026-10-06-website-launched.md
content/en/bricks/{transect,sitecompare,workpackages,timeline,partners}.md   # section intros
layouts/baseof.html                        # font preload, link rel=expect   (vendored, modified)
layouts/sites/page.html                    # site page layout (new)
layouts/_partials/strata.html              # decorative SVG band (new)
layouts/_partials/sites-by-latitude.html   # returns site pages sorted N→S (new)
layouts/_partials/quarter.html             # "Y1Q2" → "Q2 2026" (new)
layouts/_partials/quarter-index.html       # "Y1Q2" → 1 (0-based) (new)
layouts/_partials/sections/{hero,transect,sitecompare,workpackages,timeline,partners}.html   # new bricks
layouts/_partials/site/footer.html         # funders (vendored, modified)
layouts/_partials/sections/post.html       # news/ tag links, image_alt (vendored, modified)
layouts/_shortcodes/{team,blog,tabs}.html  # group filter, limit, (tabs unchanged markup) (vendored, modified)
layouts/_shortcodes/{publications,deliverables,datasets,partnerstrip}.html   # new
static/css/variables.css, fonts.css, style.css   # tokens, faces, [hidden] fix (vendored, modified)
static/css/aquicirc.css                    # global identity layer (new), appended in styles.html
static/css/sections/{hero,transect,sitecompare,workpackages,timeline,partners,site}.css   # new
static/fonts/{archivo,source-serif-4}-*.woff2   # new (OFL)
static/js/site.js                          # tabs until-found, reveal Escape, today marker (vendored, modified)
static/js/map.js                           # locator map loader (new)
static/vendor/leaflet/{leaflet.js,leaflet.css,LICENSE}   # new
static/img/bluesky.svg                     # new
tests/conftest.py, tests/test_*.py         # build-output tests
tests/browser/test_*.py                    # Playwright behaviour tests (marker: browser)
```

---

### Task 1: Test harness and pixi-only CI

**Files:**
- Modify: `pixi.toml`, `.github/workflows/pages.yml`, `CLAUDE.md`, `.gitignore`
- Create: `tests/conftest.py`, `tests/test_build.py`, `tests/browser/conftest.py`, `pytest.ini`

**Interfaces:**
- Produces fixtures used by every later test:
  - `site` (session, `pathlib.Path` of the built `public` dir)
  - `html(path: str) -> bs4.BeautifulSoup` (e.g. `html("/sites/kinrooi/")`)
  - `css() -> str` (the built CSS bundle text)
  - `build_variant(edit: callable) -> subprocess.CompletedProcess` (builds a temp copy of the repo after `edit(tmp_root: Path)` runs)
  - Browser tests: `served` (session, base URL string of a local static server over `site`); the `page` fixture comes from pytest-playwright.

- [ ] **Step 1: Add the test toolchain to pixi**

Replace `pixi.toml` with:

```toml
[workspace]
name = "aquicirc-website"
description = "AQUICIRC project website, built with Hugo and Hugobricks v2"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "osx-64", "win-64"]

[dependencies]
# The only Hugo pin. CI installs it through pixi too.
hugo = "==0.167.0"
python = "3.13.*"
pytest = "*"
beautifulsoup4 = "*"
pyyaml = "*"
playwright = "*"
pytest-playwright = "*"

[tasks]
dev = "hugo server --buildDrafts --buildFuture --disableFastRender"
build = "hugo --gc --minify --panicOnWarning"
clean = "rm -rf public resources .hugo_build.lock"
test = "pytest -m 'not browser'"
test-browser = "pytest -m browser"
install-browsers = "playwright install chromium"
```

Run: `pixi install && pixi run install-browsers`
Expected: environment solves; Chromium downloads.

- [ ] **Step 2: Write the fixtures**

`pytest.ini`:

```ini
[pytest]
testpaths = tests
markers =
    browser: needs Chromium via Playwright (pixi run test-browser)
```

`tests/conftest.py`:

```python
"""Build the site once per test session and expose helpers to read it."""
import shutil
import subprocess
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
# `--environment test`: not production, so the CSS bundle is unminified and readable
# by the tests (CI's production build still minifies and fingerprints it).
HUGO = ["hugo", "--panicOnWarning", "--environment", "test", "--baseURL", "https://aquicirc.eu/", "--quiet"]
COPY_IGNORE = shutil.ignore_patterns(".git", ".pixi", "public", "resources", "*.pdf", "*.txt")


def run_hugo(source: Path, destination: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [*HUGO, "--source", str(source), "--destination", str(destination)],
        capture_output=True, text=True,
    )


@pytest.fixture(scope="session")
def site(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("public")
    result = run_hugo(ROOT, out)
    assert result.returncode == 0, f"hugo failed:\n{result.stdout}\n{result.stderr}"
    return out


@pytest.fixture(scope="session")
def html(site):
    def load(path: str) -> BeautifulSoup:
        rel = path.strip("/")
        target = site / rel if rel.endswith((".html", ".xml")) else site / rel / "index.html"
        assert target.exists(), f"{path} was not built ({target})"
        return BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser")
    return load


@pytest.fixture(scope="session")
def css(site, html):
    def load() -> str:
        href = html("/").find("link", rel="stylesheet")["href"].split("?")[0]
        return (site / href.lstrip("/")).read_text(encoding="utf-8")
    return load


@pytest.fixture
def build_variant(tmp_path):
    """Copy the repo, let the test edit the copy, build it, return the result."""
    def build(edit) -> subprocess.CompletedProcess:
        src = tmp_path / "src"
        shutil.copytree(ROOT, src, ignore=COPY_IGNORE)
        edit(src)
        return run_hugo(src, tmp_path / "out")
    return build
```

`tests/browser/conftest.py`:

```python
import functools
import http.server
import threading

import pytest


@pytest.fixture(scope="session")
def served(site):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def pytest_collection_modifyitems(items):
    for item in items:
        if "/browser/" in str(item.fspath):
            item.add_marker(pytest.mark.browser)
```

- [ ] **Step 3: Write the first test**

`tests/test_build.py`:

```python
def test_home_builds_with_project_title(html):
    doc = html("/")
    assert doc.title.string.strip().endswith("AQUICIRC")


def test_page_language_is_english(html):
    assert html("/").html["lang"] == "en"
```

- [ ] **Step 4: Run tests**

Run: `pixi run test`
Expected: 2 passed.

- [ ] **Step 5: Switch CI to pixi**

Replace the `build` job steps in `.github/workflows/pages.yml` with the following. Delete the `env: HUGO_VERSION` block and the "Install Hugo" step.

```yaml
    steps:
      - name: Checkout
        uses: actions/checkout@v7
      - name: Set up pixi
        uses: prefix-dev/setup-pixi@v0.11.0
        with:
          cache: true
      - name: Configure Pages
        id: pages
        uses: actions/configure-pages@v6
      - name: Test
        run: pixi run test
      - name: Build
        env:
          HUGO_ENVIRONMENT: production
          TZ: Europe/Brussels
        run: pixi run hugo --gc --minify --panicOnWarning --baseURL "${{ steps.pages.outputs.base_url }}/"
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v5
        with:
          path: ./public
```

- [ ] **Step 6: Record policy and the change log in `CLAUDE.md`**

- Replace the line beginning "- Hugo **0.167.0**, pinned in two places" with:
  `- Hugo **0.167.0**, pinned only in pixi.toml / pixi.lock; CI installs it through prefix-dev/setup-pixi.`
- Append:

```markdown
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
```

Add `.pytest_cache/` and `__pycache__/` to `.gitignore`.

- [ ] **Step 7: Commit**

```bash
git add pixi.toml pixi.lock pytest.ini tests .github/workflows/pages.yml CLAUDE.md .gitignore
git commit -m "Add build-output test harness; CI installs Hugo via pixi and runs tests"
```

---

### Task 2: Identity layer (tokens, fonts, global CSS, head)

**Files:**
- Modify: `static/css/variables.css`, `static/css/fonts.css`, `static/css/style.css:93`, `layouts/_partials/site/styles.html`, `layouts/baseof.html`, `data/settings.yaml`, `CLAUDE.md`
- Create: `static/css/aquicirc.css`, `static/fonts/archivo-latin-wdth-normal.woff2`, `static/fonts/archivo-latin-ext-wdth-normal.woff2`, `static/fonts/source-serif-4-latin-wght-normal.woff2`, `static/fonts/source-serif-4-latin-ext-wght-normal.woff2`, `static/fonts/source-serif-4-latin-wght-italic.woff2`, `static/fonts/source-serif-4-latin-ext-wght-italic.woff2`, `static/fonts/OFL.txt`, `tests/test_identity.py`
- Delete: `static/fonts/heebo-*.woff2`, `static/fonts/signika-*.woff2`

**Guides to retrieve first:** `visually-stable-font-fallbacks`, `improve-text-layout-and-legibility`, `cross-document-transitions`, `consistent-cross-document-transitions`, `accessibility`, `css`.

**Interfaces:**
- Produces CSS custom properties used by every later CSS file: `--aquifer`, `--flow`, `--recharge`, `--porewater`, `--sediment`, `--page`, `--fontTitles`, `--fontBody`, `--surface-ring` (2px ring colour = `--page`).
- Produces the class `.visually-hidden`.
- Produces the reveal convention: an element with `data-reveal` shows its `.reveal` child on `:hover` / `:focus-within` unless it has class `dismissed`. The JS lands in Task 7.

- [ ] **Step 1: Write the failing tests**

`tests/test_identity.py`:

```python
import re


def test_tokens_present(css):
    text = css()
    for token, value in {
        "--aquifer": "#0F2A3F", "--flow": "#2471A1", "--recharge": "#32B8D9",
        "--porewater": "#EAF4F7", "--sediment": "#C9B38A",
    }.items():
        assert re.search(rf"{token}:\s*{value}", text, re.I), token


def test_fonts_are_archivo_and_source_serif(css):
    text = css()
    assert '"Archivo"' in text and '"Source Serif 4"' in text
    assert "Signika" not in text and "Heebo" not in text


def test_one_font_preload_and_render_expect(html):
    head = html("/").head
    preloads = head.find_all("link", rel="preload")
    assert len(preloads) == 1
    assert preloads[0]["href"] == "/fonts/archivo-latin-wdth-normal.woff2"
    assert preloads[0].has_attr("crossorigin")
    expect = head.find("link", rel="expect")
    assert expect["href"] == "#main" and expect["blocking"] == "render"


def test_view_transitions_respect_reduced_motion(css):
    text = css()
    block = text[text.index("@view-transition") - 80: text.index("@view-transition")]
    assert "prefers-reduced-motion: no-preference" in block


def test_until_found_is_not_display_none(css):
    assert '[hidden]:not([hidden="until-found"])' in css()


def test_section_fade_ins_are_off():
    import yaml
    from pathlib import Path
    settings = yaml.safe_load((Path(__file__).resolve().parents[1] / "data/settings.yaml").read_text())
    assert settings["intersectionobserver"] is False
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k identity`
Expected: FAIL (tokens missing, fonts are Signika/Heebo, no preload).

- [ ] **Step 3: Fetch fonts (OFL)**

```bash
cd static/fonts && rm -f heebo-*.woff2 signika-*.woff2
for f in archivo/files/archivo-latin-wdth-normal archivo/files/archivo-latin-ext-wdth-normal \
         source-serif-4/files/source-serif-4-latin-wght-normal source-serif-4/files/source-serif-4-latin-ext-wght-normal \
         source-serif-4/files/source-serif-4-latin-wght-italic source-serif-4/files/source-serif-4-latin-ext-wght-italic; do
  curl -fsSLO "https://cdn.jsdelivr.net/npm/@fontsource-variable/$f.woff2"
done
curl -fsSL -o OFL.txt https://raw.githubusercontent.com/googlefonts/archivo/main/OFL.txt
ls -la && cd ../..
```
Expected: six `.woff2` files (≈40–90 kB each) and `OFL.txt`. If the OFL URL 404s, use `https://cdn.jsdelivr.net/npm/@fontsource-variable/archivo/LICENSE`.

- [ ] **Step 4: Replace `static/css/fonts.css`**

```css
/* ==========================================================================
   Web fonts — Archivo (titles, menu, buttons) and Source Serif 4 (body).
   Variable woff2 from Fontsource, OFL-1.1 (static/fonts/OFL.txt).
   latin-ext first so latin wins the overlap.
   ========================================================================== */

@font-face {
    font-family: "Archivo";
    font-style: normal;
    font-weight: 100 900;
    font-stretch: 62% 125%;
    font-display: swap;
    src: url("/fonts/archivo-latin-ext-wdth-normal.woff2") format("woff2");
    unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
    font-family: "Archivo";
    font-style: normal;
    font-weight: 100 900;
    font-stretch: 62% 125%;
    font-display: swap;
    src: url("/fonts/archivo-latin-wdth-normal.woff2") format("woff2");
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
    font-family: "Source Serif 4";
    font-style: normal;
    font-weight: 200 900;
    font-display: swap;
    src: url("/fonts/source-serif-4-latin-ext-wght-normal.woff2") format("woff2");
    unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
    font-family: "Source Serif 4";
    font-style: normal;
    font-weight: 200 900;
    font-display: swap;
    src: url("/fonts/source-serif-4-latin-wght-normal.woff2") format("woff2");
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
    font-family: "Source Serif 4";
    font-style: italic;
    font-weight: 200 900;
    font-display: swap;
    src: url("/fonts/source-serif-4-latin-ext-wght-italic.woff2") format("woff2");
    unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
    font-family: "Source Serif 4";
    font-style: italic;
    font-weight: 200 900;
    font-display: swap;
    src: url("/fonts/source-serif-4-latin-wght-italic.woff2") format("woff2");
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
```

- [ ] **Step 5: Replace the colour and type parts of `static/css/variables.css`**

Replace the `/* colour */` and `/* type */` groups inside `:root` with the block below, keeping the measure and rhythm groups. Delete the `:root[data-color=…]` theme lines at the bottom.

```css
    /* colour — AQUICIRC, from the logo */
    --aquifer:   #0F2A3F;
    --flow:      #2471A1;
    --recharge:  #32B8D9;   /* decoration only: never text, never a data mark on light */
    --porewater: #EAF4F7;
    --sediment:  #C9B38A;
    --page:      #FFFFFF;
    --surface-ring: var(--page);

    /* v2 names, mapped */
    --textDarker:   var(--aquifer);
    --textDark:     var(--aquifer);
    --textMedium:   rgb(15 42 63 / 0.78);
    --borderMedium: rgb(15 42 63 / 0.22);
    --borderLight:  rgb(15 42 63 / 0.08);
    --light:        var(--porewater);
    --accent:       var(--flow);
    --accentDarker: #1B5A80;
    --scrim:        rgb(15 42 63 / 0.4);

    /* type */
    --fontTitles: "Archivo", ui-sans-serif, system-ui, sans-serif;
    --fontBody:   "Source Serif 4", ui-serif, Georgia, serif;
```

- [ ] **Step 6: Fix `[hidden]` in `static/css/style.css:93`**

Change `[hidden] { display: none !important; }` to:

```css
[hidden]:not([hidden="until-found"]) { display: none !important; }
```

- [ ] **Step 7: Create `static/css/aquicirc.css`**

```css
/* ==========================================================================
   AQUICIRC identity layer. Loaded after the core and before the bricks.
   ========================================================================== */

html { font-size: 100%; }
body {
    font-size: 1.0625rem;
    line-height: 1.6;
    font-size-adjust: from-font;
    color: var(--aquifer);
    background: var(--page);
}
h1, h2, h3, .button, .mainnav, .logo strong {
    font-family: var(--fontTitles);
    font-stretch: 112%;
    font-size-adjust: from-font;
}
h1 { font-size: clamp(2.25rem, 1.6rem + 3vw, 3.5rem); font-weight: 700; letter-spacing: -0.01em; }
h2 { font-size: clamp(1.75rem, 1.4rem + 1.6vw, 2.4rem); font-weight: 650; }
h3 { font-size: 1.3rem; font-weight: 650; }
h1, h2, h3 { text-wrap: balance; }
p, li, dd { text-wrap: pretty; }
.container.medium > :is(p, ul, ol, dl) { max-width: 68ch; }

a { color: var(--flow); text-underline-offset: 0.15em; }
:focus-visible { outline: 0.2rem solid var(--flow); outline-offset: 0.2rem; }

.button { min-height: 2.75rem; display: inline-flex; align-items: center; }
.mainnav a { min-height: 2.75rem; display: inline-flex; align-items: center; }

.visually-hidden {
    position: absolute !important; width: 1px; height: 1px; overflow: hidden;
    clip-path: inset(50%); white-space: nowrap;
}

/* In-place reveal (transect, timeline): the .reveal child shows on hover or
   focus of its [data-reveal] host, and Escape adds .dismissed (site.js). */
[data-reveal] .reveal { visibility: hidden; opacity: 0; }
[data-reveal]:is(:hover, :focus-within):not(.dismissed) .reveal { visibility: visible; opacity: 1; }
@media (prefers-reduced-motion: no-preference) {
    [data-reveal] .reveal { transition: opacity 0.15s ease, visibility 0.15s; }
}

/* Empty states */
.empty { color: var(--textMedium); font-style: italic; }

/* Strata band (decorative) */
.strata { display: block; width: 100%; height: 3rem; }
.strata .land { fill: var(--sediment); opacity: 0.7; }
.strata .vadose { fill: var(--sediment); opacity: 0.35; }
.strata .aquifer { fill: var(--porewater); }
.strata .watertable { stroke: var(--recharge); stroke-width: 2; fill: none; vector-effect: non-scaling-stroke; }
@media (forced-colors: active) { .strata { display: none; } }

/* Page-to-page transitions */
@media (prefers-reduced-motion: no-preference) {
    @view-transition { navigation: auto; }
    html { scroll-behavior: smooth; }
}
::view-transition-group(*) { animation-duration: 0.3s; }
```

- [ ] **Step 8: Bundle it and add the head links**

In `layouts/_partials/site/styles.html`, add `(resources.Get "css/aquicirc.css")` to the `slice` immediately after `(resources.Get "css/tabs.css")`.

In `layouts/baseof.html`, directly after `{{ partial "site/favicon.html" . }}` add:

```html
    <link rel="preload" href="/fonts/archivo-latin-wdth-normal.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="expect" href="#main" blocking="render">
```

In `data/settings.yaml` set `intersectionobserver: false`.

- [ ] **Step 9: Run tests**

Run: `pixi run test`
Expected: all pass.

- [ ] **Step 10: Log vendored changes in `CLAUDE.md`** (append under "Changes vs upstream")

```markdown
- `static/css/variables.css`: AQUICIRC colour/type tokens; v2 names mapped onto them; colour themes removed.
- `static/css/fonts.css`, `static/fonts/`: Archivo + Source Serif 4 replace Signika + Heebo.
- `static/css/style.css`: `[hidden]` rule excludes `hidden="until-found"`.
- `layouts/_partials/site/styles.html`: bundles `css/aquicirc.css`.
- `layouts/baseof.html`: Archivo preload, `<link rel="expect" href="#main" blocking="render">`.
- `data/settings.yaml`: `intersectionobserver: false`.
```

- [ ] **Step 11: Commit**

```bash
git add -A static/css static/fonts layouts data/settings.yaml tests/test_identity.py CLAUDE.md
git commit -m "Add AQUICIRC identity layer: tokens, Archivo + Source Serif 4, transitions"
```

---

### Task 3: Project data and its validation

**Files:**
- Create: `data/project.yaml`, `data/en/partners.yaml`, `data/en/workpackages.yaml`, `data/en/deliverables.yaml`, `data/en/publications.yaml`, `data/en/datasets.yaml`, `data/en/people.yaml`, `data/en/features.yaml`, `tests/test_data.py`

**Interfaces:**
- Produces the data shapes in spec §5. Later templates access them as `$d.partners`, `$d.workpackages`, `$d.deliverables`, `$d.publications`, `$d.datasets`, `$d.people`, `$d.features` (where `$d := partial "data.html" .Page`) and `hugo.Data.project`.
- Quarter strings are always `Y<1-3>Q<1-4>`.
- Partner ids: `wu, su, uwc, iot, vub, unipd, upc, inat, csir, umvoto`.

- [ ] **Step 1: Write the failing validation tests**

`tests/test_data.py`:

```python
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUARTER = re.compile(r"^Y[1-3]Q[1-4]$")


def load(name):
    return yaml.safe_load((ROOT / "data" / "en" / f"{name}.yaml").read_text()) or []


def front_matter(path):
    text = path.read_text()
    return yaml.safe_load(text.split("---")[1])


def qindex(q):
    return (int(q[1]) - 1) * 4 + int(q[3]) - 1


def test_partner_ids_unique():
    ids = [p["id"] for p in load("partners")]
    assert len(ids) == len(set(ids))


def test_workpackage_leads_are_partners():
    partners = {p["id"] for p in load("partners")}
    for wp in load("workpackages"):
        assert set(wp["leads"]) <= partners, wp["id"]


def test_tasks_have_valid_ordered_quarters():
    for wp in load("workpackages"):
        for t in wp["tasks"]:
            assert QUARTER.match(t["start"]) and QUARTER.match(t["end"]), t["id"]
            assert qindex(t["start"]) <= qindex(t["end"]), t["id"]


def test_deliverables_reference_real_wps_and_states():
    wps = {wp["id"] for wp in load("workpackages")}
    for d in load("deliverables"):
        assert d["wp"] in wps, d["id"]
        assert QUARTER.match(d["due"]), d["id"]
        assert d["status"] in {"planned", "submitted", "public"}, d["id"]
        if d["status"] == "public":
            assert d.get("url"), f"{d['id']} is public but has no url"


def test_site_pages_reference_real_partners():
    partners = {p["id"] for p in load("partners")}
    for path in (ROOT / "content/en/sites").glob("*.md"):
        if path.name == "_index.md":
            continue
        fm = front_matter(path)
        unknown = set(fm.get("partners", [])) - partners
        assert not unknown, f"{path.name}: unknown partner ids {unknown}"


def test_posts_reference_real_sites():
    sites = {p.stem for p in (ROOT / "content/en/sites").glob("*.md") if p.name != "_index.md"}
    for path in (ROOT / "content/en/posts").glob("*.md"):
        if path.name == "_index.md":
            continue
        unknown = set(front_matter(path).get("sites") or []) - sites
        assert not unknown, f"{path.name}: unknown site slugs {unknown}"


def test_people_groups_and_affiliations():
    partners = {p["id"] for p in load("partners")}
    for person in load("people"):
        assert person["group"] in {"team", "advisory"}, person["name"]
        if person.get("affiliation"):
            assert person["affiliation"] in partners, person["name"]
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k data`
Expected: FAIL with `FileNotFoundError` for `partners.yaml`.

- [ ] **Step 3: Write the data files**

`data/project.yaml`:

```yaml
start: 2026-01-01
months: 36
```

`data/en/partners.yaml`:

```yaml
- id: wu
  name: Wageningen University & Research
  short: WUR
  country: Netherlands
  url: https://www.wur.nl/
  logo: ""            # TODO(content): partner logo (SVG preferred)
  role: coordinator
  wps: [WP1]
- id: su
  name: Stellenbosch University
  short: SU
  country: South Africa
  url: https://www.sun.ac.za/
  logo: ""            # TODO(content): partner logo
  role: wp-lead
  wps: [WP2]
- id: uwc
  name: University of the Western Cape
  short: UWC
  country: South Africa
  url: https://www.uwc.ac.za/
  logo: ""            # TODO(content): partner logo
  role: wp-lead
  wps: [WP2]
- id: iot
  name: Io-Things
  short: IoT
  country: Belgium
  url: ""             # TODO(content): Io-Things website
  logo: ""            # TODO(content): partner logo
  role: wp-lead
  wps: [WP3]
- id: vub
  name: Vrije Universiteit Brussel
  short: VUB
  country: Belgium
  url: https://www.vub.be/
  logo: ""            # TODO(content): partner logo
  role: wp-lead
  wps: [WP3]
- id: unipd
  name: University of Padova
  short: UNIPD
  country: Italy
  url: https://www.unipd.it/
  logo: ""            # TODO(content): partner logo
  role: wp-lead
  wps: [WP4]
- id: upc
  name: Polytechnic University of Catalonia
  short: UPC
  country: Spain
  url: https://www.upc.edu/
  logo: ""            # TODO(content): partner logo
  role: wp-lead
  wps: [WP5]
- id: inat
  name: National Agronomic Institute of Tunisia
  short: INAT
  country: Tunisia
  url: ""             # TODO(content): INAT website
  logo: ""            # TODO(content): partner logo
  role: wp-lead
  wps: [WP6]
- id: csir
  name: Council for Scientific and Industrial Research
  short: CSIR
  country: South Africa
  url: https://www.csir.co.za/
  logo: ""            # TODO(content): partner logo
  role: partner
  wps: []
- id: umvoto
  name: Umvoto
  short: Umvoto
  country: South Africa
  url: ""             # TODO(content): Umvoto website
  logo: ""            # TODO(content): partner logo
  role: partner
  wps: []
```

`data/en/workpackages.yaml` (titles and spans from proposal §h):

```yaml
- id: WP1
  title: Project management and coordination
  leads: [wu]
  summary: Coordination, data management, the consortium agreement, plenary meetings and reporting to the funders.
  tasks:
    - { id: T1.1, title: General coordination, project management and administration, start: Y1Q1, end: Y3Q4 }
    - { id: T1.2, title: Consortium agreement and risk assessment, start: Y1Q1, end: Y1Q2 }
    - { id: T1.3, title: Plenary meetings and reporting, start: Y1Q1, end: Y3Q4 }
- id: WP2
  title: Performance evaluation of existing MAR sites
  leads: [su, uwc]
  summary: How well each site stores, recovers and cleans water today, and where it can improve.
  tasks:
    - { id: T2.1, title: Data collection and site work definition, start: Y1Q1, end: Y1Q4 }
    - { id: T2.2, title: Hydrological and water quality assessment, start: Y1Q1, end: Y1Q4 }
- id: WP3
  title: Monitoring and installation of additional equipment
  leads: [iot, vub]
  summary: Multi-level piezometers, site-specific sampling for emerging contaminants, and low-cost IoT sensors compared with conventional measurements.
  tasks:
    - { id: T3.1, title: Installation of additional monitoring equipment and infrastructure, start: Y1Q2, end: Y2Q2 }
    - { id: T3.2, title: Development of the CEC sampling plan, start: Y1Q2, end: Y2Q2 }
    - { id: T3.3, title: Regular hydrogeochemical monitoring, start: Y1Q3, end: Y2Q4 }
- id: WP4
  title: Predictive models for MAR systems
  leads: [unipd]
  summary: Flow and reactive transport models of each site, used to test management and design scenarios.
  tasks:
    - { id: T4.1, title: Development of flow models, start: Y1Q4, end: Y3Q1 }
    - { id: T4.2, title: Reactive transport modelling, start: Y2Q1, end: Y3Q2 }
    - { id: T4.3, title: Scenario analysis and model-based decision support, start: Y2Q2, end: Y3Q4 }
- id: WP5
  title: Optimising MAR systems for storage and treatment
  leads: [upc]
  summary: Design and operating changes tested in the lab and at pilot scale, then shared across sites.
  tasks:
    - { id: T5.1, title: Identification of optimisation opportunities, start: Y1Q3, end: Y2Q3 }
    - { id: T5.2, title: Pilot-scale testing of optimised designs, start: Y2Q1, end: Y3Q1 }
    - { id: T5.3, title: Cross-site learning and recommendations, start: Y2Q4, end: Y3Q4 }
- id: WP6
  title: Knowledge use, stakeholder engagement and policy
  leads: [inat]
  summary: Workshops with MAR operators and regulators, open-access publications, and this website.
  tasks:
    - { id: T6.1, title: Stakeholder co-creation workshops, start: Y1Q2, end: Y3Q2 }
    - { id: T6.2, title: Scientific dissemination and open-access publishing, start: Y2Q1, end: Y3Q4 }
    - { id: T6.3, title: Project website and social media, start: Y1Q1, end: Y3Q4 }
```

`data/en/deliverables.yaml` (statuses other than D6.3 need owner confirmation):

```yaml
# TODO(content): confirm the status of every deliverable due so far.
- { id: D1.1, title: Data management plan, wp: WP1, due: Y1Q2, status: planned }
- { id: D1.2, title: Consortium agreement, wp: WP1, due: Y1Q2, status: planned }
- { id: D1.3a, title: Interim report, wp: WP1, due: Y2Q3, status: planned }
- { id: D1.3b, title: Final report, wp: WP1, due: Y3Q4, status: planned }
- { id: D2.1, title: Case study site profiles, wp: WP2, due: Y1Q4, status: planned }
- { id: D2.2, title: Cross-site performance evaluation report, wp: WP2, due: Y1Q4, status: planned }
- { id: D3.1, title: Installation completion report, wp: WP3, due: Y2Q2, status: planned }
- { id: D3.2, title: Site-specific sampling protocols, wp: WP3, due: Y2Q2, status: planned }
- { id: D3.3, title: Hydrogeochemical monitoring database, wp: WP3, due: Y2Q4, status: planned }
- { id: D4.1, title: Site-specific flow model datasets and files, wp: WP4, due: Y3Q1, status: planned }
- { id: D4.2, title: Reactive transport modelling dataset and model files, wp: WP4, due: Y3Q2, status: planned }
- { id: D4.3, title: Scenario analysis datasets and outputs, wp: WP4, due: Y3Q4, status: planned }
- { id: D5.1, title: Optimisation strategy report, wp: WP5, due: Y2Q3, status: planned }
- { id: D5.2, title: Pilot test evaluation report, wp: WP5, due: Y3Q1, status: planned }
- { id: D5.3, title: Cross-site optimisation guidelines, wp: WP5, due: Y3Q4, status: planned }
- { id: D6.1a, title: Workshop summary reports (kick-off), wp: WP6, due: Y1Q2, status: planned }
- { id: D6.1b, title: Workshop summary reports (final), wp: WP6, due: Y3Q2, status: planned }
- { id: D6.2, title: Scientific publications and repository index, wp: WP6, due: Y3Q4, status: planned }
- { id: D6.3, title: Project website, wp: WP6, due: Y1Q2, status: public, url: "https://aquicirc.eu/" }
```

`data/en/publications.yaml` and `data/en/datasets.yaml`: each contains exactly `[]`.

`data/en/people.yaml`:

```yaml
# TODO(content): confirm consent to list both advisory board members; add the team.
- name: Ricky Murray
  function: Project advisory board, Africa
  group: advisory
  description: Hydrogeologist with more than 35 years of groundwater and MAR experience across southern and eastern Africa; principal architect of South Africa's Artificial Recharge Strategy.
- name: Sarah Garré
  function: Project advisory board, Europe
  group: advisory
  description: Expert in water, soil functioning and agricultural hydrology (ILVO, KU Leuven, ULiège), with experience in research that links science, policy and society.
```

`data/en/features.yaml` (the three objectives; icons from v2's set):

```yaml
- icon: /img/icons/material-symbols/200/rounded/performance_max.svg
  title: Follow the contaminants
  description: Track how pharmaceuticals, pesticides, PFAS and other contaminants of emerging concern move and break down in aquifers recharged with treated wastewater and other unconventional water.
- icon: /img/icons/material-symbols/200/rounded/design_services.svg
  title: Model recharge before changing it
  description: Build flow and reactive transport models that predict water quality and guard coastal aquifers against seawater intrusion.
- icon: /img/icons/material-symbols/200/rounded/auto_fix.svg
  title: Test better designs
  description: Measure what permeable reactive materials and natural attenuation add to recharge systems in very different climates and geologies.
```

- [ ] **Step 4: Run tests**

Run: `pixi run test -k data`
Expected: all pass. The posts and sites tests pass vacuously until Tasks 5 and 10 add files.

- [ ] **Step 5: Commit**

```bash
git add data tests/test_data.py
git commit -m "Add project data (partners, WPs, deliverables, people, objectives) with validation"
```

---

### Task 4: Header menu, footer and funding acknowledgement

**Files:**
- Modify: `data/en/header.yaml`, `data/en/footer.yaml`, `data/en/general.yaml`, `layouts/_partials/site/footer.html`, `CLAUDE.md`
- Create: `static/img/bluesky.svg`, `tests/test_chrome.py`

**Interfaces:**
- Consumes: tokens from Task 2.
- Produces: `data/en/footer.yaml` keys `footer_text`, `socials[] {title, link, logo_image}` and `funders[] {name, logo, url}`.

- [ ] **Step 1: Write the failing tests**

`tests/test_chrome.py`:

```python
MENU = ["About", "Case studies", "Consortium", "News", "Outputs"]


def test_main_menu_order(html):
    nav = html("/").find("nav", class_="mainnav") or html("/").select_one("header nav")
    labels = [a.get_text(strip=True) for a in nav.find_all("a") if a.get_text(strip=True)]
    assert labels[:5] == MENU


def test_footer_has_funding_statement_and_funders_slot(html):
    footer = html("/").find("footer")
    assert "Water4All" in footer.get_text()
    assert footer.select_one(".funders") is not None


def test_contact_email_slot_renders_when_set(build_variant):
    def set_email(root):
        p = root / "data/en/general.yaml"
        p.write_text(p.read_text().replace('email: ""', "email: info@example.org"))
    assert build_variant(set_email).returncode == 0


def test_socials_are_linkedin_and_bluesky(html):
    text = html("/").find("footer").get_text()
    assert "LinkedIn" in text and "Bluesky" in text
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k chrome`
Expected: FAIL (empty menu, no funders).

- [ ] **Step 3: Data**

`data/en/header.yaml`:

```yaml
logo_image: /uploads/branding/aquicirc-logo.png
logo_subtitle: Managed aquifer recharge for a circular water future
dark_header: false
mobile_view_width: 1000
menuitems:
  - { title: About, link: /about/ }
  - { title: Case studies, link: /sites/ }
  - { title: Consortium, link: /consortium/ }
  - { title: News, link: /news/ }
  - { title: Outputs, link: /outputs/ }
cta:
  active: false
```

`data/en/footer.yaml`:

```yaml
logo_image: /uploads/branding/aquicirc-logo.png
menuitems: []
socials:
  - title: LinkedIn
    link: "https://www.linkedin.com/"   # TODO(content): AQUICIRC LinkedIn page
    logo_image: /img/linkedin.svg
  - title: Bluesky
    link: "https://bsky.app/"           # TODO(content): AQUICIRC Bluesky profile
    logo_image: /img/bluesky.svg
footer_text: >-
  AQUICIRC is funded through the Water4All partnership, co-funded by the European Union.
  TODO(content): exact funding statement and grant number.
funders: []   # TODO(content): {name, logo, url} for Water4All, the EU emblem and national agencies
```

`data/en/general.yaml`: add

```yaml
contact:
  email: ""   # TODO(content): project contact address
```

`static/img/bluesky.svg` (single-colour butterfly, `currentColor`-free path at 24×24):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5.2 3.6C7.9 5.6 10.8 9.7 12 12c1.2-2.3 4.1-6.4 6.8-8.4 2-1.4 5.2-2.6 5.2 1 0 .7-.4 6-.6 6.9-.8 3-3.8 3.7-6.5 3.3 4.7.8 5.9 3.5 3.3 6.1-4.9 5-7-1.3-7.6-2.9l-.6-1.7-.6 1.7c-.6 1.6-2.7 7.9-7.6 2.9-2.6-2.6-1.4-5.3 3.3-6.1-2.7.4-5.7-.3-6.5-3.3C.4 10.6 0 5.3 0 4.6c0-3.6 3.2-2.4 5.2-1Z"/></svg>
```

- [ ] **Step 4: Footer template**

In `layouts/_partials/site/footer.html`, replace the line `{{ with $d.footer.footer_text }}<div>{{ . | markdownify }}</div>{{ end }}` with:

```html
            {{ with $d.general.contact.email }}<p class="contact"><a href="mailto:{{ . }}">{{ . }}</a></p>{{ end }}
            {{ with $d.footer.footer_text }}<div class="funding">{{ . | markdownify }}</div>{{ end }}
            <ul class="funders" aria-label="Funders">
                {{- range $d.footer.funders -}}
                <li><a href="{{ .url }}" rel="noopener"><img src="{{ .logo }}" alt="{{ .name }}" height="48" loading="lazy"></a></li>
                {{- end -}}
            </ul>
```

Append to `static/css/aquicirc.css`:

```css
.sitefooter .funders { display: flex; flex-wrap: wrap; gap: 1.5rem; list-style: none; padding: 0; margin: 1rem 0 0; }
.sitefooter .funders:empty { display: none; }
.sitefooter .funders img { height: 3rem; width: auto; }
```

- [ ] **Step 5: Run tests**

Run: `pixi run test`
Expected: all pass.

- [ ] **Step 6: Log and commit**

Append to "Changes vs upstream" in `CLAUDE.md`: `` - `layouts/_partials/site/footer.html`: funding statement wrapper + `funders` logo list from `data/en/footer.yaml`. ``

```bash
git add data/en static/img/bluesky.svg static/css/aquicirc.css layouts/_partials/site/footer.html tests/test_chrome.py CLAUDE.md
git commit -m "Add menu, socials and funding acknowledgement to header and footer"
```

---

### Task 5: Site pages and their layout

**Files:**
- Create: `content/en/sites/_index.md`, `content/en/sites/{lieshout,kinrooi,besos,llobregat,wadi-khairat,cape-town}.md`, `layouts/_partials/sites-by-latitude.html`, `layouts/sites/page.html`, `static/css/sections/site.css`, `tests/test_sites.py`

**Interfaces:**
- Consumes: `$d.partners` (Task 3).
- Produces:
  - `partial "sites-by-latitude.html" .` → slice of site pages, north → south by `index (index .Params.coordinates 0) 0`. Used by Tasks 7, 8.
  - Each site `<h1>` has `style="view-transition-name: site-<slug>"`. Task 7 must use the identical name.
  - Site pages contain `<section class="locator" data-map …>`. Task 13 adds the JS.

- [ ] **Step 1: Write the failing tests**

`tests/test_sites.py`:

```python
NORTH_TO_SOUTH = ["lieshout", "kinrooi", "besos", "llobregat", "wadi-khairat", "cape-town"]


def test_every_site_page_builds_with_facts(html):
    for slug in NORTH_TO_SOUTH:
        doc = html(f"/sites/{slug}/")
        assert doc.find("h1")["style"] == f"view-transition-name: site-{slug}"
        facts = doc.select_one("dl.facts")
        terms = [dt.get_text(strip=True) for dt in facts.find_all("dt")]
        assert terms[:4] == ["Climate", "Aquifer", "MAR system", "Source water"]


def test_previous_next_follow_latitude(html):
    nav = html("/sites/besos/").select_one("nav.sitenav")
    links = {a["rel"][0]: a["href"] for a in nav.find_all("a")}
    assert links["prev"] == "/sites/kinrooi/" and links["next"] == "/sites/llobregat/"
    first = html("/sites/lieshout/").select_one("nav.sitenav")
    assert first.find("a", rel="prev") is None


def test_partners_link_to_consortium(html):
    dd = html("/sites/cape-town/").select_one("dl.facts dd.partners")
    hrefs = [a["href"] for a in dd.find_all("a")]
    assert "/consortium/#partner-su" in hrefs


def test_site_news_empty_state(html):
    section = html("/sites/wadi-khairat/").select_one("section.sitenews")
    assert section.select_one(".empty")


def test_missing_required_field_fails_build(build_variant):
    def break_it(root):
        p = root / "content/en/sites/kinrooi.md"
        p.write_text(p.read_text().replace("mar_system:", "old_mar_system:"))
    result = build_variant(break_it)
    assert result.returncode != 0
    assert 'missing required front matter "mar_system"' in result.stderr


def test_image_without_alt_fails_build(build_variant):
    def break_it(root):
        p = root / "content/en/sites/kinrooi.md"
        p.write_text(p.read_text().replace("title:", "image: /uploads/x.jpg\ntitle:", 1))
    result = build_variant(break_it)
    assert result.returncode != 0 and "image_alt" in result.stderr
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k sites`
Expected: FAIL (`/sites/kinrooi/ was not built`).

- [ ] **Step 3: Site content (plain Markdown, no shortcodes)**

`content/en/sites/_index.md` (the composition is completed in Task 8):

```markdown
---
title: Case studies
---

# Six sites, one question

From the Netherlands to the Western Cape, each site recharges an aquifer with a different kind of water, under a different climate, through a different system. Comparing them shows what holds everywhere and what depends on the place.
```

`content/en/sites/lieshout.md`:

```markdown
---
title: Swinkels Family Brewery, Lieshout
country: Netherlands
location: Lieshout, North Brabant
coordinates: [[51.52, 5.60]]   # TODO(content): confirm with WUR
climate: Temperate, high rainfall
aquifer: Shallow unconfined, sandy soils
mar_system: Subsurface irrigation with treated industrial wastewater
source_water: Treated brewery wastewater
expected_cecs: [PFAS, Industrial organics]
partners: [wu]
references:
  - text: de Wit et al., 2022
    doi: 10.1016/j.agwat.2022.107677
---

The brewery plans to send its treated wastewater into a subsurface irrigation system that recharges the local aquifer. Little is known yet about what this does to groundwater quality, so AQUICIRC measures and models it before the scheme scales up.
```

`content/en/sites/kinrooi.md`:

```markdown
---
title: GROW pilot, Kinrooi
country: Belgium
location: Kinrooi, Limburg
coordinates: [[51.15, 5.74]]   # TODO(content): confirm with VUB
climate: Temperate
aquifer: Shallow unconfined; sandy, loamy and gravel layers
mar_system: Subsurface irrigation with treated domestic wastewater
source_water: Effluent from a municipal treatment plant
expected_cecs: [PFAS, Pharmaceuticals, Pesticides]
partners: [vub, iot]
references:
  - text: Luo et al., 2023
    doi: 10.1007/s11783-024-1806-5
---

Treated domestic wastewater has been applied to an agricultural field through subsurface irrigation for three years. Groundwater levels and quality are monitored and modelled; the long-term fate of PFAS, pharmaceuticals and pesticides is still open. Low-cost water quality sensors and real-time control are tested here.
```

`content/en/sites/besos.md`:

```markdown
---
title: Besòs river basin
country: Spain
location: North of Barcelona
coordinates: [[41.44, 2.19]]   # TODO(content): confirm with UPC
climate: Mediterranean, seasonal droughts
aquifer: Alluvial, sandy
mar_system: Direct injection
source_water: Reclaimed water after a phytoremediation zone
expected_cecs: [Pharmaceuticals, Pesticides]
partners: [upc]
references:
  - text: Valhondo et al., 2020
    doi: 10.3390/w12041012
---

A pilot site adapted to test a naturalised pretreatment zone planted with common reed (*Phragmites australis*) before the water reaches the aquifer.
```

`content/en/sites/llobregat.md`:

```markdown
---
title: Llobregat river basin
country: Spain
location: South of Barcelona
coordinates: [[41.38, 2.02]]   # TODO(content): confirm with UPC
climate: Mediterranean, seasonal droughts
aquifer: Alluvial, sandy, highly permeable
mar_system: Infiltration basins
source_water: River and reclaimed water
expected_cecs: [Pharmaceuticals, Pesticides]
partners: [upc]
references:
  - text: Sanchez-Vila et al., 2012
    doi: 10.1007/698_2012_154
---

Fifty years of recharge practice with river water, diverted channels and reclaimed water. The pilot here tests permeable reactive materials that improve contaminant removal during infiltration.
```

`content/en/sites/wadi-khairat.md`:

```markdown
---
title: Wadi Khairat
country: Tunisia
location: Sousse governorate
coordinates: [[36.13, 10.38]]   # TODO(content): confirm with INAT
climate: Semi-arid, episodic floods
aquifer: Shallow fractured and alluvial system
mar_system: Check dams, recharge basins and injection wells
source_water: Releases from the Wadi Khairat hill dam
expected_cecs: [Pesticides, Trace metals]
partners: [inat]
references:
  - text: Chekirbane et al., 2022
    doi: 10.1007/s12517-022-09484-7
---

Since 2002, water released from the hill dam infiltrates behind seven check dams and through three recharge basins with injection wells, feeding the aquifer that supplies irrigation and drinking water around Enfidha. AQUICIRC asks how much extra water it stores and how it changes groundwater quality.
```

`content/en/sites/cape-town.md`:

```markdown
---
title: Atlantis & Cape Flats
country: South Africa
location: Western Cape
coordinates: [[-33.57, 18.49], [-34.03, 18.55]]   # TODO(content): confirm with SU/UWC
climate: Winter rainfall, variable
aquifer: Sandy coastal aquifers
mar_system: Infiltration basins (Atlantis), planned injection (Cape Flats)
source_water: Treated domestic and industrial wastewater, stormwater
expected_cecs: [PFAS, Urban and industrial organics]
partners: [su, uwc, csir, umvoto]
references:
  - text: Jovanovic et al., 2017
    doi: 10.4314/wsa.v43i1.15
---

Atlantis has recharged its aquifer through infiltration basins for more than 40 years. Cape Flats plans to inject treated effluent directly. Comparing the two shows what each approach does for water quality, including PFAS that current treatment does not target.
```

- [ ] **Step 4: The sorting partial**

`layouts/_partials/sites-by-latitude.html`:

```go-html-template
{{- /*
  The site pages, north to south, by the latitude of their first coordinate.
  @context {page} any page
  @returns {slice} of pages
*/ -}}
{{- $rows := slice -}}
{{- range where site.RegularPages "Section" "sites" -}}
  {{- $rows = $rows | append (dict "lat" (float (index (index .Params.coordinates 0) 0)) "page" .) -}}
{{- end -}}
{{- $pages := slice -}}
{{- range sort $rows "lat" "desc" -}}{{- $pages = $pages | append .page -}}{{- end -}}
{{- return $pages -}}
```

- [ ] **Step 5: The site layout**

`layouts/sites/page.html`:

```go-html-template
{{- /*
  A case-study site, rendered whole (not split into bricks): header, key facts,
  prose, locator map, related news, references, previous/next north → south.
*/ -}}
{{ define "sections" }}
{{- $p := . -}}
{{- range slice "country" "coordinates" "mar_system" -}}
  {{- if not (index $p.Params .) -}}
    {{- errorf "site page %q is missing required front matter %q" $p.File.Path . -}}
  {{- end -}}
{{- end -}}
{{- if and $p.Params.image (not $p.Params.image_alt) -}}
  {{- errorf "site page %q has an image but no image_alt" $p.File.Path -}}
{{- end -}}
{{- $d := partial "data.html" $p -}}
{{- $slug := $p.File.ContentBaseName -}}
<section class="site">
  <div class="container medium">
    {{ partial "site/breadcrumbs.html" $p }}
    <h1 style="view-transition-name: site-{{ $slug }}">{{ $p.Title }}</h1>
    <p class="site-where">{{ with $p.Params.location }}{{ . }}, {{ end }}{{ $p.Params.country }}</p>

    <dl class="facts">
      <dt>Climate</dt><dd>{{ $p.Params.climate }}</dd>
      <dt>Aquifer</dt><dd>{{ $p.Params.aquifer }}</dd>
      <dt>MAR system</dt><dd>{{ $p.Params.mar_system }}</dd>
      <dt>Source water</dt><dd>{{ $p.Params.source_water }}</dd>
      {{ with $p.Params.expected_cecs }}<dt>Expected contaminants</dt><dd>{{ delimit . ", " }}</dd>{{ end }}
      {{ with $p.Params.partners }}
      <dt>Partners</dt>
      <dd class="partners">
        {{- range $i, $id := . -}}
          {{- $partner := index (where $d.partners "id" $id) 0 -}}
          {{ if $i }}, {{ end }}<a href="/consortium/#partner-{{ $id }}">{{ $partner.name }}</a>
        {{- end -}}
      </dd>
      {{ end }}
    </dl>

    {{ with $p.Params.image }}
      {{- $src := . -}}{{- $w := 1600 -}}{{- $h := 900 -}}
      {{- with resources.GetMatch . -}}{{- $img := .Fill "1600x900 webp Center q60" -}}{{- $src = $img.RelPermalink -}}{{- end -}}
      <img class="site-image" src="{{ $src }}" alt="{{ $p.Params.image_alt }}" width="{{ $w }}" height="{{ $h }}" loading="lazy">
    {{ end }}

    <div class="site-body">{{ $p.Content }}</div>
  </div>
</section>

{{- $first := index $p.Params.coordinates 0 -}}
<section class="locator" aria-labelledby="map-title">
  <div class="container medium">
    <h2 id="map-title">Location</h2>
    <div class="map-frame" data-map data-points="{{ jsonify $p.Params.coordinates }}" data-label="{{ $p.Title }}">
      <p class="map-fallback"><a href="https://www.openstreetmap.org/?mlat={{ index $first 0 }}&amp;mlon={{ index $first 1 }}#map=11/{{ index $first 0 }}/{{ index $first 1 }}">View {{ $p.Title }} on OpenStreetMap</a></p>
      <button type="button" class="button" data-map-load hidden>Show map</button>
    </div>
  </div>
</section>

{{- $news := slice -}}
{{- range where site.RegularPages "Section" "posts" -}}
  {{- if in (.Params.sites | default slice) $slug -}}{{- $news = $news | append . -}}{{- end -}}
{{- end -}}
<section class="sitenews" aria-labelledby="sitenews-title">
  <div class="container medium">
    <h2 id="sitenews-title">News from this site</h2>
    {{ with first 3 (sort $news "Date" "desc") }}
      <ul class="sitenews-list">
        {{ range . }}<li><a href="{{ .RelPermalink }}">{{ .Title }}</a> <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date | time.Format ":date_medium" }}</time></li>{{ end }}
      </ul>
    {{ else }}
      <p class="empty">No news from this site yet. Updates appear here as the work starts.</p>
    {{ end }}
  </div>
</section>

{{ with $p.Params.references }}
<section class="references" aria-labelledby="references-title">
  <div class="container medium">
    <h2 id="references-title">References</h2>
    <ul>{{ range . }}<li>{{ .text }}{{ with .doi }}. <a href="https://doi.org/{{ . }}">doi:{{ . }}</a>{{ end }}</li>{{ end }}</ul>
  </div>
</section>
{{ end }}

{{- $all := partial "sites-by-latitude.html" $p -}}
{{- $prev := false -}}{{- $next := false -}}
{{- range $i, $s := $all -}}
  {{- if eq $s.RelPermalink $p.RelPermalink -}}
    {{- if gt $i 0 -}}{{- $prev = index $all (sub $i 1) -}}{{- end -}}
    {{- if lt (add $i 1) (len $all) -}}{{- $next = index $all (add $i 1) -}}{{- end -}}
  {{- end -}}
{{- end -}}
<nav class="sitenav" aria-label="Other sites, north to south">
  <div class="container medium">
    {{ with $prev }}<a rel="prev" href="{{ .RelPermalink }}"><span class="sitenav-dir">North</span> {{ .Title }}</a>{{ end }}
    {{ with $next }}<a rel="next" href="{{ .RelPermalink }}"><span class="sitenav-dir">South</span> {{ .Title }}</a>{{ end }}
  </div>
</nav>
{{ end }}
```

- [ ] **Step 6: Site page CSS**

`static/css/sections/site.css`:

```css
/* -- site page ---------------------------------------------------------- */
section.site { padding-block: var(--brick-space) 0; }
section.site .site-where { color: var(--textMedium); margin-block: -1rem 2rem; }
dl.facts {
    display: grid; grid-template-columns: max-content 1fr; gap: 0.5rem 1.5rem;
    background: color-mix(in srgb, var(--sediment) 18%, var(--page));
    border-inline-start: 0.25rem solid var(--sediment);
    padding: 1.25rem 1.5rem; margin-block: 0 2.5rem; border-radius: var(--radius-s);
}
dl.facts dt { font-family: var(--fontTitles); font-weight: 600; }
dl.facts dd { margin: 0; }
@media (width < 36rem) { dl.facts { grid-template-columns: 1fr; } dl.facts dd { margin-block-end: 0.5rem; } }
.site-image { width: 100%; height: auto; border-radius: var(--radius); margin-block: 1rem 2rem; }
section.locator, section.sitenews, section.references { padding-block: 2rem; }
.map-frame { min-height: 22rem; border-radius: var(--radius); background: var(--porewater); display: grid; place-content: center; gap: 1rem; text-align: center; padding: 1rem; }
.map-frame.loaded { display: block; padding: 0; overflow: hidden; }
nav.sitenav { padding-block: 2rem var(--brick-space); }
nav.sitenav .container { display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
nav.sitenav a { display: inline-flex; flex-direction: column; min-height: 2.75rem; }
nav.sitenav a[rel="next"] { margin-inline-start: auto; text-align: end; }
.sitenav-dir { font-family: var(--fontTitles); font-size: 0.85rem; color: var(--textMedium); }
```

- [ ] **Step 7: Run tests**

Run: `pixi run test`
Expected: all pass. The partners-link test passes now; the `#partner-su` anchor itself lands in Task 9.

- [ ] **Step 8: Commit**

```bash
git add content/en/sites layouts/sites layouts/_partials/sites-by-latitude.html static/css/sections/site.css tests/test_sites.py
git commit -m "Add the six case-study site pages with facts, news, references and N-S navigation"
```

---

### Task 6: Hero brick, strata band and the Home page opener

**Files:**
- Create: `layouts/_partials/sections/hero.html`, `layouts/_partials/strata.html`, `static/css/sections/hero.css`, `tests/test_home.py`
- Modify: `content/en/_index.md`

**Interfaces:**
- Produces `partial "strata.html" .` → decorative SVG (no context needed). Used again in Task 8.
- Home sections after the hero are added by Tasks 7 (transect), 10 (news), 9 (partner strip).

- [ ] **Step 1: Write the failing tests**

`tests/test_home.py`:

```python
def test_home_opens_with_hero(html):
    main = html("/").find("main")
    first = main.find("section")
    assert "hero" in first["class"]
    assert first.find("h1").get_text(strip=True) == "Managed aquifer recharge for a circular water future"
    buttons = [a.get_text(strip=True) for a in first.select("a.button")]
    assert buttons == ["See the six sites", "About the project"]


def test_strata_band_is_decorative(html):
    svg = html("/").select_one("section.hero svg.strata")
    assert svg["aria-hidden"] == "true" and svg["focusable"] == "false"


def test_objectives_section(html):
    features = html("/").select_one("section.features")
    titles = [h.get_text(strip=True) for h in features.select("ul.features h3")]
    assert titles == ["Follow the contaminants", "Model recharge before changing it", "Test better designs"]


def test_single_h1(html):
    assert len(html("/").find_all("h1")) == 1
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k home`
Expected: FAIL (first section is `wide`).

- [ ] **Step 3: Partials**

`layouts/_partials/strata.html`:

```go-html-template
{{- /* Decorative cross-section: land, unsaturated zone, water table, aquifer. */ -}}
<svg class="strata" viewBox="0 0 1200 48" preserveAspectRatio="none" aria-hidden="true" focusable="false">
  <rect class="land" x="0" y="0" width="1200" height="10"/>
  <rect class="vadose" x="0" y="10" width="1200" height="14"/>
  <rect class="aquifer" x="0" y="24" width="1200" height="24"/>
  <path class="watertable" d="M0 24 C 200 20, 400 28, 600 24 S 1000 20, 1200 24"/>
</svg>
```

`layouts/_partials/sections/hero.html`:

```go-html-template
{{- /*
  Brick: hero
  The home opener on navy: h1, lead, two buttons, strata band on its lower edge.
  Placed with `---.hero` at the top of content/en/_index.md.
  @context {dict} . Content, Name, Index, Page
*/ -}}
{{- $label := partial "section_label.html" .Content -}}
<section class="hero"{{ with $label }} aria-labelledby="{{ . }}"{{ end }}>
    <div class="container medium">
        {{ .Content }}
    </div>
    {{ partial "strata.html" . }}
</section>
```

`static/css/sections/hero.css`:

```css
/* -- brick: hero --------------------------------------------------------- */
section.hero { background: var(--aquifer); color: #fff; padding-block: clamp(3rem, 8vw, 6rem) 0; }
section.hero .container { padding-block-end: clamp(2.5rem, 6vw, 4rem); }
section.hero h1 { color: #fff; max-width: 18ch; font-stretch: 118%; margin-block-end: 1.25rem; }
section.hero p { font-size: 1.2rem; max-width: 52ch; color: rgb(255 255 255 / 0.88); }
section.hero p:has(.button) { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-block-start: 2rem; }
section.hero .button { background: #fff; color: var(--aquifer); }
section.hero .button.ghost { background: none; color: #fff; box-shadow: inset 0 0 0 0.125rem var(--recharge); }
section.hero :focus-visible { outline-color: var(--recharge); }
section.hero .strata .aquifer { fill: var(--page); }
```

- [ ] **Step 4: Home content**

Replace `content/en/_index.md`:

```markdown
---
title: Home
---

---.hero

# Managed aquifer recharge for a circular water future

AQUICIRC studies how treated wastewater, industrial effluent and harvested rainwater can safely recharge aquifers, at six sites from the Netherlands to South Africa.

[See the six sites](/sites/){:.button} [About the project](/about/){:.button .ghost}

---

## What we set out to do

{{< features >}}
```

- [ ] **Step 5: Run tests**

Run: `pixi run test`
Expected: all pass. If `test_objectives_section` fails because the section routed to `wide`, check the `features` rule in `hugo.yaml` (`has: ul.features`). The `{{< features >}}` shortcode emits `ul.features`.

- [ ] **Step 6: Commit**

```bash
git add layouts/_partials/strata.html layouts/_partials/sections/hero.html static/css/sections/hero.css content/en/_index.md tests/test_home.py
git commit -m "Add hero brick with strata band and the objectives section on Home"
```

---

### Task 7: The transect brick

**Guides to retrieve first:** `scrollytelling`, `interest-triggered-tooltips` (to confirm why it is *not* used), `cross-document-transitions`. Also re-read dataviz `references/marks-and-anatomy.md`.

**Files:**
- Create: `layouts/_partials/sections/transect.html`, `static/css/sections/transect.css`, `content/en/bricks/_index.md`, `content/en/bricks/transect.md`, `tests/test_transect.py`, `tests/browser/test_transect.py`
- Modify: `static/js/site.js` (reveal Escape), `content/en/_index.md`, `CLAUDE.md`

**Interfaces:**
- Consumes: `partial "sites-by-latitude.html"` (Task 5); `[data-reveal]`/`.reveal` CSS (Task 2).
- Produces:
  - `<section class="transect">` with `ol.transect-sites > li` carrying `--dot`, `--label` (unitless percent numbers) and `--i`.
  - Each label `span.site-name` has `view-transition-name: site-<slug>`.
  - The Escape handler in `site.js` (`[data-reveal]` → `.dismissed`), reused by Task 11.

**Scale (spec §6.1):**
- North segment: `y = 2 + (53 − lat) × 66/18` (52°N … 35°N → 2 … 68).
- Break band: 68 … 80, labelled "≈ 7,000 km".
- South segment: `y = 84 + (−33 − lat) × 7` (33°S … 35°S → 84 … 98).
- Label positions: `label = max(dot, previousLabel + 11)`, so labels never sit closer than 11% (≈ 5rem at `--h: 46rem`). A leader joins label to dot.

Expected values for the test (rounded to 2 dp):

| site | dot | label |
|---|---|---|
| lieshout | 7.43 | 7.43 |
| kinrooi | 8.78 | 18.43 |
| besos | 44.39 | 44.39 |
| llobregat | 44.61 | 55.39 |
| wadi-khairat | 64.04 | 66.39 |
| cape-town | 87.99 | 87.99 |

- [ ] **Step 1: Write the failing tests**

`tests/test_transect.py`:

```python
import re

EXPECTED = {
    "lieshout": (7.43, 7.43), "kinrooi": (8.78, 18.43), "besos": (44.39, 44.39),
    "llobregat": (44.61, 55.39), "wadi-khairat": (64.04, 66.39), "cape-town": (87.99, 87.99),
}


def items(doc):
    return doc.select("section.transect ol.transect-sites > li")


def var(style, name):
    return float(re.search(rf"--{name}:\s*([\d.]+)", style).group(1))


def test_sites_in_north_to_south_order(html):
    slugs = [li.a["href"].strip("/").split("/")[-1] for li in items(html("/sites/"))]
    assert slugs == list(EXPECTED)


def test_positions_and_label_spacing(html):
    labels = []
    for li in items(html("/sites/")):
        slug = li.a["href"].strip("/").split("/")[-1]
        dot, label = var(li["style"], "dot"), var(li["style"], "label")
        assert (round(dot, 2), round(label, 2)) == EXPECTED[slug], slug
        labels.append(label)
    assert all(b - a >= 11 - 1e-6 for a, b in zip(labels, labels[1:]))


def test_multi_coordinate_site_appears_once(html):
    hrefs = [li.a["href"] for li in items(html("/sites/"))]
    assert hrefs.count("/sites/cape-town/") == 1


def test_view_transition_names_match_site_pages(html):
    for li in items(html("/")):
        slug = li.a["href"].strip("/").split("/")[-1]
        assert li.select_one(".site-name")["style"] == f"view-transition-name: site-{slug}"


def test_facts_are_in_the_link_and_revealable(html):
    li = items(html("/sites/"))[0]
    assert li.has_attr("data-reveal")
    assert "Subsurface irrigation" in li.select_one(".reveal").get_text()


def test_break_is_labelled(html):
    assert "7,000 km" in html("/sites/").select_one(".transect-break").get_text()


def test_on_home(html):
    assert html("/").select_one("section.transect") is not None
```

`tests/browser/test_transect.py`:

```python
from playwright.sync_api import expect


def test_escape_dismisses_reveal(page, served):
    page.goto(f"{served}/sites/")
    page.locator("ol.transect-sites > li a").first.focus()
    reveal = page.locator("ol.transect-sites > li .reveal").first
    expect(reveal).to_be_visible()
    page.keyboard.press("Escape")
    expect(reveal).to_be_hidden()


def test_reduced_motion_disables_animation(browser, served):
    context = browser.new_context(reduced_motion="reduce")
    page = context.new_page()
    page.goto(f"{served}/sites/")
    name = page.locator(".transect-meridian").evaluate("el => getComputedStyle(el).animationName")
    assert name == "none"
    context.close()
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k transect`
Expected: FAIL (no `section.transect`).

- [ ] **Step 3: Make brick includes headless, then add the transect include**

Upstream v2 does not stop `content/en/bricks/*.md` from publishing as pages (`/bricks/cta/`). `section_map.html` only needs `site.GetPage`, which still works for unrendered pages. Create `content/en/bricks/_index.md`:

```markdown
---
title: Bricks
build:
  render: never
  list: never
cascade:
  build:
    render: never
    list: never
---
```

Add to `tests/test_transect.py`:

```python
def test_brick_includes_not_published(site):
    assert not (site / "bricks").exists()
```

`content/en/bricks/transect.md`:

```markdown
---
title: Transect
---

## From Lieshout to Cape Town

The six sites sit on a narrow band of longitude, from the Dutch sands to the Cape flats. The north has only recently met drought; the south has managed recharge for decades. Moving knowledge along this line is the point of the project.
```

- [ ] **Step 4: The brick**

`layouts/_partials/sections/transect.html`:

```go-html-template
{{- /*
  Brick: transect — the sites on a meridian, placed by latitude (spec §6.1).
  Placed with `---.transect` (empty section → includes content/en/bricks/transect.md).
  Positions are unitless percentages of the plot height; CSS turns them into lengths.
  @context {dict} . Content, Name, Index, Page
*/ -}}
{{- $label := partial "section_label.html" .Content -}}
{{- $sites := partial "sites-by-latitude.html" .Page -}}
{{- $prevLabel := -100.0 -}}
<section class="transect"{{ with $label }} aria-labelledby="{{ . }}"{{ end }}>
  <div class="container">
    <div class="transect-intro">{{ .Content }}</div>
    <figure class="transect-figure">
      <div class="transect-meridian" aria-hidden="true"></div>
      <p class="transect-break"><span>≈ 7,000 km</span></p>
      <ul class="transect-ticks" aria-hidden="true">
        {{- range slice 50 45 40 35 -}}
          <li style="--y: {{ add 2.0 (mul (sub 53.0 .) (div 66.0 18.0)) }}">{{ . }}°N</li>
        {{- end -}}
        <li style="--y: 84">33°S</li><li style="--y: 98">35°S</li>
      </ul>
      <ol class="transect-sites">
        {{- range $i, $p := $sites -}}
          {{- $lat := float (index (index $p.Params.coordinates 0) 0) -}}
          {{- $dot := 0.0 -}}
          {{- if ge $lat 0.0 -}}
            {{- $dot = add 2.0 (mul (sub 53.0 $lat) (div 66.0 18.0)) -}}
          {{- else -}}
            {{- $dot = add 84.0 (mul (sub -33.0 $lat) 7.0) -}}
          {{- end -}}
          {{- $lab := math.Max $dot (add $prevLabel 11.0) -}}
          {{- $prevLabel = $lab -}}
          {{- $slug := $p.File.ContentBaseName -}}
          <li data-reveal style="--dot: {{ printf "%.4f" $dot }}; --label: {{ printf "%.4f" $lab }}; --i: {{ $i }}">
            <span class="dot" aria-hidden="true"></span>
            <span class="leader" aria-hidden="true"></span>
            <a href="{{ $p.RelPermalink }}">
              <span class="site-name" style="view-transition-name: site-{{ $slug }}">{{ $p.Title }}</span>
              <span class="site-meta">{{ $p.Params.country }}, {{ lower $p.Params.climate }}</span>
              <span class="reveal">{{ $p.Params.mar_system }}. Source water: {{ lower $p.Params.source_water }}.</span>
            </a>
          </li>
        {{- end -}}
      </ol>
      <figcaption class="visually-hidden">Case-study sites from north to south by latitude. The comparison table on the Case studies page lists the same facts.</figcaption>
    </figure>
  </div>
</section>
```

- [ ] **Step 5: CSS**

`static/css/sections/transect.css`:

```css
/* -- brick: transect (spec §6.1) ----------------------------------------- */
section.transect { background: var(--porewater); padding-block: var(--brick-space); }
section.transect .container { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr); gap: 3rem; align-items: start; }
@media (width < 52rem) { section.transect .container { grid-template-columns: 1fr; } }

.transect-figure { --h: 46rem; --x: 4.5rem; position: relative; height: var(--h); margin: 0; view-timeline-name: --transect; }
.transect-meridian { position: absolute; left: var(--x); top: 2%; bottom: 2%; width: 2px; background: var(--flow); }
.transect-break {
    position: absolute; left: 0; right: 0; top: 68%; height: 12%; margin: 0;
    display: flex; align-items: center; padding-inline-start: calc(var(--x) + 1rem);
    background: var(--porewater); font-family: var(--fontTitles); font-size: 0.9rem; color: var(--textMedium);
}
.transect-break::before, .transect-break::after {
    content: ""; position: absolute; left: calc(var(--x) - 0.6rem); width: 1.2rem; height: 1px; background: var(--borderMedium);
}
.transect-break::before { top: 0; } .transect-break::after { bottom: 0; }
.transect-ticks { list-style: none; margin: 0; padding: 0; }
.transect-ticks li {
    position: absolute; left: 0; top: calc(var(--y) * 1%); width: calc(var(--x) - 0.5rem);
    translate: 0 -50%; font-size: 0.8rem; color: var(--textMedium); text-align: end;
    font-variant-numeric: tabular-nums; padding-inline-end: 0.5rem;
    border-block-end: 1px solid var(--borderLight);
}
.transect-sites { list-style: none; margin: 0; padding: 0; }
.transect-sites .dot {
    position: absolute; left: calc(var(--x) - 5px); top: calc(var(--dot) * 1%); translate: 0 -50%;
    width: 12px; height: 12px; border-radius: 50%; background: var(--flow);
    box-shadow: 0 0 0 2px var(--surface-ring); z-index: 1;
}
.transect-sites .leader {
    position: absolute; left: calc(var(--x) + 0.5rem); width: 1rem;
    top: calc(min(var(--dot), var(--label)) * 1%);
    height: calc(max(var(--dot), var(--label)) * 1% - min(var(--dot), var(--label)) * 1%);
    border-inline-start: 1px solid var(--borderMedium);
}
.transect-sites a {
    position: absolute; left: calc(var(--x) + 1.5rem); right: 0; top: calc(var(--label) * 1%);
    translate: 0 -0.8rem; display: flex; flex-direction: column; min-height: 2.75rem;
    padding: 0.2rem 0.5rem; border-radius: var(--radius-s); text-decoration: none; color: var(--aquifer);
}
.transect-sites a:hover .site-name { text-decoration: underline; }
.site-name { font-family: var(--fontTitles); font-weight: 650; }
.site-meta { font-size: 0.9rem; color: var(--textMedium); }
.transect-sites .reveal {
    margin-block-start: 0.35rem; padding: 0.5rem 0.75rem; max-width: 34ch;
    background: var(--page); border: 1px solid var(--borderMedium); border-radius: var(--radius-s); font-size: 0.9rem;
}
.transect-sites li:is(:hover, :focus-within) a { z-index: 2; }

@media (forced-colors: active) {
    .transect-meridian, .transect-sites .dot { forced-color-adjust: none; background: CanvasText; }
}

@media (prefers-reduced-motion: no-preference) {
    @supports ((animation-timeline: scroll()) and (animation-range: 0% 100%)) {
        .transect-meridian {
            transform-origin: top; animation: transect-draw linear both;
            animation-timeline: --transect; animation-range: entry 10% cover 40%;
        }
        .transect-sites li > * {
            animation: transect-site linear both; animation-timeline: --transect;
            animation-range: entry calc(12% + var(--i) * 4%) cover calc(22% + var(--i) * 4%);
        }
    }
}
@keyframes transect-draw { from { scale: 1 0; } to { scale: 1 1; } }
@keyframes transect-site { from { opacity: 0; } to { opacity: 1; } }
```

- [ ] **Step 6: Escape dismissal in `static/js/site.js`**

Insert before the final `})();`:

```js
    /* -- in-place reveals ----------------------------------------------
       [data-reveal] hosts show their .reveal on hover or focus (CSS).
       Escape hides it without moving the pointer or focus (WCAG 1.4.13);
       leaving the host re-arms it. */
    document.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") return;
        Array.prototype.forEach.call(
            document.querySelectorAll("[data-reveal]:hover, [data-reveal]:focus-within"),
            function (host) { host.classList.add("dismissed"); }
        );
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-reveal]"), function (host) {
        host.addEventListener("pointerleave", function () { host.classList.remove("dismissed"); });
        host.addEventListener("focusout", function () { host.classList.remove("dismissed"); });
    });
```

- [ ] **Step 7: Put it on Home**

Append to `content/en/_index.md`:

```markdown

---.transect

---
```

(An empty named section pulls in `content/en/bricks/transect.md`. The trailing `---` closes it. Task 8 adds it to Case studies.)

- [ ] **Step 8: Add to the Case studies page**

Append to `content/en/sites/_index.md`:

```markdown

---.transect

---
```

- [ ] **Step 9: Run tests**

Run: `pixi run test && pixi run test-browser -k transect`
Expected: all pass.

- [ ] **Step 10: Look at it**

Run `pixi run dev`. With Playwright (`browser_navigate` http://localhost:1313/sites/, `browser_resize` 375×800 then 1280×900, `browser_take_screenshot`), check:
- no label overlaps
- leaders join each label to its dot
- the break band sits between Tunisia and the Cape
- the reveal box doesn't cover the next label's name when hovered

Adjust `--h`, the 11% gap or the reveal width if needed. If you change the gap, update the expected table.

- [ ] **Step 11: Log and commit**

Append to "Changes vs upstream" in `CLAUDE.md`: `` - `static/js/site.js`: Escape dismissal for `[data-reveal]` hosts. ``

```bash
git add layouts/_partials/sections/transect.html static/css/sections/transect.css content/en/bricks/transect.md content/en/_index.md content/en/sites/_index.md static/js/site.js tests/test_transect.py tests/browser/test_transect.py CLAUDE.md
git commit -m "Add the north-south transect brick on Home and Case studies"
```

---

### Task 8: Site comparison table and the shared data-table component

**Guide to retrieve first:** `responsive-table`.

**Files:**
- Create: `layouts/_partials/sections/sitecompare.html`, `content/en/bricks/sitecompare.md`, `tests/test_sitecompare.py`
- Modify: `static/css/aquicirc.css` (the `.datatable` component), `content/en/sites/_index.md`

**Interfaces:**
- Produces the table component markup convention (reused in Task 12):

```html
<div class="datatable-frame" role="region" aria-labelledby="<caption-id>" tabindex="0">
  <table class="datatable">
    <caption id="<caption-id>">…</caption>
    <thead><tr><th scope="col">…</th>…</tr></thead>
    <tbody><tr><th scope="row">…</th><td><span class="cell-label" aria-hidden="true">Column name</span>…</td>…</tr></tbody>
  </table>
</div>
```

- [ ] **Step 1: Write the failing test**

`tests/test_sitecompare.py`:

```python
def test_compare_table_semantics(html):
    table = html("/sites/").select_one("section.sitecompare table.datatable")
    assert table.caption.get_text(strip=True) == "The six case-study sites compared"
    headers = [th.get_text(strip=True) for th in table.thead.find_all("th")]
    assert headers == ["Site", "Country", "Climate", "Aquifer", "MAR system", "Expected contaminants"]
    rows = table.tbody.find_all("tr")
    assert len(rows) == 6
    assert rows[0].th["scope"] == "row" and rows[0].th.a["href"] == "/sites/lieshout/"
    frame = table.find_parent("div", class_="datatable-frame")
    assert frame["role"] == "region" and frame["tabindex"] == "0"
    assert frame["aria-labelledby"] == table.caption["id"]


def test_stacked_labels_are_dom_text(html):
    cell = html("/sites/").select_one("table.datatable tbody td")
    assert cell.select_one(".cell-label").get_text(strip=True) == "Country"
```

- [ ] **Step 2: Run to see it fail**

Run: `pixi run test -k sitecompare`
Expected: FAIL.

- [ ] **Step 3: Brick, include and page**

`content/en/bricks/sitecompare.md`:

```markdown
---
title: Compare the sites
---

## Compare the sites
```

`layouts/_partials/sections/sitecompare.html`:

```go-html-template
{{- /* Brick: sitecompare — proposal Table 1 from site front matter (spec §6.5). */ -}}
{{- $label := partial "section_label.html" .Content -}}
{{- $sites := partial "sites-by-latitude.html" .Page -}}
{{- $cols := slice "Country" "Climate" "Aquifer" "MAR system" "Expected contaminants" -}}
<section class="sitecompare"{{ with $label }} aria-labelledby="{{ . }}"{{ end }}>
  <div class="container">
    {{ .Content }}
    <div class="datatable-frame" role="region" aria-labelledby="sitecompare-caption" tabindex="0">
      <table class="datatable">
        <caption id="sitecompare-caption">The six case-study sites compared</caption>
        <thead><tr><th scope="col">Site</th>{{ range $cols }}<th scope="col">{{ . }}</th>{{ end }}</tr></thead>
        <tbody>
          {{- range $sites -}}
          {{- $vals := slice .Params.country .Params.climate .Params.aquifer .Params.mar_system (delimit (.Params.expected_cecs | default slice) ", ") -}}
          <tr>
            <th scope="row"><a href="{{ .RelPermalink }}">{{ .Title }}</a></th>
            {{- range $i, $v := $vals -}}
            <td><span class="cell-label" aria-hidden="true">{{ index $cols $i }}</span>{{ $v }}</td>
            {{- end -}}
          </tr>
          {{- end -}}
        </tbody>
      </table>
    </div>
  </div>
</section>
```

Append to `content/en/sites/_index.md`:

```markdown

---.sitecompare

---
```

- [ ] **Step 4: Table CSS (append to `static/css/aquicirc.css`)**

```css
/* Data tables: sticky headers; stacked cards when the frame is narrow (guide responsive-table). */
.datatable-frame { container-type: inline-size; overflow: auto; max-height: 80vh; border: 1px solid var(--borderLight); border-radius: var(--radius-s); }
.datatable { border-collapse: separate; border-spacing: 0; width: 100%; font-size: 0.95rem; }
.datatable caption { text-align: start; font-family: var(--fontTitles); font-weight: 600; padding: 0.75rem 1rem; }
.datatable th, .datatable td { text-align: start; vertical-align: top; padding: 0.6rem 1rem; border-block-end: 1px solid var(--borderLight); }
.datatable thead th { position: sticky; top: 0; z-index: 2; background: var(--page); font-family: var(--fontTitles); }
.datatable tbody th { position: sticky; inset-inline-start: 0; z-index: 1; background: var(--page); font-family: var(--fontTitles); font-weight: 600; }
.datatable .cell-label { display: none; }
@container (width < 600px) {
    .datatable thead { display: none; }
    .datatable, .datatable tbody, .datatable tr, .datatable th, .datatable td { display: block; }
    .datatable tr { padding-block: 0.5rem; border-block-end: 1px solid var(--borderMedium); }
    .datatable tbody th { position: sticky; top: 0; border: 0; }
    .datatable td { border: 0; padding-block: 0.2rem; }
    .datatable .cell-label { display: block; font-family: var(--fontTitles); font-size: 0.8rem; color: var(--textMedium); }
}
```

- [ ] **Step 5: Run tests and commit**

Run: `pixi run test`
Expected: all pass.

```bash
git add layouts/_partials/sections/sitecompare.html content/en/bricks/sitecompare.md content/en/sites/_index.md static/css/aquicirc.css tests/test_sitecompare.py
git commit -m "Add the site comparison table and the shared data-table component"
```

---

### Task 9: Consortium page: partners brick, team filter, partner strip

**Files:**
- Create: `layouts/_partials/sections/partners.html`, `static/css/sections/partners.css`, `content/en/bricks/partners.md`, `content/en/consortium.md`, `layouts/_shortcodes/partnerstrip.html`, `tests/test_consortium.py`
- Modify: `layouts/_shortcodes/team.html`, `content/en/_index.md`, `CLAUDE.md`

**Interfaces:**
- Consumes: `$d.partners`, `$d.people` (Task 3).
- Produces:
  - anchors `id="partner-<id>"` (the Task 5 site pages link to them)
  - `{{< team group="advisory|team" >}}`
  - `{{< partnerstrip >}}`

- [ ] **Step 1: Write the failing tests**

`tests/test_consortium.py`:

```python
def test_partners_grouped_coordinator_country_first(html):
    groups = html("/consortium/").select("section.partners .country")
    names = [g.find("h3").get_text(strip=True) for g in groups]
    assert names[0] == "Netherlands"
    assert names[1:] == sorted(names[1:])


def test_partner_anchor_and_role(html):
    doc = html("/consortium/")
    wu = doc.select_one("#partner-wu")
    assert "Coordinator" in wu.get_text()
    assert doc.select_one("#partner-su") is not None


def test_team_group_filter(html):
    doc = html("/consortium/")
    advisory = doc.select_one("section:has(h2#advisory) ul.team")
    assert [h.get_text(strip=True) for h in advisory.select("h3")] == ["Ricky Murray", "Sarah Garré"]


def test_team_empty_state(html):
    assert html("/consortium/").select_one("section:has(h2#team) .empty")


def test_partner_strip_on_home(html):
    strip = html("/").select_one("ul.partnerstrip")
    assert len(strip.find_all("li")) == 10
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k consortium`
Expected: FAIL.

- [ ] **Step 3: Team `group` filter + empty state**

In `layouts/_shortcodes/team.html`, replace `{{- with $d.people -}}` (and its matching `{{- end -}}` at the bottom) with:

```go-html-template
{{- $people := $d.people | default slice -}}
{{- with .Get "group" -}}{{- $people = where $people "group" . -}}{{- end -}}
{{- if not $people -}}
<p class="empty">Profiles will appear here as partners confirm them.</p>
{{- else -}}
{{- with $people -}}
```

and close with `{{- end -}}{{- end -}}`.

The section keeps its heading. Because `ul.team` is absent when the list is empty, the section routes to `wide`, which is fine.

- [ ] **Step 4: Partners brick**

`content/en/bricks/partners.md`:

```markdown
---
title: Partners
---

## Partners
```

`layouts/_partials/sections/partners.html`:

```go-html-template
{{- /* Brick: partners — grouped by country, coordinator's country first (spec §6.5). */ -}}
{{- $label := partial "section_label.html" .Content -}}
{{- $d := partial "data.html" .Page -}}
{{- $partners := $d.partners -}}
{{- $coord := index (where $partners "role" "coordinator") 0 -}}
{{- $countries := slice -}}
{{- range $partners -}}{{- $countries = $countries | append .country -}}{{- end -}}
{{- $countries = sort (uniq $countries) -}}
{{- $ordered := slice $coord.country -}}
{{- range $countries -}}{{- if ne . $coord.country -}}{{- $ordered = $ordered | append . -}}{{- end -}}{{- end -}}
{{- $roles := dict "coordinator" "Coordinator" "wp-lead" "Work package lead" "partner" "Partner" -}}
<section class="partners"{{ with $label }} aria-labelledby="{{ . }}"{{ end }}>
  <div class="container">
    {{ .Content }}
    {{- range $country := $ordered -}}
    <div class="country">
      <h3>{{ $country }}</h3>
      <ul>
        {{- range where $partners "country" $country -}}
        <li id="partner-{{ .id }}">
          {{ with .logo }}<img src="{{ . }}" alt="" height="48" loading="lazy">{{ end }}
          <p class="partner-name">{{ with .url }}<a href="{{ . }}" rel="noopener">{{ end }}{{ .name }}{{ with .url }}</a>{{ end }}</p>
          <p class="partner-role">{{ index $roles .role }}{{ with .wps }}, {{ delimit . ", " }}{{ end }}</p>
        </li>
        {{- end -}}
      </ul>
    </div>
    {{- end -}}
  </div>
</section>
```

`static/css/sections/partners.css`:

```css
/* -- brick: partners ----------------------------------------------------- */
section.partners { padding-block: var(--brick-space); }
section.partners .country { margin-block-start: 2rem; }
section.partners .country h3 { margin-block: 0 0.75rem; font-size: 1rem; color: var(--textMedium); }
section.partners ul { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr)); gap: 1rem; }
section.partners li { border: 1px solid var(--borderLight); border-radius: var(--radius-s); padding: 1rem; scroll-margin-top: 6rem; }
section.partners li:target { border-color: var(--flow); box-shadow: inset 0 0 0 1px var(--flow); }
section.partners img { height: 3rem; width: auto; margin-block-end: 0.5rem; }
.partner-name { font-family: var(--fontTitles); font-weight: 600; margin: 0; }
.partner-role { font-size: 0.9rem; color: var(--textMedium); margin: 0.25rem 0 0; }
ul.partnerstrip { list-style: none; padding: 0; display: flex; flex-wrap: wrap; gap: 0.75rem 1.5rem; }
ul.partnerstrip li { font-family: var(--fontTitles); font-size: 0.95rem; }
ul.partnerstrip img { height: 2.5rem; width: auto; filter: grayscale(1); }
ul.partnerstrip a:is(:hover, :focus-visible) img { filter: none; }
```

`layouts/_shortcodes/partnerstrip.html`:

```go-html-template
{{- /* All partners as a static strip (logo when present, else short name). */ -}}
{{- $d := partial "data.html" .Page -}}
<ul class="partnerstrip">
  {{- range $p := $d.partners -}}
  <li><a href="/consortium/#partner-{{ $p.id }}">{{ with $p.logo }}<img src="{{ . }}" alt="{{ $p.name }}" height="40" loading="lazy">{{ else }}{{ $p.short }}{{ end }}</a></li>
  {{- end -}}
</ul>
```

- [ ] **Step 5: Consortium page and Home strip**

`content/en/consortium.md`:

```markdown
---
title: Consortium
---

# Who does the work

Ten institutions in six countries share the six sites, the monitoring, the models and the workshops. Wageningen University & Research coordinates.

---.partners

---

## Team {#team}

{{< team group="team" >}}

---

## Advisory board {#advisory}

Two independent experts, one from Africa and one from Europe, attend the plenary meetings and review the project's direction.

{{< team group="advisory" >}}
```

Goldmark heading attributes (`{#team}`) are on by default, so the `<h2>` carries the id the tests select.

Append to `content/en/_index.md`:

```markdown

---

## Partners

{{< partnerstrip >}}
```

- [ ] **Step 6: Run tests, log, commit**

Run: `pixi run test`
Expected: all pass.

Append to "Changes vs upstream" in `CLAUDE.md`: `` - `layouts/_shortcodes/team.html`: optional `group` filter and empty state. ``

```bash
git add layouts content/en/consortium.md content/en/bricks/partners.md content/en/_index.md static/css/sections/partners.css tests/test_consortium.py CLAUDE.md
git commit -m "Add Consortium page: partners by country, team and advisory board; partner strip on Home"
```

---

### Task 10: News section

**Files:**
- Create: `content/en/posts/_index.md`, `content/en/posts/2026-10-06-website-launched.md`, `tests/test_news.py`
- Modify: `hugo.yaml` (permalinks), `layouts/_shortcodes/blog.html` (limit), `layouts/_partials/sections/post.html` (tag links, alt, errorf), `content/en/_index.md`, `CLAUDE.md`

**Interfaces:**
- Consumes: post front matter (spec §5).
- Produces: `/news/` list and `/news/<slug>/` posts; `{{< blog limit="3" >}}`.

- [ ] **Step 1: Write the failing tests**

`tests/test_news.py`:

```python
def test_news_lives_at_news(html, site):
    assert html("/news/").find("ul", class_="posts")
    assert (site / "news/website-launched/index.html").exists()
    assert not (site / "posts").exists()


def test_tag_links_point_to_news(html):
    links = [a["href"] for a in html("/news/website-launched/").select(".post .meta .tags a")]
    assert links and all(h.startswith("/news/?tag=") for h in links)


def test_home_shows_at_most_three_without_filter(html):
    section = html("/").select_one("section.posts")
    assert len(section.select("ul.posts > li")) <= 3
    assert section.select_one("form.filter") is None


def test_post_with_site_shows_on_site_page(html):
    items = [a.get_text(strip=True) for a in html("/sites/kinrooi/").select(".sitenews-list a")]
    assert "The AQUICIRC website is live" in items


def test_post_image_without_alt_fails(build_variant):
    def break_it(root):
        p = root / "content/en/posts/2026-10-06-website-launched.md"
        p.write_text(p.read_text().replace("title:", "image: /uploads/x.jpg\ntitle:", 1))
    result = build_variant(break_it)
    assert result.returncode != 0 and "image_alt" in result.stderr
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k news`
Expected: FAIL.

- [ ] **Step 3: Permalinks**

Add to `hugo.yaml` (top level):

```yaml
permalinks:
  page:
    posts: /news/:slug/
  section:
    posts: /news/
```

- [ ] **Step 4: `blog` limit**

In `layouts/_shortcodes/blog.html`, directly after the `$posts := sort …` line, add:

```go-html-template
{{- $limit := int (.Get "limit" | default 0) -}}
{{- if $limit -}}{{- $posts = first $limit $posts -}}{{- end -}}
```

Wrap the `<form class="filter">…</form>` block in `{{- if not $limit -}} … {{- end -}}`. Change the teaser call to:

```go-html-template
{{- partial "teaser_list.html" (dict "Pages" . "Dates" true "PageSize" (cond (gt $limit 0) 0 hugo.Data.settings.page_size)) -}}
{{- if not $limit -}}<p class="loadmore"><button type="button" class="button secondary ghost smaller" hidden>{{ i18n "Load more posts" }}…</button></p>{{- end -}}
```

After the closing `{{- end -}}` of `with $posts`, add the empty state: `{{- if not $posts -}}<p class="empty">No news yet.</p>{{- end -}}`.

- [ ] **Step 5: `post` brick fixes**

In `layouts/_partials/sections/post.html`:
- Change `{{ "blog/" | relLangURL }}` to `{{ "news/" | relLangURL }}`.
- Replace `alt=""` on the featured image with `alt="{{ $page.Params.image_alt }}"`.
- Directly after `{{- $page := .Page -}}` add:

```go-html-template
{{- if and $page.Params.image (not $page.Params.image_alt) -}}
  {{- errorf "post %q has an image but no image_alt" $page.File.Path -}}
{{- end -}}
```

- [ ] **Step 6: Content**

`content/en/posts/_index.md`:

```markdown
---
title: News
---

# News

Updates from the sites, the workshops and the lab.

{{< blog >}}
```

`content/en/posts/2026-10-06-website-launched.md`:

```markdown
---
title: The AQUICIRC website is live
slug: website-launched
date: 2026-10-06
tags: [Project]
sites: [kinrooi, lieshout, besos, llobregat, wadi-khairat, cape-town]
wps: [WP6]
---

The project website, deliverable D6.3, is online at aquicirc.eu. It will carry updates from the six case-study sites, the stakeholder workshops, and every publication, dataset and model the project releases.
```

In `content/en/_index.md`, insert this block immediately before the `---` line that precedes `## Partners`, so Home reads hero, objectives, transect, latest news, partners (spec §4):

```markdown

---

## Latest news

{{< blog limit="3" >}}
```

- [ ] **Step 7: Run tests, log, commit**

Run: `pixi run test`
Expected: all pass, including `test_posts_reference_real_sites` from Task 3.

Append to "Changes vs upstream" in `CLAUDE.md`:

```markdown
- `layouts/_shortcodes/blog.html`: `limit` parameter (no filter, no paging) and empty state.
- `layouts/_partials/sections/post.html`: tag links to `/news/`, featured image uses `image_alt`, build fails without it.
- `hugo.yaml`: posts published under `/news/`.
```

```bash
git add hugo.yaml layouts content/en/posts content/en/_index.md tests/test_news.py CLAUDE.md
git commit -m "Add News at /news/ with the launch post; latest three on Home"
```

---

### Task 11: About page: work packages and timeline

**Guides to retrieve first:** `search-hidden-content`, `animate-element-entry-exit`, `html` (the `::details-content` rule).

**Files:**
- Create: `layouts/_partials/quarter.html`, `layouts/_partials/quarter-index.html`, `layouts/_partials/wp-item.html`, `layouts/_partials/sections/workpackages.html`, `layouts/_partials/sections/timeline.html`, `static/css/sections/workpackages.css`, `static/css/sections/timeline.css`, `content/en/bricks/workpackages.md`, `content/en/bricks/timeline.md`, `content/en/about.md`, `tests/test_about.py`, `tests/browser/test_timeline.py`
- Modify: `static/js/site.js` (today marker)

**Interfaces:**
- Consumes: `$d.workpackages`, `$d.deliverables`, `$d.partners`, `hugo.Data.project`; the reveal convention and Escape JS (Tasks 2, 7).
- Produces:
  - `partial "quarter.html" "Y1Q2"` → `"Q2 2026"`
  - `partial "quarter-index.html" "Y1Q2"` → `1` (0-based quarter index, int)
  - WP anchors `id="wp-WP1"` … `id="wp-WP6"`.

- [ ] **Step 1: Write the failing tests**

`tests/test_about.py`:

```python
def test_workpackages_flow(html):
    doc = html("/about/")
    seq = [d["id"] for d in doc.select("section.workpackages ol.wp-sequence details")]
    assert seq == ["wp-WP2", "wp-WP3", "wp-WP4", "wp-WP5"]
    spans = [d["id"] for d in doc.select("section.workpackages details.wp-span")]
    assert spans == ["wp-WP1", "wp-WP6"]
    assert all(not d.has_attr("name") for d in doc.select("section.workpackages details"))


def test_wp_details_list_tasks_and_deliverables(html):
    wp3 = html("/about/").select_one("#wp-WP3")
    text = wp3.get_text(" ", strip=True)
    assert "T3.1" in text and "Q2 2026" in text and "D3.3" in text
    assert "Lead: IoT, VUB" in wp3.summary.get_text(" ", strip=True)


def test_timeline_bars_positions(html):
    bars = html("/about/").select("section.timeline a.bar")
    t31 = next(b for b in bars if "T3.1" in b.get_text())
    assert "grid-column: 3 / 8" in t31["style"]    # Y1Q2 (index 1) → col 3; Y2Q2 (index 5) → end col 8
    assert t31["href"] == "#wp-WP3"
    assert t31.has_attr("data-reveal")


def test_timeline_milestones_and_today(html):
    doc = html("/about/")
    assert len(doc.select("section.timeline a.milestone")) == 19
    today = doc.select_one("section.timeline .today")
    assert today.has_attr("hidden") and today["data-start"] == "2026-01-01" and today["data-months"] == "36"


def test_timeline_frame_is_keyboard_scrollable(html):
    frame = html("/about/").select_one("section.timeline .timeline-frame")
    assert frame["role"] == "region" and frame["tabindex"] == "0" and frame.get("aria-labelledby")
```

`tests/browser/test_timeline.py`:

```python
def test_today_marker_placed(page, served):
    page.clock.set_fixed_time("2026-10-06T12:00:00")
    page.goto(f"{served}/about/")
    today = page.locator("section.timeline .today")
    assert today.is_visible()
    value = float(today.evaluate("el => el.style.getPropertyValue('--today')"))
    assert 0.25 < value < 0.27     # 9 of 36 months


def test_today_hidden_after_project(page, served):
    page.clock.set_fixed_time("2030-01-01T12:00:00")
    page.goto(f"{served}/about/")
    assert not page.locator("section.timeline .today").is_visible()
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k about`
Expected: FAIL.

- [ ] **Step 3: Quarter partials**

`layouts/_partials/quarter-index.html`:

```go-html-template
{{- /* "Y2Q3" → 6 (0-based quarter index from project start). */ -}}
{{- $y := int (substr . 1 1) -}}{{- $q := int (substr . 3 1) -}}
{{- return add (mul (sub $y 1) 4) (sub $q 1) -}}
```

`layouts/_partials/quarter.html`:

```go-html-template
{{- /* "Y2Q3" → "Q3 2027", from data/project.yaml start year. */ -}}
{{- $start := time.AsTime hugo.Data.project.start -}}
{{- $y := int (substr . 1 1) -}}
{{- return printf "Q%s %d" (substr . 3 1) (add $start.Year (sub $y 1)) -}}
```

- [ ] **Step 4: Work packages brick**

`content/en/bricks/workpackages.md`:

```markdown
---
title: Work packages
---

## How the work is organised

Evaluation and monitoring feed the models; the models guide the changes tested at the sites. Management and knowledge transfer run the whole length of the project.
```

`layouts/_partials/sections/workpackages.html`:

```go-html-template
{{- /* Brick: workpackages — flow WP2→WP5 with WP1 and WP6 spanning (spec §6.2). */ -}}
{{- $label := partial "section_label.html" .Content -}}
{{- $d := partial "data.html" .Page -}}
<section class="workpackages"{{ with $label }} aria-labelledby="{{ . }}"{{ end }}>
  <div class="container">
    {{ .Content }}
    <div class="wp-flow">
      {{- range $d.workpackages -}}
        {{- if eq .id "WP1" -}}{{ partial "wp-item.html" (dict "wp" . "d" $d "span" true) }}{{- end -}}
      {{- end -}}
      <ol class="wp-sequence">
        {{- range $d.workpackages -}}
          {{- if in (slice "WP2" "WP3" "WP4" "WP5") .id -}}<li>{{ partial "wp-item.html" (dict "wp" . "d" $d "span" false) }}</li>{{- end -}}
        {{- end -}}
      </ol>
      {{- range $d.workpackages -}}
        {{- if eq .id "WP6" -}}{{ partial "wp-item.html" (dict "wp" . "d" $d "span" true) }}{{- end -}}
      {{- end -}}
    </div>
  </div>
</section>
```

`layouts/_partials/wp-item.html`:

```go-html-template
{{- /* One work package as <details>. @context dict: wp, d, span */ -}}
{{- $wp := .wp -}}{{- $d := .d -}}
{{- $leads := slice -}}
{{- range $wp.leads -}}{{- $leads = $leads | append (index (where $d.partners "id" .) 0).short -}}{{- end -}}
<details class="wp{{ if .span }} wp-span{{ end }}" id="wp-{{ $wp.id }}">
  <summary>
    <span class="wp-id">{{ $wp.id }}</span>
    <span class="wp-title">{{ $wp.title }}</span>
    <span class="wp-lead">Lead: {{ delimit $leads ", " }}</span>
  </summary>
  <div class="wp-body">
    <p>{{ $wp.summary }}</p>
    <h4>Tasks</h4>
    <ul>{{ range $wp.tasks }}<li><strong>{{ .id }}</strong> {{ .title }}, {{ partial "quarter.html" .start }} to {{ partial "quarter.html" .end }}</li>{{ end }}</ul>
    {{ with where $d.deliverables "wp" $wp.id }}
    <h4>Deliverables</h4>
    <ul>{{ range . }}<li><strong>{{ .id }}</strong> {{ .title }}, due {{ partial "quarter.html" .due }}</li>{{ end }}</ul>
    {{ end }}
  </div>
</details>
```

`static/css/sections/workpackages.css`:

```css
/* -- brick: workpackages (spec §6.2) ------------------------------------- */
section.workpackages { padding-block: var(--brick-space); }
.wp-flow { display: grid; gap: 0.75rem; margin-block-start: 2rem; }
.wp-sequence { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.75rem; }
@media (width < 56rem) { .wp-sequence { grid-template-columns: 1fr; } }
details.wp { border: 1px solid var(--borderMedium); border-radius: var(--radius-s); background: var(--page); }
details.wp-span { background: var(--porewater); }
details.wp > summary { display: grid; gap: 0.15rem; padding: 0.9rem 1rem; cursor: pointer; min-height: 2.75rem; }
.wp-id { font-family: var(--fontTitles); font-weight: 700; color: var(--flow); }
.wp-title { font-family: var(--fontTitles); font-weight: 600; }
.wp-lead { font-size: 0.9rem; color: var(--textMedium); }
.wp-body { padding: 0 1rem 1rem; }
.wp-body h4 { margin-block: 1rem 0.25rem; }
.wp-sequence li:not(:last-child) details.wp { position: relative; }
@media (width >= 56rem) {
    .wp-sequence li:not(:last-child) details.wp::after {
        content: ""; position: absolute; top: 1.4rem; right: -0.75rem; width: 0.75rem; height: 2px; background: var(--flow);
    }
}
@media (prefers-reduced-motion: no-preference) {
    @supports (interpolate-size: allow-keywords) {
        details.wp { interpolate-size: allow-keywords; }
        details.wp::details-content { height: 0; overflow: clip; transition: height 0.25s ease, content-visibility 0.25s; transition-behavior: allow-discrete; }
        details.wp[open]::details-content { height: auto; }
    }
}
```

- [ ] **Step 5: Timeline brick**

`content/en/bricks/timeline.md`:

```markdown
---
title: Timeline
---

## Timeline
```

`layouts/_partials/sections/timeline.html`:

```go-html-template
{{- /* Brick: timeline — 12-quarter Gantt, a row per task grouped by WP (spec §6.3).
       Tasks overlap inside a WP (e.g. T3.1 and T3.2), so each task has its own thin row. */ -}}
{{- $label := partial "section_label.html" .Content -}}
{{- $d := partial "data.html" .Page -}}
{{- $start := time.AsTime hugo.Data.project.start -}}
<section class="timeline"{{ with $label }} aria-labelledby="{{ . }}"{{ end }}>
  <div class="container">
    {{ .Content }}
    <div class="timeline-frame" role="region" aria-labelledby="{{ $label | default "timeline" }}" tabindex="0">
      <div class="timeline-grid">
        <div class="tl-axis" aria-hidden="true">
          {{- range $i := seq 0 2 -}}<span style="grid-column: {{ add 2 (mul $i 4) }} / span 4">{{ add $start.Year $i }}</span>{{- end -}}
        </div>
        {{- range $wp := $d.workpackages -}}
        <p class="tl-wp">{{ $wp.id }} {{ $wp.title }}</p>
        {{- range $t := $wp.tasks -}}
          {{- $s := partial "quarter-index.html" $t.start -}}{{- $e := partial "quarter-index.html" $t.end -}}
          <p class="tl-label">{{ $t.id }}</p>
          <a class="bar" href="#wp-{{ $wp.id }}" data-reveal style="grid-column: {{ add 2 $s }} / {{ add 3 $e }}">
            <span class="reveal">{{ $t.id }} {{ $t.title }}, {{ partial "quarter.html" $t.start }} to {{ partial "quarter.html" $t.end }}</span>
          </a>
        {{- end -}}
        <div class="tl-milestones">
          {{- range where $d.deliverables "wp" $wp.id -}}
            {{- $q := partial "quarter-index.html" .due -}}
            <a class="milestone" href="#wp-{{ $wp.id }}" data-reveal style="grid-column: {{ add 2 $q }}">
              <span class="reveal">{{ .id }} {{ .title }}, due {{ partial "quarter.html" .due }}</span>
            </a>
          {{- end -}}
        </div>
        {{- end -}}
        <div class="today" hidden data-start="{{ $start.Format "2006-01-02" }}" data-months="{{ hugo.Data.project.months }}"><span>Today</span></div>
      </div>
    </div>
  </div>
</section>
```

`static/css/sections/timeline.css`:

```css
/* -- brick: timeline (spec §6.3, dataviz marks) --------------------------- */
section.timeline { padding-block: var(--brick-space); }
.timeline-frame { overflow-x: auto; border: 1px solid var(--borderLight); border-radius: var(--radius-s); }
.timeline-grid {
    --label-w: 9rem; position: relative; min-width: 48rem; display: grid;
    grid-template-columns: var(--label-w) repeat(12, minmax(0, 1fr)); row-gap: 4px; padding: 0.75rem 1rem 1rem 0;
    background-image: linear-gradient(to right, var(--borderLight) 1px, transparent 1px);
    background-size: calc((100% - var(--label-w) - 1rem) / 12) 100%;
    background-position: var(--label-w) 0; background-repeat: repeat-x;
}
.tl-axis { grid-column: 1 / -1; display: grid; grid-template-columns: subgrid; font-family: var(--fontTitles); font-size: 0.85rem; color: var(--textMedium); border-block-end: 1px solid var(--borderMedium); }
.tl-wp { grid-column: 1 / -1; margin: 0.75rem 0 0; padding-inline-start: 1rem; font-family: var(--fontTitles); font-weight: 600; font-size: 0.9rem; position: sticky; left: 0; }
.tl-label { grid-column: 1; margin: 0; padding-inline-start: 1rem; font-size: 0.8rem; color: var(--textMedium); position: sticky; left: 0; background: var(--page); z-index: 1; }
a.bar { position: relative; align-self: center; height: 12px; background: var(--flow); border-radius: 4px; margin-inline: 1px; min-height: 12px; }
a.bar::before { content: ""; position: absolute; inset: -6px 0; }   /* 24px hit target */
.tl-milestones { grid-column: 1 / -1; display: grid; grid-template-columns: subgrid; height: 1.5rem; }
a.milestone { grid-row: 1; justify-self: center; align-self: center; width: 10px; height: 10px; rotate: 45deg; background: var(--aquifer); box-shadow: 0 0 0 2px var(--surface-ring); position: relative; }
a.milestone::before { content: ""; position: absolute; inset: -7px; }
:is(a.bar, a.milestone) .reveal {
    position: absolute; top: calc(100% + 6px); left: 0; z-index: 3; width: max-content; max-width: 26ch;
    background: var(--page); color: var(--aquifer); border: 1px solid var(--borderMedium); border-radius: var(--radius-s);
    padding: 0.4rem 0.6rem; font-size: 0.85rem; rotate: 0deg;
}
a.milestone .reveal { rotate: -45deg; transform-origin: top left; }
:is(a.bar, a.milestone):not(:hover, :focus-visible) .reveal { /* keep the name for screen readers */
    clip-path: inset(50%); width: 1px; height: 1px; overflow: hidden; white-space: nowrap; visibility: visible; opacity: 1; padding: 0; border: 0;
}
.today { position: absolute; top: 0; bottom: 0; left: calc(var(--label-w) + (100% - var(--label-w) - 1rem) * var(--today, 0)); width: 1px; background: var(--aquifer); pointer-events: none; }
.today span { position: absolute; top: 0; left: 0.25rem; font-family: var(--fontTitles); font-size: 0.8rem; background: var(--page); padding-inline: 0.25rem; }
@media (forced-colors: active) { a.bar, a.milestone, .today { forced-color-adjust: none; background: CanvasText; } }
```

The milestone row spans every column (`1 / -1`) as a subgrid, so `grid-column: q + 2` puts a diamond in the same column as a bar starting in quarter `q`.

- [ ] **Step 6: Today marker in `static/js/site.js`** (insert before the final `})();`)

```js
    /* -- timeline "today" ----------------------------------------------
       Placed from the visitor's clock so it stays right between builds;
       outside the project period it stays hidden. */
    Array.prototype.forEach.call(document.querySelectorAll(".timeline .today"), function (el) {
        var start = new Date(el.getAttribute("data-start") + "T00:00:00");
        var end = new Date(start);
        end.setMonth(end.getMonth() + Number(el.getAttribute("data-months")));
        var f = (Date.now() - start) / (end - start);
        if (f >= 0 && f <= 1) {
            el.style.setProperty("--today", f.toFixed(4));
            el.hidden = false;
        }
    });
```

- [ ] **Step 7: About page**

`content/en/about.md`:

```markdown
---
title: About
---

# Recharging aquifers with water we used to waste

Managed aquifer recharge puts water back into the ground on purpose, where it is stored and cleaned on its way through the soil. Treated wastewater, industrial effluent and harvested rainwater can all be recharged, but they carry contaminants of emerging concern (pharmaceuticals, pesticides, PFAS) that conventional treatment does not remove and that move easily through groundwater.

AQUICIRC asks how to recharge these waters safely: how much water the aquifer stores and gives back, and how much of each contaminant it removes on the way.

---

## What we set out to do

{{< features >}}

---.workpackages

---

---.timeline

---

## Advisory board

{{< team group="advisory" >}}
```

- [ ] **Step 8: Run tests**

Run: `pixi run test && pixi run test-browser -k timeline`
Expected: all pass.

- [ ] **Step 9: Look at it**

Playwright screenshots of `/about/` at 375 and 1280px. Check:
- bars line up with the year axis
- diamonds sit in their quarter
- the frame scrolls on 375 with labels pinned
- a focused bar shows its reveal, and Escape hides it

A diamond that is not inside its quarter means the subgrid is not applying; check `.tl-milestones` spans `1 / -1`.

- [ ] **Step 10: Log and commit**

Append to "Changes vs upstream" in `CLAUDE.md`: `` - `static/js/site.js`: timeline "today" marker. ``

```bash
git add layouts content/en/about.md content/en/bricks static/css/sections static/js/site.js tests CLAUDE.md
git commit -m "Add About page with work-package flow and the project timeline"
```

---

### Task 12: Outputs page and tabs that search can open

**Guide to retrieve first:** `search-hidden-content`.

**Files:**
- Create: `layouts/_shortcodes/publications.html`, `layouts/_shortcodes/deliverables.html`, `layouts/_shortcodes/datasets.html`, `content/en/outputs.md`, `tests/test_outputs.py`, `tests/browser/test_tabs.py`
- Modify: `static/js/site.js` (tabs), `static/css/aquicirc.css`, `CLAUDE.md`

**Interfaces:**
- Consumes: the `.datatable` component (Task 8); `$d.deliverables`, `$d.publications`, `$d.datasets`; `partial "quarter.html"` (Task 11).

- [ ] **Step 1: Write the failing tests**

`tests/test_outputs.py`:

```python
def test_outputs_tabs(html):
    tabs = [t.get_text(strip=True) for t in html("/outputs/").select(".tabs [role=tab]")]
    assert tabs == ["Publications", "Deliverables", "Data & models", "Media"]


def test_deliverables_table(html):
    table = html("/outputs/").select_one("table.deliverables")
    rows = table.tbody.find_all("tr")
    assert len(rows) == 19
    d63 = next(r for r in rows if r.th.get_text(strip=True) == "D6.3")
    status = d63.select_one(".status")
    assert status.get_text(strip=True) == "Public" and status.svg["aria-hidden"] == "true"
    assert d63.find("a", href="https://aquicirc.eu/")


def test_empty_states(html):
    doc = html("/outputs/")
    assert "No publications yet" in doc.get_text()
    assert "No datasets or models yet" in doc.get_text()
```

`tests/browser/test_tabs.py`:

```python
def test_inactive_panels_are_until_found(page, served):
    page.goto(f"{served}/outputs/")
    hidden = page.locator(".tabs [role=tabpanel]").evaluate_all("els => els.map(e => e.getAttribute('hidden'))")
    assert hidden[0] is None and all(h == "until-found" for h in hidden[1:])


def test_beforematch_selects_tab(page, served):
    page.goto(f"{served}/outputs/")
    page.locator(".tabs [role=tabpanel]").nth(1).evaluate("el => el.dispatchEvent(new Event('beforematch'))")
    assert page.locator(".tabs [role=tab]").nth(1).get_attribute("aria-selected") == "true"


def test_no_js_all_panels_readable(browser, served):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{served}/outputs/")
    assert page.locator(".tabs [role=tabpanel]").evaluate_all("els => els.every(e => e.offsetHeight > 0)")
    context.close()
```

- [ ] **Step 2: Run to see them fail**

Run: `pixi run test -k outputs`
Expected: FAIL.

- [ ] **Step 3: Shortcodes** (no blank lines inside the output, so `markdownify` in `tabs` leaves the HTML intact)

`layouts/_shortcodes/deliverables.html`:

```go-html-template
{{- $d := partial "data.html" .Page -}}
{{- $labels := dict "planned" "Planned" "submitted" "Submitted" "public" "Public" -}}
{{- $icons := dict
      "planned" `<circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="2"/>`
      "submitted" `<circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 2a6 6 0 0 1 0 12z" fill="currentColor"/>`
      "public" `<circle cx="8" cy="8" r="7" fill="currentColor"/>` -}}
<div class="datatable-frame" role="region" aria-labelledby="deliverables-caption" tabindex="0">
<table class="datatable deliverables">
<caption id="deliverables-caption">Deliverables by work package</caption>
<thead><tr><th scope="col">Deliverable</th><th scope="col">Title</th><th scope="col">Work package</th><th scope="col">Due</th><th scope="col">Status</th></tr></thead>
<tbody>
{{- range $d.deliverables -}}
<tr>
<th scope="row">{{ .id }}</th>
<td><span class="cell-label" aria-hidden="true">Title</span>{{ with .url }}<a href="{{ . }}">{{ end }}{{ .title }}{{ with .url }}</a>{{ end }}</td>
<td><span class="cell-label" aria-hidden="true">Work package</span><a href="/about/#wp-{{ .wp }}">{{ .wp }}</a></td>
<td><span class="cell-label" aria-hidden="true">Due</span>{{ partial "quarter.html" .due }}</td>
<td><span class="cell-label" aria-hidden="true">Status</span><span class="status status-{{ .status }}"><svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false">{{ index $icons .status | safeHTML }}</svg>{{ index $labels .status }}</span></td>
</tr>
{{- end -}}
</tbody>
</table>
</div>
```

`layouts/_shortcodes/publications.html`:

```go-html-template
{{- $d := partial "data.html" .Page -}}
{{- with sort ($d.publications | default slice) "year" "desc" -}}
<ol class="publications">
{{- range . -}}
<li>{{ .authors }} ({{ .year }}). <cite>{{ .title }}</cite>. {{ .venue }}.{{ with .doi }} <a href="https://doi.org/{{ . }}">doi:{{ . }}</a>{{ end }}</li>
{{- end -}}
</ol>
{{- else -}}
<p class="empty">No publications yet. The first open-access articles are expected in 2027.</p>
{{- end -}}
```

`layouts/_shortcodes/datasets.html`:

```go-html-template
{{- $d := partial "data.html" .Page -}}
{{- $kinds := dict "data" "Dataset" "model" "Model" "code" "Code" -}}
{{- with $d.datasets -}}
<ul class="datasets">
{{- range . -}}
<li><a href="{{ .url }}">{{ .title }}</a> <span class="kind">{{ index $kinds .kind }}</span><br>{{ .description }}</li>
{{- end -}}
</ul>
{{- else -}}
<p class="empty">No datasets or models yet. Each will be published openly on Zenodo or GitHub as it is released.</p>
{{- end -}}
```

`content/en/outputs.md`:

```markdown
---
title: Outputs
---

# Outputs

Everything AQUICIRC publishes: articles, reports for the funders, and the data and models behind them. All of it is open access.

{{< tabs >}}

## Publications

{{< publications >}}

---

## Deliverables

{{< deliverables >}}

---

## Data & models

{{< datasets >}}

---

## Media

Press coverage, videos and presentations will be listed here.

{{< /tabs >}}
```

Append to `static/css/aquicirc.css`:

```css
.status { display: inline-flex; align-items: center; gap: 0.4rem; }
.status-public { color: var(--flow); }
.publications li, .datasets li { margin-block-end: 0.75rem; }
.datasets .kind { font-size: 0.85rem; color: var(--textMedium); }
```

- [ ] **Step 4: Tabs JS (`static/js/site.js`, inside the tabs block)**

Replace the line `panels[i].hidden = i !== chosen;` with:

```js
                if (i === chosen) panels[i].removeAttribute("hidden");
                else panels[i].setAttribute("hidden", "until-found");
```

and, after the `forEach` that wires the tabs, add:

```js
        Array.prototype.forEach.call(panels, function (panel, i) {
            panel.addEventListener("beforematch", function () { select(i); });
        });
```

- [ ] **Step 5: Run tests**

Run: `pixi run test && pixi run test-browser -k tabs`
Expected: all pass.

- [ ] **Step 6: Log and commit**

Append to "Changes vs upstream" in `CLAUDE.md`: `` - `static/js/site.js`: inactive tab panels use `hidden="until-found"`; `beforematch` selects the tab. ``

```bash
git add layouts/_shortcodes content/en/outputs.md static tests CLAUDE.md
git commit -m "Add Outputs page; tab panels findable by in-page search"
```

---

### Task 13: Locator map (click to load)

**Guides to retrieve first:** `performance` (third-party section). Check that `conditional-async-dependencies` doesn't change the approach.

**Files:**
- Create: `static/vendor/leaflet/leaflet.js`, `static/vendor/leaflet/leaflet.css`, `static/vendor/leaflet/LICENSE`, `static/js/map.js`, `tests/browser/test_map.py`
- Modify: `layouts/sites/page.html` (load `map.js`), `CLAUDE.md`

**Interfaces:**
- Consumes: the `.map-frame[data-map]` markup from Task 5 (`data-points` = JSON `[[lat, lon], …]`, `data-label`, `button[data-map-load]`).

- [ ] **Step 1: Vendor Leaflet**

```bash
mkdir -p static/vendor/leaflet
curl -fsSL -o static/vendor/leaflet/leaflet.js  https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js
curl -fsSL -o static/vendor/leaflet/leaflet.css https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css
curl -fsSL -o static/vendor/leaflet/LICENSE     https://cdn.jsdelivr.net/npm/leaflet@1.9.4/LICENSE
```

- [ ] **Step 2: Write the failing browser tests**

`tests/browser/test_map.py`:

```python
def osm(requests):
    return [r for r in requests if "tile.openstreetmap.org" in r]


def test_no_third_party_before_click(page, served):
    seen = []
    page.on("request", lambda r: seen.append(r.url))
    page.goto(f"{served}/sites/kinrooi/")
    page.wait_for_load_state("networkidle")
    assert not [u for u in seen if not u.startswith(served)]


def test_click_loads_map_and_tiles(page, served):
    seen = []
    page.on("request", lambda r: seen.append(r.url))
    page.goto(f"{served}/sites/kinrooi/")
    page.get_by_role("button", name="Show map").click()
    page.wait_for_selector(".map-frame.loaded .leaflet-container")
    assert osm(seen)


def test_multi_coordinate_site_has_two_markers(page, served):
    page.goto(f"{served}/sites/cape-town/")
    page.get_by_role("button", name="Show map").click()
    page.wait_for_selector(".map-frame.loaded .leaflet-interactive")
    assert page.locator(".map-frame .leaflet-interactive").count() == 2


def test_without_js_link_remains(browser, served):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{served}/sites/kinrooi/")
    assert page.get_by_role("link", name="View GROW pilot, Kinrooi on OpenStreetMap").is_visible()
    assert not page.get_by_role("button", name="Show map").is_visible()
    context.close()
```

- [ ] **Step 3: Run to see them fail**

Run: `pixi run test-browser -k map`
Expected: FAIL (button stays hidden).

- [ ] **Step 4: `static/js/map.js`**

```js
/* Locator map on site pages. Nothing third-party loads until "Show map" is
   pressed; then self-hosted Leaflet draws OpenStreetMap tiles and a circle
   marker per coordinate. Without this file the OpenStreetMap link remains. */
(function () {
    "use strict";
    var frame = document.querySelector(".map-frame[data-map]");
    if (!frame) return;
    var button = frame.querySelector("[data-map-load]");
    button.hidden = false;

    var load = function (tag, attrs) {
        return new Promise(function (resolve, reject) {
            var el = document.createElement(tag);
            Object.keys(attrs).forEach(function (k) { el.setAttribute(k, attrs[k]); });
            el.onload = resolve;
            el.onerror = reject;
            document.head.appendChild(el);
        });
    };

    button.addEventListener("click", function () {
        button.disabled = true;
        button.textContent = "Loading map…";
        Promise.all([
            load("link", { rel: "stylesheet", href: "/vendor/leaflet/leaflet.css" }),
            load("script", { src: "/vendor/leaflet/leaflet.js" })
        ]).then(function () {
            var points = JSON.parse(frame.getAttribute("data-points"));
            frame.textContent = "";
            frame.classList.add("loaded");
            frame.setAttribute("tabindex", "0");
            frame.setAttribute("aria-label", "Map of " + frame.getAttribute("data-label"));
            var map = window.L.map(frame, { scrollWheelZoom: false });
            window.L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 18,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
            var flow = getComputedStyle(document.documentElement).getPropertyValue("--flow").trim() || "#2471A1";
            var markers = points.map(function (p) {
                return window.L.circleMarker(p, { radius: 8, color: "#fff", weight: 2, fillColor: flow, fillOpacity: 1 }).addTo(map);
            });
            map.fitBounds(window.L.featureGroup(markers).getBounds(), { maxZoom: 11, padding: [40, 40] });
            frame.focus();
        }).catch(function () {
            button.disabled = false;
            button.textContent = "Show map";
            var note = document.createElement("p");
            note.textContent = "The map could not be loaded. Use the OpenStreetMap link above instead.";
            frame.appendChild(note);
        });
    });
})();
```

In `layouts/sites/page.html`, at the end of the `locator` section (before `</section>`), add:

```html
  <script src="/js/map.js" defer></script>
```

- [ ] **Step 5: Run tests**

Run: `pixi run test-browser -k map && pixi run test`
Expected: all pass. The tiles test needs network; if it is offline, the request is still attempted and recorded.

- [ ] **Step 6: Log and commit**

Append to `CLAUDE.md` under Stack: `` - Leaflet 1.9.4 vendored in `static/vendor/leaflet/` (BSD-2), loaded only on "Show map". ``

```bash
git add static/vendor static/js/map.js layouts/sites/page.html tests/browser/test_map.py CLAUDE.md
git commit -m "Add click-to-load locator map with self-hosted Leaflet"
```

---

### Task 14: 404, README and content-marker hygiene

**Files:**
- Modify: `content/en/404.md`, `README.md`
- Create: `tests/test_hygiene.py`

- [ ] **Step 1: Write the tests**

`tests/test_hygiene.py`:

```python
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTNER_FILES = [*ROOT.glob("content/en/sites/*.md"), *ROOT.glob("content/en/posts/*.md"), *ROOT.glob("data/en/*.yaml")]


def test_partner_content_has_no_shortcodes_or_dividers():
    for path in PARTNER_FILES:
        text = path.read_text()
        body = text.split("---", 2)[-1] if path.suffix == ".md" else text
        assert "{{<" not in body and "{{%" not in body, path.name
        if path.suffix == ".md":
            assert not re.search(r"^---", body, re.M), f"{path.name} has a body divider"


def test_no_arrows_in_link_text(site):
    for page in site.rglob("index.html"):
        assert not re.search(r">[^<]*→\s*</a>", page.read_text(encoding="utf-8")), page


def test_every_page_one_h1(site):
    from bs4 import BeautifulSoup
    for page in site.rglob("index.html"):
        doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        assert len(doc.find_all("h1")) == 1, page.relative_to(site)


def test_brick_includes_are_not_published(site):
    assert not (site / "bricks").exists()


def test_404_copy(html):
    doc = html("/404.html")
    assert doc.find("h1").get_text(strip=True) == "This page does not exist"
```

- [ ] **Step 2: Run, fix anything they catch, commit**

Run: `pixi run test`
Expected: all pass. A failure points at real copy or markup to fix; fix it in the file named.

Update `README.md`'s "Writing content" section to name the partner-editable files and the rule: "no shortcodes and no `---` in site pages, posts or data files; images need `image_alt`". Then:

```bash
git add tests/test_hygiene.py README.md content/en/404.md
git commit -m "Add hygiene tests (partner content, one h1, no arrow links) and update README"
```

---

### Task 15: Verification pass and launch deploy

**Skills to load:** `chrome-devtools-mcp:a11y-debugging`, `chrome-devtools-mcp:debug-optimize-lcp`, `dataviz` (anti-patterns), `superpowers:verification-before-completion`.

**Files:**
- Create: `tests/browser/test_layout.py`
- Modify: whatever the checks below find

- [ ] **Step 1: No horizontal scroll at 360px (Review Focus 2)**

`tests/browser/test_layout.py`:

```python
import pytest

PAGES = ["/", "/about/", "/sites/", "/sites/cape-town/", "/sites/lieshout/", "/consortium/", "/news/", "/outputs/"]


@pytest.mark.parametrize("path", PAGES)
def test_no_horizontal_scroll_on_small_phone(browser, served, path):
    context = browser.new_context(viewport={"width": 360, "height": 780})
    page = context.new_page()
    page.goto(f"{served}{path}")
    overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    context.close()
    assert overflow <= 0, f"{path} overflows by {overflow}px"
```

Run: `pixi run test-browser`
Expected: all pass. Fix any overflow at its source (usually a long word: add `overflow-wrap: anywhere` to that element).

- [ ] **Step 2: Accessibility audit per page (DevTools MCP, a11y-debugging skill)**

Serve with `pixi run dev`. For each page in `PAGES`:
1. `new_page`, then `lighthouse_audit` (mode `navigation`, `outputDirPath` in the scratchpad). Extract failures with the skill's `node -e` filter.
2. `list_console_messages` with `types: ["issue"]`, `includePreservedMessages: true`.
3. `take_snapshot`: one h1, no skipped levels, landmarks present.
4. Keyboard pass with `press_key` through the menu, transect links, WP summaries, timeline bars, tabs (arrow keys) and "Show map". Focus is always visible and Escape hides reveals.

Expected: Accessibility = 100 and Best Practices = 100 on every page; no console issues. Fix, re-run, commit fixes as `fix(a11y): …`.

- [ ] **Step 3: LCP (debug-optimize-lcp skill) on `/` and `/sites/kinrooi/`**

`emulate` with `networkConditions: "Fast 3G"`, `cpuThrottlingRate: 4`, then `performance_start_trace` (reload, autoStop) and `performance_analyze_insight` for `LCPBreakdown` and `RenderBlocking`.

Expected:
- LCP ≤ 2.5 s, CLS < 0.1
- resource load delay and render delay each < 10% of LCP
- Lighthouse Performance ≥ 95 on mobile

If render delay dominates, check that the Archivo preload is the hero h1's face and nothing else is preloaded.

- [ ] **Step 4: Visual pass (Playwright MCP)**

Screenshots of every page at 375, 768 and 1280px, plus `browser_emulate_media` with `reducedMotion: reduce` on `/` and `/sites/`, plus `forcedColors: active` on `/sites/` and `/about/`. Compare against spec §7. The transect and timeline must pass the dataviz anti-pattern list: no dashed gridlines, no text in mark colour, no tooltip-only values.

- [ ] **Step 5: Full test run and content gate report**

```bash
pixi run test && pixi run test-browser
grep -rn "TODO(content)" content data | wc -l
```

Expected: tests pass. The grep count is the list of owner inputs still open (spec §10). Report it to the owner and don't treat it as a failure. Launch announcement waits until it is 0.

- [ ] **Step 6: Deploy**

```bash
git push
gh run watch "$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')" --exit-status
curl -s https://aquicirc.eu/ | grep -o '<title>[^<]*'
```

Expected: workflow green (tests + build + deploy); title `Home | AQUICIRC`.
