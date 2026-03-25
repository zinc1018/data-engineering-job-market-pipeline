import json
from pathlib import Path


def test_sample_job_postings_fixture_is_valid():
    path = Path("data/raw/sample_job_postings.json")
    rows = json.loads(path.read_text(encoding="utf-8"))

    assert len(rows) == 3
    assert {row["source_job_id"] for row in rows} == {"de-001", "de-002", "de-003"}
    assert all(row["posted_date"] for row in rows)
    assert all("description" in row and row["description"] for row in rows)


def test_sample_job_postings_fixture_contains_expected_skills():
    path = Path("data/raw/sample_job_postings.json")
    rows = json.loads(path.read_text(encoding="utf-8"))
    descriptions = " ".join(row["description"] for row in rows).lower()

    for skill in ("sql", "python", "airflow", "aws", "spark", "kafka", "dbt", "snowflake"):
        assert skill in descriptions
