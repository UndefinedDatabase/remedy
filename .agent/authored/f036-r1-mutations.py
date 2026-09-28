"""F036 R1 G5 — red-proof tool for packages/orchestration/result_tour.py.

Takes a worktree path. For each mutation below it edits the module INSIDE
that worktree (asserting its FROM text occurs exactly once), runs the
result-tour tests from the worktree's root after purging __pycache__, then
restores the original bytes. Prints one line per mutation: its label, the
exit code, the failed count and the failing node ids. Runs an unmutated
control first and last.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

MODULE_REL = "packages/orchestration/result_tour.py"
TEST_TARGET = "tests/orchestration/test_result_tour.py"

# (label, FROM text, TO text, description)
MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1", 'resolved = ref in context.task_ids',
     'resolved = True',
     "a node anchor resolves whatever its ref"),
    ("m2", 'elif len(kept) >= MAX_TOUR_STOPS:',
     'elif False:',
     "the resolver keeps every sound stop, with no ceiling"),
    ("m3", 'dropped.append({"title": drop_title, "reason": reason})',
     'pass  # mutated: not listed in dropped',
     "a dropped stop is logged but not listed in dropped"),
    ("m4", 'resolved = ref in context.run_commands',
     'resolved = any(cmd.startswith(ref) for cmd in context.run_commands)',
     "a command anchor resolves when a recorded command merely starts with its ref"),
    ("m5", 'names = sorted(child.name for child in directory.iterdir() if child.is_file())',
     'names = sorted(child.name for child in directory.iterdir())',
     "the context lists directories of the evidence directory as evidence files"),
    ("m6", 'area = path.split("/", 1)[0] if "/" in path else TOUR_TOP_LEVEL_AREA',
     'area = path.rsplit("/", 1)[0] if "/" in path else TOUR_TOP_LEVEL_AREA',
     "an area is the file's whole directory instead of its first segment"),
    ("m7", 'if len(areas) <= room:',
     'if True:',
     "when the areas outnumber the room, every area still gets its own stop"),
    ("m8", 'if "report.md" in context.evidence_files or not context.task_ids:',
     'if not context.task_ids:',
     "stop (a) anchors to the first task even when report.md exists"),
    ("m9", 'return text[: bound - 1] + "…"',
     'return text',
     "an over-long text is not cut"),
    ("m10", 'passed = sum(1 for check in sources.dod_checks if check.status == STATUS_PASSED)',
     'passed = len(sources.dod_checks)',
     "the Definition-of-Done stop counts every check as passed"),
    ("m11", 'elif "\\n" in title:',
     'elif False:',
     "a title holding a newline is accepted"),
    ("m12", 'command = context.run_commands[0]',
     'command = context.run_commands[-1]',
     "the run stop uses the LAST recorded command"),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_pytest(root: Path) -> subprocess.CompletedProcess:
    env = {**__import__("os").environ}
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(root) + (":" + existing if existing else "")
    return subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_TARGET],
        cwd=str(root), capture_output=True, text=True, env=env, timeout=300,
    )


def _summarize(result: subprocess.CompletedProcess) -> tuple[int, list[str]]:
    """(failed count, failing node ids) parsed from pytest's own -q output."""
    failed_nodes: list[str] = []
    for line in result.stdout.splitlines():
        if line.startswith("FAILED "):
            failed_nodes.append(line[len("FAILED "):].split(" - ", 1)[0].strip())
    failed_count = len(failed_nodes)
    return failed_count, failed_nodes


def _run_one(root: Path, label: str) -> tuple[int, int, list[str]]:
    _purge_pycache(root)
    result = _run_pytest(root)
    failed_count, failed_nodes = _summarize(result)
    return result.returncode, failed_count, failed_nodes


def main(worktree: str) -> None:
    root = Path(worktree).resolve()
    module_path = root / MODULE_REL
    original = module_path.read_bytes()
    original_text = original.decode("utf-8")

    # The worktree's own module must be importable ahead of the editable install's copy.
    sys.path.insert(0, str(root))

    exit_code, failed_count, failed_nodes = _run_one(root, "control (before)")
    print(f"control (before): exit={exit_code} failed={failed_count} nodes={failed_nodes}")
    control_before_ok = exit_code == 0 and failed_count == 0

    all_caught = True
    for label, from_text, to_text, description in MUTATIONS:
        occurrences = original_text.count(from_text)
        assert occurrences == 1, (
            f"{label}: FROM text occurs {occurrences} times, expected exactly 1: {from_text!r}")
        mutated_text = original_text.replace(from_text, to_text, 1)
        module_path.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, failed_count, failed_nodes = _run_one(root, label)
        finally:
            module_path.write_bytes(original)
        caught = exit_code != 0 and failed_count > 0
        all_caught = all_caught and caught
        status = "RED (caught)" if caught else "GREEN (NOT CAUGHT)"
        print(f"{label} [{description}]: exit={exit_code} failed={failed_count} "
              f"nodes={failed_nodes} -> {status}")

    exit_code, failed_count, failed_nodes = _run_one(root, "control (after)")
    print(f"control (after): exit={exit_code} failed={failed_count} nodes={failed_nodes}")
    control_after_ok = exit_code == 0 and failed_count == 0

    restored = module_path.read_bytes()
    restored_identical = restored == original
    print(f"restored byte-identical: {restored_identical}")

    overall = (all_caught and control_before_ok and control_after_ok and restored_identical)
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree-path>", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
