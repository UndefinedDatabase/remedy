# Handback — F278 Durable writes & loud failures · Round 2 · Book round 1, land T002's guard as a ratchet, migrate two helper groups

## Session

SESSION 1 of feature F278 · round 2 · rounds so far 2

This round booked round 1's PASS and DECISION F278 D1 into the durable
ledger files, landed `tests/orchestration/test_durable_write_guard.py` as
a ratchet over the surviving private atomic-write helpers, and migrated
the first two helper groups onto `durable_write`: `pingpong_job`'s
`atomic_write_text` (with its three importers — `checkpoints.py`,
`mission_compiler.py`, `mission_state.py`) and `proposed_tasks._atomic_write`
— each deleted in the commit that moved its callers, with its guard-set
entry removed in the same diff. All five gates (G1–G5) ran clean and
matched the reviewer's dry-run readings exactly; the revert probes
confirmed each deletion turns the guard red on its own. Context
self-assessment: a comfortable majority of the working budget remains at
handback.

## Range

Review of `41254292`..`HEAD`.

## Commits

### e4e44827 F278 R2 C1a: copy round 2 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r2-block.md | +214/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r2-decisions.md | +44/-0 | Bookkeeping copy of the decisions.md append payload |
| .agent/authored/f278-r2-ledger.md | +2/-0 | Bookkeeping copy of the live_review.md append payload |
| .agent/authored/f278-r2-plan.md | +33/-0 | Bookkeeping copy of the plan.md rewrite payload |
| .agent/authored/f278-r2-prose_slips.md | +1/-0 | Bookkeeping copy of the prose_slips.md append payload |

Measured insertions: 294 (block 214 + 80 payload lines), under the 500 cap; matches the block's expected value exactly.

### 073944eb F278 R2 C1b: copy round 2 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r2-pingpong.diff | +186/-0 | Bookkeeping copy of the pingpong-group migration diff |
| .agent/authored/f278-r2-proposed.diff | +79/-0 | Bookkeeping copy of the proposed-tasks migration diff |
| .agent/authored/f278-r2-revert_probes.py | +51/-0 | Bookkeeping copy of the G5 revert-probe tool |
| .agent/authored/f278-r2-test_durable_write_guard.py | +76/-0 | Bookkeeping copy of the new guard test file |

Measured insertions: 392 (186 + 79 + 51 + 76), matches the block's expected value exactly.

### 88b4528e F278 R2 C2: book round 1's PASS and DECISION F278 D1
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +44/-0 | `decisions.md` appended by byte concatenation |
| .agent/live_review.md | +2/-0 | `ledger.md` appended by byte concatenation |
| .agent/plan.md | +11/-13 | Rewritten to plan.md payload for round 2 |
| .agent/prose_slips.md | +1/-0 | `prose_slips.md` appended by byte concatenation (no separator: file already ended in a newline) |

Measured insertions: 58 (44 + 2 + 11 + 1), matches the block's expected value exactly. Deletions: 13, all from the plan.md rewrite.

### e36fde5a F278 R2 C3: add the private atomic-write guard as a ratchet
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_durable_write_guard.py | +76/-0 | New file, copied whole from the payload and `git add`ed |

Measured insertions: 76, matches the block's expected value exactly.

### ef10bcba F278 R2 C4: move the job, checkpoint and mission records onto durable_write
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/checkpoints.py | +2/-2 | Import + call site moved from the deleted helper to `durable_write` |
| packages/orchestration/mission_compiler.py | +2/-2 | Import + call site moved to `durable_write` |
| packages/orchestration/mission_state.py | +3/-3 | Import + both call sites moved to `durable_write` |
| packages/orchestration/pingpong_job.py | +3/-26 | `atomic_write_text` deleted; `_persist_job` gains an explicit `mkdir` and calls `durable_write` |
| tests/orchestration/test_checkpoints.py | +3/-3 | Patches retargeted from `checkpoints._atomic_write` (no longer exists) to `checkpoints.durable_write` |
| tests/orchestration/test_durable_write_guard.py | +0/-1 | `pingpong_job.py`'s `STILL_TO_MIGRATE` entry removed |

`git apply --check` real exit 0, `git apply` real exit 0. Measured insertions: 13 (2+2+3+3+3+0), matches the block's expected value exactly.

### a427034f F278 R2 C5: move proposed tasks onto durable_write
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/proposed_tasks.py | +2/-25 | `_atomic_write` deleted; `save_proposed_tasks` calls `durable_write` |
| tests/orchestration/test_durable_write_guard.py | +0/-1 | `proposed_tasks.py`'s `STILL_TO_MIGRATE` entry removed |
| tests/orchestration/test_task_execution.py | +1/-1 | Source guard now requires the string `durable_write` instead of `_atomic_write` |

`git apply --check` real exit 0, `git apply` real exit 0. Measured insertions: 3 (2+0+1), matches the block's expected value exactly.

### C6 (this commit) F278 R2 C6: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f278-r2-probe a427034f` — real exit 0.
- `python3 .remedy-wt/f278-r2-payloads/revert_probes.py .remedy-wt/f278-r2-probe 41254292` — real exit 0 (see Verification, G5).
- `git worktree remove --force .remedy-wt/f278-r2-probe` — real exit 0.
- `git worktree prune` — real exit 0.
- `git push origin feature/f278-durable-writes-loud-failures` — see Verification, G6, for the real outcome (reported separately since it runs after this commit).
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no checkout of another branch: none run, per the block's constraints.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, real exit 2 (absent, proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `feature/f278-durable-writes-loud-failures`. `git log --oneline -1` → `41254292 F278 R1 C4: rewrite handoff for round 1`.
- Block bytes (R-0954): measured lines=214, sha256=`a18e02f525da5578345cfeb28a5e5ec2820100dc0aaa90162ac1a97df7edf20e`; matches both given readings exactly.
- `git worktree list` (before) → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` only.
- `git branch --list 'remedy/job-*' | wc -l` → 38.

PAYLOADS — all 8 measured and matched the block's table exactly (lines/bytes/sha256): decisions.md (44/3424), ledger.md (2/3117), pingpong.diff (186/8741), plan.md (33/1380), proposed.diff (79/3157), prose_slips.md (1/299), revert_probes.py (51/1981), test_durable_write_guard.py (76/3563). All sha256 readings matched the table verbatim.

G1 TRANSPORT — every `.agent/authored/f278-r2-*` copy read back with `git show <commit>:<path>` and compared byte-for-byte against its source: all 9 copies (block.md + 8 payloads) matched exactly.

G2 THE BOOKING — at C2 (`88b4528e`), each appended/rewritten file's byte count matched `41254292` bytes plus the payload's bytes by strict concatenation, and the sha256 read with `git show 88b4528e:<path>` matched the reviewer's dry-run reading for all four files:
- `.agent/live_review.md`: bytes=427438, sha256=`d00deba9917bd06a55316ca02b116353a2e02dcc197e40cbde2db8909c3f04ed` — MATCH
- `.agent/decisions.md`: bytes=1842186, sha256=`c9a02a6f2d5f9b716877d564529a4d7bda2f88a3f8121eaadbe6204e61319e15` — MATCH
- `.agent/prose_slips.md`: bytes=363591, sha256=`1bc24fe2fc5cf7e0273d78f56d136c55d190169985e2bcdf1993a2abc0c5231f` — MATCH
- `.agent/plan.md`: bytes=1380, sha256=`5dcb97ba8679da99b017154cc4a3ed0a499e95dceb89058b00c5356296c88112` — MATCH

Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md` TEXT: at `41254292` count=26; at C2 (`88b4528e`) count=26; `base - c2` = `[]`; `c2 - base` = `[]` — both differences empty, matching the reviewer's 26/26.

G3 THE PRODUCT BYTES — at C5 (`a427034f`), sha256 of each file read with `git show a427034f:<path>`, all 8 MATCH:
- `tests/orchestration/test_durable_write_guard.py`: bytes=3427, sha256=`72cab2e7073a81380d1626f48c50eb6397a376e32f85d658724e420f19c9ba57`
- `packages/orchestration/pingpong_job.py`: bytes=193002, sha256=`b67a13c58a8069ef80030dd567a151fe0a3c67e2727c2d7f0a9cf8d934e8f194`
- `packages/orchestration/checkpoints.py`: bytes=22340, sha256=`49b896b169d21a5021713f51d20a8fbb69e82b49c57d785242e0548a715a57a3`
- `packages/orchestration/mission_compiler.py`: bytes=33617, sha256=`b817772e0d825074aed3c7fc446026f9607d6af4383576fd651c695be1f1548c`
- `packages/orchestration/mission_state.py`: bytes=47639, sha256=`30e64304b59cea9bea53fb4b6c52aae0d43ec4fd1817c52c2213884a7bdb7f25`
- `packages/orchestration/proposed_tasks.py`: bytes=19964, sha256=`d49887a87083215ab8ecaea98e2f41a3380179e0e8382b726174cca558c27042`
- `tests/orchestration/test_checkpoints.py`: bytes=16950, sha256=`5548d4cabf427645d81ef086ea0449e2a68a0744ade1aa96f43d18da7cfbd995`
- `tests/orchestration/test_task_execution.py`: bytes=708, sha256=`d29e60164a46d6cd57e09b9dfafb58c72ab2c89b0d386b1e68d101fd92635452`

G4 THE TESTS — command (the block's own, in the primary checkout at C5, WITH `tests/cli/test_golden_path.py`, unlike the reviewer's own dry-run selection which excluded it):
```
python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_durable_write_guard.py tests/orchestration/test_checkpoints.py tests/orchestration/test_task_execution.py tests/orchestration/test_mission_compiler.py tests/orchestration/test_mission_state.py tests/orchestration/test_proposed_tasks.py tests/orchestration/test_pingpong.py tests/orchestration/test_pingpong_integration.py tests/orchestration/test_resume_kill.py tests/orchestration/test_mission_e2e.py tests/storage/test_persistence.py tests/cli/test_job_commands.py tests/test_imports.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_secure_fs_durable_write.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
```
Result: `602 passed in 164.27s`, real exit 0 (`${PIPESTATUS[0]}`). The reviewer's own run, in a disposable worktree WITHOUT the golden path file, read `559 passed, 1 skipped` at exit 0; the primary checkout run here includes `test_golden_path.py`, which the reviewer's selection did not, accounting for the higher pass count and the absent skip.

`python3 -m ruff check` over every Python path of the G3 table (8 files) → `All checks passed!`, real exit 0.

`python3 -m apps.cli.main integrity check --json` → `fail_count: 0`, `ok: true`, `passed: true`, all 5 checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked` with `untracked=0, relevant=0`, `high_blockers_open`). Real exit 0.

G5 THE REVERT PROBES — `git worktree add --detach .remedy-wt/f278-r2-probe a427034f` real exit 0. `python3 .remedy-wt/f278-r2-payloads/revert_probes.py .remedy-wt/f278-r2-probe 41254292` real exit 0, full output:
```
control_before REAL_EXIT=0
42 passed in 2.30s
p1_pingpong_helper_only REAL_EXIT=1
FAILED tests/orchestration/test_durable_write_guard.py::test_no_private_atomic_write_helper_outside_packages_common
1 failed, 41 passed in 2.18s
p1_pingpong_helper_only restored clean: True
p2_pingpong_group REAL_EXIT=1
FAILED tests/orchestration/test_durable_write_guard.py::test_no_private_atomic_write_helper_outside_packages_common
FAILED tests/orchestration/test_checkpoints.py::TestWriteFailureIsContained::test_record_cycle_checkpoint_returns_the_reason_instead_of_raising
FAILED tests/orchestration/test_checkpoints.py::TestWriteFailureIsContained::test_the_failure_is_logged_loudly
FAILED tests/orchestration/test_checkpoints.py::TestCycleBoundaryWiring::test_a_failed_checkpoint_write_does_not_break_the_cycle
4 failed, 38 passed in 2.17s
p2_pingpong_group restored clean: True
p3_proposed_tasks REAL_EXIT=1
FAILED tests/orchestration/test_durable_write_guard.py::test_no_private_atomic_write_helper_outside_packages_common
FAILED tests/orchestration/test_task_execution.py::TestModularArchitectureGuards::test_storage_access_through_helpers
2 failed, 40 passed in 2.17s
p3_proposed_tasks restored clean: True
control_after REAL_EXIT=0
42 passed in 2.19s
```
Every reading matches the reviewer's stated expectations exactly: control_before 42 passed/0; p1 1 failed/41 passed/1 at the guard test; p2 4 failed/38 passed/1 at the guard test plus three in `test_checkpoints.py`; p3 2 failed/40 passed/1 at the guard test plus `TestModularArchitectureGuards::test_storage_access_through_helpers`; control_after 42 passed/0; every `restored clean` line `True`.

`git worktree remove --force .remedy-wt/f278-r2-probe` real exit 0. `git worktree prune` real exit 0. `git worktree list` afterward → primary checkout (`feature/f278-durable-writes-loud-failures`) and `.remedy-wt/job-129b3ad7206d4f8d` only — the probe worktree is gone.

G6 TREE AND PUSH — reported in the session's final reply, not this file, since it runs after this commit (C6). The handback cannot contain readings that postdate its own write.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- `decisions.md` (append): `.agent/decisions.md` at C2 sha256 `c9a02a6f...61319e15` == payload sha256 concatenated onto the `41254292` bytes (G2). MATCH.
- `ledger.md` (append): `.agent/live_review.md` at C2 sha256 `d00deba9...909c3f04ed` == payload sha256 concatenated onto the `41254292` bytes (G2). MATCH.
- `prose_slips.md` (append): `.agent/prose_slips.md` at C2 sha256 `1bc24fe2...93a2abc0c5231f` == payload sha256 concatenated onto the `41254292` bytes, no separator (G2). MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256 `5dcb97ba...296c88112` == payload sha256 exactly (G2). MATCH.
- `test_durable_write_guard.py` (copied whole): `.agent/authored/f278-r2-test_durable_write_guard.py` at C1b byte-identical to the payload (G1); the tracked test file at C3 sha256 matched the copy before C4/C5 each removed one `STILL_TO_MIGRATE` line (both later diffs applied cleanly per their own `git apply --check`). MATCH at C3; further changes at C4/C5 are the block's own product diffs, not a fidelity break.
- `pingpong.diff` (applied): `.agent/authored/f278-r2-pingpong.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C4; resulting files' sha256 at C5 match the G3 table. MATCH.
- `proposed.diff` (applied): `.agent/authored/f278-r2-proposed.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C5; resulting files' sha256 at C5 match the G3 table. MATCH.
- `revert_probes.py`: a TOOL run against the disposable probe worktree, never applied to a tracked file. `.agent/authored/f278-r2-revert_probes.py` at C1b verified byte-identical to the payload (G1). N/A for an "applied location" comparison by design.
- This block (`f278-r2-block.md`): `.agent/authored/f278-r2-block.md` at C1a verified byte-identical to `.remedy-wt/f278-r2-block.md` (G1) and to the two readings given in the delegation message.

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

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 2,
then T002's remaining boolean helpers in `real_test_execution`,
`self_dogfood_execution` and `token_economy`. Open findings: 26. Operator
questions: 0.
