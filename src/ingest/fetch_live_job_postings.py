"""Fetch live job postings from a connector and save them to JSON.

This starter script does not write directly to PostgreSQL. It saves fetched
records to a JSON file so source collection can be validated independently.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.ingest.live_source_connector import ExampleConnector


OUTPUT_PATH = Path("data/raw/live_job_postings.json")


def main() -> None:
    connector = ExampleConnector()
    records = connector.fetch_job_postings()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps([asdict(record) for record in records], indent=2),
        encoding="utf-8",
    )

    print(f"Saved {len(records)} live-source records to {OUTPUT_PATH}.")


if __name__ == "__main__":
    main()
