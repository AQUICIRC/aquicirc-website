import re

ACTION = "https://api.web3forms.com/submit"


def test_contact_form_posts_to_web3forms(html):
    form = html("/contact/").select_one("section.contact form#contactform")
    assert form["action"] == ACTION and form["method"] == "post"
    key = form.find("input", attrs={"name": "access_key"})
    assert key["type"] == "hidden"
    assert re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", key["value"])


def test_contact_form_fields(html):
    form = html("/contact/").select_one("form#contactform")
    for name in ("name", "email", "message", "consent"):
        assert form.find(attrs={"name": name}).has_attr("required"), name
    assert not form.find(attrs={"name": "organisation"}).has_attr("required")
    assert form.find("input", attrs={"name": "email"})["type"] == "email"
    assert form.find("legend").get_text(strip=True) == "Send us a message"


def test_redirect_lands_on_unindexed_thanks_page(html, site):
    form = html("/contact/").select_one("form#contactform")
    assert form.find("input", attrs={"name": "redirect"})["value"] == "https://aquicirc.eu/contact/thanks/"
    thanks = html("/contact/thanks/")
    assert thanks.find("meta", attrs={"name": "robots"})["content"] == "noindex"
    assert "contact/thanks" not in (site / "sitemap.xml").read_text()


def test_spam_guards(html):
    form = html("/contact/").select_one("form#contactform")
    trap = form.find("input", attrs={"name": "botcheck"})
    assert trap["type"] == "checkbox" and trap.find_parent(attrs={"hidden": True})
    assert form.select_one(".h-captcha")["data-sitekey"]
    assert form.find("script", src=re.compile(r"^https://js\.hcaptcha\.com/"))
    assert form.select_one("noscript a[href='mailto:aquicirc@gmail.com']")
    # The captcha sits before the button, so it is passed before sending.
    assert form.select_one(".captcha").find_next(class_="submit")


def test_address_beside_the_form_holds_no_form_parts(html):
    address = html("/contact/").select_one("section.contact address")
    assert address.find("script") is None and address.find("form") is None
    assert address.find("a", href="mailto:aquicirc@gmail.com")


def test_captcha_script_only_on_the_contact_page(site):
    for page in site.rglob("*.html"):
        if "hcaptcha" in page.read_text(encoding="utf-8"):
            assert page.relative_to(site).as_posix() == "contact/index.html", page


def test_footer_links_to_contact(html):
    footer = html("/").find("footer")
    assert footer.find("a", href="/contact/")


def test_header_contact_button(html):
    header = html("/news/").find("header")
    assert header.select_one(".actions a.button[href='/contact/']").get_text(strip=True) == "Contact"
    # Repeated in the menu panel for phones, where the header button is hidden.
    assert header.select_one("nav.mainnav .menu-cta a[href='/contact/']")
