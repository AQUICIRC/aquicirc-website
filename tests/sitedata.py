"""The case-study sites as the tests expect them, derived from the site front matter
(so partners editing a site never break CI). Ordered north → south."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _sites():
    rows = []
    for path in (ROOT / "content/en/sites").glob("*.md"):
        if path.name == "_index.md":
            continue
        fm = yaml.safe_load(path.read_text().split("---")[1])
        rows.append({"slug": path.stem, **fm})
    return sorted(rows, key=lambda s: -s["coordinates"][0][0])


SITES = _sites()
NORTH_TO_SOUTH = [s["slug"] for s in SITES]
POINTS = sum(len(s["coordinates"]) for s in SITES)
