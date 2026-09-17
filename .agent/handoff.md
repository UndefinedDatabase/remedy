# F281 Round 23 — Handback

## Round Summary

F281 Round 23 complete. This is F281's fourth session. C1 booked round 22's independently-reviewed PASS and updated the plan. C2 landed R-0809's "job not found" family unification across TEN sites in SEVEN files: consolidating the single-source `JobNotFoundError` message that reaches 34 call sites across orchestration paths, plus five hardcoded test-command variants, plus four project/context/stop-command variants. All unified under `Error: No job matches '<id>'. Try: remedy job list.` R-0809 remains OPEN with only one wording family remaining: the mission wording in `mission_cmd.py`'s `_load_mission_or_exit`. All six gates pass. Session 4 continues.

## Commits Table

| Commit | Message |
|--------|---------|
| 7a62b95e | F281 R23 C1: book round 22 PASS, update plan |
| 3acdb00a | F281 R23 C2: land R-0809 job-not-found family across 10 sites |

Final HEAD: 3acdb00a

## Changes Summary

**C1 (.agent files and plan update):**
- Appended F281 R22 PASS verdict paragraph to `.agent/live_review.md`
- Replaced entire `.agent/plan.md` with updated PLAN23 (current step reflects R-0809 job-not-found work, next steps for mission wording measurement and fix, R-0805, R-0895, risks)
- Saved F281 R22 ledger paragraph to `.agent/authored/f281-r23.md`
- Mirrored same paragraph to `.agent/last_block.md`

**C2 (code changes and test updates, 10 production sites + 3 test files):**

*Production files (7 files, 10 sites):*
1. `packages/orchestration/pingpong_job.py` (line 450): `JobNotFoundError.__init__` message changed from `f"Job not found: {job_id}"` to `f"No job matches {job_id!r}. Try: remedy job list."` — reaches 34 call sites via `str(exc)` across brain.py, change.py, decision.py, event.py, file.py, job.py, patch.py
2. `apps/cli/commands/test_cmds.py` (line 200): message changed from `f"Error: job {job_id_str!r} not found."` to `f"Error: No job matches {job_id_str!r}. Try: remedy job list."`
3. `apps/cli/commands/snapshot_cmds.py` (line 38): message changed (snapshot error at line 47 left unchanged)
4. `apps/cli/commands/snapshot_cmds.py` (line 114): message changed
5. `apps/cli/commands/job.py` (line 2060): message changed from `f"Error: job {job_id!r} not found."` to `f"Error: No job matches {job_id!r}. Try: remedy job list."`
6. `apps/cli/commands/job.py` (line 2302): message changed (same TO text)
7. `apps/cli/commands/project.py` (line 160): message changed from `f"ERROR: job not found: {job_id_str}"` to `f"Error: No job matches {job_id_str!r}. Try: remedy job list."`
8. `apps/cli/commands/project.py` (line 456): message changed from `f"Error: job not found: {resolved_id[:8]}"` to `f"Error: No job matches {resolved_id[:8]!r}. Try: remedy job list."`
9. `apps/cli/commands/job_context_cmd.py` (line 275): message changed from `f"Job not found: {job_id_str}"` to `f"Error: No job matches {job_id_str!r}. Try: remedy job list."`
10. `apps/cli/commands/job_stop_cmd.py` (line 69): message changed from `f"Error: job not found: {job_id}"` to `f"Error: No job matches {job_id!r}. Try: remedy job list."`

*Test files (3 files):*
1. `tests/orchestration/test_resume_cli.py` (line 334): assertion changed from `"Job not found"` to `"No job matches"`
2. `tests/cli/test_job_report.py` (line 246): assertion changed from `"Error: Job not found: ffffffff-ffff-4fff-8fff-ffffffffffff"` to `"Error: No job matches 'ffffffff-ffff-4fff-8fff-ffffffffffff'. Try: remedy job list."`
3. `tests/cli/test_job_budget_set.py` (line 149): assertion changed from `f"Error: job {missing!r} not found.\n"` to `f"Error: No job matches {missing!r}. Try: remedy job list.\n"`

## Gate Results (all real output)

**G1 TARGETED** ✓ PASS
```
python3 -m pytest tests/orchestration/test_resume_cli.py tests/cli/test_job_report.py tests/cli/test_job_budget_set.py tests/cli/test_job_context_cmd.py tests/cli/test_job_stop.py tests/cli/test_snapshot_cli_runtime.py tests/test_cli_main.py tests/test_data_paths.py tests/cli/test_scoped_listings.py tests/test_command_discovery.py -q
Result: 357 passed in 19.84s
```

**G2 CANARY** ✓ PASS
```
python3 -m pytest tests/cli/test_golden_path.py -q
Result: 42 passed in 17.72s (unchanged)
```

**G3 RUFF** ✓ PASS
```
python3 -m ruff check packages/orchestration/pingpong_job.py apps/cli/commands/test_cmds.py apps/cli/commands/snapshot_cmds.py apps/cli/commands/job.py apps/cli/commands/project.py apps/cli/commands/job_context_cmd.py apps/cli/commands/job_stop_cmd.py
Result: All checks passed!
```

**G4a SWEEP** ✓ PASS
```
grep -rn "job not found\|Job not found" apps/ packages/ tests/ --include=*.py | wc -l
Result: 21 (13 internal strings in self_dogfood_execution.py, mission_readiness.py x2, repair_request_builder.py, test_execution_service.py, self_dogfood.py, repair_loop.py x2, repository_snapshot.py, task_execution.py, real_test_execution.py, ui_server.py x2; 8 test survivors in test_digest_route.py x2, test_sse_stream.py x3, conftest.py docstring, test_command_channel.py x2 — all unrelated to CLI stderr prints)
```

**G4b SWEEP** ✓ PASS
```
grep -rn '!r} not found\.' apps/ tests/ --include=*.py | wc -l
Result: 1 (snapshot_cmds.py line 47, snapshot-specific, unchanged)
```

**G5 MUTATION RED-PROOF** ✓ PASS
- Disposable worktree created at HEAD (3acdb00a) with C2 applied
- Step 1: `python3 -B -m pytest tests/cli/test_job_report.py::TestUnknownJob::test_it_exits_cleanly_without_a_traceback -q` reads `1 passed` ✓
- Step 2: Reverted line 450 in worktree to old `f"Job not found: {job_id}"` message
- Step 3: Re-ran test: `1 failed` (assertion expected new wording but got old wording in error output) ✓
- Step 4: Reverted the revert (re-applied fix): test reads `1 passed` ✓
- Step 5: Worktree deleted; primary checkout clean

**G6 TREE** ✓ PASS
```
git status --porcelain
Result: (empty)

git worktree list
Result: 1 row (primary checkout)

HEAD: 3acdb00a
Remote: origin/feature/f281-cli-help-surface matches after push
```

## Findings

No new findings this round. R-0809 remains in progress:

**R-0809 Completion Status:**
- ✓ Round 20: "invalid job ID" wording (resolved)
- ✓ Round 20: "no job matches prefix" wording (resolved)
- ✓ Round 22: "run '...' not found." wording (resolved)
- ✓ Round 23: All "job not found" / "Job not found" variants across 10 sites (resolved this round)
- ⚠ REMAINS: mission wording in `mission_cmd.py`'s `_load_mission_or_exit` (two-line message: `"Error: no mission {mission_id} in this project."` + separate hint)

## Next Action

**R-0809 measurement pass on final piece (mission wording):** Before authoring the fix, find:
1. Every caller of `_load_mission_or_exit` to understand scope
2. Every test that asserts or pins the current two-line wording
3. Confirm unified message design (`Error: No mission matches '<id>'. Try: remedy mission list.`)

Once measurement is complete, the fix can be authored and R-0809 closure confirmed by fresh repo-wide grep that all five wordings (job, run, mission variants) are gone.

**Alternative paths:** R-0805 (ui status dead-session pruning) awaits design pass on session-state model. R-0895 (README quickstart) runs last after vocabulary settles. Session 4 continues within amend0905-throughput budget (6-to-8 target).

## Deviations & Assumptions

None. All 10 FROM strings confirmed by grep at exact locations and counts. All 10 edits applied cleanly. All six gates passed with recorded real output. Mutation red-proof (independent worktree test/revert/re-apply/test cycle) confirmed the high-leverage exception-message fix is load-bearing and reachable through `job show`'s path. Tree clean and pushed. Session 4 continues.
