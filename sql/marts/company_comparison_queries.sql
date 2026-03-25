-- Cross-company comparison queries for Greenhouse job boards

-- 1. Job counts by company
SELECT
    company,
    COUNT(*) AS job_count
FROM marts.dim_jobs
WHERE job_id IN (SELECT job_id FROM marts.target_dim_jobs)
GROUP BY company
ORDER BY job_count DESC, company;

-- 2. Top skills by company
SELECT
    j.company,
    d.skill_name,
    d.skill_category,
    COUNT(*) AS mention_count
FROM marts.fct_job_skills f
JOIN marts.target_dim_jobs j ON f.job_id = j.job_id
JOIN marts.dim_skills d ON f.skill_id = d.skill_id
GROUP BY j.company, d.skill_name, d.skill_category
ORDER BY j.company, mention_count DESC, d.skill_name;

-- 3. Seniority distribution by company
SELECT
    company,
    seniority,
    COUNT(*) AS job_count
FROM marts.dim_jobs
WHERE job_id IN (SELECT job_id FROM marts.target_dim_jobs)
GROUP BY company, seniority
ORDER BY company, job_count DESC, seniority;
