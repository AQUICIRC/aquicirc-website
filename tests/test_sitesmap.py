"""The map of all sites (Home and Case studies) and the new Home hero."""
import json

from sitedata import POINTS, SITES


def test_home_hero_carries_the_about_opener_and_two_buttons(html):
    hero = html("/").select_one("main section.hero")
    assert hero.find("h1").get_text(strip=True) == "Recharging aquifers with water we used to waste"
    buttons = [(a.get_text(strip=True), a["href"]) for a in hero.select("a.button")]
    assert buttons == [("See the six sites", "/sites/"), ("See outputs", "/outputs/")]


def test_about_has_its_own_opener(html):
    assert html("/about/").find("h1").get_text(strip=True) == "About AQUICIRC"


def test_transect_is_gone(site):
    for page in site.rglob("*.html"):
        assert 'class="transect' not in page.read_text(encoding="utf-8"), page.relative_to(site)


def test_map_on_home_and_case_studies(html):
    for path in ("/", "/sites/"):
        section = html(path).select_one("section.sitesmap")
        data = json.loads(section.select_one("[data-sites]")["data-sites"])
        assert len(data) == len(SITES)
        assert sum(len(s["points"]) for s in data) == POINTS
        first = data[0]
        assert set(first) == {"name", "url", "teaser", "points"}
        assert first["url"] == f"/sites/{SITES[0]['slug']}/" and first["teaser"] == SITES[0]["teaser"]


def test_map_has_a_plain_list_of_sites(html):
    """Keyboard, screen-reader and no-JS route to every site, beside the map."""
    links = [a["href"] for a in html("/").select("section.sitesmap .sitesmap-list a")]
    assert links == [f"/sites/{s['slug']}/" for s in SITES]


def test_map_credits_openstreetmap(html):
    assert "OpenStreetMap" in html("/").select_one("section.sitesmap").get_text()


def test_about_has_no_timeline_and_no_advisory_board(html):
    doc = html("/about/")
    assert doc.select_one("section.timeline") is None
    assert doc.select_one("ul.team") is None


def test_workpackage_panels_are_plain_summaries(html):
    for wp in html("/about/").select("section.workpackages details"):
        body = wp.select_one(".wp-body")
        text = body.get_text(" ", strip=True)
        sentences = [x for x in text.replace("e.g.", "eg").split(". ") if x]
        assert 2 <= len(sentences) <= 3, (wp["id"], text)
        assert not body.find(["ul", "h3", "h4"]), wp["id"]
        assert "Q1 20" not in text and "Q2 20" not in text, wp["id"]
