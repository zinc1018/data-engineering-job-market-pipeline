"""Generate SQL views for target engineering/data role filtering."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = ROOT / "config" / "target_role_rules.json"
OUTPUT_PATH = ROOT / "sql" / "marts" / "target_role_views.sql"


def load_role_rules() -> dict[str, list[str]]:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


def build_regex(terms: list[str]) -> str:
    return "(" + "|".join(terms) + ")"


def render_target_role_views_sql() -> str:
    rules = load_role_rules()
    include_regex = build_regex(rules["include_terms"])
    exclude_regex = build_regex(rules["exclude_terms"])

    return f"""-- Views focused on engineering- and data-relevant roles only

CREATE OR REPLACE VIEW marts.target_dim_jobs AS
SELECT *
FROM marts.dim_jobs
WHERE
    title ~* '{include_regex}'
    AND title !~* '{exclude_regex}';

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
