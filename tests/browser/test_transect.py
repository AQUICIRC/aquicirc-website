from playwright.sync_api import expect


def test_escape_dismisses_reveal(page, served):
    page.goto(f"{served}/sites/")
    page.locator("ol.transect-sites > li a").first.focus()
    reveal = page.locator("ol.transect-sites > li .reveal").first
    expect(reveal).to_be_visible()
    page.keyboard.press("Escape")
    expect(reveal).to_be_hidden()


def test_reduced_motion_disables_animation(browser, served):
    context = browser.new_context(reduced_motion="reduce")
    page = context.new_page()
    page.goto(f"{served}/sites/")
    name = page.locator(".transect-meridian").evaluate("el => getComputedStyle(el).animationName")
    assert name == "none"
    context.close()
