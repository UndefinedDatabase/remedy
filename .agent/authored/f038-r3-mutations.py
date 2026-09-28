"""F038 R3 G5 — red-proof tool.

Takes a worktree path. For each mutation, edits the named module INSIDE that
worktree (asserting its FROM text occurs exactly once), runs
`tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py`
from the worktree's root after purging its `__pycache__` directories, with the
worktree's root first on PYTHONPATH, restores the bytes, and prints one line
per mutation: its label, the exit code, the failed count and the failing node
ids. Runs an unmutated control first and last, and ends with `restored
byte-identical: True` and a final `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
<bool>` line.

Usage: python3 -B .agent/authored/f038-r3-mutations.py <worktree-path>
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TEST_SELECTION = [
    "tests/orchestration/test_chat_answer.py",
    "tests/orchestration/test_chat_evidence.py",
]

CHAT_ANSWER = "packages/orchestration/chat_answer.py"
CHAT_EVIDENCE = "packages/orchestration/chat_evidence.py"

MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "p1 a sentence citing nothing reads supported",
        CHAT_ANSWER,
        "    if not citations:\n"
        "        return ChatAnswerSentence(\n"
        '            text=sentence, citations=citations, supported=False, problem="cites no evidence item"\n'
        "        )\n",
        "    if not citations:\n"
        "        return ChatAnswerSentence(\n"
        '            text=sentence, citations=citations, supported=True, problem="cites no evidence item"\n'
        "        )\n",
    ),
    (
        "p2 a citation outside the set is accepted",
        CHAT_ANSWER,
        "    unheld = [number for number in citations if number < 1 or number > item_count]\n",
        "    unheld = []\n",
    ),
    (
        "p3 \"Not in evidence.\" needs a citation",
        CHAT_ANSWER,
        "    if sentence.strip() == CHAT_NOT_IN_EVIDENCE and not citations:\n",
        "    if sentence.strip() == CHAT_NOT_IN_EVIDENCE and citations:\n",
    ),
    (
        "p4 a fragment of citation markers stands as its own sentence",
        CHAT_ANSWER,
        "            if not bare:\n",
        "            if False:\n",
    ),
    (
        "p5 an empty answer has no sentence",
        CHAT_ANSWER,
        "    raw_sentences = split_answer_sentences(text) or [CHAT_NOT_IN_EVIDENCE]\n",
        "    raw_sentences = split_answer_sentences(text)\n",
    ),
    (
        "p6 a keyword matches whole words only",
        CHAT_ANSWER,
        "    return sum(1 for keyword in keywords if any(run.startswith(keyword) for run in runs))\n",
        "    return sum(1 for keyword in keywords if any(run == keyword for run in runs))\n",
    ),
    (
        "p7 on a tied score the higher item number comes first",
        CHAT_ANSWER,
        "    scored.sort(key=lambda triple: (-triple[2], triple[0]))\n",
        "    scored.sort(key=lambda triple: (-triple[2], -triple[0]))\n",
    ),
    (
        "p8 the mechanical answer restates every matching item",
        CHAT_ANSWER,
        "    kept = scored[:CHAT_MECHANICAL_MAX_SENTENCES]\n",
        "    kept = scored\n",
    ),
    (
        "p9 the mechanical answer's sentences are split again",
        CHAT_ANSWER,
        "    sentences = tuple(check_answer_sentence(sentence, evidence) for sentence in raw_sentences)\n"
        "    return ChatAnswer(\n"
        "        scope=evidence.scope, subject=evidence.subject, question=question,\n"
        "        generator=CHAT_GENERATOR_MECHANICAL, sentences=sentences,\n"
        "    )\n",
        "    sentences = tuple(\n"
        "        check_answer_sentence(fragment, evidence)\n"
        "        for sentence in raw_sentences\n"
        "        for fragment in (split_answer_sentences(sentence) or [sentence])\n"
        "    )\n"
        "    return ChatAnswer(\n"
        "        scope=evidence.scope, subject=evidence.subject, question=question,\n"
        "        generator=CHAT_GENERATOR_MECHANICAL, sentences=sentences,\n"
        "    )\n",
    ),
    (
        "p10 the renderer omits the unsupported mark",
        CHAT_ANSWER,
        "    parts = [\n"
        '        sentence.text if sentence.supported else f"{sentence.text} {CHAT_UNSUPPORTED_MARK}"\n'
        "        for sentence in answer.sentences\n"
        "    ]\n",
        "    parts = [sentence.text for sentence in answer.sentences]\n",
    ),
    (
        "p11 stopwords count as keywords",
        CHAT_ANSWER,
        "        if len(run) < CHAT_KEYWORD_MIN_CHARS or run in CHAT_QUESTION_STOPWORDS or run in seen:\n",
        "        if len(run) < CHAT_KEYWORD_MIN_CHARS or run in seen:\n",
    ),
    (
        "p12 in chat_evidence.py, the run-id check calls match again",
        CHAT_EVIDENCE,
        "    if not isinstance(run_id, str) or not _RUN_ID_RE.fullmatch(run_id):\n",
        "    if not isinstance(run_id, str) or not _RUN_ID_RE.match(run_id):\n",
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
