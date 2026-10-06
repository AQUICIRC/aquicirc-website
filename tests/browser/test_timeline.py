def test_today_marker_placed(page, served):
    page.clock.set_fixed_time("2026-10-06T12:00:00")
    page.goto(f"{served}/about/")
    today = page.locator("section.timeline .today")
    assert today.is_visible()
    value = float(today.evaluate("el => el.style.getPropertyValue('--today')"))
    assert 0.25 < value < 0.27     # 9 of 36 months


def test_today_hidden_after_project(page, served):
    page.clock.set_fixed_time("2030-01-01T12:00:00")
    page.goto(f"{served}/about/")
    assert not page.locator("section.timeline .today").is_visible()
