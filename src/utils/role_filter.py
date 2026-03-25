"""Helpers for identifying engineering- and data-relevant roles."""

from __future__ import annotations

import json
import re
from pathlib import Path


RULES_PATH = Path(__file__).resolve().parents[2] / "config" / "target_role_rules.json"


def load_role_rules() -> dict[str, list[str]]:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


ROLE_RULES = load_role_rules()

INCLUDE_PATTERNS = [re.compile(term, re.IGNORECASE) for term in ROLE_RULES["include_terms"]]
EXCLUDE_PATTERNS = [re.compile(term, re.IGNORECASE) for term in ROLE_RULES["exclude_terms"]]


def is_target_role(title: str | None) -> bool:
    if not title:
        return False

    if any(pattern.search(title) for pattern in EXCLUDE_PATTERNS):
        return False

    return any(pattern.search(title) for pattern in INCLUDE_PATTERNS)
