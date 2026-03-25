from pathlib import Path


def test_dim_jobs_sql_persists_target_role_flag():
    sql = Path("sql/marts/dim_jobs.sql").read_text(encoding="utf-8")
    assert "is_target_role" in sql


def test_company_aggregation_sql_files_exist():
    assert Path("sql/marts/agg_company_skill_counts.sql").exists()
    assert Path("sql/marts/agg_company_seniority_counts.sql").exists()
