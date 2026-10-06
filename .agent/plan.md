# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 1, round 2: book round 1's verdict and land T001 as DECISION F295 D2 rules it —
`remedy do <order.md>` reads an order file with an optional header, a flag wins over the header,
and a missing, unreadable or empty file, a broken header and a file without a cost cap are each
refused before any step.

## Next Steps
1. T002: `remedy status --json` gains the versioned section for a machine client.
2. T003: every decision kind answerable with `--json`, and a test that a run with `--yes --no-ui
   --json` on a pipe never reads stdin.
3. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format, and the gate test.
4. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1138 and R-1139 (Low) stay open, owned by F297; F295 owns no finding.
- The order-file detection rule must not turn order text that names a `.md` file into a path.
