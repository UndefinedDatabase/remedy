#!/usr/bin/env python3
"""Mutation-testing tool for F019 T001's brainReducer.

Given a worktree path, runs an unmutated vitest control first and last, and
between them applies each mutation below to one file (brainReducer.ts unless
noted), runs vitest, restores the file BYTE-IDENTICAL, and reports the number
of failed tests and the exit code. m3 and m12 mutate brainOntology.ts instead
of brainReducer.ts, because this design puts SEED_STATUS_STATE_TABLE and
REVIEW_OUTCOME_STATE_TABLE there, not in brainReducer.ts.

Usage: python3 mutations.py <worktree_root>
  <worktree_root> is the repo root of the worktree, e.g.
  /home/decodeux/Repos/remedy/.remedy-wt/f019-r1-proto
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r1-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

REDUCER_REL = "apps/ui/src/components/graph/brainReducer.ts"
ONTOLOGY_REL = "apps/ui/src/components/graph/brainOntology.ts"
TEST_REL = "apps/ui/src/components/graph/brainReducer.test.ts"


MUTATIONS = [
    {
        "id": "m1",
        "name": "idempotence guard removed (replayed seq re-applied)",
        "file": REDUCER_REL,
        "from": '  if (model.lastSeq !== null && row.seq <= model.lastSeq) return model;\n',
        "to": '',
    },
    {
        "id": "m2",
        "name": "task_run_started no longer closes a previous open run",
        "file": REDUCER_REL,
        "from": '  const closed = closeOpenRuns(born.nodes, row.taskId);\n',
        "to": '  const closed = born.nodes;\n',
    },
    {
        "id": "m3",
        "name": "needs_repair mapped to pass",
        "file": ONTOLOGY_REL,
        "from": '  needs_repair: "fail",\n',
        "to": '  needs_repair: "pass",\n',
    },
    {
        "id": "m4",
        "name": "rebuildBrainModel does not sort rows",
        "file": REDUCER_REL,
        "from": '  const ordered = [...bySeq.values()].sort((a, b) => a.seq - b.seq);\n',
        "to": '  const ordered = [...bySeq.values()];\n',
    },
    {
        "id": "m5",
        "name": "rebuildBrainModel does not drop duplicate seqs (first wins broken: last wins instead)",
        # NOTE: a literal "delete the dedup step, sort what's left" mutation is
        # PROVABLY UNOBSERVABLE here: Array.prototype.sort is stable, so a
        # same-seq row keeps its original relative order after sorting, and
        # reduceBrainEvent's own `lastSeq` guard then skips every row at or
        # behind the position already applied — which, for two same-seq rows,
        # is exactly "keep the one that came first in the input". The dedup
        # Map and the guard independently enforce the identical outcome for
        # this case, so deleting the Map changes no test's result. This
        # variant instead breaks WHICH duplicate wins (last overwrites first
        # in the Map, still ahead of the guard), which the guard does NOT
        # independently protect against, and IS observable.
        "file": REDUCER_REL,
        "from": (
            '  const bySeq = new Map<number, BrainEventRow>();\n'
            '  for (const row of rows) {\n'
            '    if (!bySeq.has(row.seq)) bySeq.set(row.seq, row);\n'
            '  }\n'
        ),
        "to": (
            '  const bySeq = new Map<number, BrainEventRow>();\n'
            '  for (const row of rows) {\n'
            '    bySeq.set(row.seq, row);\n'
            '  }\n'
        ),
    },
    {
        "id": "m6",
        "name": "core state stored/not derived (derivation returns 'planned' always)",
        "file": REDUCER_REL,
        "from": (
            '  if (runs.some((r) => r.state === "in_progress")) return "in_progress";\n'
            '  if (tasks.some((t) => t.state === "fail" || t.state === "blocked")) return "fail";\n'
            '  if (tasks.length > 0 && tasks.every((t) => t.state === "pass")) return "pass";\n'
            '  return "planned";\n'
        ),
        "to": '  return "planned";\n',
    },
    {
        "id": "m7",
        "name": "cluster keeps an extra run (threshold off by one)",
        "file": REDUCER_REL,
        "from": 'export function clusterBrainModel(model: BrainModel, threshold = 8): BrainModel {',
        "to": 'export function clusterBrainModel(model: BrainModel, threshold = 9): BrainModel {',
    },
    {
        "id": "m8",
        "name": "unknown kinds not counted in ignored",
        "file": REDUCER_REL,
        "from": '    default:\n      return ignoreRow(model, row);\n',
        "to": '    default:\n      return model;\n',
    },
    {
        "id": "m9",
        "name": "builder_started counted in ignored",
        "file": REDUCER_REL,
        "from": (
            '    case "builder_started":\n'
            '    case "builder_completed":\n'
            '      // Measured writer, deliberately silent: the builder_run node is born\n'
            '      // by task_run_started, not by either of these (DECISION F019 D1), and unlike\n'
            '      // an unhandled kind these are NOT counted in `ignored`.\n'
            '      return model;\n'
        ),
        "to": (
            '    case "builder_started":\n'
            '    case "builder_completed":\n'
            '      return ignoreRow(model, row);\n'
        ),
    },
    {
        "id": "m10",
        "name": "unseeded task not born",
        "file": REDUCER_REL,
        "from": (
            '  const id = taskNodeId(taskId);\n'
            '  if (nodes.some((n) => n.id === id)) return { nodes: [...nodes], links: [...links] };\n'
            '  const coreId = nodes[0].id;\n'
            '  const highestRank = nodes.reduce(\n'
            '    (max, n) => (n.kind === "task" ? Math.max(max, n.meta.rank as number) : max),\n'
            '    -1,\n'
            '  );\n'
            '  const born: BrainNode = {\n'
            '    id, kind: "task", state: "planned", parentId: coreId, seq, meta: { rank: highestRank + 1 },\n'
            '  };\n'
            '  return { nodes: [...nodes, born], links: [...links, linkFor(coreId, id)] };\n'
        ),
        "to": '  return { nodes: [...nodes], links: [...links] };\n',
    },
    {
        "id": "m11",
        "name": "job_stopped leaves runs in_progress",
        "file": REDUCER_REL,
        "from": '    if (isRunKind(n.kind) && n.state === "in_progress") return { ...n, state: "blocked" as NodeState };\n',
        "to": '',
    },
    {
        "id": "m12",
        "name": "Table 1 maps applied_to_job_workspace to planned",
        "file": ONTOLOGY_REL,
        "from": '  applied_to_job_workspace: "pass",\n',
        "to": '  applied_to_job_workspace: "planned",\n',
    },
    {
        "id": "m13",
        "name": "run id restored to a per-task counter, not birth seq (the ghost bug this fix removed)",
        # This is the R1 reviewer correction itself, inverted: reintroduce
        # `nextRunNumber` and route all three run-birthing call sites back
        # through it instead of `row.seq`. Multiple edits are needed because
        # the fix touched four distinct locations; each `from` string below
        # is still asserted to occur exactly once before being applied.
        "file": REDUCER_REL,
        "edits": [
            {
                "from": (
                    'function runNodeId(taskId: string, seq: number): string {\n'
                    '  return `run:${taskId}:${seq}`;\n'
                    '}\n'
                ),
                "to": (
                    'function runNodeId(taskId: string, seq: number): string {\n'
                    '  return `run:${taskId}:${seq}`;\n'
                    '}\n'
                    'function nextRunNumber(nodes: readonly BrainNode[], taskId: string): number {\n'
                    '  const parent = taskNodeId(taskId);\n'
                    '  return 1 + nodes.filter((n) => isRunKind(n.kind) && n.parentId === parent).length;\n'
                    '}\n'
                ),
            },
            {
                "from": (
                    '  const closed = closeOpenRuns(born.nodes, row.taskId);\n'
                    '  const runId = runNodeId(row.taskId, row.seq);\n'
                ),
                "to": (
                    '  const closed = closeOpenRuns(born.nodes, row.taskId);\n'
                    '  const runId = runNodeId(row.taskId, nextRunNumber(closed, row.taskId));\n'
                ),
            },
            {
                "from": (
                    '  const runId = runNodeId(row.taskId, row.seq);\n'
                    '  const state = REVIEW_OUTCOME_STATE_TABLE[row.outcome] ?? "planned";\n'
                ),
                "to": (
                    '  const runId = runNodeId(row.taskId, nextRunNumber(born.nodes, row.taskId));\n'
                    '  const state = REVIEW_OUTCOME_STATE_TABLE[row.outcome] ?? "planned";\n'
                ),
            },
            {
                "from": (
                    '  const runId = runNodeId(row.taskId, row.seq);\n'
                    '  const nodes: BrainNode[] = [\n'
                    '    ...born.nodes,\n'
                    '    { id: runId, kind: "test_run",'
                ),
                "to": (
                    '  const runId = runNodeId(row.taskId, nextRunNumber(born.nodes, row.taskId));\n'
                    '  const nodes: BrainNode[] = [\n'
                    '    ...born.nodes,\n'
                    '    { id: runId, kind: "test_run",'
                ),
            },
        ],
    },
]


def edits_of(mut: dict) -> list:
    """Normalize a mutation to its list of (from, to) edits, applied in order."""
    if "edits" in mut:
        return mut["edits"]
    return [{"from": mut["from"], "to": mut["to"]}]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_vitest(worktree: Path, tag: str) -> dict:
    """Run vitest over exactly brainReducer.test.ts in the worktree, with a
    FRESH cacheDir per invocation so no run can see a stale transform cache
    from a previous mutation."""
    cache_dir = HELPER_DIR / f"mutation-cache-{tag}-{int(time.time() * 1000)}"
    config_path = HELPER_DIR / f"vitest.config.mutation.{tag}.mjs"
    test_abs = worktree / TEST_REL
    config_path.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        "  test: {\n"
        '    environment: "node",\n'
        f'    include: ["{test_abs}"],\n'
        "  },\n"
        "};\n"
    )
    proc = subprocess.run(
        [str(VITEST_BIN), "run", "--config", str(config_path)],
        cwd=str(PRIMARY_UI),
        capture_output=True,
        text=True,
        timeout=120,
    )
    out = proc.stdout + proc.stderr
    m = re.search(r"Tests\s+(\d+)\s+failed\s*\|\s*(\d+)\s+passed", out)
    if m:
        failed, passed = int(m.group(1)), int(m.group(2))
    else:
        m2 = re.search(r"Tests\s+(\d+)\s+passed", out)
        if m2:
            failed, passed = 0, int(m2.group(1))
        else:
            failed, passed = -1, -1  # could not parse; treat as unknown
    return {"exit_code": proc.returncode, "failed": failed, "passed": passed, "raw_tail": out[-1200:]}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    print(f"worktree: {worktree}")
    print("=" * 78)
    print("CONTROL RUN #1 (unmutated, before any mutation)")
    before = run_vitest(worktree, "control-first")
    print(f"  exit_code={before['exit_code']} failed={before['failed']} passed={before['passed']}")
    if before["exit_code"] != 0 or before["failed"] != 0:
        print("  !! control run #1 is not green; aborting mutation sweep.")
        print(before["raw_tail"])
        return 1

    results = []
    for mut in MUTATIONS:
        target = worktree / mut["file"]
        original_bytes = target.read_bytes()
        original_hash = sha256_of(target)
        text = original_bytes.decode("utf-8")
        edits = edits_of(mut)
        print("-" * 78)
        print(f"{mut['id']}: {mut['name']}  [{mut['file']}]  ({len(edits)} edit(s))")

        bad_occurrences = None
        mutated = text
        for i, edit in enumerate(edits):
            occurrences = mutated.count(edit["from"])
            if occurrences != 1:
                bad_occurrences = (i, occurrences)
                break
            mutated = mutated.replace(edit["from"], edit["to"], 1)
        if bad_occurrences is not None:
            i, occurrences = bad_occurrences
            print(f"  !! edit[{i}] FROM string occurs {occurrences} times (expected exactly 1); skipping mutation.")
            results.append({**mut, "skipped": True, "occurrences": occurrences})
            continue

        target.write_bytes(mutated.encode("utf-8"))
        try:
            result = run_vitest(worktree, mut["id"])
        finally:
            target.write_bytes(original_bytes)
        restored_ok = sha256_of(target) == original_hash
        print(f"  exit_code={result['exit_code']} failed={result['failed']} passed={result['passed']}")
        print(f"  restored byte-identical: {restored_ok}")
        turned_red = result["exit_code"] != 0 and result["failed"] != 0
        print(f"  turned at least one test red: {turned_red}")
        if not turned_red:
            print("  !! MUTATION SURVIVED GREEN — needs a strengthened test.")
        results.append({
            **mut, "skipped": False, "restored_ok": restored_ok,
            "exit_code": result["exit_code"], "failed": result["failed"],
            "passed": result["passed"], "turned_red": turned_red,
        })

    print("=" * 78)
    print("CONTROL RUN #2 (unmutated, after the full sweep)")
    after = run_vitest(worktree, "control-last")
    print(f"  exit_code={after['exit_code']} failed={after['failed']} passed={after['passed']}")

    print("=" * 78)
    print("SUMMARY")
    all_ok = before["exit_code"] == 0 and after["exit_code"] == 0
    for r in results:
        if r.get("skipped"):
            print(f"  {r['id']}: SKIPPED (from-string occurrences={r['occurrences']})")
            all_ok = False
            continue
        status = "RED (caught)" if r["turned_red"] else "GREEN (SURVIVED — needs a stronger test)"
        restored = "restored OK" if r["restored_ok"] else "RESTORE MISMATCH"
        print(f"  {r['id']}: {status}, failed={r['failed']}, exit={r['exit_code']}, {restored}")
        if not r["turned_red"] or not r["restored_ok"]:
            all_ok = False

    print("=" * 78)
    print(f"control #1 green: {before['exit_code'] == 0 and before['failed'] == 0}")
    print(f"control #2 green: {after['exit_code'] == 0 and after['failed'] == 0}")
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
