# Plan — Steps 685-694: Runtime Hang Kill

## Goal
Fix runtime CLI file hangs, add anti-hang guards, truthful handoff.

## Current Step
694 — Final handoff

## Steps
- [x] 685: Handoff — downgraded claims
- [x] 686: Diagnosed hang — lock files left on disk, double os.close(fd), no lock file cleanup
- [x] 687: Fixed propose runtime — _file_lock deletes lock file, start_new_session subprocess
- [x] 688: Fixed worker runtime — same fix propagates
- [x] 689: Anti-hang guard — assert_no_leftover_locks in fixture teardown
- [x] 690: Smoke includes runtime files (already did from 682)
- [x] 691: Targeted stability proven — propose 11 pass, worker 6 pass, smoke 177 pass
- [x] 692: Completion table repaired in context.md
- [x] 693: Broader regression 1630 pass, 7 skip
- [x] 694: Full baseline: 4432 passed, 0 failed, 8 skipped
