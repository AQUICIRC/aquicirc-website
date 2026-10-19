import yaml

from sitedata import ROOT

MENU = ["About", "Case studies", "Consortium", "News", "Outputs"]


def test_main_menu_order(html):
    nav = html("/").find("nav", class_="mainnav") or html("/").select_one("header nav")
    labels = [a.get_text(strip=True) for a in nav.find_all("a") if a.get_text(strip=True)]
    assert labels[:5] == MENU


def test_footer_has_funding_statement_and_funders_slot(html):
    footer = html("/").find("footer")
    assert "Water4All" in footer.get_text()
    assert footer.select_one(".funders") is not None


def test_colophon_carries_contact_email(html):
    assert html("/").select_one("footer .colophon a[href='mailto:aquicirc@gmail.com']")


def test_no_content_markers_rendered(site):
    for page in site.rglob("*.html"):
        assert "TODO(content)" not in page.read_text(encoding="utf-8"), page.relative_to(site)


def test_funders_panel_logos(html):
    panel = html("/news/").select_one("footer .funders-panel")
    imgs = panel.select("ul.funders img")
    assert imgs[0]["alt"] == "Co-funded by the European Union"
    funders = yaml.safe_load((ROOT / "data/en/footer.yaml").read_text())["funders"]
    assert len(imgs) == len([f for f in funders if f.get("logo")])
    for img in imgs:
        assert img["alt"] and img["src"].endswith((".webp", ".svg")), img["src"]
        # One height for all: the EU emblem is never smaller, and NWO's minimum is 57 px.
        assert img["height"] == "64", img["src"]


def test_no_empty_colophon_without_email(build_variant, tmp_path):
    def clear_email(root):
        p = root / "data/en/general.yaml"
        p.write_text(p.read_text().replace("email: aquicirc@gmail.com", 'email: ""'))
    assert build_variant(clear_email).returncode == 0
    assert 'class="colophon"' not in (tmp_path / "out/index.html").read_text()
