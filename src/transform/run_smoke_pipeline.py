"""Run a small end-to-end smoke pipeline against PostgreSQL."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import psycopg


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_FILE = ROOT / "data" / "raw" / "sample_job_postings.json"
DEFAULT_SMOKE_DB = "data_engineering_skills_pipeline_smoke"


def run_step(command: list[str], env: dict[str, str]) -> None:
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def pg_cli_args(env: dict[str, str], dbname: str | None = None) -> list[str]:
    args: list[str] = []
    if env.get("PGHOST"):
        args.extend(["-h", env["PGHOST"]])
    if env.get("PGPORT"):
        args.extend(["-p", env["PGPORT"]])
    if env.get("PGUSER"):
        args.extend(["-U", env["PGUSER"]])
    if dbname:
        args.extend(["-d", dbname])
    return args


def get_connection(env: dict[str, str]) -> psycopg.Connection:
    database_url = env.get("DATABASE_URL")
    if database_url:
        return psycopg.connect(database_url)

    return psycopg.connect(
        host=env.get("PGHOST") or None,
        port=env.get("PGPORT") or None,
        dbname=env.get("PGDATABASE", "data_engineering_skills_pipeline"),
        user=env.get("PGUSER") or None,
        password=env.get("PGPASSWORD") or None,
    )


def print_row_counts(env: dict[str, str]) -> None:
    sql = """
        SELECT 'raw.raw_job_postings', COUNT(*) FROM raw.raw_job_postings
        UNION ALL
        SELECT 'staging.stg_job_postings', COUNT(*) FROM staging.stg_job_postings
        UNION ALL
        SELECT 'staging.stg_job_skills', COUNT(*) FROM staging.stg_job_skills
        UNION ALL
        SELECT 'marts.dim_jobs', COUNT(*) FROM marts.dim_jobs
        UNION ALL
        SELECT 'marts.fct_job_skills', COUNT(*) FROM marts.fct_job_skills
        ORDER BY 1
    """

    with get_connection(env) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            for table_name, row_count in cur.fetchall():
                print(f"{table_name}: {row_count}")


def main() -> None:
    python = os.getenv("SMOKE_PYTHON", str(ROOT / ".venv" / "bin" / "python"))
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    env["RAW_JOB_POSTINGS_FILE"] = str(SAMPLE_FILE)
    smoke_db = os.getenv("SMOKE_DATABASE", DEFAULT_SMOKE_DB)
    maintenance_db = os.getenv("PGMAINTENANCE_DB", "postgres")
    env["PGDATABASE"] = smoke_db

    dropdb_cmd = ["dropdb", "--if-exists", *pg_cli_args(env), smoke_db]
    createdb_cmd = ["createdb", *pg_cli_args(env), smoke_db]
    psql_cmd = ["psql", *pg_cli_args(env, smoke_db)]

    run_step(dropdb_cmd, env)
    run_step(createdb_cmd, env)

    try:
        run_step(["psql", *pg_cli_args(env, smoke_db), "-f", "sql/staging/schema.sql"], env)
        run_step([python, "src/ingest/load_raw_job_postings.py"], env)
        run_step(["psql", *pg_cli_args(env, smoke_db), "-f", "sql/staging/stg_job_postings.sql"], env)
        run_step([python, "src/extract/extract_skills.py"], env)
        run_step(["psql", *pg_cli_args(env, smoke_db), "-f", "sql/marts/dim_jobs.sql"], env)
        run_step(["psql", *pg_cli_args(env, smoke_db), "-f", "sql/marts/dim_skills.sql"], env)
        run_step(["psql", *pg_cli_args(env, smoke_db), "-f", "sql/marts/fct_job_skills.sql"], env)
        run_step([python, "src/transform/check_data_quality.py"], env)
        print_row_counts(env)
    finally:
        cleanup_env = env.copy()
        cleanup_env["PGDATABASE"] = maintenance_db
        run_step(["dropdb", "--if-exists", *pg_cli_args(cleanup_env), smoke_db], cleanup_env)


if __name__ == "__main__":
    main()
