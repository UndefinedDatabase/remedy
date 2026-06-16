"""
Local Model Advisor Adapter v0 (Steps 1499-1536) — optional, Ollama-compatible local-model
advisory layer for orchestrator decisions.

Core principle: LLMs advise. The orchestrator controls. Evidence is truth. Local cheap
advisor first. This module NEVER treats model output as truth or executes it. It is:

  - OPTIONAL and DISABLED by default (explicit opt-in via env config or CLI flag).
  - LOOPBACK ONLY (127.0.0.1 / localhost / ::1). External hosts, https-external, file://
    and redirects are rejected. Stdlib HTTP only — no provider/cloud SDK, no subprocess for
    model execution, no browser. Short timeout, bounded response, at most 1-2 retries.
  - SAFE-SUMMARY ONLY in the prompt (phase / top options / selected / rejected / safe
    evidence refs / risk+blocker counts / loop guard / routing plan). No raw source/diff/
    logs/secrets/absolute paths.
  - ADVISORY ONLY. The model may suggest concerns / alternatives / missing evidence; it can
    NEVER produce a command, ProposedTask, patch intent, approval, apply, PR or job, and can
    NEVER override a contract/budget/review blocker or mark evidence true/complete.

A missing/unavailable local model must NEVER break deterministic orchestration: every entry
point degrades to a safe "unavailable" result instead of raising.

Public API::

    load_local_advisor_config(...) -> LocalAdvisorConfig
    build_local_advisor_prompt(decision_or_situation, data_dir=None) -> str
    check_local_advisor_availability(config, transport=None) -> LocalAdvisorAvailability
    run_local_advisor(request, config, data_dir=None, transport=None, new=False) -> LocalAdvisorResponse
    parse_local_advisor_response(raw_text) -> tuple[dict, list[LocalAdvisorFinding], str]
    list_local_advisor_runs(data_dir=None) -> list[dict]
    load_local_advisor_usage(scope, data_dir=None) -> dict
    export_local_advisor_response_json / export_local_advisor_availability_json
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

# ---------------------------------------------------------------------------
# Bounds (no magic numbers in the flow)
# ---------------------------------------------------------------------------

MAX_PROMPT_CHARS = 8_000
MAX_RESPONSE_BYTES = 32_768
DEFAULT_TIMEOUT_SECONDS = 8
MAX_TIMEOUT_SECONDS = 30
MAX_RETRIES = 1               # at most one retry (configured max 1 or 2; never a storm)
MAX_UNAVAILABLE_REPEAT = 2    # stop re-probing the same evidence after this many failures
MAX_FIELD_LEN = 300
MAX_CONCERNS = 10
MAX_HINTS = 10
DEFAULT_MAX_RUNS = 20         # local advisor budget per scope (separate from provider budget)

_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})


# ---------------------------------------------------------------------------
# Vocabularies (Step 1500)
# ---------------------------------------------------------------------------


class LocalAdvisorStatus:
    COMPLETED = "completed"
    DISABLED = "disabled"
    UNAVAILABLE = "unavailable"
    UNPARSEABLE = "advisor_unparseable"
    REUSED = "reused"
    BLOCKED = "blocked"
    ERROR = "error"


class LocalAdvisorStopReason:
    OK = "ok"
    DISABLED = "disabled"
    ENDPOINT_BLOCKED = "endpoint_blocked"
    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    MODEL_MISSING = "model_missing"
    UNPARSEABLE = "advisor_unparseable"
    OVERSIZED = "oversized_response"
    BUDGET_EXHAUSTED = "budget_exhausted"
    REUSED = "reused"
    ERROR = "error"


class LocalAdvisorDecisionImpact:
    NO_CHANGE = "no_change"
    CONFIDENCE_ADJUSTED = "confidence_adjusted"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"


_SEVERITIES = ("low", "medium", "high")
_LOOP_RISKS = ("none", "low", "medium", "high")
_CONFIDENCE = ("low", "medium", "high")


# ---------------------------------------------------------------------------
# Models (Step 1500) — NO raw prompt/response fields are ever public.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LocalAdvisorConfig:
    """Explicit local advisor configuration. Disabled by default (Step 1501)."""

    enabled: bool = False
    endpoint: str = ""
    model_name: str = ""
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    max_runs: int = DEFAULT_MAX_RUNS

    def to_public_dict(self) -> dict[str, Any]:
        ok, _reason, label = _validate_endpoint(self.endpoint)
        return {
            "enabled": self.enabled,
            "endpoint_label": label,
            "endpoint_loopback_ok": ok,
            "model_name": _safe_label(self.model_name),
            "timeout_seconds": self.timeout_seconds,
            "max_runs": self.max_runs,
        }


@dataclass
class LocalAdvisorRequest:
    """A request to advise on a SAFE orchestrator decision/situation summary."""

    job_id: str = ""
    decision_id: str = ""
    scope: str = "repository"
    payload: dict[str, Any] = field(default_factory=dict)  # safe export, never raw


@dataclass
class LocalAdvisorFinding:
    code: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "severity": self.severity, "message": self.message}


@dataclass
class LocalAdvisorAvailability:
    enabled: bool = False
    available: bool = False
    endpoint_label: str = ""
    model_name: str = ""
    stop_reason: str = LocalAdvisorStopReason.DISABLED
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled, "available": self.available,
            "endpoint_label": self.endpoint_label, "model_name": self.model_name,
            "stop_reason": self.stop_reason, "detail": self.detail,
        }


@dataclass
class LocalAdvisorResponse:
    advisor_run_id: str = ""
    job_id: str = ""
    decision_id: str = ""
    scope: str = "repository"
    model_name: str = ""
    endpoint_label: str = ""
    enabled: bool = False
    available: bool = False
    prompt_hash: str = ""
    response_hash: str = ""
    status: str = LocalAdvisorStatus.DISABLED
    stop_reason: str = LocalAdvisorStopReason.DISABLED
    summary: str = ""
    findings: list[LocalAdvisorFinding] = field(default_factory=list)
    suggested_concerns: list[dict[str, Any]] = field(default_factory=list)
    suggested_alternatives: list[dict[str, Any]] = field(default_factory=list)
    missing_evidence_hints: list[str] = field(default_factory=list)
    loop_risk: str = "none"
    confidence_hint: str = "low"
    decision_impact: str = LocalAdvisorDecisionImpact.NO_CHANGE
    created_at: str = ""
    duration_ms: int = 0


@dataclass
class LocalAdvisorRunRecord:
    """Safe manifest of an advisor run (private dir; still holds NO raw text)."""

    advisor_run_id: str = ""
    job_id: str = ""
    decision_id: str = ""
    scope: str = "repository"
    model_name: str = ""
    endpoint_label: str = ""
    prompt_hash: str = ""
    response_hash: str = ""
    status: str = ""
    stop_reason: str = ""
    decision_impact: str = LocalAdvisorDecisionImpact.NO_CHANGE
    prompt_chars: int = 0
    response_chars: int = 0
    duration_ms: int = 0
    finding_severity_counts: dict[str, int] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": 1, "advisor_run_id": self.advisor_run_id, "job_id": self.job_id,
            "decision_id": self.decision_id, "scope": self.scope,
            "model_name": self.model_name, "endpoint_label": self.endpoint_label,
            "prompt_hash": self.prompt_hash, "response_hash": self.response_hash,
            "status": self.status, "stop_reason": self.stop_reason,
            "decision_impact": self.decision_impact,
            "prompt_chars": self.prompt_chars, "response_chars": self.response_chars,
            "duration_ms": self.duration_ms,
            "finding_severity_counts": self.finding_severity_counts,
            "created_at": self.created_at,
        }


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scrub(text: str, limit: int = MAX_FIELD_LEN) -> str:
    """Scrub secrets / absolute paths / traceback markers, collapse whitespace, bound."""
    from packages.orchestration.provider_trust import _scrub_public
    out = re.sub(r"\s+", " ", str(text)).strip()
    out = _scrub_public(out)
    return out[:limit]


def _safe_label(text: str, limit: int = 80) -> str:
    return _scrub(text, limit)


_CODE_FENCE_RE = re.compile(r"```")
_DIFF_MARKERS = ("diff --git", "@@ -", "+++ b/", "--- a/", "<<<<<<<", ">>>>>>>")


def _looks_like_code_or_diff(text: str) -> bool:
    if _CODE_FENCE_RE.search(text):
        return True
    return any(m in text for m in _DIFF_MARKERS)


# ---------------------------------------------------------------------------
# Config (Step 1501) — env-driven, disabled by default, loopback only.
# ---------------------------------------------------------------------------


def _validate_endpoint(endpoint: str) -> tuple[bool, str, str]:
    """Return (ok, reason, public_label). Loopback only; never echoes a raw external host."""
    ep = (endpoint or "").strip()
    if not ep:
        return False, "no_endpoint", "none"
    try:
        u = urlparse(ep)
    except (ValueError, TypeError):
        return False, "unparseable_endpoint", "blocked:invalid"
    if u.scheme not in ("http", "https"):
        # file://, unix://, ftp:// etc. are not allowed.
        return False, "scheme_not_http", f"blocked:{_safe_label(u.scheme or 'none', 16)}"
    host = (u.hostname or "").strip().lower()
    if host not in _LOOPBACK_HOSTS:
        # Never echo the raw external host.
        return False, "non_loopback", "blocked:non-loopback"
    port = f":{u.port}" if u.port else ""
    label = f"{u.scheme}://{host}{port}"
    return True, "loopback_ok", label


def load_local_advisor_config(
    *, enabled_override: bool | None = None, env: dict[str, str] | None = None,
) -> LocalAdvisorConfig:
    """Build config from environment. Disabled by default; never enabled silently.

    enabled_override (e.g. a CLI ``--use-local-advisor`` flag) can request enablement, but
    the config is only enabled when the endpoint is loopback-valid AND a model is set.
    """
    e = env if env is not None else os.environ
    raw_enabled = (e.get("REMEDY_LOCAL_ADVISOR_ENABLED", "") or "").strip().lower()
    enabled = raw_enabled in ("1", "true", "yes", "on")
    if enabled_override is not None:
        enabled = enabled or bool(enabled_override)
    endpoint = (e.get("REMEDY_LOCAL_ADVISOR_ENDPOINT", "") or "").strip()
    model = (e.get("REMEDY_LOCAL_ADVISOR_MODEL", "") or "").strip()
    try:
        timeout = int(e.get("REMEDY_LOCAL_ADVISOR_TIMEOUT_SECONDS", "") or DEFAULT_TIMEOUT_SECONDS)
    except (ValueError, TypeError):
        timeout = DEFAULT_TIMEOUT_SECONDS
    timeout = max(1, min(MAX_TIMEOUT_SECONDS, timeout))
    try:
        max_runs = int(e.get("REMEDY_LOCAL_ADVISOR_MAX_RUNS", "") or DEFAULT_MAX_RUNS)
    except (ValueError, TypeError):
        max_runs = DEFAULT_MAX_RUNS
    max_runs = max(1, max_runs)
    # Only truly enabled when endpoint is loopback-valid and a model is configured.
    ep_ok, _reason, _label = _validate_endpoint(endpoint)
    effective = enabled and ep_ok and bool(model)
    return LocalAdvisorConfig(
        enabled=effective, endpoint=endpoint,
        model_name=model, timeout_seconds=timeout, max_runs=max_runs)


# ---------------------------------------------------------------------------
# Safe prompt builder (Step 1502)
# ---------------------------------------------------------------------------


def _as_summary_dict(decision_or_situation: Any) -> dict[str, Any]:
    """Normalise a decision/situation (dataclass or already-exported dict) to a safe dict."""
    obj = decision_or_situation
    if isinstance(obj, dict):
        return obj
    try:
        from packages.orchestration.orchestrator_brain import (
            OrchestratorDecision,
            OrchestratorSituation,
            export_decision_json,
            export_situation_json,
        )
        if isinstance(obj, OrchestratorDecision):
            return export_decision_json(obj)
        if isinstance(obj, OrchestratorSituation):
            return export_situation_json(obj)
    except (ImportError, ValueError, TypeError):
        pass
    return {}


_PROMPT_INSTRUCTIONS = (
    "You are a local ADVISOR for an autonomous software-repair orchestrator. You do NOT "
    "control anything. Critique the deterministic decision below using ONLY the safe summary "
    "provided. Rules: do NOT produce code, do NOT produce patches/diffs, do NOT request "
    "secrets, do NOT claim you executed anything, do NOT invent commands. List concerns, "
    "missing evidence, and at most one safer alternative. Output JSON ONLY matching exactly:\n"
    '{"summary": "...", "concerns": [{"severity": "low|medium|high", "message": "...", '
    '"evidence_ref": "..."}], "missing_evidence": ["..."], "alternative_action": '
    '{"label": "...", "reason": "..."}, "loop_risk": "none|low|medium|high", '
    '"confidence_hint": "low|medium|high"}'
)


def build_local_advisor_prompt(decision_or_situation: Any, data_dir: Path | None = None) -> str:
    """Build a SAFE, bounded advisor prompt. Includes only safe summary fields — never raw
    source/diff/logs/finding bodies/provider output/test output/secrets/absolute paths."""
    d = _as_summary_dict(decision_or_situation)
    phase = _scrub(d.get("current_phase", "unknown"), 60)
    routing = (d.get("model_routing_plan") or {})
    loop = d.get("loop_guard_status", d.get("loop_guard", {}).get("status", "") if isinstance(d.get("loop_guard"), dict) else "")

    lines: list[str] = [_PROMPT_INSTRUCTIONS, "", "## Safe decision summary", f"- phase: {phase}"]

    # Selected deterministic option.
    sel = d.get("selected_option")
    if sel:
        lines.append(f"- selected_option: {_scrub(sel.get('kind',''),40)} — {_scrub(sel.get('label',''),120)}")
    else:
        lines.append(f"- selected_option: none (stop_reason={_scrub(d.get('stop_reason',''),40)})")

    # Top deterministic options (labels + scores only; no commands).
    opts = d.get("options") or []
    if opts:
        lines.append("- top_options:")
        for o in sorted(opts, key=lambda x: x.get("score", 0), reverse=True)[:5]:
            lines.append(f"  - {_scrub(o.get('kind',''),40)} (score {o.get('score',0)}, "
                         f"available={o.get('available')})")

    # Rejected alternatives (from a decision export).
    rej = d.get("rejected_options") or []
    if rej:
        lines.append("- rejected_alternatives:")
        for r in rej[:5]:
            lines.append(f"  - {_scrub(r.get('label',''),100)} (score {r.get('score',0)})")

    # Safe evidence refs (source + status only; never bodies).
    refs = d.get("evidence_refs") or []
    if refs:
        lines.append("- evidence_refs:")
        for r in refs[:10]:
            lines.append(f"  - {_scrub(r.get('source',''),40)}: {_scrub(r.get('status',''),20)}")

    # Counts only.
    lines.append(f"- blocker_count: {len(d.get('blockers', []))}")
    lines.append(f"- risk_count: {len(d.get('risks', []))}")
    lines.append(f"- loop_guard: {_scrub(loop or 'allow', 30)}")
    lines.append(f"- routing_tier: {_scrub(routing.get('tier',''),40)}")
    lines.append(f"- confidence: {_scrub(d.get('confidence',''),20)}")
    lines.append("")
    lines.append("Respond with JSON only.")

    prompt = "\n".join(lines)
    # Defensive: scrub the whole prompt once more and bound it.
    from packages.orchestration.provider_trust import _scrub_public
    prompt = _scrub_public(prompt)[:MAX_PROMPT_CHARS]
    return prompt


# ---------------------------------------------------------------------------
# Response schema + parsing (Steps 1503/1508)
# ---------------------------------------------------------------------------


def _normalise_severity(value: Any) -> str:
    v = str(value or "").strip().lower()
    return v if v in _SEVERITIES else "low"


def _normalise_loop_risk(value: Any) -> str:
    v = str(value or "").strip().lower()
    return v if v in _LOOP_RISKS else "none"


def _normalise_confidence(value: Any) -> str:
    v = str(value or "").strip().lower()
    return v if v in _CONFIDENCE else "low"


def parse_local_advisor_response(
    raw_text: str,
) -> tuple[dict[str, Any], list[LocalAdvisorFinding], str]:
    """Parse + validate + redact a model response.

    Returns (safe_parsed, findings, status). ``status`` is COMPLETED or UNPARSEABLE.
    Never raises. Code/diff content is stripped and flagged as a high concern; secrets/
    absolute paths/tracebacks are scrubbed; unknown severities normalised.
    """
    findings: list[LocalAdvisorFinding] = []
    text = raw_text or ""

    # Secret / leak scan on the RAW response (never echoes the matched value).
    try:
        from packages.orchestration.provider_trust import scan_secrets
        for f in scan_secrets(text):
            findings.append(LocalAdvisorFinding(f.code, f.severity, f.message))
    except (ImportError, AttributeError):
        pass

    obj = _extract_json_object(text)
    if obj is None:
        findings.append(LocalAdvisorFinding(
            "advisor_unparseable", "medium",
            "Advisor response was not valid JSON; treated as advisory-only and ignored."))
        return ({}, findings, LocalAdvisorStatus.UNPARSEABLE)

    # Code/diff anywhere in the response → strip + high concern, never accept as action.
    if _looks_like_code_or_diff(text):
        findings.append(LocalAdvisorFinding(
            "code_or_diff_in_response", "high",
            "Advisor response contained code/diff-like content; stripped and not actionable."))

    safe: dict[str, Any] = {}
    safe["summary"] = _scrub(obj.get("summary", ""), MAX_FIELD_LEN)

    concerns: list[dict[str, Any]] = []
    raw_concerns = obj.get("concerns")
    if isinstance(raw_concerns, list):
        for c in raw_concerns[:MAX_CONCERNS]:
            if not isinstance(c, dict):
                continue
            concerns.append({
                "severity": _normalise_severity(c.get("severity")),
                "message": _scrub(c.get("message", ""), MAX_FIELD_LEN),
                "evidence_ref": _scrub(c.get("evidence_ref", ""), 80),
            })
    safe["concerns"] = concerns

    hints: list[str] = []
    raw_hints = obj.get("missing_evidence")
    if isinstance(raw_hints, list):
        for h in raw_hints[:MAX_HINTS]:
            hint = _scrub(h, MAX_FIELD_LEN)
            if hint:
                hints.append(hint)
    safe["missing_evidence"] = hints

    alt = obj.get("alternative_action")
    safe["alternative_action"] = {}
    if isinstance(alt, dict):
        label = _scrub(alt.get("label", ""), 120)
        if label:
            safe["alternative_action"] = {
                "label": label, "reason": _scrub(alt.get("reason", ""), MAX_FIELD_LEN)}

    safe["loop_risk"] = _normalise_loop_risk(obj.get("loop_risk"))
    safe["confidence_hint"] = _normalise_confidence(obj.get("confidence_hint"))
    return (safe, findings, LocalAdvisorStatus.COMPLETED)


def _extract_json_object(text: str) -> dict[str, Any] | None:
    """Best-effort: parse the first balanced JSON object. Returns None if none/invalid."""
    if not text:
        return None
    s = text.strip()
    try:
        obj = json.loads(s)
        return obj if isinstance(obj, dict) else None
    except (json.JSONDecodeError, ValueError):
        pass
    # Fallback: slice the first {...} span.
    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        obj = json.loads(s[start:end + 1])
        return obj if isinstance(obj, dict) else None
    except (json.JSONDecodeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Ollama-compatible client (Step 1505) — stdlib only, loopback only, bounded.
# ---------------------------------------------------------------------------

# Transport seam: (method, url, body_bytes|None, timeout) -> (status_code, body_bytes).
# Tests inject a fake transport; production uses the stdlib transport. NEVER a subprocess,
# NEVER a provider SDK, NEVER a non-loopback host (validated before the call).
Transport = Callable[[str, str, "bytes | None", float], tuple[int, bytes]]


def _stdlib_transport(method: str, url: str, body: bytes | None, timeout: float) -> tuple[int, bytes]:
    """Minimal stdlib HTTP. Redirects are rejected; response is size-bounded."""
    import urllib.error
    import urllib.request

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
            return None  # reject all redirects

    opener = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request(url, data=body, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with opener.open(req, timeout=timeout) as resp:
            data = resp.read(MAX_RESPONSE_BYTES + 1)
            return (getattr(resp, "status", 200) or 200, data)
    except urllib.error.HTTPError as e:  # 4xx/5xx
        try:
            data = e.read(MAX_RESPONSE_BYTES + 1)
        except (OSError, ValueError):
            data = b""
        return (e.code, data)


def _generate(config: LocalAdvisorConfig, prompt: str, transport: Transport,
              ) -> tuple[str, str]:
    """Call the local /api/generate endpoint. Returns (model_text, stop_reason).

    stop_reason is OK on success, else TIMEOUT/UNAVAILABLE/OVERSIZED/ERROR. Never raises."""
    ok, _reason, _label = _validate_endpoint(config.endpoint)
    if not ok:
        return "", LocalAdvisorStopReason.ENDPOINT_BLOCKED
    url = config.endpoint.rstrip("/") + "/api/generate"
    payload = json.dumps({"model": config.model_name, "prompt": prompt,
                          "stream": False}).encode("utf-8")
    last = LocalAdvisorStopReason.UNAVAILABLE
    for _attempt in range(MAX_RETRIES + 1):
        try:
            status, body = transport("POST", url, payload, float(config.timeout_seconds))
        except TimeoutError:
            last = LocalAdvisorStopReason.TIMEOUT
            continue
        except (OSError, ValueError):
            last = LocalAdvisorStopReason.UNAVAILABLE
            continue
        if len(body) > MAX_RESPONSE_BYTES:
            return "", LocalAdvisorStopReason.OVERSIZED
        if status != 200:
            last = (LocalAdvisorStopReason.MODEL_MISSING if status == 404
                    else LocalAdvisorStopReason.ERROR)
            continue
        text = _extract_generate_text(body)
        return text, LocalAdvisorStopReason.OK
    return "", last


def _extract_generate_text(body: bytes) -> str:
    """Extract the model text from an Ollama /api/generate response (``response`` field)."""
    try:
        obj = json.loads(body.decode("utf-8", errors="replace"))
        if isinstance(obj, dict) and isinstance(obj.get("response"), str):
            return obj["response"]
        # Some servers return the raw text directly.
        return body.decode("utf-8", errors="replace")
    except (json.JSONDecodeError, ValueError):
        return body.decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Availability probe (Step 1506)
# ---------------------------------------------------------------------------


def check_local_advisor_availability(
    config: LocalAdvisorConfig, transport: Transport | None = None,
) -> LocalAdvisorAvailability:
    """Probe whether the local advisor can be used. Never raises, never crashes the caller."""
    ok, reason, label = _validate_endpoint(config.endpoint)
    av = LocalAdvisorAvailability(
        enabled=config.enabled, available=False, endpoint_label=label,
        model_name=_safe_label(config.model_name))
    if not config.enabled:
        av.stop_reason = LocalAdvisorStopReason.DISABLED
        av.detail = "Local advisor is disabled (opt-in required)."
        return av
    if not ok:
        av.stop_reason = LocalAdvisorStopReason.ENDPOINT_BLOCKED
        av.detail = f"Endpoint rejected ({reason}); loopback only."
        return av
    if not config.model_name:
        av.stop_reason = LocalAdvisorStopReason.MODEL_MISSING
        av.detail = "No model configured."
        return av
    tx = transport or _stdlib_transport
    url = config.endpoint.rstrip("/") + "/api/tags"
    try:
        status, body = tx("GET", url, None, float(config.timeout_seconds))
    except TimeoutError:
        av.stop_reason = LocalAdvisorStopReason.TIMEOUT
        av.detail = "Endpoint timed out."
        return av
    except (OSError, ValueError):
        av.stop_reason = LocalAdvisorStopReason.UNAVAILABLE
        av.detail = "Endpoint unavailable."
        return av
    if status != 200 or len(body) > MAX_RESPONSE_BYTES:
        av.stop_reason = LocalAdvisorStopReason.UNAVAILABLE
        av.detail = "Endpoint did not respond OK."
        return av
    if not _model_present(body, config.model_name):
        av.stop_reason = LocalAdvisorStopReason.MODEL_MISSING
        av.detail = "Configured model not present on the local server."
        return av
    av.available = True
    av.stop_reason = LocalAdvisorStopReason.OK
    av.detail = "Local advisor available."
    return av


def _model_present(body: bytes, model_name: str) -> bool:
    try:
        obj = json.loads(body.decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, ValueError):
        return False
    models = obj.get("models") if isinstance(obj, dict) else None
    if not isinstance(models, list):
        return False
    want = model_name.strip().lower()
    for m in models:
        name = (m.get("name") if isinstance(m, dict) else str(m)) or ""
        nl = name.strip().lower()
        if nl == want or nl.split(":")[0] == want.split(":")[0]:
            return True
    return False


# ---------------------------------------------------------------------------
# Private run storage (Step 1504)
# ---------------------------------------------------------------------------


def _runs_root(data_dir: Path) -> Path:
    return data_dir / "workspaces" / "orchestrator" / "local_advisor_runs"


def _store_run(
    data_dir: Path, run: LocalAdvisorRunRecord, prompt: str, raw_text: str,
) -> bool:
    """Persist the run privately: prompt.md + response.txt (raw, 0o600) + run_manifest.json
    (safe). 0o700 dir. Atomic. No overwrite (fresh run_id dir). Returns stored flag."""
    rdir = _runs_root(data_dir) / run.advisor_run_id
    try:
        rdir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(rdir, 0o700)
        except OSError:
            pass
        _atomic_private_write(rdir / "prompt.md", prompt.encode("utf-8", errors="replace"))
        _atomic_private_write(rdir / "response.txt", raw_text.encode("utf-8", errors="replace"))
        manifest = json.dumps(run.to_dict(), indent=2, sort_keys=True).encode("utf-8")
        _atomic_private_write(rdir / "run_manifest.json", manifest)
        return True
    except OSError:
        return False


def _atomic_private_write(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data[:MAX_PROMPT_CHARS * 4])  # hard upper bound
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def list_local_advisor_runs(data_dir: Path | None = None) -> list[dict]:
    """List safe run manifests (no raw prompt/response). Sorted by created_at."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    base = _runs_root(ddir)
    if not base.is_dir():
        return []
    out: list[dict] = []
    try:
        for p in sorted(base.glob("*/run_manifest.json")):
            try:
                out.append(json.loads(p.read_bytes()))
            except (OSError, json.JSONDecodeError):
                continue
    except OSError:
        return []
    out.sort(key=lambda d: d.get("created_at", ""))
    return out


def load_local_advisor_usage(scope: str, data_dir: Path | None = None) -> dict[str, Any]:
    """Aggregate safe local-advisor usage for a scope (Step 1516). Separate from the
    external provider budget. Token counts stay unknown (no tokenizer)."""
    runs = [r for r in list_local_advisor_runs(data_dir) if r.get("scope") == scope]
    completed = [r for r in runs if r.get("status") == LocalAdvisorStatus.COMPLETED]
    return {
        "scope": scope,
        "run_count": len(runs),
        "completed_count": len(completed),
        "prompt_chars_total": sum(int(r.get("prompt_chars", 0)) for r in runs),
        "response_chars_total": sum(int(r.get("response_chars", 0)) for r in runs),
        "duration_ms_total": sum(int(r.get("duration_ms", 0)) for r in runs),
        "tokens_used": "unknown",
        "models": sorted({r.get("model_name", "") for r in runs if r.get("model_name")}),
    }


def _find_reusable_run(
    data_dir: Path, scope: str, prompt_hash: str, model_label: str, endpoint_label: str,
) -> dict | None:
    """Idempotency: an existing completed run for the same prompt_hash+model+endpoint+scope."""
    for r in list_local_advisor_runs(data_dir):
        if (r.get("scope") == scope and r.get("prompt_hash") == prompt_hash
                and r.get("model_name") == model_label
                and r.get("endpoint_label") == endpoint_label
                and r.get("status") == LocalAdvisorStatus.COMPLETED):
            return r
    return None


def _count_unavailable(data_dir: Path, scope: str, prompt_hash: str) -> int:
    """Anti-loop (Step 1511): how many times the advisor was unavailable for this same
    evidence (prompt_hash). Used to stop re-probing until the evidence changes."""
    return sum(1 for r in list_local_advisor_runs(data_dir)
               if r.get("scope") == scope and r.get("prompt_hash") == prompt_hash
               and r.get("status") == LocalAdvisorStatus.UNAVAILABLE)


# ---------------------------------------------------------------------------
# Invocation (Step 1507) + impact suggestion (Step 1510 advisory side)
# ---------------------------------------------------------------------------


def _suggest_impact(safe: dict[str, Any], findings: list[LocalAdvisorFinding]) -> str:
    """Advisory-only suggested impact. The orchestrator re-derives the BINDING impact
    deterministically (Step 1510) — this is just a hint surfaced in the response."""
    high = any(f.severity == "high" for f in findings) or \
        any(c.get("severity") == "high" for c in safe.get("concerns", []))
    if safe.get("loop_risk") in ("high",) or high:
        return LocalAdvisorDecisionImpact.HUMAN_REVIEW_REQUIRED
    if safe.get("missing_evidence"):
        return LocalAdvisorDecisionImpact.EVIDENCE_INCOMPLETE
    if safe.get("concerns") or safe.get("confidence_hint") == "low":
        return LocalAdvisorDecisionImpact.CONFIDENCE_ADJUSTED
    return LocalAdvisorDecisionImpact.NO_CHANGE


def _response_from_run(run: dict, config: LocalAdvisorConfig) -> LocalAdvisorResponse:
    """Build a safe (reused) response from a stored manifest. No raw content."""
    return LocalAdvisorResponse(
        advisor_run_id=run.get("advisor_run_id", ""), job_id=run.get("job_id", ""),
        decision_id=run.get("decision_id", ""), scope=run.get("scope", "repository"),
        model_name=run.get("model_name", ""), endpoint_label=run.get("endpoint_label", ""),
        enabled=config.enabled, available=True, prompt_hash=run.get("prompt_hash", ""),
        response_hash=run.get("response_hash", ""), status=LocalAdvisorStatus.REUSED,
        stop_reason=LocalAdvisorStopReason.REUSED, decision_impact=run.get("decision_impact", ""),
        duration_ms=int(run.get("duration_ms", 0)), created_at=run.get("created_at", ""),
        summary="Reused a prior advisor run for identical evidence (no new model call).")


def run_local_advisor(
    request: LocalAdvisorRequest, config: LocalAdvisorConfig,
    data_dir: Path | None = None, transport: Transport | None = None, new: bool = False,
) -> LocalAdvisorResponse:
    """Run the local advisor on a SAFE decision/situation summary. Advisory only.

    Degrades safely (status=DISABLED/UNAVAILABLE) instead of raising. One invocation per
    decision unless ``new`` — idempotent by prompt_hash + model + endpoint + scope."""
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    ok, _reason, endpoint_label = _validate_endpoint(config.endpoint)
    model_label = _safe_label(config.model_name)
    resp = LocalAdvisorResponse(
        advisor_run_id=uuid4().hex[:16], job_id=request.job_id, decision_id=request.decision_id,
        scope=request.scope, model_name=model_label, endpoint_label=endpoint_label,
        enabled=config.enabled, created_at=_now())

    if not config.enabled:
        resp.status = LocalAdvisorStatus.DISABLED
        resp.stop_reason = LocalAdvisorStopReason.DISABLED
        resp.summary = "Local advisor disabled; deterministic decision unchanged."
        return resp
    if not ok:
        resp.status = LocalAdvisorStatus.BLOCKED
        resp.stop_reason = LocalAdvisorStopReason.ENDPOINT_BLOCKED
        resp.summary = "Local advisor endpoint rejected (loopback only)."
        return resp

    prompt = build_local_advisor_prompt(request.payload, ddir)
    resp.prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]

    # Idempotency: reuse an identical prior run unless explicitly asked for a new one.
    if not new:
        reusable = _find_reusable_run(ddir, request.scope, resp.prompt_hash,
                                      model_label, endpoint_label)
        if reusable is not None:
            return _response_from_run(reusable, config)

    # Anti-loop (Step 1511): stop re-probing the same evidence after repeated failures.
    if not new and _count_unavailable(ddir, request.scope, resp.prompt_hash) >= MAX_UNAVAILABLE_REPEAT:
        resp.status = LocalAdvisorStatus.UNAVAILABLE
        resp.stop_reason = LocalAdvisorStopReason.UNAVAILABLE
        resp.summary = ("Local advisor repeatedly unavailable for this evidence; suppressed "
                        "until new evidence. Deterministic decision unchanged.")
        return resp

    # Budget (Step 1516): separate local-advisor budget; exhausted blocks the advisor only.
    usage = load_local_advisor_usage(request.scope, ddir)
    if usage["run_count"] >= config.max_runs:
        resp.status = LocalAdvisorStatus.BLOCKED
        resp.stop_reason = LocalAdvisorStopReason.BUDGET_EXHAUSTED
        resp.summary = "Local advisor budget exhausted; deterministic decision unchanged."
        return resp

    tx = transport or _stdlib_transport
    started = time.monotonic()
    raw, gen_stop = _generate(config, prompt, tx)
    resp.duration_ms = int((time.monotonic() - started) * 1000)

    if gen_stop != LocalAdvisorStopReason.OK:
        resp.status = LocalAdvisorStatus.UNAVAILABLE
        resp.stop_reason = gen_stop
        resp.summary = "Local advisor unavailable; deterministic decision unchanged."
        # Persist the unavailable attempt for anti-loop tracking (no raw output).
        _persist(ddir, resp, prompt, "")
        return resp

    resp.available = True
    resp.response_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    safe, findings, status = parse_local_advisor_response(raw)
    resp.status = status
    resp.findings = findings
    if status == LocalAdvisorStatus.UNPARSEABLE:
        resp.stop_reason = LocalAdvisorStopReason.UNPARSEABLE
        resp.summary = "Advisor response unparseable; ignored. Deterministic decision unchanged."
        resp.decision_impact = LocalAdvisorDecisionImpact.NO_CHANGE
        _persist(ddir, resp, prompt, raw)
        return resp

    resp.summary = safe.get("summary", "")
    resp.suggested_concerns = safe.get("concerns", [])
    resp.suggested_alternatives = ([safe["alternative_action"]]
                                   if safe.get("alternative_action") else [])
    resp.missing_evidence_hints = safe.get("missing_evidence", [])
    resp.loop_risk = safe.get("loop_risk", "none")
    resp.confidence_hint = safe.get("confidence_hint", "low")
    resp.stop_reason = LocalAdvisorStopReason.OK
    resp.decision_impact = _suggest_impact(safe, findings)
    _persist(ddir, resp, prompt, raw)
    return resp


def _severity_counts(resp: LocalAdvisorResponse) -> dict[str, int]:
    counts: dict[str, int] = {}
    for sev in [f.severity for f in resp.findings] + \
            [c.get("severity", "") for c in resp.suggested_concerns]:
        if sev:
            counts[sev] = counts.get(sev, 0) + 1
    return counts


def _persist(data_dir: Path, resp: LocalAdvisorResponse, prompt: str, raw: str) -> None:
    run = LocalAdvisorRunRecord(
        advisor_run_id=resp.advisor_run_id, job_id=resp.job_id, decision_id=resp.decision_id,
        scope=resp.scope, model_name=resp.model_name, endpoint_label=resp.endpoint_label,
        prompt_hash=resp.prompt_hash, response_hash=resp.response_hash, status=resp.status,
        stop_reason=resp.stop_reason, decision_impact=resp.decision_impact,
        prompt_chars=len(prompt), response_chars=len(raw), duration_ms=resp.duration_ms,
        finding_severity_counts=_severity_counts(resp), created_at=resp.created_at)
    _store_run(data_dir, run, prompt, raw)


# ---------------------------------------------------------------------------
# Exports (safe — no raw prompt/response)
# ---------------------------------------------------------------------------


def export_local_advisor_response_json(resp: LocalAdvisorResponse) -> dict[str, Any]:
    return {
        "version": 1, "advisor_run_id": resp.advisor_run_id, "job_id": resp.job_id,
        "decision_id": resp.decision_id, "scope": resp.scope, "model_name": resp.model_name,
        "endpoint_label": resp.endpoint_label, "enabled": resp.enabled,
        "available": resp.available, "prompt_hash": resp.prompt_hash,
        "response_hash": resp.response_hash, "status": resp.status,
        "stop_reason": resp.stop_reason, "summary": resp.summary,
        "findings": [f.to_dict() for f in resp.findings],
        "suggested_concerns": resp.suggested_concerns,
        "suggested_alternatives": resp.suggested_alternatives,
        "missing_evidence_hints": resp.missing_evidence_hints,
        "loop_risk": resp.loop_risk, "confidence_hint": resp.confidence_hint,
        "decision_impact": resp.decision_impact, "duration_ms": resp.duration_ms,
        "created_at": resp.created_at,
    }


def export_local_advisor_availability_json(av: LocalAdvisorAvailability) -> dict[str, Any]:
    return av.to_dict()
