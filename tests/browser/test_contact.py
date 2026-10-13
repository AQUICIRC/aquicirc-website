from urllib.parse import parse_qs

ACTION = "https://api.web3forms.com/submit"


def fill(page):
    page.fill("#contactform-name", "Test Person")
    page.fill("#contactform-email", "test@example.org")
    page.fill("#contactform-message", "Hello")
    page.check("#contactform-consent")


def offline(page):
    """No request leaves the machine: hCaptcha is not loaded, Web3Forms is recorded."""
    sent = []
    page.route("https://js.hcaptcha.com/**", lambda route: route.abort())

    def submit(route):
        sent.append(parse_qs(route.request.post_data))
        route.fulfill(status=302, headers={"Location": sent[-1]["redirect"][0]})
    page.route(ACTION, submit)
    page.route("https://aquicirc.eu/**", lambda route: route.fulfill(status=200, body="thanks"))
    return sent


def test_not_sent_before_captcha(page, served):
    sent = offline(page)
    page.goto(f"{served}/contact/")
    fill(page)
    page.click("#contactform button[type=submit]")
    assert page.locator(".captcha-error").is_visible()
    assert page.url == f"{served}/contact/" and sent == []


def test_sent_once_captcha_passed(page, served):
    sent = offline(page)
    page.goto(f"{served}/contact/")
    fill(page)
    # What hCaptcha leaves in the form once it is solved.
    page.locator(".h-captcha").evaluate(
        "el => { const t = document.createElement('textarea'); t.name = 'h-captcha-response'; t.value = 'token'; el.append(t); }")
    with page.expect_navigation():
        page.click("#contactform button[type=submit]")
    body = sent[0]
    assert body["access_key"][0] and body["h-captcha-response"] == ["token"]
    assert body["name"] == ["Test Person"] and body["email"] == ["test@example.org"]
    assert "botcheck" not in body
    assert page.url == "https://aquicirc.eu/contact/thanks/"


def test_no_js_points_to_email(browser, served):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{served}/contact/")
    assert page.locator("#contactform a[href='mailto:aquicirc@gmail.com']").is_visible()
    context.close()


def test_contact_reachable_from_header_at_every_width(browser, served):
    for width, where in ((1280, ".actions .button"), (390, ".menu-cta a")):
        page = browser.new_page(viewport={"width": width, "height": 800})
        page.route("https://js.hcaptcha.com/**", lambda route: route.abort())
        page.goto(f"{served}/about/")
        if page.locator("#togglemenu").is_visible():
            page.click("#togglemenu")
        link = page.locator(f"header {where}")
        link.wait_for(state="visible")
        link.click()
        page.wait_for_url(f"{served}/contact/")
        page.close()
