"""Remedy has no native frontend (operator order amend1016-stabilization, DECISION amend1016 D1).

F309 "Cockpit v2" is withdrawn, not done, and nothing may make Rule A5 propose it or another
cockpit rebuild again. These checks read the real STATUS.md through the same index the
next-feature selector uses.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from packages.orchestration.roadmap_index import build_index, proposed_feature

REPO = Path(__file__).resolve().parents[2]
STATUS = REPO / "docs" / "roadmap" / "STATUS.md"

#: Titles that would rebuild Remedy's own face.
_FACE_RE = re.compile(r"\bcockpit\b.*\b(design|shell|v2|rebuild)\b", re.IGNORECASE)


def _packages() -> tuple[str, str]:
    text = STATUS.read_text(encoding="utf-8")
    head, _, parked = text.partition("## Package 2")
    return head, parked


def test_rule_a5_never_proposes_f309():
    feature, _reason = proposed_feature(build_index(REPO))
    assert feature is None or feature.id != "F309"


def test_f309_is_withdrawn_in_package_two():
    active, parked = _packages()
    assert "F309" not in active
    line = next(ln for ln in parked.splitlines() if " F309 — " in ln)
    assert line.startswith("- [!] F309 — ")
    assert "withdrawn" in line


def test_no_open_package_one_line_asks_for_a_cockpit_design():
    active, _ = _packages()
    open_lines = [ln for ln in active.splitlines() if re.match(r"^- \[[ ~]\] F\d{3} — ", ln)]
    offenders = [ln for ln in open_lines if _FACE_RE.search(ln)]
    assert offenders == []


def test_no_native_face_is_tracked():
    tracked = subprocess.run(
        ["git", "ls-files", "--", "apps/ui"], cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout.split()
    assert tracked == []
