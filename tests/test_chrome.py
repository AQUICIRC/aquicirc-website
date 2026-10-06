MENU = ["About", "Case studies", "Consortium", "News", "Outputs"]


def test_main_menu_order(html):
    nav = html("/").find("nav", class_="mainnav") or html("/").select_one("header nav")
    labels = [a.get_text(strip=True) for a in nav.find_all("a") if a.get_text(strip=True)]
    assert labels[:5] == MENU


def test_footer_has_funding_statement_and_funders_slot(html):
    footer = html("/").find("footer")
    assert "Water4All" in footer.get_text()
    assert footer.select_one(".funders") is not None


def test_contact_email_slot_renders_when_set(build_variant, tmp_path):
    def set_email(root):
        p = root / "data/en/general.yaml"
        p.write_text(p.read_text().replace('email: ""', "email: info@example.org"))
    assert build_variant(set_email).returncode == 0
    assert 'href="mailto:info@example.org"' in (tmp_path / "out/index.html").read_text()


def test_socials_are_linkedin_and_bluesky(html):
    text = html("/").find("footer").get_text()
    assert "LinkedIn" in text and "Bluesky" in text


def test_no_content_markers_rendered(site):
    for page in site.rglob("*.html"):
        assert "TODO(content)" not in page.read_text(encoding="utf-8"), page.relative_to(site)
