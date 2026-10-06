def test_outputs_tabs(html):
    tabs = [t.get_text(strip=True) for t in html("/outputs/").select(".tabs [role=tab]")]
    assert tabs == ["Publications", "Deliverables", "Data & models", "Media"]


def test_deliverables_table(html):
    table = html("/outputs/").select_one("table.deliverables")
    rows = table.tbody.find_all("tr")
    assert len(rows) == 19
    d63 = next(r for r in rows if r.th.get_text(strip=True) == "D6.3")
    status = d63.select_one(".status")
    assert status.get_text(strip=True) == "Public" and status.svg["aria-hidden"] == "true"
    assert d63.find("a", href="https://aquicirc.eu/")


def test_empty_states(html):
    doc = html("/outputs/")
    assert "No publications yet" in doc.get_text()
    assert "No datasets or models yet" in doc.get_text()
