"""
Token Economy + Context Budget Optimizer v0 (Steps 1757-1796).

The first structured layer that ESTIMATES token cost + context budget, recommends context packs, and
surfaces budget warnings — so Remedy can keep users oriented while reducing token waste. It builds on
the Worker Registry + Route Policy: cheap/small tasks should prefer local/Ollama-capable routes when
safe, expensive/unknown routes require human-facing justification.

  Workers execute. Remedy governs. Token reduction + context retention are core product pillars.

This module is ESTIMATES + METADATA + POLICY only. It NEVER calls a provider/model/Ollama/cloud/local
service, the network, a browser, a subprocess, or a shell; it never executes a worker, applies/
approves/tests anything, or syncs/claims real provider pricing. All costs/tokens are ESTIMATED bands
unless configured evidence exists — unknown stays unknown (never cheap).

Hard rules enforced here:
  - NO provider/model/Ollama/cloud/local-model calls, network, browser, subprocess, shell.
  - NO apply/approve/test/git/PR; NO worker execution; NO automatic generation.
  - NO invented exact pricing / pricing sync — estimates are labeled `estimated`.
  - Unknown token/cost estimate is NEVER treated as cheap.
  - Context pack recommendations exclude protected paths and never dump raw content; missing context
    is reported as a warning, not a fabricated zero.
  - memory_candidates are SUGGESTIONS only (no durable memory is persisted in this block).
  - Expensive/unknown/high-risk/placeholder routes always require human approval (reuses the Worker
    Registry hard-safety floor).
  - No raw prompts/context/source dumps/secrets/absolute paths in any public export.

Public API::

    estimate_text_tokens(text) -> int
    estimate_context_tokens(context_items) -> int
    estimate_task_token_band(task_type, context_estimate) -> str
    estimate_route_token_band(worker_spec, context_estimate) -> str
    estimate_token_savings(original_estimate, optimized_estimate) -> dict
    default_token_budget_profile(job_id) -> TokenBudgetProfile
    load_token_budget_profile(job_id, data_dir=None) -> TokenBudgetProfile
    save_token_budget_profile(profile, data_dir=None) -> bool
    estimate_context_budget(job_id, *, task_id, route_id, data_dir=None) -> ContextBudgetEstimate
    recommend_context_pack(job_id, *, task_id, route_id, data_dir=None) -> ContextPackRecommendation
    compute_token_economy_decision(job_id, *, task_id, route_id, data_dir=None) -> TokenEconomyDecision
    token_economy_integrity(data_dir=None) -> dict
    export_*_json(...) -> dict
"""

from __future__ import annotations

import json
import math
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

SCHEMA_VERSION = "token-economy-v0"
_TE_DIRNAME = "token_economy"
_CHARS_PER_TOKEN = 4                      # deterministic approximation (matches context_inspector)

# Safe default budget floors (estimates; user-configurable, but a floor of 1 keeps them sane).
_DEFAULT_MAX_CONTEXT_TOKENS = 32_000
_DEFAULT_MAX_GENERATION_TOKENS = 8_000
_DEFAULT_MAX_TOTAL_TOKENS = 40_000
_DEFAULT_PREFER_LOCAL_UNDER = 8_000
_DEFAULT_APPROVAL_OVER = 120_000

_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-ant", "sk-proj",
                "api_key", "password", "secret_key")


class ContextPackKind:
    MINIMAL = "minimal"
    FOCUSED = "focused"
    BALANCED = "balanced"
    FULL = "full"
    DEFER_FOR_HUMAN = "defer_for_human"


class BudgetStatus:
    WITHIN = "within_budget"
    NEAR = "near_budget"
    OVER = "over_budget"
    UNKNOWN = "unknown_budget"


class TokenBand:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


def tokens_to_cost_usd(tokens: int | None, price_basis_usd_per_1k_tokens: float | None) -> float | None:
    """Convert a token count to a USD cost at a given per-1k-token price.

    ``None`` propagates rather than becoming a fabricated 0.0: an unmeasured
    token count or an unset price basis (P6, the hard rule this module states
    at its top — no invented pricing) both mean no cost can be computed.
    """
    if tokens is None or price_basis_usd_per_1k_tokens is None:
        return None
    return tokens / 1000 * price_basis_usd_per_1k_tokens


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Estimate helpers (Step 1760) — deterministic; output is ESTIMATE, not truth.
# ---------------------------------------------------------------------------


def estimate_text_tokens(text: str) -> int:
    """Deterministic ~token estimate for a string (chars/4). Estimate only; no tokenizer dependency."""
    if not isinstance(text, str) or not text:
        return 0
    return math.ceil(len(text) / _CHARS_PER_TOKEN)


def estimate_context_tokens(context_items: Any) -> int:
    """Estimate total context tokens from a list of items. Each item may carry an `estimated_tokens`
    or `size_bytes` field, or be a raw string. Unknown/invalid items contribute 0 (never negative)."""
    if not context_items:
        return 0
    total = 0
    try:
        for item in context_items:
            if isinstance(item, str):
                total += estimate_text_tokens(item)
            elif isinstance(item, dict):
                if isinstance(item.get("estimated_tokens"), int) and item["estimated_tokens"] >= 0:
                    total += item["estimated_tokens"]
                elif isinstance(item.get("size_bytes"), int) and item["size_bytes"] >= 0:
                    total += math.ceil(item["size_bytes"] / _CHARS_PER_TOKEN)
            else:
                et = getattr(item, "estimated_tokens", None)
                if isinstance(et, int) and et >= 0:
                    total += et
    except TypeError:
        return 0
    return total


def estimate_task_token_band(task_type: str, context_estimate: int) -> str:
    """Coarse ESTIMATE band for a task from its type + context size. Unknown context stays unknown."""
    if context_estimate is None or context_estimate < 0:
        return TokenBand.UNKNOWN
    if context_estimate <= 8_000:
        return TokenBand.LOW
    if context_estimate <= 32_000:
        return TokenBand.MEDIUM
    return TokenBand.HIGH


def estimate_route_token_band(worker_spec: Any, context_estimate: int) -> str:
    """ESTIMATE band for routing a context of ~N tokens to a worker. Combines the worker's own token
    band with the context size; unknown on either side stays unknown (never downgraded to cheap)."""
    from packages.orchestration.worker_registry import estimate_token_cost_band
    if worker_spec is None:
        return TokenBand.UNKNOWN
    worker_band = estimate_token_cost_band(worker_spec)
    ctx_band = estimate_task_token_band("", context_estimate)
    order = {TokenBand.LOW: 1, TokenBand.MEDIUM: 2, TokenBand.HIGH: 3}
    if worker_band == TokenBand.UNKNOWN or ctx_band == TokenBand.UNKNOWN:
        return TokenBand.UNKNOWN
    worst = max(order.get(worker_band, 0), order.get(ctx_band, 0))
    return {1: TokenBand.LOW, 2: TokenBand.MEDIUM, 3: TokenBand.HIGH}.get(worst, TokenBand.UNKNOWN)


def estimate_token_savings(original_estimate: int, optimized_estimate: int) -> dict[str, Any]:
    """ESTIMATE token savings between an original and an optimized context size. Never claims verified
    savings; negative/invalid inputs yield unknown."""
    if not isinstance(original_estimate, int) or not isinstance(optimized_estimate, int) \
            or original_estimate < 0 or optimized_estimate < 0:
        return {"saved_tokens": "unknown", "saved_ratio": "unknown", "band": TokenBand.UNKNOWN,
                "estimated": True, "verified": False}
    saved = max(0, original_estimate - optimized_estimate)
    ratio = (saved / original_estimate) if original_estimate > 0 else 0.0
    band = TokenBand.LOW if ratio < 0.25 else TokenBand.MEDIUM if ratio < 0.6 else TokenBand.HIGH
    return {"saved_tokens": saved, "saved_ratio": round(ratio, 3), "band": band,
            "estimated": True, "verified": False}


# ---------------------------------------------------------------------------
# TokenBudgetProfile (Step 1759) + storage (Step 1761)
# ---------------------------------------------------------------------------


@dataclass
class TokenBudgetProfile:
    profile_id: str = ""
    job_id: str = ""
    max_context_tokens: int = _DEFAULT_MAX_CONTEXT_TOKENS
    max_generation_tokens: int = _DEFAULT_MAX_GENERATION_TOKENS
    max_total_estimated_tokens: int = _DEFAULT_MAX_TOTAL_TOKENS
    prefer_local_under_tokens: int = _DEFAULT_PREFER_LOCAL_UNDER
    require_human_approval_over_tokens: int = _DEFAULT_APPROVAL_OVER
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id, "job_id": self.job_id,
            "max_context_tokens": self.max_context_tokens,
            "max_generation_tokens": self.max_generation_tokens,
            "max_total_estimated_tokens": self.max_total_estimated_tokens,
            "prefer_local_under_tokens": self.prefer_local_under_tokens,
            "require_human_approval_over_tokens": self.require_human_approval_over_tokens,
            "created_at": self.created_at, "updated_at": self.updated_at,
            "schema_version": SCHEMA_VERSION,
        }


def export_token_budget_profile_json(profile: TokenBudgetProfile) -> dict[str, Any]:
    return profile.to_dict()


def default_token_budget_profile(job_id: str = "") -> TokenBudgetProfile:
    now = _now()
    return TokenBudgetProfile(profile_id=f"tb-{uuid4().hex[:8]}", job_id=job_id,
                              created_at=now, updated_at=now)


def _profile_from_dict(d: dict[str, Any]) -> TokenBudgetProfile:
    def _pos_int(key: str, default: int) -> int:
        v = d.get(key, default)
        try:
            v = int(v)
        except (TypeError, ValueError):
            return default
        return max(1, v)        # safety floor — a budget of <=0 is never allowed
    return TokenBudgetProfile(
        profile_id=str(d.get("profile_id", "")), job_id=str(d.get("job_id", "")),
        max_context_tokens=_pos_int("max_context_tokens", _DEFAULT_MAX_CONTEXT_TOKENS),
        max_generation_tokens=_pos_int("max_generation_tokens", _DEFAULT_MAX_GENERATION_TOKENS),
        max_total_estimated_tokens=_pos_int("max_total_estimated_tokens", _DEFAULT_MAX_TOTAL_TOKENS),
        prefer_local_under_tokens=_pos_int("prefer_local_under_tokens", _DEFAULT_PREFER_LOCAL_UNDER),
        require_human_approval_over_tokens=_pos_int("require_human_approval_over_tokens", _DEFAULT_APPROVAL_OVER),
        created_at=str(d.get("created_at", "")), updated_at=str(d.get("updated_at", "")))


def _te_root(job_id: str, data_dir: Path) -> Path:
    base = job_id if job_id else "orchestrator"
    return data_dir / "workspaces" / base / _TE_DIRNAME


def _profile_path(job_id: str, data_dir: Path) -> Path:
    return _te_root(job_id, data_dir) / "budget_profile.json"


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


def load_token_budget_profile(job_id: str, data_dir: Path | None = None) -> TokenBudgetProfile:
    """Load a job's budget profile, or a safe default if absent/corrupt. Never raises."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    f = _profile_path(job_id, ddir)
    try:
        if f.is_file():
            d = json.loads(f.read_text(encoding="utf-8"))
            if isinstance(d, dict) and d.get("profile_id"):
                return _profile_from_dict(d)
    except (OSError, ValueError, TypeError):
        pass
    return default_token_budget_profile(job_id)


def save_token_budget_profile(profile: TokenBudgetProfile, data_dir: Path | None = None) -> bool:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    if not profile.profile_id:
        profile.profile_id = f"tb-{uuid4().hex[:8]}"
    if not profile.created_at:
        profile.created_at = _now()
    profile.updated_at = _now()
    # Enforce safety floors before persisting.
    profile.max_context_tokens = max(1, int(profile.max_context_tokens))
    profile.max_generation_tokens = max(1, int(profile.max_generation_tokens))
    profile.max_total_estimated_tokens = max(1, int(profile.max_total_estimated_tokens))
    profile.prefer_local_under_tokens = max(1, int(profile.prefer_local_under_tokens))
    profile.require_human_approval_over_tokens = max(1, int(profile.require_human_approval_over_tokens))
    return _atomic_write(_profile_path(profile.job_id, ddir),
                         json.dumps(profile.to_dict(), indent=2).encode("utf-8"))


# ---------------------------------------------------------------------------
# ContextBudgetEstimate (Step 1759)
# ---------------------------------------------------------------------------


@dataclass
class ContextBudgetEstimate:
    job_id: str = ""
    task_id: str = ""
    route_id: str = ""
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    estimated_total_tokens: int = 0
    confidence: str = "estimated_low"
    basis: str = ""
    warnings: list[str] = field(default_factory=list)
    safe_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id, "task_id": self.task_id, "route_id": self.route_id,
            "estimated_input_tokens": self.estimated_input_tokens,
            "estimated_output_tokens": self.estimated_output_tokens,
            "estimated_total_tokens": self.estimated_total_tokens,
            "confidence": self.confidence, "basis": self.basis, "warnings": list(self.warnings),
            "safe_summary": self.safe_summary, "estimated": True, "verified": False,
            "schema_version": SCHEMA_VERSION,
        }


def export_context_budget_estimate_json(e: ContextBudgetEstimate) -> dict[str, Any]:
    return e.to_dict()


def _inspect(job_id: str, task_id: str, data_dir: Path) -> Any:
    """Run the existing safe context inspection for a job. Returns ContextInspection or None."""
    try:
        from uuid import UUID

        from packages.orchestration.context_inspector import inspect_context
        from packages.orchestration.storage import load_job
        from packages.orchestration.timeline import load_run_events
        job = load_job(UUID(job_id), data_dir)
        events = load_run_events(data_dir, job.id)
        return inspect_context(job, events, task_id=task_id or None)
    except Exception:
        # Best-effort read-only helper — any failure (missing job, import, parse) → no inspection.
        return None


def estimate_context_budget(
    job_id: str, *, task_id: str = "", route_id: str = "", data_dir: Path | None = None,
) -> ContextBudgetEstimate:
    """Estimate the input/output/total token budget for a job/task. Reuses the safe context
    inspection (relative paths + estimated_tokens, bytes/4); no raw content. Missing inspection →
    a warning + unknown-low confidence, never a fake zero presented as truth."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    est = ContextBudgetEstimate(job_id=job_id, task_id=task_id, route_id=route_id)
    inspection = _inspect(job_id, task_id, ddir)
    if inspection is None:
        est.warnings.append("no_context_inspection_available")
        est.confidence = "estimated_low"
        est.basis = "no inspection; estimate unavailable"
        est.estimated_input_tokens = 0
        est.estimated_output_tokens = 0
        est.estimated_total_tokens = 0
        est.safe_summary = "Context estimate unavailable (no inspection) — treat as unknown."
        return est
    budget = getattr(inspection, "budget", None)
    input_tokens = int(getattr(budget, "estimated_total_tokens", 0) or 0)
    # Output estimate: bounded heuristic fraction of input (estimate only).
    output_tokens = min(_DEFAULT_MAX_GENERATION_TOKENS, max(256, input_tokens // 4))
    est.estimated_input_tokens = input_tokens
    est.estimated_output_tokens = output_tokens
    est.estimated_total_tokens = input_tokens + output_tokens
    est.confidence = "estimated_medium" if input_tokens > 0 else "estimated_low"
    est.basis = f"context_inspection:{getattr(budget, 'file_count', 0)}_files"
    if getattr(inspection, "missing_context", None):
        est.warnings.append("missing_context_present")
    if getattr(budget, "status", "") == "over_budget":
        est.warnings.append("inspection_over_budget")
    est.safe_summary = (f"estimated input~{input_tokens}, output~{output_tokens}, "
                        f"total~{est.estimated_total_tokens} tokens (estimate, not verified).")
    return est


# ---------------------------------------------------------------------------
# ContextPackRecommendation (Step 1762)
# ---------------------------------------------------------------------------


@dataclass
class ContextPackRecommendation:
    pack_id: str = ""
    job_id: str = ""
    task_id: str = ""
    recommended_pack_kind: str = ContextPackKind.BALANCED
    included_context_refs: list[str] = field(default_factory=list)
    excluded_context_refs: list[str] = field(default_factory=list)
    compression_recommendation: str = ""
    memory_candidates: list[str] = field(default_factory=list)
    estimated_token_savings: dict[str, Any] = field(default_factory=dict)
    risk_notes: list[str] = field(default_factory=list)
    next_safe_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "pack_id": self.pack_id, "job_id": self.job_id, "task_id": self.task_id,
            "recommended_pack_kind": self.recommended_pack_kind,
            "included_context_refs": list(self.included_context_refs),
            "excluded_context_refs": list(self.excluded_context_refs),
            "compression_recommendation": self.compression_recommendation,
            "memory_candidates": list(self.memory_candidates),
            "memory_candidates_persisted": False,    # always — no durable memory in this block
            "estimated_token_savings": dict(self.estimated_token_savings),
            "risk_notes": list(self.risk_notes), "next_safe_action": self.next_safe_action,
            "schema_version": SCHEMA_VERSION,
        }


def export_context_pack_recommendation_json(r: ContextPackRecommendation) -> dict[str, Any]:
    return r.to_dict()


# Categories that are safe-to-keep "durable knowledge" candidates (suggestions only).
_MEMORY_CATEGORIES = ("manifest", "readme")
_PROTECTED_CATEGORIES = ("protected", "symlink", "unsupported")


def recommend_context_pack(
    job_id: str, *, task_id: str = "", route_id: str = "", data_dir: Path | None = None,
) -> ContextPackRecommendation:
    """Recommend a SAFE, bounded context pack kind for a job/task. Metadata only — uses the safe
    context inspection's relative path refs; never dumps raw content; always excludes protected/
    symlink/unsupported paths; missing context → risk note, not a fake zero. memory_candidates are
    SUGGESTIONS only (never persisted as memory in this block)."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    rec = ContextPackRecommendation(pack_id=f"cp-{uuid4().hex[:8]}", job_id=job_id, task_id=task_id)
    profile = load_token_budget_profile(job_id, ddir)
    inspection = _inspect(job_id, task_id, ddir)

    if inspection is None:
        rec.recommended_pack_kind = ContextPackKind.DEFER_FOR_HUMAN
        rec.risk_notes.append("no_context_inspection_available")
        rec.compression_recommendation = "Unavailable — no context inspection; defer to human."
        rec.estimated_token_savings = estimate_token_savings(-1, -1)
        rec.next_safe_action = f"remedy context inspect {job_id} --json" if job_id else \
            "remedy context inspect <job_id> --json"
        return rec

    included = [e for e in getattr(inspection, "included_paths", ())]
    excluded = [e for e in getattr(inspection, "excluded_paths", ())]
    # Safe relative refs only (already redacted by the inspector; pass through _safe_path_label).
    rec.included_context_refs = [_safe_path_label(getattr(e, "path", "")) for e in included][:100]
    rec.excluded_context_refs = [_safe_path_label(getattr(e, "path", "")) for e in excluded][:100]
    # Protected paths are ALWAYS excluded and never enter included refs.
    protected = list(getattr(inspection, "protected_paths", ()))
    for p in protected:
        lbl = _safe_path_label(p)
        if lbl not in rec.excluded_context_refs:
            rec.excluded_context_refs.append(lbl)
        if lbl in rec.included_context_refs:
            rec.included_context_refs.remove(lbl)
            rec.risk_notes.append("protected_path_removed_from_pack")

    input_tokens = int(getattr(getattr(inspection, "budget", None), "estimated_total_tokens", 0) or 0)
    cap = profile.max_context_tokens
    # Pack-kind decision from estimated context vs budget.
    if input_tokens <= 0:
        rec.recommended_pack_kind = ContextPackKind.DEFER_FOR_HUMAN
        rec.risk_notes.append("context_estimate_unavailable")
    elif input_tokens <= profile.prefer_local_under_tokens:
        rec.recommended_pack_kind = ContextPackKind.MINIMAL
    elif input_tokens <= cap // 2:
        rec.recommended_pack_kind = ContextPackKind.FOCUSED
    elif input_tokens <= cap:
        rec.recommended_pack_kind = ContextPackKind.BALANCED
    else:
        rec.recommended_pack_kind = ContextPackKind.FULL
        rec.risk_notes.append("context_exceeds_budget")

    # Compression target: estimate savings of compressing to the budget cap (or to focused size).
    target = min(input_tokens, cap) if input_tokens > 0 else 0
    if input_tokens > cap > 0:
        rec.compression_recommendation = (
            "Estimated context exceeds the budget — recommend compressing to the budget cap or "
            "selecting a focused pack (estimate, not verified).")
        target = cap
    elif rec.recommended_pack_kind in (ContextPackKind.MINIMAL, ContextPackKind.FOCUSED):
        rec.compression_recommendation = ("A smaller pack fits the budget comfortably — minimal/"
                                          "focused context recommended (estimate).")
        target = min(input_tokens, profile.prefer_local_under_tokens)
    else:
        rec.compression_recommendation = "Context fits the budget — no compression needed (estimate)."
    rec.estimated_token_savings = estimate_token_savings(input_tokens, target)

    # Memory candidates — durable-knowledge SUGGESTIONS only (manifest/readme). Never persisted here.
    rec.memory_candidates = [
        _safe_path_label(getattr(e, "path", "")) for e in included
        if getattr(e, "category", "") in _MEMORY_CATEGORIES][:20]

    if getattr(inspection, "missing_context", None):
        rec.risk_notes.append("missing_context_present")
    rec.next_safe_action = (f"remedy context-pack recommend {job_id} --json" if job_id
                            else "remedy context-pack recommend <job_id> --json")
    return rec


# ---------------------------------------------------------------------------
# TokenEconomyDecision (Step 1759 / 1763)
# ---------------------------------------------------------------------------


@dataclass
class TokenEconomyDecision:
    decision_id: str = ""
    job_id: str = ""
    task_id: str = ""
    route_id: str = ""
    recommended_worker_id: str = ""
    budget_status: str = BudgetStatus.UNKNOWN
    estimated_cost_band: str = TokenBand.UNKNOWN
    estimated_token_band: str = TokenBand.UNKNOWN
    requires_human_approval: bool = True
    reason: str = ""
    next_safe_action: str = ""
    context_pack_kind: str = ""
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": 1, "decision_id": self.decision_id, "job_id": self.job_id,
            "task_id": self.task_id, "route_id": self.route_id,
            "recommended_worker_id": self.recommended_worker_id,
            "budget_status": self.budget_status, "estimated_cost_band": self.estimated_cost_band,
            "estimated_token_band": self.estimated_token_band,
            "requires_human_approval": self.requires_human_approval, "reason": self.reason,
            "next_safe_action": self.next_safe_action, "context_pack_kind": self.context_pack_kind,
            "warnings": list(self.warnings), "estimated": True, "verified": False,
            "schema_version": SCHEMA_VERSION,
        }


def export_token_economy_decision_json(d: TokenEconomyDecision) -> dict[str, Any]:
    return d.to_dict()


def _budget_status(total_tokens: int, profile: TokenBudgetProfile) -> str:
    if total_tokens <= 0:
        return BudgetStatus.UNKNOWN
    cap = profile.max_total_estimated_tokens
    if total_tokens > cap:
        return BudgetStatus.OVER
    if total_tokens >= int(cap * 0.8):
        return BudgetStatus.NEAR
    return BudgetStatus.WITHIN


def compute_token_economy_decision(
    job_id: str, *, task_id: str = "", route_id: str = "", task_type: str = "repair",
    data_dir: Path | None = None,
) -> TokenEconomyDecision:
    """Combine the budget profile + context estimate + Worker Registry route policy into a SAFE,
    read-only recommendation. NEVER executes a worker / starts work. Expensive/unknown/high-risk/
    placeholder routes always require human approval (Worker Registry hard-safety floor); a
    cheap small task under the local-preference threshold recommends a local route."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.worker_registry import (
        WorkerSelectionRequest,
        evaluate_worker_selection,
        get_worker_spec,
        hard_safety_requires_approval,
        load_worker_registry,
    )
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    d = TokenEconomyDecision(decision_id=f"te-{uuid4().hex[:8]}", job_id=job_id, task_id=task_id,
                             route_id=route_id)
    profile = load_token_budget_profile(job_id, ddir)
    est = estimate_context_budget(job_id, task_id=task_id, route_id=route_id, data_dir=ddir)
    # Unknown context (no inspection) stays UNKNOWN — never downgraded to a cheap "low" band.
    if "no_context_inspection_available" in est.warnings:
        d.estimated_token_band = TokenBand.UNKNOWN
    else:
        d.estimated_token_band = estimate_task_token_band(task_type, est.estimated_input_tokens)
    d.budget_status = _budget_status(est.estimated_total_tokens, profile)
    d.warnings = list(est.warnings)

    registry = load_worker_registry(ddir)
    selection = evaluate_worker_selection(
        WorkerSelectionRequest(job_id=job_id, task_type=task_type,
                               estimated_context_tokens=est.estimated_input_tokens),
        registry=registry, data_dir=ddir)
    d.recommended_worker_id = selection.recommended_worker_id
    spec = get_worker_spec(d.recommended_worker_id, registry) if d.recommended_worker_id else None

    # Cost band from worker spec (estimate) — unknown stays unknown.
    from packages.orchestration.worker_registry import classify_route_cost
    d.estimated_cost_band = classify_route_cost(spec) if spec is not None else TokenBand.UNKNOWN

    # Unknown context/budget is NEVER cheap/safe (R-0098). If the context could not be inspected,
    # or the token band / budget status is unknown, Remedy must not claim a cheap/local route fits —
    # it must require human approval and recommend a context inspection / estimate.
    unknown_context = (
        "no_context_inspection_available" in est.warnings
        or d.estimated_token_band == TokenBand.UNKNOWN
        or d.budget_status == BudgetStatus.UNKNOWN)

    # Approval: unknown context OR hard-safety floor OR over-budget OR over the approval threshold.
    hard = bool(spec is not None and hard_safety_requires_approval(spec))
    over_threshold = est.estimated_total_tokens >= profile.require_human_approval_over_tokens \
        and est.estimated_total_tokens > 0
    d.requires_human_approval = bool(unknown_context or selection.requires_human_approval or hard
                                     or over_threshold or d.budget_status == BudgetStatus.OVER
                                     or not spec)

    if unknown_context and "unknown_context_or_budget" not in d.warnings:
        d.warnings.append("unknown_context_or_budget")
    if d.budget_status == BudgetStatus.OVER:
        d.warnings.append("estimated_total_over_budget")
    if over_threshold:
        d.warnings.append("estimated_total_over_approval_threshold")

    # Reason + next action.
    if not spec:
        d.reason = "No eligible worker under the route policy — adjust policy or use the human route."
        d.next_safe_action = f"remedy route-policy show {job_id} --json" if job_id else \
            "remedy worker registry-list --json"
    elif unknown_context:
        # Honest unknown state — never imply a cheap route is ready.
        d.reason = ("Context/budget is unknown (no inspection or unknown estimate) — cannot claim a "
                    "cheap/local route fits; run a context inspection or review before routing.")
        d.next_safe_action = (f"remedy context inspect {job_id} --json" if job_id
                              else "remedy context inspect <job_id> --json")
    elif d.requires_human_approval:
        d.reason = ("Recommended route needs human approval (expensive/unknown/high-risk/placeholder "
                    "or over budget/threshold) — estimate only, nothing runs.")
        d.next_safe_action = selection.next_safe_action or (
            f"remedy token economy-report {job_id} --json" if job_id else "remedy worker registry-list --json")
    else:
        d.reason = ("Cheap/local route fits the estimated budget — recommended (estimate; no "
                    "execution).")
        d.next_safe_action = selection.next_safe_action or (
            f"remedy token estimate {job_id} --json" if job_id else "remedy worker registry-list --json")
    d.context_pack_kind = recommend_context_pack(
        job_id, task_id=task_id, route_id=route_id, data_dir=ddir).recommended_pack_kind
    return d


# ---------------------------------------------------------------------------
# Economy report (Step 1765) — safe aggregate for a job.
# ---------------------------------------------------------------------------


def token_economy_report(job_id: str, *, task_id: str = "", route_id: str = "",
                         data_dir: Path | None = None) -> dict[str, Any]:
    """Safe read-only aggregate: budget profile + estimate + pack recommendation + decision. No raw
    content. Estimate-only."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    profile = load_token_budget_profile(job_id, ddir)
    est = estimate_context_budget(job_id, task_id=task_id, route_id=route_id, data_dir=ddir)
    pack = recommend_context_pack(job_id, task_id=task_id, route_id=route_id, data_dir=ddir)
    decision = compute_token_economy_decision(job_id, task_id=task_id, route_id=route_id, data_dir=ddir)
    return {
        "version": 1, "job_id": job_id, "task_id": task_id, "route_id": route_id,
        "budget_profile": profile.to_dict(),
        "context_budget_estimate": est.to_dict(),
        "context_pack_recommendation": pack.to_dict(),
        "decision": decision.to_dict(),
        "estimated": True, "verified": False,
        "next_safe_actions": [
            f"remedy token budget-show {job_id} --json",
            f"remedy token estimate {job_id} --json",
            f"remedy context-pack recommend {job_id} --json",
        ],
    }


def routing_token_hint(job_id: str, *, task_type: str = "repair",
                       data_dir: Path | None = None) -> dict[str, Any]:
    """Lean, read-only token/context hint for Builder Routing (Step 1764). Returns safe estimate
    bands + budget status + context pack kind + approval flag + a single warning string. Never
    executes; on any failure returns an empty-but-safe hint (unknown, not cheap)."""
    try:
        d = compute_token_economy_decision(job_id, task_type=task_type, data_dir=data_dir)
        warning = d.warnings[0] if d.warnings else ""
        return {
            "estimated_token_band": d.estimated_token_band,
            "estimated_cost_band": d.estimated_cost_band,
            "budget_status": d.budget_status,
            "context_pack_kind": d.context_pack_kind,
            "requires_human_approval": d.requires_human_approval,
            "token_budget_warning": warning,
            "local_first_recommended": (d.estimated_cost_band in ("free", "cheap")
                                        and not d.requires_human_approval),
            "next_safe_action": d.next_safe_action,
            "estimated": True,
        }
    except Exception:
        return {"estimated_token_band": TokenBand.UNKNOWN, "estimated_cost_band": TokenBand.UNKNOWN,
                "budget_status": BudgetStatus.UNKNOWN, "context_pack_kind": "",
                "requires_human_approval": True, "token_budget_warning": "",
                "local_first_recommended": False, "next_safe_action": "", "estimated": True}


# ---------------------------------------------------------------------------
# Integrity (Step 1771)
# ---------------------------------------------------------------------------


def _load_all_profiles(data_dir: Path) -> list[dict]:
    out: list[dict] = []
    ws = data_dir / "workspaces"
    try:
        for child in sorted(ws.iterdir()):
            f = child / _TE_DIRNAME / "budget_profile.json"
            if not f.is_file():
                continue
            try:
                out.append(json.loads(f.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                continue
    except OSError:
        pass
    return out


def audit_decision_safety(decision: dict[str, Any]) -> list[dict[str, str]]:
    """Focused invariant helper (R-0099): given a TokenEconomyDecision dict, flag unsafe states
    where unknown context/budget avoids human approval or is presented as a cheap/local fit. Safe
    public codes only; no raw content. Returns a list of violation dicts (empty = safe)."""
    if not isinstance(decision, dict):
        return []
    out: list[dict[str, str]] = []
    band = decision.get("estimated_token_band")
    status = decision.get("budget_status")
    warnings = decision.get("warnings", []) or []
    approval = bool(decision.get("requires_human_approval"))
    reason = str(decision.get("reason", "")).lower()
    no_inspection = "no_context_inspection_available" in warnings
    unknown_ctx = (band == TokenBand.UNKNOWN or status == BudgetStatus.UNKNOWN or no_inspection)
    if band == TokenBand.UNKNOWN and not approval:
        out.append({"code": "unknown_token_band_without_approval"})
    if status == BudgetStatus.UNKNOWN and not approval:
        out.append({"code": "unknown_budget_without_approval"})
    if no_inspection and not approval:
        out.append({"code": "no_inspection_without_approval"})
    # Unknown context must not be presented as a cheap/local budget-fit. Match only the AFFIRMATIVE
    # claim ("fits the estimated budget") — a negated reason ("cannot ... fit") is safe.
    if unknown_ctx and "fits the estimated budget" in reason:
        out.append({"code": "unknown_context_presented_as_fit"})
    return out


def token_economy_integrity(data_dir: Path | None = None,
                            decisions: list[dict] | None = None) -> dict[str, Any]:
    """Read-only invariant check over persisted budget profiles plus optional decision samples. No
    mutation. Flags: budgets <= 0; exact-pricing fields; absolute paths / raw markers in public; and
    (R-0099) decision states where unknown context/budget avoids approval or is shown as a cheap fit.
    Safe public failure codes only."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    violations: list[dict] = []
    profiles = _load_all_profiles(ddir)
    for p in profiles:
        pid = p.get("profile_id", "")
        for k in ("max_context_tokens", "max_generation_tokens", "max_total_estimated_tokens"):
            v = p.get(k)
            if isinstance(v, int) and v <= 0:
                violations.append({"profile_id": pid, "code": "non_positive_budget"})
                break
        blob = json.dumps(p).lower()
        # No exact-pricing claims persisted (we never store real prices).
        if "price_usd" in blob or "cost_usd" in blob or "$" in blob:
            violations.append({"profile_id": pid, "code": "exact_pricing_claimed"})
        if "/home/" in blob or "/users/" in blob or "/root/" in blob:
            violations.append({"profile_id": pid, "code": "absolute_path_in_public"})
        if any(m.lower() in blob for m in _RAW_MARKERS):
            violations.append({"profile_id": pid, "code": "raw_or_secret_in_public"})

    # Optional decision-state audit (R-0099).
    for dec in (decisions or []):
        for v in audit_decision_safety(dec):
            entry = {"decision_id": dec.get("decision_id", ""), **v}
            violations.append(entry)

    return {"version": 1, "profile_count": len(profiles), "decision_count": len(decisions or []),
            "violation_count": len(violations), "passed": not violations, "violations": violations[:50]}


# Keep redaction helpers referenced for parity with the rest of the orchestration package.
_REDACTION_HELPERS = (_scrub_public, _safe_path_label, re)
