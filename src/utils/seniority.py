"""Helpers for classifying job seniority from posting text."""

from __future__ import annotations

import re


TITLE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Intern", re.compile(r"\b(intern|internship|apprentice)\b", re.IGNORECASE)),
    ("Executive", re.compile(r"\b(chief|cto|cio|vp|vice president)\b", re.IGNORECASE)),
    ("Director", re.compile(r"\bdirector\b", re.IGNORECASE)),
    ("Head", re.compile(r"\bhead\b", re.IGNORECASE)),
    ("Principal", re.compile(r"\bprincipal\b", re.IGNORECASE)),
    ("Staff", re.compile(r"\bstaff\b", re.IGNORECASE)),
    ("Lead", re.compile(r"\blead\b", re.IGNORECASE)),
    ("Senior", re.compile(r"\b(senior|sr\.?)\b", re.IGNORECASE)),
    ("Manager", re.compile(r"\bmanager\b", re.IGNORECASE)),
    ("Junior", re.compile(r"\b(junior|jr\.?|entry[\s-]?level)\b", re.IGNORECASE)),
]

DESCRIPTION_FALLBACK_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Intern", re.compile(r"\b(intern|internship|apprentice)\b", re.IGNORECASE)),
    ("Junior", re.compile(r"\b(entry[\s-]?level|new grad|new graduate|early career)\b", re.IGNORECASE)),
]


def classify_seniority(title: str | None, description: str | None = None) -> str:
    title_text = title or ""
    description_text = description or ""

    for seniority, pattern in TITLE_PATTERNS:
        if pattern.search(title_text):
            return seniority

    for seniority, pattern in DESCRIPTION_FALLBACK_PATTERNS:
        if pattern.search(description_text):
            return seniority

    return "Unspecified"
