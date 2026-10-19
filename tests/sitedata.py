"""What the tests expect, derived from the content and data files (so partners editing a
site, a partner, a person or a post never break CI). Tests check that the pages render
what the data says and how — never a copy of the content itself."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def data(name):
    """A file from data/en/, or [] when it is missing or empty."""
    path = ROOT / "data" / "en" / f"{name}.yaml"
    return (yaml.safe_load(path.read_text()) if path.is_file() else None) or []


def front_matter(path):
    return yaml.safe_load(path.read_text().split("---")[1])


def _pages(section):
    return [p for p in sorted((ROOT / "content/en" / section).glob("*.md")) if p.name != "_index.md"]


def _sites():
    rows = [{"slug": p.stem, "path": p, **front_matter(p)} for p in _pages("sites")]
    return sorted(rows, key=lambda s: -s["coordinates"][0][0])


def _posts():
    return [{"path": p, **front_matter(p)} for p in _pages("posts")]


SITES = _sites()
NORTH_TO_SOUTH = [s["slug"] for s in SITES]
POINTS = sum(len(s["coordinates"]) for s in SITES)
POSTS = _posts()
