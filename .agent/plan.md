# Plan — operator order welt-2 (2026-10-29): Remedy runs on its own

## Goal
decodeux: improvement jobs from remedy-chat must run unattended end to end and stop only with a
plain reason. Six faults of the night 2026-10-28/29 become F320 to F325 (Package 3, Tier 2).

## Current Step
Review round 1 (full lane: 9 failures, all caused by this branch) fixed:
- `remedy do --repair-rounds` and an order's HTTP `repair_rounds` removed again (F280 deleted
  the flag); run and retry keep `repair_rounds`.
- The severity reading moved to `verified_repair.py`, the waiting-job settle into
  `job_run_finish.stamp_blocked_job_finish`, the stop sentence into job metadata, and the
  tri-state flags into one table, so every ratchet row holds or falls (rows lowered).
- Two broad handlers narrowed (BLE001 back to its frozen count).
- A released job starts with the roles of the job it waited for (`released_run_options`).
- Import allowlist, the client answer `client-story-working`, generated pages updated.

## Next Steps
1. One full lane on the branch tip; the orchestrator merges welt2/remedycore and pushes.

## Risks
- Branch welt2/remedycore is merged and pushed by the orchestrator, not by this session.
