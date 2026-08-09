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
R5 — the repair round for the two R4 findings. R-0229 replaces the
self-referential segment-name assertion with literal-per-role assertions on both
conventions mappings, red-proved by exchanging the two names in a disposable
worktree. R-0230 makes an undecodable document fail as a `RoleConventionsError`
like a missing one. DECISION F105 D2 caps step blocks at 240 lines so the C1
save pair stops overrunning the AGENTS.md commit cap. R1, R2 and R3 are
reviewer-gated PASS; R4 gated FINDINGS, so `LAST_REVIEWED_SHA` stays 1a054862.
NO PR exists for this branch; one is created at CLOSURE, not now.
`.agent/candidates.md` is empty.

## Next Steps
- R6 — T002 part 2, the operator addition of 2026-07-30: a distilled
  write-discoverable-code block, sourced from the AGENTS.md "Code
  Discoverability Conventions" section, added to BOTH conventions documents as a
  reviewed diff of those documents, staying under the cap the R4 loader
  enforces.
- R7 — the session-terminator round: record the R5 and R6 gates and write the
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
  `packages/orchestration/token_economy.py`, so it is an ESTIMATE, documented as
  one rather than presented as a count. The headroom is real but small — the
  worker document estimates 505 tokens and the reviewer document 515 against a
  cap of 800 — so the R6 block must be distilled, not pasted.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
