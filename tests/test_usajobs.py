from skilllens.usajobs import clean_text, parse_item, split_sentences


def test_clean_text_removes_html_and_contacts():
    raw = "<p>Contact jane.doe@agency.gov or (202) 555-0147.</p> Apply at https://usajobs.gov/x &amp; more"
    out = clean_text(raw)
    assert "@" not in out and "555" not in out and "http" not in out and "<p>" not in out
    assert out.endswith("& more")


def test_split_sentences():
    s = split_sentences("You will build data pipelines. You will analyse data with Python and SQL. Ok.")
    assert s == ["You will build data pipelines.", "You will analyse data with Python and SQL."]


def test_parse_item():
    item = {
        "MatchedObjectId": "812345600",
        "MatchedObjectDescriptor": {
            "PositionTitle": "Data Scientist",
            "OrganizationName": "Census Bureau",
            "JobCategory": [{"Name": "Data Science Series", "Code": "1560"}],
            "JobGrade": [{"Code": "GS"}],
            "PositionLocationDisplay": "Washington, District of Columbia",
            "PublicationStartDate": "2026-11-20T00:00:00.0000",
            "QualificationSummary": "Experience applying machine learning to survey data.",
            "UserArea": {"Details": {"JobSummary": "Join our team.",
                                      "MajorDuties": ["Develop models in Python and R.", "Present results to managers."],
                                      "LowGrade": "12"}},
        },
    }
    rec = parse_item(item)
    assert rec["usajobs_id"] == "812345600"
    assert rec["job_series"] == "1560" and rec["grade"] == "GS-12"
    assert rec["posted"] == "2026-11-20"
    assert "Develop models in Python and R." in rec["sentences"]
