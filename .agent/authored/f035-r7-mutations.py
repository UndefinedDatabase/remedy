"""F035 R7 G5 — the red-proof tool for R-1083's and R-1084's repairs and the end-to-end proof
(DECISION F035 D7).

Takes a worktree path (argv[1]). For each mutation below: edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), runs
`tests/orchestration/test_ownership_phrases.py`, `tests/ui_contracts/test_ownership_view_contract.py`
and `tests/ui_server/test_ownership_e2e_live.py` from the worktree's own root, after purging its
`__pycache__`, records the exit code, the failed count and the failing node ids, restores the
file's original bytes, and verifies the restoration is byte-identical. Runs an unmutated control
first and last, following G5 of `.agent/authored/f035-r7-block.md` exactly, the same pattern
`.agent/authored/f035-r6-mutations.py` already follows for this feature (a single PYTHON runner
this round — no TypeScript file changed).

  m1 `ownership_phrases.py`: the unreachable clause is appended for no id again (R-1084's own
     repair, undone).
  m2 `EvidencePanel.module.css`: `.ownershipList` loses `list-style: none`.
  m3 `EvidencePanel.tsx`: the tab's `<ul>` loses `className={styles.ownershipList}`.
  m4 `ownership.py`: a resume's actor is read from the event's `source` (the comment right
     above the mutated line names exactly why production never does this).
  m5 `ui_server.py`: `_build_ownership_json` answers the entries without their `sentence`.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")

PYTHON_TESTS = [
    "tests/orchestration/test_ownership_phrases.py",
    "tests/ui_contracts/test_ownership_view_contract.py",
    "tests/ui_server/test_ownership_e2e_live.py",
]

# label, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1 the unreachable clause is appended for no id again",
     "packages/orchestration/ownership_phrases.py",
     'if kind == "unreachable" and ids:',
     'if kind == "unreachable":'),

    ("m2 .ownershipList loses list-style: none",
     "apps/ui/src/components/graph/EvidencePanel.module.css",
     "  list-style: none;\n  margin: 0;\n  padding: 0;\n",
     "  margin: 0;\n  padding: 0;\n"),

    ("m3 the tab's <ul> loses className={styles.ownershipList}",
     "apps/ui/src/components/graph/EvidencePanel.tsx",
     '<ul className={styles.ownershipList}>',
     '<ul>'),

    ("m4 a resume's actor is read from the event's source",
     "packages/orchestration/ownership.py",
     'actor = ownership_actor("")',
     'actor = ownership_actor(md.get("source"))'),

    ("m5 _build_ownership_json answers the entries without their sentence",
     "packages/orchestration/ui_server.py",
     "    from packages.orchestration.ownership_phrases import ownership_view\n"
     "    return ownership_view(job)\n",
     "    from packages.orchestration.ownership import build_ownership_ledger\n"
     "    return build_ownership_ledger(job)\n"),
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
