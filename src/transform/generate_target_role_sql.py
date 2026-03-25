"""Generate SQL views for target engineering/data role filtering."""

from __future__ import annotations

from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT / "sql" / "marts" / "target_role_views.sql"


def render_target_role_views_sql() -> str:
    return """-- Views focused on engineering- and data-relevant roles only

CREATE OR REPLACE VIEW marts.target_dim_jobs AS
SELECT *
FROM marts.dim_jobs
WHERE is_target_role;

CREATE OR REPLACE VIEW marts.target_fct_job_skills AS
SELECT f.*
FROM marts.fct_job_skills f
JOIN marts.target_dim_jobs j ON f.job_id = j.job_id;
"""


def main() -> None:
    OUTPUT_PATH.write_text(render_target_role_views_sql(), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}.")


if __name__ == "__main__":
    main()
