# Handback — F282 Findings paydown v2 · Round 8 · Book round 7, resolve R-0892 by evidence and land T017: R-0866's parked rail ends

## Session

SESSION 2 of feature F282 · round 8 · rounds so far 8

This round booked round 7's PASS and the resolutions of R-0622 and
R-1029 into the ledger, resolved R-0892 by the evidence F268 and
amend0920-selfuse-real already landed (T014, no code needed), recorded
DECISION F282 D8, and landed T017: a self-improvement attempt now
stops `blocked` with the stop reason `external_candidate_route_removed`
once its request package is prepared, instead of waiting forever in
`awaiting_external_candidate` for a candidate no surviving command can
bring (R-0866). `reconcile_self_attempt` moves an attempt an older
Remedy parked at `awaiting_external_candidate` without a patch intent
to the same stop; one whose intent is already on disk still runs on,
per DECISION F275 D12 (a). Roughly three-quarters of this session's
working-context budget remained at handback.

## Range

Review of `7932b7c1`..`HEAD`.

## Commits

### 73acbb04 F282 R8 C1a: copy round 8 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r8-block.md | +199/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f282-r8-ledger.diff | +16/-0 | Payload copy |
| .agent/authored/f282-r8-decisions.diff | +36/-0 | Payload copy |
| .agent/authored/f282-r8-plan.md | +31/-0 | Payload copy |

Measured insertions by `git diff --stat --cached` before commit: 282
(199+83), matching the block's stated formula "this block's line count
plus 83" exactly. Under the 500 cap.

### 83c36ceb F282 R8 C1b: copy round 8 product and test payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r8-mutations.py | +75/-0 | Payload copy |
| .agent/authored/f282-r8-product.diff | +147/-0 | Payload copy |
| .agent/authored/f282-r8-tests.diff | +99/-0 | Payload copy |

Measured insertions by `git diff --stat --cached` before commit: 321,
matching the block's expected 321 exactly.

### f2119cb4 F282 R8 C2: book round 7, resolve R-0622, R-1029 and R-0892 and record DECISION F282 D8

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | `ledger.diff` applied: `Gate: F282 R7` entry and the `Done:` lines of R-0622, R-1029 and R-0892 |
| .agent/decisions.md | +28/-0 | `decisions.diff` applied: DECISION F282 D8 (a self-improvement attempt stops `blocked` at the removed candidate route; R-0892 resolves by evidence already landed) |
| .agent/plan.md | +10/-9 | Rewritten to the round-8 `plan.md` payload (via `shutil.copyfile`) |

Measured insertions/deletions by `git diff --numstat` before commit:
28/0 decisions.md, 8/0 live_review.md, 10/9 plan.md — matching the
block's expected numbers exactly.

### b6e1116b F282 R8 C3: end a self-improvement attempt at the removed candidate route, R-0866

| Path | +/- | Reason |
|---|---|---|
| docs/system/self-dogfood-execution-v0.md | +11/-7 | `product.diff` applied: T017 — describes the new stop `blocked`/`external_candidate_route_removed` in place of the permanent park at `awaiting_external_candidate` |
| packages/orchestration/self_dogfood_execution.py | +38/-15 | `product.diff` applied: T017 — new `StopReason.EXTERNAL_CANDIDATE_ROUTE_REMOVED`; `start_self_execution` transitions `request_prepared → blocked` via new helper `_stop_at_removed_candidate_route`; `reconcile_self_attempt` moves an intent-less parked attempt to the same stop; `_next_action_for` and `evaluate_self_execution_eligibility` updated to match |

Measured insertions/deletions by `git diff --numstat` before commit:
11/7 self-dogfood-execution-v0.md, 38/15 self_dogfood_execution.py —
matching the block's expected numbers exactly.

### 9fe28ba1 F282 R8 C4: pin the stop at the removed candidate route, R-0866

| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_self_dogfood_execution_cli.py | +4/-3 | `tests.diff` applied: `test_approved_execute_stops_at_the_removed_candidate_route` (renamed from the old awaits-candidate test) asserts `state == "blocked"`, `stop_reason == "external_candidate_route_removed"`, and the per-attempt next action |
| tests/orchestration/test_self_dogfood_execution.py | +42/-6 | `tests.diff` applied: renamed/updated start test, updated idempotency test, and two new tests — `test_reconcile_ends_an_attempt_an_older_remedy_parked` and `test_reconcile_keeps_a_parked_attempt_whose_intent_is_on_disk` |

Measured insertions/deletions by `git diff --numstat` before commit:
4/3 test_self_dogfood_execution_cli.py, 42/6
test_self_dogfood_execution.py — matching the block's expected numbers
exactly.

### (this commit) F282 R8 C5: rewrite handoff for round 8

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f282-r8-mut 9fe28ba1` for the
  G5 red proofs — succeeded, real exit 0, HEAD detached at `9fe28ba1`.
- `python3 -B .remedy-wt/f282-r8-payloads/mutations.py
  .remedy-wt/f282-r8-mut` — real exit 0.
- `git worktree remove --force .remedy-wt/f282-r8-mut` and
  `git worktree prune` after G5 — both real exit 0; `git worktree list`
  afterward shows only the primary checkout, `.remedy-wt/f282-r8-dry`,
  `.remedy-wt/f282-r8-sim` and the four `job-*` worktrees constraint 6
  names.
- `git push origin feature/f282-findings-paydown-v2` after C5 — real
  outcome reported in the worker's final reply (G6 readings, per the
  block, do not live in this committed file).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form.

## Verification

**G1 — transport**: each of the six payloads' lines/bytes/sha256
measured against the block's PAYLOADS table — all six rows matched
exactly (ledger.diff 16/7207, decisions.diff 36/3066, plan.md 31/1124,
product.diff 147/9330, tests.diff 99/5473, mutations.py 75/3404 — all
sha256 digests equal to the table). The block itself: 199 lines
(newline count), sha256
`d657cfc58837f6cfc59187ab784f881f12711e27f9cdfd2d56995650d8469148`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f282-r8-*` blob read with `git show
<commit>:<path>` (block + ledger.diff + decisions.diff + plan.md at
`73acbb04`; product.diff + tests.diff + mutations.py at `83c36ceb`)
compared byte-for-byte against its `.remedy-wt/f282-r8-payloads/` (or
block) source: all seven pairs byte-identical = True.

**G2 — the bookkeeping and the product**: at C2 (`f2119cb4`),
`.agent/live_review.md` 421889 bytes, sha256
`46107c56f9b30782ac52de4bf7c458a07bd491532c77ac41db2f3f89964f4ed8`;
`.agent/decisions.md` 1929153 bytes, sha256
`d848f0c46081cfc8f1710253149901a9a6661f28c3b60804d83761e2760234e7`;
`.agent/plan.md` 1124 bytes, sha256
`c55bb0b2d1fe586439c4ac360107f98c040459de630487bdf501996b9cf14f8f` —
at C3 (`b6e1116b`),
`packages/orchestration/self_dogfood_execution.py` 33836 bytes, sha256
`6f0fb4eacf7f62438175a625a4d2191233813ee0f78936b658c448c14950e69d`;
`docs/system/self-dogfood-execution-v0.md` 4735 bytes, sha256
`e8da49499a50ce5c5b3cad5e82173d409742684fafb6636c58b66b3f1287f20d` —
at C4 (`9fe28ba1`),
`tests/orchestration/test_self_dogfood_execution.py` 15314 bytes,
sha256
`0b8a4871d380601497840bd8aa3f640729429a775d568988c8049ebdaaec32f2`;
`tests/cli/test_self_dogfood_execution_cli.py` 5541 bytes, sha256
`2af5b2aa2fc8d1e32085a58b57803dd6afe17a65b8d444ccf5c90de1967d28f2` —
all seven equal to the block's table exactly. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 11 at
`7932b7c1`, 8 at C2; set difference: `R-0622`, `R-0892` and `R-1029`
the only ids leaving, none arriving — matching the block's reading
exactly. `git diff --name-only 73acbb04 83c36ceb` names exactly
`.agent/authored/f282-r8-mutations.py`,
`.agent/authored/f282-r8-product.diff`,
`.agent/authored/f282-r8-tests.diff` — C1b's list. `git diff
--name-only 83c36ceb f2119cb4` names exactly `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md` — C2's list. `git diff
--name-only f2119cb4 b6e1116b` names exactly
`docs/system/self-dogfood-execution-v0.md`,
`packages/orchestration/self_dogfood_execution.py` — C3's list. `git
diff --name-only b6e1116b 9fe28ba1` names exactly
`tests/cli/test_self_dogfood_execution_cli.py`,
`tests/orchestration/test_self_dogfood_execution.py` — C4's list.

**G3 — the linter on this block**: at C4, in the primary checkout,
`python3 -m apps.cli.main integrity block .remedy-wt/f282-r8-block.md`,
real exit 0:
```
  [OK] item 1 (size): 199 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 31 lines
  [OK] item 10 (open set recomputed): states 8; .agent/live_review.md holds 8 open by distinct id, and the block registers 0 and resolves 0, leaving 8
  [OK] item 24 (gate paths resolve): 10 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G5 before C5
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
```

**G4 — the tests and the lint**: in the primary checkout at C4, the
ordered pytest selection (10 paths), run SERIALLY, real exit 0:
```
515 passed, 1 skipped in 70.16s (0:01:10)
```
matching the reviewer's `-n 8` simulation reading of `515 passed, 1
skipped` at exit 0 exactly. `python3 -m ruff check
packages/orchestration/self_dogfood_execution.py
tests/orchestration/test_self_dogfood_execution.py
tests/cli/test_self_dogfood_execution_cli.py`: real exit 0, "All
checks passed!". `python3 -m apps.cli.main integrity check --json`:
real exit 0, `check_count: 6`, all six checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`repo_root_hygiene`, `high_blockers_open`) `pass`, `fail_count: 0`,
`ok: true`, `passed: true`.

**G5 — the red proofs**: `git worktree add --detach
.remedy-wt/f282-r8-mut 9fe28ba1` succeeded, real exit 0. `python3 -B
.remedy-wt/f282-r8-payloads/mutations.py .remedy-wt/f282-r8-mut` (real
exit 0), whole output:
```
control_before REAL_EXIT=0
31 passed in 2.68s
m1_start_parks_again FROM count in packages/orchestration/self_dogfood_execution.py: 1
m1_start_parks_again REAL_EXIT=1
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_execute_stops_blocked_at_the_removed_candidate_route
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_execute_idempotent_resume
FAILED tests/cli/test_self_dogfood_execution_cli.py::test_approved_execute_stops_at_the_removed_candidate_route
3 failed, 28 passed in 2.65s
m1_start_parks_again restored byte-identical: True
m2_reconcile_leaves_the_parked_attempt FROM count in packages/orchestration/self_dogfood_execution.py: 1
m2_reconcile_leaves_the_parked_attempt REAL_EXIT=1
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_reconcile_ends_an_attempt_an_older_remedy_parked
1 failed, 30 passed in 2.66s
m2_reconcile_leaves_the_parked_attempt restored byte-identical: True
m3_reconcile_ends_an_attempt_with_an_intent FROM count in packages/orchestration/self_dogfood_execution.py: 1
m3_reconcile_ends_an_attempt_with_an_intent REAL_EXIT=1
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_reconcile_keeps_a_parked_attempt_whose_intent_is_on_disk
1 failed, 30 passed in 2.68s
m3_reconcile_ends_an_attempt_with_an_intent restored byte-identical: True
m4_start_prepares_a_second_attempt FROM count in packages/orchestration/self_dogfood_execution.py: 1
m4_start_prepares_a_second_attempt REAL_EXIT=1
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_execute_idempotent_resume
FAILED tests/cli/test_self_dogfood_execution_cli.py::test_execute_idempotent
2 failed, 29 passed in 2.54s
m4_start_prepares_a_second_attempt restored byte-identical: True
m5_next_action_loops_on_reconcile FROM count in packages/orchestration/self_dogfood_execution.py: 1
m5_next_action_loops_on_reconcile REAL_EXIT=1
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_execute_stops_blocked_at_the_removed_candidate_route
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_reconcile_ends_an_attempt_an_older_remedy_parked
FAILED tests/cli/test_self_dogfood_execution_cli.py::test_approved_execute_stops_at_the_removed_candidate_route
3 failed, 28 passed in 2.90s
m5_next_action_loops_on_reconcile restored byte-identical: True
r1_module_before_this_round REAL_EXIT=1
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_execute_stops_blocked_at_the_removed_candidate_route
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_execute_idempotent_resume
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_reconcile_ends_an_attempt_an_older_remedy_parked
FAILED tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_reconcile_keeps_a_parked_attempt_whose_intent_is_on_disk
FAILED tests/cli/test_self_dogfood_execution_cli.py::test_approved_execute_stops_at_the_removed_candidate_route
5 failed, 26 passed in 2.59s
r1_module_before_this_round restored byte-identical: True
control_after REAL_EXIT=0
31 passed in 2.70s
REAL_EXIT=0
```
Matches the reviewer's reading exactly: control_before `31 passed`
exit 0; m1 3 failed exit 1; m2 1 failed exit 1; m3 1 failed exit 1; m4
2 failed exit 1; m5 3 failed exit 1; r1 5 failed exit 1; control_after
`31 passed` exit 0; every `restored byte-identical` line True. `git
worktree remove --force .remedy-wt/f282-r8-mut` and `git worktree
prune`: both real exit 0. `git worktree list` afterward: primary
checkout plus `.remedy-wt/f282-r8-dry`, `.remedy-wt/f282-r8-sim` and
the four `job-*` worktrees constraint 6 names — nothing else.

## Authored-text proofs

- `.agent/authored/f282-r8-block.md` (C1a) ==
  `.remedy-wt/f282-r8-block.md`: byte-identical True (sha256
  `d657cfc58837f6cfc59187ab784f881f12711e27f9cdfd2d56995650d8469148`,
  199 lines).
- `.agent/authored/f282-r8-ledger.diff`, `-decisions.diff`, `-plan.md`
  (C1a) == their `.remedy-wt/f282-r8-payloads/` sources:
  byte-identical True, all three.
- `.agent/authored/f282-r8-product.diff`, `-tests.diff`,
  `-mutations.py` (C1b) == their `.remedy-wt/f282-r8-payloads/`
  sources: byte-identical True, all three.
- `ledger.diff`, `decisions.diff`, `product.diff`, `tests.diff` were
  applied at C2/C3/C4 with `git apply --check` then `git apply`
  directly from the payload's own bytes under
  `.remedy-wt/f282-r8-payloads/` — never retyped, every `--check` and
  every real apply at real exit 0.
- `.agent/plan.md` at C2 == `plan.md` payload verbatim (rewrite by
  `shutil.copyfile`): byte-identical True (confirmed by the G2 sha256
  table above).
- No payload was edited or retyped anywhere this round; every copy
  used `shutil.copyfile` and every diff was applied by `git apply`
  reading the payload file directly.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 282 insertions, matches block formula (199+83) exactly |
| C1b | done | 321 insertions, matches block exactly |
| C2 | done | 28/8/10-9 insertions/deletions by `git diff --numstat`, matches block exactly |
| C3 | done | 11/7, 38/15, matches block exactly |
| C4 | done | 4/3, 42/6, matches block exactly |
| C5 | done | this handback |
| Round 7 booking | done | `Gate: F282 R7` entry appended to `.agent/live_review.md` via `ledger.diff` |
| R-0622 | done | resolved — booked as one of the three ids leaving the open set at C2 |
| R-1029 | done | resolved — booked as one of the three ids leaving the open set at C2 |
| R-0892 | done | resolved by evidence already landed (F268 round 6 package half, amend0920-selfuse-real skill half); no code this round; booked as one of the three ids leaving the open set at C2 |
| DECISION F282 D8 | done | recorded at C2 via `decisions.diff` |
| T014 | done | R-0892 resolved by evidence, no code needed |
| T017 | done | `start_self_execution` stops `blocked`/`external_candidate_route_removed` after preparing its request; `reconcile_self_attempt` moves an intent-less parked attempt to the same stop; an intent-bearing parked attempt still runs on (R-0866), landed at C3 with tests at C4 |
| G1 | done | all readings match; all seven authored copies byte-identical |
| G2 | done | all seven sha256/byte readings match; open-set 11 to 8, R-0622/R-0892/R-1029 leaving exactly as named; all four name-only diffs match exactly |
| G3 | done | integrity block linter, real exit 0, all 7 checkable items `[OK]` |
| G4 | done | 515 passed, 1 skipped, exit 0 (matches reviewer's `-n 8` simulation reading exactly); ruff exit 0 all checks pass; integrity check all-pass exit 0 |
| G5 | done | mutation script output matches the reviewer's reading exactly across all seven sub-checks (control_before, m1-m5, r1, control_after); worktree cleaned up |
| G6 | done | readings reported in the final reply only, per the block |
| Push | done | reported in the final reply only, per the block |

## Deviations & assumptions

None. Every reading this round matched the block's stated expectation
exactly. No payload was edited or retyped; every copy used
`shutil.copyfile` and every diff was applied via `git apply` reading
the payload file directly. The commit sequence landed in the block's
exact order C1a-C1b-C2-C3-C4-C5. This round is SESSION 2 of F282, its
eighth round.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of
round 8, then T018 — R-0950, R-1028 and R-0499. Open findings count:
8. Operator-questions count: 0.
