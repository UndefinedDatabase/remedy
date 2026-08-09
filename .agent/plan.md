# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 (the F104 closure) merged at the Open PR Gate. Build mode:
one-session self-drive, one delegated worker per round. Next finding ID: R-0231.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
R6 — T002 part 2. The operator addition of 2026-07-30 lands as a reviewed diff of
both conventions documents: a distilled write-discoverable-code block in the
worker document and its checking counterpart in the reviewer document, measured
by the reviewer at 740 and 703 estimated tokens against the cap of 800. R1, R2,
R3 and R5 are reviewer-gated PASS, R4 gated FINDINGS and both its findings are
now RESOLVED, and `LAST_REVIEWED_SHA` is a8e9ab1f. T002 is complete once this
round gates. NO PR exists for this branch; one is created at CLOSURE, not now.
`.agent/candidates.md` is empty.

## Next Steps
- R7 — the session-terminator round: record the R6 gate and write the
  session-end handoff. This session's declared cap is four rounds, R4 through R7,
  so T003 starts in the NEXT session.
- Then T003: migrate the prompt builders, ONE builder per round, each with its
  content-equality golden, and wire the segment manifest into call evidence.
- Then T004, the `remedy stats cache` view over actuals, then the integration
  gate, then closure (the PR is created there).

## Risks
- Roughly twenty assembly sites in three idioms (template `.format`, a `parts`
  join, f-string concatenation). Migration must not change content — goldens
  land before behaviour moves.
- No tokenizer here: the conventions cap rides the chars/4 estimator in
  `packages/orchestration/token_economy.py`, so every number is an ESTIMATE. The
  headroom after R6 is thin — 60 tokens on the worker document and 97 on the
  reviewer document — so any later addition to either is measured before it is
  authored, not after.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
