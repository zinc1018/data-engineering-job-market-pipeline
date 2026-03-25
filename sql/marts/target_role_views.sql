-- Views focused on engineering- and data-relevant roles only

CREATE OR REPLACE VIEW marts.target_dim_jobs AS
SELECT *
FROM marts.dim_jobs
WHERE is_target_role;

CREATE OR REPLACE VIEW marts.target_fct_job_skills AS
SELECT f.*
FROM marts.fct_job_skills f
JOIN marts.target_dim_jobs j ON f.job_id = j.job_id;
