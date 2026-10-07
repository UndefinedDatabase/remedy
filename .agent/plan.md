# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order; T001 to T003 have landed.

## Current Step
Round 9, the hardening stage (operator amendment amend0930b-slow-cap): the acceptance audit
(`.agent/f287_acceptance_audit.md`) proved nine claims and found one gap, R-1163, no proof through
the command line. Round 8 saved the audit; this round lands the repair, a test under `tests/cli/`
that pauses with `remedy job pause`, relaunches with `remedy job run` and reads
`remedy run show --json`.

## Next Steps
1. Repeat the audit for the gap's statement (the user-path proof) with a fresh worker; another
   repair round only if it is still open (at most three in all).
2. The closure sequence (docs/roadmap/STATUS_closure_protocol.md), whose first round writes the
   audit paragraph into the feature file's Built State.

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109,
  DECISION F287 D6); the closure's self-use run is the first real observation.
- R-1163 (Low, F287): open until this round's test lands and its red-proofs hold.
- R-1162 (Low, F297): a `claude-cli` job with no model configured cannot finish a stop.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 (Low) stay open,
  owned by F297.
