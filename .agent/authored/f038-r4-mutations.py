#!/usr/bin/env python3
"""F038 R4 G5 — the red-proof tool for round 4's model-written chat answer.

For each mutation named below, edits the named module INSIDE a worktree (asserting
its FROM text occurs exactly once), runs the F038 chat-answer test module from the
worktree's own root with that root first on ``PYTHONPATH``, restores the mutated
file's original bytes, and reports one line per mutation. Every mutation must turn
the run red; a mutation that stays green is reported as green, never papered over
(DECISION F038 D5, block ``.remedy-wt/f038-r4/block.md`` gate G5).

Usage: ``python3 -B .agent/authored/f038-r4-mutations.py <worktree-path>``
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TEST_RELPATH = "tests/orchestration/test_chat_answer.py"

#: One mutation per row: a label, the file it edits (relative to the worktree
#: root), the exact FROM text (asserted to occur exactly once before the edit),
#: and the TO text that replaces it. Every mutation is a real behaviour change in
#: ``chat_answer.py`` unless its label says otherwise.
MUTATIONS: list[dict[str, str]] = [
    dict(
        label="q1 the claim check never finds a token missing",
        path="packages/orchestration/chat_answer.py",
        from_text='        if token not in haystack:\n',
        to_text='        if False:\n',
    ),
    dict(
        label="q2 the claim check reads every item of the set instead of the cited ones",
        path="packages/orchestration/chat_answer.py",
        from_text='    claim_problem = _unsupported_claim_problem(sentence, cited_items)\n',
        to_text='    claim_problem = _unsupported_claim_problem(sentence, evidence.items)\n',
    ),
    dict(
        label="q3 with no call function handed in, chat_call_fn() is asked whatever the switch",
        path="packages/orchestration/chat_answer.py",
        from_text=(
            '    if call_fn is _UNSET_CALL_FN:\n'
            '        call_fn = chat_call_fn() if chat_model_written() else None\n'
        ),
        to_text=(
            '    if call_fn is _UNSET_CALL_FN:\n'
            '        call_fn = chat_call_fn()\n'
        ),
    ),
    dict(
        label="q4 chat_call_fn asks the planner role",
        path="packages/orchestration/chat_answer.py",
        from_text='    role_cfg = resolve_role_config("summary")\n',
        to_text='    role_cfg = resolve_role_config("planner")\n',
    ),
    dict(
        label="q5 only KeyError is caught around the call",
        path="packages/orchestration/chat_answer.py",
        from_text='    except PROVIDER_CALL_ERRORS as exc:\n',
        to_text='    except KeyError as exc:\n',
    ),
    dict(
        label="q6 a reply with no supported sentence is kept",
        path="packages/orchestration/chat_answer.py",
        from_text=(
            '    if any(sentence.supported for sentence in checked.sentences):\n'
            '        return checked\n'
            '    return dataclasses.replace(\n'
            '        mechanical_answer(question, evidence),\n'
            '        generator=f"{CHAT_GENERATOR_MECHANICAL}:{CHAT_NO_SUPPORTED_SENTENCE}",\n'
            '    )\n'
        ),
        to_text='    return checked\n',
    ),
    dict(
        label="q7 a fallback's label omits its reason",
        path="packages/orchestration/chat_answer.py",
        from_text=(
            '        generator=f"{CHAT_GENERATOR_MECHANICAL}:{CHAT_NO_SUPPORTED_SENTENCE}",\n'
        ),
        to_text='        generator=CHAT_GENERATOR_MECHANICAL,\n',
    ),
    dict(
        label="q8 the prompt omits the refusal rule",
        path="packages/orchestration/chat_answer.py",
        from_text=(
            '        f"- at most {CHAT_MECHANICAL_MAX_SENTENCES} sentences",\n'
            '        f"- when no item answers the question, reply exactly: '
            '{CHAT_NOT_IN_EVIDENCE}",\n'
            '    ])\n'
        ),
        to_text=(
            '        f"- at most {CHAT_MECHANICAL_MAX_SENTENCES} sentences",\n'
            '    ])\n'
        ),
    ),
    dict(
        label="q9 an outcome that is not ok is not a fallback",
        path="packages/orchestration/chat_answer.py",
        from_text='    if not outcome.ok:\n',
        to_text='    if False:\n',
    ),
    dict(
        label="q10 in config.py, the switch defaults to on",
        path="packages/orchestration/config.py",
        from_text=(
            '    ConfigKeySpec(\n'
            '        key="chat.model_written",\n'
            '        env_var="REMEDY_CHAT_MODEL_WRITTEN",\n'
            '        description=(\n'
            '            "Let the summary model write the grounded chat\'s answers (F038). Off "\n'
            '            "by default: each answer is one summary model call, and a question "\n'
            '            "makes no call the operator did not switch on; with it off, the chat "\n'
            '            "answers from its evidence mechanically."\n'
            '        ),\n'
            '        value_type=bool,\n'
            '        default=False,\n'
            '    ),\n'
        ),
        to_text=(
            '    ConfigKeySpec(\n'
            '        key="chat.model_written",\n'
            '        env_var="REMEDY_CHAT_MODEL_WRITTEN",\n'
            '        description=(\n'
            '            "Let the summary model write the grounded chat\'s answers (F038). Off "\n'
            '            "by default: each answer is one summary model call, and a question "\n'
            '            "makes no call the operator did not switch on; with it off, the chat "\n'
            '            "answers from its evidence mechanically."\n'
            '        ),\n'
            '        value_type=bool,\n'
            '        default=True,\n'
            '    ),\n'
        ),
    ),
]

#: Parses pytest's summary line, e.g. "3 failed, 27 passed in 0.12s".
_FAILED_COUNT_RE = re.compile(r"(\d+) failed")


def _purge_pycache(root: Path) -> None:
    """Remove every ``__pycache__`` directory under `root`, so a stale ``.pyc`` from
    a previous mutation is never what the next run imports."""
    for cache_dir in root.rglob("__pycache__"):
        if cache_dir.is_dir():
            shutil.rmtree(cache_dir)


def _run_tests(root: Path) -> tuple[int, int, list[str]]:
    """Run the F038 chat-answer suite from `root`, that root first on `PYTHONPATH`.

    Returns ``(exit_code, failed_count, failing_node_ids)``.
    """
    _purge_pycache(root)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rfE",
         TEST_RELPATH],
        cwd=str(root), env=env, capture_output=True, text=True,
    )
    output = proc.stdout + proc.stderr
    failed_match = _FAILED_COUNT_RE.search(output)
    failed_count = int(failed_match.group(1)) if failed_match else 0
    node_ids = sorted({
        line.split(" ", 1)[1].split(" - ")[0].strip()
        for line in output.splitlines()
        if line.startswith("FAILED ") or line.startswith("ERROR ")
    })
    return proc.returncode, failed_count, node_ids


def _report(label: str, exit_code: int, failed_count: int, node_ids: list[str]) -> None:
    print(f"{label}: exit={exit_code} failed={failed_count} nodes={node_ids}")


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: f038-r4-mutations.py <worktree-path>", file=sys.stderr)
        raise SystemExit(2)
    root = Path(sys.argv[1]).resolve()

    all_red = True
    restored_byte_identical = True

    exit_code, failed_count, node_ids = _run_tests(root)
    _report("control (before)", exit_code, failed_count, node_ids)
    if exit_code != 0:
        all_red = False

    for mutation in MUTATIONS:
        target = root / mutation["path"]
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        from_text = mutation["from_text"]
        occurrences = original_text.count(from_text)
        assert occurrences == 1, (
            f"{mutation['label']}: FROM text occurs {occurrences} times in "
            f"{mutation['path']}, expected exactly 1"
        )
        mutated_text = original_text.replace(from_text, mutation["to_text"], 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, failed_count, node_ids = _run_tests(root)
        finally:
            target.write_bytes(original)

        if target.read_bytes() != original:
            restored_byte_identical = False

        _report(mutation["label"], exit_code, failed_count, node_ids)
        is_red = exit_code != 0 and failed_count >= 1
        if not is_red:
            print(f"{mutation['label']}: GREEN (not caught)")
            all_red = False

    exit_code, failed_count, node_ids = _run_tests(root)
    _report("control (after)", exit_code, failed_count, node_ids)
    if exit_code != 0:
        all_red = False

    print(f"restored byte-identical: {restored_byte_identical}")
    everything_ok = all_red and restored_byte_identical
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {everything_ok}")


if __name__ == "__main__":
    main()
