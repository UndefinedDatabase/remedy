# Plan — scanner-fix gap work (R-0084)

## Goal
Extend _REAL_ROOT_DIRS to cover macOS/Ubuntu root dirs so bare tokens
like /Users, /snap, /Volumes are still flagged by _contains_local_path.

## Current Step
1. Persist R-0084 finding to live_review.md (own commit)

## Next Steps
2. Extend _REAL_ROOT_DIRS in run_manifest.py + trade-off comment
3. Add unsafe test cases (/Users, /snap, /Volumes) to TestSlashCommandFalsePositive
4. Mark R-0084 Done in live_review.md
5. Verify: pytest + ruff green
6. Rewrite handoff.md
