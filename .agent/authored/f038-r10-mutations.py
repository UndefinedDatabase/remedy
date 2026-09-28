"""F038 R10 C4 — the round's mutation tool (G5).

Takes a worktree path. For each mutation below, edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), runs
`tests/ui_server/test_chat_route.py`, `tests/orchestration/test_chat_turn.py` and
`tests/cli/test_chat_ask.py` from the worktree's root — after purging its
`__pycache__` directories, with the worktree's root first on `PYTHONPATH` — restores
the bytes, and prints one line per mutation: its label, the exit code, the failed
count and the failing node ids, read from the `FAILED` lines `-rf` prints. Runs an
unmutated control first and last.

Usage: `python3 -B .agent/authored/f038-r10-mutations.py <worktree-path>`
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

UI_SERVER = "packages/orchestration/ui_server.py"
CHAT_TURN = "packages/orchestration/chat_turn.py"
UI_PY = "apps/cli/commands/ui.py"
CHAT_CMD = "apps/cli/commands/chat_cmd.py"

TEST_ARGS = (
    "tests/ui_server/test_chat_route.py",
    "tests/orchestration/test_chat_turn.py",
    "tests/cli/test_chat_ask.py",
)

#: (label, repo-relative path, FROM text, TO text). Each is a real behaviour
#: change, in the file the label names.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    ("m1 (ui_server.py) a blank text runs a turn", UI_SERVER,
     "    if not text.strip():\n"
     '        return {"available": False, "reason": "empty_text"}',
     "    if False:\n"
     '        return {"available": False, "reason": "empty_text"}'),
    ("m2 (ui_server.py) a ChatTurnError is not caught", UI_SERVER,
     '    except ChatTurnError:\n'
     '        return {"available": False, "reason": "unknown_task"}',
     '    except KeyError:\n'
     '        return {"available": False, "reason": "unknown_task"}'),
    ("m3 (ui_server.py) the task is dropped", UI_SERVER,
     "task_id=task_id.strip()",
     'task_id=""'),
    ("m4 (ui_server.py) the task is not stripped", UI_SERVER,
     "task_id.strip()",
     "task_id"),
    ("m5 (chat_turn.py) the view numbers evidence from 0", CHAT_TURN,
     "enumerate(evidence.items, start=1)",
     "enumerate(evidence.items, start=0)"),
    ("m6 (chat_turn.py) every sentence is reported supported", CHAT_TURN,
     '"supported": sentence.supported, "problem": sentence.problem}',
     '"supported": True, "problem": sentence.problem}'),
    ("m7 (chat_turn.py) a card's args come back empty", CHAT_TURN,
     '"args": dict(card.args),',
     '"args": {},'),
    ("m8 (ui.py) the lookup returns the oldest session", UI_PY,
     'return max(candidates, key=lambda s: s.get("started_at", ""))',
     'return min(candidates, key=lambda s: s.get("started_at", ""))'),
    ("m9 (chat_cmd.py) every send uses one fixed nonce", CHAT_CMD,
     'client_nonce="chat-" + secrets.token_hex(8),',
     'client_nonce="chat-fixed",'),
    ("m10 (chat_cmd.py) the text form's evidence lines are dropped", CHAT_CMD,
     '        print(f"[{number}] {item.kind} {item.ref}")',
     "        pass"),
    ("m11 (chat_cmd.py) --task is not stripped", CHAT_CMD,
     'turn = run_chat_turn(job, text, task_id=(task_id or "").strip())',
     'turn = run_chat_turn(job, text, task_id=(task_id or ""))'),
    ("m12 (chat_cmd.py) the --json answer's question is blanked", CHAT_CMD,
     "emit_ok(job_id=job_id, **chat_turn_view(turn))",
     'emit_ok(job_id=job_id, **{**chat_turn_view(turn), "question": ""})'),
)


def _purge_pycache(root: str) -> None:
    for current, dirs, _files in os.walk(root):
        if "__pycache__" in dirs:
            shutil.rmtree(os.path.join(current, "__pycache__"), ignore_errors=True)
            dirs.remove("__pycache__")


def _run_tests(root: str) -> tuple[int, list[str]]:
    """Run the round's test selection from `root`. Returns (exit code, FAILED lines)."""
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
        print("usage: f038-r10-mutations.py <worktree-path>", file=sys.stderr)
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
