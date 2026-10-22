"""F074 T003 — `remedy stats calibration`, the estimate calibration's trust view.

A real git repository is registered under the test's own data root, its cost ledger and job records
are written as a project's would be, and the command runs as a user runs it, through the grouped CLI.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from apps.cli.command_catalog import get_command
from apps.cli.commands import collect_all_handlers
from packages.orchestration.data_paths import job_record_path, resolve_data_root
from packages.orchestration.estimate_calibration import calibration_snapshot_path
from packages.orchestration.token_ledger import CallRecord, record_call

RECENT = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()


def _run(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return code or 0, capsys.readouterr().out


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from packages.orchestration.project_registry import register_project_repo

    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    repo = tmp_path / "calibrated"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    return register_project_repo("Calibrated", repo)


def _seed(project, classes: tuple[tuple[str, int], ...] = (("standard_build", 20), ("format", 3))) -> None:
    root = resolve_data_root()
    for task_class, count in classes:
        for k in range(1, count + 1):
            job = f"job{task_class}{k:02d}"
            path = job_record_path(job, root)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"tasks": [{"task_id": "T001", "task_class": task_class}]}), encoding="utf-8")
            for role, tokens, cost in (("builder", k * 1000, k * 0.01), ("reviewer", 500, None)):
                assert record_call(CallRecord(
                    call_id=f"{job}:T001:{role}", job_id=job, task_id="T001", role=role, ts_utc=RECENT,
                    tokens_in=tokens - 100, tokens_out=100, cost_usd=cost,
                    cost_basis="unknown" if cost is None else "provider_reported"), project_id=str(project.id))


def test_the_command_is_catalogued_read_only_and_handled():
    entry = get_command("stats.calibration")
    assert entry.action_class == "read_only" and entry.supports_json
    assert "stats.calibration" in collect_all_handlers()


def test_the_text_shows_each_class_and_role_with_its_basis_window_floor_and_age(project, capsys):
    _seed(project)
    # One task whose job record is gone: counted as unclassified, never guessed.
    assert record_call(CallRecord(call_id="jobgone:T001", job_id="jobgone", task_id="T001", role="builder",
                                  ts_utc=RECENT, tokens_in=10, tokens_out=5), project_id=str(project.id))
    code, out = _run(["stats", "calibration", "--project", project.slug], capsys)
    assert code == 0, out
    lines = out.splitlines()
    assert lines[0] == f"Estimate calibration of project {project.id}, measured from its cost ledger"
    assert lines[1].startswith("Window: the last 90 days, tasks whose latest call is at or after ")
    assert lines[1].endswith("Floor: 20 tasks per class.")
    measured = datetime.fromisoformat(lines[2].split("Measured at ", 1)[1].split(",", 1)[0])
    next_read = lines[2].split("the first read after ", 1)[1].removesuffix(" measures again.")
    assert datetime.fromisoformat(next_read) == measured + timedelta(seconds=3600)
    assert lines[3].split() == ["class", "role", "tasks", "tokens", "P20", "P50", "P80", "cost", "P20", "P50",
                                "P80", "estimates"]
    rows = [line.split() for line in lines[4:-1]]
    assert [row[:2] for row in rows] == [["format", "all"], ["format", "builder"], ["format", "reviewer"],
                                         ["standard_build", "all"], ["standard_build", "builder"],
                                         ["standard_build", "reviewer"]]
    assert rows[0] == ["format", "all", "3", "2,500", "2,500", "2,500", "unpriced", "unpriced", "unpriced",
                       "class", "default", "(3", "of", "20)"]
    assert ["format", "builder", "3", "2,000", "2,000", "2,000", "$0.0200", "$0.0200", "$0.0200"] in rows
    assert ["standard_build", "all", "20", "5,900", "11,000", "16,100", "unpriced", "unpriced", "unpriced",
            "calibrated(20)"] in rows
    assert ["standard_build", "builder", "20", "5,400", "10,500", "15,600", "$0.0540", "$0.1050",
            "$0.1560"] in rows
    assert lines[-1] == ("Not counted: 1 tasks with no class on record, 0 tasks whose calls did not all "
                         "report their tokens.")


def test_the_json_names_the_calibrated_classes_and_the_measurement(project, capsys):
    _seed(project)
    code, out = _run(["stats", "calibration", "--project", project.slug, "--json"], capsys)
    assert code == 0, out
    body = json.loads(out)
    assert body["ok"] is True and body["version"] == 1
    assert body["calibrated_classes"] == ["standard_build"]
    assert (body["project_id"], body["sample_floor"], body["window_days"], body["max_age_seconds"]) == (
        str(project.id), 20, 90, 3600)
    whole = next(e for e in body["entries"] if (e["task_class"], e["role"]) == ("standard_build", "all"))
    assert whole["tokens"] == {"n": 20, "p20": 5900.0, "p50": 11000.0, "p80": 16100.0}
    assert whole["cost_usd"] is None


def test_a_second_read_inside_the_age_limit_shows_the_same_measurement(project, capsys):
    _seed(project)
    _run(["stats", "calibration", "--project", project.slug, "--json"], capsys)
    first = json.loads(calibration_snapshot_path(str(project.id)).read_text(encoding="utf-8"))["updated_at"]
    code, out = _run(["stats", "calibration", "--project", project.slug, "--json"], capsys)
    assert code == 0 and json.loads(out)["updated_at"] == first


def test_the_settings_come_from_the_projects_config(project, capsys):
    _seed(project)
    Path(project.canonical_repo_path, "remedy.toml").write_text(
        "[remedy.budget]\ncalibration_sample_floor = 3\n", encoding="utf-8")
    code, out = _run(["stats", "calibration", "--project", project.slug, "--json"], capsys)
    assert code == 0, out
    assert json.loads(out)["calibrated_classes"] == ["format", "standard_build"]


def test_a_project_with_no_ledger_says_every_estimate_stays_on_its_default(project, capsys):
    code, out = _run(["stats", "calibration", "--project", project.slug], capsys)
    assert code == 0, out
    assert out.splitlines()[1] == "This project has no cost ledger yet, so every estimate stays on its class default."
    assert not calibration_snapshot_path(str(project.id)).exists()


def test_a_ledger_with_nothing_in_the_window_says_so(project, capsys):
    root = resolve_data_root()
    path = job_record_path("jobold", root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"tasks": [{"task_id": "T001", "task_class": "format"}]}), encoding="utf-8")
    old = (datetime.now(timezone.utc) - timedelta(days=200)).isoformat()
    assert record_call(CallRecord(call_id="jobold:T001", job_id="jobold", task_id="T001", role="builder", ts_utc=old,
                                  tokens_in=10, tokens_out=5), project_id=str(project.id))
    code, out = _run(["stats", "calibration", "--project", project.slug], capsys)
    assert code == 0, out
    assert ("No measured task falls inside the window, so every estimate stays on its class default."
            in out.splitlines())


def test_no_project_is_refused(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    monkeypatch.chdir(tmp_path)
    code, out = _run(["stats", "calibration", "--json"], capsys)
    assert code == 1
    assert json.loads(out)["error"] == "no_project"


def test_a_malformed_setting_is_refused_as_a_usage_error(project, capsys):
    Path(project.canonical_repo_path, "remedy.toml").write_text(
        "[remedy.budget]\ncalibration_window_days = -4\n", encoding="utf-8")
    code, out = _run(["stats", "calibration", "--project", project.slug, "--json"], capsys)
    assert code == 2
    assert json.loads(out)["error"] == "invalid_budget"
