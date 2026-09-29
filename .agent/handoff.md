# Handback — F039, round 11: book round 10 with R-1103's resolution, run the closure's self-use item

## Session

SESSION 2 of feature F039 · round 11 · rounds so far 11. This session ran round 11 only: booking
round 10's PASS verdict and R-1103's `Done:` resolution into the ledger and the plan, then
generating and running the closure's self-use item (precondition 6 of
`docs/roadmap/STATUS_closure_protocol.md`) on the `self_use` role's configured provider, recording
its readings under `.agent/selfuse_f039/`. Context self-assessment: a comfortable margin remained
through the whole round — the block, AGENTS.md and the handback template were read whole before
any edit, every payload was verified before use, the booking diff applied clean on the first try,
the self-use run completed in under a minute of wall time with no repair needed, and the test
selection and integrity check both read clean on the first run; the work was not near its limit.

For the operator, in plain words: round 10 is booked PASS, and R-1103 (the zero-network test's
drain window) is now marked resolved in the ledger. The closure's self-use precondition is met:
the generator picked item `SU-035`, a doc-staleness fix for `docs/guides/story-user-guide-v1.md`
(the guide backticks the config key `story.html`, which is not a registered config key), the job
ran to completion on the real `self_use` provider (`claude-cli`, model `claude-sonnet-4-6`) at a
measured cost of $0.5522286 across 2 provider calls, and its one task passed review
(`staged_review_passed`). The job was never applied — its branch `remedy/job-7a88d05bed5c40dd` is
left on disk, untouched, for the reviewer.

## Range

Review of 0f07b2f8b..HEAD (plus C4, this commit, on top)

## Commits

### ae1928728 F039 R11 C1: copy round 11 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r11-block.md | +169/-0 | verbatim copy of the block |
| .agent/authored/f039-r11-booking.diff | +12/-0 | verbatim copy of the booking payload |
| .agent/authored/f039-r11-plan.md | +27/-0 | verbatim copy of the plan payload |
| .agent/authored/f039-r11-selfuse.py | +121/-0 | verbatim copy of the selfuse.py payload |

Measured insertions: 329 (169 + 12 + 27 + 121), matching the block's expectation of "this block's
line count plus 160" (169 + 160 = 329) exactly.

### ce717518d F039 R11 C2: book round 10 and resolve R-1103
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | F039 R10 gate entry (PASS) and R-1103's `Done:` resolution |
| .agent/plan.md | +5/-9 | rewritten to round 11's current step (the evidence round) and next steps |

Measured: 4/0, 5/9 — matching the block's expectation exactly. Pushed immediately after this
commit, per the block's instruction.

### 6fb2b0a0c F039 R11 C3: generate and run the closure's self-use item, record its readings
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | +8/-0 | appended entry `SU-035` (generator's tier-2 doc-staleness pick) |
| .agent/selfuse_f039/SU-035.md | +13/-0 | NEW: the job's generated markdown |
| .agent/selfuse_f039/changed_paths.txt | +1/-0 | NEW: `docs/guides/story-user-guide-v1.md` |
| .agent/selfuse_f039/entry_and_job_file.txt | +5/-0 | NEW: entry id/title/provenance/consumed_by, job file path |
| .agent/selfuse_f039/execution_config.txt | +39/-0 | NEW: builder/reviewer provider+model, budgets config |
| .agent/selfuse_f039/full_transcript.txt | +14/-0 | NEW: job id/title/state, task summary |
| .agent/selfuse_f039/job_diff.txt | +14/-0 | NEW: `git diff HEAD...remedy/job-<id>` |
| .agent/selfuse_f039/result_state.txt | +12/-0 | NEW: job state, budgets, budget actuals, task states |
| .agent/selfuse_f039/run_defects.txt | +1/-0 | NEW: `describe_self_use_run_defects()` output (NONE) |
| .agent/selfuse_f039/staleness_after.txt | +2/-0 | NEW: staleness catalog re-read from the job branch (NONE) |
| .agent/selfuse_f039/timing.txt | +3/-0 | NEW: started/finished timestamps, wall seconds |

No insertion count was ordered for this commit; measured above (112 total, well under the 500-line
cap). No file outside `scripts/self_use_queue.json` and `.agent/selfuse_f039/**` was touched, per
constraint 3.

### (this commit) F039 R11 C4: rewrite handoff for round 11
| Path | Reason |
|---|---|
| .agent/handoff.md | rewritten per the template (self-reference exception, R-0149 pattern) |

## External actions

- `git push -u origin feature/f039-story-replay-mode` (after C2) — outcome:
  `0f07b2f8b..ce717518d  feature/f039-story-replay-mode -> feature/f039-story-replay-mode`, branch
  set to track the remote, real exit 0.
- Inside C3's run (`selfuse.py`, not a command this worker issued directly): `git worktree add
  --detach .remedy-wt/f039-r11-jobtree remedy/job-7a88d05bed5c40dd` and `git worktree remove
  --force` of the same, both run and cleaned up by the payload script itself while reading the
  staleness catalog from the job branch. `git worktree list | wc -l` read 61 both before and after
  C3, confirming the add/remove cancelled out.
- The self-use run created branch `remedy/job-7a88d05bed5c40dd` and a job workspace at
  `.remedy-wt/job-7a88d05bed5c40dd`, both left on disk untouched per constraint 4 (the job is never
  applied and nothing not created by this worker is deleted). `git branch --list 'remedy/*' | wc
  -l` read 197 before C3 and 198 after — exactly the one new job branch.
- No PR created, no merge, no force-push, no amend, no checkout of another branch, no stash — all
  forbidden by the block and none attempted. The final `gh pr list` reading goes in the reply per
  the block (G6 cannot appear in this file since C4 cannot contain it).

## Verification

### BEFORE ANYTHING ELSE (block steps 1-4)
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f039-story-replay-mode
$ git log --oneline -1
0f07b2f8b F039 R10 C6: record the closure suite transcript and rewrite handoff for round 10
```
Block bytes: measured line count (newline count) 169 / given 169; measured sha256
`9a4b37e43a0a53623a033db881425ed86a9cb66a35add84426a50885c2d465e0` / given the same — MATCH.
`git worktree list | wc -l` at step 4: 61. `git branch --list 'remedy/*' | wc -l` at step 4: 197.

### PAYLOADS table
| file | lines measured/given | bytes measured/given | sha256 match |
|---|---|---|---|
| plan.md | 27/27 | 899/899 | match |
| booking.diff | 12/12 | 5844/5844 | match |
| selfuse.py | 121/121 | 6424/6424 | match |

### G1 TRANSPORT
- plan.md: 27 lines, 899 bytes, sha256 `07e203e61c0a43997ef16568598002c71d302667fe8218974093d155c62c91c9` — matches PAYLOADS table.
- booking.diff: 12 lines, 5844 bytes, sha256 `f6126c3132481ad35e671e61b9c95a3fb6f647f31ef986b80bad3fcd6b28ed5b` — matches PAYLOADS table.
- selfuse.py: 121 lines, 6424 bytes, sha256 `c000469068a75a2c080ba89e3c522a6cfc4239915197e968bce3b5c88a95ee08` — matches PAYLOADS table.
- `git show ae1928728:.agent/authored/f039-r11-block.md` == `.remedy-wt/f039-r11/block.md`: byte-identical (12275 bytes both sides).
- `git show ae1928728:.agent/authored/f039-r11-plan.md` == `.remedy-wt/f039-r11-payloads/plan.md`: byte-identical (899 bytes both sides).
- `git show ae1928728:.agent/authored/f039-r11-booking.diff` == `.remedy-wt/f039-r11-payloads/booking.diff`: byte-identical (5844 bytes both sides).
- `git show ae1928728:.agent/authored/f039-r11-selfuse.py` == `.remedy-wt/f039-r11-payloads/selfuse.py`: byte-identical (6424 bytes both sides).

### G2 THE BOOKING
At C2 (`ce717518d`):
| path | bytes | sha256 | matches table |
|---|---|---|---|
| .agent/live_review.md | 366785 | 2adf0ff4e1b3ca92f2aa653e1324091d2549df5130820166ea8948ec2aa95221 | yes |
| .agent/plan.md | 899 | 07e203e61c0a43997ef16568598002c71d302667fe8218974093d155c62c91c9 | yes |

`open_finding_ids(text)` over the ledger at C2 = `[]`; `latest_gate_verdict(text)` = `PASS` — both
match the block's stated readings exactly (read via `scripts/rotate_live_review.py` with `scripts`
on `sys.path`, over `git show ce717518d:.agent/live_review.md`).

### G3 THE TESTS
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_job.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -30; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
641 passed, 1 skipped in 70.94s (0:01:10)
REAL_EXIT=0
```
Exactly the reviewer's own stated reading of 641 passed, 1 skipped at exit 0; the one skip is the
D12 quarantine at `tests/test_agent_tooling.py:43`.

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=169"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0, exit 0; the verdict check's own message reads PASS,
matching the PASS just booked in C2.

### G4 THE SELF-USE READINGS
```
$ bash -c 'python3 .remedy-wt/f039-r11-payloads/selfuse.py 2>&1 | tee .remedy-wt/f039-r11-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'
generate_and_append_if_empty(): ('SU-035', 'Fix stale documentation: doc_config_keys in docs/guides/story-user-guide-v1.md', 'generated (self-use-generator tier 2, doc staleness, doc_config_keys:docs/guides/story-user-guide-v1.md:backticks the config key `story.html`)')
next_self_use_item(): SU-035 Fix stale documentation: doc_config_keys in docs/guides/story-user-guide-v1.md generated (self-use-generator tier 2, doc staleness, doc_config_keys:docs/guides/story-user-guide-v1.md:backticks the config key `story.html`)
REAL_EXIT=0
```
The item's id, title and provenance read exactly what the reviewer's own generator run over the
same booking read: `SU-035`, from Tier 2 (`doc_config_keys`), generated from the claim that
`docs/guides/story-user-guide-v1.md` backticks the config key `story.html`.

Job id `7a88d05bed5c40dd`, state `completed`, stop reason/source both empty, error empty. Task
`T001`: status `applied_to_job_workspace`, reviewer verdict `pass`, final status
`staged_review_passed`, repair rounds used 0.

Builder and reviewer provider/model, from `.agent/selfuse_f039/execution_config.txt` (never
`fake`): builder `claude-cli` / model `claude-sonnet-4-6` / effort `medium` (all source `cli`);
reviewer `claude-cli` / model `claude-sonnet-4-6` / effort `medium` (all source `cli`).

Budgets: `{"deadline": null, "max_cost_usd": 6.0, "max_provider_calls": 8,
"max_total_tokens": null, "max_wall_clock_minutes": null, "min_free_disk_bytes": null}`.
Budget actuals: `{"actual_call_count": 2, "actual_sources": ["pingpong_live"],
"measured_cost_usd": 0.5522286, "priced_call_count": 2, "provider_call_count": 2,
"schema_version": "2.0.0", "started_at": "2026-09-29T00:57:46.693243+00:00",
"total_tokens": 3045, "unmeasured_call_count": 0, "unpriced_call_count": 0}`.

`.agent/selfuse_f039/changed_paths.txt` verbatim:
```
docs/guides/story-user-guide-v1.md
```

`.agent/selfuse_f039/staleness_after.txt` verbatim:
```
Read from: the job branch remedy/job-7a88d05bed5c40dd
NONE
```

`.agent/selfuse_f039/job_diff.txt` verbatim:
```
$ git diff HEAD...remedy/job-7a88d05bed5c40dd  (exit 0)
diff --git a/docs/guides/story-user-guide-v1.md b/docs/guides/story-user-guide-v1.md
index 95c778069..4c103e809 100644
--- a/docs/guides/story-user-guide-v1.md
+++ b/docs/guides/story-user-guide-v1.md
@@ -44,7 +44,7 @@ or with the environment variables `REMEDY_STORY_STEP_MS` and `REMEDY_STORY_CHAPT
 remedy job story <job id> --export story.html
 ```

-This writes `story.html`, one file that holds everything the story needs: the story player, its
+This writes story.html, one file that holds everything the story needs: the story player, its
 styles, and the job's task list and recorded events. Open the file in any browser, straight from
 your disk. It makes no network request at all and needs no Remedy, so you can send it to someone
 by mail or put it anywhere. The file plays the same way as the cockpit's story: the chapter
```

`.agent/selfuse_f039/run_defects.txt` verbatim:
```
NONE
```

`git worktree list | wc -l` after the run: 61 (unchanged — the script's own jobtree worktree was
added and removed inside the run). `git branch --list 'remedy/*' | wc -l` after the run: 198 (one
new branch, `remedy/job-7a88d05bed5c40dd`, left behind per constraint 4; nothing was deleted that
this worker did not create as scratch).

### G5 SIZES
```
$ git show --numstat --format= ae1928728  (C1)
169	0	.agent/authored/f039-r11-block.md
12	0	.agent/authored/f039-r11-booking.diff
27	0	.agent/authored/f039-r11-plan.md
121	0	.agent/authored/f039-r11-selfuse.py
```
Total 329 insertions, matching the block's expectation (169 + 160 = 329) exactly.
```
$ git show --numstat --format= ce717518d  (C2)
4	0	.agent/live_review.md
5	9	.agent/plan.md
```
Matching the block's expectation (4/0, 5/9) exactly.
```
$ git show --numstat --format= 6fb2b0a0c  (C3)
13	0	.agent/selfuse_f039/SU-035.md
1	0	.agent/selfuse_f039/changed_paths.txt
5	0	.agent/selfuse_f039/entry_and_job_file.txt
39	0	.agent/selfuse_f039/execution_config.txt
14	0	.agent/selfuse_f039/full_transcript.txt
14	0	.agent/selfuse_f039/job_diff.txt
12	0	.agent/selfuse_f039/result_state.txt
1	0	.agent/selfuse_f039/run_defects.txt
2	0	.agent/selfuse_f039/staleness_after.txt
3	0	.agent/selfuse_f039/timing.txt
8	0	scripts/self_use_queue.json
```
Total 112 insertions; no insertion count was ordered for C3 individually, and it is well under the
500-line cap.

## Authored-text proofs

| payload | committed at | disk-to-disk vs source | result |
|---|---|---|---|
| block.md copy | ae1928728 | `.agent/authored/f039-r11-block.md` vs `.remedy-wt/f039-r11/block.md` | byte-identical |
| plan.md copy | ae1928728 | `.agent/authored/f039-r11-plan.md` vs `.remedy-wt/f039-r11-payloads/plan.md` | byte-identical |
| booking.diff copy | ae1928728 | `.agent/authored/f039-r11-booking.diff` vs `.remedy-wt/f039-r11-payloads/booking.diff` | byte-identical |
| selfuse.py copy | ae1928728 | `.agent/authored/f039-r11-selfuse.py` vs `.remedy-wt/f039-r11-payloads/selfuse.py` | byte-identical |
| booking.diff application | ce717518d | `git apply --check` then `git apply`, both exit 0; C2's two files' bytes/sha256 vs the G2 table | both match |
| plan.md rewrite | ce717518d | `.agent/plan.md` := payload plan.md via `shutil.copyfile`, bytes/sha256 vs the PAYLOADS/G2 table | match |
| selfuse.py execution | 6fb2b0a0c | run verbatim, unedited, from `.remedy-wt/f039-r11-payloads/selfuse.py`; no line retyped | N/A (script run, not applied as text) |

## Item Status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | pushed immediately after |
| C3 | done | job completed, verdict pass, never applied |
| C4 | done | this handback |
| G1 transport | done | |
| G2 the booking | done | open_finding_ids=[], latest_gate_verdict=PASS |
| G3 the tests | done | 641 passed, 1 skipped (D12 quarantine); integrity check 6/6 pass |
| G4 self-use readings | done | SU-035, completed, pass, staged_review_passed, $0.5522286 |
| G5 sizes | done | C1 329, C2 4/0+5/9, C3 112 |
| G6 tree and push | done | reported in the reply |
| R-1103 | done (already) | resolution booked this round via booking.diff |

## Deviations & assumptions

None. Every commit ran in the block's ordered sequence (C1, C2, C3, C4); no commit reached the
500-line cap, so none was split; the tracked path set after C4 matches constraint 3 exactly; the
self-use job completed rather than blocking or stopping, which the block treats as one of several
valid outcomes to record, not a deviation; nothing was merged, no PR was created, and no branch or
worktree that this worker did not itself create as scratch was touched or deleted.

## Next

Phase 1 rule 1: read `.agent/STOP` from disk before anything else. Then the review of round 11 —
the booking of round 10 and R-1103's resolution — and of the self-use run (item `SU-035`, job
`7a88d05bed5c40dd`, completed/pass/staged_review_passed, never applied). Then the closure's
evidence round: the booking of round 11, any finding the self-use run raises, the evidence bundle
and the review package. Then the closing round: the ledger rotation, the STATUS flip and the pull
request. Open-findings count: 0. Operator questions open: 1.
