# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 4, round 19: book round 18's PASS, register R-1153; T004's second part under DECISION
F295 D17 — `docs/system/machine-client-contract-v1.md`, indexed, and the test that holds its
tables to the gate test; `docs/system/proof-chain.md` names the job applies (R-1153). T004 and
the building rounds close with this round.

## Next Steps
1. The SLOW MODE hardening stage (amend0930b-slow-cap): an acceptance audit by a fresh worker
   given only the feature file and the repository, every Acceptance and Goal & Done statement
   proved by a mutation that turns a test red, at least one through the command line; each gap
   a finding owned by F295, repaired in reviewed rounds, at most three.
2. The closure sequence (docs/roadmap/STATUS_closure_protocol.md), with the one full suite.

## Risks
- R-1153 (Low, F295's) is repaired this round; its resolution is booked after review.
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
- Eleven local branches `remedy/<16 hex>` with prunable worktree entries, made on 2026-10-07 at
  `c2b9a817f` and `4ae5d4d33` while F295's round 13 and 14 tests ran, remain in this repository;
  the hardening stage measures the cause.
- After an extended job completes, the contract remainder decision its budget stop raised stays
  open in the digest; the hardening stage reads whether that is right.
