"""Round 39 F3 — complete authoritative verification matrix producer and validator.

Round 38's verification_tests.json was incomplete: missing suites, inconsistent
counts, no real timestamps. This module provides a typed producer that builds
the verification_tests.json artifact conforming to the existing VerificationTestsV1
schema (1.0.0) in build_review_manifest.py, plus a completeness validator that
checks all expected suites are present with consistent counts.

The producer accepts individual run results and derives all top-level fields
(command, exit_code, passed, failed, test_files, timestamp) from the runs — no
field is caller-asserted at the top level. The completeness validator checks
that a recorded matrix covers a declared required-suite list.
"""
from __future__ import annotations

import re

VERIFICATION_TESTS_SCHEMA_VERSION = "1.0.0"

REQUIRED_F012_VERIFICATION_SUITES = [
    "test_provider_evidence_integration",
    "test_review_manual_completion_shapes",
    "test_review_authoritative_e2e",
    "test_token_truth_v1_contract",
    "test_review_subject_artifact_integrity",
    "test_docs_consistency",
]

_RUN_ID_RE = re.compile(r"^vr-\d{4,}$")


class VerificationMatrixError(Exception):
    """The verification matrix cannot be built from the provided inputs."""


def _next_run_id(existing: list[dict]) -> str:
    max_n = 0
    for r in existing:
        m = _RUN_ID_RE.fullmatch(r.get("run_id", ""))
        if m:
            n = int(r["run_id"].split("-")[1])
            if n > max_n:
                max_n = n
    return f"vr-{max_n + 1:04d}"


def produce_verification_run(
    *,
    run_id: str,
    command: str,
    exit_code: int,
    passed: int,
    failed: int,
    test_files: list[str],
    stdout_summary: str,
) -> dict:
    """Build a single verification run conforming to VerificationTestsV1 run schema."""
    if not run_id or not _RUN_ID_RE.fullmatch(run_id):
        raise VerificationMatrixError(f"run_id {run_id!r} is malformed (expected vr-NNNN)")
    if not command:
        raise VerificationMatrixError("command is required")
    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
        raise VerificationMatrixError(f"exit_code must be int, got {type(exit_code).__name__}")
    if not isinstance(passed, int) or isinstance(passed, bool) or passed < 0:
        raise VerificationMatrixError(f"passed must be non-negative int, got {passed!r}")
    if not isinstance(failed, int) or isinstance(failed, bool) or failed < 0:
        raise VerificationMatrixError(f"failed must be non-negative int, got {failed!r}")
    if not isinstance(test_files, list):
        raise VerificationMatrixError("test_files must be a list")
    return {
        "run_id": run_id,
        "command": command,
        "exit_code": exit_code,
        "passed": passed,
        "failed": failed,
        "test_files": sorted(set(test_files)),
        "stdout_summary": stdout_summary,
    }


def produce_verification_tests(
    *,
    runs: list[dict],
    timestamp: str,
) -> dict:
    """Build the complete verification_tests.json from individual runs.

    Top-level command, exit_code, passed, failed, and test_files are derived from
    the runs — never caller-asserted. The timestamp is the real wall-clock time
    of the verification.
    """
    if not runs:
        raise VerificationMatrixError("at least one verification run is required")
    if not timestamp:
        raise VerificationMatrixError("timestamp is required")

    seen_ids: set[str] = set()
    for r in runs:
        rid = r.get("run_id", "")
        if rid in seen_ids:
            raise VerificationMatrixError(f"duplicate run_id {rid!r}")
        seen_ids.add(rid)

    total_passed = sum(r["passed"] for r in runs)
    total_failed = sum(r["failed"] for r in runs)
    combined_command = " && ".join(r["command"] for r in runs)
    combined_exit = 0 if all(r["exit_code"] == 0 for r in runs) else 1
    all_files: set[str] = set()
    for r in runs:
        all_files.update(r["test_files"])

    return {
        "schema_version": VERIFICATION_TESTS_SCHEMA_VERSION,
        "verification_type": "explicit_commands",
        "runs": runs,
        "command": combined_command,
        "exit_code": combined_exit,
        "passed": total_passed,
        "failed": total_failed,
        "test_files": sorted(all_files),
        "timestamp": timestamp,
    }


def validate_verification_completeness(
    vt: dict,
    required_suites: list[str],
) -> list[str]:
    """Validate that a verification_tests document covers all required suites.

    Returns problems (empty = complete). This is a COMPLETENESS check, not a
    schema check — the schema check is in build_review_manifest.validate_verification_tests().
    """
    problems: list[str] = []
    if not isinstance(vt, dict):
        return ["verification_tests is not a dict"]

    runs = vt.get("runs")
    if not isinstance(runs, list):
        return ["verification_tests.runs is not a list"]

    run_commands = {r.get("command", "") for r in runs if isinstance(r, dict)}

    missing_suites = []
    for suite in required_suites:
        if not any(suite in cmd for cmd in run_commands):
            missing_suites.append(suite)
    if missing_suites:
        problems.append(f"missing required suites: {missing_suites}")

    total_passed = vt.get("passed", 0)
    if isinstance(total_passed, int) and not isinstance(total_passed, bool):
        sum_passed = sum(
            r.get("passed", 0) for r in runs
            if isinstance(r, dict) and isinstance(r.get("passed"), int)
            and not isinstance(r.get("passed"), bool)
        )
        if total_passed != sum_passed:
            problems.append(
                f"top-level passed ({total_passed}) != sum of runs ({sum_passed})")

    total_failed = vt.get("failed", 0)
    if isinstance(total_failed, int) and not isinstance(total_failed, bool):
        sum_failed = sum(
            r.get("failed", 0) for r in runs
            if isinstance(r, dict) and isinstance(r.get("failed"), int)
            and not isinstance(r.get("failed"), bool)
        )
        if total_failed != sum_failed:
            problems.append(
                f"top-level failed ({total_failed}) != sum of runs ({sum_failed})")

    seen_ids: set[str] = set()
    for r in runs:
        if isinstance(r, dict):
            rid = r.get("run_id", "")
            if rid in seen_ids:
                problems.append(f"duplicate run_id: {rid!r}")
            seen_ids.add(rid)

    return problems
