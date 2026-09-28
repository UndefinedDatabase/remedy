"""F035 R8 G4 — the red-proof tool for R-1085's repair.

Takes a worktree path (argv[1]). For each mutation below: edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), runs
`tests/ui_contracts/test_ownership_view_contract.py` from the worktree's own root, after purging
its `__pycache__`, records the exit code, the failed count and the failing node ids, restores the
file's original bytes, and verifies the restoration is byte-identical. Runs an unmutated control
first and last, following G4 of `.remedy-wt/f035-r8/block.md` exactly, the same pattern
`.agent/authored/f035-r7-mutations.py` already follows for this feature.

  m1 `EvidencePanel.module.css`: the row gap reads `var(--remedy-radius-sm)` again.
  m2 `DetailPopover.module.css`: the row gap reads `var(--remedy-radius-sm)` again.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")

PYTHON_TESTS = [
    "tests/ui_contracts/test_ownership_view_contract.py",
]

# label, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1 the row gap reads var(--remedy-radius-sm) again",
     "apps/ui/src/components/graph/EvidencePanel.module.css",
     "margin-top: 6px;",
     "margin-top: var(--remedy-radius-sm);"),

    ("m2 the row gap reads var(--remedy-radius-sm) again",
     "apps/ui/src/components/detail/DetailPopover.module.css",
     "margin-top: 6px;",
     "margin-top: var(--remedy-radius-sm);"),
]


def _purge_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        if not path.is_dir():
            continue
        for child in sorted(path.rglob("*"), key=lambda p: len(p.parts), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        path.rmdir()


def run_python(worktree: Path) -> tuple[int, int, list[str]]:
    _purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf",
         *PYTHON_TESTS],
        cwd=str(worktree), capture_output=True, text=True, timeout=300,
    )
    out = proc.stdout + proc.stderr
    failing = [line[len("FAILED "):].split(" - ")[0]
               for line in out.splitlines() if line.startswith("FAILED ")]
    return proc.returncode, len(failing), failing


def _control(worktree: Path, when: str) -> bool:
    exit_code, failed_count, failing = run_python(worktree)
    print(f"control ({when}) PYTHON: exit={exit_code} failed={failed_count} tests={failing}")
    return exit_code == 0 and failed_count == 0


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()

    if not _control(worktree, "start"):
        print("CONTROL RUN IS NOT GREEN — aborting.")
        return 1

    all_caught = True
    restored_all = True
    restored_report: list[tuple[str, bool]] = []
    for label, rel_path, from_text, to_text in MUTATIONS:
        target = worktree / rel_path
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(from_text)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times in {rel_path} "
                  f"(expected 1) — SKIPPED")
            all_caught = False
            continue
        mutated_text = original_text.replace(from_text, to_text, 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, failed_count, failing = run_python(worktree)
        finally:
            target.write_bytes(original)
        restored = target.read_bytes() == original
        restored_all = restored_all and restored
        restored_report.append((f"{label} ({rel_path})", restored))
        caught = exit_code != 0 and failed_count > 0 and bool(failing)
        all_caught = all_caught and caught
        print(f"{label}: exit={exit_code} failed={failed_count} tests={failing} "
              f"caught={caught} restored={restored}")

    if not _control(worktree, "end"):
        all_caught = False

    for label, restored in restored_report:
        print(f"restored byte-identical: {restored} ({label})")

    status = subprocess.run(["git", "status", "--porcelain"], cwd=str(PRIMARY),
                             capture_output=True, text=True)
    primary_clean = status.stdout.strip() == ""
    print("PRIMARY checkout git status --porcelain:")
    print(status.stdout if status.stdout else "(empty)")

    verdict = all_caught and restored_all and primary_clean
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {verdict}")
    return 0 if verdict else 1


if __name__ == "__main__":
    raise SystemExit(main())
