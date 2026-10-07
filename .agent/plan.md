# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 3, round 12: book round 11, resolve R-1148, and land the first half of R-1146's repair
as DECISION F295 D11 rules it — a budget decision answered `extend` with raised limits, recorded
on the job, read as answered by the decision list and by the resume guard.

## Next Steps
1. Book round 12; the second half of R-1146: the budget decision answered `abandon`.
2. The rest of R-1147: `remedy job resume` runs the job's own providers.
3. T003's last part: the hunk decision under `--json`.
4. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format and the unattended path, and the gate test.
5. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1147 (High) stays open until its provider half lands; until then `remedy integrity check`
  reads one failing check, `high_blockers_open`.
- R-1146 (Medium) is F295's own and stays open until `abandon` lands.
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
