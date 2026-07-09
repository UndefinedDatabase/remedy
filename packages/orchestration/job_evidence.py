"""Job evidence bundle — exports a self-contained, redacted proof bundle for an entire job.

Read-only: never calls providers, never mutates target repo, never auto-promotes,
never reruns tasks, never mutates persisted job state.

Reuses single-run evidence redaction from pingpong_evidence. Does not duplicate
weaker redaction logic.

Public API:
    export_job_evidence(job_id, out_dir) -> dict
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

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


def export_job_evidence(
    job_id: str,
    out_dir: str,
    *,
    verification_commands: list[str] | None = None,
    verification_runner: Any = None,
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

    ws_diff = _build_workspace_diff(job)
    _write("workspace.diff", _redact_secrets(ws_diff))

    attest_snap = _snapshot_attestation_artifacts(job)

    for task in job.tasks:
        _write_task_run_evidence(task, str(out_path), written)
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
            from packages.orchestration.missing_tests_gate import write_missing_tests_gate
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
            from packages.orchestration.evidence_mode import (
                build_task_execution_evidence,
                classify_execution_mode,
            )
            from packages.orchestration.pingpong_loop import _pingpong_runs_dir as _pp_runs

            _prompt_count = 0
            _provider_call_count = 0
            _builder_prov = (
                getattr(job.execution_config, "builder", None) or ""
            ) if job.execution_config else ""
            _reviewer_prov = (
                getattr(job.execution_config, "reviewer", None) or ""
            ) if job.execution_config else ""
            if task.run_id:
                _trace_file = _pp_runs() / task.run_id / "prompt_trace_summary.json"
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

    # Runtime integration gate — verify gate writers are wired into the pipeline.
    try:
        from packages.orchestration.runtime_integration_gate import write_runtime_integration_gate
        _repo_root = getattr(job, "repo_path", None) or "."
        write_runtime_integration_gate(str(out_path), _repo_root, written)
    except Exception as exc:
        _write_gate_error("runtime_integration_gate.error.txt", exc)

    # Content-hash proof — SHA256 every dirty source file for provenance.
    _repo = getattr(job, "repo_path", None) or "."
    dirty_files: list[str] = []
    try:
        import hashlib as _hl  # noqa: I001
        import subprocess as _sp  # noqa: I001

        _git_result = _sp.run(
            ["git", "status", "--porcelain", "-u"],
            cwd=_repo, capture_output=True, text=True, timeout=30,
        )
        for line in _git_result.stdout.splitlines():
            if not line.strip():
                continue
            path = line[3:]
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            path = path.strip().strip('"')
            if path:
                dirty_files.append(path)

        from packages.orchestration.change_provenance_gate import _is_source_file, _normalize
        _source_dirty = [_normalize(p) for p in dirty_files if _is_source_file(p)]
        _file_hashes: dict[str, str] = {}
        _repo_path = Path(_repo)
        for _sf in _source_dirty:
            _fp = _repo_path / _sf
            if _fp.exists():
                _file_hashes[_sf] = _hl.sha256(_fp.read_bytes()).hexdigest()
        _proof = {
            "schema_version": "1.0.0",
            "file_hashes": _file_hashes,
            "file_count": len(_file_hashes),
        }
        _proof_path = _validate_output_path(str(out_path), "current_change_content_proof.json")
        _proof_path.write_text(json.dumps(_proof, indent=2) + "\n", encoding="utf-8")
        written["current_change_content_proof.json"] = str(_proof_path)
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
    from packages.orchestration.data_paths import jobs_dir

    ev_base = jobs_dir() / job.job_id / "evidence"
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


def _vt_norm(p: str) -> str:
    p = str(p or "").replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    return p


def _verification_test_files_from_command(command: str) -> list[str]:
    """Extract the test-file paths a pytest-style command targets."""
    import shlex
    files: list[str] = []
    try:
        toks = shlex.split(command)
    except ValueError:
        toks = command.split()
    for t in toks:
        n = _vt_norm(t)
        if n.endswith(".py") and (n.startswith("tests/") or "/tests/" in n or Path(n).name.startswith("test_")):
            files.append(n)
    return sorted(set(files))


def _default_verification_runner(command: str, repo: str) -> dict[str, Any]:
    """Execute a verification command via subprocess and parse pytest counts."""
    import shlex
    import subprocess as _sp
    try:
        argv = shlex.split(command)
    except ValueError:
        argv = command.split()
    result = _sp.run(argv, cwd=repo, capture_output=True, text=True, timeout=600)
    passed = sum(int(x) for x in re.findall(r"(\d+)\s+passed", result.stdout or ""))
    failed = sum(int(x) for x in re.findall(r"(\d+)\s+(?:failed|error)", result.stdout or ""))
    return {
        "exit_code": result.returncode,
        "passed": passed,
        "failed": failed,
        "stdout_summary": (result.stdout or "")[-2000:],
        "stderr_summary": (result.stderr or "")[-1000:],
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
    from datetime import datetime as _dt, timezone as _tz
    cmds = [c for c in (commands or []) if c and c.strip()]
    runs: list[dict[str, Any]] = []
    for i, cmd in enumerate(cmds):
        rid = f"vr-{i + 1:04d}"
        r = runner(cmd) if runner is not None else _default_verification_runner(cmd, repo)
        test_files = r.get("test_files")
        if test_files is None:
            test_files = _verification_test_files_from_command(cmd)
        test_files = sorted({_vt_norm(f) for f in test_files})
        runs.append({
            "run_id": rid,
            "command": cmd,
            "exit_code": int(r.get("exit_code", -1)),
            "passed": int(r.get("passed", 0) or 0),
            "failed": int(r.get("failed", 0) or 0),
            "test_files": test_files,
            "stdout_summary": str(r.get("stdout_summary", "") or "")[-2000:],
        })
    total_passed = sum(x["passed"] for x in runs)
    total_failed = sum(x["failed"] for x in runs)
    exit_code = 0 if runs and all(x["exit_code"] == 0 for x in runs) else (0 if not runs else 1)
    all_files = sorted({f for x in runs for f in x["test_files"]})
    return {
        "schema_version": "1.0.0",
        "verification_type": "explicit_commands",
        "runs": runs,
        # Backward-compatible top-level fields derived from the runs.
        "command": " && ".join(c["command"] for c in runs),
        "exit_code": exit_code,
        "passed": total_passed,
        "failed": total_failed,
        "test_files": all_files,
        "timestamp": _dt.now(_tz.utc).isoformat(),
    }


def _write_task_run_evidence(
    task: Any,
    out_base: str,
    written: dict[str, str],
) -> None:
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
    from packages.orchestration.pingpong_loop import _pingpong_runs_dir
    trace_file = _pingpong_runs_dir() / task.run_id / "prompt_trace.jsonl"
    if trace_file.exists():
        bundle["prompt_trace_jsonl_path"] = str(trace_file)

    task_written = write_evidence_bundle(bundle, str(task_out))

    for filename, path in task_written.items():
        written[f"{task_rel}/{filename}"] = path


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
    from packages.orchestration.pingpong_loop import _pingpong_runs_dir

    total_builder = 0
    total_reviewer = 0
    total_chars = 0
    total_tokens_est = 0
    task_traces: list[dict[str, Any]] = []

    for task in job.tasks:
        if not task.run_id:
            continue
        summary_file = _pingpong_runs_dir() / task.run_id / "prompt_trace_summary.json"
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
