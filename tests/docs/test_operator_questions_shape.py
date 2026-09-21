"""The shape of every entry in `.agent/operator_questions.md`.

Operator amendment amend0921-operator-feedback rule 3 (2026-09-21) orders every
text written for the operator in complete, plain sentences. This test pins the
part of that rule a test can check: each `### Q` entry's body carries the four
labelled paragraphs amend0911-feedback rule C names, and no body line is a bare
reference token (a feature, finding or slice id standing alone). A file holding
only its header, with no entry, passes.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
QUESTIONS = REPO / ".agent" / "operator_questions.md"

REQUIRED_LABELS = (
    "**What needs deciding.**",
    "**Why it matters.**",
    "**My recommendation.**",
    "**What happens if you say nothing.**",
)
ENTRY_HEADING_RE = re.compile(r"^### Q\d+\b")
BARE_TOKEN_RE = re.compile(r"^(F\d+|R-\d{4}|T\d{3})\s*$")


def _entries(text: str) -> list[tuple[str, list[str]]]:
    """Each `### Q` entry as its heading and its body lines, up to the next `### ` heading."""
    entries: list[tuple[str, list[str]]] = []
    body: list[str] | None = None
    for line in text.splitlines():
        if ENTRY_HEADING_RE.match(line):
            body = []
            entries.append((line, body))
        elif line.startswith("### "):
            body = None
        elif body is not None:
            body.append(line)
    return entries


def shape_problems(text: str) -> list[str]:
    problems: list[str] = []
    for heading, body in _entries(text):
        joined = "\n".join(body)
        for label in REQUIRED_LABELS:
            if label not in joined:
                problems.append(f"{heading!r} lacks the label {label}")
        for line in body:
            if BARE_TOKEN_RE.match(line.strip()):
                problems.append(f"{heading!r} has a bare reference line {line.strip()!r}")
    return problems


def test_every_operator_question_has_the_four_labels_and_no_bare_token_line() -> None:
    assert shape_problems(QUESTIONS.read_text(encoding="utf-8")) == []
