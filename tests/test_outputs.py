from sitedata import data


def test_outputs_tabs(html):
    tabs = [t.get_text(strip=True) for t in html("/outputs/").select(".tabs [role=tab]")]
    assert tabs == ["Publications", "Deliverables", "Data & models", "Media"]


def test_deliverables_table(html):
    table = html("/outputs/").select_one("table.deliverables")
    rows = {r.th.get_text(strip=True): r for r in table.tbody.find_all("tr")}
    deliverables = data("deliverables")
    assert list(rows) == [d["id"] for d in deliverables]
    for d in deliverables:
        if d["status"] == "public":
            status = rows[d["id"]].select_one(".status")
            assert status.get_text(strip=True) == "Public" and status.svg["aria-hidden"] == "true"
            assert rows[d["id"]].find("a", href=d["url"]), d["id"]


def test_empty_states(html):
    doc = html("/outputs/")
    assert bool(doc.select_one("ol.publications")) == bool(data("publications"))
    assert bool(doc.select_one("ul.datasets")) == bool(data("datasets"))
    assert len(doc.select(".tabs .empty")) == (not data("publications")) + (not data("datasets"))


def test_tabs_render_collapsed_without_waiting_for_js(html):
    """Panels after the first are hidden-until-found in the HTML (no layout shift when JS runs);
    a <noscript> style stacks them again for visitors without JS."""
    tabs = html("/outputs/").select_one(".tabs")
    assert "ready" in tabs["class"]
    panels = tabs.select("[role=tabpanel]")
    assert not panels[0].has_attr("hidden")
    assert all(p.get("hidden") == "until-found" for p in panels[1:])
    assert tabs.find("noscript")
