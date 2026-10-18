"""exec-1017c (R-1338) — an order the supervisor started is cancelled whatever it is doing.

Each test runs a real `remedy do run -- order.md` walk in this process, as `OrderLauncher` runs it:
from the order's own folder under the data root, beside an `order.json` record whose pid is this
process. The cancel arrives at a precise point (during
planning, between saving a job and the walk reading the request, while a builder call is in
flight, right before an apply, after the walk ended) and each test reads what the lifecycle did:
the steps, the jobs' states, the order's answer, the apply records. Fake providers only.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import threading
import time
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from packages.core.models import RunState
from packages.orchestration.order_cancel import cancel_order, order_cancel_request
from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan
from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.serve_runs import OrderRecord, order_record_job_ids, order_record_payload
from tests.orchestration.scale_harness import commit_repository

ORDER_ID = "0123456789abcdef"
README = {"README.md": "# Project\n\nA projcet with a typo.\n"}


@pytest.fixture
def order(tmp_path, monkeypatch):
    """The order's folder, record and repository; `walk(text, *flags)` runs it and answers the envelope."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    repo = commit_repository(tmp_path / "work", README)
    order_dir = serve_paths().orders_dir / ORDER_ID
    order_dir.mkdir(parents=True)
    order_dir = order_dir.resolve()
    record = OrderRecord(order_id=ORDER_ID, pid=os.getpid(),
                         started_at=(datetime.now(timezone.utc) - timedelta(seconds=5)).isoformat(),
                         order_file=str(order_dir / "order.md"), out_log=str(order_dir / "out.log"),
                         err_log=str(order_dir / "err.log"))
    (order_dir / "order.json").write_text(json.dumps(record.to_json()), encoding="utf-8")
    monkeypatch.chdir(order_dir)               # as OrderLauncher runs it: the walk is "this order"

    class Order:
        paths, folder, repository = serve_paths(), order_dir, repo
        rec = record

        @staticmethod
        def walk(text: str, *flags: str, header: str = "max-cost-usd: 1") -> dict:
            from apps.cli.grouped import main

            (order_dir / "order.md").write_text(f"---\n{header}\n---\n{text}\n", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
                main(["do", "run", "--repo", str(repo), "--builder-provider", "fake",
                      "--reviewer-provider", "fake", "--json", "--no-ui", "--run-unattended", *flags,
                      "--", "order.md"])
            return json.loads(out.getvalue())

        @staticmethod
        def cancel(**kwargs) -> dict:
            return cancel_order(serve_paths(), record, reason=kwargs.pop("reason", "not wanted"),
                                source="test", **kwargs)

    return Order


def _steps(envelope: dict) -> dict[str, tuple[str, str]]:
    return {step["name"]: (step["status"], step["detail"]) for step in envelope["steps"]}


def _wrap_step(monkeypatch, name: str, after) -> None:
    """Run *after(ctx)* right after the walk's step *name* returns, inside the step."""
    from packages.orchestration import do_sequence

    original = do_sequence.DO_STEP_TABLE[name]

    def step(ctx):
        result = original(ctx)
        after(ctx)
        return result
    monkeypatch.setitem(do_sequence.DO_STEP_TABLE, name, step)


def test_a_cancel_while_planning_stops_the_walk_before_any_job_exists(order, monkeypatch):
    _wrap_step(monkeypatch, "plan", lambda ctx: order.cancel())

    envelope = order.walk("Fix the typo in README.md.")

    steps = _steps(envelope)
    assert steps["shape"][0] == "stopped" and "the order was cancelled" in steps["shape"][1]
    assert "run" not in steps and "apply" not in steps
    assert envelope.get("job_ids") in ([], None)
    payload = order_record_payload(order.paths, order.rec)
    assert payload["cancel"]["reason"] == "not wanted" and payload["jobs"] == []


def test_a_job_saved_after_the_clients_listing_is_still_cancelled_and_never_runs(order, monkeypatch):
    """The race: the cancel lists the order's jobs before the walk links the one it is saving."""
    from packages.orchestration import do_sequence

    original = do_sequence.name_do_job
    answers = []

    def name_then_cancel(job, *args, **kwargs):
        original(job, *args, **kwargs)
        answers.append(order.cancel())         # the job is saved, not yet linked to its mission
    monkeypatch.setattr(do_sequence, "name_do_job", name_then_cancel)

    envelope = order.walk("Fix the typo in README.md.")

    assert answers[0]["jobs"] == []            # the client's listing could not see it
    [job_id] = order_record_job_ids(order.rec)
    assert load_job_plan(job_id).state == RunState.CANCELLED
    steps = _steps(envelope)
    assert steps["shape"][0] == "stopped" and job_id in steps["shape"][1]
    assert "run" not in steps


def test_a_cancel_while_the_builder_runs_ends_the_job_cancelled_and_applies_nothing(order, monkeypatch):
    from packages.orchestration.job_apply import job_apply_landed
    from packages.orchestration.pingpong_provider import FakeProvider

    original, answers = FakeProvider.build, []

    def build(self, prompt, **kwargs):
        if not answers:
            answers.append(order.cancel())
        return original(self, prompt, **kwargs)
    monkeypatch.setattr(FakeProvider, "build", build)

    envelope = order.walk("Fix the typo in README.md.", "--apply")

    assert answers[0]["phase"] == "cancelling" and answers[0]["state"] == "running"
    assert [entry["outcome"] for entry in answers[0]["jobs"]] == ["cancel_pending"]
    [job_id] = order_record_job_ids(order.rec)
    assert load_job_plan(job_id).state == RunState.CANCELLED
    steps = _steps(envelope)
    assert steps["run"][0] == "stopped" and "the order was cancelled" in steps["run"][1]
    assert "apply" not in steps and not job_apply_landed(job_id)


def test_a_cancel_right_before_the_apply_lands_nothing(order, monkeypatch):
    from packages.orchestration.job_apply import job_apply_landed

    _wrap_step(monkeypatch, "run", lambda ctx: order.cancel())

    envelope = order.walk("Fix the typo in README.md.", "--apply")

    [job_id] = order_record_job_ids(order.rec)
    steps = _steps(envelope)
    assert steps["apply"][0] == "stopped" and "the order was cancelled" in steps["apply"][1]
    assert load_job_plan(job_id).state == JOB_COMPLETED and not job_apply_landed(job_id)


def test_a_walks_apply_between_jobs_refuses_once_the_order_is_cancelled(order, monkeypatch):
    from packages.orchestration import do_apply, job_apply

    def must_not_apply(*args, **kwargs):
        raise AssertionError("an apply ran after the cancel")
    monkeypatch.setattr(job_apply, "apply_job", must_not_apply)
    (order.folder / "order.md").write_text("x", encoding="utf-8")
    order.cancel()

    class Ctx:
        commit_mode, job_ids, next_lines, applied = False, ["j1"], [], {}

    assert "the order was cancelled" in do_apply.do_apply_one_job(Ctx(), "j1")


def test_after_the_walk_a_cancel_ends_the_waiting_job_and_leaves_the_result_to_the_person(
        order, monkeypatch, tmp_path):
    envelope = order.walk("Add a usage section to README.md and add a CHANGELOG.md entry.", "--force-mission")
    first, second = envelope["job_ids"][:2]
    assert load_job_plan(first).state == JOB_COMPLETED and second in envelope["waiting_job_ids"]
    monkeypatch.chdir(tmp_path)               # the walk's process has ended: it is no longer "this order"

    answer = order.cancel()
    again = order.cancel(reason="twice")

    outcomes = {entry["job_id"]: entry["outcome"] for entry in answer["jobs"]}
    assert outcomes[first] == "awaiting_decision" and outcomes[second] == "cancelled"
    assert load_job_plan(second).state == RunState.CANCELLED
    assert answer["phase"] == "cancelled" and answer["already_cancelled"] is False
    assert again["already_cancelled"] is True and again["cancel"]["reason"] == "not wanted"
    assert {entry["outcome"] for entry in again["jobs"]} == {"awaiting_decision", "already_cancelled"}

    declined = order.cancel(decline_results=True)
    assert {entry["job_id"]: entry["outcome"] for entry in declined["jobs"]}[first] == "declined"
    view = {entry["job_id"]: entry["phase"] for entry in order_record_payload(order.paths, order.rec)["jobs"]}
    assert view == {first: "declined", second: "cancelled"}
    assert order_cancel_request(order.folder)["reason"] == "not wanted"


def test_only_a_walk_run_from_a_supervised_order_folder_reads_a_cancel(tmp_path, monkeypatch):
    """A `remedy do` in a terminal is stopped with Ctrl-C; its step table stays as it is."""
    from packages.orchestration import do_sequence
    from packages.orchestration.order_cancel import cancellable_do_steps, walk_order_dir

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.chdir(tmp_path)
    assert walk_order_dir() is None
    assert cancellable_do_steps(do_sequence.DO_STEP_TABLE) is do_sequence.DO_STEP_TABLE
    folder = serve_paths().orders_dir / ORDER_ID
    folder.mkdir(parents=True)
    monkeypatch.chdir(folder)
    assert walk_order_dir() is None             # no record: not an order the supervisor started
    (folder / "order.json").write_text("{}", encoding="utf-8")
    assert walk_order_dir() == folder.resolve()


def test_the_review_report_of_a_cancelled_order_says_cancelled_and_why(order, monkeypatch):
    from packages.orchestration.review_reports import review_reports_dir

    _wrap_step(monkeypatch, "plan", lambda ctx: order.cancel(reason="wrong repository"))

    envelope = order.walk("Fix the typo in README.md.", "--capture-review")

    report = json.loads((review_reports_dir() / f"{envelope['review_report']['report_id']}.json").read_text())
    assert report["outcome"]["status"] == "cancelled"
    assert "wrong repository" in report["outcome"]["reason"] and "shape" in report["outcome"]["reason"]
    assert report["order"]["supervisor_order_id"] == ORDER_ID
    assert report["order"]["cancel"]["reason"] == "wrong repository"


def test_a_waiting_job_run_later_joins_its_walks_review_report(order, monkeypatch):
    from apps.cli.grouped import main
    from packages.orchestration.review_reports import review_reports_dir

    envelope = order.walk("Add a usage section to README.md and add a CHANGELOG.md entry.",
                          "--force-mission", "--capture-review")
    waiting = envelope["waiting_job_ids"][0]
    path = review_reports_dir() / f"{envelope['review_report']['report_id']}.json"
    before = {job["job_id"]: job["state"] for job in json.loads(path.read_text())["jobs"]}
    assert before[waiting] == "planned"

    with contextlib.redirect_stdout(io.StringIO()), contextlib.suppress(SystemExit):
        main(["job", "run", waiting, "--builder-provider", "fake", "--reviewer-provider", "fake", "--json"])

    report = json.loads(path.read_text())
    after = {job["job_id"]: job["state"] for job in report["jobs"]}
    assert after[waiting] == load_job_plan(waiting).state.value != "planned"
    assert [entry["job_id"] for entry in report["continued"]] == [waiting]


def _streaming_planner(monkeypatch, on_plan_call):
    """The REAL `OllamaPlanner` over a fake `ollama.Client` whose mission-plan answer never ends.

    Every other schema answers the scale harness's minimal document at once. The mission plan's
    stream calls *on_plan_call()* (the client's cancel arrives while the call is in flight) and then
    yields nothing until its connection is closed, as a model that is still generating would.
    """
    import ollama

    from tests.orchestration.scale_harness import FakePlannerService

    service, closed, marks = FakePlannerService(target="README.md"), threading.Event(), {}

    def answer_chunks(title: str, prompt: str):
        if title == "MissionPlanDraft":
            on_plan_call()
            marks["cancelled_at"] = time.monotonic()
            if not closed.wait(30):
                raise AssertionError("the planner call was never ended")
            marks["closed_at"] = time.monotonic()
            raise OSError("the connection was closed")
        yield SimpleNamespace(message=SimpleNamespace(content=service.answer(title, prompt)))

    class Client:
        def __init__(self, *args, **kwargs):
            self._client = SimpleNamespace(close=closed.set)

        def list(self):
            return {"models": []}

        def chat(self, *, model, messages, format, stream=False, options=None):
            chunks = answer_chunks(str(format.get("title")), messages[-1]["content"])
            return chunks if stream else next(chunks)

    monkeypatch.setattr(ollama, "Client", Client)
    return service, marks


def test_a_cancel_ends_the_planner_call_in_flight_and_no_plan_is_written(order, monkeypatch):
    """exec-1018 (R-1346): the mission-plan call is streaming when the client cancels; the walk's
    reader ends that call within about a poll, the step writes no plan (no deterministic fallback)
    and stops, nothing is shaped or run, and a second cancel changes nothing."""
    from packages.orchestration.data_paths import resolve_data_root

    _service, marks = _streaming_planner(monkeypatch, lambda: order.cancel(reason="changed my mind"))

    envelope = order.walk("Improve error handling everywhere in the project.", "--force-mission",
                          header="max-provider-calls: 20")

    steps = _steps(envelope)
    assert steps["plan"][0] == "stopped", steps
    assert "the order was cancelled" in steps["plan"][1] and "wrote no plan" in steps["plan"][1]
    assert "shape" not in steps and "run" not in steps and "apply" not in steps
    assert marks["closed_at"] - marks["cancelled_at"] < 1.5, marks
    assert envelope.get("job_ids") in ([], None)
    assert list(resolve_data_root().rglob("mission_plan*.md")) == []   # no fallback plan after it
    assert order.cancel()["already_cancelled"] is True
    assert order_record_payload(order.paths, order.rec)["phase"] in ("cancelled", "cancelling")
