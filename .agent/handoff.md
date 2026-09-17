# F281 Round 19 — Handback

## Round Summary

F281 Round 19 complete. Booked round 18's independently-reviewed PASS and registered R-0957 (a MEDIUM regression from round 16 where `_print_root_help`'s default branch dropped the `hidden` filter on group display), then fixed that regression in the same round. All six gates pass with real recorded output. Session 3 continues.

## Commits

| Commit | Message |
|--------|---------|
| 0eb5818a | F281 R19 C1: book round 18 PASS, register R-0957 and resolve, update plan |
| 2e7d5ce4 | F281 R19 C2: restore hidden filter on default remedy --help view |

Final HEAD: 2e7d5ce4

## Changes Summary

**C1 (.agent files and plan update):**
- Appended RECORD18 gate entry to `.agent/live_review.md` with full measurement and verification record for round 18
- Registered R-0957 finding entry: MEDIUM, `_PRINT_ROOT_HELP`'s default view no longer respects hidden groups (contradiction of DECISION amend0905-vocab D4 guarantee)
- Registered Done: R-0957 resolution entry documenting the fix applied in C2
- Replaced `.agent/plan.md` with PLAN19 (round 19 current step, next steps for R-0809's job-id slice, risks)
- Saved authored block to `.agent/authored/f281-r19.md` and mirrored to `.agent/last_block.md`

**C2 (code changes, one file: `apps/cli/grouped.py`):**
- Restored `hidden` filter in `_print_root_help`'s default (non-`--all-commands`) branch at line 373
- Changed from: `groups = [(gid, GROUPS[gid].description) for gid in VISIBLE_GROUP_ORDER]`
- Changed to: multi-line list comprehension with `if not GROUPS[gid].hidden` check
- The `--all-commands` branch already checks `.hidden` correctly and was left untouched
- Fixes R-0957: hidden groups now properly excluded from default `remedy --help` output

## Gate Results (all real output)

**G1 TARGETED** ✓ PASS
- Command: `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py tests/test_help_renderer.py tests/cli/test_cli_ux.py tests/cli/test_golden_path.py tests/cli/test_command_catalog.py -q`
- Output: `488 passed in 37.28s`
- Expected: 488 passed ✓

**G2 CANARY** ✓ PASS
- Command: `python3 -m pytest tests/cli/test_golden_path.py -q`
- Output: `42 passed in 17.64s`
- Expected: 42 passed (unchanged) ✓

**G3 RUFF** ✓ PASS
- Command: `python3 -m ruff check apps/cli/grouped.py`
- Output: `All checks passed!`
- Expected: All checks passed! ✓

**G4 DIRECT MEASUREMENT** ✓ PASS
- Monkeypatched `GROUPS["runtime"]` to `hidden=True`, called `apps.cli.grouped._print_root_help()`, captured output
- Verified: output does NOT contain "runtime" row (correctly hidden)
- Verified: output still contains "stats" row (not affected by fix)
- Expected: both conditions met ✓

**G5 MUTATION RED-PROOF** ✓ PASS
- Disposable worktree created at HEAD (2e7d5ce4) with fix applied
- Step 1: `python3 -m pytest tests/cli/test_cli_ux.py::TestHiddenGroup -q` reads `5 passed` ✓
- Step 2: Reverted fix back to FROM text (single-line comprehension without hidden filter)
- Step 3: Re-ran tests: exactly ONE failure, `test_a_hidden_group_is_absent_from_the_default_help`, result `1 failed, 4 passed` ✓
- Step 4: Re-applied fix and re-ran: `5 passed` ✓
- Step 5: Worktree deleted; primary checkout untouched

**G6 TREE** ✓ PASS
- `git status --porcelain` empty
- `git worktree list` shows 1 row (primary checkout): `/home/decodeux/Repos/remedy  2e7d5ce4 [feature/f281-cli-help-surface]`
- HEAD 2e7d5ce4 matches `origin/feature/f281-cli-help-surface` after push ✓

## Findings

R-0957 (MEDIUM, `_PRINT_ROOT_HELP`'s default view no longer respects hidden groups) was discovered during round 19's safety-net broadening while running `tests/cli/test_cli_ux.py` for the first time since round 16. The defect was introduced by round 16's C2 (commit `d46da12f`) which rewrote the default branch to iterate `VISIBLE_GROUP_ORDER` unconditionally without the `hidden` check. Root cause of the multi-round miss: neither round 16's own G1 gate list (`tests/test_command_catalog.py`, `tests/test_grouped_cli.py`, `tests/test_help_renderer.py`) nor any later round's canary (`tests/cli/test_golden_path.py`) ever ran `tests/cli/test_cli_ux.py`, the one file exercising the DYNAMIC `hidden` flag path. The finding is registered in `.agent/live_review.md` and marked RESOLVED in the same record. No new findings in round 19 itself.

## Next Action

Round 20 should author R-0809's job-id slice, fully researched and named in PLAN19's Next Steps. The fix:
- Modify `packages/orchestration/data_paths.py`'s `resolve_job_id` except block
- Replace 18 duplicated `except ValueError: print(f"Error: invalid job ID: {job_id_str!r}", ...)` sites across `brain.py` (11), `snapshot_cmds.py` (2), `test_cmds.py` (2), `file.py` (1), `event.py` (1), `memory.py` (1) with unified message `Error: No job matches '<id>'. Try: remedy job list.`
- Update tests in `tests/test_data_paths.py` (2 assertions), `tests/test_brain_viewer.py`, `tests/test_context_coverage.py`, `tests/cli/test_product_spine.py`, `tests/cli/test_teacher_cmd.py` (2 assertions)
- Do NOT touch `job_stop_cmd.py`'s or `project.py`'s "job not found" wording (different failure semantics)
- R-0809 stays OPEN after this slice (run-id and mission-id still need unification)

Open Acceptance items remaining: R-0805 (ui status dead-session pruning, needs design pass), R-0809 (id-error messages, job-id slice ready, run/mission still pending), R-0895 (README quickstart).

## Deviations & Assumptions

None. Block executed exactly as written. The single FROM string in C2 matched on first attempt. C2 edit applied cleanly. All six gates passed with recorded real output. Tree clean and pushed.
