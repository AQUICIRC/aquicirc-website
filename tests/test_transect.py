import re

EXPECTED = {
    "lieshout": (7.43, 7.43), "kinrooi": (8.78, 18.43), "besos": (44.39, 44.39),
    "llobregat": (44.61, 55.39), "wadi-khairat": (63.86, 66.39), "cape-town": (87.99, 87.99),
}


def items(doc):
    return doc.select("section.transect ol.transect-sites > li")


def var(style, name):
    return float(re.search(rf"--{name}:\s*([\d.]+)", style).group(1))


def test_sites_in_north_to_south_order(html):
    slugs = [li.a["href"].strip("/").split("/")[-1] for li in items(html("/sites/"))]
    assert slugs == list(EXPECTED)


def test_positions_and_label_spacing(html):
    labels = []
    assert len(items(html("/sites/"))) == 6
    for li in items(html("/sites/")):
        slug = li.a["href"].strip("/").split("/")[-1]
        dot, label = var(li["style"], "dot"), var(li["style"], "label")
        assert (round(dot, 2), round(label, 2)) == EXPECTED[slug], slug
        labels.append(label)
    assert all(b - a >= 11 - 1e-6 for a, b in zip(labels, labels[1:]))


def test_multi_coordinate_site_appears_once(html):
    hrefs = [li.a["href"] for li in items(html("/sites/"))]
    assert hrefs.count("/sites/cape-town/") == 1


def test_view_transition_names_match_site_pages(html):
    assert len(items(html("/"))) == 6
    for li in items(html("/")):
        slug = li.a["href"].strip("/").split("/")[-1]
        assert li.select_one(".site-name")["style"] == f"view-transition-name: site-{slug}"


def test_facts_are_in_the_link_and_revealable(html):
    li = items(html("/sites/"))[0]
    assert li.has_attr("data-reveal")
    assert "Subsurface irrigation" in li.select_one(".reveal").get_text()


def test_break_is_labelled(html):
    assert "7,000 km" in html("/sites/").select_one(".transect-break").get_text()


def test_on_home(html):
    assert html("/").select_one("section.transect") is not None


def test_brick_includes_not_published(site):
    assert not (site / "bricks").exists()
