# Plan — R-0097 short-ID resolution fix

## Goal
`remedy job stop` resolves screen-displayed 8-char short IDs against
the Core store so the human golden path (do → status → stop) works
without --json.

## Current Step
Commit fix + tests, push, create PR.

## Done
- [x] Persist R-0097 to live_review.md
- [x] Implement _resolve_short_id in job_stop_cmd.py
- [x] Add tests: short-ID stop, ambiguity exit 2, unknown exit 3
- [x] Mark R-0097 Done in live_review.md
- [x] Verify: golden_path + job_stop green, ruff clean, no new CLI failures
