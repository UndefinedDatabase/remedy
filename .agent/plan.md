# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 4, round 18: book round 17's PASS and R-1152's resolution; T004's first part under
DECISION F295 D16 — `tests/cli/test_machine_client_contract.py`, the gate test that drives an
order file to its proof through `apps.cli.grouped.main` and fails on any read of stdin.

## Next Steps
1. T004's second part (DECISION F295 D16 (3)): `docs/system/machine-client-contract-v1.md`,
   registered in `docs/README.md`, and the test that holds the page and the gate test to the
   same commands, flags, keys and exit codes.
2. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
- Eleven local branches `remedy/<16 hex>` with prunable worktree entries, made on 2026-10-07 at
  `c2b9a817f` and `4ae5d4d33` while F295's round 13 and 14 tests ran, remain in this repository;
  the hardening stage measures the cause.
- After an extended job completes, the contract remainder decision its budget stop raised stays
  open in the digest; the hardening stage reads whether that is right.
