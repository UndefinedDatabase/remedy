# Plan — scanner-fix gap work (R-0084)

## Goal
Extend _REAL_ROOT_DIRS to cover macOS/Ubuntu root dirs so bare tokens
like /Users, /snap, /Volumes are still flagged by _contains_local_path.

## Status: COMPLETE
- R-0084 persisted (40b0065)
- _REAL_ROOT_DIRS extended: snap, applications, cores, library, private, system, users, volumes
- 3 unsafe test cases added: /Users, /snap, /Volumes
- R-0084 marked Done in live_review.md
- 77 passed, 0 failures; ruff 41 (0 new)

## Next
- Rewrite handoff.md
