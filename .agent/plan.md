# Plan — F069 Mission compiler

Branch: feature/f069-mission-compiler

## Goal
A long prose goal compiles into a MissionPlan — ordered milestones,
each with its own compiled DoD and draft job outlines — so the
orchestrator loop has a structured route instead of improvising. DONE
when three long fixture goals compile into sensible milestone plans,
every milestone carries a DoD reference, and draft jobs NEVER
autostart.

## Current Step
R2 (SPLIT, LARGE), R1 accepted PASS at 83ddb4cb: persist the R1 verdict
+ R-0168 (own commit); fix R-0168 — cap `jobs_draft` at a named
MAX_MILESTONE_DRAFT_JOBS = 8 and require non-empty DraftJob
title/goal, so a bad provider draft fails INSIDE run_structured_call
(one retry, then the honest deterministic fallback) instead of raising
out of attach_milestone_dods; name the cap in the provider prompt; pin
with tests. THEN the integration gate per
docs/agents/integration_gate.md, evidence under .agent/gate_f069_r2/.
Stop-on-red throughout. No closure work this round.

## Next Steps
- Reviewer's gate verdict on the integration-gate evidence.
- Closure per docs/roadmap/STATUS_closure_protocol.md (own round).

## Risks
- The compiler must have ZERO execution side effects: no jobs, no
  starts, no worktree touches. Pinned by a negative test.
- Persistence must stay additive/optional on the mission record; a
  silent schema-version bump would break mission_state consumers.
- Prompt-building helpers are reused, not copied — a copied helper is
  extracted into a shared one instead (feature file, Orchestrator
  brief).
