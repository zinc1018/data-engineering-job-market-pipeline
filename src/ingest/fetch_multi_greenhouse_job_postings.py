"""Fetch job postings from multiple Greenhouse boards into one JSON file.

Usage example:
    BOARD_TOKENS=airtable,stripe python3 src/ingest/fetch_multi_greenhouse_job_postings.py
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path

from src.ingest.greenhouse_connector import GreenhouseConnector


DEFAULT_OUTPUT_PATH = Path("data/raw/greenhouse_job_postings_multi.json")


def parse_board_tokens(value: str | None) -> list[str]:
    if not value:
        raise ValueError("BOARD_TOKENS environment variable is required.")

    tokens = [token.strip() for token in value.split(",") if token.strip()]
    if not tokens:
        raise ValueError("BOARD_TOKENS must include at least one board token.")
    return tokens


def main() -> None:
    board_tokens = parse_board_tokens(os.getenv("BOARD_TOKENS"))
    output_path = Path(os.getenv("GREENHOUSE_OUTPUT_FILE", DEFAULT_OUTPUT_PATH))

    records = []
    for token in board_tokens:
        connector = GreenhouseConnector(board_token=token)
        records.extend(connector.fetch_job_postings())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([asdict(record) for record in records], indent=2),
        encoding="utf-8",
    )

    print(
        f"Saved {len(records)} Greenhouse records across {len(board_tokens)} boards "
        f"to {output_path}."
    )


if __name__ == "__main__":
    main()
