"""Round 39 F2 — typed diagnostic comparison producer and validator.

The diagnostic broad run compares test results between a baseline commit and the
current HEAD. Round 38 introduced machine-validated comparison (sorted failure node
IDs, SHA-256 of failure sets, derived ``failure_sets_equal``). Round 39 closes the
finding that the comparison had no typed producer or validator.

The producer accepts pre-collected failure node IDs from both commits and builds
a typed comparison document. The validator recomputes every derived field and
checks internal consistency — a comparison that was tampered with or produced by
a broken producer is rejected.
"""
from __future__ import annotations

import hashlib
import json

DIAGNOSTIC_COMPARISON_SCHEMA_VERSION = "2.0.0"


class DiagnosticComparisonError(Exception):
    """The comparison document is structurally invalid or internally inconsistent."""


def _sha256_of_sorted_ids(node_ids: list[str]) -> str:
    canonical = json.dumps(node_ids, separators=(",", ":"), sort_keys=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def produce_diagnostic_comparison(
    *,
    base_commit: str,
    head_commit: str,
    command: str,
    base_failure_node_ids: list[str],
    head_failure_node_ids: list[str],
    base_passed: int,
    base_failed: int,
    base_skipped: int,
    head_passed: int,
    head_failed: int,
    head_skipped: int,
) -> dict:
    """Build a typed diagnostic comparison from pre-collected test results.

    Both failure node ID lists are sorted deterministically. SHA-256 hashes and
    ``failure_sets_equal`` are derived — never caller-asserted.
    """
    if not base_commit or not head_commit:
        raise DiagnosticComparisonError("base_commit and head_commit are required")
    if not command:
        raise DiagnosticComparisonError("command is required")

    sorted_base = sorted(set(base_failure_node_ids))
    sorted_head = sorted(set(head_failure_node_ids))
    base_sha = _sha256_of_sorted_ids(sorted_base)
    head_sha = _sha256_of_sorted_ids(sorted_head)
    failure_sets_equal = sorted_base == sorted_head

    only_in_base = sorted(set(sorted_base) - set(sorted_head))
    only_in_head = sorted(set(sorted_head) - set(sorted_base))

    return {
        "schema_version": DIAGNOSTIC_COMPARISON_SCHEMA_VERSION,
        "base_commit": base_commit,
        "head_commit": head_commit,
        "command": command,
        "base": {
            "passed": base_passed,
            "failed": base_failed,
            "skipped": base_skipped,
            "failure_node_ids": sorted_base,
            "failure_set_sha256": base_sha,
        },
        "head": {
            "passed": head_passed,
            "failed": head_failed,
            "skipped": head_skipped,
            "failure_node_ids": sorted_head,
            "failure_set_sha256": head_sha,
        },
        "failure_sets_equal": failure_sets_equal,
        "only_in_base": only_in_base,
        "only_in_head": only_in_head,
    }


_REQUIRED_KEYS = frozenset({
    "schema_version", "base_commit", "head_commit", "command",
    "base", "head", "failure_sets_equal", "only_in_base", "only_in_head",
})

_REQUIRED_SIDE_KEYS = frozenset({
    "passed", "failed", "skipped", "failure_node_ids", "failure_set_sha256",
})


def validate_diagnostic_comparison(comparison: dict, expected_head: str) -> list[str]:
    """Validate a diagnostic comparison document. Returns problems (empty = valid).

    Recomputes every derived field (SHA-256 hashes, failure_sets_equal, set
    differences, counts) and rejects any inconsistency.
    """
    problems: list[str] = []
    if not isinstance(comparison, dict):
        return ["comparison is not a dict"]

    missing = _REQUIRED_KEYS - set(comparison)
    if missing:
        problems.append(f"missing required keys: {sorted(missing)}")
        return problems

    if comparison["schema_version"] != DIAGNOSTIC_COMPARISON_SCHEMA_VERSION:
        problems.append(
            f"schema_version {comparison['schema_version']!r} != "
            f"expected {DIAGNOSTIC_COMPARISON_SCHEMA_VERSION!r}")

    if comparison["head_commit"] != expected_head:
        problems.append(
            f"head_commit {comparison['head_commit']!r} != expected {expected_head!r}")

    for side_name in ("base", "head"):
        side = comparison.get(side_name)
        if not isinstance(side, dict):
            problems.append(f"{side_name} is not a dict")
            continue
        side_missing = _REQUIRED_SIDE_KEYS - set(side)
        if side_missing:
            problems.append(f"{side_name} missing keys: {sorted(side_missing)}")
            continue

        node_ids = side["failure_node_ids"]
        if not isinstance(node_ids, list):
            problems.append(f"{side_name}.failure_node_ids is not a list")
            continue
        if node_ids != sorted(node_ids):
            problems.append(f"{side_name}.failure_node_ids is not sorted")

        if len(node_ids) != len(set(node_ids)):
            problems.append(f"{side_name}.failure_node_ids contains duplicates")

        expected_sha = _sha256_of_sorted_ids(node_ids)
        if side["failure_set_sha256"] != expected_sha:
            problems.append(
                f"{side_name}.failure_set_sha256 mismatch: "
                f"recorded {side['failure_set_sha256']!r} != recomputed {expected_sha!r}")

        if side["failed"] != len(node_ids):
            problems.append(
                f"{side_name}.failed ({side['failed']}) != "
                f"len(failure_node_ids) ({len(node_ids)})")

    base_side = comparison.get("base", {})
    head_side = comparison.get("head", {})
    if isinstance(base_side, dict) and isinstance(head_side, dict):
        base_ids = base_side.get("failure_node_ids", [])
        head_ids = head_side.get("failure_node_ids", [])
        if isinstance(base_ids, list) and isinstance(head_ids, list):
            expected_equal = sorted(set(base_ids)) == sorted(set(head_ids))
            if comparison["failure_sets_equal"] != expected_equal:
                problems.append(
                    f"failure_sets_equal is {comparison['failure_sets_equal']!r} "
                    f"but recomputed is {expected_equal!r}")

            expected_only_base = sorted(set(base_ids) - set(head_ids))
            expected_only_head = sorted(set(head_ids) - set(base_ids))
            if comparison["only_in_base"] != expected_only_base:
                problems.append("only_in_base mismatch")
            if comparison["only_in_head"] != expected_only_head:
                problems.append("only_in_head mismatch")

    return problems
