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
R32 is GATED; `LAST_REVIEWED_SHA` is cab89962.
R33 gives the ORCHESTRATOR prompt its call evidence: a per-iteration recorder
in `orchestrator_loop.py` carrying the segment manifest, and the sink appending
to the mission's `prompt_trace.jsonl` from INSIDE `run_mission` rather than
from a caller (DECISION F105 D11), so both callers —
`mission_cmd.py:366` and `gauntlet_runner.py:514` — inherit it.
Call evidence then reaches four prompts: both `do_cmd` flight-plan sites,
`remedy mission plan`, and the orchestrator loop.
Open findings: R-0221, R-0239, R-0247, R-0256.
No PR; one is created at CLOSURE.

## Next Steps
- Name the gauntlet's provider at `gauntlet_runner.py:514`: its orchestrator
  rows reach evidence from R33 on but carry an empty label. One line, not a
  wiring round (DECISION F105 D11).
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
