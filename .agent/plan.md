# Plan — plan0806: F255 registered; self-drive package queued

Branch: feature/reg-f255-teacher-role — registration PR open, merges
at the next round's Open PR Gate.

## Goal
Round plan0806 (operator-relayed) done: F255 (teacher role) registered
in Tier 5, ledger pinned at 255; single-command self-drive package
planned in .agent/selfdrive_package.md (full S1–S5 text + round
shapes + runtime rows there — it is part of this plan).

## Operator constraint (verbatim)
From 2026-08-13 the operator reaches this machine ONLY via SSH from a
phone. Starting Claude Code and invoking ONE skill must be the only
required touchpoint. Target: operational and rehearsed by 2026-08-12.

## Sequence (after this PR merges)
1. F080 (Machine-readable roadmap mirror & STATUS.md) — its R1 MUST
   sweep the three .agent/candidates.md entries (R-0200, R-0202,
   xdist flake): register or resolve each; they block the F080 claim.
2. S1+S2 — build skill /build-remedy-self per the package: one-session
   Window-1 discipline (state probe -> decide -> rounds in-session),
   hard guardrails (PR-only merges at Open PR Gate, no force-push,
   explicit gates, .agent/STOP / session-limit / ambiguity ->
   F079 handoff + clean end).
3. S4 — rehearsal: F254 built through the skill, operator present;
   success = accepted with zero operator edits beyond starting it.
4. Normal feature flow through the skill (S5: review-zip stays the
   operator's remote window).

## Next Steps
- Push branch, open PR for plan0806 (registration + planning docs).
- Next session: F080 per sequence above.

## Risks
- Hard date: self-drive operational and rehearsed by 2026-08-12.
- ADR-0001 (CYCLE_SAFETY_CAP) awaits human application; blocks
  multi-cycle loop delegation (S3 experiment lane), not the skill.
- Candidates R-0200/R-0202/xdist flake block the F080 claim until
  its R1 sweeps them.
