"""Starter live-source connector interface.

This module provides a simple structure for adding real job data sources
without tightly coupling source collection to database loading logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class JobPostingRecord:
    source: str
    source_job_id: str | None
    title: str | None
    company: str | None
    location: str | None
    description: str | None
    job_url: str | None
    posted_date: str | None


class LiveSourceConnector(Protocol):
    def fetch_job_postings(self) -> list[JobPostingRecord]:
        """Return job postings from a live source."""


class ExampleConnector:
    """Placeholder connector.

    Replace this with a real connector for an approved source.
    """

    source_name = "example_live_source"

    def fetch_job_postings(self) -> list[JobPostingRecord]:
        return [
            JobPostingRecord(
                source=self.source_name,
                source_job_id="example-001",
                title="Data Engineer",
                company="Example Co",
                location="Remote",
                description="SQL, Python, Airflow, and AWS experience required.",
                job_url="https://example.com/jobs/example-001",
                posted_date="2026-03-24",
            )
        ]
