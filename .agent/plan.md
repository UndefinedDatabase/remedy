# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 3, round 15: the closure's evidence round. Book round 14 (PASS: DECISION F294 D12 closes
F294 on its Acceptance's second branch), then, from the clean and pushed tree at that booking
commit, preview the staging-copy reclaim, build the evidence job and build the review package
(docs/roadmap/STATUS_closure_protocol.md algorithm steps 1 and 2). The open-findings count is 3
(`R-1117`, `R-1125`, owned by F290; `R-1127`, owned by F294 until its closure hands it to F290).

## Next Steps
1. The closing round: book round 15, rotate the ledger, hand `R-1127` to F290, accept F294
   PASS_WITH_RISKS in STATUS and README, consume `SU-041`, open the pull request.

## Risks
- A package that builds BLOCKED_EVIDENCE is a closure blocker; the evidence script stops before
  packaging on every check the closure protocol's pitfalls name.
