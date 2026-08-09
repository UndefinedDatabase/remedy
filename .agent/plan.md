# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 (the F104 closure) merged at the Open PR Gate. Build mode:
one-session self-drive, one delegated worker per round. Next finding ID: R-0235.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
R8, the record-integrity round: the R7 gate is on disk, R-0231 and R-0232 are
RESOLVED with reviewer-authored text, and R-0233 and R-0234 are registered and
fixed with `Landed:` lines the next gate converts. T001 and T002 are DONE and
reviewer-gated — `packages/orchestration/prompt_segments.py` and
`role_conventions.py`, pinned by 22 and 26 tests. `LAST_REVIEWED_SHA` is
c95db6e7. No PR exists; one is created at CLOSURE. The candidates file is empty.

## Next Steps
- R9, the T003 inventory round: read-only, one document — per builder the file,
  function, line, assembly idiom, the segments it concatenates and their order,
  and whether it reaches call evidence. The six the feature file names:
  `pingpong_loop._build_builder_prompt` and `._build_reviewer_prompt`,
  `orchestrator_loop.build_orchestrator_prompt`, `intake._build_intake_prompt`,
  `flight_plan._build_plan_prompt`, `mission_compiler.build_mission_prompt`.
- Then T003 proper, ONE builder per round: the content-equality golden lands
  first, then composition moves to the registry, then the manifest to evidence.
- Then T004, the `remedy stats cache` view over actuals, reporting "not
  reported" rather than zeros where a provider reports no cache figures.
- Then the integration gate (docs/agents/integration_gate.md), then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- Twelve candidate assembly sites in three idioms; the feature file names six.
  Migration must not change content — goldens land before behaviour moves.
- Conventions headroom is 60 estimated tokens on the worker document and 97 on
  the reviewer document against the cap of 800. Measure BEFORE authoring.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
- DECISION F105 D2 caps step blocks at 240 lines; the once-per-feature oversize
  exception is spent on `ea48ea89`.
