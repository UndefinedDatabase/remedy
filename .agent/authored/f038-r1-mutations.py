"""F038 R1 G5 — red-proof tool.

Takes a worktree path. For each mutation, edits the named module INSIDE that
worktree (asserting its FROM text occurs exactly once), runs the pinned test
selection from the worktree's root with that worktree's root first on
PYTHONPATH, restores the bytes, and prints one line per mutation: its label,
the exit code, the failed count and the failing node ids. Runs an unmutated
control first and last, and ends with `restored byte-identical: True` and a
final `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>` line.

Usage: python3 -B .agent/authored/f038-r1-mutations.py <worktree-path>
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
    "tests/orchestration/test_diff_view_source.py",
    "tests/orchestration/test_final_verifier.py",
]

DIFF_VIEW_SOURCE = "packages/orchestration/diff_view_source.py"
FINAL_VERIFIER = "packages/orchestration/final_verifier.py"
CHAT_EVIDENCE = "packages/orchestration/chat_evidence.py"

MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 diff_view_source.py lists T<digits> runs only again",
        DIFF_VIEW_SOURCE,
        'SAFE_TASK_RUN_ID_RE = re.compile(r"^(?:T\\d{3,}|[0-9a-f]{16})$")',
        'SAFE_TASK_RUN_ID_RE = re.compile(r"^T\\d{3,}$")',
    ),
    (
        "m2 final_verifier.py lists T<digits> runs only again",
        FINAL_VERIFIER,
        '_SAFE_TASK_ID_RE = re.compile(r"^(?:T\\d{3,}|[0-9a-f]{16})$")',
        '_SAFE_TASK_ID_RE = re.compile(r"^T\\d{3,}$")',
    ),
    (
        "m3 the composer keeps every item whatever the cap",
        CHAT_EVIDENCE,
        "        if estimate > token_cap:\n            break\n"
        "        kept.append(item)\n        tokens_estimated = estimate\n",
        "        if False:\n            break\n"
        "        kept.append(item)\n        tokens_estimated = estimate\n",
    ),
    (
        "m4 an item's text is not redacted",
        CHAT_EVIDENCE,
        "    redacted = redact_text(text)\n",
        "    redacted = text\n",
    ),
    (
        "m5 the run-log events come oldest first",
        CHAT_EVIDENCE,
        "        for event in reversed(events)\n",
        "        for event in events\n",
    ),
    (
        "m6 an event naming its task only under metadata is not the task's",
        CHAT_EVIDENCE,
        '    top_level = event.get("task_id")\n'
        "    if top_level is not None:\n"
        "        return top_level\n"
        '    metadata = event.get("metadata")\n'
        '    return metadata.get("task_id") if isinstance(metadata, dict) else None\n',
        '    top_level = event.get("task_id")\n'
        "    if top_level is not None:\n"
        "        return top_level\n"
        "    return None\n",
    ),
    (
        "m7 the task is found by a prefix of its id",
        CHAT_EVIDENCE,
        '(t for t in (getattr(job, "tasks", None) or []) if str(t.task_id) == task_id),',
        '(t for t in (getattr(job, "tasks", None) or [])'
        " if str(t.task_id).startswith(task_id)),",
    ),
    (
        "m8 an over-long text is not cut",
        CHAT_EVIDENCE,
        "    if len(folded) > CHAT_ITEM_TEXT_MAX_CHARS:\n"
        '        folded = folded[: CHAT_ITEM_TEXT_MAX_CHARS - 1] + "…"\n',
        "    if False:\n"
        '        folded = folded[: CHAT_ITEM_TEXT_MAX_CHARS - 1] + "…"\n',
    ),
    (
        "m9 the composer accepts a malformed item",
        CHAT_EVIDENCE,
        "        problems = chat_item_problems(item)\n"
        "        if problems:\n"
        '            raise ChatEvidenceError(f"item {index}: {\'; \'.join(problems)}")\n',
        "        problems = chat_item_problems(item)\n"
        "        if False:\n"
        '            raise ChatEvidenceError(f"item {index}: {\'; \'.join(problems)}")\n',
    ),
    (
        "m10 the diff is read at job scope instead of the task's",
        CHAT_EVIDENCE,
        "    view = build_diff_view(resolve_job_evidence_dir(job_id), task_id=task_id)\n",
        "    view = build_diff_view(resolve_job_evidence_dir(job_id))\n",
    ),
    (
        "m11 a test_passed that is neither True nor False reads failed",
        CHAT_EVIDENCE,
        '    if test_passed is True:\n        return "passed"\n'
        '    if test_passed is False:\n        return "failed"\n'
        "    return CHAT_NOT_RECORDED\n",
        '    if test_passed is True:\n        return "passed"\n'
        '    return "failed"\n',
    ),
    (
        "m12 omitted is always 0",
        CHAT_EVIDENCE,
        "    omitted = len(items) - len(kept)\n",
        "    omitted = 0\n",
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
