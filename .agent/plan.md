# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 2, round 8: book round 7 and resolve R-1142, register R-1144, and finish T002 as DECISION
F295 D7 rules it — each job's measured cost with its basis and its evidence references, each
project's ledger cost of the UTC day — then repair R-1144, so that the digest never writes.

## Next Steps
1. Book round 8 and resolve R-1144; then T003: every decision kind answerable with `--json`, and a
   test that a run with `--yes --no-ui --json` on a pipe never reads stdin.
2. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format, and the gate test.
3. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1144 (Low) is F295's own and is repaired this round; the next gate resolves it.
- R-1138, R-1139 and R-1143 (Low) stay open, owned by F297.
- The digest's read was measured at a median of 0.066 seconds for 200 jobs (DECISION F295 D7).
