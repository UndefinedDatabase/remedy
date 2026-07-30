# Handback — F050 R2 (verdict persist + INTEGRATION GATE) — evidence complete

## Range
`ac9dc6f..HEAD` · feature/f050-dag-scheduling · Slice 0 = 1 commit (`f6f6faa`)
+ 1 round-end. Merge base `c0e2bd1`. PR **#163** still open, NOT merged.
No closure work: no STATUS `[x]`, no evidence job, no zip.

## Commits
### f6f6faa chore(f050): persist R1 verdict; record Built State
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +31/-… | authored f050-r2-1 FULL REPLACE — R1 PASS verdict + DECISIONS (a)/(b) |
| docs/roadmap/features/T1_F050.md | +26 | authored f050-r2-2 appended byte-unchanged after "Do not touch" |
| .agent/last_block.md | rewrite | R2 block guard |
| .agent/authored/f050-r2-{1,2}.md | +new | authored sources, sha256-verified |

No production or test code in this round.

## Authored-text proofs
Both matched their BEGIN markers on first save, BEFORE any apply:

    a46f0d067d7438cd4ef174e93a2248228069b9f00f954155a9007dcd5b932716  .agent/authored/f050-r2-1.md
    6b727bc08b80b3894720a43c11fbf7377fce46b82688ca4e8166437cbad42406  .agent/authored/f050-r2-2.md

- `cmp .agent/authored/f050-r2-1.md .agent/live_review.md` → exit **0**.
- Append proof: `tail -c $(wc -c < f050-r2-2.md) docs/roadmap/features/T1_F050.md | cmp - f050-r2-2.md`
  → exit **0**. Feature file 3114 → 4576 bytes; diff is a pure 26-line append.

## Slice 0 gates
- `python3 -m pytest tests/docs/ -q` → exit **0**, `292 passed in 0.19s`.
- `python3 -m pytest tests/cli/test_golden_path.py -q` → exit **0**, `42 passed in 15.06s`.

## INTEGRATION GATE — raw evidence (verdict is the reviewer's)

### Step 1 — branch run
    CMD:  python3 -m pytest -n auto -q
    CWD:  /home/decodeux/Repos/remedy
    HEAD: f6f6faae29290aaf7b269922dce9a98e295f566e
    EXIT: 0
    WALL_SECONDS=164.82
    tail: 14343 passed, 19 skipped in 164.39s (0:02:44)

`grep '^FAILED' | sort > branch_failed.txt` → **0 lines**.

### Step 2 — base run (throwaway worktree at the merge base)
    CMD:  python3 -m pytest -n auto -q
    CWD:  <scratchpad>/gate_base_wt
    HEAD: c0e2bd1b7f0f1bc8810ef240ee42804c52357cd8
    EXIT: 1
    WALL_SECONDS=201.50
    tail: 20 failed, 14269 passed, 25 skipped in 201.06s (0:03:21)

`base_failed.txt` → **20 lines**: 2 × `tests/cli/test_self_dogfood_execution_cli.py`,
1 × `test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`,
1 × `test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles`,
16 × `tests/ui_server/test_live_state.py::TestUIServerIntegration::*`.

Collection delta (branch 14362 vs base 14314 selected) = the 48 tests this
feature added — consistent, nothing silently dropped.

### Step 3 — compare
- `comm -13 base_failed.txt branch_failed.txt` (**branch-only failures**) → **EMPTY, 0 lines**.
- `comm -23 base_failed.txt branch_failed.txt` → all **20** base ids.

### Step 4 — attribution
**Zero branch-only failure ids, so no serial re-run attribution was required**
(gate step 4 applies per branch-only id). Nothing to classify, no blocker.

The 20 `comm -23` ids are NOT fixes by this branch, and reporting them as such
would be false. All 20 are artifacts of a fresh `git worktree`, which checks out
tracked files only and therefore lacks install/build outputs:
- `apps/ui/node_modules` — **0 entries** in the worktree vs **205** in the main
  checkout; root `node_modules` absent entirely. Failure text:
  `Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'vitest'`, and tsc's
  "Use yarn to avoid accidentally running code from un-installed packages".
- `apps/ui/dist` — present in the main checkout, absent in the worktree; the
  `TestUIServerIntegration` failures are all `_start_server()` failing.
- The 2 dogfood ids assert on local `.data/` state (`'blocked'` vs
  `'awaiting_external_candidate'`, `0 == 1` attempts) that a fresh tree has none of.

Diagnostic re-run of those exact 20 ids at the base commit, serially, with the
root `node_modules` symlinked in: still `20 failed in 82.24s` — the missing piece
is the per-app install and build, not the base code. Scope proof that none of
this touches the feature: `git diff --name-only c0e2bd1..HEAD | grep -iE
'apps/ui|\.tsx?$|package(-lock)?\.json|vitest|tsconfig|ui_server|dogfood|test_runner'`
→ **no match**. The same 20 ids pass on the branch in the main checkout (branch
run, 0 failures), which is the environment difference stated plainly.

### Worktree removal proof
    $ git worktree list          # after remove --force + prune
    /home/decodeux/Repos/remedy  f6f6faa [feature/f050-dag-scheduling]
Worktree directory confirmed gone. The `node_modules` symlink added during
diagnosis was inside the throwaway worktree only, was created strictly AFTER the
recorded base run, and died with it — `base_failed.txt` is unaffected.

### Step 6 — budget
Branch 164.82s (2:44), base 201.50s (3:21). Both under the ~5 min threshold; no
perf pass flagged.

## Deviations & assumptions
- **Extra diagnostic work beyond gate steps 1–4.** The procedure asks for
  `comm -23` to be reported; it labels that set "failures the branch fixed",
  which would have been a false claim here. I diagnosed the cause instead of
  reporting the label. No extra commits, no code touched.
- **Observation for the reviewer, not a finding:** a fresh worktree is not a
  like-for-like baseline for any test that shells out to the JS toolchain or
  reads local `.data/`. Every such test lands in `comm -23` on every gate run
  and can mask a genuine base failure in the same files. Whether
  `docs/agents/integration_gate.md` should require installing/building in the
  base worktree, or deselecting environment-coupled ids, is the reviewer's call.
- Round-end state in a second mechanical commit (handoff + OUTCOME flip), as
  accepted in R0154 R1.
- `.agent/plan.md` untouched: still byte-verbatim as authored, and its
  "integration gate, then closure" next-step line describes exactly this round.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 last_block guard | done | flip to `executed` in the round-end commit |
| 2 f050-r2-1 → live_review.md | done | sha256 match, cmp 0 |
| 3 f050-r2-2 → T1_F050.md append | done | sha256 match, tail cmp 0 |
| 4 Slice 0 gate + commit | done | 292 / 42, both exit 0 |
| 5 gate steps 1–4 | done | 0 branch-only failures; worktree removed + pruned |
| 6 wall-clock note | done | 2:44 / 3:21, under threshold |
| 7 handback | done | this file |

## Next
Reviewer issues the **integration-gate verdict** on this evidence. Open
questions: (a) accept the `comm -23` set as worktree-environment artifacts
rather than branch fixes; (b) whether the integration_gate.md baseline
observation above deserves a finding. On PASS: closure per
docs/roadmap/STATUS_closure_protocol.md v4 — its own round, and PR #163 merges
at the next round's Open PR Gate.
