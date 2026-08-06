# Context — plan0806 registration + self-drive planning round

## Active Branch
feature/reg-f255-teacher-role — registration micro-round (precedent
reg0803). PR open after handback, NOT merged; merges at the next
round's Open PR Gate. F079 PR #181 was merged by this round's gate.

## Scope
Docs/planning only, no product code. Part 1: F255 (teacher role)
registered in Tier 5 — STATUS line, T5_F255.md (scope verbatim),
TOTAL_FEATURES 255, README counts, one commit. Part 2: single-command
self-drive package planned in .agent/selfdrive_package.md; plan.md
carries the sequence and the operator constraint verbatim.

## Constraints
- Registration is NOT a feature claim: the three candidates (R-0200,
  R-0202, xdist flake) do not block here; they block the F080 claim
  and its R1 must sweep them.
- Self-drive is planning output only; build sequenced AFTER F080
  closes. Hard date: operational and rehearsed by 2026-08-12
  (operator SSH-only from 2026-08-13).
- ADR-0001 stays PROPOSED; CYCLE_SAFETY_CAP stays 1 until a human
  applies it — prerequisite for multi-cycle loop delegation (S3).

## Steps
Part 1 done (commit 419a6243, both gates green) → Part 2 planning
docs committed → push + PR → next: F080 in a fresh session.
