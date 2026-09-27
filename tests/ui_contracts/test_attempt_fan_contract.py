"""F029 R5, DECISION F029 D5 — the Attempts list mounts where the decision
says, touches no network of its own, and the canvas chip calls the one
function that decides the `attempt <n>` word. Mirrors
`test_task_version_contract.py`'s own checks for the Versions list. No DOM
harness exists, so this is read as source, exactly as that file reads
`TaskVersionList.tsx`.
"""
from __future__ import annotations

from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"

POPOVER = UI_SRC / "components" / "detail" / "DetailPopover.tsx"
ATTEMPT_LIST = UI_SRC / "components" / "detail" / "TaskAttemptList.tsx"
BUILD_FORCE_BRAIN_MODEL = UI_SRC / "components" / "graph" / "buildForceBrainModel.ts"
ASSUMPTION_LOG = REPO_ROOT / "docs" / "ui" / "design_reference" / "assumption_log.md"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_task_attempt_list_touches_no_network():
    assert "fetch(" not in _source(ATTEMPT_LIST), "TaskAttemptList.tsx must stay a pure view"


def test_the_popover_mounts_task_attempt_list_through_taskattemptrows():
    src = _source(POPOVER)
    assert "<TaskAttemptList" in src
    assert "taskAttemptRows(" in src


def test_build_force_brain_model_calls_attempt_chip_text():
    assert "attemptChipText(" in _source(BUILD_FORCE_BRAIN_MODEL), (
        "buildForceBrainModel.ts's taskChipOf must decide the attempt fragment "
        "through attemptChipText(), never re-derive the word inline"
    )


def test_the_assumption_log_names_decision_f029_d5_in_exactly_two_rows():
    lines = ASSUMPTION_LOG.read_text(encoding="utf-8").splitlines()
    matching = [line for line in lines if "DECISION F029 D5" in line]
    assert len(matching) == 2, f"expected exactly two rows naming DECISION F029 D5, found {len(matching)}"
