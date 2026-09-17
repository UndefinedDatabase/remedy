# F281 Round 21 — Handback

## Round Summary

F281 Round 21 complete. Booked round 20's independently-reviewed PASS and registered/resolved R-0958 (a LOW pre-existing defect found while researching R-0809's remaining scope: `remedy job stop` on an unknown job id prints TWO contradictory error lines for one failure). The fix removes only a redundant duplicate print, not any of the "job not found:" / "run '...' not found." wordings R-0809 still names. All six gates pass. Session 4 continues.

## Commits Table

| Commit | Message |
|--------|---------|
| dc867577 | F281 R21 C1: book round 20 PASS, register and resolve R-0958, update plan |
| df9747f7 | F281 R21 C2: fix R-0958 — remove duplicate error print in job stop |

Final HEAD: df9747f7

## Changes Summary

**C1 (.agent files and plan update):**
- Appended RECORD20 gate entry to `.agent/live_review.md` with full measurement and verification record for round 20
- Registered R-0958 finding (LOW: duplicate error print in `job_stop_cmd.py`)
- Registered Done: R-0958 resolution (C2 fixes it)
- Replaced `.agent/plan.md` with PLAN21 (round 21 current step, next steps for R-0809's remaining wordings measurement, R-0805, R-0895, risks)
- Saved authored block to `.agent/authored/f281-r21.md` and mirrored to `.agent/last_block.md`

**C2 (code changes and test updates, 2 files):**
- `apps/cli/commands/job_stop_cmd.py` (lines 90–97): Replaced the `except SystemExit` handler's call to `_unknown_job()` with inline JSON printing (when `json_output` is set) followed by direct `raise SystemExit(EXIT_UNKNOWN_JOB)` — eliminates duplicate human-readable print while preserving exit code and JSON payload behavior
- `tests/cli/test_job_stop.py` (line 176): Replaced loose substring assertion with exact-equality check: `assert capsys.readouterr().err == "Error: No job matches '0123456789abcdef'. Try: remedy job list.\n"` — test now fails if either the duplicate returns or the message drifts
- Deliberately left untouched: `_unknown_job()` definition and its two other call sites (neither follows a prior print); JSON-mode sibling test; "job not found:" wording in `job_stop_cmd.py:69` and `project.py` (semantically different failure path)

## Gate Results (all real output)

**G1 TARGETED** ✓ PASS
- Command: `python3 -m pytest tests/cli/test_job_stop.py -q`
- Output: `26 passed in 0.35s`
- Expected: all pass ✓

**G2 CANARY** ✓ PASS
- Command: `python3 -m pytest tests/cli/test_golden_path.py -q`
- Output: `42 passed in 17.63s`
- Expected: 42 passed (unchanged) ✓

**G3 RUFF** ✓ PASS
- Command: `python3 -m ruff check apps/cli/commands/job_stop_cmd.py`
- Output: `All checks passed!`
- Expected: All checks passed! ✓

**G4 DIRECT MEASUREMENT** ✓ PASS
- Test 1 (text output): Temporary REMEDY_DATA_DIR, call `_cmd_job_stop("deadbeefdeadbeef")` with stderr captured
  - Exit code: `3` (EXIT_UNKNOWN_JOB) ✓
  - Stderr: `"Error: No job matches 'deadbeefdeadbeef'. Try: remedy job list.\n"` (exactly one line) ✓
- Test 2 (JSON output): Same call with `json_output=True`
  - Exit code: `3` ✓
  - JSON payload: `{"ok": false, "error": "job_not_found", "job_id": "deadbeefdeadbeef"}` ✓

**G5 MUTATION RED-PROOF** ✓ PASS
- Disposable worktree created at HEAD (df9747f7) with C2 applied
- Step 1: `python3 -m pytest tests/cli/test_job_stop.py::TestItRefusesToLie::test_an_unknown_job_exits_3 -q` reads `1 passed` ✓
- Step 2: Reverted fix to restore old `_unknown_job()` call
- Step 3: Re-ran test: `1 failed` (assertion expected one line but got two: the resolve_job_id print + the _unknown_job print) ✓
- Step 4: Re-applied fix and re-ran: `1 passed` ✓
- Step 5: Worktree deleted with --force; primary checkout untouched

**G6 TREE** ✓ PASS
- `git status --porcelain` empty
- `git worktree list` shows 1 row (primary checkout)
- HEAD df9747f7 matches `origin/feature/f281-cli-help-surface` after push ✓

## Findings

### R-0958 — Resolved (C2)

**Severity:** Low  
**Defect:** `remedy job stop` on an unknown job id prints TWO contradictory error lines for one failure.

**Root Cause:** Pre-dates round 20. `resolve_job_id()` prints a human message to stderr and exits with code 1. The caller at `job_stop_cmd.py:97` catches that exit, swallows it, then calls `_unknown_job()`, which prints a different error message to stderr and raises `SystemExit(EXIT_UNKNOWN_JOB)` with code 3. Net result: stderr contains two different error messages for the same failure.

**Why Low:** Exit code (3) and JSON payload (`"job_not_found"`) are both correct; only stderr text is doubled, a cosmetic redundancy that is confusing but not misleading (both lines agree the job does not exist).

**Fix Verification:** Mutation red-proof confirms the fix is load-bearing. Test `test_an_unknown_job_exits_3` now asserts stderr equals exactly one line and fails if either line is missing or doubled.

**Impact on R-0809:** None — R-0809 names four former wordings, and this fix removes only a DUPLICATE print of a wording already replaced in round 20, not one of the three remaining wordings R-0809's scope still covers ("job not found:" for well-formed ids with missing records; "run '...' not found." for distinct id kind; existing "job not found:" message in two other call sites untouched by this round).

## Next Action

**R-0809 remains OPEN and UNCHANGED in scope** — measure and author its remaining wordings ("job not found:" and "run '...' not found.") with a dedicated measurement pass before touching either, OR defer R-0809 and move on to R-0805 (ui status dead-session pruning, needs design pass) OR R-0895 (README quickstart).

Open Acceptance items remaining: R-0805 (needs design pass), R-0809 (job-id slice done; run/mission/run-id wording slices measured or pending), R-0895 (README quickstart).

## Deviations & Assumptions

None. Block executed exactly as written. Both FROM strings in job_stop_cmd.py and test_job_stop.py matched on first attempt. All edits applied cleanly. All six gates passed with recorded real output. Mutation red-proof confirmed the fix is load-bearing. Tree clean and pushed. Session 4 continues within amend0905-throughput budget.
