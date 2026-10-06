import re


def test_tokens_present(css):
    text = css()
    for token, value in {
        "--aquifer": "#0F2A3F", "--flow": "#2471A1", "--recharge": "#32B8D9",
        "--porewater": "#EAF4F7", "--sediment": "#C9B38A",
    }.items():
        assert re.search(rf"{token}:\s*{value}", text, re.I), token


def test_fonts_are_archivo_and_source_serif(css):
    text = css()
    assert '"Archivo"' in text and '"Source Serif 4"' in text
    assert not re.search(r'font-family:\s*"(Signika|Heebo)"', text)
    assert not re.search(r'--font\w+:\s*"(Signika|Heebo)"', text)


def test_font_preloads_and_render_expect(html):
    """Heading face (14.5 kB) and body face: the LCP element is h1 or the lead paragraph."""
    head = html("/").head
    preloads = head.find_all("link", rel="preload")
    assert [p["href"] for p in preloads] == [
        "/fonts/archivo-latin-wdth-normal.woff2", "/fonts/source-serif-4-latin-wght-normal.woff2"]
    assert all(p.has_attr("crossorigin") for p in preloads)
    expect = head.find("link", rel="expect")
    assert expect["href"] == "#main" and expect["blocking"] == "render"


def test_view_transitions_respect_reduced_motion(css):
    text = css()
    block = text[text.index("@view-transition") - 80: text.index("@view-transition")]
    assert "prefers-reduced-motion: no-preference" in block


def test_until_found_is_not_display_none(css):
    assert '[hidden]:not([hidden="until-found"])' in css()


def test_section_fade_ins_are_off():
    import yaml
    from pathlib import Path
    settings = yaml.safe_load((Path(__file__).resolve().parents[1] / "data/settings.yaml").read_text())
    assert settings["intersectionobserver"] is False


def test_logo_is_resized_for_display(site, html):
    img = html("/").select_one("header .logo img")
    assert img["src"].endswith(".webp")
    assert (site / img["src"].lstrip("/")).stat().st_size < 20_000


def test_empty_states_do_not_pull_the_italic_face(css):
    import re
    rule = re.search(r"\.empty\s*{[^}]*}", css()).group(0)
    assert "italic" not in rule


def test_heading_font_is_small_enough_for_lcp():
    """The hero h1 waits on this file; a full variable font cost ~0.7 s of simulated LCP."""
    from pathlib import Path
    fonts = Path(__file__).resolve().parents[1] / "static/fonts"
    assert (fonts / "archivo-latin-wdth-normal.woff2").stat().st_size < 40_000


def test_no_full_size_logo_as_favicon(html):
    icons = [l["href"] for l in html("/").head.find_all("link", rel=lambda r: r and "icon" in r)]
    assert "/uploads/branding/aquicirc-logo.png" not in icons
