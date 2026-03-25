"""Shared skill taxonomy for extraction and marts seeding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict


class SkillEntry(TypedDict):
    skill_name: str
    skill_category: str
    patterns: list[str]


TAXONOMY_PATH = Path(__file__).resolve().parents[2] / "config" / "skill_taxonomy.json"


def load_skill_taxonomy() -> list[SkillEntry]:
    return json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
