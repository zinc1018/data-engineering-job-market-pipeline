from src.ingest.greenhouse_connector import GreenhouseConnector


def test_map_job_maps_expected_fields():
    connector = GreenhouseConnector(board_token="acme")

    job = {
        "id": 123,
        "title": "Data Engineer",
        "absolute_url": "https://boards.greenhouse.io/acme/jobs/123",
        "location": {"name": "Remote"},
        "content": "SQL and Python required.",
        "metadata": [{"name": "Posted", "value": "2026-03-24"}],
    }

    record = connector._map_job(job)

    assert record.source == "greenhouse:acme"
    assert record.source_job_id == "123"
    assert record.title == "Data Engineer"
    assert record.company == "acme"
    assert record.location == "Remote"
    assert record.description == "SQL and Python required."
    assert record.job_url == "https://boards.greenhouse.io/acme/jobs/123"
    assert record.posted_date == "2026-03-24"
    assert record.company == "acme"


def test_map_job_falls_back_to_first_published_when_metadata_missing():
    connector = GreenhouseConnector(board_token="acme")

    job = {
        "id": 456,
        "title": "Data Engineer",
        "absolute_url": "https://boards.greenhouse.io/acme/jobs/456",
        "location": {"name": "Remote"},
        "content": "SQL and Python required.",
        "metadata": None,
        "company_name": "Acme Corp",
        "first_published": "2026-03-24T10:15:00-04:00",
    }

    record = connector._map_job(job)

    assert record.company == "Acme Corp"
    assert record.posted_date == "2026-03-24"
