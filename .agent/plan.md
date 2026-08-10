# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003's six migration sites are all migrated.
R34 is GATED; `LAST_REVIEWED_SHA` is 28fe51c3. Call evidence reaches four
prompts: both `do_cmd` flight-plan sites, `remedy mission plan`, and the
orchestrator loop, whose sink lives inside `run_mission` so both callers inherit
it (DECISION D11). `remedy mission run` names its provider; the gauntlet's stays
unlabelled on purpose (DECISION D13).
R35 is the session-close round: it records the R34 gate, resolves R-0258,
registers R-0260 and writes the handoff. By construction it carries no gate
entry on itself (§4.13) — the next session gates it over `28fe51c3..HEAD`.
Open findings: R-0221, R-0239, R-0247, R-0256, R-0259, R-0260.
No PR; one is created at CLOSURE.

## Next Steps
- R-0259: MOVE the misfiled R-0257 block to the end of `## Findings`, bytes
  unchanged, so the R30 gate record closes with its own `LAST_REVIEWED_SHA`
  line. Bundle R-0260's window fix with it — both are small and neither touches
  production code.
- R-0256 (compose once, not twice) needs a signature change on `plan_job_llm`
  and `run_intake`, so it is its own round.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
