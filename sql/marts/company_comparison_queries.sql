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
    company,
    skill_name,
    skill_category,
    mention_count
FROM marts.agg_company_skill_counts
ORDER BY company, mention_count DESC, skill_name;

-- 3. Seniority distribution by company
SELECT
    company,
    seniority,
    job_count
FROM marts.agg_company_seniority_counts
ORDER BY company, job_count DESC, seniority;
