.PHONY: help up down logs venv install init_db schema fetch_greenhouse fetch_multi_greenhouse load_raw stage extract marts quality dashboard_exports smoke run_all test

-include .env
export

PYTHON := .venv/bin/python
PSQL := psql -d $(PGDATABASE)

help:
	@echo "Available targets:"
	@echo "  up               - start local PostgreSQL via Docker Compose (optional)"
	@echo "  down             - stop local PostgreSQL Docker container"
	@echo "  logs             - tail PostgreSQL Docker logs"
	@echo "  venv             - create the local virtual environment"
	@echo "  install          - install Python dependencies into .venv"
	@echo "  init_db          - apply the schema to the current PostgreSQL database"
	@echo "  schema           - apply initial PostgreSQL schema"
	@echo "  fetch_greenhouse - fetch Greenhouse job postings to data/raw/"
	@echo "  fetch_multi_greenhouse - fetch multiple Greenhouse boards to one JSON file"
	@echo "  load_raw         - load raw job postings into PostgreSQL"
	@echo "  stage            - build staging job postings table"
	@echo "  extract          - extract skills into staging table"
	@echo "  marts            - build mart tables"
	@echo "  quality          - run data quality checks against PostgreSQL"
	@echo "  dashboard_exports - export dashboard-friendly CSV summaries"
	@echo "  smoke            - run a small end-to-end pipeline check from sample_job_postings.json"
	@echo "  run_all          - run the full MVP pipeline"
	@echo "  test             - run unit tests"

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f postgres

venv:
	python3 -m venv .venv

install: venv
	$(PYTHON) -m pip install -r requirements.txt

init_db:
	$(MAKE) schema

schema:
	$(PSQL) -f sql/staging/schema.sql

fetch_greenhouse:
	PYTHONPATH=. $(PYTHON) src/ingest/fetch_greenhouse_job_postings.py

fetch_multi_greenhouse:
	PYTHONPATH=. $(PYTHON) src/ingest/fetch_multi_greenhouse_job_postings.py

load_raw:
	PYTHONPATH=. $(PYTHON) src/ingest/load_raw_job_postings.py

stage:
	$(PSQL) -f sql/staging/stg_job_postings.sql

extract:
	PYTHONPATH=. $(PYTHON) src/extract/extract_skills.py

marts:
	$(PSQL) -f sql/marts/dim_jobs.sql
	$(PSQL) -f sql/marts/dim_skills.sql
	$(PSQL) -f sql/marts/fct_job_skills.sql
	$(PSQL) -f sql/marts/agg_company_skill_counts.sql
	$(PSQL) -f sql/marts/agg_company_seniority_counts.sql

quality:
	PYTHONPATH=. $(PYTHON) src/transform/check_data_quality.py

dashboard_exports:
	PYTHONPATH=. $(PYTHON) dashboards/export_dashboard_data.py

smoke:
	PYTHONPATH=. $(PYTHON) src/transform/run_smoke_pipeline.py

run_all: init_db fetch_greenhouse load_raw stage extract marts quality dashboard_exports

test:
	$(PYTHON) -m pytest -q
