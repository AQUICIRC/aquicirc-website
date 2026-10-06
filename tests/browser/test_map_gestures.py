"""Ctrl/⌘ + scroll zooms the map; a plain scroll scrolls the page and shows a hint.
On touch devices one finger scrolls the page and two fingers move the map."""
from playwright.sync_api import expect


def ready(page, served, path="/sites/"):
    page.goto(f"{served}{path}")
    page.locator("section.sitesmap").scroll_into_view_if_needed()
    page.wait_for_selector("section.sitesmap .leaflet-marker-icon")
    frame = page.locator(".sitesmap-frame")
    box = frame.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    return frame


def test_ctrl_scroll_zooms(page, served):
    frame = ready(page, served)
    before = float(frame.get_attribute("data-zoom"))
    page.keyboard.down("Control")
    page.mouse.wheel(0, -400)
    page.keyboard.up("Control")
    page.wait_for_timeout(600)
    assert float(frame.get_attribute("data-zoom")) > before


def test_plain_scroll_keeps_zoom_and_shows_hint(page, served):
    frame = ready(page, served)
    before = frame.get_attribute("data-zoom")
    page.mouse.wheel(0, 300)
    expect(frame.locator(".map-hint")).to_be_visible()
    expect(frame.locator(".map-hint")).to_contain_text("scroll to zoom")
    assert frame.get_attribute("data-zoom") == before


def test_touch_devices_need_two_fingers_to_pan(browser, served):
    context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    page = context.new_page()
    page.goto(f"{served}/sites/")
    page.locator("section.sitesmap").scroll_into_view_if_needed()
    page.wait_for_selector("section.sitesmap .leaflet-marker-icon")
    frame = page.locator(".sitesmap-frame")
    assert frame.get_attribute("data-one-finger-pan") == "false"
    assert "two fingers" in frame.locator(".map-hint").text_content()
    context.close()
