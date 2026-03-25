# Local Setup

## Prerequisites
- Python 3.11+
- PostgreSQL server and `psql`
- `python3-venv`

## Environment
Create a local `.env` from `.env.example`.

The validated local flow for this repository uses:
- a local PostgreSQL database named `data_engineering_skills_pipeline`
- a local role that can connect from your Unix user or configured env vars
- the project `.venv`

## Fast Start
From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
psql -d data_engineering_skills_pipeline -f sql/staging/schema.sql
```

If your shell does not provide `python`, the Make targets already use `python3`.

## Single-Board Run
```bash
BOARD_TOKEN=airtable PYTHONPATH=. .venv/bin/python src/ingest/fetch_greenhouse_job_postings.py
PYTHONPATH=. .venv/bin/python src/ingest/load_raw_job_postings.py
psql -d data_engineering_skills_pipeline -f sql/staging/stg_job_postings.sql
PYTHONPATH=. .venv/bin/python src/extract/extract_skills.py
psql -d data_engineering_skills_pipeline -f sql/marts/dim_jobs.sql
psql -d data_engineering_skills_pipeline -f sql/marts/dim_skills.sql
psql -d data_engineering_skills_pipeline -f sql/marts/fct_job_skills.sql
```

## Multi-Board Run
```bash
BOARD_TOKENS=airtable,stripe GREENHOUSE_OUTPUT_FILE=data/raw/greenhouse_job_postings_multi.json \
  PYTHONPATH=. .venv/bin/python src/ingest/fetch_multi_greenhouse_job_postings.py
RAW_JOB_POSTINGS_FILE=data/raw/greenhouse_job_postings_multi.json PYTHONPATH=. .venv/bin/python src/ingest/load_raw_job_postings.py
psql -d data_engineering_skills_pipeline -f sql/staging/stg_job_postings.sql
PYTHONPATH=. .venv/bin/python src/extract/extract_skills.py
psql -d data_engineering_skills_pipeline -f sql/marts/dim_jobs.sql
psql -d data_engineering_skills_pipeline -f sql/marts/dim_skills.sql
psql -d data_engineering_skills_pipeline -f sql/marts/fct_job_skills.sql
```

## Validation
Run tests:
```bash
.venv/bin/python -m pytest -q
```

Run the isolated integration smoke path:
```bash
make smoke
```

Run quality checks:
```bash
PYTHONPATH=. .venv/bin/python src/transform/check_data_quality.py
```

Export dashboard-ready CSVs:
```bash
PYTHONPATH=. .venv/bin/python dashboards/export_dashboard_data.py
```

## Notes
- `load_raw_job_postings.py` now upserts refreshed raw fields on conflict.
- company comparison queries are most useful after `target_role_views.sql` has been created through the marts build.
- `make smoke` uses a temporary PostgreSQL database and does not modify the main working dataset.
- if you rely on environment variables instead of local socket auth, set them in `.env` before running the Python entrypoints.
