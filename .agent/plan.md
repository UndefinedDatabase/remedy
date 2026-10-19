# Plan — verified repair, reliable evidence, adaptive execution (operator order exec-1018b, 2026-10-18)

## Goal
A real test that fails after a passing review leads to one budgeted, evidence-fed repair instead of
a misleading completion or a pointless loop (R-1351); the review-report export is explained and
proven end to end; PRs 360, 361 and 362 are reviewed as one release. Branch
`feature/verified-repair` from PR 362's head `cfd906254`; worktree `.remedy-wt/verified-repair`.
Merge order: 360, 361, 362, this. No merge, no deploy; `.agent/STOP`, supervisor, live checkout
untouched. Outside the roadmap queue (F078 stays next).

## Current Step
9. All steps done (D1–D10, R-1354–R-1358, handoff written): the one full gate on this commit, then
   the PR (not merged).

## Next Steps
- Operator: merge PR 360, 361, 362, then this PR; restart `remedy serve`.
- Open: context files misread as required (D6); capture-by-default is the operator's call (D3).

## Risks
- `run_job`, `run_pingpong` and both files sit at their ledger rows: edits there stay line-neutral,
  new logic lives in `verified_repair.py`.
- Another session (Universe recording) uses local Ollama and the CPU: real runs check load first.
