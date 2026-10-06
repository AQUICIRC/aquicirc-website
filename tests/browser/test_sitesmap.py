from playwright.sync_api import expect

from sitedata import POINTS, SITES


def test_map_loads_when_scrolled_into_view(page, served):
    seen = []
    page.on("request", lambda r: seen.append(r.url))
    page.set_viewport_size({"width": 1280, "height": 700})
    page.goto(f"{served}/")
    page.wait_for_load_state("networkidle")
    assert not [u for u in seen if "openstreetmap" in u], "tiles requested before the map is near view"
    page.locator("section.sitesmap").scroll_into_view_if_needed()
    page.wait_for_selector("section.sitesmap .leaflet-marker-icon")
    titles = " | ".join(page.locator("section.sitesmap .leaflet-marker-icon").evaluate_all("els => els.map(e => e.title)"))
    assert all(s["title"] in titles for s in SITES), titles   # every site is on the map (merged or not)


def test_marker_popup_has_teaser_and_link(page, served):
    page.goto(f"{served}/sites/")
    page.locator("section.sitesmap").scroll_into_view_if_needed()
    page.wait_for_selector("section.sitesmap .leaflet-marker-icon")
    page.locator("section.sitesmap .leaflet-marker-icon").first.click()
    popup = page.locator(".leaflet-popup-content")
    expect(popup).to_contain_text(SITES[0]["teaser"])
    expect(popup.locator(f"a[href='/sites/{SITES[0]['slug']}/']")).to_contain_text("Go to the site page")


def test_markers_are_keyboard_reachable(page, served):
    page.goto(f"{served}/sites/")
    page.locator("section.sitesmap").scroll_into_view_if_needed()
    page.wait_for_selector("section.sitesmap .leaflet-marker-icon")
    marker = page.locator("section.sitesmap .leaflet-marker-icon").first
    assert marker.get_attribute("tabindex") == "0"
    marker.focus()
    page.keyboard.press("Enter")
    expect(page.locator(".leaflet-popup-content")).to_be_visible()
