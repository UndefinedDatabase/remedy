# Handback — F285 Findings paydown v4 · Round 1

## Session

SESSION 1 of feature F285 · round 1 · rounds so far 1

The large majority of the session's context budget remained at the point this handback was
written. This round claimed F285, re-headed the live review record, booked F026's round 8 gate
entry, recorded DECISION F285 D1 with the slice list, and landed T001 (R-1058's repair: the
generated self-use job asks for the repair alone and `describe_self_use_run_defects` names a pass
confined to `.agent/`) and T002 (R-1057's repair: the self-use cost cap derived from the dearest
measured call, 6.00, with an operator-questions entry).

## Range

Review of 83d3bb959..HEAD

## Commits

### 054056bd9 F285 R1 C1a: copy round 1 block and claim payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-r1-block.md | +230/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f285-r1-claim.diff | +167/-0 | copy of the claim.diff payload |
| .agent/authored/f285-r1-plan.md | +30/-0 | copy of the plan.md payload |
| .agent/authored/f285-r1-context.md | +33/-0 | copy of the context.md payload |

460 insertions by `git show --numstat` (230 for the block plus 230 for the three payloads:
167+30+33) — matches the block's stated expectation exactly, under the 500-line cap.

### 53c3dea42 F285 R1 C1b: copy round 1 T001 payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-r1-t001.diff | +235/-0 | copy of the t001.diff payload |

235 insertions — matches the block's stated expectation exactly.

### f0108824f F285 R1 C1c: copy round 1 T002 payload and mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-r1-t002.diff | +201/-0 | copy of the t002.diff payload |
| .agent/authored/f285-r1-mutations.py | +68/-0 | copy of the mutations.py tool (a G4 tool, never applied to a tracked file) |

269 insertions (68+201) — matches the block's stated expectation exactly.

### b44d7d530 F285 R1 C2: claim F285, re-head the live review record, book F026 R8, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +58/-0 | DECISION F285 D1 appended: the slice list (T001/T002/T003), R-1064 as the closure's self-use item, R-1008 carried, and the derived cost cap's reasoning |
| .agent/live_review.md | +23/-21 | re-headed from F026 to F285 (`git apply claim.diff`); Steps section rewritten to T2_F285.md's slicing; F026 R8's gate entry appended (VERDICT PASS, NO DEVIATION DECLARED) |
| .agent/plan.md | +17/-14 | rewritten whole to the plan.md payload — Current Step moved to F285 round 1 |
| .agent/context.md | +11/-17 | rewritten whole to the context.md payload — Scope, Active assumptions and Constraints re-headed to F285 |
| docs/roadmap/STATUS.md | +1/-1 | F285's line flipped `[ ]` → `[~]` |
| docs/roadmap/features/T2_F285.md | +17/-0 | the slice list written: T001/T002/T003, R-1064 as the closure item, R-1008 carried, Acceptance lines per id |

Insertions by `git show --numstat`: 11 .agent/context.md, 58 .agent/decisions.md,
23 .agent/live_review.md, 17 .agent/plan.md, 1 docs/roadmap/STATUS.md,
17 docs/roadmap/features/T2_F285.md — matches the block's stated expectation exactly, in every
row, under the 500-line cap. `open_finding_ids` over `.agent/live_review.md` reads
`['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']` at both `83d3bb959` and this commit — the
reviewer's own stated reading. `docs/roadmap/STATUS.md`'s F285 line reads in full:
`- [~] F285 — Findings paydown v4`.

### 679856147 F285 R1 C3: ask the self-use builder for the repair alone and name a pass confined to .agent/
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/self_use_findings.py | +37/-0 | `_paths_the_reviewed_work_changed` reads the job hand-off and every applied task manifest; `describe_self_use_run_defects` gains one string naming a `staged_review_passed` task whose reviewed work changed no path outside `.agent/` |
| packages/orchestration/self_use_generator.py | +14/-3 | the generated job's body now tells the builder to leave `.agent/` alone and make the repair `r_id`'s FIX names; the Acceptance line's "or the reviewer records why it cannot be" alternative is removed |
| tests/orchestration/test_self_use_findings.py | +63/-0 | `TestAPassConfinedToTheRecordIsNamed`: SU-030's shape (a `staged_review_passed` task whose only changed path is `.agent/live_review.md`) is named a defect; a task that also changed a path outside `.agent/` is not |
| tests/orchestration/test_self_use_generator.py | +41/-0 | pins the new job body (`.agent/` off-limits) and the new Acceptance wording; the removed "ledger note" alternative is asserted absent |

Insertions by `git show --numstat`: 37/0 self_use_findings.py, 14/3 self_use_generator.py,
63/0 test_self_use_findings.py, 41/0 test_self_use_generator.py — matches the block's stated
expectation exactly, under the 500-line cap.

### 91397285d F285 R1 C4: derive the self-use cost cap from the dearest measured call
| Path | +/- | Reason |
|---|---|---|
| .agent/operator_questions.md | +25/-0 | Q5 appended: the raised cost cap (one dollar to six dollars), why, the recommendation (already executed) and the no-answer default |
| docs/guides/environment.md | +1/-1 | `REMEDY_SELF_USE_MODEL`'s row text updated from "1.00 USD" to "6.00 USD" per closure |
| docs/system/self-use-track-v1.md | +3/-1 | the budget prose updated to 6.00 USD, with the R-1057 measurement (1.40 USD single call) named as the reason |
| packages/orchestration/config.py | +1/-1 | the `self_use.model` key's help text updated from "1.00 USD" to "6.00 USD" |
| packages/orchestration/self_use_runner.py | +25/-6 | `_MEASURED_MAX_CALL_USD` (1.41), `_COST_CAP_CALLS` (4) and the derived `_MAX_COST_USD` (6.00) replace the flat `1.00`; three docstrings updated to match |
| tests/orchestration/test_self_use_runner.py | +20/-4 | pins `max_cost_usd == 6.00`; the renamed test `test_the_call_cap_is_eight_and_the_cost_bound_six_dollars` asserts the new bound |

Insertions by `git show --numstat`: 25/0 operator_questions.md, 1/1 environment.md, 3/1
self-use-track-v1.md, 1/1 config.py, 25/6 self_use_runner.py, 20/4 test_self_use_runner.py —
matches the block's stated expectation exactly, under the 500-line cap.

### (pending) F285 R1 C5: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

## External actions

- `git checkout -b feature/f285-findings-paydown-v4` (from `main` at `83d3bb959`) — succeeded.
- `git worktree add --detach .remedy-wt/f285-r1-mut 91397285d` (for G4) — succeeded.
- `git worktree remove --force .remedy-wt/f285-r1-mut` then `git worktree prune` (after G4) —
  succeeded; `git worktree list` afterward shows no worktree this round added.
- `git push -u origin feature/f285-findings-paydown-v4` (after C5) — its real outcome is reported
  in the final reply, since the push happens after this commit.
- No `gh pr create` (the block forbids it this round — the branch opens a PR at F285's closure).
  No `git stash`, no force-push, no checkout of `main`, no branch deletion, no `remedy/job-*`
  branch created or deleted, no `npm`/`npx`.

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
main
$ git log --oneline -1
83d3bb959 Merge pull request #281 from UndefinedDatabase/feature/f026-task-edit-runtime
$ git checkout -b feature/f285-findings-paydown-v4
Switched to a new branch 'feature/f285-findings-paydown-v4'
REAL_EXIT=0
```

```
$ (line count and sha256 of .remedy-wt/f285-r1/block.md, measured)
line_count: 230
sha256: 05d8c38b539e0a1b27d14056f45f0b70c0c39fdf2907e8a3207de0dd7249043d
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported: primary checkout + the pre-existing F015/F020/F023/F024/F025/F284 dry/sim worktrees,
the reviewer's f285-r1-dry and f285-r1-sim, and the same remedy/job-* worktrees already present
at session start. No worktree created or removed by BEFORE-ANYTHING-ELSE.)
```

### PAYLOADS — transport verification

```
$ (lines/bytes/sha256 of each .remedy-wt/f285-r1-payloads/ file, measured)
claim.diff       167 lines, 16877 bytes, f095c14408968f698a63dc5ff9fe825b7a7a39bc4c04f77fa81e1d3c6e35605e
plan.md           30 lines,  1159 bytes, 7dabdb7911c5e51708d2c671ad519cfe847bd4a0526e9518f36c1416bde4b5de
context.md        33 lines,  1366 bytes, aa332a74318c443435bc3def307b77b9041b5f554f07f3be3ca5a3eec521f93d
t001.diff        235 lines, 11424 bytes, 6fcc14675a64dd073e07851688ddb9cf73ecc6cbbf166ac230df10ecae71439f
t002.diff        201 lines, 13606 bytes, ccc179ae65fa37bd2950ec2777828b58e34d58f27b9f25b40c3c99fc5633e8ea
mutations.py      68 lines,  2958 bytes, 260e14da6082685ec09cbdd3c4bca5d3d36ea91b6696d6bbc6b5e86130284450
```
Every payload's measured lines/bytes/sha256 matched the block's PAYLOADS table exactly.

### G1 — payload transport (copies vs sources)

```
$ (committed .agent/authored/f285-r1-* bytes, read with git show <commit>:<path>, vs source file bytes)
054056bd9:.agent/authored/f285-r1-block.md      MATCH (17076 bytes, sha 05d8c38b...9043d both)
054056bd9:.agent/authored/f285-r1-claim.diff    MATCH (16877 bytes, sha f095c144...605e both)
054056bd9:.agent/authored/f285-r1-plan.md       MATCH (1159 bytes, sha 7dabdb79...4b5de both)
054056bd9:.agent/authored/f285-r1-context.md    MATCH (1366 bytes, sha aa332a74...f93d both)
53c3dea42:.agent/authored/f285-r1-t001.diff     MATCH (11424 bytes, sha 6fcc1467...439f both)
f0108824f:.agent/authored/f285-r1-t002.diff     MATCH (13606 bytes, sha ccc179ae...8ea both)
f0108824f:.agent/authored/f285-r1-mutations.py  MATCH (2958 bytes, sha 260e14da...4450 both)
```
All seven copies byte-identical to their `.remedy-wt/f285-r1-payloads/` (and, for the block,
`.remedy-wt/f285-r1/`) sources.

### G2 — the claim and the code (sha256 at each named commit)

```
$ git show <commit>:<path> | sha256sum, for every row of the block's G2 table
C2 .agent/context.md                                    1366 bytes    MATCH
C2 .agent/decisions.md                                  2144886 bytes MATCH
C2 .agent/live_review.md                                307014 bytes  MATCH
C2 .agent/plan.md                                       1159 bytes    MATCH
C2 docs/roadmap/STATUS.md                                52859 bytes   MATCH
C2 docs/roadmap/features/T2_F285.md                       4593 bytes   MATCH
C3 packages/orchestration/self_use_findings.py            6133 bytes   MATCH
C3 packages/orchestration/self_use_generator.py          20406 bytes   MATCH
C3 tests/orchestration/test_self_use_findings.py          8967 bytes   MATCH
C3 tests/orchestration/test_self_use_generator.py        27998 bytes   MATCH
C4 .agent/operator_questions.md                           9169 bytes   MATCH
C4 docs/guides/environment.md                            21268 bytes   MATCH
C4 docs/system/self-use-track-v1.md                       8139 bytes   MATCH
C4 packages/orchestration/config.py                      63251 bytes   MATCH
C4 packages/orchestration/self_use_runner.py             21902 bytes   MATCH
C4 tests/orchestration/test_self_use_runner.py           28503 bytes   MATCH
```
All sixteen files' bytes and sha256 equal the block's stated table exactly.

```
$ python3 -c "open_finding_ids(git show <commit>:.agent/live_review.md)"
83d3bb959: ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']
b44d7d530 (C2): ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']
```
Matches the block's stated reviewer reading exactly, at both commits.

```
$ git show b44d7d530:docs/roadmap/STATUS.md | grep F285
- [~] F285 — Findings paydown v4
```
Reads in full exactly as the block requires.

```
$ git diff --name-only <consecutive commit pairs>
f0108824f..b44d7d530 (C1c->C2): .agent/context.md .agent/decisions.md .agent/live_review.md
  .agent/plan.md docs/roadmap/STATUS.md docs/roadmap/features/T2_F285.md
b44d7d530..679856147 (C2->C3): packages/orchestration/self_use_findings.py
  packages/orchestration/self_use_generator.py tests/orchestration/test_self_use_findings.py
  tests/orchestration/test_self_use_generator.py
679856147..91397285d (C3->C4): .agent/operator_questions.md docs/guides/environment.md
  docs/system/self-use-track-v1.md packages/orchestration/config.py
  packages/orchestration/self_use_runner.py tests/orchestration/test_self_use_runner.py
```
Each pair names exactly the paths that commit's entry in the block lists.

### G3 — the tests, at C4

```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_self_use_findings.py
  tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py
  tests/orchestration/test_self_use_queue.py tests/orchestration/test_predictive_budget.py
  tests/orchestration/test_config.py tests/orchestration/test_role_config.py
  tests/orchestration/test_development_artifact_boundary.py
  tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
  tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs
  tests/cli/test_golden_path.py
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md
  was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's
  Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives
  there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
900 passed, 1 skipped in 88.00s (0:01:28)
REAL_EXIT=0
```
Matches the reviewer's stated reading exactly: `900 passed, 1 skipped` at exit 0, with the single
`SKIPPED` line the D12 quarantine at `tests/test_agent_tooling.py:43` (timing varies with machine
load; the reviewer read 8.98s-class timings in its own simulated tree's mutation runs, not this
serial suite run, so no divergence in outcome is claimed from timing).

```
$ python3 -m ruff check packages/orchestration/self_use_findings.py
  packages/orchestration/self_use_generator.py tests/orchestration/test_self_use_findings.py
  tests/orchestration/test_self_use_generator.py packages/orchestration/config.py
  packages/orchestration/self_use_runner.py tests/orchestration/test_self_use_runner.py
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
$ git worktree add --detach .remedy-wt/f285-r1-mut 91397285d
Preparing worktree (detached HEAD 91397285d)
HEAD is now at 91397285d F285 R1 C4: derive the self-use cost cap from the dearest measured call
REAL_EXIT=0

$ python3 -B .remedy-wt/f285-r1-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f285-r1-mut
control first: exit 0: 94 passed in 10.28s
m1 (the ledger note is offered again): FROM occurs 1x in packages/orchestration/self_use_generator.py
m1: exit 1: 2 failed, 92 passed in 10.05s; restored byte-identical: True
m2 (the builder is not told to leave the record alone): FROM occurs 1x in packages/orchestration/self_use_generator.py
m2: exit 1: 1 failed, 93 passed in 10.28s; restored byte-identical: True
m3 (a pass confined to .agent/ is not named): FROM occurs 1x in packages/orchestration/self_use_findings.py
m3: exit 1: 2 failed, 92 passed in 9.68s; restored byte-identical: True
m4 (the stopped job's applied manifests are not read): FROM occurs 1x in packages/orchestration/self_use_findings.py
m4: exit 1: 3 failed, 91 passed in 8.69s; restored byte-identical: True
m5 (the cost cap is one dollar again): FROM occurs 1x in packages/orchestration/self_use_runner.py
m5: exit 1: 3 failed, 91 passed in 8.90s; restored byte-identical: True
control last: exit 0: 94 passed in 9.04s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Matches the reviewer's stated reading exactly on every occurrence count and pass/fail count
(timings vary, as the block itself notes).

```
$ git worktree remove --force .remedy-wt/f285-r1-mut; git worktree prune
REAL_EXIT=0 (both)
$ git worktree list
(no .remedy-wt/f285-r1-mut entry; only the pre-existing worktrees, including the reviewer's
read-only f285-r1-dry and f285-r1-sim, remain)
```

### G5 — sizes (placed exactly as the tool printed)

```
$ git show --numstat --format= 054056bd9
230	0	.agent/authored/f285-r1-block.md
167	0	.agent/authored/f285-r1-claim.diff
33	0	.agent/authored/f285-r1-context.md
30	0	.agent/authored/f285-r1-plan.md
```
Expected 460 (230+230). Measured 460. MATCH.

```
$ git show --numstat --format= 53c3dea42
235	0	.agent/authored/f285-r1-t001.diff
```
Expected 235. Measured 235. MATCH.

```
$ git show --numstat --format= f0108824f
68	0	.agent/authored/f285-r1-mutations.py
201	0	.agent/authored/f285-r1-t002.diff
```
Expected 269 (68+201). Measured 269. MATCH.

```
$ git show --numstat --format= b44d7d530
11	17	.agent/context.md
58	0	.agent/decisions.md
23	21	.agent/live_review.md
17	14	.agent/plan.md
1	1	docs/roadmap/STATUS.md
17	0	docs/roadmap/features/T2_F285.md
```
Expected 11/58/23/17/1/17 by path. Measured identical per path. MATCH.

```
$ git show --numstat --format= 679856147
37	0	packages/orchestration/self_use_findings.py
14	3	packages/orchestration/self_use_generator.py
63	0	tests/orchestration/test_self_use_findings.py
41	0	tests/orchestration/test_self_use_generator.py
```
Expected 37/14/63/41 by path. Measured identical per path. MATCH.

```
$ git show --numstat --format= 91397285d
25	0	.agent/operator_questions.md
1	1	docs/guides/environment.md
3	1	docs/system/self-use-track-v1.md
1	1	packages/orchestration/config.py
25	6	packages/orchestration/self_use_runner.py
20	4	tests/orchestration/test_self_use_runner.py
```
Expected 25/1/3/1/25/20 by path. Measured identical per path. MATCH.

## Authored-text proofs

`.agent/authored/f285-r1-block.md`, `f285-r1-claim.diff`, `f285-r1-plan.md`,
`f285-r1-context.md`, `f285-r1-t001.diff`, `f285-r1-t002.diff` and `f285-r1-mutations.py` were
built with `shutil.copyfile` from the reviewer's block and payload files — never retyped, never
edited — and G1 compared every one byte for byte, read back with `git show <commit>:<path>`,
against its source: all seven BYTE-IDENTICAL. `claim.diff`, `t001.diff` and `t002.diff` were
applied verbatim with `git apply --check` then `git apply`, never retyped or hand-edited; `plan.md`
and `context.md` rewrote `.agent/plan.md` and `.agent/context.md` the same byte-exact way
(`shutil.copyfile`) — G2's byte/sha256 table on the resulting six C2 files and ten C3/C4 files
confirms the applied result matches the reviewer's own simulated target state exactly.
`mutations.py` was run as a tool against a detached worktree and never applied to a tracked file,
per the block.

## Deviations & assumptions

None. Every commit followed the block's ordered sequence exactly (C1a, C1b, C1c, C2, C3, C4, then
C5 with this handback); no payload was edited or retyped; every `git apply --check` before its
real `git apply` read exit 0; no gate went red, so C5 proceeds per constraint 5's own condition
for stopping (not triggered here); no worktree survives this round beyond the reviewer's
pre-existing read-only `f285-r1-dry`/`f285-r1-sim` and the primary checkout; no `remedy/job-*`
branch was created or deleted; no self-use job and no provider-calling `remedy` command was run,
per constraint 8. This handback writes no `Done:` line and no `Landed:` line for R-1057 or R-1058,
per constraint 4 — their resolutions are the reviewer's to author at the next gate.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 460 insertions, matches the block's expectation (230+230) exactly; all four copies byte-identical |
| C1b | done | 235 insertions, matches the block's expectation exactly; copy byte-identical |
| C1c | done | 269 insertions (68+201), matches the block's expectation exactly; both copies byte-identical |
| C2 | done | 11/58/23/17/1/17 insertions by path, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']` at base and C2; STATUS line reads `- [~] F285 — Findings paydown v4` |
| C3 | done | 37/14/63/41 insertions by path, matches the block's expectation exactly; `t001.diff` applied clean |
| C4 | done | 25/1/3/1/25/20 insertions by path, matches the block's expectation exactly; `t002.diff` applied clean |
| C5 | done | this handback, committed after G1-G5; measured in the final reply |
| G1 | done | every payload's lines/bytes/sha256 matched the table; all seven `.agent/authored/` copies byte-identical by `git show` |
| G2 | done | all sixteen named files' bytes/sha256 matched exactly; open-finding set matched at both commits; STATUS line matched; every consecutive-commit diff named exactly its entry's paths |
| G3 | done | 900 passed, 1 skipped, exit 0, matching the reviewer's reading exactly with the same one SKIPPED line; ruff `All checks passed!`; integrity six `pass`, `fail_count` 0 |
| G4 | done | all 5 mutations caught and cleanly restored, matching the reviewer's occurrence and pass/fail counts exactly; worktree removed, `git worktree list` clean of it |
| G5 | done | all six commits' `git show --numstat` readings match the block's expected insertions exactly, placed above verbatim |
| G6 | done | reported in the final reply, after C5 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 1. Then T003 — R-1055's
provider-session resume across a relaunch. Open findings: 5 — `R-1008`, `R-1055`, `R-1057`,
`R-1058` and `R-1064`, all owned by F285 (`R-1057` and `R-1058` repaired this round, their
resolution lines owed at the next gate). Operator questions open: 5 — the count of `### Q`
headings in `.agent/operator_questions.md`.
