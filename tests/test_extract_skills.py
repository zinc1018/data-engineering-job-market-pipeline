from src.extract.extract_skills import extract_matches


def test_extract_matches_finds_expected_skills():
    description = "Strong SQL, Python, Airflow, and AWS experience required."

    results = list(extract_matches(description))
    normalized_skills = {normalized for _, normalized, _ in results}

    assert "SQL" in normalized_skills
    assert "Python" in normalized_skills
    assert "Airflow" in normalized_skills
    assert "AWS" in normalized_skills


def test_extract_matches_returns_empty_for_no_skills():
    description = "Excellent communication and teamwork skills."

    results = list(extract_matches(description))

    assert results == []


def test_extract_matches_handles_case_insensitivity():
    description = "Experience with snowflake, DBT, and kAfKa."

    results = list(extract_matches(description))
    normalized_skills = {normalized for _, normalized, _ in results}

    assert "Snowflake" in normalized_skills
    assert "dbt" in normalized_skills
    assert "Kafka" in normalized_skills


def test_extract_matches_avoids_partial_word_false_positives():
    description = "We value teamwork, ownership, and growth."

    results = list(extract_matches(description))
    normalized_skills = {normalized for _, normalized, _ in results}

    assert "AWS" not in normalized_skills
