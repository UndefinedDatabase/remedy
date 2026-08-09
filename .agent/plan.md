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
R4 — T002 part 1. `packages/orchestration/role_conventions.py` loads the two
EXISTING conventions documents verbatim as the conventions segment, under the
`CONVENTIONS_TOKEN_CAP` imported from `prompt_segments` rather than restated, and
`tests/orchestration/test_role_conventions.py` holds the content-equality
goldens that prove the loaders changed no rule. R1, R2 and R3 are reviewer-gated
PASS; `LAST_REVIEWED_SHA` is 1a054862. NO PR exists for this branch; one is
created at CLOSURE, not now. `.agent/candidates.md` is empty.

## Next Steps
- R5 — T002 part 2, the operator addition of 2026-07-30: a distilled
  write-discoverable-code block, sourced from the AGENTS.md "Code
  Discoverability Conventions" section, added to BOTH conventions documents as a
  reviewed diff of those documents, staying under the cap the R4 loader
  enforces.
- R6+ — T003: migrate the prompt builders, ONE builder per round, each with its
  content-equality golden, and wire the segment manifest into call evidence.
- Then T004, the `remedy stats cache` view over actuals.
- Then the integration gate, then closure (the PR is created there).

## Risks
- Roughly twenty assembly sites in three idioms (template `.format`, a `parts`
  join, f-string concatenation). Migration must not change content — goldens
  land before behaviour moves.
- No tokenizer here: the conventions cap rides the chars/4 estimator in
  `packages/orchestration/token_economy.py`, so it is an ESTIMATE, documented as
  one rather than presented as a count. The headroom is real but small — the
  worker document estimates 505 tokens and the reviewer document 515 against a
  cap of 800 — so the R5 block must be distilled, not pasted.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
