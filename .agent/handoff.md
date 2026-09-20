# Handoff — F276 Data-root hygiene & disk budget · Round 5

## Session

SESSION 1 of feature F276 · round 5 · rounds so far 5

Context self-assessment: the worker read the step block and verified its sha256 (`7912cf78…`, 105 lines) before anything else, then AGENTS.md in full, `docs/agents/handback_template.md`, `docs/roadmap/features/T2_F276.md`, the `decisions.md` payload (DECISION F276 D6, which rules where the block is terser), the `ledger.md` payload carrying round 4's verdict and the three registrations, the `prose_slips.md` payload, and the whole 674-line code diff before applying a single slice of it, and held all of it without loss; every numeral below is the output of a command run in this round, not a recollection.

## Range

Review of a112e1fa..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 5 books round 4's verdict, registers R-1003, R-1004 and R-1005, and repairs the regression F276's own round 4 introduced.
- C1 books round 4's PASS ON WHAT IT GATED over the five commits of `543863a0`..`a112e1fa` and records that the gate list itself was too narrow; registers R-1003 (High), R-1004 (Medium) and R-1005 (Medium); appends DECISION F276 D6 and the round-4 gate slip; rewrites the plan. The five reviewer payloads are saved byte-exact under `.agent/authored/`.
- C2 is the repair: `_finalize_job_workspace`'s no-handle branch returns and frees nothing, `_release_job_workspace_copy` is deleted rather than left uncalled, and `job_apply._release_consumed_staging_copy` frees the copy after an apply whose status is exactly `applied` and whose record is already durable. Every other outcome keeps the copy.
- C3 rewrites the architecture section and amends the feature file's T003 and its acceptance line in place.
- C4 is this handoff. No pull request was opened.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 the repair and its tests | done | production and tests in one commit, as the block orders |
| C3 the docs | done | |
| C4 handoff | done | |
| G1 transport + state | done | 14 readings, every one True |
| G2 code transport | done | five object ids exactly as ordered; six paths and no other |
| G3 the consumer first | done | `579 passed in 174.72s`, exit 0, 0 failed; the pair measured |
| G4 ruff | done | `All checks passed!`, exit 0 |
| G5 mutation red-proofs | done | control green; both mutations red; neither stayed green |
| G6 push + clean tree | done | reported in the round report; it follows this commit |
| R-1003 | done | repaired at C2; it stays OPEN in the ledger — only the reviewer resolves |
| R-1004 | registered | Medium, owner F282; not this round's to fix |
| R-1005 | registered | Medium, owner F282; not this round's to fix |

Landed: R-1003 — repaired by C2 `e754a6db`, with its docs at C3 `458ffe25`. It remains OPEN in the committed ledger and in the counts below: only the reviewer's own authored text resolves a finding.

## Commits

### b86e0e6d F276 R5 C1: the round 5 bookkeeping

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r5-block.md | 105/0 | byte copy of the step block |
| .agent/authored/f276-r5-decisions.md | 47/0 | byte copy of the D6 payload |
| .agent/authored/f276-r5-ledger.md | 8/0 | byte copy of the ledger payload |
| .agent/authored/f276-r5-plan.md | 31/0 | byte copy of the plan payload |
| .agent/authored/f276-r5-prose_slips.md | 1/0 | byte copy of the prose-slip payload |
| .agent/decisions.md | 47/0 | `a112e1fa` bytes + the D6 payload |
| .agent/live_review.md | 8/0 | `a112e1fa` bytes + the ledger payload: round 4's verdict and R-1003/R-1004/R-1005 |
| .agent/plan.md | 7/8 | rewritten to the plan payload |
| .agent/prose_slips.md | 1/0 | `a112e1fa` bytes + the one-line round-4 gate slip |

Insertions 255.

### e754a6db F276 R5 C2: the R-1003 repair

| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/job_apply.py | 84/1 | `APPLY_STATUS_RELEASES_STAGING`, `_release_consumed_staging_copy`, the call after `_apply_from_workspace`, the `staging_release` field and its summary line |
| packages/orchestration/pingpong_job.py | 16/59 | `_release_job_workspace_copy` deleted; the no-handle branch returns and frees nothing; the docstring states the asymmetry |
| tests/orchestration/test_job_apply.py | 18/3 | `test_approve_verifies_file_contents` reads the workspace BEFORE the apply and gains `assert result.files_applied` |
| tests/orchestration/test_staging_lifecycle.py | 189/30 | the hook keeps a copy in every state including COMPLETED; eight end-to-end apply cases over a real `run_job` with fake providers; the no-op and the worktree-job cases |

Insertions 307.

### 458ffe25 F276 R5 C3: the docs

| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/features/T2_F276.md | 38/4 | T003's opening line amended in place, the round-5 amendment, the rewritten acceptance line |
| docs/system/architecture.md | 37/20 | the "freed where its work is CONSUMED" section replaces the terminal-hook one; the two layers restated with the apply as the stricter caller |

Insertions 75.

## External actions

- `git worktree add --detach .remedy-wt/f276-r5-base a112e1fa` — created for G3's base reading; removed with `git worktree remove --force` as that step's last action.
- `git worktree add --detach .remedy-wt/f276-r5-mut 458ffe25` — created for G5; removed with `git worktree remove --force` as that step's last action.
- `git worktree list` after both removals shows the primary checkout plus `.remedy-wt/f276-proto5`, `.remedy-wt/f276-proto5-base` and `.remedy-wt/job-468c8e62a2cc4fac`, all three untouched. Nothing was pruned.
- `git push origin feature/f276-data-root-hygiene` — follows this commit; its result is in the round report.
- No pull request was created, edited or merged. No `gh` command was run.

## Verification

- G1 transport + state — a python check printed 14 readings, every one True: each of the five payload digests matches the block's, `.agent/live_review.md` / `.agent/decisions.md` / `.agent/prose_slips.md` each equal their `a112e1fa` bytes plus their payload as committed at C3, `.agent/plan.md` equals the plan payload, and each of the five `.agent/authored/f276-r5-*` copies equals its payload. SAVED BLOCK `.agent/authored/f276-r5-block.md`: lines=105 sha256=`7912cf784cfa90f39faebfa79de129cae6af20c261432f42292c306e4c2df463`; the block's own bytes: lines=105 sha256=`7912cf784cfa90f39faebfa79de129cae6af20c261432f42292c306e4c2df463`. Identical.
- G2 code transport — `git rev-parse 458ffe25:packages 458ffe25:apps 458ffe25:tests` printed `9e1b3373800e449a81a7ebb2f2f56975d0b58297`, `c6512f5298473ca4de84e8c8dbb811283c8e0f60`, `0f4b7d2c49dc32ab41f5ba8acacda65f4ee32b66`; `git rev-parse 458ffe25:docs/system/architecture.md 458ffe25:docs/roadmap/features/T2_F276.md` printed `8a44350174409c3ddc6900e8098c786c43f4cbc4` and `9867b144cba64de8a17e3d2e3266a1f8275b47ab` — all five exactly the objects the block names. `git diff --name-only b86e0e6d 458ffe25` printed 6 paths and no other: `docs/roadmap/features/T2_F276.md`, `docs/system/architecture.md`, `packages/orchestration/job_apply.py`, `packages/orchestration/pingpong_job.py`, `tests/orchestration/test_job_apply.py`, `tests/orchestration/test_staging_lifecycle.py`.
- G3 the consumer first — the eleven-path command, serial, no `-n`, in the primary checkout: `579 passed in 174.72s (0:02:54)`, exit 0, 0 failed. THE MEASURED PAIR, two separate readings: (i) `tests/orchestration/test_job_apply.py` alone at C3 in the primary checkout — `88 passed in 92.68s (0:01:32)`, exit 0; (ii) the same file alone at `a112e1fa` in the disposable worktree `.remedy-wt/f276-r5-base` — `19 failed, 69 passed in 11.66s`, exit 1, the 19 node ids being `TestDryRunCompleted::{test_completed_job_dry_run_ready, test_dry_run_human_readable, test_dry_run_json_machine_verifiable}`, `TestDryRunMissingWorkspace::test_missing_workspace_blocks`, `TestApproveRequiresFlag::test_no_approve_no_dry_run_is_dry_run`, `TestApproveApplies::{test_approve_applies_safe_files, test_approve_does_not_push, test_approve_reports_applied_files}`, `TestApprovePostTest::{test_post_apply_test_runs, test_post_apply_test_failure_reported}`, `TestJobApplyRecord::{test_dry_run_persists_record, test_approved_persists_record, test_the_record_is_stored_under_job_apply_records_by_its_job_apply_id}`, `TestCLICommandShape::{test_cli_dry_run_json, test_cli_text_output}`, `TestTargetClobberBlocked::{test_target_modified_after_job_blocks, test_clean_target_allows_apply}`, `TestJobApplyRecordPersistence::test_unwritable_job_apply_record_dir_blocks_approved` and `TestCLICommandPaths::test_cli_approve_applies`. The regression is red at the base and green at C3.
- G4 ruff — `python3 -m ruff check packages/orchestration/pingpong_job.py packages/orchestration/job_apply.py tests/orchestration/test_staging_lifecycle.py tests/orchestration/test_job_apply.py` printed `All checks passed!`, exit 0.
- G5 mutation red-proofs — one disposable worktree `.remedy-wt/f276-r5-mut` at C3, `__pycache__` purged before each run, `python3 -B`. The imports resolved inside the worktree: `/home/decodeux/Repos/remedy/.remedy-wt/f276-r5-mut/packages/orchestration/job_apply.py` and `…/pingpong_job.py`, so no editable install shadowed them. CONTROL (unmutated): `115 passed in 15.79s`, exit 0. (a) the line `            _release_consumed_staging_copy(job, copy_out)` in `job_apply.py`, counted 1 occurrence, replaced by `pass`: exit 1, `4 failed, 111 passed in 16.24s`, FAILED `test_an_applied_copy_jobs_staging_copy_is_gone_after_the_apply`, `test_a_dry_run_apply_leaves_the_staging_copy_in_place`, `test_a_blocked_apply_leaves_the_staging_copy_in_place`, `test_a_second_apply_of_the_same_job_finds_its_source_gone`, all in `tests/orchestration/test_staging_lifecycle.py` — the four nodes R-1003's red proof predicts. (b) the two lines `    if handle is None:` and its `        return` in `pingpong_job._finalize_job_workspace`, counted 1 occurrence, replaced by that branch releasing a completed copy job again — T003's own bug restored: exit 1, `22 failed, 87 passed, 6 errors in 12.63s`. The guard `test_a_completed_copy_job_keeps_its_staging_copy_through_the_hook` went red, together with `test_the_terminal_hook_keeps_every_copy_job_whatever_its_state[completed]` and 20 nodes of `tests/orchestration/test_job_apply.py` — the 19 of the base reading plus `TestApproveApplies::test_approve_verifies_file_contents`, which C2 strengthened. The 6 errors, read with a second `-rfE` run rather than inferred, are the six `copy_job`-fixture tests of `test_staging_lifecycle.py`, whose fixture asserts "the job's own copy must survive its completion": `test_a_completed_copy_job_that_was_never_applied_keeps_its_copy`, `test_an_applied_copy_jobs_staging_copy_is_gone_after_the_apply`, `test_a_dry_run_apply_leaves_the_staging_copy_in_place`, `test_an_unapproved_apply_leaves_the_staging_copy_in_place`, `test_a_blocked_apply_leaves_the_staging_copy_in_place`, `test_a_second_apply_of_the_same_job_finds_its_source_gone`. NO MUTATION STAYED GREEN. Both files restored byte-identically — `job_apply.py` `48d0cb4f30d9be1ad6a0213a0a8dd14b4d19d9f36269785c547aa607180b9992`, `pingpong_job.py` `5ef6ac73f9a235d51f337863cb8d8f3bccf72430e6e590960bafede10098ea4f`, each matching its pre-mutation reading — the worktree's `git status --porcelain` was empty before removal, and `git worktree list` after removal shows the primary checkout and the three worktrees this round was told not to touch.
- G6 push + clean tree — follows this commit; the reading is in the round report.

## Open findings

17 by distinct id and 17 by the canonical formula `scripts/rotate_live_review.py::count_open_findings`, both measured on the committed ledger at `458ffe25:.agent/live_review.md`: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880, R-0892, R-0950, R-0984, R-0998, R-0999, R-1000, R-1003, R-1004, R-1005. By severity: 1 High (R-1003, repaired this round and awaiting the reviewer's own resolution), 9 Medium, 7 Low. Fourteen were open at `a112e1fa`; this round's three registrations are the difference.

## Authored-text proofs

All five reviewer payloads were copied with `shutil.copyfile` and never retyped. Disk-to-disk, as committed at C3 against the reviewer's scratch originals: `.agent/authored/f276-r5-block.md`, `-ledger.md`, `-decisions.md`, `-plan.md` and `-prose_slips.md` each compare byte-equal to their payload, and the three appended record files each equal their `a112e1fa` bytes plus their payload exactly. Every digest was verified before use and again at G1. The code diff was applied with `git apply` in the block's two disjoint `--include` slices; no hunk was retyped or edited.

## Deviations & assumptions

- THE BLOCK'S COMMIT SEQUENCE WAS FOLLOWED EXACTLY: C1, C2, C3, C4, no extra commit, none dropped, none reordered.
- Mutation (b) reddened MORE than the ledger's R-1003 paragraph predicts. That paragraph says "the guard … and 21 further nodes go red, the 19 of `test_job_apply.py` among them"; the measured reading is 22 failed plus 6 errors. The cause is in this round's own C2: `TestApproveApplies::test_approve_verifies_file_contents` used to pass VACUOUSLY when the apply blocked, because `result.files_applied` was empty and its loop body never ran, which is why it is absent from the base's 19; C2 added `assert result.files_applied`, so it now goes red for the right reason. The 6 errors are the new `copy_job` fixture refusing to set up when the hook eats the copy. Both readings are stronger than predicted, not weaker, and no assertion was weakened anywhere.
- An extra reading beyond the block's literal ordering: mutation (b) was run a second time with `-rfE` so the six error node ids could be READ rather than inferred. It mutated and restored the same file byte-identically and left the worktree clean.
- R-1004's cost is visible in this round's own gates and is recorded as a measurement, not a complaint: G3's eleven-path run took 277s of wall clock for 174.72s of tests in the primary checkout, and `test_job_apply.py` alone took 178.83s wall for 92.68s of tests there against 11.93s wall for the whole run in a worktree. The data-root fingerprint of `tests/conftest.py` is the difference; the operator's `.data` was never read, listed or written by this worker.
- Every `REMEDY_DATA_DIR` in play is set in-process by the suite's own fixtures. No shell assignment was used, no provider was called, and pytest ran serially with no `-n` in every invocation.

## Next

1. Phase 1 rule 1 — re-read `.agent/STOP` from disk; if it exists, write the handoff and end the session, doing nothing else.
2. Otherwise review round 5: re-run G1 to G6 independently and read `git diff a112e1fa..HEAD` bottom-up, then book the verdict. R-1003 is repaired here and still open in the ledger — its resolution paragraph is the reviewer's to write.
3. Then T004 — `min_free_disk_bytes` on `JobBudgets` behind an injectable probe, the `free_disk` limit inside `evaluate_budget`, the STOPPED path with post-mortem status `disk_exhausted`, and a `doctor` disk section.

Operator questions open: 5
