# Plan — Split Workflow v3 + Evidence Pipeline Repair

## Goal
Replace split-workflow docs with v3 content, fix evidence pipeline bugs,
finalize with reviewer findings round.

## Status: IN PROGRESS — finalization round (R-0071..R-0074)

Completed:
- v3 docs replaced (planner_reviewer_prompt, split_workflow, STATUS_closure_protocol)
- .agent/handoff.md created
- Evidence pipeline fixed (stale plan cleanup, deprecated fallback → warning)
- Canonical zip build sequence documented
- Code-only zip build verified (NO_EVIDENCE)
- Findings R-0071..R-0074 persisted

Current:
- Applying fixes: R-0071 (handoff), R-0072 (review_protocol), R-0073 (plan),
  R-0074 (legacy subagent)
- /build-remedy command, AGENTS.md additions, consistency sweep

Next:
- Build fresh zip, commit fixes, push, update PR, handback
