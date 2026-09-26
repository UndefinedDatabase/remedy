#!/usr/bin/env python3
"""F027 R4 G5 — the red proofs for the replan proposal, its answer and the settled
completion.

Takes a worktree path. For each mutation below: edits the named module INSIDE that worktree
(asserting its FROM text occurs exactly once), purges the worktree's ``__pycache__``
directories, runs ``tests/orchestration/test_veto_proposal.py``,
``tests/orchestration/test_task_veto.py``, ``tests/orchestration/test_task_veto_runner.py``,
``tests/orchestration/test_decision_inbox.py`` and ``tests/cli/test_decision_cmd.py`` from
the worktree's root, restores the bytes byte-identically, and reports the mutation's label,
the run's real exit code, the failed-test count and the failing node ids. Runs an unmutated
control first and last.

Usage:
    python3 -B .agent/authored/f027-r4-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

TASK_VETO = "packages/orchestration/task_veto.py"
VETO_PROPOSAL = "packages/orchestration/veto_proposal.py"
PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
DECISION_CMD = "apps/cli/commands/decision.py"

TEST_RELS = [
    "tests/orchestration/test_veto_proposal.py",
    "tests/orchestration/test_task_veto.py",
    "tests/orchestration/test_task_veto_runner.py",
    "tests/orchestration/test_decision_inbox.py",
    "tests/cli/test_decision_cmd.py",
]

# Each mutation names one real behaviour this round adds: an exact FROM string, replaced by
# an exact TO string. FROM must occur exactly once in the pristine module.
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 a proposal is derived for an answered veto",
        VETO_PROPOSAL,
        "    out: list[Any] = []\n"
        "    for entry in entries:\n"
        "        if entry.request_id in answers:\n"
        "            continue\n"
        "        task = tasks_by_id.get(entry.task_id)\n",
        "    out: list[Any] = []\n"
        "    for entry in entries:\n"
        "        task = tasks_by_id.get(entry.task_id)\n",
    ),
    (
        "m2 the summary drops the reason",
        VETO_PROPOSAL,
        "        summary = (\n"
        "            f\"You vetoed {title} — reason: {entry.reason}.{tail} \"\n"
        "            \"Replan the remaining work as a follow-up job, or accept the reduced "
        "scope.\"\n"
        "        )\n",
        "        summary = (\n"
        "            f\"You vetoed {title}.{tail} \"\n"
        "            \"Replan the remaining work as a follow-up job, or accept the reduced "
        "scope.\"\n"
        "        )\n",
    ),
    (
        "m3 the options are offered in the other order",
        TASK_VETO,
        "REPLAN_PROPOSAL_OPTIONS = (REPLAN_FOLLOW_UP, ACCEPT_REDUCED_SCOPE)\n",
        "REPLAN_PROPOSAL_OPTIONS = (ACCEPT_REDUCED_SCOPE, REPLAN_FOLLOW_UP)\n",
    ),
    (
        "m4 the answer file is published without create_only, so a race overwrites",
        TASK_VETO,
        "        published = _fs.write_file_atomically(\n"
        "            answers_fd, name, _fs.json_bytes(answer.to_json()), create_only=True,\n"
        "            file_mode=_sp.CONTROL_FILE_MODE, error_cls=TaskVetoError, "
        "noun=\"veto answer\")\n",
        "        published = _fs.write_file_atomically(\n"
        "            answers_fd, name, _fs.json_bytes(answer.to_json()), create_only=False,\n"
        "            file_mode=_sp.CONTROL_FILE_MODE, error_cls=TaskVetoError, "
        "noun=\"veto answer\")\n",
    ),
    (
        "m5 a replan saves no follow-up job",
        VETO_PROPOSAL,
        "    follow_up = build_follow_up_job(job, entry, unreachable, job_id=answer.follow_up_job_id)\n"
        "    save_job_plan(follow_up, root)\n",
        "    follow_up = build_follow_up_job(job, entry, unreachable, job_id=answer.follow_up_job_id)\n",
    ),
    (
        "m6 a replan also sets the original job completed and saves it",
        VETO_PROPOSAL,
        "    _ensure_follow_up_job(job, entry, unreachable, answer, root)\n"
        "    _maybe_repair_veto_proposal_answered_event(job, entry, answer)\n",
        "    _ensure_follow_up_job(job, entry, unreachable, answer, root)\n"
        "    if answer.option == _tv.REPLAN_FOLLOW_UP:\n"
        "        from packages.orchestration.pingpong_job import JOB_COMPLETED, save_job_plan\n"
        "        job.state = JOB_COMPLETED\n"
        "        save_job_plan(job, root)\n"
        "    _maybe_repair_veto_proposal_answered_event(job, entry, answer)\n",
    ),
    (
        "m7 the follow-up job's goal leaves out the reason",
        VETO_PROPOSAL,
        "    lines = [\n"
        "        f\"Replan the work vetoed on job {job.job_id[:8]}.\",\n"
        "        f\"Vetoed task: {vetoed_title}\",\n"
        "        f\"Reason: {entry.reason}\",\n"
        "    ]\n",
        "    lines = [\n"
        "        f\"Replan the work vetoed on job {job.job_id[:8]}.\",\n"
        "        f\"Vetoed task: {vetoed_title}\",\n"
        "    ]\n",
    ),
    (
        "m8 a repeated answer writes a second event",
        VETO_PROPOSAL,
        "def _maybe_repair_veto_proposal_answered_event(job: Any, entry: Any, answer: Any) "
        "-> None:\n"
        "    already = _veto_proposal_answered_event_exists(job.job_id, entry.request_id)\n"
        "    if already is not None and not already:\n"
        "        _write_veto_proposal_answered_event(job, entry, answer)\n",
        "def _maybe_repair_veto_proposal_answered_event(job: Any, entry: Any, answer: Any) "
        "-> None:\n"
        "    _write_veto_proposal_answered_event(job, entry, answer)\n",
    ),
    (
        "m9 an option outside the two is recorded",
        VETO_PROPOSAL,
        "    if option not in _tv.REPLAN_PROPOSAL_OPTIONS:\n"
        "        return _refuse(\n"
        "            \"invalid_option\",\n"
        "            f\"option must be one of {', '.join(_tv.REPLAN_PROPOSAL_OPTIONS)}\", "
        "decision_id)\n",
        "",
    ),
    (
        "m10 the settled completion ignores the answers and always completes",
        PINGPONG_JOB,
        "                    if _vid_answer is None:\n"
        "                        _veto_terminal_settled = False\n"
        "                        continue\n",
        "                    if _vid_answer is None:\n"
        "                        continue\n",
    ),
    (
        "m11 the settled completion never completes",
        PINGPONG_JOB,
        "                _veto_terminal_answered_options: dict[str, str] = {}\n"
        "                _veto_terminal_settled = True\n",
        "                _veto_terminal_answered_options: dict[str, str] = {}\n"
        "                _veto_terminal_settled = False\n",
    ),
    (
        "m12 all_done leaves out TASK_VETOED, so a settled run ends as it began",
        PINGPONG_JOB,
        "        all_done = all(\n"
        "            t.status in (TASK_APPLIED, TASK_SKIPPED, TASK_SPLIT, TASK_VETOED)\n"
        "            for t in job.tasks\n"
        "        )\n",
        "        all_done = all(\n"
        "            t.status in (TASK_APPLIED, TASK_SKIPPED, TASK_SPLIT)\n"
        "            for t in job.tasks\n"
        "        )\n",
    ),
    (
        "m13 the CLI route answers with --answer instead of --reason",
        DECISION_CMD,
        "        result = answer_replan_proposal(job, decision_id, str(reason or \"\"), "
        "actor=\"cli\")\n",
        "        result = answer_replan_proposal(\n"
        "            job, decision_id, str(answer[0]) if answer else \"\", actor=\"cli\")\n",
    ),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_tests(root: Path) -> tuple[int, str]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_RELS],
        cwd=str(root), capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count_and_ids(output: str) -> tuple[int, list[str]]:
    ids = sorted(set(re.findall(r"^FAILED (\S+)", output, re.MULTILINE)))
    match = re.search(r"(\d+) failed", output)
    count = int(match.group(1)) if match else 0
    return count, ids


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f027-r4-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    print("--- control run (unmutated, before) ---")
    code, output = _run_tests(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")
    if code != 0:
        print("CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        return 1

    all_caught = True
    all_restored = True

    for label, rel_path, from_text, to_text in MUTATIONS:
        path = root / rel_path
        original = path.read_bytes()
        text = original.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times (expected 1) — aborting")
            return 1
        mutated = text.replace(from_text, to_text, 1)
        path.write_bytes(mutated.encode("utf-8"))
        try:
            code, output = _run_tests(root)
            failed_count, failing_ids = _failed_count_and_ids(output)
            caught = code != 0 and failed_count > 0
            all_caught = all_caught and caught
            tag = "" if caught else " — GREEN, NOT CAUGHT"
            print(f"{label}: exit={code} failed={failed_count} "
                  f"failing_node_ids={failing_ids}{tag}")
        finally:
            path.write_bytes(original)
        restored = path.read_bytes() == original
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored}")

    print("--- control run (unmutated, after) ---")
    code, output = _run_tests(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")

    result = all_caught and all_restored and code == 0
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
