"""Expected site order and transect positions, derived from the site front matter."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _expected():
    """Positions computed from the site front matter with the spec §6.1 scale, so
    partners confirming coordinates never break CI. Ordered north → south."""
    rows = []
    for path in (ROOT / "content/en/sites").glob("*.md"):
        if path.name == "_index.md":
            continue
        lat = yaml.safe_load(path.read_text().split("---")[1])["coordinates"][0][0]
        dot = 2 + (53 - lat) * 66 / 18 if lat >= 0 else 84 + (-33 - lat) * 7
        rows.append((path.stem, lat, dot))
    rows.sort(key=lambda r: -r[1])
    out, prev = {}, -100.0
    for slug, _, dot in rows:
        label = max(dot, prev + 11)
        out[slug], prev = (round(dot, 2), round(label, 2)), label
    return out


EXPECTED = _expected()
