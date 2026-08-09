# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 (the F104 closure) merged at the Open PR Gate. Build mode:
one-session self-drive, one delegated worker per round. Next finding ID: R-0233.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
Session ended at its declared FOUR-ROUND CAP (R4 through R7) with F105 work
remaining — a clean ending under docs/agents/self_drive_protocol.md G7, not a
failure. T001 and T002 are both DONE and reviewer-gated: the segment registry,
compose and manifest in `packages/orchestration/prompt_segments.py`, and the
conventions loaders in `packages/orchestration/role_conventions.py` reading both
role documents verbatim under an imported cap, pinned by 22 and 26 tests. The
operator addition of 2026-07-30 landed as a pure append to both documents.
`LAST_REVIEWED_SHA` is c0ce100a. R-0229 and R-0230 are RESOLVED; R-0231 and
R-0232 are FIXED but carry `Landed:` lines only, so the next session's reviewer
gates R7 and authors their `Done:` text. NO PR exists for this branch; one is
created at CLOSURE. `.agent/candidates.md` is empty.

## Next Steps
- T003, one builder per round: migrate the prompt builders to compose through
  the registry, each round carrying its own content-equality golden, and wire
  `manifest_as_dicts()` into call evidence. Inventory the assembly sites first —
  that inspection is its own small round, because the ground is unknown.
- Then T004, the `remedy stats cache` view over actuals, reporting "not
  reported" for providers that report no cache figures rather than zeros.
- Then the integration gate (docs/agents/integration_gate.md), then closure per
  docs/roadmap/STATUS_closure_protocol.md, where the PR is created.

## Risks
- Roughly twenty assembly sites in three idioms (template `.format`, a `parts`
  join, f-string concatenation). Migration must not change content — goldens
  land before behaviour moves.
- The conventions headroom is thin: 60 estimated tokens on the worker document
  and 97 on the reviewer document against the cap of 800. Any later addition to
  either is measured BEFORE it is authored. A mutation red-proof at c0ce100a
  confirms the cap is enforced — padding past it turns 5 tests RED.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
- DECISION F105 D2 caps step blocks at 240 lines; F105's once-per-feature
  oversize-commit exception is already spent on `ea48ea89`.
