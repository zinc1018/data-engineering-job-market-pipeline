"""Fetch job postings from a Greenhouse board and save them to JSON.

Usage example:
    BOARD_TOKEN=acme python src/ingest/fetch_greenhouse_job_postings.py
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime, UTC
from pathlib import Path

from src.ingest.greenhouse_connector import GreenhouseConnector
from src.ingest.ingestion_logging import log_ingestion_run
from src.ingest.ingestion_validation import validate_records


DEFAULT_OUTPUT_PATH = Path("data/raw/greenhouse_job_postings.json")
DEFAULT_LOG_PATH = Path("data/processed/ingestion_runs.jsonl")


def main() -> None:
    board_token = os.getenv("BOARD_TOKEN")
    if not board_token:
        raise ValueError("BOARD_TOKEN environment variable is required.")

    output_path = Path(os.getenv("GREENHOUSE_OUTPUT_FILE", DEFAULT_OUTPUT_PATH))
    log_path = Path(os.getenv("INGESTION_LOG_FILE", DEFAULT_LOG_PATH))

    connector = GreenhouseConnector(board_token=board_token)
    records = validate_records(connector.fetch_job_postings())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([asdict(record) for record in records], indent=2),
        encoding="utf-8",
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "source_type": "greenhouse",
        "board_tokens": [board_token],
        "record_count": len(records),
        "output_path": str(output_path),
        "fetched_at": datetime.now(UTC).isoformat(),
        "status": "success",
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
    log_ingestion_run(log_entry)

    print(
        f"Saved {len(records)} Greenhouse records for board '{board_token}' "
        f"to {output_path}. Logged run to PostgreSQL and {log_path}."
    )


if __name__ == "__main__":
    main()
