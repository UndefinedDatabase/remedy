# Plan — F298 Machine client contract v1.1: what a client can rely on

## Goal
What a program relies on when it drives Remedy is true and written down once: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, and one document generated from the code names
every operation, field, word, token and exit code (docs/roadmap/features/T12_F298.md). DECISION
F298 D1 fixes the slices and their order; D2 names the document the machine client interface.

## Current Step
Session 5, round 20: T001's page part. The last section of
`docs/system/machine-client-contract-v1.md` is the interface rendered between two markers, held to
the code by its bytes and by reading it back, while the walk through the path stays written by hand
(DECISION F298 D20); round 19's verdict and R-1178's resolution are booked.

## Next Steps
1. Decide, before the soft limit of 25 rounds is reached, where F298 closes and which slices move
   to a follow-up feature placed directly behind it (DECISION F298 D1 (6)).
2. T002: an order runs in the repository of the project it names, or is refused before any step.
3. T003: honest refusals under `--approve --json`, and one command that declines a result.
4. T004: the second gate test — commit and push, two jobs, one order file started twice.
5. T005, T006, T007; then the amend0930b-slow-cap hardening stage and the closure sequence.

## Risks
- F298 stands at 20 rounds of 25; D1 names the split point.
- The operator's data root holds 11,652 jobs and 13,480 open decisions, so T007's default matters.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297.
