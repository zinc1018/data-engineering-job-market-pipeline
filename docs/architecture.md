# Architecture

## Overview
The Data Engineering Skills Pipeline collects job postings from public Greenhouse boards, stores raw posting data in PostgreSQL, extracts and normalizes technical skills, and transforms the data into analytics-ready tables for reporting and dashboard exports.

## Architecture Goals
- keep ingestion simple and reliable
- preserve raw source data for traceability
- use PostgreSQL as the primary system of record
- separate raw, staging, and analytical layers
- support both single-company and multi-company comparisons
- filter final analysis to engineering/data-relevant roles
- make the design easy to explain in interviews

## High-Level Flow
1. **Ingestion (Python)**
   - Fetch public Greenhouse board payloads for one or many companies
   - Normalize source fields into a raw job posting shape
   - Load raw records into PostgreSQL with upsert behavior

2. **Raw Layer (PostgreSQL)**
   - Store records with minimal transformation
   - Preserve source fields and raw payload where practical
   - Support auditability and reprocessing

3. **Skill Extraction (Python)**
   - Parse job descriptions
   - identify tool and skill keywords with regex-based matching
   - normalize synonyms into standard skill names
   - assign skill categories

4. **Staging Layer (SQL)**
   - standardize titles, company names, locations, and dates
   - clean raw values
   - isolate reusable transformations

5. **Mart Layer (SQL)**
   - create analytics-ready dimensions and fact tables
   - classify seniority from job titles
   - create target-role views for engineering/data jobs only
   - support dashboard queries such as top skills, tool demand, and seniority trends

6. **Analytics / Dashboard Layer**
   - export CSV summaries for dashboards
   - compare technical skill demand across companies
   - summarize role distribution and posting trends

## Recommended Components
### Application Layer
- Python ingestion scripts in `src/ingest/`
- Python extraction logic in `src/extract/`
- Python quality checks in `src/transform/`
- helper utilities in `src/utils/`

### Storage Layer
- PostgreSQL database
- raw tables for source data
- staging tables or views for cleanup
- mart tables or views for analytics

### Transformation Layer
- SQL scripts in `sql/staging/`
- SQL scripts in `sql/marts/`
- optional dbt adoption in a later phase

### Documentation Layer
- `PROJECT_PLAN.md` for scope and milestones
- `docs/data_dictionary.md` for table and column definitions
- `docs/agent_workflow.md` for delivery flow
- `docs/local_setup.md` for local execution

## Logical Data Layers
### Raw
Purpose:
- hold source records as collected
- minimize data loss and preserve reprocessing capability

Examples:
- `raw_job_postings`

### Staging
Purpose:
- clean and standardize raw source fields
- make downstream logic simpler and more consistent

Examples:
- `stg_job_postings`
- `stg_job_skills`

### Mart
Purpose:
- support final analysis and dashboards
- provide business-friendly entities and metrics

Examples:
- `dim_jobs`
- `dim_skills`
- `fct_job_skills`
- `agg_skill_counts_by_date`
- `target_dim_jobs`
- `target_fct_job_skills`

## Design Principles
- keep raw data as close to source as possible
- make transformations explicit and reproducible
- prefer clear schema names over clever ones
- separate extraction logic from SQL modeling logic
- optimize for explainability and portfolio value

## Initial MVP Design
For MVP, the project should support:
- public Greenhouse boards as live sources
- single-board and multi-board ingestion
- PostgreSQL raw table load with dedupe/upsert behavior
- skill extraction for major DE tools
- core mart tables plus target-role views
- data quality checks and dashboard exports

## Future Enhancements
- dbt project for transformation management
- better company and location normalization
- orchestration with Airflow or Prefect
- richer skill taxonomy and synonym coverage
- dashboard publishing
