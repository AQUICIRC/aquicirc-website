from pathlib import Path

import yaml


def test_workpackages_flow(html):
    doc = html("/about/")
    seq = [d["id"] for d in doc.select("section.workpackages ol.wp-sequence details")]
    assert seq == ["wp-WP2", "wp-WP3", "wp-WP4", "wp-WP5"]
    spans = [d["id"] for d in doc.select("section.workpackages details.wp-span")]
    assert spans == ["wp-WP1", "wp-WP6"]
    assert all(not d.has_attr("name") for d in doc.select("section.workpackages details"))
