#!/usr/bin/env python3
"""F029 R6 G5 — the red proofs for the run detail's Rerun control: the send
module's request shape and refusal sentence (S1), the words half's estimate
and prepared sentences (S2), the report's attempt clause (S4), and the
control staying a non-dialog panel (S3).

Takes a worktree path. Two kinds of mutation, each with its own unmutated
control run first and last:

  TYPESCRIPT (m1-m5): the PRIMARY checkout's `apps/ui/node_modules/.bin/vitest`
  run against a scratch, PLAIN-OBJECT config written under
  `.remedy-wt/f029-r6-worker/` — `root` the primary's `apps/ui` (the only tree
  with `node_modules`), a fresh `cacheDir` per call, `test.environment`
  `"node"` and `test.include` the WORKTREE's own `rerunSend.test.ts` and
  `rerunView.test.ts` by absolute path.

  PYTHON (m6-m8): `python3 -B -m pytest -q -p no:cacheprovider
  tests/orchestration/test_run_report.py tests/ui_contracts/test_run_detail_wiring.py
  tests/ui_contracts/test_attempt_fan_contract.py` from the worktree's own
  root, after purging its `__pycache__` directories. m8 mutates
  `RunDetailPopover.tsx` (a TypeScript file) but is caught by this route: the
  round's own pin reads that file as SOURCE TEXT (no DOM harness exists), so
  its `role="dialog"` assertion is a Python test.

For each mutation: edits the named file INSIDE the worktree (its FROM text
asserted to occur exactly once), runs the route that catches it, restores the
original bytes, and prints the mutation's label, the run's real exit code,
the failed count and the failing tests' names. Ends with `restored
byte-identical: <bool>` per touched file, the PRIMARY checkout's own
`git status --porcelain` (must be empty) and
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f029-r6-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

PRIMARY_ROOT = Path("/home/decodeux/Repos/remedy")
PRIMARY_UI = PRIMARY_ROOT / "apps" / "ui"
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"
MUTSCRATCH_DIR = PRIMARY_ROOT / ".remedy-wt" / "f029-r6-worker" / "vitest-scratch"

RERUN_SEND = "apps/ui/src/api/rerunSend.ts"
RERUN_VIEW = "apps/ui/src/api/rerunView.ts"
RUN_REPORT = "packages/orchestration/run_report.py"
RUN_DETAIL_POPOVER = "apps/ui/src/components/graph/RunDetailPopover.tsx"

VITEST_TEST_RELS = [
    "apps/ui/src/api/rerunSend.test.ts",
    "apps/ui/src/api/rerunView.test.ts",
]

PYTEST_ARGS = [
    "tests/orchestration/test_run_report.py",
    "tests/ui_contracts/test_run_detail_wiring.py",
    "tests/ui_contracts/test_attempt_fan_contract.py",
]

# Each entry: (label, kind, relative path, FROM text, TO text). FROM must
# occur exactly once in the pristine file.
MUTATIONS: list[tuple[str, str, str, str, str]] = [
    (
        "m1 the request always sends confirm_cost: true",
        "vitest",
        RERUN_SEND,
        '        ...(options.confirmCost === true ? { confirm_cost: true } : {}),\n',
        '        { confirm_cost: true },  // MUTATED (m1): always sent\n',
    ),
    (
        "m2 the request never sends model",
        "vitest",
        RERUN_SEND,
        '        ...(trimmedModel !== "" ? { model: trimmedModel } : {}),\n',
        '        {},  // MUTATED (m2): model dropped\n',
    ),
    (
        "m3 a refusal's sentence keeps the code's prefix",
        "vitest",
        RERUN_SEND,
        '  const separator = error.indexOf(": ");\n'
        '  const sentence = separator === -1 ? error : error.slice(separator + 2);\n',
        '  const separator = error.indexOf(": ");\n'
        '  const sentence = error;  // MUTATED (m3): prefix kept\n',
    ),
    (
        "m4 an unavailable estimate reads as the priced sentence",
        "vitest",
        RERUN_VIEW,
        '  if (isFiniteNumber(low) && isFiniteNumber(high) && isFiniteNumber(threshold)) {\n',
        '  if (true) {  // MUTATED (m4): always priced\n',
    ),
    (
        "m5 the prepared view's runCommand is \"\"",
        "vitest",
        RERUN_VIEW,
        '    const runCommand = typeof answer.run_command === "string" ? answer.run_command : "";\n',
        '    const runCommand = "";  // MUTATED (m5): run_command dropped\n',
    ),
    (
        "m6 _attempt_clause answers a clause for attempt 1",
        "pytest",
        RUN_REPORT,
        '    if task.attempt < 2:\n',
        '    if task.attempt < 1:  # MUTATED (m6): attempt 1 earns a clause\n',
    ),
    (
        "m7 _attempt_clause leaves out the override",
        "pytest",
        RUN_REPORT,
        '    clause = f" — attempt {task.attempt}"\n'
        '    if task.model_override:\n'
        '        clause += f", run on {task.model_override}"\n'
        '    return clause\n',
        '    clause = f" — attempt {task.attempt}"\n'
        '    return clause  # MUTATED (m7): override left out\n',
    ),
    (
        "m8 RunDetailPopover.tsx keeps a role=\"dialog\" on its panel",
        "pytest",
        RUN_DETAIL_POPOVER,
        '    <aside className={styles.popover} aria-label="Run detail" data-ui="run-detail">\n',
        '    <aside className={styles.popover} aria-label="Run detail" data-ui="run-detail" role="dialog">\n',
    ),
]


def _run_vitest(worktree: Path, tag: str) -> tuple[int, str]:
    """Runs vitest from the PRIMARY `apps/ui` (the only tree with `node_modules`),
    against a scratch config whose `root` is that same primary tree but whose
    `test.include` names the WORKTREE's own absolute test-file paths. A config
    importing `vitest/config` cannot resolve here, so this exports a PLAIN
    OBJECT. A fresh `cacheDir` per call keeps one run's transform cache from
    hiding another's mutation."""
    MUTSCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = MUTSCRATCH_DIR / f"cache-{tag}-{int(time.time() * 1000)}"
    config_path = MUTSCRATCH_DIR / f"vitest.config.{tag}.mjs"
    test_files = [str(worktree / rel) for rel in VITEST_TEST_RELS]
    config_path.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        "  test: {\n"
        '    environment: "node",\n'
        '    include: ["' + '", "'.join(test_files) + '"],\n'
        "  },\n"
        "};\n"
    )
    proc = subprocess.run(
        [str(VITEST_BIN), "run", "--config", str(config_path)],
        cwd=str(PRIMARY_UI), capture_output=True, text=True, timeout=180)
    return proc.returncode, proc.stdout + proc.stderr


def _vitest_failed_count_and_names(output: str) -> tuple[int, list[str]]:
    match = re.search(r"Tests\s+(\d+)\s+failed", output)
    count = int(match.group(1)) if match else (0 if re.search(r"Tests\s+\d+\s+passed", output) else -1)
    names = re.findall(r"^\s*(?:×|FAIL)\s+(.+)$", output, re.MULTILINE)
    return count, names


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_pytest(worktree: Path) -> tuple[int, str]:
    _purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PYTEST_ARGS],
        cwd=str(worktree), capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _pytest_failed_count_and_names(output: str) -> tuple[int, list[str]]:
    failing = sorted({
        line.split(" ", 1)[1].split(" - ", 1)[0].strip()
        for line in output.splitlines()
        if line.startswith("FAILED ")
    })
    failed_count = 0
    for line in output.splitlines():
        if " failed" in line and ("passed" in line or "error" in line or line.strip().endswith("failed")):
            for token in line.split(","):
                token = token.strip()
                if token.endswith("failed"):
                    failed_count = int(token.split()[0])
    return failed_count, failing


def _run_route(worktree: Path, kind: str, tag: str) -> tuple[int, str]:
    return _run_vitest(worktree, tag) if kind == "vitest" else _run_pytest(worktree)


def _failed_count_and_names(kind: str, output: str) -> tuple[int, list[str]]:
    return (_vitest_failed_count_and_names(output) if kind == "vitest"
            else _pytest_failed_count_and_names(output))


def _apply_edit(path: Path, from_text: str, to_text: str, label: str) -> bytes | None:
    """Applies one edit, asserting FROM occurs exactly once. Returns the ORIGINAL bytes on
    success (for the caller to restore), or None (with a printed reason) if it refused."""
    original = path.read_bytes()
    text = original.decode("utf-8")
    occurrences = text.count(from_text)
    if occurrences != 1:
        print(f"{label}: FROM text occurs {occurrences} times (expected 1) — aborting")
        return None
    mutated = text.replace(from_text, to_text, 1)
    path.write_bytes(mutated.encode("utf-8"))
    return original


def _git_status_porcelain() -> str:
    proc = subprocess.run(
        ["git", "-C", str(PRIMARY_ROOT), "status", "--porcelain"],
        capture_output=True, text=True)
    return proc.stdout


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f029-r6-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, _, rel, _, _ in MUTATIONS})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    all_ok = True

    # --- unmutated controls, before any mutation ----------------------------
    print("=" * 78)
    print("--- vitest control run (unmutated, before) ---")
    code, output = _run_vitest(root, "control-first")
    failed, _names = _vitest_failed_count_and_names(output)
    print(f"control (vitest): exit={code} failed={failed}")
    if code != 0:
        print("VITEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        print(output[-2000:])
        return 1

    print("--- pytest control run (unmutated, before) ---")
    code, output = _run_pytest(root)
    failed, _names = _pytest_failed_count_and_names(output)
    print(f"control (pytest): exit={code} failed={failed}")
    if code != 0:
        print("PYTEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        print(output[-2000:])
        return 1

    # --- the eight mutations -------------------------------------------------
    for label, kind, rel_path, from_text, to_text in MUTATIONS:
        path = root / rel_path
        original = originals[rel_path]
        applied = _apply_edit(path, from_text, to_text, label)
        if applied is None:
            all_ok = False
            continue
        try:
            tag = re.sub(r"[^a-z0-9]+", "-", label.split(" ", 1)[0].lower())
            code, output = _run_route(root, kind, tag)
            failed_count, failing_names = _failed_count_and_names(kind, output)
            caught = code != 0 and failed_count != 0
            all_ok = all_ok and caught
            tag_txt = "" if caught else " — GREEN, NOT CAUGHT"
            print(f"{label} [{kind}]: exit={code} failed={failed_count} "
                  f"failing_tests={failing_names}{tag_txt}")
            if not caught:
                print(output[-2000:])
        finally:
            path.write_bytes(original)

    # --- restore verification ------------------------------------------------
    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    # --- unmutated controls, after the full sweep ----------------------------
    print("--- vitest control run (unmutated, after) ---")
    code, output = _run_vitest(root, "control-last")
    vitest_after_ok = code == 0
    print(f"control (vitest): exit={code}")

    print("--- pytest control run (unmutated, after) ---")
    code, output = _run_pytest(root)
    pytest_after_ok = code == 0
    print(f"control (pytest): exit={code}")

    porcelain = _git_status_porcelain()
    primary_clean = porcelain == ""
    print(f"git status --porcelain (primary checkout): {porcelain!r}")

    result = all_ok and all_restored and vitest_after_ok and pytest_after_ok and primary_clean
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
