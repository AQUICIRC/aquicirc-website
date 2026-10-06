import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PARTNER_FILES = [*ROOT.glob("content/en/sites/*.md"), *ROOT.glob("content/en/posts/*.md"), *ROOT.glob("data/en/*.yaml")]


def test_partner_content_has_no_shortcodes_or_dividers():
    for path in PARTNER_FILES:
        if path.name == "_index.md":
            continue
        text = path.read_text()
        body = text.split("---", 2)[-1] if path.suffix == ".md" else text
        assert "{{<" not in body and "{{%" not in body, path.name
        if path.suffix == ".md":
            assert not re.search(r"^---", body, re.M), f"{path.name} has a body divider"


def test_no_arrows_in_link_text(site):
    for page in site.rglob("index.html"):
        assert not re.search(r">[^<]*→\s*</a>", page.read_text(encoding="utf-8")), page


def test_every_page_one_h1(site):
    for page in site.rglob("index.html"):
        doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        assert len(doc.find_all("h1")) == 1, page.relative_to(site)


def test_brick_includes_are_not_published(site):
    assert not (site / "bricks").exists()


def test_404_copy(html):
    doc = html("/404.html")
    assert doc.find("h1").get_text(strip=True) == "This page does not exist"
