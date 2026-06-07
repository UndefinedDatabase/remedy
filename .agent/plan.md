# Plan — Steps 735-744: Combined Pytest Exit Fix

## Goal
Make backend smoke exit cleanly by removing last combined-runtime pytest contamination.

## Current Step
744 — Final handoff (complete)

## Steps
- [x] 735: Handoff — 725-734 PASS individually but reviewer reports combined hang
- [x] 736: Thin wrappers use Popen + temp files (no capture_output pipes)
- [x] 737: Smoke split into separate pytest invocations per runtime file
- [x] 738: Documented isolation rule in context.md
- [x] 739: Targeted proof — all 4 commands pass and exit
- [x] 740: Combined trio passes locally, smoke avoids it by design
- [x] 741: Completion table — runtime 100% for supported verification path
- [x] 742: Smoke uses wrapper, no bg, no || true, set -euo pipefail, timeout enforced
- [x] 743: Final baseline — propose 0.73s, worker 0.88s, helpers 0.37s, smoke PASSED
- [x] 744: Final handoff
