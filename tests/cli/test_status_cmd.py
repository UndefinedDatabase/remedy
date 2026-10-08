"""`remedy status --json`'s `client` key (T002, DECISION F295 D4).

In-process through `apps.cli.grouped.main`, against a temporary git repository
holding one committed file, with the data root a short directory from
`tmp_path_factory.mktemp` (a unix socket path has a length limit,
`tests/cli/test_serve_cmd.py`), `--no-llm`, `--no-ui` and the fake builder and
reviewer for every `do`. A tripwire fails the test if any model-call factory
is reached.
"""
from __future__ import annotations

import hashlib
import json
import socket as socket_module
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main

FAKE_ROLES = ("--builder-provider", "fake", "--reviewer-provider", "fake")
ORDER = "Write a CONTRIBUTING.md"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


def _git_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@e.com")
    _git(path, "config", "user.name", "T")
    _git(path, "config", "commit.gpgsign", "false")
    (path / "README.md").write_text(f"# {path.name}\n")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "init")
    return path.resolve()


@pytest.fixture
def repo(tmp_path_factory, monkeypatch) -> Path:
    """An UNREGISTERED git repository, its data root a short `tmp_path_factory.mktemp` dir."""
    base = tmp_path_factory.mktemp("sc")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(base / "data"))
    target = _git_repo(base / "target")
    monkeypatch.chdir(target)
    return target


@pytest.fixture(autouse=True)
def no_model_call(monkeypatch):
    """Every factory that could reach a model fails the test when called."""
    def tripwire(*args, **kwargs):
        raise AssertionError("remedy do reached a model-call factory")

    monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", tripwire)


def _do(capsys, order_arg: str, *extra: str) -> str:
    main(["do", order_arg, "--no-llm", "--no-ui", *FAKE_ROLES, *extra])
    return capsys.readouterr().out


def _do_json(capsys, order_arg: str, *extra: str) -> dict:
    return json.loads(_do(capsys, order_arg, "--json", *extra))


def _status_json(capsys) -> dict:
    main(["status", "--json"])
    return json.loads(capsys.readouterr().out)


# ── 1: --plan-only leaves one planned job, waiting on nothing ───────────────


def test_after_plan_only_the_jobs_entry_is_planned_and_nothing_awaits_apply(repo, capsys):
    data = _do_json(capsys, ORDER, "--plan-only")
    [job_id] = data["job_ids"]

    client = _status_json(capsys)["client"]

    assert client["version"] == 1
    [project] = client["projects"]
    [mission] = project["missions"]
    assert mission["job_ids"] == [job_id]
    [job] = client["jobs"]
    assert job["job_id"] == job_id
    assert job["project_id"] == project["project_id"]
    assert job["mission_id"] == mission["mission_id"]
    assert job["state"] == "planned"
    assert job["waits_for_apply"] is False
    assert client["awaiting_apply"] == []


# ── 2: a full `do` stops before apply, so its completed job awaits apply ────


def test_a_full_do_without_apply_completes_the_job_and_it_awaits_apply(repo, capsys):
    data = _do_json(capsys, ORDER)
    [job_id] = data["job_ids"]

    client = _status_json(capsys)["client"]

    [job] = client["jobs"]
    assert job["job_id"] == job_id
    assert job["state"] == "completed"
    assert job["waits_for_apply"] is True
    assert client["awaiting_apply"] == [job_id]


# ── 2b: the completed job's approval card, read through the command line (DECISION F304 D10) ──


def test_a_full_dos_completed_job_carries_its_approval_card_from_its_record(repo, capsys):
    from apps.cli.client_interface import DIGEST_KEY_TREE
    from packages.orchestration.pingpong_job import load_job_plan

    done = _do_json(capsys, ORDER)
    [job_id] = done["job_ids"]

    [job] = _status_json(capsys)["client"]["jobs"]

    record = load_job_plan(job_id)
    card = job["approval_card"]
    assert set(card) == set(DIGEST_KEY_TREE["jobs"]["approval_card"])
    # The fake builder writes one file; the job's result diff, a record of its own, names the same.
    diff = Path(job["evidence"]["result_diff_path"]).read_text(encoding="utf-8")
    assert card["changed_files"] == ["docs/README.md"]
    assert [line[len("+++ b/"):] for line in diff.splitlines()
            if line.startswith("+++ b/")] == card["changed_files"]
    assert card["changed_file_count"] == 1
    assert card["test_command"] is None
    assert card["tasks"] == [
        {"task_id": task.task_id, "title": task.title, "reviewer_verdict": task.reviewer_verdict,
         "repair_rounds_used": task.repair_rounds_used, "test_ran": False, "test_passed": None}
        for task in record.tasks
    ]
    assert [task["reviewer_verdict"] for task in card["tasks"]] == ["pass"]
    # The planner's one criterion, unmet in a repository without tests, as `remedy do` answered.
    assert card["blocking_criteria"] == [
        {"id": "C001", "text": f"The mission goal is met in full: {ORDER}", "status": "unmet"}]
    assert [criterion["id"] for criterion in card["blocking_criteria"]
            if criterion["status"] != "met"] == done["unmet_blocking_criteria"]
    assert card["checks_ran"] is True
    # An unmet blocking criterion holds the result, and the one repair round makes it medium.
    assert (card["recommendation"], card["risk"]) == ("hold", "medium")


# ── 3: `--apply` lands the apply record, so the job no longer awaits it ─────


def test_do_apply_leaves_the_completed_job_not_awaiting_apply(repo, capsys):
    data = _do_json(capsys, ORDER, "--apply")
    [job_id] = data["job_ids"]

    client = _status_json(capsys)["client"]

    [job] = client["jobs"]
    assert job["job_id"] == job_id
    assert job["state"] == "completed"
    assert job["waits_for_apply"] is False
    assert client["awaiting_apply"] == []


# ── 4: an order file's path and digest land on the mission; text leaves them empty ──


def test_an_order_files_mission_carries_its_path_and_digest_a_text_order_does_not(
        repo, capsys):
    order_path = repo / "order.md"
    order_path.write_text("---\nmax-cost-usd: 1\n---\nWrite a CONTRIBUTING.md\n")
    raw = order_path.read_bytes()

    file_data = _do_json(capsys, str(order_path), "--plan-only")
    [file_job_id] = file_data["job_ids"]

    client = _status_json(capsys)["client"]
    [project] = client["projects"]
    file_mission = next(m for m in project["missions"] if m["job_ids"] == [file_job_id])
    assert file_mission["order_source_path"] == str(order_path.resolve())
    assert file_mission["order_source_sha256"] == hashlib.sha256(raw).hexdigest()

    text_data = _do_json(capsys, "fix the heading in README.md", "--plan-only")
    [text_job_id] = text_data["job_ids"]

    client = _status_json(capsys)["client"]
    [project] = client["projects"]
    text_mission = next(m for m in project["missions"] if m["job_ids"] == [text_job_id])
    assert text_mission["order_source_path"] == ""
    assert text_mission["order_source_sha256"] == ""


# ── 5: a second registered project appears too, both named and sorted ──────


def test_a_second_registered_project_names_both_slugs_sorted(
        repo, tmp_path_factory, capsys, monkeypatch):
    main(["init"])
    capsys.readouterr()

    other = _git_repo(tmp_path_factory.mktemp("other"))
    monkeypatch.chdir(other)
    main(["init"])
    monkeypatch.chdir(repo)
    capsys.readouterr()

    client = _status_json(capsys)["client"]

    slugs = [p["slug"] for p in client["projects"]]
    assert len(slugs) == 2
    assert slugs == sorted(slugs)


# ── 6: the supervisor's socket flips `supervisor.answers` ───────────────────


def test_a_listening_socket_makes_supervisor_answers_true_closing_it_makes_it_false(
        repo, capsys):
    from packages.orchestration.serve_paths import serve_paths

    client = _status_json(capsys)["client"]
    assert client["supervisor"]["answers"] is False

    paths = serve_paths()
    paths.root.mkdir(parents=True, exist_ok=True)
    sock = socket_module.socket(socket_module.AF_UNIX, socket_module.SOCK_STREAM)
    try:
        sock.bind(str(paths.socket))
        sock.listen(1)
        client = _status_json(capsys)["client"]
        assert client["supervisor"]["answers"] is True
    finally:
        sock.close()


# ── 7: the text output never leaks the JSON-only keys ───────────────────────


def test_status_without_json_prints_neither_client_nor_awaiting_apply(repo, capsys):
    main(["status"])
    out = capsys.readouterr().out

    assert "client" not in out
    assert "awaiting_apply" not in out


# ── 8: a task decision lands in client.decisions and agrees with decisions_open ──


def test_a_task_decision_appears_in_client_decisions_and_matches_decisions_open(
        repo, capsys):
    from datetime import datetime, timezone

    from packages.orchestration.escalation import enqueue_task_decision
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    data = _do_json(capsys, ORDER, "--plan-only")
    [job_id] = data["job_ids"]

    job = load_job_plan(job_id)
    enqueue_task_decision(
        job, task_id="t1", question="Which port?",
        options=["8080", "9090"], safe_default="8080",
        now=datetime.now(timezone.utc),
    )
    save_job_plan(job)

    result = _status_json(capsys)
    client = result["client"]

    job_decisions = [d for d in client["decisions"] if d["job_id"] == job_id]
    assert len(job_decisions) == 1
    assert job_decisions[0]["type"] == "task_decision"
    assert result["decisions_open"] == len(job_decisions)


# ── 9: a completed job references its evidence; the project names its cost of the day ──


def test_a_completed_jobs_entry_references_its_evidence_and_the_project_its_cost_today(
        repo, capsys):
    data = _do_json(capsys, ORDER)
    [job_id] = data["job_ids"]

    client = _status_json(capsys)["client"]

    [job] = client["jobs"]
    assert job["job_id"] == job_id
    assert job["cost"] == {"value_usd": None, "basis": "absent"}
    evidence = job["evidence"]
    assert Path(evidence["evidence_dir"]).is_dir()
    assert evidence["run_ids"]
    diff = Path(evidence["result_diff_path"])
    assert hashlib.sha256(diff.read_bytes()).hexdigest() == evidence["result_diff_sha256"]
    # The fake providers' calls reach today's ledger and none of them reports a price.
    [project] = client["projects"]
    cost_today = project["cost_today"]
    assert cost_today["day"] == client["read_at"][:10]
    assert cost_today["calls"] >= 1
    assert cost_today["value_usd"] is None
    assert cost_today["basis"] == "absent"
