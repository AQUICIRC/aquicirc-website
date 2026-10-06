def osm(requests):
    return [r for r in requests if "tile.openstreetmap.org" in r]


def test_no_third_party_before_click(page, served):
    seen = []
    page.on("request", lambda r: seen.append(r.url))
    page.goto(f"{served}/sites/kinrooi/")
    page.wait_for_load_state("networkidle")
    assert not [u for u in seen if not u.startswith(served)]


def test_click_loads_map_and_tiles(page, served):
    seen = []
    page.on("request", lambda r: seen.append(r.url))
    page.goto(f"{served}/sites/kinrooi/")
    page.get_by_role("button", name="Show map").click()
    page.wait_for_selector(".map-frame.loaded.leaflet-container")
    assert osm(seen)


def test_multi_coordinate_site_has_two_markers(page, served):
    page.goto(f"{served}/sites/cape-town/")
    page.get_by_role("button", name="Show map").click()
    page.wait_for_selector(".map-frame.loaded .leaflet-interactive")
    assert page.locator(".map-frame .leaflet-interactive").count() == 2


def test_without_js_link_remains(browser, served):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{served}/sites/kinrooi/")
    assert page.get_by_role("link", name="View GROW pilot, Kinrooi on OpenStreetMap").is_visible()
    assert not page.get_by_role("button", name="Show map").is_visible()
    context.close()
