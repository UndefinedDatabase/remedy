# Handoff — F288, round 5

## Session

SESSION 1 of feature F288 · round 5 · rounds so far 5. Context remaining at
handback: comfortable — the round's own derivations (the mutation tool's ten
FROM/TO edits, the scratch vitest config, and the route proof) used a
moderate share of the session's budget; a full context window remains for
the next round.

## Range

Review of `a5ee2dc8`..`HEAD` (`HEAD` is this handback's own commit, `F288 R5
C6`, on `feature/f288-event-stream-completeness`).

## Commits

### f665aefa4 F288 R5 C1: copy round 5 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r5-block.md | 248/0 | copy of this round's block |
| .agent/authored/f288-r5-plan.md | 29/0 | copy of the plan payload |
| .agent/authored/f288-r5-records.diff | 70/0 | copy of the records payload |

Measured insertions: 347 (block's own line count 248 + 99), matching the
block's expectation exactly (and under the 500-line cap).

### f3a5d0354 F288 R5 C2: book round 4's PASS and R-1075's resolution, record D5 and the round 5 plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 48/0 | DECISION F288 D5 |
| .agent/live_review.md | 3/1 | round 4's Gate entry (VERDICT PASS), R-1075's `Landed:` line replaced by `Done:` |
| .agent/plan.md | 8/8 | round 5's plan (payload rewrite) |

Matches the block's expected numstat (48/0, 3/1, 8/8) exactly.

### 800940cad F288 R5 C3: compose the prompt trace onto the live model as synapse nodes at graph_spec's radius
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainOntology.ts | 10/4 | header and `NodeKind` doc comment: `synapse` now born by `promptNodes.ts`, not the reducer (S5) |
| apps/ui/src/components/graph/buildForceBrainModel.test.ts | 37/1 | new test: two synapses under one task, radius 2, link width 1, truth rule holds |
| apps/ui/src/components/graph/buildForceBrainModel.ts | 13/2 | `BRAIN_SYNAPSE_RADIUS`/`BRAIN_SYNAPSE_LINK_WIDTH`; a synapse layout node/link uses them (S3) |
| apps/ui/src/components/graph/promptNodes.test.ts | 102/0 | new file: `promptNodeId`/`withPromptNodes` test coverage (birth, state, orphan skip, dedupe, order, identity) |
| apps/ui/src/components/graph/promptNodes.ts | 70/0 | new module: `promptNodeId`, `withPromptNodes` (S1) |

No insertion count was expected by the block for C3; measured 232 total (7
deletions), under the 500-line cap.

### aec880c25 F288 R5 C4: draw the prompts on the live stage and let a click select the prompt
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/BrainGraphStage.tsx | 20/6 | `promptItems` memo, `liveModel` composes `withPromptNodes`, `selectedId` tries `selectedPromptNodeId` first (S2) |
| apps/ui/src/components/graph/ForceBrainGraph.tsx | 2/2 | click handler calls `selectionIdOf` instead of `selectionTaskIdOf` (S4) |
| apps/ui/src/components/graph/brainView.test.ts | 46/3 | new tests: `selectionIdOf`, `selectedPromptNodeId` |
| apps/ui/src/components/graph/brainView.ts | 25/1 | new `selectionIdOf`, `selectedPromptNodeId` (S4) |
| tests/ui_contracts/test_brain_stage_mount.py | 22/0 | new `TestStageComposesThePromptTraceOntoTheLiveModelOnly` class (S6) |
| tests/ui_contracts/test_timeline_scrub_wiring.py | 1/1 | the one existing assertion re-pinned to the new `liveModel` line (S6) |

No insertion count was expected by the block for C4; measured 116 total (12
deletions), under the 500-line cap.

### 44aa94db4 F288 R5 C5: add the mutation tool for the round's red proofs
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r5-mutations.py | 341/0 | the G5 tool: route proof + 10 ordered mutations, two runners (vitest, pytest) |

No insertion count was expected by the block for C5; measured 341, under the
500-line cap.

### F288 R5 C6: rewrite handoff for round 5 (this commit — a handoff cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f288-r5-test-mut HEAD` (at `aec880c25`,
  before the tool was committed) — succeeded; used to develop and debug the
  mutation tool's mechanics (route proof + all ten mutations) before relying
  on it for the official gate (DEVIATION — see below).
- `python3 .remedy-wt/f288-r5-worker/f288-r5-mutations.py
  .remedy-wt/f288-r5-test-mut` — run twice against this worktree while
  developing the tool's vitest-failure-name regex; both runs ended
  `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove .remedy-wt/f288-r5-test-mut` then `git worktree
  prune` — succeeded; count returned to 70.
- `git worktree add --detach .remedy-wt/f288-r5-mut 44aa94db4` — succeeded
  (the official G5 worktree, at C5).
- `python3 .agent/authored/f288-r5-mutations.py .remedy-wt/f288-r5-mut` —
  the official G5 run, reported whole in this round's reply; real outcome
  `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove .remedy-wt/f288-r5-mut` then `git worktree prune` —
  succeeded; count returned to 70, matching step 4's reading.
- `git push -u origin feature/f288-event-stream-completeness` — reported
  under G6 in this round's reply (run after this file is committed).
- No `gh pr create`, no `gh pr merge`, no branch deletion, no force-push, no
  `git stash`, no `git checkout`/`git switch` in the primary checkout.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table):
- `records.diff`: 70 lines, 15367 bytes, sha256
  `bbeb1c63325b84676f19b966ac20544b4de8a6eb3b19e27452e59880779f18d3` — MATCH.
- `plan.md`: 29 lines, 1056 bytes, sha256
  `25d4fd0efb47e045a29bd9bae3574c551f823ea5781bb3359a6ecc385c14d954` — MATCH.

Each `.agent/authored/f288-r5-*` copy, read back with `git show
f665aefa4:<path>`, compared byte-for-byte (Python, not `diff`) with its
source — all three identical: block copy vs `.remedy-wt/f288-r5/block.md`;
`records.diff` copy vs `.remedy-wt/f288-r5-payloads/records.diff`;
`plan.md` copy vs `.remedy-wt/f288-r5-payloads/plan.md`.

### G2 — THE BOOKING
`git show f3a5d0354:<path>`, bytes and sha256, each MATCHING the reviewer's
reading exactly:
```
.agent/decisions.md    bytes=2240433  2d4a36d905e7109ec3386b181d22fae21bb165eef110f0f7b14f957f3f7986a9
.agent/live_review.md  bytes=315776   cc66f3145d66d16c1c6ece52f4dae86809c3a85d2542d8040761c32fabc635a0
.agent/plan.md         bytes=1056     25d4fd0efb47e045a29bd9bae3574c551f823ea5781bb3359a6ecc385c14d954
```
Open set (`open_finding_ids` from `scripts/rotate_live_review.py` over
`.agent/live_review.md`'s text at `f3a5d0354`): `[]` — empty, matching the
round's own plan ("Open findings: 0").

### G3 — THE CODE
```
$ python3 -m ruff check tests/ui_contracts/test_timeline_scrub_wiring.py tests/ui_contracts/test_brain_stage_mount.py
All checks passed!
REAL_EXIT=0
```
(Run at `HEAD`/C5; these two files are unchanged between C4 and C5, verified
by an empty `git diff aec880c25 HEAD -- <both paths>`.)

Quoted from the diff, in full:

`withPromptNodes` (promptNodes.ts, at `800940cad`):
```ts
export function withPromptNodes(
  model: BrainModel,
  items: readonly RemedyPromptTraceItem[],
): BrainModel {
  const knownIds = new Set(model.nodes.map((n) => n.id));
  const taskStateById = new Map(model.nodes.map((n) => [n.id, n.state]));
  const bornNodes: BrainNode[] = [];
  const bornLinks: BrainLink[] = [];

  for (const item of items) {
    const taskId = `task:${item.taskId}`;
    const taskState = taskStateById.get(taskId);
    if (taskState === undefined) continue;
    const id = promptNodeId(item.id);
    if (knownIds.has(id)) continue;
    knownIds.add(id);
    bornNodes.push({
      id,
      kind: "synapse",
      state: taskState,
      parentId: taskId,
      seq: 0,
      meta: {
        promptId: item.id,
        role: item.role,
        promptKind: item.promptKind,
        round: item.round,
        attemptId: item.runId,
      },
    });
    bornLinks.push({ id: `${taskId}->${id}`, source: taskId, target: id });
  }

  if (bornNodes.length === 0) return model;
  return {
    ...model,
    nodes: [...model.nodes, ...bornNodes],
    links: [...model.links, ...bornLinks],
  };
}
```

`selectionIdOf` and `selectedPromptNodeId` (brainView.ts, at `aec880c25`):
```ts
export function selectionIdOf(node: Pick<BrainLayoutNode, "id" | "kind" | "parentId">): string | null {
  if (node.kind === "synapse" && node.id.startsWith("prompt:")) {
    return node.id.slice("prompt:".length);
  }
  return selectionTaskIdOf(node);
}

export function selectedPromptNodeId(
  items: readonly RemedyPromptTraceItem[],
  selectedNodeId: string | null,
): string | null {
  if (selectedNodeId === null) return null;
  return items.some((item) => item.id === selectedNodeId) ? promptNodeId(selectedNodeId) : null;
}
```

The stage's `promptItems`, `liveModel` and `selectedId` lines (BrainGraphStage.tsx, at `aec880c25`):
```ts
  const promptItems = dashboard.promptTrace?.items ?? EMPTY_PROMPT_ITEMS;
  const liveModel = useMemo(() => withPromptNodes(rebuildBrainModel(dashboard.jobId, seeds, rows), promptItems), [dashboard.jobId, seeds, rows, promptItems]);
  const selectedId = selectedPromptNodeId(promptItems, selectedNodeId ?? null)
    ?? selectedBrainNodeId(dashboard.tasks, selectedNodeId ?? null);
```

### G4 — THE TESTS
```
$ python3 -m pytest -q -p no:cacheprovider -rs <the ordered selection>
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1828 passed, 5 skipped in 109.56s (0:01:49)
REAL_EXIT=0
```
Same five skips as the reviewer's `a5ee2dc8` baseline (1825 passed, 5
skipped). Difference: +3 passed. `--collect-only -q` on the two edited
Python files: 24 nodes at `a5ee2dc8`, 27 at `HEAD` (the three new tests in
`TestStageComposesThePromptTraceOntoTheLiveModelOnly`) — accounts for the
difference exactly.

```
$ (cd apps/ui && node_modules/.bin/vitest run)
Test Files  75 passed | 1 skipped (76)
     Tests  1455 passed | 5 skipped (1460)
REAL_EXIT=0
```
The 1 skipped file/5 skipped tests are `scrubLive.test.ts`'s own five tests,
pre-existing and untouched by this round (present at `a5ee2dc8` too).
Difference from the reviewer's `a5ee2dc8` reading (74 files, 1439 passed):
+1 file (`promptNodes.test.ts`, new) and +16 tests. `git diff
a5ee2dc8..HEAD` over the three touched vitest files shows exactly 16 added
`it(` lines (8 in `promptNodes.test.ts`, 7 in `brainView.test.ts`, 1 in
`buildForceBrainModel.test.ts`) — accounts for the difference exactly.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}
```
All six checks `pass`, `fail_count` 0.

### G5 — THE RED PROOFS
Reported whole in this round's reply (the official run against
`.remedy-wt/f288-r5-mut` at `44aa94db4`). Summary: the route proof
(promptNodes.ts broken at its own syntax) turned all three vitest files red
(`Error: Transform failed`), proving the scratch config reads the
worktree's own sources; both restored byte-identical. TypeScript runner:
control green, m1-m8 each red (1-2 failing tests apiece, matching the
mutation's own defect), control green again. Python runner: control green,
m9 red (3 failing tests across both files), m10 red (1 failing test),
control green again. `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
Every file restored byte-identical after every mutation. Worktree removed,
pruned; `git worktree list | wc -l` back to 70.

## Authored-text proofs

- Block copy (`.agent/authored/f288-r5-block.md`, at `f665aefa4`) vs
  `.remedy-wt/f288-r5/block.md`: byte-identical (Python comparison).
- `records.diff` copy vs `.remedy-wt/f288-r5-payloads/records.diff`:
  byte-identical.
- `plan.md` copy vs `.remedy-wt/f288-r5-payloads/plan.md`: byte-identical.
- `records.diff` applied via `git apply`: `--check` and the real apply both
  exit 0; the payload was never edited or retyped.
- `.agent/plan.md` after the payload rewrite: sha256
  `25d4fd0efb47e045a29bd9bae3574c551f823ea5781bb3359a6ecc385c14d954`,
  matching the payload's own reading exactly.
- `.agent/authored/f288-r5-mutations.py` at `HEAD` (C5) vs
  `.remedy-wt/f288-r5-worker/f288-r5-mutations.py` (the file developed and
  smoke-tested before commit): byte-identical, verified by Python
  `filecmp.cmp` before the commit was made.

## Deviations & assumptions

1. **An extra worktree, not the one G5 orders, added and removed before the
   official gate.** Before trusting the mutation tool for the official G5
   run, I developed and smoke-tested it (route proof mechanics, all ten
   mutations, the vitest failing-name regex) in a throwaway worktree at the
   then-tip (`aec880c25`, before the tool was committed), then removed it
   and pruned. `git worktree list | wc -l` read 70 before, during cleanup,
   and after — the same as step 4's reading — and `git status --porcelain`
   was empty throughout. No round-owned file was touched inside it; only
   the tool's own draft (outside git, under `.remedy-wt/f288-r5-worker/`)
   changed between runs.
2. Every other reading in this handback is real and measured, not expected.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 5, then
the second half of T003 — the keyboard's parallel list of the live
picture's prompt nodes and a rendered proof in a headless browser. Open
findings: 0. Operator questions: 0.
