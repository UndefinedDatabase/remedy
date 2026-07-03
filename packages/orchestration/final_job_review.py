"""Final job-level review v1.

After every per-task reviewer has passed, a job still needs one final,
job-level review: the individual tasks may each be locally correct yet fail to
satisfy the *original job goal* as a whole. This module performs that review
deterministically from evidence already collected — the original goal, the task
plan, each task's summary/diff/verdict, the test evidence, and the proof-gate
verdicts — and produces a single job-level verdict plus structured findings.

It also models the *final job repair loop*: when the final review surfaces
findings, repair tasks are created, completed, and the job is re-reviewed. The
loop tracks attempts and budget so it cannot spin forever.

Pure orchestration logic: no provider calls, no target-repo mutation, no job
state mutation. The same inputs always yield the same report, so the persisted
``final_job_review.json`` / ``final_job_review_findings.json`` are reproducible.

Public API:
    SCHEMA_VERSION
    FinalJobVerdict — str Enum (PASS / NEEDS_REPAIR / BLOCKED)
    build_final_job_review(job_goal, task_plan, task_summaries, task_diffs,
                           task_verdicts, test_evidence, gate_verdicts, ...) -> dict
    build_final_job_repair_loop(findings, repair_tasks, re_review_verdict, ...) -> dict
"""
from __future__ import annotations

from enum import Enum
from typing import Any

SCHEMA_VERSION = "1.0.0"

# Per-task verdict strings that count as "passed" at the task level.
_PASSING_TASK_VERDICTS = {"pass", "passed", "staged_review_passed", "approved", "ok"}

# Per-task verdict strings that are hard blockers (not merely repairable).
_BLOCKING_TASK_VERDICTS = {"blocked", "block", "critical", "reject", "rejected"}


class FinalJobVerdict(str, Enum):
    """Job-level final review verdict."""

    PASS = "PASS"
    NEEDS_REPAIR = "NEEDS_REPAIR"
    BLOCKED = "BLOCKED"


def _as_list(value: Any) -> list[Any]:
    """Normalize a value into a list (None -> [], dict -> its values)."""
    if value is None:
        return []
    if isinstance(value, dict):
        return list(value.values())
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _verdict_string(verdict: Any) -> str:
    """Extract a lowercase verdict string from a str or a dict entry."""
    if isinstance(verdict, dict):
        raw = verdict.get("verdict", verdict.get("status", ""))
    else:
        raw = verdict
    return str(raw or "").strip().lower()


def _task_id_of(verdict: Any, index: int) -> str:
    """Best-effort task id for routing a finding to a repair task."""
    if isinstance(verdict, dict):
        for key in ("task_id", "id", "task"):
            if verdict.get(key):
                return str(verdict[key])
    return f"T{index + 1:03d}"


def _finding(
    finding_id: str,
    severity: str,
    category: str,
    message: str,
    task_id: str | None = None,
) -> dict[str, Any]:
    """Build one structured finding. ``severity`` is 'critical' or 'repairable'."""
    return {
        "id": finding_id,
        "severity": severity,
        "category": category,
        "message": message,
        "task_id": task_id,
    }


def build_final_job_review(
    job_goal: Any,
    task_plan: Any,
    task_summaries: Any,
    task_diffs: Any,
    task_verdicts: Any,
    test_evidence: Any,
    gate_verdicts: Any,
    *,
    job_id: str = "",
    expected_changed_files: Any = None,
    actual_changed_files: Any = None,
    acceptance_criteria: Any = None,
) -> dict[str, Any]:
    """Build a deterministic job-level final review report.

    Findings are collected from four sources:
        1. Per-task verdicts that did not pass (blocking -> critical, else repairable).
        2. Test evidence with any failures/errors (critical).
        3. Proof-gate verdicts that did not pass (critical).
        4. Scope: expected vs actual changed files mismatch (repairable).

    Verdict:
        BLOCKED       if any critical finding exists,
        NEEDS_REPAIR  if findings exist but all are repairable,
        PASS          if there are no findings.
    """
    plan = _as_list(task_plan)
    verdicts = _as_list(task_verdicts)
    gates = _as_list(gate_verdicts)

    findings: list[dict[str, Any]] = []

    # 1. Per-task verdicts.
    tasks_reviewed = 0
    for index, verdict in enumerate(verdicts):
        tasks_reviewed += 1
        state = _verdict_string(verdict)
        if state in _PASSING_TASK_VERDICTS:
            continue
        task_id = _task_id_of(verdict, index)
        if state in _BLOCKING_TASK_VERDICTS:
            findings.append(
                _finding(
                    f"F-TASK-{index + 1:03d}",
                    "critical",
                    "task_verdict",
                    f"Task {task_id} is blocked (verdict={state or 'unknown'}).",
                    task_id,
                )
            )
        else:
            findings.append(
                _finding(
                    f"F-TASK-{index + 1:03d}",
                    "repairable",
                    "task_verdict",
                    f"Task {task_id} did not pass (verdict={state or 'unknown'}).",
                    task_id,
                )
            )

    # 2. Test evidence.
    evidence = test_evidence if isinstance(test_evidence, dict) else {}
    failed = int(evidence.get("failed", 0) or 0)
    errors = int(evidence.get("errors", 0) or 0)
    if failed > 0 or errors > 0:
        findings.append(
            _finding(
                "F-TESTS-001",
                "critical",
                "test_evidence",
                f"Test evidence reports {failed} failed / {errors} error(s).",
            )
        )

    # 3. Proof gates.
    for index, gate in enumerate(gates):
        state = _verdict_string(gate)
        if state in _PASSING_TASK_VERDICTS:
            continue
        name = gate.get("name") if isinstance(gate, dict) else None
        findings.append(
            _finding(
                f"F-GATE-{index + 1:03d}",
                "critical",
                "proof_gate",
                f"Proof gate {name or index + 1} did not pass (verdict={state or 'unknown'}).",
            )
        )

    # 4. Scope / changed-files check.
    expected_files = set(str(f) for f in _as_list(expected_changed_files))
    actual_files = set(str(f) for f in _as_list(actual_changed_files))
    if expected_files:
        unexpected = sorted(actual_files - expected_files)
        changed_files_match = not unexpected
        if unexpected:
            findings.append(
                _finding(
                    "F-SCOPE-001",
                    "repairable",
                    "scope",
                    f"Changed files outside plan scope: {', '.join(unexpected)}.",
                )
            )
    else:
        # No expected set provided -> cannot detect drift; treat as matching.
        changed_files_match = True

    scope_check = {
        "expected_changed_files": sorted(expected_files),
        "actual_changed_files": sorted(actual_files),
        "changed_files_match": changed_files_match,
        "in_scope": changed_files_match,
    }

    # Acceptance-criteria check.
    criteria = _as_list(acceptance_criteria)
    unmet = [
        c for c in criteria
        if isinstance(c, dict) and not bool(c.get("met", c.get("passed", False)))
    ]
    acceptance_all_met = len(unmet) == 0
    if unmet:
        findings.append(
            _finding(
                "F-ACCEPT-001",
                "repairable",
                "acceptance_criteria",
                f"{len(unmet)} acceptance criterion/criteria not met.",
            )
        )
    acceptance_criteria_check = {
        "total": len(criteria),
        "unmet": len(unmet),
        "all_met": acceptance_all_met,
    }

    has_critical = any(f["severity"] == "critical" for f in findings)
    if not findings:
        verdict = FinalJobVerdict.PASS
    elif has_critical:
        verdict = FinalJobVerdict.BLOCKED
    else:
        verdict = FinalJobVerdict.NEEDS_REPAIR

    return {
        "schema_version": SCHEMA_VERSION,
        "job_id": str(job_id),
        "job_goal": "" if job_goal is None else str(job_goal),
        "verdict": verdict.value,
        "findings": findings,
        "task_count": len(plan),
        "tasks_reviewed": tasks_reviewed,
        "scope_check": scope_check,
        "acceptance_criteria_check": acceptance_criteria_check,
        "changed_files_match": changed_files_match,
    }


def build_final_job_repair_loop(
    findings: Any,
    repair_tasks: Any,
    re_review_verdict: Any,
    *,
    rounds: int = 1,
    budget: int = 3,
) -> dict[str, Any]:
    """Track a final job repair loop attempt.

    ``findings`` are the findings that triggered repair; ``repair_tasks`` is the
    list of repair tasks created to address them (each may carry a ``status``);
    ``re_review_verdict`` is the job-level verdict after re-review.

    ``budget`` is the maximum number of repair rounds allowed. ``budget_remaining``
    is ``max(0, budget - rounds)``; ``budget_exhausted`` is True once no rounds
    remain. ``resolved`` is True only when re-review passed within budget.
    """
    finding_list = _as_list(findings)
    task_list = _as_list(repair_tasks)

    completed = sum(
        1 for t in task_list
        if isinstance(t, dict)
        and str(t.get("status", "")).strip().lower() in {"completed", "done", "pass", "passed"}
    )

    rounds_used = max(0, int(rounds or 0))
    budget_total = max(0, int(budget or 0))
    budget_remaining = max(0, budget_total - rounds_used)
    budget_exhausted = budget_remaining == 0

    re_review = _verdict_string(re_review_verdict).upper() or "UNKNOWN"

    return {
        "schema_version": SCHEMA_VERSION,
        "findings_count": len(finding_list),
        "repair_tasks_created": len(task_list),
        "repair_tasks_completed": completed,
        "re_review_verdict": re_review,
        "rounds": rounds_used,
        "budget": budget_total,
        "budget_remaining": budget_remaining,
        "budget_exhausted": budget_exhausted,
        "resolved": re_review == FinalJobVerdict.PASS.value,
    }
