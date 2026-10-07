# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 3, round 10: book round 9 and resolve R-1145, register R-1146, R-1147 and R-1148, and land
DECISION F295 D9 — `remedy job resume` and the loop's resume refuse a job its budget stopped until
its budget decision is answered, the first part of R-1147's repair.

## Next Steps
1. Book round 10; repair R-1148: a job `remedy do` plans writes its run manifest, so a budget stop
   of such a job ends `stopped`.
2. Repair R-1146: the budget decision is answered with `extend` and a raised limit, or with
   `abandon`, under `--json`.
3. The rest of R-1147: `remedy job resume` runs the job's own providers.
4. T003's last part: the hunk decision under `--json`.
5. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format and the unattended path, and the gate test.
6. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1147 (High) stays open until its provider half lands; until then `remedy integrity check`
  reads one failing check, `high_blockers_open`.
- R-1146 and R-1148 (Medium) are F295's own.
- R-1138, R-1139 and R-1143 (Low) stay open, owned by F297.
