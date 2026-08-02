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
R1 (SPLIT, LARGE bundle) COMPLETE — awaiting review. T001 schema
`mission_plan_v1` + milestone-DAG validation + compiler + deterministic
fallback + three long-goal golden fixtures; T002 per-milestone DoD
hand-off through the F061 compiler (A6) + additive persistence on the
mission record + mission_plan.md rendering + the no-autostart
guarantee; T003 CLI `remedy mission plan <id>` + recompile versioning
+ in-progress refusal. All slice gates exit 0; branch pushed.

## Next Steps
- Integration gate per docs/agents/integration_gate.md.
- Closure per docs/roadmap/STATUS_closure_protocol.md (own round).

## Risks
- The compiler must have ZERO execution side effects: no jobs, no
  starts, no worktree touches. Pinned by a negative test.
- Persistence must stay additive/optional on the mission record; a
  silent schema-version bump would break mission_state consumers.
- Prompt-building helpers are reused, not copied — a copied helper is
  extracted into a shared one instead (feature file, Orchestrator
  brief).
