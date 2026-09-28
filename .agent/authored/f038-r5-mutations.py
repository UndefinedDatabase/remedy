"""F038 R5 G5 — the red-proof tool. Given a worktree path, it mutates
`packages/orchestration/chat_intent.py` inside that worktree, one real behaviour change
at a time, and shows that `tests/orchestration/test_chat_intent.py` catches every one of
them, then restores the file byte-identical. Run directly: `python3 -B
f038-r5-mutations.py <worktree>`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

TARGET_REL = "packages/orchestration/chat_intent.py"
TEST_NODE = "tests/orchestration/test_chat_intent.py"


def _purge_pycache(root: Path) -> None:
    for current, dirs, _files in os.walk(root):
        if "__pycache__" in dirs:
            shutil.rmtree(Path(current, "__pycache__"))
            dirs.remove("__pycache__")


def _run_tests(root: Path) -> tuple[int, str]:
    _purge_pycache(root)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_NODE],
        cwd=str(root), env=env, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count_and_nodes(output: str) -> tuple[int, list[str]]:
    nodes = [line[len("FAILED "):].split(" - ", 1)[0].strip()
             for line in output.splitlines() if line.startswith("FAILED ")]
    count = 0
    for line in output.splitlines():
        line = line.strip().strip("= ")
        if "failed" not in line:
            continue
        for token in line.split(", "):
            token = token.strip()
            if token.endswith("failed") and token[: -len("failed")].strip().isdigit():
                count = int(token[: -len("failed")].strip())
    return count, nodes


MUTATIONS: tuple[tuple[str, str, str], ...] = (
    ("r1 nothing is ever a question",
     'def _is_question(folded: str) -> bool:\n'
     '    return folded.endswith("?") or bool(_QUESTION_PATTERN.match(folded))\n',
     'def _is_question(folded: str) -> bool:\n'
     '    return False\n'),
    ("r2 a ?-ended text is a question only with a question word",
     '    return folded.endswith("?") or bool(_QUESTION_PATTERN.match(folded))\n',
     '    return folded.endswith("?") and bool(_QUESTION_PATTERN.match(folded))\n'),
    ("r3 a note goes to the job even when a task is focused",
     '        message = folded[note_match.end():]\n'
     '        if focused_task_id:\n'
     '            return _action_intent(\n'
     '                "job.steer", {"task_id": focused_task_id, "message": message})\n'
     '        return _action_intent("chat.send", {"message": message})\n',
     '        message = folded[note_match.end():]\n'
     '        return _action_intent("chat.send", {"message": message})\n'),
    ("r4 nothing is ever missing",
     '    missing = tuple(name for name in required if not raw_args.get(name))\n',
     '    missing = ()\n'),
    ("r5 an unknown request is read as a question",
     '        return _action_intent("job.rerun-subtree", {"task_id": focused_task_id})\n'
     '\n'
     '    return ChatIntent(kind=CHAT_INTENT_UNKNOWN)\n',
     '        return _action_intent("job.rerun-subtree", {"task_id": focused_task_id})\n'
     '\n'
     '    return ChatIntent(kind=CHAT_INTENT_QUESTION)\n'),
    ("r6 a card that is not confirmable still yields a payload",
     '    if not card.confirmable:\n'
     '        raise ChatIntentError(\n'
     '            "this card is not confirmable, so it has no command to send")\n',
     ''),
    ("r7 the nonce is not checked",
     '    if not nonce_is_valid(client_nonce):\n'
     '        raise ChatIntentError("client_nonce is not a usable id")\n',
     ''),
    ("r8 the reason after because is never taken",
     'def _reason_after_because(text: str) -> str:\n'
     '    match = _BECAUSE_PATTERN.search(text)\n'
     '    return text[match.end():].strip() if match else ""\n',
     'def _reason_after_because(text: str) -> str:\n'
     '    return ""\n'),
    ("r9 a note's message is lower-cased",
     '        message = folded[note_match.end():]\n',
     '        message = folded[note_match.end():].lower()\n'),
    ("r10 a leading please is kept",
     '    folded = _fold(text)\n'
     '    if folded[:7].lower() == "please ":\n'
     '        folded = folded[7:]\n',
     '    folded = _fold(text)\n'),
)


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    target = root / TARGET_REL
    original = target.read_bytes()

    all_caught = True

    label, code = "control (unmutated, first)", None
    code, output = _run_tests(root)
    count, nodes = _failed_count_and_nodes(output)
    print(f"{label}: exit={code} failed={count} nodes={nodes}")
    if code != 0:
        all_caught = False

    for label, from_text, to_text in MUTATIONS:
        text = target.read_text(encoding="utf-8")
        occurrences = text.count(from_text)
        assert occurrences == 1, f"{label}: FROM text occurs {occurrences} times, not 1"
        mutated = text.replace(from_text, to_text, 1)
        target.write_text(mutated, encoding="utf-8")
        try:
            code, output = _run_tests(root)
        finally:
            target.write_bytes(original)
        count, nodes = _failed_count_and_nodes(output)
        print(f"{label}: exit={code} failed={count} nodes={nodes}")
        if code == 0:
            all_caught = False

    label = "control (unmutated, last)"
    code, output = _run_tests(root)
    count, nodes = _failed_count_and_nodes(output)
    print(f"{label}: exit={code} failed={count} nodes={nodes}")
    if code != 0:
        all_caught = False

    restored = target.read_bytes() == original
    print(f"restored byte-identical: {restored}")
    result = bool(all_caught and restored)
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
