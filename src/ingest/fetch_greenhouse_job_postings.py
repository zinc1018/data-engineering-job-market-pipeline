"""Fetch job postings from a Greenhouse board and save them to JSON.

Usage example:
    BOARD_TOKEN=acme python src/ingest/fetch_greenhouse_job_postings.py
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path

from src.ingest.greenhouse_connector import GreenhouseConnector


DEFAULT_OUTPUT_PATH = Path("data/raw/greenhouse_job_postings.json")


def main() -> None:
    board_token = os.getenv("BOARD_TOKEN")
    if not board_token:
        raise ValueError("BOARD_TOKEN environment variable is required.")

    output_path = Path(os.getenv("GREENHOUSE_OUTPUT_FILE", DEFAULT_OUTPUT_PATH))

    connector = GreenhouseConnector(board_token=board_token)
    records = connector.fetch_job_postings()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([asdict(record) for record in records], indent=2),
        encoding="utf-8",
    )

    print(
        f"Saved {len(records)} Greenhouse records for board '{board_token}' "
        f"to {output_path}."
    )


if __name__ == "__main__":
    main()
