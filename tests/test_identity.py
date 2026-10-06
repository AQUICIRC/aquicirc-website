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


def test_one_font_preload_and_render_expect(html):
    head = html("/").head
    preloads = head.find_all("link", rel="preload")
    assert len(preloads) == 1
    assert preloads[0]["href"] == "/fonts/archivo-latin-wdth-normal.woff2"
    assert preloads[0].has_attr("crossorigin")
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
