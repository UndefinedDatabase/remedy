# Handback — F278 Durable writes & loud failures · Round 3 · Book round 2, migrate the boolean helpers

## Session

SESSION 1 of feature F278 · round 3 · rounds so far 3

This round booked round 2's PASS and DECISION F278 D2 into the durable
ledger files, then migrated the three remaining boolean-returning
`_atomic_write` helpers onto `durable_write`: `real_test_execution._atomic_write`
(two `create_snapshot_proof` call sites, now let the write error propagate),
`self_dogfood_execution._atomic_write` (`save_attempt` keeps its boolean via
an explicit try/except, `_store_request` now propagates), and
`token_economy._atomic_write` (`save_token_budget_profile` keeps its
boolean). Each deletion removed its entry from the guard's
`STILL_TO_MIGRATE` set in the same commit that moved its callers, and each
module's own test file gained a test class covering the durable-write path
and the loud-failure path. All five gates (G1–G5) ran clean and matched the
reviewer's dry-run readings exactly; the revert probes confirmed each
deletion turns the guard red on its own. Context self-assessment: a
comfortable majority of the working budget remains at handback.

## Range

Review of `b449d7b2`..`HEAD`.

## Commits

### 6258aed1 F278 R3 C1a: copy round 3 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r3-block.md | +201/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r3-decisions.md | +32/-0 | Bookkeeping copy of the decisions.md append payload |
| .agent/authored/f278-r3-ledger.md | +2/-0 | Bookkeeping copy of the live_review.md append payload |
| .agent/authored/f278-r3-plan.md | +31/-0 | Bookkeeping copy of the plan.md rewrite payload |

Measured insertions: 266 (block 201 + 65 payload lines), under the 500 cap; matches the block's expected value exactly.

### 1bf35d5e F278 R3 C1b: copy round 3 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r3-revert_probes.py | +47/-0 | Bookkeeping copy of the G5 revert-probe tool |
| .agent/authored/f278-r3-rte.diff | +114/-0 | Bookkeeping copy of the real_test_execution migration diff |
| .agent/authored/f278-r3-sd.diff | +121/-0 | Bookkeeping copy of the self_dogfood_execution migration diff |
| .agent/authored/f278-r3-te.diff | +112/-0 | Bookkeeping copy of the token_economy migration diff |

Measured insertions: 394 (47 + 114 + 121 + 112), matches the block's expected value exactly.

### c9aef442 F278 R3 C2: book round 2's PASS and DECISION F278 D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +32/-0 | `decisions.md` appended by byte concatenation |
| .agent/live_review.md | +2/-0 | `ledger.md` appended by byte concatenation |
| .agent/plan.md | +11/-13 | Rewritten to plan.md payload for round 3 |

Measured insertions: 45 (32 + 2 + 11), matches the block's expected value exactly. Deletions: 13, all from the plan.md rewrite.

### 43747468 F278 R3 C3: move the snapshot proof record onto durable_write
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/real_test_execution.py | +7/-27 | `_atomic_write` deleted; both `create_snapshot_proof` sites gain explicit `mkdir(mode=0o700)` and call `durable_write`, letting a failed write raise |
| tests/orchestration/test_durable_write_guard.py | +0/-1 | `real_test_execution.py`'s `STILL_TO_MIGRATE` entry removed |
| tests/orchestration/test_real_test_execution.py | +28/-0 | New `TestSnapshotRecordIsDurableAndLoud` class: durable-write routing + raise-on-failure, both parametrized over `repo` |

`git apply --check` real exit 0, `git apply` real exit 0. Measured insertions: 35 (7+0+28), matches the block's expected value exactly.

### ce7eb57c F278 R3 C4: move the self-use attempt and request records onto durable_write
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/self_dogfood_execution.py | +10/-23 | `_atomic_write` and `import os` deleted; `save_attempt` keeps its boolean via try/except around `durable_write`, `_store_request` now lets the write raise |
| tests/orchestration/test_durable_write_guard.py | +0/-1 | `self_dogfood_execution.py`'s `STILL_TO_MIGRATE` entry removed |
| tests/orchestration/test_self_dogfood_execution.py | +34/-0 | New `TestAttemptRecordsAreDurable` class: durable-write routing for both records, boolean-false on attempt-write failure, raise on request-write failure |

`git apply --check` real exit 0, `git apply` real exit 0. Measured insertions: 44 (10+0+34), matches the block's expected value exactly.

### 1e3dcb40 F278 R3 C5: move the token budget profile onto durable_write
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/token_economy.py | +8/-26 | `_atomic_write` and `import os` deleted; `save_token_budget_profile` keeps its boolean via try/except around `mkdir(mode=0o700)` + `durable_write` |
| tests/orchestration/test_durable_write_guard.py | +0/-1 | `token_economy.py`'s `STILL_TO_MIGRATE` entry removed |
| tests/orchestration/test_token_economy.py | +26/-0 | New `TestProfileWriteIsDurable` class: durable-write routing, boolean-false on failure |

`git apply --check` real exit 0, `git apply` real exit 0. Measured insertions: 34 (8+0+26), matches the block's expected value exactly.

### C6 (this commit) F278 R3 C6: rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f278-r3-probe 1e3dcb40` — real exit 0.
- `python3 .remedy-wt/f278-r3-payloads/revert_probes.py .remedy-wt/f278-r3-probe b449d7b2` — real exit 0 (see Verification, G5).
- `git worktree remove --force .remedy-wt/f278-r3-probe` — real exit 0.
- `git worktree prune` — real exit 0.
- `git push origin feature/f278-durable-writes-loud-failures` — see Verification, G6, for the real outcome (reported separately since it runs after this commit).
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no checkout of another branch: none run, per the block's constraints.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, absent (proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `feature/f278-durable-writes-loud-failures`. `git log --oneline -1` → `b449d7b2 F278 R2 C6: rewrite handoff for round 2`.
- Block bytes (R-0954): measured lines=201, sha256=`6601943a46b5e91139f1938f4ec71cd954debedc681b6dfdfdd99951da2ab6eb`; matches both given readings exactly.
- `git worktree list` (before) → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` only.
- `git branch --list 'remedy/job-*' | wc -l` → 38.

PAYLOADS — all 7 measured and matched the block's table exactly (lines/bytes/sha256): decisions.md (32/2269), ledger.md (2/3018), plan.md (31/1234), revert_probes.py (47/1897), rte.diff (114/5450), sd.diff (121/5042), te.diff (112/4846). All sha256 readings matched the table verbatim.

G1 TRANSPORT — every `.agent/authored/f278-r3-*` copy read back with `git show <commit>:<path>` and compared byte-for-byte against its source: all 8 copies (block.md + 7 payloads) matched exactly.

G2 THE BOOKING — at C2 (`c9aef442`), each appended/rewritten file's byte count matched `b449d7b2` bytes plus the payload's bytes by strict concatenation (live_review.md: 427438+3018=430456; decisions.md: 1842186+2269=1844455; plan.md rewritten to 1234), and the sha256 read with `git show c9aef442:<path>` matched the reviewer's dry-run reading for all three files:
- `.agent/live_review.md`: bytes=430456, sha256=`9e5fd03a7c7e3ec308268fc3ca25276f8ee30156585c661efb5ae0f7a34bfbee` — MATCH
- `.agent/decisions.md`: bytes=1844455, sha256=`228754110918a12a5e4add02145e566a92dbe7dcfef74e10ec75a90e5345d853` — MATCH
- `.agent/plan.md`: bytes=1234, sha256=`31cab2fd08429194bd8a035b0cce9e8a56121adeb857e7e76cffcca92992d816` — MATCH

Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md` TEXT: at `b449d7b2` count=26; at C2 (`c9aef442`) count=26; `base - c2` = `[]`; `c2 - base` = `[]` — both differences empty, matching the reviewer's 26/26.

G3 THE PRODUCT BYTES — at C5 (`1e3dcb40`), sha256 of each file read with `git show 1e3dcb40:<path>`, all 7 MATCH:
- `packages/orchestration/real_test_execution.py`: bytes=20693, sha256=`71e2937dce02ff262b72987f5959817887ea3649c98af25d26feedb78c4e69a1`
- `packages/orchestration/self_dogfood_execution.py`: bytes=32243, sha256=`26bcba0716070a7d788586c860a1772cceacabcfe218782041aebe6b85ebf22f`
- `packages/orchestration/token_economy.py`: bytes=36221, sha256=`42bc47d864411c12a3f3e7c57ff312b44656850f9d49e25d1688825ebe75bcaa`
- `tests/orchestration/test_durable_write_guard.py`: bytes=3214, sha256=`a7324ec24a9ab0376f4abc3c9f8d6952ae9744ff9b8e02c3b43ab74d5fa9cb8b`
- `tests/orchestration/test_real_test_execution.py`: bytes=11575, sha256=`c6515d5de9e4d6c0c249e0db6b37c9999c3f1df2280ddb08086dbf1cc8bf8b18`
- `tests/orchestration/test_self_dogfood_execution.py`: bytes=12989, sha256=`2802c9cced19f7bc0c59dcd2ff6a54f17975908ee2a90c628d1a93ca40ea6975`
- `tests/orchestration/test_token_economy.py`: bytes=18052, sha256=`fafcc0b7161737b906fd0ab55b0c2130c0f26db919425750491a739344dc5bb8`

G4 THE TESTS — command (the block's own, in the primary checkout at C5, WITH `tests/cli/test_golden_path.py`, unlike the reviewer's own dry-run selection which excluded it):
```
python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_durable_write_guard.py tests/orchestration/test_real_test_execution.py tests/orchestration/test_self_dogfood_execution.py tests/orchestration/test_token_economy.py tests/cli/test_real_test_execution_cli.py tests/cli/test_self_dogfood_execution_cli.py tests/cli/test_self_dogfood_cli.py tests/orchestration/test_self_dogfood.py tests/test_token_policy.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
```
Result: `308 passed in 160.64s`, real exit 0 (`${PIPESTATUS[0]}`). The reviewer's own run, in a disposable worktree WITHOUT the golden path file, read `265 passed, 1 skipped` at exit 0; the primary checkout run here includes `test_golden_path.py`, which the reviewer's selection did not, accounting for the higher pass count and the absent skip.

`python3 -m ruff check` over every Python path of the G3 table (7 files) → `All checks passed!`, real exit 0.

`python3 -m apps.cli.main integrity check --json` → `fail_count: 0`, `ok: true`, `passed: true`, all 5 checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked` with `untracked=0, relevant=0`, `high_blockers_open`). Real exit 0.

G5 THE REVERT PROBES — `git worktree add --detach .remedy-wt/f278-r3-probe 1e3dcb40` real exit 0. `python3 .remedy-wt/f278-r3-payloads/revert_probes.py .remedy-wt/f278-r3-probe b449d7b2` real exit 0, full output:
```
control_before REAL_EXIT=0
92 passed in 2.55s
p1_real_test_execution REAL_EXIT=1
FAILED tests/orchestration/test_durable_write_guard.py::test_no_private_atomic_write_helper_outside_packages_common
FAILED tests/orchestration/test_real_test_execution.py::TestSnapshotRecordIsDurableAndLoud::test_the_record_is_written_through_durable_write[True]
FAILED tests/orchestration/test_real_test_execution.py::TestSnapshotRecordIsDurableAndLoud::test_the_record_is_written_through_durable_write[False]
FAILED tests/orchestration/test_real_test_execution.py::TestSnapshotRecordIsDurableAndLoud::test_a_failed_write_raises[True]
FAILED tests/orchestration/test_real_test_execution.py::TestSnapshotRecordIsDurableAndLoud::test_a_failed_write_raises[False]
5 failed, 87 passed in 2.40s
p1_real_test_execution restored clean: True
p2_self_dogfood_execution REAL_EXIT=1
FAILED tests/orchestration/test_durable_write_guard.py::test_no_private_atomic_write_helper_outside_packages_common
FAILED tests/orchestration/test_self_dogfood_execution.py::TestAttemptRecordsAreDurable::test_both_records_are_written_through_durable_write
FAILED tests/orchestration/test_self_dogfood_execution.py::TestAttemptRecordsAreDurable::test_a_failed_attempt_write_answers_false
FAILED tests/orchestration/test_self_dogfood_execution.py::TestAttemptRecordsAreDurable::test_a_failed_request_write_raises
4 failed, 88 passed in 2.34s
p2_self_dogfood_execution restored clean: True
p3_token_economy REAL_EXIT=1
FAILED tests/orchestration/test_durable_write_guard.py::test_no_private_atomic_write_helper_outside_packages_common
FAILED tests/orchestration/test_token_economy.py::TestProfileWriteIsDurable::test_the_profile_is_written_through_durable_write
FAILED tests/orchestration/test_token_economy.py::TestProfileWriteIsDurable::test_a_failed_write_answers_false
3 failed, 89 passed in 2.46s
p3_token_economy restored clean: True
control_after REAL_EXIT=0
92 passed in 2.36s
```
Every reading matches the reviewer's stated expectations exactly: control_before 92 passed/0; p1 5 failed/87 passed/1 at the guard test plus the four `TestSnapshotRecordIsDurableAndLoud` cases; p2 4 failed/88 passed/1 at the guard test plus the three `TestAttemptRecordsAreDurable` tests; p3 3 failed/89 passed/1 at the guard test plus the two `TestProfileWriteIsDurable` tests; control_after 92 passed/0; every `restored clean` line `True`.

`git worktree remove --force .remedy-wt/f278-r3-probe` real exit 0. `git worktree prune` real exit 0. `git worktree list` afterward → primary checkout (`feature/f278-durable-writes-loud-failures`) and `.remedy-wt/job-129b3ad7206d4f8d` only — the probe worktree is gone.

G6 TREE AND PUSH — reported in the session's final reply, not this file, since it runs after this commit (C6). The handback cannot contain readings that postdate its own write.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- `decisions.md` (append): `.agent/decisions.md` at C2 sha256 `228754...345d853` == payload sha256 concatenated onto the `b449d7b2` bytes (G2). MATCH.
- `ledger.md` (append): `.agent/live_review.md` at C2 sha256 `9e5fd0...34bfbee` == payload sha256 concatenated onto the `b449d7b2` bytes (G2). MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256 `31cab2...92992d816` == payload sha256 exactly (G2). MATCH.
- `rte.diff` (applied): `.agent/authored/f278-r3-rte.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C3; resulting files' sha256 at C5 match the G3 table. MATCH.
- `sd.diff` (applied): `.agent/authored/f278-r3-sd.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C4; resulting files' sha256 at C5 match the G3 table. MATCH.
- `te.diff` (applied): `.agent/authored/f278-r3-te.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C5; resulting files' sha256 at C5 match the G3 table. MATCH.
- `revert_probes.py`: a TOOL run against the disposable probe worktree, never applied to a tracked file. `.agent/authored/f278-r3-revert_probes.py` at C1b verified byte-identical to the payload (G1). N/A for an "applied location" comparison by design.
- This block (`f278-r3-block.md`): `.agent/authored/f278-r3-block.md` at C1a verified byte-identical to `.remedy-wt/f278-r3-block.md` (G1) and to the two readings given in the delegation message.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| G1 TRANSPORT | done | |
| G2 THE BOOKING | done | |
| G3 THE PRODUCT BYTES | done | |
| G4 THE TESTS | done | |
| G5 THE REVERT PROBES | done | |
| G6 TREE AND PUSH | done | runs after C6; real readings reported in the session's final chat reply, not this file |

## Deviations & assumptions

None. The round followed the block's ordered commit sequence (C1a, C1b, C2,
C3, C4, C5, C6) exactly, touched exactly the tracked path set the block
names, ran no full suite, and left `.remedy-wt/job-129b3ad7206d4f8d`, its
branch, and every existing stash untouched.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 3,
then T002's last group — `dev_server`'s helpers with `runtime_supervisor`
and `runtime_cmd`, and the inline writers in `repository_snapshot` and
`project_registry`. Open findings: 26. Operator questions: 0.
