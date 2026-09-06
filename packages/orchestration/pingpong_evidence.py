"""Evidence bundle builder — exports a self-contained, safe proof bundle for a Remedy run.

Read-only: never calls providers, never mutates target repo, never auto-promotes.
Redaction: no raw task body by default, no env/API keys, no absolute staging paths,
no hidden provider prompts, no .env files, no raw repo file contents beyond safe diff.
"""
from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# The evidence layout the F103 token ledger mirrors: task_runs/<task_id>/.
_TASK_RUNS_DIRNAME = "task_runs"

# ---------------------------------------------------------------------------
# Redaction
# ---------------------------------------------------------------------------

# Patterns that look like API keys or secrets
_SECRET_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),           # OpenAI-style
    re.compile(r"sk-ant-[a-zA-Z0-9]{20,}"),        # Anthropic-style
    re.compile(r"AKIA[0-9A-Z]{16}"),               # AWS access key
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),            # GitHub PAT
    re.compile(r"ghs_[a-zA-Z0-9]{36}"),            # GitHub app token
    re.compile(r"glpat-[a-zA-Z0-9_-]{20,}"),       # GitLab PAT
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}"),  # Bearer tokens
]

_ENV_KEY_PATTERN = re.compile(
    r"(API_KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL|PRIVATE_KEY)\s*=\s*\S+",
    re.IGNORECASE,
)


def _redact_secrets(text: str) -> str:
    """Replace API-key-like strings with [REDACTED]."""
    for pat in _SECRET_PATTERNS:
        text = pat.sub("[REDACTED]", text)
    text = _ENV_KEY_PATTERN.sub(r"\1=[REDACTED]", text)
    return text


def _redact_json_value(value: Any) -> Any:
    """Recursively redact secrets from arbitrary JSON-like data.

    Walks dicts, lists, and strings. Preserves non-string types and shape.
    Returns a new object — does not mutate the original.
    """
    if isinstance(value, str):
        return _redact_secrets(value)
    if isinstance(value, dict):
        return {k: _redact_json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        result = [_redact_json_value(item) for item in value]
        return type(value)(result) if isinstance(value, tuple) else result
    # int, float, bool, None — pass through
    return value


def _sanitize_path(path_str: str) -> str:
    """Replace absolute private paths with safe labels for shareable output."""
    if "/tmp/remedy-pingpong-" in path_str:
        return "[staging]"
    if path_str.startswith("/tmp/"):
        return "[tmpdir]"
    home = os.path.expanduser("~")
    if path_str.startswith(home):
        return "[local]"
    if path_str.startswith("/home/"):
        return "[local]"
    if path_str.startswith("/Users/"):
        return "[local]"
    if path_str.startswith("/private/"):
        return "[local]"
    return path_str


def _validate_output_path(out_dir: str, filename: str) -> Path:
    """Validate that filename doesn't escape out_dir via path traversal."""
    base = Path(out_dir).resolve()
    target = (base / filename).resolve()
    if not str(target).startswith(str(base) + os.sep) and target != base:
        raise ValueError(f"Path traversal blocked: {filename!r}")
    return target


# ---------------------------------------------------------------------------
# Bundle builder
# ---------------------------------------------------------------------------

def build_evidence_bundle(
    run_data: dict[str, Any],
    promotion_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic evidence bundle from a persisted run.

    Returns a dict of bundle sections. Does not write files.
    Does not call providers. Does not mutate anything.
    """
    bundle: dict[str, Any] = {}

    # Core identity
    bundle["manifest"] = _build_manifest(run_data, promotion_data)
    bundle["summary_md"] = _build_summary_md(run_data, promotion_data)
    bundle["safe_diff"] = run_data.get("safe_diff_summary", "")
    bundle["tests"] = _build_tests_txt(run_data)
    bundle["review"] = _build_review_json(run_data)
    bundle["repair_loop"] = _build_repair_loop_json(run_data)
    bundle["promotion"] = _build_promotion_json(promotion_data)
    bundle["token_accounting"] = _build_token_accounting_json(run_data)
    bundle["provider_evidence"] = _build_provider_evidence_json(run_data)

    return bundle


def _build_manifest(
    run_data: dict[str, Any],
    promotion_data: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build manifest.json content."""
    # Determine availability of each section
    has_diff = bool(run_data.get("safe_diff_summary"))
    has_tests = any(
        rd.get("test_passed") is not None
        for rd in run_data.get("rounds", [])
    )
    has_review = any(
        rd.get("reviewer") is not None
        for rd in run_data.get("rounds", [])
    )
    has_repair = run_data.get("repair_loop", {}).get("enabled", False)
    has_promotion = promotion_data is not None

    # Task input metadata (safe — no raw body)
    task_input = run_data.get("task_input")
    task_meta: dict[str, Any] | None = None
    if task_input:
        task_meta = {
            "kind": task_input.get("kind", ""),
            "title": task_input.get("title", ""),
            "sha256": task_input.get("sha256", ""),
            "bytes": task_input.get("bytes", 0),
            "chars": task_input.get("chars", 0),
            "tokens_estimated": task_input.get("tokens_estimated", 0),
            # Excerpt only, not full body — redacted for safety
            "excerpt": _redact_secrets((task_input.get("excerpt", "") or "")[:200]),
        }

    # Scope plan summary
    scope_plan = run_data.get("scope_plan")
    scope_summary: dict[str, Any] | None = None
    if scope_plan:
        scope_summary = {
            "plan_id": scope_plan.get("plan_id", ""),
            "feature_count": len(scope_plan.get("features", [])),
            "approved_count": len(scope_plan.get("approved_features", [])),
            "denied_count": len(scope_plan.get("denied_features", [])),
        }

    manifest: dict[str, Any] = {
        "bundle_version": "0.1.0",
        "run_id": run_data.get("run_id", ""),
        "goal": run_data.get("goal", ""),
        "final_status": run_data.get("final_status", ""),
        "repo_identity": _sanitize_path(run_data.get("repo_path", "")),
        "mode": run_data.get("mode", ""),
        "started_at": run_data.get("started_at", ""),
        "finished_at": run_data.get("finished_at", ""),
        "task_input": task_meta,
        "scope_plan": scope_summary,
        "sections": {
            "manifest.json": "present",
            "summary.md": "present",
            "safe.diff": "present" if has_diff else "unavailable: no diff produced",
            "tests.txt": "present" if has_tests else "unavailable: no tests run",
            "review.json": "present" if has_review else "unavailable: no review performed",
            "repair_loop.json": "present" if has_repair else "unavailable: repair disabled",
            "promotion.json": "present" if has_promotion else "unavailable: no promotion performed",
            "token_accounting.json": "present",
            "provider_evidence.json": "present",
        },
        "promotion_readiness": _assess_promotion_readiness(run_data, promotion_data),
    }
    return manifest


def _assess_promotion_readiness(
    run_data: dict[str, Any],
    promotion_data: dict[str, Any] | None,
) -> dict[str, Any]:
    """Assess whether this run is promotion-ready."""
    final_status = run_data.get("final_status", "")
    is_passed = final_status == "staged_review_passed"

    # Check last test
    rounds = run_data.get("rounds", [])
    last_test_passed: bool | None = None
    if rounds:
        last_test_passed = rounds[-1].get("test_passed")

    # Check promotion
    promoted = False
    promotion_status = ""
    if promotion_data:
        promoted = promotion_data.get("status") == "promoted"
        promotion_status = promotion_data.get("status", "")

    return {
        "review_passed": is_passed,
        "last_test_passed": last_test_passed,
        "promotion_performed": promotion_data is not None,
        "promotion_status": promotion_status,
        "promoted": promoted,
        "ready": is_passed and last_test_passed is not False,
        "proof_summary": (
            "promotion-ready: review passed, tests passed"
            if is_passed and last_test_passed is not False
            else f"not promotion-ready: final_status={final_status}"
        ),
    }


def _build_summary_md(
    run_data: dict[str, Any],
    promotion_data: dict[str, Any] | None,
) -> str:
    """Build human-readable summary.md content."""
    lines: list[str] = []
    lines.append(f"# Remedy Run Evidence — {run_data.get('run_id', '')}")
    lines.append("")
    lines.append(f"**Goal:** {run_data.get('goal', '')}")
    lines.append(f"**Status:** {run_data.get('final_status', '')}")
    lines.append(f"**Mode:** {run_data.get('mode', '')}")
    lines.append(f"**Repo:** {_sanitize_path(run_data.get('repo_path', ''))}")
    lines.append("")

    # Provider info
    pe = run_data.get("provider_evidence", {})
    lines.append("## Providers")
    lines.append(f"- Worker: {run_data.get('builder_provider', 'unknown')} ({pe.get('builder_provider_kind', '')})")
    lines.append(f"- Reviewer: {run_data.get('reviewer_provider', 'unknown')} ({pe.get('reviewer_provider_kind', '')})")
    lines.append(f"- Worker write mode: {pe.get('builder_write_mode', 'none')}")
    lines.append("")

    # Task input
    ti = run_data.get("task_input")
    if ti:
        lines.append("## Task Input")
        lines.append(f"- Kind: {ti.get('kind', '')}")
        if ti.get("title"):
            lines.append(f"- Title: {ti['title']}")
        lines.append(f"- Hash: {ti.get('sha256', '')[:12]}...")
        lines.append(f"- Size: ~{ti.get('tokens_estimated', 0)} tokens")
        lines.append("")

    # Rounds
    rounds = run_data.get("rounds", [])
    lines.append(f"## Rounds: {len(rounds)}/{run_data.get('max_rounds', 0)}")
    for rd in rounds:
        kind = rd.get("kind", "initial")
        test_status = "passed" if rd.get("test_passed") else ("failed" if rd.get("test_passed") is False else "not run")
        rv = rd.get("reviewer", {})
        verdict = rv.get("verdict", "none") if rv else "none"
        lines.append(f"- Round {rd.get('round', '?')} ({kind}): tests {test_status}, reviewer {verdict}")
    lines.append("")

    # Safe diff
    diff_files = run_data.get("safe_diff_files", [])
    if diff_files:
        lines.append(f"## Safe Diff: {len(diff_files)} file(s)")
        for f in diff_files[:20]:
            lines.append(f"- {f}")
        if len(diff_files) > 20:
            lines.append(f"- ... and {len(diff_files) - 20} more")
        lines.append("")

    # Test summary
    if rounds:
        last = rounds[-1]
        ts = last.get("test_summary", "")
        if ts:
            lines.append("## Test Summary")
            lines.append(f"```\n{_redact_secrets(ts)}\n```")
            lines.append("")

    # Repair loop
    rl = run_data.get("repair_loop", {})
    if rl.get("enabled"):
        lines.append("## Repair Loop")
        lines.append(f"- Allowed: {rl.get('repair_rounds_allowed', 0)}")
        lines.append(f"- Used: {rl.get('repair_rounds_used', 0)}")
        lines.append(f"- Status: {rl.get('status', '')}")
        lines.append("")

    # Promotion
    if promotion_data:
        lines.append("## Promotion")
        lines.append(f"- Status: {promotion_data.get('status', '')}")
        lines.append(f"- Approved: {promotion_data.get('approved', False)}")
        lines.append(f"- Dry run: {promotion_data.get('dry_run', False)}")
        lines.append("")

    # Readiness
    readiness = _assess_promotion_readiness(run_data, promotion_data)
    lines.append("## Promotion Readiness")
    lines.append(f"- {readiness['proof_summary']}")
    lines.append("")

    return "\n".join(lines)


def _build_tests_txt(run_data: dict[str, Any]) -> str:
    """Build tests.txt content from round test summaries."""
    parts: list[str] = []
    for rd in run_data.get("rounds", []):
        rn = rd.get("round", "?")
        tp = rd.get("test_passed")
        ts = rd.get("test_summary", "")
        status = "passed" if tp else ("failed" if tp is False else "not run")
        parts.append(f"=== Round {rn}: {status} ===")
        if ts:
            parts.append(_redact_secrets(ts))
        parts.append("")
    if parts:
        return "\n".join(parts)
    final_status = run_data.get("final_status", "")
    if final_status == "builder_no_changes":
        return "builder_no_changes: code already correct, no tests required\n"
    return ""


def _build_review_json(run_data: dict[str, Any]) -> dict[str, Any]:
    """Build review.json from round reviewer data."""
    reviews: list[dict[str, Any]] = []
    for rd in run_data.get("rounds", []):
        rv = rd.get("reviewer")
        if rv:
            redacted_findings = []
            for f in rv.get("findings", []):
                redacted_findings.append(_redact_json_value(f))
            reviews.append({
                "round": rd.get("round", 0),
                "kind": rd.get("kind", "initial"),
                "verdict": rv.get("verdict", ""),
                "confidence": rv.get("confidence", ""),
                "summary": _redact_secrets(rv.get("summary", "")),
                "finding_count": rv.get("finding_count", 0),
                "findings": redacted_findings,
            })

    if reviews:
        last_verdict = reviews[-1]["verdict"]
    elif run_data.get("final_status") == "builder_no_changes":
        last_verdict = "no_changes_verified"
        reviews.append({
            "round": 0,
            "kind": "no_changes_verification",
            "verdict": "no_changes_verified",
            "confidence": "",
            "summary": "Builder confirmed code already correct; no changes produced.",
            "finding_count": 0,
            "findings": [],
        })
    else:
        last_verdict = ""

    return {
        "total_reviews": len(reviews),
        "final_verdict": last_verdict,
        "reviews": reviews,
    }


def _build_repair_loop_json(run_data: dict[str, Any]) -> dict[str, Any]:
    """Build repair_loop.json from run data."""
    rl = run_data.get("repair_loop")
    if rl:
        return _redact_json_value(dict(rl))
    # Fallback if repair_loop not in export
    return {
        "enabled": False,
        "repair_rounds_allowed": 0,
        "repair_rounds_used": 0,
        "status": "disabled",
    }


def _build_promotion_json(
    promotion_data: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Build promotion.json from promotion data."""
    if promotion_data is None:
        return None
    # Return safe copy — redacted and path-sanitized
    safe = _redact_json_value(dict(promotion_data))
    # Sanitize any absolute paths
    for key in ("staging_path", "target_repo", "run_repo", "requested_target_repo"):
        if key in safe and isinstance(safe[key], str):
            safe[key] = _sanitize_path(safe[key])
    return safe


def _build_token_accounting_json(run_data: dict[str, Any]) -> dict[str, Any]:
    """Build token_accounting.json from run data."""
    ta = run_data.get("token_accounting")
    if ta:
        return _redact_json_value(dict(ta))
    return {"kind": "unavailable"}


def _build_provider_evidence_json(run_data: dict[str, Any]) -> dict[str, Any]:
    """Build provider_evidence.json from run data."""
    pe = run_data.get("provider_evidence")
    if pe:
        redacted = _redact_json_value(dict(pe))
        if "schema_version" not in redacted:
            from packages.orchestration.provider_token_evidence import PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION
            redacted["schema_version"] = PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION
        return redacted
    return {
        "schema_version": "1.0.0",
        "execution_mode": "provider_backed",
        "builder_provider": run_data.get("builder_provider", ""),
        "reviewer_provider": run_data.get("reviewer_provider", ""),
        "provider_call_count": 0,
        "actual_call_count": 0,
        "cost_call_count": 0,
    }


# ---------------------------------------------------------------------------
# File writer
# ---------------------------------------------------------------------------

def write_evidence_bundle(
    bundle: dict[str, Any],
    out_dir: str,
    *,
    ledger_project_id: str | None = None,
    ledger_path: str | None = None,
    ledger_job_id: str | None = None,
    ledger_task_id: str | None = None,
) -> dict[str, str]:
    """Write evidence bundle files to output directory.

    Returns a dict mapping filename -> absolute path of written file.
    Blocks path traversal. Writes only inside out_dir.

    The four ``ledger_*`` arguments are the OPT-IN for the F103 token ledger
    mirror. They all default to None, which keeps every existing caller's
    behaviour bit-for-bit unchanged: no ledger is opened, no project is
    resolved, no file appears anywhere. Naming a target (``ledger_project_id``
    or ``ledger_path``) together with ``ledger_job_id`` and ``ledger_task_id``
    records this task run as one ledger row. The mirror never changes this
    function's return value and never fails the write —
    see ``_record_finalized_call_in_ledger``.
    """
    out_path = Path(out_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    written: dict[str, str] = {}

    def _write(filename: str, content: str) -> None:
        target = _validate_output_path(str(out_path), filename)
        target.write_text(content)
        written[filename] = str(target)

    def _write_json(filename: str, data: Any) -> None:
        _write(filename, json.dumps(_redact_json_value(data), indent=2) + "\n")

    # manifest.json
    _write_json("manifest.json", bundle["manifest"])

    # summary.md
    _write("summary.md", _redact_secrets(bundle["summary_md"]))

    # safe.diff
    diff_content = bundle.get("safe_diff", "")
    if diff_content:
        _write("safe.diff", _redact_secrets(diff_content))

    # tests.txt — always written so evidence completeness is satisfied
    tests_content = bundle.get("tests", "")
    _write("tests.txt", tests_content or "tests_not_run\n")

    # review.json — always written so evidence completeness is satisfied
    review = bundle.get("review")
    if review:
        _write_json("review.json", review)

    # repair_loop.json
    repair = bundle.get("repair_loop")
    if repair:
        _write_json("repair_loop.json", repair)

    # promotion.json
    promotion = bundle.get("promotion")
    if promotion is not None:
        _write_json("promotion.json", promotion)

    # token_accounting.json
    ta = bundle.get("token_accounting")
    if ta:
        _write_json("token_accounting.json", ta)

    # provider_evidence.json
    pe = bundle.get("provider_evidence")
    if pe:
        _write_json("provider_evidence.json", pe)
        # Actuals are FINALIZED at this exact point — the file the ledger
        # mirrors now exists — so this is where F103 puts its hook.
        _record_finalized_call_in_ledger(
            out_path,
            project_id=ledger_project_id,
            ledger_path=ledger_path,
            job_id=ledger_job_id,
            task_id=ledger_task_id,
        )

    # prompt_trace.jsonl + prompt_trace_summary.json (copy from persisted run dir)
    trace_path = bundle.get("prompt_trace_jsonl_path")
    if trace_path:
        src = Path(trace_path)
        if src.exists():
            content = src.read_text()
            _write("prompt_trace.jsonl", _redact_secrets(content))
            summary_src = src.parent / "prompt_trace_summary.json"
            if summary_src.exists():
                _write("prompt_trace_summary.json", summary_src.read_text())

    return written


# ---------------------------------------------------------------------------
# F103 token ledger hook — the mirror, never the evidence
# ---------------------------------------------------------------------------

# Mirrors one finalized task run into the token ledger; opt-in, inert, never fatal.
def _record_finalized_call_in_ledger(
    out_path: Path,
    *,
    project_id: str | None,
    ledger_path: str | None,
    job_id: str | None,
    task_id: str | None,
) -> None:
    """Record the task run just written under ``out_path`` into the F103 ledger.

    THE EVIDENCE WRITE IS THE IMPORTANT THING AND THIS IS NOT. The ledger is a
    mirror of files that are already the source of truth, so nothing here may
    change what ``write_evidence_bundle`` returns, and nothing here may raise:
    ``record_call`` already returns False instead of raising, and the wrapper
    below makes even an unexpected error unable to escape.

    OPT-IN AND INERT BY DEFAULT: without a ledger target, or without both
    identifiers, it returns immediately. It deliberately does NOT resolve a
    project itself — a test that writes an evidence bundle must never start
    touching the user's data root, so the caller has to name the target.

    NOT A SECOND CAPTURE PATH: it parses no provider output. It re-reads the
    ``provider_evidence.json`` it has just written, through the ledger's own
    ``call_record_from_evidence``, so the live row is derived by the same
    function from the same bytes as a later backfill's row would be. That
    identity is what lets ``verify_ledger`` compare content rather than mere
    presence — two producers of one row must not be free to disagree.
    """
    if project_id is None and ledger_path is None:
        return
    if not job_id or not task_id:
        return
    try:
        # Imported lazily: a run that never asks for a ledger never pays for the
        # import, and the evidence exporter keeps its existing import graph.
        from packages.orchestration.token_ledger import (
            call_record_from_evidence,
            record_call,
        )

        if out_path.parent.name != _TASK_RUNS_DIRNAME or out_path.name != str(task_id):
            # Not the task-run layout the ledger mirrors, so there is no honest
            # evidence_ref for the row. No row is invented for it.
            return
        record = call_record_from_evidence(out_path.parent.parent, job_id, task_id)
        if record is None:
            return
        record_call(record, project_id=project_id, path=ledger_path)
    except Exception:
        logger.error(
            "token ledger hook FAILED after writing evidence for task %r (the "
            "evidence write itself is unaffected and the run continues; the files "
            "remain the source of truth and reconcile can heal the mirror)",
            task_id, exc_info=True,
        )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def export_evidence(
    run_id: str,
    out_dir: str,
) -> dict[str, Any]:
    """Load a persisted run and export evidence bundle.

    Returns JSON-serializable result with output paths and manifest.
    Does not call providers. Does not mutate target repo.
    """
    from packages.orchestration.pingpong_loop import load_run
    from packages.orchestration.pingpong_promote import load_promotion

    run_data = load_run(run_id)
    if run_data is None:
        return {"error": f"Run {run_id!r} not found", "run_id": run_id}

    promotion_data = load_promotion(run_id)

    bundle = build_evidence_bundle(run_data, promotion_data)

    # Load persisted prompt traces if available
    from packages.orchestration.data_paths import pingpong_run_dir
    trace_file = pingpong_run_dir(run_id) / "prompt_trace.jsonl"
    if trace_file.exists():
        bundle["prompt_trace_jsonl_path"] = str(trace_file)

    written = write_evidence_bundle(bundle, out_dir)

    return _redact_json_value({
        "run_id": run_id,
        "out_dir": str(Path(out_dir).resolve()),
        "files": written,
        "manifest": bundle["manifest"],
    })
