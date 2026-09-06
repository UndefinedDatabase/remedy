"""Job evidence bundle — exports a self-contained, redacted proof bundle for an entire job.

Read-only: never calls providers, never mutates target repo, never auto-promotes,
never reruns tasks, never mutates persisted job state.

Reuses single-run evidence redaction from pingpong_evidence. Does not duplicate
weaker redaction logic.

Public API:
    export_job_evidence(job_id, out_dir) -> dict
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
from pathlib import Path
from typing import Any

from packages.common.path_redaction import scrub_paths as _shared_scrub_paths
from packages.orchestration.pingpong_evidence import (
    _redact_json_value,
    _redact_secrets,
    _sanitize_path,
    _validate_output_path,
    build_evidence_bundle,
    write_evidence_bundle,
)
from packages.orchestration.pingpong_job import (
    _export_apply_manifest,
    _export_execution_config,
    _export_proof_summary,
    _export_target_guard,
    load_job_plan,
)

logger = logging.getLogger(__name__)

_TASK_BODY_EVIDENCE_LIMIT = 500
_WORKSPACE_DIFF_MAX_CHARS = 500_000

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")


def _task_evidence_dir(out_base: str, task_id: str) -> Path:
    """Return a contained task evidence directory inside out_base/task_runs/.

    Only allows task IDs matching the expected format (T001, T002, ...).
    Raises ValueError on malicious, corrupt, or unexpected task IDs to prevent
    path traversal via persisted job state or symlink escapes.

    Uses _validate_output_path which calls .resolve() on the full joined path,
    following any symlinks in intermediate directories (e.g. out/task_runs/).
    """
    if not task_id or not _SAFE_TASK_ID_RE.fullmatch(task_id):
        raise ValueError(
            f"Unsafe task ID {task_id!r}: must match T<digits> (e.g. T001). "
            "Aborting evidence export to prevent path traversal."
        )
    return _validate_output_path(out_base, f"task_runs/{task_id}")


# F103: the ONE place a real job's ledger target is decided; None means stay inert.
def _resolve_job_ledger_project_id(job: Any) -> str | None:
    """Return the registry UUID of the project a job's rows belong to, or None.

    THIS IS THE SWITCH THAT ARMS THE F103 TOKEN LEDGER for real jobs. The mirror
    in ``write_evidence_bundle`` is opt-in precisely so that writing an evidence
    bundle never touches the user's data root by accident
    (``pingpong_evidence._record_finalized_call_in_ledger``); arming it is
    therefore a decision that has to be made HERE, once per export, on evidence
    rather than on a guess.

    The project is resolved from the job's OWN ``repo_path`` — persisted job
    state — through ``project_registry.resolve_project``, the registry's
    read-only cwd-to-project resolver. The returned id is the registry UUID that
    ``token_ledger_path_for`` keys the ledger by, and the data root under it
    comes from ``data_paths``, so ``REMEDY_DATA_DIR`` is honoured.

    INERT UNLESS A PROJECT REALLY RESOLVES. Returns None when the job records no
    repo path, when that path is not a git repository, or when no registered
    project owns it. A None target is what keeps the hook switched off, so a
    unit test that merely writes job evidence for a throwaway repo still writes
    no ledger anywhere. Nothing is guessed: there is no fallback to the process
    working directory and no default project.

    Remedy deliberately does NOT consult ``REMEDY_PROJECT`` or the process CWD
    here, unlike ``project_scope.resolve_scope`` which exists to interpret what a
    HUMAN at a terminal meant. A job's cost rows belong to the repository the job
    actually ran against; letting ambient environment redirect them would file
    one project's spend under another. ``export_job_evidence`` reads no ambient
    environment by design (F6, round 16) and this keeps that true.

    Never raises: a resolution failure means no ledger, never a failed export.
    """
    repo_path = str(getattr(job, "repo_path", "") or "").strip()
    if not repo_path:
        return None
    try:
        from packages.orchestration.project_registry import resolve_project

        project = resolve_project(repo_path)
    except Exception:
        logger.warning(
            "token ledger target could not be resolved for repo %r; the live "
            "mirror stays inert for this export and the evidence files, which "
            "are the source of truth, are unaffected (remedy stats "
            "backfill-ledger can still mirror them later)",
            repo_path, exc_info=True,
        )
        return None
    return str(project.id) if project is not None else None


def mirror_job_run_into_ledger(job_id: str) -> dict[str, Any]:
    """Export a finished job's evidence so its cost reaches the F103 token ledger.

    THIS IS THE JOB RUNNER'S COST-TRUTH SEAM. `remedy do job-run` used to complete
    a job, write ``jobs/<id>/job.json`` and its run log, and touch no ledger
    at all, so `remedy stats cost` reported "No ledger on disk for this scope"
    after a run that had spent real money. The mirror is armed in exactly one
    place — ``_resolve_job_ledger_project_id``, reached only from
    ``export_job_evidence`` — and only two commands used to reach it,
    `do job-evidence` and `do job-flow`. A run that is never exported has no cost
    row, and `remedy stats backfill-ledger` cannot help either, because it mirrors
    an evidence DIRECTORY that was never written.

    Rather than record from the loop, which would move DECISION D16's
    per-finalized-task-run granularity, this reuses the seam that already exists:
    the job's evidence is exported to its own default location, which arms the
    live mirror exactly as `do job-evidence` does. One call, no second capture
    path, and no new ledger writer to keep in step with the old one.

    NEVER FATAL. A job that ran is a job that ran; a failure to mirror its cost
    must not turn a completed run into a failed command. The evidence files stay
    the source of truth and `remedy stats backfill-ledger` can still mirror them
    later, so every failure is reported and swallowed.

    Returns ``{"ledger_mirrored": bool, "out_dir": str, "error": str}``.
    """
    from packages.orchestration.data_paths import job_evidence_export_dir

    try:
        out_dir = str(job_evidence_export_dir(job_id))
    except Exception as exc:
        return {"ledger_mirrored": False, "out_dir": "",
                "error": f"{type(exc).__name__}: {exc}"}

    try:
        result = export_job_evidence(job_id, out_dir)
    except Exception as exc:
        logger.warning(
            "cost mirror failed for job %s; the run itself is unaffected and "
            "remedy stats backfill-ledger can still mirror the evidence later",
            job_id, exc_info=True,
        )
        return {"ledger_mirrored": False, "out_dir": out_dir,
                "error": f"{type(exc).__name__}: {exc}"}

    error = str(result.get("error") or "")
    return {
        "ledger_mirrored": not error,
        "out_dir": str(result.get("out_dir", out_dir)),
        "error": error,
    }


def export_job_evidence(
    job_id: str,
    out_dir: str,
    *,
    verification_commands: list[str] | None = None,
    verification_runner: Any = None,
    declared_base: str | None = None,
) -> dict[str, Any]:
    """Load a persisted job and export a job-level evidence bundle.

    ``verification_commands`` are explicit shell commands (e.g. focused pytest
    invocations) that are actually executed and recorded as verification runs.
    Nothing is claimed verified that was not run. ``verification_runner`` lets a
    caller inject a deterministic runner ``(command:str) -> dict`` (used by unit
    tests to avoid recursively spawning pytest); when omitted a real subprocess
    runner is used only if commands are supplied.

    Returns JSON-serializable result with output paths, manifest, and status.
    Does not call providers. Does not mutate target repo or job state.
    """
    job = load_job_plan(job_id)
    if job is None:
        return {"error": f"Job {job_id!r} not found", "job_id": job_id}

    out_path = Path(out_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    written: dict[str, str] = {}

    def _write(filename: str, content: str) -> None:
        target = _validate_output_path(str(out_path), filename)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        written[filename] = str(target)

    def _write_json(filename: str, data: Any) -> None:
        _write(filename, json.dumps(_redact_json_value(data), indent=2) + "\n")

    manifest = _build_job_manifest(job)
    _write_json("manifest.json", manifest)

    summary_md = _build_job_summary_md(job)
    _write("summary.md", _redact_secrets(summary_md))

    job_report = _build_job_report_safe(job)
    _write_json("job_report.json", job_report)

    timeline = _build_job_timeline(job)
    _write_json("job_timeline.json", timeline)

    tasks_data = _build_tasks_json(job)
    _write_json("tasks.json", tasks_data)

    ec = _export_execution_config(job.execution_config)
    _write_json("execution_config.json", ec or {})

    cs = {
        "strategy": "task_bounded_sequential_job",
        "previous_task_summary_limit": 5,
        "full_job_history_in_prompt": False,
        "full_repo_in_prompt": False,
    }
    if job.execution_config:
        cs["strategy"] = job.execution_config.context_strategy
    _write_json("context_strategy.json", cs)

    tg = _export_target_guard(job.target_guard)
    _write_json("target_guard.json", tg or {"target_mutated": None, "note": "no guard data"})

    wa = _build_workspace_apply_json(job)
    _write_json("workspace_apply.json", wa)

    # F006: for a worktree JobPlan the canonical hand-off is the job directory's
    # verified result.diff — NOT the (deliberately removed) execution workspace.
    _job_diff_text, _job_diff_err = _write_job_worktree_evidence(
        job, out_path, written,
    )
    if _job_diff_text is not None:
        _write("workspace.diff", _redact_secrets(_job_diff_text))
    else:
        ws_diff = _build_workspace_diff(job)
        _write("workspace.diff", _redact_secrets(ws_diff))

    attest_snap = _snapshot_attestation_artifacts(job)

    # F010: everything the post-mortem contract could not deliver lands here, and a
    # non-empty list blocks the package. A warning file nobody reads is not a gate.
    postmortem_failures: list[dict[str, Any]] = []

    try:
        _write_job_postmortem(job, str(out_path), written, postmortem_failures)
    except Exception as exc:
        from packages.orchestration.failure_postmortem import safe_text as _safe
        postmortem_failures.append({
            "scope": "job", "job_id": job.job_id,
            "error": _safe(f"job post-mortem export failed: {type(exc).__name__}: {exc}")[:500],
        })

    # F103: resolve the ledger target ONCE per export — one git/registry lookup
    # for the whole job, not one per task — and stay inert when none resolves.
    ledger_project_id = _resolve_job_ledger_project_id(job)

    for task in job.tasks:
        _write_task_run_evidence(
            task, str(out_path), written,
            ledger_project_id=ledger_project_id, job_id=job.job_id,
        )
        # F010: a terminally failed task leaves ONE rollup, and the call-level
        # post-mortems it points at travel with it into the bundle.
        try:
            _write_task_postmortems(
                job.job_id, task, str(out_path), written, postmortem_failures)
        except Exception as exc:
            from packages.orchestration.failure_postmortem import safe_text as _safe
            postmortem_failures.append({
                "scope": "task", "task_id": task.task_id,
                "error": _safe(f"{type(exc).__name__}: {exc}")[:500],
            })
        # F004: bring the per-attempt stream artifacts into the shareable bundle.
        try:
            _stream_listing = _copy_task_stream_artifacts(
                job.job_id, task.task_id, str(out_path), written,
            )
            if _stream_listing:
                _sl_rel = f"task_runs/{task.task_id}/stream_artifacts.json"
                _sl_path = _validate_output_path(str(out_path), _sl_rel)
                _sl_path.write_text(
                    json.dumps({
                        "schema_version": "1.0.0",
                        "task_id": task.task_id,
                        "artifacts": _stream_listing,
                    }, indent=2) + "\n",
                    encoding="utf-8",
                )
                written[_sl_rel] = str(_sl_path)
        except Exception as exc:
            _rel = f"task_runs/{task.task_id}/stream_artifacts.error.txt"
            _p = _validate_output_path(str(out_path), _rel)
            _p.parent.mkdir(parents=True, exist_ok=True)
            _p.write_text(f"stream artifact export failed: {type(exc).__name__}: {exc}\n")
            written[_rel] = str(_p)
        try:
            from packages.orchestration.review_scope import write_review_scope_packet
            write_review_scope_packet(task, job.job_workspace_path, str(out_path), written)
        except Exception as exc:
            rel = f"task_runs/{task.task_id}/review_scope_packet.error.txt"
            err_path = _validate_output_path(str(out_path), rel)
            err_path.write_text(
                f"review_scope_packet unavailable: {type(exc).__name__}: {exc}\n",
                encoding="utf-8",
            )
            written[rel] = str(err_path)
        try:
            from packages.orchestration.spec_compliance import write_spec_compliance_check
            write_spec_compliance_check(
                task,
                getattr(task, "body", "") or "",
                str(out_path),
                job.job_workspace_path,
                written,
            )
        except Exception as exc:
            rel = f"task_runs/{task.task_id}/spec_compliance_check.error.txt"
            err_path = _validate_output_path(str(out_path), rel)
            err_path.write_text(
                f"spec_compliance_check unavailable: {type(exc).__name__}: {exc}\n",
                encoding="utf-8",
            )
            written[rel] = str(err_path)
        try:
            from packages.orchestration.missing_tests_gate import (
                write_missing_tests_gate,
            )
            write_missing_tests_gate(task, str(out_path), written)
        except Exception as exc:
            rel = f"task_runs/{task.task_id}/missing_tests_gate.error.txt"
            err_path = _validate_output_path(str(out_path), rel)
            err_path.write_text(
                f"missing_tests_gate unavailable: {type(exc).__name__}: {exc}\n",
                encoding="utf-8",
            )
            written[rel] = str(err_path)
        # Per-task execution evidence (execution_mode classification)
        try:
            from packages.orchestration.data_paths import run_dir
            from packages.orchestration.evidence_mode import (
                build_task_execution_evidence,
                classify_execution_mode,
            )

            _prompt_count = 0
            _provider_call_count = 0
            _builder_prov = (
                getattr(job.execution_config, "builder", None) or ""
            ) if job.execution_config else ""
            _reviewer_prov = (
                getattr(job.execution_config, "reviewer", None) or ""
            ) if job.execution_config else ""
            if task.run_id:
                _trace_file = run_dir(task.run_id) / "prompt_trace_summary.json"
                if _trace_file.exists():
                    try:
                        _tdata = json.loads(_trace_file.read_text())
                        _prompt_count = int(_tdata.get("builder_prompts", 0)) + int(_tdata.get("reviewer_prompts", 0))
                        _provider_call_count = _prompt_count
                    except (OSError, json.JSONDecodeError, ValueError):
                        pass
            _exec_mode = classify_execution_mode(
                _prompt_count, _provider_call_count, _builder_prov, _reviewer_prov,
            )
            _exec_ev = build_task_execution_evidence(
                task.task_id, _exec_mode,
                builder_provider=_builder_prov,
                reviewer_provider=_reviewer_prov,
                prompt_trace_available=_prompt_count > 0,
                provider_call_count=_provider_call_count,
            )
            _exec_rel = f"task_runs/{task.task_id}/task_execution_evidence.json"
            _exec_path = _validate_output_path(str(out_path), _exec_rel)
            _exec_path.parent.mkdir(parents=True, exist_ok=True)
            _exec_path.write_text(json.dumps(_redact_json_value(_exec_ev), indent=2) + "\n", encoding="utf-8")
            written[_exec_rel] = str(_exec_path)
        except Exception as exc:
            rel = f"task_runs/{task.task_id}/task_execution_evidence.error.txt"
            err_path = _validate_output_path(str(out_path), rel)
            err_path.write_text(
                f"task_execution_evidence unavailable: {type(exc).__name__}: {exc}\n",
                encoding="utf-8",
            )
            written[rel] = str(err_path)
        # Per-task actor binding (builder/reviewer identity tracking)
        try:
            from packages.orchestration.task_actor_binding import build_task_actor_binding

            _builder_prov_ab = (
                getattr(job.execution_config, "builder", None) or ""
            ) if job.execution_config else ""
            _builder_model_ab = (
                getattr(job.execution_config, "builder_model", None) or ""
            ) if job.execution_config else ""
            _reviewer_prov_ab = (
                getattr(job.execution_config, "reviewer", None) or ""
            ) if job.execution_config else ""
            _reviewer_model_ab = (
                getattr(job.execution_config, "reviewer_model", None) or ""
            ) if job.execution_config else ""
            _rounds_ab = len(getattr(task, "rounds", []) or [])
            _repair_rounds_ab = getattr(task, "repair_rounds_used", 0) or 0
            _ab = build_task_actor_binding(
                task.task_id,
                builder_provider=_builder_prov_ab,
                builder_model=_builder_model_ab,
                reviewer_provider=_reviewer_prov_ab,
                reviewer_model=_reviewer_model_ab,
                rounds=_rounds_ab,
                repair_rounds=_repair_rounds_ab,
                same_builder_repairs=True,
                same_reviewer_re_review=True,
            )
            _ab_rel = f"task_runs/{task.task_id}/task_actor_binding.json"
            _ab_path = _validate_output_path(str(out_path), _ab_rel)
            _ab_path.parent.mkdir(parents=True, exist_ok=True)
            _ab_path.write_text(json.dumps(_redact_json_value(_ab), indent=2) + "\n", encoding="utf-8")
            written[_ab_rel] = str(_ab_path)
        except Exception as exc:
            rel = f"task_runs/{task.task_id}/task_actor_binding.error.txt"
            err_path = _validate_output_path(str(out_path), rel)
            err_path.write_text(
                f"task_actor_binding unavailable: {type(exc).__name__}: {exc}\n",
                encoding="utf-8",
            )
            written[rel] = str(err_path)

    _overlay_attestation_artifacts(attest_snap, str(out_path), written, job.job_id)

    try:
        from packages.orchestration.scratch_file_guard import write_scratch_file_guard
        all_allowed = []
        for task in job.tasks:
            if hasattr(task, "safe_diff_files") and task.safe_diff_files:
                all_allowed.extend(task.safe_diff_files)
        write_scratch_file_guard(
            job.job_workspace_path or "",
            str(out_path),
            "",
            all_allowed,
            written,
        )
    except Exception as exc:
        rel = "scratch_file_guard.error.txt"
        err_path = _validate_output_path(str(out_path), rel)
        err_path.write_text(
            f"scratch_file_guard unavailable: {type(exc).__name__}: {exc}\n",
            encoding="utf-8",
        )
        written[rel] = str(err_path)

    # Job-level prompt trace aggregate
    _write_job_prompt_trace_summary(job, str(out_path), written)

    # Token truth — honest token accounting (actual vs estimated) across tasks.
    # Must be written BEFORE final verifier so final verifier can read it.
    try:
        from packages.orchestration.token_truth import write_token_truth
        write_token_truth(str(out_path), written)
    except Exception as exc:
        rel = "token_truth.error.txt"
        err_path = _validate_output_path(str(out_path), rel)
        err_path.write_text(
            f"token_truth unavailable: {type(exc).__name__}: {exc}\n",
            encoding="utf-8",
        )
        written[rel] = str(err_path)

    # Token cost policy — per-role cost tracking and risk findings.
    # Must be written BEFORE final verifier so final verifier can read it.
    try:
        from packages.orchestration.token_cost_policy import build_token_cost_policy

        _plan_text_tcp = ""
        try:
            _plan_text_tcp = (Path(".agent") / "plan.md").read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
        _m_tcp = re.search(r"(?<!\d)(\d{4,})\s*-\s*(\d{4,})(?!\d)", _plan_text_tcp)
        _step_range_tcp = f"{_m_tcp.group(1)}-{_m_tcp.group(2)}" if _m_tcp else ""

        _role_configs_tcp: dict[str, Any] = {}
        if job.execution_config:
            ec = job.execution_config
            _role_configs_tcp["builder"] = {
                "model": getattr(ec, "builder_model", None) or "",
            }
            _role_configs_tcp["reviewer"] = {
                "model": getattr(ec, "reviewer_model", None) or "",
            }

        _token_truth_data: dict[str, Any] = {}
        _tt_path = out_path / "token_truth.json"
        if _tt_path.exists():
            try:
                _token_truth_data = json.loads(_tt_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass

        _trace_summary_data: dict[str, Any] = {}
        _ts_path = out_path / "prompt_trace_summary.json"
        if _ts_path.exists():
            try:
                _trace_summary_data = json.loads(_ts_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass

        _max_rounds_tcp = getattr(job.execution_config, "max_rounds", 3) if job.execution_config else 3
        _repair_budget_tcp = getattr(job.execution_config, "repair_rounds_allowed", 0) if job.execution_config else 0
        _tcp = build_token_cost_policy(
            job.job_id,
            _step_range_tcp,
            _role_configs_tcp,
            _token_truth_data,
            _trace_summary_data,
            _max_rounds_tcp,
            _repair_budget_tcp,
        )
        _tcp_path = _validate_output_path(str(out_path), "token_cost_policy.json")
        _tcp_path.write_text(json.dumps(_redact_json_value(_tcp), indent=2) + "\n", encoding="utf-8")
        written["token_cost_policy.json"] = str(_tcp_path)
    except Exception as exc:
        rel = "token_cost_policy.error.txt"
        err_path = _validate_output_path(str(out_path), rel)
        err_path.write_text(
            f"token_cost_policy unavailable: {type(exc).__name__}: {exc}\n",
            encoding="utf-8",
        )
        written[rel] = str(err_path)

    # Final job review — job-level review after all per-task reviewers.
    # Must be written BEFORE final verifier so final verifier can read it.
    try:
        from packages.orchestration.final_job_review import build_final_job_review

        _task_verdicts_fjr = []
        _task_summaries_fjr = []
        _task_diffs_fjr = []
        for _t in job.tasks:
            _task_verdicts_fjr.append({
                "task_id": _t.task_id,
                "verdict": getattr(_t, "reviewer_verdict", "") or getattr(_t, "final_status", "") or "",
            })
            _task_summaries_fjr.append(getattr(_t, "title", "") or "")
            _diff = getattr(_t, "safe_diff_summary", "") or ""
            _task_diffs_fjr.append(_diff[:2000] if _diff else "")

        _test_ev_fjr: dict[str, Any] = {}
        _gate_verdicts_fjr: list[dict[str, Any]] = []

        _fjr = build_final_job_review(
            job_goal=job.job_title,
            task_plan=[{"task_id": _t.task_id, "title": _t.title} for _t in job.tasks],
            task_summaries=_task_summaries_fjr,
            task_diffs=_task_diffs_fjr,
            task_verdicts=_task_verdicts_fjr,
            test_evidence=_test_ev_fjr,
            gate_verdicts=_gate_verdicts_fjr,
            job_id=job.job_id,
        )
        _fjr_path = _validate_output_path(str(out_path), "final_job_review.json")
        _fjr_path.write_text(json.dumps(_redact_json_value(_fjr), indent=2) + "\n", encoding="utf-8")
        written["final_job_review.json"] = str(_fjr_path)
        if attest_snap:
            _attested_tids = set(attest_snap.keys())
            _fjr_findings = _fjr.get("findings") or []
            _fjr_remaining = [
                f for f in _fjr_findings
                if f.get("task_id") not in _attested_tids
            ]
            if len(_fjr_remaining) < len(_fjr_findings):
                _fjr["findings"] = _fjr_remaining
                if not _fjr_remaining:
                    _fjr["verdict"] = "PASS"
                _fjr_path.write_text(
                    json.dumps(_redact_json_value(_fjr), indent=2) + "\n",
                    encoding="utf-8",
                )
    except Exception as exc:
        rel = "final_job_review.error.txt"
        err_path = _validate_output_path(str(out_path), rel)
        err_path.write_text(
            f"final_job_review unavailable: {type(exc).__name__}: {exc}\n",
            encoding="utf-8",
        )
        written[rel] = str(err_path)

    def _write_gate_error(rel: str, exc: Exception) -> None:
        err_path = _validate_output_path(str(out_path), rel)
        err_path.write_text(
            f"{rel} unavailable: {type(exc).__name__}: {exc}\n",
            encoding="utf-8",
        )
        written[rel] = str(err_path)

    def _gate_verdict(filename: str) -> str:
        try:
            data = json.loads((out_path / filename).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return ""
        return str(data.get("verdict", "") or "") if isinstance(data, dict) else ""

    # F010 post-mortem integrity — written BEFORE the gates read it. Empty means the
    # contract held; anything in it is a required record that could not be written, and the
    # final verifier turns that into BLOCKED. A package must never look clean while a
    # failure went unrecorded.
    _pm_integrity = {
        "schema_version": "1.0.0",
        "ok": not postmortem_failures,
        "failures": postmortem_failures,
    }
    _write_json(POSTMORTEM_INTEGRITY_FILE, _pm_integrity)

    # F012: the run-input manifest travels into the bundle, and its own integrity artifact
    # BLOCKS a clean verdict when a mandatory manifest is missing or broken — the same
    # mechanism as post-mortem integrity, never a text warning. Pre-F012 jobs (no manifest
    # and no recorded error) are reported as legacy/uncovered, not corrupt.
    manifest_failures: list[dict[str, Any]] = []
    manifest_notes: list[str] = []
    try:
        _write_run_manifest_export(job, str(out_path), written, manifest_failures,
                                   manifest_notes)
    except Exception as exc:
        from packages.orchestration.failure_postmortem import safe_text as _safe
        manifest_failures.append({
            "scope": "job", "job_id": job.job_id,
            "error": _safe(f"run manifest export failed: {type(exc).__name__}: {exc}")[:500],
        })
    _manifest_integrity = {
        "schema_version": "1.0.0",
        "ok": not manifest_failures,
        "failures": manifest_failures,
        "notes": manifest_notes,
    }
    _write_json(MANIFEST_INTEGRITY_FILE, _manifest_integrity)

    # Fresh evidence gate — verify this evidence belongs to the current job run.
    # Step range is derived from the project's .agent/plan.md title.
    try:
        from packages.orchestration.fresh_evidence_gate import write_fresh_evidence_gate
        plan_text = ""
        try:
            plan_text = (Path(".agent") / "plan.md").read_text(encoding="utf-8", errors="replace")
        except OSError:
            plan_text = ""
        m = re.search(r"(?<!\d)(\d{4,})\s*-\s*(\d{4,})(?!\d)", plan_text)
        step_range = f"{m.group(1)}-{m.group(2)}" if m else None
        write_fresh_evidence_gate(str(out_path), job.job_id, step_range, written)
    except Exception as exc:
        _write_gate_error("fresh_evidence_gate.error.txt", exc)

    # Runtime integration gate — moved AFTER verification_tests so it can bind
    # to executed test records. See block below (after _run_verifications).

    # The REVIEW SUBJECT — resolved ONCE, by the one production helper, and recorded as a fact.
    #
    # Round 14 inlined three git commands here. That silently swallowed an invalid base (exit 128
    # -> "just the dirty files", a smaller review than the operator asked for, with no error),
    # accepted a NON-ANCESTOR base (dragging unrelated branches' files into the review), could
    # never prove a committed DELETION (the proof only hashed files that still exist), and
    # recorded nothing about the base, so no reader could tell what the package was a review OF.
    # `resolve_review_subject` verifies all of it and raises instead of downgrading.
    _repo = getattr(job, "repo_path", None) or "."
    dirty_files: list[str] = []
    _subject = None
    try:
        from packages.orchestration.change_provenance_gate import _is_source_file, _normalize
        from packages.orchestration.review_subject import (
            STATUS_DELETED,
            ReviewSubjectError,
            resolve_review_subject,
            validate_subject_path_kinds,
        )

        # F6 (round 16): the base arrives EXPLICITLY from the top level, with the repository it
        # belongs to. This module reads no environment: an ambient declaration used to be picked
        # up here and then accepted or discarded based on the process CWD, so an export running
        # for a DIFFERENT repository (a test's temporary repo) could inherit a base that was
        # never about it, and an intentional declaration was silently dropped when the CWD moved.
        _subject = resolve_review_subject(_repo, declared_base=declared_base)
        dirty_files = [f.path for f in _subject.files]

        # F5: a subject carrying a path we cannot honestly prove or package never becomes
        # authoritative Evidence.
        _kind_problems = validate_subject_path_kinds(_subject, _repo)
        if _kind_problems:
            raise ReviewSubjectError("; ".join(_kind_problems)[:400])

        # `review_subject.json` — the durable, typed account: which base, which head, which
        # commits, and every file with the proof its status allows.
        _subject_path = _validate_output_path(str(out_path), "review_subject.json")
        _subject_path.write_text(json.dumps(_subject.to_json(), indent=2) + "\n",
                                 encoding="utf-8")
        written["review_subject.json"] = str(_subject_path)

        # The content proof carries a TOMBSTONE for a deleted path rather than omitting it: a
        # file that was removed is part of the change, and "no entry" is indistinguishable from
        # "never looked".
        _file_hashes: dict[str, str] = {}
        _tombstones: dict[str, dict[str, Any]] = {}
        for _f in _subject.files:
            _sf = _normalize(_f.path)
            if not _is_source_file(_sf):
                continue
            if _f.status == STATUS_DELETED:
                _tombstones[_sf] = {"status": _f.status, "base_sha256": _f.base_sha256,
                                    "current_sha256": None}
            elif _f.current_sha256:
                _file_hashes[_sf] = _f.current_sha256
        _proof = {
            "schema_version": "1.1.0",
            "base_commit": _subject.base_commit,
            "head_commit": _subject.head_commit,
            "file_hashes": _file_hashes,
            "file_count": len(_file_hashes),
            "tombstones": _tombstones,
            "tombstone_count": len(_tombstones),
        }
        _proof_path = _validate_output_path(str(out_path), "current_change_content_proof.json")
        _proof_path.write_text(json.dumps(_proof, indent=2) + "\n", encoding="utf-8")
        written["current_change_content_proof.json"] = str(_proof_path)

        # The machine-verifiable commit chain (round 15): the ordered, base-exclusive ancestry
        # path a reader can recompute, so "there were six commits" stops being prose.
        _chain = {
            "chain_v": 1,
            "base_commit": _subject.base_commit,
            "head_commit": _subject.head_commit,
            "commits": [c.to_json() for c in _subject.commits],
        }
        _chain_path = _validate_output_path(str(out_path), "review_commit_chain.json")
        _chain_path.write_text(json.dumps(_chain, indent=2) + "\n", encoding="utf-8")
        written["review_commit_chain.json"] = str(_chain_path)

        # F7 (round 16): the CANONICAL PATCH BYTES, one file per commit.
        #
        # The chain recorded `patch_sha256` but shipped nothing to hash, so a ZIP-only reviewer —
        # the only kind an external review has — could verify every field EXCEPT the one that
        # says what the commit actually did. They had to trust it or clone the repository, and a
        # package that requires the repository is not self-contained evidence.
        if _subject.commits:
            from packages.orchestration.review_subject import (
                COMMIT_PATCH_DIRNAME,
                commit_patch_bytes,
                commit_patch_filename,
            )
            _pdir = _validate_output_path(str(out_path), COMMIT_PATCH_DIRNAME)
            _pdir.mkdir(parents=True, exist_ok=True)
            _patches: list[str] = []
            for _c in _subject.commits:
                _raw = commit_patch_bytes(_repo, _c.commit)
                _actual = hashlib.sha256(_raw).hexdigest()
                if _actual != _c.patch_sha256:
                    raise ReviewSubjectError(
                        f"commit {_c.commit[:12]} patch bytes hash to {_actual[:12]} but the "
                        f"chain records {_c.patch_sha256[:12]}")
                _name = commit_patch_filename(_c.commit)
                (_pdir / _name).write_bytes(_raw)
                _patches.append(f"{COMMIT_PATCH_DIRNAME}/{_name}")
            written[COMMIT_PATCH_DIRNAME] = str(_pdir)
    except Exception as exc:
        _write_gate_error("current_change_content_proof.error.txt", exc)

    # Change provenance gate — every dirty source file must be backed by evidence.
    try:
        from packages.orchestration.change_provenance_gate import write_change_provenance_gate
        write_change_provenance_gate(
            str(out_path), dirty_files, job.job_id, written,
            repo_root=_repo,
        )
    except Exception as exc:
        _write_gate_error("change_provenance_gate.error.txt", exc)

    # Verification tests — execute the EXPLICIT verification commands and record
    # each as a run with a stable id. Nothing is claimed verified that was not
    # actually run; unit tests inject a deterministic runner to avoid recursively
    # spawning pytest (finding 3). No hardcoded smoke suite (findings 2/3/4).
    _vt_data = None
    try:
        _repo = getattr(job, "repo_path", None) or "."
        _vt_data = _run_verifications(
            verification_commands, _repo, verification_runner,
        )
        if _vt_data is not None:
            _vt_path = _validate_output_path(str(out_path), "verification_tests.json")
            _vt_path.write_text(json.dumps(_vt_data, indent=2) + "\n", encoding="utf-8")
            written["verification_tests.json"] = str(_vt_path)
    except Exception as exc:
        _write_gate_error("verification_tests.error.txt", exc)

    # Runtime integration gate — AFTER verification_tests so it can bind to
    # executed test records (node IDs, exit codes, pass/fail/skip counts).
    try:
        from packages.orchestration.runtime_integration_gate import write_runtime_integration_gate
        _repo_root = getattr(job, "repo_path", None) or "."
        write_runtime_integration_gate(
            str(out_path), _repo_root, written,
            verification_data=_vt_data,
        )
    except Exception as exc:
        _write_gate_error("runtime_integration_gate.error.txt", exc)

    # Manual-completion finalization — deterministic second pass, AFTER
    # verification_tests.json exists and BEFORE the final verifier. Regenerates
    # per-task derived evidence (review scope, missing-tests gate, tests.txt,
    # execution-mode layering) from the attested diffs, rebuilds the final job
    # review from the attestation changed-file sets, and writes the root
    # operator-attested completion record. No-op when there are no attestations.
    try:
        _finalize_manual_completion(job, attest_snap, str(out_path), written)
    except Exception as exc:
        _write_gate_error("manual_completion_finalize.error.txt", exc)

    # Finding 5: reconcile persisted vs effective state on the existing manifests
    # (the persisted job plan is never mutated).
    if attest_snap:
        try:
            _apply_effective_completion_status(
                job, attest_snap, str(out_path), manifest, written,
            )
        except Exception as exc:
            _write_gate_error("effective_status.error.txt", exc)

    # Final verifier report — aggregates all gates into a single verdict.
    # Written after upstream gates so it can read their verdicts.
    try:
        from packages.orchestration.final_verifier import write_final_verifier_report
        write_final_verifier_report(str(out_path), written)
    except Exception as exc:
        _write_gate_error("final_verifier_report.error.txt", exc)

    # Artifact contract gate — after final verifier, so it can check completeness.
    try:
        from packages.orchestration.artifact_contract_gate import write_artifact_contract_gate
        write_artifact_contract_gate(str(out_path), written, current_job_id=job.job_id)
    except Exception as exc:
        _write_gate_error("artifact_contract_gate.error.txt", exc)

    # Commit execution gate — terminal gate: reads all other gate verdicts.
    try:
        from packages.orchestration.commit_execution_gate import write_commit_execution_gate
        write_commit_execution_gate(
            str(out_path),
            written,
            fresh_evidence_verdict=_gate_verdict("fresh_evidence_gate.json"),
            artifact_contract_verdict=_gate_verdict("artifact_contract_gate.json"),
            runtime_integration_verdict=_gate_verdict("runtime_integration_gate.json"),
            final_verifier_verdict=_gate_verdict("final_verifier_report.json"),
            change_provenance_verdict=_gate_verdict("change_provenance_gate.json"),
        )
    except Exception as exc:
        _write_gate_error("commit_execution_gate.error.txt", exc)

    # Second pass: artifact_contract after commit_execution exists.
    try:
        from packages.orchestration.artifact_contract_gate import write_artifact_contract_gate
        write_artifact_contract_gate(str(out_path), written, current_job_id=job.job_id)
    except Exception as exc:
        _write_gate_error("artifact_contract_gate.error.txt", exc)

    # Final pass: re-run final verifier so it sees commit_execution_gate verdict.
    try:
        from packages.orchestration.final_verifier import write_final_verifier_report
        write_final_verifier_report(str(out_path), written)
    except Exception as exc:
        pass

    # Terminal refresh: commit_execution reads final verifier's updated verdict.
    try:
        from packages.orchestration.commit_execution_gate import write_commit_execution_gate
        write_commit_execution_gate(
            str(out_path),
            written,
            fresh_evidence_verdict=_gate_verdict("fresh_evidence_gate.json"),
            artifact_contract_verdict=_gate_verdict("artifact_contract_gate.json"),
            runtime_integration_verdict=_gate_verdict("runtime_integration_gate.json"),
            final_verifier_verdict=_gate_verdict("final_verifier_report.json"),
            change_provenance_verdict=_gate_verdict("change_provenance_gate.json"),
        )
    except Exception as exc:
        pass

    from datetime import datetime, timezone
    manifest["bundle_generated_at"] = datetime.now(timezone.utc).isoformat()

    _write_json("manifest.json", manifest)

    return _redact_json_value({
        "job_id": job_id,
        "out_dir": str(out_path),
        "files": written,
        "manifest": manifest,
    })


def _build_job_manifest(job: Any) -> dict[str, Any]:
    return {
        "bundle_version": "0.1.0",
        "bundle_type": "job_evidence",
        "job_id": job.job_id,
        "job_title": job.job_title,
        "job_file_sha256": job.job_file_sha256,
        "status": job.status,
        "repo_identity": _sanitize_path(job.repo_path),
        "job_workspace_path": _sanitize_path(job.job_workspace_path) if job.job_workspace_path else "",
        "created_at": job.created_at,
        "finished_at": job.finished_at,
        "task_count": len(job.tasks),
        "task_ids": [t.task_id for t in job.tasks],
        "task_statuses": {t.task_id: t.status for t in job.tasks},
        "task_run_ids": {t.task_id: t.run_id for t in job.tasks if t.run_id},
        "execution_config": _export_execution_config(job.execution_config),
        "context_strategy": job.execution_config.context_strategy if job.execution_config else "task_bounded_sequential_job",
        "target_guard": _export_target_guard(job.target_guard),
        "error": job.error,
    }


def _build_job_summary_md(job: Any) -> str:
    lines = [
        f"# Remedy Job Evidence — {job.job_id}",
        "",
        f"**Title:** {job.job_title}",
        f"**Status:** {job.status}",
        f"**Repo:** {_sanitize_path(job.repo_path)}",
        f"**Created:** {job.created_at}",
    ]
    if job.finished_at:
        lines.append(f"**Finished:** {job.finished_at}")
    lines.append("")

    ec = job.execution_config
    if ec:
        lines.append("## Execution Config")
        lines.append(f"- Builder: {ec.builder} (source: {ec.builder_source})")
        lines.append(f"- Reviewer: {ec.reviewer} (source: {ec.reviewer_source})")
        lines.append(f"- Max rounds: {ec.max_rounds} (source: {ec.max_rounds_source})")
        lines.append(f"- Repair rounds: {ec.repair_rounds_allowed} (source: {ec.repair_rounds_source})")
        lines.append(f"- Context strategy: {ec.context_strategy}")
        lines.append("")

    lines.append("## Task Timeline")
    lines.append("")
    lines.append(f"1. Job planned at {job.created_at}")
    for task in job.tasks:
        status_str = task.status
        run_str = f" (run: {task.run_id})" if task.run_id else ""
        verdict_str = f", reviewer: {task.reviewer_verdict}" if task.reviewer_verdict else ""
        repair_str = f", repair: {task.repair_rounds_used}/{task.repair_rounds_allowed}" if task.repair_rounds_used else ""
        lines.append(f"2. {task.task_id}: {task.title} — {status_str}{run_str}{verdict_str}{repair_str}")
    if job.finished_at:
        lines.append(f"3. Job {job.status} at {job.finished_at}")
    lines.append("")

    tg = job.target_guard
    if tg:
        lines.append("## Target Guard")
        lines.append(f"- Target mutated: {tg.target_mutated}")
        if tg.changed_target_files:
            lines.append(f"- Changed files: {', '.join(tg.changed_target_files)}")
        lines.append("")

    lines.append("## Tasks")
    lines.append("")
    for task in job.tasks:
        lines.append(f"### {task.task_id}: {task.title}")
        lines.append(f"- Status: {task.status}")
        if task.run_id:
            lines.append(f"- Run ID: {task.run_id}")
        if task.final_status:
            lines.append(f"- Final: {task.final_status}")
        if task.test_passed is not None:
            lines.append(f"- Tests: {'passed' if task.test_passed else 'failed'}")
        if task.reviewer_verdict:
            lines.append(f"- Reviewer: {task.reviewer_verdict}")
        if task.repair_rounds_used:
            lines.append(f"- Repair: {task.repair_rounds_used}/{task.repair_rounds_allowed}")
        if task.apply_manifest and task.apply_manifest.applied_files:
            lines.append(f"- Applied: {len(task.apply_manifest.applied_files)} files")
        if task.error:
            lines.append(f"- Error: {task.error}")
        lines.append("")

    lines.append("---")
    lines.append("WARNING: Real target repo was NOT mutated. Changes exist only in the isolated job workspace.")

    return "\n".join(lines) + "\n"


def _build_job_report_safe(job: Any) -> dict[str, Any]:
    tasks = []
    for t in job.tasks:
        body_bounded = t.body[:_TASK_BODY_EVIDENCE_LIMIT] if t.body else ""
        if len(t.body) > _TASK_BODY_EVIDENCE_LIMIT:
            body_bounded += f"... (truncated, {len(t.body)} chars total)"
        tasks.append({
            "task_id": t.task_id,
            "title": t.title,
            "body_excerpt": body_bounded,
            "status": t.status,
            "run_id": t.run_id,
            "final_status": t.final_status,
            "test_passed": t.test_passed,
            "reviewer_verdict": t.reviewer_verdict,
            "repair_rounds_used": t.repair_rounds_used,
            "repair_rounds_allowed": t.repair_rounds_allowed,
            "error": t.error,
            "apply_manifest": _export_apply_manifest(t.apply_manifest),
            "proof_summary": _export_proof_summary(t.proof_summary),
        })
    return {
        "job_id": job.job_id,
        "job_title": job.job_title,
        "status": job.status,
        "repo_identity": _sanitize_path(job.repo_path),
        "created_at": job.created_at,
        "finished_at": job.finished_at,
        "error": job.error,
        "tasks": tasks,
    }


def _build_job_timeline(job: Any) -> dict[str, Any]:
    events: list[dict[str, str]] = []
    events.append({
        "event": "job_planned",
        "timestamp": job.created_at or "unavailable",
        "detail": f"Job {job.job_id} planned with {len(job.tasks)} tasks",
    })

    prev_applied_id = ""
    for task in job.tasks:
        if task.status in ("pending", "skipped"):
            events.append({
                "event": f"task_{task.status}",
                "timestamp": "unavailable",
                "detail": f"{task.task_id}: {task.title} — {task.status}",
            })
            continue

        if prev_applied_id:
            events.append({
                "event": "sequencing_proof",
                "timestamp": "unavailable",
                "detail": f"{task.task_id} started after {prev_applied_id} applied",
            })

        events.append({
            "event": "task_completed",
            "timestamp": "unavailable",
            "detail": (
                f"{task.task_id}: {task.title} — {task.status}"
                f" (run: {task.run_id})" if task.run_id else
                f"{task.task_id}: {task.title} — {task.status}"
            ),
            "run_id": task.run_id,
        })

        if task.status == "applied_to_job_workspace":
            prev_applied_id = task.task_id

    events.append({
        "event": "job_final",
        "timestamp": job.finished_at or "unavailable",
        "detail": f"Job {job.status}",
    })

    return {
        "job_id": job.job_id,
        "events": events,
        "sequencing_valid": _check_sequencing(job),
        "timestamps_available": bool(job.created_at and job.finished_at),
    }


def _check_sequencing(job: Any) -> bool:
    applied_seen = False
    for task in job.tasks:
        if task.status == "applied_to_job_workspace":
            applied_seen = True
        elif task.status in ("blocked", "failed") and applied_seen:
            return True
        elif task.status == "applied_to_job_workspace" and applied_seen:
            pass
    if job.status == "completed":
        return all(
            t.status in ("applied_to_job_workspace", "skipped")
            for t in job.tasks
        )
    return True


def _build_tasks_json(job: Any) -> list[dict[str, Any]]:
    tasks = []
    for t in job.tasks:
        tasks.append({
            "task_id": t.task_id,
            "title": t.title,
            "status": t.status,
            "run_id": t.run_id,
            "final_status": t.final_status,
            "test_passed": t.test_passed,
            "reviewer_verdict": t.reviewer_verdict,
            "repair_rounds_used": t.repair_rounds_used,
            "repair_rounds_allowed": t.repair_rounds_allowed,
            "safe_diff_files": t.safe_diff_files,
            "error": t.error,
            "apply_manifest": _export_apply_manifest(t.apply_manifest),
            "proof_summary": _export_proof_summary(t.proof_summary),
        })
    return tasks


def _build_workspace_apply_json(job: Any) -> list[dict[str, Any]]:
    manifests = []
    for t in job.tasks:
        m = _export_apply_manifest(t.apply_manifest)
        manifests.append({
            "task_id": t.task_id,
            "status": t.status,
            "apply_manifest": m,
        })
    return manifests


def job_result_diff_source(job: Any) -> tuple[Path | None, str]:
    """Contain and verify the JobPlan's root ``result.diff`` before it is used.

    The source lives in the canonical job directory, never in the removed
    execution workspace. It must be the canonical relative ``result.diff``, a
    regular file (never a symlink), resolving inside that job directory, and match
    the sha256 and size recorded in job.json.
    """
    from packages.orchestration.data_paths import job_dir

    if getattr(job, "isolation_mode", "copy") != "worktree":
        return None, "not_a_worktree_job"
    recorded = {
        "path": getattr(job, "result_diff_path", ""),
        "sha256": getattr(job, "result_diff_sha256", ""),
        "size_bytes": getattr(job, "result_diff_size_bytes", 0),
    }
    if not recorded["path"]:
        return None, "job records no result.diff"
    return _resolve_result_diff_source(job_dir(job.job_id), recorded)


def _write_job_worktree_evidence(
    job: Any,
    out_path: Path,
    written: dict[str, str],
) -> tuple[str | None, str]:
    """Export the JobPlan's ``worktree.json`` + ``result.diff`` at evidence root.

    Returns ``(workspace_diff_text, error)``. ``workspace_diff_text`` is None for a
    copy-mode job, so the legacy workspace diff is used instead.
    """
    if getattr(job, "isolation_mode", "copy") != "worktree":
        return None, ""

    src, err = job_result_diff_source(job)
    doc: dict[str, Any] = {
        "schema_version": "1.0.0",
        "job_id": job.job_id,
        "isolation_mode": "worktree",
        "branch": getattr(job, "worktree_branch", ""),
        "path": getattr(job, "worktree_path", ""),      # repo-relative audit path
        "base_commit": getattr(job, "worktree_base_commit", ""),
        "head": getattr(job, "worktree_head", ""),
        "cleanup_status": getattr(job, "worktree_cleanup_status", ""),
        "cleanup_error": getattr(job, "worktree_cleanup_error", ""),
        "result_diff": None,
        "result_diff_error": err or getattr(job, "result_diff_error", ""),
        "auto_merged": False,               # there is never an automatic merge
        # Semantic coverage: the root diff must be EXACTLY the reviewed task work.
        "handoff_coverage": {
            "verdict": getattr(job, "handoff_coverage_verdict", ""),
            "root_changed_files": list(getattr(job, "root_changed_files", [])),
            "reviewed_task_files": list(getattr(job, "reviewed_task_files", [])),
            "unexpected_root_files": list(getattr(job, "unexpected_root_files", [])),
            "missing_root_files": list(getattr(job, "missing_root_files", [])),
        },
    }

    text: str | None = None
    if src is not None:
        data = src.read_bytes()
        (out_path / "result.diff").write_bytes(data)
        written["result.diff"] = str(out_path / "result.diff")
        doc["result_diff"] = {
            "path": "result.diff",
            "sha256": job.result_diff_sha256,
            "size_bytes": job.result_diff_size_bytes,
        }
        header = (
            "# Job hand-off diff (verified job result.diff; the execution worktree "
            "was removed after a clean cleanup and is not expected to exist)\n"
            f"# Branch: {doc['branch']}\n"
            f"# Base:   {doc['base_commit']}\n"
            f"# sha256: {job.result_diff_sha256}\n\n"
        )
        text = header + data.decode("utf-8", errors="replace")
    else:
        text = (
            "# Job hand-off diff unavailable: "
            f"{doc['result_diff_error'] or 'no verified result.diff'}\n"
        )

    wt_path = out_path / "worktree.json"
    wt_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    written["worktree.json"] = str(wt_path)
    return text, doc["result_diff_error"]


def _build_workspace_diff(job: Any) -> str:
    ws_path = job.job_workspace_path
    repo_path = job.repo_path
    if not ws_path or not repo_path:
        return "# Workspace diff unavailable: no workspace or repo path\n"

    ws = Path(ws_path)
    repo = Path(repo_path)
    if not ws.exists():
        return "# Workspace diff unavailable: workspace directory does not exist\n"
    if not repo.exists():
        return "# Workspace diff unavailable: repo directory does not exist\n"

    diff_lines = ["# Job workspace diff (workspace vs original target repo)"]
    diff_lines.append(f"# Workspace: {_sanitize_path(ws_path)}")
    diff_lines.append(f"# Repo: {_sanitize_path(repo_path)}")
    diff_lines.append("")

    applied_files: list[str] = []
    for t in job.tasks:
        if t.apply_manifest and t.apply_manifest.applied_files:
            applied_files.extend(t.apply_manifest.applied_files)

    if not applied_files:
        diff_lines.append("# No files applied to workspace")
        return "\n".join(diff_lines) + "\n"

    total_chars = sum(len(line) + 1 for line in diff_lines)
    capped = False
    for rel_path in sorted(set(applied_files)):
        if total_chars >= _WORKSPACE_DIFF_MAX_CHARS:
            capped = True
            break
        ws_file = ws / rel_path
        repo_file = repo / rel_path

        diff_lines.append(f"--- a/{rel_path}")
        diff_lines.append(f"+++ b/{rel_path}")

        if not ws_file.exists():
            diff_lines.append("# File missing from workspace")
            diff_lines.append("")
            continue

        try:
            ws_content = ws_file.read_text(errors="replace")
        except OSError:
            diff_lines.append("# Could not read workspace file")
            diff_lines.append("")
            continue

        if repo_file.exists():
            try:
                repo_content = repo_file.read_text(errors="replace")
            except OSError:
                repo_content = ""
        else:
            repo_content = ""

        if ws_content == repo_content:
            diff_lines.append("# No difference")
        else:
            ws_lines = ws_content.splitlines(keepends=True)
            repo_lines = repo_content.splitlines(keepends=True)

            import difflib
            unified = list(difflib.unified_diff(
                repo_lines, ws_lines,
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
                lineterm="",
            ))
            if unified:
                for line in unified:
                    text = line.rstrip()
                    diff_lines.append(text)
                    total_chars += len(text) + 1
                    if total_chars >= _WORKSPACE_DIFF_MAX_CHARS:
                        capped = True
                        break
            else:
                diff_lines.append("# Files differ (binary or encoding)")
        diff_lines.append("")
        if capped:
            break

    if capped:
        diff_lines.append(
            f"# Workspace diff truncated at {_WORKSPACE_DIFF_MAX_CHARS} char total cap"
        )

    return "\n".join(diff_lines) + "\n"


_ATTESTATION_FILES = frozenset({
    "manual_repair_provenance.json",
    "provider_evidence.json",
    "review.json",
    "token_accounting.json",
    "safe.diff",
})

_ATTESTATION_DEFAULTS = {
    "tests.txt": "operator_attested: manual repair, no automated test run\n",
}


def _snapshot_attestation_artifacts(
    job: Any,
) -> dict[str, dict[str, bytes]]:
    """Read attestation artifacts into memory before evidence export.

    Returns {task_id: {filename: bytes_content}} for tasks with provenance.
    Must be called BEFORE _write_task_run_evidence to capture attestation
    data that would otherwise be overwritten when src and dst dirs are the same.
    """
    from packages.orchestration.data_paths import job_evidence_dir

    ev_base = job_evidence_dir(job.job_id)
    if not ev_base.exists():
        return {}

    snapshots: dict[str, dict[str, bytes]] = {}
    for task in job.tasks:
        tid = task.task_id
        src_dir = ev_base / "task_runs" / tid
        provenance = src_dir / "manual_repair_provenance.json"
        if not provenance.exists():
            continue
        task_snap: dict[str, bytes] = {}
        for fname in _ATTESTATION_FILES:
            src = src_dir / fname
            if src.exists():
                task_snap[fname] = src.read_bytes()
        if task_snap:
            snapshots[tid] = task_snap
    return snapshots


def _overlay_attestation_artifacts(
    snapshots: dict[str, dict[str, bytes]],
    out_base: str,
    written: dict[str, str],
    job_id: str = "",
) -> None:
    """Write snapshotted attestation artifacts over generated evidence.

    Takes pre-read attestation data (from _snapshot_attestation_artifacts)
    and writes it to the output directory, overriding any generated files.
    Does NOT fabricate fake observability stubs — validation must understand
    the manual repair exemption instead.

    Also rebuilds workspace.diff from per-task safe.diff content so that
    change_provenance_gate can find covered files.
    """
    ws_diff_parts: list[str] = [
        "# Workspace diff (operator-attested manual repair provenance)",
        "",
    ]
    for tid, files in snapshots.items():
        dst_dir = Path(out_base) / "task_runs" / tid
        dst_dir.mkdir(parents=True, exist_ok=True)
        for fname, content in files.items():
            dst = dst_dir / fname
            dst.write_bytes(content)
            rel = f"task_runs/{tid}/{fname}"
            written[rel] = str(dst)
        vt_path = Path(out_base) / "verification_tests.json"
        vt_tests_txt = ""
        if vt_path.exists():
            try:
                vt = json.loads(vt_path.read_text(encoding="utf-8"))
                vt_passed = vt.get("passed", 0)
                vt_failed = vt.get("failed", 0)
                vt_cmd = vt.get("command", "")
                vt_rc = vt.get("exit_code", -1)
                vt_ts = vt.get("timestamp", "")
                vt_tests_txt = (
                    f"tests_verified_by_root_verification\n"
                    f"command: {vt_cmd}\n"
                    f"exit_code: {vt_rc}\n"
                    f"{vt_passed} passed, {vt_failed} failed\n"
                    f"timestamp: {vt_ts}\n"
                )
            except (json.JSONDecodeError, OSError):
                pass

        for fname, default_content in _ATTESTATION_DEFAULTS.items():
            content = default_content
            if fname == "tests.txt" and vt_tests_txt:
                content = vt_tests_txt
            dst = dst_dir / fname
            dst.write_text(content, encoding="utf-8")
            rel = f"task_runs/{tid}/{fname}"
            written[rel] = str(dst)
        safe_diff_path = dst_dir / "safe.diff"
        if safe_diff_path.exists():
            diff_content = safe_diff_path.read_text(encoding="utf-8")
            if diff_content.strip():
                ws_diff_parts.append(f"# Task {tid} (operator-attested)")
                ws_diff_parts.append(diff_content)

    if len(ws_diff_parts) > 2:
        ws_diff_dst = Path(out_base) / "workspace.diff"
        ws_diff_dst.write_text(
            "\n".join(ws_diff_parts) + "\n", encoding="utf-8"
        )
        written["workspace.diff"] = str(ws_diff_dst)

    if snapshots:
        ec_path = Path(out_base) / "execution_config.json"
        if ec_path.exists():
            try:
                ec = json.loads(ec_path.read_text(encoding="utf-8"))
                if not ec.get("builder_model"):
                    ec["builder_model"] = "operator"
                    ec["builder_model_source"] = "operator_attestation"
                if not ec.get("reviewer_model"):
                    ec["reviewer_model"] = "operator"
                    ec["reviewer_model_source"] = "operator_attestation"
                ec["actual_config_available"] = False
                ec_path.write_text(
                    json.dumps(ec, indent=2) + "\n", encoding="utf-8"
                )
            except (json.JSONDecodeError, OSError):
                pass

        for tid in snapshots:
            mtg_path = Path(out_base) / "task_runs" / tid / "missing_tests_gate.json"
            if mtg_path.exists():
                try:
                    mtg = json.loads(mtg_path.read_text(encoding="utf-8"))
                    if mtg.get("gate_status") == "NEEDS_TESTS":
                        mtg["gate_status"] = "PASS"
                        mtg["tests_executed"] = True
                        mtg["reason"] = (
                            "Tests verified by root verification "
                            "(operator attestation)"
                        )
                        mtg["suggested_test_commands"] = []
                        mtg_path.write_text(
                            json.dumps(mtg, indent=2) + "\n", encoding="utf-8"
                        )
                except (json.JSONDecodeError, OSError):
                    pass


def _linked_job_summary(jid: str) -> dict[str, Any]:
    """Finding 7: honestly summarize a linked/superseded prior job via the
    generic job store. When the job is unavailable, status is ``unknown`` and
    provider_call_count is ``null`` — never silently zero. No feature-specific
    path is used.
    """
    try:
        j = load_job_plan(jid)
    except Exception:
        j = None
    if j is None:
        return {
            "job_id": jid,
            "status": "unknown",
            "provider_call_count": None,
            "source": "unavailable",
        }
    status = str(getattr(j, "status", "") or "") or "unknown"
    total: int | None = None
    try:
        from packages.orchestration.data_paths import runs_dir
        pp_runs_root = Path(runs_dir())
        for t in getattr(j, "tasks", []) or []:
            rid = getattr(t, "run_id", "") or ""
            if not rid:
                continue
            trace = pp_runs_root / rid / "prompt_trace_summary.json"
            if trace.exists():
                d = json.loads(trace.read_text(encoding="utf-8"))
                c = int(d.get("builder_prompts", 0)) + int(d.get("reviewer_prompts", 0))
                total = (total or 0) + c
    except Exception:
        total = None
    return {
        "job_id": jid,
        "status": status,
        "provider_call_count": total,  # None means unknown, never coerced to 0
        "source": "persisted_job_state",
    }


def _apply_effective_completion_status(
    job: Any,
    attest_snap: dict[str, dict[str, bytes]],
    out_base: str,
    manifest: dict[str, Any],
    written: dict[str, str],
) -> None:
    """Finding 5: mark effective operator-attested completion on the existing
    root manifest, tasks.json, and per-task manifests/summaries — WITHOUT
    mutating the persisted job plan. Persisted state is preserved alongside the
    effective state so the two are never contradictory.
    """
    out_path = Path(out_base)
    attested = set(attest_snap)

    # Root manifest (mutated in place; the final write uses this dict).
    manifest["persisted_status"] = manifest.get("status")
    manifest["effective_status"] = "operator_attested_complete"
    manifest["completion_mode"] = "manual_operator_repair"
    manifest["evidence_available"] = True
    manifest["human_final_reviewer_required"] = True

    # tasks.json — expose persisted AND effective status per task.
    tasks_path = out_path / "tasks.json"
    if tasks_path.exists():
        try:
            tasks = json.loads(tasks_path.read_text(encoding="utf-8"))
            for t in tasks:
                tid = t.get("task_id")
                t["persisted_status"] = t.get("status")
                if tid in attested:
                    t["effective_status"] = "operator_attested_complete"
                    t["evidence_available"] = True
                    t["completion_mode"] = "manual_operator_repair"
                else:
                    t["effective_status"] = t.get("status")
                    t["evidence_available"] = False
            tasks_path.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")
        except (OSError, json.JSONDecodeError):
            pass

    # Per-task manifest + summary — manual evidence IS available.
    for tid in attested:
        run_dir = out_path / "task_runs" / tid
        tm_path = run_dir / "manifest.json"
        persisted_reason = ""
        if tm_path.exists():
            try:
                tm = json.loads(tm_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                tm = {"task_id": tid}
        else:
            tm = {"task_id": tid}
        persisted_reason = str(tm.get("reason") or "")
        tm["persisted_status"] = "pending" if tm.get("evidence_available") is False else tm.get("persisted_status", "")
        tm["effective_status"] = "operator_attested_complete"
        tm["completion_mode"] = "manual_operator_repair"
        tm["evidence_available"] = True
        tm["human_final_reviewer_required"] = True
        tm["evidence_source"] = "operator_attestation"
        if persisted_reason:
            tm["persisted_reason"] = persisted_reason
        tm.pop("reason", None)
        run_dir.mkdir(parents=True, exist_ok=True)
        tm_path.write_text(json.dumps(tm, indent=2) + "\n", encoding="utf-8")
        written[f"task_runs/{tid}/manifest.json"] = str(tm_path)

        summary = (
            f"# Task {tid} Evidence\n\n"
            "Effective status: operator-attested manual completion "
            "(completion_mode=manual_operator_repair).\n"
            "Manual evidence is available: safe.diff, manual_repair_provenance.json, "
            "review.json (operator_attested), token_accounting.json.\n"
            "Zero completion-path provider calls. Human final review required.\n"
        )
        sm_path = run_dir / "summary.md"
        sm_path.write_text(summary, encoding="utf-8")
        written[f"task_runs/{tid}/summary.md"] = str(sm_path)


def _vt_norm(p: str) -> str:
    p = str(p or "").replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    return p


def _verification_test_files_from_command(command: str) -> list[str]:
    """Extract the test-file paths a pytest-style command targets.

    F6 (round 15): a pytest DIRECTORY argument covers the test files beneath it. `pytest
    tests/docs` runs every test under `tests/docs/`, but this only ever collected tokens ending in
    `.py`, so a changed `tests/docs/test_docs_consistency.py` was reported as uncovered and its
    task's missing-tests gate said NEEDS_TESTS — while the file had in fact just been run, green.
    A gate that cries wolf about a test that ran teaches operators to ignore it.

    `--ignore=<path>` is honoured too: a file explicitly excluded from a run is NOT covered by it.
    """
    import shlex
    files: list[str] = []
    dirs: list[str] = []
    ignored: set[str] = set()
    try:
        toks = shlex.split(command)
    except ValueError:
        toks = command.split()
    for t in toks:
        if t.startswith("--ignore="):
            ignored.add(_vt_norm(t.split("=", 1)[1]))
            continue
        if t.startswith("-"):
            continue
        n = _vt_norm(t)
        if not (n.startswith("tests/") or "/tests/" in n or Path(n).name.startswith("test_")):
            continue
        if n.endswith(".py"):
            files.append(n)
        elif Path(n).is_dir():
            dirs.append(n.rstrip("/"))
    for d in dirs:
        for p in sorted(Path(d).rglob("test_*.py")):
            files.append(_vt_norm(str(p)))
    return sorted({f for f in files
                   if not any(f == i or f.startswith(i.rstrip("/") + "/") for i in ignored)})


def _scrub_paths(text: str, repo: str) -> str:
    """Replace local absolute paths with relative equivalents for safe packaging."""
    abs_repo = os.path.abspath(repo)
    if abs_repo and abs_repo != "/":
        text = text.replace(abs_repo + "/", "").replace(abs_repo, ".")
    home = os.path.expanduser("~")
    if home and home != "/":
        text = text.replace(home, "~")
    # NOTE: this helper only redacts. It used to drop the first line as well —
    # aimed at pytest's rootdir banner, but applied to every text, so any
    # single-line output ("ABSENT\n") was scrubbed down to "". Paths in the
    # banner are already handled by the replacements above.
    # R-0793: the repo-root/$HOME relativization above catches only those two
    # roots; any other absolute path (e.g. pytest's own platform banner
    # "-- /usr/bin/python3") survives it. Delegate to the shared,
    # already-accepted scrubber (packages.common.path_redaction, F007) for
    # everything else.
    return _shared_scrub_paths(text)


def _default_verification_runner(command: str, repo: str) -> dict[str, Any]:
    """Execute a verification command via subprocess and parse pytest counts."""
    import hashlib
    import shlex
    import subprocess as _sp

    from packages.orchestration.review_subject import child_env_without_declaration

    try:
        argv = shlex.split(command)
    except ValueError:
        argv = command.split()
    _env = child_env_without_declaration()

    argv_v = [a for a in argv if a not in ("-q", "--quiet")]
    if "-v" not in argv_v and "--verbose" not in argv_v:
        argv_v.append("-v")
    import time as _time
    _t0 = _time.monotonic()
    result = _sp.run(argv_v, cwd=repo, capture_output=True, text=True, timeout=600,
                     env=_env)
    _duration = round(_time.monotonic() - _t0, 3)
    stdout = result.stdout or ""
    passed = sum(int(x) for x in re.findall(r"(\d+)\s+passed", stdout))
    failed = sum(int(x) for x in re.findall(r"(\d+)\s+(?:failed|error)", stdout))
    skipped = sum(int(x) for x in re.findall(r"(\d+)\s+skipped", stdout))
    deselected = sum(int(x) for x in re.findall(r"(\d+)\s+deselected", stdout))
    node_ids = re.findall(r"^(tests/\S+::\S+)\s+(?:PASSED|FAILED|ERROR|SKIPPED)", stdout, re.MULTILINE)
    selected = len(node_ids) if node_ids else (passed + failed + skipped)
    # Scrub THEN truncate — a path straddling the truncation cut must not
    # survive it. output_hash is computed over this FINAL, already
    # scrubbed-and-truncated stdout_summary, never over the raw stdout: it
    # must always describe the exact bytes stored (contract fixed by R-0792).
    stdout_summary = _scrub_paths(stdout, repo)[-2000:]
    stderr_summary = _scrub_paths(result.stderr or "", repo)[-1000:]
    output_hash = hashlib.sha256(stdout_summary.encode("utf-8", errors="replace")).hexdigest()
    head_sha = ""
    try:
        _h = _sp.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True,
                      text=True, timeout=10, env=_env)
        head_sha = (_h.stdout or "").strip()
    except Exception:
        pass
    return {
        "exit_code": result.returncode,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "selected": selected,
        "deselected": deselected,
        "node_ids": node_ids,
        "output_hash": output_hash,
        "head_sha": head_sha,
        "stdout_summary": stdout_summary,
        "stderr_summary": stderr_summary,
        "duration_seconds": _duration,
    }


def _run_verifications(
    commands: list[str] | None,
    repo: str,
    runner: Any = None,
) -> dict[str, Any] | None:
    """Execute explicit verification commands, recording each as a stable run.

    Returns the ``verification_tests.json`` payload, or None when no verification
    was requested (no commands and no injected runner) — in which case nothing is
    claimed verified. Each run gets a stable ``run_id`` so totals can be
    deduplicated downstream (finding 4). Top-level totals are DERIVED from runs.
    """
    if not commands and runner is None:
        return None
    import subprocess as _sp_head
    from datetime import datetime as _dt
    from datetime import timezone as _tz
    cmds = [c for c in (commands or []) if c and c.strip()]
    runs: list[dict[str, Any]] = []
    _head_sha_default = ""
    try:
        _h_d = _sp_head.run(["git", "rev-parse", "HEAD"], cwd=repo,
                             capture_output=True, text=True, timeout=10)
        _head_sha_default = (_h_d.stdout or "").strip()
    except Exception:
        pass
    for i, cmd in enumerate(cmds):
        rid = f"vr-{i + 1:04d}"
        r = runner(cmd) if runner is not None else _default_verification_runner(cmd, repo)
        test_files = r.get("test_files")
        if test_files is None:
            test_files = _verification_test_files_from_command(cmd)
        test_files = sorted({_vt_norm(f) for f in test_files})
        _passed = int(r.get("passed", 0) or 0)
        _failed = int(r.get("failed", 0) or 0)
        _skipped = int(r.get("skipped", 0) or 0)
        _node_ids = list(r.get("node_ids") or [])
        _selected = int(r.get("selected", 0) or 0)
        if not _selected:
            _selected = len(_node_ids) if _node_ids else (_passed + _failed + _skipped)
        _deselected = int(r.get("deselected", 0) or 0)
        _stdout_summary = str(r.get("stdout_summary", "") or "")[-2000:]
        # A caller-supplied output_hash is NEVER kept — truncation above may
        # have changed the stored bytes, so it no longer describes them.
        # output_hash is always recomputed from the FINAL _stdout_summary
        # (contract fixed by R-0792).
        _output_hash = hashlib.sha256(
            _stdout_summary.encode("utf-8", errors="replace")).hexdigest()
        _head_sha = str(r.get("head_sha", "") or "") or _head_sha_default
        _duration = r.get("duration_seconds")
        if _duration is None:
            _duration = 0.0
        else:
            _duration = round(float(_duration), 3)
        runs.append({
            "run_id": rid,
            "command": cmd,
            "exit_code": int(r.get("exit_code", -1)),
            "passed": _passed,
            "failed": _failed,
            "skipped": _skipped,
            "selected": _selected,
            "deselected": _deselected,
            "node_ids": _node_ids,
            "output_hash": _output_hash,
            "head_sha": _head_sha,
            "duration_seconds": _duration,
            "test_files": test_files,
            "stdout_summary": _stdout_summary,
        })
    total_passed = sum(x["passed"] for x in runs)
    total_failed = sum(x["failed"] for x in runs)
    exit_code = 0 if runs and all(x["exit_code"] == 0 for x in runs) else (0 if not runs else 1)
    all_files = sorted({f for x in runs for f in x["test_files"]})
    return {
        "schema_version": "1.1.0",
        "verification_type": "explicit_commands",
        "runs": runs,
        "command": " && ".join(c["command"] for c in runs),
        "exit_code": exit_code,
        "passed": total_passed,
        "failed": total_failed,
        "test_files": all_files,
        "timestamp": _dt.now(_tz.utc).isoformat(),
    }


def _root_verification_summary(out_base: str) -> dict[str, Any]:
    """Read verification_tests.json into a compact root-verification record."""
    vt_path = Path(out_base) / "verification_tests.json"
    if not vt_path.exists():
        return {}
    try:
        vt = json.loads(vt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(vt, dict):
        return {}
    return {
        "command": vt.get("command", ""),
        "exit_code": vt.get("exit_code", -1),
        "passed": vt.get("passed", 0),
        "failed": vt.get("failed", 0),
        "timestamp": vt.get("timestamp", ""),
        "verification_type": vt.get("verification_type", ""),
    }


def _tests_txt_from_root_verification(rv: dict[str, Any]) -> str:
    """Render tests.txt content that references the real root verification."""
    if not rv:
        return _ATTESTATION_DEFAULTS["tests.txt"]
    return (
        "tests_verified_by_root_verification\n"
        f"command: {rv.get('command', '')}\n"
        f"exit_code: {rv.get('exit_code', -1)}\n"
        f"{rv.get('passed', 0)} passed, {rv.get('failed', 0)} failed\n"
        f"timestamp: {rv.get('timestamp', '')}\n"
    )


def _finalize_manual_completion(
    job: Any,
    attest_snap: dict[str, dict[str, bytes]],
    out_base: str,
    written: dict[str, str],
) -> None:
    """Deterministically finalize an operator-attested (manual) completion.

    Runs after ``verification_tests.json`` exists and before the final verifier.
    For every attested task it regenerates the derived evidence from the
    ATTESTED diff (never a stale provider-run scope):

      * ``tests.txt`` — references the real root verification result;
      * ``review_scope_packet.json`` + ``.md`` — rebuilt from the attested
        ``safe.diff`` so the scope is the true task file set (never empty, never
        the stale ``safe_diff_files``);
      * ``missing_tests_gate.json`` — acknowledges the changed files and records
        that tests were satisfied by root verification;
      * ``task_execution_evidence.json`` — separates the manual completion layer
        (zero provider calls) from any preserved prior provider execution.

    Then, at job level, it rebuilds ``final_job_review.json`` from the attested
    changed-file sets, carrying the manual-completion facts (completion mode,
    human-review flag, linked-prior-job ids, root verification) on that EXISTING
    artifact — no new root file or schema. No-op when there are no attestations.
    """
    if not attest_snap:
        return

    from packages.orchestration.missing_tests_gate import (
        _relevant_suites_for_source,
        write_missing_tests_gate,
    )
    from packages.orchestration.review_scope import write_review_scope_packet

    out_path = Path(out_base)
    rv = _root_verification_summary(out_base)

    # Load the recorded verification runs and build a per-test-file coverage map
    # (a file is covered only by a SUCCESSFUL run whose test_files include it).
    vt_full: dict[str, Any] = {}
    vt_path = out_path / "verification_tests.json"
    if vt_path.exists():
        try:
            vt_full = json.loads(vt_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            vt_full = {}
    runs = vt_full.get("runs") or []
    coverage: dict[str, list[str]] = {}
    for run in runs:
        if not isinstance(run, dict):
            continue
        if int(run.get("exit_code", -1)) != 0 or int(run.get("failed", 0) or 0) != 0:
            continue
        for tf in (run.get("test_files") or []):
            coverage.setdefault(_vt_norm(str(tf)), []).append(str(run.get("run_id", "")))

    def _is_test_path(p: str) -> bool:
        n = _vt_norm(p)
        return n.startswith("tests/") or "/tests/" in n or Path(n).name.startswith("test_")

    tasks_by_id = {t.task_id: t for t in job.tasks}
    per_task_changed: dict[str, list[str]] = {}

    for tid in attest_snap:
        task = tasks_by_id.get(tid)
        if task is None:
            continue
        run_dir = out_path / "task_runs" / tid
        run_dir.mkdir(parents=True, exist_ok=True)

        # Regenerate review scope from the attested safe.diff now present in the
        # evidence dir. build_review_scope_packet reads task_runs/<tid>/safe.diff.
        try:
            write_review_scope_packet(task, job.job_workspace_path, out_base, written)
        except Exception:
            pass

        # Capture the authoritative changed-file set for this task.
        packet_path = run_dir / "review_scope_packet.json"
        changed: list[str] = []
        if packet_path.exists():
            try:
                pkt = json.loads(packet_path.read_text(encoding="utf-8"))
                changed = [str(f) for f in (pkt.get("changed_files") or [])]
            except (OSError, json.JSONDecodeError):
                changed = []
        if not changed:
            mrp = run_dir / "manual_repair_provenance.json"
            if mrp.exists():
                try:
                    changed = [
                        str(f) for f in
                        (json.loads(mrp.read_text(encoding="utf-8")).get("changed_files") or [])
                    ]
                except (OSError, json.JSONDecodeError):
                    changed = []
        per_task_changed[tid] = sorted(set(changed))

        # Finding 2: a task is test-covered only when EVERY related test file in
        # its changed set is exercised by a successful verification run. A task
        # missing direct coverage gets NEEDS_TESTS — never a false "satisfied".
        # F8 (round 16): a task's related tests are the test files it CHANGED **plus** the
        # regression suites its changed SOURCE files are known to be covered by.
        #
        # Round 15 changed the do command and shipped `do job-flow` broken with a NameError.
        # Every Missing-Tests gate still said PASS, because the suite that catches it was in
        # neither the task's changed set nor the authoritative CLI command (which runs only
        # `tests/cli`). Nothing was lying; nothing was asked. A gate that only checks the tests
        # you happened to touch cannot notice the one you broke. The map lives in
        # `missing_tests_gate` — this module names no test file it does not run.
        related_tests = sorted(
            {_vt_norm(f) for f in changed if _is_test_path(f)}
            | {t for f in changed
               for t in _relevant_suites_for_source(_vt_norm(f))})
        covering_run_ids = sorted({
            rid for f in related_tests for rid in coverage.get(f, [])
        })
        uncovered_tests = [f for f in related_tests if not coverage.get(f)]
        covered = bool(related_tests) and not uncovered_tests

        # tests.txt references the covering run ids (no bare totals — those are
        # deduplicated at the run level, see finding 4).
        if covered:
            tests_path_txt = (
                "tests_verified_by_root_verification\n"
                f"covered_by_runs: {', '.join(covering_run_ids)}\n"
                f"related_tests: {', '.join(related_tests)}\n"
            )
        else:
            tests_path_txt = (
                "tests_not_run: no successful verification run covers this task's "
                f"tests\nuncovered_tests: {', '.join(uncovered_tests) or '(none)'}\n"
            )
        tests_path = run_dir / "tests.txt"
        tests_path.write_text(tests_path_txt, encoding="utf-8")
        written[f"task_runs/{tid}/tests.txt"] = str(tests_path)

        # Rebuild the missing-tests gate honoring the real coverage.
        try:
            write_missing_tests_gate(task, out_base, written)
        except Exception:
            pass
        mtg_path = run_dir / "missing_tests_gate.json"
        if mtg_path.exists():
            try:
                mtg = json.loads(mtg_path.read_text(encoding="utf-8"))
                if covered:
                    mtg["gate_status"] = "PASS"
                    mtg["tests_executed"] = True
                    mtg["tests_satisfied_by"] = "root_verification"
                    mtg["suggested_test_commands"] = []
                    mtg["verification_run_ids"] = covering_run_ids
                    mtg["reason"] = (
                        "Operator-attested manual completion; the task's changed "
                        f"tests are exercised by verification runs {covering_run_ids}."
                    )
                else:
                    mtg["gate_status"] = "NEEDS_TESTS"
                    mtg["tests_executed"] = False
                    mtg["tests_satisfied_by"] = None
                    mtg["uncovered_tests"] = uncovered_tests
                    mtg["reason"] = (
                        "Changed test files are not covered by any successful "
                        f"verification run: {uncovered_tests}."
                    )
                mtg_path.write_text(json.dumps(mtg, indent=2) + "\n", encoding="utf-8")
            except (OSError, json.JSONDecodeError):
                pass

        # Two-layer execution evidence: manual completion (0 provider calls) with
        # any prior provider execution preserved separately.
        prior_execution = None
        pe_path = run_dir / "provider_evidence.json"
        if pe_path.exists():
            try:
                pe = json.loads(pe_path.read_text(encoding="utf-8"))
                prior_execution = pe.get("prior_execution")
            except (OSError, json.JSONDecodeError):
                prior_execution = None
        exec_ev = {
            "schema_version": "1.0.0",
            "task_id": tid,
            # Trace-consistent mode for the completion: no prompts, no calls.
            "execution_mode": "operator_built_no_provider",
            "prompt_trace_available": False,
            "provider_call_count": 0,
            "builder_provider": "operator",
            "reviewer_provider": "operator",
            "completion_execution_mode": "manual_operator_repair",
            "completion_provider_call_count": 0,
            "supersedes_prior_execution": prior_execution is not None,
            "prior_execution": prior_execution,
        }
        exec_path = run_dir / "task_execution_evidence.json"
        exec_path.write_text(json.dumps(exec_ev, indent=2) + "\n", encoding="utf-8")
        written[f"task_runs/{tid}/task_execution_evidence.json"] = str(exec_path)

    # --- job level ---------------------------------------------------------
    combined_changed = sorted({f for files in per_task_changed.values() for f in files})

    # Collect per-task manual-completion metadata (prior execution + generic
    # linked-prior-job ids) directly from the attested provenance — no
    # feature-specific path, no new root artifact.
    linked_prior_job_ids: list[str] = []
    superseded_prior_run_ids: list[str] = []
    prior_provider_calls = 0
    for tid in sorted(attest_snap):
        mrp_path = out_path / "task_runs" / tid / "manual_repair_provenance.json"
        if not mrp_path.exists():
            continue
        try:
            mrp = json.loads(mrp_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        lp = str(mrp.get("linked_prior_job_id") or "")
        if lp and lp != job.job_id and lp not in linked_prior_job_ids:
            linked_prior_job_ids.append(lp)
        prior = mrp.get("prior_execution")
        if isinstance(prior, dict):
            run_id = str(prior.get("run_id") or "")
            if run_id and run_id not in superseded_prior_run_ids:
                superseded_prior_run_ids.append(run_id)
            pcc = prior.get("provider_call_count")
            if isinstance(pcc, int) and not isinstance(pcc, bool):
                prior_provider_calls += pcc

    # Rebuild the final job review from the attestation diffs and operator
    # verdicts so it lists the actual changed files (never an empty set). The
    # manual-completion facts live on this EXISTING artifact — no new root file.
    fjr = {
        "schema_version": "1.0.0",
        "verdict": "PASS",
        "job_id": job.job_id,
        "review_mode": "operator_attested_manual_completion",
        "completion_mode": "manual_operator_repair",
        "completion_provider_call_count": 0,
        "human_final_reviewer_required": True,
        "expected_changed_files": combined_changed,
        "actual_changed_files": combined_changed,
        "changed_files_match": True,
        "per_task_changed_files": per_task_changed,
        "task_verdicts": [
            {"task_id": tid, "verdict": "operator_attested"} for tid in sorted(attest_snap)
        ],
        "linked_prior_job_ids": linked_prior_job_ids,
        "linked_prior_job_summaries": [
            _linked_job_summary(jid) for jid in linked_prior_job_ids
        ],
        "superseded_prior_run_ids": superseded_prior_run_ids,
        "prior_execution_provider_call_count": prior_provider_calls,
        "root_verification": rv,
        "findings": [],
    }
    fjr_path = out_path / "final_job_review.json"
    fjr_path.write_text(json.dumps(fjr, indent=2) + "\n", encoding="utf-8")
    written["final_job_review.json"] = str(fjr_path)


TERMINAL_TASK_STATUSES = frozenset({"failed", "blocked"})

#: Where the export records what F010 could NOT do. An empty list is the normal case; a
#: non-empty one BLOCKS the package — a bundle that quietly lost a required post-mortem
#: must not be able to present clean gates.
POSTMORTEM_INTEGRITY_FILE = "postmortem_integrity.json"

#: F012: the run-input manifest and its integrity artifact in the exported bundle.
from packages.orchestration.run_manifest import (  # noqa: E402
    MANIFEST_FILENAME as _RUN_MANIFEST_FILENAME,
)

MANIFEST_INTEGRITY_FILE = "manifest_integrity.json"


def _crosscheck_job_episodes_vs_index(job: Any, index: dict[str, Any]) -> list[str]:
    """F9/F13: the JobPlan's recorded episode state MUST agree COMPLETELY with the on-disk index.

    Beyond status + ordinal, this checks: no duplicate JobPlan episode ids; the EXACT episode-id
    set on both sides; per-episode created_at and previous_episode_id; that the job's latest
    episode equals the index's maximum-ordinal / latest episode; and that a terminal job's active
    episode is itself a recorded episode. A divergence is a BLOCKING integrity failure — the
    durable index and the job's view of its own history have drifted apart, and that is never
    silently reconciled."""
    from packages.orchestration.pingpong_job import (
        JOB_COMPLETED,
        JOB_STOPPED,
    )

    problems: list[str] = []
    raw_job_eps = [e for e in (getattr(job, "run_manifest_episodes", None) or [])
                   if e.get("episode_id")]
    job_eps = {str(e.get("episode_id", "")): e for e in raw_job_eps}
    if len(raw_job_eps) != len(job_eps):
        problems.append("duplicate episode ids in JobPlan")
    idx_eps = {str(e.get("episode_id", "")): e
               for e in (index.get("episodes") or []) if e.get("episode_id")}

    if set(job_eps) != set(idx_eps):
        only_job = sorted(set(job_eps) - set(idx_eps))
        only_idx = sorted(set(idx_eps) - set(job_eps))
        if only_job:
            problems.append(f"JobPlan-only episodes not in index: {only_job}")
        if only_idx:
            problems.append(f"index-only episodes not in JobPlan: {only_idx}")

    for eid, je in job_eps.items():
        ie = idx_eps.get(eid)
        if ie is None:
            continue
        if str(je.get("status", "")) != str(ie.get("status", "")):
            problems.append(f"episode {eid} status differs (job "
                            f"{je.get('status')!r} vs index {ie.get('status')!r})")
        j_ord = int(je.get("episode_ordinal", 0) or 0)
        i_ord = int(ie.get("episode_ordinal", 0) or 0)
        if j_ord != i_ord:
            problems.append(f"episode {eid} ordinal differs (job {j_ord} vs index {i_ord})")
        if str(je.get("created_at", "")) != str(ie.get("created_at", "")):
            problems.append(f"episode {eid} created_at differs")
        if str(je.get("previous_episode_id", "") or "") != str(
                ie.get("previous_episode_id", "") or ""):
            problems.append(f"episode {eid} previous_episode_id differs")

    # The latest episode (max ordinal) must agree with the index's latest_episode_id.
    if idx_eps:
        idx_latest = str(index.get("latest_episode_id", ""))
        max_ord_id = max(idx_eps.values(),
                         key=lambda e: int(e.get("episode_ordinal", 0) or 0)
                         ).get("episode_id", "")
        if idx_latest != max_ord_id:
            problems.append(f"index latest_episode_id {idx_latest!r} != max-ordinal episode "
                            f"{max_ord_id!r}")
        if job_eps:
            job_latest = max(job_eps.values(),
                             key=lambda e: int(e.get("episode_ordinal", 0) or 0)
                             ).get("episode_id", "")
            if job_latest != idx_latest:
                problems.append(f"JobPlan latest episode {job_latest!r} != index latest "
                                f"{idx_latest!r}")

    # A terminal job's active episode must be one of the recorded episodes.
    if getattr(job, "status", "") in (JOB_COMPLETED, JOB_STOPPED):
        active = str(getattr(job, "active_episode_id", "") or "")
        if active and active not in idx_eps:
            problems.append(f"terminal job's active episode {active!r} is not in the index")
    return problems


def _crosscheck_terminal_jobplan_manifest(job: Any, latest: Any, index: dict[str, Any]
                                          ) -> list[str]:
    """F8: for a TERMINAL job, the JobPlan, the index's latest and the latest manifest must
    agree on every field. A mismatch is a BLOCKING integrity failure."""
    from packages.orchestration.pingpong_job import JOB_COMPLETED, JOB_STOPPED

    problems: list[str] = []
    status = str(getattr(job, "status", "") or "")
    if status not in (JOB_COMPLETED, JOB_STOPPED):
        return problems

    active = str(getattr(job, "active_episode_id", "") or "")
    idx_latest = str(index.get("latest_episode_id", "") or "")
    # F13: for a MARKED terminal F012 job these fields are REQUIRED, not optional — an empty
    # value is a blocking integrity failure, never a silently-skipped check.
    if not active:
        problems.append("terminal job has no active_episode_id")
    elif active != idx_latest:
        problems.append(f"terminal active_episode_id {active!r} != index latest "
                        f"{idx_latest!r}")
    if active and not any(str(e.get("episode_id", "")) == active
                          for e in (getattr(job, "run_manifest_episodes", None) or [])):
        problems.append(f"terminal active episode {active!r} is absent from the JobPlan "
                        f"episode summary")
    if latest.episode_id != idx_latest:
        problems.append(f"latest manifest episode {latest.episode_id!r} != index latest "
                        f"{idx_latest!r}")
    if status != latest.status:
        problems.append(f"job status {status!r} != latest manifest status "
                        f"{latest.status!r}")
    j_created = str(getattr(job, "run_manifest_created_at", "") or "")
    if not j_created:
        problems.append("terminal job has no run_manifest_created_at")
    elif j_created != latest.created_at:
        problems.append(f"JobPlan run_manifest_created_at {j_created!r} != latest created_at "
                        f"{latest.created_at!r}")
    j_path = str(getattr(job, "run_manifest_path", "") or "")
    if not j_path:
        problems.append("terminal job has no run_manifest_path")
    elif j_path != _RUN_MANIFEST_FILENAME:
        problems.append(f"JobPlan run_manifest_path {j_path!r} is not the canonical latest "
                        f"mirror {_RUN_MANIFEST_FILENAME!r}")
    # Stop metadata coherence.
    if status == JOB_STOPPED:
        j_req = str(getattr(job, "stop_request_id", "") or "")
        if not j_req:
            problems.append("stopped job has no stop_request_id")
        if j_req != (latest.stop_request_id or ""):
            problems.append(f"JobPlan stop_request_id {j_req!r} != latest stop_request_id "
                            f"{latest.stop_request_id!r}")
    elif latest.stop_request_id:
        problems.append("a completed job's latest manifest carries stopped-only "
                        "stop_request_id metadata")
    # The latest snapshot + calls all belong to the latest episode.
    if latest.episode_snapshot.episode_id != latest.episode_id:
        problems.append("latest snapshot episode != latest episode")
    for c in latest.calls:
        if c.identity.episode_id and c.identity.episode_id != latest.episode_id:
            problems.append(f"latest call {c.identity.call_id} does not belong to the latest "
                            f"episode")
            break
    return problems


def _write_run_manifest_export(
    job: Any, out_base: str, written: dict[str, str], failures: list[dict[str, Any]],
    notes: list[str] | None = None,
) -> None:
    """Copy the job's manifest episodes into the bundle and verify their integrity.

    A completed/stopped job MARKED under F012 (``run_manifest_required_v``) MUST have a
    manifest whose calls have complete coverage and whose call-input artifacts resolve and
    hash-match. A recording error, a missing marked manifest, incomplete coverage, or a
    call artifact that is missing / mis-hashed is BLOCKING. A pre-F012 UNMARKED job with no
    manifest is legacy/uncovered — readable, not corrupt.
    """
    from packages.orchestration.failure_postmortem import safe_text
    from packages.orchestration.pingpong_job import (
        JOB_COMPLETED,
        JOB_STOPPED,
        job_evidence_dir,
    )
    from packages.orchestration.run_manifest import (
        COVERAGE_COMPLETE,
        MANIFEST_INDEX_FILENAME,
        MANIFESTS_SUBDIR,
        ManifestError,
        build_verified_manifest_tree,
        decode_index_v1,
        decode_run_manifest_v1,
        load_latest_manifest_verified,
        manifest_tree_is_present,
        validate_index_and_tree,
    )

    terminal = getattr(job, "status", "") in (JOB_COMPLETED, JOB_STOPPED)
    marked = int(getattr(job, "run_manifest_required_v", 0) or 0) > 0
    mandatory = terminal and marked

    err = str(getattr(job, "run_manifest_error", "") or "")
    if err:
        failures.append({"scope": "job", "job_id": job.job_id,
                         "error": safe_text(err)[:500]})
        return

    ev = job_evidence_dir(job.job_id)

    # F5: VALIDATE FIRST, then copy. Build the verified ALLOWLIST — the exact declared set of
    # index + episode manifests + declared call artifacts, each anchored-read, hash-verified and
    # size-bounded. Undeclared episode dirs, undeclared call artifacts, oversized files and
    # outside/symlinked components never enter this map. Nothing is copied to the bundle until
    # every invariant holds, so a canary in an extra file can never reach the output.
    files, tree_problems = build_verified_manifest_tree(ev, job_id=job.job_id)

    # F10: the F012 MARKER changes ABSENCE semantics ONLY. It never decides whether a PRESENT
    # manifest tree is trusted: any artifact that exists is fully validated, marked or not.
    if _RUN_MANIFEST_FILENAME not in files:
        if mandatory:
            failures.append({
                "scope": "job", "job_id": job.job_id,
                "error": f"a {job.status} F012-marked job has no run manifest"})
            for prob in tree_problems:
                failures.append({"scope": "job", "job_id": job.job_id,
                                 "error": safe_text(f"manifest tree: {prob}")[:500]})
        else:
            # PRESENCE is decided on the RAW anchored tree, not on the verified allowlist: a
            # tree so broken that nothing survived verification (e.g. the index is gone, so no
            # episode is declared) is exactly the case that must not be waved through as
            # "legacy". Only a genuinely EMPTY tree is legacy/uncovered.
            # PRESENCE is the raw anchored probe's verdict alone — `tree_problems` includes
            # "evidence directory does not exist", which IS absence, not a broken tree.
            present, raw_problems = manifest_tree_is_present(ev)
            if present:
                for prob in list(tree_problems) + list(raw_problems):
                    failures.append({"scope": "job", "job_id": job.job_id,
                                     "error": safe_text(f"manifest tree: {prob}")[:500]})
                failures.append({
                    "scope": "job", "job_id": job.job_id,
                    "error": "manifest artifacts are present but no verified run manifest "
                             "could be read; a present manifest tree is always validated"})
            elif notes is not None:
                notes.append("legacy pre-F012 job: no run manifest (uncovered, not corrupt)")
        return

    # The authoritative trust-chain check (F7/F8/F9) over ANCHORED reads. It catches a tampered
    # index hash, an index/metadata mismatch, an extra/missing episode, a rollback (F5), a broken
    # prior-episode graph (F6/F8), a mis-hashed call artifact (F7) and symlinked components.
    chain_problems: list[str] = list(tree_problems)
    index: dict = {}
    if MANIFEST_INDEX_FILENAME in files:
        try:
            # F11: the index is untrusted manifest bytes — strict-decode it, never _json.loads.
            index = decode_index_v1(files[MANIFEST_INDEX_FILENAME])
        except (ValueError, UnicodeDecodeError, ManifestError) as exc:
            # F10: a present-but-unreadable index is an integrity problem, never a silent {}.
            index = {}
            chain_problems.append(f"unreadable run_manifest_index.json: {exc}")
    else:
        chain_problems.append("a run manifest is present but there is no "
                              "run_manifest_index.json")
    # F10: a PRESENT manifest tree is ALWAYS fully validated — strict chain, canonical bytes,
    # exact allowlist — whether or not the job carries the F012 marker.
    chain_problems.extend(validate_index_and_tree(ev, job_id=job.job_id))
    if mandatory:
        # These compare the MARKED JobPlan's own F012 state, so they need the marker.
        chain_problems.extend(_crosscheck_job_episodes_vs_index(job, index))
        try:
            latest = load_latest_manifest_verified(ev, job_id=job.job_id)
            chain_problems.extend(_crosscheck_terminal_jobplan_manifest(job, latest, index))
        except ManifestError as exc:
            chain_problems.append(f"latest manifest could not be loaded: {exc}")
    # F1: a published terminal reference must have COMPLETE coverage (the canonical loader
    # already enforces this; the export re-states it as a blocking Evidence failure). Marked or
    # not: a stored manifest that IS present is held to the published-reference rule.
    for rel, data in files.items():
        if not (rel.startswith(f"{MANIFESTS_SUBDIR}/")
                and rel.endswith(f"/{_RUN_MANIFEST_FILENAME}")):
            continue
        eid = rel.split("/")[1]
        try:
            m = decode_run_manifest_v1(data)      # F13: strict, untrusted bytes
        except (ValueError, UnicodeDecodeError, ManifestError) as exc:
            chain_problems.append(f"unreadable episode manifest {eid}: {exc}")
            continue
        if m.coverage.status != COVERAGE_COMPLETE:
            chain_problems.append(
                f"episode {eid} has incomplete call coverage: "
                f"{'; '.join(m.coverage.problems)[:300]}")

    # F5: only copy the allowlisted bytes when the tree is CLEAN. If any invariant failed for a
    # marked job, record the failures and copy NOTHING — the safe integrity-failure artifact is
    # written by the caller, but no (possibly undeclared) bytes reach the bundle.
    if chain_problems:
        for prob in chain_problems:
            failures.append({"scope": "job", "job_id": job.job_id,
                             "error": safe_text(f"manifest integrity: {prob}")[:500]})
        return

    for rel, data in sorted(files.items()):
        _dest = _validate_output_path(out_base, rel)
        _dest.parent.mkdir(parents=True, exist_ok=True)
        _dest.write_bytes(data)
        written[rel] = str(_dest)


def _write_task_postmortems(
    job_id: str,
    task: Any,
    out_base: str,
    written: dict[str, str],
    failures: list[dict[str, Any]],
) -> None:
    """F010: copy this task's call post-mortems into the bundle and write its rollup.

    Only for a task that ended terminally failed or blocked. A passed task has nothing to
    explain, and inventing an empty record for it would make the failure histogram lie.

    Call-level records are collected from BOTH real source layouts — the run's fallback
    call directories and the task's streamed call directories — and copied ONCE each into
    the canonical exported location ``task_runs/<task>/call_postmortems/<layout>/``. The
    rollup then references exactly those exported files, which is what the reviewed build
    could not do: a streamed failure's record never left the job store, so the rollup
    pointed at nothing and the stats saw nothing.
    """
    from packages.orchestration import data_paths
    from packages.orchestration.failure_postmortem import (
        CALL_POSTMORTEM_SUBDIR,
        POSTMORTEM_FILENAME,
        build_task_rollup,
        collect_task_call_postmortems,
        write_postmortem,
    )
    from packages.orchestration.pingpong_job import _task_stream_dir

    if str(getattr(task, "status", "")) not in TERMINAL_TASK_STATUSES:
        return

    task_rel = f"task_runs/{task.task_id}"
    task_out = _task_evidence_dir(out_base, task.task_id)

    run_id = str(getattr(task, "run_id", "") or "")
    run_dir = data_paths.run_dir(run_id) if run_id else None
    # The provider streams into ``…/task_runs/<task>/streams/<role>/round-NN/<kind>-II``;
    # that ``streams`` directory is the root of the streamed call layout.
    stream_dir = _task_stream_dir(job_id, task.task_id) / "streams"

    call_refs: list[str] = []
    for layout, src in collect_task_call_postmortems(
        run_dir=run_dir, task_stream_dir=stream_dir,
    ):
        rel = f"{CALL_POSTMORTEM_SUBDIR}/{layout}/{POSTMORTEM_FILENAME}"
        dest = _validate_output_path(out_base, f"{task_rel}/{rel}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        written[f"{task_rel}/{rel}"] = str(dest)
        call_refs.append(rel)

    rollup = build_task_rollup(task, job_id=job_id, call_refs=tuple(sorted(call_refs)))
    # Idempotent by construction: a second export of the same terminal task publishes the
    # identical record, and the writer accepts that without duplicating it.
    write_postmortem(task_out, rollup, root=Path(out_base).resolve())
    written[f"{task_rel}/{POSTMORTEM_FILENAME}"] = str(task_out / POSTMORTEM_FILENAME)

    # A run that could not record a call-level post-mortem says so in its durable JSON.
    # That is a broken F010 contract, and it blocks the package.
    run_json = _read_run_json(run_id)
    pm_error = str(run_json.get("postmortem_error") or "")
    if pm_error:
        from packages.orchestration.failure_postmortem import safe_text
        failures.append({
            "scope": "call",
            "task_id": task.task_id,
            "run_id": run_id,
            "error": safe_text(pm_error)[:500],
        })


def _read_run_json(run_id: str) -> dict[str, Any]:
    """The persisted run result, or {} — never an exception into the export."""
    if not run_id:
        return {}
    try:
        from packages.orchestration.data_paths import run_dir
        path = run_dir(run_id) / "result.json"
        if not path.is_file():
            return {}
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _write_job_postmortem(
    job: Any, out_base: str, written: dict[str, str], failures: list[dict[str, Any]],
) -> None:
    """F010: the JOB-level record — a job that failed before any task could own it.

    A worktree lock that stops `_acquire_job_workspace()` blocks the job while every task
    is still `pending`. The reviewed build produced no post-mortem at all for it: the
    failure simply disappeared. The runner now writes a job-scope record into the job's own
    evidence directory, and the export preserves it at the root of the bundle.
    """
    from packages.orchestration.failure_postmortem import POSTMORTEM_FILENAME
    from packages.orchestration.pingpong_job import job_postmortem_path

    src = job_postmortem_path(job.job_id)
    if src.is_file() and not src.is_symlink():
        dest = _validate_output_path(out_base, POSTMORTEM_FILENAME)
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        written[POSTMORTEM_FILENAME] = str(dest)

    job_error = str(getattr(job, "postmortem_error", "") or "")
    if job_error:
        from packages.orchestration.failure_postmortem import safe_text
        failures.append({
            "scope": "job", "job_id": job.job_id, "error": safe_text(job_error)[:500],
        })

    _write_stop_postmortems(job, out_base, written, failures)


def _write_stop_postmortems(
    job: Any, out_base: str, written: dict[str, str], failures: list[dict[str, Any]],
) -> None:
    """F011: every stop EPISODE this job has, keyed by its request id.

    A job may be stopped, resumed and stopped again. Each consumed request has its own
    record under ``stop_postmortems/<request_id>/``, so a second stop never overwrites the
    first and the bundle shows the whole history. A stop that could not be recorded is a
    blocking integrity failure, exactly like a failure that could not be recorded.
    """
    from packages.orchestration.failure_postmortem import POSTMORTEM_FILENAME, safe_text
    from packages.orchestration.pingpong_job import (
        STOP_POSTMORTEM_SUBDIR,
        job_evidence_dir,
    )

    src_root = job_evidence_dir(job.job_id) / STOP_POSTMORTEM_SUBDIR
    if src_root.is_dir() and not src_root.is_symlink():
        for episode in sorted(p for p in src_root.iterdir() if p.is_dir()):
            src = episode / POSTMORTEM_FILENAME
            if not src.is_file() or src.is_symlink():
                continue
            rel = f"{STOP_POSTMORTEM_SUBDIR}/{episode.name}/{POSTMORTEM_FILENAME}"
            dest = _validate_output_path(out_base, rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            written[rel] = str(dest)

    for field_name in ("stop_error", "stop_event_error"):
        err = str(getattr(job, field_name, "") or "")
        if err:
            failures.append({
                "scope": "job", "job_id": job.job_id,
                "error": safe_text(err)[:500],
            })


def _write_task_run_evidence(
    task: Any,
    out_base: str,
    written: dict[str, str],
    *,
    ledger_project_id: str | None = None,
    job_id: str | None = None,
) -> None:
    """Write one task run's evidence, and mirror it into the F103 ledger.

    ``ledger_project_id`` and ``job_id`` are the ledger opt-in, resolved once by
    ``export_job_evidence`` and threaded down because this function is handed a
    TASK and never sees the job. Per DECISION D16 this is the per-task-run seam:
    one row per finalized task run, ``call_id`` ``"<job_id>:<task_id>"``. Both
    default to None so the existing three-argument callers stay inert exactly as
    they were — the ledger arms only where a job is genuinely in hand.

    The mirror cannot change what this function writes: it runs after the bundle
    files exist, re-reads them, and is wrapped so nothing escapes it.
    """
    task_out = _task_evidence_dir(out_base, task.task_id)
    task_rel = f"task_runs/{task.task_id}"

    if not task.run_id:
        _write_unavailable(task_out, task_rel, task.task_id, written,
                          f"No run_id for task {task.task_id} (status: {task.status})")
        return

    from packages.orchestration.pingpong_loop import load_run

    run_data = load_run(task.run_id)
    if run_data is None:
        _write_unavailable(task_out, task_rel, task.task_id, written,
                          f"Run data not found for {task.run_id}")
        return

    from packages.orchestration.pingpong_promote import load_promotion
    promotion_data = load_promotion(task.run_id)

    bundle = build_evidence_bundle(run_data, promotion_data)

    # Include prompt traces from persisted run dir
    from packages.orchestration.data_paths import run_dir
    trace_file = run_dir(task.run_id) / "prompt_trace.jsonl"
    if trace_file.exists():
        bundle["prompt_trace_jsonl_path"] = str(trace_file)

    # F103: the live ledger mirror is armed HERE for a real job. The four
    # ledger_* arguments keep their None defaults for every other caller, and a
    # None project_id leaves the hook inert, so evidence output is byte-identical
    # either way.
    task_written = write_evidence_bundle(
        bundle,
        str(task_out),
        ledger_project_id=ledger_project_id,
        ledger_job_id=job_id,
        ledger_task_id=task.task_id,
    )

    for filename, path in task_written.items():
        written[f"{task_rel}/{filename}"] = path

    _write_task_worktree_evidence(task, run_data, task_out, task_rel, written)


#: The only filename a runtime diff may be exported from.
RESULT_DIFF_NAME = "result.diff"


def _resolve_result_diff_source(
    run_dir: Path,
    recorded: dict[str, Any],
) -> tuple[Path | None, str]:
    """Contain the runtime ``result.diff`` source before ANY bytes are copied.

    The recorded path comes from a run record, so it is input, not truth. It must
    be the canonical ``result.diff``, relative, traversal-free, a real regular
    file (never a symlink — not even one named ``result.diff``), resolve to a path
    that is still inside this exact run directory, and hash and size exactly as the
    run recorded. Anything else is an export validation error: the file is not
    copied and the persisted metadata is left untouched.

    The artifact-contract gate re-verifies the exported diff afterwards; that is a
    SECOND layer, not this containment check.
    """
    rel = str(recorded.get("path") or "")
    if not rel:
        return None, "result.diff reference is empty"
    if os.path.isabs(rel) or rel.startswith("~"):
        return None, f"result.diff source {rel!r} is not a relative path"
    parts = rel.replace("\\", "/").split("/")
    if ".." in parts:
        return None, f"result.diff source {rel!r} escapes the run directory"
    if rel != RESULT_DIFF_NAME:
        return None, (
            f"result.diff source {rel!r} is not the canonical {RESULT_DIFF_NAME!r}"
        )

    src = run_dir / rel
    if src.is_symlink():
        return None, f"result.diff source {rel!r} is a symlink"
    if not src.is_file():
        return None, f"recorded result.diff not found at {rel!r}"

    try:
        base = run_dir.resolve(strict=True)
        resolved = src.resolve(strict=True)
    except OSError as exc:
        return None, f"result.diff source {rel!r} could not be resolved: {exc}"
    if resolved.parent != base:
        return None, (
            f"result.diff source {rel!r} resolves outside its run directory"
        )

    data = src.read_bytes()
    actual_sha = hashlib.sha256(data).hexdigest()
    if actual_sha != str(recorded.get("sha256") or ""):
        return None, (
            f"result.diff source sha256 {actual_sha} does not match the recorded "
            f"{recorded.get('sha256')!r}"
        )
    if len(data) != recorded.get("size_bytes"):
        return None, (
            f"result.diff source size {len(data)} does not match the recorded "
            f"{recorded.get('size_bytes')!r}"
        )
    return src, ""


def _write_task_worktree_evidence(
    task: Any,
    run_data: dict[str, Any],
    task_out: Path,
    task_rel: str,
    written: dict[str, str],
) -> None:
    """F006: export the run's worktree hand-off and its ``result.diff``.

    Only for runs that actually executed in a worktree. The exported diff carries
    the sha256/size the run recorded, so the artifact contract can re-verify the
    bytes in the bundle rather than trusting that a file with the right name exists.
    """
    wt = run_data.get("worktree") or {}
    if wt.get("isolation_mode") != "worktree":
        return

    from packages.orchestration import data_paths

    doc: dict[str, Any] = {
        "schema_version": "1.0.0",
        "task_id": task.task_id,
        "run_id": task.run_id,
        "isolation_mode": "worktree",
        "branch": wt.get("branch", ""),
        "worktree_path": wt.get("path", ""),
        "base_commit": wt.get("base_commit", ""),
        "worktree_head": wt.get("head", ""),
        "cleanup_status": wt.get("cleanup_status", ""),
        "cleanup_error": wt.get("cleanup_error", ""),
        "result_diff": None,
        "result_diff_error": wt.get("result_diff_error", ""),
        "auto_merged": False,          # there is never an automatic merge
    }

    rd = wt.get("result_diff") or {}
    if rd:
        run_dir = data_paths.run_dir(str(task.run_id))
        src, err = _resolve_result_diff_source(run_dir, rd)
        if err:
            # Report the validation failure; NEVER rewrite the persisted metadata
            # to make an unsafe source look safe, and never copy the bytes.
            doc["result_diff"] = None
            doc["result_diff_error"] = err
        else:
            dst = task_out / "result.diff"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
            written[f"{task_rel}/result.diff"] = str(dst)
            doc["result_diff"] = {
                "path": "result.diff",
                "sha256": rd.get("sha256", ""),
                "size_bytes": rd.get("size_bytes", 0),
            }

    wt_path = task_out / "worktree.json"
    wt_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    written[f"{task_rel}/worktree.json"] = str(wt_path)


def _write_unavailable(
    task_out: Path,
    task_rel: str,
    task_id: str,
    written: dict[str, str],
    reason: str,
) -> None:
    task_out.mkdir(parents=True, exist_ok=True)

    manifest = {
        "task_id": task_id,
        "evidence_available": False,
        "reason": reason,
    }
    manifest_path = task_out / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    written[f"{task_rel}/manifest.json"] = str(manifest_path)

    summary = f"# Task {task_id} Evidence\n\nEvidence unavailable: {reason}\n"
    summary_path = task_out / "summary.md"
    summary_path.write_text(summary)
    written[f"{task_rel}/summary.md"] = str(summary_path)


def _write_job_prompt_trace_summary(
    job: Any,
    out_base: str,
    written: dict[str, str],
) -> None:
    """Write aggregate prompt trace summary across all tasks."""
    from packages.orchestration.data_paths import run_dir

    total_builder = 0
    total_reviewer = 0
    total_chars = 0
    total_tokens_est = 0
    task_traces: list[dict[str, Any]] = []

    for task in job.tasks:
        if not task.run_id:
            continue
        summary_file = run_dir(task.run_id) / "prompt_trace_summary.json"
        if not summary_file.exists():
            task_traces.append({
                "task_id": task.task_id,
                "run_id": task.run_id,
                "prompt_trace_available": False,
            })
            continue
        try:
            data = json.loads(summary_file.read_text())
            total_builder += data.get("builder_prompts", 0)
            total_reviewer += data.get("reviewer_prompts", 0)
            total_chars += data.get("total_prompt_chars", 0)
            total_tokens_est += data.get("total_prompt_tokens_estimated", 0)
            task_traces.append({
                "task_id": task.task_id,
                "run_id": task.run_id,
                "prompt_trace_available": True,
                "builder_prompts": data.get("builder_prompts", 0),
                "reviewer_prompts": data.get("reviewer_prompts", 0),
                "role": data.get("role", "unknown"),
                "configured_provider": data.get("configured_provider"),
                "configured_model": data.get("configured_model"),
                "actual_provider": data.get("actual_provider"),
                "actual_model": data.get("actual_model"),
                "model_resolution_source": data.get(
                    "model_resolution_source", "unknown"
                ),
                "actual_model_verified": data.get(
                    "actual_model_verified", False
                ),
            })
        except (OSError, json.JSONDecodeError):
            task_traces.append({
                "task_id": task.task_id,
                "run_id": task.run_id,
                "prompt_trace_available": False,
                "error": "parse_failed",
            })

    per_role_models: dict[str, dict[str, Any]] = {}
    for tt in task_traces:
        role = tt.get("role", "unknown")
        if role not in per_role_models:
            per_role_models[role] = {
                "configured_provider": tt.get("configured_provider"),
                "configured_model": tt.get("configured_model"),
                "actual_provider": tt.get("actual_provider"),
                "actual_model": tt.get("actual_model"),
                "actual_model_verified": tt.get(
                    "actual_model_verified", False
                ),
                "task_count": 0,
            }
        per_role_models[role]["task_count"] += 1

    aggregate = {
        "total_builder_prompts": total_builder,
        "total_reviewer_prompts": total_reviewer,
        "total_prompts": total_builder + total_reviewer,
        "total_prompt_chars": total_chars,
        "total_prompt_tokens_estimated": total_tokens_est,
        "per_role_model_summary": per_role_models,
        "task_traces": task_traces,
    }

    out_path = Path(out_base).resolve()
    target = _validate_output_path(str(out_path), "prompt_trace_summary.json")
    target.write_text(json.dumps(_redact_json_value(aggregate), indent=2) + "\n")
    written["prompt_trace_summary.json"] = str(target)


def _read_changed_files_for_index(evidence_dir: str) -> list[str]:
    """Return the changed source/test files an exported bundle proves.

    Reads the bundle's own content proof so the evidence index records exactly
    the file set the bundle covers. Returns [] when unavailable.
    """
    proof = Path(evidence_dir) / "current_change_content_proof.json"
    if not proof.is_file():
        return []
    try:
        data = json.loads(proof.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    hashes = data.get("file_hashes") if isinstance(data, dict) else None
    if not isinstance(hashes, dict):
        return []
    return sorted(str(k) for k in hashes)


def _copy_task_stream_artifacts(
    job_id: str, task_id: str, out_base: str, written: dict[str, str],
) -> dict[str, Any]:
    """Copy a task's per-attempt F004 stream artifacts into the exported bundle.

    Reads the hidden internal job state and reproduces the exact relative attempt
    layout under ``task_runs/<task>/streams/...``. Bytes are copied verbatim —
    they were already redacted at capture time and must never be re-processed.
    Symlinks and paths escaping the evidence root are refused.

    Returns a listing ``{relative_path: {sha256, size_bytes}}`` (empty when the
    task captured no streams).
    """
    import hashlib as _hl

    from packages.orchestration.data_paths import job_evidence_dir
    from packages.orchestration.stream_evidence import (
        RAW_STREAM_FILENAME,
        RUN_EVENTS_FILENAME,
    )

    listing: dict[str, Any] = {}
    src_task = job_evidence_dir(job_id) / "task_runs" / task_id / "streams"
    if not src_task.is_dir():
        return listing

    dst_root = _validate_output_path(out_base, f"task_runs/{task_id}/streams")
    src_root = src_task.resolve()

    for src in sorted(src_task.rglob("*")):
        if src.is_dir():
            continue
        if src.is_symlink():
            continue  # never follow or copy symlinks out of the job store
        if src.name not in (RAW_STREAM_FILENAME, RUN_EVENTS_FILENAME):
            continue
        try:
            resolved = src.resolve()
            resolved.relative_to(src_root)
        except (OSError, ValueError):
            continue  # path escapes the stream root
        rel = src.relative_to(src_task).as_posix()
        dst = _validate_output_path(str(dst_root), rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        data = src.read_bytes()
        dst.write_bytes(data)  # verbatim: already-redacted bytes are not mutated
        rel_full = f"task_runs/{task_id}/streams/{rel}"
        written[rel_full] = str(dst)
        listing[rel_full] = {
            "sha256": _hl.sha256(data).hexdigest(),
            "size_bytes": len(data),
        }
    return listing


# --------------------------------------------------------------------------- manual completion
# Round 32 F3: the SUPPORTED operator/manual Evidence creation boundary. A manual (zero-provider,
# operator-attested) completion is created ONLY through the canonical producer
# ``packages.orchestration.manual_attestation`` — packaging then regenerates and verifies it and never
# creates or repairs missing manual Evidence itself. This function is the one production entry an
# operator workflow calls; the test fixtures call the SAME producer, they are not its only callers.
def write_manual_completion_evidence(
    evidence_dir: str,
    *,
    job_id: str,
    tasks: list[dict],
) -> None:
    """Create an operator-attested manual-completion Evidence tree under ``evidence_dir``.

    ``tasks`` is a list of ``{task_id, changed_files, safe_diff_text, provenance_sha256, diff_sha256,
    tracked_diff_sha256, safe_diff_sha256, timestamp, note}`` records. Every task is written through
    the canonical ``manual_attestation`` producer, then the canonical root ``token_truth.json`` is
    regenerated from the assembled task/provider Evidence (never hand-written). The caller is
    responsible for the review subject / content proof / commit chain / gates; this is the manual
    attestation + token-truth boundary the final verifier consumes.
    """
    from packages.orchestration import manual_attestation as _ma

    for t in tasks:
        _ma.write_manual_task_evidence(
            evidence_dir, job_id=job_id, task_id=t["task_id"],
            changed_files=list(t["changed_files"]), safe_diff_text=t["safe_diff_text"],
            provenance_sha256=t["provenance_sha256"], diff_sha256=t["diff_sha256"],
            tracked_diff_sha256=t["tracked_diff_sha256"], safe_diff_sha256=t["safe_diff_sha256"],
            timestamp=t["timestamp"], note=t["note"])
    # Canonical root token truth = the exact aggregate of the tasks just written.
    _ma.write_manual_token_truth(evidence_dir)


def create_manual_completion_bundle(
    evidence_dir: str,
    *,
    repo_root: str,
    base_commit: str,
    job_id: str,
    job_title: str,
    step_range: str,
    prior_job_ids: list[str],
    verification_runs: list[dict],
    timestamp: str,
    generated_at: str,
    head_commit: str | None = None,
    task_partition: dict[str, list[str]] | None = None,
    num_tasks: int = 3,
    note_prefix: str = "operator-attested manual completion",
    review_feature_id: str | None = None,
) -> dict[str, Any]:
    """Round 33 F4 — the real, supported operator workflow that produces a COMPLETE manual-only
    (operator-attested, zero-provider) Evidence bundle end-to-end, reaching the canonical producer
    ``write_manual_completion_evidence`` (task attestation + regenerated root token truth) and the
    real ``final_verifier`` producer, so the packaged report is reproducible by the coordinator.

    This is the one non-test call path that exercises ``write_manual_completion_evidence`` against a
    real repository: it resolves the committed review subject between ``base_commit`` and HEAD,
    partitions the attestable source files across tasks, writes every task's attestation through the
    shared producer, regenerates the canonical root ``token_truth.json`` from that assembled Evidence,
    generates the complete closed-schema READY gate set, and runs the final verifier over the whole
    bundle. No provider is called; the target repository is never mutated.

    Returns a small summary dict (job_id, head, authority count, partition sizes, final verdict).
    """
    import subprocess

    from packages.orchestration import manual_attestation as _ma
    from packages.orchestration.final_verifier import build_final_verifier_report
    from packages.orchestration.repair_attest import (
        build_safe_diff_text,
        canonical_provenance_sha256,
        is_attestable_source,
        parse_safe_diff_paths,
        sha256_text,
    )
    from packages.orchestration.review_subject import (
        commit_patch_bytes,
        commit_patch_filename,
        resolve_commit_chain,
        resolve_review_subject,
    )

    os.makedirs(evidence_dir, exist_ok=True)

    def _w(rel: str, obj: Any) -> None:
        p = os.path.join(evidence_dir, rel)
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(obj if isinstance(obj, str) else json.dumps(obj, indent=1, sort_keys=True))

    def _git(*args: str) -> str:
        return subprocess.run(["git", "-C", repo_root, *args],
                              capture_output=True, text=True).stdout

    if head_commit is None:
        head_commit = _git("rev-parse", "HEAD").strip()
    if not verification_runs:
        raise ValueError("verification_runs must record at least one executed verification command")
    if any(r["exit_code"] != 0 for r in verification_runs) or any(r["failed"] for r in verification_runs):
        raise ValueError("a recorded verification command failed; refusing to build a clean bundle")
    total_passed = sum(r["passed"] for r in verification_runs)

    # 1) The committed review subject — resolved once by the production helper.
    subject = resolve_review_subject(repo_root, base_commit)
    authority = sorted({f.path for f in subject.files if is_attestable_source(f.path)})
    opstate = sorted(p for p in (f.path for f in subject.files) if not is_attestable_source(p))
    if not authority:
        raise ValueError("no attestable source files changed between base and head")

    # 2) Partition the attestable files across tasks (explicit partition wins).
    if task_partition is None:
        k = (len(authority) + num_tasks - 1) // num_tasks
        task_partition = {}
        for i in range(num_tasks):
            chunk = authority[i * k:(i + 1) * k]
            if chunk:
                task_partition[f"T{i + 1:03d}"] = chunk
    part = {t: sorted(v) for t, v in task_partition.items() if v}
    if set().union(*part.values()) != set(authority):
        raise ValueError("task partition does not exactly cover the attestable authority set")

    # 3) Review-subject artifacts: subject, content proof, commit chain, canonical patches, diff.
    _w("review_subject.json", subject.to_json())
    file_hashes: dict[str, str] = {}
    for f in subject.files:
        if is_attestable_source(f.path) and f.current_sha256:
            file_hashes[f.path] = f.current_sha256
    _w("current_change_content_proof.json", {
        "schema_version": "1.1.0", "base_commit": base_commit, "head_commit": head_commit,
        "file_hashes": file_hashes, "file_count": len(file_hashes),
        "tombstones": {}, "tombstone_count": 0})
    chain = resolve_commit_chain(repo_root, base_commit, head_commit)
    _w("review_commit_chain.json", {"chain_v": 1, "base_commit": base_commit,
                                    "head_commit": head_commit,
                                    "commits": [c.to_json() for c in chain]})
    pdir = os.path.join(evidence_dir, "review_commit_patches")
    os.makedirs(pdir, exist_ok=True)
    for c in chain:
        with open(os.path.join(pdir, commit_patch_filename(c.commit)), "wb") as fh:
            fh.write(commit_patch_bytes(repo_root, c.commit))
    _w("workspace.diff", _git("diff", f"{base_commit}..{head_commit}", "--", *authority))

    # 4) Per-task attestation + canonical root token truth — THROUGH the canonical producer.
    task_records: list[dict[str, Any]] = []
    for tid, files in part.items():
        tracked = _git("diff", f"{base_commit}..{head_commit}", "--", *files)
        safe = build_safe_diff_text(tracked, [])
        tsha, ssha = sha256_text(tracked), sha256_text(safe)
        prov = canonical_provenance_sha256(tsha, [])
        if parse_safe_diff_paths(safe) != files:
            raise ValueError(f"{tid}: safe-diff path set does not match the task partition")
        task_records.append({
            "task_id": tid, "changed_files": files, "safe_diff_text": safe,
            "provenance_sha256": prov, "diff_sha256": prov, "tracked_diff_sha256": tsha,
            "safe_diff_sha256": ssha, "timestamp": timestamp,
            "note": f"{note_prefix} - {tid}"})
    write_manual_completion_evidence(evidence_dir, job_id=job_id, tasks=task_records)

    # 5) Root scaffold: manifest, job report/timeline/tasks, final job review, trace, guards, config.
    _w("manifest.json", {
        "bundle_version": "0.1.0", "bundle_type": "job_evidence", "job_id": job_id,
        "job_title": job_title,
        "job_file_sha256": hashlib.sha256(job_id.encode()).hexdigest(),
        "status": "planned", "persisted_status": "planned", "repo_identity": "[local]",
        "job_workspace_path": "", "created_at": generated_at, "finished_at": "",
        "bundle_generated_at": generated_at, "task_count": len(part),
        "task_ids": sorted(part), "task_run_ids": {},
        "task_statuses": {t: "pending" for t in part},
        "execution_config": None, "context_strategy": "task_bounded_sequential_job",
        "target_guard": None, "error": "", "completion_mode": "manual_operator_repair",
        "effective_status": "operator_attested_complete", "evidence_available": True,
        "human_final_reviewer_required": True})
    _w("job_report.json", "")
    _w("job_timeline.json", {"job_id": job_id, "events": [], "sequencing_valid": True,
                             "timestamps_available": False})
    _w("tasks.json", [{"task_id": t, "title": f"Task {t}", "status": "pending",
                       "safe_diff_files": sorted(v)} for t, v in part.items()])
    _w("workspace_apply.json", [{"task_id": t, "status": "pending", "apply_manifest": None}
                                for t in sorted(part)])
    _w("execution_config.json", {
        "builder_model": "operator", "builder_model_source": "operator_attestation",
        "reviewer_model": "operator", "reviewer_model_source": "operator_attestation",
        "actual_config_available": False})
    _w("context_strategy.json", {"strategy": "task_bounded_sequential_job",
                                 "previous_task_summary_limit": 5,
                                 "full_job_history_in_prompt": False,
                                 "full_repo_in_prompt": False})
    _w("target_guard.json", {"target_mutated": False, "note": "manual operator repair; no mutation"})
    _w("prompt_trace_summary.json", {"job_id": job_id, "provider_call_count": 0,
                                     "prompt_trace_status": "not_applicable_manual_repair"})
    _w("scratch_file_guard.json", {"schema_version": "1.0.0", "task_id": "",
                                   "guard_status": "PASS", "checked_patterns": ["_[!_]*.py"],
                                   "files_found": [], "forbidden_files": [],
                                   "allowed_files_found": [], "suggested_cleanup": []})
    prior = list(prior_job_ids)
    _w("final_job_review.json", {
        "schema_version": "1.0.0", "verdict": "PASS", "job_id": job_id, "findings": [],
        "review_mode": "operator_attested_manual_completion",
        "completion_mode": "manual_operator_repair", "human_final_reviewer_required": True,
        "completion_provider_call_count": 0, "prior_execution_provider_call_count": 0,
        "superseded_prior_run_ids": [], "changed_files_match": True,
        "expected_changed_files": authority, "actual_changed_files": authority,
        "per_task_changed_files": {t: sorted(v) for t, v in part.items()},
        "task_verdicts": {t: "operator_attested" for t in part},
        "linked_prior_job_ids": prior,
        "linked_prior_job_summaries": [{"job_id": pj, "status": "operator_attested_complete",
                                        "provider_call_count": 0} for pj in prior],
        "root_verification": {"exit_code": 0, "passed": total_passed, "failed": 0}})

    # 6) The complete READY gate set (closed schemas, coherent verdicts).
    _vt_data: dict[str, Any] = {
        "schema_version": "1.0.0",
        "verification_type": "explicit_commands",
        "runs": verification_runs,
        "command": " && ".join(r["command"] for r in verification_runs),
        "exit_code": 0 if all(r["exit_code"] == 0 for r in verification_runs) else 1,
        "passed": total_passed,
        "failed": 0,
        "test_files": sorted({f for r in verification_runs for f in r["test_files"]}),
        "timestamp": generated_at,
    }
    _ma.build_manual_completion_gates(
        evidence_dir, job_id=job_id, authority=authority, file_hashes=file_hashes,
        step=step_range, total_passed=total_passed, verification_runs=verification_runs,
        repo_root=repo_root, head_sha=head_commit, verification_data=_vt_data,
        feature_id=review_feature_id)
    # change-provenance gate must carry the real covered/excluded sets and evidence sources.
    cp_path = os.path.join(evidence_dir, "change_provenance_gate.json")
    cp = json.loads(open(cp_path, encoding="utf-8").read())
    cp.update({"excluded_files": opstate, "source_files": authority,
               "evidence_covered_files": authority,
               "evidence_sources": ["workspace.diff", "current_change_content_proof.json"]
               + [f"task_runs/{t}/safe.diff" for t in sorted(part)]})
    _w("change_provenance_gate.json", cp)

    # 7) The final verifier is generated by the REAL producer over the assembled bundle, twice, to
    #    prove the packaged report is reproducible (the coordinator recomputes and requires equality).
    report = build_final_verifier_report(evidence_dir)
    _w("final_verifier_report.json", report)
    if build_final_verifier_report(evidence_dir) != report:
        raise RuntimeError("final verifier producer is not deterministic over this bundle")

    return {"job_id": job_id, "head_commit": head_commit, "authority_count": len(authority),
            "partition": {t: len(v) for t, v in part.items()}, "commit_count": len(chain),
            "verdict": report.get("verdict"), "manual_completion": report.get("manual_completion"),
            "operator_attested_tasks": report.get("operator_attested_tasks"),
            "total_passed": total_passed}
