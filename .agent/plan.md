# Plan — adaptive execution, complete safety, real-world reliability (operator order 2026-10-18)

## Goal
Small work runs without orchestration, complex work is not underplanned, every applicable project
rule reaches the model, outstanding work can really be cancelled, outcomes are verified and cost
stays bounded. Branch `feature/adaptive-reliability` from PR 361's head `652029edc` (merge order:
PR 360, then PR 361, then this); worktree `.remedy-wt/adaptive-reliability`. Outside the roadmap
queue (F078 stays next). No merge, no deploy; `.agent/STOP`, supervisor, live checkout untouched.

## Current Step
8b. All steps done (D1-D10, R-1345..R-1353, handoff written). Now: the one full local gate on this
commit, then the PR (not merged).

## Next Steps
- Operator: merge PR 360, PR 361, then this PR; restart `remedy serve`.
- Open: R-1351 (A/B of one repair round from a red DoD), R-1353 (lessons in the builder context).

## Risks
- `pingpong_loop.run_pingpong`, `pingpong_job.run_job` and their files are at their ledger rows:
  edits there are line-neutral, new logic in other modules.
- Another session's model (`muse-glimmer`) is loaded in Ollama and a Universe bench run is active:
  calibration must not evict or slow it; skip if it would.
