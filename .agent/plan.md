# Plan — Steps 565-579

## Goal
Implement orchestrator task evaluation flow. Review-created tasks become proposed tasks that need evaluation before build. Finalized blocked by unresolved proposals.

## Current Step
Complete — all steps done.

## Steps
- [x] Step 565: Handoff — update context.md, plan.md, live_review.md
- [x] Step 566: ProposedTask domain model (packages/orchestration/proposed_tasks.py)
- [x] Step 567: Proposed task store (save/load/list/update in .data/)
- [x] Step 568: Review findings create proposed tasks (propose_task_from_review_finding)
- [x] Step 569: Deterministic evaluator rules v1
- [x] Step 570: Optional LLM evaluator interface (disabled by default)
- [x] Step 571: Approve/reject/defer state transitions
- [x] Step 572: Build queue only picks approved tasks
- [x] Step 573: Review loop creates rework proposals
- [x] Step 574: Finalized gate includes proposed tasks
- [x] Step 575: CLI proposed task commands
- [x] Step 576: Events/audit trail for proposed task lifecycle
- [x] Step 577: Dashboard backend counts (proposed_task_count, etc.)
- [x] Step 578: Tests — 4259 passed, 0 failed, Vitest 35, tsc clean
- [x] Step 579: Handoff report
