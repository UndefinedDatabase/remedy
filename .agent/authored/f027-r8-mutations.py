#!/usr/bin/env python3
"""F027 R8 G5 — the red proofs for the veto's view helpers, its send module, the canvas's
fade and hover wiring, the popover's Veto/Unreachable sections and form, and the shell's
task-to-task jump (DECISION F027 D8).

Takes a worktree path. Runs an unmutated PYTEST control (over the round's one contract
node id, `tests/ui_contracts/test_veto_controls_contract.py`) and an unmutated VITEST
control (over the round's three changed `.test.ts` files, through a scratch vitest config
that reads the WORKTREE's own sources via the PRIMARY checkout's `apps/ui/node_modules` —
DECISION F256 D6's route, round 7's own, since a worktree carries no `node_modules` of its
own) first and last. BEFORE the ordered mutations, one CANARY mutation proves that route
really reads the worktree's sources rather than the primary checkout's: it makes the
worktree's `vetoView.ts` throw at module load, a side effect no bundler can tree-shake
away, so a green run there would mean the route silently fell back to the primary tree's
unmutated file.

Ten mutations (m1-m10) touch `vetoView.ts`, `brainView.ts` or `vetoSend.ts` and are proven
red by the vitest route above. Four mutations (m11-m14) touch `ForceBrainGraph.tsx`,
`DetailPopover.tsx` or `RemedyShell.tsx` — none of which has a vitest DOM harness — and are
proven red by the round's own PYTHON contract test, `test_veto_controls_contract.py`,
which reads each file's source as text.

For each of the fourteen ordered mutations below: edits the named file INSIDE the worktree
(asserting its FROM text occurs exactly once), purges the worktree's `__pycache__`
directories for a Python-run mutation, runs the matching test runner, restores the bytes
BYTE-IDENTICAL, and reports the mutation's label, the run's real exit code, the failed
count and the failing test names/ids. Ends with `restored byte-identical: <bool>` per
touched file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f027-r8-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"
MUTSCRATCH_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f027-r8-worker/vitest-scratch")

VETO_VIEW = "apps/ui/src/api/vetoView.ts"
VETO_SEND = "apps/ui/src/api/vetoSend.ts"
BRAIN_VIEW = "apps/ui/src/components/graph/brainView.ts"
FORCE_BRAIN_GRAPH = "apps/ui/src/components/graph/ForceBrainGraph.tsx"
DETAIL_POPOVER = "apps/ui/src/components/detail/DetailPopover.tsx"
REMEDY_SHELL = "apps/ui/src/components/shell/RemedyShell.tsx"

PYTEST_NODE_IDS = [
    "tests/ui_contracts/test_veto_controls_contract.py",
]

VITEST_TEST_RELS = [
    "apps/ui/src/api/vetoView.test.ts",
    "apps/ui/src/api/vetoSend.test.ts",
    "apps/ui/src/components/graph/brainView.test.ts",
]

# The ten TypeScript-caught mutations: an exact FROM string, replaced by an exact TO
# string. FROM must occur exactly once in the pristine file. Caught by the vitest route
# over the three test files above.
VITEST_MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 vetoHoverText drops the reason from the vetoed text",
        VETO_VIEW,
        '  if (vetoed) {\n    return `Vetoed: ${vetoed.reason}`;\n  }\n',
        '  if (vetoed) {\n    return "Vetoed";  // MUTATED (m1): reason dropped\n  }\n',
    ),
    (
        "m2 vetoHoverText names an unreachable task's vetoing task by id instead of title",
        VETO_VIEW,
        '    const titles = vetoing.map((entry) => taskTitleOf(dashboard, entry.taskId));\n',
        '    const titles = vetoing.map((entry) => entry.taskId);  // MUTATED (m2): id, not title\n',
    ),
    (
        "m3 taskVetoAction ignores vetoableTaskIds",
        VETO_VIEW,
        '  if (vetoes.error !== "" || !vetoes.vetoableTaskIds.includes(taskId)) {\n',
        '  if (vetoes.error !== "") {  // MUTATED (m3): vetoableTaskIds ignored\n',
    ),
    (
        "m4 taskVetoAction ignores the section's error",
        VETO_VIEW,
        '  if (vetoes.error !== "" || !vetoes.vetoableTaskIds.includes(taskId)) {\n',
        '  if (!vetoes.vetoableTaskIds.includes(taskId)) {  // MUTATED (m4): error ignored\n',
    ),
    (
        'm5 vetoAnswerSentence("") reads as answered',
        VETO_VIEW,
        '  if (answer === "") {\n    return REPLAN_WAITING_SENTENCE;\n  }\n',
        '  if (answer === "") {\n    return ANSWERED_SENTENCE;  // MUTATED (m5)\n  }\n',
    ),
    (
        "m6 vetoFadedNodeIds drops the task: prefix",
        BRAIN_VIEW,
        '  return new Set(vetoes.unreachableTaskIds.map((id) => `task:${id}`));\n',
        '  return new Set(vetoes.unreachableTaskIds.map((id) => id));  // MUTATED (m6): prefix dropped\n',
    ),
    (
        "m7 buildVetoTaskRequest sends the task as task instead of task_id",
        VETO_SEND,
        '      args: { task_id: taskId, reason },\n',
        '      args: { task: taskId, reason },  // MUTATED (m7): wrong key\n',
    ),
    (
        "m8 buildVetoTaskRequest accepts a blank reason",
        VETO_SEND,
        '  if (taskId === "" || reason.trim() === "" || !isUsableCommandNonce(clientNonce)) {\n',
        '  if (taskId === "" || !isUsableCommandNonce(clientNonce)) {  // MUTATED (m8): blank reason accepted\n',
    ),
    (
        "m9 describeVetoTaskResult reads a 409 task_already_vetoed as the generic refusal",
        VETO_SEND,
        '  if (result.outcome === "refused" && result.status === 409) {\n'
        '    return describeVetoConflict(result.body);\n'
        '  }\n',
        '  if (false) {  // MUTATED (m9): every 409 now falls through to the generic refusal\n'
        '    return describeVetoConflict(result.body);\n'
        '  }\n',
    ),
    (
        "m10 the accepted sentence ignores the size of unreachable",
        VETO_SEND,
        '  const unreachable = Array.isArray(body.unreachable) ? body.unreachable : [];\n'
        '  const count = unreachable.length;\n',
        '  const unreachable = Array.isArray(body.unreachable) ? body.unreachable : [];\n'
        '  const count = 0;  // MUTATED (m10): size ignored\n',
    ),
]

# The four PYTHON-caught mutations: touch a `.tsx` file no vitest harness exercises, and
# are read back as TEXT by `test_veto_controls_contract.py`.
PYTEST_MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m11 ForceBrainGraph.tsx sets the tooltip's text through innerHTML",
        FORCE_BRAIN_GRAPH,
        '    span.textContent = text;\n',
        '    (span as unknown as { innerHTML: string }).innerHTML = text;  // MUTATED (m11)\n',
    ),
    (
        "m12 ForceBrainGraph.tsx's node fade reads 1 instead of VETO_DOWNSTREAM_ALPHA",
        FORCE_BRAIN_GRAPH,
        '    const vetoFade = vetoFaded.has(n.id) ? VETO_DOWNSTREAM_ALPHA : 1;\n',
        '    const vetoFade = vetoFaded.has(n.id) ? 1 : 1;  // MUTATED (m12)\n',
    ),
    (
        "m13 the popover mounts TaskVetoForm without the vetoAction gate",
        DETAIL_POPOVER,
        '      {task && serverToken && vetoAction && (\n',
        '      {task && serverToken && (  // MUTATED (m13): vetoAction gate dropped\n',
    ),
    (
        "m14 RemedyShell.tsx stops passing onSelectTask",
        REMEDY_SHELL,
        ' onSelectTask={(taskId) => onSelectNode(shellSelectionIdOf(dashboard.tasks, taskId))}',
        '',
    ),
]

# The canary (not one of the ordered fourteen): a top-level THROW, not an import — round
# 7's own measured lesson: esbuild's per-file transform elides an unresolvable import
# whose named binding is never referenced, so an import-shaped canary stays green for the
# wrong reason. A throw is a side effect no tree-shaking step can drop, so a run over the
# scratch config that stayed GREEN here would mean it silently read the PRIMARY checkout's
# unmutated file instead of the worktree's. `vetoView.ts` is read directly by
# `vetoView.test.ts` and transitively by `brainView.test.ts` (through `brainView.ts`'s own
# import of it) — one shared dependency is what the route needs proving against, the same
# reach round 7's canary in `brainOntology.ts` proved.
CANARY: tuple[str, str, str, str] = (
    "canary: proves the vitest route reads the WORKTREE's own sources",
    VETO_VIEW,
    'import type { RemedyDashboard, RemedyVetoEntry, RemedyVetoes } from "./types";',
    'import type { RemedyDashboard, RemedyVetoEntry, RemedyVetoes } from "./types";\n\n'
    'throw new Error("F027_R8_CANARY_PROOF_OF_WORKTREE_READ");',
)


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
    the WORKTREE's own absolute test-file paths — DECISION F256 D6's route: a config
    importing `vitest/config` cannot resolve, so this exports a PLAIN OBJECT. A fresh
    `cacheDir` per call keeps one run's transform cache from hiding another's mutation."""
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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f027-r8-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, rel, _, _ in [*PYTEST_MUTATIONS, *VITEST_MUTATIONS]})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    all_ok = True

    # --- the canary, before anything else ------------------------------------------
    print("=" * 78)
    print(CANARY[0])
    canary_path = root / CANARY[1]
    canary_original = _apply_edit(canary_path, CANARY[2], CANARY[3], CANARY[0])
    if canary_original is None:
        return 1
    try:
        code, output = _run_vitest(root, "canary")
        failed, names = _vitest_failed_count_and_names(output)
        caught = code != 0
        print(f"  exit={code} failed={failed} names={names}")
        print(f"  the broken module load turned the run red: {caught}")
        if not caught:
            print("  !! THE ROUTE DID NOT REACH THE WORKTREE'S SOURCE — aborting.")
            print(output[-2000:])
            return 1
    finally:
        canary_path.write_bytes(canary_original)
    restored = canary_path.read_bytes() == canary_original
    print(f"  canary file restored byte-identical: {restored}")
    all_ok = all_ok and restored

    # --- control runs, before any of the fourteen mutations ---------------------------
    print("=" * 78)
    print("--- pytest control run (unmutated, before) ---")
    code, output = _run_pytest(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")
    if code != 0:
        print("PYTEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        return 1

    print("--- vitest control run (unmutated, before) ---")
    code, output = _run_vitest(root, "control-first")
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")
    if code != 0:
        print("VITEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        return 1

    # --- the ten vitest-caught mutations -----------------------------------------------
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

    # --- the four pytest-caught mutations -----------------------------------------------
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
        finally:
            path.write_bytes(original)

    # --- restore verification --------------------------------------------------------
    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    # --- control runs, after the full sweep -------------------------------------------
    print("--- pytest control run (unmutated, after) ---")
    code, output = _run_pytest(root)
    pytest_after_ok = code == 0
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")

    print("--- vitest control run (unmutated, after) ---")
    code, output = _run_vitest(root, "control-last")
    vitest_after_ok = code == 0
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")

    result = all_ok and all_restored and pytest_after_ok and vitest_after_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
