from pathlib import Path

import yaml


def test_outputs_tabs(html):
    tabs = [t.get_text(strip=True) for t in html("/outputs/").select(".tabs [role=tab]")]
    assert tabs == ["Publications", "Deliverables", "Data & models", "Media"]


def test_deliverables_table(html):
    table = html("/outputs/").select_one("table.deliverables")
    rows = table.tbody.find_all("tr")
    assert len(rows) == len(yaml.safe_load((Path(__file__).resolve().parents[1] / "data/en/deliverables.yaml").read_text()))
    d63 = next(r for r in rows if r.th.get_text(strip=True) == "D6.3")
    status = d63.select_one(".status")
    assert status.get_text(strip=True) == "Public" and status.svg["aria-hidden"] == "true"
    assert d63.find("a", href="https://aquicirc.eu/")


def test_empty_states(html):
    doc = html("/outputs/")
    assert "No publications yet" in doc.get_text()
    assert "No datasets or models yet" in doc.get_text()


def test_tabs_render_collapsed_without_waiting_for_js(html):
    """Panels after the first are hidden-until-found in the HTML (no layout shift when JS runs);
    a <noscript> style stacks them again for visitors without JS."""
    tabs = html("/outputs/").select_one(".tabs")
    assert "ready" in tabs["class"]
    panels = tabs.select("[role=tabpanel]")
    assert not panels[0].has_attr("hidden")
    assert all(p.get("hidden") == "until-found" for p in panels[1:])
    assert tabs.find("noscript")
