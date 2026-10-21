"""A finished job's certificate sources, claims and issue record (F060 T002, DECISION F060 D2)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import (
    job_dir,
    job_evidence_dir,
    job_evidence_export_dir,
    run_log_dir,
)
from packages.orchestration.job_certificate import (
    CERTIFICATE_DEFAULT_MAX_BYTES,
    CertificateError,
    build_job_certificate,
)
from packages.orchestration.job_certificate_sources import (
    CERTIFICATE_ISSUES_FILENAME,
    CertificateNotReadyError,
    collect_certificate_inputs,
    next_certificate_issue,
    record_certificate_issue,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

STARTED = "2026-10-01T00:00:00+00:00"
GOOD_ACTUALS = {
    "schema_version": "2.0.0", "provider_call_count": 2, "actual_call_count": 2,
    "unmeasured_call_count": 0, "total_tokens": 10, "actual_sources": ["pingpong_actuals"],
    "started_at": STARTED, "measured_cost_usd": 0.5, "priced_call_count": 2,
    "unpriced_call_count": 0,
}
DIFF_BYTES = b"--- a/x\n+++ b/x\n@@ -1 +1 @@\n-old\n+new\n"


def _make_job(state: RunState) -> JobPlan:
    return JobPlan(
        job_title="certificate-job",
        user_prompt="build the thing",
        tasks=[TaskEntry(title="task 0", inputs={"task_type": "documentation"})],
        state=state,
        # A job with no target repository derives one open decision; this one has a repository.
        metadata={"target_repo": "/repo/fixture"},
    )


def _put(path: Path, data: bytes) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def _by_path(inputs) -> dict:
    return {s.path: s for s in inputs.sources}


def _full_job():
    job = _make_job(RunState.COMPLETED)
    job.project_id = "project-fixture"
    job.isolation_mode = "worktree"
    job.result_diff_path = "result.diff"
    job.result_diff_sha256 = hashlib.sha256(DIFF_BYTES).hexdigest()
    job.result_diff_size_bytes = len(DIFF_BYTES)
    job.first_running_at = STARTED
    job.budget_actuals = dict(GOOD_ACTUALS)
    save_job_plan(job)
    return job


def test_a_completed_worktree_job_with_every_file_yields_every_member():
    job = _full_job()
    jid = str(job.job_id)
    evidence, export = job_evidence_dir(jid), job_evidence_export_dir(jid)
    expected = {
        "report.md": ("report", _put(evidence / "report.md", b"# Run report\n\n- State: completed\n")),
        "token/token_truth.json": ("token_truth", _put(export / "token_truth.json", b'{"t": 1}\n')),
        "verdicts/dod_result.json": ("verdicts", _put(evidence / "dod_result.json", json.dumps({
            "released": True,
            "checks": [{"status": "passed"}, {"status": "passed"}, {"status": "failed"}]}).encode())),
        "verdicts/final_verifier_report.json": ("verdicts", _put(
            export / "final_verifier_report.json", b'{"test_status": "passed"}\n')),
        "ownership/ownership.json": ("ownership", _put(export / "ownership.json", b'{"o": 1}\n')),
        "run_manifest/run_manifest_index.json": ("run_manifest", _put(
            evidence / "run_manifest_index.json", b'{"i": 1}\n')),
        "run_manifest/run_manifest.json": ("run_manifest", _put(
            evidence / "run_manifest.json", b'{"m": 1}\n')),
        "diff/result.diff": ("diff", _put(job_dir(jid) / "result.diff", DIFF_BYTES)),
        "logs/run.jsonl": ("log", _put(run_log_dir(jid) / "run.jsonl", b'{"e": 1}\n')),
    }
    inputs = collect_certificate_inputs(jid)
    got = _by_path(inputs)
    assert {(p, s.member_class) for p, s in got.items()} == (
        {(p, c) for p, (c, _d) in expected.items()} | {("token/budget_actuals.json", "token_truth")})
    for path, (_cls, data) in expected.items():
        assert got[path].data == data
    assert json.loads(got["token/budget_actuals.json"].data) == {
        "budget_actuals": GOOD_ACTUALS, "first_running_at": STARTED}
    assert got["diff/result.diff"].obtain == (
        f"Fetch jobs/{jid}/result.diff from the Remedy data folder that ran this job; "
        f"its sha256 is in this manifest.")
    assert got["logs/run.jsonl"].obtain == (
        f"Fetch job_logs/{jid}/run.jsonl from the Remedy data folder that ran this job; "
        f"its sha256 is in this manifest.")
    assert inputs.job_id == jid
    assert inputs.project_id == "project-fixture"
    assert inputs.issue == 1
    assert inputs.claims == {
        "terminal_state": "completed",
        "dod_summary": {"released": True, "check_count": 3, "passed_count": 2},
        "cost": "$0.5000", "cost_basis": ["pingpong_actuals"],
        "decisions_count": 0, "regression_status": "passed"}


def test_a_failed_job_with_only_its_record_yields_a_rendered_report(tmp_path):
    job = _make_job(RunState.FAILED)
    save_job_plan(job)
    inputs = collect_certificate_inputs(str(job.job_id))
    assert [s.path for s in inputs.sources] == ["report.md"]
    assert "- State: failed" in inputs.sources[0].data.decode("utf-8")
    assert inputs.claims == {
        "terminal_state": "failed", "dod_summary": None, "cost": None, "cost_basis": [],
        "decisions_count": 0, "regression_status": None}
    out = tmp_path / "cert.zip"
    build_job_certificate(
        out_path=out, job_id=inputs.job_id, project_id=inputs.project_id,
        created="2026-10-21T00:00:00Z", issue=inputs.issue, sources=inputs.sources,
        claims=inputs.claims, size_budget_bytes=CERTIFICATE_DEFAULT_MAX_BYTES)
    assert out.is_file()


NOT_READY = ("pending", "planned", "running", "paused")
TERMINAL = ("blocked", "cancelled", "completed", "failed", "stopped")


@pytest.mark.parametrize("state", TERMINAL)
def test_each_terminal_state_is_accepted(state):
    job = _make_job(RunState(state))
    save_job_plan(job)
    assert collect_certificate_inputs(str(job.job_id)).claims["terminal_state"] == state


@pytest.mark.parametrize("state", NOT_READY)
def test_a_job_that_has_not_ended_is_refused(state):
    job = _make_job(RunState(state))
    save_job_plan(job)
    jid = str(job.job_id)
    with pytest.raises(CertificateNotReadyError) as exc:
        collect_certificate_inputs(jid)
    assert str(exc.value) == (
        f"Job {jid} is {state}, and a certificate is made only for a job that has ended: "
        f"blocked, cancelled, completed, failed or stopped.")


def test_an_unknown_job_is_refused_naming_its_id():
    with pytest.raises(CertificateNotReadyError) as exc:
        collect_certificate_inputs("no-such-job")
    assert str(exc.value) == "No job no-such-job is recorded in this Remedy data folder."


def test_a_persisted_report_naming_another_state_is_replaced_by_the_rendering():
    job = _make_job(RunState.FAILED)
    save_job_plan(job)
    jid = str(job.job_id)
    _put(job_evidence_dir(jid) / "report.md", b"# Run report\n\n- State: completed\n")
    text = collect_certificate_inputs(jid).sources[0].data.decode("utf-8")
    assert "- State: failed" in text.splitlines()
    assert "- State: completed" not in text.splitlines()


def test_a_persisted_report_naming_the_jobs_state_is_used_byte_for_byte():
    job = _make_job(RunState.FAILED)
    save_job_plan(job)
    jid = str(job.job_id)
    data = _put(job_evidence_dir(jid) / "report.md", "# Mine\n\n- State: failed\nümlaut\n".encode())
    assert collect_certificate_inputs(jid).sources[0].data == data


def test_actuals_that_cannot_be_decoded_leave_the_member_and_no_cost():
    job = _make_job(RunState.COMPLETED)
    job.budget_actuals = {"schema_version": "9.9.9"}
    save_job_plan(job)
    inputs = collect_certificate_inputs(str(job.job_id))
    member = _by_path(inputs)["token/budget_actuals.json"]
    assert json.loads(member.data)["budget_actuals"] == {"schema_version": "9.9.9"}
    assert inputs.claims["cost"] is None
    assert inputs.claims["cost_basis"] == []


def test_the_issue_record_counts_lines_and_writes_exactly_its_keys():
    job = _make_job(RunState.COMPLETED)
    save_job_plan(job)
    jid = str(job.job_id)
    assert next_certificate_issue(jid) == 1
    record_certificate_issue(jid, issue=1, created="2026-10-21T00:00:00Z", path="/x/cert.zip",
                             manifest_sha256="ab" * 32)
    assert next_certificate_issue(jid) == 2
    lines = (job_dir(jid) / CERTIFICATE_ISSUES_FILENAME).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == {
        "issue": 1, "created": "2026-10-21T00:00:00Z", "path": "/x/cert.zip",
        "manifest_sha256": "ab" * 32}
    assert list(json.loads(lines[0])) == ["issue", "created", "path", "manifest_sha256"]
    assert collect_certificate_inputs(jid).issue == 2


def test_a_symlink_in_place_of_a_member_file_is_refused_naming_it(tmp_path):
    job = _make_job(RunState.COMPLETED)
    save_job_plan(job)
    jid = str(job.job_id)
    target = tmp_path / "elsewhere.json"
    target.write_bytes(b"{}")
    link = job_evidence_dir(jid) / "dod_result.json"
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target)
    with pytest.raises(CertificateError) as exc:
        collect_certificate_inputs(jid)
    assert str(link) in str(exc.value)
