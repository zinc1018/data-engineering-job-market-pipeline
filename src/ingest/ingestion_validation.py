"""Validation helpers for fetched job posting payloads."""

from __future__ import annotations

from collections.abc import Iterable

from src.ingest.live_source_connector import JobPostingRecord


REQUIRED_FIELDS = ("source", "source_job_id", "title", "description", "job_url", "posted_date")


def validate_records(records: Iterable[JobPostingRecord]) -> list[JobPostingRecord]:
    validated = list(records)
    if not validated:
        raise ValueError("Fetched records are empty.")

    for index, record in enumerate(validated, start=1):
        missing = [field for field in REQUIRED_FIELDS if not getattr(record, field)]
        if missing:
            raise ValueError(
                f"Record {index} is missing required fields: {', '.join(missing)}"
            )

    return validated
