"""F038 R9 C4 — the round's mutation tool (G5).

Takes a worktree path. For each mutation below, edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), runs
`tests/cli/test_chat_ask.py` and `tests/orchestration/test_chat_turn.py` from the
worktree's root — after purging its `__pycache__` directories, with the worktree's
root first on `PYTHONPATH` — restores the bytes, and prints one line per mutation:
its label, the exit code, the failed count and the failing node ids, read from the
`FAILED` lines `-rf` prints. Runs an unmutated control first and last.

Usage: `python3 -B .agent/authored/f038-r9-mutations.py <worktree-path>`
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

CHAT_CMD = "apps/cli/commands/chat_cmd.py"
UI_PY = "apps/cli/commands/ui.py"
CHAT_TURN = "packages/orchestration/chat_turn.py"

TEST_ARGS = (
    "tests/cli/test_chat_ask.py",
    "tests/orchestration/test_chat_turn.py",
)

#: (label, repo-relative path, FROM text, TO text). Each is a real behaviour
#: change, in `chat_cmd.py` unless the label names its own file.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    ("r1 --yes is ignored", CHAT_CMD,
     "elif not yes and not _chat_stdin_is_a_tty():",
     "elif not _chat_stdin_is_a_tty():"),
    ("r2 a card is sent with neither --yes nor a terminal", CHAT_CMD,
     "elif not yes and not _chat_stdin_is_a_tty():",
     "elif False:"),
    ("r3 a card that is not confirmable is sent", CHAT_CMD,
     "    if not card.confirmable:\n        not_sent_reason = \"the card is not confirmable\"",
     "    if False:\n        not_sent_reason = \"the card is not confirmable\""),
    ("r4 an answer other than y sends", CHAT_CMD,
     'confirmed = answer.strip().lower() in ("y", "yes")',
     "confirmed = True"),
    ("r5 (ui.py) the lookup ignores the job id", UI_PY,
     'if s.get("job_id") == job_id and _is_pid_alive(s.get("pid", 0))',
     'if _is_pid_alive(s.get("pid", 0))'),
    ("r6 (ui.py) the lookup ignores a dead pid", UI_PY,
     'if s.get("job_id") == job_id and _is_pid_alive(s.get("pid", 0))',
     'if s.get("job_id") == job_id'),
    ("r7 a refused card exits 0", CHAT_CMD,
     "json_output=json_output, exit_code=1, job_id=job.job_id,",
     "json_output=json_output, exit_code=0, job_id=job.job_id,"),
    ("r8 no cockpit exits 0", CHAT_CMD,
     '                fail(\n'
     '                    "cockpit_not_running",\n'
     '                    f"No cockpit is running for job {job.job_id}. Start one with: "\n'
     '                    f"remedy ui start {job.job_id}.",\n'
     '                    json_output=json_output, exit_code=3, job_id=job.job_id,\n'
     '                )',
     '                fail(\n'
     '                    "cockpit_not_running",\n'
     '                    f"No cockpit is running for job {job.job_id}. Start one with: "\n'
     '                    f"remedy ui start {job.job_id}.",\n'
     '                    json_output=json_output, exit_code=0, job_id=job.job_id,\n'
     '                )'),
    ("r9 a ChatTurnError is not caught", CHAT_CMD,
     "    try:\n"
     "        turn = run_chat_turn(job, text, task_id=(task_id or \"\").strip())\n"
     "    except ChatTurnError as exc:\n"
     "        fail(\"invalid_task\", f\"The turn was not run: {exc}.\", json_output=json_output,\n"
     "             exit_code=2, job_id=job.job_id)\n",
     "    turn = run_chat_turn(job, text, task_id=(task_id or \"\").strip())\n"),
    ("r10 (chat_turn.py) a handed-in answer_call_fn is dropped (R-1093)", CHAT_TURN,
     'answer_kwargs["call_fn"] = answer_call_fn',
     "pass"),
)


def _purge_pycache(root: str) -> None:
    for current, dirs, _files in os.walk(root):
        if "__pycache__" in dirs:
            shutil.rmtree(os.path.join(current, "__pycache__"), ignore_errors=True)
            dirs.remove("__pycache__")


def _run_tests(root: str) -> tuple[int, list[str]]:
    """Run the two test files from `root`. Returns (exit code, FAILED lines)."""
    _purge_pycache(root)
    env = dict(os.environ)
    env["PYTHONPATH"] = root + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf",
         *TEST_ARGS],
        cwd=root, env=env, capture_output=True, text=True,
    )
    output = proc.stdout + proc.stderr
    failed_lines = [line for line in output.splitlines() if line.startswith("FAILED ")]
    return proc.returncode, failed_lines


def _node_ids(failed_lines: list[str]) -> list[str]:
    ids = []
    for line in failed_lines:
        rest = line[len("FAILED "):]
        node_id = rest.split(" - ", 1)[0].strip()
        ids.append(node_id)
    return ids


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f038-r9-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = os.path.abspath(sys.argv[1])

    all_caught = True

    code, failed = _run_tests(root)
    print(f"control (before): exit={code} failed={len(failed)} nodes={_node_ids(failed)}")
    if code != 0:
        all_caught = False

    for label, rel_path, from_text, to_text in MUTATIONS:
        path = os.path.join(root, rel_path)
        with open(path, encoding="utf-8") as f:
            original = f.read()
        occurrences = original.count(from_text)
        assert occurrences == 1, (
            f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected exactly 1"
        )
        mutated = original.replace(from_text, to_text, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(mutated)
        try:
            code, failed = _run_tests(root)
        finally:
            with open(path, "w", encoding="utf-8") as f:
                f.write(original)
        with open(path, encoding="utf-8") as f:
            restored = f.read()
        byte_identical = restored == original
        node_ids = _node_ids(failed)
        caught = code != 0 and len(failed) >= 1
        if not caught or not byte_identical:
            all_caught = False
        print(f"{label}: exit={code} failed={len(failed)} nodes={node_ids} "
              f"restored byte-identical: {byte_identical}")

    code, failed = _run_tests(root)
    print(f"control (after): exit={code} failed={len(failed)} nodes={_node_ids(failed)}")
    if code != 0:
        all_caught = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught}")
    return 0 if all_caught else 1


if __name__ == "__main__":
    raise SystemExit(main())
