# Plan — adaptive execution, complete safety, real-world reliability (operator order 2026-10-18)

## Goal
Small work runs without orchestration, complex work is not underplanned, every applicable project
rule reaches the model, outstanding work can really be cancelled, outcomes are verified and cost
stays bounded. Branch `feature/adaptive-reliability` from PR 361's head `652029edc` (merge order:
PR 360, then PR 361, then this); worktree `.remedy-wt/adaptive-reliability`. Outside the roadmap
queue (F078 stays next). No merge, no deploy; `.agent/STOP`, supervisor, live checkout untouched.

## Current Step
7c. P1 9 lessons measured (D8, R-1353), P1 10 test audit (D9); next API version, docs, full gate.

## Next Steps
7. Scale matrix v5 rows for every case of the order; P1 items (efficiency, go/cargo, lessons,
   test audit) as far as measured; up to four local Ollama calibration runs if every limit holds.
8. Docs, API/interface version, one full local gate on the final commit, PR, German handback.

## Risks
- `pingpong_loop.run_pingpong`, `pingpong_job.run_job` and their files are at their ledger rows:
  edits there are line-neutral, new logic in other modules.
- Another session's model (`muse-glimmer`) is loaded in Ollama and a Universe bench run is active:
  calibration must not evict or slow it; skip if it would.
