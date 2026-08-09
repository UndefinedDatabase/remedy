# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 — the F104 closure — was merged at the Open PR Gate. Build mode:
one-session self-drive (docs/agents/self_drive_protocol.md), one delegated
worker per round. Next free finding ID: R-0229.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals, so the
ordering's value is visible in numbers rather than asserted. Prompt CONTENT does
not change; only its composition.

## Current Step
R1 — claim, candidate sweep, state reset. F105 goes `[~]` in
docs/roadmap/STATUS.md under Rule A5. Both F104 closure candidates are RESOLVED
as written rules in docs/agents/planner_reviewer_prompt.md — §4.4 gains the
`Landed:` versus `Done:` split, §4.13 names the terminating convention — and
`.agent/candidates.md` is emptied. No production code this round.

## Next Steps
- R2 — T001: `packages/orchestration/prompt_segments.py` with the segment
  registry, the documented rank scale, `compose()` and its stable delimiters,
  the segment manifest, and `tests/orchestration/test_prompt_segments.py`
  (ordering stability, delimiter stability, over-cap loader failure).
- R3 — T002: role loaders for the existing docs/agents/worker_conventions.md and
  docs/agents/reviewer_conventions.md under the token cap, with the
  content-equality goldens that prove extraction changed no rule.
- R4+ — T003, one builder per round, each with its content-equality golden;
  T004 the cache stats view last; then the integration gate and closure.

## Risks
- Roughly twenty assembly sites in three idioms (template `.format`, a `parts`
  list join, f-string concatenation). Migration must not change content —
  goldens land before behaviour moves.
- No tokenizer exists in this repo: the conventions cap has to ride the
  chars/4 estimator in `packages/orchestration/token_economy.py`, so the cap is
  an ESTIMATE and must be documented as one rather than presented as a count.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
