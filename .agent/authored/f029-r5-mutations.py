#!/usr/bin/env python3
"""F029 R5 G5 — the red proofs for the browser's attempt fan: the dashboard task
item's `attempt`/`attempts` normalisation (S1), the pure chip and its threading
through the seed (S2), and the popover's Attempts list rows (S3).

Takes a worktree path. Runs an unmutated VITEST control (over the round's five
touched `.test.ts` files, through a scratch vitest config that reads the
WORKTREE's own sources via the PRIMARY checkout's `apps/ui/node_modules` — a
worktree carries no `node_modules` of its own) first and last.

All eight mutations are TypeScript, caught by the same vitest route: m1-m2
touch `brainView.ts`/`brainReducer.ts` (the seed and its threading), m3-m4
touch `buildForceBrainModel.ts` (the chip), m5-m7 touch `attemptView.ts` (the
Attempts list rows and their facts), and m8 touches `remedyApi.ts` (the
normalisation).

For each of the eight ordered mutations below: edits the named file INSIDE the
worktree (asserting its FROM text occurs exactly once), runs the vitest route,
restores the bytes BYTE-IDENTICAL, and reports the mutation's label, the run's
real exit code and the failed count. Ends with `restored byte-identical:
<bool>` per touched file, `git status --porcelain` of the PRIMARY checkout, and
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f029-r5-mutations.py <worktree-path>
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
MUTSCRATCH_DIR = PRIMARY_ROOT / ".remedy-wt" / "f029-r5-worker" / "vitest-scratch"

REMEDY_API = "apps/ui/src/api/remedyApi.ts"
ATTEMPT_VIEW = "apps/ui/src/api/attemptView.ts"
BRAIN_VIEW = "apps/ui/src/components/graph/brainView.ts"
BRAIN_REDUCER = "apps/ui/src/components/graph/brainReducer.ts"
BUILD_FORCE_BRAIN_MODEL = "apps/ui/src/components/graph/buildForceBrainModel.ts"

VITEST_TEST_RELS = [
    "apps/ui/src/api/remedyApi.test.ts",
    "apps/ui/src/api/attemptView.test.ts",
    "apps/ui/src/components/graph/brainView.test.ts",
    "apps/ui/src/components/graph/brainReducer.test.ts",
    "apps/ui/src/components/graph/buildForceBrainModel.test.ts",
]

# Eight ordered mutations: an exact FROM string, replaced by an exact TO
# string. FROM must occur exactly once in the pristine file.
VITEST_MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 dashboardBrainSeeds puts attempt on every seed",
        BRAIN_VIEW,
        '    ...(typeof t.attempt === "number" && t.attempt >= 2 ? { attempt: t.attempt } : {}),\n',
        '    ...(typeof t.attempt === "number" ? { attempt: t.attempt } : {}),  // MUTATED (m1): threshold dropped\n',
    ),
    (
        "m2 seedBrainModel never copies attempt",
        BRAIN_REDUCER,
        '    if (seed.attempt !== undefined) meta.attempt = seed.attempt;\n',
        '    // MUTATED (m2): attempt copy removed\n',
    ),
    (
        "m3 taskChipOf ignores attempt",
        BUILD_FORCE_BRAIN_MODEL,
        '  const attemptChip = typeof attempt === "number" && attempt >= 2 ? attemptChipText(attempt) : undefined;\n',
        '  const attemptChip = undefined;  // MUTATED (m3): attempt ignored\n',
    ),
    (
        "m4 taskChipOf drops v<n> when attempt applies",
        BUILD_FORCE_BRAIN_MODEL,
        '  const parts = [versionChip, addedChip, attemptChip].filter((part): part is string => part !== undefined);\n',
        '  const parts = [attemptChip !== undefined ? undefined : versionChip, addedChip, attemptChip]\n'
        '    .filter((part): part is string => part !== undefined);  // MUTATED (m4): v<n> dropped when attempt applies\n',
    ),
    (
        "m5 taskAttemptRows omits the current row",
        ATTEMPT_VIEW,
        '  rows.push({\n'
        '    attempt: item.attempt as number,\n'
        '    label: `Attempt ${item.attempt} · current`,\n'
        '    facts: [`Now ${currentStateWord(item.state)}`],\n'
        '    changes: [],\n'
        '    current: true,\n'
        '  });\n'
        '  return rows;\n',
        '  return rows;  // MUTATED (m5): current row omitted\n',
    ),
    (
        "m6 an earlier row's changes compare with the FIRST earlier row",
        ATTEMPT_VIEW,
        '    rows.push({\n'
        '      attempt: entry.attempt,\n'
        '      label: `Attempt ${entry.attempt}`,\n'
        '      facts,\n'
        '      changes: changesFromFacts(previousFacts, facts),\n'
        '      current: false,\n'
        '    });\n'
        '    previousFacts = facts;\n',
        '    rows.push({\n'
        '      attempt: entry.attempt,\n'
        '      label: `Attempt ${entry.attempt}`,\n'
        '      facts,\n'
        '      changes: changesFromFacts(previousFacts, facts),\n'
        '      current: false,\n'
        '    });\n'
        '    if (previousFacts === null) previousFacts = facts;  // MUTATED (m6): compares with the FIRST earlier row only\n',
    ),
    (
        "m7 the model fact reads 'it ran on ' with an empty override",
        ATTEMPT_VIEW,
        'function modelFact(modelOverride: string): string {\n'
        '  return modelOverride === "" ? "it ran on the job\'s own model" : `it ran on ${modelOverride}`;\n'
        '}\n',
        'function modelFact(modelOverride: string): string {\n'
        '  return `it ran on ${modelOverride}`;  // MUTATED (m7): empty override reads "it ran on "\n'
        '}\n',
    ),
    (
        "m8 the normalisation keeps an attempt of 0",
        REMEDY_API,
        'function normalizeTaskAttemptNumber(raw: unknown): number {\n'
        '  return typeof raw === "number" && Number.isInteger(raw) && raw >= 1 ? raw : 1;\n'
        '}\n',
        'function normalizeTaskAttemptNumber(raw: unknown): number {\n'
        '  return typeof raw === "number" && Number.isInteger(raw) && raw >= 0 ? raw : 1;  // MUTATED (m8): keeps 0\n'
        '}\n',
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
        print("usage: f029-r5-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, rel, _, _ in VITEST_MUTATIONS})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    all_ok = True

    # --- control run, before any of the eight mutations --------------------
    print("=" * 78)
    print("--- vitest control run (unmutated, before) ---")
    code, output = _run_vitest(root, "control-first")
    failed, names = _vitest_failed_count_and_names(output)
    print(f"control: exit={code} failed={failed}")
    if code != 0:
        print("VITEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        print(output[-2000:])
        return 1

    # --- the eight vitest-caught mutations ----------------------------------
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

    # --- restore verification ------------------------------------------------
    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    # --- control run, after the full sweep -----------------------------------
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
