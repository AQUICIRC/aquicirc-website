from sitedata import data

PARTNERS = data("partners")
COORDINATOR = next(p for p in PARTNERS if p["role"] == "coordinator")


def test_partners_grouped_coordinator_country_first(html):
    groups = html("/consortium/").select("section.partners .country")
    names = [g.find("h3").get_text(strip=True) for g in groups]
    assert names[0] == COORDINATOR["country"]
    assert names[1:] == sorted(names[1:])
    assert set(names) == {p["country"] for p in PARTNERS}


def test_partner_anchor_and_role(html):
    doc = html("/consortium/")
    assert "Coordinator" in doc.select_one(f"#partner-{COORDINATOR['id']}").get_text()
    for p in PARTNERS:
        assert doc.select_one(f"#partner-{p['id']}") is not None, p["id"]


def test_team_group_filter(html):
    doc = html("/consortium/")
    for group in ("advisory", "team"):
        people = [p["name"] for p in data("people") if p["group"] == group]
        section = doc.select_one(f"section:has(h2#{group})")
        if people:
            assert [h.get_text(strip=True) for h in section.select("ul.team h3")] == people
        else:
            assert section.select_one(".empty"), group   # empty state until people are added


def test_partner_strip_on_home(html):
    # One entry per partner in the data file, so adding a partner needs no test change.
    strip = html("/").select_one("ul.partnerstrip")
    hrefs = [a["href"] for a in strip.select("li > a")]
    assert hrefs == [f"/consortium/#partner-{p['id']}" for p in PARTNERS]


def test_partner_logos_are_sized_webp_or_svg(html):
    for page, sel in (("/", "ul.partnerstrip img"), ("/consortium/", "section.partners img")):
        imgs = html(page).select(sel)
        assert imgs, page
        for img in imgs:
            assert img["src"].endswith((".webp", ".svg")), img["src"]
            assert int(img["width"]) > 0 and int(img["height"]) > 0, img["src"]


def test_partner_names_link_to_their_sites(html):
    doc = html("/consortium/")
    for p in PARTNERS:
        link = doc.select_one(f"#partner-{p['id']} .partner-name a")
        if p.get("url"):
            assert link["href"] == p["url"], p["id"]
        else:
            assert link is None, p["id"]
