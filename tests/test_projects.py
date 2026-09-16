from instagram_poster import projects


def test_load_projects_reads_full_portfolio():
    rows = projects.load_projects()
    assert len(rows) == 53
    names = [r["Project Name"] for r in rows]
    assert "Luminara" in names
    assert "Golden Hill" in names


def test_get_project_by_number():
    row = projects.get_project(15)
    assert row["Project Name"] == "Galaxy ONE"
    assert row["Area / Neighbourhood"] == "Westlands"


def test_generate_caption_includes_key_facts_and_no_overclaiming():
    row = projects.get_project(15)
    caption = projects.generate_caption(row)
    assert "Galaxy ONE" in caption
    assert "Westlands" in caption
    assert "KSh 5.2M" in caption
    assert "#NestKenya" in caption
    # never promise unrealistic returns / guaranteed outcomes
    assert "guarantee" not in caption.lower()


def test_generate_caption_handles_missing_developer():
    row = projects.get_project(1)  # Luminara has developer=TBC
    caption = projects.generate_caption(row)
    assert "watching Nairobi's property market" in caption
