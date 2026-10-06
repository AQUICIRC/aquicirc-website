def test_news_lives_at_news(html, site):
    assert html("/news/").find("ul", class_="posts")
    assert (site / "news/website-launched/index.html").exists()
    assert not (site / "posts").exists()


def test_tag_links_point_to_news(html):
    links = [a["href"] for a in html("/news/website-launched/").select(".post .meta .tags a")]
    assert links and all(h.startswith("/news/?tag=") for h in links)


def test_home_shows_at_most_three_without_filter(html):
    section = html("/").select_one("section.posts")
    assert 1 <= len(section.select("ul.posts > li")) <= 3
    assert section.select_one("form.filter") is None


def test_post_with_case_site_shows_on_that_site_page(build_variant, tmp_path):
    def tag_it(root):
        p = root / "content/en/posts/2026-10-06-website-launched.md"
        p.write_text(p.read_text().replace("wps:", "case_sites: [kinrooi]\nwps:", 1))
    assert build_variant(tag_it).returncode == 0
    kinrooi = (tmp_path / "out/sites/kinrooi/index.html").read_text()
    lieshout = (tmp_path / "out/sites/lieshout/index.html").read_text()
    assert "The AQUICIRC website is live" in kinrooi
    assert "The AQUICIRC website is live" not in lieshout


def test_post_image_without_alt_fails(build_variant):
    def break_it(root):
        p = root / "content/en/posts/2026-10-06-website-launched.md"
        p.write_text(p.read_text().replace("title:", "image: /uploads/x.jpg\ntitle:", 1))
    result = build_variant(break_it)
    assert result.returncode != 0 and "image_alt" in result.stderr
