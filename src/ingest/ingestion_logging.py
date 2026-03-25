"""Helpers for persisting ingestion run logs."""

from __future__ import annotations

import json
import os
from typing import Any

import psycopg


def get_connection() -> psycopg.Connection:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg.connect(database_url)

    return psycopg.connect(
        host=os.getenv("PGHOST") or None,
        port=os.getenv("PGPORT") or None,
        dbname=os.getenv("PGDATABASE", "data_engineering_skills_pipeline"),
        user=os.getenv("PGUSER") or None,
        password=os.getenv("PGPASSWORD") or None,
    )


def log_ingestion_run(log_entry: dict[str, Any]) -> None:
    insert_sql = """
        INSERT INTO raw.ingestion_runs (
            source_type,
            board_tokens,
            record_count,
            output_path,
            fetched_at,
            status,
            metadata
        )
        VALUES (%s, %s::jsonb, %s, %s, %s, %s, %s::jsonb)
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                insert_sql,
                (
                    log_entry["source_type"],
                    json.dumps(log_entry["board_tokens"]),
                    log_entry["record_count"],
                    log_entry["output_path"],
                    log_entry["fetched_at"],
                    log_entry["status"],
                    json.dumps(log_entry),
                ),
            )
        conn.commit()
