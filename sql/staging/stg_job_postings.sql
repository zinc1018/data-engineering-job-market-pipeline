-- Build staging job postings from raw input

TRUNCATE TABLE staging.stg_job_skills, staging.stg_job_postings CASCADE;

INSERT INTO staging.stg_job_postings (
    job_id,
    source,
    source_job_id,
    normalized_title,
    company,
    location,
    description,
    job_url,
    posted_date,
    collected_at
)
SELECT
    rjp.job_id,
    TRIM(rjp.source) AS source,
    NULLIF(TRIM(rjp.source_job_id), '') AS source_job_id,
    NULLIF(TRIM(rjp.title), '') AS normalized_title,
    NULLIF(TRIM(rjp.company), '') AS company,
    NULLIF(TRIM(rjp.location), '') AS location,
    NULLIF(TRIM(rjp.description), '') AS description,
    NULLIF(TRIM(rjp.job_url), '') AS job_url,
    rjp.posted_date,
    rjp.collected_at
FROM raw.raw_job_postings rjp;
