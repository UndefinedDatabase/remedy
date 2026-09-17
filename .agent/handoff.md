# F281 Round 18 — Handback

## Round Summary

F281 Round 18 complete. Booked round 17's independently-reviewed PASS (one LOW finding, R-0956: trailing newline dropped in `.agent/decisions.md`), fixed that finding, and resolved R-0934 (advertised-flag scanner missed flags after quoted arguments due to regex treating opening quote as immediate command-line end).

## Commits

| Commit | Message |
|--------|---------|
| 43602cef | F281 R18 C1: book round 17 PASS (finding R-0956), fix .agent/decisions.md trailing newline, resolve R-0934, update plan |
| edc7ad59 | F281 R18 C2: resolve R-0934 — flag scanner now skips quoted arguments |

Final HEAD: edc7ad59

## Changes Summary

**C1 (.agent files and plan update):**
- Fixed `.agent/decisions.md`: appended exactly one `\n` byte to file ending in `paragraph.` (R-0956 resolution)
- Appended R17 gate entry to `.agent/live_review.md` with full measurement and verification record
- Registered R-0956 finding entry documenting the trailing-newline defect
- Registered R-0934 Done entry (resolved in C2)
- Replaced `.agent/plan.md` with PLAN18 (current step, next steps per R-0809/R-0805/R-0895, risks)
- Saved authored block to `.agent/authored/f281-r18.md` and mirrored to `.agent/last_block.md`

**C2 (code changes, one file: `tests/cli/test_advertised_commands.py`):**
- Replaced `_COMMAND_LINE_END_RE` regex with `_command_line_end(tail)` function (R-0934 fix)
- New function treats `"` or `'` as opening a QUOTED ARGUMENT, skips to matching close instead of ending at opening quote
- Unterminated quote still ends scan at opening position (unchanged from before)
- New `_HARD_STOP_RE` regex for backticks, parens, pipes, semicolons, backslash, `&&`, `remedy`
- Updated `scan_advertised_command_flags` to use new function (line 171 area)
- Updated `scan_group_only_invocations` to use new function (line 412 area)
- New regression test: `test_flag_scanner_skips_a_quoted_argument_and_still_catches_a_later_flag` verifies `` `remedy do run "<goal>" --bogus-flag x` `` now catches `--bogus-flag`

## Gate Results (all real output)

**G1 TARGETED** ✓ PASS
- Command: `python3 -m pytest tests/cli/test_advertised_commands.py -q`
- Output: `14 passed in 0.46s`
- Expected: 14 passed (13 baseline + 1 new) ✓

**G2 CANARY** ✓ PASS
- Command: `python3 -m pytest tests/cli/test_golden_path.py -q`
- Output: `42 passed in 17.68s`
- Expected: 42 passed (unchanged) ✓

**G3 RUFF** ✓ PASS
- Command: `python3 -m ruff check tests/cli/test_advertised_commands.py`
- Output: `All checks passed!`
- Expected: All checks passed! ✓

**G4 DIRECT MEASUREMENT** ✓ PASS
- Import `scan_advertised_command_flags` fresh, call on `` '`remedy do run "<goal>" --bogus-flag x`' ``
- Output: `[(('do', 'run'), ['--bogus-flag'])]`
- Expected: `[(("do", "run"), ["--bogus-flag"])]` ✓

**G5 MUTATION RED-PROOF** ✓ PASS
- Disposable worktree created at HEAD (edc7ad59) with edits applied
- Step 1: `python3 -m pytest tests/cli/test_advertised_commands.py -q` reads `14 passed`
- Step 2: Mutated `_command_line_end`: changed quote handler from skip-to-matching-close to immediate `return i` (removed `close = tail.find(ch, i + 1)` lookup, left rest applied)
- Step 3: Re-ran tests: exactly ONE failure, `test_flag_scanner_skips_a_quoted_argument_and_still_catches_a_later_flag`, result `1 failed, 13 passed` ✓
- Step 4: Restored quote-skip logic and re-ran: `14 passed` ✓
- Step 5: Worktree deleted; primary checkout untouched

**G6 TREE** ✓ PASS
- `git status --porcelain` empty
- `git worktree list` shows 1 row (primary checkout): `/home/decodeux/Repos/remedy  edc7ad59 [feature/f281-cli-help-surface]`
- HEAD edc7ad59 matches `origin/feature/f281-cli-help-surface` after push ✓

## Findings

Round 17 had one LOW finding (R-0956, trailing newline dropped in `.agent/decisions.md`). **RESOLVED** in this round's C1 by appending the missing `\n` byte. No new findings identified in round 18.

## Next Action

Round 19 should scope R-0809 (one id-error-message shape for mission/job/run). Per PLAN18's Next Steps: research found FOUR current wordings across 20+ call sites, shared job-id resolver exists but run-id and mission-id do not, 9+ tests need updating. This is LARGE and does not fit one round. Starting round should:
1. Measure exact call-site and test count fresh
2. Scope shared-helper design (probably one round per id kind: job, run, mission)
3. **Do not attempt a single-round mechanical sweep** — plan the shared-helper design first

Open Acceptance items remaining: R-0805 (ui status dead-session pruning, needs design pass), R-0809 (id-error messages), R-0895 (README quickstart).

## Deviations & Assumptions

None. Block executed exactly as written. All FROM/TO string matches succeeded on first attempt. All four C2 code edits applied cleanly. Newline fix verified by byte read. All six gates passed with recorded real output. Tree clean and pushed.
