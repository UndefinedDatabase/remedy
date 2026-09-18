"""F268 T001 to T003 — `remedy do "<order>"` end to end, one test per step boundary,
then the shape decision and the force flags (DECISIONs F268 D5 and D6), then
`--step-by-step` and `--plan-only` (DECISION F268 D8).

In-process through `apps.cli.grouped.main`, against a temporary git repository
holding one committed file, with the data root under `tmp_path`, the fake
builder and reviewer, `--no-ui`, and `--no-llm`. A tripwire fails the test if
any model-call factory is reached: no step of this walk may call a model.
"""
from __future__ import annotations

import json
import re
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
    """An UNREGISTERED git repository with one committed file, as the working directory."""
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


def _do(capsys, *extra: str, order: str = ORDER) -> str:
    main(["do", order, "--no-llm", "--no-ui",
          "--builder-provider", "fake", "--reviewer-provider", "fake", *extra])
    return capsys.readouterr().out


def _do_json(capsys, order: str = ORDER) -> dict:
    return json.loads(_do(capsys, "--json", order=order))


def _step(data: dict, name: str) -> dict:
    return next(s for s in data["steps"] if s["name"] == name)


def test_init_to_study_registers_studies_once_and_records_it(repo, capsys):
    from packages.orchestration.project_registry import resolve_project

    assert resolve_project(repo) is None
    head = _git(repo, "rev-parse", "HEAD").strip()

    first = _do_json(capsys)

    project = resolve_project(repo)
    assert project is not None
    assert _step(first, "init")["detail"].startswith(f"registered {repo} as project ")
    assert _step(first, "study")["status"] == "done"
    studied_at = project.metadata["studied_at"]
    assert studied_at
    assert project.metadata["studied_head"] == head

    second = _do_json(capsys, order="Write a CHANGELOG.md")

    assert _step(second, "study")["status"] == "skipped"
    assert "already studied" in _step(second, "study")["detail"]
    assert resolve_project(repo).metadata["studied_at"] == studied_at


def test_init_writes_every_ignore_entry_into_the_repos_exclude_file(repo, capsys, monkeypatch):
    """R-0963 / DECISION F268 D2: the init step keeps Remedy's own paths out of `git status`.

    The data root sits INSIDE the repository here, so `ignore_entries` returns its
    entry as well as `.remedy-wt/`. Only the init step writes the data-root entry;
    the run step's worktree code writes `.remedy-wt/` by itself, which alone would
    let this test pass with the init step's loop emptied.
    """
    from packages.orchestration.repo_ignore import ignore_entries

    monkeypatch.setenv("REMEDY_DATA_DIR", str(repo / ".remedy-data"))
    exclude = repo / ".git" / "info" / "exclude"
    entries = ignore_entries(repo)
    assert ".remedy-data/" in entries
    before = exclude.read_text(encoding="utf-8").split() if exclude.is_file() else []
    assert not set(entries) & set(before)

    _do_json(capsys)

    written = exclude.read_text(encoding="utf-8").split()
    assert [entry for entry in entries if entry not in written] == []


def test_study_to_plan_creates_the_mission_carrying_the_order(repo, capsys):
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.project_registry import resolve_project

    data = _do_json(capsys)

    mission = load_mission(str(resolve_project(repo).id), data["mission_id"])
    assert mission.id == data["mission_id"]
    assert mission.goal == ORDER
    assert mission.order.text == ORDER
    assert mission.mission_plan is not None
    assert data["mission_id"] in _step(data, "plan")["detail"]


def test_plan_to_shape_yields_one_job_linked_to_the_mission_targeting_the_repo(repo, capsys):
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.pingpong_job import list_job_plans, load_job_plan
    from packages.orchestration.project_registry import resolve_project

    data = _do_json(capsys)

    [job_id] = data["job_ids"]
    assert [str(j.job_id) for j in list_job_plans()] == [job_id]
    mission = load_mission(str(resolve_project(repo).id), data["mission_id"])
    assert [(link.job_id, link.role) for link in mission.job_links] == [(job_id, "initial")]
    assert load_job_plan(job_id).repo_path == str(repo)


def test_shape_to_run_completes_on_the_named_fake_providers(repo, capsys):
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan

    data = _do_json(capsys)

    job = load_job_plan(data["job_ids"][0])
    assert job.state == JOB_COMPLETED
    assert job.tasks and {str(t.status) for t in job.tasks} == {"applied_to_job_workspace"}
    assert _step(data, "run")["status"] == "done"
    # R-0933: the flag reached the run — recorded as the CLI's choice, not a default.
    config = job.execution_config
    assert (config.builder, config.builder_source) == ("fake", "cli")
    assert (config.reviewer, config.reviewer_source) == ("fake", "cli")


def _recorded_contract(repo, data, origins=frozenset({"planner"})):
    """The contract on the walk's mission record: planned, so never null."""
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.project_registry import resolve_project

    body = load_mission(str(resolve_project(repo).id), data["mission_id"]).contract
    assert body is not None and body["schema"] == "contract_v1"
    assert {c["origin"] for c in body["criteria"]} == set(origins)
    return body


def test_run_to_stop_leaves_the_target_untouched_and_stops_before_apply(repo, capsys):
    before = _git(repo, "status", "--porcelain", "--untracked-files=all")
    head = _git(repo, "rev-parse", "HEAD")

    data = _do_json(capsys)

    assert _git(repo, "status", "--porcelain", "--untracked-files=all") == before
    assert _git(repo, "rev-parse", "HEAD") == head
    assert data["stopped_before_apply"] is True
    # DECISION F269 D4 (6): the mission's contract body, as its record holds it.
    assert data["contract"] == _recorded_contract(repo, data)
    assert [s["name"] for s in data["steps"]] == [
        "init", "study", "plan", "shape", "run", "ui", "apply"]
    assert _step(data, "apply")["status"] == "stopped"


def test_job_apply_accepts_the_job_do_ran(repo, capsys):
    """R-0897: every run `remedy do` starts belongs to a job `job apply` accepts."""
    from packages.orchestration.job_apply import apply_job

    data = _do_json(capsys)

    result = apply_job(data["job_ids"][0], str(repo), approve=True)
    assert result.status == "applied", result.blocked_reason
    assert result.files_applied


def test_next_lines_carry_real_ids_and_paths_never_placeholders(repo, capsys):
    """R-0811: `do` attaches the working directory's repo without a flag, and every
    `Next:` line names the real job and path."""
    out = _do(capsys)

    for placeholder in ("<job_id>", "<path>", "<mission>"):
        assert placeholder not in out
    assert not re.search(r"<[a-z_]+>", out)
    [job_id] = re.findall(r"one job ([0-9a-f]{16}) linked", out)
    next_lines = [line for line in out.splitlines() if line.startswith("Next: ")]
    assert next_lines
    assert all(job_id in line for line in next_lines)
    assert f"Next: remedy job apply {job_id} --repo {repo} --approve" in next_lines


# ── T002: the shape and the force flags (DECISION F268 D5) ─────────────────

TEN_FILES = [f"docs/part_{n:02d}.md" for n in range(10)]


def test_the_order_plans_one_job_of_at_most_three_tasks_by_the_planners_shape(repo, capsys):
    data = _do_json(capsys)

    [job_id] = data["job_ids"]
    assert (data["shape"], data["shape_source"]) == ("one job", "planner")
    from packages.orchestration.pingpong_job import load_job_plan
    assert 1 <= len(load_job_plan(job_id).tasks) <= 3


def test_force_mission_yields_linked_jobs_runs_the_first_and_leaves_the_repo_untouched(
        repo, capsys):
    """DECISION F268 D12: only the first job runs; the rest wait, named in `waiting_job_ids`."""
    from packages.core.models import RunState
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan
    from packages.orchestration.project_registry import resolve_project

    before = _git(repo, "status", "--porcelain", "--untracked-files=all")

    data = json.loads(_do(capsys, "--json", "--force-mission"))

    assert (data["shape"], data["shape_source"]) == ("milestones", "--force-mission")
    job_ids = data["job_ids"]
    assert len(job_ids) >= 2
    mission = load_mission(str(resolve_project(repo).id), data["mission_id"])
    assert [(link.job_id, link.role) for link in mission.job_links] == [
        (job_ids[0], "initial"), *((j, "follow_up") for j in job_ids[1:])]
    jobs = [load_job_plan(j) for j in job_ids]
    assert [job.state for job in jobs] == (
        [JOB_COMPLETED] + [RunState.PLANNED] * (len(jobs) - 1))
    assert data["waiting_job_ids"] == job_ids[1:]
    assert [job.repo_path for job in jobs] == [str(repo)] * len(jobs)
    assert _git(repo, "status", "--porcelain", "--untracked-files=all") == before
    applies = [line for line in data["next"] if line.startswith("remedy job apply ")]
    assert applies == [f"remedy job apply {job_ids[0]} --repo {repo} --approve"]


def test_force_job_on_an_order_naming_ten_files_yields_one_job_of_ten_tasks(repo, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    order = "Write " + ", ".join(TEN_FILES)

    data = json.loads(_do(capsys, "--json", "--force-job", order=order))

    assert (data["shape"], data["shape_source"]) == ("one job", "--force-job")
    [job_id] = data["job_ids"]
    tasks = load_job_plan(job_id).tasks
    assert [t.inputs["deliverable"] for t in tasks] == TEN_FILES


def test_force_job_and_force_mission_together_exit_2(repo, capsys):
    with pytest.raises(SystemExit) as exc:
        _do(capsys, "--force-job", "--force-mission")

    assert exc.value.code == 2
    assert "cannot be given together" in capsys.readouterr().err


def test_the_shape_function_reads_milestones_from_two_outlines_and_one_job_from_one():
    from packages.orchestration.do_sequence import do_shape_of_plan
    from packages.orchestration.mission_compiler import deterministic_mission_plan
    from packages.orchestration.mission_plan_schema import MissionPlan

    one = deterministic_mission_plan(ORDER)
    data = one.model_dump()
    data["milestones"][0]["jobs_draft"].append(
        dict(title="Changelog", goal="Write a CHANGELOG.md", est_band="M"))
    two = MissionPlan(**data)

    assert do_shape_of_plan(one) == "one job"
    assert do_shape_of_plan(two) == "milestones"


# ── T003: --step-by-step and --plan-only (DECISION F268 D8) ─────────────────

PLAIN_RUN_STEPS = [("init", "done"), ("study", "done"), ("plan", "done"), ("shape", "done"),
                   ("run", "done"), ("ui", "skipped"), ("apply", "stopped")]


def _answer_every_halt(monkeypatch, answer):
    """Stand in for the terminal: every `--step-by-step` halt reads through `input`.

    ``answer`` is called with the halt's index and returns the line typed there.
    Returns the list of halt indexes read, in order.
    """
    halts: list[int] = []

    def reader(*_prompt):
        halts.append(len(halts))
        return answer(halts[-1])

    monkeypatch.setattr("builtins.input", reader)
    return halts


def _count_fake_provider_calls(monkeypatch) -> dict[str, int]:
    """Count every fake builder and reviewer call, across every provider instance."""
    from packages.orchestration.pingpong_provider import FakeProvider

    calls = {"n": 0}
    for method in ("build", "review"):
        original = getattr(FakeProvider, method)

        def counted(self, *args, _original=original, **kwargs):
            calls["n"] += 1
            return _original(self, *args, **kwargs)

        monkeypatch.setattr(FakeProvider, method, counted)
    return calls


def test_step_by_step_halts_at_least_three_times_and_completes_like_a_plain_run(
        repo, capsys, monkeypatch):
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan

    halts = _answer_every_halt(monkeypatch, lambda index: "")

    data = json.loads(_do(capsys, "--json", "--step-by-step"))

    assert len(halts) >= 3
    assert [(s["name"], s["status"]) for s in data["steps"]] == PLAIN_RUN_STEPS
    assert [load_job_plan(j).state for j in data["job_ids"]] == [JOB_COMPLETED]


def test_no_provider_call_happens_while_a_halt_waits(repo, capsys, monkeypatch):
    calls = _count_fake_provider_calls(monkeypatch)
    waits: list[tuple[int, int]] = []

    def reader(*_prompt):
        entry = calls["n"]
        exit_ = calls["n"]
        waits.append((entry, exit_))
        return ""

    monkeypatch.setattr("builtins.input", reader)

    _do(capsys, "--json", "--step-by-step")

    assert len(waits) >= 3
    assert all(entry == exit_ for entry, exit_ in waits)
    # The counter is live: the run made calls, and a later halt saw them.
    assert calls["n"] > 0
    assert waits[-1][0] == calls["n"] > waits[0][0]


def test_q_at_the_first_halt_after_shape_runs_no_job_and_asks_every_job_to_stop(
        repo, capsys, monkeypatch):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import list_job_plans, load_job_plan
    from packages.orchestration.safe_points import stop_requested

    # Jobs exist from the shape step on, so the first halt that sees one is after shape.
    halts = _answer_every_halt(
        monkeypatch, lambda index: "q" if list_job_plans() else "")

    data = json.loads(_do(capsys, "--json", "--step-by-step", "--force-mission"))

    job_ids = data["job_ids"]
    assert len(job_ids) >= 2
    assert [(s["name"], s["status"]) for s in data["steps"]] == [
        ("init", "done"), ("study", "done"), ("plan", "done"), ("shape", "done"),
        ("run", "stopped")]
    assert _step(data, "run")["detail"].startswith("not run: stopped by 'q'")
    assert [load_job_plan(j).state for j in job_ids] == [RunState.PLANNED] * len(job_ids)
    requests = [stop_requested(j) for j in job_ids]
    assert all(r is not None and r.source == "do" for r in requests), requests
    assert len(halts) == 4


@pytest.mark.parametrize("after_shape", [False, True],
                         ids=["the-first-halt", "the-first-halt-after-shape"])
def test_end_of_input_at_a_halt_stops_the_walk_runs_no_job_and_asks_every_job_to_stop(
        repo, capsys, monkeypatch, after_shape):
    """R-0967 / DECISION F268 D8: end of input at a halt stops the walk exactly as `q` does.

    At the very first halt no job exists yet; the second case reads end of input
    at the first halt that sees the jobs, so the stop requests are measured too.
    """
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import list_job_plans, load_job_plan
    from packages.orchestration.safe_points import stop_requested

    calls = _count_fake_provider_calls(monkeypatch)
    halts: list[int] = []

    def reader(*_prompt):
        halts.append(len(halts))
        if after_shape and not list_job_plans():
            return ""
        raise EOFError

    monkeypatch.setattr("builtins.input", reader)
    extra = ("--force-mission",) if after_shape else ()

    data = json.loads(_do(capsys, "--json", "--step-by-step", *extra))

    steps = [(s["name"], s["status"]) for s in data["steps"]]
    job_ids = data["job_ids"]
    if after_shape:
        assert steps == [("init", "done"), ("study", "done"), ("plan", "done"),
                         ("shape", "done"), ("run", "stopped")]
        assert len(halts) == 4
        assert len(job_ids) >= 2
    else:
        assert steps == [("init", "done"), ("study", "stopped")]
        assert len(halts) == 1
        assert job_ids == [] and list_job_plans() == []
    assert data["steps"][-1]["detail"].startswith("not run: stopped by end of input")
    assert calls["n"] == 0
    assert [load_job_plan(j).state for j in job_ids] == [RunState.PLANNED] * len(job_ids)
    requests = [stop_requested(j) for j in job_ids]
    assert all(r is not None and r.source == "do" for r in requests), requests


def test_plan_only_writes_the_mission_plan_plans_the_jobs_and_runs_none(
        repo, capsys, monkeypatch):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.task_deliverables import task_deliverable

    data = json.loads(_do(capsys, "--json", "--plan-only"))

    assert Path(data["mission_plan_path"]).is_file()
    # DECISION F269 D4 (6): planning wrote the contract; --plan-only reports it.
    assert data["contract"] == _recorded_contract(repo, data)
    job_ids = data["job_ids"]
    assert job_ids
    assert [load_job_plan(j).state for j in job_ids] == [RunState.PLANNED] * len(job_ids)
    run = _step(data, "run")
    assert (run["status"], run["detail"].split(":", 1)[0]) == ("stopped", "--plan-only")
    assert [job["job_id"] for job in data["jobs"]] == job_ids
    for job in data["jobs"]:
        planned = load_job_plan(job["job_id"]).tasks
        assert job["tasks"] == [
            {"title": t.title, "deliverable": task_deliverable(t)} for t in planned]
        assert all(task["deliverable"] for task in job["tasks"])
    assert data["jobs"][0]["tasks"][0]["deliverable"] == "CONTRIBUTING.md"


def test_text_output_lists_each_tasks_deliverable(repo, capsys):
    from packages.orchestration.pingpong_job import list_job_plans

    out = _do(capsys, "--force-mission")

    jobs = list_job_plans()
    assert len(jobs) >= 2
    for job in jobs:
        for number, task in enumerate(job.tasks, start=1):
            deliverable = task.inputs["deliverable"]
            assert (f"  job {job.job_id} task {number}: {task.title}"
                    f" — deliverable: {deliverable}") in out.splitlines()


# ── T004: the cockpit, --apply and the flags not yet available (DECISION F268 D9) ──


def _do_with_ui(capsys, *extra: str, order: str = ORDER) -> str:
    """`_do` without `--no-ui`: the ui step reaches the launcher the test stands in."""
    main(["do", order, "--no-llm",
          "--builder-provider", "fake", "--reviewer-provider", "fake", *extra])
    return capsys.readouterr().out


def _stand_in_for_the_cockpit(monkeypatch, launcher) -> None:
    """Replace the CLI's default launcher: no test starts a UI server or a browser."""
    monkeypatch.setattr("packages.orchestration.do_sequence.launch_do_cockpit", launcher)


def test_without_no_ui_the_cockpit_opens_for_the_job_that_ran_and_reports_its_url(
        repo, capsys, monkeypatch):
    """DECISION F268 D12: in a walk of two jobs the cockpit opens for job 1, the one that ran."""
    launched: list[str] = []

    def launcher(job_id: str) -> str:
        launched.append(job_id)
        return f"http://127.0.0.1:43210/?job={job_id}&token=t"

    _stand_in_for_the_cockpit(monkeypatch, launcher)

    data = json.loads(_do_with_ui(capsys, "--json", "--force-mission"))

    job_ids = data["job_ids"]
    assert len(job_ids) >= 2
    assert launched == [job_ids[0]]
    ui = _step(data, "ui")
    assert ui["status"] == "done"
    assert f"http://127.0.0.1:43210/?job={job_ids[0]}&token=t" in ui["detail"]
    assert "remedy ui stop" in ui["detail"]
    assert "remedy ui stop" in data["next"]
    assert [(s["name"], s["status"]) for s in data["steps"]][-2:] == [
        ("ui", "done"), ("apply", "stopped")]


def test_a_cockpit_that_does_not_come_up_is_skipped_and_the_walk_ends_at_apply(
        repo, capsys, monkeypatch):
    from packages.orchestration.do_sequence import DoCockpitLaunchError

    def launcher(job_id: str) -> str:
        raise DoCockpitLaunchError("the cockpit did not come up within 15s; its log: x.log")

    _stand_in_for_the_cockpit(monkeypatch, launcher)

    data = json.loads(_do_with_ui(capsys, "--json"))

    [job_id] = data["job_ids"]
    ui = _step(data, "ui")
    assert ui["status"] == "skipped"
    assert "did not come up within 15s" in ui["detail"]
    assert f"remedy ui start {job_id}" in ui["detail"]
    assert f"remedy ui start {job_id}" in data["next"]
    assert (data["steps"][-1]["name"], data["steps"][-1]["status"]) == ("apply", "stopped")
    assert data["stopped_before_apply"] is True


def _track(repo: Path, *paths: str) -> None:
    """Commit each path into the target, so the fake builder's writes change tracked content."""
    for rel in paths:
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(f"# {rel}\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "tracked files the fake builder writes")


def test_apply_applies_the_one_job_and_changes_the_targets_tracked_content(repo, capsys):
    _track(repo, "docs/README.md")
    assert _git(repo, "status", "--porcelain", "--untracked-files=all") == ""

    data = json.loads(_do(capsys, "--json", "--apply"))

    [job_id] = data["job_ids"]
    assert data["stopped_before_apply"] is False
    apply = _step(data, "apply")
    assert apply["status"] == "done"
    assert f"job {job_id} applied 1 file(s)" in apply["detail"]
    assert _git(repo, "diff", "--name-only") == "docs/README.md\n"
    assert _git(repo, "status", "--porcelain", "--untracked-files=all") == " M docs/README.md\n"


def test_apply_with_force_mission_applies_the_job_that_ran_and_leaves_the_rest_waiting(
        repo, capsys, monkeypatch):
    """DECISION F268 D12: every job's fake build would write its own tracked file, but
    only job 1 runs, so only job 1's file is applied; the rest wait unrun."""
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.pingpong_provider import FakeProvider

    tracked = [f"docs/job_{n:02d}.md" for n in range(20)]
    _track(repo, *tracked)
    built = iter(tracked)
    original_init = FakeProvider.__init__

    def one_file_per_provider(self, *args, builder_files=None, **kwargs):
        original_init(self, *args, builder_files=builder_files or [next(built)], **kwargs)

    monkeypatch.setattr(FakeProvider, "__init__", one_file_per_provider)

    data = json.loads(_do(capsys, "--json", "--apply", "--force-mission"))

    job_ids = data["job_ids"]
    assert len(job_ids) >= 2
    assert data["stopped_before_apply"] is False
    apply = _step(data, "apply")
    assert apply["status"] == "done"
    assert re.search(rf"job {job_ids[0]} applied \d+ file\(s\)", apply["detail"])
    assert [j for j in job_ids[1:] if j in apply["detail"]] == []
    assert data["waiting_job_ids"] == job_ids[1:]
    assert [load_job_plan(j).state for j in job_ids[1:]] == (
        [RunState.PLANNED] * (len(job_ids) - 1))
    changed = _git(repo, "diff", "--name-only").split()
    assert len(changed) >= 1
    assert set(changed) <= set(tracked)


def _waiting_job_has_no_run(job_id: str) -> bool:
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import load_job_plan

    job = load_job_plan(job_id)
    return job.state == RunState.PLANNED and all(not t.run_id for t in job.tasks)


def test_apply_with_force_mission_on_the_stock_fake_applies_job_1_and_job_2_waits(
        repo, capsys):
    """R-0968 / DECISION F268 D12 (2a): the case R-0968 measured — every build writes
    the same file — now applies job 1, runs no other job and exits 0."""
    assert not (repo / "docs" / "README.md").exists()

    data = json.loads(_do(capsys, "--json", "--apply", "--force-mission"))

    job_ids = data["job_ids"]
    assert len(job_ids) >= 2
    assert [(s["name"], s["status"]) for s in data["steps"]][-3:] == [
        ("run", "done"), ("ui", "skipped"), ("apply", "done")]
    assert f"job {job_ids[0]} applied 1 file(s)" in _step(data, "apply")["detail"]
    assert "<!-- Remedy: " in (repo / "docs" / "README.md").read_text()
    assert data["stopped_before_apply"] is False
    assert data["waiting_job_ids"] == job_ids[1:]
    assert [_waiting_job_has_no_run(j) for j in job_ids[1:]] == [True] * (len(job_ids) - 1)
    assert (f"commit job {job_ids[0]}'s applied output in {repo}, then: "
            f"remedy job run {job_ids[1]} --builder-provider fake "
            f"--reviewer-provider fake") in data["next"]


def test_without_apply_a_force_mission_walk_runs_job_1_and_prints_how_job_2_runs(
        repo, capsys):
    """R-0968 / DECISION F268 D12 (2b): job 1 runs, job 2 does not, and the Next lines
    carry job 1's apply command and job 2's run command with real ids."""
    from packages.orchestration.pingpong_job import JOB_COMPLETED, list_job_plans, load_job_plan

    out = _do(capsys, "--force-mission")

    # The shape step's line names the jobs in walk order.
    job_ids = re.findall(r"([0-9a-f]{16}) \(\d+ task\(s\)\)", out)
    assert len(job_ids) >= 2
    assert sorted(job_ids) == sorted(str(j.job_id) for j in list_job_plans())
    assert load_job_plan(job_ids[0]).state == JOB_COMPLETED
    assert _waiting_job_has_no_run(job_ids[1])
    assert f"[done] run: job {job_ids[0]} ran " in out
    next_lines = [line for line in out.splitlines() if line.startswith("Next: ")]
    assert f"Next: remedy job apply {job_ids[0]} --repo {repo} --approve" in next_lines
    assert (f"Next: commit job {job_ids[0]}'s applied output in {repo}, then: "
            f"remedy job run {job_ids[1]} --builder-provider fake "
            f"--reviewer-provider fake") in next_lines
    assert not re.search(r"<[a-z_]+>", out)


def test_an_apply_the_baseline_check_refuses_fails_the_walk_naming_the_job(
        repo, capsys, monkeypatch):
    """The target changes between the run and the apply: `job_apply` refuses it."""
    from packages.orchestration import job_apply

    _track(repo, "docs/README.md")
    real_apply_job = job_apply.apply_job

    def apply_after_someone_edited_the_target(job_id, target_repo, **kwargs):
        (Path(target_repo) / "docs" / "README.md").write_text("edited by hand\n")
        return real_apply_job(job_id, target_repo, **kwargs)

    monkeypatch.setattr(job_apply, "apply_job", apply_after_someone_edited_the_target)

    with pytest.raises(SystemExit) as exc:
        _do(capsys, "--json", "--apply")

    assert exc.value.code == 1
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    [job_id] = data["job_ids"]
    apply = _step(data, "apply")
    assert apply["status"] == "failed"
    assert apply["detail"].startswith(f"job {job_id} was not applied to {repo} (status blocked)")
    assert "target_changed_since_job: docs/README.md" in apply["detail"]
    assert data["stopped_before_apply"] is True
    assert (repo / "docs" / "README.md").read_text() == "edited by hand\n"
    assert f"Error: apply failed: job {job_id} was not applied" in captured.err


# ── R-0807's F268 half: measured tokens per role and cost (DECISION F268 D11) ──


def test_the_json_cost_has_a_row_per_role_with_the_ledgers_own_numbers(repo, capsys):
    from packages.orchestration.project_registry import resolve_project
    from packages.orchestration.token_ledger import query_cost

    data = _do_json(capsys)

    [job_id] = data["job_ids"]
    report = query_cost(project_id=str(resolve_project(repo).id), job_id=job_id, by="role")
    assert report.ledger_exists and report.rows, "the run step mirrored nothing into the ledger"
    assert data["cost"]["roles"] == [
        {"role": row.bucket, "calls": row.calls, "tokens_in": row.tokens_in,
         "tokens_out": row.tokens_out, "cache_read": row.cache_read, "cost_usd": row.cost_usd}
        for row in sorted(report.rows, key=lambda r: str(r.bucket))]
    assert data["cost"]["cost_usd"] == report.total.cost_usd
    assert (data["cost"]["job_ids"], data["cost"]["mirror_failed_job_ids"]) == ([job_id], [])

    out = _do(capsys, order="Write a CHANGELOG.md")
    assert re.search(r"^Tokens builder: input .+, output .+, cache read .+ \(\d+ call\(s\)\)$",
                     out, re.MULTILINE)
    assert re.search(r"^Cost: ", out, re.MULTILINE)


def test_a_job_whose_cost_mirror_failed_is_named_not_counted_as_zero(
        repo, capsys, monkeypatch):
    def mirror_fails(job_id):
        return {"ledger_mirrored": False, "out_dir": "", "error": "OSError: disk full"}

    monkeypatch.setattr("packages.orchestration.job_evidence.mirror_job_run_into_ledger",
                        mirror_fails)

    data = _do_json(capsys)

    [job_id] = data["job_ids"]
    assert data["cost"]["mirror_failed_job_ids"] == [job_id]
    assert data["cost"]["mirror_errors"] == {job_id: "OSError: disk full"}
    assert (data["cost"]["roles"], data["cost"]["cost_usd"], data["cost"]["job_ids"]) == (
        [], None, [])

    out = _do(capsys, order="Write a CHANGELOG.md")
    [second] = re.findall(r"one job ([0-9a-f]{16}) linked", out)
    assert f"Cost NOT recorded to the ledger for job {second}: OSError: disk full" in out
    assert "Cost: not reported by the provider" in out


NOT_YET_AVAILABLE = [
    (("--commit","Add the contributing guide"), "F270"),
    (("--commit-auto",), "F270"),
    (("--commit-with-history",), "F270"),
    (("--push",), "F270"),
]


@pytest.mark.parametrize(("flag", "feature"), NOT_YET_AVAILABLE,
                         ids=[flag[0] for flag, _ in NOT_YET_AVAILABLE])
def test_a_flag_whose_feature_is_not_built_refuses_before_any_step(
        repo, capsys, flag, feature):
    from packages.orchestration.pingpong_job import list_job_plans
    from packages.orchestration.project_registry import resolve_project

    data_root = repo.parent / "data"

    with pytest.raises(SystemExit) as exc:
        _do(capsys, "--json", *flag)

    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert f"{flag[0]} is not yet available; {feature} brings it" in captured.err
    assert [p for p in data_root.rglob("*") if p.is_file()] == []
    assert resolve_project(repo) is None
    assert list_job_plans() == []


# ── F269 T003: `--contract` and the proposed template (DECISION F269 D1 (4)) ──


def _template_criteria(name: str) -> list[dict]:
    from packages.orchestration.contract_templates import (
        compile_contract_template,
        load_contract_template,
    )

    return _as_compiled(
        [c.to_json() for c in compile_contract_template(load_contract_template(name))])


#: The fields the job's gate writes after the run (DECISION F269 D6 (2), (3)).
_GATE_WRITTEN_FIELDS = ("status", "evidence_ref")


def _as_compiled(criteria: list[dict]) -> list[dict]:
    """Criteria without the fields the walk's gated job decides: what the template compiled."""
    return [{k: v for k, v in c.items() if k not in _GATE_WRITTEN_FIELDS} for c in criteria]


def _contract_by_origin(data: dict, origin: str) -> list[dict]:
    return _as_compiled([c for c in data["contract"]["criteria"] if c["origin"] == origin])


def test_contract_website_on_a_bare_order_gives_the_website_templates_criteria(repo, capsys):
    data = json.loads(_do(capsys, "--json", "--contract", "website"))

    assert data["contract"] == _recorded_contract(repo, data, {"template", "planner"})
    assert data["contract"]["template"] == "website"
    assert _contract_by_origin(data, "template") == _template_criteria("website")
    assert _step(data, "plan")["detail"].endswith(
        "; contract template website, forced by --contract")


def test_contract_website_with_an_extra_requirement_adds_planner_criteria_and_drops_none(
        repo, capsys):
    order = "Write a CONTRIBUTING.md that also lists the release checklist"

    data = json.loads(_do(capsys, "--json", "--contract", "website", order=order))

    assert data["contract"]["template"] == "website"
    template = _template_criteria("website")
    assert _contract_by_origin(data, "template") == template
    assert _as_compiled(data["contract"]["criteria"][:len(template)]) == template
    assert len(_contract_by_origin(data, "planner")) >= 1


def test_without_contract_the_website_fixture_order_gets_the_proposed_template(repo, capsys):
    from packages.orchestration.contract_templates import load_contract_template

    order = load_contract_template("website").fixture_order

    data = _do_json(capsys, order=order)

    assert data["contract"]["template"] == "website"
    assert _contract_by_origin(data, "template") == _template_criteria("website")
    detail = _step(data, "plan")["detail"]
    assert detail.endswith("; contract template website, proposed from the order")


def test_contract_naming_no_template_exits_2_naming_the_templates_and_writes_nothing(
        repo, capsys):
    from packages.orchestration.pingpong_job import list_job_plans
    from packages.orchestration.project_registry import resolve_project

    data_root = repo.parent / "data"

    with pytest.raises(SystemExit) as exc:
        _do(capsys, "--json", "--contract", "nosuch")

    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert ("--contract 'nosuch' is not a contract template; the templates are "
            "api-service, cli-tool, python-library, website. Nothing was run.") in captured.err
    assert [p for p in data_root.rglob("*") if p.is_file()] == []
    assert resolve_project(repo) is None
    assert list_job_plans() == []


# ── F269 round 5: `do`'s job is gated on its contract slice (DECISION F269 D6) ──

SUITE_PASSES = "The test suite passes."


def test_contract_cli_tool_gates_the_job_on_its_whole_mission_checks_and_names_the_unmet(
        repo, capsys):
    """D6 (1), (3), (4): the repository has no tests, so the suite criterion reads
    `unmet`; the hygiene criteria read `met`; the job still completes."""
    from packages.orchestration.dod_gate import load_dod, load_gate_result
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan

    data = json.loads(_do(capsys, "--json", "--contract", "cli-tool"))

    [job_id] = data["job_ids"]
    criteria = data["contract"]["criteria"]
    whole = [c for c in criteria if not c["milestones"]]
    assert [c["origin"] for c in whole] == ["template"] * 7
    # Every whole-mission check is in the job's DoD (the four suite-judged
    # criteria share one check), and not one of them is blocking.
    dod = load_dod(job_id)
    assert {(c.kind, json.dumps(c.spec, sort_keys=True)) for c in dod.checks} == {
        (c["check"]["kind"], json.dumps(c["check"]["spec"], sort_keys=True)) for c in whole}
    assert [c.blocking for c in dod.checks] == [False] * len(dod.checks)
    assert load_gate_result(job_id)["released"] is True
    assert load_job_plan(job_id).state == JOB_COMPLETED

    by_text = {c["text"]: c for c in criteria}
    suite = by_text[SUITE_PASSES]
    assert suite["status"] == "unmet"
    assert suite["evidence_ref"].startswith(f"{job_id}:")
    hygiene = [c for c in whole if c["check"]["kind"] == "custom_cmd"]
    assert len(hygiene) == 3
    assert [c["status"] for c in hygiene] == ["met"] * 3

    # Not met, in contract order: the four suite-judged template criteria
    # (unmet: no tests) and the planner's milestone criterion (open: `do`'s job
    # serves no milestone, so nothing evaluated it).
    suite_judged = [c for c in whole if c["check"]["kind"] != "custom_cmd"]
    planner = [c for c in criteria if c["origin"] == "planner"]
    assert [c["status"] for c in suite_judged] == ["unmet"] * 4
    assert [c["status"] for c in planner] == ["open"] * len(planner)
    expected = [c["id"] for c in suite_judged + planner]
    assert expected == [c["id"] for c in criteria if c not in hygiene]
    assert data["unmet_blocking_criteria"] == expected

    out = _do(capsys, "--contract", "cli-tool", order="Write a CHANGELOG.md")
    [line] = [line for line in out.splitlines() if line.startswith("Contract: ")]
    named = ", ".join([f"{c['id']} (unmet)" for c in suite_judged]
                      + [f"{c['id']} (open)" for c in planner])
    assert line == (f"Contract: 3 of {len(criteria)} criteria met; "
                    f"blocking criteria not met: {named}")


def test_a_do_whose_order_proposes_no_template_names_only_criteria_not_met(repo, capsys):
    from packages.orchestration.dod_gate import load_dod

    data = _do_json(capsys)

    [job_id] = data["job_ids"]
    assert data["contract"]["template"] is None
    # No whole-mission criterion: the job's slice is empty and it stores no DoD.
    assert load_dod(job_id) is None
    criteria = data["contract"]["criteria"]
    assert criteria
    assert {(c["origin"], c["blocking"], c["status"]) for c in criteria} == {
        ("planner", True, "open")}
    assert data["unmet_blocking_criteria"] == [c["id"] for c in criteria]


def test_the_old_name_with_history_is_never_created(repo, capsys):
    with pytest.raises(SystemExit) as exc:
        _do(capsys, "--with-history")

    assert exc.value.code == 2
    assert "--with-history" in capsys.readouterr().err


def test_the_default_launcher_starts_ui_start_detached_and_reads_its_url(tmp_path, monkeypatch):
    """The argv and the spawn's keywords, measured through a stand-in: nothing is spawned."""
    import sys

    from packages.orchestration.do_sequence import (
        DoCockpitLaunchError,
        do_cockpit_argv,
        do_cockpit_paths,
        launch_do_cockpit,
    )

    data_root = tmp_path / "cockpit-data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
    info_file, log_file = do_cockpit_paths("abc123")

    assert do_cockpit_argv("abc123", info_file) == [
        sys.executable, "-m", "apps.cli.grouped", "ui", "start", "abc123",
        "--port", "0", "--info-file", str(info_file)]
    assert info_file.parent == data_root / "ui" / "sessions"
    assert log_file.is_relative_to(data_root)

    class Child:
        terminated = False

        def poll(self):
            return None

        def terminate(self):
            self.terminated = True

    spawned: list[tuple[list[str], dict]] = []
    url = "http://127.0.0.1:43210/?job=abc123&token=t"

    def comes_up(argv, **kwargs):
        spawned.append((argv, kwargs))
        info_file.write_text(json.dumps({"url": url}))
        return Child()

    assert launch_do_cockpit("abc123", spawn=comes_up, sleep=lambda _s: None) == url
    [(argv, kwargs)] = spawned
    assert argv == do_cockpit_argv("abc123", info_file)
    assert kwargs["start_new_session"] is True
    assert kwargs["stdout"].name == str(log_file)

    silent = Child()
    with pytest.raises(DoCockpitLaunchError, match="did not come up within 0s"):
        launch_do_cockpit("abc123", wait_seconds=0, spawn=lambda argv, **kw: silent,
                          sleep=lambda _s: None)
    assert silent.terminated is True
