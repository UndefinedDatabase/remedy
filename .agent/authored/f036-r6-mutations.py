"""F036 R6 G5 — the red-proof tool for R-1089's switch and R-1088's dock (DECISION F036 D7).

Takes a worktree path (argv[1]). For each mutation below: edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), runs the mutation's own runner, records
the exit code, the failed count and the failing tests' names, restores the file's original
bytes, and verifies the restoration is byte-identical. Runs an unmutated control of EACH runner
first and last. Modelled on `.agent/authored/f036-r5-mutations.py`, whose CONTRACT route this
tool reuses unchanged.

PYTHON mutations (`config.py`, `result_tour.py`) run `python3 -B -m pytest -q -p no:cacheprovider
tests/orchestration/test_result_tour.py tests/orchestration/test_config.py` from the WORKTREE's
own root, with that root first on `PYTHONPATH` — so the interpreter imports the worktree's own
mutated `packages/orchestration/config.py` / `result_tour.py`, never the primary checkout's.

CONTRACT mutations (`TourOverlay.tsx`, `TourOverlay.module.css`) run `python3 -B -m pytest -q -p
no:cacheprovider tests/ui_contracts/test_tour_overlay_contract.py` from the worktree's own root
— the one gate that reads these two files as source, since nothing in this repository can
render them (DECISION F031 D5). `-rf` is added beyond the block's own quoted command so this
tool's own report can name which assertion failed; it changes no outcome, only what the runner
prints.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")

#: PYTHON's own selection: the switch's tests and the key registry's own tests.
PYTHON_TESTS = [
    "tests/orchestration/test_result_tour.py",
    "tests/orchestration/test_config.py",
]

#: CONTRACT's own selection: the one file that reads the overlay's card and its CSS module as
#: source.
CONTRACT_TESTS = ["tests/ui_contracts/test_tour_overlay_contract.py"]

# label, runner, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str, str]] = [
    ("m1 the key's default is True",
     "PYTHON", "packages/orchestration/config.py",
     '        key="tour.model_written",\n'
     '        env_var="REMEDY_TOUR_MODEL_WRITTEN",\n'
     "        description=(\n"
     '            "Let the summary model write each job\'s guided tour at the end of "\n'
     '            "its run (F036). Off by default: each tour is one summary model "\n'
     '            "call, and a run makes no call the operator did not switch on; "\n'
     '            "with it off, every job still gets the tour built from its own "\n'
     '            "records."\n'
     "        ),\n"
     "        value_type=bool,\n"
     "        default=False,\n",
     '        key="tour.model_written",\n'
     '        env_var="REMEDY_TOUR_MODEL_WRITTEN",\n'
     "        description=(\n"
     '            "Let the summary model write each job\'s guided tour at the end of "\n'
     '            "its run (F036). Off by default: each tour is one summary model "\n'
     '            "call, and a run makes no call the operator did not switch on; "\n'
     '            "with it off, every job still gets the tour built from its own "\n'
     '            "records."\n'
     "        ),\n"
     "        value_type=bool,\n"
     "        default=True,\n"),

    ("m2 write_result_tour asks tour_call_fn() whatever the key",
     "PYTHON", "packages/orchestration/result_tour.py",
     "        if call_fn is _UNSET_CALL_FN:\n"
     "            resolved_call_fn = tour_call_fn() if tour_model_written() else None\n"
     "        else:\n"
     "            resolved_call_fn = call_fn\n",
     "        resolved_call_fn = tour_call_fn() if call_fn is _UNSET_CALL_FN else call_fn\n"),

    ("m3 tour_model_written answers the key's opposite",
     "PYTHON", "packages/orchestration/result_tour.py",
     '    return bool(get_config().get("tour.model_written"))',
     '    return not bool(get_config().get("tour.model_written"))'),

    ("m4 the .card[data-shown=\"true\"] rule is removed",
     "CONTRACT", "apps/ui/src/components/tour/TourOverlay.module.css",
     '.card[data-shown="true"] {\n'
     "  top: auto;\n"
     "  left: 16px;\n"
     "  bottom: 16px;\n"
     "  transform: none;\n"
     "  width: calc(var(--remedy-left-width) - 32px);\n"
     "  max-height: 60vh;\n"
     "}\n\n",
     ""),

    ("m5 the card's data-shown attribute is removed",
     "CONTRACT", "apps/ui/src/components/tour/TourOverlay.tsx",
     '      <section role="dialog" aria-label="Guided tour" className={styles.card} '
     'data-ui="tour-overlay"\n'
     '               data-shown={backdropVisible ? "false" : "true"}>',
     '      <section role="dialog" aria-label="Guided tour" className={styles.card} '
     'data-ui="tour-overlay">'),
]


def run_python(worktree: Path) -> tuple[int, int, list[str]]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(worktree) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf",
         *PYTHON_TESTS],
        cwd=str(worktree), env=env, capture_output=True, text=True, timeout=90,
    )
    out = proc.stdout + proc.stderr
    failing = [line[len("FAILED "):].split(" - ")[0]
               for line in out.splitlines() if line.startswith("FAILED ")]
    return proc.returncode, len(failing), failing


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


RUNNERS = {"PYTHON": run_python, "CONTRACT": run_contract}


def _control(worktree: Path, when: str) -> bool:
    ok = True
    for runner in ("PYTHON", "CONTRACT"):
        exit_code, failed_count, failing = RUNNERS[runner](worktree)
        print(f"control ({when}) {runner}: exit={exit_code} failed={failed_count} "
              f"tests={failing}")
        if exit_code != 0 or failed_count != 0:
            ok = False
    return ok


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()

    if not _control(worktree, "start"):
        print("CONTROL RUN IS NOT GREEN — aborting.")
        return 1

    all_caught = True
    restored_all = True
    restored_report: list[tuple[str, bool]] = []
    for label, runner, rel_path, from_text, to_text in MUTATIONS:
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
            exit_code, failed_count, failing = RUNNERS[runner](worktree)
        finally:
            target.write_bytes(original)
        restored = target.read_bytes() == original
        restored_all = restored_all and restored
        restored_report.append((f"{label} ({rel_path})", restored))
        caught = exit_code != 0 and failed_count > 0 and bool(failing)
        all_caught = all_caught and caught
        print(f"{label}: runner={runner} exit={exit_code} failed={failed_count} "
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
