import json
from pathlib import Path

from src.ingest.load_raw_job_postings import load_job_postings


def test_load_job_postings_reads_list_of_records(tmp_path: Path):
    input_file = tmp_path / "jobs.json"
    payload = [
        {"source": "sample", "title": "Data Engineer"},
        {"source": "sample", "title": "Senior Data Engineer"},
    ]
    input_file.write_text(json.dumps(payload), encoding="utf-8")

    records = load_job_postings(input_file)

    assert isinstance(records, list)
    assert len(records) == 2
    assert records[0]["title"] == "Data Engineer"


def test_load_job_postings_raises_for_non_list_payload(tmp_path: Path):
    input_file = tmp_path / "jobs.json"
    input_file.write_text(json.dumps({"bad": "payload"}), encoding="utf-8")

    try:
        load_job_postings(input_file)
        assert False, "Expected ValueError for non-list payload"
    except ValueError as exc:
        assert "list of job posting objects" in str(exc)
