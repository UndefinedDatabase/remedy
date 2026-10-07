# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 3, round 15: book round 14's FAIL verdict, register R-1151, and repair it — the exit-code
guard's registry names the site `remedy job resume` now reaches through `remedy job run`'s
handler, so the selection is green again over round 14's code.

## Next Steps
1. Book round 15 and resolve R-1147 and R-1151; T003's last part: the hunk decision under
   `--json`.
2. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format and the unattended path, and the gate test.
3. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1147 (High) is repaired by round 14's code; until its resolution is booked,
  `remedy integrity check` reads one failing check, `high_blockers_open`.
- R-1151 (Low) is F295's own and is repaired this round.
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
