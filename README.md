# Data Engineering Skills Pipeline

An end-to-end data engineering portfolio project that collects job postings from public Greenhouse boards, extracts required skills, transforms raw text into analytics-ready PostgreSQL tables, and surfaces market signals through SQL queries and dashboard exports.

## Project Goal
Build a pipeline that helps answer:
- which skills appear most often in data engineering job postings?
- which cloud and orchestration tools are in demand?
- how do role expectations vary across postings?

## Current MVP Status
- working local PostgreSQL pipeline from fetch to marts
- Greenhouse ingestion for single-board and multi-board runs
- persisted target-role classification for engineering and data-relevant jobs
- seniority classification and skill extraction logic
- company-level summary marts for skills and seniority
- data quality checks against live mart tables and modeled summaries
- isolated end-to-end smoke validation against a temporary PostgreSQL database
- dashboard-ready CSV exports
- unit tests passing

## Current Results
Latest validated live run:
- `558` total jobs loaded across `Airtable` and `Stripe`
- `135` target engineering/data jobs after role filtering
- data quality checks passing
- test suite passing

Filtered target-role counts:
- `Stripe`: `119`
- `Airtable`: `16`

Filtered top skill signals:
- `Airtable`: `SQL`, `Kubernetes`, `Python`, `AWS`
- `Stripe`: `Python`, `AWS`, `Scala`, `SQL`, `Kubernetes`, `Spark`

This is enough to show cross-company comparison, skill extraction, mart modeling, and quality validation on live public job-board data.

## MVP Stack
- Python for ingestion and parsing
- PostgreSQL for raw and analytics storage
- SQL for staging and mart transformations
- Pandas for lightweight data wrangling
- pytest for basic test coverage

This repository is intentionally optimized for job-ready fundamentals. The MVP uses PostgreSQL rather than DuckDB so the project demonstrates a database platform that appears more often in production data engineering environments.

## Project Structure
```text
data_engineering_skills_pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── ingest/
│   │   ├── fetch_greenhouse_job_postings.py
│   │   ├── fetch_multi_greenhouse_job_postings.py
│   │   ├── greenhouse_connector.py
│   │   └── load_raw_job_postings.py
│   ├── extract/
│   │   └── extract_skills.py
│   ├── transform/
│   │   └── check_data_quality.py
│   └── utils/
│       ├── role_filter.py
│       └── seniority.py
├── sql/
│   ├── staging/
│   │   ├── schema.sql
│   │   └── stg_job_postings.sql
│   └── marts/
│       ├── dim_jobs.sql
│       ├── dim_skills.sql
│       ├── fct_job_skills.sql
│       ├── analytics_queries.sql
│       ├── company_comparison_queries.sql
│       └── target_role_views.sql
├── dashboards/
│   ├── export_dashboard_data.py
│   └── output/
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── local_setup.md
│   └── agent_workflow.md
├── tests/
├── Makefile
├── .env.example
├── requirements.txt
├── PROJECT_PLAN.md
└── AGENTS.md
```

## Local Development
For local PostgreSQL setup and Greenhouse ingestion, see `docs/local_setup.md`.

Quick start:

```bash
make install
psql -d data_engineering_skills_pipeline -f sql/staging/schema.sql
BOARD_TOKENS=airtable,stripe GREENHOUSE_OUTPUT_FILE=data/raw/greenhouse_job_postings_multi.json \
  PYTHONPATH=. .venv/bin/python src/ingest/fetch_multi_greenhouse_job_postings.py
RAW_JOB_POSTINGS_FILE=data/raw/greenhouse_job_postings_multi.json PYTHONPATH=. .venv/bin/python src/ingest/load_raw_job_postings.py
psql -d data_engineering_skills_pipeline -f sql/staging/stg_job_postings.sql
PYTHONPATH=. .venv/bin/python src/extract/extract_skills.py
psql -d data_engineering_skills_pipeline -f sql/marts/dim_jobs.sql
psql -d data_engineering_skills_pipeline -f sql/marts/dim_skills.sql
psql -d data_engineering_skills_pipeline -f sql/marts/fct_job_skills.sql
PYTHONPATH=. .venv/bin/python src/transform/check_data_quality.py
PYTHONPATH=. .venv/bin/python dashboards/export_dashboard_data.py
```

The repository works with Docker if available, but the current validated flow uses a local PostgreSQL server and the project `.venv`.

## Validation
Unit tests:

```bash
make test
```

Isolated end-to-end smoke run:

```bash
make smoke
```

`make smoke` creates a temporary PostgreSQL database, loads the sample fixture, runs the full raw-to-marts pipeline, checks data-quality invariants, prints row counts, and drops the temporary database without touching the main working dataset.

## Live Workflow
### Single board
```bash
BOARD_TOKEN=airtable PYTHONPATH=. .venv/bin/python src/ingest/fetch_greenhouse_job_postings.py
PYTHONPATH=. .venv/bin/python src/ingest/load_raw_job_postings.py
```

### Multiple boards
```bash
BOARD_TOKENS=airtable,stripe GREENHOUSE_OUTPUT_FILE=data/raw/greenhouse_job_postings_multi.json \
  PYTHONPATH=. .venv/bin/python src/ingest/fetch_multi_greenhouse_job_postings.py
RAW_JOB_POSTINGS_FILE=data/raw/greenhouse_job_postings_multi.json PYTHONPATH=. .venv/bin/python src/ingest/load_raw_job_postings.py
```

## Analytics Queries
Sample analytical queries are included in:
- `sql/marts/analytics_queries.sql`
- `sql/marts/company_comparison_queries.sql`

These cover:
- top requested skills
- filtered engineering/data-role comparisons by company
- seniority distributions
- skill demand over time

## Target-Role Filtering
The repository now keeps all raw jobs but filters comparisons and dashboard-facing analysis to engineering- and data-relevant roles through:
- `marts.dim_jobs.is_target_role`
- `marts.target_dim_jobs`
- `marts.target_fct_job_skills`

This avoids sales and non-technical roles dominating company comparisons on mixed Greenhouse boards.

## Summary Marts
The mart layer now includes persisted company-level summaries for target roles:
- `marts.agg_company_skill_counts`
- `marts.agg_company_seniority_counts`

These make company comparisons easier to query and easier to explain in interviews than repeating the same aggregation logic ad hoc.

## Dashboard Outputs
Dashboard-ready CSV exports are written to:
- `dashboards/output/top_skills.csv`
- `dashboards/output/top_skills_by_company.csv`
- `dashboards/output/seniority_by_company.csv`

## Portfolio Value
This project demonstrates:
- Python-based data ingestion
- PostgreSQL-based storage and querying
- SQL data modeling
- analytics-oriented schema design
- practical text parsing and normalization
- multi-source comparison logic
- data quality validation
- dashboard export generation
- documentation and end-to-end pipeline thinking
