"""F301's Acceptance, held through the command line on a fixture mission of six jobs.

`docs/roadmap/features/T7_F301.md` names four lines: the sixth job of the fixture mission is an
upkeep job whose plan names the planted open finding and the planted oversized file, and a planted
replacement without its deletion is in the ledger and in that plan; skipping an upkeep job without
a recorded decision is impossible through the command line; a mission record and a job record
written before this feature load and run unchanged; and the digest names the jobs left until the
next upkeep job. Every command below runs `remedy` in a child process, as a user does; only the
fixture's records and the jobs' completion are written in this process, because no model runs.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FINDING = {"id": "F-TASK-001", "severity": "repairable", "category": "task_verdict",
           "message": "T001 did not pass review", "task_id": "T001"}
PAIR = {"path": "src/importer_v2.py", "original": "src/importer.py"}


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), check=True, capture_output=True, timeout=60)


@pytest.fixture()
def world(tmp_path, monkeypatch):
    """A data root and a registered project whose repository holds the planted oversized file and
    the planted replacement; answers (data_root, repo, project_id)."""
    data_root = tmp_path / "data"
    repo = tmp_path / "project"
    (repo / "src").mkdir(parents=True)
    body = "".join(f"    x = {n}\n" for n in range(119))
    filler = "".join(f"VALUE_{n} = {n}\n" for n in range(1000))
    (repo / "src" / "big.py").write_text(f"def very_long():\n{body}\n\n{filler}", encoding="utf-8")
    (repo / "src" / "importer.py").write_text("OLD = 1\n", encoding="utf-8")
    (repo / "src" / "importer_v2.py").write_text("NEW = 2\n", encoding="utf-8")
    for args in (("init", "-q"), ("config", "user.email", "f@example.com"), ("config", "user.name", "F"),
                 ("config", "commit.gpgsign", "false"), ("add", "-A"), ("commit", "-qm", "base")):
        _git(repo, *args)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    monkeypatch.delenv("REMEDY_MISSION_UPKEEP_EVERY", raising=False)
    from packages.orchestration.config import reset_config
    from packages.orchestration.project_registry import RemyProject, save_project

    reset_config()
    project = RemyProject(name="Acceptance", slug="f301-acceptance", canonical_repo_path=str(repo))
    save_project(project)
    yield data_root, repo, str(project.id)
    reset_config()


def _remedy(data_root: Path, *args: str, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess:
    """`remedy <args>` in a child process; this tree's code comes first even when ``cwd`` is the
    project, which `remedy status` needs to find it."""
    env = {key: value for key, value in os.environ.items()
           if key not in ("REMEDY_PROJECT", "REMEDY_MISSION_UPKEEP_EVERY")}
    return subprocess.run([sys.executable, "-m", "apps.cli.grouped", *args], cwd=str(cwd),
                          capture_output=True, text=True, timeout=180,
                          env={**env, "REMEDY_DATA_DIR": str(data_root), "PYTHONPATH": str(REPO_ROOT)})


def _ok(proc: subprocess.CompletedProcess) -> dict:
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def _complete(job_id: str, *, finding: bool = False) -> None:
    """The job ran and completed; the first one leaves the planted finding in its final review."""
    from packages.core.models import RunState
    from packages.orchestration.data_paths import job_dir
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    job = load_job_plan(job_id)
    job.state = RunState.COMPLETED
    save_job_plan(job)
    if finding:
        (job_dir(job_id) / "final_job_review.json").write_text(json.dumps({"findings": [FINDING]}),
                                                               encoding="utf-8")


def _digest_mission(data_root: Path, repo: Path, mission_id: str) -> dict:
    client = _ok(_remedy(data_root, "status", "--json", cwd=repo))["client"]
    return next(m for project in client["projects"] for m in project["missions"] if m["mission_id"] == mission_id)


def test_the_sixth_job_is_the_upkeep_job_and_a_skip_needs_its_reason(world):
    from packages.orchestration.mission_upkeep import read_upkeep_ledger

    data_root, repo, project_id = world
    mission_id = _ok(_remedy(data_root, "mission", "start", "Keep the importer working",
                             "--project", project_id, "--json"))["mission"]["id"]
    for step in range(1, 6):
        body = _ok(_remedy(data_root, "mission", "continue", mission_id, f"Step {step}",
                           "--project", project_id, "--json"))
        assert body["upkeep"] is None
        _complete(body["job_id"], finding=step == 1)

    # The digest names the jobs left: none, upkeep is due.
    due = _digest_mission(data_root, repo, mission_id)
    assert (due["upkeep_every"], due["upkeep_jobs_left"], due["upkeep_open_findings"]) == (5, 0, 1)

    # Skipping without a recorded reason is refused and changes nothing.
    refused = _remedy(data_root, "mission", "continue", mission_id, "Step 6", "--project", project_id,
                      "--skip-upkeep", " ")
    assert refused.returncode == 2 and "reason" in refused.stderr
    assert len(_ok(_remedy(data_root, "mission", "show", mission_id, "--project", project_id,
                           "--json"))["mission"]["job_links"]) == 5

    # The sixth job is the upkeep job, and its plan names what was planted.
    sixth = _ok(_remedy(data_root, "mission", "continue", mission_id, "Step 6", "--project", project_id, "--json"))
    step = sixth["tasks"][-1]
    assert sixth["upkeep"]["kind"] == "upkeep_planned" and "Step 6" not in sixth["tasks"]
    assert "finding F-TASK-001" in step
    assert "Shorten the file src/big.py, 1122 lines" in step
    assert "- src/importer.py, replaced by src/importer_v2.py" in step
    [planned] = [line for line in read_upkeep_ledger(project_id, data_root) if line["kind"] == "upkeep_planned"]
    assert planned["job_id"] == sixth["job_id"] and planned["replaced"] == [PAIR]
    assert planned["structure"]["largest_file"]["path"] == "src/big.py"
    assert not any(line["kind"] == "upkeep_skipped" for line in read_upkeep_ledger(project_id, data_root))

    # After it, the digest counts down from five again.
    assert _digest_mission(data_root, repo, mission_id)["upkeep_jobs_left"] == 5


def test_a_mission_and_a_job_written_before_this_feature_load_and_run_unchanged(world):
    from packages.core.models import RunState
    from packages.orchestration.data_paths import job_record_path
    from packages.orchestration.mission_state import mission_record_path
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan

    data_root, _repo, project_id = world
    old_job = JobPlan(job_title="Before F301", state=RunState.COMPLETED, metadata={"mission_role": "initial"})
    save_job_plan(old_job)
    mission_id = "c" * 32
    link = {"job_id": str(old_job.job_id), "role": "initial", "created_at": "2026-10-01T00:00:00+00:00"}
    record = {"schema_version": 1, "id": mission_id, "project_id": project_id, "goal": "Written before F301",
              "status": "active", "job_links": [link], "dossier_ref": "", "created_at": "2026-10-01T00:00:00+00:00"}
    path = mission_record_path(project_id, mission_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record), encoding="utf-8")
    job_bytes = job_record_path(str(old_job.job_id)).read_bytes()

    shown = _ok(_remedy(data_root, "mission", "show", mission_id, "--project", project_id, "--json"))
    assert shown["mission"]["goal"] == "Written before F301" and shown["upkeep"]["jobs_left"] == 4
    nxt = _ok(_remedy(data_root, "mission", "continue", mission_id, "The next step", "--project", project_id,
                      "--json"))
    assert nxt["role"] == "follow_up" and nxt["upkeep"] is None

    after = json.loads(path.read_text(encoding="utf-8"))
    assert sorted(after) == sorted(record) and after["job_links"][0] == link
    assert job_record_path(str(old_job.job_id)).read_bytes() == job_bytes
