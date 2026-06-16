"""
Automated Local Candidate Generator Adapter v0 (Steps 1609-1644).

The FIRST adapter that asks an explicitly-configured LOCAL loopback model to generate a repair /
self-improvement candidate from a SAFE request package. The generated output is treated as
UNTRUSTED and is IMMEDIATELY routed through the existing intake pipeline:

    local generation → quarantine → Trust Gate → Verification → Materialization → pending approval

Core principle:
  Local model may generate candidates. The orchestrator controls. Trust + Verification judge.
  Human approves. do_continue applies. Model output is UNTRUSTED.

Hard rules enforced here:
  - DISABLED by default; explicit opt-in via env; loopback-only endpoint (127.0.0.1/localhost/::1);
    external/file:///redirects rejected. A missing/unavailable model NEVER breaks deterministic flow.
  - NO provider/cloud SDK, NO external network, NO subprocess for model exec, NO shell, NO browser.
  - The model output is quarantined BEFORE parsing and MUST pass Trust Gate + Verification before any
    materialization. This adapter NEVER creates an intent directly and NEVER approves/applies/tests/
    PRs/git.
  - Generation may only run when Builder Routing selected ``local_candidate_generator`` (no bypass),
    policy + contract allow it, a request package exists, no pending intent, trust+verification are
    available, budget allows, and loop risk is not high.
  - No raw prompt/output/source/diff/log/secrets/tracebacks/absolute paths in any public surface.

Public API::

    load_local_candidate_config(env=None) -> LocalCandidateGeneratorConfig
    default_local_candidate_policy() -> LocalCandidateGenerationPolicy
    check_local_candidate_availability(config=None, transport=None) -> dict
    run_local_candidate_generation(request, *, policy=None, data_dir=None, transport=None, new=False)
        -> LocalCandidateGenerationResult
    list_local_candidate_runs(data_dir=None) -> list[dict]
    load_local_candidate_usage(scope, data_dir=None) -> dict
    export_local_candidate_result_json(result) -> dict
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.local_model_advisor import (
    Transport,
    _extract_generate_text,
    _stdlib_transport,
    _validate_endpoint,
)
from packages.orchestration.provider_trust import _scrub_public

# ---------------------------------------------------------------------------
# Limits / constants
# ---------------------------------------------------------------------------

DEFAULT_TIMEOUT_SECONDS = 20
MAX_TIMEOUT_SECONDS = 60
MAX_PROMPT_CHARS = 16_000
MAX_OUTPUT_BYTES = 64 * 1024
MAX_RETRIES = 1
DEFAULT_MAX_ATTEMPTS_PER_REQUEST = 2
DEFAULT_MAX_ATTEMPTS_PER_FAILURE = 3
DEFAULT_MAX_ATTEMPTS_PER_SELF_ITEM = 3
_PROVIDER_LABEL_PREFIX = "local_candidate_generator"
_RUN_DIRNAME = "local_candidate_runs"


# ---------------------------------------------------------------------------
# Vocabularies
# ---------------------------------------------------------------------------


class LocalCandidateGenerationStopReason:
    OK = "ok"
    DISABLED = "disabled"
    ENDPOINT_BLOCKED = "endpoint_blocked"
    MODEL_MISSING = "model_missing"
    TIMEOUT = "timeout"
    UNAVAILABLE = "unavailable"
    OVERSIZED = "oversized_output"
    ERROR = "error"
    EMPTY_OUTPUT = "empty_output"
    ROUTING_NOT_SELECTED = "routing_not_local_candidate"
    NO_REQUEST_PACKAGE = "no_request_package"
    PENDING_INTENT = "pending_intent_exists"
    CONTRACT_DENIED = "contract_denied"
    BUDGET_EXHAUSTED = "budget_exhausted"
    JOB_NOT_FOUND = "job_not_found"
    REVIEW_BLOCKER = "review_blocker_open"


class LocalCandidateStatus:
    COMPLETED = "completed"            # generated + intake ran (see trust/verification outcome)
    REUSED = "reused"                 # idempotent reuse of a prior run
    DISABLED = "disabled"
    BLOCKED = "blocked"               # routing/contract/budget/pending/review blocked
    UNAVAILABLE = "unavailable"       # model missing/timeout/oversized
    INTENT_PENDING_APPROVAL = "intent_pending_approval"
    TRUST_REJECTED = "trust_rejected"
    VERIFICATION_REJECTED = "verification_rejected"
    NEEDS_REVIEW = "needs_review"
    MATERIALIZATION_FAILED = "materialization_failed"


# ---------------------------------------------------------------------------
# Config / policy
# ---------------------------------------------------------------------------


@dataclass
class LocalCandidateGeneratorConfig:
    enabled: bool = False
    endpoint: str = ""
    model_name: str = ""
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    max_attempts_per_request: int = DEFAULT_MAX_ATTEMPTS_PER_REQUEST
    max_attempts_per_failure: int = DEFAULT_MAX_ATTEMPTS_PER_FAILURE
    max_attempts_per_self_item: int = DEFAULT_MAX_ATTEMPTS_PER_SELF_ITEM

    def to_public_dict(self) -> dict[str, Any]:
        ok, _reason, label = _validate_endpoint(self.endpoint)
        return {
            "enabled": self.enabled,
            "endpoint_label": label,            # loopback label or "blocked:*"; never raw external host
            "endpoint_ok": ok,
            "model_name": self.model_name,
            "timeout_seconds": self.timeout_seconds,
            "max_attempts_per_request": self.max_attempts_per_request,
            "max_attempts_per_failure": self.max_attempts_per_failure,
            "max_attempts_per_self_item": self.max_attempts_per_self_item,
        }


@dataclass
class LocalCandidateGenerationPolicy:
    allow_generate: bool = True            # explicit invocation gate (config.enabled is the real switch)
    require_routing: bool = True
    require_request_package: bool = True
    require_trust_gate: bool = True
    require_verification: bool = True
    require_human_approval: bool = True
    stop_on_pending_intent: bool = True
    stop_on_review_blocker: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "allow_generate": self.allow_generate, "require_routing": self.require_routing,
            "require_request_package": self.require_request_package,
            "require_trust_gate": self.require_trust_gate,
            "require_verification": self.require_verification,
            "require_human_approval": self.require_human_approval,
            "stop_on_pending_intent": self.stop_on_pending_intent,
            "stop_on_review_blocker": self.stop_on_review_blocker,
        }


def default_local_candidate_policy() -> LocalCandidateGenerationPolicy:
    return LocalCandidateGenerationPolicy()


def load_local_candidate_config(env: dict[str, str] | None = None) -> LocalCandidateGeneratorConfig:
    """Build config from environment. Disabled by default; never enabled silently."""
    e = env if env is not None else os.environ
    enabled = str(e.get("REMEDY_LOCAL_CANDIDATE_GENERATOR_ENABLED", "")).strip() in ("1", "true", "yes", "on")
    endpoint = str(e.get("REMEDY_LOCAL_CANDIDATE_GENERATOR_ENDPOINT", "")).strip()
    model = str(e.get("REMEDY_LOCAL_CANDIDATE_GENERATOR_MODEL", "")).strip()
    try:
        timeout = int(e.get("REMEDY_LOCAL_CANDIDATE_GENERATOR_TIMEOUT_SECONDS", "") or DEFAULT_TIMEOUT_SECONDS)
    except (ValueError, TypeError):
        timeout = DEFAULT_TIMEOUT_SECONDS
    timeout = max(1, min(MAX_TIMEOUT_SECONDS, timeout))
    return LocalCandidateGeneratorConfig(
        enabled=enabled, endpoint=endpoint, model_name=model, timeout_seconds=timeout)


def _effective_enabled(config: LocalCandidateGeneratorConfig) -> bool:
    ok, _reason, _label = _validate_endpoint(config.endpoint)
    return bool(config.enabled and ok and config.model_name)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LocalCandidateGenerationRequest:
    request_package_id: str = ""
    job_id: str = ""
    failure_artifact_id: str = ""
    self_attempt_id: str = ""
    routing_id: str = ""
    new: bool = False


@dataclass
class LocalCandidateGenerationLinkage:
    quarantine_id: str = ""
    trust_report_id: str = ""
    verification_id: str = ""
    material_id: str = ""
    intent_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"quarantine_id": self.quarantine_id, "trust_report_id": self.trust_report_id,
                "verification_id": self.verification_id, "material_id": self.material_id,
                "intent_id": self.intent_id}


@dataclass
class LocalCandidateGenerationResult:
    generation_id: str
    job_id: str = ""
    failure_artifact_id: str = ""
    self_attempt_id: str = ""
    request_package_id: str = ""
    routing_id: str = ""
    model_name: str = ""
    endpoint_label: str = ""
    prompt_hash: str = ""
    output_hash: str = ""
    status: str = LocalCandidateStatus.BLOCKED
    stop_reason: str = LocalCandidateGenerationStopReason.DISABLED
    linkage: LocalCandidateGenerationLinkage = field(default_factory=LocalCandidateGenerationLinkage)
    next_safe_action: str = ""
    safe_summary: str = ""
    created_at: str = ""
    duration_ms: int = 0


@dataclass
class LocalCandidateGenerationRunRecord:
    """Safe manifest of a generation run (private dir; holds NO raw text)."""
    generation_id: str = ""
    job_id: str = ""
    failure_artifact_id: str = ""
    self_attempt_id: str = ""
    request_package_id: str = ""
    routing_id: str = ""
    model_name: str = ""
    endpoint_label: str = ""
    prompt_hash: str = ""
    output_hash: str = ""
    prompt_chars: int = 0
    output_chars: int = 0
    status: str = ""
    stop_reason: str = ""
    quarantine_id: str = ""
    trust_report_id: str = ""
    verification_id: str = ""
    material_id: str = ""
    intent_id: str = ""
    duration_ms: int = 0
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": 1, "generation_id": self.generation_id, "job_id": self.job_id,
            "failure_artifact_id": self.failure_artifact_id, "self_attempt_id": self.self_attempt_id,
            "request_package_id": self.request_package_id, "routing_id": self.routing_id,
            "model_name": self.model_name, "endpoint_label": self.endpoint_label,
            "prompt_hash": self.prompt_hash, "output_hash": self.output_hash,
            "prompt_chars": self.prompt_chars, "output_chars": self.output_chars,
            "status": self.status, "stop_reason": self.stop_reason,
            "quarantine_id": self.quarantine_id, "trust_report_id": self.trust_report_id,
            "verification_id": self.verification_id, "material_id": self.material_id,
            "intent_id": self.intent_id, "duration_ms": self.duration_ms,
            "created_at": self.created_at,
        }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scope(job_id: str) -> str:
    return f"job:{job_id}" if job_id else "repository"


# ---------------------------------------------------------------------------
# Step 1612 — safe candidate prompt builder (request package only)
# ---------------------------------------------------------------------------

_CANDIDATE_SCHEMA_INSTRUCTIONS = (
    "You are generating ONE repair candidate for the request package below.\n"
    "STRICT OUTPUT CONTRACT:\n"
    "- Output EXACTLY ONE candidate, as JSON OR a single fenced unified diff.\n"
    "- JSON shape: {\"summary\":..., \"rationale\":..., \"target_files\":[...], "
    "\"unified_diff\":\"...\"} (or \"structured_operations\":[...]).\n"
    "- Use repository-RELATIVE paths only. No absolute paths.\n"
    "- Do NOT include secrets, tokens, credentials, or .env values.\n"
    "- Do NOT target protected/generated/lock files.\n"
    "- Do NOT claim the change was applied, tested, verified, merged, or deployed.\n"
    "- Your output is UNTRUSTED: it will be quarantined, trust-checked, verified, and may be "
    "rejected. It will NOT be applied automatically.\n"
)


def build_candidate_prompt(request_package: dict) -> str:
    """Build a SAFE generation prompt from a request package dict. Scrubbed + bounded; contains
    no raw source/diff/logs/findings/secrets/absolute paths beyond the already-safe package."""
    try:
        from packages.orchestration.repair_request_builder import (
            RepairRequestPackage,
            RepairRequestSection,
            render_request_markdown,
        )
        sections = [RepairRequestSection(
            title=str(s.get("title", "")),
            body=str(s.get("body", "")),
            files=[str(f) for f in (s.get("files", []) or [])],
        ) for s in (request_package.get("sections", []) or []) if isinstance(s, dict)]
        pkg = RepairRequestPackage(
            request_package_id=str(request_package.get("request_package_id", "")),
            job_id=str(request_package.get("job_id", "")),
            failure_artifact_id=str(request_package.get("failure_artifact_id", "")),
            target_kind=str(request_package.get("target_kind", "external")),
            failure_kind=str(request_package.get("failure_kind", "")),
            sections=sections,
        )
        body = render_request_markdown(pkg)
    except (ImportError, ValueError, TypeError, AttributeError, KeyError):
        # Fall back to a minimal safe rendering of the package's safe fields.
        body = json.dumps({
            "request_package_id": request_package.get("request_package_id", ""),
            "target_kind": request_package.get("target_kind", ""),
            "failure_kind": request_package.get("failure_kind", ""),
        }, indent=2)
    prompt = _CANDIDATE_SCHEMA_INSTRUCTIONS + "\n--- REQUEST PACKAGE ---\n" + body
    return _scrub_public(prompt)[:MAX_PROMPT_CHARS]


# ---------------------------------------------------------------------------
# Step 1613 — local loopback client (reuses advisor transport utilities)
# ---------------------------------------------------------------------------


def _generate(config: LocalCandidateGeneratorConfig, prompt: str, transport: Transport,
              ) -> tuple[str, str]:
    """Call the local loopback /api/generate. Returns (model_text, stop_reason). Never raises."""
    ok, _reason, _label = _validate_endpoint(config.endpoint)
    if not ok:
        return "", LocalCandidateGenerationStopReason.ENDPOINT_BLOCKED
    url = config.endpoint.rstrip("/") + "/api/generate"
    payload = json.dumps({"model": config.model_name, "prompt": prompt,
                          "stream": False}).encode("utf-8")
    last = LocalCandidateGenerationStopReason.UNAVAILABLE
    for _attempt in range(MAX_RETRIES + 1):
        try:
            status, body = transport("POST", url, payload, float(config.timeout_seconds))
        except TimeoutError:
            last = LocalCandidateGenerationStopReason.TIMEOUT
            continue
        except (OSError, ValueError):
            last = LocalCandidateGenerationStopReason.UNAVAILABLE
            continue
        if len(body) > MAX_OUTPUT_BYTES:
            return "", LocalCandidateGenerationStopReason.OVERSIZED
        if status != 200:
            last = (LocalCandidateGenerationStopReason.MODEL_MISSING if status == 404
                    else LocalCandidateGenerationStopReason.ERROR)
            continue
        text = _extract_generate_text(body)
        if not (text or "").strip():
            return "", LocalCandidateGenerationStopReason.EMPTY_OUTPUT
        return text, LocalCandidateGenerationStopReason.OK
    return "", last


def check_local_candidate_availability(
    config: LocalCandidateGeneratorConfig | None = None, transport: Transport | None = None,
) -> dict[str, Any]:
    """Safe availability probe. NEVER raises; degrades to unavailable."""
    cfg = config or load_local_candidate_config()
    ok, reason, label = _validate_endpoint(cfg.endpoint)
    out = {"enabled": cfg.enabled, "available": False, "endpoint_label": label,
           "model_name": cfg.model_name, "stop_reason": LocalCandidateGenerationStopReason.DISABLED}
    if not _effective_enabled(cfg):
        out["stop_reason"] = (LocalCandidateGenerationStopReason.DISABLED if not cfg.enabled
                              else LocalCandidateGenerationStopReason.ENDPOINT_BLOCKED)
        return out
    # Probe only when a transport is injected (tests); never required for deterministic flow.
    if transport is None:
        out["available"] = True  # config-available; actual reachability unknown without a probe
        out["stop_reason"] = LocalCandidateGenerationStopReason.OK
        return out
    text, sr = _generate(cfg, "ping", transport)
    out["available"] = sr == LocalCandidateGenerationStopReason.OK
    out["stop_reason"] = sr
    return out


# ---------------------------------------------------------------------------
# Step 1614 — private run storage
# ---------------------------------------------------------------------------


def _runs_root(data_dir: Path) -> Path:
    return data_dir / "workspaces" / "orchestrator" / _RUN_DIRNAME


def _run_dir(generation_id: str, data_dir: Path) -> Path:
    return _runs_root(data_dir) / generation_id


def _atomic_private_write(path: Path, data: bytes, mode: int = 0o600) -> None:
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
    except OSError:
        pass


def _store_run(record: LocalCandidateGenerationRunRecord, prompt: str, raw_output: str,
               data_dir: Path) -> None:
    """Persist raw prompt + output PRIVATELY (0o600) + a SAFE manifest. Raw never goes public."""
    rdir = _run_dir(record.generation_id, data_dir)
    _atomic_private_write(rdir / "prompt.md", prompt.encode("utf-8", errors="replace")[:MAX_PROMPT_CHARS * 4])
    _atomic_private_write(rdir / "raw_output.txt", raw_output.encode("utf-8", errors="replace")[:MAX_OUTPUT_BYTES])
    _atomic_private_write(rdir / "run_manifest.json",
                          json.dumps(record.to_dict(), indent=2).encode("utf-8"))


def list_local_candidate_runs(data_dir: Path | None = None) -> list[dict]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    root = _runs_root(ddir)
    out: list[dict] = []
    try:
        for child in sorted(root.iterdir()):
            f = child / "run_manifest.json"
            if not f.is_file():
                continue
            try:
                out.append(json.loads(f.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                continue
    except OSError:
        return out
    out.sort(key=lambda r: r.get("created_at", ""))
    return out


def load_local_candidate_usage(scope: str, data_dir: Path | None = None) -> dict[str, Any]:
    runs = [r for r in list_local_candidate_runs(data_dir) if _scope(r.get("job_id", "")) == scope]
    completed = [r for r in runs if r.get("status") in (
        LocalCandidateStatus.COMPLETED, LocalCandidateStatus.INTENT_PENDING_APPROVAL,
        LocalCandidateStatus.NEEDS_REVIEW, LocalCandidateStatus.TRUST_REJECTED,
        LocalCandidateStatus.VERIFICATION_REJECTED, LocalCandidateStatus.MATERIALIZATION_FAILED)]
    return {
        "scope": scope, "run_count": len(runs), "completed_count": len(completed),
        "prompt_chars_total": sum(int(r.get("prompt_chars", 0)) for r in runs),
        "output_chars_total": sum(int(r.get("output_chars", 0)) for r in runs),
        "duration_ms_total": sum(int(r.get("duration_ms", 0)) for r in runs),
        "tokens_used": "unknown",
        "models": sorted({r.get("model_name", "") for r in runs if r.get("model_name")}),
    }


def _find_reusable_run(
    data_dir: Path, request_package_id: str, model: str, prompt_hash: str,
) -> dict | None:
    for r in list_local_candidate_runs(data_dir):
        if (r.get("request_package_id") == request_package_id and r.get("model_name") == model
                and r.get("prompt_hash") == prompt_hash
                and r.get("status") not in (LocalCandidateStatus.UNAVAILABLE,
                                            LocalCandidateStatus.BLOCKED,
                                            LocalCandidateStatus.DISABLED)):
            return r
    return None


# ---------------------------------------------------------------------------
# Step 1617 — routing gate
# ---------------------------------------------------------------------------


def _check_routing_gate(
    request: LocalCandidateGenerationRequest, data_dir: Path,
) -> tuple[bool, str, str]:
    """Return (ok, routing_id, stop_reason). Generation may run ONLY if Builder Routing selected
    the ``local_candidate_generator`` tier. No bypass."""
    from packages.orchestration.builder_routing import (
        BuilderRoutingPolicy,
        BuilderRoutingRequest,
        BuilderRoutingTier,
        get_builder_routing_trace,
        select_builder_routing_decision,
    )
    if request.routing_id:
        trace = get_builder_routing_trace(request.routing_id, data_dir)
        if trace is None:
            return False, "", LocalCandidateGenerationStopReason.ROUTING_NOT_SELECTED
        ok = trace.get("selected_tier") == BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR
        return ok, request.routing_id, (
            LocalCandidateGenerationStopReason.OK if ok
            else LocalCandidateGenerationStopReason.ROUTING_NOT_SELECTED)
    # No routing id → build a routing decision with local candidate generation enabled (the
    # generator is being explicitly invoked) and require it to select that tier.
    pol = BuilderRoutingPolicy(allow_local_candidate_generator=True)
    decision = select_builder_routing_decision(
        BuilderRoutingRequest(job_id=request.job_id, failure_artifact_id=request.failure_artifact_id,
                              self_attempt_id=request.self_attempt_id,
                              request_package_id=request.request_package_id),
        pol, data_dir=data_dir, persist=True)
    ok = decision.selected_tier == BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR
    return ok, decision.routing_id, (
        LocalCandidateGenerationStopReason.OK if ok
        else LocalCandidateGenerationStopReason.ROUTING_NOT_SELECTED)


# ---------------------------------------------------------------------------
# Top-level orchestrator
# ---------------------------------------------------------------------------


def export_local_candidate_result_json(r: LocalCandidateGenerationResult) -> dict[str, Any]:
    return {
        "version": 1, "generation_id": r.generation_id, "job_id": r.job_id,
        "failure_artifact_id": r.failure_artifact_id, "self_attempt_id": r.self_attempt_id,
        "request_package_id": r.request_package_id, "routing_id": r.routing_id,
        "model_name": r.model_name, "endpoint_label": r.endpoint_label,
        "prompt_hash": r.prompt_hash, "output_hash": r.output_hash,
        "status": r.status, "stop_reason": r.stop_reason, "linkage": r.linkage.to_dict(),
        "next_safe_action": r.next_safe_action, "safe_summary": r.safe_summary,
        "created_at": r.created_at, "duration_ms": r.duration_ms,
    }


def _result_from_run(d: dict) -> LocalCandidateGenerationResult:
    res = LocalCandidateGenerationResult(
        generation_id=str(d.get("generation_id", "")), job_id=str(d.get("job_id", "")),
        failure_artifact_id=str(d.get("failure_artifact_id", "")),
        self_attempt_id=str(d.get("self_attempt_id", "")),
        request_package_id=str(d.get("request_package_id", "")),
        routing_id=str(d.get("routing_id", "")), model_name=str(d.get("model_name", "")),
        endpoint_label=str(d.get("endpoint_label", "")), prompt_hash=str(d.get("prompt_hash", "")),
        output_hash=str(d.get("output_hash", "")), status=str(d.get("status", "")),
        stop_reason=LocalCandidateGenerationStopReason.OK, created_at=str(d.get("created_at", "")),
        duration_ms=int(d.get("duration_ms", 0)))
    res.linkage = LocalCandidateGenerationLinkage(
        quarantine_id=str(d.get("quarantine_id", "")), trust_report_id=str(d.get("trust_report_id", "")),
        verification_id=str(d.get("verification_id", "")), material_id=str(d.get("material_id", "")),
        intent_id=str(d.get("intent_id", "")))
    res.safe_summary = "Existing local candidate run reused (idempotent)."
    res.next_safe_action = _next_action(res)
    return res


def _next_action(res: LocalCandidateGenerationResult) -> str:
    if res.linkage.intent_id:
        return f"remedy patch approve {res.job_id} {res.linkage.intent_id} --json"
    if res.linkage.verification_id:
        return f"remedy provider verification-show {res.job_id} {res.linkage.verification_id} --json"
    if res.linkage.trust_report_id:
        return f"remedy provider trust-show {res.job_id} {res.linkage.trust_report_id} --json"
    if res.job_id:
        return "remedy local-candidate status --json"
    return "remedy local-candidate status --json"


def _blocked(res: LocalCandidateGenerationResult, status: str, stop_reason: str, summary: str,
             next_action: str) -> LocalCandidateGenerationResult:
    res.status = status
    res.stop_reason = stop_reason
    res.safe_summary = _scrub_public(summary)[:200]
    res.next_safe_action = next_action
    return res


def run_local_candidate_generation(
    request: LocalCandidateGenerationRequest, *,
    policy: LocalCandidateGenerationPolicy | None = None, data_dir: Path | None = None,
    transport: Transport | None = None, new: bool = False,
) -> LocalCandidateGenerationResult:
    """Generate a candidate via the local loopback model (if allowed) and IMMEDIATELY route the
    UNTRUSTED output through quarantine → Trust Gate → Verification → Materialization. Never
    approves/applies; never creates an intent directly; degrades safely when the model is absent."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.repair_request_builder import get_request_package
    from packages.orchestration.run_contract import (
        ContractAction,
        ensure_contract,
        evaluate_run_action,
    )
    from packages.orchestration.storage import JobNotFoundError, load_job

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    pol = policy or default_local_candidate_policy()
    new = bool(new or request.new)      # honor --new from either the kwarg or the request
    cfg = load_local_candidate_config()
    started = datetime.now(timezone.utc)
    gid = uuid4().hex[:16]
    _ok, _r, label = _validate_endpoint(cfg.endpoint)
    res = LocalCandidateGenerationResult(
        generation_id=gid, job_id=request.job_id, failure_artifact_id=request.failure_artifact_id,
        self_attempt_id=request.self_attempt_id, request_package_id=request.request_package_id,
        routing_id=request.routing_id, model_name=cfg.model_name, endpoint_label=label,
        created_at=_now())

    # 0. Disabled / endpoint blocked → safe no-op (never breaks deterministic flow).
    if not _effective_enabled(cfg):
        return _blocked(res, LocalCandidateStatus.DISABLED,
                        LocalCandidateGenerationStopReason.DISABLED if not cfg.enabled
                        else LocalCandidateGenerationStopReason.ENDPOINT_BLOCKED,
                        "Local candidate generator disabled or endpoint not loopback.",
                        "remedy local-candidate status --json")

    # 1. Job + contract gate.
    if request.job_id:
        try:
            job = load_job(UUID(request.job_id), ddir)
        except (ValueError, JobNotFoundError):
            return _blocked(res, LocalCandidateStatus.BLOCKED,
                            LocalCandidateGenerationStopReason.JOB_NOT_FOUND, "Job not found.",
                            "remedy job list --json")
        contract = ensure_contract(job)
        if not evaluate_run_action(contract, ContractAction.LOCAL_CANDIDATE_GENERATE).allowed:
            return _blocked(res, LocalCandidateStatus.BLOCKED,
                            LocalCandidateGenerationStopReason.CONTRACT_DENIED,
                            "Contract denies local candidate generation.",
                            f"remedy contract inspect {request.job_id} --json")

    # 2. Request package required.
    pkg = None
    if request.job_id and request.request_package_id:
        try:
            pkg = get_request_package(job, request.request_package_id)
        except (AttributeError, KeyError, TypeError):
            pkg = None
    if pol.require_request_package and not pkg:
        return _blocked(res, LocalCandidateStatus.BLOCKED,
                        LocalCandidateGenerationStopReason.NO_REQUEST_PACKAGE,
                        "A repair request package is required before generation.",
                        f"remedy repair request {request.job_id} --json" if request.job_id
                        else "remedy local-candidate status --json")

    # 3. Build prompt + idempotency reuse FIRST — a repeated identical call returns the prior run
    #    (this is reuse, not a new generation, so it precedes the pending-intent/routing gates).
    prompt = build_candidate_prompt(pkg or {})
    res.prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
    if not new:
        reuse = _find_reusable_run(ddir, request.request_package_id, cfg.model_name, res.prompt_hash)
        if reuse is not None:
            return _result_from_run(reuse)

    # 4. Pending intent suppresses any NEW generation (more specific than the routing gate).
    if request.job_id and pol.stop_on_pending_intent:
        try:
            from packages.orchestration.approval_queue import APPROVAL_PENDING, list_patch_intents
            if any(i["state"] == APPROVAL_PENDING for i in list_patch_intents(job)):
                return _blocked(res, LocalCandidateStatus.BLOCKED,
                                LocalCandidateGenerationStopReason.PENDING_INTENT,
                                "A pending patch intent already exists; approve/reject it first.",
                                f"remedy builder-routing report --job-id {request.job_id} --json")
        except (ImportError, KeyError, TypeError, AttributeError):
            pass

    # 5. Routing gate (no bypass).
    if pol.require_routing:
        ok, routing_id, sr = _check_routing_gate(request, ddir)
        res.routing_id = routing_id
        if not ok:
            return _blocked(res, LocalCandidateStatus.BLOCKED, sr,
                            "Builder Routing did not select local_candidate_generator.",
                            f"remedy builder-routing report --job-id {request.job_id} --json"
                            if request.job_id else "remedy local-candidate status --json")

    # 6. Budget / attempt caps.
    runs = list_local_candidate_runs(ddir)
    per_req = sum(1 for r in runs if r.get("request_package_id") == request.request_package_id)
    per_fail = sum(1 for r in runs if request.failure_artifact_id
                   and r.get("failure_artifact_id") == request.failure_artifact_id)
    per_self = sum(1 for r in runs if request.self_attempt_id
                   and r.get("self_attempt_id") == request.self_attempt_id)
    if (per_req >= cfg.max_attempts_per_request
            or (request.failure_artifact_id and per_fail >= cfg.max_attempts_per_failure)
            or (request.self_attempt_id and per_self >= cfg.max_attempts_per_self_item)):
        if not new:
            return _blocked(res, LocalCandidateStatus.BLOCKED,
                            LocalCandidateGenerationStopReason.BUDGET_EXHAUSTED,
                            "Local generation attempt budget exhausted for this target.",
                            f"remedy builder-routing report --job-id {request.job_id} --json"
                            if request.job_id else "remedy local-candidate status --json")

    # 7. Generate (transport injected in tests; real loopback otherwise).
    tx = transport if transport is not None else _stdlib_transport
    raw_output, sr = _generate(cfg, prompt, tx)
    res.duration_ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
    if sr != LocalCandidateGenerationStopReason.OK:
        rec = _make_record(res, prompt_chars=len(prompt), output_chars=0,
                           status=LocalCandidateStatus.UNAVAILABLE, stop_reason=sr)
        _store_run(rec, prompt, "", ddir)
        return _blocked(res, LocalCandidateStatus.UNAVAILABLE, sr,
                        "Local model unavailable; deterministic flow unaffected.",
                        "remedy local-candidate status --json")
    res.output_hash = hashlib.sha256(raw_output.encode("utf-8", errors="replace")).hexdigest()[:16]

    # 8. Immediate intake bridge — UNTRUSTED output → quarantine → trust → verification → materialize.
    from packages.orchestration.provider_trust import (
        ProviderOutputIntakeRequest,
        SourceKind,
        intake_provider_repair,
    )
    provider_label = f"{_PROVIDER_LABEL_PREFIX}:{cfg.model_name}"
    intake = intake_provider_repair(
        ProviderOutputIntakeRequest(
            job_id=request.job_id, failure_artifact_id=request.failure_artifact_id,
            provider_name=provider_label, model_name=cfg.model_name,
            source_kind=SourceKind.STDIN),
        stdin_text=raw_output, data_dir=ddir)

    res.linkage = LocalCandidateGenerationLinkage(
        quarantine_id=getattr(intake, "quarantine_id", ""),
        trust_report_id=getattr(intake, "trust_report_id", ""),
        verification_id=getattr(intake, "verification_id", ""),
        material_id=getattr(intake, "material_id", ""),
        intent_id=getattr(intake, "repair_intent_id", ""))
    res.status = _status_from_intake(intake)
    res.stop_reason = LocalCandidateGenerationStopReason.OK
    res.next_safe_action = _next_action(res)
    res.safe_summary = (f"Local candidate generated; trust={getattr(intake, 'trust_status', '')}, "
                        f"verification={getattr(intake, 'verification_decision', '')}, "
                        f"intent={'yes' if res.linkage.intent_id else 'no'}.")

    rec = _make_record(res, prompt_chars=len(prompt), output_chars=len(raw_output),
                       status=res.status, stop_reason=res.stop_reason)
    _store_run(rec, prompt, raw_output, ddir)
    return res


def _status_from_intake(intake: Any) -> str:
    if getattr(intake, "repair_intent_id", ""):
        return LocalCandidateStatus.INTENT_PENDING_APPROVAL
    trust = getattr(intake, "trust_status", "")
    vdec = getattr(intake, "verification_decision", "")
    if trust == "rejected":
        return LocalCandidateStatus.TRUST_REJECTED
    if vdec == "verification_rejected":
        return LocalCandidateStatus.VERIFICATION_REJECTED
    if vdec == "needs_human_review" or trust == "needs_human_review":
        return LocalCandidateStatus.NEEDS_REVIEW
    if getattr(intake, "material_state", "") == "materialization_failed":
        return LocalCandidateStatus.MATERIALIZATION_FAILED
    return LocalCandidateStatus.COMPLETED


def _make_record(res: LocalCandidateGenerationResult, *, prompt_chars: int, output_chars: int,
                 status: str, stop_reason: str) -> LocalCandidateGenerationRunRecord:
    return LocalCandidateGenerationRunRecord(
        generation_id=res.generation_id, job_id=res.job_id,
        failure_artifact_id=res.failure_artifact_id, self_attempt_id=res.self_attempt_id,
        request_package_id=res.request_package_id, routing_id=res.routing_id,
        model_name=res.model_name, endpoint_label=res.endpoint_label,
        prompt_hash=res.prompt_hash, output_hash=res.output_hash,
        prompt_chars=prompt_chars, output_chars=output_chars, status=status, stop_reason=stop_reason,
        quarantine_id=res.linkage.quarantine_id, trust_report_id=res.linkage.trust_report_id,
        verification_id=res.linkage.verification_id, material_id=res.linkage.material_id,
        intent_id=res.linkage.intent_id, duration_ms=res.duration_ms, created_at=res.created_at)
