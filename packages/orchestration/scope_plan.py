"""Scope Plan — deterministic scope extraction, persistence, and validation.

Given a Markdown task file, deterministically extracts proposed features,
persists a scope plan the user can edit, and validates user decisions
before execution.

No provider calls. No Claude. Pure deterministic parsing.
"""
from __future__ import annotations

import json as _json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

# ---------------------------------------------------------------------------
# Data model (Step 4706)
# ---------------------------------------------------------------------------

@dataclass
class ScopeRisk:
    """A risk note attached to a feature or the whole plan."""
    id: str
    description: str
    severity: str = "medium"  # low, medium, high


@dataclass
class ScopeFeature:
    """One feature extracted from the task file."""
    id: str
    title: str
    description: str = ""
    status: str = "proposed"  # proposed, out_of_scope, future
    default_selected: bool = True
    user_decision: str = "pending"  # pending, approved, denied, deferred, backlog
    risk: ScopeRisk | None = None
    expected_files: list[str] = field(default_factory=list)
    acceptance: str = ""


_VALID_DECISIONS = frozenset({"pending", "approved", "denied", "deferred", "backlog"})


@dataclass
class ScopePlan:
    """A complete scope plan for a task file."""
    plan_id: str = field(default_factory=lambda: uuid4().hex[:16])
    task_sha256: str = ""
    repo_path: str = ""
    task_title: str = ""
    task_input_kind: str = ""
    task_tokens_estimated: int = 0
    features: list[ScopeFeature] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    risks: list[ScopeRisk] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggested_tests: list[str] = field(default_factory=list)
    scope_file: str = ""
    created_at: str = ""


@dataclass
class ScopePlanValidationResult:
    """Result of validating a scope plan file against a task file."""
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    approved_features: list[ScopeFeature] = field(default_factory=list)
    denied_features: list[ScopeFeature] = field(default_factory=list)
    deferred_features: list[ScopeFeature] = field(default_factory=list)
    backlog_features: list[ScopeFeature] = field(default_factory=list)
    pending_features: list[ScopeFeature] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Deterministic parser (Step 4707)
# ---------------------------------------------------------------------------

# Headings/sections that indicate features/tasks
# Matches both `## Features` and `Features:` label style
_FEATURE_HEADINGS = re.compile(
    r"^(?:#{1,3}\s+)?(features?|tasks?|goals?|requirements?|deliverables?|scope)\s*:?\s*$",
    re.IGNORECASE,
)

# Headings that indicate out-of-scope/future
_OUT_OF_SCOPE_HEADINGS = re.compile(
    r"^(?:#{1,3}\s+)?(out\s+of\s+scope|future|do\s+not|don'?t|non[- ]?goals?|excluded?|not\s+in\s+scope)\s*:?\s*$",
    re.IGNORECASE,
)

# Headings that indicate acceptance criteria
_ACCEPTANCE_HEADINGS = re.compile(
    r"^(?:#{1,3}\s+)?(acceptance|criteria|done\s+when|definition\s+of\s+done)\s*:?\s*$",
    re.IGNORECASE,
)

# Headings that indicate constraints
_CONSTRAINT_HEADINGS = re.compile(
    r"^(?:#{1,3}\s+)?(constraints?|rules?|limitations?|guardrails?)\s*:?\s*$",
    re.IGNORECASE,
)

# Headings that indicate suggested tests
_TEST_HEADINGS = re.compile(
    r"^(?:#{1,3}\s+)?(tests?|test\s+plan|testing|verification)\s*:?\s*$",
    re.IGNORECASE,
)

# Future/out-of-scope markers in text
_FUTURE_MARKERS = re.compile(
    r"\b(FUTURE|DO\s+NOT\s+IMPLEMENT|OUT\s+OF\s+SCOPE|NOT\s+NOW|LATER|DEFERRED)\b",
    re.IGNORECASE,
)


# Pattern that matches any known section label (heading or bare label)
_ANY_SECTION = re.compile(
    r"^(?:#{1,3}\s+)?"
    r"(features?|tasks?|goals?|requirements?|deliverables?|scope"
    r"|out\s+of\s+scope|future|do\s+not|don'?t|non[- ]?goals?|excluded?|not\s+in\s+scope"
    r"|acceptance|criteria|done\s+when|definition\s+of\s+done"
    r"|constraints?|rules?|limitations?|guardrails?"
    r"|tests?|test\s+plan|testing|verification"
    r")\s*:?\s*$",
    re.IGNORECASE,
)


def _extract_bullet_items(lines: list[str], start: int) -> list[str]:
    """Extract bullet items starting from a line index until next section or end."""
    items: list[str] = []
    for i in range(start, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith("#"):
            break
        # Stop at next bare section label
        if i > start and _ANY_SECTION.match(stripped):
            break
        if stripped.startswith(("- ", "* ", "• ")):
            items.append(stripped[2:].strip())
        elif stripped.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            # Numbered list
            text = re.sub(r"^\d+\.\s*", "", stripped)
            if text:
                items.append(text)
    return items


def _has_future_marker(text: str) -> bool:
    """Check if text contains future/out-of-scope markers."""
    return bool(_FUTURE_MARKERS.search(text))


def extract_scope_plan(
    task_text: str,
    *,
    task_sha256: str = "",
    repo_path: str = "",
    task_title: str = "",
    task_input_kind: str = "",
    task_tokens_estimated: int = 0,
) -> ScopePlan:
    """Deterministically extract a scope plan from Markdown task text.

    No provider calls. No inference. Pure text parsing.
    """
    plan = ScopePlan(
        task_sha256=task_sha256,
        repo_path=str(Path(repo_path).resolve()) if repo_path else "",
        task_title=task_title,
        task_input_kind=task_input_kind,
        task_tokens_estimated=task_tokens_estimated,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    lines = task_text.splitlines()
    feature_items: list[str] = []
    out_of_scope_items: list[str] = []
    acceptance_items: list[str] = []
    constraint_items: list[str] = []
    test_items: list[str] = []

    # Parse sections
    for i, line in enumerate(lines):
        stripped = line.strip()
        if _FEATURE_HEADINGS.match(stripped):
            feature_items.extend(_extract_bullet_items(lines, i + 1))
        elif _OUT_OF_SCOPE_HEADINGS.match(stripped):
            out_of_scope_items.extend(_extract_bullet_items(lines, i + 1))
        elif _ACCEPTANCE_HEADINGS.match(stripped):
            acceptance_items.extend(_extract_bullet_items(lines, i + 1))
        elif _CONSTRAINT_HEADINGS.match(stripped):
            constraint_items.extend(_extract_bullet_items(lines, i + 1))
        elif _TEST_HEADINGS.match(stripped):
            test_items.extend(_extract_bullet_items(lines, i + 1))

    # Create features from feature section
    fid = 0
    for item in feature_items:
        fid += 1
        has_future = _has_future_marker(item)
        risk = None
        if has_future:
            risk = ScopeRisk(
                id=f"R{fid:03d}",
                description=f"Marked as future/out-of-scope in task text: {item[:80]}",
                severity="medium",
            )
        plan.features.append(ScopeFeature(
            id=f"F{fid:03d}",
            title=item[:120],
            description=item,
            status="future" if has_future else "proposed",
            default_selected=not has_future,
            user_decision="pending",
            risk=risk,
        ))

    # Create features from out-of-scope items (proposed with pending, risk note)
    for item in out_of_scope_items:
        fid += 1
        plan.features.append(ScopeFeature(
            id=f"F{fid:03d}",
            title=item[:120],
            description=item,
            status="out_of_scope",
            default_selected=False,
            user_decision="pending",
            risk=ScopeRisk(
                id=f"R{fid:03d}",
                description=f"Listed under out-of-scope in task: {item[:80]}",
                severity="low",
            ),
        ))
        plan.out_of_scope.append(item)

    # Acceptance criteria
    if acceptance_items:
        # Attach to all proposed features
        acceptance_text = "; ".join(acceptance_items)
        for feat in plan.features:
            if feat.status == "proposed":
                feat.acceptance = acceptance_text

    # Constraints as risks
    for item in constraint_items:
        plan.risks.append(ScopeRisk(
            id=f"RC{len(plan.risks) + 1:03d}",
            description=item,
            severity="low",
        ))

    # Suggested tests
    plan.suggested_tests = test_items

    # If no features were extracted, create one from the title
    if not plan.features:
        plan.warnings.append(
            "Task has no structured feature/task sections. "
            "Created one proposed feature from title. "
            "Consider adding '## Features' or '## Tasks' section."
        )
        plan.features.append(ScopeFeature(
            id="F001",
            title=task_title or "Unnamed task",
            description=task_text[:500],
            status="proposed",
            default_selected=True,
            user_decision="pending",
        ))

    return plan


# ---------------------------------------------------------------------------
# Persistence (Step 4708, 4710)
# ---------------------------------------------------------------------------

def _scope_plans_dir() -> Path:
    """Return scope plans storage directory."""
    from packages.orchestration.data_paths import resolve_data_root
    return resolve_data_root() / "scope_plans"


def _feature_to_dict(f: ScopeFeature) -> dict[str, Any]:
    """Serialize a ScopeFeature to dict."""
    d: dict[str, Any] = {
        "id": f.id,
        "title": f.title,
        "description": f.description,
        "status": f.status,
        "default_selected": f.default_selected,
        "user_decision": f.user_decision,
        "expected_files": f.expected_files,
        "acceptance": f.acceptance,
    }
    if f.risk:
        d["risk"] = {
            "id": f.risk.id,
            "description": f.risk.description,
            "severity": f.risk.severity,
        }
    return d


def _risk_to_dict(r: ScopeRisk) -> dict[str, Any]:
    return {"id": r.id, "description": r.description, "severity": r.severity}


def export_scope_plan(plan: ScopePlan) -> dict[str, Any]:
    """Export scope plan to JSON-serializable dict."""
    return {
        "plan_id": plan.plan_id,
        "task_sha256": plan.task_sha256,
        "repo_path": plan.repo_path,
        "task_title": plan.task_title,
        "task_input_kind": plan.task_input_kind,
        "task_tokens_estimated": plan.task_tokens_estimated,
        "features": [_feature_to_dict(f) for f in plan.features],
        "out_of_scope": plan.out_of_scope,
        "risks": [_risk_to_dict(r) for r in plan.risks],
        "warnings": plan.warnings,
        "suggested_tests": plan.suggested_tests,
        "scope_file": plan.scope_file,
        "created_at": plan.created_at,
    }


def persist_scope_plan(plan: ScopePlan) -> Path:
    """Persist scope plan as editable JSON. Returns path to scope file."""
    plan_dir = _scope_plans_dir() / plan.plan_id
    plan_dir.mkdir(parents=True, exist_ok=True)
    scope_file = plan_dir / "scope_plan.json"
    data = export_scope_plan(plan)
    data["scope_file"] = str(scope_file)
    plan.scope_file = str(scope_file)
    scope_file.write_text(_json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return scope_file


def load_scope_plan(path: str) -> dict[str, Any]:
    """Load a scope plan JSON file. Raises ValueError on problems."""
    p = Path(path)
    if not p.exists():
        raise ValueError(f"Scope file not found: {path}")
    try:
        data = _json.loads(p.read_text(encoding="utf-8"))
    except (_json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"Invalid scope file: {exc}")
    return data


# ---------------------------------------------------------------------------
# Validation (Step 4711)
# ---------------------------------------------------------------------------

def validate_scope_plan(
    scope_data: dict[str, Any],
    *,
    task_sha256: str = "",
    repo_path: str = "",
) -> ScopePlanValidationResult:
    """Validate a scope plan file against task and repo constraints.

    Returns validation result with categorized features.
    """
    result = ScopePlanValidationResult()

    # Check task hash match
    plan_hash = scope_data.get("task_sha256", "")
    if task_sha256 and plan_hash and plan_hash != task_sha256:
        result.valid = False
        result.errors.append(
            f"Task hash mismatch: scope plan has {plan_hash[:12]}..., "
            f"task file has {task_sha256[:12]}... — regenerate scope plan."
        )

    # Check repo path match
    plan_repo = scope_data.get("repo_path", "")
    if repo_path and plan_repo:
        resolved_repo = str(Path(repo_path).resolve())
        if plan_repo != resolved_repo:
            result.valid = False
            result.errors.append(
                f"Repo mismatch: scope plan targets {plan_repo}, "
                f"but --repo resolves to {resolved_repo}."
            )

    features = scope_data.get("features", [])
    if not features:
        result.valid = False
        result.errors.append("Scope plan has no features.")
        return result

    # Check for duplicate IDs
    seen_ids: set[str] = set()
    for feat in features:
        fid = feat.get("id", "")
        if not fid:
            result.valid = False
            result.errors.append("Feature missing 'id' field.")
            continue
        if fid in seen_ids:
            result.valid = False
            result.errors.append(f"Duplicate feature ID: {fid}")
        seen_ids.add(fid)

    # Categorize by decision
    for feat in features:
        decision = feat.get("user_decision", "pending")
        if decision not in _VALID_DECISIONS:
            result.valid = False
            result.errors.append(
                f"Invalid decision '{decision}' for feature {feat.get('id', '?')}. "
                f"Allowed: {', '.join(sorted(_VALID_DECISIONS))}."
            )
            continue

        sf = ScopeFeature(
            id=feat.get("id", ""),
            title=feat.get("title", ""),
            description=feat.get("description", ""),
            status=feat.get("status", "proposed"),
            default_selected=feat.get("default_selected", True),
            user_decision=decision,
            expected_files=feat.get("expected_files", []),
            acceptance=feat.get("acceptance", ""),
        )

        if decision == "approved":
            result.approved_features.append(sf)
        elif decision == "denied":
            result.denied_features.append(sf)
        elif decision == "deferred":
            result.deferred_features.append(sf)
        elif decision == "backlog":
            result.backlog_features.append(sf)
        else:
            result.pending_features.append(sf)

    # Must have at least one approved feature
    if not result.approved_features:
        result.valid = False
        result.errors.append(
            "No features approved. At least one feature must have "
            "user_decision='approved' before execution."
        )

    return result


# ---------------------------------------------------------------------------
# Out-of-scope detection helper (Step 4715)
# ---------------------------------------------------------------------------

def check_scope_hints(
    changed_files: list[str],
    safe_diff: str,
    *,
    approved_features: list[ScopeFeature],
    denied_features: list[ScopeFeature],
    deferred_features: list[ScopeFeature],
    backlog_features: list[ScopeFeature],
) -> list[str]:
    """Conservative deterministic out-of-scope detection.

    Returns list of hint strings. Never claims perfect enforcement.
    No provider calls.
    """
    hints: list[str] = []

    # Check expected files — flag files not expected by any approved feature
    all_expected: set[str] = set()
    for feat in approved_features:
        all_expected.update(feat.expected_files)

    if all_expected:
        for f in changed_files:
            if f not in all_expected:
                hints.append(f"Changed file '{f}' not in expected_files of any approved feature.")

    # Check diff for denied/deferred/backlog feature titles
    out_of_scope = denied_features + deferred_features + backlog_features
    diff_lower = safe_diff.lower()
    for feat in out_of_scope:
        title_lower = feat.title.lower()
        # Only flag if title is specific enough (> 5 chars)
        if len(title_lower) > 5 and title_lower in diff_lower:
            hints.append(
                f"Diff may contain work related to out-of-scope feature "
                f"{feat.id} ('{feat.title[:60]}', decision: {feat.user_decision})."
            )

    return hints


# ---------------------------------------------------------------------------
# Builder/Reviewer scope contract text (Steps 4713-4714)
# ---------------------------------------------------------------------------

def build_scope_contract_for_builder(
    validation: ScopePlanValidationResult,
) -> str:
    """Build the scope contract section for Builder prompt."""
    lines = ["## APPROVED SCOPE FOR THIS RUN"]
    for f in validation.approved_features:
        lines.append(f"- {f.id}: {f.title}")

    lines.append("")
    lines.append("## OUT OF SCOPE FOR THIS RUN")
    for f in validation.denied_features:
        lines.append(f"- {f.id} denied by user: {f.title}")
    for f in validation.deferred_features:
        lines.append(f"- {f.id} deferred by user: {f.title}")
    for f in validation.pending_features:
        lines.append(f"- {f.id} pending (not approved): {f.title}")
    for f in validation.backlog_features:
        lines.append(f"- {f.id} backlog: {f.title}")

    if not (validation.denied_features or validation.deferred_features
            or validation.pending_features or validation.backlog_features):
        lines.append("- (none)")

    lines.append("")
    lines.append(
        "You must implement only approved scope. "
        "Do not implement denied, deferred, pending, or backlog items. "
        "If the task body asks for more, ignore those parts for this run."
    )
    return "\n".join(lines)


def build_scope_contract_for_reviewer(
    validation: ScopePlanValidationResult,
    *,
    staged_files: list[str] | None = None,
    safe_diff: str = "",
    test_result: str = "",
    task_title: str = "",
    task_sha256: str = "",
    task_excerpt: str = "",
) -> str:
    """Build the scope contract section for Reviewer prompt."""
    lines = ["## Scope Contract for Review"]
    lines.append("")
    lines.append("### Approved Features (must be implemented)")
    for f in validation.approved_features:
        lines.append(f"- {f.id}: {f.title}")

    lines.append("")
    lines.append("### Out of Scope (must NOT be implemented)")
    for f in validation.denied_features:
        lines.append(f"- {f.id} denied: {f.title}")
    for f in validation.deferred_features:
        lines.append(f"- {f.id} deferred: {f.title}")
    for f in validation.backlog_features:
        lines.append(f"- {f.id} backlog: {f.title}")
    for f in validation.pending_features:
        lines.append(f"- {f.id} pending: {f.title}")

    lines.append("")
    lines.append("### Review Rules")
    lines.append("- FAIL or request repair if out-of-scope features appear in the diff.")
    lines.append("- FAIL or request repair if an approved feature is clearly missing.")
    lines.append("- FAIL if unexpected files are changed that no approved feature covers.")
    lines.append("- FAIL if tests failed.")
    lines.append("- FAIL if Builder claims are not backed by evidence in the diff.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Scope data for reports (Step 4716)
# ---------------------------------------------------------------------------

def build_scope_report_data(
    scope_data: dict[str, Any],
    validation: ScopePlanValidationResult,
    *,
    scope_hints: list[str] | None = None,
) -> dict[str, Any]:
    """Build scope data for JSON report."""
    return {
        "plan_id": scope_data.get("plan_id", ""),
        "task_sha256": scope_data.get("task_sha256", ""),
        "scope_source": "scope-file",
        "scope_approved": validation.valid and bool(validation.approved_features),
        "approved_features": [
            {"id": f.id, "title": f.title} for f in validation.approved_features
        ],
        "denied_features": [
            {"id": f.id, "title": f.title} for f in validation.denied_features
        ],
        "deferred_features": [
            {"id": f.id, "title": f.title} for f in validation.deferred_features
        ],
        "backlog_features": [
            {"id": f.id, "title": f.title} for f in validation.backlog_features
        ],
        "pending_features": [
            {"id": f.id, "title": f.title} for f in validation.pending_features
        ],
        "warnings": scope_data.get("warnings", []),
        "scope_review_hints": scope_hints or [],
    }
