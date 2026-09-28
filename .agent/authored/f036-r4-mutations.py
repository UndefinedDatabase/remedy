"""F036 R4 G5 — the red-proof tool for the `tour` route, `tour_view` (DECISION F036 D5) and
the R-1087 repair.

Takes a worktree path (argv[1]). For each mutation below: edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), runs the mutation's own runner, records
the exit code, the failed count and the failing tests' names, restores the file's original
bytes, and verifies the restoration is byte-identical. Runs an unmutated control of EACH runner
first and last. Modelled exactly on `.agent/authored/f035-r5-mutations.py`, whose VITEST route
this tool reuses.

PYTHON mutations run `pytest` from the worktree's own root, after purging its `__pycache__`,
over `tests/orchestration/test_result_tour.py` (`tour_view` and the R-1087 claim-check tests),
`tests/ui_server/test_tour_route.py` (the route's own byte-for-byte pin) and
`tests/cli/test_job_show.py` (the `_tour_section` behaviour). VITEST mutations run the PRIMARY
checkout's own `vitest` binary against a scratch config this tool writes under
`.remedy-wt/f036-r4-worker/`: a plain object naming the primary's `apps/ui` as `root`, a cache
directory under `.remedy-wt/`, `test.environment` `"node"`, and `test.include` the WORKTREE's
`resultTour.test.ts` by absolute path — so the binary is the primary's, but the relative import
the test file carries resolves inside the mutated worktree.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
WORKER_DIR = PRIMARY / ".remedy-wt" / "f036-r4-worker"
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"

#: PYTHON's own selection: `tour_view`, the route's byte-for-byte pin and the `_tour_section`
#: behaviour, which also reads `_TOUR_PATH_TOKEN_RE` through the claim-check tests.
PYTHON_TESTS = [
    "tests/orchestration/test_result_tour.py",
    "tests/ui_server/test_tour_route.py",
    "tests/cli/test_job_show.py",
]

#: VITEST's own selection, by filename under the worktree's `apps/ui/src/api/`.
VITEST_TEST_NAMES = ["resultTour.test.ts"]

# label, runner, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str, str]] = [
    ("m1 tour_view reads stored true when none is stored",
     "PYTHON", "packages/orchestration/result_tour.py",
     '    if loaded is None:\n'
     '        return {"stored": False, "version": 0, "tour": build_fallback_tour(job), '
     '"error": ""}',
     '    if loaded is None:\n'
     '        return {"stored": True, "version": 0, "tour": build_fallback_tour(job), '
     '"error": ""}'),

    ("m2 tour_view lets a ResultTourError propagate",
     "PYTHON", "packages/orchestration/result_tour.py",
     '    try:\n'
     '        loaded = load_result_tour(job_id)\n'
     '    except ResultTourError as exc:\n'
     '        return {"stored": False, "version": 0, "tour": build_fallback_tour(job), '
     '"error": str(exc)}',
     '    loaded = load_result_tour(job_id)'),

    ("m3 the slashed-path half is round 3's pattern again",
     "PYTHON", "packages/orchestration/result_tour.py",
     'r"(?:[\\w.-]+/)+[\\w.-]*\\w|\\w+\\.[A-Za-z]{1,5}\\b"',
     'r"\\w+(?:/\\w+)+|\\w+\\.[A-Za-z]{1,5}\\b"'),

    ("m4 the slashed-path half no longer has to end at a word character",
     "PYTHON", "packages/orchestration/result_tour.py",
     'r"(?:[\\w.-]+/)+[\\w.-]*\\w|\\w+\\.[A-Za-z]{1,5}\\b"',
     'r"(?:[\\w.-]+/)+[\\w.-]*|\\w+\\.[A-Za-z]{1,5}\\b"'),

    ("m5 the tour entry of handlers serves the ownership view",
     "PYTHON", "packages/orchestration/ui_server.py",
     '"tour": _build_tour_json,',
     '"tour": _build_ownership_json,'),

    ("m6 the decoder accepts more than MAX_TOUR_STOPS stops",
     "VITEST", "apps/ui/src/api/resultTour.ts",
     "  if (rawStops.length > MAX_TOUR_STOPS) return null;\n",
     ""),

    ("m7 the decoder accepts an anchor kind outside TOUR_ANCHOR_KINDS",
     "VITEST", "apps/ui/src/api/resultTour.ts",
     'if (kind === null || !(TOUR_ANCHOR_KINDS as readonly string[]).includes(kind)) '
     'return null;',
     'if (kind === null) return null;'),

    ("m8 tourNeighbours answers a next at the last stop",
     "VITEST", "apps/ui/src/api/resultTour.ts",
     "next: current + 1 < count ? current + 1 : null,",
     "next: current + 1 <= count ? current + 1 : null,"),

    ("m9 tourPanelState answers stops for a tour with none",
     "VITEST", "apps/ui/src/api/resultTour.ts",
     'if (view.tour.stops.length === 0) return { kind: "empty", line: TOUR_EMPTY_LINE };',
     'if (view.tour.stops.length < 0) return { kind: "empty", line: TOUR_EMPTY_LINE };'),

    ("m10 loadTourView lets a rejected fetch throw",
     "VITEST", "apps/ui/src/api/remedyApi.ts",
     "  try {\n    return decodeTourView(await fetchPayload(tourViewPath(request)));\n"
     "  } catch {\n    return null;\n  }\n}",
     "  return decodeTourView(await fetchPayload(tourViewPath(request)));\n}"),
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
        cwd=str(worktree), capture_output=True, text=True, timeout=120,
    )
    out = proc.stdout + proc.stderr
    failing = [line[len("FAILED "):].split(" - ")[0]
               for line in out.splitlines() if line.startswith("FAILED ")]
    return proc.returncode, len(failing), failing


def _write_vitest_config(worktree: Path) -> Path:
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
    return config_path


def run_vitest(worktree: Path) -> tuple[int, int, list[str]]:
    config_path = _write_vitest_config(worktree)
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


RUNNERS = {"PYTHON": run_python, "VITEST": run_vitest}


def _control(worktree: Path, when: str) -> bool:
    ok = True
    for runner in ("PYTHON", "VITEST"):
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
