"""R-1351 end to end: a project test that goes red after a passing review gets one budgeted repair.

The case is the 2026-10-18 local calibration's c2, made deterministic: the lab repository (a Node
project whose test command is `node --test`), the lab's add order verbatim, a reviewer that passes
every diff, and a scripted builder whose first answer imports `strictEqual` from `node:test` (it
is `node:assert`'s) and whose repair answer imports it correctly only when the failing test's own
diagnostic is in its prompt. The project's tests really run unless a case replaces the spawn to
stand for a broken host (a refused sandbox, a missing tool).
"""
from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

from tests.orchestration.scale_harness import FakePlannerService, commit_repository
from tests.orchestration.scale_matrix import LAB, LAB_ADD_ORDER

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="the lab project needs node")

FIXED_CALC = "export function add(a, b) {\n  return a + b;\n}\n"
#: The calibration's real defect: `strictEqual` is not an export of `node:test`.
BROKEN_TEST = ('import { test, strictEqual } from "node:test";\nimport { add } from "../src/calc.js";\n\n'
               'test("add adds", () => {\n  strictEqual(add(2, 3), 5);\n});\n')
FIXED_TEST = ('import { test } from "node:test";\nimport { strictEqual } from "node:assert";\n'
              'import { add } from "../src/calc.js";\n\n'
              'test("add adds", () => {\n  strictEqual(add(2, 3), 5);\n});\n')
#: What the scripted builder needs to see before it writes the correct import.
DIAGNOSTIC = "does not provide an export named 'strictEqual'"


def _walk(tmp_path: Path, *, repair_fixes: bool = True, extra_argv: tuple[str, ...] = (),
          on_first_review: Any = None, spawn_exit: int | None = None, sandbox_refuses: bool = False,
          provider_calls_seen: int | None = None, repair_writes: dict[str, str] | None = None) -> dict[str, Any]:
    """One `remedy do` walk of the lab add order; the answer, the job, its rounds and builder prompts."""
    from apps.cli.grouped import main
    from packages.orchestration import pingpong_loop
    from packages.orchestration.pingpong_provider_fake import FakeProvider

    repo = commit_repository(tmp_path / "work", LAB)
    prompts: list[str] = []
    reviews: list[str] = []
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        patch.chdir(repo)
        FakePlannerService(target="src/calc.js").install(patch)
        build = FakeProvider.build

        def recorded_build(self, prompt, **kwargs):
            prompts.append(prompt)
            return build(self, prompt, **kwargs)

        def scripted_changes(staging: Path, output: Any, goal: str) -> None:
            (staging / "src").mkdir(exist_ok=True)
            (staging / "test").mkdir(exist_ok=True)
            (staging / "src/calc.js").write_text(FIXED_CALC)
            fixed = repair_fixes and len(prompts) > 1 and DIAGNOSTIC in prompts[-1]
            (staging / "test/calc.test.js").write_text(FIXED_TEST if fixed else BROKEN_TEST)
            output.files_changed = ["src/calc.js", "test/calc.test.js"]
            for name, text in (repair_writes or {}).items() if len(prompts) > 1 else ():
                (staging / name).write_text(text)      # a repair answer that reaches past the order
                output.files_changed.append(name)

        review = FakeProvider.review

        def passing_review(self, prompt, **kwargs):
            reviews.append(prompt)
            if len(reviews) == 1 and on_first_review is not None:
                on_first_review()
            out = review(self, prompt, **kwargs)      # keeps the call's recorded input for the manifest
            out.verdict, out.findings, out.summary = "pass", [], "looks right"
            return out

        patch.setattr(FakeProvider, "build", recorded_build)
        patch.setattr(pingpong_loop, "_apply_fake_builder_changes", scripted_changes)
        patch.setattr(FakeProvider, "review", passing_review)
        if spawn_exit is not None:
            from packages.orchestration import dod_runners
            from packages.orchestration.exec_guard import TRIPPED_LIMIT_ATTR

            def broken_host(cmd, *, timeout_sec, cwd, env_overlay=None):
                done = subprocess.CompletedProcess(list(cmd), spawn_exit, b"", b"sh: 1: node: not found\n")
                if sandbox_refuses:
                    setattr(done, TRIPPED_LIMIT_ATTR, "sandbox_unavailable")
                return done
            patch.setattr(dod_runners, "run_guarded_dod_process_command", broken_host)
        if provider_calls_seen is not None:
            # The fake provider's calls are not counted (budget_guard); this stands for real ones.
            from dataclasses import replace

            from packages.orchestration import budget_guard
            collect = budget_guard.collect_counters_from_actuals
            patch.setattr(budget_guard, "collect_counters_from_actuals", lambda *a, **k: replace(
                collect(*a, **k), provider_calls=provider_calls_seen, unmeasured_call_count=provider_calls_seen))
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
            main(["do", LAB_ADD_ORDER, "--repo", ".", "--builder-provider", "fake",
                  "--reviewer-provider", "fake", "--json", "--no-ui", "--run-unattended", *extra_argv])
        data = json.loads(out.getvalue())
        from packages.orchestration.pingpong_job import load_job_plan
        from packages.orchestration.pingpong_loop import load_run
        [job] = [load_job_plan(j) for j in data["job_ids"]]
        runs = [load_run(t.run_id) or {} for t in job.tasks if t.run_id]
    return {"data": data, "job": job, "prompts": prompts, "repo": repo,
            "rounds": [r for run in runs for r in run.get("rounds", [])],
            "decisions": [d for run in runs for d in (run.get("repair_loop") or {}).get("decisions", [])],
            "staged": sorted({f for run in runs for f in run.get("staged_files", [])}),
            "verification": [j["verification"] for j in data["jobs"]][0]}


def _state(job: Any) -> str:
    return str(getattr(job.state, "value", job.state))


def test_c2_red_tests_after_a_passing_review_get_one_repair_that_turns_them_green(tmp_path):
    walk = _walk(tmp_path)
    prompts = walk["prompts"]

    # The first verification really failed, and its diagnostic reached the repair prompt.
    assert len(prompts) == 2
    assert DIAGNOSTIC not in prompts[0] and DIAGNOSTIC in prompts[1]
    assert [r["test_passed"] for r in walk["rounds"]] == [False, True]
    # The corrected implementation passes the project's tests, and the job's own gate agrees.
    assert walk["verification"]["status"] == "passed", walk["verification"]
    assert _state(walk["job"]) == "completed"
    # Only the order's two files changed, and nothing reached the repository: apply stays manual.
    assert walk["staged"] == ["src/calc.js", "test/calc.test.js"]
    assert (walk["repo"] / "src/calc.js").read_text() == LAB["src/calc.js"]
    assert not (walk["repo"] / "test/calc.test.js").exists()


def test_an_unchanged_failure_is_never_fed_to_a_second_repair(tmp_path):
    walk = _walk(tmp_path, repair_fixes=False)

    assert len(walk["prompts"]) == 2      # one repair, never a third build on the same failure
    assert [r["test_passed"] for r in walk["rounds"]] == [False, False]
    assert walk["decisions"][-1]["reason"] == "test_failure_unchanged"
    assert _state(walk["job"]) == "blocked"
    assert walk["verification"]["status"] == "failed"


def test_no_repair_starts_after_the_job_is_cancelled(tmp_path):
    def cancel():
        from packages.orchestration.job_cancel import cancel_job
        from packages.orchestration.pingpong_job import list_job_plans
        [job] = list_job_plans()
        cancel_job(job, reason="operator cancelled", source="test")

    walk = _walk(tmp_path, on_first_review=cancel)

    assert len(walk["prompts"]) == 1
    assert _state(walk["job"]) == "cancelled"


def test_no_repair_starts_when_the_remaining_budget_cannot_pay_one_round(tmp_path):
    # Two calls spent of three: a repair round needs a builder and a reviewer call.
    walk = _walk(tmp_path, extra_argv=("--max-provider-calls", "3"), provider_calls_seen=2)

    assert len(walk["prompts"]) == 1
    assert walk["decisions"][-1]["reason"] == "test_failed_repair_budget_insufficient"
    assert _state(walk["job"]) == "blocked"


@pytest.mark.parametrize(("spawn_exit", "sandbox_refuses", "reason"),
                         [(126, True, "sandbox_unavailable"), (127, False, "tool_unavailable")],
                         ids=["sandbox-refused", "tool-missing"])
def test_a_test_that_never_started_is_not_run_and_never_repaired(tmp_path, spawn_exit, sandbox_refuses, reason):
    walk = _walk(tmp_path, spawn_exit=spawn_exit, sandbox_refuses=sandbox_refuses)

    assert len(walk["prompts"]) == 1        # the code was never blamed for a host that ran no test
    assert [r["test_passed"] for r in walk["rounds"]] == [None]
    assert reason in walk["rounds"][0]["test_summary"]
    assert walk["verification"]["status"] == "not_run", walk["verification"]
    assert _state(walk["job"]) == "blocked"     # required tests that did not run are no pass


def test_a_repair_round_stays_inside_the_files_the_order_names(tmp_path):
    """The lab order says "Ändere keine anderen Dateien": a repair answer that also rewrites another
    file is refused like any round's, so the job blocks and nothing of it waits for an apply."""
    walk = _walk(tmp_path, repair_writes={"src/format.js": "export function normalizeName(i) { return i; }\n"})

    assert [r["test_passed"] for r in walk["rounds"]] == [False, True]     # the repair itself went green
    assert _state(walk["job"]) == "blocked"
    assert walk["job"].tasks[-1].error.startswith("unrequested_file_changed: the change touched src/format.js")
    assert (walk["repo"] / "src/format.js").read_text() == LAB["src/format.js"]


def test_a_repair_round_cannot_pass_by_rewriting_the_test_command(tmp_path):
    """A repair that edits package.json's test script never runs as its own check: not run, blocked."""
    cheat = '{"name": "remedy-lab", "type": "module", "scripts": {"test": "exit 0"}}\n'
    walk = _walk(tmp_path, repair_fixes=False, repair_writes={"package.json": cheat})

    assert [r["test_passed"] for r in walk["rounds"]] == [False, None]
    assert "test_command_changed" in walk["rounds"][-1]["test_summary"]
    assert walk["verification"]["status"] == "not_run" and _state(walk["job"]) == "blocked"
    assert (walk["repo"] / "package.json").read_text() == LAB["package.json"]


def test_a_refused_repair_reads_review_not_passed_in_the_story(tmp_path, monkeypatch):
    """R-1367: the story a client reads names why the job ended; a change Remedy's own file check
    refused read `unknown`, although the release matrix of 1.21 promised `review_not_passed`."""
    from packages.orchestration.client_story import job_client_story

    walk = _walk(tmp_path, repair_writes={"src/format.js": "export function normalizeName(i) { return i; }\n"})
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    story = job_client_story(str(walk["job"].job_id), walk["job"])

    assert story["state"] == "failed"
    assert story["state_detail"]["reason"] == {"key": "review_not_passed", "args": {"rounds": 2}}
    # R-1331 (DECISION F307 D22): a job a run left blocked at a task that ended blocked offers its retry.
    assert (story["next"]["action"], story["end"]["action"]) == ("retry", "abandon")
