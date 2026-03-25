from src.utils.seniority import classify_seniority


def test_classify_seniority_detects_title_levels():
    assert classify_seniority("Senior Data Engineer") == "Senior"
    assert classify_seniority("Staff Data Engineer") == "Staff"
    assert classify_seniority("Lead Platform Engineer") == "Lead"
    assert classify_seniority("Director of Data Engineering") == "Director"


def test_classify_seniority_uses_description_fallback():
    assert classify_seniority("Data Engineer", "This is an entry-level role.") == "Junior"
    assert classify_seniority("Platform Engineer", "Ideal for internship candidates.") == "Intern"


def test_classify_seniority_returns_unspecified_when_no_signal():
    assert classify_seniority("Data Engineer", "Build reliable pipelines.") == "Unspecified"


def test_classify_seniority_ignores_verb_noise_in_description():
    assert classify_seniority("Data Engineer", "You will lead roadmap execution.") == "Unspecified"
    assert classify_seniority("Software Engineer", "Help manage stakeholder expectations.") == "Unspecified"
