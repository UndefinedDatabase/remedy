"""
Open-Ended Dogfood Run Orchestrator + Replay Analyzer v0 (Steps 2146-2205).

Makes Remedy dogfoodable without pretending full autonomy. A dogfood run is an open-ended,
step-at-a-time orchestration loop that stops when the mission is satisfied, blocked, budget-
exhausted, or operator-stopped — never when a fixed timer expires.

  Workers execute. Remedy governs. The run evaluator decides when work is done.

This module is METADATA + STATE-MACHINE + EVALUATION + REPLAY only. It NEVER calls a provider/
Claude/Pi/OpenCode/Ollama/cloud/local model, the network, a browser, a subprocess, or a shell;
it never executes a worker, runs a test, applies/approves a patch, or automates git/PR. It
builds no internal MemPalace memory / embeddings / vector DB.

Honesty rules:
  - A run is never satisfied from builder self-report alone.
  - Open review findings or failing tests block satisfaction when policy requires them.
  - Token/step/wall-clock budgets are hard ceilings, not suggestions.
  - Brainstorm lane is metadata-only — ideas are recorded, never auto-injected into execution.
  - Done != Resolved. Reviewer verdict beats builder self-report.

Public API (see __all__ at the bottom).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.provider_trust import _scrub_public

SCHEMA_VERSION = "dogfood-run-v0"
_DR_DIRNAME = "dogfood_runs"
_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-ant", "sk-proj",
                "api_key", "password", "secret_key")
_MAX_SUMMARY = 300


# ---------------------------------------------------------------------------
# Statuses
# ---------------------------------------------------------------------------


class DogfoodRunStatus:
    NOT_STARTED = "not_started"
    RUNNING = "running"
    WAITING_FOR_APPROVAL = "waiting_for_approval"
    WAITING_FOR_BUILDER = "waiting_for_builder"
    WAITING_FOR_REVIEW = "waiting_for_review"
    WAITING_FOR_TESTS = "waiting_for_tests"
    REPAIRING = "repairing"
    SATISFIED = "satisfied"
    BLOCKED = "blocked"
    STOPPED_BY_OPERATOR = "stopped_by_operator"
    BUDGET_EXHAUSTED = "budget_exhausted"
    ERROR = "error"


_ALL_STATUSES = frozenset({
    DogfoodRunStatus.NOT_STARTED, DogfoodRunStatus.RUNNING,
    DogfoodRunStatus.WAITING_FOR_APPROVAL, DogfoodRunStatus.WAITING_FOR_BUILDER,
    DogfoodRunStatus.WAITING_FOR_REVIEW, DogfoodRunStatus.WAITING_FOR_TESTS,
    DogfoodRunStatus.REPAIRING, DogfoodRunStatus.SATISFIED,
    DogfoodRunStatus.BLOCKED, DogfoodRunStatus.STOPPED_BY_OPERATOR,
    DogfoodRunStatus.BUDGET_EXHAUSTED, DogfoodRunStatus.ERROR,
})

_TERMINAL_STATUSES = frozenset({
    DogfoodRunStatus.SATISFIED, DogfoodRunStatus.BLOCKED,
    DogfoodRunStatus.STOPPED_BY_OPERATOR, DogfoodRunStatus.BUDGET_EXHAUSTED,
    DogfoodRunStatus.ERROR,
})


class DogfoodLane:
    MISSION = "mission"
    BUILDER = "builder"
    REVIEWER = "reviewer"
    TEST = "test"
    REPAIR = "repair"
    BRAINSTORM = "brainstorm"


_ALL_LANES = frozenset({
    DogfoodLane.MISSION, DogfoodLane.BUILDER, DogfoodLane.REVIEWER,
    DogfoodLane.TEST, DogfoodLane.REPAIR, DogfoodLane.BRAINSTORM,
})


class LaneStatus:
    IDLE = "idle"
    ACTIVE = "active"
    WAITING = "waiting"
    BLOCKED = "blocked"
    DONE = "done"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe(text: Any, limit: int = _MAX_SUMMARY) -> str:
    return _scrub_public(str(text or ""))[:limit]


def _resolve_ddir(data_dir: Path | None) -> Path:
    from packages.orchestration.data_paths import resolve_data_root
    return Path(data_dir) if data_dir is not None else resolve_data_root()


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


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return None


def _run_root(job_id: str, data_dir: Path) -> Path:
    return data_dir / "workspaces" / job_id / _DR_DIRNAME


def _run_dir(job_id: str, run_id: str, data_dir: Path) -> Path:
    return _run_root(job_id, data_dir) / run_id


def _run_path(job_id: str, run_id: str, data_dir: Path) -> Path:
    return _run_dir(job_id, run_id, data_dir) / "run.json"


def _checkpoints_path(job_id: str, run_id: str, data_dir: Path) -> Path:
    return _run_dir(job_id, run_id, data_dir) / "checkpoints.jsonl"


def _replay_path(job_id: str, run_id: str, data_dir: Path) -> Path:
    return _run_dir(job_id, run_id, data_dir) / "replay.json"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class DogfoodRunPolicy:
    max_steps: int = 100
    max_tokens_estimated: int = 500_000
    max_wall_minutes: int = 480
    require_clean_review: bool = True
    require_tests_green: bool = True
    require_proof_chain: bool = False
    allowed_lanes: list[str] = field(default_factory=lambda: list(_ALL_LANES))
    forbidden_actions: list[str] = field(default_factory=lambda: [
        "arbitrary_shell", "network_fetch", "install_packages", "cloud_provider",
        "apply_patch_without_approval", "modify_permissions_autonomously",
    ])
    auto_step: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_steps": self.max_steps, "max_tokens_estimated": self.max_tokens_estimated,
            "max_wall_minutes": self.max_wall_minutes,
            "require_clean_review": self.require_clean_review,
            "require_tests_green": self.require_tests_green,
            "require_proof_chain": self.require_proof_chain,
            "allowed_lanes": list(self.allowed_lanes),
            "forbidden_actions": list(self.forbidden_actions),
            "auto_step": self.auto_step,
        }


def _policy_from_dict(d: dict[str, Any]) -> DogfoodRunPolicy:
    return DogfoodRunPolicy(
        max_steps=int(d.get("max_steps", 100)),
        max_tokens_estimated=int(d.get("max_tokens_estimated", 500_000)),
        max_wall_minutes=int(d.get("max_wall_minutes", 480)),
        require_clean_review=bool(d.get("require_clean_review", True)),
        require_tests_green=bool(d.get("require_tests_green", True)),
        require_proof_chain=bool(d.get("require_proof_chain", False)),
        allowed_lanes=list(d.get("allowed_lanes", list(_ALL_LANES))),
        forbidden_actions=list(d.get("forbidden_actions", [])),
        auto_step=bool(d.get("auto_step", False)),
    )


@dataclass
class DogfoodRunRecord:
    run_id: str = ""
    job_id: str = ""
    contract_id: str = ""
    status: str = DogfoodRunStatus.NOT_STARTED
    policy: DogfoodRunPolicy = field(default_factory=DogfoodRunPolicy)
    step_count: int = 0
    cumulative_tokens: int = 0
    current_lane: str = ""
    lane_statuses: dict[str, str] = field(default_factory=dict)
    blocking_reasons: list[str] = field(default_factory=list)
    last_action: str = ""
    next_suggested_action: str = ""
    stop_reason: str = ""
    created_at: str = ""
    updated_at: str = ""
    started_at: str = ""
    finished_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id, "job_id": self.job_id, "contract_id": self.contract_id,
            "status": self.status, "policy": self.policy.to_dict(),
            "step_count": self.step_count, "cumulative_tokens": self.cumulative_tokens,
            "current_lane": self.current_lane,
            "lane_statuses": dict(self.lane_statuses),
            "blocking_reasons": list(self.blocking_reasons),
            "last_action": _safe(self.last_action),
            "next_suggested_action": _safe(self.next_suggested_action),
            "stop_reason": _safe(self.stop_reason),
            "created_at": self.created_at, "updated_at": self.updated_at,
            "started_at": self.started_at, "finished_at": self.finished_at,
            "schema_version": SCHEMA_VERSION,
        }


def _run_from_dict(d: dict[str, Any]) -> DogfoodRunRecord:
    return DogfoodRunRecord(
        run_id=str(d.get("run_id", "")), job_id=str(d.get("job_id", "")),
        contract_id=str(d.get("contract_id", "")),
        status=str(d.get("status", DogfoodRunStatus.NOT_STARTED)),
        policy=_policy_from_dict(d.get("policy", {})),
        step_count=int(d.get("step_count", 0)),
        cumulative_tokens=int(d.get("cumulative_tokens", 0)),
        current_lane=str(d.get("current_lane", "")),
        lane_statuses=dict(d.get("lane_statuses", {})),
        blocking_reasons=list(d.get("blocking_reasons", [])),
        last_action=str(d.get("last_action", "")),
        next_suggested_action=str(d.get("next_suggested_action", "")),
        stop_reason=str(d.get("stop_reason", "")),
        created_at=str(d.get("created_at", "")),
        updated_at=str(d.get("updated_at", "")),
        started_at=str(d.get("started_at", "")),
        finished_at=str(d.get("finished_at", "")),
    )


@dataclass
class DogfoodRunCheckpoint:
    checkpoint_id: str = ""
    run_id: str = ""
    step_index: int = 0
    timestamp: str = ""
    lane: str = ""
    action_taken: str = ""
    outcome: str = ""
    run_status: str = ""
    lane_statuses: dict[str, str] = field(default_factory=dict)
    blocking_reasons: list[str] = field(default_factory=list)
    next_suggested_action: str = ""
    token_estimate_used: int = 0
    cumulative_tokens: int = 0
    cumulative_steps: int = 0
    wall_elapsed_seconds: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id, "run_id": self.run_id,
            "step_index": self.step_index, "timestamp": self.timestamp,
            "lane": self.lane, "action_taken": _safe(self.action_taken),
            "outcome": _safe(self.outcome), "run_status": self.run_status,
            "lane_statuses": dict(self.lane_statuses),
            "blocking_reasons": list(self.blocking_reasons),
            "next_suggested_action": _safe(self.next_suggested_action),
            "token_estimate_used": self.token_estimate_used,
            "cumulative_tokens": self.cumulative_tokens,
            "cumulative_steps": self.cumulative_steps,
            "wall_elapsed_seconds": self.wall_elapsed_seconds,
        }


def _checkpoint_from_dict(d: dict[str, Any]) -> DogfoodRunCheckpoint:
    return DogfoodRunCheckpoint(
        checkpoint_id=str(d.get("checkpoint_id", "")), run_id=str(d.get("run_id", "")),
        step_index=int(d.get("step_index", 0)), timestamp=str(d.get("timestamp", "")),
        lane=str(d.get("lane", "")), action_taken=str(d.get("action_taken", "")),
        outcome=str(d.get("outcome", "")), run_status=str(d.get("run_status", "")),
        lane_statuses=dict(d.get("lane_statuses", {})),
        blocking_reasons=list(d.get("blocking_reasons", [])),
        next_suggested_action=str(d.get("next_suggested_action", "")),
        token_estimate_used=int(d.get("token_estimate_used", 0)),
        cumulative_tokens=int(d.get("cumulative_tokens", 0)),
        cumulative_steps=int(d.get("cumulative_steps", 0)),
        wall_elapsed_seconds=float(d.get("wall_elapsed_seconds", 0.0)),
    )


@dataclass
class BrainstormIdea:
    idea_id: str = ""
    run_id: str = ""
    job_id: str = ""
    title: str = ""
    rationale: str = ""
    evidence_needed: list[str] = field(default_factory=list)
    priority: str = "low"
    status: str = "proposed"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "idea_id": self.idea_id, "run_id": self.run_id, "job_id": self.job_id,
            "title": _safe(self.title), "rationale": _safe(self.rationale),
            "evidence_needed": [_safe(e) for e in self.evidence_needed],
            "priority": self.priority, "status": self.status,
            "created_at": self.created_at,
        }


def _brainstorm_from_dict(d: dict[str, Any]) -> BrainstormIdea:
    return BrainstormIdea(
        idea_id=str(d.get("idea_id", "")), run_id=str(d.get("run_id", "")),
        job_id=str(d.get("job_id", "")), title=str(d.get("title", "")),
        rationale=str(d.get("rationale", "")),
        evidence_needed=list(d.get("evidence_needed", [])),
        priority=str(d.get("priority", "low")), status=str(d.get("status", "proposed")),
        created_at=str(d.get("created_at", "")),
    )


# ---------------------------------------------------------------------------
# Storage (Phase 3)
# ---------------------------------------------------------------------------


def create_dogfood_run(
    job_id: str, *, contract_id: str = "", policy: DogfoodRunPolicy | None = None,
    data_dir: Path | None = None,
) -> DogfoodRunRecord:
    """Create a new open-ended dogfood run for a job. Returns the persisted record."""
    ddir = _resolve_ddir(data_dir)
    run = DogfoodRunRecord(
        run_id=f"dfr-{uuid4().hex[:12]}", job_id=job_id, contract_id=contract_id,
        status=DogfoodRunStatus.NOT_STARTED,
        policy=policy if policy is not None else DogfoodRunPolicy(),
        lane_statuses={lane: LaneStatus.IDLE for lane in _ALL_LANES},
        created_at=_now(),
    )
    save_dogfood_run(run, ddir)
    return run


def save_dogfood_run(run: DogfoodRunRecord, data_dir: Path | None = None) -> bool:
    ddir = _resolve_ddir(data_dir)
    run.updated_at = _now()
    return _atomic_write(_run_path(run.job_id, run.run_id, ddir),
                         json.dumps(run.to_dict(), indent=2).encode("utf-8"))


def load_dogfood_run(run_id: str, job_id: str, data_dir: Path | None = None) -> DogfoodRunRecord | None:
    ddir = _resolve_ddir(data_dir)
    d = _load_json(_run_path(job_id, run_id, ddir))
    if d is None:
        return None
    return _run_from_dict(d)


def list_dogfood_runs(job_id: str | None = None, data_dir: Path | None = None) -> list[dict[str, Any]]:
    """List all dogfood runs, optionally filtered by job_id. Returns dicts (safe exports)."""
    ddir = _resolve_ddir(data_dir)
    roots: list[Path] = []
    ws = ddir / "workspaces"
    if job_id:
        roots.append(_run_root(job_id, ddir))
    else:
        try:
            for child in ws.iterdir():
                roots.append(child / _DR_DIRNAME)
        except OSError:
            pass
    out: list[dict[str, Any]] = []
    for root in roots:
        try:
            for child in sorted(root.iterdir()):
                f = child / "run.json"
                if not f.is_file():
                    continue
                try:
                    out.append(json.loads(f.read_text(encoding="utf-8")))
                except (OSError, ValueError):
                    continue
        except OSError:
            continue
    out.sort(key=lambda r: r.get("created_at", ""))
    return out


def append_checkpoint(cp: DogfoodRunCheckpoint, job_id: str, data_dir: Path | None = None) -> bool:
    """Append a checkpoint to the JSONL log."""
    ddir = _resolve_ddir(data_dir)
    path = _checkpoints_path(job_id, cp.run_id, ddir)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(cp.to_dict()) + "\n")
        return True
    except OSError:
        return False


def load_checkpoints(run_id: str, job_id: str, data_dir: Path | None = None) -> list[DogfoodRunCheckpoint]:
    """Load all checkpoints for a run."""
    ddir = _resolve_ddir(data_dir)
    path = _checkpoints_path(job_id, run_id, ddir)
    out: list[DogfoodRunCheckpoint] = []
    try:
        if not path.is_file():
            return out
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(_checkpoint_from_dict(json.loads(line)))
            except (ValueError, KeyError):
                continue
    except OSError:
        pass
    return out


def save_brainstorm_idea(idea: BrainstormIdea, data_dir: Path | None = None) -> bool:
    """Save a brainstorm idea (metadata-only, never auto-injected into execution)."""
    ddir = _resolve_ddir(data_dir)
    if not idea.created_at:
        idea.created_at = _now()
    path = _run_dir(idea.job_id, idea.run_id, ddir) / "brainstorm" / f"{idea.idea_id}.json"
    return _atomic_write(path, json.dumps(idea.to_dict(), indent=2).encode("utf-8"))


def list_brainstorm_ideas(run_id: str, job_id: str, data_dir: Path | None = None) -> list[dict[str, Any]]:
    """List brainstorm ideas for a run."""
    ddir = _resolve_ddir(data_dir)
    d = _run_dir(job_id, run_id, ddir) / "brainstorm"
    out: list[dict[str, Any]] = []
    try:
        for f in sorted(d.iterdir()):
            if not f.is_file() or f.suffix != ".json":
                continue
            try:
                out.append(json.loads(f.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                continue
    except OSError:
        pass
    return out


# ---------------------------------------------------------------------------
# Evidence gathering (internal)
# ---------------------------------------------------------------------------


def _gather_run_evidence(job_id: str, data_dir: Path) -> dict[str, Any]:
    """Collect safe durable signals for run evaluation. Read-only; absence -> honest unknown."""
    ev: dict[str, Any] = {
        "contract_status": "unknown", "contract_satisfied": False,
        "open_review_findings": 0, "failed_tests": 0, "tests_status": "unavailable",
        "proof_status": "unavailable", "repair_open": 0, "repair_blocked": 0,
        "builder_sessions_active": 0, "builder_sessions_blocked": 0,
        "managed_executions_active": 0,
    }

    # Mission contract evaluation.
    try:
        from packages.orchestration.overnight_mission import (
            list_mission_contracts,
            load_latest_mission_evaluation,
        )
        contracts = list_mission_contracts(job_id=job_id, data_dir=data_dir)
        if contracts:
            latest = contracts[-1]
            cid = latest.get("contract_id", "")
            ev_data = load_latest_mission_evaluation(cid, data_dir=data_dir)
            if ev_data:
                ev["contract_status"] = ev_data.get("status", "unknown")
                ev["contract_satisfied"] = bool(ev_data.get("satisfied", False))
                ev["open_review_findings"] = int(ev_data.get("open_review_findings", 0))
                ev["failed_tests"] = int(ev_data.get("failed_tests", 0))
    except (ImportError, Exception):
        pass

    # Repair loop status.
    try:
        from packages.orchestration.repair_loop_v2 import list_repair_items
        items = list_repair_items(job_id=job_id, data_dir=data_dir)
        for item in items:
            s = item.get("status", "")
            if s not in ("repaired", "abandoned"):
                ev["repair_open"] += 1
            if s == "blocked":
                ev["repair_blocked"] += 1
    except (ImportError, Exception):
        pass

    # Test execution status.
    try:
        from packages.orchestration.real_test_execution import list_test_runs
        runs = list_test_runs(job_id=job_id, data_dir=data_dir)
        if runs:
            latest_run = runs[-1]
            ev["tests_status"] = latest_run.get("status", "unavailable")
            ev["failed_tests"] = int(latest_run.get("failed_count", 0))
    except (ImportError, Exception):
        pass

    # Main Builder Adapter — active/blocked sessions.
    try:
        from packages.orchestration.main_builder_adapter import list_builder_sessions
        sessions = list_builder_sessions(job_id, data_dir=data_dir)
        for s in sessions:
            st = s.get("status", "")
            if st in ("package_ready", "submitted", "candidate_received"):
                ev["builder_sessions_active"] += 1
            elif st in ("blocked", "error", "failed"):
                ev["builder_sessions_blocked"] += 1
    except (ImportError, Exception):
        pass

    # Managed Builder Execution — active/blocked/failed executions.
    try:
        from packages.orchestration.managed_builder_execution import list_execution_results
        results = list_execution_results(job_id, data_dir=data_dir)
        for r in results:
            st = r.get("status", "")
            if st in ("running", "approval_required"):
                ev["managed_executions_active"] += 1
            elif st in ("failed", "timeout", "blocked"):
                ev.setdefault("managed_executions_blocked", 0)
                ev["managed_executions_blocked"] += 1
    except (ImportError, Exception):
        pass

    # Proof chain status.
    try:
        from uuid import UUID

        from packages.orchestration.proof_chain import build_proof_chain
        from packages.orchestration.storage import load_job
        from packages.orchestration.timeline import load_run_events
        job = load_job(UUID(job_id), data_dir)
        events = load_run_events(data_dir, UUID(job_id))
        chain = build_proof_chain(job, events)
        if chain:
            ev["proof_status"] = chain.overall_status
    except (ImportError, Exception):
        pass

    return ev


# ---------------------------------------------------------------------------
# Run evaluator (Phase 4)
# ---------------------------------------------------------------------------


@dataclass
class DogfoodRunEvaluation:
    run_id: str = ""
    job_id: str = ""
    status: str = DogfoodRunStatus.NOT_STARTED
    satisfied: bool = False
    active_lane: str = ""
    lane_statuses: dict[str, str] = field(default_factory=dict)
    blocking_reasons: list[str] = field(default_factory=list)
    next_actions: list[dict[str, Any]] = field(default_factory=list)
    budget_remaining_steps: int = 0
    budget_remaining_tokens: int = 0
    budget_remaining_wall_minutes: float = 0.0
    evidence: dict[str, Any] = field(default_factory=dict)
    user_summary: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id, "job_id": self.job_id, "status": self.status,
            "satisfied": self.satisfied, "active_lane": self.active_lane,
            "lane_statuses": dict(self.lane_statuses),
            "blocking_reasons": list(self.blocking_reasons),
            "next_actions": list(self.next_actions),
            "budget_remaining_steps": self.budget_remaining_steps,
            "budget_remaining_tokens": self.budget_remaining_tokens,
            "budget_remaining_wall_minutes": self.budget_remaining_wall_minutes,
            "evidence": dict(self.evidence),
            "user_summary": _safe(self.user_summary),
            "created_at": self.created_at,
        }


def evaluate_dogfood_run(run: DogfoodRunRecord, data_dir: Path | None = None) -> DogfoodRunEvaluation:
    """Evaluate the current state of a dogfood run. Read-only, never mutates the run."""
    ddir = _resolve_ddir(data_dir)
    evidence = _gather_run_evidence(run.job_id, ddir)
    policy = run.policy

    ev = DogfoodRunEvaluation(
        run_id=run.run_id, job_id=run.job_id, status=run.status,
        lane_statuses=dict(run.lane_statuses),
        evidence=evidence, created_at=_now(),
    )

    # Budget remaining.
    ev.budget_remaining_steps = max(0, policy.max_steps - run.step_count)
    ev.budget_remaining_tokens = max(0, policy.max_tokens_estimated - run.cumulative_tokens)
    if run.started_at:
        try:
            start = datetime.fromisoformat(run.started_at)
            elapsed = (datetime.now(timezone.utc) - start).total_seconds() / 60.0
            ev.budget_remaining_wall_minutes = max(0.0, policy.max_wall_minutes - elapsed)
        except (ValueError, TypeError):
            ev.budget_remaining_wall_minutes = float(policy.max_wall_minutes)
    else:
        ev.budget_remaining_wall_minutes = float(policy.max_wall_minutes)

    # Terminal state check.
    if run.status in _TERMINAL_STATUSES:
        ev.satisfied = run.status == DogfoodRunStatus.SATISFIED
        return ev

    # Budget exhaustion check.
    blockers: list[str] = list(run.blocking_reasons)
    if ev.budget_remaining_steps <= 0:
        ev.status = DogfoodRunStatus.BUDGET_EXHAUSTED
        blockers.append("step_budget_exhausted")
    if ev.budget_remaining_tokens <= 0:
        ev.status = DogfoodRunStatus.BUDGET_EXHAUSTED
        blockers.append("token_budget_exhausted")
    if ev.budget_remaining_wall_minutes <= 0:
        ev.status = DogfoodRunStatus.BUDGET_EXHAUSTED
        blockers.append("wall_clock_budget_exhausted")

    if ev.status == DogfoodRunStatus.BUDGET_EXHAUSTED:
        ev.blocking_reasons = blockers
        return ev

    # Satisfaction check.
    satisfied = evidence.get("contract_satisfied", False)
    if satisfied:
        if policy.require_clean_review and evidence.get("open_review_findings", 0) > 0:
            satisfied = False
            blockers.append("review_findings_open")
        if policy.require_tests_green and evidence.get("failed_tests", 0) > 0:
            satisfied = False
            blockers.append("tests_failing")
        if policy.require_proof_chain and evidence.get("proof_status") != "complete":
            satisfied = False
            blockers.append("proof_chain_incomplete")

    if satisfied:
        ev.status = DogfoodRunStatus.SATISFIED
        ev.satisfied = True
        ev.user_summary = "Mission contract satisfied with required evidence."
        return ev

    # Determine active lane and next actions.
    ev.blocking_reasons = blockers
    next_actions: list[dict[str, Any]] = []

    # Repair takes priority if items are open.
    if evidence.get("repair_open", 0) > 0 and DogfoodLane.REPAIR in policy.allowed_lanes:
        ev.active_lane = DogfoodLane.REPAIR
        ev.status = DogfoodRunStatus.REPAIRING
        next_actions.append({"lane": DogfoodLane.REPAIR, "action": "process_open_repair_items",
                             "reason": f"{evidence['repair_open']} repair items open"})

    # Tests failing -> suggest test lane.
    elif evidence.get("failed_tests", 0) > 0 and DogfoodLane.TEST in policy.allowed_lanes:
        ev.active_lane = DogfoodLane.TEST
        ev.status = DogfoodRunStatus.WAITING_FOR_TESTS
        next_actions.append({"lane": DogfoodLane.TEST, "action": "review_test_failures",
                             "reason": f"{evidence['failed_tests']} tests failing"})

    # Review findings open -> suggest reviewer lane.
    elif evidence.get("open_review_findings", 0) > 0 and DogfoodLane.REVIEWER in policy.allowed_lanes:
        ev.active_lane = DogfoodLane.REVIEWER
        ev.status = DogfoodRunStatus.WAITING_FOR_REVIEW
        next_actions.append({"lane": DogfoodLane.REVIEWER, "action": "check_review_findings",
                             "reason": f"{evidence['open_review_findings']} review findings open"})

    # Builder sessions active -> builder lane.
    elif evidence.get("builder_sessions_active", 0) > 0 and DogfoodLane.BUILDER in policy.allowed_lanes:
        ev.active_lane = DogfoodLane.BUILDER
        ev.status = DogfoodRunStatus.WAITING_FOR_BUILDER
        next_actions.append({"lane": DogfoodLane.BUILDER, "action": "check_builder_sessions",
                             "reason": "builder sessions active"})

    # Default: mission lane evaluation.
    elif DogfoodLane.MISSION in policy.allowed_lanes:
        ev.active_lane = DogfoodLane.MISSION
        ev.status = DogfoodRunStatus.RUNNING
        next_actions.append({"lane": DogfoodLane.MISSION, "action": "evaluate_mission_progress",
                             "reason": "check mission contract progress"})

    else:
        ev.status = DogfoodRunStatus.BLOCKED
        blockers.append("no_lanes_available")
        ev.blocking_reasons = blockers

    ev.next_actions = next_actions
    return ev


# ---------------------------------------------------------------------------
# Run stepping (Phase 5)
# ---------------------------------------------------------------------------


def step_dogfood_run(
    run: DogfoodRunRecord, *, data_dir: Path | None = None,
) -> tuple[DogfoodRunRecord, DogfoodRunCheckpoint]:
    """Execute one safe, bounded step of a dogfood run.

    This function:
    1. Evaluates the current run state.
    2. Determines the active lane and next action.
    3. Records a checkpoint.
    4. Updates and saves the run record.
    5. Returns (updated_run, checkpoint).

    It does NOT execute any external action — it only determines and records what should happen.
    The caller acts on the suggested action.
    """
    ddir = _resolve_ddir(data_dir)

    # First step: set started_at.
    if run.status == DogfoodRunStatus.NOT_STARTED:
        run.status = DogfoodRunStatus.RUNNING
        run.started_at = _now()

    # Terminal guard.
    if run.status in _TERMINAL_STATUSES:
        cp = DogfoodRunCheckpoint(
            checkpoint_id=f"cp-{uuid4().hex[:12]}", run_id=run.run_id,
            step_index=run.step_count, timestamp=_now(),
            lane="", action_taken="no_op", outcome="run_in_terminal_state",
            run_status=run.status, lane_statuses=dict(run.lane_statuses),
            blocking_reasons=list(run.blocking_reasons),
            next_suggested_action="none", cumulative_tokens=run.cumulative_tokens,
            cumulative_steps=run.step_count,
            wall_elapsed_seconds=_wall_elapsed(run),
        )
        append_checkpoint(cp, run.job_id, ddir)
        return run, cp

    # Evaluate.
    evaluation = evaluate_dogfood_run(run, ddir)

    # Build checkpoint.
    action = "evaluate_state"
    outcome = "evaluated"
    next_action = ""
    if evaluation.next_actions:
        na = evaluation.next_actions[0]
        action = na.get("action", "evaluate_state")
        outcome = na.get("reason", "evaluated")
        next_action = action

    run.step_count += 1
    run.status = evaluation.status
    run.current_lane = evaluation.active_lane
    run.lane_statuses = dict(evaluation.lane_statuses)
    run.blocking_reasons = list(evaluation.blocking_reasons)
    run.last_action = action
    run.next_suggested_action = next_action

    if evaluation.satisfied:
        run.finished_at = _now()

    if evaluation.status in _TERMINAL_STATUSES and not run.finished_at:
        run.finished_at = _now()

    cp = DogfoodRunCheckpoint(
        checkpoint_id=f"cp-{uuid4().hex[:12]}", run_id=run.run_id,
        step_index=run.step_count, timestamp=_now(),
        lane=evaluation.active_lane, action_taken=action, outcome=outcome,
        run_status=run.status, lane_statuses=dict(run.lane_statuses),
        blocking_reasons=list(run.blocking_reasons),
        next_suggested_action=next_action,
        cumulative_tokens=run.cumulative_tokens,
        cumulative_steps=run.step_count,
        wall_elapsed_seconds=_wall_elapsed(run),
    )

    append_checkpoint(cp, run.job_id, ddir)
    save_dogfood_run(run, ddir)
    return run, cp


def stop_dogfood_run(
    run: DogfoodRunRecord, *, reason: str = "operator_stop", data_dir: Path | None = None,
) -> DogfoodRunRecord:
    """Stop a dogfood run. Returns the updated record."""
    ddir = _resolve_ddir(data_dir)
    if run.status in _TERMINAL_STATUSES:
        return run
    run.status = DogfoodRunStatus.STOPPED_BY_OPERATOR
    run.stop_reason = reason
    run.finished_at = _now()
    save_dogfood_run(run, ddir)

    cp = DogfoodRunCheckpoint(
        checkpoint_id=f"cp-{uuid4().hex[:12]}", run_id=run.run_id,
        step_index=run.step_count, timestamp=_now(),
        lane="", action_taken="operator_stop", outcome=reason,
        run_status=run.status, lane_statuses=dict(run.lane_statuses),
        blocking_reasons=list(run.blocking_reasons),
        next_suggested_action="none",
        cumulative_tokens=run.cumulative_tokens,
        cumulative_steps=run.step_count,
        wall_elapsed_seconds=_wall_elapsed(run),
    )
    append_checkpoint(cp, run.job_id, ddir)
    return run


def _wall_elapsed(run: DogfoodRunRecord) -> float:
    if not run.started_at:
        return 0.0
    try:
        start = datetime.fromisoformat(run.started_at)
        return (datetime.now(timezone.utc) - start).total_seconds()
    except (ValueError, TypeError):
        return 0.0


# ---------------------------------------------------------------------------
# Replay analyzer (Phase 6)
# ---------------------------------------------------------------------------


@dataclass
class DogfoodLaneSummary:
    lane: str = ""
    step_count: int = 0
    first_step: int = 0
    last_step: int = 0
    outcomes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "lane": self.lane, "step_count": self.step_count,
            "first_step": self.first_step, "last_step": self.last_step,
            "outcomes": [_safe(o) for o in self.outcomes],
        }


@dataclass
class BlockingEpisode:
    start_step: int = 0
    end_step: int = 0
    reasons: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "start_step": self.start_step, "end_step": self.end_step,
            "reasons": list(self.reasons), "duration_seconds": self.duration_seconds,
        }


@dataclass
class DogfoodReplayAnalysis:
    run_id: str = ""
    job_id: str = ""
    run_status: str = ""
    total_steps: int = 0
    total_tokens: int = 0
    wall_elapsed_seconds: float = 0.0
    timeline: list[dict[str, Any]] = field(default_factory=list)
    lane_summaries: list[DogfoodLaneSummary] = field(default_factory=list)
    blocking_episodes: list[BlockingEpisode] = field(default_factory=list)
    token_curve: list[dict[str, Any]] = field(default_factory=list)
    anomalies: list[str] = field(default_factory=list)
    next_actions: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id, "job_id": self.job_id, "run_status": self.run_status,
            "total_steps": self.total_steps, "total_tokens": self.total_tokens,
            "wall_elapsed_seconds": self.wall_elapsed_seconds,
            "timeline": list(self.timeline),
            "lane_summaries": [ls.to_dict() for ls in self.lane_summaries],
            "blocking_episodes": [be.to_dict() for be in self.blocking_episodes],
            "token_curve": list(self.token_curve),
            "anomalies": list(self.anomalies),
            "next_actions": list(self.next_actions),
            "created_at": self.created_at,
        }


def analyze_dogfood_run_replay(
    run_id: str, job_id: str, *, data_dir: Path | None = None,
) -> DogfoodReplayAnalysis:
    """Analyze the checkpoint log for a dogfood run. Works on both completed and in-progress runs."""
    ddir = _resolve_ddir(data_dir)
    checkpoints = load_checkpoints(run_id, job_id, ddir)
    run_data = _load_json(_run_path(job_id, run_id, ddir))

    analysis = DogfoodReplayAnalysis(
        run_id=run_id, job_id=job_id,
        run_status=run_data.get("status", "unknown") if run_data else "unknown",
        created_at=_now(),
    )

    if not checkpoints:
        analysis.anomalies.append("no_checkpoints")
        return analysis

    analysis.total_steps = len(checkpoints)
    last_cp = checkpoints[-1]
    analysis.total_tokens = last_cp.cumulative_tokens
    analysis.wall_elapsed_seconds = last_cp.wall_elapsed_seconds

    # Build timeline.
    for cp in checkpoints:
        analysis.timeline.append({
            "step": cp.step_index, "lane": cp.lane,
            "action": _safe(cp.action_taken), "outcome": _safe(cp.outcome),
            "status": cp.run_status, "tokens": cp.cumulative_tokens,
        })

    # Lane summaries.
    lane_data: dict[str, DogfoodLaneSummary] = {}
    for cp in checkpoints:
        if not cp.lane:
            continue
        if cp.lane not in lane_data:
            lane_data[cp.lane] = DogfoodLaneSummary(lane=cp.lane, first_step=cp.step_index)
        ls = lane_data[cp.lane]
        ls.step_count += 1
        ls.last_step = cp.step_index
        ls.outcomes.append(_safe(cp.outcome, 100))
    analysis.lane_summaries = list(lane_data.values())

    # Blocking episodes.
    current_episode: BlockingEpisode | None = None
    for cp in checkpoints:
        if cp.blocking_reasons:
            if current_episode is None:
                current_episode = BlockingEpisode(start_step=cp.step_index, reasons=list(cp.blocking_reasons))
            else:
                current_episode.end_step = cp.step_index
                current_episode.reasons = list(set(current_episode.reasons + cp.blocking_reasons))
        else:
            if current_episode is not None:
                current_episode.end_step = cp.step_index - 1
                analysis.blocking_episodes.append(current_episode)
                current_episode = None
    if current_episode is not None:
        current_episode.end_step = last_cp.step_index
        analysis.blocking_episodes.append(current_episode)

    # Token curve.
    for cp in checkpoints:
        analysis.token_curve.append({
            "step": cp.step_index, "cumulative_tokens": cp.cumulative_tokens,
        })

    # Anomalies.
    activated_lanes = set(lane_data.keys())
    if run_data:
        policy = run_data.get("policy", {})
        allowed = set(policy.get("allowed_lanes", list(_ALL_LANES)))
        never_activated = allowed - activated_lanes - {DogfoodLane.BRAINSTORM}
        for lane in never_activated:
            if analysis.total_steps > 5:
                analysis.anomalies.append(f"lane_never_activated:{lane}")

        # Budget warnings.
        max_steps = policy.get("max_steps", 100)
        if max_steps > 0 and analysis.total_steps >= max_steps * 0.8:
            analysis.anomalies.append("approaching_step_budget")
        max_tokens = policy.get("max_tokens_estimated", 500_000)
        if max_tokens > 0 and analysis.total_tokens >= max_tokens * 0.8:
            analysis.anomalies.append("approaching_token_budget")

    # Next actions from last checkpoint.
    if last_cp.next_suggested_action and last_cp.next_suggested_action != "none":
        analysis.next_actions.append({
            "action": last_cp.next_suggested_action, "lane": last_cp.lane,
            "source": "last_checkpoint",
        })

    # Cache replay analysis.
    _atomic_write(_replay_path(job_id, run_id, ddir),
                  json.dumps(analysis.to_dict(), indent=2).encode("utf-8"))

    return analysis


# ---------------------------------------------------------------------------
# Integrity checks (Phase 11)
# ---------------------------------------------------------------------------


def dogfood_run_integrity(data_dir: Path | None = None) -> dict[str, Any]:
    """Run integrity checks across all dogfood runs."""
    ddir = _resolve_ddir(data_dir)
    out: dict[str, Any] = {"checks": [], "passed": True}
    runs = list_dogfood_runs(data_dir=ddir)

    for run_data in runs:
        run_id = run_data.get("run_id", "")
        job_id = run_data.get("job_id", "")
        status = run_data.get("status", "")

        # Check 1: status must be a known value.
        if status not in _ALL_STATUSES:
            out["checks"].append({"run_id": run_id, "code": "unknown_status", "value": status})
            out["passed"] = False

        # Check 2: terminal runs must have finished_at.
        if status in _TERMINAL_STATUSES and not run_data.get("finished_at"):
            out["checks"].append({"run_id": run_id, "code": "terminal_missing_finished_at"})
            out["passed"] = False

        # Check 3: step_count must match checkpoint count.
        checkpoints = load_checkpoints(run_id, job_id, ddir)
        actual_steps = len([c for c in checkpoints if c.action_taken != "no_op"])
        recorded = run_data.get("step_count", 0)
        if actual_steps != recorded and status != DogfoodRunStatus.NOT_STARTED:
            out["checks"].append({
                "run_id": run_id, "code": "step_count_mismatch",
                "recorded": recorded, "actual": actual_steps,
            })
            out["passed"] = False

        # Check 4: satisfied runs must not have open blockers.
        if status == DogfoodRunStatus.SATISFIED and run_data.get("blocking_reasons"):
            out["checks"].append({"run_id": run_id, "code": "satisfied_with_blockers"})
            out["passed"] = False

        # Check 5: policy must exist and have valid fields.
        policy = run_data.get("policy", {})
        if not policy:
            out["checks"].append({"run_id": run_id, "code": "missing_policy"})
            out["passed"] = False
        elif policy.get("max_steps", 0) <= 0:
            out["checks"].append({"run_id": run_id, "code": "invalid_max_steps"})
            out["passed"] = False

        # Check 6: lane_statuses keys must be known lanes.
        for lane in run_data.get("lane_statuses", {}):
            if lane not in _ALL_LANES:
                out["checks"].append({"run_id": run_id, "code": "unknown_lane", "lane": lane})
                out["passed"] = False

        # Check 7: cumulative tokens must be non-negative.
        if run_data.get("cumulative_tokens", 0) < 0:
            out["checks"].append({"run_id": run_id, "code": "negative_tokens"})
            out["passed"] = False

        # Check 8: run_id must be non-empty.
        if not run_id:
            out["checks"].append({"run_id": "(empty)", "code": "empty_run_id"})
            out["passed"] = False

        # Check 9 (R-0116): satisfied run must not have unsatisfied mission contract.
        if status == DogfoodRunStatus.SATISFIED:
            evidence = _gather_run_evidence(job_id, ddir)
            if evidence.get("contract_status") not in ("unknown", "contract_satisfied") and \
               not evidence.get("contract_satisfied", False):
                out["checks"].append({"run_id": run_id, "code": "satisfied_with_unsatisfied_mission"})
                out["passed"] = False

            # Check 10: satisfied run must not have open review findings.
            if evidence.get("open_review_findings", 0) > 0:
                policy = run_data.get("policy", {})
                if policy.get("require_clean_review", True):
                    out["checks"].append({"run_id": run_id, "code": "satisfied_with_open_findings",
                                          "count": evidence["open_review_findings"]})
                    out["passed"] = False

            # Check 11: satisfied run must not have failing tests.
            if evidence.get("failed_tests", 0) > 0:
                policy = run_data.get("policy", {})
                if policy.get("require_tests_green", True):
                    out["checks"].append({"run_id": run_id, "code": "satisfied_with_failing_tests",
                                          "count": evidence["failed_tests"]})
                    out["passed"] = False

        # Check 12: guardrail exceeded must produce terminal status.
        policy = run_data.get("policy", {})
        if status not in _TERMINAL_STATUSES:
            step_count = run_data.get("step_count", 0)
            max_steps = policy.get("max_steps", 100)
            if max_steps > 0 and step_count > max_steps:
                out["checks"].append({"run_id": run_id, "code": "guardrail_exceeded_without_terminal_status",
                                      "detail": f"steps {step_count} > max {max_steps}"})
                out["passed"] = False
            cum_tokens = run_data.get("cumulative_tokens", 0)
            max_tokens = policy.get("max_tokens_estimated", 500_000)
            if max_tokens > 0 and cum_tokens > max_tokens:
                out["checks"].append({"run_id": run_id, "code": "guardrail_exceeded_without_terminal_status",
                                      "detail": f"tokens {cum_tokens} > max {max_tokens}"})
                out["passed"] = False

        # Check 13: active lane/status coherence.
        current_lane = run_data.get("current_lane", "")
        lane_statuses = run_data.get("lane_statuses", {})
        if current_lane and lane_statuses:
            lane_st = lane_statuses.get(current_lane, "")
            if lane_st in ("done", "blocked") and status == DogfoodRunStatus.RUNNING:
                out["checks"].append({"run_id": run_id, "code": "active_lane_status_mismatch",
                                      "lane": current_lane, "lane_status": lane_st})
                out["passed"] = False

        # Check 14: replay export must not leak raw data.
        replay_file = _replay_path(job_id, run_id, ddir)
        replay_data = _load_json(replay_file)
        if replay_data:
            replay_str = json.dumps(replay_data)
            for marker in _RAW_MARKERS:
                if marker in replay_str:
                    out["checks"].append({"run_id": run_id, "code": "replay_raw_data_leak",
                                          "marker": marker[:20]})
                    out["passed"] = False
                    break

        # Check 15: brainstorm ideas with status=required must have evidence.
        brainstorm_dir = _run_dir(job_id, run_id, ddir) / "brainstorm"
        try:
            if brainstorm_dir.is_dir():
                for f in brainstorm_dir.iterdir():
                    if not f.is_file() or f.suffix != ".json":
                        continue
                    try:
                        idea = json.loads(f.read_text(encoding="utf-8"))
                        if idea.get("status") == "required" and not idea.get("evidence_needed"):
                            out["checks"].append({
                                "run_id": run_id, "code": "brainstorm_required_without_evidence",
                                "idea_id": idea.get("idea_id", "?"),
                            })
                            out["passed"] = False
                    except (OSError, ValueError):
                        continue
        except OSError:
            pass

    return out


# ---------------------------------------------------------------------------
# Export helpers
# ---------------------------------------------------------------------------


def export_dogfood_run_json(run: DogfoodRunRecord) -> dict[str, Any]:
    return run.to_dict()


def export_checkpoint_json(cp: DogfoodRunCheckpoint) -> dict[str, Any]:
    return cp.to_dict()


def export_replay_json(analysis: DogfoodReplayAnalysis) -> dict[str, Any]:
    return analysis.to_dict()


# ---------------------------------------------------------------------------
# Policy grant hook (Step 2748)
# ---------------------------------------------------------------------------


def _try_policy_grant(run: DogfoodRunRecord, ddir: Path) -> dict[str, Any]:
    """Try to grant execution approval via policy. Returns grant result dict.

    Never executes anything. Creates approval metadata only if policy allows.
    Extracts session_id and template_id from the run's next_suggested_action.
    """
    try:
        from packages.orchestration.execution_approval_policy import (
            create_policy_granted_execution_approval,
        )
    except ImportError:
        return {"granted": False}

    action = run.next_suggested_action or ""
    session_id = ""
    template_id = ""

    import re
    session_match = re.search(r"approve\s+(\S+)", action)
    if session_match:
        session_id = session_match.group(1)
    template_match = re.search(r"--template\s+(\S+)", action)
    if template_match:
        template_id = template_match.group(1)

    if not session_id or not template_id:
        return {"granted": False}

    try:
        return create_policy_granted_execution_approval(
            session_id, template_id, data_dir=ddir,
        )
    except Exception:
        return {"granted": False}


# ---------------------------------------------------------------------------
# Bounded mission run loop (Step 2589-2590)
# ---------------------------------------------------------------------------

_WAITING_STATUSES = frozenset({
    DogfoodRunStatus.WAITING_FOR_APPROVAL, DogfoodRunStatus.WAITING_FOR_BUILDER,
    DogfoodRunStatus.WAITING_FOR_REVIEW, DogfoodRunStatus.WAITING_FOR_TESTS,
})

_LOOP_STOP_REASONS = frozenset({
    "mission_satisfied", "blocked", "waiting_for_approval", "waiting_for_operator",
    "budget_exhausted", "operator_stopped", "max_steps_reached",
    "max_seconds_reached", "no_safe_next_action", "internal_error",
})


@dataclass
class MissionRunLoopResult:
    """Safe result from a bounded mission run loop iteration."""
    run_id: str = ""
    job_id: str = ""
    started_at: str = ""
    ended_at: str = ""
    steps_attempted: int = 0
    final_status: str = ""
    stop_reason: str = ""
    latest_checkpoint_id: str = ""
    next_safe_action: str = ""
    blocking_reasons: list[str] = field(default_factory=list)
    report_summary: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id, "job_id": self.job_id,
            "started_at": self.started_at, "ended_at": self.ended_at,
            "steps_attempted": self.steps_attempted,
            "final_status": self.final_status,
            "stop_reason": _safe(self.stop_reason),
            "latest_checkpoint_id": self.latest_checkpoint_id,
            "next_safe_action": _safe(self.next_safe_action),
            "blocking_reasons": list(self.blocking_reasons),
            "report_summary": _safe(self.report_summary),
            "errors": [_safe(e) for e in self.errors],
        }


def run_mission_loop(
    run_id: str, *, job_id: str = "",
    max_steps: int = 10, max_seconds: int = 300,
    data_dir: Path | None = None,
) -> MissionRunLoopResult:
    """Run a bounded mission loop. Calls step_dogfood_run() repeatedly until a stop condition.

    Stop conditions:
    - mission satisfied
    - blocked / waiting for approval / waiting for operator
    - budget exhausted
    - operator stopped
    - max_steps reached (loop-level cap, separate from policy cap)
    - max_seconds reached (wall clock for this loop invocation)
    - no safe next action
    - internal error

    No provider execution. No auto-approval. No auto-apply.
    """
    import time

    ddir = _resolve_ddir(data_dir)

    result = MissionRunLoopResult(
        run_id=run_id, started_at=_now(),
    )

    run = load_dogfood_run(run_id, job_id, ddir)
    if run is None:
        # Try searching across jobs if job_id empty.
        if not job_id:
            runs = list_dogfood_runs(data_dir=ddir)
            for r in runs:
                if r.get("run_id") == run_id:
                    run = load_dogfood_run(run_id, r.get("job_id", ""), ddir)
                    break
        if run is None:
            result.stop_reason = "internal_error"
            result.errors.append(f"run not found: {run_id}")
            result.ended_at = _now()
            return result

    result.job_id = run.job_id
    start_time = time.monotonic()
    steps_done = 0

    while steps_done < max_steps:
        elapsed = time.monotonic() - start_time
        if elapsed >= max_seconds:
            result.stop_reason = "max_seconds_reached"
            break

        if run.status in _TERMINAL_STATUSES:
            if run.status == DogfoodRunStatus.SATISFIED:
                result.stop_reason = "mission_satisfied"
            elif run.status == DogfoodRunStatus.BLOCKED:
                result.stop_reason = "blocked"
            elif run.status == DogfoodRunStatus.STOPPED_BY_OPERATOR:
                result.stop_reason = "operator_stopped"
            elif run.status == DogfoodRunStatus.BUDGET_EXHAUSTED:
                result.stop_reason = "budget_exhausted"
            else:
                result.stop_reason = "internal_error"
            break

        if run.status in _WAITING_STATUSES:
            if run.status == DogfoodRunStatus.WAITING_FOR_APPROVAL:
                policy_result = _try_policy_grant(run, ddir)
                if policy_result.get("granted"):
                    result.report_summary = (
                        f"policy_grant:{policy_result.get('approval_id', '')}"
                    )
                    run.status = DogfoodRunStatus.RUNNING
                    save_dogfood_run(run, data_dir=ddir)
                    continue
                result.stop_reason = "waiting_for_approval"
            else:
                result.stop_reason = "waiting_for_operator"
            break

        try:
            run, cp = step_dogfood_run(run, data_dir=ddir)
            steps_done += 1
            result.latest_checkpoint_id = cp.checkpoint_id

            if cp.next_suggested_action and cp.next_suggested_action != "none":
                result.next_safe_action = cp.next_suggested_action
            else:
                result.stop_reason = "no_safe_next_action"
                break

        except Exception as exc:
            result.stop_reason = "internal_error"
            result.errors.append(str(exc)[:200])
            break

    if not result.stop_reason and steps_done >= max_steps:
        result.stop_reason = "max_steps_reached"

    result.steps_attempted = steps_done
    result.final_status = run.status
    result.blocking_reasons = list(run.blocking_reasons)
    result.ended_at = _now()
    policy_note = ""
    if result.report_summary and result.report_summary.startswith("policy_grant:"):
        policy_note = f" [{result.report_summary}]"
    result.report_summary = (
        f"{steps_done} steps, status={run.status}, stop={result.stop_reason}"
        f"{policy_note}"
    )
    return result


# ---------------------------------------------------------------------------
# Morning report (Steps 2592-2593, 2598, 2600-2601)
# ---------------------------------------------------------------------------


@dataclass
class MissionMorningReport:
    """Safe morning report for operator inspection. No raw logs/output/prompts/secrets."""
    run_id: str = ""
    job_id: str = ""
    mission_status: str = ""
    final_status: str = ""
    stopped_because: str = ""
    steps_completed: int = 0
    budget_remaining_steps: int = 0
    budget_remaining_tokens: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    waiting_for_approval: list[str] = field(default_factory=list)
    builder_execution_summary: dict[str, Any] = field(default_factory=dict)
    sandbox_intake_summary: dict[str, Any] = field(default_factory=dict)
    review_summary: dict[str, Any] = field(default_factory=dict)
    test_summary: dict[str, Any] = field(default_factory=dict)
    self_repair_summary: dict[str, Any] = field(default_factory=dict)
    core_readiness: dict[str, Any] = field(default_factory=dict)
    evidence_refs: list[str] = field(default_factory=list)
    next_safe_action: str = ""
    operator_summary: str = ""
    created_at: str = ""
    policy_considered: bool = False
    policy_decision_code: str = ""
    policy_granted_approval: bool = False
    policy_id: str = ""
    manual_approval_required: bool = True
    policy_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id, "job_id": self.job_id,
            "mission_status": self.mission_status,
            "final_status": self.final_status,
            "stopped_because": _safe(self.stopped_because),
            "steps_completed": self.steps_completed,
            "budget_remaining_steps": self.budget_remaining_steps,
            "budget_remaining_tokens": self.budget_remaining_tokens,
            "completed_items": [_safe(i) for i in self.completed_items],
            "blocked_items": [_safe(i) for i in self.blocked_items],
            "waiting_for_approval": [_safe(i) for i in self.waiting_for_approval],
            "builder_execution_summary": dict(self.builder_execution_summary),
            "sandbox_intake_summary": dict(self.sandbox_intake_summary),
            "review_summary": dict(self.review_summary),
            "test_summary": dict(self.test_summary),
            "self_repair_summary": dict(self.self_repair_summary),
            "core_readiness": dict(self.core_readiness),
            "evidence_refs": list(self.evidence_refs),
            "next_safe_action": _safe(self.next_safe_action),
            "operator_summary": _safe(self.operator_summary, 500),
            "created_at": self.created_at,
            "policy_considered": self.policy_considered,
            "policy_decision_code": self.policy_decision_code,
            "policy_granted_approval": self.policy_granted_approval,
            "policy_id": self.policy_id,
            "manual_approval_required": self.manual_approval_required,
            "policy_reason": _safe(self.policy_reason),
        }


def _build_core_readiness(job_id: str, ddir: Path) -> dict[str, Any]:
    """Check readiness of each component in the core run path."""
    readiness: dict[str, Any] = {}

    try:
        from packages.orchestration.overnight_mission import list_mission_contracts
        contracts = list_mission_contracts(job_id=job_id, data_dir=ddir)
        readiness["mission_contract"] = len(contracts) > 0
    except (ImportError, Exception):
        readiness["mission_contract"] = False

    runs = list_dogfood_runs(job_id=job_id, data_dir=ddir)
    readiness["run_exists"] = len(runs) > 0

    try:
        from packages.orchestration.main_builder_adapter import (
            get_builder_adapter_spec,
            list_builder_sessions,
        )
        claude_adapter = get_builder_adapter_spec("claude-code-v0")
        readiness["builder_adapter_available"] = claude_adapter is not None
        readiness["builder_adapter_enabled"] = bool(claude_adapter and claude_adapter.get("enabled", False))
        sessions = list_builder_sessions(job_id, data_dir=ddir)
        readiness["builder_sessions"] = len(sessions)
    except (ImportError, Exception):
        readiness["builder_adapter_available"] = False
        readiness["builder_adapter_enabled"] = False
        readiness["builder_sessions"] = 0

    try:
        from packages.orchestration.managed_builder_execution import (
            get_command_template,
            list_execution_approvals,
        )
        claude_tmpl = get_command_template("claude-code-repair-v0")
        readiness["claude_template_available"] = claude_tmpl is not None
        readiness["claude_template_enabled"] = bool(claude_tmpl and claude_tmpl.get("enabled", False))
        approvals = list_execution_approvals()
        readiness["approval_count"] = len(approvals)
    except (ImportError, Exception):
        readiness["claude_template_available"] = False
        readiness["claude_template_enabled"] = False
        readiness["approval_count"] = 0

    try:
        from packages.orchestration.self_repair_proposal import list_self_repair_proposals
        proposals = list_self_repair_proposals(job_id=job_id, data_dir=ddir)
        readiness["self_repair_proposals"] = len(proposals)
    except (ImportError, Exception):
        readiness["self_repair_proposals"] = 0

    return readiness


def _build_builder_execution_summary(job_id: str, ddir: Path) -> dict[str, Any]:
    """Safe builder/execution summary for morning report."""
    summary: dict[str, Any] = {}
    try:
        from packages.orchestration.main_builder_adapter import list_builder_sessions
        sessions = list_builder_sessions(job_id, data_dir=ddir)
        summary["session_count"] = len(sessions)
        if sessions:
            latest = sessions[-1]
            summary["latest_session_status"] = latest.get("status", "unknown")
            summary["latest_adapter_id"] = latest.get("adapter_id", "")
            summary["output_ref_exists"] = bool(latest.get("output_artifact_ref"))
            summary["intake_pending"] = latest.get("status") in (
                "candidate_received", "package_ready", "submitted")
        else:
            summary["latest_session_status"] = "none"
            summary["output_ref_exists"] = False
            summary["intake_pending"] = False
    except (ImportError, Exception):
        summary["latest_session_status"] = "unavailable"
        summary["output_ref_exists"] = False
        summary["intake_pending"] = False

    try:
        from packages.orchestration.managed_builder_execution import list_execution_results
        results = list_execution_results(job_id, data_dir=ddir)
        summary["execution_count"] = len(results)
        if results:
            latest = results[-1]
            summary["latest_execution_status"] = latest.get("status", "unknown")
        else:
            summary["latest_execution_status"] = "none"
    except (ImportError, Exception):
        summary["execution_count"] = 0
        summary["latest_execution_status"] = "unavailable"

    return summary


def _build_self_repair_summary(job_id: str, ddir: Path) -> dict[str, Any]:
    """Safe self-repair proposal summary for morning report."""
    summary: dict[str, Any] = {}
    try:
        from packages.orchestration.self_repair_proposal import list_self_repair_proposals
        proposals = list_self_repair_proposals(job_id=job_id, data_dir=ddir)
        summary["proposal_count"] = len(proposals)
        awaiting = sum(1 for p in proposals if p.get("status") in ("awaiting_operator", "edited"))
        summary["awaiting_approval"] = awaiting
        if proposals:
            latest = proposals[-1]
            summary["latest_status"] = latest.get("status", "unknown")
            summary["inspect_command"] = "remedy self-repair proposal-list --json"
        else:
            summary["latest_status"] = "none"
    except (ImportError, Exception):
        summary["proposal_count"] = 0
        summary["awaiting_approval"] = 0
        summary["latest_status"] = "unavailable"
    return summary


def build_mission_morning_report(
    run_id: str, *, job_id: str = "", data_dir: Path | None = None,
) -> MissionMorningReport:
    """Build a safe morning report from existing evidence. Read-only, no execution."""
    ddir = _resolve_ddir(data_dir)
    report = MissionMorningReport(run_id=run_id, created_at=_now())

    run = load_dogfood_run(run_id, job_id, ddir)
    if run is None and not job_id:
        runs = list_dogfood_runs(data_dir=ddir)
        for r in runs:
            if r.get("run_id") == run_id:
                run = load_dogfood_run(run_id, r.get("job_id", ""), ddir)
                break
    if run is None:
        report.operator_summary = f"Run not found: {run_id}"
        return report

    report.job_id = run.job_id
    report.final_status = run.status
    report.stopped_because = run.stop_reason
    report.steps_completed = run.step_count

    ev = evaluate_dogfood_run(run, ddir)
    report.mission_status = "satisfied" if ev.satisfied else ev.status
    report.budget_remaining_steps = ev.budget_remaining_steps
    report.budget_remaining_tokens = ev.budget_remaining_tokens

    if ev.next_actions:
        report.next_safe_action = ev.next_actions[0].get("action", "")

    for reason in run.blocking_reasons:
        report.blocked_items.append(reason)

    if run.status == DogfoodRunStatus.WAITING_FOR_APPROVAL:
        report.waiting_for_approval.append("execution_approval_needed")
        try:
            from packages.orchestration.execution_approval_policy import (
                execution_approval_policy_summary,
            )
            pol_summary = execution_approval_policy_summary(ddir)
            enabled_count = pol_summary.get("enabled_policy_count", 0)
            report.policy_considered = enabled_count > 0
            report.manual_approval_required = pol_summary.get(
                "manual_approval_required", True,
            )
            report.policy_decision_code = pol_summary.get(
                "latest_decision_code", "",
            )
            enabled_ids = pol_summary.get("enabled_policy_ids", [])
            if enabled_ids:
                report.policy_id = enabled_ids[0]
            report.policy_reason = (
                f"{enabled_count} enabled policies, "
                f"{pol_summary.get('grant_count', 0)} grants"
            )
        except (ImportError, Exception):
            pass

    if ev.satisfied:
        report.completed_items.append("mission_contract_satisfied")

    report.core_readiness = _build_core_readiness(run.job_id, ddir)
    report.builder_execution_summary = _build_builder_execution_summary(run.job_id, ddir)
    report.self_repair_summary = _build_self_repair_summary(run.job_id, ddir)

    # Test summary from evidence.
    evidence = ev.evidence
    report.test_summary = {
        "status": evidence.get("tests_status", "unavailable"),
        "failed_count": evidence.get("failed_tests", 0),
    }

    # Review summary.
    report.review_summary = {
        "open_findings": evidence.get("open_review_findings", 0),
    }

    # Sandbox intake.
    report.sandbox_intake_summary = {
        "intake_pending": report.builder_execution_summary.get("intake_pending", False),
        "output_ref_exists": report.builder_execution_summary.get("output_ref_exists", False),
    }

    # Evidence refs.
    checkpoints = load_checkpoints(run_id, run.job_id, ddir)
    if checkpoints:
        report.evidence_refs.append(f"checkpoints:{len(checkpoints)}")
    replay = _load_json(_replay_path(run.job_id, run_id, ddir))
    if replay:
        report.evidence_refs.append("replay_analysis")

    # Operator summary.
    parts: list[str] = []
    parts.append(f"Run {run_id}: {run.status}.")
    if run.stop_reason:
        parts.append(f"Stopped: {run.stop_reason}.")
    parts.append(f"{run.step_count} steps completed.")
    if ev.budget_remaining_steps <= 0:
        parts.append("Step budget exhausted.")
    if report.self_repair_summary.get("awaiting_approval", 0) > 0:
        parts.append(f"{report.self_repair_summary['awaiting_approval']} self-repair proposals awaiting approval.")
    if report.next_safe_action:
        parts.append(f"Next: {report.next_safe_action}.")
    report.operator_summary = " ".join(parts)

    return report


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    # Statuses + lanes.
    "DogfoodRunStatus", "DogfoodLane", "LaneStatus",
    "_ALL_STATUSES", "_TERMINAL_STATUSES", "_ALL_LANES",
    # Models.
    "DogfoodRunPolicy", "DogfoodRunRecord", "DogfoodRunCheckpoint",
    "DogfoodRunEvaluation", "BrainstormIdea",
    "DogfoodLaneSummary", "BlockingEpisode", "DogfoodReplayAnalysis",
    # Storage.
    "create_dogfood_run", "save_dogfood_run", "load_dogfood_run", "list_dogfood_runs",
    "append_checkpoint", "load_checkpoints",
    "save_brainstorm_idea", "list_brainstorm_ideas",
    # Evaluator.
    "evaluate_dogfood_run",
    # Stepping.
    "step_dogfood_run", "stop_dogfood_run",
    # Replay.
    "analyze_dogfood_run_replay",
    # Bounded loop.
    "MissionRunLoopResult", "run_mission_loop",
    # Morning report.
    "MissionMorningReport", "build_mission_morning_report",
    # Integrity.
    "dogfood_run_integrity",
    # Export.
    "export_dogfood_run_json", "export_checkpoint_json", "export_replay_json",
    # Schema.
    "SCHEMA_VERSION",
]
