# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 (the F104 closure) merged at the Open PR Gate. Build mode:
one-session self-drive, one delegated worker per round. Next finding ID: R-0236.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
R9, the T003 inventory round: `.agent/t003_inventory.md` surveys every prompt
assembly site the migration must touch, the R8 gate is on disk, R-0233 and
R-0234 are RESOLVED, and R-0235 is registered and fixed with a `Landed:` line
the next gate converts. T001 and T002 are DONE and reviewer-gated —
`packages/orchestration/prompt_segments.py` and `role_conventions.py`, pinned by
22 and 26 tests. `LAST_REVIEWED_SHA` is 337ba21f. No PR exists; one is created
at CLOSURE. The candidates file is empty.

## Next Steps
- T003 proper, ONE builder per round in the order `.agent/t003_inventory.md`
  proposes: the content-equality golden lands FIRST, then composition moves to
  the registry, then the segment manifest reaches call evidence.
- Then the acceptance guard the feature file names: a test that greps direct
  string-assembly patterns in the builder modules, allowlist starting empty.
- Then T004, the `remedy stats cache` view over actuals, reporting "not
  reported" rather than zeros where a provider reports no cache figures.
- Then the integration gate (docs/agents/integration_gate.md), then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- The inventory is the first read of this ground; a site it misses is a site
  T003 will not migrate. Migration must not change content — goldens land first.
- Conventions headroom is 60 estimated tokens on the worker document and 97 on
  the reviewer document against the cap of 800. Measure BEFORE authoring.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
- DECISION F105 D2 caps step blocks at 240 lines; the once-per-feature oversize
  exception is spent on `ea48ea89`.
