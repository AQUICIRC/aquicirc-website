"""Regression tests for the final-review findings."""
from playwright.sync_api import expect



def test_hidden_tab_panels_are_not_tab_stops(page, served):
    page.goto(f"{served}/outputs/")
    stops = page.locator(".tabs [role=tabpanel]").evaluate_all("els => els.map(e => e.tabIndex)")
    assert stops == [0] + [-1] * (len(stops) - 1)
    page.locator(".tabs [role=tab]").nth(1).click()
    stops = page.locator(".tabs [role=tabpanel]").evaluate_all("els => els.map(e => e.tabIndex)")
    assert stops == [-1, 0] + [-1] * (len(stops) - 2)


def test_footer_focus_ring_is_recharge_cyan(page, served):
    page.goto(f"{served}/")
    page.locator("footer a").first.focus()
    color = page.locator("footer a").first.evaluate("e => getComputedStyle(e).outlineColor")
    assert color == "rgb(50, 184, 217)"
