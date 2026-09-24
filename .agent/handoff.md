# Handback — F284 Findings paydown v3 · Round 1

## Session

SESSION 1 of feature F284 · round 1 · rounds so far 1

This round claims F284, re-heads the live review record, books F019's round 9 gate entry,
records DECISION F284 D1, writes F284's slice list, and lands T001 (R-1046: `teacher.model`
reaches `teacher ask` and the lessons path through one helper) and T002 (R-0499: the vitest
node's skip gate reads the installed runner, not the directory), with red proofs for both. I had
ample context remaining throughout this round; no session-limit pressure at any point.

## Range

Review of a36a8759..HEAD

## Commits

### 283362dd9 F284 R1 C1a: copy round 1 block and claim payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f284-r1-block.md | +226/-0 | copy of this round's block, verbatim |
| .agent/authored/f284-r1-plan.md | +30/-0 | copy of the plan.md payload |
| .agent/authored/f284-r1-context.md | +36/-0 | copy of the context.md payload |
| .agent/authored/f284-r1-claim.diff | +161/-0 | copy of the claim.diff payload |

453 insertions by `git show --numstat` (block's 226 lines + 227 for the three payloads); matches
the block's expectation exactly; under the 500-insertion cap.

### 213ee4138 F284 R1 C1b: copy round 1 code payloads and mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f284-r1-r1046.diff | +166/-0 | copy of the r1046.diff payload |
| .agent/authored/f284-r1-r0499.diff | +22/-0 | copy of the r0499.diff payload |
| .agent/authored/f284-r1-mutations.py | +85/-0 | copy of the mutations.py tool |

273 insertions by `git show --numstat`; matches the block's expectation exactly.

### 038035cf7 F284 R1 C2: claim F284, re-head the live review record, book F019 R9, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +12/-16 | rewritten to the context.md payload (F284 scope) |
| .agent/decisions.md | +49/-0 | DECISION F284 D1 appended (claim.diff) |
| .agent/live_review.md | +28/-14 | re-headed to F284; F019 round 9 gate entry appended (claim.diff) |
| .agent/plan.md | +17/-18 | rewritten to the plan.md payload (F284 round 1 scope) |
| docs/roadmap/STATUS.md | +1/-1 | F284's line `[ ]` → `[~]` (claim.diff) |
| docs/roadmap/features/T2_F284.md | +19/-0 | slice list and R-1046 Acceptance line (claim.diff) |

`git apply --check` on claim.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 12/49/28/17/1/19 across the six paths — matches the block's expectation exactly.

### ca04d1aff F284 R1 C3: read teacher.model for teacher ask and lessons through one helper
| Path | +/- | Reason |
|---|---|---|
| docs/guides/environment.md | +1/-1 | `REMEDY_TEACHER_MODEL` row no longer says nothing reads the key |
| packages/orchestration/config.py | +2/-3 | key description says who reads `teacher.model` now |
| packages/orchestration/lessons.py | +0/-8 | `lesson_role_overrides` deleted (replacing is deleting) |
| packages/orchestration/pingpong_job.py | +2/-1 | lessons path imports and calls `teacher_role_overrides` |
| packages/orchestration/teacher_model.py | +13/-2 | new helper `teacher_role_overrides`; `ask_teacher` passes it to both `resolve_role_config` and `resolve_teacher_transport` |
| tests/orchestration/test_lessons.py | +3/-1 | test updated to the new helper; asserts the override reaches `config_file` |
| tests/orchestration/test_teacher_model.py | +28/-0 | new `TestTheConfiguredModelReachesTheQuestion` class |

`git apply --check` on r1046.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 1/2/0/2/13/3/28 across the seven paths — matches the block's expectation exactly.

### 73d7f809b F284 R1 C4: gate the vitest node on the installed runner, as the tsc node is gated
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_test_runner.py | +6/-3 | `test_vitest_passes` skip condition reads `apps/ui/node_modules/.bin/vitest` (a file), not the directory |

`git apply --check` on r0499.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 6 — matches the block's expectation exactly.

### (this commit) F284 R1 C5: rewrite handoff for round 1
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f284-r1-mut 73d7f809b` — exit 0, created for G4's red
  proofs.
- `git worktree remove --force .remedy-wt/f284-r1-mut` — exit 0, removed as G4's last action.
- `git worktree prune` — exit 0.
- No `git push` yet at the time this handback is written; the block orders it after this commit.
  Its real outcome is reported in the reply per the block's own instruction (G6 cannot be inside
  C5).
- No `gh pr create`: the block forbids it this round; the branch opens a pull request at F284's
  closure.

## Verification

```
$ python3 - (line/byte/sha256 of each payload under .remedy-wt/f284-r1-payloads/)
claim.diff lines 161 bytes 16484 sha256 b3081565b0b236688352e8caaa116278daec6680219b95fa992bada889577204
plan.md lines 30 bytes 1017 sha256 3d1d514742beb4849b92ce114e0096b44587189aa9985c2eed0963ae48d6234b
context.md lines 36 bytes 1469 sha256 082b2105331af24ae6894c2addf00ddc8cb7b5c322c10a41d8788d4f1357db92
r1046.diff lines 166 bytes 10481 sha256 fbe2063fd3a547820acfb470b03155c520059f395972cfc604e180b9b9a3fe76
r0499.diff lines 22 bytes 1325 sha256 85e6bf172fe437cf01a88f4d8664b8cd8382dfb5b44eaca5a6d7c0d988119d96
mutations.py lines 85 bytes 3686 sha256 d3caa395f704dc5d83e4f72a4133c078364d2cc3948d3f584e873f9d4a141b6f
REAL_EXIT=0
```
All six match the PAYLOADS table exactly.

```
$ (compare each .agent/authored/f284-r1-* copy against its source, read back with git show)
.agent/authored/f284-r1-block.md @ 283362dd9: bytes=16374 sha256=c62e5fb5...267a308 matches_source=True
.agent/authored/f284-r1-plan.md @ 283362dd9: bytes=1017 sha256=3d1d5147...48c234b matches_source=True
.agent/authored/f284-r1-context.md @ 283362dd9: bytes=1469 sha256=082b2105...357db92 matches_source=True
.agent/authored/f284-r1-claim.diff @ 283362dd9: bytes=16484 sha256=b3081565...889577204 matches_source=True
.agent/authored/f284-r1-r1046.diff @ 213ee4138: bytes=10481 sha256=fbe2063fd3...180b9b9a3fe76 matches_source=True
.agent/authored/f284-r1-r0499.diff @ 213ee4138: bytes=1325 sha256=85e6bf17...988119d96 matches_source=True
.agent/authored/f284-r1-mutations.py @ 213ee4138: bytes=3686 sha256=d3caa395...a4141b6f matches_source=True
REAL_EXIT=0
```
All 7 (the block copy plus the six payload copies) BYTE-IDENTICAL against their sources (G1).

```
$ (sha256 of each C2/C3/C4 file, read with git show <commit>:<path>, against the reviewer's table)
038035cf7 .agent/context.md: bytes=1469 match=True
038035cf7 .agent/decisions.md: bytes=2019743 match=True
038035cf7 .agent/live_review.md: bytes=304288 match=True
038035cf7 .agent/plan.md: bytes=1017 match=True
038035cf7 docs/roadmap/STATUS.md: bytes=50463 match=True
038035cf7 docs/roadmap/features/T2_F284.md: bytes=4015 match=True
ca04d1aff docs/guides/environment.md: bytes=21268 match=True
ca04d1aff packages/orchestration/config.py: bytes=63251 match=True
ca04d1aff packages/orchestration/lessons.py: bytes=21150 match=True
ca04d1aff packages/orchestration/pingpong_job.py: bytes=204054 match=True
ca04d1aff packages/orchestration/teacher_model.py: bytes=10626 match=True
ca04d1aff tests/orchestration/test_lessons.py: bytes=20517 match=True
ca04d1aff tests/orchestration/test_teacher_model.py: bytes=12399 match=True
73d7f809b tests/orchestration/test_test_runner.py: bytes=37844 match=True
ALL_MATCH: True
REAL_EXIT=0
```
All 14 sha256 readings match the reviewer's simulated-tree table exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
a36a8759 open ids: ['R-0499', 'R-0950', 'R-1008', 'R-1046'] count: 4
038035cf7 open ids: ['R-0499', 'R-0950', 'R-1008', 'R-1046'] count: 4
```
Open set is 4 by distinct id at both commits, identical set, matching the reviewer's reading
(G2).

```
STATUS line: '- [~] F284 — Findings paydown v3'
```
F284's STATUS line at C2 reads exactly `- [~] F284 — Findings paydown v3` (G2).

```
$ git diff --name-only 283362dd9 213ee4138   (C1a..C1b)
.agent/authored/f284-r1-mutations.py
.agent/authored/f284-r1-r0499.diff
.agent/authored/f284-r1-r1046.diff

$ git diff --name-only 213ee4138 038035cf7   (C1b..C2)
.agent/context.md
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
docs/roadmap/STATUS.md
docs/roadmap/features/T2_F284.md

$ git diff --name-only 038035cf7 ca04d1aff   (C2..C3)
docs/guides/environment.md
packages/orchestration/config.py
packages/orchestration/lessons.py
packages/orchestration/pingpong_job.py
packages/orchestration/teacher_model.py
tests/orchestration/test_lessons.py
tests/orchestration/test_teacher_model.py

$ git diff --name-only ca04d1aff 73d7f809b   (C3..C4)
tests/orchestration/test_test_runner.py
```
Each consecutive-commit diff names exactly the paths that commit's entry in the block lists (G2).

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_teacher_model.py
tests/orchestration/test_lessons.py tests/orchestration/test_test_runner.py
tests/cli/test_teacher_cmd.py tests/ui_server/test_lessons_route.py
tests/cli/test_study_teacher_e2e.py tests/ui_server/test_dashboard_contract.py
tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -30;
echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md
  was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1,
  docs/agents/planner_reviewer_prompt.md). ...
627 passed, 1 skipped in 65.19s (0:01:05)
REAL_EXIT=0
```
The reviewer's sim read `625 passed, 3 skipped`; my run in the primary checkout read `627 passed,
1 skipped` — exactly +2 passed / -2 skipped, because `test_vitest_passes` and
`test_typescript_compiles` PASS here instead of skip, as required. The one remaining skip is the
unrelated D12-quarantine node, not a toolchain node.

```
$ python3 -m ruff check packages/orchestration/config.py packages/orchestration/teacher_model.py
packages/orchestration/lessons.py packages/orchestration/pingpong_job.py
tests/orchestration/test_teacher_model.py tests/orchestration/test_lessons.py
tests/orchestration/test_test_runner.py
All checks passed!
REAL_EXIT=0
```

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status":
"pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
{"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
{"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message":
"no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status":
"pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status":
"pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0 (G3).

```
$ git worktree add --detach .remedy-wt/f284-r1-mut 73d7f809b
Preparing worktree (detached HEAD 73d7f809b)
REAL_EXIT=0

$ python3 -B .remedy-wt/f284-r1-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f284-r1-mut
control first R-1046 tests: exit 0: 55 passed in 1.97s
control first vitest node over an empty node_modules: exit 0: 1 skipped in 0.14s
m1 (ask_teacher reads no override): FROM occurs 1x in packages/orchestration/teacher_model.py
m1: exit 1: 1 failed, 54 passed in 1.96s; restored byte-identical: True
m2 (the transport ignores the override): FROM occurs 1x in packages/orchestration/teacher_model.py
m2: exit 1: 1 failed, 54 passed in 2.41s; restored byte-identical: True
m3 (the lessons path hands in no override): FROM occurs 1x in packages/orchestration/pingpong_job.py
m3: exit 1: 1 failed, 54 passed in 2.12s; restored byte-identical: True
m4 (the helper never reads the key): FROM occurs 1x in packages/orchestration/teacher_model.py
m4: exit 1: 3 failed, 52 passed in 1.86s; restored byte-identical: True
m5 (the vitest gate reads the directory again): FROM occurs 1x in tests/orchestration/test_test_runner.py
m5: exit 1: 1 failed in 0.80s; restored byte-identical: True
control last R-1046 tests: exit 0: 55 passed in 1.94s
control last vitest node over an empty node_modules: exit 0: 1 skipped in 0.14s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0

$ git worktree remove --force .remedy-wt/f284-r1-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
```
Matches the reviewer's own simulated-tree reading exactly, mutation-for-mutation (G4). Worktree
cleanly removed; every pre-existing worktree and branch under `.remedy-wt/` left untouched.

```
$ git show --numstat --format= 283362dd9   (C1a)
226	0	.agent/authored/f284-r1-block.md
161	0	.agent/authored/f284-r1-claim.diff
36	0	.agent/authored/f284-r1-context.md
30	0	.agent/authored/f284-r1-plan.md

$ git show --numstat --format= 213ee4138   (C1b)
85	0	.agent/authored/f284-r1-mutations.py
22	0	.agent/authored/f284-r1-r0499.diff
166	0	.agent/authored/f284-r1-r1046.diff

$ git show --numstat --format= 038035cf7   (C2)
12	16	.agent/context.md
49	0	.agent/decisions.md
28	14	.agent/live_review.md
17	18	.agent/plan.md
1	1	docs/roadmap/STATUS.md
19	0	docs/roadmap/features/T2_F284.md

$ git show --numstat --format= ca04d1aff   (C3)
1	1	docs/guides/environment.md
2	3	packages/orchestration/config.py
0	8	packages/orchestration/lessons.py
2	1	packages/orchestration/pingpong_job.py
13	2	packages/orchestration/teacher_model.py
3	1	tests/orchestration/test_lessons.py
28	0	tests/orchestration/test_teacher_model.py

$ git show --numstat --format= 73d7f809b   (C4)
6	3	tests/orchestration/test_test_runner.py
```
C1a total 453 (expected 453). C1b total 273 (expected 273). C2 insertions 12/49/28/17/1/19
(expected same, sum 126). C3 insertions 1/2/0/2/13/3/28 (expected same, sum 49). C4 insertion 6
(expected 6). All five commits match their block entries exactly and stay under the 500-insertion
cap (G5).

G6 — reported in the reply per the block's own instruction (measured after C5, after the push).

## Authored-text proofs

All 7 authored copies under `.agent/authored/f284-r1-*` (the block copy plus the six payload
copies) were built by reading each source's bytes with `shutil.copyfile` and writing them
unedited — never retyped, never edited. Each was read back with `git show <commit>:<path>` from
the commit that added it (283362dd9 for the block/plan/context/claim.diff copies, 213ee4138 for
the r1046.diff/r0499.diff/mutations.py copies) and compared byte for byte against its source: all
7 BYTE-IDENTICAL (G1 above). `claim.diff`, `r1046.diff` and `r0499.diff` were each applied with
`git apply` after `git apply --check` passed (exit 0 both, all three), never retyped or edited;
the resulting file contents were verified by byte count and sha256 against the reviewer's own
simulated-tree table at G2 above — all 14 named files MATCH. `.agent/plan.md` and
`.agent/context.md` were separately rewritten whole via `shutil.copyfile` from their payloads and
also confirmed MATCH against the PAYLOADS table and the G2 table.

## Deviations & assumptions

None. Every commit landed in the block's stated order C1a, C1b, C2, C3, C4, then this handback
commit C5, exactly as ordered. G1 through G5 ran before this handback was written, as the block
orders; G6 runs after C5 and is reported in the reply, since C5 cannot contain it. No payload was
edited, retyped or repaired. The round wrote no `Done:` line and no `Landed:` line for R-1046 or
R-0499 — those resolutions belong to the reviewer at the next gate, per constraint 4. Nothing is
merged: no `gh pr merge`, no `gh pr create`, no checkout of `main` after the branch was cut, no
branch deletion, no force-push, no `git stash`. The full suite was not run: amend0917 rule 1 gives
F284 exactly one full-suite run, reserved for its closure.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 453 insertions, matches block + 3 payloads exactly |
| C1b | done | 273 insertions, matches exactly |
| C2 | done | claim.diff apply --check and apply both exit 0; 12/49/28/17/1/19 insertions, matches |
| C3 | done | r1046.diff apply --check and apply both exit 0; 1/2/0/2/13/3/28 insertions, matches |
| C4 | done | r0499.diff apply --check and apply both exit 0; 6 insertions, matches |
| C5 | done | this handback, self-reference exception |
| T001 (R-1046) | done | landed in C3; red-proved by m1-m4, all caught and restored (G4) |
| T002 (R-0499) | done | landed in C4; red-proved by m5, caught and restored (G4) |
| G1 | done | all 6 payload digests and 7 authored-copy comparisons matched |
| G2 | done | all 14 named file digests matched; open set 4 at both commits; STATUS line exact; 4 consecutive-commit path sets exact |
| G3 | done | 627 passed/1 skipped exit 0 (both toolchain nodes PASS, not skip); ruff All checks passed; integrity check all 6 pass, fail_count 0 |
| G4 | done | all 5 mutations + 2 controls caught/restored exactly as the reviewer's own reading; worktree removed, pruned |
| G5 | done | all 5 commits' numstat matches their block entries exactly |
| G6 | done | reported in the reply (measured after C5, after the push) |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 1. Then T003 — R-0950's
zombie-process node in `tests/orchestration/test_product_smoke.py`. Open findings: 4.
Operator questions open: 3.
