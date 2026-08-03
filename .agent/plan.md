# Plan — F071 Mission dossier

Branch: feature/f071-mission-dossier

## Goal
Long missions no longer die of context bloat: mission_dossier.py
maintains a hard-budgeted structured dossier (GOAL immutable,
MILESTONES, RISKS open-only, DECISIONS recent, NEXT) as the stable
prefix of the orchestrator prompt. Over budget compresses via one
schema-validated provider call under explicit rules; failure keeps
the previous dossier + raw facts with an honest over-budget flag.
Versions archived as dossier_v<N>.md. DONE when a fixture mission
stays under budget across many iterations, survives recall checks,
and the dossier is the asserted prompt prefix.

## Current Step
R2 (SPLIT, LARGE repair+continue) DELIVERED — awaiting reviewer
verdict. R1's FAIL is repaired: R-0172 (rule check now judges the
REBUILT document), R-0173 (a stored version is immutable; an
identical rewrite is a no-op), R-0174 (IterationFacts docstring).
The R1 gate was re-run green BEFORE T003 started. T003 landed in
three slices: the live state + iteration facts + refresh, the loop
wiring through the existing assemble_context dossier seam, and the
reusable recall harness. Seven mutation red-proofs; one survivor
(the harness's `missing` set) produced a negative-control test.
No PR — closure creates it. The worker writes no verdict.

## Next Steps
- R3: integration gate per docs/agents/integration_gate.md.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The loop's compression provider is a SEPARATE opt-in seam so
  F070's one-call-per-iteration accounting is unchanged; the
  default path flags over-budget instead of compressing.
- The live state is JSON (dossier_state.json); the markdown
  versions stay a pure projection. See .agent/decisions.md.
- Do-not-touch held: no move-schema change, no new move kinds,
  cross-session handoffs (F079) untouched — the recall harness is
  published for F079 to reuse, not wired into it.
