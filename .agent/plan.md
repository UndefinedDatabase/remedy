# Plan — F080 Machine-readable roadmap mirror & STATUS.md (R1)

Branch: feature/f080-roadmap-mirror — claimed after the Open PR Gate
merged PR #182 (main 1da1b07a).

## Goal
F080 R1 (SPLIT, LARGE): candidate sweep (done — R-0200 → T9_F163,
R-0202 → T2_F085, R-0204 → T7_F135; .agent/candidates.md now empty),
claim (STATUS [~]), then T001 (pure parser roadmap_index.py + strict
grammar validation with file:line errors + index writer under the data
root + CLI `remedy plan status` / `remedy plan next`) and T002
(report-only consistency checks). Index is a one-way mirror, never
committed; STATUS.md stays human-owned (A4).

## Operator constraint (verbatim)
From 2026-08-13 the operator reaches this machine ONLY via SSH from a
phone. Starting Claude Code and invoking ONE skill must be the only
required touchpoint. Target: operational and rehearsed by 2026-08-12.

## Sequence
1. F080 (Machine-readable roadmap mirror & STATUS.md) — R1 in progress;
   its candidate sweep is done, so the claim is unblocked.
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
- R1 done: sweep, claim, T001 (parser + grammar + index writer + CLI
  status/next) and T002 (consistency checks) are committed and green;
  branch pushed, no PR (F080's PR is created only at closure).
- R2: T003 feature→mission adapter + end-to-end compile of one real
  feature file, no execution side effects.
- Open for R2/closure: docs/ entry for the new `plan` CLI group — out
  of this round's declared change scope.

## Risks
- Hard date: self-drive operational and rehearsed by 2026-08-12.
- ADR-0001 (CYCLE_SAFETY_CAP) awaits human application; blocks
  multi-cycle loop delegation (S3 experiment lane), not the skill.
- Parser anchors are markdown header conventions — grammar strictness
  must not turn existing valid feature files red (tests/docs/ is the
  guard).
