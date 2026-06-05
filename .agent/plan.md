# Plan — Steps 695-704: Runtime Exit Final Fix

## Goal
Both runtime CLI test files must exit cleanly.

## Current Step
704 — Final handoff

## Steps
- [x] 695: Handoff — admitted runtime exit bug
- [x] 696: Diagnosed — flock in test process prevents pytest exit on some platforms
- [x] 697: Fixed helper — subprocess.run, stdin=DEVNULL, close_fds=True, no Popen leak
- [x] 698: Fixed setup — runtime_helpers creates data via JSON writes, no flock imports
- [x] 699: Propose runtime exits — 11 passed, 0 errors, exit code 0
- [x] 700: Worker runtime exits — 6 passed, 0 errors, exit code 0
- [x] 701: Smoke catches hangs — REMEDY_PYTEST_TIMEOUT_SEC enforced
- [x] 702: Completion table: runtime stability 100% after elimination of flock in tests
- [x] 703: Smoke 177 passed
- [x] 704: Full baseline: 4432 passed, 0 failed, 8 skipped
