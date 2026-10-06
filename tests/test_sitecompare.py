def test_compare_table_semantics(html):
    table = html("/sites/").select_one("section.sitecompare table.datatable")
    assert table.caption.get_text(strip=True) == "The six case-study sites compared"
    headers = [th.get_text(strip=True) for th in table.thead.find_all("th")]
    assert headers == ["Site", "Country", "Climate", "Aquifer", "MAR system", "Expected contaminants"]
    rows = table.tbody.find_all("tr")
    assert len(rows) == 6
    assert rows[0].th["scope"] == "row" and rows[0].th.a["href"] == "/sites/lieshout/"
    frame = table.find_parent("div", class_="datatable-frame")
    assert frame["role"] == "region" and frame["tabindex"] == "0"
    assert frame["aria-labelledby"] == table.caption["id"]


def test_stacked_labels_are_dom_text(html):
    cell = html("/sites/").select_one("table.datatable tbody td")
    assert cell.select_one(".cell-label").get_text(strip=True) == "Country"
