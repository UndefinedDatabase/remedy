#!/usr/bin/env python3
"""F035 R3 G5 — the round's red-proof tool (DECISION F035 D3).

Usage: ``python3 -B .agent/authored/f035-r3-mutations.py <worktree-path>``.

Takes the path of a disposable worktree, and for each mutation below: reads the named
file INSIDE that worktree, asserts its FROM text occurs exactly once, writes the TO
text in its place, purges every ``__pycache__`` directory under the worktree, runs the
round's test selection from the worktree's own root, restores the file's ORIGINAL bytes
(never a reversed edit — the saved original is written back verbatim), and prints one
line naming the mutation, its exit code, its failed-test count and its failing node ids.
An unmutated control run brackets the twelve mutations, first and last, and the tool
ends by stating whether every mutated file came back byte-identical to what it read
before editing, and whether every mutation was caught.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TEST_SELECTION = (
    "tests/orchestration/test_ownership_phrases.py",
    "tests/orchestration/test_pingpong_job_ownership.py",
    "tests/orchestration/test_job_digest.py",
    "tests/orchestration/test_task_veto_runner.py",
)

OWNERSHIP_PHRASES = "packages/orchestration/ownership_phrases.py"
PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
JOB_DIGEST = "packages/orchestration/job_digest.py"

MUTATIONS = [
    ("m1", OWNERSHIP_PHRASES,
     "an unattended action's phrase drops (auto-approved via --yes)",
     '        return "You (auto-approved via --yes)"',
     '        return "You"'),
    ("m2", OWNERSHIP_PHRASES,
     "the default policy's phrase drops (you accepted at plan approval)",
     '        return "The default policy (you accepted at plan approval)"',
     '        return "The default policy"'),
    ("m3", OWNERSHIP_PHRASES,
     "a browser phrase leaves out its token number",
     '        return f"You (browser, token #{token_number})"',
     '        return "You (browser)"'),
    ("m4", OWNERSHIP_PHRASES,
     "a reason is cut to its first 20 characters",
     '        return f" — reason: “{text}”"',
     '        return f" — reason: “{text[:20]}”"'),
    ("m5", OWNERSHIP_PHRASES,
     "an action with no template renders \"\" instead of raising",
     '    raise OwnershipError(f"no ownership sentence template for action {action!r}")',
     '    return ""'),
    ("m6", OWNERSHIP_PHRASES,
     "the task phrase ignores the title",
     "    if title and title != task_id:",
     "    if False and title and title != task_id:"),
    ("m7", OWNERSHIP_PHRASES,
     "the reason clause is printed for an empty reason",
     "    if text:",
     "    if True:"),
    ("m8", PINGPONG_JOB,
     "the section header is printed for a job with no entry",
     "        if sentences:",
     "        if True:"),
    ("m9", PINGPONG_JOB,
     "the per-task Vetoed by line is printed again",
     '        if t.error:\n'
     '            lines.append(f"      Error: {t.error}")\n'
     '        for note in steering_map.get(t.task_id, []):',
     '        if t.error:\n'
     '            lines.append(f"      Error: {t.error}")\n'
     '        veto_info = _task_veto_report_map(job).get(t.task_id)\n'
     '        if veto_info is not None:\n'
     '            lines.append(\n'
     '                f"      Vetoed by {veto_info.get(\'actor\', \'\')}: "\n'
     '                f"{veto_info.get(\'reason\', \'\')}"\n'
     '            )\n'
     '        for note in steering_map.get(t.task_id, []):'),
    ("m10", PINGPONG_JOB,
     "a ledger error adds no line to the report",
     '    except (OwnershipError, OSError) as exc:\n'
     '        lines.append(f"Ownership: the ledger could not be read — {exc}")\n'
     '        lines.append("")',
     '    except (OwnershipError, OSError):\n'
     '        pass'),
    ("m11", JOB_DIGEST,
     "ownership is [] for a job with entries",
     "    titles = {t.task_id: t.title for t in job.tasks}\n"
     "    return ownership_sentences(ledger, titles=titles)",
     "    titles = {t.task_id: t.title for t in job.tasks}\n"
     "    return []"),
    ("m12", JOB_DIGEST,
     "an OwnershipError propagates out of build_job_digest",
     "    try:\n"
     "        ledger = build_ownership_ledger(job)\n"
     "    except (OwnershipError, OSError) as exc:\n"
     '        return [f"The ownership ledger could not be read: {exc}"]',
     "    ledger = build_ownership_ledger(job)"),
]

FAILED_RE = re.compile(r"(\d+) failed")
FAILED_NODE_RE = re.compile(r"^FAILED (\S+)", re.MULTILINE)


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        if cache_dir.is_dir():
            for child in cache_dir.rglob("*"):
                if child.is_file():
                    child.unlink()
            for child in sorted(cache_dir.rglob("*"), reverse=True):
                if child.is_dir():
                    child.rmdir()
            cache_dir.rmdir()


def _run_selection(root: Path) -> tuple[int, str]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf",
         *TEST_SELECTION],
        cwd=str(root), capture_output=True, text=True, timeout=600,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _report(label: str, exit_code: int, output: str) -> None:
    m = FAILED_RE.search(output)
    failed_count = int(m.group(1)) if m else 0
    node_ids = FAILED_NODE_RE.findall(output)
    print(f"{label}: exit={exit_code} failed={failed_count} nodes={node_ids}")


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    all_ok = True
    restored_identical = True

    exit_code, output = _run_selection(root)
    _report("control (before)", exit_code, output)
    if exit_code != 0:
        all_ok = False

    for label, rel_path, description, from_text, to_text in MUTATIONS:
        target = root / rel_path
        original = target.read_text(encoding="utf-8")
        assert original.count(from_text) == 1, (
            f"{label}: FROM text does not occur exactly once in {rel_path}")
        mutated = original.replace(from_text, to_text, 1)
        target.write_text(mutated, encoding="utf-8")
        try:
            exit_code, output = _run_selection(root)
        finally:
            target.write_text(original, encoding="utf-8")
        restored = target.read_text(encoding="utf-8")
        if restored != original:
            restored_identical = False
        m = FAILED_RE.search(output)
        failed_count = int(m.group(1)) if m else 0
        node_ids = FAILED_NODE_RE.findall(output)
        print(f"{label} ({description}): exit={exit_code} failed={failed_count} "
              f"nodes={node_ids}")
        if exit_code == 0 or failed_count < 1:
            all_ok = False

    exit_code, output = _run_selection(root)
    _report("control (after)", exit_code, output)
    if exit_code != 0:
        all_ok = False

    print(f"restored byte-identical: {restored_identical}")
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: "
          f"{bool(all_ok and restored_identical)}")
    return 0 if (all_ok and restored_identical) else 1


if __name__ == "__main__":
    raise SystemExit(main())
