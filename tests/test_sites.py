NORTH_TO_SOUTH = ["lieshout", "kinrooi", "besos", "llobregat", "wadi-khairat", "cape-town"]


def test_every_site_page_builds_with_facts(html):
    for slug in NORTH_TO_SOUTH:
        doc = html(f"/sites/{slug}/")
        assert doc.find("h1")["style"] == f"view-transition-name: site-{slug}"
        facts = doc.select_one("dl.facts")
        terms = [dt.get_text(strip=True) for dt in facts.find_all("dt")]
        assert terms[:4] == ["Climate", "Aquifer", "MAR system", "Source water"]


def test_previous_next_follow_latitude(html):
    nav = html("/sites/besos/").select_one("nav.sitenav")
    links = {a["rel"][0]: a["href"] for a in nav.find_all("a")}
    assert links["prev"] == "/sites/kinrooi/" and links["next"] == "/sites/llobregat/"
    first = html("/sites/lieshout/").select_one("nav.sitenav")
    assert first.find("a", rel="prev") is None


def test_partners_link_to_consortium(html):
    dd = html("/sites/cape-town/").select_one("dl.facts dd.partners")
    hrefs = [a["href"] for a in dd.find_all("a")]
    assert "/consortium/#partner-su" in hrefs


def test_site_news_empty_state(html):
    section = html("/sites/wadi-khairat/").select_one("section.sitenews")
    assert section.select_one(".empty")


def test_missing_required_field_fails_build(build_variant):
    def break_it(root):
        p = root / "content/en/sites/kinrooi.md"
        p.write_text(p.read_text().replace("mar_system:", "old_mar_system:"))
    result = build_variant(break_it)
    assert result.returncode != 0
    assert 'missing required front matter "mar_system"' in result.stderr


def test_image_without_alt_fails_build(build_variant):
    def break_it(root):
        p = root / "content/en/sites/kinrooi.md"
        p.write_text(p.read_text().replace("title:", "image: /uploads/x.jpg\ntitle:", 1))
    result = build_variant(break_it)
    assert result.returncode != 0 and "image_alt" in result.stderr
