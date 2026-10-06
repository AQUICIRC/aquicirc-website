def test_inactive_panels_are_until_found(page, served):
    page.goto(f"{served}/outputs/")
    hidden = page.locator(".tabs [role=tabpanel]").evaluate_all("els => els.map(e => e.getAttribute('hidden'))")
    assert hidden[0] is None and all(h == "until-found" for h in hidden[1:])


def test_beforematch_selects_tab(page, served):
    page.goto(f"{served}/outputs/")
    page.locator(".tabs [role=tabpanel]").nth(1).evaluate("el => el.dispatchEvent(new Event('beforematch'))")
    assert page.locator(".tabs [role=tab]").nth(1).get_attribute("aria-selected") == "true"


def test_no_js_all_panels_readable(browser, served):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{served}/outputs/")
    assert page.locator(".tabs [role=tabpanel]").evaluate_all("els => els.every(e => e.offsetHeight > 0)")
    context.close()
