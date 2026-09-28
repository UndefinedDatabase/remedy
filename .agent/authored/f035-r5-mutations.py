"""F035 R5 G5 — the red-proof tool for T003's browser reader (DECISION F035 D5) and the R-1082
repair.

Takes a worktree path (argv[1]). For each mutation below: edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), runs the mutation's own runner, records
the exit code, the failed count and the failing tests' names, restores the file's original
bytes, and verifies the restoration is byte-identical. Runs an unmutated control of EACH runner
first and last, following G5 of `.agent/authored/f030-r3-block.md` exactly.

PYTHON mutations run `pytest` from the worktree's own root, after purging its `__pycache__`, over
`tests/orchestration/test_ownership_phrases.py` (the golden and inline assertions S0 repairs) and
`tests/ui_contracts/test_ownership_view_contract.py` (the contract test, which reads
`DetailPopover.tsx` and `RemedyShell.tsx` as plain text — so a mutation to either of those two
`.tsx` files is caught by this PYTHON runner, never a JS one). VITEST mutations run the PRIMARY
checkout's own `vitest` binary against a scratch config this tool writes under
`.remedy-wt/f035-r5-worker/`: a plain object naming the primary's `apps/ui` as `root`, a cache
directory under `.remedy-wt/`, `test.environment` `"node"`, and `test.include` the WORKTREE's
`ownership.test.ts` by absolute path — so the binary is the primary's, but the relative import
the test file carries resolves inside the mutated worktree.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
WORKER_DIR = PRIMARY / ".remedy-wt" / "f035-r5-worker"
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"

#: PYTHON's own selection: the phrase catalog's golden and inline assertions, and the contract
#: test that also reads DetailPopover.tsx and RemedyShell.tsx as source.
PYTHON_TESTS = [
    "tests/orchestration/test_ownership_phrases.py",
    "tests/ui_contracts/test_ownership_view_contract.py",
]

#: VITEST's own selection, by filename under the worktree's `apps/ui/src/api/`.
VITEST_TEST_NAMES = ["ownership.test.ts"]

# label, runner, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str, str]] = [
    ("m1 the plan-edit sentences drop at",
     "PYTHON", "packages/orchestration/ownership_phrases.py",
     'return f"{actor_phrase} changed {t_display} in the plan; the plan is now at '
     '{version_phrase}."',
     'return f"{actor_phrase} changed {t_display} in the plan; the plan is now '
     '{version_phrase}."'),

    ("m2 the acceptance sentence gains in the plan",
     "PYTHON", "packages/orchestration/ownership_phrases.py",
     'f"{actor_phrase} changed the acceptance checks of {t_display}; "\n'
     '                f"the plan is now at {version_phrase}."',
     'f"{actor_phrase} changed the acceptance checks of {t_display} in the plan; "\n'
     '                f"the plan is now at {version_phrase}."'),

    ("m3 the decoder accepts an entry whose sentence is not a string",
     "VITEST", "apps/ui/src/api/ownership.ts",
     "if (recordRef === null || ts === null || actor === null || action === null "
     "|| taskId === null\n      || text === null || consequence === null || sentence === null) {",
     "if (recordRef === null || ts === null || actor === null || action === null "
     "|| taskId === null\n      || text === null || consequence === null) {"),

    ("m4 ownershipEntriesForTask ignores consequence.taskIds",
     "VITEST", "apps/ui/src/api/ownership.ts",
     "entry.taskId === taskId || entry.consequence.taskIds.includes(taskId));",
     "entry.taskId === taskId);"),

    ("m5 ownershipRefreshKey counts every frame's seq",
     "VITEST", "apps/ui/src/api/ownership.ts",
     "(newest, row) => (kinds.includes(row.kind) && row.seq > newest ? row.seq : newest), 0);",
     "(newest, row) => (row.seq > newest ? row.seq : newest), 0);"),

    ("m6 the path leaves the job id unencoded",
     "VITEST", "apps/ui/src/api/ownership.ts",
     "return `${base}/api/jobs/${encodeURIComponent(request.jobId)}/ownership`",
     "return `${base}/api/jobs/${request.jobId}/ownership`"),

    ("m7 loadOwnershipView lets a throwing fetcher reject",
     "VITEST", "apps/ui/src/api/remedyApi.ts",
     "  try {\n    return decodeOwnershipView(await fetchPayload(ownershipViewPath(request)));\n"
     "  } catch {\n    return null;\n  }\n}",
     "  return decodeOwnershipView(await fetchPayload(ownershipViewPath(request)));\n}"),

    ("m8 the section renders ownership.error instead of the line",
     "PYTHON", "apps/ui/src/components/detail/DetailPopover.tsx",
     "<p>{OWNERSHIP_UNREADABLE_LINE}</p>",
     "<p>{ownership.error}</p>"),

    ("m9 the effect's dependencies drop the refresh key",
     "PYTHON", "apps/ui/src/components/shell/RemedyShell.tsx",
     "}, [dashboard.jobId, serverToken, ownershipKey, focusedTaskId]);",
     "}, [dashboard.jobId, serverToken, focusedTaskId]);"),
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
