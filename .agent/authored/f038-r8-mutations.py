"""F038 R8 G5 — the red-proof tool. Given a worktree path, it mutates
`packages/orchestration/chat_turn.py` (r1-r6) and `packages/orchestration/chat_intent_model.py`
(r7-r8) inside that worktree, one real behaviour change at a time, and shows that
`tests/orchestration/test_chat_turn.py` and `tests/orchestration/test_chat_intent_model.py`
catch every one of them, then restores each file byte-identical. Run directly:
`python3 -B f038-r8-mutations.py <worktree>`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

TURN_REL = "packages/orchestration/chat_turn.py"
MODEL_REL = "packages/orchestration/chat_intent_model.py"
TEST_NODES = (
    "tests/orchestration/test_chat_turn.py",
    "tests/orchestration/test_chat_intent_model.py",
)


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
         *TEST_NODES],
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
    ("r1 a task id that names no task of the job is not refused",
     TURN_REL,
     "    if task_id and task_id not in {str(task.task_id) for task in job.tasks}:\n",
     "    if False:\n"),
    ("r2 the parse is handed no open decisions",
     TURN_REL,
     "        open_decision_ids=chat_open_decision_ids(job),\n",
     "        open_decision_ids=(),\n"),
    ("r3 every inbox card's id is listed, answerable or not",
     TURN_REL,
     '        card["id"] for card in inbox["decisions"] '
     'if card.get("answerable_by_decision_resolve")\n',
     '        card["id"] for card in inbox["decisions"]\n'),
    ("r4 a question with a focused task is answered from the project scope",
     TURN_REL,
     "    if task_id:\n        evidence = node_evidence_set(job, task_id)\n    else:\n",
     "    if False:\n        evidence = node_evidence_set(job, task_id)\n    else:\n"),
    ("r5 an action is answered as if it were a question",
     TURN_REL,
     "    if intent.kind != CHAT_INTENT_QUESTION:\n",
     "    if False:\n"),
    ("r6 with no registered project, project_evidence_set is called with None",
     TURN_REL,
     "        evidence = (\n"
     "            project_evidence_set(project)\n"
     "            if project is not None\n"
     '            else compose_chat_evidence(CHAT_SCOPE_PROJECT, "", [])\n'
     "        )\n",
     "        evidence = project_evidence_set(project)\n"),
    ("r7 a confidence that is not a finite number is kept (R-1092)",
     MODEL_REL,
     "not math.isfinite(reply.confidence) or ",
     ""),
    ("r8 argument values are not stripped (R-1092)",
     MODEL_REL,
     'value.strip() if isinstance(value, str) else ""',
     'value if isinstance(value, str) else ""'),
)


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    targets = {rel: root / rel for rel in (TURN_REL, MODEL_REL)}
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
