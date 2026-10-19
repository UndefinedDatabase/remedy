"""exec-1018c — every open job and order is ended over HTTP exactly as its story says (R-1360, R-1361, R-1362).

The release matrix of PRs 360-364, through the public API as a client reaches it: the story is read
with `answer_public_api_get`, the action it offers is POSTed with `answer_public_api_post` and the
supervisor's own `CommandRunner`, which runs the real `remedy` command in a child process. Each job
comes from a real fake-provider run, or is such a run's record moved to a state the runner writes.
For every state the test pins what the client sees before (`state`, `next`, `end`), what the action
answers (and whether a process may still hold the job), what the story and the digest read after,
and that a fresh runner reading the disk again (a supervisor restart) reads the same. No model is
called; no order of the live data root is read.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration import public_api
from packages.orchestration.pingpong_job import job_is_terminal, load_job_plan, save_job_plan
from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.serve_runs import CommandRunner, RunRecord

_JOB = "# Job: lifecycle\n\n## Task 1\nAdd a usage line to README.md.\n\nAcceptance:\n- it is there\n"
TOKEN = "lifecycle-matrix-token-0123456789abcdef"


class Api:
    """One client of one project over the real routes; `restart()` is a supervisor that starts again."""

    def __init__(self, repo: Path, project_id: str, project_slug: str) -> None:
        from packages.orchestration.api_clients import ApiClient

        self.repo, self.project_id, self.project_slug = repo, project_id, project_slug
        self.client = ApiClient(name="lifecycle-bot", token=TOKEN, projects=(project_id,),
                                max_total_tokens=None, max_provider_calls=None, may_apply=True)
        self.runner = CommandRunner(serve_paths())

    def restart(self) -> None:
        self.runner = CommandRunner(serve_paths())

    def get(self, path: str, query: str = "") -> tuple[int, dict]:
        status, body, _headers = public_api.answer_public_api_get(path, query, client=self.client)
        return status, body

    def post(self, path: str, body: dict, runner: CommandRunner | None = None) -> tuple[int, dict]:
        status, answer, _headers = public_api.answer_public_api_post(
            path, json.dumps(body).encode(), (runner or self.runner).run, client=self.client)
        return status, answer

    def story(self, job_id: str) -> dict:
        from packages.orchestration.client_story_words import story_problems

        status, story = self.get(f"/api/v1/jobs/{job_id}/story")
        assert status == 200, story
        assert story_problems(story) == [], story
        return story

    def end(self, job_id: str, reason: str = "closed from the chat") -> tuple[int, dict]:
        """POST the route the story's `end` names, with the body a client sends: `{"reason": ...}`."""
        route = self.story(job_id)["end"]["route"]
        assert route["method"] == "POST"
        return self.post(route["path"], {"reason": reason})

    def active(self, job_id: str) -> bool:
        """Whether the digest still lists the job as needing something (DECISION F304 D16)."""
        status, digest = self.get("/api/v1/digest", "all_ended_jobs=true")
        assert status == 200, digest
        [entry] = [job for job in digest["jobs"] if job["job_id"] == job_id]
        asks = [d for d in digest["decisions"] if d["job_id"] == job_id]
        return not (job_is_terminal(entry["state"]) and not entry["waits_for_apply"] and not asks)


@pytest.fixture
def api(tmp_path, monkeypatch) -> Api:
    from packages.orchestration.project_registry import register_project_repo

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=repo, check=True)
    project = register_project_repo("lifecycle", repo)
    return Api(repo, str(project.id), str(project.slug))


def _planned(api: Api, **metadata: str) -> str:
    from packages.orchestration.pingpong_job import parse_job_file

    job = parse_job_file(_JOB, str(api.repo))
    job.project_id = api.project_id
    job.metadata.update({"target_repo": str(api.repo), **metadata})     # as an order's mission writes it
    save_job_plan(job)
    return str(job.job_id)


def _ran(api: Api) -> str:
    """A job the real runner ran to its end with fake providers: completed, its result waiting."""
    from packages.orchestration.pingpong_job import run_job
    from packages.orchestration.pingpong_provider import FakeProvider

    job_id = _planned(api)
    run_job(job_id, builder_provider=FakeProvider(), reviewer_provider=FakeProvider(), repair_rounds=1)
    assert load_job_plan(job_id).state == RunState.COMPLETED
    return job_id


def _move(job_id: str, **fields) -> None:
    job = load_job_plan(job_id)
    for name, value in fields.items():
        setattr(job, name, value)
    save_job_plan(job)


def _ended_cancelled(api: Api, job_id: str, answer: dict, status: int) -> None:
    assert status == 200, answer
    assert (answer["job_status"], answer["cancel_pending"]) == ("cancelled", False), answer
    story = api.story(job_id)
    assert (story["state"], story["state_detail"]["reason"]["key"]) == ("stopped", "cancelled")
    assert (story["next"]["action"], story["end"]) == ("none", None)
    assert api.active(job_id) is False
    assert load_job_plan(job_id).state == RunState.CANCELLED


# --- the states, one test each ------------------------------------------------------------------


def test_never_started_runs_or_ends_and_ends_for_good(api):
    job_id = _planned(api)
    story = api.story(job_id)
    assert (story["state"], story["next"]["action"], story["end"]["action"]) == ("queued", "run", "abandon")
    assert api.active(job_id) is True

    status, answer = api.end(job_id)

    _ended_cancelled(api, job_id, answer, status)
    api.restart()
    assert api.story(job_id)["end"] is None and load_job_plan(job_id).state == RunState.CANCELLED
    status, again = api.post(f"/api/v1/jobs/{job_id}/abandon", {"reason": "x"})
    assert status == 200 and again["already_cancelled"] is True


def test_waiting_for_another_job_offers_no_run_and_ends(api):
    first = _ran(api)
    job_id = _planned(api, waits_for_job=first)
    story = api.story(job_id)
    assert (story["state"], story["state_detail"], story["next"]["action"], story["end"]["action"]) == (
        "queued", {"after_job": first}, "none", "abandon")

    status, answer = api.end(job_id)

    _ended_cancelled(api, job_id, answer, status)
    assert api.story(first)["end"]["action"] == "decline"        # the predecessor is untouched


def test_a_job_whose_predecessor_was_cancelled_still_ends(api):
    first = _planned(api)
    api.post(f"/api/v1/jobs/{first}/abandon", {"reason": "not wanted"})
    job_id = _planned(api, waits_for_job=first)
    story = api.story(job_id)
    assert (story["state"], story["next"]["action"], story["end"]["action"]) == ("queued", "none", "abandon")

    status, answer = api.end(job_id)

    _ended_cancelled(api, job_id, answer, status)


def test_blocked_by_a_task_loop_cap_asks_no_budget_question_and_ends(api):
    """R-1359: the live state of 2026-10-18. No budget question is offered, so none can fail."""
    job_id = _ran(api)
    tasks = load_job_plan(job_id).tasks
    tasks[0].final_status = "budget_exhausted"
    _move(job_id, state=RunState.BLOCKED, tasks=tasks,
          error="task_0485b88a5c724372_gate_failed: final_status=budget_exhausted; missing_reviewer_output")
    story = api.story(job_id)
    assert (story["state"], story["next"]["action"], story["end"]["action"]) == ("failed", "none", "abandon")
    assert story["state_detail"]["reason"]["key"] == "budget_exhausted"
    _status, digest = api.get("/api/v1/digest")
    assert [d for d in digest["decisions"] if d["job_id"] == job_id] == []

    status, answer = api.end(job_id)

    _ended_cancelled(api, job_id, answer, status)


def test_a_stopped_job_resumes_or_ends(api):
    job_id = _planned(api)
    _move(job_id, state=RunState.STOPPED, stop_source="api", stop_reason="later",
          stop_request_id="s1", stopped_at="2026-10-18T10:00:00+00:00")
    story = api.story(job_id)
    assert (story["state"], story["next"]["action"], story["end"]["action"]) == ("stopped", "resume", "abandon")
    assert story["next"]["route"]["path"] == f"/api/v1/jobs/{job_id}/run"

    status, answer = api.end(job_id)

    _ended_cancelled(api, job_id, answer, status)


def _budget_stopped(api: Api) -> str:
    job_id = _planned(api)
    _move(job_id, state=RunState.STOPPED, stop_source="budget", stop_reason="budget_exhausted:max_provider_calls",
          stop_request_id="req-b1", stopped_at="2026-10-18T10:00:00+00:00")
    return job_id


def test_a_budget_stop_is_answered_abandon_through_its_question(api):
    job_id = _budget_stopped(api)
    story = api.story(job_id)
    assert (story["state"], story["state_detail"]["question"]) == ("waiting", "token_budget")
    assert (story["next"]["action"], story["end"]["action"]) == ("answer", "abandon")

    status, answer = api.post(story["next"]["route"]["path"], {"reason": "abandon"})

    assert status == 200, answer
    assert api.story(job_id)["end"] is None and load_job_plan(job_id).state == RunState.CANCELLED
    assert api.active(job_id) is False


def test_a_budget_stop_is_also_ended_through_the_story_end_and_its_question_closes(api):
    job_id = _budget_stopped(api)

    status, answer = api.end(job_id)

    _ended_cancelled(api, job_id, answer, status)
    _status, digest = api.get("/api/v1/digest")
    assert [d for d in digest["decisions"] if d["job_id"] == job_id] == []


def test_an_answered_budget_stop_then_stopped_by_the_person_asks_nothing_unanswerable(api):
    """R-1362 over HTTP: extended, resumed, then stopped from the chat; the old question stays closed."""
    job_id = _budget_stopped(api)
    question = api.story(job_id)["next"]["route"]["path"]
    status, answer = api.post(question, {"reason": "extend", "answer": ["max_provider_calls=50"]})
    assert status == 200, answer
    _move(job_id, stop_source="api", stop_reason="closed", stop_request_id="req-s2",
          stopped_at="2099-01-01T00:00:00+00:00")
    story = api.story(job_id)
    assert (story["state"], story["next"]["action"], story["end"]["action"]) == ("stopped", "resume", "abandon")

    status, answer = api.end(job_id)

    _ended_cancelled(api, job_id, answer, status)



def _awaiting_plan_approval(api: Api) -> str:
    """A job whose task plan waits for the person's approval, as `remedy do --approve-plan` leaves it."""
    job_id = _planned(api)
    job = load_job_plan(job_id)
    job.task_plan = {"_approval": "pending", "tasks": [{"title": "Add a usage line", "files": ["README.md"]}]}
    save_job_plan(job)
    return job_id


def test_a_plan_waiting_for_approval_is_answered_through_its_question_or_ended(api):
    job_id = _awaiting_plan_approval(api)
    story = api.story(job_id)
    assert (story["state"], story["state_detail"]["question"]) == ("waiting", "task_plan_approval")
    assert (story["next"]["action"], story["end"]["action"]) == ("answer", "abandon")

    status, answer = api.post(story["next"]["route"]["path"], {"reason": "approve"})

    assert status == 200 and answer["outcome"] == "approved", answer
    story = api.story(job_id)
    assert (story["state"], story["next"]["action"], story["end"]["action"]) == ("queued", "run", "abandon")
    _ended_cancelled(api, job_id, *reversed(api.end(job_id)))


def test_a_rejected_plan_offers_no_run_and_ends_through_its_end(api):
    """R-1366: a rejected plan is final for its job; before, the story read `queued` and offered `run`,
    which every run refuses with `plan_rejected`, and the order's view still read `needs_plan_approval`."""
    from packages.orchestration.order_jobs import order_jobs_view

    job_id = _awaiting_plan_approval(api)
    status, answer = api.post(api.story(job_id)["next"]["route"]["path"], {"reason": "reject"})
    assert status == 200 and answer["outcome"] == "rejected", answer

    story = api.story(job_id)
    assert (story["state"], story["state_detail"]["reason"]["key"]) == ("stopped", "declined")
    assert (story["next"]["action"], story["end"]["action"]) == ("none", "abandon")
    assert [entry["phase"] for entry in order_jobs_view([job_id])] == ["declined"]
    assert api.active(job_id) is True                 # still open until the person ends it

    _ended_cancelled(api, job_id, *reversed(api.end(job_id)))


def test_a_result_waiting_for_its_apply_is_declined_and_stays_auditable(api):
    job_id = _ran(api)
    story = api.story(job_id)
    assert (story["state"], story["next"]["action"], story["end"]["action"]) == ("done", "apply", "decline")
    assert api.active(job_id) is True
    status, refused = api.post(story["end"]["route"]["path"], {})      # a decline needs its reason
    assert (status, refused["error"]) == (400, "missing_argument"), refused
    assert api.story(job_id)["end"]["action"] == "decline"

    status, answer = api.end(job_id, reason="not what I asked for")

    assert status == 200 and answer["already_declined"] is False, answer
    story = api.story(job_id)
    assert (story["state"], story["state_detail"]["reason"]["key"], story["end"]) == ("stopped", "declined", None)
    assert story["changes"], story                                      # the result stays readable
    assert api.active(job_id) is False
    api.restart()
    status, again = api.post(f"/api/v1/jobs/{job_id}/decline", {"reason": "again"})
    assert status == 200 and again["already_declined"] is True and again["reason"] == "not what I asked for"
    status, refused = api.post(f"/api/v1/jobs/{job_id}/abandon", {"reason": "x"})
    assert (status, refused["error"]) == (409, "job_not_cancellable")   # `end` is null: nothing offered it


def test_an_ended_job_offers_nothing_and_every_end_route_refuses_or_repeats(api):
    failed = _planned(api)
    _move(failed, state=RunState.FAILED)
    story = api.story(failed)
    assert (story["state"], story["next"]["action"], story["end"]) == ("failed", "none", None)
    status, refused = api.post(f"/api/v1/jobs/{failed}/abandon", {"reason": "x"})
    assert (status, refused["error"]) == (409, "job_not_cancellable")
    assert api.active(failed) is False


def test_a_running_job_ends_at_its_safe_point_and_at_once_when_its_process_is_gone(api):
    """The run the supervisor started is alive: the cancel is pending and the job still runs. Once that
    process is gone (a crash, a restart), the same request ends the job at once (R-1361's sibling)."""
    job_id = _planned(api)
    _move(job_id, state=RunState.RUNNING)
    holder = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)", job_id])
    paths = serve_paths()
    paths.runs_dir.mkdir(parents=True, exist_ok=True)
    (paths.runs_dir / f"{job_id}.json").write_text(json.dumps(RunRecord(
        job_id=job_id, pid=holder.pid, started_at="2026-10-18T10:00:00Z", out_log="o", err_log="e").to_json()))
    try:
        assert api.story(job_id)["end"]["action"] == "abandon"
        status, answer = api.end(job_id)
        assert status == 200 and (answer["cancel_pending"], answer["job_status"]) == (True, "running"), answer
        assert api.story(job_id)["end"]["action"] == "abandon" and api.active(job_id) is True
    finally:
        holder.kill()
        holder.wait()

    status, answer = api.end(job_id, reason="once more")

    _ended_cancelled(api, job_id, answer, status)
    assert load_job_plan(job_id).metadata["cancel"]["reason"] == "closed from the chat"   # the first stands


def test_two_clients_ending_the_same_job_end_it_once(api):
    job_id = _planned(api)
    answers: list[tuple[int, dict]] = []
    second = CommandRunner(serve_paths())        # two supervisors' runners: nothing serializes them
    path = api.story(job_id)["end"]["route"]["path"]

    threads = [threading.Thread(target=lambda r=r: answers.append(api.post(path, {"reason": "mine"}, r)))
               for r in (api.runner, second)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(60)

    assert [status for status, _ in answers] == [200, 200], answers
    assert {a["job_status"] for _, a in answers} == {"cancelled"}
    assert len({a["cancel"]["requested_at"] for _, a in answers}) == 1   # one request, read by both
    _ended_cancelled(api, job_id, answers[0][1] | {"cancel_pending": False}, 200)


def test_a_decline_while_another_client_polls_reads_one_story_at_a_time(api):
    job_id = _ran(api)
    seen: list[tuple[str, str | None]] = []
    done = threading.Event()

    def poll() -> None:
        while not done.is_set():
            story = api.story(job_id)
            seen.append((story["state"], (story["end"] or {}).get("action")))
            time.sleep(0.01)

    poller = threading.Thread(target=poll)
    poller.start()
    try:
        status, answer = api.end(job_id, reason="no")
    finally:
        done.set()
        poller.join(30)

    assert status == 200, answer
    assert set(seen) <= {("done", "decline"), ("stopped", None)}, set(seen)
    assert api.story(job_id)["state"] == "stopped"


def test_a_client_of_another_project_ends_nothing(api, tmp_path):
    from packages.orchestration.api_clients import ApiClient

    job_id = _ran(api)
    other = ApiClient(name="other-bot", token=TOKEN, projects=("another-project",),
                      max_total_tokens=None, max_provider_calls=None, may_apply=True)
    for action in ("decline", "abandon"):
        status, body, _headers = public_api.answer_public_api_post(
            f"/api/v1/jobs/{job_id}/{action}", b'{"reason": "x"}', api.runner.run, client=other)
        assert (status, body["error"]) == (403, "api_client_policy_refused"), (action, body)
    assert api.story(job_id)["end"]["action"] == "decline"


#: A stand-in for `remedy do run` that waits for a release file, so the order reads `running` while
#: it plans; it never makes a job, as a walk cancelled during planning makes none.
_PLANNING_ORDER_CHILD = """\
import sys, time
from pathlib import Path
release = Path(sys.argv[3])
deadline = time.monotonic() + 60
while not release.exists() and time.monotonic() < deadline:
    time.sleep(0.01)
"""


def test_an_order_still_planning_is_cancelled_and_stays_cancelled_after_a_restart(api, tmp_path):
    from packages.orchestration.serve_runs import OrderLauncher

    release = tmp_path / "release"
    launcher = OrderLauncher(serve_paths(), argv_prefix=[sys.executable, "-c", _PLANNING_ORDER_CHILD])
    record = launcher.start(f"---\nproject: {api.project_slug}\n---\nAdd a usage line.\n", [str(release)])
    order = f"/api/v1/orders/{record.order_id}"
    try:
        status, polled = api.get(order)
        assert status == 200 and polled["phase"] == "planning", polled
        status, answer = api.post(f"{order}/cancel", {"reason": "wrong project"})
        assert status == 200, answer
        assert (answer["state"], answer["phase"], answer["already_cancelled"]) == ("running", "cancelling", False)
        _status, polled = api.get(order)
        assert polled["phase"] == "cancelling"            # its process may still run: never `cancelled` yet
    finally:
        release.touch()
        launcher.wait(record.order_id, timeout=30)

    api.restart()
    status, polled = api.get(order)
    assert status == 200 and (polled["state"], polled["phase"], polled["jobs"]) == ("ended", "cancelled", [])
    assert polled["cancel"]["reason"] == "wrong project"
    status, again = api.post(f"{order}/cancel", {"reason": "twice"})
    assert status == 200 and again["already_cancelled"] is True and again["cancel"]["reason"] == "wrong project"
