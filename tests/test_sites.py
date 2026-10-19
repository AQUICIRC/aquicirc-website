import re

from sitedata import NORTH_TO_SOUTH, POSTS, ROOT, SITES

ANY_SITE = SITES[0]["path"].relative_to(ROOT)   # the build variants break one site file


def test_every_site_page_builds_with_facts(html):
    for slug in NORTH_TO_SOUTH:
        doc = html(f"/sites/{slug}/")
        facts = doc.select_one("dl.facts")
        terms = [dt.get_text(strip=True) for dt in facts.find_all("dt")]
        assert terms[:4] == ["Climate", "Aquifer", "MAR system", "Source water"]


def test_previous_next_follow_latitude(html):
    for i, slug in enumerate(NORTH_TO_SOUTH):
        nav = html(f"/sites/{slug}/").select_one("nav.sitenav")
        links = {a["rel"][0]: a["href"] for a in nav.find_all("a")}
        assert links.get("prev") == (f"/sites/{NORTH_TO_SOUTH[i - 1]}/" if i else None)
        assert links.get("next") == (f"/sites/{NORTH_TO_SOUTH[i + 1]}/" if i + 1 < len(NORTH_TO_SOUTH) else None)


def test_partners_link_to_consortium(html):
    for site in SITES:
        if not site.get("partners"):
            continue
        dd = html(f"/sites/{site['slug']}/").select_one("dl.facts dd.partners")
        hrefs = [a["href"] for a in dd.find_all("a")]
        assert hrefs == [f"/consortium/#partner-{p}" for p in site["partners"]], site["slug"]


def test_site_news_empty_state(html):
    tagged = {s for post in POSTS for s in post.get("case_sites") or []}
    for slug in NORTH_TO_SOUTH:
        section = html(f"/sites/{slug}/").select_one("section.sitenews")
        assert bool(section.select_one(".empty")) == (slug not in tagged), slug


def test_missing_required_field_fails_build(build_variant):
    def break_it(root):
        p = root / ANY_SITE
        p.write_text(p.read_text().replace("mar_system:", "old_mar_system:"))
    result = build_variant(break_it)
    assert result.returncode != 0
    assert 'missing required front matter "mar_system"' in result.stderr


def test_missing_teaser_fails_build(build_variant):
    def break_it(root):
        p = root / ANY_SITE
        p.write_text(p.read_text().replace("teaser:", "old_teaser:"))
    result = build_variant(break_it)
    assert result.returncode != 0 and 'missing required front matter "teaser"' in result.stderr


def test_swapped_coordinates_fail_build(build_variant):
    def swap(root):
        p = root / ANY_SITE   # lon 51.52 lies east of the project area whatever the site
        p.write_text(re.sub(r"^coordinates:.*$", "coordinates: [[5.60, 51.52]]", p.read_text(), count=1, flags=re.M))
    result = build_variant(swap)
    assert result.returncode != 0 and "swapped" in result.stderr


def test_image_without_alt_fails_build(build_variant):
    def break_it(root):
        p = root / ANY_SITE
        p.write_text(p.read_text().replace("title:", "image: /uploads/x.jpg\ntitle:", 1))
    result = build_variant(break_it)
    assert result.returncode != 0 and "image_alt" in result.stderr
