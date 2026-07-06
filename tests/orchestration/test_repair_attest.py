"""Tests for operator repair attestation (F002 T001).

Covers: the four artifact writers, their schema fields, and error handling for
non-existent job/task.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import parse_job_file
from packages.orchestration.repair_attest import attest_operator_repair

_ONE_TASK_JOB = """\
# Job: Operator Repair Test

## Task 1
Fix the broken thing by hand.

Acceptance:
- thing works
"""


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("def hello():\n    return 'hi'\n")

    def _git(*args):
        subprocess.run(["git", *args], cwd=str(repo), check=True,
                       capture_output=True, text=True)

    _git("init", "-q")
    _git("config", "user.email", "t@example.com")
    _git("config", "user.name", "Test")
    _git("add", "-A")
    _git("commit", "-q", "-m", "init")
    # Operator makes a manual repair after the last valid (committed) state.
    (repo / "main.py").write_text("def hello():\n    return 'fixed'\n")
    return repo


def _attest(job, repo, note="operator fixed it by hand"):
    return attest_operator_repair(job.job_id, "T001", note, str(repo))


def test_writes_all_four_json_files(isolate_data_root, git_repo):
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)

    out_dir = Path(result["out_dir"])
    for name in (
        "provider_evidence.json",
        "review.json",
        "token_accounting.json",
        "manual_repair_provenance.json",
    ):
        assert (out_dir / name).exists(), f"missing {name}"
        assert name in result["files"]


def test_provider_evidence_execution_mode(isolate_data_root, git_repo):
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)
    data = json.loads(Path(result["files"]["provider_evidence.json"]).read_text())
    assert data["execution_mode"] == "manual_operator_repair"


def test_review_verdict_operator_attested(isolate_data_root, git_repo):
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)
    data = json.loads(Path(result["files"]["review.json"]).read_text())
    assert data["verdict"] == "operator_attested"
    assert data["reviewer"] == "operator"


def test_token_accounting_manual(isolate_data_root, git_repo):
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)
    data = json.loads(Path(result["files"]["token_accounting.json"]).read_text())
    assert data["actual_available"] is False
    assert data["reason"] == "manual"


def test_provenance_fields(isolate_data_root, git_repo):
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo, note="hand fix")
    data = json.loads(
        Path(result["files"]["manual_repair_provenance.json"]).read_text()
    )
    assert len(data["diff_sha256"]) == 64
    assert len(data["provenance_sha256"]) == 64
    assert len(data["tracked_diff_sha256"]) == 64
    assert "main.py" in data["changed_files"]
    assert data["note"] == "hand fix"
    assert data["timestamp"]


def test_attestation_records_original_task_status(isolate_data_root, git_repo):
    """Attestation includes original_task_status in review.json."""
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)
    review = json.loads(Path(result["files"]["review.json"]).read_text())
    assert "original_task_status" in review
    assert review["human_final_reviewer_required"] is True


def test_attestation_records_workspace_scope(isolate_data_root, git_repo):
    """Attestation provenance includes workspace_scope and task_scope_known."""
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)
    mrp = json.loads(
        Path(result["files"]["manual_repair_provenance.json"]).read_text()
    )
    assert mrp["workspace_scope"] in ("full_working_tree", "task_scoped")
    assert "task_scope_known" in mrp
    assert isinstance(mrp.get("task_scoped_files"), list)


def test_attestation_prompt_trace_status(isolate_data_root, git_repo):
    """Provider evidence records prompt_trace_status for manual repair."""
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)
    pe = json.loads(Path(result["files"]["provider_evidence.json"]).read_text())
    assert pe["prompt_trace_status"] == "not_applicable_manual_repair"


def test_empty_note_produces_default(isolate_data_root, git_repo):
    """Empty note produces safe default instead of invalid attestation."""
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo, note="")
    mrp = json.loads(
        Path(result["files"]["manual_repair_provenance.json"]).read_text()
    )
    assert mrp["note"]
    assert len(mrp["note"].strip()) > 0


def test_whitespace_only_note_produces_default(isolate_data_root, git_repo):
    """Whitespace-only note produces safe default."""
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo, note="   ")
    mrp = json.loads(
        Path(result["files"]["manual_repair_provenance.json"]).read_text()
    )
    assert mrp["note"].strip()


def test_manual_operator_repair_fields_written(isolate_data_root, git_repo):
    """manual_operator_repair and no_provider_calls are always written."""
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)
    mrp = json.loads(
        Path(result["files"]["manual_repair_provenance.json"]).read_text()
    )
    assert mrp["manual_operator_repair"] is True
    assert mrp["no_provider_calls"] is True


def test_untracked_path_change_affects_provenance_hash(isolate_data_root, git_repo):
    """Renaming an untracked file changes provenance hash."""
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    (git_repo / "new_file.txt").write_text("content")
    result1 = _attest(job, git_repo)

    (git_repo / "new_file.txt").unlink()
    (git_repo / "renamed_file.txt").write_text("content")
    result2 = _attest(job, git_repo)

    assert result1["diff_sha256"] != result2["diff_sha256"]


def test_untracked_size_affects_provenance_hash(isolate_data_root, git_repo):
    """Changing untracked file size changes provenance hash."""
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    (git_repo / "data.bin").write_text("short")
    result1 = _attest(job, git_repo)

    (git_repo / "data.bin").write_text("this is much longer content for testing")
    result2 = _attest(job, git_repo)

    assert result1["diff_sha256"] != result2["diff_sha256"]


def test_tracked_file_in_provenance(isolate_data_root, git_repo):
    """Modified tracked file is included in provenance."""
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)
    data = json.loads(
        Path(result["files"]["manual_repair_provenance.json"]).read_text()
    )
    assert "main.py" in data["changed_files"]
    assert len(data["tracked_diff_sha256"]) == 64


def test_untracked_file_in_changed_files(isolate_data_root, git_repo):
    """New untracked file is included in changed_files."""
    (git_repo / "new_file.py").write_text("print('new')\n")
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = _attest(job, git_repo)
    data = json.loads(
        Path(result["files"]["manual_repair_provenance.json"]).read_text()
    )
    assert "new_file.py" in data["changed_files"]
    assert any(h["path"] == "new_file.py" for h in data["untracked_file_hashes"])


def test_untracked_file_content_affects_provenance_hash(isolate_data_root, git_repo):
    """New untracked file content affects provenance hash."""
    (git_repo / "new_file.py").write_text("version_a\n")
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result1 = _attest(job, git_repo)
    data1 = json.loads(
        Path(result1["files"]["manual_repair_provenance.json"]).read_text()
    )

    (git_repo / "new_file.py").write_text("version_b\n")
    result2 = _attest(job, git_repo)
    data2 = json.loads(
        Path(result2["files"]["manual_repair_provenance.json"]).read_text()
    )

    assert data1["provenance_sha256"] != data2["provenance_sha256"]


def test_no_git_repo_empty_provenance(isolate_data_root, tmp_path):
    """No git repo gracefully reports empty provenance."""
    no_git = tmp_path / "no_git_dir"
    no_git.mkdir()
    job = parse_job_file(_ONE_TASK_JOB, str(no_git))
    result = _attest(job, no_git)
    data = json.loads(
        Path(result["files"]["manual_repair_provenance.json"]).read_text()
    )
    assert data["changed_files"] == []
    assert data["untracked_file_hashes"] == []
    assert len(data["provenance_sha256"]) == 64


def test_missing_job_returns_error(isolate_data_root, tmp_path):
    result = attest_operator_repair(
        "nonexistent-job", "T001", "note", str(tmp_path)
    )
    assert "error" in result


def test_missing_task_returns_error(isolate_data_root, git_repo):
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    result = attest_operator_repair(job.job_id, "T999", "note", str(git_repo))
    assert "error" in result


# -- CLI: remedy do repair-attest <job_id> <task_id> [--note "..."] --------


def test_cli_repair_attest_writes_evidence(isolate_data_root, git_repo, capsys):
    from apps.cli.grouped import main

    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    main([
        "do", "repair-attest", job.job_id, "T001",
        "--note", "operator hand fix", "--repo", str(git_repo), "--yes", "--json",
    ])
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["job_id"] == job.job_id
    assert payload["task_id"] == "T001"
    assert len(payload["diff_sha256"]) == 64
    assert "review.json" in payload["files"]

    review = json.loads(Path(payload["files"]["review.json"]).read_text())
    assert review["verdict"] == "operator_attested"


def test_cli_repair_attest_missing_job_exits_nonzero(isolate_data_root, tmp_path):
    from apps.cli.grouped import main

    with pytest.raises(SystemExit) as exc:
        main([
            "do", "repair-attest", "nonexistent-job", "T001",
            "--repo", str(tmp_path), "--yes", "--json",
        ])
    assert exc.value.code == 1


def test_cli_without_yes_does_not_write(isolate_data_root, git_repo):
    """CLI without --yes exits 2 and does not write attestation."""
    from apps.cli.grouped import main

    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    with pytest.raises(SystemExit) as exc:
        main([
            "do", "repair-attest", job.job_id, "T001",
            "--note", "test", "--repo", str(git_repo), "--json",
        ])
    assert exc.value.code == 2


def test_cli_with_yes_writes(isolate_data_root, git_repo, capsys):
    """CLI with --yes writes attestation and exits normally."""
    from apps.cli.grouped import main

    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    main([
        "do", "repair-attest", job.job_id, "T001",
        "--note", "fix", "--repo", str(git_repo), "--yes", "--json",
    ])
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert "error" not in payload
    assert len(payload["diff_sha256"]) == 64


def test_cli_text_output_shows_diff_stat(isolate_data_root, git_repo, capsys):
    """Text output includes diff stat when --yes is passed."""
    from apps.cli.grouped import main

    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    main([
        "do", "repair-attest", job.job_id, "T001",
        "--note", "fix", "--repo", str(git_repo), "--yes",
    ])
    out = capsys.readouterr().out
    assert "Diff stat" in out
    assert "OPERATOR ATTESTED" in out


# -- F002 T003: end-to-end — blocked job -> attest -> verifier PASS ---------


def _seed_blocked_task_evidence(base: Path, task_id: str = "T001") -> None:
    """Seed one task's evidence complete except for a blocking review verdict.

    Everything a clean PASS needs is present, but the reviewer verdict is
    ``needs_repair`` with an open finding — so the final verifier is NOT PASS
    until an operator attestation replaces the reviewer verdict. The blocking
    finding lives in the review rounds only (no ``repair_loop`` open findings),
    since operator attestation is what supersedes that review path.
    """
    d = base / "task_runs" / task_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "review_scope_packet.json").write_text(json.dumps({
        "changed_files": ["main.py"],
        "changed_line_ranges": {"main.py": [[1, 2]]},
    }))
    (d / "spec_compliance_check.json").write_text(json.dumps({"verdict": "PASS"}))
    (d / "missing_tests_gate.json").write_text(json.dumps({"gate_status": "PASS"}))
    (d / "review.json").write_text(json.dumps({
        "final_verdict": "needs_repair",
        "verdict": "needs_repair",
        "reviews": [{
            "round": 1,
            "findings": [{
                "id": "F1", "severity": "high", "file": "main.py",
                "summary": "returns the wrong value",
            }],
        }],
    }))
    (d / "repair_loop.json").write_text(json.dumps({"open_findings": []}))
    (d / "tests.txt").write_text("3 passed in 0.1s\n")
    (d / "safe.diff").write_text("--- a/main.py\n+++ b/main.py\n")
    (d / "token_accounting.json").write_text(json.dumps({
        "actual_tokens_available": False,
        "builder_prompt_tokens_estimated": 100,
        "reviewer_prompt_tokens_estimated": 200,
    }))
    (base / "scratch_file_guard.json").write_text(json.dumps({"guard_status": "PASS"}))
    (base / "token_truth.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "actual_available": False,
        "estimated_prompt_tokens": 300,
        "estimated_total_tokens": 300,
        "measurement_source": "character_heuristic",
        "measurement_confidence": "low",
        "missing_reason": "actual usage unavailable",
        "builder_estimated_total": 100,
        "reviewer_estimated_total": 200,
        "repair_estimated_total": 0,
        "provider_call_count": 2,
    }))
    (base / "execution_config.json").write_text(json.dumps({
        "builder_model": "opus", "builder_actual_model": "opus",
        "reviewer_model": "opus", "reviewer_actual_model": "opus",
        "repair_model": "opus", "repair_actual_model": "opus",
        "actual_config_available": True,
    }))


def test_e2e_blocked_job_attest_verifier_pass(isolate_data_root, git_repo):
    """Full pipeline: a blocked task -> operator attestation -> verifier PASS."""
    from packages.orchestration.data_paths import jobs_dir
    from packages.orchestration.final_verifier import build_final_verifier_report
    from packages.orchestration.token_truth import build_token_truth

    # 1. Fake blocked job with a failed/blocked task.
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    evidence_dir = jobs_dir() / job.job_id / "evidence"
    _seed_blocked_task_evidence(evidence_dir, "T001")

    # Precondition: the verifier is NOT PASS while the task is blocked.
    before = build_final_verifier_report(str(evidence_dir))
    assert before["verdict"] != "PASS"
    assert before["unresolved_findings"], "task should be blocked before attest"

    # 2. Operator attests the manual repair for that task.
    result = attest_operator_repair(
        job.job_id, "T001", "operator fixed by hand", str(git_repo)
    )
    assert "error" not in result

    # 3 + 4. Verifier now PASS with the operator_attested badge.
    report = build_final_verifier_report(str(evidence_dir))
    assert report["verdict"] == "PASS"
    assert report["unresolved_findings"] == []
    assert report["operator_attested_tasks"] == ["T001"]
    assert "[OPERATOR ATTESTED]" in report["report_badges"]

    # 5. token_truth: the attested task has no actual provider usage.
    truth = build_token_truth(str(evidence_dir))
    assert truth["per_task"]["T001"]["actual_available"] is False
    assert truth["actual_available"] is False

    # 6. All four attestation artifacts are present and valid JSON.
    out_dir = Path(result["out_dir"])
    for name in (
        "provider_evidence.json",
        "review.json",
        "token_accounting.json",
        "manual_repair_provenance.json",
    ):
        path = out_dir / name
        assert path.exists(), f"missing {name}"
        assert isinstance(json.loads(path.read_text()), dict), f"invalid JSON: {name}"
