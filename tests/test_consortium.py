def test_partners_grouped_coordinator_country_first(html):
    groups = html("/consortium/").select("section.partners .country")
    names = [g.find("h3").get_text(strip=True) for g in groups]
    assert names[0] == "Netherlands"
    assert names[1:] == sorted(names[1:])


def test_partner_anchor_and_role(html):
    doc = html("/consortium/")
    wu = doc.select_one("#partner-wu")
    assert "Coordinator" in wu.get_text()
    assert doc.select_one("#partner-su") is not None


def test_team_group_filter(html):
    doc = html("/consortium/")
    advisory = doc.select_one("section:has(h2#advisory) ul.team")
    assert [h.get_text(strip=True) for h in advisory.select("h3")] == ["Ricky Murray", "Sarah Garré"]


def test_team_empty_state(html):
    assert html("/consortium/").select_one("section:has(h2#team) .empty")


def test_partner_strip_on_home(html):
    strip = html("/").select_one("ul.partnerstrip")
    assert len(strip.find_all("li")) == 10
