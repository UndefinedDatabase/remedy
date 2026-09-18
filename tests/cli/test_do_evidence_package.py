"""R-0892 / DECISION F268 D13 — a `remedy do` job's evidence export passes the review-package check.

`scripts/build_review_manifest.py`'s `validate_evidence_candidate` requires four root files
whose only writers left with `do job-flow`; `export_job_evidence` writes them again from the
job's own records. In-process through `apps.cli.grouped.main` on a temporary git repository,
the data root under `tmp_path`, the fake builder and reviewer, `--no-llm` and `--no-ui`.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main

ORDER = "Write a CONTRIBUTING.md"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    """An unregistered git repository with one committed file, as the working directory."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = tmp_path / "target"
    target.mkdir()
    _git(target, "init", "-q")
    _git(target, "config", "user.email", "t@e.com")
    _git(target, "config", "user.name", "T")
    _git(target, "config", "commit.gpgsign", "false")
    (target / "README.md").write_text("# target\n")
    _git(target, "add", "-A")
    _git(target, "commit", "-qm", "init")
    monkeypatch.chdir(target)
    return target.resolve()


@pytest.fixture(autouse=True)
def no_model_call(monkeypatch):
    """Every factory that could reach a model fails the test when called."""
    def tripwire(*args, **kwargs):
        raise AssertionError("remedy do reached a model-call factory under --no-llm")

    monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", tripwire)


def _do_job(capsys) -> str:
    main(["do", ORDER, "--no-llm", "--no-ui", "--json",
          "--builder-provider", "fake", "--reviewer-provider", "fake"])
    [job_id] = json.loads(capsys.readouterr().out)["job_ids"]
    return job_id


def _export(job_id: str, out: Path, **kwargs) -> Path:
    from packages.orchestration.job_evidence import export_job_evidence

    result = export_job_evidence(job_id, str(out), **kwargs)
    assert not result.get("error"), result
    return out


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_a_do_jobs_exported_evidence_passes_the_review_package_check(repo, tmp_path, capsys):
    from scripts.build_review_manifest import validate_evidence_candidate

    out = _export(_do_job(capsys), tmp_path / "evidence")

    validation = validate_evidence_candidate(str(out))

    errors = validation["validation_errors"]
    assert not [e for e in errors if e.startswith("missing root artifact")], errors
    assert not [e for e in errors if e.startswith("task_runs/") and ": missing" in e], errors
    assert validation["is_valid_current_run"] is True, errors
    assert set(validation["required_root_artifacts"].values()) == {"present"}
    assert validation["missing_observability_artifacts"] == []


@pytest.mark.parametrize("verdict", ["PASS", "NEEDS_TESTS"])
def test_job_flow_final_audit_status_is_the_exports_own_verifier_verdict(
        repo, tmp_path, capsys, monkeypatch, verdict):
    """The status is read from `final_verifier_report.json`, never chosen: two different
    verdicts written by the verifier reach `job_flow.json` unchanged."""
    import packages.orchestration.final_verifier as final_verifier

    real_writer = final_verifier.write_final_verifier_report

    def writer_with_verdict(out_dir, written, *args, **kwargs):
        result = real_writer(out_dir, written, *args, **kwargs)
        report_path = Path(out_dir) / "final_verifier_report.json"
        report = _read(report_path)
        report["verdict"] = verdict
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return result

    job_id = _do_job(capsys)
    monkeypatch.setattr(final_verifier, "write_final_verifier_report", writer_with_verdict)
    out = _export(job_id, tmp_path / "evidence")

    assert _read(out / "final_verifier_report.json")["verdict"] == verdict
    assert _read(out / "job_flow.json")["final_audit"]["status"] == verdict


def test_the_unforced_verdict_reaches_job_flow_and_the_manifest_check(repo, tmp_path, capsys):
    from scripts.build_review_manifest import validate_evidence_candidate

    out = _export(_do_job(capsys), tmp_path / "evidence")

    fv_verdict = _read(out / "final_verifier_report.json")["verdict"]
    job_flow = _read(out / "job_flow.json")
    assert job_flow["final_audit"]["status"] == fv_verdict
    assert validate_evidence_candidate(str(out))["final_audit_status"] == fv_verdict
    tg = _read(out / "target_guard.json")
    assert job_flow["target_guard"]["mutated_target"] is tg["target_mutated"] is False


def test_the_trace_reconstructs_each_round_from_the_run_record(repo, tmp_path, capsys):
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.pingpong_loop import load_run

    job_id = _do_job(capsys)
    out = _export(job_id, tmp_path / "evidence")

    [task] = load_job_plan(job_id).tasks
    rounds = load_run(task.run_id)["rounds"]
    events = [json.loads(line) for line in
              (out / "agent_run_trace.jsonl").read_text(encoding="utf-8").splitlines()]
    builder_rounds = [e["round"] for e in events
                      if e["event_kind"] in ("builder_prompt_created", "repair_prompt_created")]
    assert builder_rounds == [r["round"] for r in rounds if r.get("builder")]
    assert {e["provider"] for e in events if e["role"]} == {"fake"}
    summary = _read(out / "agent_run_trace_summary.json")
    assert summary["total_events"] == len(events)
    assert summary["tasks_traced"] == [task.task_id]


def test_a_fake_run_with_no_command_has_an_empty_transcript_and_says_why(
        repo, tmp_path, capsys):
    out = _export(_do_job(capsys), tmp_path / "evidence")

    transcript = _read(out / "command_transcript.json")
    assert transcript["commands"] == []
    assert "no executed command" in transcript["reason"]


def test_an_executed_verification_command_is_the_transcripts_one_entry(
        repo, tmp_path, capsys):
    def runner(command):
        return {"exit_code": 3, "passed": 0, "failed": 1, "stdout_summary": "1 failed"}

    out = _export(_do_job(capsys), tmp_path / "evidence",
                  verification_commands=["python3 -m pytest -q tests/test_x.py"],
                  verification_runner=runner)

    transcript = _read(out / "command_transcript.json")
    assert [(c["command_id"], c["argv_safe"], c["exit_code"])
            for c in transcript["commands"]] == [
        ("verification_command", "python3 -m pytest -q tests/test_x.py", 3)]
    assert "reason" not in transcript


def test_the_mirrored_required_lists_equal_the_manifest_scripts_own():
    from packages.orchestration import job_evidence
    from scripts import build_review_manifest as manifest_script

    assert list(job_evidence.REVIEW_REQUIRED_ROOT_ARTIFACTS) == (
        manifest_script.REQUIRED_ROOT_ARTIFACTS)
    assert list(job_evidence.REVIEW_REQUIRED_TASK_ARTIFACTS) == (
        manifest_script.REQUIRED_TASK_ARTIFACTS)
    assert job_evidence.REVIEW_MANUAL_REPAIR_EXEMPT_ARTIFACTS == (
        manifest_script.MANUAL_REPAIR_EXEMPT_ARTIFACTS)
