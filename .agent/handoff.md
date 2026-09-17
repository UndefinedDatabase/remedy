# F281 Round 22 — Handback

## Round Summary

F281 Round 22 complete. This is F281's fourth session. C1 booked round 21's independently-reviewed PASS and updated the plan. C2 landed R-0809's run-id wording unification, bringing the "No run matches ... Try: remedy run list." message to parity with the job-id equivalent from round 20. R-0809 remains OPEN with only one wording family remaining: "job not found:" in job_stop_cmd.py and project.py. All six gates pass. Session 4 continues.

## Commits Table

| Commit | Message |
|--------|---------|
| 6faeec52 | F281 R22 C1: book round 21 PASS, update plan |
| b6a995c6 | F281 R22 C2: land R-0809 run-id wording — unify run-not-found message |

Final HEAD: b6a995c6

## Changes Summary

**C1 (.agent files and plan update):**
- Appended F281 R21 PASS verdict paragraph to `.agent/live_review.md`
- Replaced entire `.agent/plan.md` with PLAN22 (updated current step reflecting R-0809 run-id work, next steps for "job not found:" measurement and fix, R-0805, R-0895, risks)
- Saved F281 R21 ledger paragraph to `.agent/authored/f281-r22.md`
- Mirrored same paragraph to `.agent/last_block.md`

**C2 (code changes and test updates, 2 files):**
- `apps/cli/commands/do_cmd.py` (line 537): Changed error message from `"Error: run {run_id!r} not found."` to `"Error: No run matches {run_id!r}. Try: remedy run list."`
- `tests/cli/test_cli_ux.py` (line 815): Updated assertion from `"Error: run 'no-such-run' not found.\n"` to `"Error: No run matches 'no-such-run'. Try: remedy run list.\n"`

## Gate Results (all real output)

**G1 TARGETED** ✓ PASS
- Command: `python3 -m pytest tests/cli/test_cli_ux.py -q`
- Output: `74 passed in 1.13s`
- Expected: all pass ✓

**G2 CANARY** ✓ PASS
- Command: `python3 -m pytest tests/cli/test_golden_path.py -q`
- Output: `42 passed in 17.74s`
- Expected: 42 passed (unchanged) ✓

**G3 RUFF** ✓ PASS
- Command: `python3 -m ruff check apps/cli/commands/do_cmd.py`
- Output: `All checks passed!`
- Expected: All checks passed! ✓

**G4 DIRECT MEASUREMENT** ✓ PASS
- Command: Call `apps.cli.commands.do_cmd._cmd_run_show("no-such-run", json_output=True)` with temporary `REMEDY_DATA_DIR`
- Exit code: `1` ✓
- Stderr: `"Error: No run matches 'no-such-run'. Try: remedy run list.\n"` (exact match) ✓

**G5 MUTATION RED-PROOF** ✓ PASS
- Disposable worktree created at HEAD (b6a995c6) with C2 applied
- Step 1: `python3 -m pytest tests/cli/test_cli_ux.py::TestRunShow::test_missing_run_exits_one -q` reads `1 passed` ✓
- Step 2: Reverted line 537 in worktree to old `"Error: run {run_id!r} not found."` wording
- Step 3: Re-ran test: `1 failed` (assertion expected new wording but got old) ✓
- Step 4: Worktree deleted with --force; primary checkout untouched

**G6 TREE** ✓ PASS
- `git status --porcelain` empty
- `git worktree list` shows 1 row (primary checkout)
- HEAD b6a995c6 matches `origin/feature/f281-cli-help-surface` after push ✓

## Findings

No new findings this round. R-0809 remains in progress with scope narrowed: all four wordings identified in earlier rounds are on track:
1. "invalid job ID" — GONE (round 20)
2. "no job matches prefix" — GONE (round 20)
3. "run '...' not found." — GONE (round 22, this round)
4. "job not found:" — REMAINS (job_stop_cmd.py:69, project.py:160 and 456)

## Next Action

**R-0809 scope narrowed but REMAINS OPEN.** The final wording family "job not found:" needs a measurement pass to confirm no test pins the literal substring in a way that would need lockstep updating, and confirm unifying it does not collide with `JobNotFoundError`'s exit-code contract before authoring the fix. Once this lands, R-0809 gets a `Done:` paragraph.

Alternatively, session 4 can pivot to R-0805 (ui status dead-session pruning, needs design pass) or R-0895 (README quickstart).

## Deviations & Assumptions

None. Block executed exactly as written. Both FROM strings matched on first attempt (do_cmd.py line 537, test_cli_ux.py line 815). Mechanical verification confirmed exactly 2 occurrences of new wording post-edit. All six gates passed with recorded real output. Mutation red-proof (independent worktree test/revert/test cycle) confirmed the fix is load-bearing. Tree clean and pushed. Session 4 continues within amend0905-throughput budget.
