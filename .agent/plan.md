# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 5, round 22: book round 21's PASS and R-1155's resolution; save the repeated acceptance
audit as `.agent/f295_acceptance_reaudit1.md`; write the feature file's Built State, with the
hardening stage's record (amend0930b-slow-cap rule (4)). The hardening stage closes with this
round.

## Next Steps
1. The closure sequence (docs/roadmap/STATUS_closure_protocol.md): the one self-use item
   (precondition 6), the one full suite in the integration-gate round, the evidence bundle and
   the review zip, the ledger rotation, the re-assignment of open findings, the STATUS line, the
   pull request.

## Risks
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
- F295 reaches its soft limit of 25 rounds inside the closure sequence; the handoff then carries
  the scope report, and the closure is the self-consistent close.
- Eleven local branches `remedy/<16 hex>` from rounds 13 and 14 remain; at `d0ca96e49` the two
  test files that made them leak nothing (DECISION F295 D18).
