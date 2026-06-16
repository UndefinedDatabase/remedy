"""
Token-Aware Repair Loop v1/v2 (Steps 1917-1960).

The next core Overnight step after Real Test Execution + Snapshot/Rollback Proof v1. Turns test
failures and review findings into a controlled, token-aware repair workflow:

  Failure Artifact → Minimal Repair Context → Fix Candidate → Review → Re-Test

  Workers execute. Remedy governs. The Repair Loop decides what should happen next, tracks whether the
  Mission Contract is getting closer to done, and prevents unbounded/expensive/unsafe repair attempts.

This module is an ORCHESTRATION + METADATA + EVALUATION layer. It performs NO model/provider/worker
execution, NO automatic candidate generation, NO auto-apply, NO auto-approval, NO autonomous mutation,
NO PR/git, NO real rollback restore, NO MemPalace / internal memory / embeddings. It REUSES the v0/v1
``repair_loop`` building blocks, ``real_test_execution`` results, the live review parser, and
``token_economy`` estimates — it does not duplicate the apply cycle.

Honesty rules:
  - A candidate received is NOT repaired; a candidate-quality pass is NOT applied; an applied change is
    NOT repaired until the re-test passes. A builder ``Done:`` marker is NOT a reviewer ``Resolved``.
  - ``repaired`` requires the policy-required gates (reviewer pass, re-test green, apply proof) with
    durable evidence. No fake repaired state.
  - Token reduction is first-class: repair context carries safe summaries + ``output_ref`` only, never
    raw stdout/stderr / full logs / raw candidates / diffs / secrets / absolute paths. Unknown or
    oversized context → compression or a human decision, never a blind cheap route.

Public API (see __all__ at the bottom).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.provider_trust import _safe_path_label, _scrub_public


SCHEMA_VERSION = "repair-loop-v2"
_RL_DIRNAME = "repair_loop_v2"
_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-ant", "sk-proj",
                "api_key", "password", "secret_key")
_MAX_SUMMARY = 300
_MAX_FILE_REFS = 12


# ---------------------------------------------------------------------------
# Statuses (Step 1919)
# ---------------------------------------------------------------------------


class RepairLoopStatus:
    NEW = "new"
    CONTEXT_NEEDED = "context_needed"
    READY_FOR_ROUTE = "ready_for_route"
    WAITING_FOR_CANDIDATE = "waiting_for_candidate"
    CANDIDATE_RECEIVED = "candidate_received"
    WAITING_FOR_REVIEW = "waiting_for_review"
    REVIEW_FAILED = "review_failed"
    WAITING_FOR_APPLY_APPROVAL = "waiting_for_apply_approval"
    APPLIED_WAITING_RETEST = "applied_waiting_retest"
    RETEST_FAILED = "retest_failed"
    REPAIRED = "repaired"
    BLOCKED = "blocked"
    ABANDONED = "abandoned"


_ALL_STATUSES = frozenset({
    RepairLoopStatus.NEW, RepairLoopStatus.CONTEXT_NEEDED, RepairLoopStatus.READY_FOR_ROUTE,
    RepairLoopStatus.WAITING_FOR_CANDIDATE, RepairLoopStatus.CANDIDATE_RECEIVED,
    RepairLoopStatus.WAITING_FOR_REVIEW, RepairLoopStatus.REVIEW_FAILED,
    RepairLoopStatus.WAITING_FOR_APPLY_APPROVAL, RepairLoopStatus.APPLIED_WAITING_RETEST,
    RepairLoopStatus.RETEST_FAILED, RepairLoopStatus.REPAIRED, RepairLoopStatus.BLOCKED,
    RepairLoopStatus.ABANDONED,
})

# Terminal-ish states that should not be re-counted as open repair work.
_DONE_STATUSES = frozenset({RepairLoopStatus.REPAIRED, RepairLoopStatus.ABANDONED})

SOURCE_FAILURE = "failure_artifact"
SOURCE_REVIEW = "review_finding"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_ddir(data_dir: Path | None) -> Path:
    from packages.orchestration.data_paths import resolve_data_root
    return Path(data_dir) if data_dir is not None else resolve_data_root()


def _safe(text: Any, limit: int = _MAX_SUMMARY) -> str:
    return _scrub_public(str(text or ""))[:limit]


def _safe_file_refs(values: Any) -> list[str]:
    """Basenames only, bounded, scrubbed — never absolute paths."""
    out: list[str] = []
    for v in (values or [])[:_MAX_FILE_REFS]:
        base = str(v).replace("\\", "/").rsplit("/", 1)[-1].strip()
        if base and len(base) < 80 and ".." not in base:
            out.append(base)
    return out


# ---------------------------------------------------------------------------
# Models (Step 1919)
# ---------------------------------------------------------------------------


@dataclass
class RepairLoopPolicy:
    policy_id: str = ""
    job_id: str = ""
    max_attempts: int = 3
    max_retests: int = 3
    max_estimated_tokens_per_attempt: int = 60000
    require_reviewer_pass: bool = True
    require_tests_green: bool = True
    require_apply_proof: bool = True
    stop_on_repeated_failure: bool = True
    prefer_local_for_small_repairs: bool = True
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id, "job_id": self.job_id,
            "max_attempts": int(self.max_attempts), "max_retests": int(self.max_retests),
            "max_estimated_tokens_per_attempt": int(self.max_estimated_tokens_per_attempt),
            "require_reviewer_pass": bool(self.require_reviewer_pass),
            "require_tests_green": bool(self.require_tests_green),
            "require_apply_proof": bool(self.require_apply_proof),
            "stop_on_repeated_failure": bool(self.stop_on_repeated_failure),
            "prefer_local_for_small_repairs": bool(self.prefer_local_for_small_repairs),
            "created_at": self.created_at, "schema_version": SCHEMA_VERSION,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "RepairLoopPolicy":
        base = cls()
        return cls(**{k: d.get(k, getattr(base, k)) for k in base.__dict__})


@dataclass
class RepairWorkItem:
    repair_id: str = ""
    job_id: str = ""
    contract_id: str = ""
    source_type: str = ""            # failure_artifact | review_finding
    source_id: str = ""
    failure_artifact_id: str = ""
    review_finding_id: str = ""
    test_run_id: str = ""
    status: str = RepairLoopStatus.NEW
    title: str = ""
    safe_summary: str = ""
    suspected_files: list[str] = field(default_factory=list)
    required_evidence: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "repair_id": self.repair_id, "job_id": self.job_id, "contract_id": self.contract_id,
            "source_type": self.source_type, "source_id": self.source_id,
            "failure_artifact_id": self.failure_artifact_id,
            "review_finding_id": self.review_finding_id, "test_run_id": self.test_run_id,
            "status": self.status, "title": _safe(self.title, 200),
            "safe_summary": _safe(self.safe_summary), "suspected_files": list(self.suspected_files),
            "required_evidence": list(self.required_evidence),
            "created_at": self.created_at, "updated_at": self.updated_at,
            "schema_version": SCHEMA_VERSION,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "RepairWorkItem":
        base = cls()
        return cls(**{k: d.get(k, getattr(base, k)) for k in base.__dict__})


@dataclass
class RepairAttempt:
    attempt_id: str = ""
    repair_id: str = ""
    attempt_index: int = 0
    route_id: str = ""
    worker_id: str = ""
    context_pack_id: str = ""
    candidate_id: str = ""
    candidate_quality_status: str = "unknown"
    review_status: str = "unknown"
    apply_status: str = "unknown"
    retest_status: str = "unknown"
    token_estimate_band: str = "unknown"
    blocking_reasons: list[str] = field(default_factory=list)
    next_safe_action: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id, "repair_id": self.repair_id,
            "attempt_index": int(self.attempt_index), "route_id": self.route_id,
            "worker_id": self.worker_id, "context_pack_id": self.context_pack_id,
            "candidate_id": self.candidate_id,
            "candidate_quality_status": self.candidate_quality_status,
            "review_status": self.review_status, "apply_status": self.apply_status,
            "retest_status": self.retest_status, "token_estimate_band": self.token_estimate_band,
            "blocking_reasons": list(self.blocking_reasons), "next_safe_action": self.next_safe_action,
            "created_at": self.created_at, "schema_version": SCHEMA_VERSION,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "RepairAttempt":
        base = cls()
        return cls(**{k: d.get(k, getattr(base, k)) for k in base.__dict__})


@dataclass
class RepairLoopEvaluation:
    repair_id: str = ""
    job_id: str = ""
    status: str = RepairLoopStatus.NEW
    attempts_count: int = 0
    satisfied: bool = False
    blocked_reasons: list[str] = field(default_factory=list)
    required_next_actions: list[str] = field(default_factory=list)
    optional_next_ideas: list[str] = field(default_factory=list)
    user_summary: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "repair_id": self.repair_id, "job_id": self.job_id, "status": self.status,
            "attempts_count": int(self.attempts_count), "satisfied": bool(self.satisfied),
            "blocked_reasons": list(self.blocked_reasons),
            "required_next_actions": list(self.required_next_actions),
            "optional_next_ideas": list(self.optional_next_ideas),
            "user_summary": _safe(self.user_summary), "created_at": self.created_at,
            "schema_version": SCHEMA_VERSION,
        }


def export_repair_policy_json(p: RepairLoopPolicy) -> dict[str, Any]:
    return p.to_dict()


def export_repair_work_item_json(i: RepairWorkItem) -> dict[str, Any]:
    return i.to_dict()


def export_repair_attempt_json(a: RepairAttempt) -> dict[str, Any]:
    return a.to_dict()


def export_repair_evaluation_json(e: RepairLoopEvaluation) -> dict[str, Any]:
    return e.to_dict()


# ---------------------------------------------------------------------------
# Storage (Step 1920)
# ---------------------------------------------------------------------------


def _rl_root(job_id: str, data_dir: Path) -> Path:
    base = job_id if job_id else "orchestrator"
    return data_dir / "workspaces" / base / _RL_DIRNAME


def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(data)
        try:
            os.chmod(tmp, mode)
        except OSError:
            pass
        os.replace(tmp, path)
        try:
            os.chmod(path, mode)
        except OSError:
            pass
        return True
    except OSError:
        return False


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _load_json_dir(root: Path) -> list[dict]:
    out: list[dict] = []
    try:
        for f in sorted(root.iterdir()):
            if f.is_file() and f.suffix == ".json":
                d = _load_json(f)
                if isinstance(d, dict):
                    out.append(d)
    except OSError:
        pass
    out.sort(key=lambda r: r.get("created_at", ""))
    return out


def default_repair_loop_policy(job_id: str = "") -> RepairLoopPolicy:
    return RepairLoopPolicy(policy_id=f"rlp-{uuid4().hex[:10]}", job_id=job_id, created_at=_now())


def save_repair_loop_policy(policy: RepairLoopPolicy, data_dir: Path | None = None) -> bool:
    ddir = _resolve_ddir(data_dir)
    path = _rl_root(policy.job_id, ddir) / "policy.json"
    return _atomic_write(path, json.dumps(policy.to_dict(), indent=2).encode("utf-8"))


def load_repair_loop_policy(job_id: str, data_dir: Path | None = None) -> RepairLoopPolicy:
    """Load the per-job policy, or a safe default (never raises)."""
    ddir = _resolve_ddir(data_dir)
    d = _load_json(_rl_root(job_id, ddir) / "policy.json")
    if isinstance(d, dict):
        return RepairLoopPolicy.from_dict(d)
    return default_repair_loop_policy(job_id)


def _item_path(job_id: str, repair_id: str, data_dir: Path) -> Path:
    return _rl_root(job_id, data_dir) / "items" / f"{repair_id}.json"


def save_repair_work_item(item: RepairWorkItem, data_dir: Path | None = None) -> bool:
    ddir = _resolve_ddir(data_dir)
    item.updated_at = _now()
    return _atomic_write(_item_path(item.job_id, item.repair_id, ddir),
                         json.dumps(item.to_dict(), indent=2).encode("utf-8"))


def list_repair_work_items(job_id: str | None = None, data_dir: Path | None = None) -> list[dict]:
    ddir = _resolve_ddir(data_dir)
    roots: list[Path] = []
    if job_id:
        roots.append(_rl_root(job_id, ddir) / "items")
    else:
        try:
            for child in sorted((ddir / "workspaces").iterdir()):
                roots.append(child / _RL_DIRNAME / "items")
        except OSError:
            pass
    out: list[dict] = []
    for r in roots:
        out.extend(_load_json_dir(r))
    out.sort(key=lambda r: r.get("created_at", ""))
    return out


def load_repair_work_item(repair_id: str, data_dir: Path | None = None) -> RepairWorkItem | None:
    for d in list_repair_work_items(data_dir=data_dir):
        if d.get("repair_id") == repair_id:
            return RepairWorkItem.from_dict(d)
    return None


def _attempts_dir(job_id: str, repair_id: str, data_dir: Path) -> Path:
    return _rl_root(job_id, data_dir) / "attempts" / repair_id


def save_repair_attempt(attempt: RepairAttempt, job_id: str, data_dir: Path | None = None) -> bool:
    ddir = _resolve_ddir(data_dir)
    if not attempt.attempt_id:
        attempt.attempt_id = f"rat-{uuid4().hex[:10]}"
    if not attempt.created_at:
        attempt.created_at = _now()
    path = _attempts_dir(job_id, attempt.repair_id, ddir) / f"{attempt.attempt_id}.json"
    return _atomic_write(path, json.dumps(attempt.to_dict(), indent=2).encode("utf-8"))


def list_repair_attempts(repair_id: str, job_id: str = "", data_dir: Path | None = None) -> list[dict]:
    ddir = _resolve_ddir(data_dir)
    if job_id:
        roots = [_attempts_dir(job_id, repair_id, ddir)]
    else:
        roots = []
        try:
            for child in sorted((ddir / "workspaces").iterdir()):
                roots.append(child / _RL_DIRNAME / "attempts" / repair_id)
        except OSError:
            pass
    out: list[dict] = []
    for r in roots:
        out.extend(_load_json_dir(r))
    out.sort(key=lambda r: (r.get("attempt_index", 0), r.get("created_at", "")))
    return out


def _eval_path(job_id: str, repair_id: str, data_dir: Path) -> Path:
    return _rl_root(job_id, data_dir) / "evaluations" / f"{repair_id}.json"


def save_repair_evaluation(ev: RepairLoopEvaluation, data_dir: Path | None = None) -> bool:
    ddir = _resolve_ddir(data_dir)
    return _atomic_write(_eval_path(ev.job_id, ev.repair_id, ddir),
                         json.dumps(ev.to_dict(), indent=2).encode("utf-8"))


def load_latest_repair_evaluation(repair_id: str, data_dir: Path | None = None) -> dict | None:
    ddir = _resolve_ddir(data_dir)
    try:
        for child in sorted((ddir / "workspaces").iterdir()):
            d = _load_json(child / _RL_DIRNAME / "evaluations" / f"{repair_id}.json")
            if isinstance(d, dict):
                return d
    except OSError:
        pass
    return None


# ---------------------------------------------------------------------------
# Failure artifact → repair work item (Step 1921)
# ---------------------------------------------------------------------------


def _stable_repair_id(source_type: str, source_id: str) -> str:
    """Deterministic id so the same source yields the same work item (idempotent)."""
    import hashlib
    h = hashlib.sha256(f"{source_type}::{source_id}".encode("utf-8")).hexdigest()[:12]
    return f"rep-{h}"


def _find_existing_item(job_id: str, repair_id: str, data_dir: Path) -> RepairWorkItem | None:
    d = _load_json(_item_path(job_id, repair_id, data_dir))
    return RepairWorkItem.from_dict(d) if isinstance(d, dict) else None


def create_repair_item_from_failure_artifact(
    job_id: str, failure_artifact_id: str, *, test_run_id: str = "",
    contract_id: str = "", data_dir: Path | None = None,
) -> RepairWorkItem | None:
    """Create (idempotently) a repair work item from a Test Failure Artifact.

    Uses the artifact's SAFE summary + output_ref only — never raw stdout/stderr. Returns None when
    the artifact cannot be found. Does NOT mark the repair as started."""
    ddir = _resolve_ddir(data_dir)
    repair_id = _stable_repair_id(SOURCE_FAILURE, failure_artifact_id)
    existing = _find_existing_item(job_id, repair_id, ddir)
    if existing is not None:
        return existing

    meta: dict[str, Any] = {}
    try:
        from packages.orchestration.storage import load_job
        job = load_job(UUID(job_id), ddir)
        for art in (job.artifacts or []):
            if str(art.id) == failure_artifact_id and (art.metadata or {}).get("test_failure"):
                meta = art.metadata or {}
                break
    except Exception:
        meta = {}
    if not meta:
        return None

    kind = str(meta.get("failure_kind", "unknown") or "unknown")
    item = RepairWorkItem(
        repair_id=repair_id, job_id=job_id, contract_id=contract_id,
        source_type=SOURCE_FAILURE, source_id=failure_artifact_id,
        failure_artifact_id=failure_artifact_id,
        test_run_id=test_run_id or str(meta.get("related_test_run_id", "") or ""),
        status=RepairLoopStatus.NEW,
        title=f"Repair failing {kind}",
        safe_summary=_safe(meta.get("safe_summary", "")),
        suspected_files=_safe_file_refs(meta.get("related_files")),
        required_evidence=["reviewer_pass", "retest_green", "apply_proof"],
        created_at=_now(),
    )
    save_repair_work_item(item, ddir)
    return item


# ---------------------------------------------------------------------------
# Review finding → repair work item (Step 1922)
# ---------------------------------------------------------------------------


_REQUIRED_REVIEW_SEVERITIES = frozenset({"blocker", "high", "medium"})


def _parse_review_finding_blocks(path: Path | None = None) -> list[dict[str, str]]:
    """Return [{id, severity, status}] for each `### R-xxxx` block. Counts/labels only — no detail."""
    if path is not None:
        p = Path(path)
    else:
        env = os.environ.get("REMEDY_REVIEW_FILE", "")
        p = Path(env) if env else Path(".agent") / "live_review.md"
    if not p.exists():
        return []
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    out: list[dict[str, str]] = []
    cur_id = ""
    cur: list[str] = []

    def _flush(fid: str, block: list[str]) -> None:
        if not fid:
            return
        joined = "\n".join(block).lower()
        sev = _grab(joined, "severity")
        st = _grab(joined, "status")
        out.append({"id": fid, "severity": sev, "status": st})

    for line in text.splitlines():
        s = line.strip()
        m = re.match(r"^###\s+(R-\d+)", s)
        if m:
            _flush(cur_id, cur)
            cur_id = m.group(1)
            cur = [line]
        elif cur_id and (s.startswith("### ") or s.startswith("## ")):
            _flush(cur_id, cur)
            cur_id = ""
            cur = []
        elif cur_id:
            cur.append(line)
    _flush(cur_id, cur)
    return out


def _grab(block_lower: str, field_name: str) -> str:
    needle = f"**{field_name}**".lower()
    for line in block_lower.splitlines():
        st = line.strip()
        if st.startswith("- " + needle) or st.startswith(needle):
            _, _, rhs = line.partition(":")
            return rhs.strip()
    return ""


def create_repair_item_from_review_finding(
    job_id: str, finding_id: str, *, review_path: Path | None = None,
    contract_id: str = "", data_dir: Path | None = None,
) -> RepairWorkItem | None:
    """Create (idempotently) a repair work item from an OPEN Blocker/High/Medium review finding.

    A finding that is Resolved (reviewer) — or merely has a builder `Done:` marker but status is not
    `Open` — does NOT create a required repair item. Returns None when the finding is absent, resolved,
    or below the required-severity floor (no raw finding detail is read or stored)."""
    ddir = _resolve_ddir(data_dir)
    findings = _parse_review_finding_blocks(review_path)
    match = next((f for f in findings if f.get("id") == finding_id), None)
    if match is None:
        return None
    severity = (match.get("severity") or "").strip()
    status = (match.get("status") or "").strip()
    # Done ≠ Resolved: only an explicitly OPEN finding at the required floor becomes a required item.
    if status != "open" or severity not in _REQUIRED_REVIEW_SEVERITIES:
        return None

    repair_id = _stable_repair_id(SOURCE_REVIEW, finding_id)
    existing = _find_existing_item(job_id, repair_id, ddir)
    if existing is not None:
        return existing

    item = RepairWorkItem(
        repair_id=repair_id, job_id=job_id, contract_id=contract_id,
        source_type=SOURCE_REVIEW, source_id=finding_id, review_finding_id=finding_id,
        status=RepairLoopStatus.NEW,
        title=f"Repair review finding {finding_id} ({severity})",
        safe_summary=f"Open {severity} review finding {finding_id} requires a fix and reviewer Resolved.",
        required_evidence=["reviewer_pass"],
        created_at=_now(),
    )
    save_repair_work_item(item, ddir)
    return item


# ---------------------------------------------------------------------------
# Token-aware repair context pack (Step 1923)
# ---------------------------------------------------------------------------


def build_repair_context_pack(
    repair_id: str, *, data_dir: Path | None = None,
) -> dict[str, Any]:
    """Build a MINIMAL, token-aware repair context pack (read-only). Includes safe summaries +
    output_ref + ids + a token estimate + route recommendation only. Never raw logs/diffs/candidates.

    If the token estimate exceeds the policy budget → recommends compression. If the context is unknown
    → requires context inspection / human decision (never a blind cheap route)."""
    ddir = _resolve_ddir(data_dir)
    item = load_repair_work_item(repair_id, ddir)
    if item is None:
        return {"context_pack_id": "", "status": "blocked", "blocker": "repair_item_not_found",
                "schema_version": SCHEMA_VERSION}

    policy = load_repair_loop_policy(item.job_id, ddir)
    pack: dict[str, Any] = {
        "context_pack_id": f"rcp-{uuid4().hex[:10]}",
        "repair_id": repair_id, "job_id": item.job_id, "schema_version": SCHEMA_VERSION,
        "repair_summary": _safe(item.safe_summary),
        "failure_artifact_id": item.failure_artifact_id,
        "review_finding_id": item.review_finding_id,
        "test_command_id": "", "output_ref": "", "latest_test_status": "unavailable",
        "review_finding_summary": "", "suspected_files": list(item.suspected_files),
        "mission_acceptance_refs": [], "token_estimate": {}, "route_recommendation_hint": {},
        "status": "ready", "recommendation": "", "blocker": "",
    }

    # Failure context — safe failure summary + output_ref only (never raw output).
    if item.failure_artifact_id:
        try:
            from packages.orchestration.repair_loop import build_repair_context
            ctx = build_repair_context(item.job_id, item.failure_artifact_id, ddir)
            pack["failure_summary"] = _safe(ctx.safe_summary)
            pack["test_command_id"] = item.test_run_id or ctx.test_run_id
            if not pack["suspected_files"]:
                pack["suspected_files"] = _safe_file_refs(ctx.changed_files_safe)
        except Exception:
            pack["failure_summary"] = ""

    # Latest test status + output_ref (from durable real test runs — never raw output).
    try:
        from packages.orchestration.real_test_execution import list_test_runs
        runs = list_test_runs(item.job_id, ddir)
        if runs:
            latest = runs[-1]
            pack["latest_test_status"] = str(latest.get("status", "unavailable"))
            pack["output_ref"] = str(latest.get("output_ref", ""))
            if not pack["test_command_id"]:
                pack["test_command_id"] = str(latest.get("command_id", ""))
    except Exception:
        pass

    # Relevant review finding summary (counts/labels only).
    if item.review_finding_id:
        pack["review_finding_summary"] = _safe(item.safe_summary, 200)

    # Mission acceptance criteria refs (ids/labels only).
    try:
        from packages.orchestration.overnight_mission import list_mission_contracts
        contracts = list_mission_contracts(job_id=item.job_id, data_dir=ddir)
        for c in contracts[:1]:
            crit = c.get("acceptance_criteria", []) or []
            pack["mission_acceptance_refs"] = [f"ac-{i+1}" for i in range(min(len(crit), 8))]
    except Exception:
        pass

    # Token estimate + route hint (estimates only; unknown stays unknown).
    hint: dict[str, Any] = {}
    try:
        from packages.orchestration.token_economy import routing_token_hint
        hint = routing_token_hint(item.job_id, task_type="repair", data_dir=ddir)
    except Exception:
        hint = {}
    band = str(hint.get("estimated_token_band", "unknown") or "unknown")
    pack["token_estimate"] = {
        "estimated_token_band": band,
        "budget_status": hint.get("budget_status", "unknown"),
        "requires_human_approval": bool(hint.get("requires_human_approval", True)),
        "estimated": True,
    }
    pack["route_recommendation_hint"] = {
        "local_first_recommended": bool(hint.get("local_first_recommended", False)),
        "context_pack_kind": hint.get("context_pack_kind", ""),
    }

    # Token-aware decision: oversized → compress; unknown → inspect / human decision.
    if band == "unknown" or pack["token_estimate"]["budget_status"] == "unknown":
        pack["status"] = "needs_decision"
        pack["recommendation"] = "inspect_context_or_human_decision"
        pack["blocker"] = "unknown_context"
    elif band in ("very_high", "huge", "over_budget") or pack["token_estimate"]["budget_status"] == "over":
        pack["status"] = "needs_compression"
        pack["recommendation"] = "compress_context_before_routing"
    else:
        pack["status"] = "ready"
        pack["recommendation"] = "proceed_to_route_recommendation"
    pack["next_safe_action"] = f"remedy repair route-recommend {repair_id} --json"
    return pack


# ---------------------------------------------------------------------------
# Route recommendation (Step 1924)
# ---------------------------------------------------------------------------


def recommend_repair_route(
    repair_id: str, *, persist_attempt: bool = False, data_dir: Path | None = None,
) -> dict[str, Any]:
    """Recommend a repair route from Worker Registry + Route Policy + Token Economy (read-only).

    NEVER executes a worker/provider/model. An external builder route yields a package-create next
    action (ingress), not execution. An expensive/unknown route requires human approval. A small/cheap
    repair may prefer a local route ONLY when it is safe and available (no fake Ollama readiness)."""
    ddir = _resolve_ddir(data_dir)
    item = load_repair_work_item(repair_id, ddir)
    if item is None:
        return {"repair_id": repair_id, "status": "blocked", "blocker": "repair_item_not_found",
                "schema_version": SCHEMA_VERSION}

    policy = load_repair_loop_policy(item.job_id, ddir)
    rec: dict[str, Any] = {
        "repair_id": repair_id, "job_id": item.job_id, "schema_version": SCHEMA_VERSION,
        "recommended_route_kind": "human_review", "worker_id": "", "route_id": "",
        "requires_human_approval": True, "local_first_recommended": False,
        "estimated_token_band": "unknown", "reason": "", "next_safe_action": "", "status": "ready",
    }

    hint: dict[str, Any] = {}
    try:
        from packages.orchestration.token_economy import routing_token_hint
        hint = routing_token_hint(item.job_id, task_type="repair", data_dir=ddir)
    except Exception:
        hint = {}
    band = str(hint.get("estimated_token_band", "unknown") or "unknown")
    requires_approval = bool(hint.get("requires_human_approval", True))
    local_first = bool(hint.get("local_first_recommended", False))
    rec["estimated_token_band"] = band
    rec["requires_human_approval"] = requires_approval
    rec["local_first_recommended"] = local_first

    # Find a safe, available, user-selectable local worker (no fake readiness / placeholders).
    local_worker_id = ""
    try:
        from packages.orchestration import worker_registry as wr
        for spec in wr.list_worker_specs():
            kind = str(getattr(spec, "kind", "")).lower()
            enabled = bool(getattr(spec, "enabled", False))
            selectable = bool(getattr(spec, "user_selectable", False))
            if (enabled and selectable and not wr.is_placeholder(spec)
                    and not wr.hard_safety_requires_approval(spec)
                    and ("local" in kind or "ollama" in kind)):
                local_worker_id = str(getattr(spec, "worker_id", "") or getattr(spec, "id", ""))
                break
    except Exception:
        local_worker_id = ""

    if band == "unknown" or requires_approval:
        rec["recommended_route_kind"] = "human_review"
        rec["requires_human_approval"] = True
        rec["reason"] = ("Unknown/expensive context — human approval required before any route."
                         if band == "unknown" else "Route requires human approval per token economy.")
        rec["next_safe_action"] = f"remedy repair context-pack {repair_id} --json"
    elif policy.prefer_local_for_small_repairs and local_first and local_worker_id:
        rec["recommended_route_kind"] = "local_worker"
        rec["worker_id"] = local_worker_id
        rec["requires_human_approval"] = False
        rec["reason"] = "Small/cheap repair fits a safe, available local worker."
        rec["next_safe_action"] = f"remedy repair evaluate {repair_id} --json"
    else:
        # Default safe path: external builder INGRESS package (no execution).
        rec["recommended_route_kind"] = "external_builder_package"
        rec["requires_human_approval"] = True
        rec["reason"] = "Route via an external builder request package (ingress only; no execution)."
        rec["next_safe_action"] = f"remedy external-builder package-create {item.job_id} --json"

    if persist_attempt:
        attempts = list_repair_attempts(repair_id, item.job_id, ddir)
        attempt = RepairAttempt(
            repair_id=repair_id, attempt_index=len(attempts),
            route_id=rec["recommended_route_kind"], worker_id=rec["worker_id"],
            token_estimate_band=band, review_status="unknown", apply_status="unknown",
            retest_status="unknown", candidate_quality_status="unknown",
            next_safe_action=rec["next_safe_action"], created_at=_now(),
        )
        save_repair_attempt(attempt, item.job_id, ddir)
        rec["attempt_id"] = attempt.attempt_id
    return rec


# ---------------------------------------------------------------------------
# Gate helpers (Steps 1925-1927)
# ---------------------------------------------------------------------------


def _review_gate(item: RepairWorkItem, policy: RepairLoopPolicy) -> tuple[str, str]:
    """Return (state, detail). state ∈ pass|open|unknown|not_required."""
    if not policy.require_reviewer_pass:
        return "not_required", ""
    try:
        from packages.orchestration.overnight_executor import parse_review_findings
        findings = parse_review_findings()
    except Exception:
        return "unknown", "review_unavailable"
    if findings.source in ("unavailable", "malformed"):
        return "unknown", findings.source
    # For a review-sourced item, the specific finding must no longer be open.
    if item.review_finding_id:
        blocks = _parse_review_finding_blocks()
        m = next((b for b in blocks if b.get("id") == item.review_finding_id), None)
        if m is not None and (m.get("status") or "") == "open":
            return "open", f"{item.review_finding_id} still open"
    if findings.verdict == "pass":
        return "pass", "reviewer pass"
    if findings.verdict == "pass_with_risks":
        # PASS WITH RISKS may proceed only if no Medium/High/Blocker remains.
        if findings.open_blocker_or_high == 0 and findings.open_medium == 0:
            return "pass", "pass with risks (low-only)"
        return "open", "pass_with_risks but medium+ open"
    if findings.open_blocker_or_high > 0 or findings.open_medium > 0:
        return "open", "open blocker/high/medium findings"
    return "unknown", findings.verdict


def _v1_attempt_view(item: RepairWorkItem, data_dir: Path) -> dict[str, str]:
    """Read candidate/apply/retest evidence from the existing repair_loop v1 attempt (durable)."""
    view = {"candidate": "absent", "apply": "absent", "retest": "none", "quality": "unknown"}
    if not item.failure_artifact_id:
        return view
    try:
        from packages.orchestration.storage import load_job
        from packages.orchestration.repair_loop import load_repair_attempts, RepairStatus
        job = load_job(UUID(item.job_id), data_dir)
        attempts = load_repair_attempts(job)
        att = next((a for a in attempts.values()
                    if a.failure_artifact_id == item.failure_artifact_id), None)
        if att is None:
            return view
        if att.repair_intent_id:
            view["candidate"] = "present"
        if att.repair_apply_id or att.status in (
                RepairStatus.APPLIED, RepairStatus.TESTED_PASSED, RepairStatus.TESTED_FAILED):
            view["apply"] = "present"
        if att.status == RepairStatus.TESTED_PASSED:
            view["retest"] = "passed"
        elif att.status == RepairStatus.TESTED_FAILED:
            view["retest"] = "failed"
        elif view["apply"] == "present":
            view["retest"] = "none"
    except Exception:
        return view
    return view


def _retest_gate(item: RepairWorkItem, policy: RepairLoopPolicy, data_dir: Path,
                 v1view: dict[str, str]) -> tuple[str, str]:
    """Return (state, detail). state ∈ green|failing|none|not_required."""
    if not policy.require_tests_green:
        return "not_required", ""
    # Prefer the v1 attempt's post-repair test outcome when present.
    if v1view["retest"] == "passed":
        return "green", "post-repair test passed"
    if v1view["retest"] == "failed":
        return "failing", "post-repair test failed"
    # Fall back to the latest real test run for the job.
    try:
        from packages.orchestration.real_test_execution import list_test_runs
        runs = list_test_runs(item.job_id, data_dir)
        if runs:
            latest = str(runs[-1].get("status", ""))
            if latest == "passed":
                return "green", "latest test run passed"
            if latest in ("failed", "timeout"):
                return "failing", "latest test run failing"
    except Exception:
        pass
    return "none", "no relevant re-test recorded"


# ---------------------------------------------------------------------------
# State machine (Step 1928)
# ---------------------------------------------------------------------------


def evaluate_repair_loop(
    repair_id: str, *, persist: bool = True, data_dir: Path | None = None,
) -> RepairLoopEvaluation:
    """Evaluate a repair work item against durable evidence + policy bounds. No execution, no apply.

    Drives the bounded state machine; never fabricates ``repaired`` (requires the policy-required gates
    with durable evidence). Every state has a catalog-valid next safe action; every blocked state has a
    reason. ``required_next_actions`` are separated from ``optional_next_ideas``."""
    ddir = _resolve_ddir(data_dir)
    item = load_repair_work_item(repair_id, ddir)
    if item is None:
        return RepairLoopEvaluation(repair_id=repair_id, status=RepairLoopStatus.BLOCKED,
                                    blocked_reasons=["repair_item_not_found"],
                                    user_summary="Repair item not found.", created_at=_now())

    policy = load_repair_loop_policy(item.job_id, ddir)
    attempts = list_repair_attempts(repair_id, item.job_id, ddir)
    ev = RepairLoopEvaluation(repair_id=repair_id, job_id=item.job_id,
                              attempts_count=len(attempts), created_at=_now())

    if item.status == RepairLoopStatus.ABANDONED:
        ev.status = RepairLoopStatus.ABANDONED
        ev.blocked_reasons = ["abandoned"]
        ev.required_next_actions = [f"remedy repair item-show {repair_id} --json"]
        ev.user_summary = "Repair abandoned — user decision required."
        if persist:
            save_repair_evaluation(ev, ddir)
        return ev

    review_state, review_detail = _review_gate(item, policy)
    v1view = _v1_attempt_view(item, ddir)
    retest_state, retest_detail = _retest_gate(item, policy, ddir, v1view)
    apply_present = v1view["apply"] == "present"
    candidate_present = v1view["candidate"] == "present"

    # Bound: too many attempts → blocked, ask the user (no infinite loop).
    if len(attempts) > policy.max_attempts:
        ev.status = RepairLoopStatus.BLOCKED
        ev.blocked_reasons = [f"max_attempts_reached ({len(attempts)}>{policy.max_attempts})"]
        ev.required_next_actions = [f"remedy repair item-show {repair_id} --json"]
        ev.user_summary = "Maximum repair attempts reached — user decision required."
        if persist:
            save_repair_evaluation(ev, ddir)
        return ev

    # Bound: repeated re-test failures → blocked.
    retests = [a for a in attempts if a.get("retest_status") == "failing"]
    if policy.stop_on_repeated_failure and len(retests) > policy.max_retests:
        ev.status = RepairLoopStatus.BLOCKED
        ev.blocked_reasons = [f"max_retests_reached ({len(retests)}>{policy.max_retests})"]
        ev.required_next_actions = [f"remedy repair item-show {repair_id} --json"]
        ev.user_summary = "Repeated re-test failures — user decision required."
        if persist:
            save_repair_evaluation(ev, ddir)
        return ev

    # State machine — evidence-driven, conservative (never fake repaired).
    status = RepairLoopStatus.CONTEXT_NEEDED
    required: list[str] = []
    if not candidate_present:
        if len(attempts) == 0:
            status = RepairLoopStatus.CONTEXT_NEEDED
            required = [f"remedy repair context-pack {repair_id} --json"]
        else:
            status = RepairLoopStatus.WAITING_FOR_CANDIDATE
            required = [f"remedy repair route-recommend {repair_id} --json"]
    else:
        # Candidate present → review gate → apply gate → re-test gate.
        if policy.require_reviewer_pass and review_state == "open":
            status = RepairLoopStatus.REVIEW_FAILED
            required = [f"remedy repair item-show {repair_id} --json"]
            ev.blocked_reasons.append(f"review_open: {review_detail}")
        elif policy.require_reviewer_pass and review_state == "unknown":
            status = RepairLoopStatus.WAITING_FOR_REVIEW
            required = [f"remedy repair item-show {repair_id} --json"]
            ev.blocked_reasons.append(f"review_unknown: {review_detail}")
        elif policy.require_apply_proof and not apply_present:
            status = RepairLoopStatus.WAITING_FOR_APPLY_APPROVAL
            required = [f"remedy patch approve {item.job_id} <repair_intent_id>"]
        elif retest_state == "failing":
            status = RepairLoopStatus.RETEST_FAILED
            required = [f"remedy repair route-recommend {repair_id} --json"]
            ev.blocked_reasons.append(f"retest_failing: {retest_detail}")
        elif policy.require_tests_green and retest_state in ("none", "unknown"):
            status = RepairLoopStatus.APPLIED_WAITING_RETEST
            required = [f"remedy test run {item.job_id} --json"]
        else:
            # All policy-required gates satisfied with durable evidence → repaired.
            review_ok = (not policy.require_reviewer_pass) or review_state in ("pass", "not_required")
            apply_ok = (not policy.require_apply_proof) or apply_present
            retest_ok = (not policy.require_tests_green) or retest_state in ("green", "not_required")
            if review_ok and apply_ok and retest_ok:
                status = RepairLoopStatus.REPAIRED
                ev.satisfied = True
                required = [f"remedy repair item-show {repair_id} --json"]
            else:
                status = RepairLoopStatus.WAITING_FOR_REVIEW
                required = [f"remedy repair item-show {repair_id} --json"]
                ev.blocked_reasons.append("gates_not_all_satisfied")

    ev.status = status
    ev.required_next_actions = required
    ev.optional_next_ideas = _optional_ideas(item, policy, status)
    ev.user_summary = _user_summary(item, status, review_state, retest_state, apply_present)

    # Persist the work item's derived status (no fake repaired downgrade of a real one).
    if item.status != status:
        item.status = status
        save_repair_work_item(item, ddir)

    if persist:
        save_repair_evaluation(ev, ddir)
    return ev


def _optional_ideas(item: RepairWorkItem, policy: RepairLoopPolicy, status: str) -> list[str]:
    """Optional FUTURE product ideas — never required blockers (no auto-build, evidence-gated)."""
    ideas: list[str] = []
    if status in (RepairLoopStatus.BLOCKED, RepairLoopStatus.RETEST_FAILED):
        ideas.append("Configure a real Claude/Pi/OpenCode builder adapter (future Worker Control Plane).")
    if policy.prefer_local_for_small_repairs and status == RepairLoopStatus.WAITING_FOR_CANDIDATE:
        ideas.append("Configure Ollama for cheap small repairs (future, disabled by default).")
    if status == RepairLoopStatus.APPLIED_WAITING_RETEST:
        ideas.append("Add a real rollback restore so a failed re-test can revert safely (future).")
    return ideas[:5]


def _user_summary(item: RepairWorkItem, status: str, review_state: str, retest_state: str,
                  apply_present: bool) -> str:
    bits = [f"Repair {item.repair_id} ({item.source_type}): {status}."]
    if status == RepairLoopStatus.REPAIRED:
        bits.append("Reviewer pass + apply proof + re-test green — repaired.")
    elif status == RepairLoopStatus.RETEST_FAILED:
        bits.append("Re-test failed after apply — needs another safe attempt.")
    elif status == RepairLoopStatus.REVIEW_FAILED:
        bits.append("Open review finding blocks completion (Done is not Resolved).")
    elif status == RepairLoopStatus.APPLIED_WAITING_RETEST:
        bits.append("Applied — waiting for a bounded re-test (not run automatically).")
    return _safe(" ".join(bits))


# ---------------------------------------------------------------------------
# Integrity (Step 1936)
# ---------------------------------------------------------------------------


def audit_work_item_safety(item: dict[str, Any]) -> list[dict[str, str]]:
    """Flag unsafe states on a public work-item dict. Safe codes only."""
    if not isinstance(item, dict):
        return []
    out: list[dict[str, str]] = []
    rid = item.get("repair_id", "")
    blob = json.dumps(item).lower()
    if any(m.lower() in blob for m in _RAW_MARKERS):
        out.append({"repair_id": rid, "code": "raw_or_secret_in_public"})
    if "/home/" in blob or "/users/" in blob or "/root/" in blob:
        out.append({"repair_id": rid, "code": "absolute_path_in_public"})
    if item.get("status") not in _ALL_STATUSES:
        out.append({"repair_id": rid, "code": "unknown_status"})
    return out


def audit_evaluation_safety(ev: dict[str, Any], item: dict[str, Any] | None,
                            *, review_open: bool, retest_failing: bool,
                            apply_present: bool, policy: dict[str, Any] | None) -> list[dict[str, str]]:
    """Flag dishonest repaired claims. Safe codes only."""
    out: list[dict[str, str]] = []
    rid = ev.get("repair_id", "")
    status = ev.get("status", "")
    pol = policy or {}
    if status == RepairLoopStatus.REPAIRED:
        if pol.get("require_reviewer_pass", True) and review_open:
            out.append({"repair_id": rid, "code": "repaired_with_open_review_finding"})
        if pol.get("require_tests_green", True) and retest_failing:
            out.append({"repair_id": rid, "code": "repaired_with_failing_retest"})
        if pol.get("require_apply_proof", True) and not apply_present:
            out.append({"repair_id": rid, "code": "repaired_without_apply_proof"})
        if not ev.get("satisfied"):
            out.append({"repair_id": rid, "code": "repaired_but_not_satisfied"})
    return out


def _next_action_is_catalog_valid(action: str) -> bool:
    """A next safe action must start with a known catalog group command prefix."""
    if not action or not action.startswith("remedy "):
        return False
    valid_prefixes = (
        "remedy repair ", "remedy test ", "remedy patch ", "remedy external-builder ",
        "remedy job ", "remedy contract ", "remedy snapshot ", "remedy rollback ",
        "remedy overnight ", "remedy context ",
    )
    return any(action.startswith(p) for p in valid_prefixes)


def repair_loop_integrity(data_dir: Path | None = None,
                          work_items: list[dict] | None = None) -> dict[str, Any]:
    """Read-only invariant check over repair work items + evaluations. Safe codes only."""
    ddir = _resolve_ddir(data_dir)
    items = work_items if work_items is not None else list_repair_work_items(data_dir=ddir)
    violations: list[dict] = []
    for it in (items or []):
        violations.extend(audit_work_item_safety(it))
        # Check the latest evaluation honesty for repaired items.
        rid = it.get("repair_id", "")
        if it.get("status") == RepairLoopStatus.REPAIRED:
            evd = load_latest_repair_evaluation(rid, ddir) or {}
            if not evd.get("satisfied"):
                violations.append({"repair_id": rid, "code": "repaired_but_not_satisfied"})
        # next actions catalog-valid.
        evd = load_latest_repair_evaluation(rid, ddir) or {}
        for act in (evd.get("required_next_actions", []) or []):
            if act and "<" not in act and not _next_action_is_catalog_valid(act):
                violations.append({"repair_id": rid, "code": "non_catalog_next_action"})
    return {"version": 1, "work_item_count": len(items or []),
            "violation_count": len(violations), "passed": not violations,
            "violations": violations[:50]}


# ---------------------------------------------------------------------------
# Mission integration helper (Step 1929)
# ---------------------------------------------------------------------------


def repair_loop_mission_signal(job_id: str, data_dir: Path | None = None) -> dict[str, Any]:
    """Safe summary of repair state for the Mission Contract: open/blocked/repaired counts + whether a
    required repair work item still blocks satisfaction. Read-only; honest (no fake repaired)."""
    ddir = _resolve_ddir(data_dir)
    items = list_repair_work_items(job_id=job_id, data_dir=ddir)
    open_count = 0
    blocked_count = 0
    repaired_count = 0
    user_decision = False
    for it in items:
        st = it.get("status", "")
        if st == RepairLoopStatus.REPAIRED:
            repaired_count += 1
        elif st == RepairLoopStatus.ABANDONED:
            user_decision = True
        else:
            open_count += 1
            if st == RepairLoopStatus.BLOCKED:
                blocked_count += 1
                user_decision = True
    needed = open_count > 0
    return {"open_repair_count": open_count, "blocked_repair_count": blocked_count,
            "repaired_count": repaired_count, "user_decision_required": user_decision,
            "repair_needed": needed, "total": len(items)}


__all__ = [
    "SCHEMA_VERSION", "RepairLoopStatus", "SOURCE_FAILURE", "SOURCE_REVIEW",
    "RepairLoopPolicy", "RepairWorkItem", "RepairAttempt", "RepairLoopEvaluation",
    "export_repair_policy_json", "export_repair_work_item_json", "export_repair_attempt_json",
    "export_repair_evaluation_json",
    "default_repair_loop_policy", "save_repair_loop_policy", "load_repair_loop_policy",
    "save_repair_work_item", "load_repair_work_item", "list_repair_work_items",
    "save_repair_attempt", "list_repair_attempts",
    "save_repair_evaluation", "load_latest_repair_evaluation",
    "create_repair_item_from_failure_artifact", "create_repair_item_from_review_finding",
    "build_repair_context_pack", "recommend_repair_route", "evaluate_repair_loop",
    "audit_work_item_safety", "audit_evaluation_safety", "repair_loop_integrity",
    "repair_loop_mission_signal",
]

# Keep redaction helpers referenced for package parity.
_REDACTION_HELPERS = (_scrub_public, _safe_path_label)
