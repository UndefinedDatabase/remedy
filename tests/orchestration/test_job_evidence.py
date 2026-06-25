"""Tests for job evidence bundle export (Steps 4906-4916).

Covers: bundle model, CLI command, file layout, redaction, behavior,
timeline proof, workspace diff, read-only safety, no-provider guarantees.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_PAUSED,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_provider import FakeProvider

_TWO_TASK_JOB = """\
# Job: Evidence Export Test

## Task 1
Add a test file.

Acceptance:
- file exists

## Task 2
Add another test file.

Acceptance:
- file exists
"""


def _pass_provider():
    return FakeProvider(pass_on_round=1, fail_on_round=99)


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n")
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    return repo


def _run_completed_job(demo_repo):
    job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
    return run_job(
        job.job_id,
        builder_provider=_pass_provider(),
        reviewer_provider=_pass_provider(),
        repair_rounds=0,
    )


def _run_blocked_job(demo_repo, monkeypatch):
    job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

    import packages.orchestration.pingpong_loop as pp_mod
    real_run = pp_mod.run_pingpong

    def fail_run(*args, **kwargs):
        result = real_run(*args, **kwargs)
        if result.rounds:
            result.rounds[-1].test_passed = False
        return result

    monkeypatch.setattr(pp_mod, "run_pingpong", fail_run)

    return run_job(
        job.job_id,
        builder_provider=_pass_provider(),
        reviewer_provider=_pass_provider(),
        repair_rounds=0,
    )


def _run_paused_job(demo_repo):
    job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
    return run_job(
        job.job_id,
        builder_provider=_pass_provider(),
        reviewer_provider=_pass_provider(),
        repair_rounds=0,
        max_tasks=1,
    )


# ---------------------------------------------------------------------------
# Step 4913: Behavior tests
# ---------------------------------------------------------------------------


class TestCompletedJobExport:
    def test_completed_job_exports(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        assert result["job_id"] == job.job_id
        assert result["manifest"]["status"] == "completed"

    def test_manifest_json_exists(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        assert (out / "manifest.json").exists()
        data = json.loads((out / "manifest.json").read_text())
        assert data["job_id"] == job.job_id
        assert data["bundle_type"] == "job_evidence"

    def test_summary_md_readable(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        summary = (out / "summary.md").read_text()
        assert "# Remedy Job Evidence" in summary
        assert job.job_id in summary
        assert "T001" in summary
        assert "T002" in summary

    def test_all_top_level_files_present(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        expected = [
            "manifest.json", "summary.md", "job_report.json",
            "job_timeline.json", "tasks.json", "execution_config.json",
            "context_strategy.json", "target_guard.json",
            "workspace_apply.json", "workspace.diff",
        ]
        for f in expected:
            assert (out / f).exists(), f"{f} missing"

    def test_task_run_evidence_nested(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        for task in job.tasks:
            task_dir = out / "task_runs" / task.task_id
            assert task_dir.exists(), f"task_runs/{task.task_id} missing"
            assert (task_dir / "manifest.json").exists()
            assert (task_dir / "summary.md").exists()


class TestBlockedJobExport:
    def test_blocked_job_exports(self, isolate_data_root, demo_repo, monkeypatch, tmp_path):
        job = _run_blocked_job(demo_repo, monkeypatch)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        assert result["manifest"]["status"] == JOB_BLOCKED

    def test_blocked_task_has_evidence(self, isolate_data_root, demo_repo, monkeypatch, tmp_path):
        job = _run_blocked_job(demo_repo, monkeypatch)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        t1_dir = out / "task_runs" / "T001"
        assert t1_dir.exists()


class TestPausedJobExport:
    def test_paused_job_exports(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_paused_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        assert result["manifest"]["status"] == JOB_PAUSED

    def test_paused_pending_task_unavailable(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_paused_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        t2_dir = out / "task_runs" / "T002"
        assert t2_dir.exists()
        manifest = json.loads((t2_dir / "manifest.json").read_text())
        assert manifest["evidence_available"] is False


class TestMissingTaskEvidence:
    def test_task_without_run_id(self, isolate_data_root, demo_repo, tmp_path):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        t1_dir = out / "task_runs" / "T001"
        manifest = json.loads((t1_dir / "manifest.json").read_text())
        assert manifest["evidence_available"] is False
        assert "No run_id" in manifest["reason"]


class TestMissingJob:
    def test_missing_job_returns_error(self, isolate_data_root, tmp_path):
        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence("nonexistent_id", str(tmp_path / "out"))
        assert "error" in result


class TestReadOnly:
    def test_does_not_mutate_target_repo(self, isolate_data_root, demo_repo, tmp_path):
        readme_before = (demo_repo / "README.md").read_text()
        main_before = (demo_repo / "src" / "main.py").read_text()

        job = _run_completed_job(demo_repo)
        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(tmp_path / "evidence"))

        assert (demo_repo / "README.md").read_text() == readme_before
        assert (demo_repo / "src" / "main.py").read_text() == main_before

    def test_does_not_mutate_job_state(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.pingpong_job import load_job_plan
        before = load_job_plan(job.job_id)
        before_status = before.status
        before_tasks = [(t.task_id, t.status) for t in before.tasks]

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(tmp_path / "evidence"))

        after = load_job_plan(job.job_id)
        assert after.status == before_status
        assert [(t.task_id, t.status) for t in after.tasks] == before_tasks


class TestOutputPathTraversal:
    def test_traversal_blocked(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.pingpong_evidence import _validate_output_path
        with pytest.raises(ValueError, match="traversal"):
            _validate_output_path(str(out), "../../../etc/passwd")


# ---------------------------------------------------------------------------
# Step 4910: Timeline proof
# ---------------------------------------------------------------------------


class TestTimelineProof:
    def test_timeline_has_events(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        timeline = json.loads((out / "job_timeline.json").read_text())
        assert len(timeline["events"]) >= 3
        event_types = [e["event"] for e in timeline["events"]]
        assert "job_planned" in event_types
        assert "job_final" in event_types

    def test_timeline_proves_ordering(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        timeline = json.loads((out / "job_timeline.json").read_text())
        sequencing = [
            e for e in timeline["events"]
            if e["event"] == "sequencing_proof"
        ]
        assert len(sequencing) >= 1
        assert "T002" in sequencing[0]["detail"]
        assert "T001" in sequencing[0]["detail"]

    def test_sequencing_valid(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        timeline = json.loads((out / "job_timeline.json").read_text())
        assert timeline["sequencing_valid"] is True


# ---------------------------------------------------------------------------
# Step 4911: Workspace diff
# ---------------------------------------------------------------------------


class TestWorkspaceDiff:
    def test_workspace_diff_present(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        diff = (out / "workspace.diff").read_text()
        assert "workspace diff" in diff.lower() or "---" in diff

    def test_workspace_diff_unavailable_for_planned(self, isolate_data_root, demo_repo, tmp_path):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        diff = (out / "workspace.diff").read_text()
        assert "unavailable" in diff.lower() or "No files applied" in diff


# ---------------------------------------------------------------------------
# Step 4912: Redaction and output scanner tests
# ---------------------------------------------------------------------------

_SECRET_SHAPES = [
    "API_KEY=sk-ant-abc123def456ghi789jkl012mno345pqr",
    "SECRET=mysecretpassword123",
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0",
    "sk-ant-api03-abcdefghijklmnopqrstuvwxyz",
    "sk-abcdefghijklmnopqrstuvwxyz1234567890",
    "ghp_abcdefghijklmnopqrstuvwxyz1234567890",
    "AKIAIOSFODNN7EXAMPLE",
]


class TestRedactionScanner:
    def _export_with_secrets(self, isolate_data_root, demo_repo, tmp_path, monkeypatch):
        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        secret_blob = "\n".join(_SECRET_SHAPES)

        def injecting_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            result.safe_diff_summary = f"--- a/file.py\n+++ b/file.py\n# {secret_blob}"
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", injecting_run)

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        completed = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        out = tmp_path / "evidence"
        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(completed.job_id, str(out))
        return result, out

    def test_no_secrets_in_json_files(self, isolate_data_root, demo_repo, tmp_path, monkeypatch):
        _, out = self._export_with_secrets(isolate_data_root, demo_repo, tmp_path, monkeypatch)

        for json_file in out.rglob("*.json"):
            content = json_file.read_text()
            for secret in _SECRET_SHAPES:
                assert secret not in content, f"Secret leaked in {json_file.name}: {secret[:20]}..."

    def test_no_secrets_in_text_files(self, isolate_data_root, demo_repo, tmp_path, monkeypatch):
        _, out = self._export_with_secrets(isolate_data_root, demo_repo, tmp_path, monkeypatch)

        for text_file in list(out.rglob("*.md")) + list(out.rglob("*.diff")) + list(out.rglob("*.txt")):
            content = text_file.read_text()
            for secret in _SECRET_SHAPES:
                assert secret not in content, f"Secret leaked in {text_file.name}: {secret[:20]}..."

    def test_no_secrets_in_cli_json(self, isolate_data_root, demo_repo, tmp_path, monkeypatch):
        result, _ = self._export_with_secrets(isolate_data_root, demo_repo, tmp_path, monkeypatch)

        result_str = json.dumps(result)
        for secret in _SECRET_SHAPES:
            assert secret not in result_str, f"Secret in CLI JSON: {secret[:20]}..."

    def test_no_raw_task_body_unbounded(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        report = json.loads((out / "job_report.json").read_text())
        for task in report["tasks"]:
            if "body_excerpt" in task:
                assert len(task["body_excerpt"]) <= 600
            assert "body" not in task or task.get("body") is None

    def test_no_absolute_private_paths_leaked(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        manifest = json.loads((out / "manifest.json").read_text())
        home = str(Path.home())
        if home != "/":
            repo_id = manifest.get("repo_identity", "")
            assert not repo_id.startswith(home), f"Absolute home path leaked: {repo_id}"


class TestCLIJsonRedaction:
    def test_cli_handler_json_output(self, isolate_data_root, demo_repo, tmp_path, capsys):
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        out_dir = str(tmp_path / "cli_evidence")
        args = types.SimpleNamespace(
            job_id=job.job_id,
            out=out_dir,
            json=True,
        )
        COMMAND_HANDLERS["do.job-evidence"](args)

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["job_id"] == job.job_id
        assert "error" not in output

    def test_cli_handler_text_output(self, isolate_data_root, demo_repo, tmp_path, capsys):
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        out_dir = str(tmp_path / "cli_evidence")
        args = types.SimpleNamespace(
            job_id=job.job_id,
            out=out_dir,
            json=False,
        )
        COMMAND_HANDLERS["do.job-evidence"](args)

        captured = capsys.readouterr()
        assert "exported to" in captured.out.lower()
        assert "manifest.json" in captured.out


# ---------------------------------------------------------------------------
# Step 4913: Machine-verifiable JSON
# ---------------------------------------------------------------------------


class TestMachineVerifiable:
    def test_all_json_files_parse(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        for json_file in out.rglob("*.json"):
            data = json.loads(json_file.read_text())
            assert isinstance(data, (dict, list)), f"{json_file.name} not dict/list"

    def test_manifest_has_required_fields(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        manifest = json.loads((out / "manifest.json").read_text())
        required = [
            "job_id", "job_title", "status", "task_count",
            "task_ids", "task_statuses", "execution_config",
            "context_strategy", "target_guard",
        ]
        for field in required:
            assert field in manifest, f"Missing field: {field}"

    def test_tasks_json_matches_task_count(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        tasks = json.loads((out / "tasks.json").read_text())
        manifest = json.loads((out / "manifest.json").read_text())
        assert len(tasks) == manifest["task_count"]


# ---------------------------------------------------------------------------
# Step 4914: Dogfood export command shape
# ---------------------------------------------------------------------------


class TestDogfoodCommandShape:
    def test_command_catalog_has_job_evidence(self):
        from apps.cli.command_catalog import CATALOG
        cmd = next(
            (c for c in CATALOG if c.command_id == "do.job-evidence"),
            None,
        )
        assert cmd is not None
        assert cmd.action_class == "read_only"
        assert cmd.may_mutate_repo is False
        assert cmd.may_execute_commands is False

    def test_handler_exists(self):
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS
        assert "do.job-evidence" in COMMAND_HANDLERS

    def test_documented_shape_runs(self, isolate_data_root, demo_repo, tmp_path, capsys):
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        out_dir = str(tmp_path / f"remedy-job-evidence-{job.job_id}")
        args = types.SimpleNamespace(
            job_id=job.job_id,
            out=out_dir,
            json=True,
        )
        COMMAND_HANDLERS["do.job-evidence"](args)

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["manifest"]["status"] == "completed"

        out = Path(out_dir)
        files = sorted(str(f.relative_to(out)) for f in out.rglob("*") if f.is_file())
        assert "manifest.json" in files
        assert "summary.md" in files
