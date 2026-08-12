# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Next free finding ID: R-0298. Last reviewed SHA: none yet (R1 in flight).

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R1 — claim F111, reset the session state files, and carry the 22 open F107
findings forward. No production code this round: which repair path owns the
response-side diff channel is not yet settled, and R2 opens with that
DECISION rather than guessing.

## Next Steps
1. R2 — the repair-path DECISION, its feature-file amendment, and T001: the
   hunk selection helper plus unit tests.
2. T002 — response schema, fence pre-check, strict apply with conflict
   fallback.
3. T003 — wiring into repair rounds, mode and token evidence, a fixture
   comparison recording both modes' token counts.
4. Integration gate, then closure.

## Risks
- The ping-pong repair round's builder is an agentic CLI that edits staging
  itself: `BuilderOutput` carries no patch field and `apply_structured_patch`
  is never called from `pingpong_loop.py`. The prompt-side saving is
  reachable there; the response-side diff channel is not. R2 settles this as
  a recorded DECISION, never as a silent re-plan.
- The full suite is RED at the merge base with five known ids (R-0286), so
  the integration gate must compare base against branch, not read absolute
  green.
