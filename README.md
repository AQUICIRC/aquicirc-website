# AQUICIRC website

Project website for **AQUICIRC — Managed Aquifer Recharge for a circular water future**
(Water4All). Built with [Hugo](https://gohugo.io) and the
[Hugobricks v2](https://github.com/jhvanderschee/hugobricks_v2) starter, deployed to
GitHub Pages on every push to `main`.

## Run locally

```bash
pixi run dev      # http://localhost:1313, with drafts
pixi run build    # production build into public/
```

[pixi](https://pixi.sh) installs the pinned Hugo version; nothing else is needed.

## Writing content

**Files partners edit** (plain Markdown or YAML, nothing else):

| What | Where |
|---|---|
| A news post | `content/en/posts/YYYY-MM-DD-slug.md` (`title`, `date`, `tags`, optional `case_sites`, `wps`, `image` + `image_alt`) |
| A case-study site | `content/en/sites/<slug>.md` (`country`, `coordinates`, `mar_system` … see an existing site) |
| Partners, people, work packages, deliverables, publications, datasets | `data/en/*.yaml` |

Rules for those files: no shortcodes (`{{< … >}}`) and no `---` dividers in the text, and
every image needs `image_alt`. The build fails, with a message naming the file, when a site
page misses a required field or an image has no alt text. `pixi run test` checks ids and
cross-references.

**Structural pages** (`content/en/_index.md`, `about.md`, `consortium.md`, `outputs.md`,
`sites/_index.md`) are stacks of sections separated by `---`; a divider written as
`---.transect` places a named section. See the
[Hugobricks v2 docs](https://www.hugobricks2.preview.usecue.com/docs/) for the built-in
section types. Site-wide text (title, menu, footer, funding) is in `data/en/`.

Placeholders still waiting for real content are marked `TODO(content)`:
`grep -rn "TODO(content)" content data`.

## Licence

The Hugobricks starter files are © Joost van der Schee, MIT licence
(`LICENSE.hugobricks`).
