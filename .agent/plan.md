# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 2, round 7: book round 6's FAIL verdict with R-1142, register R-1143, and repair R-1142 as
DECISION F295 D6 rules it — the digest's decision read catches exactly the four exception classes
a damaged record raises, with no excused blind handler.

## Next Steps
1. Book round 7 and resolve R-1142; then T002, last part: each job's measured cost with its basis
   and its evidence references, and each project's cost of the day, in the digest; and the
   digest's read cost measured.
2. T003: every decision kind answerable with `--json`, and a test that a run with `--yes --no-ui
   --json` on a pipe never reads stdin.
3. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format, and the gate test.
4. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1142 (Low) is F295's own and is repaired this round; the next gate resolves it.
- R-1138, R-1139 and R-1143 (Low) stay open, owned by F297.
- The digest reads every job file and every job's events on each call; its cost is measured
  before T002 closes.
