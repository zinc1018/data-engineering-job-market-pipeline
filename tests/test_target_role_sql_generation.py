from pathlib import Path

from src.transform.generate_target_role_sql import render_target_role_views_sql


def test_target_role_sql_file_matches_generated_output():
    sql_path = Path("sql/marts/target_role_views.sql")
    assert sql_path.read_text(encoding="utf-8") == render_target_role_views_sql()
