# Plan — scale correctness (operator order 2026-10-17, audit remedy_scale_audit_2026-10-17.md)

## Goal
Minimal correct work for small orders, reliable work for medium ones, controlled decomposition for
risky or multi-repo ones. A focused change of the lane decision, plan normalization and the
cost policy; no new orchestrator. Branch feature/scale-correctness-routing; roadmap queue F078 untouched.
`.agent/STOP` kept; no unattended loop, no real model call, no merge, no install.

## Current Step
PR 348 closure review (DECISION scale-1017 D12): force-job keeps a hold, waiting jobs share the
leftover, an unpriced money cap fails safe. Focused tests green; one full local run, then merge.

## Next Steps
- Full local gate once on the final commit; record SHA, tree, commands, result.
- Merge PR 348 by the normal workflow, sync main; no deploy, no restart, no real model.

## Risks
- Verification scope by changed language/package is not built (project_tests runs one command).
- A money cap stops a walk after its planning (planner calls are unpriced); use call/token caps with local models.
