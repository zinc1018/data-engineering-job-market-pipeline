-- Build company-level seniority counts for target engineering/data roles

TRUNCATE TABLE marts.agg_company_seniority_counts;

INSERT INTO marts.agg_company_seniority_counts (
    company,
    seniority,
    job_count
)
SELECT
    company,
    seniority,
    COUNT(*) AS job_count
FROM marts.dim_jobs
WHERE is_target_role
GROUP BY company, seniority;
