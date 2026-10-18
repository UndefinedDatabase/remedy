# Plan — adaptive execution, complete safety, real-world reliability (operator order 2026-10-18)

## Goal
Small work runs without orchestration, complex work is not underplanned, every applicable project
rule reaches the model, outstanding work can really be cancelled, outcomes are verified and cost
stays bounded. Branch `feature/adaptive-reliability` from PR 361's head `652029edc` (merge order:
PR 360, then PR 361, then this); worktree `.remedy-wt/adaptive-reliability`. Outside the roadmap
queue (F078 stays next). No merge, no deploy; `.agent/STOP`, supervisor, live checkout untouched.

## Current Step
1. Findings R-1345..R-1350 registered (this commit); baseline scale matrix v4 recorded on 652029edc.

## Next Steps
2. R-1343/R-1345: a sandbox-refused test command ends the loop `sandbox_unavailable`, no review,
   no repair; post-mortem class `sandbox_unavailable`; verification `not_run` with its reason.
3. R-1346: planner calls of a supervised walk are cancellable in flight (Ollama streamed, Claude
   CLI through the guard's cancel_check); a cancelled call never degrades to a fallback plan.
4. R-1347: the repository's rule files (root and nested along the task's files) reach builder and
   reviewer whole under a hard ceiling, with provenance and precedence; over it the call stops.
5. R-1348/R-1350: named files get roles (required, optional, context, protected); protected ones
   refuse a change; independent deliverables become one task each in the one bounded job.
6. R-1349: an order that asks for a plan only walks `--plan-only`; one that asks for verification
   only plans no change (hold with the verification answer).
7. Scale matrix v5 rows for every case of the order; P1 items (efficiency, go/cargo, lessons,
   test audit) as far as measured; up to four local Ollama calibration runs if every limit holds.
8. Docs, API/interface version, one full local gate on the final commit, PR, German handback.

## Risks
- `pingpong_loop.run_pingpong`, `pingpong_job.run_job` and their files are at their ledger rows:
  edits there are line-neutral, new logic in other modules.
- Another session's model (`muse-glimmer`) is loaded in Ollama and a Universe bench run is active:
  calibration must not evict or slow it; skip if it would.
