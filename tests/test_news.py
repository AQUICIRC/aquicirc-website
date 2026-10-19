import re

from sitedata import NORTH_TO_SOUTH, POSTS


def post_urls(html):
    """The posts linked from /news/, as the build published them."""
    hrefs = [a["href"] for a in html("/news/").select("ul.posts a[href^='/news/']") if "?" not in a["href"]]
    return list(dict.fromkeys(hrefs))


def test_news_lives_at_news(html, site):
    assert html("/news/").find("ul", class_="posts")
    urls = post_urls(html)
    assert urls and all(u.startswith("/news/") and (site / u.strip("/") / "index.html").exists() for u in urls)
    assert not (site / "posts").exists()


def test_tag_links_point_to_news(html):
    for url in post_urls(html):
        links = [a["href"] for a in html(url).select(".post .meta .tags a")]
        assert all(h.startswith("/news/?tag=") for h in links), url


def test_home_shows_at_most_three_without_filter(html):
    section = html("/").select_one("section.posts")
    assert len(section.select("ul.posts > li")) == min(3, len(POSTS))
    assert section.select_one("form.filter") is None


def test_post_with_case_site_shows_on_that_site_page(build_variant, tmp_path):
    post = POSTS[0]
    target, other = NORTH_TO_SOUTH[:2]
    def tag_it(root):
        p = root / "content/en/posts" / post["path"].name
        text = p.read_text()
        text = re.sub(r"^case_sites:.*\n", "", text, flags=re.M)
        p.write_text(text.replace("---\n", f"---\ncase_sites: [{target}]\n", 1))
    assert build_variant(tag_it).returncode == 0
    assert post["title"] in (tmp_path / f"out/sites/{target}/index.html").read_text()
    assert post["title"] not in (tmp_path / f"out/sites/{other}/index.html").read_text()


def test_post_image_without_alt_fails(build_variant):
    def break_it(root):
        p = root / "content/en/posts" / POSTS[0]["path"].name
        p.write_text(p.read_text().replace("title:", "image: /uploads/x.jpg\ntitle:", 1))
    result = build_variant(break_it)
    assert result.returncode != 0 and "image_alt" in result.stderr
