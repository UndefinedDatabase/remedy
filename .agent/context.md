# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 343-350: Visual target alignment, token metrics, organic brain graph v2.

## Completed
- Token usage metric: backend _build_token_usage() + frontend fifth metric with tooltip
- Main layout: PipelinePanel moved from main column to right panel, 4-row grid restored
- Organic brain graph v2: branching tree layout, fewer particles, deterministic from jobId
- Phase timeline v2: compact rail, smaller icons, quieter proportions
- Right panel: compact stack with LivePill, AgentNow, Pipeline, Activity, Tasks
- Top metrics: 5 columns, smaller font/icon sizes, token tooltip on hover/focus
- Vitest: 35 passed (4 new token tests)
- Backend: 12 pipeline+token contract tests

## Constraints
- UI remains read-only — no POST/PUT/DELETE
- No browser mutation endpoints
- source_apply requires job + intent_id (approved) before mutation
- No shell=True, no 0.0.0.0

## Remaining Risks
- No pixel-perfect visual regression system
- Real browser screenshot/manual visual QA still recommended
- Token usage is estimated only (from event metadata)
- Full visual polish later

## Recommended Next Block
Steps 351-358 — Event-Ledger Replay And Checkpoint Resume
Or if visual gaps remain:
Steps 351-358 — UI Interaction Polish And Graph Filtering
