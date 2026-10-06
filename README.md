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

Pages live in `content/en/` as plain Markdown. A page is a stack of sections
separated by `---`; Hugobricks picks each section's layout from what it contains
(a heading, an image with `{:.about}`, a link with `{:.button}`, …). See the
[Hugobricks v2 docs](https://www.hugobricks2.preview.usecue.com/docs/) for the
available section types. Site-wide text (title, menu, footer) is in `data/en/`.

## Licence

The Hugobricks starter files are © Joost van der Schee, MIT licence
(`LICENSE.hugobricks`).
