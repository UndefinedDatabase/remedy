# Handback — F285 Findings paydown v4 · Round 2

## Session

SESSION 1 of feature F285 · round 2 · rounds so far 2

The large majority of the session's context budget remained at the point this handback was
written. This round booked round 1's PASS with the resolutions of R-1057 and R-1058, recorded
DECISION F285 D2, and landed T003 (R-1055's repair): every round's builder and reviewer blocks in
a run's `result.json` now carry the provider session the call reported and whether it resumed one,
and `run_job` hands the parked run's sessions of a task a park or a stop interrupted to the
relaunch's first calls, which resume them where the provider supports resume.

## Range

Review of 26f44f49..HEAD

## Commits

### 81dea1602 F285 R2 C1a: copy round 2 block and booking payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-r2-block.md | +209/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f285-r2-book.diff | +61/-0 | copy of the book.diff payload |
| .agent/authored/f285-r2-plan.md | +28/-0 | copy of the plan.md payload |

298 insertions by `git show --numstat` (209 for the block plus 89 for the two payloads: 61+28) —
matches the block's stated expectation exactly, under the 500-line cap.

### 993e89ab9 F285 R2 C1b: copy round 2 T003 payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-r2-t003.diff | +451/-0 | copy of the t003.diff payload |

451 insertions — matches the block's stated expectation exactly.

### c85116935 F285 R2 C1c: copy round 2 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-r2-mutations.py | +68/-0 | copy of the mutations.py tool (a G4 tool, never applied to a tracked file) |

68 insertions — matches the block's stated expectation exactly.

### 40e32d188 F285 R2 C2: book F285 R1 with the resolutions of R-1057 and R-1058, record D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +39/-0 | DECISION F285 D2 appended: the provider-session persistence and relaunch-resume design (R-1055), the CONTEXT measured at `26f44f49`, the CHOSEN five-point fix, the ALTERNATIVES rejected, and HOW TO REVERSE |
| .agent/live_review.md | +6/-0 | the F285 round 1 gate entry appended (VERDICT PASS, NO DEVIATION DECLARED), plus the RESOLVED lines for R-1058 and R-1057 |
| .agent/plan.md | +9/-11 | rewritten whole to the plan.md payload — Current Step moved to F285 round 2 (T003), Risks' open-findings count dropped from 5 to 3 |

Insertions by `git show --numstat`: 39 .agent/decisions.md, 6 .agent/live_review.md,
9 .agent/plan.md (11 deletions on the plan rewrite) — matches the block's stated expectation
exactly, in every row, under the 500-line cap. `open_finding_ids` over `.agent/live_review.md`
reads `['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']` at `26f44f49` and
`['R-1008', 'R-1055', 'R-1064']` at this commit — the reviewer's own stated reading at both
points.

### e2f86af8e F285 R2 C3: resume an interrupted task's parked provider session on relaunch
| Path | +/- | Reason |
|---|---|---|
| docs/system/session-resume-v1.md | +17/-0 | doc section added describing the relaunch-resume design |
| packages/orchestration/pingpong_job.py | +10/-0 | `run_job` imports `load_run`/`parked_session_refs`; a task whose `run_id` is set and `final_status` is `stopped` reads its parked run's sessions and passes `resume_sessions`/`resumed_from_run_id` into `run_pingpong` |
| packages/orchestration/pingpong_loop.py | +69/-6 | `_session_fields`/`parked_session_refs` added; `run_pingpong` accepts `resume_sessions`/`resumed_from_run_id`, round 1's first call of each role resumes the offered session when the provider supports resume (separated from the repair-round prompt gate, so the resumed call still sends full context); `export_pingpong_json` writes `session_id`/`resume_used`/`resume_session_ref`/`resume_fallback` per round block and `resumed_from_run_id` on the record |
| tests/orchestration/test_prompt_trace.py | +6/-2 | the two source guards that locate the fallback branch by its condition follow the renamed condition |
| tests/orchestration/test_relaunch_session_resume.py | +165/-0 | new file: `TestParkedSessionRefs`, `TestTheRunRecordCarriesEachCallsSession`, `TestTheFirstCallsResumeTheOfferedSessions`, `TestAParkedTaskResumesOnRelaunch` |

Insertions by `git show --numstat`: 17 session-resume-v1.md, 10 pingpong_job.py,
69/-6 pingpong_loop.py, 6/-2 test_prompt_trace.py, 165 test_relaunch_session_resume.py — matches
the block's stated expectation exactly, under the 500-line cap. `git status --porcelain`
immediately before this commit showed only these five paths staged, matching the round's whole
tracked-path allowance for C3.

### (pending) F285 R2 C4: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f285-r2-mut e2f86af8e` (for G4) — succeeded.
- `git worktree remove --force .remedy-wt/f285-r2-mut` then `git worktree prune` (after G4) —
  succeeded; `git worktree list` afterward shows no worktree this round added.
- `git push origin feature/f285-findings-paydown-v4` (after C4) — its real outcome is reported in
  the final reply, since the push happens after this commit.
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
feature/f285-findings-paydown-v4
$ git log --oneline -1
26f44f496 F285 R1 C5: rewrite handoff for round 1
```
All three matched the delegation message's stated readings exactly.

```
$ (line count and sha256 of .remedy-wt/f285-r2/block.md, measured)
line_count: 209
sha256: 5c83724d41a44b4904cb62e0309c811e5e08c3f010204259b2b88daf928533f7
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported: primary checkout + the pre-existing F015/F020/F023/F024/F025/F284 dry/sim worktrees,
the reviewer's f285-r2-dry and f285-r2-sim, and the same remedy/job-* worktrees already present
at session start. No worktree created or removed by BEFORE-ANYTHING-ELSE.)
```

### PAYLOADS — transport verification

```
$ (lines/bytes/sha256 of each .remedy-wt/f285-r2-payloads/ file, measured)
book.diff       61 lines, 11536 bytes, 99d549e0cd517960c470621032d0d77881c83a3317a574a60adb31310067287e
plan.md         28 lines,   992 bytes, ba2692e1513dd44c877cad521a813da63bf8a95aff18390377fc6f246e732b32
t003.diff      451 lines, 23111 bytes, 1c5983158c7dd98eb082e2ca7c73bd4de3fbbe492b2afcefd5f199724a56664a
mutations.py    68 lines,  2894 bytes, bde3a1817e5b1bc3ecc2bd42c05d37f96596855e1e309c5c911033dfd638ff41
```
Every payload's measured lines/bytes/sha256 matched the block's PAYLOADS table exactly.

### G1 — payload transport (copies vs sources)

```
$ (committed .agent/authored/f285-r2-* bytes, read with git show <commit>:<path>, vs source file bytes)
81dea1602:.agent/authored/f285-r2-block.md      MATCH (sha 5c83724d...533f7 both)
81dea1602:.agent/authored/f285-r2-book.diff     MATCH (sha 99d549e0...067287e both)
81dea1602:.agent/authored/f285-r2-plan.md       MATCH (sha ba2692e1...e732b32 both)
993e89ab9:.agent/authored/f285-r2-t003.diff     MATCH (sha 1c598315...4a56664a both)
c85116935:.agent/authored/f285-r2-mutations.py  MATCH (sha bde3a181...d638ff41 both)
```
All five copies byte-identical to their `.remedy-wt/f285-r2-payloads/` (and, for the block,
`.remedy-wt/f285-r2/`) sources.

### G2 — the booking and the code (sha256 at each named commit)

```
$ git show <commit>:<path> | sha256sum / wc -c, for every row of the block's G2 table
C2 (40e32d188) .agent/decisions.md                                    2147985 bytes   MATCH
C2 (40e32d188) .agent/live_review.md                                   311104 bytes   MATCH
C2 (40e32d188) .agent/plan.md                                             992 bytes   MATCH
C3 (e2f86af8e) docs/system/session-resume-v1.md                          6782 bytes   MATCH
C3 (e2f86af8e) packages/orchestration/pingpong_job.py                 230224 bytes   MATCH
C3 (e2f86af8e) packages/orchestration/pingpong_loop.py                233212 bytes   MATCH
C3 (e2f86af8e) tests/orchestration/test_prompt_trace.py                31122 bytes   MATCH
C3 (e2f86af8e) tests/orchestration/test_relaunch_session_resume.py      7682 bytes   MATCH
```
All eight files' bytes and sha256 equal the block's stated table exactly.

```
$ python3 -c "open_finding_ids(git show <commit>:.agent/live_review.md)" (scripts/rotate_live_review.py)
26f44f49: ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']
40e32d188 (C2): ['R-1008', 'R-1055', 'R-1064']
```
Matches the block's stated reviewer reading exactly, at both commits.

```
$ git diff --name-only <consecutive commit pairs>
c85116935..40e32d188 (C1c->C2): .agent/decisions.md .agent/live_review.md .agent/plan.md
40e32d188..e2f86af8e (C2->C3): docs/system/session-resume-v1.md
  packages/orchestration/pingpong_job.py packages/orchestration/pingpong_loop.py
  tests/orchestration/test_prompt_trace.py tests/orchestration/test_relaunch_session_resume.py
```
Each pair names exactly the paths that commit's entry in the block lists. (First attempt used
993e89ab9 (C1b) by mistake, which showed `f285-r2-mutations.py` also differing — a keying error
on my part, not a tree defect; corrected to c85116935 (C1c) before reporting, above.)

### G3 — the tests, at C3

```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_relaunch_session_resume.py
  tests/orchestration/test_session_resume.py tests/orchestration/test_prompt_trace.py
  tests/orchestration/test_semantic_dedupe.py tests/orchestration/test_pause_resume.py
  tests/orchestration/test_pause_manifest.py tests/orchestration/test_pause_resume_cycles.py
  tests/orchestration/test_pause_control.py tests/orchestration/test_job_stop_integration.py
  tests/orchestration/test_pingpong.py tests/orchestration/test_pingpong_integration.py
  tests/orchestration/test_pingpong_job_dod_gate.py tests/orchestration/test_pingpong_job_hunk_ledger.py
  tests/orchestration/test_provider_evidence_integration.py
  tests/orchestration/test_run_manifest_chain_append.py tests/orchestration/test_import_reachability.py
  tests/test_no_orphan_modules.py tests/orchestration/test_live_review_rotation.py
  tests/orchestration/test_integrity_gate.py tests/ui_server/test_pause_e2e_live.py
  tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py
FAILED tests/ui_server/test_pause_e2e_live.py::TestJobScopeE2ELive::test_pause_relaunch_through_the_cli_matches_an_unpaused_control
  AssertionError: assert 'FINAL:paused' in 'FINAL:completed\n'
1 failed, 889 passed in 116.48s (0:01:56)
REAL_EXIT=1
```
Red on the first run, matching the block's stated shape (the reviewer's own first run in its
freshly created tree read the same `1 failed, 889 passed` without capturing the failing node; this
run captured it: the node above, a pause-vs-completion race in a live E2E subprocess test).

```
$ python3 -m pytest -q -p no:cacheprovider -rs "tests/ui_server/test_pause_e2e_live.py::TestJobScopeE2ELive::test_pause_relaunch_through_the_cli_matches_an_unpaused_control"
1 passed in 7.27s
REAL_EXIT=0
```
Re-run of that single node alone: green.

```
$ (whole selection re-run, warm)
890 passed in 120.46s (0:02:00)
REAL_EXIT=0
```
Matches the reviewer's stated warm-rerun reading exactly (`890 passed` at exit 0). No `SKIPPED`
line printed by the `-rs` summary in either run, matching the reviewer's own reading of none.

```
$ python3 -m ruff check packages/orchestration/pingpong_job.py
  packages/orchestration/pingpong_loop.py tests/orchestration/test_prompt_trace.py
  tests/orchestration/test_relaunch_session_resume.py
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
$ git worktree add --detach .remedy-wt/f285-r2-mut e2f86af8e
Preparing worktree (detached HEAD e2f86af8e)
HEAD is now at e2f86af8e F285 R2 C3: resume an interrupted task's parked provider session on relaunch
REAL_EXIT=0

$ python3 -B .remedy-wt/f285-r2-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f285-r2-mut
control first: exit 0: 82 passed in 2.26s
m1 (run_job offers the relaunch no session): FROM occurs 1x in packages/orchestration/pingpong_job.py
m1: exit 1: 1 failed, 81 passed in 2.40s; restored byte-identical: True
m2 (the builder's first call ignores the offer): FROM occurs 1x in packages/orchestration/pingpong_loop.py
m2: exit 1: 3 failed, 79 passed in 2.19s; restored byte-identical: True
m3 (the reviewer's first call ignores the offer): FROM occurs 1x in packages/orchestration/pingpong_loop.py
m3: exit 1: 1 failed, 81 passed in 1.83s; restored byte-identical: True
m4 (the run record drops the session): FROM occurs 1x in packages/orchestration/pingpong_loop.py
m4: exit 1: 2 failed, 80 passed in 1.62s; restored byte-identical: True
m5 (the fallback fires on the prompt gate again): FROM occurs 1x in packages/orchestration/pingpong_loop.py
m5: exit 1: 2 failed, 80 passed in 1.91s; restored byte-identical: True
control last: exit 0: 82 passed in 1.90s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Matches the reviewer's stated reading exactly on every occurrence count and pass/fail count
(timings vary, as the block itself notes).

```
$ git worktree remove --force .remedy-wt/f285-r2-mut; git worktree prune
REAL_EXIT=0 (both)
$ git worktree list
(no .remedy-wt/f285-r2-mut entry; only the pre-existing worktrees, including the reviewer's
read-only f285-r2-dry and f285-r2-sim, remain)
```

### G5 — sizes (placed exactly as the tool printed)

```
$ git show --numstat --format= 81dea1602
209	0	.agent/authored/f285-r2-block.md
61	0	.agent/authored/f285-r2-book.diff
28	0	.agent/authored/f285-r2-plan.md
```
Expected 298 (209+89). Measured 298. MATCH.

```
$ git show --numstat --format= 993e89ab9
451	0	.agent/authored/f285-r2-t003.diff
```
Expected 451. Measured 451. MATCH.

```
$ git show --numstat --format= c85116935
68	0	.agent/authored/f285-r2-mutations.py
```
Expected 68. Measured 68. MATCH.

```
$ git show --numstat --format= 40e32d188
39	0	.agent/decisions.md
6	0	.agent/live_review.md
9	11	.agent/plan.md
```
Expected 39/6/9 by path. Measured identical per path. MATCH.

```
$ git show --numstat --format= e2f86af8e
17	0	docs/system/session-resume-v1.md
10	0	packages/orchestration/pingpong_job.py
69	6	packages/orchestration/pingpong_loop.py
6	2	tests/orchestration/test_prompt_trace.py
165	0	tests/orchestration/test_relaunch_session_resume.py
```
Expected 17/10/69/6/165 by path. Measured identical per path. MATCH.

## Authored-text proofs

`.agent/authored/f285-r2-block.md`, `f285-r2-book.diff`, `f285-r2-plan.md`, `f285-r2-t003.diff`
and `f285-r2-mutations.py` were built with `shutil.copyfile` from the reviewer's block and payload
files — never retyped, never edited — and G1 compared every one byte for byte, read back with
`git show <commit>:<path>`, against its source: all five BYTE-IDENTICAL. `book.diff` and
`t003.diff` were applied verbatim with `git apply --check` then `git apply`, never retyped or
hand-edited; `plan.md` rewrote `.agent/plan.md` the same byte-exact way (`shutil.copyfile`) — G2's
byte/sha256 table on the resulting three C2 files and five C3 files confirms the applied result
matches the reviewer's own simulated target state exactly. `mutations.py` was run as a tool
against a detached worktree and never applied to a tracked file, per the block.

## Deviations & assumptions

One clerical deviation, corrected before this handback was finalized: in the G2 consecutive-commit
diff check, my first attempt keyed the C1c→C2 boundary off `993e89ab9` (C1b) instead of
`c85116935` (C1c), which surfaced `f285-r2-mutations.py` as an apparent extra difference — that
file was added by C1c and is correctly absent from a true C1c→C2 diff. Re-ran with the correct
commit and it matched exactly (reported above under G2). No tracked file was affected; the error
was confined to a verification command's argument.

Otherwise none: every commit followed the block's ordered sequence exactly (C1a, C1b, C1c, C2, C3,
C4 with this handback); no payload was edited or retyped; every `git apply --check` before its
real `git apply` read exit 0; G3's first test run went red on
`tests/ui_server/test_pause_e2e_live.py::TestJobScopeE2ELive::test_pause_relaunch_through_the_cli_matches_an_unpaused_control`,
exactly the shape the block predicted for a fresh run (a pause/completion race in a live E2E
subprocess test, unrelated to this round's diff — none of C3's five files touch pause-vs-completion
timing), and both the single-node re-run and a full warm re-run of the whole selection came back
green, matching the reviewer's own reported behavior; per AGENTS.md this is not treated as a red
gate. No worktree survives this round beyond the reviewer's pre-existing read-only
`f285-r2-dry`/`f285-r2-sim` and the primary checkout; no `remedy/job-*` branch was created or
deleted; no self-use job and no provider-calling `remedy` command was run, per constraint 8. This
handback writes no `Done:` line and no `Landed:` line for R-1055, per constraint 4 — its resolution
is the reviewer's to author at the next gate.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 298 insertions, matches the block's expectation (209+89) exactly; all three copies byte-identical |
| C1b | done | 451 insertions, matches the block's expectation exactly; copy byte-identical |
| C1c | done | 68 insertions, matches the block's expectation exactly; copy byte-identical |
| C2 | done | 39/6/9 insertions by path, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008','R-1055','R-1057','R-1058','R-1064']` at base and `['R-1008','R-1055','R-1064']` at C2 |
| C3 | done | 17/10/69/6/165 insertions by path, matches the block's expectation exactly; `t003.diff` applied clean; tracked-path set for the commit exactly the five named files |
| C4 | done | this handback, committed after G1-G5; measured in the final reply |
| G1 | done | every payload's lines/bytes/sha256 matched the table; all five `.agent/authored/` copies byte-identical by `git show` |
| G2 | done | all eight named files' bytes/sha256 matched exactly; open-finding set matched at both commits; every consecutive-commit diff (corrected keying, see Deviations) named exactly its entry's paths |
| G3 | done | first run red on one E2E node (pause/completion race, unrelated to the diff), matching the reviewer's own fresh-run shape; single-node re-run and full warm re-run both green (`890 passed` at exit 0, no SKIPPED lines); ruff `All checks passed!`; integrity six `pass`, `fail_count` 0 |
| G4 | done | all 5 mutations caught and cleanly restored, matching the reviewer's occurrence and pass/fail counts exactly; worktree removed, `git worktree list` clean of it |
| G5 | done | all five commits' `git show --numstat` readings match the block's expected insertions exactly, placed above verbatim |
| G6 | done | reported in the final reply, after C4 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 2. Then the closure
sequence's self-use run on R-1064. Open findings: 3 — `R-1008`, `R-1055` and `R-1064`, all owned
by F285. Operator questions open: 5 — the count of `### Q` headings in
`.agent/operator_questions.md`.
