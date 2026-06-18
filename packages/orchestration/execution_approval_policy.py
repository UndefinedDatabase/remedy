"""Execution Approval Policy — bounded policy layer for managed execution.

Policy approval creates approval metadata only. It never executes anything.
Manual approval remains the default. Policy approval is an advanced setting.

Hard rules:
  - NO auto-apply / auto-PR / auto-merge / auto-rollback.
  - NO provider SDK calls. NO secrets in policy fields.
  - NO shell=True. NO arbitrary execution.
  - NO raw prompts/output/logs in policy records.
  - Policies are disabled by default.
  - Real provider policies require explicit operator confirmation.
  - Fixture policies exist for deterministic tests.
  - Policy grant creates ExecutionApproval metadata — execution is separate.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_log = logging.getLogger("remedy.approval_policy")

SCHEMA_VERSION = "execution-approval-policy-v0"
_POLICY_DIRNAME = "approval_policies"

_SK_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{6,}\b")
_PATH_PATTERN = re.compile(r"/(home|Users|root|tmp|mnt)/([^/\s]+/)?")
_SECRET_KV_PATTERN = re.compile(
    r'(?i)(key|token|secret|password|api_key|credential)='
    r'(?:"[^"]*"|\'[^\']*\'|[^\s,;)\"\']+)',
)
_PEM_PATTERN = re.compile(r"-----BEGIN\s+[A-Z\s]+-----")

MAX_POLICY_TIMEOUT_SECONDS = 600
MAX_POLICY_OUTPUT_BYTES = 256 * 1024
MAX_POLICY_USES = 1000
MAX_POLICY_TOKEN_ESTIMATE = 500_000


# ---------------------------------------------------------------------------
# Decision codes
# ---------------------------------------------------------------------------


class PolicyDecisionCode:
    ALLOWED = "allowed"
    POLICY_DISABLED = "policy_disabled"
    NO_MATCHING_POLICY = "no_matching_policy"
    ADAPTER_MISMATCH = "adapter_mismatch"
    ADAPTER_KIND_MISMATCH = "adapter_kind_mismatch"
    TEMPLATE_MISMATCH = "template_mismatch"
    TEMPLATE_KIND_MISMATCH = "template_kind_mismatch"
    TASK_TYPE_NOT_ALLOWED = "task_type_not_allowed"
    TIMEOUT_EXCEEDS_POLICY = "timeout_exceeds_policy"
    OUTPUT_CAP_EXCEEDS_POLICY = "output_cap_exceeds_policy"
    TOKEN_ESTIMATE_EXCEEDS_POLICY = "token_estimate_exceeds_policy"
    POLICY_EXPIRED = "policy_expired"
    POLICY_USES_EXHAUSTED = "policy_uses_exhausted"
    REAL_PROVIDER_NOT_ALLOWED = "real_provider_not_allowed"
    FIXTURE_REQUIRED = "fixture_required"
    UNSAFE_TEMPLATE = "unsafe_template"
    MISSING_SESSION = "missing_session"
    MISSING_PACKAGE = "missing_package"
    MISSING_ADAPTER = "missing_adapter"
    MISSING_TEMPLATE = "missing_template"
    MISSING_TASK_TYPE = "missing_task_type"
    TOKEN_ESTIMATE_UNKNOWN = "token_estimate_unknown"
    REAL_PROVIDER_UNCONFIRMED = "real_provider_unconfirmed"


_ALL_DECISION_CODES = frozenset({
    PolicyDecisionCode.ALLOWED,
    PolicyDecisionCode.POLICY_DISABLED,
    PolicyDecisionCode.NO_MATCHING_POLICY,
    PolicyDecisionCode.ADAPTER_MISMATCH,
    PolicyDecisionCode.ADAPTER_KIND_MISMATCH,
    PolicyDecisionCode.TEMPLATE_MISMATCH,
    PolicyDecisionCode.TEMPLATE_KIND_MISMATCH,
    PolicyDecisionCode.TASK_TYPE_NOT_ALLOWED,
    PolicyDecisionCode.TIMEOUT_EXCEEDS_POLICY,
    PolicyDecisionCode.OUTPUT_CAP_EXCEEDS_POLICY,
    PolicyDecisionCode.TOKEN_ESTIMATE_EXCEEDS_POLICY,
    PolicyDecisionCode.POLICY_EXPIRED,
    PolicyDecisionCode.POLICY_USES_EXHAUSTED,
    PolicyDecisionCode.REAL_PROVIDER_NOT_ALLOWED,
    PolicyDecisionCode.FIXTURE_REQUIRED,
    PolicyDecisionCode.UNSAFE_TEMPLATE,
    PolicyDecisionCode.MISSING_SESSION,
    PolicyDecisionCode.MISSING_PACKAGE,
    PolicyDecisionCode.MISSING_ADAPTER,
    PolicyDecisionCode.MISSING_TEMPLATE,
    PolicyDecisionCode.MISSING_TASK_TYPE,
    PolicyDecisionCode.TOKEN_ESTIMATE_UNKNOWN,
    PolicyDecisionCode.REAL_PROVIDER_UNCONFIRMED,
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe(text: str, limit: int = 300) -> str:
    t = str(text or "")[:limit]
    t = _SK_PATTERN.sub("[redacted]", t)
    t = _PATH_PATTERN.sub("[path]/", t)
    t = _SECRET_KV_PATTERN.sub(r"\1=***", t)
    t = _PEM_PATTERN.sub("[redacted-pem]", t)
    return t


def _resolve_ddir(data_dir: Path | None) -> Path:
    if data_dir is not None:
        return Path(data_dir)
    from packages.orchestration.data_paths import resolve_data_root
    return resolve_data_root()


def _policies_dir(ddir: Path) -> Path:
    return ddir / _POLICY_DIRNAME


def _atomic_write(p: Path, data: dict[str, Any]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.parent.exists():
        os.chmod(p.parent, 0o700)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, p)


def _load_json(p: Path) -> dict[str, Any] | None:
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _load_json_dir(d: Path) -> list[dict[str, Any]]:
    if not d.is_dir():
        return []
    out: list[dict[str, Any]] = []
    for f in sorted(d.iterdir()):
        if f.suffix == ".json":
            blob = _load_json(f)
            if blob:
                out.append(blob)
    return out


# ---------------------------------------------------------------------------
# ExecutionApprovalPolicy model (Step 2723)
# ---------------------------------------------------------------------------


@dataclass
class ExecutionApprovalPolicy:
    policy_id: str = ""
    label: str = ""
    enabled: bool = False
    adapter_id: str = ""
    adapter_kind: str = ""
    template_id: str = ""
    template_kind: str = ""
    allowed_task_types: list[str] = field(default_factory=list)
    max_timeout_seconds: int = MAX_POLICY_TIMEOUT_SECONDS
    max_output_bytes: int = MAX_POLICY_OUTPUT_BYTES
    max_estimated_tokens: int = MAX_POLICY_TOKEN_ESTIMATE
    max_uses: int = 0
    uses_consumed: int = 0
    expires_at: str = ""
    requires_fixture_only: bool = False
    allow_real_provider: bool = False
    confirmed_real_provider_at: str = ""
    confirmed_by_operator: str = ""
    real_provider_confirmation_reason: str = ""
    operator_id: str = ""
    reason: str = ""
    created_at: str = ""
    updated_at: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "label": _safe(self.label, 200),
            "enabled": bool(self.enabled),
            "adapter_id": self.adapter_id,
            "adapter_kind": self.adapter_kind,
            "template_id": self.template_id,
            "template_kind": self.template_kind,
            "allowed_task_types": list(self.allowed_task_types)[:20],
            "max_timeout_seconds": min(
                int(self.max_timeout_seconds), MAX_POLICY_TIMEOUT_SECONDS,
            ),
            "max_output_bytes": min(
                int(self.max_output_bytes), MAX_POLICY_OUTPUT_BYTES,
            ),
            "max_estimated_tokens": min(
                int(self.max_estimated_tokens), MAX_POLICY_TOKEN_ESTIMATE,
            ),
            "max_uses": max(0, int(self.max_uses)),
            "uses_consumed": max(0, int(self.uses_consumed)),
            "expires_at": self.expires_at,
            "requires_fixture_only": bool(self.requires_fixture_only),
            "allow_real_provider": bool(self.allow_real_provider),
            "confirmed_real_provider_at": self.confirmed_real_provider_at,
            "confirmed_by_operator": _safe(self.confirmed_by_operator, 100),
            "real_provider_confirmation_reason": _safe(
                self.real_provider_confirmation_reason, 200,
            ),
            "operator_id": _safe(self.operator_id, 100),
            "reason": _safe(self.reason, 500),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "notes": _safe(self.notes, 500),
            "schema_version": SCHEMA_VERSION,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ExecutionApprovalPolicy:
        return cls(
            policy_id=str(d.get("policy_id", "")),
            label=str(d.get("label", "")),
            enabled=bool(d.get("enabled", False)),
            adapter_id=str(d.get("adapter_id", "")),
            adapter_kind=str(d.get("adapter_kind", "")),
            template_id=str(d.get("template_id", "")),
            template_kind=str(d.get("template_kind", "")),
            allowed_task_types=list(d.get("allowed_task_types") or []),
            max_timeout_seconds=min(
                int(d.get("max_timeout_seconds", MAX_POLICY_TIMEOUT_SECONDS)),
                MAX_POLICY_TIMEOUT_SECONDS,
            ),
            max_output_bytes=min(
                int(d.get("max_output_bytes", MAX_POLICY_OUTPUT_BYTES)),
                MAX_POLICY_OUTPUT_BYTES,
            ),
            max_estimated_tokens=min(
                int(d.get("max_estimated_tokens", MAX_POLICY_TOKEN_ESTIMATE)),
                MAX_POLICY_TOKEN_ESTIMATE,
            ),
            max_uses=max(0, int(d.get("max_uses", 0))),
            uses_consumed=max(0, int(d.get("uses_consumed", 0))),
            expires_at=str(d.get("expires_at", "")),
            requires_fixture_only=bool(d.get("requires_fixture_only", False)),
            allow_real_provider=bool(d.get("allow_real_provider", False)),
            confirmed_real_provider_at=str(d.get("confirmed_real_provider_at", "")),
            confirmed_by_operator=str(d.get("confirmed_by_operator", "")),
            real_provider_confirmation_reason=str(d.get("real_provider_confirmation_reason", "")),
            operator_id=str(d.get("operator_id", "")),
            reason=str(d.get("reason", "")),
            created_at=str(d.get("created_at", "")),
            updated_at=str(d.get("updated_at", "")),
            notes=str(d.get("notes", "")),
        )


# ---------------------------------------------------------------------------
# ExecutionApprovalPolicyDecision (Step 2724)
# ---------------------------------------------------------------------------


@dataclass
class ExecutionApprovalPolicyDecision:
    allowed: bool = False
    policy_id: str = ""
    decision_code: str = PolicyDecisionCode.NO_MATCHING_POLICY
    reason: str = ""
    required_manual_approval: bool = True
    matched_adapter_id: str = ""
    matched_template_id: str = ""
    matched_session_id: str = ""
    matched_package_id: str = ""
    limits_applied: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": bool(self.allowed),
            "policy_id": self.policy_id,
            "decision_code": self.decision_code,
            "reason": _safe(self.reason, 500),
            "required_manual_approval": bool(self.required_manual_approval),
            "matched_adapter_id": self.matched_adapter_id,
            "matched_template_id": self.matched_template_id,
            "matched_session_id": self.matched_session_id,
            "matched_package_id": self.matched_package_id,
            "limits_applied": dict(self.limits_applied),
            "warnings": [_safe(w) for w in self.warnings[:10]],
        }


# ---------------------------------------------------------------------------
# Default policies (Step 2727)
# ---------------------------------------------------------------------------


def default_policies() -> list[ExecutionApprovalPolicy]:
    return [
        ExecutionApprovalPolicy(
            policy_id="fixture-echo-v0",
            label="Fixture echo — deterministic test policy",
            enabled=False,
            adapter_id="fixture-v0",
            adapter_kind="fixture_builder",
            template_id="fixture-echo-v0",
            template_kind="fixture_builder",
            allowed_task_types=["repair", "test", "diagnostic"],
            max_timeout_seconds=60,
            max_output_bytes=64 * 1024,
            max_estimated_tokens=10_000,
            max_uses=100,
            requires_fixture_only=True,
            allow_real_provider=False,
            reason="Deterministic fixture for testing only",
            created_at=_now(),
            updated_at=_now(),
        ),
        ExecutionApprovalPolicy(
            policy_id="claude-code-repair-v0",
            label="Claude Code repair — disabled by default",
            enabled=False,
            adapter_id="claude-code-v0",
            adapter_kind="claude_code",
            template_id="claude-code-repair-v0",
            template_kind="claude_code",
            allowed_task_types=["repair"],
            max_timeout_seconds=300,
            max_output_bytes=MAX_POLICY_OUTPUT_BYTES,
            max_estimated_tokens=100_000,
            max_uses=10,
            requires_fixture_only=False,
            allow_real_provider=False,
            reason="Real provider policy — requires explicit operator enablement",
            created_at=_now(),
            updated_at=_now(),
        ),
        ExecutionApprovalPolicy(
            policy_id="generic-cli-v0",
            label="Generic CLI — disabled by default",
            enabled=False,
            adapter_id="generic-cli-v0",
            adapter_kind="generic_external_cli_builder",
            template_id="generic-cli-repair-v0",
            template_kind="generic_external_cli_builder",
            allowed_task_types=["repair"],
            max_timeout_seconds=300,
            max_output_bytes=MAX_POLICY_OUTPUT_BYTES,
            max_estimated_tokens=100_000,
            max_uses=10,
            requires_fixture_only=False,
            allow_real_provider=False,
            reason="Generic CLI policy — requires explicit operator enablement",
            created_at=_now(),
            updated_at=_now(),
        ),
    ]


# ---------------------------------------------------------------------------
# Storage (Step 2728)
# ---------------------------------------------------------------------------


def save_execution_approval_policy(
    policy: ExecutionApprovalPolicy, data_dir: Path | None = None,
) -> bool:
    ddir = _resolve_ddir(data_dir)
    if not policy.policy_id:
        return False
    raw_fields = " ".join([
        policy.label, policy.reason, policy.notes, policy.operator_id,
    ])
    raw_lower = raw_fields.lower()
    for marker in ("sk-", "api_key=", "password=", "secret_key=",
                    "credential=", "token=", "-----begin"):
        if marker in raw_lower:
            _log.warning("Policy %s rejected: contains secret marker", policy.policy_id)
            return False
    for prefix in ("/home/", "/root/", "/Users/", "/mnt/", "/tmp/"):
        if prefix in raw_fields:
            _log.warning("Policy %s rejected: contains private path", policy.policy_id)
            return False
    d = policy.to_dict()
    _atomic_write(_policies_dir(ddir) / f"{policy.policy_id}.json", d)
    return True


def load_execution_approval_policy(
    policy_id: str, data_dir: Path | None = None,
) -> ExecutionApprovalPolicy | None:
    ddir = _resolve_ddir(data_dir)
    d = _load_json(_policies_dir(ddir) / f"{policy_id}.json")
    if not d:
        return None
    return ExecutionApprovalPolicy.from_dict(d)


def list_execution_approval_policies(
    data_dir: Path | None = None,
) -> list[dict[str, Any]]:
    ddir = _resolve_ddir(data_dir)
    stored = _load_json_dir(_policies_dir(ddir))
    if stored:
        return stored
    return [p.to_dict() for p in default_policies()]


# ---------------------------------------------------------------------------
# Integrity scanner (Step 2729)
# ---------------------------------------------------------------------------


def execution_approval_policy_integrity(
    data_dir: Path | None = None,
) -> dict[str, Any]:
    ddir = _resolve_ddir(data_dir)
    policies = list_execution_approval_policies(ddir)
    warnings: list[str] = []
    errors: list[str] = []

    for p in policies:
        pid = p.get("policy_id", "unknown")

        if p.get("allow_real_provider") and p.get("enabled"):
            warnings.append(f"{pid}: real provider policy enabled")
            if not p.get("confirmed_real_provider_at"):
                errors.append(
                    f"{pid}: real provider enabled without confirmation metadata"
                )

        if p.get("requires_fixture_only") and p.get("allow_real_provider"):
            errors.append(f"{pid}: fixture_only + real_provider conflict")

        blob = json.dumps(p).lower()
        for marker in ("sk-", "-----begin", "password=", "secret_key=",
                        "credential=", "token=", "api_key="):
            if marker in blob:
                errors.append(f"{pid}: secret marker in policy data")
                break
        raw = json.dumps(p)
        for prefix in ("/home/", "/root/", "/Users/", "/tmp/", "/mnt/"):
            if prefix in raw:
                errors.append(f"{pid}: private path in policy data")
                break

        mc = int(p.get("max_uses", 0))
        uc = int(p.get("uses_consumed", 0))
        if mc > 0 and uc > mc:
            errors.append(f"{pid}: uses_consumed ({uc}) > max_uses ({mc})")

        if p.get("enabled") and p.get("expires_at"):
            try:
                exp = datetime.fromisoformat(p["expires_at"])
                if datetime.now(timezone.utc) > exp:
                    warnings.append(f"{pid}: enabled but expired")
            except (ValueError, TypeError):
                warnings.append(f"{pid}: invalid expires_at")

        timeout = int(p.get("max_timeout_seconds", 0))
        if timeout > MAX_POLICY_TIMEOUT_SECONDS:
            errors.append(f"{pid}: timeout {timeout} exceeds max {MAX_POLICY_TIMEOUT_SECONDS}")

        output = int(p.get("max_output_bytes", 0))
        if output > MAX_POLICY_OUTPUT_BYTES:
            errors.append(f"{pid}: output cap {output} exceeds max {MAX_POLICY_OUTPUT_BYTES}")

    return {
        "policy_count": len(policies),
        "enabled_count": sum(1 for p in policies if p.get("enabled")),
        "warnings": warnings,
        "errors": errors,
        "healthy": len(errors) == 0,
    }


# ---------------------------------------------------------------------------
# Safe loaders for policy evaluation (Step 2730)
# ---------------------------------------------------------------------------


def _load_session(session_id: str, ddir: Path) -> dict[str, Any] | None:
    try:
        from packages.orchestration.main_builder_adapter import load_builder_session
        session = load_builder_session(session_id, ddir)
        if session is None:
            return None
        if hasattr(session, "to_dict"):
            return session.to_dict()
        return vars(session)
    except (ImportError, Exception):
        return None


def _load_package(package_id: str, ddir: Path, job_id: str = "") -> dict[str, Any] | None:
    """Load BuilderRequestPackage from main_builder_adapter workspace."""
    if not package_id:
        return None
    try:
        # Search within the job workspace for the package.
        if job_id:
            pkg_path = ddir / "workspaces" / job_id / "builder_adapter" / "packages" / f"{package_id}.json"
            blob = _load_json(pkg_path)
            if blob:
                return blob
        # Fall back: scan all workspaces for this package_id.
        ws_root = ddir / "workspaces"
        if ws_root.is_dir():
            for ws in sorted(ws_root.iterdir()):
                pkg_path = ws / "builder_adapter" / "packages" / f"{package_id}.json"
                blob = _load_json(pkg_path)
                if blob:
                    return blob
        return None
    except (OSError, Exception):
        return None


def _load_adapter(adapter_id: str, ddir: Path) -> dict[str, Any] | None:
    try:
        from packages.orchestration.main_builder_adapter import get_builder_adapter_spec
        spec = get_builder_adapter_spec(adapter_id, ddir)
        if spec is None:
            return None
        return spec if isinstance(spec, dict) else spec.to_dict()
    except (ImportError, Exception):
        return None


def _load_template(template_id: str, ddir: Path) -> dict[str, Any] | None:
    try:
        from packages.orchestration.managed_builder_execution import get_command_template
        return get_command_template(template_id, ddir)
    except (ImportError, Exception):
        return None


# ---------------------------------------------------------------------------
# Policy evaluation (Steps 2731-2742)
# ---------------------------------------------------------------------------


def evaluate_execution_approval_policy(
    session_id: str, template_id: str, *,
    data_dir: Path | None = None,
) -> ExecutionApprovalPolicyDecision:
    """Evaluate whether a policy allows approval for this session+template.

    Returns a decision. NEVER creates approval. NEVER executes anything.
    """
    ddir = _resolve_ddir(data_dir)

    decision = ExecutionApprovalPolicyDecision(
        matched_session_id=session_id,
        matched_template_id=template_id,
    )

    template = _load_template(template_id, ddir)
    if not template:
        decision.decision_code = PolicyDecisionCode.MISSING_TEMPLATE
        decision.reason = f"Template {template_id} not found"
        return decision

    if not template.get("enabled", False):
        decision.decision_code = PolicyDecisionCode.UNSAFE_TEMPLATE
        decision.reason = "Template is disabled"
        return decision

    session = _load_session(session_id, ddir)
    if not session:
        decision.decision_code = PolicyDecisionCode.MISSING_SESSION
        decision.reason = f"Session {session_id} not found"
        return decision

    adapter_id = session.get("adapter_id", "")
    package_id = session.get("package_id", "")
    decision.matched_adapter_id = adapter_id
    decision.matched_package_id = package_id

    if not adapter_id:
        decision.decision_code = PolicyDecisionCode.MISSING_ADAPTER
        decision.reason = "Session has no adapter_id"
        return decision

    adapter = _load_adapter(adapter_id, ddir)
    if not adapter:
        decision.decision_code = PolicyDecisionCode.MISSING_ADAPTER
        decision.reason = f"Adapter {adapter_id} not found"
        return decision

    adapter_kind = adapter.get("kind", "")

    policies = list_execution_approval_policies(ddir)
    enabled_policies = [p for p in policies if p.get("enabled", False)]
    if not enabled_policies:
        decision.decision_code = PolicyDecisionCode.NO_MATCHING_POLICY
        decision.reason = "No enabled policies"
        return decision

    job_id = session.get("job_id", "")
    package = None
    task_type = ""
    token_budget: dict[str, Any] = {}
    if package_id:
        package = _load_package(package_id, ddir, job_id=job_id)
        if package:
            task_type = package.get("task_type", "")
            token_budget = package.get("token_budget_summary", {}) or {}

    template_kind = template.get("adapter_kind", "")

    for pol in enabled_policies:
        deny_reason = _evaluate_single_policy(
            pol, session_id, template_id, adapter_id, adapter_kind,
            template_kind, task_type, template, decision,
            package=package, token_budget=token_budget,
        )
        if deny_reason is None:
            decision.allowed = True
            decision.policy_id = pol.get("policy_id", "")
            decision.decision_code = PolicyDecisionCode.ALLOWED
            decision.reason = f"Policy {decision.policy_id} allows approval"
            decision.required_manual_approval = False
            decision.limits_applied = {
                "max_timeout_seconds": min(
                    int(pol.get("max_timeout_seconds", MAX_POLICY_TIMEOUT_SECONDS)),
                    int(template.get("timeout_seconds", MAX_POLICY_TIMEOUT_SECONDS)),
                ),
                "max_output_bytes": min(
                    int(pol.get("max_output_bytes", MAX_POLICY_OUTPUT_BYTES)),
                    int(template.get("max_output_bytes", MAX_POLICY_OUTPUT_BYTES)),
                ),
            }
            return decision

    decision.decision_code = PolicyDecisionCode.NO_MATCHING_POLICY
    decision.reason = "No policy matched all conditions"
    return decision


def _evaluate_single_policy(
    pol: dict[str, Any],
    session_id: str,
    template_id: str,
    adapter_id: str,
    adapter_kind: str,
    template_kind: str,
    task_type: str,
    template: dict[str, Any],
    decision: ExecutionApprovalPolicyDecision,
    *,
    package: dict[str, Any] | None = None,
    token_budget: dict[str, Any] | None = None,
) -> str | None:
    """Check a single policy against all conditions.

    Returns None if allowed, or a denial reason string.
    """
    pid = pol.get("policy_id", "")

    if not pol.get("enabled", False):
        return "policy_disabled"

    # Adapter match
    pol_adapter = pol.get("adapter_id", "")
    if pol_adapter and pol_adapter != adapter_id:
        return "adapter_mismatch"

    pol_adapter_kind = pol.get("adapter_kind", "")
    if pol_adapter_kind and adapter_kind and pol_adapter_kind != adapter_kind:
        return "adapter_kind_mismatch"

    # Template match
    pol_template = pol.get("template_id", "")
    if pol_template and pol_template != template_id:
        return "template_mismatch"

    pol_template_kind = pol.get("template_kind", "")
    if pol_template_kind and template_kind and pol_template_kind != template_kind:
        return "template_kind_mismatch"

    # Task type — deny when policy restricts tasks and task type is missing or wrong
    allowed_tasks = pol.get("allowed_task_types") or []
    if allowed_tasks:
        if not task_type:
            return "missing_task_type"
        if task_type not in allowed_tasks:
            return "task_type_not_allowed"

    # Timeout cap
    pol_timeout = int(pol.get("max_timeout_seconds", MAX_POLICY_TIMEOUT_SECONDS))
    tmpl_timeout = int(template.get("timeout_seconds", 0))
    if pol_timeout > 0 and tmpl_timeout > pol_timeout:
        return "timeout_exceeds_policy"

    # Output cap
    pol_output = int(pol.get("max_output_bytes", MAX_POLICY_OUTPUT_BYTES))
    tmpl_output = int(template.get("max_output_bytes", 0))
    if pol_output > 0 and tmpl_output > pol_output:
        return "output_cap_exceeds_policy"

    # Token estimate — unknown requires manual approval in v0
    pol_tokens = int(pol.get("max_estimated_tokens", MAX_POLICY_TOKEN_ESTIMATE))
    tb = token_budget or {}
    token_band = tb.get("estimated_token_band", "unknown")
    budget_status = tb.get("budget_status", "unknown")

    if pol_tokens > 0:
        decision.limits_applied["max_estimated_tokens"] = pol_tokens
        # Unknown token estimate → require manual approval
        if token_band in ("unknown",) and budget_status in ("unknown",):
            if not pol.get("requires_fixture_only", False):
                return "token_estimate_unknown"
        # Over budget → deny
        if budget_status in ("over_budget", "over"):
            return "token_estimate_exceeds_policy"

    # Expiry
    expires_at = pol.get("expires_at", "")
    if expires_at:
        try:
            exp_dt = datetime.fromisoformat(expires_at)
            if datetime.now(timezone.utc) > exp_dt:
                return "policy_expired"
        except (ValueError, TypeError):
            return "policy_expired"

    # Uses
    max_uses = int(pol.get("max_uses", 0))
    uses_consumed = int(pol.get("uses_consumed", 0))
    if max_uses > 0 and uses_consumed >= max_uses:
        return "policy_uses_exhausted"

    # Real provider allowance — also check confirmation metadata (R-0159)
    is_fixture = pol.get("requires_fixture_only", False)
    if not is_fixture and pol.get("allow_real_provider", False):
        if not pol.get("confirmed_real_provider_at"):
            return "real_provider_unconfirmed"
    if not is_fixture and not pol.get("allow_real_provider", False):
        if adapter_kind and adapter_kind != "fixture_builder":
            return "real_provider_not_allowed"

    # Fixture-only requirement
    if is_fixture:
        if adapter_kind and adapter_kind != "fixture_builder":
            return "fixture_required"
        if template_kind and template_kind != "fixture_builder":
            return "fixture_required"

    # Unsafe template
    if not template.get("enabled", False):
        return "unsafe_template"

    return None


# ---------------------------------------------------------------------------
# Policy grant (Step 2743)
# ---------------------------------------------------------------------------


def create_policy_granted_execution_approval(
    session_id: str, template_id: str, *,
    data_dir: Path | None = None,
) -> dict[str, Any]:
    """Create approval metadata if policy allows. Never executes anything.

    Returns dict with keys: granted, approval_id, decision.
    """
    ddir = _resolve_ddir(data_dir)
    decision = evaluate_execution_approval_policy(
        session_id, template_id, data_dir=ddir,
    )

    result: dict[str, Any] = {
        "granted": False,
        "approval_id": "",
        "decision": decision.to_dict(),
    }

    if not decision.allowed:
        return result

    policy = load_execution_approval_policy(decision.policy_id, ddir)
    if not policy:
        result["decision"]["reason"] = "Policy not found after evaluation"
        return result

    # Pre-check uses (but do NOT decrement yet — R-0161)
    if policy.max_uses > 0:
        if policy.uses_consumed >= policy.max_uses:
            result["decision"]["decision_code"] = PolicyDecisionCode.POLICY_USES_EXHAUSTED
            result["decision"]["reason"] = "Policy uses exhausted during grant"
            result["decision"]["allowed"] = False
            return result

    from datetime import timedelta

    from packages.orchestration.managed_builder_execution import (
        DEFAULT_APPROVAL_EXPIRY_SECONDS,
        approve_managed_execution,
    )

    short_expiry = min(
        DEFAULT_APPROVAL_EXPIRY_SECONDS,
        int(policy.max_timeout_seconds) + 60,
    )
    expires_at = (
        datetime.now(timezone.utc) + timedelta(seconds=short_expiry)
    ).isoformat()

    # Create approval FIRST — bind package_id and policy_id (R-0161)
    approval = approve_managed_execution(
        session_id, template_id,
        operator_id=f"policy:{policy.policy_id}",
        package_id=decision.matched_package_id,
        adapter_id=decision.matched_adapter_id,
        adapter_kind=policy.adapter_kind,
        expires_at=expires_at,
        max_runs=1,
        max_runtime_seconds=decision.limits_applied.get(
            "max_timeout_seconds", policy.max_timeout_seconds,
        ),
        max_output_bytes=decision.limits_applied.get(
            "max_output_bytes", policy.max_output_bytes,
        ),
        data_dir=ddir,
    )

    if not approval:
        result["decision"]["reason"] = "Approval creation failed"
        result["decision"]["allowed"] = False
        return result

    # Decrement uses ONLY after approval exists (R-0161)
    if policy.max_uses > 0:
        policy.uses_consumed += 1
        policy.updated_at = _now()
        save_execution_approval_policy(policy, ddir)

    result["granted"] = True
    result["approval_id"] = approval.approval_id
    result["decision"]["reason"] = (
        f"Policy {policy.policy_id} granted approval {approval.approval_id}"
    )

    # Audit event
    _record_policy_grant_event(
        policy.policy_id, session_id, template_id,
        approval.approval_id, decision.decision_code, ddir,
    )

    return result


def _record_policy_grant_event(
    policy_id: str, session_id: str, template_id: str,
    approval_id: str, decision_code: str, ddir: Path,
) -> None:
    try:
        from packages.orchestration.managed_builder_execution import _append_event
        _append_event(
            execution_id="",
            session_id=session_id,
            job_id="",
            kind="policy_grant",
            summary=f"Policy {_safe(policy_id, 50)} granted approval {approval_id[:12]}",
            metadata={
                "policy_id": policy_id,
                "template_id": template_id,
                "approval_id": approval_id,
                "decision_code": decision_code,
            },
            ddir=ddir,
        )
    except (ImportError, Exception):
        _log.debug("Could not record policy grant event", exc_info=True)


# ---------------------------------------------------------------------------
# Policy summary for review bundle (Step 2751)
# ---------------------------------------------------------------------------


def execution_approval_policy_summary(
    data_dir: Path | None = None,
) -> dict[str, Any]:
    ddir = _resolve_ddir(data_dir)
    policies = list_execution_approval_policies(ddir)
    integrity = execution_approval_policy_integrity(ddir)
    enabled = [p for p in policies if p.get("enabled")]

    # Count grants from event log if available.
    grant_count = 0
    latest_decision_code = ""
    try:
        events_dir = ddir / "execution_events"
        if events_dir.is_dir():
            for f in sorted(events_dir.iterdir(), reverse=True):
                if f.suffix == ".json":
                    blob = _load_json(f)
                    if blob and blob.get("kind") == "policy_grant":
                        grant_count += 1
                        if not latest_decision_code:
                            meta = blob.get("metadata", {})
                            latest_decision_code = meta.get("decision_code", "")
    except (OSError, Exception):
        pass

    return {
        "configured_policy_count": len(policies),
        "enabled_policy_count": len(enabled),
        "policy_ids": [p.get("policy_id", "") for p in policies],
        "enabled_policy_ids": [p.get("policy_id", "") for p in enabled],
        "grant_count": grant_count,
        "latest_decision_code": latest_decision_code,
        "integrity_healthy": integrity.get("healthy", False),
        "integrity_warnings": integrity.get("warnings", []),
        "integrity_errors": integrity.get("errors", []),
        "manual_approval_required": len(enabled) == 0,
        "next_safe_action": (
            "remedy approval policy-list --json"
            if len(enabled) == 0 else
            "remedy approval policy-evaluate <session_id> --template <template_id> --json"
        ),
    }
