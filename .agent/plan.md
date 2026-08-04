# Plan — F071 Mission dossier

Branch: feature/f071-mission-dossier

## Goal
Long missions no longer die of context bloat: mission_dossier.py
maintains a hard-budgeted structured dossier (GOAL immutable,
MILESTONES, RISKS open-only, DECISIONS recent, NEXT) as the stable
prefix of the orchestrator prompt. Over budget compresses via one
schema-validated provider call under explicit rules; failure keeps
the previous dossier + raw facts with an honest over-budget flag.
Versions archived as dossier_v<N>.md. DONE — accepted 2026-08-03.

## Current Step
R4 (closure) COMPLETE. R3 verdict PASS + GATE PASS persisted;
R-0176 amendment applied to docs/agents/integration_gate.md;
Built State recorded in T1_F071.md (accepted HEAD acb02acd);
evidence job b3b98e3ee1d10668; package
remedy-review-20260803-190339-READY_FOR_REVIEW.zip
(SHA-256 aa117e26…); STATUS [x] + README sync (R-0177) in the
closure commit. PR open, NOT merged — it merges at the next
feature's Open PR Gate. Open findings: 0.

## Next Steps
- Next session: Rule A5 selects the next feature (F075 —
  MILESTONE GATE: 10 flawless self-runs). Its Open PR Gate merges
  this closure PR first.

## Risks
- None open for F071. Carried knowledge: version numbers are a
  monotonic high-water mark (torn-write self-heal, R-0175); gate
  run logs live outside the repo during a run (R-0176).
- .agent/candidates.md stays empty — this closure raised no
  candidates.
