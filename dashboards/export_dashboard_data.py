"""Export dashboard-friendly CSV summaries from PostgreSQL."""

from __future__ import annotations

import csv
import os
from pathlib import Path

import psycopg


OUTPUT_DIR = Path("dashboards/output")

QUERIES = {
    "top_skills.csv": """
        SELECT
            d.skill_name,
            d.skill_category,
            COUNT(*) AS mention_count
        FROM marts.fct_job_skills f
        JOIN marts.dim_skills d ON f.skill_id = d.skill_id
        GROUP BY d.skill_name, d.skill_category
        ORDER BY mention_count DESC, d.skill_name
    """,
    "top_skills_by_company.csv": """
        SELECT
            j.company,
            d.skill_name,
            d.skill_category,
            COUNT(*) AS mention_count
        FROM marts.fct_job_skills f
        JOIN marts.dim_jobs j ON f.job_id = j.job_id
        JOIN marts.dim_skills d ON f.skill_id = d.skill_id
        GROUP BY j.company, d.skill_name, d.skill_category
        ORDER BY j.company, mention_count DESC, d.skill_name
    """,
    "seniority_by_company.csv": """
        SELECT
            company,
            seniority,
            COUNT(*) AS job_count
        FROM marts.dim_jobs
        GROUP BY company, seniority
        ORDER BY company, job_count DESC, seniority
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


def export_query(cur: psycopg.Cursor, filename: str, sql: str) -> None:
    cur.execute(sql)
    rows = cur.fetchall()
    headers = [desc.name for desc in cur.description]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            for filename, sql in QUERIES.items():
                export_query(cur, filename, sql)

    print(f"Exported dashboard CSVs to {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()
