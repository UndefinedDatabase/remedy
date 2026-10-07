# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 3, round 13: book round 12, register R-1150, and land DECISION F295 D12 — a budget
decision answered `abandon` cancels the job, a cancelled job never runs again, and a test pins
the current-deadline rule R-1150 names.

## Next Steps
1. Book round 13 and resolve R-1146 and R-1150; the rest of R-1147: `remedy job resume` runs the
   job's own providers.
2. T003's last part: the hunk decision under `--json`.
3. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format and the unattended path, and the gate test.
4. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1147 (High) stays open until its provider half lands; until then `remedy integrity check`
  reads one failing check, `high_blockers_open`.
- R-1146 (Medium) and R-1150 (Low) are F295's own and are repaired this round.
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
