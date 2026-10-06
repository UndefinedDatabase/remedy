# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 1, round 4: book round 3's verdict and R-1140's resolution, register R-1141, and repair it
as DECISION F295 D3 rules — a mission started from an order file records the file's absolute
path and the sha256 of its bytes.

## Next Steps
1. T002: `remedy status --json` gains the versioned section for a machine client.
2. T003: every decision kind answerable with `--json`, and a test that a run with `--yes --no-ui
   --json` on a pipe never reads stdin.
3. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format, and the gate test.
4. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1141 (Low) is F295's own; R-1138 and R-1139 (Low) stay open, owned by F297.
