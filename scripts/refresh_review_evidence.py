#!/usr/bin/env python3
"""Regenerate derivable gates in a staged Evidence copy.

Called AFTER stage_review_evidence.py copies Evidence into private staging and
BEFORE build_review_manifest.py validates the staged gates.  Ensures the staged
runtime_integration_gate.json matches the production v1.1.0 schema with real
checks, even if the original Evidence was produced with a stale v1.0.0 gate.

The original Evidence directory is never read or mutated.  Every change applies
only to the private staged copy.

Writes ``evidence_refresh_report.json`` into the staged directory documenting
what was regenerated (or left unchanged) and with what verdicts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Any


def _read_json(path: str) -> dict | None:
    try:
        with open(path, encoding="utf-8") as f:
            return json.loads(f.read())
    except (OSError, json.JSONDecodeError):
        return None


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, indent=1, sort_keys=True))


def refresh_staged_evidence(staged_dir: str, repo_root: str) -> dict:
    """Regenerate derivable gates in *staged_dir* from production source.

    Returns the refresh report dict (also written to
    ``<staged_dir>/evidence_refresh_report.json``).
    """
    gate_path = os.path.join(staged_dir, "runtime_integration_gate.json")
    vt_path = os.path.join(staged_dir, "verification_tests.json")

    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "staged_dir": os.path.basename(staged_dir),
        "refreshed_gates": [],
        "unchanged_gates": [],
        "issues": [],
    }

    existing_gate = _read_json(gate_path)
    verification_data = _read_json(vt_path)

    if existing_gate is None:
        refresh_reason = "runtime_integration_gate.json missing from staged evidence"
    elif existing_gate.get("schema_version") != "1.1.0":
        refresh_reason = (
            f"stale schema_version {existing_gate.get('schema_version')!r} "
            f"(production is 1.1.0)")
    elif existing_gate.get("checks_total", 0) == 0:
        refresh_reason = "zero checks in existing gate"
    else:
        refresh_reason = "always-rebuild: regenerated and compared against existing"

    feature_id = None
    if existing_gate is not None:
        feature_id = existing_gate.get("feature_id")

    try:
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        new_gate = build_runtime_integration_gate(
            repo_root, verification_data=verification_data,
            feature_id=feature_id)
        existing_json = json.dumps(existing_gate, indent=1, sort_keys=True) if existing_gate else None
        new_json = json.dumps(new_gate, indent=1, sort_keys=True)
        if existing_json == new_json:
            report["unchanged_gates"].append({
                "gate": "runtime_integration_gate.json",
                "reason": "rebuilt from source; identical to existing",
                "schema_version": new_gate.get("schema_version"),
                "checks_total": new_gate.get("checks_total"),
                "verdict": new_gate.get("verdict"),
            })
        else:
            _write_json(gate_path, new_gate)
            report["refreshed_gates"].append({
                "gate": "runtime_integration_gate.json",
                "reason": refresh_reason,
                "new_schema_version": new_gate.get("schema_version"),
                "new_checks_total": new_gate.get("checks_total"),
                "new_checks_passed": new_gate.get("checks_passed"),
                "new_verdict": new_gate.get("verdict"),
            })
    except Exception as exc:
        report["issues"].append(
            f"failed to regenerate runtime_integration_gate: "
            f"{type(exc).__name__}: {exc}")

    report_path = os.path.join(staged_dir, "evidence_refresh_report.json")
    _write_json(report_path, report)

    _update_inventory(staged_dir, report)
    return report


def _file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _update_inventory(staged_dir: str, report: dict) -> None:
    """Update evidence_snapshot_inventory.json for files written by this refresh."""
    inv_path = os.path.join(staged_dir, "evidence_snapshot_inventory.json")
    inv = _read_json(inv_path)
    if inv is None or not isinstance(inv.get("members"), list):
        return

    touched: list[str] = ["evidence_refresh_report.json"]
    for g in report.get("refreshed_gates", []):
        touched.append(g["gate"])

    members_by_path = {m["relative_path"]: m for m in inv["members"]}
    for rel in touched:
        disk = os.path.join(staged_dir, rel)
        if not os.path.isfile(disk):
            continue
        entry = {
            "kind": "regular",
            "mode": 0o644,
            "relative_path": rel,
            "sha256": _file_sha256(disk),
            "size": os.path.getsize(disk),
            "source_class": "evidence",
        }
        members_by_path[rel] = entry

    inv["members"] = sorted(members_by_path.values(), key=lambda m: m["relative_path"])
    inv["member_count"] = len(inv["members"])
    _write_json(inv_path, inv)


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate derivable gates in staged Evidence")
    parser.add_argument("--staged-dir", required=True,
                        help="Path to the private staged evidence copy")
    parser.add_argument("--repo-root", required=True,
                        help="Path to the repository root")
    args = parser.parse_args()

    if not os.path.isdir(args.staged_dir):
        print(f"ERROR: staged dir does not exist: {args.staged_dir}",
              file=sys.stderr)
        sys.exit(2)

    report = refresh_staged_evidence(args.staged_dir, args.repo_root)

    if report["refreshed_gates"]:
        for g in report["refreshed_gates"]:
            print(f"REFRESHED: {g['gate']} — {g['reason']} "
                  f"→ v{g['new_schema_version']} "
                  f"({g['new_checks_passed']}/{g['new_checks_total']} checks, "
                  f"verdict={g['new_verdict']})")
    if report["unchanged_gates"]:
        for g in report["unchanged_gates"]:
            print(f"UNCHANGED: {g['gate']} — {g['reason']}")
    if report["issues"]:
        for issue in report["issues"]:
            print(f"ISSUE: {issue}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
