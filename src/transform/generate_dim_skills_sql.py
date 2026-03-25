"""Generate dim_skills seed SQL from the shared skill taxonomy."""

from __future__ import annotations

from pathlib import Path

from src.utils.skill_taxonomy import load_skill_taxonomy


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT / "sql" / "marts" / "dim_skills.sql"


def render_dim_skills_sql() -> str:
    rows = []
    for entry in load_skill_taxonomy():
        skill_name = entry["skill_name"].replace("'", "''")
        skill_category = entry["skill_category"].replace("'", "''")
        rows.append(f"    ('{skill_name}', '{skill_category}')")

    values = ",\n".join(rows)

    return f"""-- Seed normalized skills dimension for MVP

INSERT INTO marts.dim_skills (skill_name, skill_category)
VALUES
{values}
ON CONFLICT (skill_name) DO UPDATE
SET skill_category = EXCLUDED.skill_category;
"""


def main() -> None:
    OUTPUT_PATH.write_text(render_dim_skills_sql(), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}.")


if __name__ == "__main__":
    main()
