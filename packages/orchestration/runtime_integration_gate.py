"""Runtime integration gate — verify gate writers are wired into the pipeline.

Deterministic, read-only orchestration logic: no provider calls, no target-repo
mutation, no job state mutation. Uses static analysis (source-text search) to
confirm that the evidence-pipeline module actually *calls* each gate writer,
and binds to executed test records when verification data is provided.

Public API:
    build_runtime_integration_gate(repo_root, checks=None, verification_data=None) -> dict
    write_runtime_integration_gate(evidence_dir, repo_root, written=None, verification_data=None) -> None
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.1.0"

_JOB_EVIDENCE = "packages/orchestration/job_evidence.py"

# Each check: the evidence pipeline must reference the given pattern in the
# named source file. ``call_exists`` asserts a writer function is invoked;
# ``artifact_written`` asserts an artifact filename is registered.
_PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
_BUDGET_GUARD = "packages/orchestration/budget_guard.py"
_BUDGET_RES = "packages/orchestration/budget_resolution.py"
_RUN_CONTRACT = "packages/orchestration/run_contract.py"
_DECISION_Q = "packages/orchestration/decision_queue.py"
_RUN_MANIFEST = "packages/orchestration/run_manifest.py"
_CONFIG = "packages/orchestration/config.py"
_DO_CMD = "apps/cli/commands/do_cmd.py"

_F018_TEST = "tests/orchestration/test_f018_authority_integration.py"

INTEGRATION_CHECKS: tuple[dict[str, str], ...] = (
    # Gate-writer meta-checks
    {
        "check_id": "job_evidence_calls_fresh_evidence_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_fresh_evidence_gate",
    },
    {
        "check_id": "job_evidence_calls_artifact_contract_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_artifact_contract_gate",
    },
    {
        "check_id": "job_evidence_calls_runtime_integration_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_runtime_integration_gate",
    },
    {
        "check_id": "job_evidence_calls_change_provenance_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_change_provenance_gate",
    },
    {
        "check_id": "job_evidence_calls_commit_execution_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_commit_execution_gate",
    },
    # F018: budget system production-path integration checks
    {
        "check_id": "f018_run_job_calls_collect_counters",
        "source_file": _PINGPONG_JOB,
        "check_type": "call_exists",
        "pattern": "collect_counters_from_actuals",
    },
    {
        "check_id": "f018_run_job_persists_budget_actuals",
        "source_file": _PINGPONG_JOB,
        "check_type": "call_exists",
        "pattern": "_persist_budget_actuals",
    },
    {
        "check_id": "f018_run_job_uses_first_running_at",
        "source_file": _PINGPONG_JOB,
        "check_type": "call_exists",
        "pattern": "first_running_at",
    },
    {
        "check_id": "f018_config_fail_closed_budgets",
        "source_file": _CONFIG,
        "check_type": "call_exists",
        "pattern": "fail_closed_for_budgets",
    },
    {
        "check_id": "f018_budget_resolution_project_root",
        "source_file": _BUDGET_RES,
        "check_type": "call_exists",
        "pattern": "project_root",
    },
    {
        "check_id": "f018_run_manifest_decode_budgets",
        "source_file": _RUN_MANIFEST,
        "check_type": "call_exists",
        "pattern": "_decode_budgets_field",
    },
    {
        "check_id": "f018_run_contract_reconcile_budgets",
        "source_file": _RUN_CONTRACT,
        "check_type": "call_exists",
        "pattern": "_reconcile_budget_fields",
    },
    {
        "check_id": "f018_decision_queue_budget_actions",
        "source_file": _DECISION_Q,
        "check_type": "call_exists",
        "pattern": "\"extend\", \"abandon\"",
    },
    {
        "check_id": "f018_do_job_plan_budget_flags",
        "source_file": _DO_CMD,
        "check_type": "call_exists",
        "pattern": "resolve_job_budgets",
    },
    {
        "check_id": "f018_budget_guard_counter_validation",
        "source_file": _BUDGET_GUARD,
        "check_type": "call_exists",
        "pattern": "BudgetCounterError",
    },
)

TEST_EXECUTION_BINDINGS: tuple[dict[str, Any], ...] = (
    {
        "check_id": "f018_test_authority_integration_execution",
        "check_type": "test_execution_binding",
        "test_file": _F018_TEST,
        "min_passed": 70,
    },
    {
        "check_id": "f018_test_budget_guard_execution",
        "check_type": "test_execution_binding",
        "test_file": "tests/orchestration/test_budget_guard.py",
        "min_passed": 45,
    },
    {
        "check_id": "f018_test_job_budgets_execution",
        "check_type": "test_execution_binding",
        "test_file": "tests/orchestration/test_job_budgets.py",
        "min_passed": 65,
    },
    {
        "check_id": "f018_test_budget_stop_integration_execution",
        "check_type": "test_execution_binding",
        "test_file": "tests/orchestration/test_budget_stop_integration.py",
        "min_passed": 30,
    },
)


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return None


def build_runtime_integration_gate(
    repo_root: str,
    checks: list[dict[str, str]] | None = None,
    verification_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Verify integration via source-text checks and test execution bindings.

    ``checks`` overrides ``INTEGRATION_CHECKS`` when provided. For each
    ``call_exists`` check, the named ``source_file`` is read and searched for
    ``pattern``. ``test_execution_binding`` checks validate against
    ``verification_data`` (the verification_tests.json payload).

    Gate never passes with zero checks.
    """
    root = Path(repo_root) if repo_root else Path(".")
    active = list(checks) if checks is not None else [dict(c) for c in INTEGRATION_CHECKS]

    results: list[dict[str, Any]] = []
    issues: list[str] = []

    for check in active:
        check_id = str(check.get("check_id", ""))
        source_file = str(check.get("source_file", ""))
        check_type = str(check.get("check_type", "call_exists"))
        pattern = str(check.get("pattern", ""))

        text = _read_text(root / source_file)
        found = bool(pattern) and text is not None and pattern in text
        file_missing = text is None

        results.append({
            "check_id": check_id,
            "source_file": source_file,
            "check_type": check_type,
            "pattern": pattern,
            "found": found,
            "file_missing": file_missing,
        })

        if not found:
            if file_missing:
                issues.append(f"{check_id}: source file {source_file!r} not found")
            else:
                issues.append(
                    f"{check_id}: pattern {pattern!r} not found in {source_file!r}"
                )

    if checks is None:
        _bind_test_execution(results, issues, verification_data)

    if not results:
        return {
            "schema_version": SCHEMA_VERSION,
            "verdict": "BLOCKED",
            "checks": [],
            "checks_total": 0,
            "checks_passed": 0,
            "issues": ["gate has zero checks"],
        }

    all_passed = all(r["found"] for r in results)
    verdict = "PASS" if all_passed else "BLOCKED"

    return {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "checks": results,
        "checks_total": len(results),
        "checks_passed": sum(1 for r in results if r["found"]),
        "issues": issues,
    }


def _bind_test_execution(
    results: list[dict[str, Any]],
    issues: list[str],
    verification_data: dict[str, Any] | None,
) -> None:
    """Validate TEST_EXECUTION_BINDINGS against verification run data."""
    runs = []
    if isinstance(verification_data, dict):
        runs = verification_data.get("runs") or []

    for binding in TEST_EXECUTION_BINDINGS:
        check_id = binding["check_id"]
        test_file = binding["test_file"]
        min_passed = int(binding.get("min_passed", 1))

        bound_run = None
        for run in runs:
            run_files = run.get("test_files") or []
            if test_file not in run_files:
                continue
            if run.get("exit_code", -1) != 0:
                continue
            if (run.get("passed") or 0) < min_passed:
                continue
            bound_run = {
                "run_id": run.get("run_id", ""),
                "command": run.get("command", ""),
                "exit_code": run.get("exit_code", -1),
                "passed": run.get("passed", 0),
                "failed": run.get("failed", 0),
                "skipped": run.get("skipped", 0),
                "selected": run.get("selected", 0),
                "node_ids": run.get("node_ids", []),
                "output_hash": run.get("output_hash", ""),
                "head_sha": run.get("head_sha", ""),
            }
            break

        found = bound_run is not None
        entry: dict[str, Any] = {
            "check_id": check_id,
            "check_type": "test_execution_binding",
            "test_file": test_file,
            "min_passed": min_passed,
            "found": found,
        }
        if bound_run is not None:
            entry["bound_run"] = bound_run
        results.append(entry)

        if not found:
            issues.append(
                f"{check_id}: no passing execution for {test_file!r} "
                f"(need >= {min_passed} passed, exit_code 0)"
            )


def write_runtime_integration_gate(
    evidence_dir: str,
    repo_root: str,
    written: dict[str, str] | None = None,
    verification_data: dict[str, Any] | None = None,
) -> None:
    """Build and write ``runtime_integration_gate.json`` into ``evidence_dir``.

    Registers the written path in ``written`` when provided. No-op when
    ``evidence_dir`` is empty.
    """
    if not evidence_dir:
        return

    gate = build_runtime_integration_gate(
        repo_root, verification_data=verification_data,
    )

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "runtime_integration_gate.json"
    json_path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")

    if written is not None:
        written["runtime_integration_gate.json"] = str(json_path)
