def test_workpackages_flow(html):
    doc = html("/about/")
    seq = [d["id"] for d in doc.select("section.workpackages ol.wp-sequence details")]
    assert seq == ["wp-WP2", "wp-WP3", "wp-WP4", "wp-WP5"]
    spans = [d["id"] for d in doc.select("section.workpackages details.wp-span")]
    assert spans == ["wp-WP1", "wp-WP6"]
    assert all(not d.has_attr("name") for d in doc.select("section.workpackages details"))


def test_wp_details_list_tasks_and_deliverables(html):
    wp3 = html("/about/").select_one("#wp-WP3")
    text = wp3.get_text(" ", strip=True)
    assert "T3.1" in text and "Q2 2026" in text and "D3.3" in text
    assert "Lead: IoT, VUB" in wp3.summary.get_text(" ", strip=True)


def test_timeline_bars_positions(html):
    bars = html("/about/").select("section.timeline a.bar")
    t31 = next(b for b in bars if "T3.1" in b.get_text())
    assert "grid-column: 3 / 8" in t31["style"]    # Y1Q2 (index 1) → col 3; Y2Q2 (index 5) → end col 8
    assert t31["href"] == "#wp-WP3"
    assert t31.has_attr("data-reveal")


def test_timeline_milestones_and_today(html):
    doc = html("/about/")
    assert len(doc.select("section.timeline a.milestone")) == 19
    today = doc.select_one("section.timeline .today")
    assert today.has_attr("hidden") and today["data-start"] == "2026-01-01" and today["data-months"] == "36"


def test_timeline_frame_is_keyboard_scrollable(html):
    frame = html("/about/").select_one("section.timeline .timeline-frame")
    assert frame["role"] == "region" and frame["tabindex"] == "0" and frame.get("aria-labelledby")
