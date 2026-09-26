#!/usr/bin/env python3
"""F027 R7 G5 — the red proofs for the dashboard's `vetoes` section, the reason verbatim
in the job's text and exported reports, the proposal's option labels, the page's veto
event names, the vetoed seed and stream case, and the inbox's option-label lookup
(DECISION F027 D7).

Takes a worktree path. Runs an unmutated PYTEST control (over the round's four pytest
node ids) and an unmutated VITEST control (over the round's four changed `.test.ts`
files, through a scratch vitest config that reads the WORKTREE's own sources via the
PRIMARY checkout's `apps/ui/node_modules` — DECISION F256 D6's route, since a worktree
carries no `node_modules` of its own) first and last. BEFORE the ordered mutations, one
CANARY mutation proves that route really reads the worktree's sources rather than the
primary checkout's: it breaks an import no test can resolve, so a green run there would
mean the route silently fell back to the primary tree's unmutated file.

For each of the eleven ordered mutations below: edits the named file INSIDE the worktree
(asserting its FROM text occurs exactly once), purges the worktree's `__pycache__`
directories for a Python mutation, runs the matching test runner, restores the bytes
BYTE-IDENTICAL, and reports the mutation's label, the run's real exit code, the failed
count and the failing test names/ids. Ends with `restored byte-identical: <bool>` per
touched file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f027-r7-mutations.py <worktree-path>
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
MUTSCRATCH_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f027-r7-worker/vitest-scratch")

UI_SERVER = "packages/orchestration/ui_server.py"
PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
VETO_PROPOSAL = "packages/orchestration/veto_proposal.py"
HUMANIZE_CATALOG = "apps/ui/src/api/humanizeCatalog.ts"
BRAIN_ONTOLOGY = "apps/ui/src/components/graph/brainOntology.ts"
BRAIN_REDUCER = "apps/ui/src/components/graph/brainReducer.ts"
DECISION_CARD = "apps/ui/src/api/decisionCard.ts"
REMEDY_API = "apps/ui/src/api/remedyApi.ts"

PYTEST_NODE_IDS = [
    "tests/ui_server/test_dashboard_vetoes.py",
    "tests/orchestration/test_task_veto_runner.py",
    "tests/orchestration/test_veto_proposal.py",
    "tests/ui_contracts/test_humanize_catalog.py",
]

VITEST_TEST_RELS = [
    "apps/ui/src/api/decisionCard.test.ts",
    "apps/ui/src/api/remedyApi.test.ts",
    "apps/ui/src/components/graph/brainView.test.ts",
    "apps/ui/src/components/graph/brainReducer.test.ts",
]

# Each mutation names one real behaviour this round adds: an exact FROM string, replaced
# by an exact TO string. FROM must occur exactly once in the pristine file.
PYTEST_MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 _build_veto_section lets a TaskVetoError out",
        UI_SERVER,
        '    except _tv.TaskVetoError as exc:\n'
        '        return {"tasks": [], "vetoable_task_ids": [], "unreachable_task_ids": [], '
        '"error": str(exc)}\n',
        '    except ValueError as exc:  # MUTATED (m1): TaskVetoError no longer caught here\n'
        '        return {"tasks": [], "vetoable_task_ids": [], "unreachable_task_ids": [], '
        '"error": str(exc)}\n',
    ),
    (
        "m2 the section's unreachable_task_ids is always empty",
        UI_SERVER,
        '        unreachable_task_ids = list(_tv.veto_unreachable(job.tasks, vetoed_ids))\n',
        '        unreachable_task_ids = []  # MUTATED (m2): always empty\n',
    ),
    (
        "m3 the text report drops the Vetoed by line",
        PINGPONG_JOB,
        '        veto_info = veto_map.get(t.task_id)\n'
        '        if veto_info is not None:\n'
        '            lines.append(\n'
        '                f"      Vetoed by {veto_info.get(\'actor\', \'\')}: '
        '{veto_info.get(\'reason\', \'\')}"\n'
        '            )\n',
        '        veto_info = veto_map.get(t.task_id)\n'
        '        if False:  # MUTATED (m3): Vetoed by line disabled\n'
        '            lines.append(\n'
        '                f"      Vetoed by {veto_info.get(\'actor\', \'\')}: '
        '{veto_info.get(\'reason\', \'\')}"\n'
        '            )\n',
    ),
    (
        "m4 export_job_report drops the veto object",
        PINGPONG_JOB,
        '        veto_info = veto_map.get(t.task_id)\n'
        '        if veto_info is not None:\n'
        '            report["veto"] = {\n'
        '                "reason": veto_info.get("reason", ""),\n'
        '                "actor": veto_info.get("actor", ""),\n'
        '                "requested_at": veto_info.get("requested_at", ""),\n'
        '                "unreachable_task_ids": list(veto_info.get("unreachable_task_ids") '
        'or []),\n'
        '            }\n',
        '        veto_info = veto_map.get(t.task_id)\n'
        '        if False:  # MUTATED (m4): veto object never attached\n'
        '            report["veto"] = {\n'
        '                "reason": veto_info.get("reason", ""),\n'
        '                "actor": veto_info.get("actor", ""),\n'
        '                "requested_at": veto_info.get("requested_at", ""),\n'
        '                "unreachable_task_ids": list(veto_info.get("unreachable_task_ids") '
        'or []),\n'
        '            }\n',
    ),
    (
        "m5 the proposal's payload drops option_labels",
        VETO_PROPOSAL,
        '                "option_labels": dict(_OPTION_LABELS),\n',
        '',
    ),
    (
        "m6 task_vetoed leaves the page's catalog",
        HUMANIZE_CATALOG,
        '  "task_vetoed": "A task was vetoed and struck from the run.",\n',
        '',
    ),
]

VITEST_MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m7 SEED_STATUS_STATE_TABLE loses its vetoed row",
        BRAIN_ONTOLOGY,
        '  vetoed: "vetoed",\n',
        '',
    ),
    (
        "m8 the task_vetoed case paints vetoed over a passed node",
        BRAIN_REDUCER,
        '  const state: NodeState = current && current.state === "pass" ? current.state : '
        '"vetoed";\n',
        '  const state: NodeState = "vetoed";  // MUTATED (m8): guard removed\n',
    ),
    (
        "m9 decisionAnswers ignores option_labels",
        DECISION_CARD,
        '    const optionLabels = payloadOptionLabels(card.payload);\n'
        '    const labelFor = optionLabels ? (value: string) => optionLabels[value] ?? value '
        ': undefined;\n'
        '    return entriesAsAnswers(options, "option", posts, outcomeFor, labelFor);\n',
        '    const optionLabels = payloadOptionLabels(card.payload);\n'
        '    const labelFor = optionLabels ? (value: string) => optionLabels[value] ?? value '
        ': undefined;\n'
        '    return entriesAsAnswers(options, "option", posts, outcomeFor);  // MUTATED (m9)\n',
    ),
    (
        "m10 decisionAnswers posts the label instead of the value",
        DECISION_CARD,
        '      kind,\n'
        '      label: labelFor(text),\n'
        '      value: text,\n',
        '      kind,\n'
        '      label: labelFor(text),\n'
        '      value: labelFor(text),  // MUTATED (m10): posts the label instead of the value\n',
    ),
    (
        "m11 the normalizer drops each veto's reason",
        REMEDY_API,
        '    reason: typeof r.reason === "string" ? r.reason : "",\n',
        '    reason: "",  // MUTATED (m11): reason dropped\n',
    ),
]

# The canary (not one of the ordered eleven): breaks an import no vitest run can resolve,
# so a run over the scratch config that stayed GREEN would mean it silently read the
# PRIMARY checkout's unmutated file instead of the worktree's.
CANARY: tuple[str, str, str, str] = (
    "canary: proves the vitest route reads the WORKTREE's own sources",
    BRAIN_ONTOLOGY,
    "// Types and literal lookup tables the reducer counts on.",
    'import { __f027_r7_canary__ } from "./__no_such_module_f027_r7__";\n'
    '// Types and literal lookup tables the reducer counts on.',
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
        print("usage: f027-r7-mutations.py <worktree-path>", file=sys.stderr)
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
        print(f"  the broken import turned the run red: {caught}")
        if not caught:
            print("  !! THE ROUTE DID NOT REACH THE WORKTREE'S SOURCE — aborting.")
            print(output[-2000:])
            return 1
    finally:
        canary_path.write_bytes(canary_original)
    restored = canary_path.read_bytes() == canary_original
    print(f"  canary file restored byte-identical: {restored}")
    all_ok = all_ok and restored

    # --- control runs, before any of the eleven mutations ---------------------------
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

    # --- the eleven ordered mutations -------------------------------------------------
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
