"""Final verifier report — deterministic, read-only verification summary.

Aggregates every gate and evidence artifact produced for a job into a single
final verdict. Pure orchestration logic: no provider calls, no target-repo
mutation, no job state mutation. The report is built only from files already on
disk, so the same evidence dir always yields the same report.

Reads (all optional — missing inputs degrade gracefully):
    job_report.json / job_flow.json
    self_run_observability_index.json
    scratch_file_guard.json
    prompt_trace_summary.json
    task_runs/<task_id>/review_scope_packet.json
    task_runs/<task_id>/spec_compliance_check.json
    task_runs/<task_id>/missing_tests_gate.json
    task_runs/<task_id>/scratch_file_guard.json
    task_runs/<task_id>/review.json
    task_runs/<task_id>/repair_loop.json
    task_runs/<task_id>/tests.txt
    task_runs/<task_id>/token_accounting.json
    task_runs/<task_id>/safe.diff
    task_runs/<task_id>/task_execution_evidence.json
    task_runs/<task_id>/task_actor_binding.json
    task_runs/<task_id>/prompt_trace_summary.json
    token_cost_policy.json
    final_job_review.json
    execution_config.json

Public API:
    build_final_verifier_report(evidence_dir) -> dict
    write_final_verifier_report(evidence_dir, written) -> None
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from packages.orchestration.evidence_mode import (
    ExecutionMode,
    classify_execution_mode,
)

SCHEMA_VERSION = "1.0.0"

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")

# pytest-style result counters, e.g. "3 passed", "1 failed".
_PASSED_RE = re.compile(r"(\d+)\s+passed", re.IGNORECASE)
_FAILED_RE = re.compile(r"(\d+)\s+(?:failed|error[s]?)", re.IGNORECASE)

_RECOMMENDED_ACTION = {
    "PASS": "Approve and promote.",
    "PASS_WITH_RISKS": "Approve with risks; review missing optional evidence before promoting.",
    "NEEDS_TESTS": "Run the missing tests before promoting.",
    "NEEDS_REPAIR": "Resolve the open findings before promoting.",
    "BLOCKED": "Blocked: resolve gate violations before promoting.",
}


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return ""


def _read_gate_verdict(base: Path, filename: str) -> str:
    """Return the ``verdict`` string from a job-level gate JSON, or "" if absent."""
    data = _read_json(base / filename)
    if isinstance(data, dict):
        return str(data.get("verdict", "") or "")
    return ""


def _task_ids(base: Path) -> list[str]:
    """Return sorted, safe task IDs that have a task_runs/<id>/ directory."""
    runs = base / "task_runs"
    if not runs.is_dir():
        return []
    ids = [
        child.name
        for child in runs.iterdir()
        if child.is_dir() and _SAFE_TASK_ID_RE.fullmatch(child.name)
    ]
    return sorted(ids)


def _normalize(path: str) -> str:
    p = path.replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    return p


def _diff_paths(diff_text: str) -> set[str]:
    """Extract file paths from unified diff headers."""
    _PATH_RE = re.compile(r"^[+-]{3}\s+[ab]/(.+)$")
    files: set[str] = set()
    for line in diff_text.splitlines():
        m = _PATH_RE.match(line)
        if m:
            p = m.group(1).strip()
            if p and p != "/dev/null":
                files.add(_normalize(p))
    return files


def _collect_changes(base: Path, task_ids: list[str]) -> tuple[list[str], dict[str, Any]]:
    changed_files: set[str] = set()
    range_acc: dict[str, list[Any]] = {}
    for tid in task_ids:
        packet = _read_json(base / "task_runs" / tid / "review_scope_packet.json")
        if not isinstance(packet, dict):
            continue
        for f in packet.get("changed_files") or []:
            changed_files.add(str(f))
        for f, ranges in (packet.get("changed_line_ranges") or {}).items():
            acc = range_acc.setdefault(str(f), [])
            for r in ranges or []:
                if r not in acc:
                    acc.append(r)
    changed_line_ranges: dict[str, Any] = {
        f: sorted(acc, key=lambda r: r if isinstance(r, list) else [r])
        for f, acc in range_acc.items()
    }
    return sorted(changed_files), changed_line_ranges


_OPERATIONAL_PREFIXES = (".agent/", ".data/", "remedy-job-evidence", "run_transcript")
_OPERATIONAL_SUFFIXES = (".log", ".zip", ".tar", ".gz", ".pyc", ".pyo")


def _is_source_for_alignment(path: str) -> bool:
    """Filter out operational/excluded files from authoritative set."""
    if any(path.startswith(p) for p in _OPERATIONAL_PREFIXES):
        return False
    if any(path.endswith(s) for s in _OPERATIONAL_SUFFIXES):
        return False
    if any(sub in path for sub in ("__pycache__", "htmlcov/", ".coverage")):
        return False
    return True


def _collect_authoritative_changed_files(base: Path, task_ids: list[str]) -> list[str]:
    """Union changed files from all evidence sources, excluding operational files."""
    files: set[str] = set()

    for tid in task_ids:
        packet = _read_json(base / "task_runs" / tid / "review_scope_packet.json")
        if isinstance(packet, dict):
            for f in packet.get("changed_files") or []:
                files.add(_normalize(str(f)))
        safe_diff = base / "task_runs" / tid / "safe.diff"
        if safe_diff.exists():
            files |= _diff_paths(_read_text(safe_diff))

    ws_diff = base / "workspace.diff"
    if ws_diff.exists():
        files |= _diff_paths(_read_text(ws_diff))

    apply_json = _read_json(base / "workspace_apply.json")
    if isinstance(apply_json, list):
        for entry in apply_json:
            if isinstance(entry, dict):
                manifest = entry.get("apply_manifest")
                if isinstance(manifest, dict):
                    for f in manifest.get("applied_files") or []:
                        files.add(_normalize(str(f)))

    cp_gate = _read_json(base / "change_provenance_gate.json")
    if isinstance(cp_gate, dict):
        for f in cp_gate.get("covered_files") or []:
            files.add(_normalize(str(f)))

    return sorted(f for f in files if _is_source_for_alignment(f))


def _file_set_alignment(
    base: Path,
    authoritative_files: list[str],
    review_scope_files: list[str],
) -> dict[str, Any]:
    """Compare authoritative changed files against review scope changed files."""
    auth_set = set(authoritative_files)
    scope_set = set(review_scope_files)

    cp_gate = _read_json(base / "change_provenance_gate.json")
    cp_present = isinstance(cp_gate, dict) and cp_gate.get("verdict")
    cp_covered = set()
    cp_hash_mismatches: list[dict[str, str]] = []
    if cp_present:
        cp_covered = {_normalize(str(f)) for f in (cp_gate.get("covered_files") or [])}
        cp_hash_mismatches = cp_gate.get("hash_mismatches") or []

    in_auth_not_scope = sorted(auth_set - scope_set)
    in_scope_not_auth = sorted(scope_set - auth_set)

    uncovered = sorted(auth_set - cp_covered) if cp_present else []

    mismatches: list[str] = []
    blocking: list[str] = []

    if in_auth_not_scope:
        mismatches.append(
            f"authoritative files not in review_scope: {in_auth_not_scope}"
        )
    if in_scope_not_auth:
        mismatches.append(
            f"review_scope files not in authoritative set: {in_scope_not_auth}"
        )
    if uncovered:
        blocking.append(
            f"authoritative files not covered by change_provenance: {uncovered}"
        )
        mismatches.append(blocking[-1])

    has_hash_mismatches = bool(cp_hash_mismatches)
    if has_hash_mismatches:
        blocking.append(
            f"content hash mismatches: {[m['file'] for m in cp_hash_mismatches]}"
        )
        mismatches.append(blocking[-1])

    if blocking:
        status = "BLOCKED"
    elif mismatches:
        status = "PASS_WITH_RISKS"
    else:
        status = "PASS"

    return {
        "authoritative_changed_files": authoritative_files,
        "change_source_mismatches": mismatches,
        "review_subject_uncovered_files": uncovered,
        "content_hash_mismatches": cp_hash_mismatches,
        "file_set_alignment_status": status,
    }


def _aggregate_gate(base: Path, task_ids: list[str], filename: str, key: str,
                    severity: dict[str, int], default: str) -> str:
    """Return the worst per-task gate status for the given evidence file."""
    worst = default
    worst_rank = severity.get(default, 0)
    for tid in task_ids:
        data = _read_json(base / "task_runs" / tid / filename)
        if not isinstance(data, dict):
            continue
        status = str(data.get(key, "") or "")
        rank = severity.get(status, 0)
        if rank > worst_rank:
            worst_rank = rank
            worst = status
    return worst


def _scratch_status(base: Path, task_ids: list[str]) -> str:
    severity = {"PASS": 0, "BLOCKED": 2}
    worst = "PASS"
    worst_rank = 0
    job_level = _read_json(base / "scratch_file_guard.json")
    candidates: list[Any] = [job_level]
    for tid in task_ids:
        candidates.append(_read_json(base / "task_runs" / tid / "scratch_file_guard.json"))
    for data in candidates:
        if not isinstance(data, dict):
            continue
        rank = severity.get(str(data.get("guard_status", "") or ""), 0)
        if rank > worst_rank:
            worst_rank = rank
            worst = "BLOCKED"
    return worst


def _collect_unresolved_findings(base: Path, task_ids: list[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for tid in task_ids:
        review = _read_json(base / "task_runs" / tid / "review.json")
        # Map finding id -> latest detail seen across review rounds.
        detail_by_id: dict[str, dict[str, Any]] = {}
        last_round_findings: list[dict[str, Any]] = []
        final_verdict = ""
        if isinstance(review, dict):
            final_verdict = str(review.get("final_verdict", "") or "")
            for rnd in review.get("reviews") or []:
                if not isinstance(rnd, dict):
                    continue
                round_findings = rnd.get("findings") or []
                last_round_findings = [f for f in round_findings if isinstance(f, dict)]
                for f in last_round_findings:
                    fid = str(f.get("id", "") or "")
                    if fid:
                        detail_by_id[fid] = f

        repair = _read_json(base / "task_runs" / tid / "repair_loop.json")
        open_ids: list[str] = []
        if isinstance(repair, dict):
            open_ids = [str(i) for i in (repair.get("open_findings") or [])]

        if open_ids:
            for fid in open_ids:
                detail = detail_by_id.get(fid, {})
                findings.append({
                    "task_id": tid,
                    "finding_id": fid,
                    "severity": str(detail.get("severity", "") or ""),
                    "file": str(detail.get("file", "") or ""),
                    "summary": str(detail.get("summary", "") or ""),
                })
        elif final_verdict and final_verdict not in ("pass", "operator_attested"):
            for f in last_round_findings:
                findings.append({
                    "task_id": tid,
                    "finding_id": str(f.get("id", "") or ""),
                    "severity": str(f.get("severity", "") or ""),
                    "file": str(f.get("file", "") or ""),
                    "summary": str(f.get("summary", "") or ""),
                })
    return findings


_SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


def _is_valid_sha256(val: Any) -> bool:
    return isinstance(val, str) and bool(_SHA256_RE.fullmatch(val))


def _operator_attested_tasks(
    base: Path, task_ids: list[str],
) -> tuple[list[str], list[dict[str, Any]]]:
    """Validate operator-repair attestation across all four required artifacts.

    A valid attestation requires:
      1. review.json         — verdict = operator_attested, reviewer present,
                               task_id matches
      2. provider_evidence    — execution_mode = manual_operator_repair,
                               calls = 0, task_id matches
      3. token_accounting     — actual_available = false, kind/reason = manual,
                               task_id matches
      4. manual_repair_provenance — job_id matches, task_id matches,
                                    diff_sha256/provenance_sha256 valid sha256,
                                    changed_files is list, note non-empty,
                                    timestamp present

    Returns (valid_task_ids, attestation_findings).  Invalid attestations are
    reported as findings so the verifier can block instead of silently passing.
    """
    job_id = ""
    jf = _read_json(base / "job_flow.json")
    if isinstance(jf, dict):
        job_id = jf.get("job_id", "")
    if not job_id:
        mf = _read_json(base / "manifest.json")
        if isinstance(mf, dict):
            job_id = mf.get("job_id", "")

    attested: list[str] = []
    findings: list[dict[str, Any]] = []

    for tid in task_ids:
        review = _read_json(base / "task_runs" / tid / "review.json")
        if not isinstance(review, dict):
            continue
        verdict = str(
            review.get("final_verdict") or review.get("verdict") or ""
        ).strip().lower()
        if verdict != "operator_attested":
            continue

        errors: list[str] = []

        if not (review.get("reviewer") or ""):
            errors.append("review.json missing reviewer identity")
        if not review.get("task_id"):
            errors.append("review.json missing task_id")
        elif review["task_id"] != tid:
            errors.append(
                f"review.json task_id={review['task_id']!r}, expected {tid!r}"
            )

        pe = _read_json(base / "task_runs" / tid / "provider_evidence.json")
        if not isinstance(pe, dict):
            errors.append("provider_evidence.json missing")
        else:
            if not pe.get("task_id"):
                errors.append("provider_evidence missing task_id")
            elif pe["task_id"] != tid:
                errors.append(
                    f"provider_evidence task_id={pe['task_id']!r}, expected {tid!r}"
                )
            if pe.get("execution_mode") != "manual_operator_repair":
                errors.append(
                    f"provider_evidence execution_mode="
                    f"{pe.get('execution_mode')!r}, expected manual_operator_repair"
                )
            if pe.get("provider_call_count", -1) != 0:
                errors.append(
                    f"provider_evidence provider_call_count="
                    f"{pe.get('provider_call_count')}, expected 0"
                )
            pts = pe.get("prompt_trace_status") or ""
            if "manual" not in pts and "not_applicable" not in pts:
                errors.append(
                    f"provider_evidence prompt_trace_status={pts!r}, "
                    f"expected manual/not_applicable status"
                )

        ta = _read_json(base / "task_runs" / tid / "token_accounting.json")
        if not isinstance(ta, dict):
            errors.append("token_accounting.json missing")
        else:
            if not ta.get("task_id"):
                errors.append("token_accounting missing task_id")
            elif ta["task_id"] != tid:
                errors.append(
                    f"token_accounting task_id={ta['task_id']!r}, expected {tid!r}"
                )
            if ta.get("actual_available") is not False:
                errors.append(
                    f"token_accounting actual_available="
                    f"{ta.get('actual_available')}, expected false"
                )
            if ta.get("kind") != "manual":
                errors.append(
                    f"token_accounting kind={ta.get('kind')!r}, expected 'manual'"
                )
            if ta.get("reason") != "manual":
                errors.append(
                    f"token_accounting reason={ta.get('reason')!r}, expected 'manual'"
                )

        mrp = _read_json(base / "task_runs" / tid / "manual_repair_provenance.json")
        if not isinstance(mrp, dict):
            errors.append("manual_repair_provenance.json missing")
        else:
            if mrp.get("manual_operator_repair") is not True:
                errors.append("provenance manual_operator_repair is not true")
            if mrp.get("no_provider_calls") is not True:
                errors.append("provenance no_provider_calls is not true")
            if not mrp.get("task_id"):
                errors.append("provenance missing task_id")
            elif mrp["task_id"] != tid:
                errors.append(
                    f"provenance task_id={mrp['task_id']!r}, expected {tid!r}"
                )
            if not mrp.get("job_id"):
                errors.append("provenance missing job_id")
            elif job_id and mrp["job_id"] != job_id:
                errors.append(
                    f"provenance job_id={mrp['job_id']!r}, expected {job_id!r}"
                )
            if not isinstance(mrp.get("changed_files"), list):
                errors.append("provenance changed_files is not a list")
            note_val = mrp.get("note")
            if not note_val or (isinstance(note_val, str) and not note_val.strip()):
                errors.append("provenance note is empty")
            if not mrp.get("timestamp"):
                errors.append("provenance timestamp missing")
            if "workspace_scope" not in mrp:
                errors.append("provenance missing workspace_scope")
            if "task_scope_known" not in mrp:
                errors.append("provenance missing task_scope_known")
            for hash_field in ("diff_sha256", "provenance_sha256"):
                hv = mrp.get(hash_field)
                if not hv:
                    errors.append(f"provenance missing {hash_field}")
                elif not _is_valid_sha256(hv):
                    errors.append(
                        f"provenance {hash_field}={hv!r} is not valid sha256"
                    )

        if errors:
            findings.append({
                "task_id": tid,
                "finding_id": "invalid_operator_attestation",
                "severity": "high",
                "file": "",
                "summary": (
                    "operator_attested verdict incomplete: "
                    + "; ".join(errors)
                ),
            })
        else:
            attested.append(tid)

    return attested, findings


def _final_test_section(text: str) -> str:
    """Extract the last round section from tests.txt.

    tests.txt contains sections like ``=== Round 1: failed ===`` followed by
    ``=== Round 2: passed ===``. Return the text after the last header so
    resolved repair-round failures are not counted as current failures.
    """
    last_header = -1
    for m in re.finditer(r"^=== Round \d+:", text, re.MULTILINE):
        last_header = m.start()
    return text[last_header:] if last_header >= 0 else text


def _aggregate_test_status(base: Path, task_ids: list[str]) -> dict[str, Any]:
    ran = False
    passed = 0
    failed = 0
    for tid in task_ids:
        text = _read_text(base / "task_runs" / tid / "tests.txt")
        if not text.strip():
            continue
        final = _final_test_section(text)
        last_passed = None
        last_failed = None
        for m in _PASSED_RE.finditer(final):
            last_passed = int(m.group(1))
        for m in _FAILED_RE.finditer(final):
            last_failed = int(m.group(1))
        if last_passed is not None:
            passed += last_passed
            ran = True
        if last_failed is not None:
            failed += last_failed
            ran = True
    return {"ran": ran, "passed": passed, "failed": failed}


def _token_status(base: Path, task_ids: list[str]) -> dict[str, Any]:
    truth = _read_json(base / "token_truth.json")
    if isinstance(truth, dict) and truth.get("schema_version"):
        # F003: propagate coverage/cost/model fields without substituting
        # zero/false for unknown — absent fields stay None.
        return {
            "actual_available": bool(truth.get("actual_available", False)),
            "actual_prompt_tokens": truth.get("actual_prompt_tokens"),
            "actual_completion_tokens": truth.get("actual_completion_tokens"),
            "actual_total_tokens": truth.get("actual_total_tokens"),
            "estimated_prompt_tokens": truth.get("estimated_prompt_tokens", 0),
            "estimated_completion_tokens": truth.get("estimated_completion_tokens", 0),
            "estimated_total_tokens": truth.get("estimated_total_tokens", 0),
            "measurement_source": truth.get("measurement_source", ""),
            "measurement_confidence": truth.get("measurement_confidence", ""),
            "total_cost_usd": truth.get("total_cost_usd"),
            "missing_reason": truth.get("missing_reason"),
            "builder_estimated_total": truth.get("builder_estimated_total", 0),
            "reviewer_estimated_total": truth.get("reviewer_estimated_total", 0),
            "repair_estimated_total": truth.get("repair_estimated_total", 0),
            "provider_call_count": truth.get("provider_call_count"),
            "prompt_trace_count": truth.get("prompt_trace_count"),
            "actual_call_count": truth.get("actual_call_count"),
            "actual_coverage_complete": truth.get("actual_coverage_complete"),
            "actual_missing_reasons": truth.get("actual_missing_reasons"),
            "cost_call_count": truth.get("cost_call_count"),
            "cost_coverage_complete": truth.get("cost_coverage_complete"),
            "cost_coverage_reason": truth.get("cost_coverage_reason"),
            "cli_version": truth.get("cli_version"),
            "configured_models": {
                "builder": truth.get("builder_configured_model"),
                "reviewer": truth.get("reviewer_configured_model"),
            },
            "actual_models": {
                "builder": truth.get("builder_actual_model"),
                "reviewer": truth.get("reviewer_actual_model"),
            },
            "actual_model_verified": truth.get("actual_model_verified"),
        }
    actual_available = False
    estimated = 0
    for tid in task_ids:
        acc = _read_json(base / "task_runs" / tid / "token_accounting.json")
        if not isinstance(acc, dict):
            continue
        if acc.get("actual_tokens_available") or acc.get("kind") == "actual":
            actual_available = True
        for field in (
            "builder_prompt_tokens_estimated",
            "reviewer_prompt_tokens_estimated",
            "repair_prompt_tokens_estimated",
        ):
            val = acc.get(field)
            if isinstance(val, (int, float)):
                estimated += int(val)
    trace = _read_json(base / "prompt_trace_summary.json")
    if isinstance(trace, dict):
        total = trace.get("total_prompt_tokens_estimated")
        if isinstance(total, (int, float)) and total:
            estimated = int(total)
    return {
        "actual_available": actual_available,
        "estimated_prompt_tokens": estimated,
    }


# Round 29 F1: the pure token-measurement derivation is the SINGLE source of truth, shared with the
# review gate so the two can never drift. This module keeps a thin back-compatible alias.
from packages.orchestration.token_measurement import (  # noqa: E402
    LOW_CONFIDENCE_TOKEN_NOTE as _LOW_CONFIDENCE_TOKEN_NOTE,
    token_measurement_summary as _token_measurement_summary,
)


def _evidence_completeness(base: Path, task_ids: list[str]) -> dict[str, bool]:
    def all_tasks_have(filename: str) -> bool:
        if not task_ids:
            return False
        return all((base / "task_runs" / tid / filename).exists() for tid in task_ids)

    scratch = (base / "scratch_file_guard.json").exists() or all_tasks_have(
        "scratch_file_guard.json"
    )
    return {
        "review_scope_packet": all_tasks_have("review_scope_packet.json"),
        "spec_compliance_check": all_tasks_have("spec_compliance_check.json"),
        "missing_tests_gate": all_tasks_have("missing_tests_gate.json"),
        "scratch_file_guard": scratch,
        "token_truth": (base / "token_truth.json").exists(),
        "safe_diff": all_tasks_have("safe.diff"),
        "review_json": all_tasks_have("review.json"),
        "tests_txt": all_tasks_have("tests.txt"),
    }


def _trace_provider_calls(base: Path, tid: str) -> int | None:
    """Provider call count recorded in a task's prompt_trace_summary, if present."""
    trace = _read_json(base / "task_runs" / tid / "prompt_trace_summary.json")
    if not isinstance(trace, dict):
        return None
    for key in ("provider_call_count", "total_provider_calls", "provider_calls"):
        if key in trace:
            val = trace[key]
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                return int(val)
    return None


def _execution_mode_consistency(base: Path, task_ids: list[str]) -> dict[str, Any]:
    """Validate each task's declared execution_mode against its prompt trace.

    Only active when at least one ``task_execution_evidence.json`` is present, so
    jobs predating the taxonomy are unaffected. A task that claims
    ``provider_backed`` while the trace shows no provider activity is a phantom
    provider and blocks; other disagreements warn.
    """
    by_task: dict[str, str] = {}
    findings: list[str] = []
    blocked = False
    active = any(
        (base / "task_runs" / tid / "task_execution_evidence.json").exists()
        for tid in task_ids
    )
    if not active:
        return {"by_task": by_task, "findings": findings, "blocked": blocked, "active": False}

    for tid in task_ids:
        ev = _read_json(base / "task_runs" / tid / "task_execution_evidence.json")
        if not isinstance(ev, dict):
            findings.append(f"{tid}: task_execution_evidence.json missing")
            continue
        recorded = str(ev.get("execution_mode", "") or "")
        by_task[tid] = recorded

        prompt_available = bool(ev.get("prompt_trace_available"))
        provider_calls = max(0, int(ev.get("provider_call_count") or 0))

        trace_calls = _trace_provider_calls(base, tid)
        if trace_calls is not None and trace_calls != provider_calls:
            findings.append(
                f"{tid}: provider_call_count={provider_calls} disagrees with "
                f"prompt trace ({trace_calls})"
            )
            provider_calls = trace_calls

        expected = classify_execution_mode(
            1 if prompt_available else 0,
            provider_calls,
            ev.get("builder_provider"),
            ev.get("reviewer_provider"),
        ).value

        if recorded and recorded != expected:
            findings.append(
                f"{tid}: execution_mode={recorded} inconsistent with prompt trace "
                f"(expected {expected})"
            )
            if (
                recorded == ExecutionMode.PROVIDER_BACKED.value
                and expected != ExecutionMode.PROVIDER_BACKED.value
            ):
                blocked = True

    return {"by_task": by_task, "findings": findings, "blocked": blocked, "active": True}


def _sticky_binding_check(base: Path, task_ids: list[str]) -> dict[str, Any]:
    """Read per-task actor bindings and warn where sticky proof is missing/broken.

    Only active when at least one ``task_actor_binding.json`` is present.
    """
    warnings: list[str] = []
    by_task: dict[str, Any] = {}
    active = any(
        (base / "task_runs" / tid / "task_actor_binding.json").exists()
        for tid in task_ids
    )
    if not active:
        return {"warnings": warnings, "by_task": by_task, "active": False}

    for tid in task_ids:
        binding = _read_json(base / "task_runs" / tid / "task_actor_binding.json")
        if not isinstance(binding, dict):
            warnings.append(f"{tid}: sticky actor binding proof missing")
            by_task[tid] = None
            continue
        sticky = bool(binding.get("sticky_across_rounds"))
        by_task[tid] = sticky
        if not sticky:
            warnings.append(f"{tid}: actors not sticky across rounds")

    return {"warnings": warnings, "by_task": by_task, "active": True}


def _token_cost_policy_findings(base: Path) -> dict[str, Any]:
    """Surface cost-risk findings from the job-level token_cost_policy artifact."""
    data = _read_json(base / "token_cost_policy.json")
    if not isinstance(data, dict):
        return {"present": False, "findings": [], "has_critical": False}
    findings = [f for f in (data.get("cost_risk_findings") or []) if isinstance(f, dict)]
    has_critical = any(
        str(f.get("severity", "")).strip().lower() == "critical" for f in findings
    )
    return {"present": True, "findings": findings, "has_critical": has_critical}


def _final_job_review_check(base: Path) -> dict[str, Any]:
    """Read the final job-level review; unresolved findings block promotion."""
    data = _read_json(base / "final_job_review.json")
    if not isinstance(data, dict):
        return {"present": False, "verdict": "", "findings": [], "blocked": False}
    verdict = str(data.get("verdict", "") or "")
    findings = [f for f in (data.get("findings") or []) if isinstance(f, dict)]
    blocked = bool(findings) or verdict.strip().upper() == "BLOCKED"
    return {
        "present": True,
        "verdict": verdict,
        "findings": findings,
        "blocked": blocked,
    }


def _invocation_args_honesty(exec_config: Any) -> list[str]:
    """Warn when configured invocation args are treated as actual (unobserved)."""
    warnings: list[str] = []
    if not isinstance(exec_config, dict):
        return warnings
    observed = bool(exec_config.get("actual_invocation_observed"))
    if observed:
        return warnings
    if exec_config.get("configured_invocation_args"):
        warnings.append(
            "configured_invocation_args recorded but not observed as actual invocation"
        )
    if exec_config.get("actual_invocation_args"):
        warnings.append(
            "actual_invocation_args present without observation proof"
        )
    return warnings


def build_final_verifier_report(evidence_dir: str) -> dict[str, Any]:
    """Build a deterministic final verifier report from evidence artifacts."""
    base = Path(evidence_dir) if evidence_dir else Path(".")
    task_ids = _task_ids(base)

    operator_attested_tasks, attestation_findings = _operator_attested_tasks(
        base, task_ids,
    )

    review_scope_files, changed_line_ranges = _collect_changes(base, task_ids)
    authoritative_changed_files = _collect_authoritative_changed_files(base, task_ids)
    changed_files = authoritative_changed_files
    file_alignment = _file_set_alignment(base, authoritative_changed_files, review_scope_files)

    missing_tests_gate = _aggregate_gate(
        base, task_ids, "missing_tests_gate.json", "gate_status",
        {"PASS": 0, "NEEDS_TESTS": 2}, "PASS",
    )
    spec_compliance = _aggregate_gate(
        base, task_ids, "spec_compliance_check.json", "verdict",
        {"PASS": 0, "FAIL": 1, "BLOCKED": 2}, "PASS",
    )
    scratch_file_guard = _scratch_status(base, task_ids)

    fresh_evidence_gate = _read_gate_verdict(base, "fresh_evidence_gate.json")
    artifact_contract_gate = _read_gate_verdict(base, "artifact_contract_gate.json")
    runtime_integration_gate = _read_gate_verdict(base, "runtime_integration_gate.json")
    change_provenance = _read_gate_verdict(base, "change_provenance_gate.json")
    # commit_execution_gate is downstream — reads OUR verdict, so we don't read it
    # (avoids circular dependency). We expose it in output for informational use.
    commit_execution_gate = _read_gate_verdict(base, "commit_execution_gate.json")

    verification_tests = _read_json(base / "verification_tests.json")

    # F010: a required post-mortem that could not be written is a broken evidence contract.
    # It BLOCKS — a bundle that lost the only account of a failure is not "clean with a
    # warning".
    _pm_integrity = _read_json(base / "postmortem_integrity.json")
    postmortem_failures = (
        list(_pm_integrity.get("failures") or [])
        if isinstance(_pm_integrity, dict) else []
    )
    postmortem_integrity_blocked = bool(postmortem_failures)

    # F012: a required run-input manifest that could not be written or read is a broken
    # evidence contract, the same as a lost post-mortem. It BLOCKS.
    _manifest_integrity = _read_json(base / "manifest_integrity.json")
    manifest_failures = (
        list(_manifest_integrity.get("failures") or [])
        if isinstance(_manifest_integrity, dict) else []
    )
    manifest_integrity_blocked = bool(manifest_failures)

    unresolved_findings = _collect_unresolved_findings(base, task_ids)

    _vt_runs = verification_tests.get("runs") if isinstance(verification_tests, dict) else None
    if isinstance(_vt_runs, list) and _vt_runs:
        # Finding 4: each shared verification run is counted EXACTLY ONCE
        # (deduplicated by run_id). Per-task tests.txt only reference these runs
        # and must never re-add their totals — otherwise a single 528-test root
        # run would be multiplied across every task.
        _seen: dict[str, Any] = {}
        for _r in _vt_runs:
            if not isinstance(_r, dict):
                continue
            _rid = str(_r.get("run_id", ""))
            if _rid and _rid not in _seen:
                _seen[_rid] = _r
        _passed = sum(int(_r.get("passed", 0) or 0) for _r in _seen.values())
        _failed = sum(int(_r.get("failed", 0) or 0) for _r in _seen.values())
        test_status = {"ran": True, "passed": _passed, "failed": _failed}
    else:
        test_status = _aggregate_test_status(base, task_ids)
        if (
            isinstance(verification_tests, dict)
            and verification_tests.get("exit_code") == 0
            and verification_tests.get("passed", 0) > 0
            and verification_tests.get("failed", 0) == 0
        ):
            test_status["ran"] = True
            test_status["passed"] += verification_tests["passed"]
            test_status["failed"] += verification_tests.get("failed", 0)

    token_status = _token_status(base, task_ids)
    token_measurement = _token_measurement_summary(token_status)

    evidence_completeness = _evidence_completeness(base, task_ids)
    missing_evidence = sorted(
        name for name, present in evidence_completeness.items() if not present
    )

    # Model mismatch detection from execution config
    exec_config = _read_json(base / "execution_config.json")
    model_mismatch_warnings: list[str] = []
    model_mismatch_blocked = False
    model_needs_repair = False
    if isinstance(exec_config, dict):
        for role in ("builder", "reviewer", "repair"):
            configured = exec_config.get(f"{role}_model")
            actual = exec_config.get(f"{role}_actual_model")
            actual_available = exec_config.get("actual_config_available", False)

            if configured and actual and configured != actual:
                model_mismatch_warnings.append(
                    f"{role}: configured={configured} actual={actual}"
                )
                if role in ("builder", "reviewer"):
                    model_mismatch_blocked = True

            if not configured and role in ("builder", "reviewer"):
                model_mismatch_warnings.append(
                    f"{role}: no configured model"
                )
                model_needs_repair = True

            if configured and actual is None and not actual_available:
                model_mismatch_warnings.append(
                    f"{role}: actual model unavailable (configured={configured})"
                )
    else:
        model_mismatch_warnings.append("execution_config.json missing")

    # T006 final verifier integration: execution mode, sticky binding, token
    # cost policy, final job review, and configured-vs-actual invocation args.
    exec_mode = _execution_mode_consistency(base, task_ids)
    sticky = _sticky_binding_check(base, task_ids)
    token_cost = _token_cost_policy_findings(base)
    final_job_review = _final_job_review_check(base)
    invocation_args_warnings = _invocation_args_honesty(exec_config)

    upstream_gate_verdicts = {
        "fresh_evidence_gate": fresh_evidence_gate,
        "artifact_contract_gate": artifact_contract_gate,
        "runtime_integration_gate": runtime_integration_gate,
        "change_provenance_gate": change_provenance,
    }
    any_core_gate_blocked = any(
        v == "BLOCKED" for v in upstream_gate_verdicts.values() if v
    )

    file_alignment_blocked = (
        file_alignment["file_set_alignment_status"] == "BLOCKED"
    )
    file_alignment_risky = (
        file_alignment["file_set_alignment_status"] == "PASS_WITH_RISKS"
    )

    gates_blocked = (
        postmortem_integrity_blocked
        or manifest_integrity_blocked
        or scratch_file_guard == "BLOCKED"
        or spec_compliance == "BLOCKED"
        or any_core_gate_blocked
        or file_alignment_blocked
        or model_mismatch_blocked
        or exec_mode["blocked"]
        or final_job_review["blocked"]
        or token_cost["has_critical"]
    )
    needs_repair = (
        bool(unresolved_findings)
        or bool(attestation_findings)
        or spec_compliance == "FAIL"
        or test_status["failed"] > 0
        or model_needs_repair
    )

    tests_verified = (
        isinstance(verification_tests, dict)
        and verification_tests.get("exit_code") == 0
        and verification_tests.get("passed", 0) > 0
        and verification_tests.get("failed", 0) == 0
    )
    effective_missing_tests = missing_tests_gate
    if tests_verified and missing_tests_gate == "NEEDS_TESTS":
        effective_missing_tests = "PASS"

    integration_warnings = bool(
        exec_mode["findings"]
        or sticky["warnings"]
        or token_cost["findings"]
        or invocation_args_warnings
    )

    if gates_blocked:
        verdict = "BLOCKED"
    elif effective_missing_tests == "NEEDS_TESTS":
        verdict = "NEEDS_TESTS"
    elif needs_repair:
        verdict = "NEEDS_REPAIR"
    elif missing_evidence or file_alignment_risky or integration_warnings or (
        model_mismatch_warnings and not model_mismatch_blocked
    ):
        verdict = "PASS_WITH_RISKS"
    else:
        verdict = "PASS"

    # A fully operator-attested manual completion is a valid evidence path, but
    # human final review is mandatory — so it is never an unconditional PASS.
    # Detected from existing artifacts: every task attested + the final job
    # review declaring the manual completion mode (no bespoke root artifact).
    fjr_data = _read_json(base / "final_job_review.json")
    manual_completion = (
        bool(operator_attested_tasks)
        and len(operator_attested_tasks) == len(task_ids)
        and len(task_ids) > 0
    )
    human_final_review_required = bool(
        manual_completion
        or (isinstance(fjr_data, dict) and fjr_data.get("human_final_reviewer_required"))
    )
    if verdict == "PASS" and human_final_review_required:
        verdict = "PASS_WITH_RISKS"

    also_needs_repair = needs_repair and verdict == "NEEDS_TESTS"
    recommended_action = _RECOMMENDED_ACTION[verdict]

    # Visible badges surfaced in the report output. An operator-attested manual
    # repair is a valid, PASS-equivalent evidence path and is flagged so readers
    # can see the task passed via operator attestation rather than a provider run.
    report_badges: list[str] = []
    if operator_attested_tasks:
        report_badges.append("[OPERATOR ATTESTED]")
    if also_needs_repair:
        recommended_action += (
            " Open findings / failing tests are also present; resolve them too."
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "also_needs_repair": also_needs_repair,
        "changed_files": changed_files,
        "changed_line_ranges": changed_line_ranges,
        "authoritative_changed_files": file_alignment["authoritative_changed_files"],
        "change_source_mismatches": file_alignment["change_source_mismatches"],
        "review_subject_uncovered_files": file_alignment["review_subject_uncovered_files"],
        "content_hash_mismatches": file_alignment["content_hash_mismatches"],
        "file_set_alignment_status": file_alignment["file_set_alignment_status"],
        "unresolved_findings": unresolved_findings + attestation_findings,
        "test_status": test_status,
        "missing_tests_gate": missing_tests_gate,
        "scratch_file_guard": scratch_file_guard,
        # F010: required post-mortems that could not be written. Non-empty ⇒ BLOCKED.
        "postmortem_failures": postmortem_failures,
        "postmortem_integrity_blocked": postmortem_integrity_blocked,
        "manifest_integrity_blocked": manifest_integrity_blocked,
        "change_provenance": change_provenance,
        "change_provenance_gate": change_provenance,
        "fresh_evidence_gate": fresh_evidence_gate,
        "artifact_contract_gate": artifact_contract_gate,
        "runtime_integration_gate": runtime_integration_gate,
        "commit_execution_gate": commit_execution_gate,
        "spec_compliance": spec_compliance,
        "token_status": token_status,
        "token_measurement": token_measurement,
        "token_measurement_confidence": token_measurement["measurement_confidence"],
        "token_measurement_note": token_measurement["measurement_note"],
        "token_actual_summary": token_measurement["actual_summary"],
        "evidence_completeness": evidence_completeness,
        "missing_evidence": missing_evidence,
        "model_mismatch_warnings": model_mismatch_warnings,
        "model_mismatch_blocked": model_mismatch_blocked,
        "model_needs_repair": model_needs_repair,
        "execution_mode_by_task": exec_mode["by_task"],
        "execution_mode_findings": exec_mode["findings"],
        "execution_mode_blocked": exec_mode["blocked"],
        "sticky_binding_by_task": sticky["by_task"],
        "sticky_binding_warnings": sticky["warnings"],
        "token_cost_risk_findings": token_cost["findings"],
        "token_cost_policy_present": token_cost["present"],
        "token_cost_has_critical": token_cost["has_critical"],
        "final_job_review_verdict": final_job_review["verdict"],
        "final_job_review_findings": final_job_review["findings"],
        "final_job_review_blocked": final_job_review["blocked"],
        "invocation_args_warnings": invocation_args_warnings,
        "operator_attested_tasks": operator_attested_tasks,
        "manual_completion": manual_completion,
        "human_final_reviewer_required": human_final_review_required,
        "report_badges": report_badges,
        "recommended_action": recommended_action,
    }


def write_final_verifier_report(evidence_dir: str, written: dict[str, str]) -> None:
    """Build and write ``final_verifier_report.json`` to the evidence dir.

    No-op without an evidence dir. Registers the output path in ``written``.
    """
    if not evidence_dir:
        return

    report = build_final_verifier_report(evidence_dir)

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "final_verifier_report.json"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    written["final_verifier_report.json"] = str(json_path)
