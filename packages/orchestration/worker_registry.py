"""
Worker Registry + User-Selectable Route Policy v0 (Steps 1717-1756).

The modular Baukasten layer. Remedy must not become a single hardcoded coding agent — workers,
models, providers, routes, token profiles, risk profiles, and output contracts must remain
swappable and user-selectable. This module models workers as REPLACEABLE specs and lets the user
constrain/select routes via a per-job RoutePolicy.

  Workers execute. Remedy governs. Users choose or constrain workers/routes.

This module is METADATA + POLICY + selection EVALUATION only. It NEVER executes a worker, calls a
provider/model/Ollama/cloud service, touches the network, runs a subprocess, applies/approves a
patch, or starts any work. It reads safe durable summaries and returns recommendations +
catalog-backed next_safe_actions.

Hard rules enforced here:
  - NO provider/model/Ollama/cloud calls, NO network, NO browser, NO subprocess, NO shell.
  - NO apply/approve/reject/test-run/git/PR; NO automatic generation/repair; NO worker execution.
  - Disabled/blocked workers can never be selected or recommended.
  - Unknown cost is NEVER treated as cheap; expensive/cloud/unknown routes require human-facing
    justification.
  - local/Ollama preference is metadata-only and cannot override safety or a missing capability.
  - Ollama/cloud workers are PLACEHOLDERS — clearly non-executable; selecting them yields a
    "configure first" recommendation, never an execution.
  - Token/cost figures are ESTIMATED bands only — no invented exact pricing, no pricing calls.
  - No secrets / API keys / raw prompts / raw model output / absolute private paths in any export.

Public API::

    list_worker_specs(registry=None) -> list[WorkerSpec]
    get_worker_spec(worker_id, registry=None) -> WorkerSpec | None
    load_worker_registry(data_dir=None) -> list[WorkerSpec]
    default_route_policy(job_id="") -> RoutePolicy
    load_route_policy(job_id, data_dir=None) -> RoutePolicy
    save_route_policy(policy, data_dir=None) -> bool
    evaluate_worker_selection(request, policy=None, registry=None, data_dir=None)
        -> WorkerSelectionResult
    estimate_context_fit(spec, estimated_context_tokens) -> dict
    estimate_token_cost_band(spec) -> str
    classify_route_cost(spec) -> str
    token_reduction_reason(spec) -> str
    worker_registry_integrity(data_dir=None) -> dict
    export_worker_spec_json(spec) / export_route_policy_json(policy) -> dict
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.provider_trust import _safe_path_label, _scrub_public


# ---------------------------------------------------------------------------
# Constants / vocabularies
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "worker-registry-v0"
_RP_DIRNAME = "route_policy"

# Markers used to detect accidental raw/secret leakage in public exports.
_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-",
                "api_key", "apikey", "password", "secret_key")


class WorkerKind:
    FIXTURE = "fixture"
    LOCAL_CANDIDATE = "local_candidate"
    EXTERNAL_BUILDER = "external_builder"
    OLLAMA_CANDIDATE = "ollama_candidate"
    CLOUD_CANDIDATE = "cloud_candidate"
    HUMAN = "human"
    REVIEWER = "reviewer"
    UNKNOWN = "unknown"


ALL_WORKER_KINDS: frozenset[str] = frozenset({
    v for k, v in vars(WorkerKind).items() if not k.startswith("_") and isinstance(v, str)
})


class WorkerCostTier:
    FREE = "free"
    CHEAP = "cheap"
    STANDARD = "standard"
    EXPENSIVE = "expensive"
    UNKNOWN = "unknown"


class WorkerRiskTier:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class WorkerExecutionMode:
    METADATA_ONLY = "metadata_only"
    EXTERNAL_INGRESS = "external_ingress"
    LOCAL_MODEL = "local_model"
    CLOUD_MODEL = "cloud_model"
    HUMAN_IN_LOOP = "human_in_loop"
    REVIEW_ONLY = "review_only"


# Ordered low→high. "unknown" is deliberately ABSENT — it sorts as worse-than-max so it can never
# be treated as cheap/low (R-class safety rule).
_COST_ORDER: tuple[str, ...] = (
    WorkerCostTier.FREE, WorkerCostTier.CHEAP, WorkerCostTier.STANDARD, WorkerCostTier.EXPENSIVE,
)
_RISK_ORDER: tuple[str, ...] = (
    WorkerRiskTier.LOW, WorkerRiskTier.MEDIUM, WorkerRiskTier.HIGH, WorkerRiskTier.BLOCKED,
)

# Cost tiers that count as "cheap task" eligible for local/Ollama-first preference.
_CHEAP_TIERS: frozenset[str] = frozenset({WorkerCostTier.FREE, WorkerCostTier.CHEAP})
# Cost tiers that require human-facing justification when routed.
_EXPENSIVE_TIERS: frozenset[str] = frozenset({WorkerCostTier.EXPENSIVE})
# Execution modes that are placeholders / not executable in this block.
_PLACEHOLDER_MODES: frozenset[str] = frozenset({WorkerExecutionMode.CLOUD_MODEL})


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _cost_rank(tier: str) -> int:
    """Rank a cost tier. Unknown ranks ABOVE the most expensive concrete tier (never cheap)."""
    return _COST_ORDER.index(tier) if tier in _COST_ORDER else len(_COST_ORDER)


def _risk_rank(tier: str) -> int:
    """Rank a risk tier. Unknown ranks ABOVE the highest concrete tier (never low)."""
    return _RISK_ORDER.index(tier) if tier in _RISK_ORDER else len(_RISK_ORDER)


# ---------------------------------------------------------------------------
# WorkerSpec (Step 1719)
# ---------------------------------------------------------------------------


@dataclass
class WorkerSpec:
    """A replaceable, provider-neutral worker specification. Metadata only — no secrets, no keys,
    no endpoints, no raw prompts, no execution."""

    worker_id: str
    label: str = ""
    kind: str = WorkerKind.UNKNOWN
    enabled: bool = False
    user_selectable: bool = False
    capabilities: list[str] = field(default_factory=list)
    allowed_task_types: list[str] = field(default_factory=list)
    forbidden_task_types: list[str] = field(default_factory=list)
    cost_tier: str = WorkerCostTier.UNKNOWN
    risk_tier: str = WorkerRiskTier.UNKNOWN
    execution_mode: str = WorkerExecutionMode.METADATA_ONLY
    token_profile: dict[str, Any] = field(default_factory=dict)
    context_profile: dict[str, Any] = field(default_factory=dict)
    output_contract: str = ""
    required_permissions: list[str] = field(default_factory=list)
    supports_external_builder_package: bool = False
    supports_candidate_quality: bool = False
    supports_review_loop: bool = False
    default_autonomy_ceiling: int = 1
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "worker_id": self.worker_id,
            "label": self.label,
            "kind": self.kind,
            "enabled": self.enabled,
            "user_selectable": self.user_selectable,
            "capabilities": list(self.capabilities),
            "allowed_task_types": list(self.allowed_task_types),
            "forbidden_task_types": list(self.forbidden_task_types),
            "cost_tier": self.cost_tier,
            "risk_tier": self.risk_tier,
            "execution_mode": self.execution_mode,
            "token_profile": dict(self.token_profile),
            "context_profile": dict(self.context_profile),
            "output_contract": self.output_contract,
            "required_permissions": list(self.required_permissions),
            "supports_external_builder_package": self.supports_external_builder_package,
            "supports_candidate_quality": self.supports_candidate_quality,
            "supports_review_loop": self.supports_review_loop,
            "default_autonomy_ceiling": self.default_autonomy_ceiling,
            "notes": self.notes,
            # Never-executable placeholder flag — derived, surfaced so no caller can mistake a
            # placeholder for a runnable worker.
            "is_placeholder": is_placeholder(self),
            "schema_version": SCHEMA_VERSION,
        }


def export_worker_spec_json(spec: WorkerSpec) -> dict[str, Any]:
    return spec.to_dict()


def is_placeholder(spec: WorkerSpec) -> bool:
    """A worker is a placeholder (NOT executable in this block) when it is disabled OR uses a
    placeholder execution mode (cloud) OR its notes mark it placeholder. Placeholders exist so
    future routing can prefer them once real execution is built — they never claim readiness."""
    if not spec.enabled:
        return True
    if spec.execution_mode in _PLACEHOLDER_MODES:
        return True
    if spec.kind in (WorkerKind.OLLAMA_CANDIDATE, WorkerKind.CLOUD_CANDIDATE):
        return True
    return "placeholder" in (spec.notes or "").lower()


# ---------------------------------------------------------------------------
# Built-in registry (Step 1720) — deterministic, no provider/network imports.
# ---------------------------------------------------------------------------


def _builtin_specs() -> list[WorkerSpec]:
    return [
        WorkerSpec(
            worker_id="fixture.worker",
            label="Deterministic Fixture Worker",
            kind=WorkerKind.FIXTURE,
            enabled=True,
            user_selectable=True,
            capabilities=["deterministic_fixture", "metadata"],
            allowed_task_types=["test", "fixture", "smoke"],
            cost_tier=WorkerCostTier.FREE,
            risk_tier=WorkerRiskTier.LOW,
            execution_mode=WorkerExecutionMode.METADATA_ONLY,
            token_profile={"band": "none", "estimated": True},
            context_profile={"band": "tiny", "max_context_tokens_estimate": 2000, "estimated": True},
            output_contract="Deterministic fixture output; never trusted as real work.",
            default_autonomy_ceiling=2,
            notes="Built-in deterministic fixture for tests/smoke. No model, no network.",
        ),
        WorkerSpec(
            worker_id="local.candidate_generator",
            label="Local Candidate Generator (loopback)",
            kind=WorkerKind.LOCAL_CANDIDATE,
            enabled=True,
            user_selectable=True,
            capabilities=["candidate_generation", "loopback_local_model"],
            allowed_task_types=["repair", "candidate", "fix"],
            cost_tier=WorkerCostTier.CHEAP,
            risk_tier=WorkerRiskTier.MEDIUM,
            execution_mode=WorkerExecutionMode.LOCAL_MODEL,
            token_profile={"band": "small", "estimated": True},
            context_profile={"band": "small", "max_context_tokens_estimate": 8000, "estimated": True},
            output_contract="One candidate; UNTRUSTED; goes through Trust Gate + Verification.",
            supports_candidate_quality=True,
            default_autonomy_ceiling=1,
            notes="Maps to the existing routing-gated local candidate generator (disabled by "
                  "default in its own config; output still quarantined + verified).",
        ),
        WorkerSpec(
            worker_id="external.builder_package",
            label="External Builder (request-package ingress)",
            kind=WorkerKind.EXTERNAL_BUILDER,
            enabled=True,
            user_selectable=True,
            capabilities=["external_request_package", "untrusted_ingress"],
            allowed_task_types=["repair", "candidate", "fix", "feature"],
            cost_tier=WorkerCostTier.STANDARD,
            risk_tier=WorkerRiskTier.HIGH,
            execution_mode=WorkerExecutionMode.EXTERNAL_INGRESS,
            token_profile={"band": "unknown", "estimated": True},
            context_profile={"band": "medium", "max_context_tokens_estimate": 32000, "estimated": True},
            output_contract="External worker returns ONE candidate file; UNTRUSTED; quarantined "
                            "+ trust-checked + verified + human-approved before any apply.",
            supports_external_builder_package=True,
            supports_candidate_quality=True,
            default_autonomy_ceiling=1,
            notes="Maps to the External Builder Sandbox v0 package rail (no execution; ingress only).",
        ),
        WorkerSpec(
            worker_id="human.operator",
            label="Human Operator",
            kind=WorkerKind.HUMAN,
            enabled=True,
            user_selectable=True,
            capabilities=["decision", "approval", "manual_edit"],
            allowed_task_types=["repair", "candidate", "fix", "feature", "review", "decision"],
            cost_tier=WorkerCostTier.FREE,
            risk_tier=WorkerRiskTier.LOW,
            execution_mode=WorkerExecutionMode.HUMAN_IN_LOOP,
            token_profile={"band": "none", "estimated": True},
            context_profile={"band": "any", "estimated": True},
            output_contract="Human-authored change or decision; still tracked + approval-gated.",
            supports_review_loop=True,
            default_autonomy_ceiling=6,
            notes="The human in the loop — always available; the safe fallback route.",
        ),
        WorkerSpec(
            worker_id="reviewer.parallel",
            label="Parallel Reviewer",
            kind=WorkerKind.REVIEWER,
            enabled=True,
            user_selectable=True,
            capabilities=["review", "finding", "verdict"],
            allowed_task_types=["review"],
            cost_tier=WorkerCostTier.FREE,
            risk_tier=WorkerRiskTier.LOW,
            execution_mode=WorkerExecutionMode.REVIEW_ONLY,
            token_profile={"band": "none", "estimated": True},
            context_profile={"band": "medium", "estimated": True},
            output_contract="Findings + verdict only; never applies/generates.",
            supports_review_loop=True,
            default_autonomy_ceiling=2,
            notes="Independent reviewer rail (owns verdict). Read/review only.",
        ),
        WorkerSpec(
            worker_id="ollama.placeholder",
            label="Ollama Worker (placeholder — not executable)",
            kind=WorkerKind.OLLAMA_CANDIDATE,
            enabled=False,
            user_selectable=False,
            capabilities=["candidate_generation", "local_model"],
            allowed_task_types=["repair", "candidate", "fix"],
            cost_tier=WorkerCostTier.CHEAP,
            risk_tier=WorkerRiskTier.MEDIUM,
            execution_mode=WorkerExecutionMode.LOCAL_MODEL,
            token_profile={"band": "small", "estimated": True},
            context_profile={"band": "small", "max_context_tokens_estimate": 8000, "estimated": True},
            output_contract="(future) One candidate; UNTRUSTED; quarantined + verified.",
            supports_candidate_quality=True,
            default_autonomy_ceiling=1,
            notes="METADATA-ONLY placeholder. NOT executable in this block — no Ollama call is "
                  "made. Exists so future routing can prefer local/Ollama-capable routes for cheap "
                  "tasks once execution is built. Disabled until a real adapter + config land.",
        ),
        WorkerSpec(
            worker_id="cloud.placeholder",
            label="Cloud Model Worker (placeholder — not executable)",
            kind=WorkerKind.CLOUD_CANDIDATE,
            enabled=False,
            user_selectable=False,
            capabilities=["candidate_generation", "cloud_model"],
            allowed_task_types=["repair", "candidate", "fix", "feature"],
            cost_tier=WorkerCostTier.EXPENSIVE,
            risk_tier=WorkerRiskTier.HIGH,
            execution_mode=WorkerExecutionMode.CLOUD_MODEL,
            token_profile={"band": "unknown", "estimated": True},
            context_profile={"band": "large", "max_context_tokens_estimate": 128000, "estimated": True},
            output_contract="(future) One candidate; UNTRUSTED; quarantined + verified + approved.",
            required_permissions=["cloud_provider"],
            supports_candidate_quality=True,
            default_autonomy_ceiling=1,
            notes="METADATA-ONLY placeholder. NOT executable in this block — no cloud/provider call "
                  "is made. Expensive route: always requires human-facing justification. Disabled.",
        ),
    ]


# ---------------------------------------------------------------------------
# Registry load (Step 1722) — built-ins + corruption-aware optional persisted specs.
# ---------------------------------------------------------------------------


def load_worker_registry(data_dir: Path | None = None) -> list[WorkerSpec]:
    """Return the worker registry. Built-ins are canonical; optional persisted custom specs (if a
    future block adds them) are merged corruption-aware. Never raises; unknown fields ignored."""
    specs = {s.worker_id: s for s in _builtin_specs()}
    # Optional persisted custom specs (none written in v0; load is corruption-aware + bounded).
    try:
        from packages.orchestration.data_paths import resolve_data_root
        ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
        root = ddir / "workspaces" / "orchestrator" / "worker_registry"
        if root.is_dir():
            for child in sorted(root.iterdir()):
                f = child / "worker.json"
                if not f.is_file():
                    continue
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    spec = _spec_from_dict(d)
                    if spec is not None and spec.worker_id and spec.worker_id not in specs:
                        specs[spec.worker_id] = spec
                except (OSError, ValueError, TypeError):
                    continue
    except (ImportError, OSError, ValueError):
        pass
    return list(specs.values())


def list_worker_specs(registry: list[WorkerSpec] | None = None) -> list[WorkerSpec]:
    return list(registry) if registry is not None else load_worker_registry()


def get_worker_spec(worker_id: str, registry: list[WorkerSpec] | None = None) -> WorkerSpec | None:
    return next((s for s in list_worker_specs(registry) if s.worker_id == worker_id), None)


def _spec_from_dict(d: dict[str, Any]) -> WorkerSpec | None:
    if not isinstance(d, dict) or not d.get("worker_id"):
        return None
    kind = str(d.get("kind", WorkerKind.UNKNOWN))
    if kind not in ALL_WORKER_KINDS:
        kind = WorkerKind.UNKNOWN          # unknown stays unknown, never faked
    return WorkerSpec(
        worker_id=str(d.get("worker_id", "")),
        label=str(d.get("label", "")),
        kind=kind,
        enabled=bool(d.get("enabled", False)),
        user_selectable=bool(d.get("user_selectable", False)),
        capabilities=list(d.get("capabilities", [])),
        allowed_task_types=list(d.get("allowed_task_types", [])),
        forbidden_task_types=list(d.get("forbidden_task_types", [])),
        cost_tier=str(d.get("cost_tier", WorkerCostTier.UNKNOWN)),
        risk_tier=str(d.get("risk_tier", WorkerRiskTier.UNKNOWN)),
        execution_mode=str(d.get("execution_mode", WorkerExecutionMode.METADATA_ONLY)),
        token_profile=dict(d.get("token_profile", {})),
        context_profile=dict(d.get("context_profile", {})),
        output_contract=str(d.get("output_contract", "")),
        required_permissions=list(d.get("required_permissions", [])),
        supports_external_builder_package=bool(d.get("supports_external_builder_package", False)),
        supports_candidate_quality=bool(d.get("supports_candidate_quality", False)),
        supports_review_loop=bool(d.get("supports_review_loop", False)),
        default_autonomy_ceiling=int(d.get("default_autonomy_ceiling", 1)),
        notes=str(d.get("notes", "")),
    )


# ---------------------------------------------------------------------------
# RoutePolicy (Step 1721)
# ---------------------------------------------------------------------------


@dataclass
class RoutePolicy:
    policy_id: str = ""
    job_id: str = ""
    user_selected_worker_ids: list[str] = field(default_factory=list)
    preferred_worker_ids: list[str] = field(default_factory=list)
    blocked_worker_ids: list[str] = field(default_factory=list)
    allowed_worker_kinds: list[str] = field(default_factory=list)
    blocked_worker_kinds: list[str] = field(default_factory=list)
    max_cost_tier: str = WorkerCostTier.EXPENSIVE
    max_risk_tier: str = WorkerRiskTier.HIGH
    prefer_local_for_cheap_tasks: bool = True
    prefer_ollama_for_cheap_tasks: bool = False
    require_human_approval_for_expensive: bool = True
    require_human_approval_for_high_risk: bool = True
    token_budget_hint: Any = "unknown"
    context_budget_hint: Any = "unknown"
    autonomy_level: int = 1
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "job_id": self.job_id,
            "user_selected_worker_ids": list(self.user_selected_worker_ids),
            "preferred_worker_ids": list(self.preferred_worker_ids),
            "blocked_worker_ids": list(self.blocked_worker_ids),
            "allowed_worker_kinds": list(self.allowed_worker_kinds),
            "blocked_worker_kinds": list(self.blocked_worker_kinds),
            "max_cost_tier": self.max_cost_tier,
            "max_risk_tier": self.max_risk_tier,
            "prefer_local_for_cheap_tasks": self.prefer_local_for_cheap_tasks,
            "prefer_ollama_for_cheap_tasks": self.prefer_ollama_for_cheap_tasks,
            "require_human_approval_for_expensive": self.require_human_approval_for_expensive,
            "require_human_approval_for_high_risk": self.require_human_approval_for_high_risk,
            "token_budget_hint": self.token_budget_hint,
            "context_budget_hint": self.context_budget_hint,
            "autonomy_level": self.autonomy_level,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "schema_version": SCHEMA_VERSION,
        }


def export_route_policy_json(policy: RoutePolicy) -> dict[str, Any]:
    return policy.to_dict()


def default_route_policy(job_id: str = "") -> RoutePolicy:
    """Safe defaults: local-first for cheap tasks; expensive + high-risk require human approval;
    Ollama preference off (placeholder not executable); broad cost/risk ceilings."""
    now = _now()
    return RoutePolicy(policy_id=f"rp-{uuid4().hex[:8]}", job_id=job_id,
                       created_at=now, updated_at=now)


def _policy_from_dict(d: dict[str, Any]) -> RoutePolicy:
    return RoutePolicy(
        policy_id=str(d.get("policy_id", "")),
        job_id=str(d.get("job_id", "")),
        user_selected_worker_ids=list(d.get("user_selected_worker_ids", [])),
        preferred_worker_ids=list(d.get("preferred_worker_ids", [])),
        blocked_worker_ids=list(d.get("blocked_worker_ids", [])),
        allowed_worker_kinds=list(d.get("allowed_worker_kinds", [])),
        blocked_worker_kinds=list(d.get("blocked_worker_kinds", [])),
        max_cost_tier=str(d.get("max_cost_tier", WorkerCostTier.EXPENSIVE)),
        max_risk_tier=str(d.get("max_risk_tier", WorkerRiskTier.HIGH)),
        prefer_local_for_cheap_tasks=bool(d.get("prefer_local_for_cheap_tasks", True)),
        prefer_ollama_for_cheap_tasks=bool(d.get("prefer_ollama_for_cheap_tasks", False)),
        require_human_approval_for_expensive=bool(d.get("require_human_approval_for_expensive", True)),
        require_human_approval_for_high_risk=bool(d.get("require_human_approval_for_high_risk", True)),
        token_budget_hint=d.get("token_budget_hint", "unknown"),
        context_budget_hint=d.get("context_budget_hint", "unknown"),
        autonomy_level=int(d.get("autonomy_level", 1)),
        created_at=str(d.get("created_at", "")),
        updated_at=str(d.get("updated_at", "")),
    )


# ---------------------------------------------------------------------------
# RoutePolicy storage (Step 1722) — safe atomic writes, corruption-aware load.
# ---------------------------------------------------------------------------


def _rp_path(job_id: str, data_dir: Path) -> Path:
    base = job_id if job_id else "orchestrator"
    return data_dir / "workspaces" / base / _RP_DIRNAME / "policy.json"


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


def load_route_policy(job_id: str, data_dir: Path | None = None) -> RoutePolicy:
    """Load the persisted RoutePolicy for a job, or a safe default if absent/corrupt. Never raises."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    f = _rp_path(job_id, ddir)
    try:
        if f.is_file():
            d = json.loads(f.read_text(encoding="utf-8"))
            if isinstance(d, dict) and d.get("policy_id"):
                return _policy_from_dict(d)
    except (OSError, ValueError, TypeError):
        pass
    return default_route_policy(job_id)


def save_route_policy(policy: RoutePolicy, data_dir: Path | None = None) -> bool:
    """Persist a RoutePolicy safely (atomic, 0o600). Returns success."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    if not policy.policy_id:
        policy.policy_id = f"rp-{uuid4().hex[:8]}"
    if not policy.created_at:
        policy.created_at = _now()
    policy.updated_at = _now()
    return _atomic_write(_rp_path(policy.job_id, ddir),
                         json.dumps(policy.to_dict(), indent=2).encode("utf-8"))


# ---------------------------------------------------------------------------
# Token economy (Step 1724) — ESTIMATED bands only; never invented exact cost.
# ---------------------------------------------------------------------------


def classify_route_cost(spec: WorkerSpec) -> str:
    """Return the worker's cost tier (free/cheap/standard/expensive/unknown). Unknown stays unknown."""
    return spec.cost_tier if spec.cost_tier in (*_COST_ORDER, WorkerCostTier.UNKNOWN) \
        else WorkerCostTier.UNKNOWN


def estimate_token_cost_band(spec: WorkerSpec) -> str:
    """Coarse ESTIMATED token band from the worker's profile. Returns 'unknown' if not configured —
    unknown is never downgraded to cheap."""
    band = str((spec.token_profile or {}).get("band", "unknown"))
    if band in ("none", "tiny", "small"):
        return "low"
    if band in ("medium",):
        return "medium"
    if band in ("large",):
        return "high"
    return "unknown"


def estimate_context_fit(spec: WorkerSpec, estimated_context_tokens: int) -> dict[str, Any]:
    """ESTIMATE whether a context of ~N tokens fits the worker's context profile. Returns a band +
    a flag; unknown profile yields 'unknown' (never a fabricated fit)."""
    cap = (spec.context_profile or {}).get("max_context_tokens_estimate")
    if not isinstance(cap, int) or cap <= 0 or estimated_context_tokens < 0:
        return {"fits": "unknown", "headroom": "unknown", "estimated": True,
                "reason": "no configured context estimate"}
    fits = estimated_context_tokens <= cap
    return {"fits": fits, "headroom": max(0, cap - estimated_context_tokens),
            "max_context_tokens_estimate": cap, "estimated": True,
            "reason": "estimated context fit; not a verified measurement"}


def token_reduction_reason(spec: WorkerSpec) -> str:
    """Human-facing reason a route helps (or not) with token reduction. Estimate-only language."""
    if spec.cost_tier in _CHEAP_TIERS:
        return ("estimated cheap/local route — prefer for cheap tasks to reduce token spend "
                "(estimate, not a billed measurement)")
    if spec.cost_tier in _EXPENSIVE_TIERS:
        return "estimated expensive route — use only with evidence-based justification"
    if spec.cost_tier == WorkerCostTier.UNKNOWN:
        return "estimated cost unknown — treated as not-cheap until configured"
    return "estimated standard route"


# ---------------------------------------------------------------------------
# Worker selection evaluation (Step 1722) — read-only; NEVER executes.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkerSelectionRequest:
    job_id: str = ""
    task_type: str = ""
    estimated_context_tokens: int = -1
    user_requested_worker_id: str = ""


@dataclass
class WorkerCandidate:
    worker_id: str
    eligible: bool
    reason: str = ""
    cost_tier: str = WorkerCostTier.UNKNOWN
    risk_tier: str = WorkerRiskTier.UNKNOWN
    is_placeholder: bool = False
    requires_human_justification: bool = False
    score: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "worker_id": self.worker_id, "eligible": self.eligible, "reason": self.reason,
            "cost_tier": self.cost_tier, "risk_tier": self.risk_tier,
            "is_placeholder": self.is_placeholder,
            "requires_human_justification": self.requires_human_justification, "score": self.score,
        }


@dataclass
class WorkerSelectionResult:
    job_id: str = ""
    task_type: str = ""
    policy_id: str = ""
    recommended_worker_id: str = ""
    recommended_reason: str = ""
    requires_human_approval: bool = False
    eligible_candidates: list[WorkerCandidate] = field(default_factory=list)
    rejected_candidates: list[WorkerCandidate] = field(default_factory=list)
    local_first_applied: bool = False
    ollama_preference_applied: bool = False
    token_budget_warning: str = ""
    next_safe_action: str = ""
    safe_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": 1,
            "job_id": self.job_id,
            "task_type": self.task_type,
            "policy_id": self.policy_id,
            "recommended_worker_id": self.recommended_worker_id,
            "recommended_reason": self.recommended_reason,
            "requires_human_approval": self.requires_human_approval,
            "eligible_candidates": [c.to_dict() for c in self.eligible_candidates],
            "rejected_candidates": [c.to_dict() for c in self.rejected_candidates],
            "local_first_applied": self.local_first_applied,
            "ollama_preference_applied": self.ollama_preference_applied,
            "token_budget_warning": self.token_budget_warning,
            "next_safe_action": self.next_safe_action,
            "safe_summary": self.safe_summary,
        }


def _task_type_allowed(spec: WorkerSpec, task_type: str) -> bool:
    if task_type and spec.forbidden_task_types and task_type in spec.forbidden_task_types:
        return False
    if task_type and spec.allowed_task_types and task_type not in spec.allowed_task_types:
        return False
    return True


def _worker_next_action(spec: WorkerSpec | None, job_id: str) -> str:
    """Catalog-backed next action for a selected worker. Placeholders → 'configure first' via the
    feature planner; never an execution command."""
    jid = job_id or "<job_id>"
    if spec is None:
        return "remedy worker registry-list --json"
    if is_placeholder(spec):
        # Not executable — point at the safe planner/registry, never at execution.
        return "remedy feature plan --agent --json"
    if spec.kind == WorkerKind.EXTERNAL_BUILDER:
        return f"remedy external-builder package-create {jid} --json"
    if spec.kind in (WorkerKind.LOCAL_CANDIDATE,):
        return f"remedy builder-routing report --job-id {jid} --json"
    if spec.kind == WorkerKind.REVIEWER:
        return "remedy review list --json"
    if spec.kind == WorkerKind.HUMAN:
        return f"remedy guide next {jid} --json" if job_id else "remedy guide next --json"
    return "remedy worker registry-list --json"


def evaluate_worker_selection(
    request: WorkerSelectionRequest,
    policy: RoutePolicy | None = None,
    registry: list[WorkerSpec] | None = None,
    data_dir: Path | None = None,
) -> WorkerSelectionResult:
    """Evaluate which worker the route policy recommends for a task. READ-ONLY: never executes a
    worker, never starts work, never calls a provider/model. User selection beats default
    preference unless a safety rule (disabled/blocked/cost/risk) blocks it.

    Selection rules (in order):
      1. Disabled and policy-blocked (by id or kind) workers are always rejected.
      2. task_type allow/forbid filters apply.
      3. cost tier > policy.max_cost_tier or risk tier > policy.max_risk_tier reject (unknown is
         worse-than-max → rejected unless the ceiling is itself unknown).
      4. User-selected/explicitly-requested worker wins among the eligible set.
      5. Else, for cheap tasks, local/Ollama preference (only if the preferred worker is eligible
         and enabled — placeholders are never auto-selected as ready).
      6. Else preferred_worker_ids, else lowest-cost eligible non-placeholder.
      7. Expensive or high-risk recommendation sets requires_human_approval per policy.
    """
    pol = policy if policy is not None else (
        load_route_policy(request.job_id, data_dir) if request.job_id else default_route_policy())
    specs = list_worker_specs(registry)
    result = WorkerSelectionResult(job_id=request.job_id, task_type=request.task_type,
                                   policy_id=pol.policy_id)

    blocked_ids = set(pol.blocked_worker_ids)
    blocked_kinds = set(pol.blocked_worker_kinds)
    allowed_kinds = set(pol.allowed_worker_kinds)
    max_cost = _cost_rank(pol.max_cost_tier)
    max_risk = _risk_rank(pol.max_risk_tier)
    cost_ceiling_unknown = pol.max_cost_tier not in _COST_ORDER
    risk_ceiling_unknown = pol.max_risk_tier not in _RISK_ORDER

    eligible: list[WorkerCandidate] = []
    rejected: list[WorkerCandidate] = []

    for s in specs:
        ph = is_placeholder(s)
        cand = WorkerCandidate(worker_id=s.worker_id, eligible=False, cost_tier=s.cost_tier,
                               risk_tier=s.risk_tier, is_placeholder=ph)
        if not s.enabled:
            cand.reason = "disabled worker — never recommended"
            rejected.append(cand); continue
        if s.worker_id in blocked_ids:
            cand.reason = "blocked by route policy (worker id)"
            rejected.append(cand); continue
        if s.kind in blocked_kinds:
            cand.reason = "blocked by route policy (worker kind)"
            rejected.append(cand); continue
        if allowed_kinds and s.kind not in allowed_kinds:
            cand.reason = "kind not in policy allowed_worker_kinds"
            rejected.append(cand); continue
        if not _task_type_allowed(s, request.task_type):
            cand.reason = f"task_type '{request.task_type}' not allowed for this worker"
            rejected.append(cand); continue
        # Cost ceiling: unknown cost is worse-than-max unless the ceiling is itself unknown.
        if not cost_ceiling_unknown and _cost_rank(s.cost_tier) > max_cost:
            cand.reason = f"cost_tier '{s.cost_tier}' exceeds policy max '{pol.max_cost_tier}'"
            rejected.append(cand); continue
        if not risk_ceiling_unknown and _risk_rank(s.risk_tier) > max_risk:
            cand.reason = f"risk_tier '{s.risk_tier}' exceeds policy max '{pol.max_risk_tier}'"
            rejected.append(cand); continue
        cand.eligible = True
        cand.requires_human_justification = (
            s.cost_tier in _EXPENSIVE_TIERS or s.cost_tier == WorkerCostTier.UNKNOWN
            or s.risk_tier in (WorkerRiskTier.HIGH, WorkerRiskTier.UNKNOWN))
        # Score: cheaper + lower risk + enabled non-placeholder rank higher.
        cand.score = (100 - _cost_rank(s.cost_tier) * 10 - _risk_rank(s.risk_tier) * 5
                      - (20 if ph else 0))
        cand.reason = token_reduction_reason(s)
        eligible.append(cand)

    eligible.sort(key=lambda c: (-c.score, c.worker_id))
    result.eligible_candidates = eligible
    result.rejected_candidates = rejected

    chosen = _choose_worker(request, pol, specs, eligible, result)
    spec = get_worker_spec(chosen.worker_id, specs) if chosen else None
    if chosen is None or spec is None:
        result.recommended_worker_id = ""
        result.recommended_reason = ("No eligible worker under the current route policy — adjust "
                                     "the policy or use the human operator.")
        result.requires_human_approval = True
        result.next_safe_action = ("remedy route-policy show "
                                   f"{request.job_id or '<job_id>'} --json")
    else:
        result.recommended_worker_id = spec.worker_id
        result.recommended_reason = chosen.reason
        result.requires_human_approval = _requires_approval(spec, pol)
        result.next_safe_action = _worker_next_action(spec, request.job_id)

    # Token budget warning (estimate only).
    if request.estimated_context_tokens >= 0 and spec is not None:
        fit = estimate_context_fit(spec, request.estimated_context_tokens)
        if fit.get("fits") is False:
            result.token_budget_warning = (
                "estimated context exceeds the recommended worker's context band — consider a "
                "smaller context or a larger-context worker (estimate, not verified)")
    if isinstance(pol.token_budget_hint, int) and spec is not None:
        band = estimate_token_cost_band(spec)
        if band in ("high", "unknown") and pol.token_budget_hint > 0:
            result.token_budget_warning = (result.token_budget_warning or
                "estimated token band exceeds the policy token budget hint — human review advised")

    result.safe_summary = (f"task={request.task_type or 'any'}; "
                           f"recommended={result.recommended_worker_id or 'none'}; "
                           f"approval={result.requires_human_approval}; "
                           f"local_first={result.local_first_applied}")
    return result


def _requires_approval(spec: WorkerSpec, pol: RoutePolicy) -> bool:
    if pol.require_human_approval_for_expensive and (
            spec.cost_tier in _EXPENSIVE_TIERS or spec.cost_tier == WorkerCostTier.UNKNOWN):
        return True
    if pol.require_human_approval_for_high_risk and (
            spec.risk_tier in (WorkerRiskTier.HIGH, WorkerRiskTier.UNKNOWN)):
        return True
    # Placeholders are never "ready" — recommending one always needs a human (to configure it).
    if is_placeholder(spec):
        return True
    return False


def _choose_worker(
    request: WorkerSelectionRequest, pol: RoutePolicy, specs: list[WorkerSpec],
    eligible: list[WorkerCandidate], result: WorkerSelectionResult,
) -> WorkerCandidate | None:
    if not eligible:
        return None
    elig_ids = {c.worker_id: c for c in eligible}

    # 4. Explicit user request / selection wins among the eligible set (safety already applied).
    requested = request.user_requested_worker_id or (
        pol.user_selected_worker_ids[0] if pol.user_selected_worker_ids else "")
    if requested and requested in elig_ids:
        c = elig_ids[requested]
        c.reason = "user-selected worker (eligible under policy)"
        return c

    cheap_task = _is_cheap_task(request, specs)

    # 5. local/Ollama-first preference for cheap tasks (only eligible enabled non-placeholders).
    if cheap_task and pol.prefer_ollama_for_cheap_tasks:
        oll = _first_eligible_of_kind(elig_ids, specs, WorkerKind.OLLAMA_CANDIDATE)
        if oll is not None and not oll.is_placeholder:
            result.ollama_preference_applied = True
            oll.reason = "Ollama-first preference for cheap task (eligible, enabled)"
            return oll
    if cheap_task and pol.prefer_local_for_cheap_tasks:
        loc = _first_eligible_of_kind(elig_ids, specs, WorkerKind.LOCAL_CANDIDATE)
        if loc is not None and not loc.is_placeholder:
            result.local_first_applied = True
            loc.reason = "local-first preference for cheap task (eligible, enabled)"
            return loc

    # 6. preferred_worker_ids order.
    for pid in pol.preferred_worker_ids:
        if pid in elig_ids:
            c = elig_ids[pid]
            c.reason = "policy-preferred worker (eligible)"
            return c

    # 7. Highest-scoring eligible non-placeholder; else highest-scoring eligible.
    for c in eligible:
        if not c.is_placeholder:
            return c
    return eligible[0]


def _is_cheap_task(request: WorkerSelectionRequest, specs: list[WorkerSpec]) -> bool:
    """A task is treated as cheap when its task_type is small/repair-class. Heuristic + estimate."""
    cheap_types = {"repair", "candidate", "fix", "test", "fixture", "smoke"}
    if request.task_type and request.task_type in cheap_types:
        return True
    # Small estimated context → cheap.
    if 0 <= request.estimated_context_tokens <= 8000:
        return True
    return False


def _first_eligible_of_kind(
    elig_ids: dict[str, WorkerCandidate], specs: list[WorkerSpec], kind: str,
) -> WorkerCandidate | None:
    by_id = {s.worker_id: s for s in specs}
    for wid, c in elig_ids.items():
        s = by_id.get(wid)
        if s is not None and s.kind == kind:
            return c
    return None


# ---------------------------------------------------------------------------
# Integrity (Step 1731) — read-only invariant checks. No mutation.
# ---------------------------------------------------------------------------


def worker_registry_integrity(data_dir: Path | None = None) -> dict[str, Any]:
    """Read-only invariant check over the registry + persisted route policies."""
    specs = list_worker_specs(load_worker_registry(data_dir))
    by_id = {s.worker_id: s for s in specs}
    violations: list[dict] = []

    for s in specs:
        # Placeholder must not claim executable readiness (enabled + non-placeholder mode).
        if is_placeholder(s) and s.enabled and s.execution_mode not in _PLACEHOLDER_MODES \
                and s.kind not in (WorkerKind.OLLAMA_CANDIDATE, WorkerKind.CLOUD_CANDIDATE):
            violations.append({"worker_id": s.worker_id, "code": "placeholder_claims_ready"})
        # Unknown cost must never be a cheap tier.
        if s.cost_tier == WorkerCostTier.UNKNOWN and s.cost_tier in _CHEAP_TIERS:
            violations.append({"worker_id": s.worker_id, "code": "unknown_cost_treated_cheap"})
        # No secrets / raw markers / absolute private paths in the public export.
        blob = json.dumps(s.to_dict()).lower()
        if any(m.lower() in blob for m in _RAW_MARKERS):
            violations.append({"worker_id": s.worker_id, "code": "raw_or_secret_in_public"})
        if "/home/" in blob or "/users/" in blob or "/root/" in blob:
            violations.append({"worker_id": s.worker_id, "code": "absolute_path_in_public"})
        # User-selectable workers must be enabled (a disabled worker can't be selected).
        if s.user_selectable and not s.enabled:
            violations.append({"worker_id": s.worker_id, "code": "disabled_but_user_selectable"})

    # Persisted policies: every referenced selected worker must exist + be enabled; blocked+selected
    # is contradictory; expensive selection without approval requirement is flagged.
    policies = _load_all_policies(data_dir)
    for p in policies:
        for wid in p.get("user_selected_worker_ids", []):
            spec = by_id.get(wid)
            if spec is None:
                violations.append({"policy_id": p.get("policy_id"), "code": "selected_worker_missing"})
            elif not spec.enabled:
                violations.append({"policy_id": p.get("policy_id"), "code": "selected_worker_disabled"})
            if wid in p.get("blocked_worker_ids", []):
                violations.append({"policy_id": p.get("policy_id"), "code": "worker_selected_and_blocked"})
        blob = json.dumps(p).lower()
        if "/home/" in blob or "/users/" in blob:
            violations.append({"policy_id": p.get("policy_id"), "code": "absolute_path_in_policy"})

    return {"version": 1, "worker_count": len(specs), "policy_count": len(policies),
            "violation_count": len(violations), "passed": not violations, "violations": violations[:50]}


def _load_all_policies(data_dir: Path | None = None) -> list[dict]:
    """Load every persisted route policy across job workspaces. Corruption-aware; never raises."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    out: list[dict] = []
    ws = ddir / "workspaces"
    try:
        for child in sorted(ws.iterdir()):
            f = child / _RP_DIRNAME / "policy.json"
            if not f.is_file():
                continue
            try:
                out.append(json.loads(f.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                continue
    except OSError:
        pass
    return out


def load_route_policies(data_dir: Path | None = None) -> list[dict]:
    """Public read-only listing of persisted route policies (safe dicts)."""
    return _load_all_policies(data_dir)


# Keep _scrub_public / _safe_path_label referenced for redaction-helper reuse parity with the
# rest of the orchestration package (labels in any future free-text export must pass through them).
_REDACTION_HELPERS = (_scrub_public, _safe_path_label)
