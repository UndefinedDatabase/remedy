# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 9

## Session

SESSION 5 of feature F277 · round 9 · rounds so far 9

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`.remedy-wt/f277-r9-block.md` and `docs/roadmap/features/T2_F277.md` in full, verified the
step block's own bytes before using it (R-0954: measured 257 lines, sha256
`171b6284b96f697101108bddbf407d57ee072f5d9e11c07af18a0e05c086074d`, matching both of the
delegation message's readings exactly), found no `.agent/STOP` on disk, verified the branch
was already `feature/f277-machine-contracts` clean at `0ae3d6fd`, then verified all nine
PAYLOADS entries (line count + bytes + sha256) against the block's table before using any of
them — all nine matched exactly, unlike round 8. Executed the full eight-commit bundle
(C1a, C1b, C2-C6, C7) in order, ran all six gates for real, and pushed.

## Range

Review of `0ae3d6fd`..`HEAD`.

## Commits

### 9cd05720 F277 R9 C1a: copy round 9 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r9-block.md | +257/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r9-decisions.md | +54/-0 | byte-for-byte copy of decisions.md payload |
| .agent/authored/f277-r9-ledger.md | +4/-0 | byte-for-byte copy of ledger.md payload |
| .agent/authored/f277-r9-plan.md | +49/-0 | byte-for-byte copy of plan.md payload |
| .agent/authored/f277-r9-slips.md | +3/-0 | byte-for-byte copy of slips.md payload |

Measured insertions: 367 (257+54+4+49+3). Block's formula: block's own line count (257) plus
110 = 367. Matches exactly.

### 50f54398 F277 R9 C1b: book rounds 7 and 8, record DECISION F277 D8, rewrite plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +54/-0 | append DECISION F277 D8 (decisions.md payload) |
| .agent/live_review.md | +4/-0 | append round 7 PASS + round 8 stop entries (ledger.md payload) |
| .agent/plan.md | +29/-27 | rewrite to plan.md payload, byte-identical |
| .agent/prose_slips.md | +3/-0 | append three slip lines (slips.md payload) |

Measured insertions by `git show --numstat`: 90 (54+4+29+3). Matches the block's expected
reading exactly. Note: `git commit`'s own terminal summary printed "110 insertions(+), 47
deletions(-)" because of rename-detection folding on the `.agent/plan.md` rewrite (a 74%
similarity match) — the `git show --numstat` reading of 90 is the one DECISION F104 D1 fixes,
per the block's own warning.

### 2dfc45c8 F277 R9 C2: migrate the job context group onto the shared fail helper
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job_context_cmd.py | +9/-9 | apply s1-job-context.diff: migrate onto `fail()` |
| tests/cli/test_job_context_cmd.py | +49/-0 | apply s1-job-context.diff: new coverage |

Measured insertions: 58 (9+49). Matches expected exactly.

### a2f73eb1 F277 R9 C3: migrate the worker group onto the shared fail helper
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/worker.py | +9/-9 | apply s2-worker.diff: migrate onto `fail()` |
| tests/cli/test_worker.py | +37/-0 | apply s2-worker.diff: new coverage |

Measured insertions: 46 (9+37). Matches expected exactly.

### cf7e6d1b F277 R9 C4: migrate the change group onto the shared fail helper
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/change.py | +9/-13 | apply s3-change.diff: migrate onto `fail()` |
| tests/cli/test_change_proof_cli.py | +34/-3 | apply s3-change.diff: new + adjusted coverage |

Measured insertions: 43 (9+34). Matches expected exactly.

### 9ab60690 F277 R9 C5: migrate the blocker group onto the shared fail helper
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/blocker.py | +9/-7 | apply s4-blocker.diff: migrate onto `fail()`, thread `json_output` into `_cmd_blocker_resolve` |
| tests/cli/test_blocker_cmd.py | +42/-0 | apply s4-blocker.diff: new coverage |

Measured insertions: 51 (9+42). Matches expected exactly.

### 23345808 F277 R9 C6: migrate the contract group onto the shared fail helper
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/contract_cmd.py | +10/-8 | apply s5-contract.diff: migrate onto `fail()` |
| tests/cli/test_contract_cmd.py | +18/-0 | apply s5-contract.diff: new coverage |

Measured insertions: 28 (10+18). Matches expected exactly.

### (this commit) F277 R9 C7: rewrite handoff for round 9
Self-reference exception (handback template): a handback cannot table the commit that writes
it. This is the round's single handoff-writing commit — no trailing bookkeeping trims are
expected.

## External actions

- `git worktree add --detach .remedy-wt/f277-r9-g5 23345808` — succeeded, for G5's mutation
  red-proofs.
- `git worktree remove .remedy-wt/f277-r9-g5` — succeeded, as G5's last action.
- `git push -u origin feature/f277-machine-contracts` — reported under Verification/G6 below
  (the round's final act).

## Verification

### Pre-flight

- `ls .agent/STOP` → `No such file or directory`.
- `git status --porcelain` → empty.
- `git branch --show-current` → `feature/f277-machine-contracts`.
- `git rev-parse HEAD` → `0ae3d6fd92a148255a5fdd79a72b44e403d078dd`. Matches the block's stated tip.
- Block self-verification (R-0954): measured 257 lines, sha256
  `171b6284b96f697101108bddbf407d57ee072f5d9e11c07af18a0e05c086074d` for
  `.remedy-wt/f277-r9-block.md`. Both match the delegation message's two readings exactly.

### G1(a) — PAYLOADS transport, all nine files

| file | lines measured | lines expected | bytes measured | bytes expected | sha256 match |
|---|---|---|---|---|---|
| ledger.md | 4 | 4 | 7291 | 7291 | True (`01c2d43b...`) |
| decisions.md | 54 | 54 | 4185 | 4185 | True (`2b34e363...`) |
| plan.md | 49 | 49 | 2643 | 2643 | True (`db374813...`) |
| slips.md | 3 | 3 | 2838 | 2838 | True (`43c314a0...`) |
| s1-job-context.diff | 104 | 104 | 4620 | 4620 | True (`8708c77f...`) |
| s2-worker.diff | 105 | 105 | 4102 | 4102 | True (`3f128a0d...`) |
| s3-change.diff | 136 | 136 | 6203 | 6203 | True (`e6f0d0dc...`) |
| s4-blocker.diff | 112 | 112 | 4306 | 4306 | True (`97cac518...`) |
| s5-contract.diff | 91 | 91 | 3832 | 3832 | True (`ec46cc2c...`) |

All nine equal. `git apply --check` exit code for each of the five `.diff` files: 0 (all
five), run before the corresponding `git apply`.

### G1(b) — the five `.agent/authored/f277-r9-*` copies vs. their sources

| copy | source | `cmp -s` result |
|---|---|---|
| f277-r9-block.md | .remedy-wt/f277-r9-block.md | True |
| f277-r9-ledger.md | .remedy-wt/f277-r8-payloads/ledger.md | True |
| f277-r9-decisions.md | .remedy-wt/f277-r8-payloads/decisions.md | True |
| f277-r9-plan.md | .remedy-wt/f277-r8-payloads/plan.md | True |
| f277-r9-slips.md | .remedy-wt/f277-r8-payloads/slips.md | True |

Five readings, all True.

### G1(c) — the three appends at C1b, pre/payload/post, plus the negative control

| file | pre (bytes at 0ae3d6fd) | payload (bytes) | post (bytes at C1b) | pre+payload=post |
|---|---|---|---|---|
| .agent/live_review.md | 423688 | 7291 | 430979 | True |
| .agent/decisions.md | 1779057 | 4185 | 1783242 | True |
| .agent/prose_slips.md | 337487 | 2838 | 340325 | True |

Three readings, all True. Negative control: copied the post-append `.agent/live_review.md`
to scratch, flipped one bit inside the appended region (byte offset 423688+50), and compared
against the real post-append file with `cmp -s`: result False (files differ), as required.

### G1(d) — `.agent/plan.md` at C1b vs. `plan.md` payload

Both sha256 `db3748130146fca29e99acbd0215b3d531f4f90e60a86cdfcd4fb507cf54fb64`. Equal.
49 lines, under the 50-line rule.

### G1(e) — open set by distinct id in `.agent/live_review.md`

At `0ae3d6fd`: 27 distinct ids matching `^- R-\d+ — ` minus 7 distinct ids matching
`^Done: R-\d+ — ` (via `comm -23` on sorted id lists) = 20.
At C1b (`50f54398`): re-measured the same way = 20 (round 9 registers and resolves nothing
under this pattern, so the append to `.agent/live_review.md` — two `Gate:` entries — does not
change the distinct-id open count).
Both readings: 20 and 20, as required — reported as measured, not merely claimed equal.

### G2 — code transport, blob ids at C6 (23345808)

| path | blob id measured | blob id expected | match |
|---|---|---|---|
| apps/cli/commands/job_context_cmd.py | 9199a10bc9894c785bdef09a0c20a46dab9cf564 | same | True |
| tests/cli/test_job_context_cmd.py | aeb4a43a0f761f6ffa5ab709e247cd498aca5ad4 | same | True |
| apps/cli/commands/worker.py | e57de9a68cc816eba47bde66f432304d4621b6b9 | same | True |
| tests/cli/test_worker.py | e78d19aa662845a9cf9dc2a693502452f50cd14f | same | True |
| apps/cli/commands/change.py | 5e35870792338ae383cfaec682b84add33ce9cb3 | same | True |
| tests/cli/test_change_proof_cli.py | 1d10f4f604e1c51da85deb7cbefa3a4fbc79a29d | same | True |
| apps/cli/commands/blocker.py | ff93fed06e62010f7507dc4018aea2bc3dea770f | same | True |
| tests/cli/test_blocker_cmd.py | d64d3b645fba5ff6547ba5108762dd7eb4a6b7e1 | same | True |
| apps/cli/commands/contract_cmd.py | 8a23d6014cccb0237246ef721e9ebef857d30c24 | same | True |
| tests/cli/test_contract_cmd.py | a1d4ca7191c612cffa7136adc5b92b58f8f40af0 | same | True |

All ten match. `git diff --name-only 50f54398 23345808` named exactly these ten paths, length
10, no eleventh.

### G3 — targeted suite, in the primary checkout at C6

```
$ python3 -m pytest -q -p no:cacheprovider tests/cli/test_blocker_cmd.py \
  tests/cli/test_change_proof_cli.py tests/cli/test_job_context_cmd.py \
  tests/cli/test_mission_cmd.py tests/cli/test_worker_facade_cmd.py \
  tests/cli/test_worker.py tests/cli/test_contract_cmd.py \
  tests/orchestration/test_command_discovery.py \
  tests/orchestration/test_development_artifact_boundary.py \
  tests/orchestration/test_disk_floor.py tests/storage/test_persistence.py \
  tests/test_grouped_cli.py tests/test_command_catalog.py \
  tests/cli/test_command_catalog.py tests/orchestration/test_import_reachability.py \
  tests/test_no_orphan_modules.py tests/cli/test_golden_path.py tests/docs
1018 passed in 345.18s (0:05:45)
```
Exit code: 0. Matches the reviewer's dry-run reading of `1018 passed` exactly. Full suite was
NOT run, per amend0917 rule 1.

### G4 — lint over the ten G2 paths

```
$ python3 -m ruff check apps/cli/commands/job_context_cmd.py tests/cli/test_job_context_cmd.py \
  apps/cli/commands/worker.py tests/cli/test_worker.py apps/cli/commands/change.py \
  tests/cli/test_change_proof_cli.py apps/cli/commands/blocker.py tests/cli/test_blocker_cmd.py \
  apps/cli/commands/contract_cmd.py tests/cli/test_contract_cmd.py
All checks passed!
```
Exit code: 0.

### G6 — push and tree, after C7

- `git push -u origin feature/f277-machine-contracts` → `0ae3d6fd..29f2b0af
  feature/f277-machine-contracts -> feature/f277-machine-contracts`, branch set to track the
  remote. Succeeded.
- `git status --porcelain` after push: empty.
- `git worktree list` after push:
```
/home/decodeux/Repos/remedy                                  29f2b0af [feature/f277-machine-contracts]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```
  Primary checkout plus the two pre-existing `remedy/job-*` worktrees, nothing else.

### G5 — mutation red-proofs, disposable worktree

`git worktree add --detach .remedy-wt/f277-r9-g5 23345808` → succeeded, detached HEAD at
`23345808`.

Unmutated control: `72 passed in 10.02s`, exit 0. Matches the reviewer's `72 passed` reading.

| mutation | anchor count | result | exit | failed node ids |
|---|---|---|---|---|
| (a) job_context_cmd.py: drop `, exit_code=2` from `no_target_repo` call | 1 | 3 failed, 69 passed | 1 | `test_job_without_target_repo_exits_two`, `test_a_ping_pong_job_without_a_repo_path_exits_two`, `TestJobContextRefusesInTheCallersShape::test_no_target_repo_is_exit_two_and_names_its_token` |
| (b) job_context_cmd.py: drop `, exit_code=3` from `task_not_resolvable` call | 1 | 2 failed, 70 passed | 1 | `test_unknown_task_exits_three_and_names_nothing_it_did_not_find`, `TestJobContextRefusesInTheCallersShape::test_an_unresolvable_task_is_exit_three` |
| (c) worker.py: `"unknown_provider"` → `"bad_provider"` | 1 | 1 failed, 71 passed | 1 | `TestAWorkerRefusalIsShapedLikeTheCaller::test_an_unknown_provider_is_an_envelope_under_json` |
| (d) change.py: `invalid_path` call's `json_output=json_output` → `json_output=False` | 1 | 1 failed, 71 passed | 1 | `test_a_traversing_path_is_refused_as_an_envelope_under_json` |
| (e) blocker.py: `_cmd_blocker_show`'s message text `blocker not found` → `no blocker` (anchor includes the preceding `sr = get_stop_reason(...)` line to disambiguate from the identical text in `_cmd_blocker_resolve`) | 1 | 1 failed, 71 passed | 1 | `TestABlockerRefusalIsShapedLikeTheCaller::test_without_json_it_is_the_line_it_always_was` |
| (f) contract_cmd.py: `"invalid_contract"` → `"contract_error"` | 1 | 1 failed, 71 passed | 1 | `TestTheMissionView::test_under_json_that_same_refusal_is_an_envelope_on_stdout` |

Every reading matches the block's expected numbers and node ids exactly. Each file was
restored byte-identically after its mutation (`git checkout --` in the worktree, confirmed
with `git status --porcelain` empty after every single revert). No mutation stayed green.

Restored control (after all six reverts): `72 passed in 9.47s`, exit 0. `git status
--porcelain` in the mutation worktree: empty.

`git worktree remove .remedy-wt/f277-r9-g5` → succeeded. `git worktree list` after removal
shows the primary checkout and the two pre-existing `remedy/job-*` worktrees only (see G6).

## Authored-text proofs

The five `.agent/authored/f277-r9-*` files copied at C1a were each compared byte-for-byte
(`cmp -s`) against their reviewer-authored source under `.remedy-wt/f277-r8-payloads/` (the
block copy against `.remedy-wt/f277-r9-block.md`). All five: True. See G1(b) above.

## Deviations & assumptions

1. The block's ordered commit sequence (C1a, C1b, C2, C3, C4, C5, C6, C7) was followed
   exactly, with no dropped, added, or reordered commit among the eight the block named. All
   nine payloads verified clean this round, unlike round 8 — the reviewer's fix (re-measuring
   `decisions.md` after its last edit) held. All six gates ran for real with no red result.
2. **One trailing bookkeeping commit beyond C7.** C7 wrote this handoff with the G6 push
   outcome not yet knowable (the push is C7's own trailing action); a second, small commit
   filled in the real `git push`/`git status`/`git worktree list` readings for G6 once they
   existed. This is the handback template's explicit "trailing bookkeeping commits that only
   trim it" exception (R-0149 pattern), the same shape round 8's C-STOP-fix used — it adds no
   new fact beyond the actual G6 output.

## Next

T003 continues over the modules that need threading next, measured by `sys.exit` site: `job`
(44), `decision` (31), `project` (25), `brain` (24), `do` (19), `patch` (18), `mission` (12),
`memory` (9), `grouped` (8), `test_cmds` (7), then the tail; `runtime_cmd.py` is its own round.
