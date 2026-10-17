"""The README order of 2026-10-17 (order a6a87e65809f6bd6, job 84b0cc4272164bb2), replayed without a model.

The order came through the public HTTP API, so the supervisor ran `remedy do run ... -- order.md`
from the order's own folder. It walked the full lane (the two sentences to insert, "Verändere sonst
nichts" and "Führe den vorhandenen Testbefehl aus" each counted as a part), and the planner's repo
facts listed that folder (order.md, order.json, out.log, err.log) instead of the repository, so it
planned a task that wrote `test_command.txt`. Its builder then took 28 Pi turns and 223,221 input
tokens for a three-line append. This module holds the order, the lab repository's files and the
expectations the fix must meet: one bounded job, one task for README.md, no planner call.
"""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path

import pytest

from packages.orchestration.do_lane import select_do_lane
from packages.orchestration.job_plan import compose_task_plan_prompt
from packages.orchestration.order_scope import split_order_scope
from tests.orchestration.scale_harness import FakePlannerService, commit_repository

#: The order exactly as the job record holds it (`mission`).
INCIDENT_ORDER = (
    "Ergänze am Ende der Datei `README.md` den Abschnitt `## Testbetrieb` mit genau diesen zwei Sätzen:\n\n"
    "Dieses Repository dient ausschließlich dazu, Codeänderungen sicher zu testen.\n"
    "Alle Änderungen werden vor der Übernahme geprüft.\n\n"
    "Verändere sonst nichts. Führe den vorhandenen Testbefehl aus. Übernimm die Änderungen nicht automatisch."
)

#: The lab repository at its base commit 2aef9be (contents shortened; names and the test script exact).
LAB_FILES = {
    ".gitignore": "node_modules/\n",
    "README.md": "# remedy-lab\n\nRun the tests with `npm test` (Node's built-in test runner, Node 20 or newer).\n",
    "package.json": json.dumps({"name": "remedy-lab", "private": True, "type": "module",
                                "scripts": {"test": "node --test"}}, indent=2) + "\n",
    "src/calc.js": "export function add(a, b) {\n  return a - b;\n}\n",
    "src/format.js": "export function normalizeName(input) {\n  return input.trim();\n}\n",
    "test/baseline.test.js": "import test from 'node:test';\n\ntest('baseline', () => {});\n",
}

#: What the supervisor's order folder holds while the order runs (serve_runs.OrderLauncher).
ORDER_FOLDER_FILES = ("order.md", "order.json", "out.log", "err.log")


def test_the_incident_order_is_one_part_on_readme_bound_by_three_constraints():
    scope = split_order_scope(INCIDENT_ORDER)

    [deliverable] = scope.deliverables
    assert "Dieses Repository dient ausschließlich dazu, Codeänderungen sicher zu testen." in deliverable
    assert "Alle Änderungen werden vor der Übernahme geprüft." in deliverable
    assert scope.constraints == ("Verändere sonst nichts.", "Führe den vorhandenen Testbefehl aus.",
                                 "Übernimm die Änderungen nicht automatisch.")
    lane = select_do_lane(INCIDENT_ORDER, tracked_files=sorted(LAB_FILES))
    assert (lane.lane, lane.deliverable, lane.with_tests) == ("bounded", "README.md", False)


def test_the_task_planner_is_shown_the_target_repository_not_the_order_folder(tmp_path, monkeypatch):
    repo = commit_repository(tmp_path / "lab", LAB_FILES)
    folder = tmp_path / "orders" / "a6a87e65809f6bd6"
    folder.mkdir(parents=True)
    for name in ORDER_FOLDER_FILES:
        (folder / name).write_text("")
    monkeypatch.chdir(folder)

    text = compose_task_plan_prompt({"goal": "g"}, repo_root=str(repo)).text

    assert "Top-level files: README.md, package.json" in text
    assert not any(name in text for name in ORDER_FOLDER_FILES)


def _walk_order_file(tmp_path: Path, monkeypatch, order: str, files: dict[str, str]):
    """`remedy do run --repo <lab> ... -- order.md` from an order folder, as the supervisor runs it."""
    from apps.cli.grouped import main
    from packages.orchestration.pingpong_job import load_job_plan

    repo = commit_repository(tmp_path / "lab", files)
    folder = tmp_path / "orders" / "replay"
    folder.mkdir(parents=True)
    (folder / "order.md").write_text(f"---\nmax-provider-calls: 20\n---\n{order}\n", encoding="utf-8")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.chdir(folder)
    planner = FakePlannerService(target="README.md").install(monkeypatch)
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
        main(["do", "run", "--repo", str(repo), "--builder-provider", "fake", "--reviewer-provider", "fake",
              "--json", "--no-ui", "--run-unattended", "--", "order.md"])
    answer = json.loads(out.getvalue())
    jobs = [load_job_plan(job_id) for job_id in answer["job_ids"]]
    return answer, jobs, planner


def test_the_incident_order_from_its_order_folder_is_one_job_one_task_and_no_planner_call(tmp_path, monkeypatch):
    answer, jobs, planner = _walk_order_file(tmp_path, monkeypatch, INCIDENT_ORDER, LAB_FILES)

    steps = {step["name"]: step for step in answer["steps"]}
    assert "lane: bounded" in steps["plan"]["detail"], steps["plan"]["detail"]
    assert planner.count() == 0
    [job] = jobs
    [task] = job.tasks
    assert task.inputs.get("deliverable") == "README.md"
    assert INCIDENT_ORDER in task.body             # the exact sentences reach the builder
    assert steps["apply"]["status"] == "stopped"   # nothing lands without approval


@pytest.mark.parametrize("order", [
    "Fix the typo in README.md and change nothing else.",
    "Korrigiere den Tippfehler in README.md. Verändere sonst nichts.",
    "Add a line to README.md with this text:\nHello world.\nSecond line.\n\nRun the test command.",
])
def test_fences_and_test_runs_of_any_wording_keep_a_one_file_order_bounded(order):
    lane = select_do_lane(order, tracked_files=sorted(LAB_FILES))

    assert (lane.lane, lane.deliverable) == ("bounded", "README.md"), lane.reason


def test_every_planner_prompt_of_a_full_lane_order_describes_the_repository(tmp_path, monkeypatch):
    order = "Fix add in src/calc.js and normalizeName in src/format.js."
    _answer, _jobs, planner = _walk_order_file(tmp_path, monkeypatch, order, LAB_FILES)

    facts = [prompt for prompt in planner.prompts if "Top-level files:" in prompt]
    assert facts, planner.by_schema()                 # the mission plan and the task plan carry facts
    for prompt in facts:
        assert "README.md, package.json" in prompt
        assert not any(name in prompt for name in ORDER_FOLDER_FILES)
