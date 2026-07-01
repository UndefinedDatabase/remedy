"""Fresh evidence gate — verify evidence belongs to the current job run.

Deterministic, read-only orchestration logic: no provider calls, no target-repo
mutation, no job state mutation. Given the same evidence directory and repository
state, the same gate is produced every time.

The gate cross-checks the ``job_id`` recorded inside an evidence bundle against
the current job id, and (optionally) checks that the step range named in the
project's ``.agent/plan.md`` and ``.agent/live_review.md`` titles matches the
current run's step range. Stale evidence left over from a previous run is thus
flagged instead of being trusted as authoritative.

Public API:
    build_fresh_evidence_gate(evidence_dir, current_job_id, current_step_range=None) -> dict
    write_fresh_evidence_gate(evidence_dir, current_job_id, current_step_range=None, written=None) -> None
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

# Matches "Steps 5621-5680" (or a bare "5621-5680") and captures both bounds.
# Both bounds require 4+ digits (with no adjacent digit) so date-like pairs such
# as "2026-07" and other small numeric pairs are not mistaken for a step range.
_STEP_RANGE_RE = re.compile(r"(?<!\d)(\d{4,})\s*-\s*(\d{4,})(?!\d)")


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return ""


def _normalize_range(text: str) -> str:
    """Return the first ``NNNN-NNNN`` step range found in ``text``, else ""."""
    if not text:
        return ""
    m = _STEP_RANGE_RE.search(text)
    if not m:
        return ""
    return f"{m.group(1)}-{m.group(2)}"


def _derive_step_range(path: Path) -> str:
    """Derive the normalized step range from an ``.agent`` markdown title."""
    return _normalize_range(_read_text(path))


def build_fresh_evidence_gate(
    evidence_dir: str,
    current_job_id: str,
    current_step_range: str | None = None,
) -> dict[str, Any]:
    """Check whether the evidence in ``evidence_dir`` belongs to the current run.

    Reads ``manifest.json`` (and ``job_report.json`` as a fallback) from
    ``evidence_dir`` to recover the evidence's own ``job_id``, and reads the
    step range from ``.agent/plan.md`` and ``.agent/live_review.md`` titles.
    Never mutates any file.
    """
    base = Path(evidence_dir)
    manifest = _read_json(base / "manifest.json")
    job_flow = _read_json(base / "job_report.json")

    ev_job_id = ""
    if manifest and manifest.get("job_id"):
        ev_job_id = str(manifest.get("job_id") or "")
    elif job_flow and job_flow.get("job_id"):
        ev_job_id = str(job_flow.get("job_id") or "")

    job_id_match = bool(ev_job_id) and ev_job_id == current_job_id
    # A missing evidence job_id is an absence (validity issue), not a mismatch;
    # only a present-but-different id is a hard BLOCK.
    job_id_mismatch = bool(ev_job_id) and ev_job_id != current_job_id

    current_range = _normalize_range(current_step_range or "")
    agent_dir = Path(".agent")
    lr_range = _derive_step_range(agent_dir / "live_review.md")
    plan_range = _derive_step_range(agent_dir / "plan.md")

    lr_match = True if not current_range else (lr_range == current_range)
    plan_match = True if not current_range else (plan_range == current_range)

    freshness_ok = job_id_match and (not current_range or lr_match) and plan_match
    validity_ok = bool(ev_job_id) and bool(manifest or job_flow)

    issues: list[str] = []
    if job_id_mismatch:
        issues.append(
            f"evidence job_id {ev_job_id!r} does not match "
            f"current job_id {current_job_id!r}"
        )
    if current_range and not lr_match:
        issues.append(
            f"live_review step range {lr_range or '(missing)'!r} does not match "
            f"current step range {current_range!r}"
        )
    if current_range and not plan_match:
        issues.append(
            f"plan step range {plan_range or '(missing)'!r} does not match "
            f"current step range {current_range!r}"
        )
    if not ev_job_id:
        issues.append("evidence has no job_id (manifest.json / job_report.json)")
    if not (manifest or job_flow):
        issues.append("evidence has no manifest.json or job_report.json")

    evidence_authoritative = freshness_ok and validity_ok and not issues

    if job_id_mismatch:
        verdict = "BLOCKED"
    elif not issues:
        verdict = "PASS"
    else:
        verdict = "PASS_WITH_RISKS"

    return {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "evidence_job_id": ev_job_id,
        "current_job_id": current_job_id,
        "job_id_match": job_id_match,
        "current_step_range": current_range,
        "live_review_step_range": lr_range,
        "live_review_match": lr_match,
        "plan_step_range": plan_range,
        "plan_match": plan_match,
        "evidence_freshness": {
            "is_fresh": freshness_ok,
            "job_id_match": job_id_match,
            "step_range_match": lr_match and plan_match,
        },
        "evidence_validity": {
            "is_valid_current_run": validity_ok,
            "has_job_id": bool(ev_job_id),
            "has_manifest": bool(manifest),
        },
        "evidence_authoritative": evidence_authoritative,
        "issues": issues,
    }


def write_fresh_evidence_gate(
    evidence_dir: str,
    current_job_id: str,
    current_step_range: str | None = None,
    written: dict[str, str] | None = None,
) -> None:
    """Build and write ``fresh_evidence_gate.json`` into ``evidence_dir``.

    Registers the written path in ``written`` when provided. No-op when
    ``evidence_dir`` is empty.
    """
    if not evidence_dir:
        return

    gate = build_fresh_evidence_gate(evidence_dir, current_job_id, current_step_range)

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "fresh_evidence_gate.json"
    json_path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")

    if written is not None:
        written["fresh_evidence_gate.json"] = str(json_path)
