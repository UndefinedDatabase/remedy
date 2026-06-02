# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 335-342: Operator Cockpit v2, pipeline visibility, stop-reason UX.

## Completed
- Pipeline status contract in dashboard v4 (`pipeline` object with provider, context, memory, parse, intent, approval, apply, test, repair, stop_reason, next_command)
- Pipeline timeline component (PipelineTimeline with 8-10 steps, state-based icons)
- Stop reason card with human labels, explanations, copy-to-clipboard next command
- Read-only decision queue (approval visibility via pipeline fields, CLI commands in StopReasonCard)
- Repair loop visibility (repair_loop object, repair step in timeline with cycle count)
- Memory and source context visibility (ContextCard with safe metadata only)
- Pipeline next_command generation (catalog-valid commands based on stop_reason)
- 9 backend pipeline contract tests, 10 Vitest pipeline normalization tests

## Constraints
- UI remains read-only — no POST/PUT/DELETE
- No browser mutation endpoints
- No browser approve/apply buttons
- source_apply requires job + intent_id (approved) before mutation
- No unittest.mock in production packages
- No shell=True, no 0.0.0.0

## Remaining Risks
- Visual polish not final
- No browser mutation actions (by design)
- Updates via 5s polling (no WebSocket/SSE)
- Pipeline panel placement may need layout tuning

## Recommended Next Block
Steps 343-350 — Event-Ledger Replay And Checkpoint Resume
Or if UI exposed new gaps:
Steps 343-350 — UI Interaction Polish And Graph Filtering
