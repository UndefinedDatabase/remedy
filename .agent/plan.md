# Plan — F298 Machine client contract v1.1: what a client can rely on

## Goal
What a program relies on when it drives Remedy is true and written down once: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, and one contract document generated from the code
names every operation, field, word, token and exit code (docs/roadmap/features/T12_F298.md).
DECISION F298 D1 fixes the slices and their order.

## Current Step
Session 1, round 1: the claim. Branch from `main` at `77493e0f9`, mark F298 `[~]` in STATUS,
re-head the review record and book F116's round 15, record DECISION F298 D1 and the slice order,
and save the claim's measurement as `.agent/f298_inventory.md`. No production code.

## Next Steps
1. T001: the contract as data, one command that prints it, the page rendered from it, and the test
   that fails when code and document differ.
2. T002: an order runs in the repository of the project it names, or is refused before any step.
3. T003: honest refusals under `--approve --json`, and one command that declines a result.
4. T004: the second gate test — commit and push, two jobs, one order file started twice.
5. T005, T006, T007: the approval card, tokens and calls, the bounded digest.
6. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- F298 is large for 25 rounds; D1 names the split point if the soft limit is reached.
- The operator's data root holds 11,652 jobs and 13,480 open decisions, so T007's default matters.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297.
