"""Regression tests for the final-review findings."""
from playwright.sync_api import expect


def test_transect_figure_does_not_clip(page, served):
    page.goto(f"{served}/sites/")
    assert page.locator(".transect-figure").evaluate("e => getComputedStyle(e).overflow") == "visible"


def test_hidden_tab_panels_are_not_tab_stops(page, served):
    page.goto(f"{served}/outputs/")
    stops = page.locator(".tabs [role=tabpanel]").evaluate_all("els => els.map(e => e.tabIndex)")
    assert stops == [0, -1, -1, -1]
    page.get_by_role("tab", name="Deliverables").click()
    stops = page.locator(".tabs [role=tabpanel]").evaluate_all("els => els.map(e => e.tabIndex)")
    assert stops == [-1, 0, -1, -1]


def test_footer_focus_ring_is_recharge_cyan(page, served):
    page.goto(f"{served}/")
    page.locator("footer a").first.focus()
    color = page.locator("footer a").first.evaluate("e => getComputedStyle(e).outlineColor")
    assert color == "rgb(50, 184, 217)"


def test_transect_dot_is_inside_the_link(page, served):
    """Clicking a dot follows a site link. (Besòs and Llobregat are 0.06° apart, so their
    dots overlap and the top one wins: that is the data, not a defect.)"""
    page.goto(f"{served}/sites/")
    dots = page.locator("ol.transect-sites .dot")
    for i in range(dots.count()):
        dots.nth(i).scroll_into_view_if_needed()
        hit = dots.nth(i).evaluate(
            """d => { const r = d.getBoundingClientRect();
                      const el = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
                      return !!(el && el.closest('ol.transect-sites a')); }""")
        assert hit, f"dot {i} is not inside a site link"


def test_transect_link_box_hugs_its_text(page, served):
    page.goto(f"{served}/sites/")
    heights = page.locator("ol.transect-sites > li > a").evaluate_all(
        "els => els.map(a => a.getBoundingClientRect().height)")
    assert max(heights) < 90, heights


def test_latitude_tick_line_sits_at_its_latitude(page, served):
    page.goto(f"{served}/sites/")
    off = page.locator(".transect-ticks li").evaluate_all(
        """els => els.map(li => { const f = li.closest('.transect-figure').getBoundingClientRect();
            const y = f.top + f.height * parseFloat(li.style.getPropertyValue('--y')) / 100;
            return Math.abs(li.getBoundingClientRect().bottom - y); })""")
    assert max(off) <= 1.5, off
