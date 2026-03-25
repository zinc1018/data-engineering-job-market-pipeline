"""Helpers for identifying engineering- and data-relevant roles."""

from __future__ import annotations

import re


INCLUDE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bdata engineer\b",
        r"\banalytics engineer\b",
        r"\bdata analyst\b",
        r"\bsoftware engineer\b",
        r"\bsecurity engineer\b",
        r"\bplatform engineer\b",
        r"\binfrastructure engineer\b",
        r"\bengineering manager\b",
        r"\bweb developer\b",
        r"\bdesign developer\b",
        r"\bdeveloper\b",
        r"\bengineer\b",
        r"\bengineering\b",
        r"\bbackend\b",
        r"\bfrontend\b",
        r"\bfull stack\b",
        r"\bdevops\b",
        r"\bmachine learning\b",
        r"\bml engineer\b",
        r"\bdata science\b",
        r"\banalytics\b",
    )
]

EXCLUDE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\baccount executive\b",
        r"\bbusiness development\b",
        r"\bcustomer success\b",
        r"\brenewals?\b",
        r"\bsales\b",
        r"\bsolutions consultant\b",
        r"\bprogram manager\b",
        r"\bproduct manager\b",
        r"\bfinance\b",
        r"\bprocurement\b",
        r"\bcontracts?\b",
        r"\bmarketing\b",
        r"\bpeople systems\b",
        r"\bdemand gen\b",
        r"\btechnical account manager\b",
        r"\baccount manager\b",
        r"\boperations\b",
    )
]


def is_target_role(title: str | None) -> bool:
    if not title:
        return False

    if any(pattern.search(title) for pattern in EXCLUDE_PATTERNS):
        return False

    return any(pattern.search(title) for pattern in INCLUDE_PATTERNS)
