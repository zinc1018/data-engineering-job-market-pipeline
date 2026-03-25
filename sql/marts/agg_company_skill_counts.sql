-- Build company-level skill counts for target engineering/data roles

TRUNCATE TABLE marts.agg_company_skill_counts;

INSERT INTO marts.agg_company_skill_counts (
    company,
    skill_name,
    skill_category,
    mention_count
)
SELECT
    j.company,
    d.skill_name,
    d.skill_category,
    COUNT(*) AS mention_count
FROM marts.fct_job_skills f
JOIN marts.dim_jobs j ON f.job_id = j.job_id
JOIN marts.dim_skills d ON f.skill_id = d.skill_id
WHERE j.is_target_role
GROUP BY j.company, d.skill_name, d.skill_category;
