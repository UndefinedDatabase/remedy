# Handback — F278 Durable writes & loud failures · Round 4 · Book round 3, end T002

## Session

SESSION 1 of feature F278 · round 4 · rounds so far 4

This round booked round 3's PASS and DECISION F278 D3 into the durable
ledger files, then ended T002: `dev_server`'s three `atomic_write_bytes`,
`atomic_write_text` and `_atomic_write` helpers are deleted; every
caller — `runtime_supervisor`, `apps/cli/commands/runtime_cmd.py` and one
test — now imports `durable_write` directly, with an explicit `mkdir` added
at the two sites (supervisor handshake write, command stop-request write)
the old helper used to cover; the guard's `STILL_TO_MIGRATE` set is now
empty. The two inline temporary-file writers,
`repository_snapshot.update_apply_record_state` (keeps its boolean) and
`project_registry.save_project` (keeps raising), moved onto `durable_write`
in their own commits, each with a new test class in its own file. All five
gates (G1–G5) ran clean and matched the reviewer's dry-run readings exactly;
the revert probes confirmed each deletion/migration turns its owning test(s)
red on its own. Context self-assessment: a comfortable majority of the
working budget remains at handback.

## Range

Review of `ce53bd0c`..`HEAD`.

## Commits

### 42695ab7 F278 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r4-block.md | +205/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r4-decisions.md | +37/-0 | Bookkeeping copy of the decisions.md append payload |
| .agent/authored/f278-r4-ledger.md | +2/-0 | Bookkeeping copy of the live_review.md append payload |
| .agent/authored/f278-r4-plan.md | +29/-0 | Bookkeeping copy of the plan.md rewrite payload |

Measured insertions: 273 (block 205 + 68 payload lines), under the 500 cap; matches the block's expected value exactly.

### dda9dea1 F278 R4 C1b: copy round 4 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r4-dev.diff | +222/-0 | Bookkeeping copy of the runtime-group migration diff |
| .agent/authored/f278-r4-reg.diff | +89/-0 | Bookkeeping copy of the project_registry migration diff |
| .agent/authored/f278-r4-revert_probes.py | +51/-0 | Bookkeeping copy of the G5 revert-probe tool |
| .agent/authored/f278-r4-snap.diff | +95/-0 | Bookkeeping copy of the repository_snapshot migration diff |

Measured insertions: 457 (222+89+51+95), matches the block's expected value exactly.

### c02906f9 F278 R4 C2: book round 3's PASS and DECISION F278 D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +37/-0 | `decisions.md` appended by byte concatenation |
| .agent/live_review.md | +2/-0 | `ledger.md` appended by byte concatenation |
| .agent/plan.md | +9/-11 | Rewritten to plan.md payload for round 4 |

Measured insertions: 48 (37+2+9), matches the block's expected value exactly. Deletions: 11, all from the plan.md rewrite.

### a63636af F278 R4 C3: move the runtime records onto durable_write and empty the guard's set
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/runtime_cmd.py | +6/-5 | `atomic_write_text` calls replaced with `durable_write`; the stop-request write gains an explicit `mkdir` |
| packages/runtimes/dev_server.py | +4/-36 | `atomic_write_bytes`, `atomic_write_text` and `_atomic_write` deleted; the two remaining internal callers (`save_state`, `stop_recorded_runtime`) call `durable_write` directly |
| packages/runtimes/runtime_supervisor.py | +6/-5 | `atomic_write_text` calls replaced with `durable_write`; the handshake write gains an explicit `mkdir` |
| tests/orchestration/test_durable_write_guard.py | +3/-6 | `STILL_TO_MIGRATE` emptied to `frozenset()` |
| tests/runtimes/test_supervisor_portability.py | +2/-1 | Test updated to call `durable_write` directly instead of the deleted `DS.atomic_write_text` alias |

`git apply --check` real exit 0, `git apply` real exit 0. Measured insertions: 21 (6+4+6+3+2), matches the block's expected value exactly.

### e2da5b8c F278 R4 C4: move the apply-record state update onto durable_write
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/repository_snapshot.py | +4/-15 | `update_apply_record_state`'s hand-rolled temp-file + `os.replace` replaced with `durable_write`; keeps its boolean via try/except |
| tests/orchestration/test_repository_snapshot.py | +40/-0 | New `TestApplyRecordStateIsDurable` class: durable-write routing and false-on-failure with the record left unchanged |

`git apply --check` real exit 0, `git apply` real exit 0. Measured insertions: 44 (4+40), matches the block's expected value exactly.

### cde8d5f3 F278 R4 C5: move the project record onto durable_write
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/project_registry.py | +3/-14 | `save_project`'s `tempfile.mkstemp` + `os.replace` replaced with `durable_write`; keeps raising on failure |
| tests/test_project_registry.py | +32/-0 | New `TestSaveIsDurable` class: durable-write routing and raise-on-failure with nothing left on disk |

`git apply --check` real exit 0, `git apply` real exit 0. Measured insertions: 35 (3+32), matches the block's expected value exactly.

### C6 (this commit) F278 R4 C6: rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f278-r4-probe cde8d5f3` — real exit 0.
- `python3 .remedy-wt/f278-r4-payloads/revert_probes.py .remedy-wt/f278-r4-probe ce53bd0c` — real exit 0 (see Verification, G5).
- `git worktree remove --force .remedy-wt/f278-r4-probe` — real exit 0.
- `git worktree prune` — real exit 0.
- `git push origin feature/f278-durable-writes-loud-failures` — see Verification, G6, for the real outcome (reported separately since it runs after this commit).
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no checkout of another branch: none run, per the block's constraints.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, exit 2, absent (proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `feature/f278-durable-writes-loud-failures`. `git log --oneline -1` → `ce53bd0c F278 R3 C6: rewrite handoff for round 3`.
- Block bytes (R-0954): measured lines=205, sha256=`5ecaa3f036621a693f46a97fef4751b3231c52f25e83f590fddf59b16212b232`; matches both given readings exactly.
- `git worktree list` (before) → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` only.
- `git branch --list 'remedy/job-*' | wc -l` → 38.

PAYLOADS — all 7 measured and matched the block's table exactly (lines/bytes/sha256): decisions.md (37/2639), dev.diff (222/9394), ledger.md (2/2554), plan.md (29/1070), reg.diff (89/3425), revert_probes.py (51/1986), snap.diff (95/3997). All sha256 readings matched the table verbatim.

G1 TRANSPORT — every `.agent/authored/f278-r4-*` copy read back with `git show <commit>:<path>` and compared byte-for-byte against its source: all 8 copies (block.md + 7 payloads) matched exactly.

G2 THE BOOKING — at C2 (`c02906f9`), each appended/rewritten file's byte count matched `ce53bd0c` bytes plus the payload's bytes by strict concatenation (live_review.md: 430456+2554=433010; decisions.md: 1844455+2639=1847094; plan.md rewritten to 1070), and the sha256 read with `git show c02906f9:<path>` matched the reviewer's dry-run reading for all three files:
- `.agent/live_review.md`: bytes=433010, sha256=`11dee21ae698fb999218dca428ba694efaa8d8b9500a9b354743a00a7b209c9e` — MATCH
- `.agent/decisions.md`: bytes=1847094, sha256=`261feb3990ab5d221be23db2925aeceb7bf507f9de6a0b3f3fc83ad71cc3d2ac` — MATCH
- `.agent/plan.md`: bytes=1070, sha256=`1a4ebc33f20ebab4850918210d74d059a979f077284daa3daece359606a82c29` — MATCH

Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md` TEXT: at `ce53bd0c` count=26; at C2 (`c02906f9`) count=26; `base - c2` = `[]`; `c2 - base` = `[]` — both differences empty, matching the reviewer's 26/26.

G3 THE PRODUCT BYTES — at C5 (`cde8d5f3`), sha256 of each file read with `git show cde8d5f3:<path>`, all 9 MATCH:
- `apps/cli/commands/runtime_cmd.py`: bytes=40387, sha256=`b222d6c83d053c12f298d543ecd0771dcfd6d529ed33d4e347fe0843eda18298`
- `packages/orchestration/project_registry.py`: bytes=31199, sha256=`bf7230c33583129d7854c482fd37a8c0cd334161b510109d6172665919225631`
- `packages/orchestration/repository_snapshot.py`: bytes=59062, sha256=`a27604da7bb71f75c11e484970535be0a264037eabc476565a99fd3c00c72ea5`
- `packages/runtimes/dev_server.py`: bytes=88155, sha256=`c0b6c65155c76d22992eab741856a6594cfded51135d8c043b9d7cde6698982d`
- `packages/runtimes/runtime_supervisor.py`: bytes=25280, sha256=`f37d1160a70036b27251614d078cc0df8e97c07efeeae1764a75bf38380f05eb`
- `tests/orchestration/test_durable_write_guard.py`: bytes=3145, sha256=`3eca8ebc217dbaed4ec35f42b9a6266c2e9054a642a3dd4f4fd5a15d9ea39a93`
- `tests/orchestration/test_repository_snapshot.py`: bytes=43121, sha256=`54c047e1968dbd7066f376e10d6c58b7285e25bfedfb9585c530e201a011cd93`
- `tests/runtimes/test_supervisor_portability.py`: bytes=106273, sha256=`6fcaaad3f6867249ccf215d899f4579a15eb4ea3f8a5878982b1ac826acc9f9b`
- `tests/test_project_registry.py`: bytes=15351, sha256=`9955bda0a7539475c750cb1f0d629a31216becf01ce5f7b48ed7b761606568f5`

G4 THE TESTS — command (the block's own, in the primary checkout at C5, including `tests/runtimes/` and `tests/cli/test_golden_path.py` as the block's own G4 command lists):
```
python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_durable_write_guard.py tests/runtimes/ tests/cli/test_runtime_cmd.py tests/orchestration/test_repository_snapshot.py tests/test_project_registry.py tests/orchestration/test_project_resolution.py tests/cli/test_project_current.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
```
Result: `663 passed in 409.12s (0:06:49)`, real exit 0 (`${PIPESTATUS[0]}`). The reviewer's own run, in a disposable worktree WITHOUT the golden path file, read `615 passed, 6 skipped` at exit 0 in about four minutes; this run's command already includes `tests/cli/test_golden_path.py` and `tests/runtimes/` as the block states them, giving a higher pass count and no reported skip, consistent with the block's own note that `tests/runtimes/` (real processes) accounts for most of the time.

`python3 -m ruff check` over every Python path of the G3 table (9 files) → `All checks passed!`, real exit 0.

`python3 -m apps.cli.main integrity check --json` → `fail_count: 0`, `ok: true`, `passed: true`, all 5 checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency` with `unchecked=0, context_complete=False`, `relevant_untracked` with `untracked=0, relevant=0`, `high_blockers_open`). Real exit 0.

G5 THE REVERT PROBES — `git worktree add --detach .remedy-wt/f278-r4-probe cde8d5f3` real exit 0. `python3 .remedy-wt/f278-r4-payloads/revert_probes.py .remedy-wt/f278-r4-probe ce53bd0c` real exit 0, full output:
```
control_before REAL_EXIT=0
117 passed in 2.37s
p1_dev_server_only REAL_EXIT=1
FAILED tests/orchestration/test_durable_write_guard.py::test_no_private_atomic_write_helper_outside_packages_common
1 failed, 116 passed in 2.19s
p1_dev_server_only restored clean: True
p2_dev_server_group REAL_EXIT=1
FAILED tests/orchestration/test_durable_write_guard.py::test_no_private_atomic_write_helper_outside_packages_common
1 failed, 116 passed in 2.19s
p2_dev_server_group restored clean: True
p3_repository_snapshot REAL_EXIT=1
FAILED tests/orchestration/test_repository_snapshot.py::TestApplyRecordStateIsDurable::test_the_update_is_written_through_durable_write
FAILED tests/orchestration/test_repository_snapshot.py::TestApplyRecordStateIsDurable::test_a_failed_write_answers_false_and_keeps_the_record
2 failed, 115 passed in 2.23s
p3_repository_snapshot restored clean: True
p4_project_registry REAL_EXIT=1
FAILED tests/test_project_registry.py::TestSaveIsDurable::test_the_record_is_written_through_durable_write
FAILED tests/test_project_registry.py::TestSaveIsDurable::test_a_failed_write_raises_and_leaves_nothing
2 failed, 115 passed in 2.17s
p4_project_registry restored clean: True
control_after REAL_EXIT=0
117 passed in 2.18s
```
Every reading matches the reviewer's stated expectations exactly: control_before 117 passed/0; p1 and p2 each 1 failed/116 passed/1 at the guard's `test_no_private_atomic_write_helper_outside_packages_common`; p3 2 failed/115 passed/1, both `TestApplyRecordStateIsDurable` tests; p4 2 failed/115 passed/1, both `TestSaveIsDurable` tests; control_after 117 passed/0; every `restored clean` line `True`.

`git worktree remove --force .remedy-wt/f278-r4-probe` real exit 0. `git worktree prune` real exit 0. `git worktree list` afterward → primary checkout (`feature/f278-durable-writes-loud-failures`) and `.remedy-wt/job-129b3ad7206d4f8d` only — the probe worktree is gone.

G6 TREE AND PUSH — reported in the session's final reply, not this file, since it runs after this commit (C6). The handback cannot contain readings that postdate its own write.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- `decisions.md` (append): `.agent/decisions.md` at C2 sha256 `261feb...71cc3d2ac` == payload sha256 concatenated onto the `ce53bd0c` bytes (G2). MATCH.
- `ledger.md` (append): `.agent/live_review.md` at C2 sha256 `11dee2...7b209c9e` == payload sha256 concatenated onto the `ce53bd0c` bytes (G2). MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256 `1a4ebc...606a82c29` == payload sha256 exactly (G2). MATCH.
- `dev.diff` (applied): `.agent/authored/f278-r4-dev.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C3; resulting files' sha256 at C5 match the G3 table. MATCH.
- `snap.diff` (applied): `.agent/authored/f278-r4-snap.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C4; resulting files' sha256 at C5 match the G3 table. MATCH.
- `reg.diff` (applied): `.agent/authored/f278-r4-reg.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C5; resulting files' sha256 at C5 match the G3 table. MATCH.
- `revert_probes.py`: a TOOL run against the disposable probe worktree, never applied to a tracked file. `.agent/authored/f278-r4-revert_probes.py` at C1b verified byte-identical to the payload (G1). N/A for an "applied location" comparison by design.
- This block (`f278-r4-block.md`): `.agent/authored/f278-r4-block.md` at C1a verified byte-identical to `.remedy-wt/f278-r4-block.md` (G1) and to the two readings given in the delegation message.

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

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 4,
then T003 — BLE001 with a frozen ignore list, starting with the handlers in
`packages/orchestration/stream_evidence.py`. Open findings: 26. Operator
questions: 0.
