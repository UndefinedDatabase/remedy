# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 (the F104 closure) merged at the Open PR Gate. Build mode:
one-session self-drive, one delegated worker per round. Next finding ID: R-0229.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
Session ended at its declared FOUR-ROUND CAP with F105 work remaining — a clean
ending under docs/agents/self_drive_protocol.md G7, not a failure. R1 (claim,
candidate sweep, state reset) and R2 (T001) are both reviewer-gated **PASS**;
`LAST_REVIEWED_SHA` is **4d01a40a**. T001 is delivered as
`packages/orchestration/prompt_segments.py` — rank scale, registry,
`compose_prompt_segments`, segment manifest, `CONVENTIONS_TOKEN_CAP` — pinned by
22 tests in `tests/orchestration/test_prompt_segments.py`. The closing round
recorded both gates in `.agent/live_review.md` and wrote the session-end
`.agent/handoff.md`. NO PR exists for this branch; one is created at CLOSURE, not
now. `.agent/candidates.md` is empty.

## Next Steps
- R3 — T002: role loaders for docs/agents/worker_conventions.md and
  docs/agents/reviewer_conventions.md, importing `CONVENTIONS_TOKEN_CAP` instead
  of restating it, with content-equality goldens proving extraction changed no
  rule.
- R4+ — T003: migrate the prompt builders, ONE builder per round, each with its
  content-equality golden, and wire the segment manifest into call evidence.
- Then T004, the `remedy stats cache` view over actuals.
- Then the integration gate, then closure (the PR is created there).

## Risks
- Roughly twenty assembly sites in three idioms (template `.format`, a `parts`
  join, f-string concatenation). Migration must not change content — goldens
  land before behaviour moves.
- No tokenizer here: the conventions cap rides the chars/4 estimator in
  `packages/orchestration/token_economy.py`, so it is an ESTIMATE, documented as
  one rather than presented as a count.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
