from dataclasses import replace

import pytest

from src.ingest.ingestion_validation import validate_records
from src.ingest.live_source_connector import JobPostingRecord


def sample_record() -> JobPostingRecord:
    return JobPostingRecord(
        source="greenhouse:acme",
        source_job_id="123",
        title="Data Engineer",
        company="Acme",
        location="Remote",
        description="SQL and Python required.",
        job_url="https://example.com/jobs/123",
        posted_date="2026-03-25",
    )


def test_validate_records_accepts_valid_records():
    records = validate_records([sample_record()])
    assert len(records) == 1


def test_validate_records_rejects_empty_record_list():
    with pytest.raises(ValueError, match="empty"):
        validate_records([])


def test_validate_records_rejects_missing_required_fields():
    broken = replace(sample_record(), posted_date=None)

    with pytest.raises(ValueError, match="posted_date"):
        validate_records([broken])
