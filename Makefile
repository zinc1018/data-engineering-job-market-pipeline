.PHONY: help up down logs install init_db schema fetch_greenhouse fetch_multi_greenhouse load_raw stage extract marts quality dashboard_exports run_all test

-include .env
export

help:
	@echo "Available targets:"
	@echo "  up               - start local PostgreSQL via Docker Compose"
	@echo "  down             - stop local PostgreSQL"
	@echo "  logs             - tail PostgreSQL container logs"
	@echo "  install          - install Python dependencies"
	@echo "  init_db          - wait for PostgreSQL and apply the schema"
	@echo "  schema           - apply initial PostgreSQL schema"
	@echo "  fetch_greenhouse - fetch Greenhouse job postings to data/raw/"
	@echo "  fetch_multi_greenhouse - fetch multiple Greenhouse boards to one JSON file"
	@echo "  load_raw         - load raw job postings into PostgreSQL"
	@echo "  stage            - build staging job postings table"
	@echo "  extract          - extract skills into staging table"
	@echo "  marts            - build mart tables"
	@echo "  quality          - run data quality checks against PostgreSQL"
	@echo "  dashboard_exports - export dashboard-friendly CSV summaries"
	@echo "  run_all          - run the full MVP pipeline"
	@echo "  test             - run unit tests"

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f postgres

install:
	python3 -m pip install -r requirements.txt

init_db: up
	@echo "Waiting for PostgreSQL to become healthy..."
	docker compose exec -T postgres sh -c 'until pg_isready -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" >/dev/null 2>&1; do sleep 1; done'
	$(MAKE) schema

schema:
	PGPASSWORD=$(PGPASSWORD) psql -h $(PGHOST) -p $(PGPORT) -U $(PGUSER) -d $(PGDATABASE) -f sql/staging/schema.sql

fetch_greenhouse:
	python3 src/ingest/fetch_greenhouse_job_postings.py

fetch_multi_greenhouse:
	python3 src/ingest/fetch_multi_greenhouse_job_postings.py

load_raw:
	python3 src/ingest/load_raw_job_postings.py

stage:
	PGPASSWORD=$(PGPASSWORD) psql -h $(PGHOST) -p $(PGPORT) -U $(PGUSER) -d $(PGDATABASE) -f sql/staging/stg_job_postings.sql

extract:
	python3 src/extract/extract_skills.py

marts:
	PGPASSWORD=$(PGPASSWORD) psql -h $(PGHOST) -p $(PGPORT) -U $(PGUSER) -d $(PGDATABASE) -f sql/marts/dim_jobs.sql
	PGPASSWORD=$(PGPASSWORD) psql -h $(PGHOST) -p $(PGPORT) -U $(PGUSER) -d $(PGDATABASE) -f sql/marts/dim_skills.sql
	PGPASSWORD=$(PGPASSWORD) psql -h $(PGHOST) -p $(PGPORT) -U $(PGUSER) -d $(PGDATABASE) -f sql/marts/fct_job_skills.sql

quality:
	python3 src/transform/check_data_quality.py

dashboard_exports:
	python3 dashboards/export_dashboard_data.py

run_all: init_db fetch_greenhouse load_raw stage extract marts

test:
	python3 -m pytest -q
