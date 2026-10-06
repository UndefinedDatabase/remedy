# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 1, round 1: claim F295, re-head the review record, book F290's round 14, record the
claim's measurement in `.agent/f295_inventory.md`, and write the slice order.

## Next Steps
1. T001: `remedy do <order.md>` reads the order file, and refuses a missing, empty or unreadable
   file, and a file without a cost cap, before any step.
2. T002: `remedy status --json` gains the versioned section for a machine client.
3. T003: every decision kind answerable with `--json`, and a test that a run with `--yes --no-ui
   --json` on a pipe never reads stdin.
4. T004: `docs/system/machine-client-contract-v1.md` and the gate test.
5. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1138 and R-1139 (Low) stay open, owned by F297; F295 owns no finding at its claim.
- The order-file detection rule must not turn order text that names a `.md` file into a path.
