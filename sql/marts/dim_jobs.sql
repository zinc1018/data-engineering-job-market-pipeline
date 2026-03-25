-- Build mart job dimension from staging data

TRUNCATE TABLE marts.fct_job_skills, marts.dim_jobs CASCADE;

INSERT INTO marts.dim_jobs (
    job_id,
    source,
    title,
    company,
    location,
    seniority,
    posted_date,
    collected_at
)
SELECT
    sjp.job_id,
    sjp.source,
    sjp.normalized_title AS title,
    sjp.company,
    sjp.location,
    CASE
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])(intern|internship|apprentice)([^a-z]|$)' THEN 'Intern'
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])(chief|cto|cio|vp|vice president)([^a-z]|$)' THEN 'Executive'
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])director([^a-z]|$)' THEN 'Director'
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])head([^a-z]|$)' THEN 'Head'
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])principal([^a-z]|$)' THEN 'Principal'
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])staff([^a-z]|$)' THEN 'Staff'
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])lead([^a-z]|$)' THEN 'Lead'
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])(senior|sr\.?)([^a-z]|$)' THEN 'Senior'
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])manager([^a-z]|$)' THEN 'Manager'
        WHEN COALESCE(sjp.normalized_title, '') ~* '(^|[^a-z])(junior|jr\.?|entry[ -]?level)([^a-z]|$)' THEN 'Junior'
        WHEN COALESCE(sjp.description, '') ~* '(^|[^a-z])(intern|internship|apprentice)([^a-z]|$)' THEN 'Intern'
        WHEN COALESCE(sjp.description, '') ~* '(^|[^a-z])(entry[ -]?level|new grad|new graduate|early career)([^a-z]|$)' THEN 'Junior'
        ELSE 'Unspecified'
    END AS seniority,
    sjp.posted_date,
    sjp.collected_at
FROM staging.stg_job_postings sjp;
