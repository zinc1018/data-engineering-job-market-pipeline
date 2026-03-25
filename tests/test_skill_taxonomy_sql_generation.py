from pathlib import Path

from src.transform.generate_dim_skills_sql import render_dim_skills_sql


def test_dim_skills_sql_matches_generated_taxonomy_seed():
    sql_path = Path("sql/marts/dim_skills.sql")
    assert sql_path.read_text(encoding="utf-8") == render_dim_skills_sql()
