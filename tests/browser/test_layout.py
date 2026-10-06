import pytest

PAGES = ["/", "/about/", "/sites/", "/sites/cape-town/", "/sites/lieshout/", "/consortium/", "/news/", "/outputs/"]


@pytest.mark.parametrize("path", PAGES)
def test_no_horizontal_scroll_on_small_phone(browser, served, path):
    context = browser.new_context(viewport={"width": 360, "height": 780})
    page = context.new_page()
    page.goto(f"{served}{path}")
    overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    context.close()
    assert overflow <= 0, f"{path} overflows by {overflow}px"
