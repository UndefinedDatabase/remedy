# Plan — F080 CLOSED; next up the self-drive skill (S1+S2)

Branch: feature/f080-roadmap-mirror — closure commit landed, PR open.
The PR is NOT merged here: it merges at the NEXT feature's Open PR
Gate, and the gap is the operator's manual-review window.

## Goal
F080 (Machine-readable roadmap mirror & STATUS.md) is DONE and accepted
at R5: STATUS carries `[x] F080` with the evidence job, package,
SHA-256 and accepted HEAD 0a22bcbf, README is synced in the same commit
(38 of 255 accepted; Tier 1 at 22 of 22), and the closure candidate is
on disk in .agent/candidates.md. Built: the roadmap parser with strict
grammar validation and its generated one-way index, `remedy plan
status` / `remedy plan next` (Rule A5, proposes and never starts),
report-only consistency checks, and the feature→mission adapter that
prepares a mission and never executes one.

## Operator constraint (verbatim)
From 2026-08-13 the operator reaches this machine ONLY via SSH from a
phone. Starting Claude Code and invoking ONE skill must be the only
required touchpoint. Target: operational and rehearsed by 2026-08-12.

## Sequence
1. F080 — DONE (R1–R5), PR open awaiting the next feature's Open PR
   Gate.
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
- Next session (fresh): the Open PR Gate merges F080's PR first, then
  the S1+S2 skill build per .agent/selfdrive_package.md.
- Window-1 bootstrap must read .agent/candidates.md: it holds ONE open
  candidate (bundles cannot carry full-suite node ids; the closure
  protocol should state the scoped-suites shape). It is a block
  condition at the next feature claim — register or resolve it in that
  round's first reviewed round.
- Rule A5 now names the next feature itself: `remedy plan next` reports
  F103 (Token ledger (SQLite)).

## Risks
- Hard date: self-drive operational and rehearsed by 2026-08-12.
- ADR-0001 (CYCLE_SAFETY_CAP) awaits human application; blocks
  multi-cycle loop delegation (S3 experiment lane), not the skill.
- The F080 PR must merge before unrelated work branches, or the Open PR
  Gate blocks the next feature.
