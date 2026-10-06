"""Regression tests for the final-review findings (build output)."""
import re
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def test_headings_never_skip_a_level(site):
    for page in site.rglob("*.html"):
        doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        levels = [int(h.name[1]) for h in doc.find_all(re.compile(r"^h[1-6]$"))]
        for a, b in zip(levels, levels[1:]):
            assert b <= a + 1, f"{page.relative_to(site)}: h{a} -> h{b}"


def test_meta_descriptions_are_clean_prose(site):
    for page in site.rglob("*.html"):
        doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        meta = doc.find("meta", attrs={"name": "description"})
        if not meta:
            continue
        text = meta["content"]
        for junk in ("—.", "{:", "Filter tags", "Filter posts", "PublicationsDeliverable"):
            assert junk not in text, f"{page.relative_to(site)}: {text[:80]}"


def test_no_placeholder_social_links(html):
    hrefs = [a["href"] for a in html("/").select("footer a")]
    assert "https://www.linkedin.com/" not in hrefs and "https://bsky.app/" not in hrefs


def test_inactive_tab_panels_render_with_tabindex_minus_one(html):
    panels = html("/outputs/").select(".tabs [role=tabpanel]")
    assert [p["tabindex"] for p in panels] == ["0", "-1", "-1", "-1"]
