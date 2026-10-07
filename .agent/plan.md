# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 5, round 20: the SLOW MODE hardening stage (amend0930b-slow-cap). Book round 19's PASS and
R-1153's resolution; save the acceptance audit as `.agent/f295_acceptance_audit.md`; register
R-1154 and R-1155 under DECISION F295 D18; repair R-1154 with a test in
`tests/cli/test_do_sequence_cli.py`.

## Next Steps
1. Repair R-1155 under a DECISION of its own: the contract remainder decision a budget stop
   raised does not outlive an `extend` of that stop.
2. Repeat the acceptance audit for the claims that had gaps (claim 7) and for the claims
   R-1155's repair touches; write the feature file's Built State paragraph (rule (4)).
3. The closure sequence (docs/roadmap/STATUS_closure_protocol.md), with the one full suite.

## Risks
- R-1154 (Low, F295's) is repaired this round; its resolution is booked after review.
- R-1155 (Low, F295's) changes production code; it gets its own round and mutations.
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
- Eleven local branches `remedy/<16 hex>` from rounds 13 and 14 remain; at `d0ca96e49` the two
  test files that made them leak nothing (DECISION F295 D18).
