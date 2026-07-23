# Plan — Split Workflow v3 + Evidence Pipeline Repair

## Goal
Replace split-workflow docs with v3 content, fix evidence pipeline bugs,
finalize with reviewer findings round.

## Status: FINISHING — zip-last ordering proven, final package pending

Completed:
- v3 docs replaced (planner_reviewer_prompt, split_workflow, STATUS_closure_protocol)
- .agent/handoff.md created + rewritten at handback (R-0071)
- Evidence pipeline fixed (stale plan cleanup, deprecated fallback → warning)
- Canonical zip build sequence documented + NO_EVIDENCE clause added
- R-0072..R-0074 resolved by reviewer
- R-0075 fix: zip-last ordering codified in protocol + workflow
- R-0076 fix: audit-doc annotation
- /build-remedy command created, AGENTS.md audience + handoff sections added

Remaining:
- Handoff rewrite + commit (this round)
- Clean-tree zip build (LAST action)
- PART B: verify + resolve R-0071/R-0075/R-0076 if zip clean
- PART C: README redesign (own PR)
- PART D: Start F081
