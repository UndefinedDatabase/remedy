"""F334: job 3f80bd014da944e2's merged no-change task, and its builder's refused Bash.

Task 2 („Remove onInfo wiring from NetHeader.tsx + Run full test suite and confirm green“) staged
nothing because task 1 had changed NetHeader.tsx; its run part names an e2e spec nobody changes. The
builder had one compound command refused and then ran no test at all. Fakes only; no model call.
"""
from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration import job_task_already_done as A
from packages.orchestration.claude_cli_command import (
    build_claude_cli_args,
    builder_allowed_commands,
    builder_bash_note,
)
from packages.orchestration.empty_diff_gate import reject_verdict_on_empty_diff
from packages.orchestration.pingpong_job import TASK_APPLIED, ApplyManifest, TaskEntry
from packages.orchestration.pingpong_provider import ReviewerOutput, ReviewFinding

_NET_HEADER = "src/screens/net/NetHeader.tsx"
_MERGED = ("Remove onInfo wiring from NetHeader.tsx + Run full test suite and confirm green: Delete the "
           "onInfo prop from NetHeader's props interface.; Execute the project's standard test command to "
           "verify that all e2e tests (including memory-net-592.spec.ts) pass.")


class _Job:
    def __init__(self, tasks: list[TaskEntry]) -> None:
        self.tasks = tasks


def _job(second_title: str = _MERGED, deliverable: str = _NET_HEADER) -> _Job:
    first = TaskEntry(task_id="d683a401", title="Replace hand-built (i) with InfoButton in Memory.tsx",
                      status=TASK_APPLIED)
    first.inputs = {"deliverable": "src/screens/Memory.tsx", "plan": {"files_hint": []}}
    first.apply_manifest = ApplyManifest(task_id="d683a401", status="applied", applied_files=[
        "src/screens/KnowledgeNet.tsx", "src/screens/Memory.tsx", _NET_HEADER])
    second = TaskEntry(task_id="66a9a589", title=second_title)
    second.inputs = {"deliverable": deliverable,
                     "plan": {"files_hint": [_NET_HEADER, "tests/e2e/memory-net-592.spec.ts"]}}
    return _Job([first, second])


def test_a_lone_deliverable_path_is_read_as_a_path() -> None:
    assert A.paths_in(_NET_HEADER) == [_NET_HEADER]
    assert A.task_named_files(_job().tasks[1]) == [_NET_HEADER, "tests/e2e/memory-net-592.spec.ts"]


def test_a_merged_task_splits_into_its_parts_and_its_run_part_is_a_test_run() -> None:
    parts = A.task_parts(_job().tasks[1])
    assert [p.split(":")[0] for p in parts] == ["Remove onInfo wiring from NetHeader.tsx",
                                                 "Run full test suite and confirm green"]
    assert [A.is_test_run_text(p) for p in parts] == [False, True]


def test_the_merged_task_is_already_done_by_task_one_without_the_spec_its_run_part_names() -> None:
    job = _job()
    work = A.earlier_work(job, job.tasks[1])
    assert work is not None and (work.task_number, work.file_names()) == (1, [_NET_HEADER])
    gate = A.settle_already_done(job, job.tasks[1], type("R", (), {"staged_files": []})(),
                                 (False, ["no_file_changed"]))
    assert gate == (True, []) and A.already_done_record(job.tasks[1])["task_id"] == "d683a401"


def test_a_merged_task_whose_work_part_names_an_untouched_file_is_not_already_done() -> None:
    job = _job(_MERGED.replace("NetHeader.tsx", "src/screens/Other.tsx"), deliverable="src/screens/Other.tsx")
    assert A.earlier_work(job, job.tasks[1]) is None


def test_a_merge_of_two_test_runs_checks_every_earlier_file() -> None:
    job = _job("Run the unit tests + Run the e2e tests", deliverable="")
    job.tasks[1].inputs["plan"]["files_hint"] = []
    work = A.earlier_work(job, job.tasks[1])
    assert work is not None and work.test_run


def test_a_review_with_only_low_findings_keeps_its_verdict_on_the_no_change_path() -> None:
    """The reviewer's R1 of job 3f80 (low: the builder ran no test) counts as a pass (F321)."""
    low = ReviewerOutput(verdict="needs_repair", summary="", findings=[ReviewFinding(
        id="R1", severity="low", file=_NET_HEADER, summary="The builder did not run the suite itself.")])
    assert reject_verdict_on_empty_diff(low, staged_files=[], is_fake=False, already_done=True) is low
    assert low.verdict == "needs_repair" and low.findings[0].id == "R1"   # unchanged, so the gate sees all-low


def _workspace(tmp_path: Path) -> str:
    scripts = {"typecheck": "tsc -p tsconfig.json --noEmit", "test": "vitest run", "e2e": "playwright test"}
    (tmp_path / "package.json").write_text(json.dumps({"scripts": scripts}))
    return str(tmp_path)


def test_the_project_runners_are_allowed_in_every_spelling(tmp_path: Path) -> None:
    allowed = builder_allowed_commands(_workspace(tmp_path))
    for command in ("pnpm test", "npm test", "pnpm run test", "pnpm e2e", "npm run e2e", "yarn test",
                    "vitest", "npx vitest", "pnpm exec vitest", "npm exec vitest", "./node_modules/.bin/vitest",
                    "playwright test", "npx playwright test", "pnpm playwright test", "pnpm typecheck", "echo"):
        assert command in allowed, command


def test_the_builder_is_told_a_refusal_refuses_one_call_and_to_run_the_tests(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    note = builder_bash_note(workspace)
    assert "never means Bash is denied" in note and "`npm test`" in note
    argv = build_claude_cli_args("claude", "P", write_mode="allowed-tools", config={}, workspace=workspace)
    assert argv[argv.index("--append-system-prompt") + 1] == note
    assert "--append-system-prompt" not in build_claude_cli_args("claude", "P", config={})
