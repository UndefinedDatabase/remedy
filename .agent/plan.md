# Plan — Steps 705-714: Runtime Process Cleanup Final Fix

## Goal
Both runtime CLI test files must pass AND exit cleanly under remedy_pytest.sh.

## Current Step
714 — Final handoff (complete)

## Steps
- [x] 705: Correct handoff truth — marked 695-704 FAIL for runtime closure
- [x] 706: Rewrote run_grouped_cli with Popen + temp files + start_new_session + killpg
- [x] 707: Added assert_no_leftover_locks() with fixture teardown in both test files
- [x] 708: Bounded event reads (max_files, max_bytes params, is_dir check, error handling)
- [x] 709: Propose runtime — 11 passed, 2.37s, clean exit
- [x] 710: Worker runtime — 6 passed, 4.84s, clean exit
- [x] 711: Smoke includes both runtime files, uses remedy_pytest.sh, no || true
- [x] 712: Completion table updated — runtime 100% after proof
- [x] 713: Final proof — all 3 commands pass and exit: 11 + 6 + 177
- [x] 714: Final handoff
