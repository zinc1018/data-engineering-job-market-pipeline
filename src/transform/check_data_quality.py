"""Run simple data quality checks against the PostgreSQL pipeline output."""

from __future__ import annotations

import os
import sys

import psycopg


CHECKS = {
    "raw_missing_source_job_id": """
        SELECT COUNT(*) FROM raw.raw_job_postings
        WHERE source_job_id IS NULL OR source_job_id = ''
    """,
    "staging_job_count_matches_raw": """
        SELECT
            (SELECT COUNT(*) FROM raw.raw_job_postings) -
            (SELECT COUNT(*) FROM staging.stg_job_postings)
    """,
    "fact_orphans_vs_dim_jobs": """
        SELECT COUNT(*) FROM marts.fct_job_skills f
        LEFT JOIN marts.dim_jobs j ON f.job_id = j.job_id
        WHERE j.job_id IS NULL
    """,
    "fact_orphans_vs_dim_skills": """
        SELECT COUNT(*) FROM marts.fct_job_skills f
        LEFT JOIN marts.dim_skills s ON f.skill_id = s.skill_id
        WHERE s.skill_id IS NULL
    """,
    "dim_jobs_missing_posted_date": """
        SELECT COUNT(*) FROM marts.dim_jobs
        WHERE posted_date IS NULL
    """,
}


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


def main() -> None:
    failures: list[tuple[str, int]] = []

    with get_connection() as conn:
        with conn.cursor() as cur:
            for check_name, sql in CHECKS.items():
                cur.execute(sql)
                value = int(cur.fetchone()[0])
                print(f"{check_name}: {value}")
                if value != 0:
                    failures.append((check_name, value))

    if failures:
        print("Data quality checks failed:", file=sys.stderr)
        for check_name, value in failures:
            print(f" - {check_name}: {value}", file=sys.stderr)
        raise SystemExit(1)

    print("All data quality checks passed.")


if __name__ == "__main__":
    main()
