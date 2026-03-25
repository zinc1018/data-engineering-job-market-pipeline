-- Build job-skill fact table from extracted staging rows and skill dimension

TRUNCATE TABLE marts.fct_job_skills;

INSERT INTO marts.fct_job_skills (
    job_id,
    skill_id,
    matched_text,
    match_method
)
SELECT DISTINCT
    sjs.job_id,
    ds.skill_id,
    sjs.matched_text,
    COALESCE(sjs.match_method, 'keyword_match') AS match_method
FROM staging.stg_job_skills sjs
JOIN marts.dim_skills ds
    ON LOWER(sjs.normalized_skill_name) = LOWER(ds.skill_name)
JOIN marts.dim_jobs dj
    ON sjs.job_id = dj.job_id;

\i sql/marts/target_role_views.sql
