"""Starter Greenhouse connector for Data Engineering Skills Pipeline.

This connector fetches jobs from the public Greenhouse boards API for a single
company board token and maps them into the project's normalized raw shape.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import requests

from src.ingest.live_source_connector import JobPostingRecord


BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"


@dataclass
class GreenhouseConnector:
    board_token: str

    @property
    def source_name(self) -> str:
        return f"greenhouse:{self.board_token}"

    def fetch_job_postings(self) -> list[JobPostingRecord]:
        url = BASE_URL.format(board_token=self.board_token)
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        payload = response.json()

        jobs = payload.get("jobs", [])
        return [self._map_job(job) for job in jobs]

    def _map_job(self, job: dict[str, Any]) -> JobPostingRecord:
        metadata = self._metadata_map(job.get("metadata", []))
        location = (job.get("location") or {}).get("name")
        description = job.get("content")
        posted_date = self._extract_posted_date(metadata)

        return JobPostingRecord(
            source=self.source_name,
            source_job_id=str(job.get("id")) if job.get("id") is not None else None,
            title=job.get("title"),
            company=job.get("company_name") or self.board_token,
            location=location,
            description=description,
            job_url=job.get("absolute_url"),
            posted_date=posted_date or self._extract_posted_date_from_job(job),
        )

    @staticmethod
    def _metadata_map(metadata_rows: list[dict[str, Any]] | None) -> dict[str, Any]:
        mapped: dict[str, Any] = {}
        for row in metadata_rows or []:
            name = row.get("name")
            value = row.get("value")
            if name:
                mapped[name] = value
        return mapped

    @staticmethod
    def _extract_posted_date(metadata: dict[str, Any]) -> str | None:
        for key in ("Posted", "posted", "posted_date", "date"):
            value = metadata.get(key)
            if value:
                return str(value)
        return None

    @staticmethod
    def _extract_posted_date_from_job(job: dict[str, Any]) -> str | None:
        for key in ("first_published", "updated_at"):
            value = job.get(key)
            if not value:
                continue
            try:
                return datetime.fromisoformat(value).date().isoformat()
            except (TypeError, ValueError):
                continue
        return None
