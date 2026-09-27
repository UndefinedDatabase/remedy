# Handoff — F288, round 7

## Session

SESSION 2 of feature F288 · round 7 · rounds so far 7. Context remaining at
handback: comfortable — this round ran five straight-line commits (three
payload applications, one long provider-calling self-use run, and this
handoff) with no repair loop and no mutation-tool authoring, so a full
context window remains for the next round.

## Range

Review of `2f49da5c`..`HEAD` (`HEAD` is this handback's own commit, `F288
R7 C5`, on `feature/f288-event-stream-completeness`).

## Commits

### da5b2fe0c F288 R7 C1: copy round 7 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r7-block.md | 187/0 | copy of this round's block |
| .agent/authored/f288-r7-built_state.diff | 79/0 | copy of the built_state payload |
| .agent/authored/f288-r7-plan.md | 29/0 | copy of the plan payload |
| .agent/authored/f288-r7-records.diff | 29/0 | copy of the records payload |
| .agent/authored/f288-r7-selfuse.py | 121/0 | copy of the reviewer's C4 script |

Measured insertions: 445 (block's own line count 187 + 258), matching the
block's expectation exactly, under the 500-line cap.

### 15b2dde11 F288 R7 C2: book round 6, consolidate the checklist, plan round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | round 6's Gate entry (VERDICT PASS), appended verbatim from the handoff |
| .agent/plan.md | 9/9 | round 7's plan (payload rewrite) |
| docs/agents/planner_reviewer_prompt.md | 8/0 | closure's consolidation paragraph, checklist stays at 34 items |

Matches the block's expected numstat (2/0, 9/9, 8/0) exactly.

### 78e53297a F288 R7 C3: write the Built State
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F288.md | 71/0 | `## Built State (F288, 2026-09-27)` section, closure precondition 4 |

Matches the block's expected numstat (71/0) exactly.

### 11212c6eb F288 R7 C4: generate and run the closure's self-use item, record its readings
| Path | +/- | Reason |
|---|---|---|
| .agent/selfuse_f288/SU-034.md | 13/0 | the generated item's job file |
| .agent/selfuse_f288/changed_paths.txt | 1/0 | the job's one changed path |
| .agent/selfuse_f288/entry_and_job_file.txt | 5/0 | entry id/title/provenance/consumed_by, job file path |
| .agent/selfuse_f288/execution_config.txt | 39/0 | the `self_use` role's execution config (provider `claude-cli`, never `fake`) |
| .agent/selfuse_f288/full_transcript.txt | 14/0 | job/task summary |
| .agent/selfuse_f288/job_diff.txt | 13/0 | the job branch's diff against HEAD |
| .agent/selfuse_f288/result_state.txt | 12/0 | job id/state, budgets, budget actuals, task states |
| .agent/selfuse_f288/run_defects.txt | 1/0 | `describe_self_use_run_defects()` — NONE |
| .agent/selfuse_f288/staleness_after.txt | 2/0 | doc-staleness catalog read from the job branch after the run — NONE |
| .agent/selfuse_f288/timing.txt | 3/0 | start/finish/wall-seconds |
| scripts/self_use_queue.json | 8/0 | the generated item SU-034 appended, `consumed_by` empty |

111 insertions total, under the 500-line cap. No insertion count was
expected by the block for C4.

### F288 R7 C5: rewrite handoff for round 7 (this commit — a handoff cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `python3 .remedy-wt/f288-r7-payloads/selfuse.py`, run in the primary
  checkout via `bash -c 'python3 ... | tee .remedy-wt/f288-r7-worker/selfuse.log; echo
  "REAL_EXIT=${PIPESTATUS[0]}"'` — real exit 0. Ran the `self_use` role's
  provider twice (`pingpong_live`), created job `8356faebdc904fd1` and its
  branch `remedy/job-8356faebdc904fd1`, and a job workspace at
  `/home/decodeux/Repos/remedy/.remedy-wt/job-8356faebdc904fd1` (script's own
  scratch, never touched further). The job branch and its workspace are left
  behind per constraint 4 — nothing was applied, nothing was deleted that
  this round did not create as scratch.
- `git push -u origin feature/f288-event-stream-completeness` — reported
  under G6 in this round's reply (run after this file is committed).
- No `gh pr create`, no `gh pr merge`, no branch deletion, no force-push, no
  `git stash`, no `git checkout`/`git switch` in the primary checkout.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `plan.md`: 29 lines, 1078 bytes, sha256
  `83d89f6f4ada45dfdb44ad46a5689b4ed22a3665096f1d95fa15ea5493a8fd0a`.
- `records.diff`: 29 lines, 11008 bytes, sha256
  `ec3ec0281e0ccc78f543f524b77f7b9d02050598afe40167b7b11934610f8bbc`.
- `built_state.diff`: 79 lines, 5968 bytes, sha256
  `5efb7f4142289d3e399a80e0197a4344bef197366b50f1f8a984c09dffdf527e`.
- `selfuse.py`: 121 lines, 6420 bytes, sha256
  `f70612e69c39682b41e11168ecbeffb785af00cdcf306d13dd50d541e5ceffce`.
- Block: 187 lines, sha256
  `bd5a5d0ea643bab9dcc7ac097fe6109040ec5eb53f3cfd0d1fa789359d8f65a2` — MATCH
  against both readings the delegation message stated.

Each `.agent/authored/f288-r7-*` copy, read back with `git show
da5b2fe0c:<path>`, compared byte-for-byte against its source: block copy vs
`.remedy-wt/f288-r7/block.md` (13671 bytes both sides); `plan.md` copy vs
the payload (1078 bytes both sides); `records.diff` copy vs the payload
(11008 bytes both sides); `built_state.diff` copy vs the payload (5968
bytes both sides); `selfuse.py` copy vs the payload (6420 bytes both
sides). All five `bytes_equal=True`.

### G2 — THE BOOKKEEPING AND THE BUILT STATE
`git show <commit>:<path>`, bytes and sha256, each MATCHING the reviewer's
reading exactly:
```
15b2dde11 .agent/live_review.md                  bytes=322392 3e122392b3f04cba97655c57d7b9eb5356c51304e8104ab92610bf0488395721
15b2dde11 docs/agents/planner_reviewer_prompt.md  bytes=105869 61fab16e0c8c77c10d1979f2c84ea2de8a98504c6b29dcfaa0c92e72dd1e90a6
15b2dde11 .agent/plan.md                          bytes=1078   83d89f6f4ada45dfdb44ad46a5689b4ed22a3665096f1d95fa15ea5493a8fd0a
78e53297a docs/roadmap/features/T5_F288.md        bytes=8149   464873a969d453a721602df901e02c67dbd364634564177ee76501a740a2f49d
```
Open set (`open_finding_ids` from `scripts/rotate_live_review.py`, imported
with `scripts` on `sys.path`, over `.agent/live_review.md`'s text): at
`2f49da5c` → `[]`; at `15b2dde11` (C2) → `[]`. Both empty, matching the
reviewer's reading.

### G3 — THE TESTS
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_doc_staleness.py
  tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py
  tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_findings.py
  tests/orchestration/test_self_use_job.py tests/orchestration/test_live_review_rotation.py
  tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py
  tests/orchestration/test_test_runner.py tests/test_agent_tooling.py tests/cli/test_golden_path.py
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md
  was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1,
  docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there.
  Backlog: re-pin this contract on the split-workflow docs, or retire the test.
690 passed, 1 skipped in 80.40s (0:01:20)
REAL_EXIT=0
```
The reviewer's simulation tree at C3 read `689 passed, 2 skipped`, the
second skip being `tests/orchestration/test_test_runner.py:414` (no
`apps/ui/node_modules` in the simulation tree). In THIS primary checkout
that node has `apps/ui/node_modules` and ran for real: 689+1=690 passed,
2-1=1 skipped — the one remaining skip is the same standing
`test_agent_tooling.py:43` quarantine the reviewer also read. Counts
reconcile exactly.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=161"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0 by STATUS, not merely exit code.

### G4 — THE SELF-USE READINGS
Full command and output (verbatim, C4):
```
$ bash -c 'python3 .remedy-wt/f288-r7-payloads/selfuse.py 2>&1 | tee .remedy-wt/f288-r7-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'
generate_and_append_if_empty(): ('SU-034', 'Fix stale documentation: config_cli_table_complete in
  docs/guides/remedy-toml-user-guide.md', 'generated (self-use-generator tier 2, doc staleness,
  config_cli_table_complete:docs/guides/remedy-toml-user-guide.md:the CLI commands table never
  documents the `config` subcommand `show`)')
next_self_use_item(): SU-034 Fix stale documentation: config_cli_table_complete in
  docs/guides/remedy-toml-user-guide.md generated (self-use-generator tier 2, doc staleness, ...)
REAL_EXIT=0
```
Item id `SU-034` — MATCHES the reviewer's simulation-tree reading exactly
(Tier 2, doc staleness, the same claim about `config show`).

Job id `8356faebdc904fd1`, state `completed`. Builder and reviewer provider:
`claude-cli` (both `builder` and `reviewer` keys), model `claude-sonnet-4-6`,
effort `medium` — the `self_use` role's configured provider, never `fake`.

Budgets: `{"deadline": null, "max_cost_usd": 6.0, "max_provider_calls": 8,
"max_total_tokens": null, "max_wall_clock_minutes": null,
"min_free_disk_bytes": null}`.
Budget actuals: `{"actual_call_count": 2, "actual_sources":
["pingpong_live"], "measured_cost_usd": 1.0727937, "priced_call_count": 2,
"provider_call_count": 2, "schema_version": "2.0.0", "started_at":
"2026-09-27T03:30:07.515292+00:00", "total_tokens": 7984,
"unmeasured_call_count": 0, "unpriced_call_count": 0}`.

Task states: `T001: applied_to_job_workspace (verdict: pass; final_status:
staged_review_passed; repair_rounds_used: 0; run_id: dc4b978959f643b6)`.
Wall time 129.5 seconds (started 2026-09-27T03:30:07Z, finished
2026-09-27T03:32:16Z).

`.agent/selfuse_f288/changed_paths.txt` (verbatim):
```
docs/guides/remedy-toml-user-guide.md
```

`.agent/selfuse_f288/staleness_after.txt` (verbatim):
```
Read from: the job branch remedy/job-8356faebdc904fd1
NONE
```

`.agent/selfuse_f288/job_diff.txt` (verbatim):
```
$ git diff HEAD...remedy/job-8356faebdc904fd1  (exit 0)
diff --git a/docs/guides/remedy-toml-user-guide.md b/docs/guides/remedy-toml-user-guide.md
index e5ebc84b5..b90194558 100644
--- a/docs/guides/remedy-toml-user-guide.md
+++ b/docs/guides/remedy-toml-user-guide.md
@@ -77,6 +77,7 @@ temperature = 0.2
 | Command | Description |
 |---------|-------------|
 | `remedy config list` | List all keys with values and sources |
+| `remedy config show` | Alias for `config list` |
 | `remedy config list --json` | Same, as JSON |
 | `remedy config get <key>` | Show value, source, env var, type for one key |
 | `remedy config sources` | Show which config files are loaded |
```

`.agent/selfuse_f288/run_defects.txt` (verbatim):
```
NONE
```

`git worktree list | wc -l` after the run: 61 (unchanged from step 4's
reading before the run). `git branch --list 'remedy/*' | wc -l` after the
run: 197 (up from 196 at step 4, the one new `remedy/job-8356faebdc904fd1`
branch the run created and the block permits leaving behind).

### G5 — SIZES
```
$ git show --numstat --format= da5b2fe0c   (C1)
187  0  .agent/authored/f288-r7-block.md
79   0  .agent/authored/f288-r7-built_state.diff
29   0  .agent/authored/f288-r7-plan.md
29   0  .agent/authored/f288-r7-records.diff
121  0  .agent/authored/f288-r7-selfuse.py

$ git show --numstat --format= 15b2dde11   (C2)
2  0  .agent/live_review.md
9  9  .agent/plan.md
8  0  docs/agents/planner_reviewer_prompt.md

$ git show --numstat --format= 78e53297a   (C3)
71  0  docs/roadmap/features/T5_F288.md

$ git show --numstat --format= 11212c6eb   (C4)
13  0  .agent/selfuse_f288/SU-034.md
1   0  .agent/selfuse_f288/changed_paths.txt
5   0  .agent/selfuse_f288/entry_and_job_file.txt
39  0  .agent/selfuse_f288/execution_config.txt
14  0  .agent/selfuse_f288/full_transcript.txt
13  0  .agent/selfuse_f288/job_diff.txt
12  0  .agent/selfuse_f288/result_state.txt
1   0  .agent/selfuse_f288/run_defects.txt
2   0  .agent/selfuse_f288/staleness_after.txt
3   0  .agent/selfuse_f288/timing.txt
8   0  scripts/self_use_queue.json
```
C1 measured insertions: 445, expected 445 (187+258) — MATCH. C2 measured
2/0, 9/9, 8/0 — MATCH against the block's stated numstat. C3 measured
71/0 — MATCH against the block's stated numstat. C4: no insertion count
was expected by the block; measured 111 total, under the 500-line cap.

## Authored-text proofs

- Block copy (`.agent/authored/f288-r7-block.md`, at `da5b2fe0c`) vs
  `.remedy-wt/f288-r7/block.md`: byte-identical (13671 bytes both sides).
- `plan.md` copy vs `.remedy-wt/f288-r7-payloads/plan.md`: byte-identical
  (1078 bytes both sides).
- `records.diff` copy vs `.remedy-wt/f288-r7-payloads/records.diff`:
  byte-identical (11008 bytes both sides); applied via `git apply` with
  `--check` and the real apply both exit 0; never edited or retyped.
- `built_state.diff` copy vs `.remedy-wt/f288-r7-payloads/built_state.diff`:
  byte-identical (5968 bytes both sides); applied via `git apply` with
  `--check` and the real apply both exit 0; never edited or retyped.
- `selfuse.py` copy vs `.remedy-wt/f288-r7-payloads/selfuse.py`:
  byte-identical (6420 bytes both sides); run verbatim from the primary
  checkout, never edited.
- `.agent/plan.md` after the payload rewrite: sha256
  `83d89f6f4ada45dfdb44ad46a5689b4ed22a3665096f1d95fa15ea5493a8fd0a`,
  matching the payload's own reading exactly.

## Deviations & assumptions

None. Every commit landed in the block's own order (C1, C2, C3, C4, C5),
every `git apply --check` and real apply exited 0 on the first try, no
commit approached the 500-line cap, the self-use item generated and its
id matched the reviewer's simulation-tree reading exactly, the job ended
`completed`/`staged_review_passed` with no Python exception, and no gate
went red. Every reading in this handback is real and measured, not
expected.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 7 and
of the self-use run's diff, then the rest of the closure sequence. Open
findings: 0. Operator questions: 0.
