# Plan — F298 Machine client contract v1.1: what a client can rely on

## Goal
What a program relies on when it drives Remedy is true and written down once: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, and one document generated from the code names
every operation, field, word, token and exit code (docs/roadmap/features/T12_F298.md). DECISION
F298 D1 fixes the slices and their order; D2 names the document the machine client interface.

## Current Step
Session 2, round 5: T001's fourth part. The interface names the top-level answer keys of the
path's six operations (DECISION F298 D5), held to a static reading of each handler and to a real
run of the path; round 4's verdict is booked.

## Next Steps
1. T001, next part: the top-level answer keys of the other eight operations, with their sites
   verified by hand and held to their code.
2. T001, next part: the keys under the answers' top-level keys, as trees like the digest's.
3. T001, last part: `docs/system/machine-client-contract-v1.md` rendered from the interface, and
   the test that fails when page and interface differ.
4. T002: an order runs in the repository of the project it names, or is refused before any step.
5. T003: honest refusals under `--approve --json`, and one command that declines a result.
6. T004: the second gate test — commit and push, two jobs, one order file started twice.
7. T005, T006, T007; then the amend0930b-slow-cap hardening stage and the closure sequence.

## Risks
- F298 is large for 25 rounds; D1 names the split point if the soft limit is reached.
- The operator's data root holds 11,652 jobs and 13,480 open decisions, so T007's default matters.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297.
