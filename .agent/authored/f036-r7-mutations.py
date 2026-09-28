"""F036 R7 G4 — the red-proof tool for R-1090's repair (DECISION F036 D7, checklist item 30's
mutation-coverage rule).

Takes a worktree path (argv[1]). For each mutation below: edits `TourOverlay.module.css` INSIDE
that worktree (asserting its FROM text occurs exactly once), runs
`python3 -B -m pytest -q -p no:cacheprovider tests/ui_contracts/test_tour_overlay_contract.py`
from the worktree's own root — the one gate that reads this file as source (DECISION F031 D5) —
restores the file's original bytes, and verifies the restoration is byte-identical. Runs an
unmutated control of the runner first and last. Modelled on `.agent/authored/f036-r6-mutations.py`,
whose CONTRACT route this tool reuses unchanged; round 7 has no PYTHON mutation, so that route is
dropped rather than carried forward unused.

  m1 the `white-space: nowrap;` line inside `.actions button` is removed;
  m2 the `.card[data-shown="true"] .actions { flex-wrap: wrap; }` rule line is removed.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")

CONTRACT_TESTS = ["tests/ui_contracts/test_tour_overlay_contract.py"]
CSS_PATH = "apps/ui/src/components/tour/TourOverlay.module.css"

# label, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1 the white-space: nowrap; line is removed",
     CSS_PATH,
     "  white-space: nowrap;\n",
     ""),

    ("m2 the .card[data-shown=\"true\"] .actions rule line is removed",
     CSS_PATH,
     '.card[data-shown="true"] .actions { flex-wrap: wrap; }\n',
     ""),
]


def run_contract(worktree: Path) -> tuple[int, int, list[str]]:
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf",
         *CONTRACT_TESTS],
        cwd=str(worktree), capture_output=True, text=True, timeout=60,
    )
    out = proc.stdout + proc.stderr
    failing = [line[len("FAILED "):].split(" - ")[0]
               for line in out.splitlines() if line.startswith("FAILED ")]
    return proc.returncode, len(failing), failing


def _control(worktree: Path, when: str) -> bool:
    exit_code, failed_count, failing = run_contract(worktree)
    print(f"control ({when}) CONTRACT: exit={exit_code} failed={failed_count} tests={failing}")
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
            exit_code, failed_count, failing = run_contract(worktree)
        finally:
            target.write_bytes(original)
        restored = target.read_bytes() == original
        restored_all = restored_all and restored
        restored_report.append((f"{label} ({rel_path})", restored))
        caught = exit_code != 0 and failed_count > 0 and bool(failing)
        all_caught = all_caught and caught
        print(f"{label}: runner=CONTRACT exit={exit_code} failed={failed_count} "
              f"tests={failing} caught={caught} restored={restored}")

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
