def test_home_opens_with_hero(html):
    main = html("/").find("main")
    first = main.find("section")
    assert "hero" in first["class"]
    assert first.find("h1").get_text(strip=True) == "Managed aquifer recharge for a circular water future"
    buttons = [a.get_text(strip=True) for a in first.select("a.button")]
    assert buttons == ["See the six sites", "About the project"]


def test_strata_band_is_decorative(html):
    svg = html("/").select_one("section.hero svg.strata")
    assert svg["aria-hidden"] == "true" and svg["focusable"] == "false"


def test_objectives_section(html):
    features = html("/").select_one("section.features")
    titles = [h.get_text(strip=True) for h in features.select("ul.features h3")]
    assert titles == ["Follow the contaminants", "Model recharge before changing it", "Test better designs"]


def test_single_h1(html):
    assert len(html("/").find_all("h1")) == 1
