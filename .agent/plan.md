# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 2, round 9: book round 8 and resolve R-1144, register R-1145, and land T003's first part
as DECISION F295 D8 rules it — every child Remedy starts for a provider reads end-of-file, and
four real-pipe tests prove an unattended run never reads stdin.

## Next Steps
1. Book round 9 and resolve R-1145; then T003's second part: measure which command answers each
   decision kind under `--json`, the budget raise and the hunk decision first, and close the gaps.
2. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format and the unattended path, and the gate test.
3. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1145 (Medium) is F295's own and is repaired this round; the next gate resolves it.
- R-1138, R-1139 and R-1143 (Low) stay open, owned by F297.
