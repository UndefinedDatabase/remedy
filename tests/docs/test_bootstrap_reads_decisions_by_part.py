"""Session bootstrap reads `.agent/decisions.md` by part, never whole (R-1029).

Both bootstrap texts — the self-drive protocol's Phase 0 and the planner prompt's §1 — say
which part: the last five `## DECISION` entries and those the feature file or handoff names.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _section(path: str, start: str, end: str) -> str:
    text = (REPO_ROOT / path).read_text(encoding="utf-8")
    return text[text.index(start):text.index(end, text.index(start))]


def _normalized(text: str) -> str:
    return " ".join(text.split())


def test_phase_0_reads_decisions_by_part():
    phase0 = _normalized(_section("docs/agents/self_drive_protocol.md", "## Phase 0", "## Phase 1"))
    assert "`.agent/decisions.md` is NEVER read whole at session start" in phase0
    assert "last five `## DECISION` entries" in phase0
    assert "the active feature file or the handoff names" in phase0


def test_the_planner_bootstrap_reads_decisions_by_part():
    bootstrap = _normalized(_section("docs/agents/planner_reviewer_prompt.md", "## 1. Bootstrap", "## 2."))
    assert "`.agent/decisions.md` is never read whole" in bootstrap
    assert "last five `## DECISION` entries" in bootstrap
