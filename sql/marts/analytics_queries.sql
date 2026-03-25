-- Sample analytics queries for Data Engineering Skills Pipeline

-- 1. Top requested skills
SELECT
    ds.skill_name,
    ds.skill_category,
    COUNT(*) AS mention_count
FROM marts.fct_job_skills fjs
JOIN marts.target_fct_job_skills tfjs
    ON fjs.job_id = tfjs.job_id AND fjs.skill_id = tfjs.skill_id
JOIN marts.dim_skills ds ON fjs.skill_id = ds.skill_id
GROUP BY ds.skill_name, ds.skill_category
ORDER BY mention_count DESC, ds.skill_name;

-- 2. Top cloud skills
SELECT
    ds.skill_name,
    COUNT(*) AS mention_count
FROM marts.fct_job_skills fjs
JOIN marts.target_fct_job_skills tfjs
    ON fjs.job_id = tfjs.job_id AND fjs.skill_id = tfjs.skill_id
JOIN marts.dim_skills ds ON fjs.skill_id = ds.skill_id
WHERE ds.skill_category = 'Cloud'
GROUP BY ds.skill_name
ORDER BY mention_count DESC, ds.skill_name;

-- 3. Top orchestration skills
SELECT
    ds.skill_name,
    COUNT(*) AS mention_count
FROM marts.fct_job_skills fjs
JOIN marts.target_fct_job_skills tfjs
    ON fjs.job_id = tfjs.job_id AND fjs.skill_id = tfjs.skill_id
JOIN marts.dim_skills ds ON fjs.skill_id = ds.skill_id
WHERE ds.skill_category = 'Orchestration'
GROUP BY ds.skill_name
ORDER BY mention_count DESC, ds.skill_name;

-- 4. Job counts by seniority
SELECT
    seniority,
    COUNT(*) AS job_count
FROM marts.target_dim_jobs
GROUP BY seniority
ORDER BY job_count DESC, seniority;

-- 5. Skill demand over time
SELECT
    posted_date,
    skill_name,
    skill_category,
    job_skill_count
FROM marts.agg_skill_counts_by_date
WHERE posted_date IN (SELECT DISTINCT posted_date FROM marts.target_dim_jobs)
ORDER BY posted_date, job_skill_count DESC, skill_name;

-- 6. Most common skills by seniority
SELECT
    dj.seniority,
    ds.skill_name,
    COUNT(*) AS mention_count
FROM marts.fct_job_skills fjs
JOIN marts.target_dim_jobs dj ON fjs.job_id = dj.job_id
JOIN marts.dim_skills ds ON fjs.skill_id = ds.skill_id
GROUP BY dj.seniority, ds.skill_name
ORDER BY dj.seniority, mention_count DESC, ds.skill_name;
