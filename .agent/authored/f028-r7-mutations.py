#!/usr/bin/env python3
"""F028 R7 G5 — the red proofs for the canvas chip's origin thread (S1) and the
draft view (S2).

Takes a worktree path. Runs an unmutated VITEST control first and last, over the
worktree's own `injectView.test.ts`, `brainView.test.ts`, `brainReducer.test.ts` and
`buildForceBrainModel.test.ts`, through a scratch vitest config that reads the
WORKTREE's own sources via the PRIMARY checkout's `apps/ui/node_modules` — a worktree
carries no `node_modules` of its own.

For each of the seven ordered mutations below: edits the named file INSIDE the
worktree (asserting its FROM text occurs exactly once), runs the vitest route above,
restores the bytes BYTE-IDENTICAL, and reports the mutation's label, the run's real
exit code and the failed count. Ends with `restored byte-identical: <bool>` per
touched file, `git status --porcelain` of the PRIMARY checkout, and
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f028-r7-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

PRIMARY_ROOT = Path("/home/decodeux/Repos/remedy")
PRIMARY_UI = PRIMARY_ROOT / "apps" / "ui"
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"
MUTSCRATCH_DIR = PRIMARY_ROOT / ".remedy-wt" / "f028-r7-worker" / "vitest-scratch"

BRAIN_VIEW = "apps/ui/src/components/graph/brainView.ts"
BRAIN_REDUCER = "apps/ui/src/components/graph/brainReducer.ts"
BUILD_FORCE_BRAIN_MODEL = "apps/ui/src/components/graph/buildForceBrainModel.ts"
INJECT_VIEW = "apps/ui/src/api/injectView.ts"

VITEST_TEST_RELS = [
    "apps/ui/src/api/injectView.test.ts",
    "apps/ui/src/components/graph/brainView.test.ts",
    "apps/ui/src/components/graph/brainReducer.test.ts",
    "apps/ui/src/components/graph/buildForceBrainModel.test.ts",
]

# Each mutation: an exact FROM string, replaced by an exact TO string. FROM must
# occur exactly once in the pristine file. All seven are caught by the vitest route
# above, over the four test files VITEST_TEST_RELS names.
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 dashboardBrainSeeds puts origin on every seed",
        BRAIN_VIEW,
        '    ...(t.origin === INJECTED_TASK_ORIGIN ? { origin: t.origin } : {}),\n',
        '    ...({ origin: t.origin }),  // MUTATED (m1): origin on every seed\n',
    ),
    (
        "m2 seedBrainModel never copies origin",
        BRAIN_REDUCER,
        '    if (seed.origin !== undefined) meta.origin = seed.origin;\n',
        '    if (false) meta.origin = seed.origin;  // MUTATED (m2): origin never copied\n',
    ),
    (
        "m3 taskChipOf ignores origin",
        BUILD_FORCE_BRAIN_MODEL,
        '  const addedChip = task.meta.origin === INJECTED_TASK_ORIGIN ? ORIGIN_CANVAS_CHIP_TEXT : undefined;\n',
        '  const addedChip = undefined;  // MUTATED (m3): origin ignored\n',
    ),
    (
        "m4 taskChipOf answers only the version when both apply",
        BUILD_FORCE_BRAIN_MODEL,
        '  if (versionChip !== undefined && addedChip !== undefined) return `${versionChip} · ${addedChip}`;\n'
        '  return versionChip ?? addedChip;\n',
        '  return versionChip ?? addedChip;  // MUTATED (m4): never joins both\n',
    ),
    (
        "m5 injectDraftView answers a shortfall's confirm token",
        INJECT_VIEW,
        '    confirmToken: kind === "shortfall" ? null : readString(answer.confirm_token),\n',
        '    confirmToken: readString(answer.confirm_token),  // MUTATED (m5): shortfall gets a token\n',
    ),
    (
        "m6 injectDraftView drops the acceptance lines",
        INJECT_VIEW,
        '    acceptance: readStringList(task.acceptance),\n',
        '    acceptance: [],  // MUTATED (m6): acceptance dropped\n',
    ),
    (
        "m7 a fence warning omits its path",
        INJECT_VIEW,
        '    .map((path) => `${path} is outside what this job may change.`);\n',
        '    .map((path) => `is outside what this job may change.`);  // MUTATED (m7): path omitted\n',
    ),
]


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
        print("usage: f028-r7-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, rel, _, _ in MUTATIONS})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    all_ok = True

    # --- control run, before any of the seven mutations --------------------------------
    print("=" * 78)
    print("--- vitest control run (unmutated, before) ---")
    code, output = _run_vitest(root, "control-first")
    failed, names = _vitest_failed_count_and_names(output)
    print(f"control: exit={code} failed={failed}")
    if code != 0:
        print("VITEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        print(output[-2000:])
        return 1

    # --- the seven mutations -------------------------------------------------------------
    for label, rel_path, from_text, to_text in MUTATIONS:
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

    # --- restore verification ------------------------------------------------------------
    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    # --- control run, after the full sweep ------------------------------------------------
    print("--- vitest control run (unmutated, after) ---")
    code, output = _run_vitest(root, "control-last")
    vitest_after_ok = code == 0
    print(f"control: exit={code}")

    porcelain = _git_status_porcelain()
    primary_clean = porcelain == ""
    print(f"git status --porcelain (primary checkout): {porcelain!r}")

    result = all_ok and all_restored and vitest_after_ok and primary_clean
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
