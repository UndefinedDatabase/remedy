"""F036 R5 G5 — the red-proof tool for the tour overlay's browser surface (DECISION F036 D6).

Takes a worktree path (argv[1]). For each mutation below: edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), runs the mutation's own runner, records
the exit code, the failed count and the failing tests' names, restores the file's original
bytes, and verifies the restoration is byte-identical. Runs an unmutated control of EACH runner
first and last. Modelled exactly on `.agent/authored/f036-r4-mutations.py`, whose VITEST route
this tool reuses.

VITEST mutations (`resultTour.ts`) run the PRIMARY checkout's own `vitest` binary against a
scratch config this tool writes under `.remedy-wt/f036-r5-worker/`: a plain object naming the
primary's `apps/ui` as `root`, a cache directory under `.remedy-wt/`, `test.environment`
`"node"`, and `test.include` the WORKTREE's `resultTour.test.ts` by absolute path — so the
binary is the primary's, but the relative import the test file carries resolves inside the
mutated worktree.

CONTRACT mutations (`TourOverlay.tsx`, `RemedyShell.tsx`) run `python3 -B -m pytest -q -p
no:cacheprovider tests/ui_contracts/test_tour_overlay_contract.py` from the worktree's own
root — the one gate that reads these two files as source, since nothing in this repository can
render them (DECISION F031 D5). `-rf` is added beyond the block's own quoted command so this
tool's own report can name which assertion failed; it changes no outcome, only what the runner
prints.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
WORKER_DIR = PRIMARY / ".remedy-wt" / "f036-r5-worker"
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"

#: VITEST's own selection, by filename under the worktree's `apps/ui/src/api/`.
VITEST_TEST_NAMES = ["resultTour.test.ts"]

#: CONTRACT's own selection: the one file that reads the overlay and the shell's tour wiring
#: as source.
CONTRACT_TESTS = ["tests/ui_contracts/test_tour_overlay_contract.py"]

# label, runner, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str, str]] = [
    ("m1 tourCanShow holds for command",
     "VITEST", "apps/ui/src/api/resultTour.ts",
     'return anchor.kind === "node" || anchor.kind === "diff";',
     'return anchor.kind === "node" || anchor.kind === "diff" || anchor.kind === "command";'),

    ("m2 tourDiffRowKey answers the LAST matching summary's key",
     "VITEST", "apps/ui/src/api/resultTour.ts",
     "const found = summaries.find((summary) => summary.path === path);",
     "const found = [...summaries].reverse().find((summary) => summary.path === path);"),

    ("m3 tourGeneratorLabel calls every generator model-written",
     "VITEST", "apps/ui/src/api/resultTour.ts",
     "  return generator === TOUR_GENERATOR_SUMMARY_ROLE\n"
     '    ? "Written by the summary model and checked against the job\'s records"',
     '  return true\n'
     '    ? "Written by the summary model and checked against the job\'s records"'),

    ("m4 the overlay renders in place, without createPortal",
     "CONTRACT", "apps/ui/src/components/tour/TourOverlay.tsx",
     "  return createPortal(",
     "  return ("),

    ("m5 the Escape handling is removed",
     "CONTRACT", "apps/ui/src/components/tour/TourOverlay.tsx",
     '      if (event.key === "Escape") onClose();\n'
     '      else if (event.key === "ArrowLeft") stepTo(neighbours.previous);',
     '      if (event.key === "ArrowLeft") stepTo(neighbours.previous);'),

    ("m6 the tour mounts inside <main> instead of after it",
     "CONTRACT", "apps/ui/src/components/shell/RemedyShell.tsx",
     '<main className={styles.main} data-testid="main-column">',
     '<main className={styles.main} data-testid="main-column"><TourOverlay '
     'jobId={dashboard.jobId} serverToken={serverToken} onClose={() => setTourOpen(false)} '
     'onShowAnchor={handleTourShowAnchor} />'),

    ("m7 a diff stop opens the diff of the task id \"x\", not the job's",
     "CONTRACT", "apps/ui/src/components/shell/RemedyShell.tsx",
     'setOpenDiffTaskId("");',
     'setOpenDiffTaskId("x");'),
]


def run_vitest_files(worktree: Path) -> tuple[int, int, list[str]]:
    ui_src = worktree / "apps" / "ui" / "src" / "api"
    includes = ",\n    ".join(json.dumps(str(ui_src / name)) for name in VITEST_TEST_NAMES)
    config = (
        "export default {\n"
        f"  root: {json.dumps(str(PRIMARY / 'apps' / 'ui'))},\n"
        f"  cacheDir: {json.dumps(str(WORKER_DIR / 'vitest-cache'))},\n"
        "  test: {\n"
        '    environment: "node",\n'
        "    include: [\n"
        f"    {includes},\n"
        "    ],\n"
        "  },\n"
        "};\n"
    )
    config_path = WORKER_DIR / "scratch.vitest.config.ts"
    config_path.write_text(config, encoding="utf-8")
    report_path = WORKER_DIR / "vitest-report.json"
    report_path.unlink(missing_ok=True)
    proc = subprocess.run(
        [str(VITEST_BIN), "run", "--config", str(config_path),
         "--reporter=json", f"--outputFile={report_path}"],
        cwd=str(PRIMARY / "apps" / "ui"), capture_output=True, text=True, timeout=60,
    )
    failed_names: list[str] = []
    failed_count = 0
    if report_path.exists():
        data = json.loads(report_path.read_text(encoding="utf-8"))
        failed_count = data.get("numFailedTests", 0)
        for test_result in data.get("testResults", []):
            for assertion in test_result.get("assertionResults", []):
                if assertion.get("status") == "failed":
                    failed_names.append(assertion.get("fullName", "?"))
    return proc.returncode, failed_count, failed_names


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


RUNNERS = {"VITEST": run_vitest_files, "CONTRACT": run_contract}


def _control(worktree: Path, when: str) -> bool:
    ok = True
    for runner in ("VITEST", "CONTRACT"):
        exit_code, failed_count, failing = RUNNERS[runner](worktree)
        print(f"control ({when}) {runner}: exit={exit_code} failed={failed_count} "
              f"tests={failing}")
        if exit_code != 0 or failed_count != 0:
            ok = False
    return ok


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    WORKER_DIR.mkdir(parents=True, exist_ok=True)

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
