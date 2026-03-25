"""Starter skill extraction script for Data Engineering Skills Pipeline.

This MVP version uses a simple keyword dictionary and loads results into
staging.stg_job_skills.
"""

from __future__ import annotations

import os
import re
from typing import Iterable

import psycopg


SKILL_MAP = {
    "python": ("Python", "Programming"),
    "sql": ("SQL", "Programming"),
    "scala": ("Scala", "Programming"),
    "spark": ("Spark", "Data Processing"),
    "hadoop": ("Hadoop", "Data Processing"),
    "airflow": ("Airflow", "Orchestration"),
    "prefect": ("Prefect", "Orchestration"),
    "aws": ("AWS", "Cloud"),
    "azure": ("Azure", "Cloud"),
    "gcp": ("GCP", "Cloud"),
    "snowflake": ("Snowflake", "Warehousing"),
    "redshift": ("Redshift", "Warehousing"),
    "bigquery": ("BigQuery", "Warehousing"),
    "kafka": ("Kafka", "Streaming"),
    "docker": ("Docker", "DevOps"),
    "kubernetes": ("Kubernetes", "DevOps"),
    "dbt": ("dbt", "Transformation"),
}

SKILL_PATTERNS = {
    raw_keyword: re.compile(rf"(?<![a-z0-9]){re.escape(raw_keyword)}(?![a-z0-9])")
    for raw_keyword in SKILL_MAP
}


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


def extract_matches(description: str) -> Iterable[tuple[str, str, str]]:
    text = (description or "").lower()
    for raw_keyword, (normalized_skill, skill_category) in SKILL_MAP.items():
        if SKILL_PATTERNS[raw_keyword].search(text):
            yield raw_keyword, normalized_skill, skill_category


def main() -> None:
    truncate_sql = "TRUNCATE TABLE staging.stg_job_skills;"
    select_sql = "SELECT job_id, description FROM staging.stg_job_postings;"
    insert_sql = """
        INSERT INTO staging.stg_job_skills (
            job_id,
            matched_text,
            normalized_skill_name,
            skill_category,
            match_method
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (job_id, matched_text, match_method) DO UPDATE
        SET normalized_skill_name = EXCLUDED.normalized_skill_name,
            skill_category = EXCLUDED.skill_category,
            match_method = EXCLUDED.match_method,
            extracted_at = CURRENT_TIMESTAMP
    """

    inserted = 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(truncate_sql)
            cur.execute(select_sql)
            rows = cur.fetchall()

            for job_id, description in rows:
                for matched_text, normalized_skill_name, skill_category in extract_matches(description):
                    cur.execute(
                        insert_sql,
                        (job_id, matched_text, normalized_skill_name, skill_category, "keyword_match"),
                    )
                    inserted += 1

        conn.commit()

    print(f"Inserted or updated {inserted} extracted skill rows.")


if __name__ == "__main__":
    main()
