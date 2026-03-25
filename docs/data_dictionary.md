# Data Dictionary

This document defines the initial PostgreSQL objects used in the Data Engineering Skills Pipeline project.

## Schemas

### `raw`
Purpose:
- stores source records with minimal transformation
- preserves original values for traceability and reprocessing

### `staging`
Purpose:
- stores cleaned and standardized intermediate data
- prepares records for analytics modeling

### `marts`
Purpose:
- stores analytics-ready dimensions, facts, and aggregate views
- supports dashboards and reporting

---

## Tables

## `raw.raw_job_postings`
Purpose:
- store job postings exactly or almost exactly as collected from source systems

| Column | Type | Description |
|---|---|---|
| `job_id` | `BIGSERIAL` | Surrogate primary key for each collected job posting record. |
| `source` | `VARCHAR(100)` | Source system name, such as a job board or API provider. |
| `source_job_id` | `VARCHAR(255)` | Source-specific job identifier when available. |
| `title` | `TEXT` | Raw job title from the source. |
| `company` | `TEXT` | Raw company name from the source. |
| `location` | `TEXT` | Raw job location text. |
| `description` | `TEXT` | Raw job description text. |
| `job_url` | `TEXT` | Original job posting URL. |
| `posted_date` | `DATE` | Job posting date when available from the source. |
| `collected_at` | `TIMESTAMP` | Timestamp when the pipeline collected the record. |
| `raw_payload` | `JSONB` | Full source payload or source-specific raw metadata. |

Business notes:
- This is the system-of-record raw layer.
- Keep transformations out of this table whenever possible.

---

## `raw.ingestion_runs`
Purpose:
- store operational fetch history for live ingestion runs

| Column | Type | Description |
|---|---|---|
| `ingestion_run_id` | `BIGSERIAL` | Surrogate primary key for each ingestion run. |
| `source_type` | `VARCHAR(100)` | Source family, such as `greenhouse`. |
| `board_tokens` | `JSONB` | Source tokens included in the run. |
| `record_count` | `INTEGER` | Number of records fetched in the run. |
| `output_path` | `TEXT` | Local JSON file path written by the fetch step. |
| `fetched_at` | `TIMESTAMPTZ` | Timestamp when the run completed. |
| `status` | `VARCHAR(50)` | Run status, currently `success`. |
| `metadata` | `JSONB` | Full run log payload for traceability. |

Business notes:
- This table supports operational debugging and lightweight ingestion observability.
- File-based JSONL logs may still exist locally, but PostgreSQL is the authoritative run log.

---

## `staging.stg_job_postings`
Purpose:
- standardize raw posting fields for downstream use

| Column | Type | Description |
|---|---|---|
| `job_id` | `BIGINT` | Job key inherited from `raw.raw_job_postings`. |
| `source` | `VARCHAR(100)` | Source system name. |
| `source_job_id` | `VARCHAR(255)` | Source-specific identifier. |
| `title` | `TEXT` | Standardized or cleaned title. |
| `company` | `TEXT` | Standardized company name. |
| `location` | `TEXT` | Standardized location text. |
| `description` | `TEXT` | Cleaned description used for extraction. |
| `job_url` | `TEXT` | Job URL. |
| `posted_date` | `DATE` | Posting date. |
| `collected_at` | `TIMESTAMP` | Collection timestamp. |

Business notes:
- This layer removes simple inconsistencies and makes extraction/modeling easier.
- This table should remain close enough to raw that transformations are easy to audit.

---

## `staging.stg_job_skills`
Purpose:
- store extracted and normalized skill signals before dimensional modeling

| Column | Type | Description |
|---|---|---|
| `job_id` | `BIGINT` | Job identifier tied to the posting. |
| `matched_text` | `TEXT` | Raw or normalized text matched in the description. |
| `normalized_skill_name` | `VARCHAR(255)` | Standardized skill name, such as `Python` or `Airflow`. |
| `skill_category` | `VARCHAR(100)` | Skill grouping such as Programming, Cloud, or Orchestration. |
| `match_method` | `VARCHAR(100)` | Method used to identify the skill, such as keyword match or regex rule. |
| `extracted_at` | `TIMESTAMP` | Timestamp when extraction occurred. |

Business notes:
- This table is an intermediate layer between text extraction and final dimensional modeling.
- Multiple raw expressions may map to one normalized skill.

---

## `marts.dim_skills`
Purpose:
- define the standardized skill catalog used in analytics

| Column | Type | Description |
|---|---|---|
| `skill_id` | `BIGSERIAL` | Surrogate primary key for the skill. |
| `skill_name` | `VARCHAR(255)` | Standardized skill name. |
| `skill_category` | `VARCHAR(100)` | Skill category used for reporting. |

Business notes:
- One record per normalized skill.
- Used to support consistent analytics across sources and wording differences.

---

## `marts.dim_jobs`
Purpose:
- provide an analytics-friendly job entity

| Column | Type | Description |
|---|---|---|
| `job_id` | `BIGINT` | Job identifier from the raw/staging layer. |
| `source` | `VARCHAR(100)` | Source system name. |
| `title` | `TEXT` | Cleaned job title. |
| `company` | `TEXT` | Cleaned company name. |
| `location` | `TEXT` | Cleaned location. |
| `seniority` | `VARCHAR(100)` | Derived seniority classification such as Junior, Mid, Senior, or Lead. |
| `is_target_role` | `BOOLEAN` | Whether the modeled job is classified as engineering/data relevant for downstream comparisons. |
| `posted_date` | `DATE` | Posting date. |
| `collected_at` | `TIMESTAMP` | Collection timestamp. |

Business notes:
- This table supports job-level slicing and filtering in analytics.
- Seniority may be derived from title heuristics in the MVP.

---

## `marts.fct_job_skills`
Purpose:
- link jobs and standardized skills for analysis

| Column | Type | Description |
|---|---|---|
| `job_id` | `BIGINT` | Foreign key to `marts.dim_jobs`. |
| `skill_id` | `BIGINT` | Foreign key to `marts.dim_skills`. |
| `matched_text` | `TEXT` | Text fragment that triggered the skill match. |
| `match_method` | `VARCHAR(100)` | Method used to identify the skill. |
| `created_at` | `TIMESTAMP` | Timestamp when the fact row was created. |

Business notes:
- This is the core fact table for skill-demand analysis.
- One row represents a job requiring or mentioning a standardized skill.

---

## `marts.agg_company_skill_counts`
Purpose:
- summarize target-role skill demand by company

| Column | Type | Description |
|---|---|---|
| `company` | `TEXT` | Company name from `marts.dim_jobs`. |
| `skill_name` | `VARCHAR(255)` | Standardized skill name. |
| `skill_category` | `VARCHAR(100)` | Skill category used for reporting. |
| `mention_count` | `INTEGER` | Number of target-role fact rows for the company and skill. |

Business notes:
- This summary table avoids repeated aggregation logic for company comparison queries.
- Counts only include rows where `is_target_role = true`.

---

## `marts.agg_company_seniority_counts`
Purpose:
- summarize target-role job counts by company and seniority

| Column | Type | Description |
|---|---|---|
| `company` | `TEXT` | Company name from `marts.dim_jobs`. |
| `seniority` | `VARCHAR(100)` | Derived seniority classification. |
| `job_count` | `INTEGER` | Number of target-role jobs in the bucket. |

Business notes:
- This summary table supports company-level role distribution analysis.
- Counts only include rows where `is_target_role = true`.

---

## Views

## `marts.agg_skill_counts_by_date`
Purpose:
- summarize skill frequency over time for trend analysis and dashboards

Output columns:
- `posted_date`
- `skill_name`
- `skill_category`
- `job_skill_count`

Business notes:
- Supports charting top skills by date.
- Can be extended later to include source, seniority, or location dimensions.

---

## Initial KPI Mapping
- **Top requested skills** -> `marts.fct_job_skills` joined to `marts.dim_skills`
- **Cloud tool demand** -> filtered `skill_category = 'Cloud'`
- **Orchestration demand** -> filtered `skill_category = 'Orchestration'`
- **Role title distribution** -> `marts.dim_jobs`
- **Skill trend over time** -> `marts.agg_skill_counts_by_date`
- **Company skill comparison** -> `marts.agg_company_skill_counts`
- **Company seniority comparison** -> `marts.agg_company_seniority_counts`
