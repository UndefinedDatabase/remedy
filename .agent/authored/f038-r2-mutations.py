"""F038 R2 G5 — red-proof tool.

Takes a worktree path. For each mutation, edits `chat_evidence.py` INSIDE that
worktree (asserting its FROM text occurs exactly once), runs
`tests/orchestration/test_chat_evidence.py` from the worktree's root after
purging its `__pycache__` directories, with the worktree's root first on
PYTHONPATH, restores the bytes, and prints one line per mutation: its label,
the exit code, the failed count and the failing node ids. Runs an unmutated
control first and last, and ends with `restored byte-identical: True` and a
final `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>` line.

Usage: python3 -B .agent/authored/f038-r2-mutations.py <worktree-path>
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TEST_SELECTION = [
    "tests/orchestration/test_chat_evidence.py",
]

CHAT_EVIDENCE = "packages/orchestration/chat_evidence.py"

MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "n1 a prompt item's text carries the entry's prompt_text_redacted",
        CHAT_EVIDENCE,
        "        text_line = (\n"
        '            f"Prompt for round {round_number}, {role} ({prompt_kind}): "\n'
        '            f"{tokens_estimated} tokens estimated; provider {provider}; "\n'
        '            f"model {configured_model}"\n'
        "        )\n",
        "        text_line = (\n"
        '            f"Prompt for round {round_number}, {role} ({prompt_kind}): "\n'
        '            f"{tokens_estimated} tokens estimated; provider {provider}; "\n'
        "            f\"model {configured_model} {entry.get('prompt_text_redacted', '')}\"\n"
        "        )\n",
    ),
    (
        "n2 a trace line that parses to something not a dict is not skipped",
        CHAT_EVIDENCE,
        "        if not isinstance(entry, dict):\n"
        "            continue\n",
        "        if False:\n"
        "            continue\n",
    ),
    (
        "n3 the project scope takes every job, linked or not",
        CHAT_EVIDENCE,
        "    jobs = [job for job in all_jobs if str(job.job_id) in linked_ids]\n",
        "    jobs = list(all_jobs)\n",
    ),
    (
        "n4 the linked jobs come oldest first",
        CHAT_EVIDENCE,
        "    jobs = [job for job in all_jobs if str(job.job_id) in linked_ids]\n",
        "    jobs = list(reversed("
        "[job for job in all_jobs if str(job.job_id) in linked_ids]))\n",
    ),
    (
        "n5 a decision's ref is its id alone, without its job",
        CHAT_EVIDENCE,
        '                    "decision", f"{job_id}/{decision.id}",\n',
        '                    "decision", decision.id,\n',
    ),
    (
        "n6 the roadmap is read from Remedy's own repository instead of the project's",
        CHAT_EVIDENCE,
        "        index = build_index(repo_path)\n",
        "        index = build_index()\n",
    ),
    (
        "n7 an in-progress feature reads as the next open feature",
        CHAT_EVIDENCE,
        '    verb = "is in progress" if reason == "in_progress" '
        'else "is the next open feature"\n',
        '    verb = "is the next open feature"\n',
    ),
    (
        "n8 a resolved dossier risk is listed",
        CHAT_EVIDENCE,
        "        for risk in dossier.risks:\n"
        "            if not risk.resolved:\n",
        "        for risk in dossier.risks:\n"
        "            if True:\n",
    ),
    (
        "n9 an unmeasured ledger figure reads 0",
        CHAT_EVIDENCE,
        '    return "unmeasured" if value is None else str(value)\n',
        '    return "0" if value is None else str(value)\n',
    ),
    (
        "n10 the job items come before the decisions",
        CHAT_EVIDENCE,
        "    return [\n"
        "        _project_record_item(project, pid, len(jobs)),\n"
        "        *_project_roadmap_items(project, pid),\n"
        "        *_project_decision_items(jobs, events_by_job_id),\n"
        "        *_project_pattern_items(jobs, events_by_job_id),\n"
        "        *_project_dossier_items(project, pid),\n"
        "        *_project_ledger_items(pid),\n"
        "        *_project_job_items(jobs, pid, events_by_job_id),\n"
        "    ]\n",
        "    return [\n"
        "        _project_record_item(project, pid, len(jobs)),\n"
        "        *_project_roadmap_items(project, pid),\n"
        "        *_project_job_items(jobs, pid, events_by_job_id),\n"
        "        *_project_pattern_items(jobs, events_by_job_id),\n"
        "        *_project_dossier_items(project, pid),\n"
        "        *_project_ledger_items(pid),\n"
        "        *_project_decision_items(jobs, events_by_job_id),\n"
        "    ]\n",
    ),
    (
        "n11 the prompt items come after the diff",
        CHAT_EVIDENCE,
        "    return [\n"
        "        *_record_items(task, task_id),\n"
        "        *_round_items(job, task_id),\n"
        "        *_prompt_trace_items(task, task_id),\n"
        "        *_diff_items(job.job_id, task_id),\n"
        "        *_run_log_items(job.job_id, task_id),\n"
        "    ]\n",
        "    return [\n"
        "        *_record_items(task, task_id),\n"
        "        *_round_items(job, task_id),\n"
        "        *_diff_items(job.job_id, task_id),\n"
        "        *_prompt_trace_items(task, task_id),\n"
        "        *_run_log_items(job.job_id, task_id),\n"
        "    ]\n",
    ),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_tests(root: Path) -> tuple[int, str]:
    _purge_pycache(root)
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(root) + (os.pathsep + existing if existing else "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_SELECTION],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


_FAILED_LINE_RE = re.compile(r"^FAILED (\S+)", re.MULTILINE)
_SUMMARY_FAILED_RE = re.compile(r"(\d+) failed")


def _summarize(output: str) -> tuple[int, list[str]]:
    node_ids = _FAILED_LINE_RE.findall(output)
    match = _SUMMARY_FAILED_RE.search(output)
    failed_count = int(match.group(1)) if match else len(node_ids)
    return failed_count, node_ids


def main() -> None:
    worktree = Path(sys.argv[1]).resolve()
    all_caught = True

    exit_code, output = _run_tests(worktree)
    failed_count, node_ids = _summarize(output)
    print(f"control (before): exit={exit_code} failed={failed_count} nodes={node_ids}")
    if exit_code != 0:
        all_caught = False

    for label, rel_path, from_text, to_text in MUTATIONS:
        target = worktree / rel_path
        original = target.read_text(encoding="utf-8")
        occurrences = original.count(from_text)
        assert occurrences == 1, (
            f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected 1"
        )
        mutated = original.replace(from_text, to_text, 1)
        target.write_text(mutated, encoding="utf-8")
        try:
            exit_code, output = _run_tests(worktree)
            failed_count, node_ids = _summarize(output)
            caught = exit_code != 0 and failed_count > 0
            if not caught:
                all_caught = False
            print(
                f"{label}: exit={exit_code} failed={failed_count} nodes={node_ids} "
                f"caught={caught}"
            )
        finally:
            target.write_text(original, encoding="utf-8")
            restored = target.read_bytes() == original.encode("utf-8")
            print(f"  restored byte-identical: {restored}")
            if not restored:
                all_caught = False

    exit_code, output = _run_tests(worktree)
    failed_count, node_ids = _summarize(output)
    print(f"control (after): exit={exit_code} failed={failed_count} nodes={node_ids}")
    if exit_code != 0:
        all_caught = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught}")


if __name__ == "__main__":
    main()
