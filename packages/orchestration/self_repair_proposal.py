"""
Self-Repair Proposal v0 (Steps 2446-2505).

Turns run replay analysis into a safe, bounded self-repair proposal that a human
operator can approve, deny, or edit before it becomes a Worker prompt.

  Replay evidence in → safe proposal draft out → operator decides → prompt text only.

This module is METADATA + EVALUATION only. It NEVER calls a provider/model/cloud/
local model, the network, a browser, a subprocess, or a shell; it never executes
a worker, runs a test, applies/approves a patch, or automates git/PR. It builds
no internal MemPalace memory / embeddings / vector DB.

Honesty rules:
  - A proposal is never approved from builder self-report alone.
  - Evidence refs only — no raw logs, prompts, transcripts, candidates, secrets, paths.
  - Denied proposals cannot convert to worker prompts.
  - Edited proposals return to awaiting_operator status.
  - Conversion produces prompt text only, not execution.

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
from uuid import uuid4

from packages.orchestration.provider_trust import _scrub_public

SCHEMA_VERSION = "self-repair-proposal-v0"
_SRP_DIRNAME = "self_repair_proposals"
_MAX_SUMMARY = 300
_MAX_PROMPT_LENGTH = 8000
_MAX_SUSPECTED_FILES = 20
_MAX_EVIDENCE_REFS = 30

_RAW_MARKERS = (
    "diff --git", "-----BEGIN", "Traceback (most recent call last)",
    "sk-ant", "sk-proj", "api_key", "password", "secret_key",
)

_ABS_PATH_RE = re.compile(r"(?<![:/])/(?:home|Users|tmp|var|etc)/\S+")

_SECRET_RE = re.compile(
    r"(?i)"
    r"(?:sk-ant-[A-Za-z0-9_-]+|sk-proj-[A-Za-z0-9_-]+"
    r"|(?:api_key|password|secret_key|token|credential)\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s,;'\"]*)"
    r"|-----BEGIN\s+[A-Z ]+-----[\s\S]*?-----END\s+[A-Z ]+-----)",
)


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------


class SelfRepairProposalStatus:
    DRAFT = "draft"
    AWAITING_OPERATOR = "awaiting_operator"
    APPROVED = "approved"
    DENIED = "denied"
    EDITED = "edited"
    CONVERTED_TO_WORKER_PROMPT = "converted_to_worker_prompt"
    BLOCKED = "blocked"


_ALL_STATUSES = frozenset({
    SelfRepairProposalStatus.DRAFT,
    SelfRepairProposalStatus.AWAITING_OPERATOR,
    SelfRepairProposalStatus.APPROVED,
    SelfRepairProposalStatus.DENIED,
    SelfRepairProposalStatus.EDITED,
    SelfRepairProposalStatus.CONVERTED_TO_WORKER_PROMPT,
    SelfRepairProposalStatus.BLOCKED,
})

_TERMINAL_STATUSES = frozenset({
    SelfRepairProposalStatus.DENIED,
    SelfRepairProposalStatus.CONVERTED_TO_WORKER_PROMPT,
})

_APPROVABLE_STATUSES = frozenset({
    SelfRepairProposalStatus.AWAITING_OPERATOR,
    SelfRepairProposalStatus.EDITED,
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe(text: Any, limit: int = _MAX_SUMMARY) -> str:
    return _scrub_public(str(text or ""))[:limit]


def _scrub_secret_markers(text: str) -> str:
    """Remove secret-like patterns from text for public export."""
    return _SECRET_RE.sub("<secret-redacted>", text)


def _sanitize_prompt(text: str) -> str:
    """Redact paths and secrets from prompt text for public export."""
    return _scrub_secret_markers(_redact_abs_paths(text))


def _redact_abs_paths(text: str) -> str:
    home = os.path.expanduser("~")
    def _repl(m: re.Match[str]) -> str:
        p = m.group(0)
        if p.startswith(home):
            return "~/..." + p[len(home):][-30:]
        return "<path-redacted>"
    return _ABS_PATH_RE.sub(_repl, text)


def _resolve_ddir(data_dir: Path | None) -> Path:
    from packages.orchestration.data_paths import resolve_data_root
    return Path(data_dir) if data_dir is not None else resolve_data_root()


def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(data)
        try:
            os.chmod(tmp, mode)
        except OSError:
            pass
        os.replace(tmp, path)
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


def _proposals_dir(data_dir: Path) -> Path:
    return data_dir / _SRP_DIRNAME


def _proposal_path(proposal_id: str, data_dir: Path) -> Path:
    return _proposals_dir(data_dir) / f"{proposal_id}.json"


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


@dataclass
class SelfRepairProposal:
    proposal_id: str = ""
    run_id: str = ""
    source_replay_id: str = ""
    status: str = SelfRepairProposalStatus.DRAFT
    title: str = ""
    problem_summary: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    suspected_files: list[str] = field(default_factory=list)
    suggested_worker_prompt: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)
    forbidden_actions: list[str] = field(default_factory=list)
    risk_summary: str = ""
    operator_decision: str = ""
    operator_notes: str = ""
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "run_id": self.run_id,
            "source_replay_id": self.source_replay_id,
            "status": self.status,
            "title": _safe(self.title),
            "problem_summary": _safe(self.problem_summary),
            "evidence_refs": list(self.evidence_refs[:_MAX_EVIDENCE_REFS]),
            "suspected_files": list(self.suspected_files[:_MAX_SUSPECTED_FILES]),
            "suggested_worker_prompt": _sanitize_prompt(
                self.suggested_worker_prompt[:_MAX_PROMPT_LENGTH]
            ),
            "acceptance_criteria": [_safe(c) for c in self.acceptance_criteria],
            "required_tests": [_safe(t) for t in self.required_tests],
            "forbidden_actions": [_safe(a) for a in self.forbidden_actions],
            "risk_summary": _safe(_scrub_secret_markers(self.risk_summary)),
            "operator_decision": self.operator_decision,
            "operator_notes": _safe(_scrub_secret_markers(self.operator_notes)),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "schema_version": SCHEMA_VERSION,
        }


def _proposal_from_dict(d: dict[str, Any]) -> SelfRepairProposal:
    return SelfRepairProposal(
        proposal_id=str(d.get("proposal_id", "")),
        run_id=str(d.get("run_id", "")),
        source_replay_id=str(d.get("source_replay_id", "")),
        status=str(d.get("status", SelfRepairProposalStatus.DRAFT)),
        title=str(d.get("title", "")),
        problem_summary=str(d.get("problem_summary", "")),
        evidence_refs=list(d.get("evidence_refs", [])),
        suspected_files=list(d.get("suspected_files", [])),
        suggested_worker_prompt=str(d.get("suggested_worker_prompt", "")),
        acceptance_criteria=list(d.get("acceptance_criteria", [])),
        required_tests=list(d.get("required_tests", [])),
        forbidden_actions=list(d.get("forbidden_actions", [])),
        risk_summary=str(d.get("risk_summary", "")),
        operator_decision=str(d.get("operator_decision", "")),
        operator_notes=str(d.get("operator_notes", "")),
        created_at=str(d.get("created_at", "")),
        updated_at=str(d.get("updated_at", "")),
    )


# ---------------------------------------------------------------------------
# Storage (Phase 5)
# ---------------------------------------------------------------------------


def save_self_repair_proposal(
    proposal: SelfRepairProposal, *, data_dir: Path | None = None,
) -> bool:
    ddir = _resolve_ddir(data_dir)
    proposal.updated_at = _now()
    return _atomic_write(
        _proposal_path(proposal.proposal_id, ddir),
        json.dumps(proposal.to_dict(), indent=2).encode("utf-8"),
    )


def load_self_repair_proposal(
    proposal_id: str, *, data_dir: Path | None = None,
) -> SelfRepairProposal | None:
    ddir = _resolve_ddir(data_dir)
    d = _load_json(_proposal_path(proposal_id, ddir))
    if d is None:
        return None
    return _proposal_from_dict(d)


def list_self_repair_proposals(
    *, run_id: str | None = None, status: str | None = None,
    data_dir: Path | None = None,
) -> list[dict[str, Any]]:
    ddir = _resolve_ddir(data_dir)
    pdir = _proposals_dir(ddir)
    out: list[dict[str, Any]] = []
    try:
        for f in sorted(pdir.iterdir()):
            if not f.is_file() or f.suffix != ".json":
                continue
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if run_id and d.get("run_id") != run_id:
                continue
            if status and d.get("status") != status:
                continue
            out.append(d)
    except OSError:
        pass
    out.sort(key=lambda p: p.get("created_at", ""))
    return out


# ---------------------------------------------------------------------------
# Proposal generation from replay (Phase 3)
# ---------------------------------------------------------------------------


def _gather_replay_signals(run_id: str, data_dir: Path) -> dict[str, Any]:
    """Gather safe signals from replay analysis, review bundle, config, and integrity."""
    signals: dict[str, Any] = {
        "blocking_reasons": [],
        "anomalies": [],
        "integrity_failures": [],
        "degraded_sections": [],
        "config_warnings": [],
        "managed_execution_failures": [],
        "repeated_test_failures": False,
        "missing_proof_evidence": False,
        "signal_collection_warnings": [],
        "signal_collection_errors": [],
    }

    # Replay analysis signals.
    try:
        from packages.orchestration.dogfood_run import (
            analyze_dogfood_run_replay,
            list_dogfood_runs,
        )
        runs = list_dogfood_runs(data_dir=data_dir)
        target_run = None
        for r in runs:
            if r.get("run_id") == run_id:
                target_run = r
                break
        if target_run:
            job_id = target_run.get("job_id", "")
            replay = analyze_dogfood_run_replay(run_id, job_id, data_dir=data_dir)
            signals["blocking_reasons"] = list(set(
                reason
                for ep in replay.blocking_episodes
                for reason in ep.reasons
            ))
            signals["anomalies"] = list(replay.anomalies)
        else:
            signals["signal_collection_warnings"].append(
                f"replay: run {run_id} not found in dogfood runs"
            )
    except ImportError:
        signals["signal_collection_warnings"].append("replay: dogfood_run module not available")
    except Exception as exc:
        signals["signal_collection_errors"].append(
            f"replay: {type(exc).__name__}: {_safe(str(exc), 120)}"
        )

    # Integrity check signals.
    try:
        from packages.orchestration.dogfood_run import dogfood_run_integrity
        integrity = dogfood_run_integrity(data_dir=data_dir)
        if not integrity.get("passed", True):
            signals["integrity_failures"] = [
                {"code": c.get("code", ""), "run_id": c.get("run_id", "")}
                for c in integrity.get("checks", [])
            ]
    except ImportError:
        signals["signal_collection_warnings"].append("integrity: dogfood_run module not available")
    except Exception as exc:
        signals["signal_collection_errors"].append(
            f"integrity: {type(exc).__name__}: {_safe(str(exc), 120)}"
        )

    # Config diagnostic signals.
    try:
        from packages.orchestration.config import get_config
        cfg = get_config()
        if cfg.load_report and cfg.load_report.warnings:
            signals["config_warnings"] = list(cfg.load_report.warnings)
    except ImportError:
        signals["signal_collection_warnings"].append("config: config module not available")
    except Exception as exc:
        signals["signal_collection_errors"].append(
            f"config: {type(exc).__name__}: {_safe(str(exc), 120)}"
        )

    return signals


def create_self_repair_proposal_from_replay(
    run_id: str, *, data_dir: Path | None = None,
) -> SelfRepairProposal:
    """Create a self-repair proposal from replay analysis of a dogfood run.

    If no suspected internal issue is found, creates a blocked proposal with
    a reason explaining why no repair is needed.
    """
    ddir = _resolve_ddir(data_dir)
    signals = _gather_replay_signals(run_id, ddir)

    proposal = SelfRepairProposal(
        proposal_id=f"srp-{uuid4().hex[:12]}",
        run_id=run_id,
        source_replay_id=run_id,
        created_at=_now(),
    )

    # R-0137: Signal collection errors → blocked proposal with diagnostic reason.
    if signals.get("signal_collection_errors"):
        proposal.status = SelfRepairProposalStatus.BLOCKED
        proposal.title = "Signal collection failed"
        proposal.problem_summary = (
            f"Replay signal collection for run {run_id} encountered errors. "
            "Cannot reliably assess internal issues."
        )
        proposal.risk_summary = "; ".join(
            signals["signal_collection_errors"]
        )[:_MAX_SUMMARY]
        save_self_repair_proposal(proposal, data_dir=ddir)
        return proposal

    issues: list[dict[str, str]] = []
    evidence_refs: list[str] = []
    suspected_files: set[str] = set()
    acceptance_criteria: list[str] = []
    required_tests: list[str] = []

    # Blocking reasons → suspected Remedy bugs.
    for reason in signals.get("blocking_reasons", []):
        issues.append({"type": "blocking", "detail": reason})

    # Anomalies → potential issues.
    for anomaly in signals.get("anomalies", []):
        if anomaly.startswith("lane_never_activated:"):
            lane = anomaly.split(":", 1)[1]
            issues.append({"type": "anomaly", "detail": f"Lane {lane} never activated"})
        elif anomaly in ("approaching_step_budget", "approaching_token_budget"):
            issues.append({"type": "budget_warning", "detail": anomaly})

    if signals.get("blocking_reasons") or signals.get("anomalies"):
        evidence_refs.append(f"replay:{run_id}")

    # Integrity failures.
    for failure in signals.get("integrity_failures", []):
        code = failure.get("code", "unknown")
        issues.append({"type": "integrity", "detail": code})
        evidence_refs.append(f"integrity:{code}")
        if code in ("step_count_mismatch", "terminal_missing_finished_at",
                     "guardrail_exceeded_without_terminal_status"):
            suspected_files.add("packages/orchestration/dogfood_run.py")
        if code == "replay_raw_data_leak":
            suspected_files.add("packages/orchestration/dogfood_run.py")
            acceptance_criteria.append("Replay export must not contain raw markers")

    # Degraded review bundle sections.
    for section in signals.get("degraded_sections", []):
        issues.append({"type": "degraded_section", "detail": section})
        evidence_refs.append(f"review_bundle:{section}")
        suspected_files.add("packages/orchestration/review_bundle.py")

    # Config diagnostic warnings.
    for warning in signals.get("config_warnings", []):
        safe_warning = _redact_abs_paths(_safe(warning))
        issues.append({"type": "config_diagnostic", "detail": safe_warning})
        evidence_refs.append(f"config:{safe_warning[:80]}")
        suspected_files.add("packages/orchestration/config.py")

    # No issues found → blocked proposal.
    if not issues:
        proposal.status = SelfRepairProposalStatus.BLOCKED
        proposal.title = "No suspected internal issues found"
        proposal.problem_summary = (
            f"Replay analysis of run {run_id} found no suspected internal "
            "Remedy issues. No repair is needed."
        )
        proposal.risk_summary = "None — no issues detected."
        save_self_repair_proposal(proposal, data_dir=ddir)
        return proposal

    # Build the proposal from discovered issues.
    proposal.status = SelfRepairProposalStatus.AWAITING_OPERATOR
    proposal.title = f"Self-repair: {len(issues)} suspected issue(s) in run {run_id[:12]}"
    proposal.evidence_refs = list(dict.fromkeys(evidence_refs))[:_MAX_EVIDENCE_REFS]
    proposal.suspected_files = sorted(suspected_files)[:_MAX_SUSPECTED_FILES]

    # Problem summary.
    summary_parts = []
    by_type: dict[str, int] = {}
    for issue in issues:
        by_type[issue["type"]] = by_type.get(issue["type"], 0) + 1
    for itype, count in by_type.items():
        summary_parts.append(f"{count} {itype} issue(s)")
    proposal.problem_summary = (
        f"Run {run_id[:12]} has {', '.join(summary_parts)}. "
        "See evidence_refs for details."
    )

    # Suggested worker prompt.
    prompt_lines = [
        f"# Self-Repair Worker Prompt (from proposal {proposal.proposal_id})",
        "",
        "## Problem",
        proposal.problem_summary,
        "",
        "## Evidence",
    ]
    for ref in proposal.evidence_refs[:10]:
        prompt_lines.append(f"- {ref}")
    prompt_lines.extend([
        "",
        "## Suspected files",
    ])
    for f in proposal.suspected_files[:10]:
        prompt_lines.append(f"- {f}")
    prompt_lines.extend([
        "",
        "## Required",
        "- Fix the identified issues",
        "- Add or update tests to cover the fix",
        "- Run targeted tests and full suite",
        "",
        "## Forbidden",
        "- Do NOT auto-apply or auto-approve",
        "- Do NOT execute providers or models",
        "- Do NOT create PRs or commits automatically",
        "- Do NOT store secrets in config files",
        "- Do NOT use shell=True",
    ])
    proposal.suggested_worker_prompt = "\n".join(prompt_lines)

    # Acceptance criteria.
    acceptance_criteria.extend([
        "All identified issues are fixed or explained",
        "Targeted tests pass",
        "Full test suite passes",
        "No new raw data leaks introduced",
    ])
    proposal.acceptance_criteria = acceptance_criteria

    # Required tests.
    required_tests.extend([
        "python -m compileall -q packages apps tests",
        "scripts/remedy_pytest.sh tests/orchestration/test_self_repair_proposal.py",
    ])
    if "packages/orchestration/dogfood_run.py" in suspected_files:
        required_tests.append(
            "scripts/remedy_pytest.sh tests/orchestration/test_dogfood_run.py"
        )
    if "packages/orchestration/review_bundle.py" in suspected_files:
        required_tests.append(
            "scripts/remedy_pytest.sh tests/orchestration/test_review_bundle.py"
        )
    if "packages/orchestration/config.py" in suspected_files:
        required_tests.append(
            "scripts/remedy_pytest.sh tests/orchestration/test_config.py"
        )
    proposal.required_tests = required_tests

    # Forbidden actions.
    proposal.forbidden_actions = [
        "auto-apply", "auto-approve", "auto-PR", "auto-git",
        "provider execution", "shell=True", "secret storage",
        "raw log exposure", "MemPalace", "embeddings",
    ]

    # Risk summary.
    proposal.risk_summary = (
        f"{len(issues)} issue(s) identified. "
        "Proposal is based on rule-based analysis, not model-assisted diagnosis. "
        "Operator should verify evidence refs before approving."
    )

    save_self_repair_proposal(proposal, data_dir=ddir)
    return proposal


# ---------------------------------------------------------------------------
# Operator decision flow (Phase 4)
# ---------------------------------------------------------------------------


def approve_self_repair_proposal(
    proposal_id: str, operator_id: str, *, notes: str | None = None,
    data_dir: Path | None = None,
) -> SelfRepairProposal | None:
    ddir = _resolve_ddir(data_dir)
    proposal = load_self_repair_proposal(proposal_id, data_dir=ddir)
    if proposal is None:
        return None
    if proposal.status not in _APPROVABLE_STATUSES:
        return None
    if (not proposal.evidence_refs
            or not proposal.suggested_worker_prompt.strip()
            or not proposal.acceptance_criteria
            or not proposal.required_tests):
        return None
    proposal.status = SelfRepairProposalStatus.APPROVED
    proposal.operator_decision = f"approved by {operator_id}"
    if notes:
        proposal.operator_notes = notes
    save_self_repair_proposal(proposal, data_dir=ddir)
    return proposal


def deny_self_repair_proposal(
    proposal_id: str, operator_id: str, *, notes: str | None = None,
    data_dir: Path | None = None,
) -> SelfRepairProposal | None:
    ddir = _resolve_ddir(data_dir)
    proposal = load_self_repair_proposal(proposal_id, data_dir=ddir)
    if proposal is None:
        return None
    if proposal.status in _TERMINAL_STATUSES:
        return None
    proposal.status = SelfRepairProposalStatus.DENIED
    proposal.operator_decision = f"denied by {operator_id}"
    if notes:
        proposal.operator_notes = notes
    save_self_repair_proposal(proposal, data_dir=ddir)
    return proposal


def edit_self_repair_proposal(
    proposal_id: str, operator_id: str, patch_or_text: str,
    *, notes: str | None = None, data_dir: Path | None = None,
) -> SelfRepairProposal | None:
    ddir = _resolve_ddir(data_dir)
    proposal = load_self_repair_proposal(proposal_id, data_dir=ddir)
    if proposal is None:
        return None
    if proposal.status in _TERMINAL_STATUSES:
        return None
    proposal.suggested_worker_prompt = _sanitize_prompt(patch_or_text[:_MAX_PROMPT_LENGTH])
    proposal.status = SelfRepairProposalStatus.AWAITING_OPERATOR
    proposal.operator_decision = f"edited by {operator_id}"
    if notes:
        proposal.operator_notes = notes
    save_self_repair_proposal(proposal, data_dir=ddir)
    return proposal


def convert_self_repair_proposal_to_worker_prompt(
    proposal_id: str, *, data_dir: Path | None = None,
) -> str | None:
    """Convert an approved proposal to worker prompt text.

    Returns the prompt text if the proposal is approved. Returns None if the
    proposal is not found, not approved, or already converted/denied.
    """
    ddir = _resolve_ddir(data_dir)
    proposal = load_self_repair_proposal(proposal_id, data_dir=ddir)
    if proposal is None:
        return None
    if proposal.status != SelfRepairProposalStatus.APPROVED:
        return None
    if (not proposal.evidence_refs
            or not proposal.suggested_worker_prompt.strip()
            or not proposal.acceptance_criteria
            or not proposal.required_tests):
        return None
    prompt = _sanitize_prompt(proposal.suggested_worker_prompt)
    proposal.status = SelfRepairProposalStatus.CONVERTED_TO_WORKER_PROMPT
    save_self_repair_proposal(proposal, data_dir=ddir)
    return prompt


# ---------------------------------------------------------------------------
# Integrity checks (Phase 9)
# ---------------------------------------------------------------------------


def self_repair_proposal_integrity(
    *, data_dir: Path | None = None,
) -> dict[str, Any]:
    """Run integrity checks across all self-repair proposals."""
    ddir = _resolve_ddir(data_dir)
    out: dict[str, Any] = {"checks": [], "passed": True}
    proposals = list_self_repair_proposals(data_dir=ddir)

    for p in proposals:
        pid = p.get("proposal_id", "")
        status = p.get("status", "")

        # Check 1: status must be known.
        if status not in _ALL_STATUSES:
            out["checks"].append({"proposal_id": pid, "code": "unknown_status", "value": status})
            out["passed"] = False

        # Check 2: approved proposal must have evidence.
        if status == SelfRepairProposalStatus.APPROVED:
            if not p.get("evidence_refs"):
                out["checks"].append({"proposal_id": pid, "code": "approved_without_evidence"})
                out["passed"] = False

        # Check 3: converted proposal must have been approved first (operator_decision).
        if status == SelfRepairProposalStatus.CONVERTED_TO_WORKER_PROMPT:
            decision = p.get("operator_decision", "")
            if "approved" not in decision:
                out["checks"].append({"proposal_id": pid, "code": "converted_without_approval"})
                out["passed"] = False

        # Check 4: denied proposal must not be converted.
        if status == SelfRepairProposalStatus.DENIED:
            pass  # Terminal — conversion is blocked by the flow

        # Check 5: proposal must not leak raw data.
        proposal_str = json.dumps(p)
        for marker in _RAW_MARKERS:
            if marker in proposal_str:
                out["checks"].append({
                    "proposal_id": pid, "code": "raw_data_leak",
                    "marker": marker[:20],
                })
                out["passed"] = False
                break

        # Check 6: proposal must not contain absolute paths.
        for field_name in ("suggested_worker_prompt", "problem_summary", "risk_summary"):
            value = p.get(field_name, "")
            if _ABS_PATH_RE.search(value):
                out["checks"].append({
                    "proposal_id": pid, "code": "absolute_path_leak",
                    "field": field_name,
                })
                out["passed"] = False

        # Check 7: proposal must not claim code was applied.
        prompt = p.get("suggested_worker_prompt", "").lower()
        if "code applied" in prompt or "patch applied" in prompt or "auto-applied" in prompt:
            out["checks"].append({"proposal_id": pid, "code": "claims_code_applied"})
            out["passed"] = False

    return out


# ---------------------------------------------------------------------------
# Export helpers
# ---------------------------------------------------------------------------


def export_self_repair_proposal_json(proposal: SelfRepairProposal) -> dict[str, Any]:
    return proposal.to_dict()


def self_repair_proposal_summary_for_bundle(
    *, data_dir: Path | None = None,
) -> dict[str, Any]:
    """Safe summary for review bundle inclusion."""
    ddir = _resolve_ddir(data_dir)
    proposals = list_self_repair_proposals(data_dir=ddir)
    by_status: dict[str, int] = {}
    for p in proposals:
        s = p.get("status", "unknown")
        by_status[s] = by_status.get(s, 0) + 1
    return {
        "total_proposals": len(proposals),
        "by_status": by_status,
        "awaiting_operator": by_status.get(SelfRepairProposalStatus.AWAITING_OPERATOR, 0),
        "approved": by_status.get(SelfRepairProposalStatus.APPROVED, 0),
        "denied": by_status.get(SelfRepairProposalStatus.DENIED, 0),
        "converted": by_status.get(SelfRepairProposalStatus.CONVERTED_TO_WORKER_PROMPT, 0),
        "blocked": by_status.get(SelfRepairProposalStatus.BLOCKED, 0),
        "latest_proposal_id": proposals[-1].get("proposal_id", "") if proposals else "",
    }


def self_repair_progress_summary(
    *, data_dir: Path | None = None,
) -> dict[str, Any]:
    """Safe summary for progress ledger inclusion."""
    ddir = _resolve_ddir(data_dir)
    proposals = list_self_repair_proposals(data_dir=ddir)
    awaiting = sum(1 for p in proposals
                   if p.get("status") == SelfRepairProposalStatus.AWAITING_OPERATOR)
    approved = sum(1 for p in proposals
                   if p.get("status") == SelfRepairProposalStatus.APPROVED)
    denied = sum(1 for p in proposals
                 if p.get("status") == SelfRepairProposalStatus.DENIED)

    latest = proposals[-1] if proposals else None
    next_action = ""
    if awaiting > 0:
        next_action = "remedy self-repair proposal-list --json"
    elif approved > 0:
        pid = next(
            (p.get("proposal_id", "") for p in proposals
             if p.get("status") == SelfRepairProposalStatus.APPROVED),
            "",
        )
        next_action = f"remedy self-repair worker-prompt {pid} --json"

    return {
        "latest_proposal_id": latest.get("proposal_id", "") if latest else "",
        "latest_status": latest.get("status", "") if latest else "",
        "awaiting_operator_count": awaiting,
        "approved_count": approved,
        "denied_count": denied,
        "next_safe_action": next_action,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    # Status.
    "SelfRepairProposalStatus", "_ALL_STATUSES", "_TERMINAL_STATUSES",
    "_APPROVABLE_STATUSES",
    # Helpers (for testing).
    "_sanitize_prompt",
    # Model.
    "SelfRepairProposal",
    # Storage.
    "save_self_repair_proposal", "load_self_repair_proposal",
    "list_self_repair_proposals",
    # Generation.
    "create_self_repair_proposal_from_replay",
    # Operator decisions.
    "approve_self_repair_proposal", "deny_self_repair_proposal",
    "edit_self_repair_proposal", "convert_self_repair_proposal_to_worker_prompt",
    # Integrity.
    "self_repair_proposal_integrity",
    # Export.
    "export_self_repair_proposal_json",
    "self_repair_proposal_summary_for_bundle",
    "self_repair_progress_summary",
    # Schema.
    "SCHEMA_VERSION",
]
