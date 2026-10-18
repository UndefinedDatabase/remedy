# Plan — verified repair, reliable evidence, adaptive execution (operator order exec-1018b, 2026-10-18)

## Goal
A real test that fails after a passing review leads to one budgeted, evidence-fed repair instead of
a misleading completion or a pointless loop (R-1351); the review-report export is explained and
proven end to end; PRs 360, 361 and 362 are reviewed as one release. Branch
`feature/verified-repair` from PR 362's head `cfd906254`; worktree `.remedy-wt/verified-repair`.
Merge order: 360, 361, 362, this. No merge, no deploy; `.agent/STOP`, supervisor, live checkout
untouched. Outside the roadmap queue (F078 stays next).

## Current Step
6. Investigative full run (durations, order dependence), then at most three controlled real runs.

## Done (this branch)
R-1351/R-1354/R-1355 verified repair; review-report e2e + diagnosis (D3); combined review: R-1356
walk order scope, R-1357 cancel during the final gate; P1 4 R-1358 adversarial matrix; P1 5 rule
dedupe (D7); P1 6 measured, nothing built (D8).

## Next Steps
7. Test-suite findings from the investigative run (P1 7), proven before any consolidation.
8. Real runs (D9) or the written blocker; API handoff; handoff.md; one full gate on the final
   commit; PR into main stacked on 360, 361, 362 (not merged).

## Risks
- `run_job`, `run_pingpong` and both files sit at their ledger rows: edits there stay line-neutral,
  new logic lives in `verified_repair.py`.
- Another session (Universe recording) uses local Ollama and the CPU: real runs check load first.
