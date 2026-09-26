# Handoff — F289, round 4

## Session

SESSION 1 of feature F289 · round 4 · rounds so far 4. Context remaining at
handback: comfortable — the round closed inside a single session with no
compaction needed.

## Range

Review of `ad7f57ad`..`HEAD` (`HEAD` is this handback's own commit, `F289 R4
C4`, on `feature/f289-self-use-sources`).

## Commits

### 0f61f735f F289 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f289-r4-block.md | 170/0 | copy of this round's block (`shutil.copyfile`) |
| .agent/authored/f289-r4-plan.md | 29/0 | copy of the plan.md payload |
| .agent/authored/f289-r4-records.diff | 30/0 | copy of the records.diff payload |
| .agent/authored/f289-r4-selfuse.py | 99/0 | copy of the selfuse.py payload |

Measured insertions: 328 (170+29+30+99), matching the block's expectation
(block's own line count 170 plus 158).

### 1a6806250 F289 R4 C2: book round 3 and R-1074's resolution, consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 3/1 | `git apply records.diff` — replaces `Landed: R-1074` with `Done: R-1074`, appends the round 3 gate entry |
| .agent/plan.md | 9/8 | rewritten to the plan.md payload |
| docs/agents/planner_reviewer_prompt.md | 7/0 | `git apply records.diff` — inserts the consolidation paragraph above "The next consolidation measures against 34." |

Expected by the block: 3/1, 9/8, 7/0 — measured identically.

### 89e841117 F289 R4 C3: generate and run the closure's self-use item, record its readings
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | 8/0 | appends the generated item SU-033 |
| .agent/selfuse_f289/SU-033.md | 13/0 | the generated job file, copied verbatim |
| .agent/selfuse_f289/changed_paths.txt | 1/0 | `docs/README.md` |
| .agent/selfuse_f289/entry_and_job_file.txt | 5/0 | id/title/provenance/consumed_by/job-file-path |
| .agent/selfuse_f289/execution_config.txt | 39/0 | the run's execution config |
| .agent/selfuse_f289/full_transcript.txt | 14/0 | job/task summary |
| .agent/selfuse_f289/result_state.txt | 12/0 | job id, state, budgets, budget actuals, task states |
| .agent/selfuse_f289/run_defects.txt | 1/0 | `NONE` |
| .agent/selfuse_f289/staleness_after.txt | 1/0 | `NO WORKSPACE: ...` — the runner had already cleaned up the job's worktree |
| .agent/selfuse_f289/timing.txt | 3/0 | started/finished/wall seconds |

No insertion count was expected by the block for C3; measured total 97.

### .agent/handoff.md (this commit, F289 R4 C4)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git push` — real outcome reported in Verification (G6).
- The self-use run itself (inside C3, not a worker action) created and then
  auto-cleaned the worktree `.remedy-wt/job-da4583bff80a47f1` for job
  `da4583bff80a47f1` (`job show`'s `worktree.cleanup_status` reads `clean`),
  leaving the branch `remedy/job-da4583bff80a47f1` and the evidence directory
  `.data/jobs/da4583bff80a47f1` behind — neither deleted by the worker.
- No PR created, no PR merged, no branch checkout, no force-push, no stash —
  none were ordered and none were done.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → does not exist (real exit 2, `No such file or
  directory`).
- `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty.
  `git branch --show-current` → `feature/f289-self-use-sources`. `git log
  --oneline -1` → `ad7f57ad6 F289 R3 C5: rewrite handoff for round 3` — all
  three matched (`ad7f57ad` per the delegation message).
- Block bytes: measured 170 lines, sha256
  `883962573192f48b9e307d8b088962f050564b226e53a52bc1dae649f1e4bf7d` against
  `.remedy-wt/f289-r4/block.md` — both matched the delegation message.
- `git worktree list` reported as found: the primary checkout plus the
  F015/F020/F023/F024/F025/F027/F284 dry/sim worktrees, `f289-r4-dry` and
  `f289-r4-sim` (the reviewer's), and ten `job-*` worktrees. `git branch
  --list 'remedy/*'` → 195.

PAYLOADS (measured against the table, before use):
| file | lines | bytes | sha256 match |
|---|---|---|---|
| plan.md | 29 | 1010 | yes |
| records.diff | 30 | 6319 | yes |
| selfuse.py | 99 | 5245 | yes |

CONSTRAINT 1 — `git apply --check .remedy-wt/f289-r4-payloads/records.diff` →
real exit 0. `git apply` (real) → real exit 0.

G1 TRANSPORT — every `.agent/authored/f289-r4-*` copy read back with `git show
0f61f735f:<path>` compared byte-for-byte (sha256) against its source: all
four byte-identical (block.md, plan.md, records.diff and selfuse.py sha256
matched on both sides — see the PAYLOADS table and the BEFORE-ANYTHING-ELSE
block reading above).

G2 THE BOOKKEEPING — every file's sha256 read with `git show
1a6806250:<path>` matched the reviewer's table exactly:
| path | bytes | sha256 match |
|---|---|---|
| .agent/live_review.md | 328714 | yes |
| docs/agents/planner_reviewer_prompt.md | 105183 | yes |
| .agent/plan.md | 1010 | yes |

`open_finding_ids` (from `scripts/rotate_live_review.py`) over the ledger
TEXT: at `ad7f57ad` → `['R-1074']`; at `1a6806250` → `[]` — matching the
reviewer's reading exactly.

G3 THE TESTS — serial run in the primary checkout at C3 (branch tip after
C3) of the block's selection:
```
585 passed in 43.75s
REAL_EXIT=0
```
No `-rs` summary line printed (none skipped), matching the reviewer's
simulation reading of `585 passed` at real exit code 0 exactly.

`python3 -m apps.cli.main integrity check --json` → all six checks `pass`,
`fail_count` 0, `ok` true.

G4 THE SELF-USE READINGS — the whole output of C3's command:
```
generate_and_append_if_empty(): ('SU-033', 'Fix stale documentation: docs_index_guide_registration in docs/README.md', 'generated (self-use-generator tier 2, doc staleness, docs_index_guide_registration:docs/README.md:the Quick-Find Table has no link to `guides/real-test-execution-snapshot-rollback-user-guide-v1.md`)')
next_self_use_item(): SU-033 Fix stale documentation: docs_index_guide_registration in docs/README.md generated (self-use-generator tier 2, doc staleness, docs_index_guide_registration:docs/README.md:the Quick-Find Table has no link to `guides/real-test-execution-snapshot-rollback-user-guide-v1.md`)
[... the nine .agent/selfuse_f289/ files printed verbatim, contents reproduced below ...]
REAL_EXIT=0
```
(Full 109-line transcript saved at `.remedy-wt/f289-r4-worker/selfuse.log`,
gitignored scratch.)

Item: id `SU-033`, title "Fix stale documentation: docs_index_guide_registration
in docs/README.md", provenance "generated (self-use-generator tier 2, doc
staleness, docs_index_guide_registration:docs/README.md:the Quick-Find Table
has no link to `guides/real-test-execution-snapshot-rollback-user-guide-v1.md`)"
— exactly the reviewer's simulation reading (`SU-033`, Tier 2, the same
missing link) named in the block.

Job: id `da4583bff80a47f1`, state `completed`.

Builder and reviewer provider/model, from `execution_config.txt`: builder
`claude-cli` / `claude-sonnet-4-6` (effort `medium`), reviewer `claude-cli` /
`claude-sonnet-4-6` (effort `medium`) — the `self_use` role's real configured
provider, never `fake`.

Budgets: `max_cost_usd` 6.0, `max_provider_calls` 8 (no deadline, token,
wall-clock or disk floor set). Budget actuals: `actual_call_count` 2,
`priced_call_count` 2, `unmeasured_call_count` 0, `unpriced_call_count` 0,
`measured_cost_usd` 0.5631039000000001, `total_tokens` 3126,
`actual_sources` `["pingpong_live"]`.

Task status: T001 — status `applied_to_job_workspace`; reviewer verdict
`pass`; final status `staged_review_passed`; `repair_rounds_used` 0; run id
`1f6f98f62e7348cb`.

`.agent/selfuse_f289/changed_paths.txt` verbatim:
```
docs/README.md
```

`.agent/selfuse_f289/staleness_after.txt` verbatim:
```
NO WORKSPACE: '/home/decodeux/Repos/remedy/.remedy-wt/job-da4583bff80a47f1'
```
(The runner's isolation mode is `worktree` and it auto-cleans the job
worktree once the job reaches `completed` — confirmed by `job show
da4583bff80a47f1 --json`'s `worktree.cleanup_status: "clean"` — so by the
time the script ran `run_staleness_checks()` against the recorded
`job_workspace_path`, the directory no longer existed. This is the runner's
normal cleanup behavior, not a script defect.)

`.agent/selfuse_f289/run_defects.txt` verbatim:
```
NONE
```

The diff the job left in its workspace: `bash -c 'git -C
.remedy-wt/job-da4583bff80a47f1 diff HEAD; echo "REAL_EXIT=$?"'` →
```
fatal: cannot change to '.remedy-wt/job-da4583bff80a47f1': No such file or directory
REAL_EXIT=128
```
— the directory is gone (see above); there are no untracked files to report
either, for the same reason. The content the job produced there survives as
the single commit on branch `remedy/job-da4583bff80a47f1`
(`ac5e6e73d "task 1: Task 1"`, parented on this round's own C2 `1a6806250`),
whose whole diff is:
```
diff --git a/docs/README.md b/docs/README.md
index 7aa7e4ac9..25c761128 100644
--- a/docs/README.md
+++ b/docs/README.md
@@ -60,6 +60,7 @@
 | steering | [steering-user-guide-v1.md](guides/steering-user-guide-v1.md) | guide |
 | teacher lessons | [teacher-lessons-user-guide-v1.md](guides/teacher-lessons-user-guide-v1.md) | guide |
 | test execution | [real-test-execution-v1.md](system/real-test-execution-v1.md) | system |
+| test execution / snapshot | [real-test-execution-snapshot-rollback-user-guide-v1.md](guides/real-test-execution-snapshot-rollback-user-guide-v1.md) | guide |
 | test lanes | [test-lanes-v0.md](system/test-lanes-v0.md) | system |
 | token economy | [token-economy-context-budget-optimizer-v0.md](system/token-economy-context-budget-optimizer-v0.md) | system |
 | token economy | [token-economy-user-guide-v0.md](guides/token-economy-user-guide-v0.md) | guide |
```
— one insertion, exactly the missing Quick-Find Table row the item's
acceptance names. It was never applied to the primary checkout (constraint
4): `git status --porcelain` in the primary checkout shows nothing under
`docs/README.md`.

`git worktree list` after the run: the primary checkout plus the same
pre-existing dry/sim worktrees, ten pre-existing `job-*` worktrees, and no
worktree for `da4583bff80a47f1` (auto-cleaned). `git branch --list
'remedy/*'` after the run → 196 (195 before C3, +1 for
`remedy/job-da4583bff80a47f1`, which the runner left behind and this round
did not delete).

G5 SIZES — `git show --numstat --format=` for C1, C2 and C3:
```
=== C1 0f61f735f ===
170	0	.agent/authored/f289-r4-block.md
29	0	.agent/authored/f289-r4-plan.md
30	0	.agent/authored/f289-r4-records.diff
99	0	.agent/authored/f289-r4-selfuse.py
=== C2 1a6806250 ===
3	1	.agent/live_review.md
9	8	.agent/plan.md
7	0	docs/agents/planner_reviewer_prompt.md
=== C3 89e841117 ===
13	0	.agent/selfuse_f289/SU-033.md
1	0	.agent/selfuse_f289/changed_paths.txt
5	0	.agent/selfuse_f289/entry_and_job_file.txt
39	0	.agent/selfuse_f289/execution_config.txt
14	0	.agent/selfuse_f289/full_transcript.txt
12	0	.agent/selfuse_f289/result_state.txt
1	0	.agent/selfuse_f289/run_defects.txt
1	0	.agent/selfuse_f289/staleness_after.txt
3	0	.agent/selfuse_f289/timing.txt
8	0	scripts/self_use_queue.json
```
C1 total 328 (expected 328, block's 170 + 158). C2 matches its stated
3/1, 9/8, 7/0 exactly. C3 had no stated expectation; total 97.

G6 TREE AND PUSH (after this commit): reported in full in the reply, since
this file cannot contain the reading of its own commit.

## Authored-text proofs

The block copy and the three payload copies (`plan.md`, `records.diff`,
`selfuse.py`), read back at `0f61f735f`, equal the reviewer's originals byte
for byte (see G1 above, all four sha256 matches). `records.diff` was applied
with `git apply` unedited (constraint 1); `.agent/plan.md` was rewritten to
the `plan.md` payload verbatim via `shutil.copyfile`, confirmed byte-identical
by the G2 sha256 reading. `selfuse.py` was run unedited from
`.remedy-wt/f289-r4-payloads/` (never copied into the tracked tree except as
the `.agent/authored/` record).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| BEFORE ANYTHING ELSE 1–4 | done | |
| PAYLOADS verification | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | job completed; item SU-033 ran to `staged_review_passed`, never applied |
| C4 | done | this commit |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | reported in the reply |
| Constraint 1 (no retype, `git apply --check` first) | done | |
| Constraint 2 (every commit under 500 insertions) | done | largest was C1 at 328 |
| Constraint 3 (tracked path set) | done | matches exactly, see reply |
| Constraint 4 (job never applied) | done | `remedy/job-da4583bff80a47f1` branch and `.data/jobs/da4583bff80a47f1` left behind, reported, nothing deleted |
| Constraint 5 (stop only if a non-self-use gate reddens) | done | none reddened |
| Constraint 6 (nothing merged) | done | no PR, no merge, no checkout, no force-push, no stash |
| Constraint 7 (no full suite) | done | only the named selection ran |

`git diff --name-only ad7f57ad` at the branch tip after this commit is
predicted to equal exactly: `.agent/authored/f289-r4-block.md`,
`.agent/authored/f289-r4-plan.md`, `.agent/authored/f289-r4-records.diff`,
`.agent/authored/f289-r4-selfuse.py`, `.agent/live_review.md`,
`.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`,
`scripts/self_use_queue.json`, `.agent/selfuse_f289/SU-033.md`,
`.agent/selfuse_f289/changed_paths.txt`,
`.agent/selfuse_f289/entry_and_job_file.txt`,
`.agent/selfuse_f289/execution_config.txt`,
`.agent/selfuse_f289/full_transcript.txt`,
`.agent/selfuse_f289/result_state.txt`, `.agent/selfuse_f289/run_defects.txt`,
`.agent/selfuse_f289/staleness_after.txt`, `.agent/selfuse_f289/timing.txt`,
`.agent/handoff.md` — the block's constraint-3 set plus this handback, none
of the forbidden paths touched. The literal post-commit reading is reported
in the reply.

## Deviations & assumptions

1. No commit needed to split this round — every commit's insertions stayed
   well under the 500-line cap (the largest was C1 at 328).
2. `.agent/selfuse_f289/staleness_after.txt` reads `NO WORKSPACE` rather than
   a staleness reading, because the self-use runner's own cleanup removed the
   job's worktree before the payload script re-read it — the payload script
   runs `run_staleness_checks()` unconditionally against
   `plan.job_workspace_path` with no guard for a runner that has already
   cleaned up, and the block's own `selfuse.py` is exactly this reviewer
   payload, run unedited. This is a reading to record, not a defect this
   round may repair (constraint: "you write no code"; the payload is
   read-only for the worker). Declared here rather than silently treated as
   a normal staleness reading.
3. The workspace diff and untracked-file listing G4 orders could not be read
   from the job workspace directly (it no longer exists); the job's single
   commit on its own branch `remedy/job-da4583bff80a47f1` is reported instead
   as the equivalent record, with the `fatal:` error reported verbatim first.
4. The self-use run completed in 102.8 seconds, not "most of an hour" — the
   block flagged the possibility, not a requirement; no re-run was performed
   and none was warranted (constraint: never re-run a completed job).
5. No test written by this round was found wrong and corrected; no reviewer
   payload was edited or retyped.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 4
and of the self-use run's diff (the single line on `docs/README.md`, held on
branch `remedy/job-da4583bff80a47f1`, never applied), then the rest of the
closure sequence: the integration gate's one full suite, the evidence
bundle and review package with the Built State, and the closing round.
Open findings: 0. Operator questions: 0.
