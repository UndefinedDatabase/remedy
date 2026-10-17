"""`review_reports`: `remedy do --capture-review` leaves a report however the walk ends (exec-1017 D5)."""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path

import pytest

from packages.orchestration import review_reports as RR
from tests.orchestration.scale_harness import FakePlannerService, commit_repository

FILES = {"README.md": "# Lab\n", "package.json": json.dumps({"scripts": {"test": "node --test"}}) + "\n"}
ORDER = "Add a usage section to README.md. Change nothing else."


def _do(tmp_path: Path, monkeypatch, *flags: str, order: str = ORDER) -> dict:
    from apps.cli.grouped import main

    repo = commit_repository(tmp_path / "lab", FILES)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.chdir(repo)
    FakePlannerService(target="README.md").install(monkeypatch)
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
        main(["do", order, "--repo", ".", "--builder-provider", "fake", "--reviewer-provider", "fake",
              "--json", "--no-ui", "--run-unattended", "--max-provider-calls", "20", *flags])
    return json.loads(out.getvalue())


def _reports(tmp_path: Path) -> list[dict]:
    folder = tmp_path / "data" / RR.REVIEW_REPORTS_CLASS
    return [json.loads(path.read_text()) for path in sorted(folder.glob("*.json"))] if folder.is_dir() else []


def test_a_walk_with_the_flag_leaves_one_report_naming_everything_without_a_job_id(tmp_path, monkeypatch):
    answer = _do(tmp_path, monkeypatch, "--capture-review")

    [report] = _reports(tmp_path)
    assert answer["review_report"] == {"report_id": report["report_id"], "status": "completed",
                                       "file": f"review_reports/{report['report_id']}.json"}
    assert report["schema"] == RR.REVIEW_REPORT_SCHEMA and report["ended_at"]
    assert report["order"]["text"] == ORDER
    assert report["configuration"]["lane"] == "bounded"
    assert report["configuration"]["flags"]["capture_review"] is True
    [job] = report["jobs"]
    assert job["job_id"] == answer["job_ids"][0] and job["state"] == "completed"
    [task] = job["tasks"]
    assert task["deliverable"] == "README.md" and task["changed_files"] == ["README.md"]
    [run] = task["runs"]
    assert run["rounds"][0]["builder_ms"] is not None and run["rounds"][-1]["reviewer_verdict"] == "pass"
    assert job["verification"]["status"] in ("passed", "failed", "not_run", "not_required")
    assert report["not_measured"]


def test_without_the_flag_no_report_is_written(tmp_path, monkeypatch):
    answer = _do(tmp_path, monkeypatch)

    assert answer["review_report"] is None and _reports(tmp_path) == []


def test_a_failed_walk_still_leaves_a_report_saying_it_failed(tmp_path, monkeypatch):
    monkeypatch.setattr("packages.orchestration.pingpong_provider.FakeProvider.build",
                        lambda self, *a, **k: __import__("packages.orchestration.pingpong_provider",
                                                         fromlist=["BuilderOutput"]).BuilderOutput(
                            error="provider_error: fake builder down", provider="fake"))
    _do(tmp_path, monkeypatch, "--capture-review")

    [report] = _reports(tmp_path)
    assert report["outcome"]["status"] == "failed" and report["outcome"]["reason"].startswith("run: ")


@pytest.mark.parametrize(("raised", "status"), [
    (KeyboardInterrupt("SIGTERM"), "cancelled"), (KeyboardInterrupt(), "cancelled"), (RuntimeError("boom"), "crashed")])
def test_an_interrupted_or_crashed_walk_finishes_its_report(tmp_path, monkeypatch, raised, status):
    from packages.orchestration import do_sequence

    def _broken_step(ctx):
        raise raised

    table = {**do_sequence.DO_STEP_TABLE, "run": _broken_step}
    monkeypatch.setattr(do_sequence, "DO_STEP_TABLE", table)
    # The CLI turns an unexpected error into its own exit; an interrupt goes on up.
    with pytest.raises(KeyboardInterrupt) if isinstance(raised, KeyboardInterrupt) else contextlib.nullcontext():
        _do(tmp_path, monkeypatch, "--capture-review")

    [report] = _reports(tmp_path)
    assert report["outcome"]["status"] == status and report["ended_at"]
    assert report["job_ids"]                       # the planned job is named although it never ran


def test_a_report_holds_no_secret_and_no_home_directory(tmp_path, monkeypatch):
    secret = "sk-ant-api03-" + "A" * 40
    _do(tmp_path, monkeypatch, "--capture-review",
        order=f"Add a usage section to README.md. ANTHROPIC_API_KEY={secret} must not leak.")

    text = json.dumps(_reports(tmp_path))
    assert secret not in text
    assert os.path.expanduser("~") not in text


def test_the_running_report_is_written_before_the_walk_starts(tmp_path, monkeypatch):
    from packages.orchestration.do_context import DoContext

    ctx = DoContext(order="x", capture_review=True)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    with RR.capture_review_report(ctx):
        [running] = _reports(tmp_path)
        assert running["outcome"]["status"] == "running" and running["ended_at"] is None
    [final] = _reports(tmp_path)
    assert final["report_id"] == running["report_id"] and final["outcome"]["status"] == "completed"


def test_the_http_order_flag_reaches_remedy_do_and_cli_only_providers_are_refused(tmp_path, monkeypatch):
    from packages.orchestration.project_registry import register_project_repo
    from packages.orchestration.public_api_writes import PublicApiWriteRefusal, _order_text_and_options

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    register_project_repo("lab", commit_repository(tmp_path / "lab", FILES))
    order = "---\nproject: lab\nmax-provider-calls: 5\n---\nFix README.md.\n"

    _text, options = _order_text_and_options({"order": order, "capture_review": True})
    assert "--capture-review" in options
    with pytest.raises(PublicApiWriteRefusal) as refused:
        _order_text_and_options({"order": order, "builder_provider": "claude-cli"})
    assert (refused.value.status, refused.value.error) == (400, "api_provider_not_offered")
    assert "outside Remedy's tool sandbox" in refused.value.message
    with pytest.raises(PublicApiWriteRefusal):
        _order_text_and_options({"order": order, "builder_provider": "ollama"})   # ollama cannot write
