"""Starter ingestion script for loading raw job postings into PostgreSQL.

This script is intentionally simple for MVP use.
Expected input: a JSON file containing a list of job posting objects.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import psycopg


DEFAULT_INPUT_PATH = Path("data/raw/greenhouse_job_postings.json")


def get_connection() -> psycopg.Connection:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg.connect(database_url)

    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "data_engineering_skills_pipeline"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
    )


def load_job_postings(input_path: Path) -> list[dict[str, Any]]:
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of job posting objects.")

    return data


def insert_raw_job_postings(records: list[dict[str, Any]]) -> int:
    insert_sql = """
        INSERT INTO raw.raw_job_postings (
            source,
            source_job_id,
            title,
            company,
            location,
            description,
            job_url,
            posted_date,
            raw_payload
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (source, source_job_id) WHERE source_job_id IS NOT NULL DO UPDATE
        SET title = EXCLUDED.title,
            company = EXCLUDED.company,
            location = EXCLUDED.location,
            description = EXCLUDED.description,
            job_url = EXCLUDED.job_url,
            posted_date = EXCLUDED.posted_date,
            raw_payload = EXCLUDED.raw_payload
    """

    inserted = 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            for record in records:
                cur.execute(
                    insert_sql,
                    (
                        record.get("source"),
                        record.get("source_job_id"),
                        record.get("title"),
                        record.get("company"),
                        record.get("location"),
                        record.get("description"),
                        record.get("job_url"),
                        record.get("posted_date"),
                        json.dumps(record),
                    ),
                )
                inserted += cur.rowcount

        conn.commit()

    return inserted


def main() -> None:
    input_path = Path(os.getenv("RAW_JOB_POSTINGS_FILE", DEFAULT_INPUT_PATH))

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. "
            "Create a sample JSON file before running the loader."
        )

    records = load_job_postings(input_path)
    inserted = insert_raw_job_postings(records)
    print(f"Inserted {inserted} raw job posting records into PostgreSQL.")


if __name__ == "__main__":
    main()
