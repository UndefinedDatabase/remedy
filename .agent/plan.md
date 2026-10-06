# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 1, round 3: book round 2's verdict, register R-1140, and repair it with four tests — the
order file's `max-cost-usd` is the job's budget, and `--max-cost-usd` and `--project` each win
over the header.

## Next Steps
1. T002: `remedy status --json` gains the versioned section for a machine client.
2. T003: every decision kind answerable with `--json`, and a test that a run with `--yes --no-ui
   --json` on a pipe never reads stdin.
3. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format, and the gate test.
4. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1140 (Medium) is F295's own; R-1138 and R-1139 (Low) stay open, owned by F297.
