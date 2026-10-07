# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 5, round 21: the SLOW MODE hardening stage (amend0930b-slow-cap). Book round 20's PASS and
R-1154's resolution; repair R-1155 under DECISION F295 D19: an `extend` of a budget stop answers
the contract remainder decision that stop raised `no`, names it under `closed_decisions`, and the
gate test and the contract page say so.

## Next Steps
1. Repeat the acceptance audit for the claims that had gaps (claim 7) and for the claims
   R-1155's repair touches; write the feature file's Built State paragraph (rule (4)).
2. The closure sequence (docs/roadmap/STATUS_closure_protocol.md), with the one full suite.

## Risks
- R-1155 (Low, F295's) is repaired this round; its resolution is booked after review.
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
- Eleven local branches `remedy/<16 hex>` from rounds 13 and 14 remain; at `d0ca96e49` the two
  test files that made them leak nothing (DECISION F295 D18).
