# Handback — F282 Findings paydown v2 · Round 9 · Book round 8, resolve R-0866 and land T018: R-1028 and R-0950's first group

## Session

SESSION 2 of feature F282 · round 9 · rounds so far 9

This round booked round 8's PASS and the resolution of R-0866 into the
ledger, recorded DECISION F282 D9, and landed T018's two repairs: the
runtime cleanup scans in `tests/runtimes/runtime_cleanup.py` now match a
temporary path as a path (a new `names_path` helper requires a path
separator, whitespace or end-of-text after the root), so worker gw1's
scans no longer count gw10's through gw19's live runtimes as its own
survivors (R-1028); and `TestTwoRealRunsShareLogicalIdentity` in
`tests/orchestration/test_run_manifest_logical_identity.py` now freezes
Remedy's own checkout identity at test start via a `frozen_remedy_identity`
fixture, so a neighbour test writing into the shared checkout between the
two runs can no longer change the hash the comparison reads (R-0950's
first group). R-0950's other two groups and R-0499 are carried open by
name, per DECISION F282 D9. Roughly three-fifths of this session's
working-context budget remained at handback.

## Range

Review of `5c43004f`..`HEAD`.

## Commits

### c29fcf15 F282 R9 C1a: copy round 9 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r9-block.md | +204/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f282-r9-decisions.diff | +44/-0 | Payload copy |
| .agent/authored/f282-r9-ledger.diff | +12/-0 | Payload copy |
| .agent/authored/f282-r9-plan.md | +30/-0 | Payload copy |

Measured insertions by `git diff --stat --cached` before commit: 290
(204+86), matching the block's stated formula "this block's line count
plus 86" exactly. Under the 500 cap.

### edc2ec15 F282 R9 C1b: copy round 9 product and test payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r9-mutations.py | +63/-0 | Payload copy |
| .agent/authored/f282-r9-product.diff | +100/-0 | Payload copy |
| .agent/authored/f282-r9-tests.diff | +95/-0 | Payload copy |

Measured insertions by `git diff --stat --cached` before commit: 258,
matching the block's expected 258 exactly.

### c66ceaa1 F282 R9 C2: book round 8, resolve R-0866 and record DECISION F282 D9

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | `ledger.diff` applied: `Gate: F282 R8` entry and the `Done:` line of R-0866 |
| .agent/decisions.md | +36/-0 | `decisions.diff` applied: DECISION F282 D9 (R-1028 cause and fix; R-0950 ruled in three groups, first repaired here; R-0499 carried) |
| .agent/plan.md | +10/-11 | Rewritten to the round-9 `plan.md` payload (via `shutil.copyfile`) |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 36/0 decisions.md, 4/0 live_review.md, 10/11 plan.md — matching
the block's expected numbers exactly.

### 468f4245 F282 R9 C3: match a temporary path as a path and freeze the checkout under real runs, R-1028 and R-0950

| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_run_manifest_logical_identity.py | +33/-0 | `product.diff` applied: new `frozen_remedy_identity` fixture pins `remedy_worktree_identity()`; new test proves a neighbour changing `worktree_identity` of the shared checkout between the two runs no longer reaches the comparison (R-0950 group 1) |
| tests/runtimes/runtime_cleanup.py | +17/-3 | `product.diff` applied: new `names_path(text, root)` helper (regex requiring a path separator, whitespace or end-of-text after the root); the three prior substring (`root in cmdline`/`root in proc.cwd()`) matching sites replaced with it (R-1028) |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 33/0 test_run_manifest_logical_identity.py, 17/3
runtime_cleanup.py — matching the block's expected numbers exactly.

### b2b32ab0 F282 R9 C4: pin the cleanup scans to their own worker, R-1028

| Path | +/- | Reason |
|---|---|---|
| tests/runtimes/test_runtime_cleanup_scope.py | +89/-0 | `tests.diff` applied (NEW FILE): parametrized `names_path` unit cases, plus three idle-process integration tests proving the file scan and the per-test scan each find only their own worker's process and never a sibling's |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 89/0 — matching the block's expected 89 exactly.

### (this commit) F282 R9 C5: rewrite handoff for round 9

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f282-r9-mut b2b32ab0` for the
  G5 red proofs — succeeded, real exit 0, HEAD detached at `b2b32ab0`.
- `python3 -B .remedy-wt/f282-r9-payloads/mutations.py
  .remedy-wt/f282-r9-mut` — real exit 0.
- `git worktree remove --force .remedy-wt/f282-r9-mut` and
  `git worktree prune` after G5 — both real exit 0; `git worktree list`
  afterward shows only the primary checkout, `.remedy-wt/f282-r9-dry`,
  `.remedy-wt/f282-r9-sim` and the four `job-*` worktrees constraint 6
  names.
- `git push origin feature/f282-findings-paydown-v2` after C5 — real
  outcome reported in the worker's final reply (G6 readings, per the
  block, do not live in this committed file).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form.

## Verification

**G1 — transport**: each of the six payloads' lines/bytes/sha256
measured against the block's PAYLOADS table — all six rows matched
exactly (ledger.diff 12/5621, decisions.diff 44/3698, plan.md 30/1148,
product.diff 100/4726, tests.diff 95/3157, mutations.py 63/2832 — all
sha256 digests equal to the table). The block itself: 204 lines
(newline count), sha256
`488bd30a50dc02cfdc8b75addb51a08b8baf1d7031a6a2c30682912a67c08f4f`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f282-r9-*` blob read with `git show
<commit>:<path>` (block + ledger.diff + decisions.diff + plan.md at
`c29fcf15`; product.diff + tests.diff + mutations.py at `edc2ec15`)
compared byte-for-byte against its `.remedy-wt/f282-r9-payloads/` (or
block) source: all seven pairs byte-identical = True.

**G2 — the bookkeeping and the product**: at C2 (`c66ceaa1`),
`.agent/live_review.md` 425229 bytes, sha256
`9d00783c64d38ba671a11cc8d333388e235bb3d2991425fa23de065dbd32c19d`;
`.agent/decisions.md` 1932265 bytes, sha256
`5d2f6a3494c0ac1e0e1c6b0688e21648a74297a5caec48effc53d3a754ce8fdc`;
`.agent/plan.md` 1148 bytes, sha256
`cebf3383e2d5a74ced8c9ab98ac3082eae332266f5dae566c80fc485557ebefd` —
at C3 (`468f4245`),
`tests/runtimes/runtime_cleanup.py` 9576 bytes, sha256
`b87c08f90f37265c9bd5a1687724d58a745d9eeea235ef9b928f7c34975b8500`;
`tests/orchestration/test_run_manifest_logical_identity.py` 7408 bytes,
sha256
`990a5425aae5840c01359251a4a0239172530e63364b58745be8ef8bdc7c9d68` —
at C4 (`b2b32ab0`),
`tests/runtimes/test_runtime_cleanup_scope.py` 2835 bytes, sha256
`19ef6cf2594791ccd1c8629e90599508686ed0fb7b04e6d3b52dc91cdfbf3b63` —
all six equal to the block's table exactly. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 8 at
`5c43004f`, 7 at C2; set difference: `R-0866` the only id leaving, none
arriving — matching the block's reading exactly. `git diff --name-only
c29fcf15 edc2ec15` names exactly `.agent/authored/f282-r9-mutations.py`,
`.agent/authored/f282-r9-product.diff`,
`.agent/authored/f282-r9-tests.diff` — C1b's list. `git diff
--name-only edc2ec15 c66ceaa1` names exactly `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md` — C2's list. `git diff
--name-only c66ceaa1 468f4245` names exactly
`tests/orchestration/test_run_manifest_logical_identity.py`,
`tests/runtimes/runtime_cleanup.py` — C3's list. `git diff --name-only
468f4245 b2b32ab0` names exactly
`tests/runtimes/test_runtime_cleanup_scope.py` — C4's list.

**G3 — the linter on this block**: at C4, in the primary checkout,
`python3 -m apps.cli.main integrity block .remedy-wt/f282-r9-block.md`,
real exit 0:
```
  [OK] item 1 (size): 204 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 30 lines
  [OK] item 10 (open set recomputed): states 7; .agent/live_review.md holds 7 open by distinct id, and the block registers 0 and resolves 0, leaving 7
  [OK] item 24 (gate paths resolve): 11 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G5 before C5
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
```

**G4 — the tests, the flake and the lint**: in the primary checkout at
C4, the ordered pytest selection (11 paths), run SERIALLY, real exit 0:
```
590 passed, 1 skipped in 197.56s (0:03:17)
```
matching the reviewer's simulation reading of `590 passed, 1 skipped`
at exit 0 in about 200 seconds exactly. Then the flake's own
reproduction, three separate runs of
`tests/orchestration/test_run_manifest_logical_identity.py` +
`tests/runtimes/test_supervisor_portability.py` under `-n auto -rfE`:
```
run 1: 110 passed in 12.69s, REAL_EXIT=0
run 2: 110 passed in 13.85s, REAL_EXIT=0
run 3: 110 passed in 13.70s, REAL_EXIT=0
```
matching the reviewer's simulation reading of `110 passed` at exit 0 in
three runs of three exactly (no reproduction of the `5c43004f`-era `109
passed, 1 error` was attempted or expected at C4). `python3 -m ruff
check tests/runtimes/runtime_cleanup.py
tests/runtimes/test_runtime_cleanup_scope.py
tests/orchestration/test_run_manifest_logical_identity.py`: real exit
0, "All checks passed!". `python3 -m apps.cli.main integrity check
--json`: real exit 0, `check_count: 6`, all six checks
(`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`)
`pass`, `fail_count: 0`, `ok: true`, `passed: true`.

**G5 — the red proofs**: `git worktree add --detach
.remedy-wt/f282-r9-mut b2b32ab0` succeeded, real exit 0. `python3 -B
.remedy-wt/f282-r9-payloads/mutations.py .remedy-wt/f282-r9-mut` (real
exit 0), whole output:
```
control_before REAL_EXIT=0
19 passed in 4.53s
m1_a_root_matches_as_a_substring_again FROM count in tests/runtimes/runtime_cleanup.py: 1
m1_a_root_matches_as_a_substring_again REAL_EXIT=1
FAILED tests/runtimes/test_runtime_cleanup_scope.py::test_a_root_is_named_only_as_itself_or_a_parent[--repo /t/popen-gw10/proj-False]
FAILED tests/runtimes/test_runtime_cleanup_scope.py::test_a_root_is_named_only_as_itself_or_a_parent[--repo /t/popen-gw1x-False]
FAILED tests/runtimes/test_runtime_cleanup_scope.py::test_the_file_scan_skips_a_sibling_basetemp_named_in_argv
FAILED tests/runtimes/test_runtime_cleanup_scope.py::test_the_file_scan_skips_a_server_running_in_a_sibling_basetemp
FAILED tests/runtimes/test_runtime_cleanup_scope.py::test_the_per_test_scan_skips_a_sibling_tmp_path
5 failed, 14 passed in 4.46s
m1_a_root_matches_as_a_substring_again restored byte-identical: True
m2_the_cwd_branch_matches_as_a_substring_again FROM count in tests/runtimes/runtime_cleanup.py: 1
m2_the_cwd_branch_matches_as_a_substring_again REAL_EXIT=1
FAILED tests/runtimes/test_runtime_cleanup_scope.py::test_the_file_scan_skips_a_server_running_in_a_sibling_basetemp
1 failed, 18 passed in 4.61s
m2_the_cwd_branch_matches_as_a_substring_again restored byte-identical: True
m3_the_real_runs_see_the_live_checkout_again FROM count in tests/orchestration/test_run_manifest_logical_identity.py: 1
m3_the_real_runs_see_the_live_checkout_again REAL_EXIT=1
FAILED tests/orchestration/test_run_manifest_logical_identity.py::TestTwoRealRunsShareLogicalIdentity::test_a_checkout_that_changes_between_the_runs_does_not_reach_the_comparison
1 failed, 18 passed in 4.83s
m3_the_real_runs_see_the_live_checkout_again restored byte-identical: True
r1_cleanup_before_this_round REAL_EXIT=2
ERROR tests/runtimes/test_runtime_cleanup_scope.py
1 error in 0.26s
r1_cleanup_before_this_round restored byte-identical: True
control_after REAL_EXIT=0
19 passed in 4.08s
REAL_EXIT=0
```
Matches the reviewer's reading exactly: control_before `19 passed`
exit 0; m1 5 failed exit 1; m2 1 failed exit 1; m3 1 failed exit 1; r1
`1 error` exit 2 (the new test module unable to import `names_path`
from `runtime_cleanup.py` at `5c43004f`); control_after `19 passed`
exit 0; every `restored byte-identical` line True. `git worktree
remove --force .remedy-wt/f282-r9-mut` and `git worktree prune`: both
real exit 0. `git worktree list` afterward: primary checkout plus
`.remedy-wt/f282-r9-dry`, `.remedy-wt/f282-r9-sim` and the four
`job-*` worktrees constraint 6 names — nothing else.

## Authored-text proofs

- `.agent/authored/f282-r9-block.md` (C1a) ==
  `.remedy-wt/f282-r9-block.md`: byte-identical True (sha256
  `488bd30a50dc02cfdc8b75addb51a08b8baf1d7031a6a2c30682912a67c08f4f`,
  204 lines).
- `.agent/authored/f282-r9-ledger.diff`, `-decisions.diff`, `-plan.md`
  (C1a) == their `.remedy-wt/f282-r9-payloads/` sources:
  byte-identical True, all three.
- `.agent/authored/f282-r9-product.diff`, `-tests.diff`,
  `-mutations.py` (C1b) == their `.remedy-wt/f282-r9-payloads/`
  sources: byte-identical True, all three.
- `ledger.diff`, `decisions.diff`, `product.diff`, `tests.diff` were
  applied at C2/C3/C4 with `git apply --check` then `git apply`
  directly from the payload's own bytes under
  `.remedy-wt/f282-r9-payloads/` — never retyped, every `--check` and
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
| C1a | done | 290 insertions, matches block formula (204+86) exactly |
| C1b | done | 258 insertions, matches block exactly |
| C2 | done | 36/0, 4/0, 10/11 insertions/deletions by `git diff --numstat`, matches block exactly |
| C3 | done | 33/0, 17/3, matches block exactly |
| C4 | done | 89/0, matches block exactly |
| C5 | done | this handback |
| Round 8 booking | done | `Gate: F282 R8` entry appended to `.agent/live_review.md` via `ledger.diff` |
| R-0866 | done | resolved — booked as the one id leaving the open set at C2 |
| R-1028 | done | repaired — `names_path` helper matches a root only as itself or a path prefix, landed at C3, pinned at C4 |
| R-0950 group 1 | done | `TestTwoRealRunsShareLogicalIdentity` freezes Remedy's own checkout identity, landed at C3 |
| R-0950 group 2 | skipped | `TestNoFalseWorkspaceDrift` no longer exists — deleted at `3be6ce11`, F273 round 15; nothing to repair |
| R-0950 group 3 | skipped | `test_no_zombie_processes_after_every_outcome` not reproduced in eight loaded targeted runs; stays open, carried by name to the closure |
| R-0499 | skipped | fix clause resolves it only when a red run names the test; no run this feature has; carried by name to the closure |
| DECISION F282 D9 | done | recorded at C2 via `decisions.diff` |
| G1 | done | all readings match; all seven authored copies byte-identical |
| G2 | done | all six sha256/byte readings match; open-set 8 to 7, R-0866 leaving exactly as named; all four name-only diffs match exactly |
| G3 | done | integrity block linter, real exit 0, all 7 checkable items `[OK]` |
| G4 | done | 590 passed, 1 skipped, exit 0 (matches reviewer's simulation reading exactly); three flake-reproduction runs all `110 passed` exit 0; ruff exit 0 all checks pass; integrity check all-pass exit 0 |
| G5 | done | mutation script output matches the reviewer's reading exactly across all six sub-checks (control_before, m1-m3, r1, control_after); worktree cleaned up |
| G6 | done | readings reported in the final reply only, per the block |
| Push | done | reported in the final reply only, per the block |

## Deviations & assumptions

None. Every reading this round matched the block's stated expectation
exactly. No payload was edited or retyped; every copy used
`shutil.copyfile` and every diff was applied via `git apply` reading
the payload file directly. The commit sequence landed in the block's
exact order C1a-C1b-C2-C3-C4-C5. This round is SESSION 2 of F282, its
ninth round.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of
round 9, then the closure sequence. Open findings count: 7.
Operator-questions count: 0.
