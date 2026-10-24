# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
a per-run `capability_degradations` evidence field, a report section and a badge show when a
degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 2, T002: book round 1's verdict, DECISION F157 D2 (the register frozen from the reviewed
inventory), the module `packages/contracts/capability_matrix.py` with its unit tests and its two
guards, and `remedy worker show` as its first consumer, with the contract page's new section.

## Next Steps
1. T003: the badge's target by DECISION, then one consolidation order per register entry with its
   existing tests unmodified, the run record's `capability_degradations` key behind the structure
   ledger's boundary, the report section and the reduced-capability end-to-end.
2. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- `pingpong_loop.py` and `run_manifest.py` are structure-ledger rows; the evidence key's commit
  draws their boundary first, in a commit of its own.
