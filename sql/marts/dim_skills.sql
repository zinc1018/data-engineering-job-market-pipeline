-- Seed normalized skills dimension for MVP

INSERT INTO marts.dim_skills (skill_name, skill_category)
VALUES
    ('Python', 'Programming'),
    ('SQL', 'Programming'),
    ('Scala', 'Programming'),
    ('PostgreSQL', 'Warehousing'),
    ('Spark', 'Data Processing'),
    ('Hadoop', 'Data Processing'),
    ('Airflow', 'Orchestration'),
    ('Prefect', 'Orchestration'),
    ('AWS', 'Cloud'),
    ('Azure', 'Cloud'),
    ('GCP', 'Cloud'),
    ('Snowflake', 'Warehousing'),
    ('Redshift', 'Warehousing'),
    ('BigQuery', 'Warehousing'),
    ('Kafka', 'Streaming'),
    ('Docker', 'DevOps'),
    ('Kubernetes', 'DevOps'),
    ('dbt', 'Transformation')
ON CONFLICT (skill_name) DO UPDATE
SET skill_category = EXCLUDED.skill_category;
