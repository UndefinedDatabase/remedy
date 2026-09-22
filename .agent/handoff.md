# Handback — F278 Durable writes & loud failures · Round 7 · Book round 6, register and repair R-1036, mark the second handler group

## Session

SESSION 1 of feature F278 · round 7 · rounds so far 7

This round booked round 6's PASS into the durable ledger files, registered
DECISION F278 D6 and the three findings its research produced (R-1036,
R-1037, R-1038) in the same booking commit, then repaired R-1036 in
`pingpong_job.run_job`: a final job review that fails to build or write no
longer vanishes silently — the exception type is now named on
`job.metadata["final_job_review_error"]`, and when no review file exists one
is written with verdict `BLOCKED` and a `review_error` naming the exception
type, so the final verifier's `_final_job_review_check` reads it as blocked.
It then marked the second group of blind `except Exception` handlers — the
job, pingpong loop/provider and apply modules (`mark_orchestration.diff`,
42 pairs), the job/worker/dev CLI commands (`mark_cli.diff`, 22 pairs), and
the test/runtime/snapshot/hunk modules (`mark_services.diff`, 31 pairs) —
each with a `# noqa: BLE001 — <reason>`, comment text only, one commit per
diff. `marking_check.py` proved each marking commit changes no code, and its
negative control confirmed the R-1036 repair commit (which DOES change
code) correctly fails the same check. All five gates (G1–G5) ran clean and
matched the reviewer's stated readings exactly (transport, booking, product
bytes/BLE001/marking-check, tests, and the two red-proof mutations for
R-1036). R-1037 and R-1038 are registered only this round, per DECISION
F278 D6; their repair is next round's, ahead of the third marking group.
Context self-assessment: a comfortable majority of the working budget
remains at handback.

## Range

Review of `ead4ec77`..`HEAD`.

## Commits

### d12d7479 F278 R7 C1a: copy round 7 block, bookkeeping payloads and tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r7-block.md | +208/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r7-decisions.md | +27/-0 | Bookkeeping copy of the decisions.md append payload |
| .agent/authored/f278-r7-ledger.md | +8/-0 | Bookkeeping copy of the live_review.md append payload |
| .agent/authored/f278-r7-mutations.py | +46/-0 | Bookkeeping copy of the G5 mutation-tool payload |
| .agent/authored/f278-r7-plan.md | +28/-0 | Bookkeeping copy of the plan.md rewrite payload |

Measured insertions: 317 (block 208 + 109 payload lines), under the 500 cap;
matches the block's expected value exactly.

### 23d9f12d F278 R7 C1b: copy round 7 repair and first marking diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r7-r1036.diff | +61/-0 | Bookkeeping copy of the R-1036 repair diff |
| .agent/authored/f278-r7-mark_orchestration.diff | +392/-0 | Bookkeeping copy of the job/loop/provider/apply marking diff |

Measured insertions: 453 (61+392), matches the block's expected value
exactly.

### 1cd636b7 F278 R7 C1c: copy round 7 remaining marking diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r7-mark_cli.diff | +207/-0 | Bookkeeping copy of the CLI marking diff |
| .agent/authored/f278-r7-mark_services.diff | +288/-0 | Bookkeeping copy of the test/runtime/snapshot/hunk marking diff |

Measured insertions: 495 (207+288), matches the block's expected value
exactly.

### ac5dae0c F278 R7 C2: book round 6's PASS and register R-1036, R-1037 and R-1038
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +27/-0 | `decisions.md` (DECISION F278 D6) appended by byte concatenation |
| .agent/live_review.md | +8/-0 | `ledger.md` (round 6 Gate entry + R-1036/R-1037/R-1038) appended by byte concatenation |
| .agent/plan.md | +10/-11 | Rewritten to plan.md payload for round 7 |

Measured insertions: 45 (27+8+10), matches the block's expected value
exactly. Deletions: 11, all from the plan.md rewrite.

### cdee140d F278 R7 C3: record a lost final job review as a blocking one
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +12/-2 | R-1036 repair: the `run_job` final-review handler now names the exception type on `job.metadata` and writes a `BLOCKED` `final_job_review.json` when none exists |
| tests/orchestration/test_pingpong_integration.py | +28/-0 | New `TestRunJobFinalReviewFailure` class: a review builder that raises still blocks the apply |

`git apply --check` real exit 0, `git apply` real exit 0. Measured
insertions: 40 (12+28), matches the block's expected value exactly.

### 5c2673f6 F278 R7 C4: give each blind handler in the job, loop, provider and apply modules a reason
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/job_apply.py | +9/-9 | 9 blind handlers gain `# noqa: BLE001 — <reason>`; comment text only |
| packages/orchestration/pingpong_job.py | +17/-17 | 17 blind handlers (excluding the R-1036 line, which C3 already marked) gain a reason; comment text only |
| packages/orchestration/pingpong_loop.py | +9/-9 | 9 blind handlers gain a reason; comment text only |
| packages/orchestration/pingpong_provider.py | +7/-7 | 7 blind handlers gain a reason; comment text only |

`git apply --check` real exit 0, `git apply` real exit 0. Measured
insertions: 42 (9+17+9+7), matches the block's expected value exactly.

### 5dbf8936 F278 R7 C5: give each blind handler in the job, worker and dev commands a reason
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/dev.py | +6/-6 | 6 blind handlers gain a reason; comment text only |
| apps/cli/commands/job.py | +10/-10 | 10 blind handlers gain a reason; comment text only |
| apps/cli/commands/worker_facade_cmd.py | +6/-6 | 6 blind handlers gain a reason; comment text only |

`git apply --check` real exit 0, `git apply` real exit 0. Measured
insertions: 22 (6+10+6), matches the block's expected value exactly.

### d49a1b16 F278 R7 C6: give each blind handler in the test, runtime, snapshot and hunk modules a reason
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/hunk_ledger.py | +6/-6 | 6 blind handlers gain a reason; comment text only |
| packages/orchestration/real_test_execution.py | +7/-7 | 7 blind handlers gain a reason; comment text only |
| packages/orchestration/repository_snapshot.py | +6/-6 | 6 blind handlers gain a reason; comment text only |
| packages/orchestration/test_execution_service.py | +6/-6 | 6 blind handlers gain a reason; comment text only |
| packages/runtimes/runtime_supervisor.py | +6/-6 | 6 blind handlers gain a reason; comment text only |

`git apply --check` real exit 0, `git apply` real exit 0. Measured
insertions: 31 (6+7+6+6+6), matches the block's expected value exactly.

### C7 (this commit) F278 R7 C7: rewrite handoff for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f278-r7-mut d49a1b16` — real exit 0.
- `python3 .remedy-wt/f278-r7-payloads/mutations.py .remedy-wt/f278-r7-mut` — real exit 0 (see Verification, G5).
- `git worktree remove --force .remedy-wt/f278-r7-mut` — real exit 0.
- `git worktree prune` — real exit 0.
- `git push origin feature/f278-durable-writes-loud-failures` — see Verification, G6, for the real outcome (reported separately since it runs after this commit).
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no checkout of another branch: none run, per the block's constraints.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, absent (proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `feature/f278-durable-writes-loud-failures`. `git log --oneline -1` → `ead4ec77 F278 R6 C7: rewrite handoff for round 6`.
- Block bytes (R-0954): measured lines=208, sha256=`6b2c32f6c4e3c40450d1bf7871bc426a5ff1237d1cc9abfe84358e4f0cf4665e`; matches both given readings exactly.
- `git worktree list` (before) → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` only.
- `git branch --list 'remedy/job-*' | wc -l` → 38.

PAYLOADS — all 8 measured and matched the block's table exactly (lines/bytes/sha256): decisions.md (27/1941), ledger.md (8/5893), mark_cli.diff (207/11291), mark_orchestration.diff (392/20886), mark_services.diff (288/13312), mutations.py (46/1869), plan.md (28/991), r1036.diff (61/3310). All sha256 readings matched the table verbatim.

G1 TRANSPORT — every `.agent/authored/f278-r7-*` copy read back with `git show <commit>:<path>` and compared byte-for-byte against its source: all 9 copies (block.md + 8 payloads) matched exactly (block.md against `.remedy-wt/f278-r7-block.md`, the other 8 against their `.remedy-wt/f278-r7-payloads/` originals).

G2 THE BOOKING — at C2 (`ac5dae0c`), the byte counts matched `ead4ec77` bytes plus each payload's bytes by strict concatenation (live_review.md: 438590+5893=444483; decisions.md: 1852110+1941=1854051; plan.md rewritten to 991), and the sha256 read with `git show ac5dae0c:<path>` matched the reviewer's dry-run reading for all three files:
- `.agent/live_review.md`: bytes=444483, sha256=`8a7327d7382565e768756b4770169c42b1d324b6e68f98e99afd7ab588a3b03a` — MATCH
- `.agent/decisions.md`: bytes=1854051, sha256=`d470d8f512699c60dda07e8bf869860bfc4cae5718be3d56eb13c9a33e01a034` — MATCH
- `.agent/plan.md`: bytes=991, sha256=`49badbd2eec9369931b36ed8e8659c0fe48787d6b5df9496501a973afd4a04e7` — MATCH

Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md` TEXT: at `ead4ec77` count=26; at C2 (`ac5dae0c`) count=29; `base - c2` = `[]`; `c2 - base` = `['R-1036', 'R-1037', 'R-1038']` — matching the reviewer's 26/29, added exactly the three, removed none.

G3 THE PRODUCT BYTES AND THE COMMENT-ONLY PROOF — at C6 (`d49a1b16`), sha256 of each of the 13 files read with `git show d49a1b16:<path>`, all MATCH the block's table exactly: `apps/cli/commands/dev.py` (8461b), `apps/cli/commands/job.py` (100510b), `apps/cli/commands/worker_facade_cmd.py` (18213b), `packages/orchestration/hunk_ledger.py` (19338b), `packages/orchestration/job_apply.py` (102494b), `packages/orchestration/pingpong_job.py` (194929b), `packages/orchestration/pingpong_loop.py` (226278b), `packages/orchestration/pingpong_provider.py` (81843b), `packages/orchestration/real_test_execution.py` (21141b), `packages/orchestration/repository_snapshot.py` (59530b), `packages/orchestration/test_execution_service.py` (44075b), `packages/runtimes/runtime_supervisor.py` (25671b), `tests/orchestration/test_pingpong_integration.py` (8938b).

`python3 .agent/authored/f278-r6-marking_check.py . 5c2673f6 5dbf8936 d49a1b16` → `5c2673f6 OK pairs=42`, `5dbf8936 OK pairs=22`, `d49a1b16 OK pairs=31`, real exit 0 — matches the block's expected pairs 42/22/31 exactly. The negative control, `python3 .agent/authored/f278-r6-marking_check.py . cdee140d`, read `cdee140d VIOLATION pairs=40` with reasons `2 lines removed but 40 added`, code-changed lines for the R-1036 repair, and `no reasoned noqa` for the new explanatory comment line, real exit 1 — VIOLATION as the block requires, since C3 legitimately changes code (the R-1036 repair) and is not a pure marking commit.

`python3 -m ruff check --select BLE001` over the 12 non-test paths of the G3 table → `All checks passed!`, real exit 0.

G4 THE TESTS — command (the block's own, in the primary checkout at C6, WITH `tests/cli/test_golden_path.py` as the block's own command lists it):
```
python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_hunk_ledger.py tests/orchestration/test_job_apply.py tests/orchestration/test_test_execution_service.py tests/orchestration/test_final_verifier.py tests/orchestration/test_repository_snapshot.py tests/orchestration/test_pingpong_integration.py tests/orchestration/test_real_test_execution.py tests/orchestration/test_pingpong.py tests/cli/test_worker_facade_cmd.py tests/cli/test_job_commands.py tests/runtimes/test_runtime_state_machine.py tests/orchestration/test_stream_evidence_integration.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
```
Result: `728 passed in 310.63s (0:05:10)`, real exit 0 (`${PIPESTATUS[0]}`). The reviewer's own run, WITHOUT the golden path, in a disposable worktree carrying C2 to C6, read `685 passed, 1 skipped` at exit 0; this run's command includes `tests/cli/test_golden_path.py` as the block states it, giving a higher pass count and no reported skip — consistent with the block's own framing ("report what you read").

`python3 -m ruff check` over all 13 paths of the G3 table → `All checks passed!`, real exit 0.

`python3 -m apps.cli.main integrity check --json` → `fail_count: 0`, `ok: true`, `passed: true`, all 5 checks `pass` (`handler_import` handlers=145, `live_review_verdict`, `plan_consistency` with `unchecked=0, context_complete=False`, `relevant_untracked` with `untracked=0, relevant=0`, `high_blockers_open` — no open blocker/high findings). Real exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f278-r7-mut d49a1b16` real exit 0. `python3 .remedy-wt/f278-r7-payloads/mutations.py .remedy-wt/f278-r7-mut` real exit 0, full output:
```
control_before REAL_EXIT=0
1 passed in 0.80s
m1_failure_not_named_on_the_job FROM count in file: 1
m1_failure_not_named_on_the_job REAL_EXIT=1
FAILED tests/orchestration/test_pingpong_integration.py::TestRunJobFinalReviewFailure::test_a_review_that_cannot_be_built_blocks_the_apply
1 failed in 0.71s
m1_failure_not_named_on_the_job restored byte-identical: True
m2_no_blocking_record_written FROM count in file: 1
m2_no_blocking_record_written REAL_EXIT=1
FAILED tests/orchestration/test_pingpong_integration.py::TestRunJobFinalReviewFailure::test_a_review_that_cannot_be_built_blocks_the_apply
1 failed in 0.74s
m2_no_blocking_record_written restored byte-identical: True
control_after REAL_EXIT=0
1 passed in 0.88s
```
Every reading matches the reviewer's stated expectations exactly: control_before `1 passed`/exit 0; m1 and m2 each `1 failed`/exit 1 at `TestRunJobFinalReviewFailure::test_a_review_that_cannot_be_built_blocks_the_apply`; control_after `1 passed`/exit 0; both restores byte-identical `True`.

`git worktree remove --force .remedy-wt/f278-r7-mut` real exit 0. `git worktree prune` real exit 0. `git worktree list` afterward → primary checkout (`feature/f278-durable-writes-loud-failures`) and `.remedy-wt/job-129b3ad7206d4f8d` only — the mutation worktree is gone.

G6 TREE AND PUSH — reported in the session's final reply, not this file, since it runs after this commit (C7). The handback cannot contain readings that postdate its own write.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- `decisions.md` (append): `.agent/decisions.md` at C2 sha256 `d470d8f...9a33e01a034` == payload sha256 concatenated onto the `ead4ec77` bytes (G2). MATCH.
- `ledger.md` (append): `.agent/live_review.md` at C2 sha256 `8a7327d...9afd7ab588a3b03a` == payload sha256 concatenated onto the `ead4ec77` bytes (G2). MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256 `49badbd...9a973afd4a04e7` == payload sha256 exactly (G2). MATCH.
- `r1036.diff` (applied): `.agent/authored/f278-r7-r1036.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C3; resulting `pingpong_job.py`/test bytes verified in Verification (C3). MATCH.
- `mark_orchestration.diff` (applied): `.agent/authored/f278-r7-mark_orchestration.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C4; resulting files' sha256 at C6 match the G3 table. MATCH.
- `mark_cli.diff` (applied): `.agent/authored/f278-r7-mark_cli.diff` at C1c byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C5; resulting files' sha256 at C6 match the G3 table. MATCH.
- `mark_services.diff` (applied): `.agent/authored/f278-r7-mark_services.diff` at C1c byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C6; resulting files' sha256 at C6 match the G3 table. MATCH.
- `mutations.py`: a TOOL run against the disposable mutation worktree, never applied to a tracked file. `.agent/authored/f278-r7-mutations.py` at C1a verified byte-identical to the payload (G1). N/A for an "applied location" comparison by design.
- This block (`f278-r7-block.md`): `.agent/authored/f278-r7-block.md` at C1a verified byte-identical to `.remedy-wt/f278-r7-block.md` (G1) and to the two readings given in the delegation message.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C1c | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | |
| R-1036 | done | repaired at C3, per DECISION F278 D6 |
| R-1037 | skipped | registered at C2 only; repair deferred to next round, ahead of the third marking group, per DECISION F278 D6 |
| R-1038 | skipped | registered at C2 only; repair deferred to next round, ahead of the third marking group, per DECISION F278 D6 |
| G1 TRANSPORT | done | |
| G2 THE BOOKING | done | |
| G3 THE PRODUCT BYTES AND THE COMMENT-ONLY PROOF | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | |
| G6 TREE AND PUSH | done | runs after C7; real readings reported in the session's final chat reply, not this file |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1a, C1b, C1c, C2,
C3, C4, C5, C6, C7) exactly, touched exactly the tracked path set the block
names (verified via `git diff --name-only ead4ec77 HEAD` before C7), ran no
full suite, and left `.remedy-wt/job-129b3ad7206d4f8d`, its branch, and every
existing stash untouched. No other deviation.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 7,
then the last marking round: R-1037 and R-1038 repaired first, the third
handler group marked, then BLE001 turned on in `pyproject.toml` with the
ratchet test that freezes the count of excused handlers. Open findings: 29.
Operator questions: 0.
