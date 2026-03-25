-- Initial PostgreSQL schema for Data Engineering Skills Pipeline

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;

-- Raw job postings collected from source systems
CREATE TABLE IF NOT EXISTS raw.raw_job_postings (
    job_id BIGSERIAL PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    source_job_id VARCHAR(255),
    title TEXT,
    company TEXT,
    location TEXT,
    description TEXT,
    job_url TEXT,
    posted_date DATE,
    collected_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    raw_payload JSONB
);

CREATE INDEX IF NOT EXISTS idx_raw_job_postings_source ON raw.raw_job_postings(source);
CREATE INDEX IF NOT EXISTS idx_raw_job_postings_posted_date ON raw.raw_job_postings(posted_date);
CREATE UNIQUE INDEX IF NOT EXISTS uq_raw_job_postings_source_job_id
    ON raw.raw_job_postings(source, source_job_id)
    WHERE source_job_id IS NOT NULL;

-- Ingestion run history for operational visibility
CREATE TABLE IF NOT EXISTS raw.ingestion_runs (
    ingestion_run_id BIGSERIAL PRIMARY KEY,
    source_type VARCHAR(100) NOT NULL,
    board_tokens JSONB NOT NULL,
    record_count INTEGER NOT NULL,
    output_path TEXT NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(50) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_ingestion_runs_fetched_at
    ON raw.ingestion_runs(fetched_at);
CREATE INDEX IF NOT EXISTS idx_ingestion_runs_source_type
    ON raw.ingestion_runs(source_type);

-- Staging table for cleaned job posting fields
CREATE TABLE IF NOT EXISTS staging.stg_job_postings (
    job_id BIGINT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    source_job_id VARCHAR(255),
    normalized_title TEXT,
    company TEXT,
    location TEXT,
    description TEXT,
    job_url TEXT,
    posted_date DATE,
    collected_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT fk_stg_job_postings_raw_job
        FOREIGN KEY (job_id) REFERENCES raw.raw_job_postings(job_id)
);

-- Extracted skills before final dimensional modeling
CREATE TABLE IF NOT EXISTS staging.stg_job_skills (
    job_id BIGINT NOT NULL,
    matched_text TEXT NOT NULL,
    normalized_skill_name VARCHAR(255),
    skill_category VARCHAR(100),
    match_method VARCHAR(100) NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id, matched_text, match_method),
    CONSTRAINT fk_stg_job_skills_stg_job
        FOREIGN KEY (job_id) REFERENCES staging.stg_job_postings(job_id)
);

CREATE INDEX IF NOT EXISTS idx_stg_job_skills_norm_skill
    ON staging.stg_job_skills(normalized_skill_name);

-- Final skill dimension
CREATE TABLE IF NOT EXISTS marts.dim_skills (
    skill_id BIGSERIAL PRIMARY KEY,
    skill_name VARCHAR(255) NOT NULL UNIQUE,
    skill_category VARCHAR(100) NOT NULL
);

-- Final job dimension
CREATE TABLE IF NOT EXISTS marts.dim_jobs (
    job_id BIGINT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    title TEXT,
    company TEXT,
    location TEXT,
    seniority VARCHAR(100),
    is_target_role BOOLEAN NOT NULL DEFAULT FALSE,
    posted_date DATE,
    collected_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT fk_dim_jobs_stg_job
        FOREIGN KEY (job_id) REFERENCES staging.stg_job_postings(job_id)
);

ALTER TABLE marts.dim_jobs
    ADD COLUMN IF NOT EXISTS is_target_role BOOLEAN NOT NULL DEFAULT FALSE;

-- Fact table linking jobs and skills
CREATE TABLE IF NOT EXISTS marts.fct_job_skills (
    job_id BIGINT NOT NULL,
    skill_id BIGINT NOT NULL,
    matched_text TEXT,
    match_method VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id, skill_id),
    CONSTRAINT fk_fct_job_skills_job
        FOREIGN KEY (job_id) REFERENCES marts.dim_jobs(job_id),
    CONSTRAINT fk_fct_job_skills_skill
        FOREIGN KEY (skill_id) REFERENCES marts.dim_skills(skill_id)
);

CREATE INDEX IF NOT EXISTS idx_fct_job_skills_skill_id ON marts.fct_job_skills(skill_id);

-- Company-level summary marts
CREATE TABLE IF NOT EXISTS marts.agg_company_skill_counts (
    company TEXT NOT NULL,
    skill_name VARCHAR(255) NOT NULL,
    skill_category VARCHAR(100) NOT NULL,
    mention_count INTEGER NOT NULL,
    PRIMARY KEY (company, skill_name)
);

CREATE TABLE IF NOT EXISTS marts.agg_company_seniority_counts (
    company TEXT NOT NULL,
    seniority VARCHAR(100) NOT NULL,
    job_count INTEGER NOT NULL,
    PRIMARY KEY (company, seniority)
);

-- Example aggregate view for analytics
CREATE OR REPLACE VIEW marts.agg_skill_counts_by_date AS
SELECT
    dj.posted_date,
    ds.skill_name,
    ds.skill_category,
    COUNT(*) AS job_skill_count
FROM marts.fct_job_skills fjs
JOIN marts.dim_jobs dj ON fjs.job_id = dj.job_id
JOIN marts.dim_skills ds ON fjs.skill_id = ds.skill_id
GROUP BY dj.posted_date, ds.skill_name, ds.skill_category;
