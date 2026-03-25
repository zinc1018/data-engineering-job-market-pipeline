-- Views focused on engineering- and data-relevant roles only

CREATE OR REPLACE VIEW marts.target_dim_jobs AS
SELECT *
FROM marts.dim_jobs
WHERE
    title ~* '(data engineer|analytics engineer|data analyst|software engineer|security engineer|platform engineer|infrastructure engineer|engineering manager|web developer|design developer|developer|engineer|engineering|backend|frontend|full stack|devops|machine learning|ml engineer|data science|analytics)'
    AND title !~* '(account executive|business development|customer success|renewals?|sales|solutions consultant|program manager|product manager|finance|procurement|contracts?|marketing|people systems|demand gen|technical account manager|account manager|operations)';

CREATE OR REPLACE VIEW marts.target_fct_job_skills AS
SELECT f.*
FROM marts.fct_job_skills f
JOIN marts.target_dim_jobs j ON f.job_id = j.job_id;
