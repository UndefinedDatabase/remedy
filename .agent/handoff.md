# Handback — F285 Findings paydown v4 · Round 3

## Session

SESSION 1 of feature F285 · round 3 · rounds so far 3

The large majority of the session's context budget remained at the point this handback was
written. This round booked round 2's PASS with the resolution of R-1055, then met closure
precondition 6 of `docs/roadmap/STATUS_closure_protocol.md`: generated the closure's self-use
item — `SU-032`, "Address ledger finding R-1064" — and ran it to its approval gate on the
`self_use` role (job `78ecdc636060461c`, `completed`, task `T001` verdict `pass`), recording its
readings and its defects under `.agent/selfuse_f285/`. The job is not applied; its diff is the
reviewer's to judge at the next gate (DECISION F285 D1).

## Range

Review of 0fc0d8d0..HEAD

## Commits

### a78a47bfc F285 R3 C1: copy round 3 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f285-r3-block.md | +170/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f285-r3-records.diff | +12/-0 | copy of the records.diff payload |
| .agent/authored/f285-r3-plan.md | +29/-0 | copy of the plan.md payload |
| .agent/authored/f285-r3-selfuse.py | +85/-0 | copy of the selfuse.py tool (a C3 tool, run from the primary checkout, never applied to a tracked file) |

296 insertions by `git show --numstat` (170 for the block plus 126 for the three payloads:
12+29+85) — matches the block's stated expectation exactly, under the 500-line cap.

### c67932fe7 F285 R3 C2: book F285 R2 with the resolution of R-1055
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | the F285 round 2 gate entry appended (VERDICT PASS, ONE DEVIATION DECLARED AND ACCEPTED — the cold-`apps/ui/dist`-build E2E race, no id minted) and the RESOLVED line for R-1055, via `git apply` of records.diff |
| .agent/plan.md | +10/-9 | rewritten whole to the plan.md payload — Current Step moved to F285 round 3 (the closure sequence's first round), Risks' open-findings count dropped from 3 to 2 |

Insertions by `git show --numstat`: 4 .agent/live_review.md, 10/-9 .agent/plan.md — matches the
block's stated expectation exactly, under the 500-line cap. `open_finding_ids` over
`.agent/live_review.md` at this commit reads `['R-1008', 'R-1064']` — the reviewer's own stated
reading exactly.

### 148c54d25 F285 R3 C3: generate and run the closure's self-use item, record its readings
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | +8/-0 | `SU-032` ("Address ledger finding R-1064") appended by `generate_and_append_if_empty()`, `consumed_by` left empty — this round sets no `consumed_by` |
| .agent/selfuse_f285/SU-032.md | +10/-0 | the generated job file, copied verbatim from the job workspace |
| .agent/selfuse_f285/entry_and_job_file.txt | +5/-0 | entry id/title/provenance/consumed_by and the job file path |
| .agent/selfuse_f285/execution_config.txt | +39/-0 | the run's execution config: builder/reviewer both `claude-cli` at `claude-sonnet-4-6`, `medium` effort |
| .agent/selfuse_f285/result_state.txt | +12/-0 | job id/state/stop-reason/budgets/budget-actuals/workspace and every task's status line |
| .agent/selfuse_f285/changed_paths.txt | +2/-0 | the two files T001's applied manifest touched |
| .agent/selfuse_f285/full_transcript.txt | +14/-0 | job id/title/state and the one task's summary |
| .agent/selfuse_f285/timing.txt | +3/-0 | start/finish timestamps and wall-clock seconds (248.6s) |
| .agent/selfuse_f285/run_defects.txt | +1/-0 | `describe_self_use_run_defects()` over the completed plan: `NONE` |

94 insertions by `git show --numstat`, under the 500-line cap. `git status --porcelain`
immediately before this commit showed only these nine paths (one modified, eight new), matching
the round's whole tracked-path allowance for C3 — no other file changed by the run.

### (pending) F285 R3 C4: rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

## External actions

- `git push origin feature/f285-findings-paydown-v4` (after C4) — its real outcome is reported in
  the final reply, since the push happens after this commit.
- No `gh pr create` (the block forbids it this round). No `git stash`, no force-push, no checkout
  of `main`, no branch deletion, no `remedy/job-*` branch deleted, no worktree add/remove by me.
  The self-use run itself minted `remedy/job-78ecdc636060461c` and a job workspace under
  `.remedy-wt/job-78ecdc636060461c` that the run's own teardown removed after the task reached
  `staged_review_passed`; the branch remains (48 `remedy/job-*` branches now vs 47 at session
  start) — reported, not deleted, per constraint 4. The one `npm --prefix apps/ui run build` ran
  at G3; no `npm install`, `npm ci` or `npx`.

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
0fc0d8d0f F285 R2 C4: rewrite handoff for round 2
```
All three matched the delegation message's stated readings exactly.

```
$ (line count and sha256 of .remedy-wt/f285-r3/block.md, measured)
line_count: 170
sha256: 7d4b9ebba32bee07d8313563b838812240e72447a9571a2d7661c23dbae13138
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported: primary checkout + the pre-existing F015/F020/F023/F024/F025/F284 dry/sim worktrees,
the reviewer's read-only f285-r3-dry, and the pre-existing remedy/job-* worktrees already present
at session start. No worktree created or removed by BEFORE-ANYTHING-ELSE.)
$ git branch --list 'remedy/job-*'
(47 branches, as at session start — reported in full at BEFORE-ANYTHING-ELSE; none created or
deleted by that step.)
```

### PAYLOADS — transport verification

```
$ (lines/bytes/sha256 of each .remedy-wt/f285-r3-payloads/ file, measured)
records.diff   12 lines,  6713 bytes, 935261ff0ee1a812d1ebcc096539bc14b654008eb1cd61c55d9abb3d9a953b03
plan.md        29 lines,  1080 bytes, 2402f472e5956ee2702f17bcfe79a921ef321fa86c90afec34a3be88bca89911
selfuse.py     85 lines,  4481 bytes, 4476d47c9625234cba0966f285120ac10854057463095cee5fdd0242127e808b
```
Every payload's measured lines/bytes/sha256 matched the block's PAYLOADS table exactly.

### G1 — payload transport (copies vs sources)

```
$ (committed .agent/authored/f285-r3-* bytes, read with git show a78a47bfc:<path>, vs source file bytes)
a78a47bfc:.agent/authored/f285-r3-block.md      IDENTICAL (11361 bytes both, sha 7d4b9ebb...bae13138 both)
a78a47bfc:.agent/authored/f285-r3-records.diff  IDENTICAL (6713 bytes both, sha 935261ff...a953b03 both)
a78a47bfc:.agent/authored/f285-r3-plan.md       IDENTICAL (1080 bytes both, sha 2402f472...bca89911 both)
a78a47bfc:.agent/authored/f285-r3-selfuse.py    IDENTICAL (4481 bytes both, sha 4476d47c...127e808b both)
```
All four copies byte-identical to their sources (`.remedy-wt/f285-r3/block.md` for the block,
`.remedy-wt/f285-r3-payloads/` for the three payloads).

### G2 — the booking (sha256 at C2)

```
$ git show c67932fe7:<path> | wc -c / sha256sum, for every row of the block's G2 table
C2 (c67932fe7) .agent/live_review.md   315159 bytes   sha 60ce388e3f800369481eff65360cd9ae896dc56057f75f6a3eedb5e1dc047aae   MATCH
C2 (c67932fe7) .agent/plan.md            1080 bytes   sha 2402f472e5956ee2702f17bcfe79a921ef321fa86c90afec34a3be88bca89911   MATCH
```
Both files' bytes and sha256 equal the block's stated table exactly.

```
$ python3 -c "open_finding_ids(git show c67932fe7:.agent/live_review.md)" (scripts/rotate_live_review.py)
['R-1008', 'R-1064']
```
Matches the block's stated reviewer reading exactly.

### G3 — the UI build and the tests, at C3

```
$ npm --prefix apps/ui run build 2>&1 | tail -2
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 2.27s
REAL_EXIT=0
$ git status --porcelain
(empty)
```

```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_self_use_generator.py
  tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_runner.py
  tests/orchestration/test_self_use_findings.py tests/orchestration/test_live_review_rotation.py
  tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
........................................................................ [ 13%]
........................................................................ [ 27%]
........................................................................ [ 40%]
........................................................................ [ 54%]
........................................................................ [ 67%]
........................................................................ [ 81%]
........................................................................ [ 94%]
...........................                                              [100%]
531 passed in 65.99s (0:01:05)
REAL_EXIT=0
```
Matches the reviewer's dry-tree reading exactly (`531 passed` at exit 0, no `SKIPPED` line printed
by the `-rs` summary).

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

### G4 — the self-use readings

```
$ bash -c 'python3 .remedy-wt/f285-r3-payloads/selfuse.py 2>&1 | tee .remedy-wt/f285-r3-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'
generate_and_append_if_empty(): ('SU-032', 'Address ledger finding R-1064', 'generated (self-use-generator tier 1, ledger scan, R-1064)')
next_self_use_item(): SU-032 Address ledger finding R-1064 generated (self-use-generator tier 1, ledger scan, R-1064)
=== SU-032.md ===
[job file body: Task 1 = R-1064, Low, the stream-evidence redactor's `sk-` pattern has no left
boundary and misreads plan-edit test node ids as secrets; FIX = give the pattern a token-start
boundary as R-1060's does, with a test pinning those ids clean and a real key after space/=/quote/
//- still caught; instruction not to touch any file under `.agent/`]
=== changed_paths.txt ===
packages/orchestration/stream_evidence.py
tests/orchestration/test_stream_evidence.py
=== entry_and_job_file.txt ===
Entry ID: SU-032
Entry Title: Address ledger finding R-1064
Entry Provenance: generated (self-use-generator tier 1, ledger scan, R-1064)
Entry Consumed By:
Job File Path: /home/decodeux/Repos/remedy/.remedy-wt/f285-r3-selfuse/SU-032.md
=== execution_config.txt ===
{
  "builder": "claude-cli", "builder_effort": "medium", "builder_effort_source": "cli",
  "builder_model": "claude-sonnet-4-6", "builder_model_source": "cli", "builder_source": "cli",
  "claude_cli_write_mode": "allowed-tools", "claude_cli_write_mode_source": "cli",
  "context_strategy": "task_bounded_sequential_job", "max_output_chars": 50000,
  "max_output_chars_source": "default", "max_rounds": 3, "max_rounds_source": "default",
  "max_tasks": 1, "max_tasks_source": "invocation", "repair_effort": "",
  "repair_effort_source": "default", "repair_model": "", "repair_model_source": "default",
  "repair_provider": "", "repair_provider_source": "default", "repair_rounds_allowed": 2,
  "repair_rounds_source": "default", "reviewer": "claude-cli", "reviewer_effort": "medium",
  "reviewer_effort_source": "cli", "reviewer_model": "claude-sonnet-4-6",
  "reviewer_model_source": "cli", "reviewer_source": "cli", "stream_evidence": false,
  "stream_evidence_source": "default", "test_command": "", "test_command_source": "default",
  "timeout_profile": "", "timeout_profile_source": "default", "timeout_sec": 600,
  "timeout_sec_source": "invocation"
}
=== full_transcript.txt ===
Job ID: 78ecdc636060461c
Job Title: Address ledger finding R-1064
Job State: completed
Stop Reason:
Stop Source:
Execution: {...same config as above...}

Task Summary:

Task T001:
- Status: applied_to_job_workspace
- Reviewer Verdict: pass
- Final Status: staged_review_passed
- Error:
=== result_state.txt ===
Job ID: 78ecdc636060461c
Job State: completed
Stop Reason:
Stop Source:
Error:
Run Manifest Error:
Budgets: {"deadline": null, "max_cost_usd": 6.0, "max_provider_calls": 8, "max_total_tokens": null,
  "max_wall_clock_minutes": null, "min_free_disk_bytes": null}
Budget Actuals: {"actual_call_count": 2, "actual_sources": ["pingpong_live"],
  "measured_cost_usd": 0.8483763000000001, "priced_call_count": 2, "provider_call_count": 2,
  "schema_version": "2.0.0", "started_at": "2026-09-25T23:18:59.353523+00:00",
  "total_tokens": 11068, "unmeasured_call_count": 0, "unpriced_call_count": 0}
Job Workspace: /home/decodeux/Repos/remedy/.remedy-wt/job-78ecdc636060461c

Task States:
  T001: applied_to_job_workspace (verdict: pass; final_status: staged_review_passed;
        repair_rounds_used: 0; run_id: 94eae4484e9f432f)
=== run_defects.txt ===
NONE
=== timing.txt ===
Started: 2026-09-25T23:18:59.296426+00:00
Finished: 2026-09-25T23:23:07.849118+00:00
Wall seconds: 248.6

REAL_EXIT=0
```

Item: id `SU-032`, title "Address ledger finding R-1064", provenance "generated
(self-use-generator tier 1, ledger scan, R-1064)". Job: id `78ecdc636060461c`, state `completed`.
Builder and reviewer provider both `claude-cli` at model `claude-sonnet-4-6` (never `fake`), read
from `.agent/selfuse_f285/execution_config.txt` — the `self_use` role's configured provider.
Budgets: `max_cost_usd` 6.0, `max_provider_calls` 8, no deadline/token/wall-clock/disk caps set.
Budget actuals: 2 provider calls (both priced, both `pingpong_live`), 0.8483763 USD measured,
11068 total tokens — well inside the cap. Task `T001`: status `applied_to_job_workspace`,
reviewer verdict `pass`, final status `staged_review_passed`, `repair_rounds_used` 0, `run_id`
`94eae4484e9f432f`. `.agent/selfuse_f285/changed_paths.txt` verbatim:
```
packages/orchestration/stream_evidence.py
tests/orchestration/test_stream_evidence.py
```
`.agent/selfuse_f285/run_defects.txt` verbatim: `NONE`.

```
$ git worktree list (after the run)
(no .remedy-wt/job-78ecdc636060461c entry — the job's own teardown removed the worktree after
T001 reached staged_review_passed; no other worktree added or removed by this round)
$ git branch --list 'remedy/job-*' | wc -l
48
$ git branch --list 'remedy/job-*' | grep 78ecdc636060461c
  remedy/job-78ecdc636060461c
```
One new `remedy/job-*` branch, `remedy/job-78ecdc636060461c`, left behind by the run (47 → 48);
its worktree directory is already gone. Nothing was deleted by me — per constraint 4, the branch
is reported, not removed.

### G5 — sizes (placed exactly as the tool printed)

```
$ git show --numstat --format= a78a47bfc
170	0	.agent/authored/f285-r3-block.md
29	0	.agent/authored/f285-r3-plan.md
12	0	.agent/authored/f285-r3-records.diff
85	0	.agent/authored/f285-r3-selfuse.py
```
Expected 296 (170+126). Measured 296. MATCH.

```
$ git show --numstat --format= c67932fe7
4	0	.agent/live_review.md
10	9	.agent/plan.md
```
Expected 4 .agent/live_review.md, 10 .agent/plan.md. Measured identical per path. MATCH.

```
$ git show --numstat --format= 148c54d25
10	0	.agent/selfuse_f285/SU-032.md
2	0	.agent/selfuse_f285/changed_paths.txt
5	0	.agent/selfuse_f285/entry_and_job_file.txt
39	0	.agent/selfuse_f285/execution_config.txt
14	0	.agent/selfuse_f285/full_transcript.txt
12	0	.agent/selfuse_f285/result_state.txt
1	0	.agent/selfuse_f285/run_defects.txt
3	0	.agent/selfuse_f285/timing.txt
8	0	scripts/self_use_queue.json
```
No expectation stated for C3 in the block beyond the 500-line cap; 94 insertions total, well
under it.

## Authored-text proofs

`.agent/authored/f285-r3-block.md`, `f285-r3-records.diff`, `f285-r3-plan.md` and
`f285-r3-selfuse.py` were built with `shutil.copyfile` from the reviewer's block and payload
files — never retyped, never edited — and G1 compared every one byte for byte, read back with
`git show a78a47bfc:<path>`, against its source: all four BYTE-IDENTICAL. `records.diff` was
applied verbatim with `git apply --check` (exit 0) then `git apply` (exit 0), never retyped or
hand-edited; `plan.md` rewrote `.agent/plan.md` the same byte-exact way (`shutil.copyfile`) — G2's
byte/sha256 table on the resulting two C2 files confirms the applied result matches the reviewer's
own stated target state exactly. `selfuse.py` was run as a tool from the primary checkout — never
applied to a tracked file — exactly as the block specifies.

## Deviations & assumptions

None. Every commit followed the block's ordered sequence exactly (C1, C2, C3, C4 with this
handback); no payload was edited or retyped; `git apply --check` before the real `git apply` read
exit 0; the self-use job ran to a clean `completed` state on its first attempt — no repair round
was needed, no exception occurred before the job existed, so no re-run and no stop condition
applied. The job's own teardown left one `remedy/job-*` branch behind
(`remedy/job-78ecdc636060461c`) with its worktree directory already removed; per constraint 4 this
is reported, not deleted, since it is the run's own artifact, not scratch I created. No
`consumed_by` was set on `SU-032` this round, per constraint 3 — the closure commit sets it. This
handback writes no `Done:`/`Landed:` line for R-1064 or R-1008 — the self-use diff's judgment is
the reviewer's, at the next gate. G3's test selection, the UI build, and `integrity check` all
read green on the first and only run — no red-then-green race surfaced this round.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 296 insertions, matches the block's expectation (170+126) exactly; all four copies byte-identical |
| C2 | done | 4/10 insertions by path, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008', 'R-1064']` |
| C3 | done | 94 insertions across 9 paths, exactly `scripts/self_use_queue.json` + `.agent/selfuse_f285/**`; job `78ecdc636060461c` reached `completed` with T001 `pass`/`staged_review_passed` on the first attempt |
| C4 | done | this handback, committed after G1-G5; measured in the final reply |
| G1 | done | every payload's lines/bytes/sha256 matched the table; all four `.agent/authored/` copies byte-identical by `git show` |
| G2 | done | both named files' bytes/sha256 matched exactly; open-finding set `['R-1008','R-1064']` matched the reviewer's stated reading |
| G3 | done | UI build exit 0, tree stayed clean; `531 passed` at exit 0, no SKIPPED; integrity six `pass`, `fail_count` 0 |
| G4 | done | full C3 output and readings recorded above; provider `claude-cli`/`claude-sonnet-4-6` (never fake); budgets/actuals/task states/changed_paths/run_defects all recorded verbatim; one `remedy/job-*` branch left behind, reported |
| G5 | done | all three commits' `git show --numstat` readings match the block's stated expectations exactly (C3 unstated beyond the cap), placed above verbatim |
| G6 | done | reported in the final reply, after C4 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 3 and of the self-use run's
diff. Then the rest of the closure sequence. Open findings: 2 — `R-1008` and `R-1064`, both owned
by F285. Operator questions open: 5 — the count of `### Q` headings in
`.agent/operator_questions.md`.
