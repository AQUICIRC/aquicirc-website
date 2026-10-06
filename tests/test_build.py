def test_home_builds_with_project_title(html):
    doc = html("/")
    assert doc.title.string.strip().endswith("AQUICIRC")


def test_page_language_is_english(html):
    assert html("/").html["lang"] == "en"
