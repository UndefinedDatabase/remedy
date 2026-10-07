# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 4, round 16: book round 15's PASS and the resolutions of R-1147 and R-1151; then T003's
last part under DECISION F295 D14 — `remedy patch hunks <job> [--task-run <task-id>] [--json]`,
the command line's read of a job's hunk ids and of the hunk decision recorded for them, so a
client without the cockpit can answer a hunk decision. T003 closes with this round.

## Next Steps
1. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format, the unattended path and which command answers each kind of decision, and the gate
   test.
2. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
