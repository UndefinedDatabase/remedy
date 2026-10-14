"""Operator amendment amend1014-do-golden-path-now — the `remedy do` golden path, end to end.

The incident: a committed repository holding only `README.md` ("# Test\\n") and the order "Add one
concise project-description paragraph below the existing heading in README.md. Change no other
files." run as a bare `remedy do`, with no `--force-job`, no approval flag and no `--no-llm`.
It must plan with ZERO provider calls, open the cockpit before the builder runs, say what it is
doing as it goes, and leave the target untouched.

In-process through `apps.cli.grouped.main`, the data root under `tmp_path`, the fake builder and
reviewer. Every model-call factory is a counter that fails the test when reached, which is the
proof that planning made no provider call.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main

INCIDENT_ORDER = (
    "Add one concise project-description paragraph below the existing heading in README.md. "
    "Change no other files.")
FAKE_ROLES = ("--builder-provider", "fake", "--reviewer-provider", "fake")
COCKPIT_URL = "http://127.0.0.1:43210/?job={job_id}&token=t"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


def _commit_repo(target: Path, files: dict[str, str]) -> Path:
    target.mkdir()
    _git(target, "init", "-q")
    _git(target, "config", "user.email", "t@e.com")
    _git(target, "config", "user.name", "T")
    _git(target, "config", "commit.gpgsign", "false")
    for name, text in files.items():
        (target / name).parent.mkdir(parents=True, exist_ok=True)
        (target / name).write_text(text)
    _git(target, "add", "-A")
    _git(target, "commit", "-qm", "init")
    return target.resolve()


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    """The incident repository: one real commit containing README.md."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = _commit_repo(tmp_path / "test", {"README.md": "# Test\n"})
    monkeypatch.chdir(target)
    return target


@pytest.fixture
def planning_calls(monkeypatch) -> list[str]:
    """Every factory that could make a planning or study call fails the test when reached."""
    reached: list[str] = []

    def tripwire_for(name):
        def tripwire(*args, **kwargs):
            reached.append(name)
            raise AssertionError(f"a planning or study provider call was made through {name}")
        return tripwire

    import packages.orchestration.study  # noqa: F401 — bound by `from … import`, patched below
    for target in ("packages.orchestration.intake.make_provider_call_fn",
                   "packages.orchestration.intake.make_structured_call_fn",
                   "packages.orchestration.study.make_structured_call_fn",
                   "packages.orchestration.study.study_call_fn"):
        monkeypatch.setattr(target, tripwire_for(target.rsplit(".", 1)[1]))
    return reached


@pytest.fixture
def events(monkeypatch) -> list[str]:
    """The walk's ordered events: ``cockpit``, ``builder``, ``reviewer`` and ``progress: <line>``."""
    log: list[str] = []
    from packages.orchestration import do_cockpit, do_progress
    from packages.orchestration.pingpong_provider import FakeProvider

    for method, name in (("build", "builder"), ("review", "reviewer")):
        original = getattr(FakeProvider, method)

        def counted(self, *args, _original=original, _name=name, **kwargs):
            log.append(_name)
            return _original(self, *args, **kwargs)

        monkeypatch.setattr(FakeProvider, method, counted)

    def launcher(job_id: str) -> str:
        log.append("cockpit")
        return COCKPIT_URL.format(job_id=job_id)

    monkeypatch.setattr(do_cockpit, "launch_do_cockpit", launcher)
    real_progress = do_progress.DoProgress
    monkeypatch.setattr(
        do_progress, "DoProgress",
        lambda: real_progress(write=lambda line: log.append(f"progress: {line}")))
    return log


def _do(capsys, *extra: str, order: str = INCIDENT_ORDER, repo_args=("--repo", ".")) -> str:
    main(["do", order, *repo_args, *FAKE_ROLES, *extra])
    return capsys.readouterr().out


def _step(data: dict, name: str) -> dict:
    return next(s for s in data["steps"] if s["name"] == name)


def _snapshot(repo: Path) -> tuple[str, str, str]:
    return (_git(repo, "status", "--porcelain", "--untracked-files=all"),
            _git(repo, "rev-parse", "HEAD"), (repo / "README.md").read_text())


# ── tests 1, 2 and 10: the exact incident, its call count, the untouched target ──


def test_the_incident_order_is_one_job_one_task_with_no_flag_and_no_planning_call(
        repo, capsys, planning_calls, events):
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan

    before = _snapshot(repo)

    data = json.loads(_do(capsys, "--json"))

    assert planning_calls == []
    assert [s["name"] for s in data["steps"]] == [
        "init", "study", "plan", "shape", "ui", "run", "apply"]
    assert (data["shape"], data["shape_source"]) == ("one job", "bounded lane")
    assert "lane: bounded" in _step(data, "plan")["detail"]
    assert "deterministic" in _step(data, "plan")["detail"]
    [job_listing] = data["jobs"]
    assert [t["deliverable"] for t in job_listing["tasks"]] == ["README.md"]
    [job_id] = data["job_ids"]
    job = load_job_plan(job_id)
    assert len(job.tasks) == 1
    assert job.state == JOB_COMPLETED
    # Only the worker roles ran. The stock fake reviewer asks for one repair on its first round,
    # so its sequence is builder, reviewer, builder, reviewer; a real run with no repair is one
    # of each. Either way every builder call is answered by a reviewer call and nothing else ran.
    assert set(events) == {"cockpit", "builder", "reviewer"}, events
    assert events.count("builder") == events.count("reviewer") >= 1, events
    assert _snapshot(repo) == before
    assert data["stopped_before_apply"] is True
    assert _step(data, "apply")["status"] == "stopped"


def test_the_cockpit_is_launched_before_the_builder_runs(repo, capsys, planning_calls, events):
    data = json.loads(_do(capsys, "--json"))

    assert events.index("cockpit") < events.index("builder")
    assert COCKPIT_URL.format(job_id=data["job_ids"][0]) in _step(data, "ui")["detail"]


def test_the_study_of_a_tiny_repository_is_facts_without_narration(
        repo, capsys, planning_calls, events):
    data = json.loads(_do(capsys, "--json"))

    assert _step(data, "study")["status"] == "done"
    assert planning_calls == []


# ── test 4: visible progress ─────────────────────────────────────────────────


def test_the_human_walk_speaks_first_names_its_providers_and_prints_the_cockpit_url(
        repo, capsys, planning_calls, events):
    out = _do(capsys)

    progress = [e for e in events if e.startswith("progress: ")]
    assert events[0].startswith("progress: [remedy] init started")
    assert events.index(progress[0]) < events.index("builder")
    started = [line for line in progress if " started — " in line]
    assert [line.split()[2] for line in started] == [
        "init", "study", "plan", "shape", "ui", "run", "apply"]
    assert any("run started — builder fake, reviewer fake" in line for line in progress)
    assert any("study started — deterministic scan, no provider call" in line for line in progress)
    assert any("bounded one-deliverable lane" in line for line in progress)
    url_line = next(e for e in events if e.startswith("progress: [remedy] cockpit: http://"))
    assert events.index(url_line) < events.index("builder")
    assert re.search(r"\[remedy\] run done — [\d.]+s", "\n".join(progress))
    assert "[done] plan:" in out


# ── test 5: machine output preservation ──────────────────────────────────────


def test_json_output_is_one_clean_document_and_stderr_stays_silent(
        repo, capsys, planning_calls, events):
    main(["do", INCIDENT_ORDER, "--repo", ".", *FAKE_ROLES, "--json"])
    captured = capsys.readouterr()

    assert json.loads(captured.out)["ok"] is True
    assert captured.err == ""
    assert not [e for e in events if e.startswith("progress: ")]


# ── test 6: the cockpit survives a blocked run, and a cockpit failure never stops the run ──


def test_a_blocked_run_leaves_the_cockpit_already_started(
        repo, capsys, planning_calls, events, monkeypatch):
    from packages.core.models import RunState
    from packages.orchestration import pingpong_job

    real_run_job = pingpong_job.run_job

    def blocked_run(job_id, **kwargs):
        job = real_run_job(job_id, **kwargs)
        job.state = RunState.BLOCKED
        job.error = "no_file_changed"
        return job

    monkeypatch.setattr(pingpong_job, "run_job", blocked_run)

    with pytest.raises(SystemExit) as exc:
        _do(capsys, "--json")

    assert exc.value.code == 1
    assert events.count("cockpit") == 1
    assert events.index("cockpit") < events.index("builder")


def test_a_cockpit_that_does_not_come_up_prints_the_manual_command_and_the_run_goes_on(
        repo, capsys, planning_calls, events, monkeypatch):
    from packages.orchestration import do_cockpit
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan

    def failing_launcher(job_id: str) -> str:
        raise do_cockpit.DoCockpitLaunchError("the cockpit did not come up within 15s; its log: x")

    monkeypatch.setattr(do_cockpit, "launch_do_cockpit", failing_launcher)

    out = _do(capsys)

    line = next(e for e in events if "cockpit did not open" in e)
    [job_id] = re.findall(r"remedy ui start ([0-9a-f]{16})", line)
    assert load_job_plan(job_id).state == JOB_COMPLETED
    assert events.index(line) < events.index("builder")
    assert f"Next: remedy ui start {job_id}" in out


def test_no_ui_still_skips_the_cockpit(repo, capsys, planning_calls, events):
    data = json.loads(_do(capsys, "--json", "--no-ui"))

    assert "cockpit" not in events
    assert _step(data, "ui")["status"] == "skipped"


# ── test 7: scaling up still works ───────────────────────────────────────────


def test_an_order_naming_two_files_keeps_the_full_lane_and_two_tasks(repo, capsys, events):
    data = json.loads(_do(capsys, "--json", "--no-llm", "--plan-only",
                          order="Write CONTRIBUTING.md and CHANGELOG.md"))

    assert "lane: full" in _step(data, "plan")["detail"]
    assert data["shape_source"] == "planner"
    [job_listing] = data["jobs"]
    assert [t["deliverable"] for t in job_listing["tasks"]] == ["CONTRIBUTING.md", "CHANGELOG.md"]


def test_force_mission_on_the_incident_order_still_scales_up(repo, capsys, events):
    data = json.loads(_do(capsys, "--json", "--no-llm", "--plan-only", "--force-mission"))

    assert "lane: full" in _step(data, "plan")["detail"]
    assert data["shape"] == "milestones"
    assert len(data["job_ids"]) >= 2


def test_a_repository_of_many_files_and_a_vague_order_is_the_full_lane(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = _commit_repo(tmp_path / "big", {f"src/mod{n}.py": "x = 1\n" for n in range(12)})
    monkeypatch.chdir(target)

    data = json.loads(_do(capsys, "--json", "--no-llm", "--plan-only", order="Tidy up the modules"))

    assert "lane: full" in _step(data, "plan")["detail"]


# ── test 8: a planner may not invent scope ───────────────────────────────────

_INVENTED_DRAFT = {
    "schema_v": "mission_plan_draft_v1",
    "milestones": [{
        "id": "M001", "goal": "The README is polished and the project is releasable",
        "rationale": "An improved README makes the project ready.",
        "depends_on": [],
        "jobs_draft": [
            {"title": "Expand README.md with badges", "goal": "Add badges to README.md",
             "est_band": "S"},
            {"title": "Add a license", "goal": "Add a LICENSE file", "est_band": "S"},
            {"title": "Add CI", "goal": "Add .github/workflows/ci.yml", "est_band": "S"},
            {"title": "Add env example", "goal": "Add .env.example", "est_band": "S"},
        ]}],
    "risks": [], "assumptions": [],
}


def test_a_planner_that_expands_improve_the_readme_is_replaced_by_the_deterministic_plan(
        tmp_path, monkeypatch, capsys):
    from packages.orchestration import do_sequence

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = _commit_repo(tmp_path / "mixed", {
        "README.md": "# Mixed\n", "src/app.py": "x = 1\n", "tests/test_app.py": "x = 1\n"})
    monkeypatch.chdir(target)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", lambda *a, **kw: None)
    monkeypatch.setattr(
        "packages.orchestration.intake.make_structured_call_fn",
        lambda model_cls, **kw: lambda prompt, attempt: json.dumps(_INVENTED_DRAFT))
    real_plan_order_job = do_sequence.plan_order_job
    monkeypatch.setattr(
        do_sequence, "plan_order_job",
        lambda order, **kwargs: real_plan_order_job(order, **{**kwargs, "no_llm": True}))

    data = json.loads(_do(capsys, "--json", "--plan-only", order="Improve the README"))

    plan_detail = _step(data, "plan")["detail"]
    assert "named files the order did not request" in plan_detail
    for invented in ("LICENSE", ".github/workflows/ci.yml", ".env.example"):
        assert invented in plan_detail
    plan_text = Path(data["mission_plan_path"]).read_text()
    for invented in ("LICENSE", "ci.yml", ".env.example"):
        assert invented not in plan_text
    for job in data["jobs"]:
        for task in job["tasks"]:
            assert not any(name in task["deliverable"] for name in ("LICENSE", "ci.yml", ".env"))


# ── test 9: the vocabulary replacement ───────────────────────────────────────


def _do_run_args() -> dict[str, object]:
    from apps.cli.command_catalog import get_command

    entry = get_command("do.run")
    return {arg.name: arg for arg in entry.args}


def test_run_unattended_replaces_yes_in_the_catalog_with_its_exact_effect():
    args = _do_run_args()

    assert "--yes" not in args
    flag = args["--run-unattended"]
    assert flag.is_flag is True
    for sentence in ("without interactive confirmation", "documented default for every open",
                     "never implies --apply, a commit, a push, a merge or a deployment"):
        assert sentence in flag.help


def test_the_parser_accepts_run_unattended_and_no_longer_knows_yes(capsys):
    from apps.cli.grouped import build_parser

    parser = build_parser()
    parsed = parser.parse_args(["do", "run", "an order", "--run-unattended"])
    assert parsed.run_unattended is True
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["do", "run", "an order", "--yes"])
    assert exc.value.code == 2
    assert "--yes" not in capsys.readouterr().out


def test_the_generated_client_interface_names_run_unattended_and_not_yes():
    from apps.cli.client_interface import build_client_interface

    operation = next(op for op in build_client_interface()["operations"]
                     if op["command_id"] == "do.run")
    names = {arg["name"] for arg in operation["arguments"]}
    assert "--run-unattended" in names and "--yes" not in names


def test_no_document_or_caller_pairs_remedy_do_with_yes():
    root = Path(__file__).resolve().parents[2]
    offenders = []
    for path in [root / "README.md", *(root / "docs" / "system").glob("*.md"),
                 *(root / "docs" / "user").glob("*.md"),
                 *(root / "packages").rglob("*.py"), *(root / "apps" / "cli").rglob("*.py")]:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if re.search(r"remedy do\b.*--yes\b|\bdo run\b.*--yes\b", line):
                offenders.append(f"{path.relative_to(root)}:{number}")
    assert offenders == []


# ── D3: the plan boundary of a full plan ─────────────────────────────────────

TWO_FILE_ORDER = "Write CONTRIBUTING.md and CHANGELOG.md"


def _plan_with_mocked_llm(monkeypatch) -> None:
    from packages.orchestration import do_sequence
    from tests.cli.test_plan_approval import _setup_llm_mocks

    real_plan_order_job = do_sequence.plan_order_job

    def planned_on_the_llm_branch(order, **kwargs):
        _setup_llm_mocks(monkeypatch, plan_succeeds=True)
        return real_plan_order_job(order, **{**kwargs, "no_llm": False})

    monkeypatch.setattr(do_sequence, "plan_order_job", planned_on_the_llm_branch)


def test_a_full_plan_without_a_terminal_or_the_flag_stops_and_names_the_flag(
        repo, capsys, monkeypatch):
    _plan_with_mocked_llm(monkeypatch)

    data = json.loads(_do(capsys, "--json", "--no-llm", "--no-ui", order=TWO_FILE_ORDER))

    assert _step(data, "run")["status"] == "stopped"
    assert "--run-unattended runs a generated plan without asking" in _step(data, "run")["detail"]
    assert any(line.startswith("remedy decision resolve") for line in data["next"])


def test_a_full_plan_runs_when_the_flag_approves_it(repo, capsys, monkeypatch):
    _plan_with_mocked_llm(monkeypatch)

    data = json.loads(_do(capsys, "--json", "--no-llm", "--no-ui", "--run-unattended",
                          order=TWO_FILE_ORDER))

    assert _step(data, "run")["status"] == "done"
    assert _snapshot(repo)[0] == ""


@pytest.mark.parametrize(("answer", "ran"), [("y", True), ("n", False), ("", False)])
def test_an_interactive_terminal_shows_the_plan_and_asks_before_a_full_plan_runs(
        repo, capsys, monkeypatch, answer, ran):
    from packages.orchestration import do_plan_confirm

    _plan_with_mocked_llm(monkeypatch)
    asked: list[str] = []
    monkeypatch.setattr(
        do_plan_confirm, "interactive_plan_confirmer",
        lambda: do_plan_confirm.make_plan_confirmer(
            ask=lambda question: asked.append(question) or answer, write=lambda line: None))

    out = _do(capsys, "--no-llm", "--no-ui", order=TWO_FILE_ORDER)

    assert len(asked) == 1
    assert f"[{'done' if ran else 'stopped'}] run:" in out
    assert _snapshot(repo)[0] == ""


def test_the_plan_confirmer_asks_a_descriptive_question_and_only_a_yes_approves():
    from types import SimpleNamespace

    from packages.orchestration.do_plan_confirm import make_plan_confirmer
    from packages.orchestration.pingpong_job import TaskEntry

    job = SimpleNamespace(
        job_id="j1", task_plan={"clarifications_resolved": [
            {"question": "Which license?", "default_answer": "MIT", "answer": ""}]},
        tasks=[TaskEntry(title="Deliver A.md", inputs={"deliverable": "A.md"})])
    shown: list[str] = []
    asked: list[str] = []

    for answer, expected in (("y", True), ("YES", True), ("n", False), ("", False)):
        confirm = make_plan_confirmer(ask=lambda q, _a=answer: asked.append(q) or _a,
                                      write=shown.append)
        assert confirm(job) is expected

    def at_end_of_input(_question):
        raise EOFError

    assert make_plan_confirmer(ask=at_end_of_input, write=shown.append)(job) is False
    assert any("Deliver A.md — deliverable: A.md" in line for line in shown)
    assert any("open question: Which license? (default: MIT)" in line for line in shown)
    assert "nothing is applied to your repository unless you pass --apply" in asked[0]
    assert "isolated workspace" in asked[0]
