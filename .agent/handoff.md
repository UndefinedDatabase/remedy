# Handback — F278 Durable writes & loud failures · Round 1 · Claim F278 and land T001

## Session

SESSION 1 of feature F278 · round 1 · rounds so far 1

This round cut the feature branch from `9817a927` (the merge commit of pull
request 265, F283's closure), claimed F278 by re-heading the live review
record and flipping its STATUS line to `[~]`, and landed T001 alone —
`durable_write` and `durable_write_json` in `packages/common/secure_fs.py` —
with a new test file whose fsync test and concurrent-writer test served as
this slice's two red proofs, both verified by mutation inside a disposable
worktree that was removed afterward. Context self-assessment: a comfortable
majority of the working budget remains at handback.

## Range

Review of `9817a927`..`HEAD`.

## Commits

### 85869bfa F278 R1 C1a: copy round 1 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r1-block.md | +208/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r1-context.md | +50/-0 | Bookkeeping copy of the context.md rewrite payload |
| .agent/authored/f278-r1-plan.md | +35/-0 | Bookkeeping copy of the plan.md rewrite payload |
| .agent/authored/f278-r1-rehead.diff | +63/-0 | Bookkeeping copy of the live_review.md re-head diff |
| .agent/authored/f278-r1-status.diff | +13/-0 | Bookkeeping copy of the STATUS.md diff |

Measured insertions: 369 (block 208 + 161 payload lines), under the 500 cap.

### 4c2c9970 F278 R1 C1b: copy round 1 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r1-mutations.py | +53/-0 | Bookkeeping copy of the G5 mutation-testing tool |
| .agent/authored/f278-r1-secure_fs.diff | +86/-0 | Bookkeeping copy of the durable_write diff |
| .agent/authored/f278-r1-test_secure_fs_durable_write.py | +173/-0 | Bookkeeping copy of the new test file |

Measured insertions: 312 (expected 312).

### 7db6d334 F278 R1 C2: claim F278 and re-head the live review record
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +22/-30 | `git apply rehead.diff`: re-head the live review record for F278 |
| docs/roadmap/STATUS.md | +1/-1 | `git apply status.diff`: flip F278's STATUS line to `[~]` (claimed) |
| .agent/plan.md | +22/-18 | Rewritten to plan.md payload for round 1 |
| .agent/context.md | +22/-36 | Rewritten to context.md payload for round 1 |

Measured insertions: 67 (22 + 1 + 22 + 22, expected 67 in that order).

### 5031b1bc F278 R1 C3: add durable_write, the one path-based durable write
| Path | +/- | Reason |
|---|---|---|
| packages/common/secure_fs.py | +64/-0 | `git apply secure_fs.diff`: adds `durable_write` and `durable_write_json` |
| tests/orchestration/test_secure_fs_durable_write.py | +173/-0 | New test file, copied whole and `git add`ed (an untracked test file fails `integrity check`'s `relevant_untracked`) |

Measured insertions: 237 (64 + 173, expected 237).

### C4 (this commit) F278 R1 C4: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git checkout -b feature/f278-durable-writes-loud-failures` at `9817a927` — branch created, no pull (Open PR Gate had already run; `main` at the merge commit).
- `git worktree add --detach .remedy-wt/f278-r1-mut 5031b1bc` — real exit 0.
- `python3 .remedy-wt/f278-r1-payloads/mutations.py .remedy-wt/f278-r1-mut` — real exit 0 (see Verification, G5).
- `git worktree remove --force .remedy-wt/f278-r1-mut` — real exit 0.
- `git worktree prune` — real exit 0.
- `git push -u origin feature/f278-durable-writes-loud-failures` — see Verification, G6, for the real outcome (reported separately since it runs after this commit).
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`: none run, per the block's constraints.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, real exit 2 (absent, proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `main`. `git log --oneline -1` → `9817a927 Merge pull request #265 ...`.
- Block bytes (R-0954): measured lines=208, sha256=`19dc1c5cb7429fd7b69bd4952dbcc3324a4e3bac89256b46d6775af738ab342a`; matches both given readings exactly.
- `git worktree list` (before) → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` only.
- `git branch --list 'remedy/job-*' | wc -l` → 38.

PAYLOADS — all 7 measured and matched the block's table exactly (lines/bytes/sha256): context.md (50/2451), plan.md (35/1483), rehead.diff (63/6919), secure_fs.diff (86/3878), status.diff (13/2027), test_secure_fs_durable_write.py (173/6828), mutations.py (53/2169). All sha256 readings matched the table verbatim.

G1 TRANSPORT — every `.agent/authored/f278-r1-*` copy read back with `git show <commit>:<path>` and compared byte-for-byte (via sha256) against its source: all 8 copies (block.md + 7 payloads) matched exactly, `match=True` for each.

G2 THE CLAIM — sha256 of the four claim files read with `git show 7db6d334:<path>`:
- `.agent/live_review.md`: bytes=424321, sha256=`c02956ae55c72f2f52e00dcfc4f8bfa1a16ea751fa0f9203b08567cfb89210ff` — MATCH
- `docs/roadmap/STATUS.md`: bytes=46787, sha256=`e4171f9f665060d7e477661e86ee4d078b7f9691a81fd8bb371e4e4357e385cb` — MATCH
- `.agent/plan.md`: bytes=1483, sha256=`ef79958425dd58e1c5873ea3b438afedf5ce13ed0addc62155502aa61ec41ad1` — MATCH
- `.agent/context.md`: bytes=2451, sha256=`55be0a982026b146d5511ffee64a3d8cc46a730085e074fdf401cb64144dfd4b` — MATCH

Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md` TEXT: at `9817a927` count=26; at C2 (`7db6d334`) count=26; `base - c2` = `[]`; `c2 - base` = `[]` — both differences empty, matching the reviewer's 26/26.

`.agent/plan.md` line count at C2: 35 (under 50).

STATUS F278 line at C2: `- [~] F278 — Durable writes & loud failures` — begins `- [~] F278 — ` as required.

`git diff --name-only 4c2c9970 7db6d334` → `.agent/context.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md` — exactly the paths C2 lists.

G3 THE HELPER — `git diff --name-only 7db6d334 5031b1bc` → `packages/common/secure_fs.py`, `tests/orchestration/test_secure_fs_durable_write.py` — exactly these two. sha256 read with `git show 5031b1bc:<path>`:
- `packages/common/secure_fs.py`: bytes=39941, sha256=`5affd1a24a88d390bb6fec5e019012b0b122a42786e9e47919025ded70d0fae0` — MATCH
- `tests/orchestration/test_secure_fs_durable_write.py`: bytes=6828, sha256=`e2de683d0958dce574051ec0c683fbde83e2eb330b43cc07567e4405e7c86f92` — MATCH

G4 THE TESTS — command:
```
python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_secure_fs_durable_write.py tests/orchestration/test_secure_fs.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/cli/test_golden_path.py
```
Result: `585 passed in 156.56s`, real exit 0 (`${PIPESTATUS[0]}`). The reviewer's own run, in a disposable worktree lacking the UI toolchain and WITHOUT `tests/cli/test_golden_path.py`, read `541 passed, 2 skipped` at exit 0; the primary checkout run here includes the golden path file and carries the UI toolchain the worktree lacked, so it reads more passes and no skips — consistent with the block's stated expectation that "a skip may pass there."

`python3 -m ruff check packages/common/secure_fs.py tests/orchestration/test_secure_fs_durable_write.py` → `All checks passed!`, real exit 0.

`python3 -m apps.cli.main integrity check --json` → `fail_count: 0`, `ok: true`, `passed: true`, all 5 checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked` with `untracked=0, relevant=0`, `high_blockers_open`). Real exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f278-r1-mut 5031b1bc` real exit 0. `python3 .remedy-wt/f278-r1-payloads/mutations.py .remedy-wt/f278-r1-mut` real exit 0, full output:
```
control_before REAL_EXIT=0
11 passed in 0.30s
m1_no_file_fsync FROM count in file: 1
m1_no_file_fsync REAL_EXIT=1
FAILED tests/orchestration/test_secure_fs_durable_write.py::TestBothFsyncsHappen::test_the_file_and_then_its_parent_directory_are_fsynced
FAILED tests/orchestration/test_secure_fs_durable_write.py::TestBothFsyncsHappen::test_fsync_dir_false_skips_only_the_directory
2 failed, 9 passed in 0.26s
m1_no_file_fsync restored byte-identical: True
m2_no_dir_fsync FROM count in file: 1
m2_no_dir_fsync REAL_EXIT=1
FAILED tests/orchestration/test_secure_fs_durable_write.py::TestBothFsyncsHappen::test_the_file_and_then_its_parent_directory_are_fsynced
1 failed, 10 passed in 0.28s
m2_no_dir_fsync restored byte-identical: True
m3_fixed_sibling FROM count in file: 1
m3_fixed_sibling REAL_EXIT=1
FAILED tests/orchestration/test_secure_fs_durable_write.py::TestConcurrentWritersOfOnePath::test_eight_writers_leave_exactly_one_intact_payload_and_no_residue
FAILED tests/orchestration/test_secure_fs_durable_write.py::TestTheTemporaryFile::test_a_multi_suffix_name_keeps_its_temporary_file_a_sibling_under_its_whole_name
2 failed, 9 passed in 0.25s
m3_fixed_sibling restored byte-identical: True
control_after REAL_EXIT=0
11 passed in 0.28s
```
Every reading matches the reviewer's stated expectations exactly: control_before 11 passed/0; m1 2 failed/9 passed/1, both failures in `TestBothFsyncsHappen`; m2 1 failed/10 passed/1 at `test_the_file_and_then_its_parent_directory_are_fsynced`; m3 2 failed/9 passed/1 at the two named tests; control_after 11 passed/0.

`git worktree remove --force .remedy-wt/f278-r1-mut` real exit 0. `git worktree prune` real exit 0. `git worktree list` afterward → primary checkout (`feature/f278-durable-writes-loud-failures`) and `.remedy-wt/job-129b3ad7206d4f8d` only — the mutation worktree is gone.

G6 TREE AND PUSH — reported in the session's final reply, not this file, since it runs after this commit (C4). The handback cannot contain readings that postdate its own write.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- `context.md` (rewrite): `.agent/context.md` at C2 sha256 `55be0a98...4dfd4b` == `.agent/authored/f278-r1-context.md` at C1a == payload sha256. MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256 `ef799584...1ec41ad1` == `.agent/authored/f278-r1-plan.md` at C1a == payload sha256. MATCH.
- `rehead.diff` (applied): `.agent/authored/f278-r1-rehead.diff` at C1a byte-identical to the payload (G1); resulting `.agent/live_review.md` at C2 sha256 `c02956ae...cfb89210ff` matches the reviewer's stated reading (G2). MATCH.
- `status.diff` (applied): `.agent/authored/f278-r1-status.diff` at C1a byte-identical to the payload (G1); resulting `docs/roadmap/STATUS.md` at C2 sha256 `e4171f9f...357e385cb` matches the reviewer's stated reading (G2). MATCH.
- `secure_fs.diff` (applied): `.agent/authored/f278-r1-secure_fs.diff` at C1b byte-identical to the payload (G1); resulting `packages/common/secure_fs.py` at C3 sha256 `5affd1a2...ed70d0fae0` matches the reviewer's stated reading (G3). MATCH.
- `test_secure_fs_durable_write.py` (copied whole): `.agent/authored/f278-r1-test_secure_fs_durable_write.py` at C1b byte-identical to the payload (G1); the tracked test file at C3 sha256 `e2de683d...4405e7c86f92` matches both the payload and the reviewer's stated reading (G3). MATCH.
- `mutations.py`: a TOOL run against the disposable worktree, never applied to a tracked file. `.agent/authored/f278-r1-mutations.py` at C1b verified byte-identical to the payload (G1). N/A for an "applied location" comparison by design.
- This block (`f278-r1-block.md`): `.agent/authored/f278-r1-block.md` at C1a verified byte-identical to `.remedy-wt/f278-r1-block.md` (G1) and to the two readings given in the delegation message.

## Deviations & assumptions

None. The round followed the block's ordered commit sequence (C1a, C1b, C2, C3, C4) exactly, touched exactly the tracked path set the block names, and ran no full suite.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 1,
then T002 — the migration of the surviving private atomic-write helpers onto
`durable_write`, re-derived from the tree, one module per commit. Open
findings: 26. Operator questions: 0.
