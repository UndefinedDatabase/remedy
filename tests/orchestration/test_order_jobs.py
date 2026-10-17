"""`order_jobs`: an order's jobs, which one runs, which wait and why, read without a job id."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from packages.orchestration import order_jobs as OJ
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, load_job_plan, save_job_plan


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    return tmp_path / "data"


def _saved(title: str, state: str = "planned", tasks: list[TaskEntry] | None = None) -> JobPlan:
    from packages.core.models import RunState

    job = JobPlan(job_title=title, mission="m", tasks=tasks or [TaskEntry(title=f"Deliver {title}")])
    job.state = RunState(state)
    save_job_plan(job)
    return job


def test_a_waiting_job_names_the_job_it_waits_for_and_why(data_root):
    first, second = _saved("a.md", "running"), _saved("b.md")

    OJ.record_job_waits([str(first.job_id), str(second.job_id)], [str(second.job_id)])
    view = OJ.order_jobs_view([str(first.job_id), str(second.job_id)])

    assert [(job["phase"], job["executable"], job["waits_for"]) for job in view] == [
        ("running", False, None), ("waiting", False, str(first.job_id))]
    assert str(first.job_id) in view[1]["waiting_reason"] and "applied and committed" in view[1]["waiting_reason"]
    assert view[1]["story"] == f"/api/v1/jobs/{second.job_id}/story"
    assert load_job_plan(str(first.job_id)).metadata.get(OJ.ORDER_JOB_WAITS_KEY) is None


def test_a_job_whose_predecessor_was_cancelled_says_nothing_releases_it(data_root):
    """exec-1017c: it would otherwise wait for an apply that can never come."""
    first, second = _saved("a.md", "cancelled"), _saved("b.md")
    OJ.record_job_waits([str(first.job_id), str(second.job_id)], [str(second.job_id)])

    view = OJ.order_jobs_view([str(first.job_id), str(second.job_id)])

    assert view[1]["phase"] == "waiting" and view[1]["waits_for"] == str(first.job_id)
    assert "was cancelled" in view[1]["waiting_reason"] and "cancel it" in view[1]["waiting_reason"]


def test_a_job_whose_predecessor_landed_is_the_executable_one(data_root, monkeypatch):
    first, second = _saved("a.md", "completed"), _saved("b.md")
    OJ.record_job_waits([str(first.job_id), str(second.job_id)], [str(second.job_id)])
    import packages.orchestration.job_apply as JA
    monkeypatch.setattr(JA, "job_apply_landed", lambda job_id: job_id == str(first.job_id))

    view = OJ.order_jobs_view([str(first.job_id), str(second.job_id)])

    assert [(job["phase"], job["executable"]) for job in view] == [("applied", False), ("ready", True)]


@pytest.mark.parametrize(("state", "phase"), [
    ("completed", "awaiting_apply"), ("blocked", "blocked"), ("stopped", "stopped"),
    ("failed", "failed"), ("planned", "ready"), ("cancelled", "cancelled"),
])
def test_each_job_state_reads_as_the_phase_a_person_needs(data_root, state, phase):
    job = _saved("x.md", state)

    [entry] = OJ.order_jobs_view([str(job.job_id)])

    assert (entry["state"], entry["phase"]) == (state, phase)
    assert entry["phase"] in OJ.ORDER_JOB_PHASES


def test_the_tasks_say_how_far_the_job_is_and_which_one_runs(data_root):
    from packages.orchestration.pingpong_job import TASK_APPLIED, TASK_RUNNING

    job = _saved("x", "running", [TaskEntry(title="Deliver a.md", status=TASK_APPLIED),
                                  TaskEntry(title="Deliver b.md", status=TASK_RUNNING),
                                  TaskEntry(title="Deliver c.md")])

    [entry] = OJ.order_jobs_view([str(job.job_id)])

    assert entry["tasks"] == {"total": 3, "done": 1, "current": "Deliver b.md"}


def test_a_job_whose_record_is_gone_is_listed_never_dropped(data_root):
    [entry] = OJ.order_jobs_view(["0123456789abcdef"])

    assert (entry["job_id"], entry["state"], entry["executable"]) == ("0123456789abcdef", "missing", False)


def test_the_jobs_of_an_order_file_come_from_the_missions_batches_of_this_run_only(data_root, monkeypatch):
    import packages.orchestration.mission_state as MS

    batch = lambda order_id, source, at: SimpleNamespace(order_id=order_id, source_path=source, created_at=at)  # noqa: E731
    link = lambda job_id, order_id: SimpleNamespace(job_id=job_id, order_id=order_id)  # noqa: E731
    mission = SimpleNamespace(
        orders=[batch("o1", "/orders/a/order.md", "2026-10-17T10:00:00.000000+00:00"),
                batch("o2", "/orders/a/order.md", "2026-10-17T12:00:05.000000+00:00"),
                batch("o3", "/orders/b/order.md", "2026-10-17T12:00:06.000000+00:00")],
        job_links=[link("j-old", "o1"), link("j-1", "o2"), link("j-2", "o2"), link("j-other", "o3")])
    monkeypatch.setattr(MS, "project_ids_with_missions", lambda: ["p"])
    monkeypatch.setattr(MS, "list_missions", lambda project_id: [mission])

    assert OJ.order_file_job_ids("/orders/a/order.md", since="2026-10-17T12:00:00Z") == ["j-1", "j-2"]
    assert OJ.order_file_job_ids("/orders/a/order.md") == ["j-old", "j-1", "j-2"]
    assert OJ.order_file_job_ids("") == []


def test_an_order_files_walk_lists_its_job_in_the_order_poll_with_a_title_a_person_knows(tmp_path, monkeypatch):
    """The poll an HTTP client reads (`order_record_payload`, shared by `remedy client order`,
    GET and POST /api/v1/orders) names the walk's job, read from the mission batch of this order
    file, with the order's first line as its title and the phase a person needs next."""
    import contextlib
    import io
    import json

    from apps.cli.grouped import main
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import OrderRecord, order_record_payload
    from tests.orchestration.scale_harness import commit_repository

    order = ("Die Funktion add(a, b) in src/calc.js rechnet falsch.\n\nRepariere sie und ergänze einen "
             "Regressionstest in test/calc.test.js.")
    repo = commit_repository(tmp_path / "lab", {"src/calc.js": "export const add = (a, b) => a - b;\n",
                                                "package.json": "{}\n"})
    folder = tmp_path / "orders" / "o1"
    folder.mkdir(parents=True)
    (folder / "order.md").write_text(f"---\nmax-provider-calls: 20\n---\n{order}\n", encoding="utf-8")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.chdir(folder)
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
        main(["do", "run", "--repo", str(repo), "--builder-provider", "fake", "--reviewer-provider", "fake",
              "--json", "--no-ui", "--run-unattended", "--", "order.md"])
    [job_id] = json.loads(out.getvalue())["job_ids"]
    record = OrderRecord(order_id="o1", pid=0, started_at="2000-01-01T00:00:00Z",
                         order_file=str(folder / "order.md"), out_log="", err_log="", exit_code=0,
                         ended_at="2000-01-01T00:01:00Z")

    [entry] = order_record_payload(serve_paths(), record)["jobs"]

    assert (entry["job_id"], entry["phase"], entry["executable"]) == (job_id, "awaiting_apply", False)
    assert entry["title"] == "Die Funktion add(a, b) in src/calc.js rechnet falsch."
    assert entry["verification"] in ("not_required", "not_run", "passed")
    later = OrderRecord(**{**record.to_json(), "started_at": "2999-01-01T00:00:00Z"})
    assert order_record_payload(serve_paths(), later)["jobs"] == []     # another run of the same file


@pytest.mark.parametrize(("job_order", "several", "deliverables", "title"), [
    ("Fix the typo in README.md.\nChange no other files.", False, ["README.md"], "Fix the typo in README.md."),
    ("## Testbetrieb\n\nErgänze den Abschnitt.", False, [], "Testbetrieb"),
    ("Write docs/a.md and docs/b.md", True, ["docs/a.md"], "Write docs/a.md and docs/b.md — docs/a.md"),
    ("Write the API docs\n\nThis job does the part of this order that belongs to project web; …", True, [],
     "Write the API docs — in web"),
    ("Ergänze " + "sehr " * 30 + "lang", False, [], "Ergänze " + "sehr " * 13 + "sehr…"),
])
def test_a_job_title_is_the_orders_first_line_and_tells_sibling_jobs_apart(job_order, several, deliverables, title):
    from packages.orchestration.do_targets import do_job_title

    order = job_order.split("\n\nThis job does")[0] if "This job does" in job_order else job_order
    assert do_job_title(job_order, order, project_slug="web", deliverables=deliverables, several=several) == title
