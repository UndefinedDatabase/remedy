#!/usr/bin/env python3
"""F028 R6 G5 — the red proofs for the dashboard task item's `origin` (S1), the pure
chip (S2) and the browser's send module for the three injection commands (S3).

Takes a worktree path. Runs an unmutated PYTEST control (over the round's one new
Python test, `tests/ui_server/test_dashboard_task_origin.py`) and an unmutated VITEST
control (over the round's two new `.test.ts` files, through a scratch vitest config
that reads the WORKTREE's own sources via the PRIMARY checkout's `apps/ui/node_modules`
— a worktree carries no `node_modules` of its own) first and last.

One mutation (m1) touches `ui_server.py` and is proven red by the pytest route above.
Six mutations (m2-m7) touch `injectView.ts` or `injectSend.ts` and are proven red by
the vitest route above, over `injectView.test.ts` and `injectSend.test.ts`.

For each of the seven ordered mutations below: edits the named file INSIDE the
worktree (asserting its FROM text occurs exactly once), purges the worktree's
`__pycache__` directories for the Python-run mutation, runs the matching test runner,
restores the bytes BYTE-IDENTICAL, and reports the mutation's label, the run's real
exit code and the failed count. Ends with `restored byte-identical: <bool>` per
touched file, `git status --porcelain` of the PRIMARY checkout, and
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f028-r6-mutations.py <worktree-path>
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
MUTSCRATCH_DIR = PRIMARY_ROOT / ".remedy-wt" / "f028-r6-worker" / "vitest-scratch"

UI_SERVER = "packages/orchestration/ui_server.py"
INJECT_VIEW = "apps/ui/src/api/injectView.ts"
INJECT_SEND = "apps/ui/src/api/injectSend.ts"

PYTEST_NODE_IDS = [
    "tests/ui_server/test_dashboard_task_origin.py",
]

VITEST_TEST_RELS = [
    "apps/ui/src/api/injectView.test.ts",
    "apps/ui/src/api/injectSend.test.ts",
]

# The one PYTHON-caught mutation: touches ui_server.py's `_task_origin`, read back by
# the round's own pytest node.
PYTEST_MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 the task item's origin is always the empty string",
        UI_SERVER,
        '    origin = plan.get("origin")\n'
        '    return origin if isinstance(origin, str) and origin else ""\n',
        '    origin = plan.get("origin")\n'
        '    return ""  # MUTATED (m1): origin never read\n',
    ),
]

# The six TypeScript-caught mutations: an exact FROM string, replaced by an exact TO
# string. FROM must occur exactly once in the pristine file. Caught by the vitest route
# over injectView.test.ts and injectSend.test.ts.
VITEST_MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m2 taskOriginChip answers the chip for any non-empty origin",
        INJECT_VIEW,
        '  return task?.origin === INJECTED_TASK_ORIGIN ? ORIGIN_CHIP_TEXT : null;\n',
        '  return task?.origin ? ORIGIN_CHIP_TEXT : null;  // MUTATED (m2): any origin chips\n',
    ),
    (
        "m3 buildInjectDraftRequest accepts a blank text",
        INJECT_SEND,
        '  if (text.trim() === "" || !isUsableCommandNonce(clientNonce)) {\n',
        '  if (!isUsableCommandNonce(clientNonce)) {  // MUTATED (m3): blank text accepted\n',
    ),
    (
        "m4 buildInjectAnswerRequest accepts an option outside the three",
        INJECT_SEND,
        '  if (\n'
        '    draftId === "" ||\n'
        '    !(INJECT_SHORTFALL_OPTIONS as readonly string[]).includes(option) ||\n'
        '    !isUsableCommandNonce(clientNonce)\n'
        '  ) {\n',
        '  if (\n'
        '    draftId === "" ||\n'
        '    !isUsableCommandNonce(clientNonce)\n'
        '  ) {  // MUTATED (m4): option check dropped\n',
    ),
    (
        "m5 INJECT_DRAFT_DEADLINE_MS is 20000",
        INJECT_SEND,
        'export const INJECT_DRAFT_DEADLINE_MS = 120000;\n',
        'export const INJECT_DRAFT_DEADLINE_MS = 20000;  // MUTATED (m5)\n',
    ),
    (
        "m6 a 409 draft_expired is worded by the unknown-code fallback",
        INJECT_SEND,
        '  draft_expired: "Not confirmed: this draft has expired.",\n',
        '  draft_expired_MUTATED: "Not confirmed: this draft has expired.",\n',
    ),
    (
        "m7 buildInjectConfirmRequest names job.inject as its command",
        INJECT_SEND,
        '      command: JOB_INJECT_CONFIRM_COMMAND_ID,\n',
        '      command: JOB_INJECT_COMMAND_ID,  // MUTATED (m7): wrong command\n',
    ),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_pytest(worktree: Path) -> tuple[int, str]:
    _purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PYTEST_NODE_IDS],
        cwd=str(worktree), capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def _pytest_failed_count_and_ids(output: str) -> tuple[int, list[str]]:
    ids = sorted(set(re.findall(r"^FAILED (\S+)", output, re.MULTILINE)))
    match = re.search(r"(\d+) failed", output)
    count = int(match.group(1)) if match else 0
    return count, ids


def _run_vitest(worktree: Path, tag: str) -> tuple[int, str]:
    """Runs vitest from the PRIMARY `apps/ui` (the only tree with `node_modules`), against
    a scratch config whose `root` is that same primary tree but whose `test.include` names
    the WORKTREE's own absolute test-file paths. A config importing `vitest/config` cannot
    resolve here, so this exports a PLAIN OBJECT. A fresh `cacheDir` per call keeps one
    run's transform cache from hiding another's mutation."""
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
        print("usage: f028-r6-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, rel, _, _ in [*PYTEST_MUTATIONS, *VITEST_MUTATIONS]})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    all_ok = True

    # --- control runs, before any of the seven mutations ------------------------------
    print("=" * 78)
    print("--- pytest control run (unmutated, before) ---")
    code, output = _run_pytest(root)
    failed, ids = _pytest_failed_count_and_ids(output)
    print(f"control: exit={code} failed={failed}")
    if code != 0:
        print("PYTEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        print(output[-2000:])
        return 1

    print("--- vitest control run (unmutated, before) ---")
    code, output = _run_vitest(root, "control-first")
    failed, names = _vitest_failed_count_and_names(output)
    print(f"control: exit={code} failed={failed}")
    if code != 0:
        print("VITEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        print(output[-2000:])
        return 1

    # --- the one pytest-caught mutation ------------------------------------------------
    for label, rel_path, from_text, to_text in PYTEST_MUTATIONS:
        path = root / rel_path
        original = originals[rel_path]
        applied = _apply_edit(path, from_text, to_text, label)
        if applied is None:
            all_ok = False
            continue
        try:
            code, output = _run_pytest(root)
            failed_count, failing_ids = _pytest_failed_count_and_ids(output)
            caught = code != 0 and failed_count > 0
            all_ok = all_ok and caught
            tag = "" if caught else " — GREEN, NOT CAUGHT"
            print(f"{label}: exit={code} failed={failed_count} "
                  f"failing_node_ids={failing_ids}{tag}")
            if not caught:
                print(output[-2000:])
        finally:
            path.write_bytes(original)

    # --- the six vitest-caught mutations -----------------------------------------------
    for label, rel_path, from_text, to_text in VITEST_MUTATIONS:
        path = root / rel_path
        original = originals[rel_path]
        applied = _apply_edit(path, from_text, to_text, label)
        if applied is None:
            all_ok = False
            continue
        try:
            tag = re.sub(r"[^a-z0-9]+", "-", label.split(" ", 1)[0].lower())
            code, output = _run_vitest(root, tag)
            failed_count, failing_names = _vitest_failed_count_and_names(output)
            caught = code != 0 and failed_count != 0
            all_ok = all_ok and caught
            tag_txt = "" if caught else " — GREEN, NOT CAUGHT"
            print(f"{label}: exit={code} failed={failed_count} "
                  f"failing_tests={failing_names}{tag_txt}")
            if not caught:
                print(output[-2000:])
        finally:
            path.write_bytes(original)

    # --- restore verification ----------------------------------------------------------
    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    # --- control runs, after the full sweep ---------------------------------------------
    print("--- pytest control run (unmutated, after) ---")
    code, output = _run_pytest(root)
    pytest_after_ok = code == 0
    print(f"control: exit={code}")

    print("--- vitest control run (unmutated, after) ---")
    code, output = _run_vitest(root, "control-last")
    vitest_after_ok = code == 0
    print(f"control: exit={code}")

    porcelain = _git_status_porcelain()
    primary_clean = porcelain == ""
    print(f"git status --porcelain (primary checkout): {porcelain!r}")

    result = all_ok and all_restored and pytest_after_ok and vitest_after_ok and primary_clean
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
