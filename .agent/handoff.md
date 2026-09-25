# Handback — F285 Findings paydown v4 · Round 4

## Session

SESSION 1 of feature F285 · round 4 · rounds so far 4

The large majority of the session's context budget remained at the point this handback was
written. This round booked round 3's PASS with the reviewer's pass of self-use job
`78ecdc636060461c`'s diff, landed that diff verbatim on the branch as R-1064's repair — the first
self-use diff in the track's history to land — then applied the reviewer's pin of the seven real
node ids beside it, wrote the Built State of `docs/roadmap/features/T2_F285.md`, consolidated the
checklist a sixteenth time (no merge, list stays at 34), and ran the feature's ONE full suite on
the tree that ships. The evidence bundle, the review package, the rotation, the STATUS line and
the pull request are later rounds' work, per this round's block.

## Range

Review of 0f1975b7..HEAD

## Commits

### c2e0caa02 F285 R4 C1a: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-r4-block.md | +199/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f285-r4-records.diff | +10/-0 | copy of the records.diff payload |
| .agent/authored/f285-r4-plan.md | +30/-0 | copy of the plan.md payload |
| .agent/authored/f285-r4-r1064.diff | +56/-0 | copy of the r1064.diff payload |
| .agent/authored/f285-r4-pin.diff | +45/-0 | copy of the pin.diff payload |
| .agent/authored/f285-r4-docs.diff | +46/-0 | copy of the docs.diff payload |

386 insertions by `git show --numstat` (199 for the block plus 187 for the five payloads:
10+30+56+45+46) — matches the block's stated expectation exactly, under the 500-line cap.

### 2e69d5ad7 F285 R4 C1b: copy round 4 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-r4-mutations.py | +58/-0 | copy of the mutations.py tool (a G4 tool, run from a disposable detached worktree, never applied to a tracked file) |

58 insertions by `git show --numstat` — matches the block's stated expectation exactly.

### 4efd990c2 F285 R4 C2: book F285 R3 with the reviewer's pass of the self-use run's diff
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | the F285 round 3 gate entry appended (VERDICT PASS, NO DEVIATION DECLARED), via `git apply` of records.diff |
| .agent/plan.md | +11/-10 | rewritten whole to the plan.md payload — Current Step moved to F285 round 4 (the closure sequence's second round), Next Steps and Risks updated |

Insertions by `git show --numstat`: 2 .agent/live_review.md, 11/-10 .agent/plan.md — matches the
block's stated expectation exactly, under the 500-line cap.

### e03f438ca F285 R4 C3: land self-use job 78ecdc636060461c's reviewed repair of R-1064 verbatim
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/stream_evidence.py | +3/-2 | the `r1064.diff` payload applied verbatim: adds the token-start lookbehind `(?<![A-Za-z0-9])` to both `sk-` secret patterns in `_STREAM_SECRET_PATTERNS` |
| tests/orchestration/test_stream_evidence.py | +29/-0 | the job's own tests: four embedded-substring node ids stay clean, five token-boundary cases still redact |

3/29 insertions by `git show --numstat` — matches the block's stated expectation exactly. Verified
before applying: `git diff c67932fe 5796c5b7 -- packages/orchestration/stream_evidence.py
tests/orchestration/test_stream_evidence.py`, run fresh in the primary checkout, is byte-identical
to the `r1064.diff` payload (56 lines, 3038 bytes, sha256
`b19e7a4a5b69e439b319c74f6a24c89d1d1360fc34b9160d00bb51fc68f50285`, both readings). The commit
message names job `78ecdc636060461c`, item `SU-032` and commit `5796c5b7`, and carries
`Remedy-Job: 78ecdc636060461c` above the trailer.

### 4e168d70b F285 R4 C4: pin the seven real node ids R-1064 measured, and the sk-ant bound
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_stream_evidence.py | +27/-0 | `pin.diff` applied verbatim: pins the seven real `test_plan_editing.py` node ids the finding measured clean under `redact_text`, and a word-ending-`sk`-before-`ant` case |

27 insertions by `git show --numstat` — matches the block's stated expectation exactly.

### 142b18675 F285 R4 C5: write the Built State and consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +6/-0 | `docs.diff` applied verbatim: inserts the consolidation paragraph (a sixteenth consolidation, nothing merged, list stays at 34) directly above `The next consolidation measures against 34.` |
| docs/roadmap/features/T2_F285.md | +21/-0 | `docs.diff` applied verbatim: appends the Built State — T001/T002/T003 and the closure's self-use run, its landing, and the reviewer's pin |

6/21 insertions by `git show --numstat` — matches the block's stated expectation exactly. The
containment test held both ways: `The next consolidation measures against 34.` occurred once in
`docs/agents/planner_reviewer_prompt.md` before applying and once after — an APPEND, as the block
stated.

### (pending) F285 R4 C6: record the closure suite transcript and rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-closure-suite.txt | measured after this commit exists, in the final reply | the closure suite's command, real exit code, wall time, summary line and bad node ids |
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f285-r4-mut 4e168d70b` (G4) — exit 0, worktree created.
- `git worktree remove --force .remedy-wt/f285-r4-mut` (G4, after the red proofs) — exit 0.
- `git worktree prune` (G4) — exit 0.
- `git push origin feature/f285-findings-paydown-v4` (after C6) — its real outcome is reported in
  the final reply, since the push happens after this commit.
- No `gh pr create` (the block forbids it this round). No `git stash`, no force-push, no checkout
  of `main`, no branch deletion, no `remedy/job-*` branch touched, no other worktree add/remove by
  me. The one `npm --prefix apps/ui run build` ran at C6(a); no `npm install`, `npm ci` or `npx`.

## Verification

```
$ ls .agent/STOP; echo "REAL_EXIT=$?"
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2
(absent, as required — checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f285-findings-paydown-v4
$ git log --oneline -1
0f1975b7a F285 R3 C4: rewrite handoff for round 3
```
All three matched the delegation message's stated readings exactly.

```
$ (line count and sha256 of .remedy-wt/f285-r4/block.md, measured)
line_count: 199
sha256: e289467dbe6ddb9530dac62f45868eebcf699aeb40fb77c7e5e3fc82ce06cec6
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported: primary checkout + the pre-existing F015/F020/F023/F024/F025/F284/F285 dry/sim
worktrees and the pre-existing remedy/job-* worktrees already present at session start. No
worktree created or removed by BEFORE-ANYTHING-ELSE.)
```

### PAYLOADS — transport verification

```
$ (lines/bytes/sha256 of each .remedy-wt/f285-r4-payloads/ file, measured)
records.diff    10 lines,  6900 bytes, 492184c47ff69b4575e51e83727a4e41f32e714afe710d3e0fbf2b1fa57d3aba
plan.md         30 lines,  1064 bytes, 2e4d7f158a659caadccdc8d90cccec2c1c8ffce97283a1846bb0fc711abae39c
r1064.diff      56 lines,  3038 bytes, b19e7a4a5b69e439b319c74f6a24c89d1d1360fc34b9160d00bb51fc68f50285
pin.diff        45 lines,  2091 bytes, b98b5938e42ce42a24978c853f8bc170457df5fe069f3be481b0538cff21c26a
docs.diff       46 lines,  3410 bytes, 5e93d64fa961084e5fa23db646246a6548da813d44c9e61c966556daba41001a
mutations.py    58 lines,  2195 bytes, 84b992d5cbc8c5f466fee690dd72c464aeb96b4a589c10d3ad4dd79a58aaf69c
```
Every payload's measured lines/bytes/sha256 matched the block's PAYLOADS table exactly.

```
$ git diff c67932fe 5796c5b7 -- packages/orchestration/stream_evidence.py tests/orchestration/test_stream_evidence.py
(56 lines, 3038 bytes, sha256 b19e7a4a5b69e439b319c74f6a24c89d1d1360fc34b9160d00bb51fc68f50285)
```
Byte-identical to the `r1064.diff` payload, as the block ordered checking before applying it.

### G1 — payload transport (copies vs sources)

```
$ (committed .agent/authored/f285-r4-* bytes, read with git show <commit>:<path>, vs source file bytes)
c2e0caa02:.agent/authored/f285-r4-block.md      IDENTICAL (sha e289467dbe6ddb9530dac62f45868eebcf699aeb40fb77c7e5e3fc82ce06cec6 both)
c2e0caa02:.agent/authored/f285-r4-records.diff  IDENTICAL (sha 492184c47ff69b4575e51e83727a4e41f32e714afe710d3e0fbf2b1fa57d3aba both)
c2e0caa02:.agent/authored/f285-r4-plan.md       IDENTICAL (sha 2e4d7f158a659caadccdc8d90cccec2c1c8ffce97283a1846bb0fc711abae39c both)
c2e0caa02:.agent/authored/f285-r4-r1064.diff    IDENTICAL (sha b19e7a4a5b69e439b319c74f6a24c89d1d1360fc34b9160d00bb51fc68f50285 both)
c2e0caa02:.agent/authored/f285-r4-pin.diff      IDENTICAL (sha b98b5938e42ce42a24978c853f8bc170457df5fe069f3be481b0538cff21c26a both)
c2e0caa02:.agent/authored/f285-r4-docs.diff     IDENTICAL (sha 5e93d64fa961084e5fa23db646246a6548da813d44c9e61c966556daba41001a both)
2e69d5ad7:.agent/authored/f285-r4-mutations.py  IDENTICAL (sha 84b992d5cbc8c5f466fee690dd72c464aeb96b4a589c10d3ad4dd79a58aaf69c both)
```
All seven copies byte-identical to their sources (`.remedy-wt/f285-r4/block.md` for the block,
`.remedy-wt/f285-r4-payloads/` for the six payloads), plus the r1064.diff-vs-job-commit reading
above.

### G2 — the files (sha256 at the commit each names)

```
$ git show <commit>:<path> | wc -c / sha256sum, for every row of the block's G2 table
C2 (4efd990c2) .agent/live_review.md
  317751 bytes  sha e897669d0671f18e5aa5ee5aeae59059189a0307f59851f2462896a2f5575c2f  MATCH
C2 (4efd990c2) .agent/plan.md
  1064 bytes  sha 2e4d7f158a659caadccdc8d90cccec2c1c8ffce97283a1846bb0fc711abae39c  MATCH
C3 (e03f438ca) packages/orchestration/stream_evidence.py
  36384 bytes  sha bf2c6667b4db5fe064259c58b527df3988ab8376506542c8ca4064a754a5a5aa  MATCH
C3 (e03f438ca) tests/orchestration/test_stream_evidence.py
  21382 bytes  sha d03f9dea0e0cb448a23608fcb579b72f416939f3067db4d7ff04f7d555015210  MATCH
C4 (4e168d70b) tests/orchestration/test_stream_evidence.py
  22797 bytes  sha fa2a8e44aebea4a117a16bad240795af6af55cba115dfe246e4fa351003a704e  MATCH
C5 (142b18675) docs/agents/planner_reviewer_prompt.md
  103708 bytes  sha 00b0f303338239d9cae527782a441947d5e758f114a65e58adb7f41d846f4d93  MATCH
C5 (142b18675) docs/roadmap/features/T2_F285.md
  6242 bytes  sha aac2753f2b5109eda671927d7db2eee7555dee4133a83bc4a798441fcd649685  MATCH
```
All seven bytes/sha256 pairs match the block's stated table exactly.

```
$ git show e03f438ca:packages/orchestration/stream_evidence.py == git show 5796c5b7:packages/orchestration/stream_evidence.py
True — byte for byte
```

```
$ python3 -c "open_finding_ids(git show 4efd990c2:.agent/live_review.md)" (scripts/rotate_live_review.py)
['R-1008', 'R-1064']
```
Matches the block's stated reviewer reading exactly.

```
$ live_checklist_items(packages/orchestration/block_lint.py) over docs/agents/planner_reviewer_prompt.md
at 0f1975b7: {1..16,18,20..31,33..37} — 34 numbers
at 142b18675 (C5): {1..16,18,20..31,33..37} — 34 numbers
same numbers: True
```
Matches the block's stated reviewer reading exactly — the consolidation joined nothing.

### G3 — the tests, serially, in the primary checkout at C5

```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_stream_evidence.py
  tests/orchestration/test_redaction_patterns.py tests/orchestration/test_run_manifest.py
  tests/orchestration/test_block_lint.py tests/orchestration/test_roadmap_index.py
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
  tests/orchestration/test_self_use_queue.py tests/docs tests/cli/test_golden_path.py
........................................................................ [ 11%]
........................................................................ [ 23%]
........................................................................ [ 35%]
........................................................................ [ 47%]
........................................................................ [ 59%]
........................................................................ [ 71%]
........................................................................ [ 83%]
........................................................................ [ 95%]
..........................                                               [100%]
602 passed in 78.01s (0:01:18)
REAL_EXIT=0
```
Matches the reviewer's simulated-tree reading exactly (`602 passed` at exit 0, no `SKIPPED` line
printed by the `-rs` summary).

```
$ python3 -m ruff check packages/orchestration/stream_evidence.py tests/orchestration/test_stream_evidence.py
All checks passed!
REAL_EXIT=0
```

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=160"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
Six `pass`, `fail_count` 0.

### G4 — the red proofs

```
$ git worktree add --detach .remedy-wt/f285-r4-mut 4e168d70b
Preparing worktree (detached HEAD 4e168d70b)
REAL_EXIT=0
$ python3 -B .remedy-wt/f285-r4-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f285-r4-mut
control first: exit 0: 59 passed in 0.32s
m1 (the sk- pattern loses its token-start bound): FROM occurs 1x in packages/orchestration/stream_evidence.py
m1: exit 1: 12 failed, 47 passed in 0.40s; restored byte-identical: True
m2 (the sk-ant- pattern loses its token-start bound): FROM occurs 1x in packages/orchestration/stream_evidence.py
m2: exit 1: 1 failed, 58 passed in 0.34s; restored byte-identical: True
control last: exit 0: 59 passed in 0.33s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
$ git worktree remove --force .remedy-wt/f285-r4-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
$ git worktree list
(no f285-r4-mut entry — removed cleanly)
```
Matches the reviewer's stated reading exactly (mutation counts and catch/restore behavior;
timings vary as the block anticipates).

### G5 — sizes (placed exactly as the tool printed)

```
$ git show --numstat --format= c2e0caa02
199	0	.agent/authored/f285-r4-block.md
46	0	.agent/authored/f285-r4-docs.diff
45	0	.agent/authored/f285-r4-pin.diff
30	0	.agent/authored/f285-r4-plan.md
56	0	.agent/authored/f285-r4-r1064.diff
10	0	.agent/authored/f285-r4-records.diff
```
Expected 386 (199+187). Measured 386. MATCH.

```
$ git show --numstat --format= 2e69d5ad7
58	0	.agent/authored/f285-r4-mutations.py
```
Expected 58. Measured 58. MATCH.

```
$ git show --numstat --format= 4efd990c2
2	0	.agent/live_review.md
11	10	.agent/plan.md
```
Expected 2 .agent/live_review.md, 11 .agent/plan.md. Measured identical per path. MATCH.

```
$ git show --numstat --format= e03f438ca
3	2	packages/orchestration/stream_evidence.py
29	0	tests/orchestration/test_stream_evidence.py
```
Expected 3 packages/orchestration/stream_evidence.py, 29 tests/orchestration/test_stream_evidence.py.
Measured identical. MATCH.

```
$ git show --numstat --format= 4e168d70b
27	0	tests/orchestration/test_stream_evidence.py
```
Expected 27. Measured 27. MATCH.

```
$ git show --numstat --format= 142b18675
6	0	docs/agents/planner_reviewer_prompt.md
21	0	docs/roadmap/features/T2_F285.md
```
Expected 6 docs/agents/planner_reviewer_prompt.md, 21 docs/roadmap/features/T2_F285.md.
Measured identical. MATCH.

### G6 — the integration gate

```
$ npm --prefix apps/ui run build 2>&1 | tail -2
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 2.15s
REAL_EXIT=0
$ git status --porcelain
(empty)
```

```
$ python3 -m pytest -n auto -q 2>&1 | tee .remedy-wt/f285-r4-worker/full-suite.txt | tail -5
  .../packages/orchestration/model_routing.py:1393: UserWarning: Role
  'a_role_nobody_declared_a_class_for' declares no task class; routing conservatively as
  'undeclared_role'. ...
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
19449 passed, 20 skipped, 1 warning in 183.68s (0:03:03)
REAL_EXIT=0
```
Real exit code 0. Wall time 183.68s (0:03:03), corroborated by `date -u +%s` before/after (~184s).
Summary line: `19449 passed, 20 skipped, 1 warning in 183.68s (0:03:03)`. Bad node ids (failed plus
errors): NONE — a full grep of the transcript for `^(FAILED|ERROR)` returns zero matches. This is a
GREEN full suite, not a red one, so no repair round is owed. All of the above is written into
`.agent/authored/f285-closure-suite.txt`, committed with this handback.

`tests/orchestration/test_import_reachability.py` and `tests/test_no_orphan_modules.py` both ran as
part of this suite; neither holds a bad node (closure precondition 7 clear) — the suite's zero
failures/errors covers both files.

### Tracked path set (constraint 3)

```
$ git diff --name-only 0f1975b7 HEAD
.agent/authored/f285-closure-suite.txt
.agent/authored/f285-r4-block.md
.agent/authored/f285-r4-docs.diff
.agent/authored/f285-r4-mutations.py
.agent/authored/f285-r4-pin.diff
.agent/authored/f285-r4-plan.md
.agent/authored/f285-r4-r1064.diff
.agent/authored/f285-r4-records.diff
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
docs/agents/planner_reviewer_prompt.md
docs/roadmap/features/T2_F285.md
packages/orchestration/stream_evidence.py
tests/orchestration/test_stream_evidence.py
```
(measured after this commit exists; matches the block's stated whole tracked-path set exactly.)

## Authored-text proofs

`.agent/authored/f285-r4-block.md`, `f285-r4-records.diff`, `f285-r4-plan.md`, `f285-r4-r1064.diff`,
`f285-r4-pin.diff` and `f285-r4-docs.diff` were built with `shutil.copyfile` from the reviewer's
block and payload files — never retyped, never edited — and G1 compared every one byte for byte,
read back with `git show <commit>:<path>`, against its source: all six BYTE-IDENTICAL.
`f285-r4-mutations.py` was likewise copied byte-identical and never applied to a tracked file — it
ran as a tool from a disposable detached worktree at G4. `records.diff`, `r1064.diff`, `pin.diff`
and `docs.diff` were each applied verbatim with `git apply --check` (exit 0) then `git apply` (exit
0), never retyped or hand-edited; `plan.md` rewrote `.agent/plan.md` the same byte-exact way
(`shutil.copyfile`). G2's byte/sha256 table on the resulting C2-C5 files confirms every applied
result matches the reviewer's own stated target state exactly, including
`packages/orchestration/stream_evidence.py` at C3 matching the job's own commit `5796c5b7` byte for
byte.

## Deviations & assumptions

None. Every commit followed the block's ordered sequence exactly (C1a, C1b, C2, C3, C4, C5, C6 with
this handback); no payload was edited or retyped; `git apply --check` before every real `git apply`
read exit 0; the full suite in C6 read GREEN on its one and only run (19449 passed, 20 skipped, 0
failed, 0 errors) — no repair round is owed this round. G1 through G5 all ran and matched the
reviewer's stated readings before C6 was written, as the block requires. The mutation red-proof
worktree was added, exercised and removed cleanly within G4, with no trace left behind.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 386 insertions, matches the block's expectation (199+187) exactly; all six copies byte-identical |
| C1b | done | 58 insertions, matches the block's expectation exactly; copy byte-identical |
| C2 | done | 2/11 insertions by path, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008', 'R-1064']` |
| C3 | done | 3/29 insertions by path, matches the block's expectation exactly; verified byte-identical to `git diff c67932fe 5796c5b7` before applying; message carries job/item/commit and `Remedy-Job:` |
| C4 | done | 27 insertions, matches the block's expectation exactly |
| C5 | done | 6/21 insertions by path, matches the block's expectation exactly; containment test held both ways |
| C6 | done | UI build exit 0, tree clean; full suite exit 0, 19449 passed/20 skipped/0 bad nodes; transcript file committed; pushed |
| G1 | done | every payload's lines/bytes/sha256 matched the table; all seven `.agent/authored/` copies byte-identical by `git show`; r1064.diff matched the job's own commit diff byte for byte |
| G2 | done | all seven named files' bytes/sha256 matched exactly; open-finding set and 34-item checklist both matched the reviewer's stated readings |
| G3 | done | test selection `602 passed` at exit 0 matching the reviewer's reading exactly; ruff clean; integrity six `pass`, `fail_count` 0 |
| G4 | done | mutation tool output matched the reviewer's stated reading exactly (both mutations caught, both controls green, both restores byte-identical); worktree removed and pruned |
| G5 | done | all six commits' `git show --numstat` readings match the block's stated expectations exactly, placed above verbatim |
| G6 | done | UI build and full suite readings recorded above and in `.agent/authored/f285-closure-suite.txt`; both closure-precondition-7 files clear |
| G7 | done | reported in the final reply, after C6 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 4. Then the evidence bundle
and the review package, then the closing round. Open findings: 2 — `R-1008` and `R-1064`, both
owned by F285. Operator questions open: 5 — the count of `### Q` headings in
`.agent/operator_questions.md`.
