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
