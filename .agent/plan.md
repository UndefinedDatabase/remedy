# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 3, round 11: book round 10, register R-1149, and repair R-1148 as DECISION F295 D10 rules
it — a job `remedy do` plans records the digest of its order text, so its run manifest is written
and a budget stop of it ends `stopped`.

## Next Steps
1. Book round 11 and resolve R-1148; repair R-1146: the budget decision is answered with `extend`
   and a raised limit, or with `abandon`, under `--json`.
2. The rest of R-1147: `remedy job resume` runs the job's own providers.
3. T003's last part: the hunk decision under `--json`.
4. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format and the unattended path, and the gate test.
5. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1147 (High) stays open until its provider half lands; until then `remedy integrity check`
  reads one failing check, `high_blockers_open`.
- R-1146 and R-1148 (Medium) are F295's own; R-1148 is repaired this round.
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
