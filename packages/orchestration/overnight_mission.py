"""
Overnight Mission Contract + Review/Repair Spine v0 (Steps 1837-1876).

The first hard mission-contract spine for Overnight Mode. A user gives Remedy a mission/prompt; Remedy
turns it into a CONTRACT and tracks it until the contract is fulfilled or safely blocked. Satisfaction
is decided from DURABLE EVIDENCE (progress ledger, review findings, tests/proof/snapshot gates, repair
status, route/token/tournament readiness) — never from builder self-report.

  Workers execute. Remedy governs. The Mission Contract decides whether work is done.

This module is METADATA + STATE-MACHINE + EVALUATION + REPORTING only. It NEVER calls a provider/
Claude/Pi/OpenCode/Ollama/cloud/local model, the network, a browser, a subprocess, or a shell; it
never executes a worker, runs a test, applies/approves a patch, or automates git/PR. It builds no
internal MemPalace memory / embeddings / vector DB (MemPalace is a future EXTERNAL adapter).

Hard rules enforced here:
  - NO provider/model/Ollama/cloud/local execution, network, browser, subprocess, shell.
  - NO worker execution, test run, apply/approve, git/PR automation, MemPalace/memory, MCP, pricing.
  - Reviewer verdict beats builder self-report; a Done marker is NOT Resolved.
  - Open Blocker/High review findings block contract satisfaction.
  - Missing required gates (tests green / proof chain / snapshot) block satisfaction.
  - Contract is NEVER satisfied from builder self-report alone; no fake overnight readiness.
  - Required blockers (needed for the current contract) are kept separate from optional future ideas.
  - No raw prompts (beyond a scrubbed user_goal summary)/logs/diffs/secrets/absolute paths in exports.

Public API::

    create_mission_contract_from_job(job_id, *, user_goal="", acceptance_criteria=None,
        autonomy_level=1, required_gates=None, data_dir=None) -> MissionContract
    save/load/list_mission_contract(s); save/list_mission_cycle(s);
    save/load_latest_mission_evaluation
    evaluate_mission_contract(contract, data_dir=None) -> MissionEvaluation
    mission_next_safe_actions(contract, evaluation) -> list[dict]
    mission_state_machine(evaluation) -> str  (phase)
    mission_readiness(job_id, data_dir=None) -> dict
    mission_integrity(data_dir=None, evaluations=None) -> dict
    export_*_json(...) -> dict
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.provider_trust import _safe_path_label, _scrub_public


SCHEMA_VERSION = "overnight-mission-v0"
_OM_DIRNAME = "overnight_mission"
_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-ant", "sk-proj",
                "api_key", "password", "secret_key")


class MissionStatus:
    NOT_STARTED = "not_started"
    NEEDS_USER_ACCEPTANCE_CRITERIA = "needs_user_acceptance_criteria"
    READY = "ready"
    RUNNING_METADATA_ONLY = "running_metadata_only"
    WAITING_FOR_WORKER = "waiting_for_worker"
    WAITING_FOR_REVIEW = "waiting_for_review"
    REPAIR_NEEDED = "repair_needed"
    WAITING_FOR_USER = "waiting_for_user"
    BLOCKED = "blocked"
    CONTRACT_SATISFIED = "contract_satisfied"


class MissionPhase:
    PLAN = "plan"
    ROUTE = "route"
    WORKER_WAIT = "worker_wait"
    REVIEW = "review"
    REPAIR = "repair"
    TEST_GATE = "test_gate"
    PROOF_GATE = "proof_gate"
    USER_DECISION = "user_decision"
    BLOCKED = "blocked"
    SATISFIED = "satisfied"


# Required-gate vocabulary.
GATE_CLEAN_REVIEW = "clean_review"
GATE_TESTS_GREEN = "tests_green"
GATE_PROOF_CHAIN = "proof_chain"
GATE_SNAPSHOT_BEFORE_APPLY = "snapshot_before_apply"
GATE_ROLLBACK_RESTORE = "rollback_restore_available"

_DEFAULT_FORBIDDEN = (
    "arbitrary_shell", "network_fetch", "install_packages", "cloud_provider",
    "apply_patch_without_approval", "modify_permissions_autonomously",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scrub_goal(goal: str) -> str:
    return _scrub_public(goal or "")[:300]


# ---------------------------------------------------------------------------
# Models (Step 1839)
# ---------------------------------------------------------------------------


@dataclass
class MissionContract:
    contract_id: str = ""
    job_id: str = ""
    user_goal: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    allowed_actions: list[str] = field(default_factory=list)
    forbidden_actions: list[str] = field(default_factory=lambda: list(_DEFAULT_FORBIDDEN))
    required_gates: list[str] = field(default_factory=lambda: [GATE_CLEAN_REVIEW])
    max_cycles: int = 10
    max_runtime_minutes: int = 60
    max_test_runs: int = 0
    max_estimated_tokens: int = 200_000
    autonomy_level: int = 1
    require_clean_review: bool = True
    require_tests_green: bool = False
    require_proof_chain: bool = False
    require_snapshot_before_apply: bool = True
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id, "job_id": self.job_id,
            "user_goal": _scrub_goal(self.user_goal),
            "acceptance_criteria": [_scrub_public(c)[:200] for c in self.acceptance_criteria],
            "allowed_actions": list(self.allowed_actions),
            "forbidden_actions": list(self.forbidden_actions),
            "required_gates": list(self.required_gates), "max_cycles": self.max_cycles,
            "max_runtime_minutes": self.max_runtime_minutes, "max_test_runs": self.max_test_runs,
            "max_estimated_tokens": self.max_estimated_tokens, "autonomy_level": self.autonomy_level,
            "require_clean_review": self.require_clean_review,
            "require_tests_green": self.require_tests_green,
            "require_proof_chain": self.require_proof_chain,
            "require_snapshot_before_apply": self.require_snapshot_before_apply,
            "created_at": self.created_at, "updated_at": self.updated_at,
            "schema_version": SCHEMA_VERSION,
        }


@dataclass
class MissionCycle:
    cycle_id: str = ""
    contract_id: str = ""
    job_id: str = ""
    cycle_index: int = 0
    phase: str = MissionPhase.PLAN
    inputs_summary: str = ""
    actions_considered: list[str] = field(default_factory=list)
    next_safe_action: str = ""
    blocking_reasons: list[str] = field(default_factory=list)
    review_findings_open: int = 0
    tests_status: str = "unknown"
    proof_status: str = "unknown"
    repair_status: str = "unknown"
    user_decision_required: bool = False
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle_id": self.cycle_id, "contract_id": self.contract_id, "job_id": self.job_id,
            "cycle_index": self.cycle_index, "phase": self.phase,
            "inputs_summary": self.inputs_summary, "actions_considered": list(self.actions_considered),
            "next_safe_action": self.next_safe_action, "blocking_reasons": list(self.blocking_reasons),
            "review_findings_open": self.review_findings_open, "tests_status": self.tests_status,
            "proof_status": self.proof_status, "repair_status": self.repair_status,
            "user_decision_required": self.user_decision_required, "created_at": self.created_at,
            "schema_version": SCHEMA_VERSION,
        }


@dataclass
class MissionEvaluation:
    contract_id: str = ""
    job_id: str = ""
    status: str = MissionStatus.NOT_STARTED
    satisfied: bool = False
    phase: str = MissionPhase.PLAN
    unsatisfied_criteria: list[str] = field(default_factory=list)
    open_review_findings: int = 0
    open_tasks: int = 0
    failed_tests: int = 0
    missing_proofs: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    required_next_actions: list[dict] = field(default_factory=list)
    optional_next_ideas: list[dict] = field(default_factory=list)
    next_safe_actions: list[str] = field(default_factory=list)
    user_decision_required: bool = False
    user_summary: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": 1, "contract_id": self.contract_id, "job_id": self.job_id,
            "status": self.status, "satisfied": self.satisfied, "phase": self.phase,
            "unsatisfied_criteria": list(self.unsatisfied_criteria),
            "open_review_findings": self.open_review_findings, "open_tasks": self.open_tasks,
            "failed_tests": self.failed_tests, "missing_proofs": list(self.missing_proofs),
            "blocked_reasons": list(self.blocked_reasons),
            "required_next_actions": list(self.required_next_actions),
            "optional_next_ideas": list(self.optional_next_ideas),
            "next_safe_actions": list(self.next_safe_actions),
            "user_decision_required": self.user_decision_required, "user_summary": self.user_summary,
            "created_at": self.created_at, "schema_version": SCHEMA_VERSION,
        }


def export_mission_contract_json(c: MissionContract) -> dict[str, Any]:
    return c.to_dict()


def export_mission_evaluation_json(e: MissionEvaluation) -> dict[str, Any]:
    return e.to_dict()


def validate_mission_contract(c: MissionContract) -> list[str]:
    errors: list[str] = []
    if not c.contract_id:
        errors.append("contract_id is empty")
    if c.max_cycles < 0:
        errors.append("max_cycles must be >= 0")
    if c.autonomy_level < 0:
        errors.append("autonomy_level must be >= 0")
    bad_gates = [g for g in c.required_gates
                 if g not in (GATE_CLEAN_REVIEW, GATE_TESTS_GREEN, GATE_PROOF_CHAIN,
                              GATE_SNAPSHOT_BEFORE_APPLY, GATE_ROLLBACK_RESTORE)]
    if bad_gates:
        errors.append(f"unknown required_gates: {bad_gates}")
    return errors


# ---------------------------------------------------------------------------
# Storage (Step 1840)
# ---------------------------------------------------------------------------


def _om_root(job_id: str, data_dir: Path) -> Path:
    base = job_id if job_id else "orchestrator"
    return data_dir / "workspaces" / base / _OM_DIRNAME


def _contract_path(job_id: str, contract_id: str, data_dir: Path) -> Path:
    return _om_root(job_id, data_dir) / contract_id / "contract.json"


def _cycle_path(job_id: str, contract_id: str, cycle_id: str, data_dir: Path) -> Path:
    return _om_root(job_id, data_dir) / contract_id / "cycles" / f"{cycle_id}.json"


def _eval_path(job_id: str, contract_id: str, data_dir: Path) -> Path:
    return _om_root(job_id, data_dir) / contract_id / "evaluation.json"


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


def _resolve_ddir(data_dir: Path | None) -> Path:
    from packages.orchestration.data_paths import resolve_data_root
    return Path(data_dir) if data_dir is not None else resolve_data_root()


def save_mission_contract(contract: MissionContract, data_dir: Path | None = None) -> bool:
    ddir = _resolve_ddir(data_dir)
    if not contract.created_at:
        contract.created_at = _now()
    contract.updated_at = _now()
    return _atomic_write(_contract_path(contract.job_id, contract.contract_id, ddir),
                         json.dumps(contract.to_dict(), indent=2).encode("utf-8"))


def _contract_from_dict(d: dict) -> MissionContract:
    return MissionContract(
        contract_id=str(d.get("contract_id", "")), job_id=str(d.get("job_id", "")),
        user_goal=str(d.get("user_goal", "")),
        acceptance_criteria=list(d.get("acceptance_criteria", [])),
        allowed_actions=list(d.get("allowed_actions", [])),
        forbidden_actions=list(d.get("forbidden_actions", list(_DEFAULT_FORBIDDEN))),
        required_gates=list(d.get("required_gates", [GATE_CLEAN_REVIEW])),
        max_cycles=int(d.get("max_cycles", 10)),
        max_runtime_minutes=int(d.get("max_runtime_minutes", 60)),
        max_test_runs=int(d.get("max_test_runs", 0)),
        max_estimated_tokens=int(d.get("max_estimated_tokens", 200_000)),
        autonomy_level=int(d.get("autonomy_level", 1)),
        require_clean_review=bool(d.get("require_clean_review", True)),
        require_tests_green=bool(d.get("require_tests_green", False)),
        require_proof_chain=bool(d.get("require_proof_chain", False)),
        require_snapshot_before_apply=bool(d.get("require_snapshot_before_apply", True)),
        created_at=str(d.get("created_at", "")), updated_at=str(d.get("updated_at", "")))


def list_mission_contracts(job_id: str | None = None, data_dir: Path | None = None) -> list[dict]:
    ddir = _resolve_ddir(data_dir)
    roots: list[Path] = []
    ws = ddir / "workspaces"
    if job_id:
        roots.append(_om_root(job_id, ddir))
    else:
        try:
            for child in ws.iterdir():
                roots.append(child / _OM_DIRNAME)
        except OSError:
            pass
    out: list[dict] = []
    for root in roots:
        try:
            for child in sorted(root.iterdir()):
                f = child / "contract.json"
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


def load_mission_contract(contract_id: str, data_dir: Path | None = None) -> dict | None:
    return next((c for c in list_mission_contracts(data_dir=data_dir)
                 if c.get("contract_id") == contract_id), None)


def save_mission_cycle(cycle: MissionCycle, data_dir: Path | None = None) -> bool:
    ddir = _resolve_ddir(data_dir)
    if not cycle.created_at:
        cycle.created_at = _now()
    return _atomic_write(_cycle_path(cycle.job_id, cycle.contract_id, cycle.cycle_id, ddir),
                         json.dumps(cycle.to_dict(), indent=2).encode("utf-8"))


def list_mission_cycles(contract_id: str, data_dir: Path | None = None) -> list[dict]:
    ddir = _resolve_ddir(data_dir)
    c = load_mission_contract(contract_id, ddir)
    if c is None:
        return []
    root = _om_root(c.get("job_id", ""), ddir) / contract_id / "cycles"
    out: list[dict] = []
    try:
        for f in sorted(root.iterdir()):
            if not f.is_file() or f.suffix != ".json":
                continue
            try:
                out.append(json.loads(f.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                continue
    except OSError:
        return out
    out.sort(key=lambda r: r.get("cycle_index", 0))
    return out


def save_mission_evaluation(ev: MissionEvaluation, data_dir: Path | None = None) -> bool:
    ddir = _resolve_ddir(data_dir)
    if not ev.created_at:
        ev.created_at = _now()
    return _atomic_write(_eval_path(ev.job_id, ev.contract_id, ddir),
                         json.dumps(ev.to_dict(), indent=2).encode("utf-8"))


def load_latest_mission_evaluation(contract_id: str, data_dir: Path | None = None) -> dict | None:
    ddir = _resolve_ddir(data_dir)
    c = load_mission_contract(contract_id, ddir)
    if c is None:
        return None
    f = _eval_path(c.get("job_id", ""), contract_id, ddir)
    try:
        if f.is_file():
            return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return None


# ---------------------------------------------------------------------------
# Contract creation (Step 1841)
# ---------------------------------------------------------------------------


def create_mission_contract_from_job(
    job_id: str, *, user_goal: str = "", acceptance_criteria: list[str] | None = None,
    autonomy_level: int = 1, required_gates: list[str] | None = None,
    max_cycles: int = 10, max_estimated_tokens: int = 200_000, data_dir: Path | None = None,
) -> MissionContract:
    """Create a conservative mission contract from a job. If acceptance criteria are missing the
    contract is valid but will evaluate to ``needs_user_acceptance_criteria`` (never fake-complete).
    Defaults are conservative: clean review required; tests/proof not auto-required (no real test
    execution exists yet — required gates report honestly as unavailable when set)."""
    ddir = _resolve_ddir(data_dir)
    goal = user_goal
    if not goal and job_id:
        try:
            from uuid import UUID
            from packages.orchestration.storage import load_job
            job = load_job(UUID(job_id), ddir)
            goal = job.user_prompt or job.name or ""
        except Exception:
            goal = ""
    gates = list(required_gates) if required_gates is not None else [GATE_CLEAN_REVIEW]
    contract = MissionContract(
        contract_id=f"msn-{uuid4().hex[:12]}", job_id=job_id, user_goal=goal,
        acceptance_criteria=list(acceptance_criteria or []), required_gates=gates,
        autonomy_level=max(0, autonomy_level), max_cycles=max_cycles,
        max_estimated_tokens=max_estimated_tokens, created_at=_now())
    contract.require_tests_green = GATE_TESTS_GREEN in gates
    contract.require_proof_chain = GATE_PROOF_CHAIN in gates
    contract.require_clean_review = GATE_CLEAN_REVIEW in gates or True
    save_mission_contract(contract, ddir)
    return contract


# ---------------------------------------------------------------------------
# Evidence gathering (Steps 1842/1843)
# ---------------------------------------------------------------------------


def _review_findings() -> Any:
    from packages.orchestration.overnight_executor import parse_review_findings
    return parse_review_findings()


def _gather_mission_evidence(job_id: str, data_dir: Path) -> dict[str, Any]:
    """Collect SAFE durable signals for mission evaluation. Read-only; absence → honest unknown."""
    ev: dict[str, Any] = {
        "open_tasks": 0, "blocked_tasks": 0, "failed_tests": 0, "tests_status": "unavailable",
        "proof_status": "unavailable", "repair_status": "unknown", "ledger_available": False,
        "snapshot_recorded": False, "rollback_restore_available": False,
        "repair_loop_open": 0, "repair_loop_blocked": 0, "repair_loop_user_decision": False,
        "builder_adapter_active": False, "builder_adapter_blocked": 0,
        "builder_adapter_user_decision": False,
    }
    job = None
    events: list[dict] = []
    try:
        from uuid import UUID
        from packages.orchestration.storage import load_job
        from packages.orchestration.timeline import load_run_events
        job = load_job(UUID(job_id), data_dir)
        events = load_run_events(data_dir, job.id)
    except Exception:
        job = None

    # Progress ledger (open tasks, failed tests, blocked).
    if job is not None:
        try:
            from packages.orchestration.progress_ledger import build_progress_ledger, ProgressStatus
            ledger = build_progress_ledger(job=job, events=events)
            ev["ledger_available"] = True
            open_tasks = 0
            failed = 0
            blocked = 0
            test_pass = False
            for it in ledger.items:
                iid = str(it.item_id)
                # The mission's OWN status surface (mission-*) must NOT be counted as a real open
                # task — build_progress_ledger merges this contract's own items, so counting them
                # would make the evaluator self-block (R-0102). Also skip pure forward-looking
                # feature suggestions. Genuine job/task/repair/test blockers are still counted.
                if iid.startswith(("mission-", "token-economy-local", "route-policy-local",
                                   "tournament-winner")):
                    continue
                if it.status in (ProgressStatus.PLANNED, ProgressStatus.IN_PROGRESS):
                    open_tasks += 1
                if it.status == ProgressStatus.BLOCKED:
                    blocked += 1
                    open_tasks += 1
                if "test-fail" in str(it.item_id) or "cont-test-fail" in str(it.item_id):
                    failed += 1
                if str(it.item_id).startswith(("test-pass", "cont-test-pass")):
                    test_pass = True
            ev["open_tasks"] = open_tasks
            ev["blocked_tasks"] = blocked
            ev["failed_tests"] = failed
            ev["tests_status"] = ("failing" if failed > 0 else "green" if test_pass else "unavailable")
        except Exception:
            pass

    # Proof chain (safe overall status only).
    if job is not None:
        try:
            from packages.orchestration.proof_chain import build_proof_chain
            pc = build_proof_chain(job, events, data_dir=data_dir)
            ev["proof_status"] = getattr(pc, "overall_status", "unverified")
        except Exception:
            ev["proof_status"] = "unavailable"

    # Real test execution + snapshot/rollback proof (Step 1886). The latest REAL test run overrides
    # the ledger-derived tests_status; snapshot/rollback availability come from honest proofs.
    if job_id:
        try:
            from packages.orchestration.real_test_execution import (
                list_test_runs, list_snapshot_proofs, list_rollback_proofs,
            )
            runs = list_test_runs(job_id, data_dir)
            if runs:
                latest = runs[-1].get("status", "")
                if latest == "passed":
                    ev["tests_status"] = "green"
                elif latest in ("failed", "timeout"):
                    ev["tests_status"] = "failing"
            ev["snapshot_recorded"] = bool(list_snapshot_proofs(job_id=job_id, data_dir=data_dir))
            ev["rollback_restore_available"] = any(
                r.get("restore_available") for r in list_rollback_proofs(job_id=job_id, data_dir=data_dir))
        except Exception:
            pass

    # Repair status (any open/needed repair).
    if job is not None:
        try:
            from packages.orchestration.repair_loop import load_repair_attempts
            attempts = load_repair_attempts(job)
            states = [getattr(a, "status", "") for a in attempts.values()]
            ev["repair_status"] = ("needed" if any(s in ("blocked", "needs_review", "failed")
                                                   for s in states) else
                                   "in_progress" if states else "none")
        except Exception:
            ev["repair_status"] = "unknown"

    # Token-Aware Repair Loop v1/v2 (Step 1929) — required repair work items block satisfaction; an
    # abandoned/blocked repair signals a user decision. Honest (no fake repaired).
    if job_id:
        try:
            from packages.orchestration.repair_loop_v2 import repair_loop_mission_signal
            sig = repair_loop_mission_signal(job_id, data_dir)
            ev["repair_loop_open"] = int(sig.get("open_repair_count", 0))
            ev["repair_loop_blocked"] = int(sig.get("blocked_repair_count", 0))
            ev["repair_loop_user_decision"] = bool(sig.get("user_decision_required", False))
            if sig.get("repair_needed") or sig.get("user_decision_required"):
                ev["repair_status"] = "needed"
            elif ev["repair_status"] in ("unknown", "none") and sig.get("total"):
                ev["repair_status"] = "none"
        except Exception:
            pass
    # Main Builder Adapter v0 (Step 1977) — running/waiting builder sessions do NOT satisfy mission;
    # blocked sessions create user decisions. Honest (no fake done).
    if job_id:
        try:
            from packages.orchestration.main_builder_adapter import builder_adapter_mission_signal
            bsig = builder_adapter_mission_signal(job_id, data_dir)
            ev["builder_adapter_active"] = bool(bsig.get("has_active_sessions", False))
            ev["builder_adapter_blocked"] = int(bsig.get("blocked_session_count", 0))
            ev["builder_adapter_user_decision"] = bool(bsig.get("user_decision_required", False))
            if bsig.get("user_decision_required"):
                ev["repair_status"] = "needed"
        except Exception:
            pass
    return ev


# ---------------------------------------------------------------------------
# Contract evaluation (Step 1843)
# ---------------------------------------------------------------------------


def evaluate_mission_contract(
    contract: MissionContract, data_dir: Path | None = None, persist: bool = False,
) -> MissionEvaluation:
    """Evaluate contract satisfaction from durable evidence. NEVER satisfied from builder self-report.
    Reviewer verdict beats self-report; open Blocker/High blocks; missing required gates block."""
    ddir = _resolve_ddir(data_dir)
    e = MissionEvaluation(contract_id=contract.contract_id, job_id=contract.job_id, created_at=_now())
    rf = _review_findings()
    ev = _gather_mission_evidence(contract.job_id, ddir)

    e.open_review_findings = rf.open_blocker + rf.open_high + rf.open_medium
    e.open_tasks = ev["open_tasks"]
    e.failed_tests = ev["failed_tests"]
    blockers: list[str] = []
    missing_proofs: list[str] = []

    # 1. Acceptance criteria required.
    if not contract.acceptance_criteria:
        e.status = MissionStatus.NEEDS_USER_ACCEPTANCE_CRITERIA
        e.user_decision_required = True
        e.unsatisfied_criteria = ["(none defined — user must supply acceptance criteria)"]
        blockers.append("no acceptance criteria defined")

    # 2. Review gate (reviewer verdict beats self-report; Done != Resolved).
    review_clean = (rf.verdict in ("pass", "pass_with_risks") and rf.open_blocker == 0
                    and rf.open_high == 0)
    if contract.require_clean_review and rf.verdict == "pass_with_risks":
        review_clean = review_clean and rf.open_medium == 0
    if rf.open_blocker + rf.open_high > 0:
        blockers.append(f"open Blocker/High review findings ({rf.open_blocker + rf.open_high})")
    if contract.require_clean_review and rf.verdict in ("pending", "fail", "unknown"):
        blockers.append(f"reviewer verdict is {rf.verdict} (not PASS)")

    # 3. Open tasks.
    if e.open_tasks > 0:
        blockers.append(f"{e.open_tasks} task(s) still open/blocked")

    # 4. Required gates.
    if contract.require_tests_green:
        if ev["tests_status"] != "green":
            missing_proofs.append(f"tests_green (status={ev['tests_status']})")
    if e.failed_tests > 0:
        blockers.append(f"{e.failed_tests} failing test(s)")
    if contract.require_proof_chain and ev["proof_status"] != "verified":
        missing_proofs.append(f"proof_chain (status={ev['proof_status']})")
    # Snapshot / rollback gates (Step 1886) — honest: a recorded metadata snapshot satisfies
    # snapshot_before_apply, but rollback_restore_available requires a real verified restore path.
    if GATE_SNAPSHOT_BEFORE_APPLY in contract.required_gates and not ev["snapshot_recorded"]:
        missing_proofs.append("snapshot_before_apply (no snapshot proof recorded)")
    if GATE_ROLLBACK_RESTORE in contract.required_gates and not ev["rollback_restore_available"]:
        missing_proofs.append("rollback_restore_available (no verified restore path)")
    e.missing_proofs = missing_proofs

    # 5. Repair.
    if ev["repair_status"] == "needed":
        blockers.append("repair needed (open repair attempt)")

    e.blocked_reasons = blockers

    # ---- Decide satisfaction (ALL must hold) ----
    satisfied = bool(
        contract.acceptance_criteria and review_clean and e.open_tasks == 0
        and e.failed_tests == 0 and not missing_proofs and ev["repair_status"] != "needed")
    e.satisfied = satisfied

    if satisfied:
        e.status = MissionStatus.CONTRACT_SATISFIED
        e.unsatisfied_criteria = []
    elif e.status != MissionStatus.NEEDS_USER_ACCEPTANCE_CRITERIA:
        # Pick the most informative non-satisfied status.
        if rf.open_blocker + rf.open_high > 0 or rf.verdict in ("pending", "fail"):
            e.status = MissionStatus.WAITING_FOR_REVIEW
        elif ev["repair_status"] == "needed" or e.failed_tests > 0:
            e.status = MissionStatus.REPAIR_NEEDED
        elif missing_proofs:
            e.status = MissionStatus.BLOCKED
        elif e.open_tasks > 0:
            e.status = MissionStatus.RUNNING_METADATA_ONLY
        else:
            e.status = MissionStatus.BLOCKED
        if contract.acceptance_criteria:
            e.unsatisfied_criteria = list(contract.acceptance_criteria)

    # Next safe actions (required blockers vs optional ideas).
    required, optional, flat = mission_next_safe_actions(contract, e, data_dir=ddir)
    e.required_next_actions = required
    e.optional_next_ideas = optional
    e.next_safe_actions = flat
    if not flat and not satisfied:
        e.status = MissionStatus.BLOCKED
        if "no safe next action available" not in e.blocked_reasons:
            e.blocked_reasons.append("no safe next action available")

    e.phase = mission_state_machine(e)
    e.user_summary = _user_summary(contract, e, rf, ev)
    if persist:
        save_mission_evaluation(e, ddir)
    return e


def _user_summary(contract: MissionContract, e: MissionEvaluation, rf: Any, ev: dict) -> str:
    if e.satisfied:
        return ("Mission contract satisfied: acceptance criteria met, review clean, no open tasks, "
                "required gates passed (evidence-based; nothing executed by Remedy).")
    if e.status == MissionStatus.NEEDS_USER_ACCEPTANCE_CRITERIA:
        return ("Mission needs acceptance criteria from you before Remedy can judge 'done'. "
                "Define what counts as complete.")
    parts = []
    if rf.open_blocker + rf.open_high > 0:
        parts.append(f"{rf.open_blocker + rf.open_high} open Blocker/High review finding(s)")
    if rf.verdict in ("pending", "fail", "unknown"):
        parts.append(f"reviewer verdict {rf.verdict}")
    if e.open_tasks > 0:
        parts.append(f"{e.open_tasks} open task(s)")
    if e.failed_tests > 0:
        parts.append(f"{e.failed_tests} failing test(s)")
    if e.missing_proofs:
        parts.append("missing required gate(s): " + ", ".join(e.missing_proofs))
    blk = "; ".join(parts) if parts else "work remaining"
    return (f"Mission not done — {blk}. Status: {e.status}. See required next actions "
            "(nothing runs automatically).")


# ---------------------------------------------------------------------------
# Next safe action planner (Step 1844) + idea queue (Step 1846)
# ---------------------------------------------------------------------------


def mission_next_safe_actions(
    contract: MissionContract, evaluation: MissionEvaluation, data_dir: Path | None = None,
) -> tuple[list[dict], list[dict], list[str]]:
    """Return (required_blocker_actions, optional_future_ideas, flat_command_list). All commands are
    catalog-valid. Required actions are what's needed to satisfy THIS contract; optional ideas are
    future product work and are clearly separated. User-approval-required actions are flagged."""
    jid = contract.job_id or "<job_id>"
    cid = contract.contract_id or "<contract_id>"
    required: list[dict] = []

    def _req(title: str, command: str, *, user_decision: bool = False) -> None:
        required.append({"title": title, "command": command, "required": True,
                         "user_decision_required": user_decision})

    if evaluation.status == MissionStatus.NEEDS_USER_ACCEPTANCE_CRITERIA:
        _req("Define acceptance criteria for this mission",
             f"remedy overnight contract-show {cid} --json", user_decision=True)
    if evaluation.open_review_findings > 0 or evaluation.status == MissionStatus.WAITING_FOR_REVIEW:
        _req("Review findings / await reviewer PASS", "remedy review list --json")
    if evaluation.failed_tests > 0:
        _req("Start repair for failing test(s)", f"remedy repair status {jid} --json")
    if any("repair needed" in r for r in evaluation.blocked_reasons):
        _req("Continue the open repair", f"remedy repair status {jid} --json")
    if evaluation.missing_proofs:
        _req("Provide the missing required gate (tests/proof)",
             f"remedy progress checklist --json")
    if evaluation.open_tasks > 0 and not required:
        _req("Work the remaining open task(s)", "remedy progress checklist --json")

    # Always-safe inspection actions (not blockers themselves).
    inspection = [
        {"title": "Re-evaluate the mission contract", "command":
         f"remedy overnight evaluate {cid} --json", "required": False, "user_decision_required": False},
        {"title": "Show the progress checklist", "command": "remedy progress checklist --json",
         "required": False, "user_decision_required": False},
    ]

    # Optional future ideas (NOT needed for the current contract) — from the feature plan.
    optional: list[dict] = []
    if evaluation.satisfied:
        optional = _optional_feature_ideas(contract.job_id, data_dir)

    flat: list[str] = []
    for a in required + inspection:
        if a["command"] not in flat:
            flat.append(a["command"])
    return required, optional, flat


def _optional_feature_ideas(job_id: str, data_dir: Path | None) -> list[dict]:
    """Optional future product ideas from the Feature Planner — only surfaced once the current
    contract is satisfied, so blockers and future ideas never mix."""
    try:
        from uuid import UUID
        from packages.orchestration.storage import load_job
        from packages.orchestration.timeline import load_run_events
        from packages.orchestration.progress_ledger import build_progress_ledger
        from packages.orchestration.feature_planner import build_feature_plan
        ddir = _resolve_ddir(data_dir)
        job = load_job(UUID(job_id), ddir)
        events = load_run_events(ddir, job.id)
        ledger = build_progress_ledger(job=job, events=events)
        plan = build_feature_plan(ledger, job)
        out = []
        for s in plan.suggestions[:8]:
            out.append({"title": s.title[:120], "impact": getattr(s, "priority", "medium"),
                        "effort": getattr(s, "estimated_risk", "low"), "required": False,
                        "next_action": getattr(s, "next_action", "")})
        return out
    except Exception:
        return []


# ---------------------------------------------------------------------------
# State machine (Step 1845)
# ---------------------------------------------------------------------------


def mission_state_machine(evaluation: MissionEvaluation) -> str:
    """Derive the current spine phase from the evaluation. Metadata-only — determines what should
    happen next; never executes anything."""
    s = evaluation.status
    if s == MissionStatus.CONTRACT_SATISFIED:
        return MissionPhase.SATISFIED
    if s == MissionStatus.NEEDS_USER_ACCEPTANCE_CRITERIA or evaluation.user_decision_required:
        return MissionPhase.USER_DECISION
    if s == MissionStatus.WAITING_FOR_REVIEW:
        return MissionPhase.REVIEW
    if s == MissionStatus.REPAIR_NEEDED:
        return MissionPhase.REPAIR
    if evaluation.missing_proofs:
        # Distinguish test gate vs proof gate.
        if any("tests_green" in m for m in evaluation.missing_proofs):
            return MissionPhase.TEST_GATE
        return MissionPhase.PROOF_GATE
    if s == MissionStatus.BLOCKED:
        return MissionPhase.BLOCKED
    if evaluation.open_tasks > 0:
        return MissionPhase.PLAN
    return MissionPhase.PLAN


# ---------------------------------------------------------------------------
# Readiness (Step 1850 — overnight contract-readiness)
# ---------------------------------------------------------------------------


def mission_readiness(job_id: str, data_dir: Path | None = None) -> dict[str, Any]:
    """Honest overnight readiness for a job. Never claims overnight autonomy exists — reports which
    gates/adapters are available vs missing."""
    ddir = _resolve_ddir(data_dir)
    contracts = list_mission_contracts(job_id=job_id, data_dir=ddir)
    ev = _gather_mission_evidence(job_id, ddir)
    rf = _review_findings()
    return {
        "version": 1, "job_id": job_id,
        "has_mission_contract": bool(contracts),
        "review_verdict": rf.verdict,
        "open_blocker_or_high": rf.open_blocker + rf.open_high,
        "tests_status": ev["tests_status"],
        "proof_status": ev["proof_status"],
        "open_tasks": ev["open_tasks"],
        "worker_execution_available": False,      # no provider/Ollama/Claude/Pi adapter yet
        "real_test_execution_available": False,   # next block
        "full_overnight_autonomy": False,         # honest: NOT built
        "next_safe_action": (f"remedy overnight contract-create {job_id} --json" if not contracts
                             else f"remedy overnight evaluate {contracts[-1].get('contract_id')} --json"),
        "note": "Overnight Mission Contract spine is metadata/evaluation only; no worker/test/provider "
                "execution exists yet.",
    }


# ---------------------------------------------------------------------------
# Integrity (Step 1852)
# ---------------------------------------------------------------------------


def audit_evaluation_safety(evaluation: dict[str, Any]) -> list[dict[str, str]]:
    """Flag unsafe mission-evaluation states. Safe public codes only."""
    if not isinstance(evaluation, dict):
        return []
    out: list[dict[str, str]] = []
    cid = evaluation.get("contract_id", "")
    satisfied = bool(evaluation.get("satisfied"))
    if satisfied and evaluation.get("open_review_findings", 0) > 0:
        out.append({"contract_id": cid, "code": "satisfied_with_open_findings"})
    if satisfied and evaluation.get("missing_proofs"):
        out.append({"contract_id": cid, "code": "satisfied_with_missing_gates"})
    if satisfied and evaluation.get("open_tasks", 0) > 0:
        out.append({"contract_id": cid, "code": "satisfied_with_open_tasks"})
    if satisfied and evaluation.get("failed_tests", 0) > 0:
        out.append({"contract_id": cid, "code": "satisfied_with_failing_tests"})
    blob = json.dumps(evaluation).lower()
    if any(m.lower() in blob for m in _RAW_MARKERS):
        out.append({"contract_id": cid, "code": "raw_or_secret_in_public"})
    if "/home/" in blob or "/users/" in blob or "/root/" in blob:
        out.append({"contract_id": cid, "code": "absolute_path_in_public"})
    return out


def mission_integrity(data_dir: Path | None = None,
                      evaluations: list[dict] | None = None) -> dict[str, Any]:
    """Read-only invariant check over persisted (or supplied) mission evaluations + contracts."""
    ddir = _resolve_ddir(data_dir)
    violations: list[dict] = []
    contracts = list_mission_contracts(data_dir=ddir)
    scan = evaluations
    if scan is None:
        scan = []
        for c in contracts:
            le = load_latest_mission_evaluation(c.get("contract_id", ""), ddir)
            if le:
                scan.append(le)
    for ev in scan:
        violations.extend(audit_evaluation_safety(ev))
    for c in contracts:
        blob = json.dumps(c).lower()
        if "/home/" in blob or "/users/" in blob:
            violations.append({"contract_id": c.get("contract_id", ""),
                               "code": "absolute_path_in_contract"})
    return {"version": 1, "contract_count": len(contracts), "evaluation_count": len(scan),
            "violation_count": len(violations), "passed": not violations, "violations": violations[:50]}


# Keep redaction helpers referenced for parity with the rest of the orchestration package.
_REDACTION_HELPERS = (_scrub_public, _safe_path_label)
