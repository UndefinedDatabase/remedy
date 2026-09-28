"""F038 R7 G5 — the red-proof tool. Given a worktree path, it mutates
`packages/orchestration/chat_intent_model.py` (r1-r9) and `packages/orchestration/chat_intent.py`
(r10) inside that worktree, one real behaviour change at a time, and shows that
`tests/orchestration/test_chat_intent_model.py` catches every one of them, then restores each
file byte-identical. Run directly: `python3 -B f038-r7-mutations.py <worktree>`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

MODEL_REL = "packages/orchestration/chat_intent_model.py"
INTENT_REL = "packages/orchestration/chat_intent.py"
TEST_NODE = "tests/orchestration/test_chat_intent_model.py"


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
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf",
         TEST_NODE],
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


#: label, target file (repo-relative), FROM text, TO text.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    ("r1 the model is asked even when the mechanical parse read an action or a question",
     MODEL_REL,
     "    if mechanical.kind != chat_intent.CHAT_INTENT_UNKNOWN:\n"
     "        return mechanical\n",
     "    if False:\n"
     "        return mechanical\n"),
    ("r2 no confidence floor is applied",
     MODEL_REL,
     "reply.confidence < CHAT_MODEL_MIN_CONFIDENCE",
     "False"),
    ("r3 the reply's task id is kept instead of the focused task",
     MODEL_REL,
     '        args["task_id"] = focused_task_id\n',
     "        pass\n"),
    ("r4 a decision id outside the open set is kept",
     MODEL_REL,
     '        args["decision_id"] = args["decision_id"] if args["decision_id"] in '
     'open_decisions else ""\n',
     "        pass\n"),
    ("r5 argument names the verb does not take are kept",
     MODEL_REL,
     "    for name in allowed_names:\n",
     "    for name in reply.args:\n"),
    ("r6 a provider error escapes the parse",
     MODEL_REL,
     "    except PROVIDER_CALL_ERRORS:\n",
     "    except NameError:\n"),
    ("r7 an unset call function asks the model whatever the switch reads",
     MODEL_REL,
     "        call_fn = chat_call_fn(GeneratedChatIntent) if chat_model_written() else "
     "None\n",
     "        call_fn = chat_call_fn(GeneratedChatIntent)\n"),
    ("r8 the call site is asked for the answer schema rather than GeneratedChatIntent",
     MODEL_REL,
     "        call_fn = chat_call_fn(GeneratedChatIntent) if chat_model_written() else "
     "None\n",
     "        call_fn = chat_call_fn() if chat_model_written() else None\n"),
    ("r9 a verb outside the chat's tables is not refused before the arguments are built",
     MODEL_REL,
     "    if verb not in chat_intent.CHAT_VERB_REQUIRED_ARGS:\n"
     "        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)\n"
     "    if not math.isfinite(reply.confidence) or reply.confidence < "
     "CHAT_MODEL_MIN_CONFIDENCE:\n",
     "    if not math.isfinite(reply.confidence) or reply.confidence < "
     "CHAT_MODEL_MIN_CONFIDENCE:\n"),
    ("r10 a card never states its Decision: line",
     INTENT_REL,
     '    if "decision_id" in intent.args:\n'
     '        lines.append(f"Decision: {intent.args[\'decision_id\']}")\n',
     ""),
)


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    targets = {rel: root / rel for rel in (MODEL_REL, INTENT_REL)}
    originals = {rel: path.read_bytes() for rel, path in targets.items()}

    all_caught = True

    label = "control (unmutated, first)"
    code, output = _run_tests(root)
    count, nodes = _failed_count_and_nodes(output)
    print(f"{label}: exit={code} failed={count} nodes={nodes}")
    if code != 0:
        all_caught = False

    for label, rel, from_text, to_text in MUTATIONS:
        target = targets[rel]
        text = target.read_text(encoding="utf-8")
        occurrences = text.count(from_text)
        assert occurrences == 1, f"{label}: FROM text occurs {occurrences} times, not 1"
        mutated = text.replace(from_text, to_text, 1)
        target.write_text(mutated, encoding="utf-8")
        try:
            code, output = _run_tests(root)
        finally:
            target.write_bytes(originals[rel])
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

    restored = all(path.read_bytes() == originals[rel] for rel, path in targets.items())
    print(f"restored byte-identical: {restored}")
    result = bool(all_caught and restored)
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
