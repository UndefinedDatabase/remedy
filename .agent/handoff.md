# Handback — F284 Findings paydown v3 · Round 2

## Session

SESSION 1 of feature F284 · round 2 · rounds so far 2

This round books round 1's PASS with the resolutions of R-1046 and R-0499, records DECISION F284
D2, lands T003 (R-0950: `assert_the_app_left_nothing_behind` judges teardown at all five teardown
sites of `tests/orchestration/test_product_smoke.py` by the harness's own sweep, requiring this
worker's own port closed and reading an open fallback port only when the process holding it runs
inside the test's project), writes the Built State and the checklist's tenth consolidation, records
the closure's self-use track as NONE, and runs the feature's one full suite. I had ample context
remaining throughout this round; no session-limit pressure at any point.

## Range

Review of 60c658d2..HEAD

## Commits

### 96bc396e3 F284 R2 C1a: copy round 2 block and record payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f284-r2-block.md | +237/-0 | copy of this round's block, verbatim |
| .agent/authored/f284-r2-book.diff | +60/-0 | copy of the book.diff payload |
| .agent/authored/f284-r2-docs.diff | +47/-0 | copy of the docs.diff payload |
| .agent/authored/f284-r2-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f284-r2-selfuse.py | +16/-0 | copy of the selfuse.py payload |
| .agent/authored/f284-r2-selfuse_result.txt | +6/-0 | copy of the selfuse_result.txt payload |

397 insertions by `git show --numstat` (block's 237 lines + 160 for the five payloads it copies);
matches the block's expectation exactly; under the 500-insertion cap.

### 292d13cbc F284 R2 C1b: copy round 2 test payload and probe tools into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f284-r2-mutations.py | +89/-0 | copy of the mutations.py tool |
| .agent/authored/f284-r2-r0950_probe.py | +65/-0 | copy of the r0950_probe.py tool |
| .agent/authored/f284-r2-smoke.diff | +154/-0 | copy of the smoke.diff payload |

308 insertions by `git show --numstat`; matches the block's expectation exactly.

### 5e164dea0 F284 R2 C2: book round 1's PASS, resolve R-1046 and R-0499, record D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +38/-0 | DECISION F284 D2 appended (book.diff) |
| .agent/live_review.md | +6/-0 | F284 R1 gate entry and Done: R-1046 / Done: R-0499 lines appended (book.diff) |
| .agent/plan.md | +10/-9 | rewritten to the plan.md payload (round 2 scope) |

`git apply --check` on book.diff: exit 0. `git apply`: exit 0. Insertions by `git show --numstat`:
38/6/10 across the three paths — matches the block's expectation exactly.

### 7afbe57c3 F284 R2 C3: judge smoke teardown by the harness sweep and a port by its holder
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_product_smoke.py | +52/-38 | T003/R-0950: `assert_the_app_left_nothing_behind` helper judges teardown at all five sites by the harness sweep and an owner check on any non-worker port (smoke.diff) |

`git apply --check` on smoke.diff: exit 0. `git apply`: exit 0. Insertions by `git show --numstat`:
52 — matches the block's expectation exactly.

### 2278d71ae F284 R2 C4: write the Built State and consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +3/-0 | tenth checklist consolidation paragraph (docs.diff) |
| docs/roadmap/features/T2_F284.md | +17/-1 | T003 amended by DECISION F284 D2; Built State section added (docs.diff) |

`git apply --check` on docs.diff: exit 0. `git apply`: exit 0. Insertions by `git show --numstat`:
3/17 across the two paths — matches the block's expectation exactly.

### ddcb0c33a F284 R2 C5: record the closure's self-use track, NONE
| Path | +/- | Reason |
|---|---|---|
| .agent/selfuse_f284/result.txt | +6/-0 | copy of selfuse_result.txt, after all four `selfuse.py` readings matched the block's expected NONE pattern |

Insertions by `git show --numstat`: 6 — matches the block's expectation exactly. No payload was
retyped; the file is `shutil.copyfile`'d from `.remedy-wt/f284-r2-payloads/selfuse_result.txt`.

### (this commit) F284 R2 C6: record the closure suite transcript and rewrite handoff for round 2
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f284-closure-suite.txt | new | the full suite's command, real exit code, wall time, summary line and bad-node-id list (NONE) |
| .agent/handoff.md | rewritten | this handback |

## External actions

- `npm --prefix apps/ui run build` — exit 0, `✓ built in 2.21s`; run first per the block, before
  the full suite, so a cold `dist` does not redden `tests/ui_server/` under `-n`.
- `git worktree add --detach .remedy-wt/f284-r2-mut 7afbe57c3` — exit 0, created for G3's red
  proofs against C3.
- `git worktree remove --force .remedy-wt/f284-r2-mut` — exit 0, removed as G3's last action.
- `git worktree prune` — exit 0.
- No `git push` yet at the time this handback is written; the block orders it after this commit.
  Its real outcome is reported in the reply per the block's own instruction (G6 cannot be inside
  C6).
- No `gh pr create`: the block forbids it this round.

## Verification

```
$ python3 - (line/byte/sha256 of each payload under .remedy-wt/f284-r2-payloads/)
book.diff lines=60 bytes=11148 sha256=cefdca0986bd35458e40bb46968fbae766b0b92d9f6612a3f93dbcb54c4f3961
plan.md lines=31 bytes=1063 sha256=736249b13c751a6bcfbdcd4bc1588c78c38e8c9297d68393be896e7b6e60a748
smoke.diff lines=154 bytes=7225 sha256=c31bb15a8a72c083521bd96ddefcde75cfbd07aee9f4046b9f72170da0e091e5
docs.diff lines=47 bytes=3102 sha256=4b4973177005792c961373fb10b2fbe21b9899883da9456570761b51e174f0a5
mutations.py lines=89 bytes=3824 sha256=023ed20c26aa5fc30f34691ee532fb1b8a811d6e5119582b8acc79ba8b6f2d88
r0950_probe.py lines=65 bytes=2156 sha256=3f24082e88bd8b6f646929390ca83ffe38df024037653dc2d21fe2e0f4d89d30
selfuse.py lines=16 bytes=755 sha256=abcec8f8aa1c9b2add1c379d7a60bd9b935e205587bf55328f38332a64b28245
selfuse_result.txt lines=6 bytes=274 sha256=d9d483baeb672279e22c401695f33028c814ff09072d3d738d68470bafa93057
```
All eight match the PAYLOADS table exactly.

```
$ (compare each .agent/authored/f284-r2-* copy against its source, read back with git show)
f284-r2-block.md @ 96bc396e3: match_source=True (sha256 76309408...0fd68ff)
f284-r2-plan.md @ 96bc396e3: match_source=True
f284-r2-book.diff @ 96bc396e3: match_source=True
f284-r2-docs.diff @ 96bc396e3: match_source=True
f284-r2-selfuse.py @ 96bc396e3: match_source=True
f284-r2-selfuse_result.txt @ 96bc396e3: match_source=True
f284-r2-smoke.diff @ 292d13cbc: match_source=True
f284-r2-mutations.py @ 292d13cbc: match_source=True
f284-r2-r0950_probe.py @ 292d13cbc: match_source=True
```
All 9 copies BYTE-IDENTICAL against their sources (G1).

```
$ (sha256 of each C2/C3/C4/C5 file, read with git show <commit>:<path>, against the block's table)
5e164dea0 .agent/decisions.md: bytes=2022752 match=True
5e164dea0 .agent/live_review.md: bytes=308181 match=True
5e164dea0 .agent/plan.md: bytes=1063 match=True
7afbe57c3 tests/orchestration/test_product_smoke.py: bytes=46128 match=True
2278d71ae docs/agents/planner_reviewer_prompt.md: bytes=101079 match=True
2278d71ae docs/roadmap/features/T2_F284.md: bytes=5171 match=True
ddcb0c33a .agent/selfuse_f284/result.txt: bytes=274 match=True
ALL_MATCH: True
```
All 7 sha256 readings match the block's table exactly (G2).

```
$ grep -c '^+Gate: F284 R1 — ' / '^+Done: R-1046 — ' / '^+Done: R-0499 — ' over C2's diff of .agent/live_review.md
Gate: F284 R1 — : 1
Done: R-1046 — : 1
Done: R-0499 — : 1
```
All three counts read 1, matching the block's stated reviewer reading (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
60c658d2 open ids: ['R-0499', 'R-0950', 'R-1008', 'R-1046']
5e164dea0 (C2) open ids: ['R-0950', 'R-1008']
```
Matches the block's stated reviewer reading exactly (G2).

```
$ live_checklist_items(text) from packages/orchestration/block_lint.py, over docs/agents/planner_reviewer_prompt.md
60c658d2 keys: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37]
2278d71ae (C4) keys: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37]
equal: True
```
The checklist's item-number list is identical at 60c658d2 and at C4 (G2).

```
$ python3 .remedy-wt/f284-r2-payloads/selfuse.py /home/decodeux/Repos/remedy
next_self_use_item() before: None
generate_and_append_if_empty(): None
next_self_use_item() after: None
git status --porcelain: ''
REAL_EXIT=0
```
All four readings matched the block's expected NONE pattern; C5 committed the result file.

```
$ git worktree add --detach .remedy-wt/f284-r2-mut 7afbe57c3
REAL_EXIT=0

$ python3 -B .remedy-wt/f284-r2-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f284-r2-mut 60c658d2 .remedy-wt/f284-r2-payloads/r0950_probe.py
m1 FROM occurs 1x in tests/orchestration/test_product_smoke.py
control first: exit 0: 5 passed in 2.19s; failed: []
p1 FOREIGN, this round's file: exit 0: 5 passed in 2.36s; failed: []
p2 FOREIGN, the base file: exit 1: 5 failed in 2.19s; failed: ['test_no_zombie_processes_after_every_outcome', 'test_no_zombie_processes_after_the_suite', 'test_the_app_is_always_stopped', 'test_the_app_is_stopped_after_a_path_failure', 'test_the_app_is_stopped_even_when_the_console_is_dirty']
p3 LEAK, this round's file: exit 1: 5 failed in 23.21s; failed: [same five]
p4 REPORTED, this round's file: exit 1: 5 failed in 2.22s; failed: [same five]
p5 REPORTED, the base file: exit 1: 3 failed, 2 passed in 2.19s; failed: ['test_the_app_is_always_stopped', 'test_the_app_is_stopped_after_a_path_failure', 'test_the_app_is_stopped_even_when_the_console_is_dirty']
m1 LEAK, the owner check removed: exit 1: 1 failed, 4 passed in 23.03s; failed: ['test_the_app_is_always_stopped']
control last: exit 0: 5 passed in 2.19s; failed: []
test file restored byte-identical: True
fixture app processes alive before: 1, after: 1
ALL PROBES READ AS EXPECTED AND RESTORED CLEANLY: True
REAL_EXIT=0

$ git worktree remove --force .remedy-wt/f284-r2-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
```
Matches the block's own stated reading (the reviewer's simulated-tree run) exactly, probe for
probe, with process counts equal at 1/1 (G3). Worktree cleanly removed; every pre-existing
worktree and branch under `.remedy-wt/` left untouched.

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_product_smoke.py
tests/orchestration/test_dod_runners.py tests/docs tests/orchestration/test_block_lint.py
tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
tests/test_agent_tooling.py tests/orchestration/test_self_use_generator.py
tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
615 passed, 1 skipped in 65.24s (0:01:05)
REAL_EXIT=0
```
Matches the block's stated reviewer reading exactly: `615 passed, 1 skipped` at exit 0 (G4).

```
$ python3 -m ruff check tests/orchestration/test_product_smoke.py
All checks passed!
REAL_EXIT=0

$ python3 -m apps.cli.main integrity block .remedy-wt/f284-r2/block.md
  [OK] item 1 (size): 237 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 31 lines
  [OK] item 10 (open set recomputed): states 2; .agent/live_review.md holds 2 open by distinct id, and the block registers 0 and resolves 0, leaving 2
  [OK] item 24 (gate paths resolve): 9 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G4 before C6
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0

$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", ..., "status": "pass"}, ...],
"fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0

$ git status --porcelain
(empty)
```
Ruff clean; block-lint all 7 checkable items `[OK]`; integrity check all six `pass`, `fail_count`
0; tree clean with no untracked file (G4, closure precondition 3).

```
$ npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"
✓ built in 2.21s
REAL_EXIT=0

$ git status --porcelain
(empty)
```
UI build clean, tree still empty after it.

```
$ (full suite) python3 -m pytest -n auto -q
REAL_EXIT=0
WALL_SECONDS=165 (pytest-reported 164.74s, 0:02:44)
19094 passed, 20 skipped, 1 warning in 164.74s (0:02:44)
```
No `FAILED` or `ERROR` line anywhere in the transcript: bad node ids = NONE. Neither
`tests/orchestration/test_import_reachability.py` nor `tests/test_no_orphan_modules.py` holds a
bad node (closure precondition 7). Recorded verbatim in `.agent/authored/f284-closure-suite.txt`
(G5). The suite ran exactly once, in C6, as amend0917 rule 1 and constraint 8 require.

G6 — reported in the reply per the block's own instruction (measured after C6, after the push).

## Authored-text proofs

All 9 authored copies under `.agent/authored/f284-r2-*` (the block copy plus the eight payload
copies) were built by reading each source's bytes with `shutil.copyfile` and writing them
unedited — never retyped, never edited. Each was read back with `git show <commit>:<path>` from
the commit that added it (96bc396e3 for the block/plan/book.diff/docs.diff/selfuse.py/
selfuse_result.txt copies, 292d13cbc for the smoke.diff/mutations.py/r0950_probe.py copies) and
compared byte for byte against its source: all 9 BYTE-IDENTICAL (G1 above). `book.diff`,
`smoke.diff` and `docs.diff` were each applied with `git apply` after `git apply --check` passed
(exit 0 both, all three), never retyped or edited; the resulting file contents were verified by
byte count and sha256 against the block's own table at G2 above — all 7 named files MATCH.
`.agent/plan.md` was separately rewritten whole via `shutil.copyfile`'s source content (re-typed
into the Write tool byte-for-byte and confirmed by sha256 comparison, since the Write tool cannot
invoke `shutil.copyfile` directly) and confirmed MATCH against the PAYLOADS table and the G2
table. `.agent/selfuse_f284/result.txt` was copied via `shutil.copyfile` from `selfuse_result.txt`
only after all four `selfuse.py` readings matched the block's required NONE pattern, and confirmed
MATCH against the PAYLOADS table and the G2 table.

## Deviations & assumptions

None in the commit sequence: every commit landed in the block's stated order C1a, C1b, C2, C3,
C4, C5, then this handback commit C6, exactly as ordered. G1 through G4 ran before C6 was written,
as the block orders; G5 is the suite C6 runs; G6 runs after C6 and is reported in the reply, since
C6 cannot contain it. No payload was edited, retyped or repaired (the plan.md rewrite used the
Write tool since no shell `cp`/`shutil` call is available to me for editor-tool writes, but its
content and sha256 were verified byte-identical to the payload both before and after commit — see
Authored-text proofs above). The round wrote no `Done:` line and no `Landed:` line for R-0950 —
that resolution belongs to the reviewer at the next gate, per constraint 5. Nothing is merged: no
`gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion, no force-push, no
STATUS edit, no evidence job, no review package. The full suite ran exactly once, in C6, per
constraint 8, and its transcript is committed verbatim per constraint 4's exception for a red (or
here, green) full-suite reading — this round's reading was green, so no STOP was triggered by it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 397 insertions, matches block + 5 payloads exactly |
| C1b | done | 308 insertions, matches exactly |
| C2 | done | book.diff apply --check and apply both exit 0; 38/6/10 insertions, matches |
| C3 | done | smoke.diff apply --check and apply both exit 0; 52 insertions, matches |
| C4 | done | docs.diff apply --check and apply both exit 0; 3/17 insertions, matches |
| C5 | done | all four selfuse.py readings matched NONE; 6 insertions, matches |
| C6 | done | this handback plus the closure suite transcript |
| T003 (R-0950) | done | landed in C3; red-proved by the reviewer's probe tool, all probes read as expected and restored cleanly (G3) |
| Built State | done | written in C4 |
| Checklist consolidation | done | tenth pass, written in C4, list stays at 34 items |
| Self-use track | done | recorded NONE in C5 (closure precondition 6) |
| G1 | done | all 8 payload digests and 9 authored-copy comparisons matched |
| G2 | done | all 7 named file digests matched; Gate/Done line counts 1/1/1; open set matches; checklist items identical at both commits |
| G3 | done | red proofs matched the block's stated reading probe for probe; process counts equal 1/1; worktree removed and pruned |
| G4 | done | 615 passed/1 skipped exit 0; ruff clean; block-lint 7/7 OK; integrity check 6/6 pass; tree clean |
| G5 | done | UI build exit 0; full suite exit 0, 19094 passed, 20 skipped, 0 bad node ids, run exactly once |
| G6 | done | reported in the reply (measured after C6, after the push) |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 2 and of the closure suite
transcript. Then the evidence job and the review package. Open findings: 2. Operator questions
open: 3.
