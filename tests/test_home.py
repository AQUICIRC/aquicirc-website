def test_strata_band_is_decorative(html):
    svg = html("/").select_one("section.hero svg.strata")
    assert svg["aria-hidden"] == "true" and svg["focusable"] == "false"


def test_objectives_section(html):
    features = html("/").select_one("section.features")
    titles = [h.get_text(strip=True) for h in features.select("ul.features h3")]
    assert titles == ["Follow the contaminants", "Model recharge before changing it", "Test better designs"]


def test_single_h1(html):
    assert len(html("/").find_all("h1")) == 1
