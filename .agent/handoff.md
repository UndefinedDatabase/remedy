# Handback — F282 Findings paydown v2 · Round 4 · Book round 3 and land T006/T007, R-1007's kept verdict and the timeout status

## Session

SESSION 1 of feature F282 · round 4 · rounds so far 4

This round booked round 3's PASS and the resolutions of R-1040 and R-1005
into the ledger, recorded DECISION F282 D4, and landed T006 and T007: a
budget-stopped self-use task now keeps the last reviewer verdict it
actually reached and the self-use runner's default call ceiling clears
what its own loop can spend (R-1007), and a provider call that timed out
now ends a run at `provider_timeout` rather than `provider_unavailable`,
carrying the timeout text as its detail (R-1016, R-1027, R-1035). A large
majority of the session's working context budget remained at handback.

## Range

Review of `a5715ae8`..`HEAD`.

## Commits

### 04a1d4ce F282 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r4-block.md | +202/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f282-r4-ledger.diff | +14/-0 | Payload copy |
| .agent/authored/f282-r4-decisions.diff | +37/-0 | Payload copy |
| .agent/authored/f282-r4-plan.md | +30/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 283
(202+81), matching the block's stated formula "this block's line count
plus 81" exactly. Under the 500 cap.

### f4537322 F282 R4 C1b: copy round 4 product payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r4-mutations.py | +77/-0 | Payload copy |
| .agent/authored/f282-r4-product.diff | +141/-0 | Payload copy |
| .agent/authored/f282-r4-tests.diff | +90/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 308
(77+141+90), matching the block's expected 308 exactly.

### b5fe04e3 F282 R4 C2: book round 3, resolve R-1040 and R-1005 and record DECISION F282 D4

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | `ledger.diff` applied: `Gate: F282 R3` entry and the `Done:` lines of R-1040 and R-1005 |
| .agent/decisions.md | +29/-0 | `decisions.diff` applied: DECISION F282 D4 |
| .agent/plan.md | +8/-8 | Rewritten to the round-4 `plan.md` payload (via `shutil.copyfile`) |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 29/0 decisions.md, 6/0 live_review.md, 8/8 plan.md — matching the
block's expected numbers exactly.

### 15a2e88c F282 R4 C3: record a provider timeout as one, and keep a stopped task's verdict

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/failure_postmortem.py | +1/-0 | `product.diff` applied: T007 — `TERMINAL_STATUS_CLASSES` gains the `provider_timeout` entry |
| packages/orchestration/pingpong_job.py | +11/-4 | `product.diff` applied: T006/T007 — `final_status_detail_of` also carries detail for `provider_timeout`; `run_job` sets `task.reviewer_verdict` from the last round the reviewer actually reached before a budget stop (R-1007) |
| packages/orchestration/pingpong_loop.py | +15/-3 | `product.diff` applied: T007 — new `provider_failure_status` helper picks `provider_timeout` vs `provider_unavailable` via `is_timeout_error`, used at the builder-call-failed-for-good exit |
| packages/orchestration/run_manifest.py | +1/-0 | `product.diff` applied: T007 — `RUN_FINAL_STATUS_TO_LEDGER_STATE` maps `provider_timeout` to `failed` |
| packages/orchestration/self_use_runner.py | +15/-2 | `product.diff` applied: T006 — `run_next_self_use_item`'s default `max_provider_calls` is raised to one more than `2 x (1 + repair_rounds) x max_tasks` whenever 8 would tie or undercut what the loop can spend; a passed or declared ceiling is never raised (R-1007) |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 1/0 failure_postmortem.py, 11/4 pingpong_job.py, 15/3
pingpong_loop.py, 1/0 run_manifest.py, 15/2 self_use_runner.py — matching
the block's expected numbers exactly.

### 4c944b4b F282 R4 C4: test the timeout status, the kept verdict and the call ceiling

| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_predictive_budget.py | +53/-0 | `tests.diff` applied: tests for a timed-out builder call recorded as `provider_timeout` and for a call-budget stop keeping the verdict the reviewer last reached (R-1007, R-1016, R-1027, R-1035) |
| tests/orchestration/test_self_use_runner.py | +15/-0 | `tests.diff` applied: tests for the default call cap staying above what the loop can spend, the caller override standing, and a passed cap never being raised (R-1007) |

Measured insertions by `git diff --cached --numstat` before commit: 53
test_predictive_budget.py, 15 test_self_use_runner.py — matching the
block's expected numbers exactly.

### (this commit) F282 R4 C5: rewrite handoff for round 4

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f282-r4-mut 4c944b4b` for G5 —
  succeeded, HEAD detached at `4c944b4b`.
- `git worktree remove --force .remedy-wt/f282-r4-mut` and
  `git worktree prune` after G5 — both real exit 0; `git worktree list`
  afterward shows only the primary checkout, `.remedy-wt/f282-r4-dry`,
  `.remedy-wt/f282-r4-sim` and the four `job-*` worktrees constraint 6
  names.
- `git push origin feature/f282-findings-paydown-v2` after C5 — real
  outcome reported in the worker's final reply (G6 readings, per the
  block, do not live in this committed file).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form.

## Verification

**G1 — transport**: each of the six payloads' lines/bytes/sha256 measured
against the block's PAYLOADS table — all six rows matched exactly
(ledger.diff 14/8254, decisions.diff 37/3085, plan.md 30/1120,
product.diff 141/8098, tests.diff 90/5085, mutations.py 77/3402 — all
sha256 digests equal to the table). The block itself: 202 lines (newline
count), sha256
`4eb9dc9f3ebedda267f0f2327d4e5be41d515468129bb88816d22982b8777e9c`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f282-r4-*` blob read with `git show
<commit>:<path>` (block + ledger.diff + decisions.diff + plan.md at
`04a1d4ce`; product.diff + tests.diff + mutations.py at `f4537322`)
compared byte-for-byte against its `.remedy-wt/f282-r4-payloads/` (or
block) source: all seven pairs byte-identical = True.

**G2 — the bookkeeping and the product**: at C2 (`b5fe04e3`),
`.agent/live_review.md` 400952 bytes, sha256
`287376fec350faf71787ebbcf1023e958b8bdf6d895d07b8f8444a1cea77c919`;
`.agent/decisions.md` 1920363 bytes, sha256
`666e060e71a68d8f121ba8af835bc64b43e58da9e026b9711387d515867d0c9d`;
`.agent/plan.md` 1120 bytes, sha256
`77bfe2995455430e3de3cf31bcb1c3055c2007c76e3616f231fe581ac1c2bfe9` — at
C3 (`15a2e88c`), `packages/orchestration/pingpong_loop.py` 226964 bytes,
sha256
`eaa0f5629ccdbf0d0ab753d870ac2ce6ef947c14769958ed19e08dd8f109bf88`;
`packages/orchestration/pingpong_job.py` 201022 bytes, sha256
`c050ab7e6863294a38983b7372f924b6578d607ef3280dac2e8eaea8cd7a930b`;
`packages/orchestration/self_use_runner.py` 20929 bytes, sha256
`ec1a97c4fc2ae000f135438188d308af8d4e414d1be033e6ca869b0e2c62959d`;
`packages/orchestration/run_manifest.py` 339619 bytes, sha256
`49f912964180279cb16b17947a708b90e0b4f25989f13edb683f4d1132d76ffb`;
`packages/orchestration/failure_postmortem.py` 41466 bytes, sha256
`cacb7e1d8959918f7318964f9e405e0faa170fc17a29c639c8bd7e9a563b9cdd` — at
C4 (`4c944b4b`), `tests/orchestration/test_predictive_budget.py` 56834
bytes, sha256
`7c2cc2665c2b2f6cec7c3bbc4c91b0436dc2b32edf5c5f3418dd0db955ac2973`;
`tests/orchestration/test_self_use_runner.py` 27681 bytes, sha256
`cd857e88b06992b185fc3ddecade71690c1ce9f9c22346fc0693539ee4d56c50` — all
ten equal to the block's table exactly. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 23 at
`a5715ae8`, 21 at C2; set difference: `R-1005` and `R-1040` the only ids
leaving, none arriving — matching the block's reading exactly. `git diff
--name-only 04a1d4ce f4537322` names exactly
`.agent/authored/f282-r4-mutations.py`,
`.agent/authored/f282-r4-product.diff`, `.agent/authored/f282-r4-tests.diff`
— C1b's list. `git diff --name-only f4537322 b5fe04e3` names exactly
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` — C2's
list. `git diff --name-only b5fe04e3 15a2e88c` names exactly
`packages/orchestration/failure_postmortem.py`,
`packages/orchestration/pingpong_job.py`,
`packages/orchestration/pingpong_loop.py`,
`packages/orchestration/run_manifest.py`,
`packages/orchestration/self_use_runner.py` — C3's list. `git diff
--name-only 15a2e88c 4c944b4b` names exactly
`tests/orchestration/test_predictive_budget.py`,
`tests/orchestration/test_self_use_runner.py` — C4's list.

**G3 — the linter on this block**: at C4, in the primary checkout,
`python3 -m apps.cli.main integrity block .remedy-wt/f282-r4-block.md`,
real exit 0:
```
  [OK] item 1 (size): 202 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 30 lines
  [OK] item 10 (open set recomputed): the block states no open-findings count
  [OK] item 24 (gate paths resolve): 24 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G5 before C5
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
```

**G4 — the tests**: in the primary checkout at C4, the ordered pytest
selection (24 paths, including `tests/cli/test_golden_path.py`), run
SERIALLY, real exit 0: `1305 passed in 367.52s (0:06:07)`. The reviewer's
disposable-worktree run without the golden path read `1261 passed, 2
skipped` at exit 0; the primary checkout carries the toolchain the
worktree lacked, so the two skips there ran and passed here (and the
golden-path selection adds its own tests), consistent with the block's
own note ("a skip may pass in the primary checkout"). `python3 -m ruff
check packages/orchestration/pingpong_loop.py
packages/orchestration/pingpong_job.py
packages/orchestration/self_use_runner.py
packages/orchestration/run_manifest.py
packages/orchestration/failure_postmortem.py
tests/orchestration/test_predictive_budget.py
tests/orchestration/test_self_use_runner.py`: real exit 0, "All checks
passed!". `python3 -m apps.cli.main integrity check --json`: real exit 0,
`check_count: 6`, all six checks (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`,
`high_blockers_open`) `pass`, `fail_count: 0`, `ok: true`, `passed: true`.

**G5 — the red proofs**: `git worktree add --detach .remedy-wt/f282-r4-mut
4c944b4b` succeeded. `python3 -B .remedy-wt/f282-r4-payloads/mutations.py
.remedy-wt/f282-r4-mut` (real exit 0), whole output:
```
control_before REAL_EXIT=0
133 passed in 13.00s
m1_a_timeout_reads_unavailable FROM count in packages/orchestration/pingpong_loop.py: 1
m1_a_timeout_reads_unavailable REAL_EXIT=1
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_timed_out_builder_call_is_recorded_as_a_timeout
1 failed, 132 passed in 12.28s
m1_a_timeout_reads_unavailable restored byte-identical: True
m2_a_timeout_records_no_detail FROM count in packages/orchestration/pingpong_job.py: 1
m2_a_timeout_records_no_detail REAL_EXIT=1
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_timed_out_builder_call_is_recorded_as_a_timeout
1 failed, 132 passed in 11.72s
m2_a_timeout_records_no_detail restored byte-identical: True
m3_the_stop_forgets_the_verdict FROM count in packages/orchestration/pingpong_job.py: 1
m3_the_stop_forgets_the_verdict REAL_EXIT=1
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_call_budget_stop_keeps_the_verdict_the_reviewer_last_reached
1 failed, 132 passed in 11.98s
m3_the_stop_forgets_the_verdict restored byte-identical: True
m4_the_default_cap_ties_the_loop FROM count in packages/orchestration/self_use_runner.py: 1
m4_the_default_cap_ties_the_loop REAL_EXIT=1
FAILED tests/orchestration/test_self_use_runner.py::TestTheSelfUseRoleAndItsBudget::test_the_default_call_cap_stays_above_what_the_loop_can_spend
1 failed, 132 passed in 11.95s
m4_the_default_cap_ties_the_loop restored byte-identical: True
m5_a_passed_cap_is_raised_too FROM count in packages/orchestration/self_use_runner.py: 1
m5_a_passed_cap_is_raised_too REAL_EXIT=1
FAILED tests/orchestration/test_self_use_runner.py::TestTheSelfUseRoleAndItsBudget::test_the_caller_still_overrides_the_budget
FAILED tests/orchestration/test_self_use_runner.py::TestTheSelfUseRoleAndItsBudget::test_a_passed_call_cap_is_never_raised
FAILED tests/orchestration/test_self_use_runner.py::TestAnOrderFileDeclaresItsOwnBudget::test_the_declared_budget_is_what_the_run_is_given
3 failed, 130 passed in 13.03s
m5_a_passed_cap_is_raised_too restored byte-identical: True
r1_loop_before_this_round REAL_EXIT=1
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_timed_out_builder_call_is_recorded_as_a_timeout
1 failed, 132 passed in 12.30s
r1_loop_before_this_round restored byte-identical: True
r2_job_before_this_round REAL_EXIT=1
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_call_budget_stop_keeps_the_verdict_the_reviewer_last_reached
FAILED tests/orchestration/test_predictive_budget.py::TestPredictiveStopAtTheLiveDispatchSafePoint::test_a_timed_out_builder_call_is_recorded_as_a_timeout
2 failed, 131 passed in 12.89s
r2_job_before_this_round restored byte-identical: True
r3_runner_before_this_round REAL_EXIT=1
FAILED tests/orchestration/test_self_use_runner.py::TestTheSelfUseRoleAndItsBudget::test_the_default_call_cap_stays_above_what_the_loop_can_spend
1 failed, 132 passed in 12.05s
r3_runner_before_this_round restored byte-identical: True
control_after REAL_EXIT=0
133 passed in 12.21s
REAL_EXIT=0
```
Matches the reviewer's reading exactly: control_before `133 passed` exit
0; m1 1 failed exit 1; m2 1 failed exit 1; m3 1 failed exit 1; m4 1
failed exit 1; m5 3 failed exit 1; r1 1 failed exit 1; r2 2 failed exit
1; r3 1 failed exit 1; control_after `133 passed` exit 0; every `restored
byte-identical` line True. `git worktree remove --force
.remedy-wt/f282-r4-mut` and `git worktree prune`: both real exit 0. `git
worktree list` afterward: primary checkout plus `.remedy-wt/f282-r4-dry`,
`.remedy-wt/f282-r4-sim` and the four `job-*` worktrees constraint 6
names — nothing else.

## Authored-text proofs

- `.agent/authored/f282-r4-block.md` (C1a) == `.remedy-wt/f282-r4-block.md`:
  byte-identical True (sha256
  `4eb9dc9f3ebedda267f0f2327d4e5be41d515468129bb88816d22982b8777e9c`, 202
  lines).
- `.agent/authored/f282-r4-ledger.diff`, `-decisions.diff`, `-plan.md`
  (C1a) == their `.remedy-wt/f282-r4-payloads/` sources: byte-identical
  True, all three.
- `.agent/authored/f282-r4-product.diff`, `-tests.diff`, `-mutations.py`
  (C1b) == their `.remedy-wt/f282-r4-payloads/` sources: byte-identical
  True, all three.
- `ledger.diff`, `decisions.diff`, `product.diff`, `tests.diff` were
  applied at C2/C3/C4 with `git apply --check` then `git apply` directly
  from the payload's own bytes under `.remedy-wt/f282-r4-payloads/` —
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
| C1a | done | 283 insertions, matches block formula (202+81) exactly |
| C1b | done | 308 insertions, matches block exactly |
| C2 | done | 29/6/8 insertions by `git diff --cached --numstat`, matches block exactly |
| C3 | done | 1/0, 11/4, 15/3, 1/0, 15/2, matches block exactly |
| C4 | done | 53/15 insertions, matches block exactly |
| C5 | done | this handback |
| Round 3 booking | done | `Gate: F282 R3` entry appended to `.agent/live_review.md` via `ledger.diff` |
| R-1040 | done | resolved — booked as one of the two ids leaving the open set at C2 |
| R-1005 | done | resolved — booked as one of the two ids leaving the open set at C2 |
| DECISION F282 D4 | done | recorded at C2 via `decisions.diff` |
| T006 | done | stopped-task verdict kept (`pingpong_job.py`) and default call ceiling clears the loop (`self_use_runner.py`), R-1007, landed at C3 with tests at C4 |
| T007 | done | a timed-out provider call ends `provider_timeout` with detail, R-1016/R-1027/R-1035, landed at C3 (`pingpong_loop.py`, `pingpong_job.py`, `run_manifest.py`, `failure_postmortem.py`) with tests at C4 |
| G1 | done | all readings match; all seven authored copies byte-identical |
| G2 | done | all ten sha256/byte readings match; open-set 23 to 21, R-1005 and R-1040 leaving exactly as named; all four name-only diffs match exactly |
| G3 | done | integrity block linter, real exit 0, all 7 checkable items `[OK]` |
| G4 | done | 1305 passed exit 0 (reviewer's worktree run: 1261 passed/2 skipped, toolchain present here plus golden path); ruff exit 0; integrity check all-pass exit 0 |
| G5 | done | mutation script output matches the reviewer's reading exactly across all nine sub-checks; worktree cleaned up |
| G6 | done | readings reported in the final reply only, per the block |
| Push | done | reported in the final reply only, per the block |

## Deviations & assumptions

None. Every reading this round matched the block's stated expectation
exactly. No payload was edited or retyped; every copy used
`shutil.copyfile` and every diff was applied via `git apply` reading the
payload file directly. The commit sequence landed in the block's exact
order C1a-C1b-C2-C3-C4-C5. This round is SESSION 1 of F282, its fourth
round.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
4, then T008 to T011 — R-0999, R-1015, R-1034 and R-1000. Open findings
count: 21. Operator-questions count: 0.
