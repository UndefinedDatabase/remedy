# Handback — F282 Findings paydown v2 · Round 3 · Book round 2, resolve R-1041 and land T004/T005, R-1040 and R-1005

## Session

SESSION 1 of feature F282 · round 3 · rounds so far 3

This round booked round 2's PASS and R-1041's resolution into the ledger,
recorded DECISION F282 D3, and landed T004 and T005: `_cmd_job_budget` in
`apps/cli/commands/job.py` now keeps the cost a job recorded when the cost
ledger names no call for it (R-1040), and `packages/orchestration/run_manifest.py`
lets a deadline budget stop write its run manifest and finalize (R-1005),
with tests and red proofs. A large majority of the session's working
context budget remained at handback.

## Range

Review of `59fa1bd8`..`HEAD`.

## Commits

### 201c97ff F282 R3 C1a: copy round 3 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r3-block.md | +200/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f282-r3-ledger.diff | +12/-0 | Payload copy |
| .agent/authored/f282-r3-decisions.diff | +28/-0 | Payload copy |
| .agent/authored/f282-r3-plan.md | +30/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 270
(200+70), matching the block's stated formula "this block's line count
plus 70" exactly. Under the 500 cap.

### 34e48db5 F282 R3 C1b: copy round 3 product payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r3-mutations.py | +62/-0 | Payload copy |
| .agent/authored/f282-r3-product.diff | +66/-0 | Payload copy |
| .agent/authored/f282-r3-tests.diff | +65/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 193
(62+66+65), matching the block's expected 193 exactly.

### 84c9ab6e F282 R3 C2: book round 2, resolve R-1041 and record DECISION F282 D3

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | `ledger.diff` applied: `Gate: F282 R2` entry and the `Done:` line of R-1041 |
| .agent/decisions.md | +20/-0 | `decisions.diff` applied: DECISION F282 D3 |
| .agent/plan.md | +6/-6 | Rewritten to the round-3 `plan.md` payload (via `shutil.copyfile`) |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 20/0 decisions.md, 4/0 live_review.md, 6/6 plan.md — matching the
block's expected numbers exactly.

### 4b72f4d5 F282 R3 C3: keep a recorded cost over an empty ledger, and let a deadline stop finalize

| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job.py | +13/-9 | `product.diff` applied: T004, R-1040 — `_cmd_job_budget` keeps a job's recorded cost when the ledger names no call for it; only a ledger answer naming at least one call (priced or unpriced) replaces the persisted figure |
| packages/orchestration/run_manifest.py | +7/-1 | `product.diff` applied: T005, R-1005 — `_decode_budgets_field` reads its own canonical `Z`-suffixed deadline form (pre-3.11 compatible), and `build_run_manifest` binds the budgets snapshot through that same decoder before publication so a deadline stop's manifest round-trip compares like with like and can finalize |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 13/9 job.py, 7/1 run_manifest.py — matching the block's expected
numbers exactly.

### 0ffe1fd3 F282 R3 C4: test the kept cost and the deadline stop, R-1040 and R-1005

| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_job_budgets.py | +27/-0 | `tests.diff` applied: two tests for R-1040 (an empty ledger answer leaves the persisted cost standing; a ledger naming even one call still replaces it) |
| tests/orchestration/test_predictive_budget.py | +16/-0 | `tests.diff` applied: parametrized test for R-1005 (a deadline stop persists `JOB_STOPPED` with a written run manifest, across three ISO-8601 deadline spellings including the `Z` form) |

Measured insertions by `git diff --cached --numstat` before commit: 27
test_job_budgets.py, 16 test_predictive_budget.py — matching the block's
expected numbers exactly.

### (this commit) F282 R3 C5: rewrite handoff for round 3

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f282-r3-mut 0ffe1fd3` for G5 —
  succeeded, HEAD detached at `0ffe1fd3`.
- `git worktree remove --force .remedy-wt/f282-r3-mut` and
  `git worktree prune` after G5 — both real exit 0; `git worktree list`
  afterward shows only the primary checkout, `.remedy-wt/f282-r2-dry`,
  `.remedy-wt/f282-r2-sim`, `.remedy-wt/f282-r3-dry`,
  `.remedy-wt/f282-r3-sim` and the four `job-*` worktrees constraint 6
  names.
- `git push origin feature/f282-findings-paydown-v2` after C5 — real
  outcome reported in the worker's final reply (G6 readings, per the
  block, do not live in this committed file).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form.

## Verification

**G1 — transport**: each of the six payloads' lines/bytes/sha256 measured
against the block's PAYLOADS table — all six rows matched exactly
(ledger.diff 12/6461, decisions.diff 28/2167, plan.md 30/1122,
product.diff 66/3984, tests.diff 65/3803, mutations.py 62/2676 — all
sha256 digests equal to the table). The block itself: 200 lines (newline
count), sha256
`3fafb90384839e03054bae0c554b6b1dc430d2f6f4f8d6a95f20dcba3c7e09cf`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f282-r3-*` blob read with `git show
<commit>:<path>` (block + ledger.diff + decisions.diff + plan.md at
`201c97ff`; product.diff + tests.diff + mutations.py at `34e48db5`)
compared byte-for-byte against its `.remedy-wt/f282-r3-payloads/` (or
block) source: all seven pairs byte-identical = True.

**G2 — the bookkeeping and the product**: at C2 (`84c9ab6e`),
`.agent/live_review.md` 396563 bytes, sha256
`c9fa23da07d1d1f073dab2feec319e5c09ab86e35e61887446307ac664cb8bd6`;
`.agent/decisions.md` 1917838 bytes, sha256
`e1f9ba0508c70b11ca15a987407860f83d58b319593f191fc8db01b357aa1ab6`;
`.agent/plan.md` 1122 bytes, sha256
`275cdc933df06af8694ee6ebae6bc6bf7ff96113e61cb37279a9f055d6a63e03` — at C3
(`4b72f4d5`), `apps/cli/commands/job.py` 100878 bytes, sha256
`5bf304f1195d14dd2e7712a62fd052778e9f4e8aa53355db0f8b2f2cdd9675d7`;
`packages/orchestration/run_manifest.py` 339525 bytes, sha256
`74687303a118b03937172ef9153fcb3fdab4652e8dbc1ed2ca0302bb9d4c7950` — at C4
(`0ffe1fd3`), `tests/orchestration/test_job_budgets.py` 68482 bytes, sha256
`d28ddf04b792707c3e21b2659a13786de939ce86abddc29ecb96de0f57de2a5a`;
`tests/orchestration/test_predictive_budget.py` 53741 bytes, sha256
`711c6615b419acfb53f2658bde1f56c303a288d00998c7477afbb1aae5eace9f` — all
seven equal to the block's table exactly. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 24 at
`59fa1bd8`, 23 at C2; set difference: `R-1041` the only id leaving, none
arriving — matching the block's reading exactly. `git diff --name-only
201c97ff 34e48db5` names exactly `.agent/authored/f282-r3-mutations.py`,
`.agent/authored/f282-r3-product.diff`, `.agent/authored/f282-r3-tests.diff`
— C1b's list. `git diff --name-only 34e48db5 84c9ab6e` names exactly
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` — C2's
list. `git diff --name-only 84c9ab6e 4b72f4d5` names exactly
`apps/cli/commands/job.py`, `packages/orchestration/run_manifest.py` —
C3's list. `git diff --name-only 4b72f4d5 0ffe1fd3` names exactly
`tests/orchestration/test_job_budgets.py`,
`tests/orchestration/test_predictive_budget.py` — C4's list.

**G3 — the linter on this block**: at C4, in the primary checkout,
`python3 -m apps.cli.main integrity block .remedy-wt/f282-r3-block.md`,
real exit 0:
```
  [OK] item 1 (size): 200 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 30 lines
  [OK] item 10 (open set recomputed): states 23; .agent/live_review.md holds 23 open by distinct id, and the block registers 0 and resolves 0, leaving 23
  [OK] item 24 (gate paths resolve): 23 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G5 before C5
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
```
Item 10's reading matches the block's stated open-findings count of 23
exactly.

**G4 — the tests**: in the primary checkout at C4, the ordered pytest
selection (23 paths, including `tests/cli/test_golden_path.py`), run
SERIALLY, real exit 0: `1069 passed in 274.96s (0:04:34)`. The reviewer's
disposable-worktree run without the golden path read `1025 passed, 2
skipped` at exit 0; the primary checkout carries the toolchain the
worktree lacked, so the two skips there ran and passed here, consistent
with the block's own note ("a skip may pass in the primary checkout").
`python3 -m ruff check apps/cli/commands/job.py
packages/orchestration/run_manifest.py
tests/orchestration/test_job_budgets.py
tests/orchestration/test_predictive_budget.py`: real exit 0, "All checks
passed!". `python3 -m apps.cli.main integrity check --json`: real exit 0,
`check_count: 6`, all six checks (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`,
`high_blockers_open`) `pass`, `fail_count: 0`, `ok: true`, `passed: true`.

**G5 — the red proofs**: `git worktree add --detach .remedy-wt/f282-r3-mut
0ffe1fd3` succeeded. `python3 -B .remedy-wt/f282-r3-payloads/mutations.py
.remedy-wt/f282-r3-mut` (real exit 0), whole output:
```
control_before REAL_EXIT=0
220 passed in 35.01s
m1_an_empty_ledger_answer_replaces_the_cost FROM count in apps/cli/commands/job.py: 1
m1_an_empty_ledger_answer_replaces_the_cost REAL_EXIT=1
FAILED tests/orchestration/test_job_budgets.py::TestJobBudgetCliRendersPredictions::test_an_empty_ledger_leaves_the_persisted_overspend_standing
1 failed, 219 passed in 35.71s
m1_an_empty_ledger_answer_replaces_the_cost restored byte-identical: True
m2_the_decoder_cannot_read_its_own_z FROM count in packages/orchestration/run_manifest.py: 1
m2_the_decoder_cannot_read_its_own_z REAL_EXIT=1
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_deadline_stop_persists_stopped[2020-01-01T00:00:00+00:00]
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_deadline_stop_persists_stopped[2020-01-01T00:00:00.250000+00:00]
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_deadline_stop_persists_stopped[2020-01-01T00:00:00Z]
3 failed, 217 passed in 34.42s
m2_the_decoder_cannot_read_its_own_z restored byte-identical: True
m3_the_builder_binds_the_raw_budgets FROM count in packages/orchestration/run_manifest.py: 1
m3_the_builder_binds_the_raw_budgets REAL_EXIT=1
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_deadline_stop_persists_stopped[2020-01-01T00:00:00+00:00]
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_deadline_stop_persists_stopped[2020-01-01T00:00:00.250000+00:00]
2 failed, 218 passed in 34.04s
m3_the_builder_binds_the_raw_budgets restored byte-identical: True
r1_job_py_before_this_round REAL_EXIT=1
FAILED tests/orchestration/test_job_budgets.py::TestJobBudgetCliRendersPredictions::test_an_empty_ledger_leaves_the_persisted_overspend_standing
1 failed, 219 passed in 34.24s
r1_job_py_before_this_round restored byte-identical: True
r2_run_manifest_before_this_round REAL_EXIT=1
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_deadline_stop_persists_stopped[2020-01-01T00:00:00+00:00]
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_deadline_stop_persists_stopped[2020-01-01T00:00:00.250000+00:00]
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_deadline_stop_persists_stopped[2020-01-01T00:00:00Z]
3 failed, 217 passed in 34.14s
r2_run_manifest_before_this_round restored byte-identical: True
control_after REAL_EXIT=0
220 passed in 33.34s
REAL_EXIT=0
```
Matches the reviewer's reading exactly: control_before `220 passed` exit
0; m1 1 failed exit 1; m2 3 failed exit 1; m3 2 failed exit 1; r1 1
failed exit 1; r2 3 failed exit 1; control_after `220 passed` exit 0;
every `restored byte-identical` line True. `git worktree remove --force
.remedy-wt/f282-r3-mut` and `git worktree prune`: both real exit 0. `git
worktree list` afterward: primary checkout plus `.remedy-wt/f282-r2-dry`,
`.remedy-wt/f282-r2-sim`, `.remedy-wt/f282-r3-dry`,
`.remedy-wt/f282-r3-sim` and the four `job-*` worktrees constraint 6
names — nothing else.

## Authored-text proofs

- `.agent/authored/f282-r3-block.md` (C1a) == `.remedy-wt/f282-r3-block.md`:
  byte-identical True (sha256
  `3fafb90384839e03054bae0c554b6b1dc430d2f6f4f8d6a95f20dcba3c7e09cf`, 200
  lines).
- `.agent/authored/f282-r3-ledger.diff`, `-decisions.diff`, `-plan.md`
  (C1a) == their `.remedy-wt/f282-r3-payloads/` sources: byte-identical
  True, all three.
- `.agent/authored/f282-r3-product.diff`, `-tests.diff`, `-mutations.py`
  (C1b) == their `.remedy-wt/f282-r3-payloads/` sources: byte-identical
  True, all three.
- `ledger.diff`, `decisions.diff`, `product.diff`, `tests.diff` were
  applied at C2/C3/C4 with `git apply --check` then `git apply` directly
  from the payload's own bytes under `.remedy-wt/f282-r3-payloads/` —
  never retyped, every `--check` and every real apply at real exit 0.
- `.agent/plan.md` at C2 == `plan.md` payload verbatim (rewrite by
  `shutil.copyfile`): byte-identical True (confirmed by the G2 sha256
  table above).
- No payload was edited or retyped anywhere this round; every copy used
  `shutil.copyfile` and every diff was applied by `git apply` reading the
  payload file directly.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 270 insertions, matches block formula (200+70) exactly |
| C1b | done | 193 insertions, matches block exactly |
| C2 | done | 20/4/6 insertions by `git diff --cached --numstat`, matches block exactly |
| C3 | done | 13/9 and 7/1, matches block exactly |
| C4 | done | 27/16 insertions, matches block exactly |
| C5 | done | this handback |
| Round 2 booking | done | `Gate: F282 R2` entry appended to `.agent/live_review.md` via `ledger.diff` |
| R-1041 | done | resolved — booked as the one id leaving the open set at C2 |
| DECISION F282 D3 | done | recorded at C2 via `decisions.diff` |
| T004 | done | `_cmd_job_budget` in `apps/cli/commands/job.py` keeps a job's recorded cost when the ledger names no call, R-1040, landed at C3 with tests at C4 |
| T005 | done | `_decode_budgets_field` / `build_run_manifest` in `packages/orchestration/run_manifest.py` let a deadline stop finalize, R-1005, landed at C3 with tests at C4 |
| G1 | done | all readings match; all seven authored copies byte-identical |
| G2 | done | all seven sha256/byte readings match; open-set 24 to 23, R-1041 leaving exactly as named; all four name-only diffs match exactly |
| G3 | done | integrity block linter, real exit 0, all 7 checkable items `[OK]`, item 10 reading matches exactly |
| G4 | done | 1069 passed exit 0 (reviewer's worktree run: 1025 passed/2 skipped, toolchain present here); ruff exit 0; integrity check all-pass exit 0 |
| G5 | done | mutation script output matches the reviewer's reading exactly across all seven sub-checks; worktree cleaned up |
| G6 | done | readings reported in the final reply only, per the block |
| Push | done | reported in the final reply only, per the block |

## Deviations & assumptions

None. Every reading this round matched the block's stated expectation
exactly. No payload was edited or retyped; every copy used
`shutil.copyfile` and every diff was applied via `git apply` reading the
payload file directly. The commit sequence landed in the block's exact
order C1a-C1b-C2-C3-C4-C5. This round is SESSION 1 of F282, its third
round.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
3, then T006 to T008 — R-1007, then R-1016, R-1027 and R-1035, then
R-0999. Open findings count: 23. Operator-questions count: 0.
