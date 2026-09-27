#!/usr/bin/env python3
"""F288 R5 G5 — the round's mutation-and-red-proof tool (DECISION F288 D5, T003).

Usage:
    python3 f288-r5-mutations.py <worktree-path>

For each of the round's ten ordered mutations, this tool edits the named file
INSIDE <worktree-path> (asserting its FROM text occurs EXACTLY ONCE first),
runs the mutation's own runner over its ordered tests, restores the file's
original bytes, and reports the mutation's label, the run's real exit code,
its failed count and failing test names.

Two runners, m1-m8 TypeScript (vitest) and m9-m10 Python (pytest) — an
unmutated CONTROL run opens and closes each runner's own block. Before the
TypeScript block, one ROUTE PROOF (not itself one of the ten) breaks
`promptNodes.ts` at its own syntax so no importer's module graph resolves —
proving the vitest scratch config reads the WORKTREE's own sources and not
the primary checkout's, whatever any one test happens to import.

Python mutations (m9, m10) run:
    python3 -B -m pytest -q -p no:cacheprovider tests/ui_contracts/test_brain_stage_mount.py
    tests/ui_contracts/test_timeline_scrub_wiring.py
from the worktree's root, after purging its __pycache__ directories.

TypeScript mutations (m1-m8) run:
    <primary>/apps/ui/node_modules/.bin/vitest run --config <scratch config>
from the primary checkout's apps/ui, where the scratch config exports a plain
object: `root` the primary apps/ui, `cacheDir` under `.remedy-wt/`, and
`test.include` the worktree's own promptNodes.test.ts, brainView.test.ts and
buildForceBrainModel.test.ts, by absolute path.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PRIMARY_ROOT = Path("/home/decodeux/Repos/remedy")
PRIMARY_UI = PRIMARY_ROOT / "apps" / "ui"
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"
WORKER_DIR = PRIMARY_ROOT / ".remedy-wt" / "f288-r5-worker"
SCRATCH_CONFIG = WORKER_DIR / "vitest.f288-r5-mutations.config.mjs"
SCRATCH_CACHE_DIR = PRIMARY_ROOT / ".remedy-wt" / "f288-r5-vite-cache"

PY_TESTS = [
    "tests/ui_contracts/test_brain_stage_mount.py",
    "tests/ui_contracts/test_timeline_scrub_wiring.py",
]
TS_TEST_RELPATHS = [
    "apps/ui/src/components/graph/promptNodes.test.ts",
    "apps/ui/src/components/graph/brainView.test.ts",
    "apps/ui/src/components/graph/buildForceBrainModel.test.ts",
]


@dataclass(frozen=True)
class Mutation:
    label: str
    rel_path: str
    from_text: str
    to_text: str
    runner: str  # "py" or "ts"


ROUTE_PROOF = Mutation(
    "ROUTE PROOF — promptNodes.ts broken at its own syntax so the worktree's "
    "module graph cannot resolve for any importer, whatever it imports",
    "apps/ui/src/components/graph/promptNodes.ts",
    "  };\n}\n",
    "  };\n}\n\nexport const __ROUTE_PROOF_SYNTAX_ERROR__ = (((;\n",
    "ts",
)

MUTATIONS = [
    Mutation(
        "m1 withPromptNodes births an orphan item (its task absent) under the core instead of skipping it",
        "apps/ui/src/components/graph/promptNodes.ts",
        "    if (taskState === undefined) continue;\n",
        (
            "    if (taskState === undefined) {\n"
            "      const orphanId = promptNodeId(item.id);\n"
            "      bornNodes.push({ id: orphanId, kind: \"synapse\", state: model.nodes[0].state, "
            "parentId: model.nodes[0].id, seq: 0, meta: { promptId: item.id, role: item.role, "
            "promptKind: item.promptKind, round: item.round, attemptId: item.runId } });\n"
            "      bornLinks.push({ id: `${model.nodes[0].id}->${orphanId}`, source: model.nodes[0].id, target: orphanId });\n"
            "      continue;\n"
            "    }\n"
        ),
        "ts",
    ),
    Mutation(
        "m2 a synapse's state is always \"pass\"",
        "apps/ui/src/components/graph/promptNodes.ts",
        "      state: taskState,\n",
        "      state: \"pass\",\n",
        "ts",
    ),
    Mutation(
        "m3 a synapse's parent is the core instead of its task",
        "apps/ui/src/components/graph/promptNodes.ts",
        "      parentId: taskId,\n",
        "      parentId: model.nodes[0].id,\n",
        "ts",
    ),
    Mutation(
        "m4 withPromptNodes answers a NEW object when it appends nothing",
        "apps/ui/src/components/graph/promptNodes.ts",
        "  if (bornNodes.length === 0) return model;\n",
        "  if (bornNodes.length === 0) return { ...model };\n",
        "ts",
    ),
    Mutation(
        "m5 a repeated item is born twice",
        "apps/ui/src/components/graph/promptNodes.ts",
        "    if (knownIds.has(id)) continue;\n    knownIds.add(id);\n",
        "    knownIds.add(id);\n",
        "ts",
    ),
    Mutation(
        "m6 selectionIdOf answers the parent task id for a synapse",
        "apps/ui/src/components/graph/brainView.ts",
        "    return node.id.slice(\"prompt:\".length);\n",
        "    return selectionTaskIdOf(node);\n",
        "ts",
    ),
    Mutation(
        "m7 selectedPromptNodeId answers null for a matching id",
        "apps/ui/src/components/graph/brainView.ts",
        "  return items.some((item) => item.id === selectedNodeId) ? promptNodeId(selectedNodeId) : null;\n",
        "  return null;\n",
        "ts",
    ),
    Mutation(
        "m8 a synapse is laid out at BRAIN_RUN_RADIUS",
        "apps/ui/src/components/graph/buildForceBrainModel.ts",
        "    const radius = n.kind === \"cluster\"\n"
        "      ? BRAIN_CLUSTER_RADIUS\n"
        "      : n.kind === \"synapse\" ? BRAIN_SYNAPSE_RADIUS : BRAIN_RUN_RADIUS;\n",
        "    const radius = n.kind === \"cluster\"\n"
        "      ? BRAIN_CLUSTER_RADIUS\n"
        "      : BRAIN_RUN_RADIUS;\n",
        "ts",
    ),
    Mutation(
        "m9 the stage composes the prompts onto `model` instead of `liveModel`",
        "apps/ui/src/components/graph/BrainGraphStage.tsx",
        (
            "  const liveModel = useMemo(() => withPromptNodes(rebuildBrainModel(dashboard.jobId, seeds, rows), promptItems), [dashboard.jobId, seeds, rows, promptItems]);\n"
            "  // While the timeline is scrubbed the stage draws the reducer state of the\n"
            "  // prefix at the handle, and the live model waits behind LIVE (DECISION F024 D4).\n"
            "  const model = scrub.scrubbedModel ?? liveModel;\n"
        ),
        (
            "  const liveModel = useMemo(() => rebuildBrainModel(dashboard.jobId, seeds, rows), [dashboard.jobId, seeds, rows]);\n"
            "  // While the timeline is scrubbed the stage draws the reducer state of the\n"
            "  // prefix at the handle, and the live model waits behind LIVE (DECISION F024 D4).\n"
            "  const model = withPromptNodes(scrub.scrubbedModel ?? liveModel, promptItems);\n"
        ),
        "py",
    ),
    Mutation(
        "m10 ForceBrainGraph's click calls selectionTaskIdOf(n) again",
        "apps/ui/src/components/graph/ForceBrainGraph.tsx",
        "    const id = selectionIdOf(n);\n",
        "    const id = selectionTaskIdOf(n);\n",
        "py",
    ),
]

def purge_pycache(root: Path) -> None:
    for d in root.rglob("__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def write_scratch_config(worktree: Path) -> None:
    WORKER_DIR.mkdir(parents=True, exist_ok=True)
    includes = ",\n      ".join(
        f'"{(worktree / rel).as_posix()}"' for rel in TS_TEST_RELPATHS
    )
    config = (
        "export default {\n"
        f'  root: "{PRIMARY_UI.as_posix()}",\n'
        f'  cacheDir: "{SCRATCH_CACHE_DIR.as_posix()}",\n'
        "  test: {\n"
        '    environment: "node",\n'
        "    include: [\n"
        f"      {includes}\n"
        "    ],\n"
        "  },\n"
        "};\n"
    )
    SCRATCH_CONFIG.write_text(config, encoding="utf-8")


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return proc.returncode, proc.stdout


def pytest_failed_count_and_names(output: str) -> tuple[int, list[str]]:
    names = sorted(set(re.findall(r"^FAILED (\S+)", output, re.MULTILINE)))
    m = re.search(r"(\d+) failed", output)
    count = int(m.group(1)) if m else 0
    if m is None and re.search(r"^ERROR ", output, re.MULTILINE):
        count = len(re.findall(r"^ERROR ", output, re.MULTILINE)) or count
    return count, names


def vitest_failed_count_and_names(output: str) -> tuple[int, list[str]]:
    # The " FAIL  <file> > <suite> > <test>" lines in vitest's own "Failed
    # Tests" section carry the full name once each; the tree view above it
    # (×/✗ markers) repeats the same names with a timing suffix, which would
    # only duplicate this list, so it is deliberately not matched here.
    names = sorted(set(re.findall(r"^\s*FAIL\s+(.+)$", output, re.MULTILINE)))
    m = re.search(r"Tests\s+(\d+) failed", output)
    if m is not None:
        count = int(m.group(1))
    else:
        # A hard failure (e.g. a broken module graph: no test even collected)
        # still counts as a red run of 1 for reporting purposes.
        count = 1 if names or re.search(r"\bError\b", output) else 0
    return count, names


def run_py_tests(worktree: Path) -> tuple[int, int, list[str]]:
    purge_pycache(worktree)
    code, out = run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PY_TESTS],
        cwd=worktree,
    )
    failed, names = pytest_failed_count_and_names(out)
    return code, failed, names


def run_ts_tests(worktree: Path) -> tuple[int, int, list[str]]:
    write_scratch_config(worktree)
    code, out = run(
        [str(VITEST_BIN), "run", "--config", str(SCRATCH_CONFIG)],
        cwd=PRIMARY_UI,
    )
    failed, names = vitest_failed_count_and_names(out)
    return code, failed, names


def apply_edit(path: Path, from_text: str, to_text: str) -> str:
    original = path.read_text(encoding="utf-8")
    if original.count(from_text) != 1:
        raise SystemExit(f"FROM text does not occur exactly once in {path}: {original.count(from_text)}")
    path.write_text(original.replace(from_text, to_text, 1), encoding="utf-8")
    return original


def restore(path: Path, original: str) -> bool:
    path.write_text(original, encoding="utf-8")
    return path.read_text(encoding="utf-8") == original


def report_run(label: str, runner: str, code: int, failed: int, names: list[str]) -> None:
    print(f"[{runner}] {label}")
    print(f"  exit={code} failed={failed}")
    for n in names:
        print(f"    failing: {n}")


def main() -> None:
    worktree = Path(sys.argv[1]).resolve()

    print("=== ROUTE PROOF (before any of the ten mutations) ===")
    rp_path = worktree / ROUTE_PROOF.rel_path
    rp_original = apply_edit(rp_path, ROUTE_PROOF.from_text, ROUTE_PROOF.to_text)
    code, failed, names = run_ts_tests(worktree)
    report_run(ROUTE_PROOF.label, "ts", code, failed, names)
    route_proof_red = code != 0
    ok = restore(rp_path, rp_original)
    print(f"  restored byte-identical: {ok}")
    if not route_proof_red:
        print("  ROUTE PROOF DID NOT REDDEN — the vitest route is not reading the worktree's sources.")

    all_caught = route_proof_red
    restored_all = ok

    print("\n=== TypeScript runner (vitest): control, then m1-m8, then control ===")
    code, failed, names = run_ts_tests(worktree)
    report_run("CONTROL (unmutated)", "ts", code, failed, names)
    ts_control_before_green = code == 0
    all_caught = all_caught and ts_control_before_green

    for mutation in MUTATIONS:
        if mutation.runner != "ts":
            continue
        path = worktree / mutation.rel_path
        original = apply_edit(path, mutation.from_text, mutation.to_text)
        code, failed, names = run_ts_tests(worktree)
        report_run(mutation.label, "ts", code, failed, names)
        red = code != 0
        if not red:
            print("  GREEN — this mutation was NOT caught.")
        all_caught = all_caught and red
        ok = restore(path, original)
        restored_all = restored_all and ok
        print(f"  restored byte-identical: {ok}")

    code, failed, names = run_ts_tests(worktree)
    report_run("CONTROL (unmutated)", "ts", code, failed, names)
    ts_control_after_green = code == 0
    all_caught = all_caught and ts_control_after_green

    print("\n=== Python runner (pytest): control, then m9-m10, then control ===")
    code, failed, names = run_py_tests(worktree)
    report_run("CONTROL (unmutated)", "py", code, failed, names)
    py_control_before_green = code == 0
    all_caught = all_caught and py_control_before_green

    for mutation in MUTATIONS:
        if mutation.runner != "py":
            continue
        path = worktree / mutation.rel_path
        original = apply_edit(path, mutation.from_text, mutation.to_text)
        code, failed, names = run_py_tests(worktree)
        report_run(mutation.label, "py", code, failed, names)
        red = code != 0
        if not red:
            print("  GREEN — this mutation was NOT caught.")
        all_caught = all_caught and red
        ok = restore(path, original)
        restored_all = restored_all and ok
        print(f"  restored byte-identical: {ok}")

    code, failed, names = run_py_tests(worktree)
    report_run("CONTROL (unmutated)", "py", code, failed, names)
    py_control_after_green = code == 0
    all_caught = all_caught and py_control_after_green

    print(f"\nALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {bool(all_caught and restored_all)}")


if __name__ == "__main__":
    main()
