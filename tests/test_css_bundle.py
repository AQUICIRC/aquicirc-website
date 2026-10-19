"""Each page ships the core stylesheet plus only the brick CSS it uses (spec §8)."""
from sitedata import NORTH_TO_SOUTH


def bundle(site, html, path):
    href = html(path).find("link", rel="stylesheet")["href"].split("?")[0]
    return (site / href.lstrip("/")).read_text(encoding="utf-8")


def test_home_bundle_has_its_bricks_only(site, html):
    css = bundle(site, html, "/")
    assert "section.hero" in css and "section.sitesmap" in css and "ul.partnerstrip" in css
    assert "carttotal" not in css and "section.prices" not in css and "section.checkout" not in css


def test_site_page_bundle_has_site_layout(site, html):
    css = bundle(site, html, f"/sites/{NORTH_TO_SOUTH[0]}/")
    assert "dl.facts" in css and "section.hero" not in css


def test_post_bundle_has_post_brick(site, html):
    post = html("/news/").select_one("ul.posts a[href^='/news/']:not([href*='?'])")["href"]
    assert "section.post" in bundle(site, html, post)


def test_about_bundle_has_workpackages(site, html):
    assert "details.wp" in bundle(site, html, "/about/")
