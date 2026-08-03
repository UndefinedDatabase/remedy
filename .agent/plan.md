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
R3 (SPLIT, LARGE repair+gate) DELIVERED — awaiting reviewer verdict.
R-0175 fixed: refresh_mission_dossier reconciles the version against
the archive before writing, so a torn write heals on the next
refresh instead of wedging the mission; reproduced before the fix,
verified after, pinned by six tests. The R2 gate was re-run green
BEFORE the integration gate started.
INTEGRATION GATE PASS: branch 15383 passed / 19 skipped / exit 0;
base 15274 / 19 / exit 0 at merge base 097e4959; comm -13 EMPTY,
comm -23 EMPTY, dist parity hash UNCHANGED. Evidence in
.agent/gate_f071_r3/ (.txt names). No closure work this round.

## Next Steps
- R4: closure per docs/roadmap/STATUS_closure_protocol.md — Built
  State, evidence job, review zip, STATUS [x] + README sync, PR.

## Risks
- Version numbers are a monotonic high-water mark, not an update
  counter: a torn run consumes one number. Explicit exception to
  the one-update-one-version decision (.agent/decisions.md).
- Gate evidence must be written OUTSIDE the repo during the run —
  an in-repo log changes remedy_worktree_digest mid-run and fails
  the identity tests. Recorded for the reviewer; no doc amended.
- Do-not-touch held: no move-schema change, no new move kinds,
  F079 untouched (the recall harness is published, not wired in).
