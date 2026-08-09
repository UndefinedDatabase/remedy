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
R2 — T001 DONE, awaiting review. `packages/orchestration/prompt_segments.py`
holds the mechanism: `SegmentStabilityRank` (SYSTEM=0 … STEERING=5),
`PromptSegmentRegistry.register()` with the `token_cap` check on the chars/4
estimator, `compose_prompt_segments()` ordering by (rank, registration index)
over a bare-blank-line `PROMPT_SEGMENT_DELIMITER`, and the
`PromptSegmentManifestEntry` audit rows. 22 tests in
`tests/orchestration/test_prompt_segments.py`. No builder migrated, no prompt
content changed, nothing else under `packages/orchestration` touched.

## Next Steps
- R3 — T002: role loaders for the existing docs/agents/worker_conventions.md and
  docs/agents/reviewer_conventions.md (both files present) under
  `CONVENTIONS_TOKEN_CAP`, with the content-equality goldens that prove
  extraction changed no rule.
- R4+ — T003, one builder per round, each with its content-equality golden, and
  the segment manifest wired into call evidence; T004 the cache stats view last;
  then the integration gate and closure.

## Risks
- Roughly twenty assembly sites in three idioms (template `.format`, a `parts`
  list join, f-string concatenation). Migration must not change content —
  goldens land before behaviour moves.
- No tokenizer exists in this repo: the conventions cap has to ride the
  chars/4 estimator in `packages/orchestration/token_economy.py`, so the cap is
  an ESTIMATE and must be documented as one rather than presented as a count.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
