# Plan — F034 Bundled clarification in the Flight Plan

## Goal
All open questions are asked ONCE, bundled, at plan time — never again:
intake clarifications ride the single plan-approval decision; every
unanswered question runs on its documented conservative default; the
runtime is provably incapable of asking mid-run. Done when an unattended
`remedy do --yes` completes with all defaults recorded in an assumption
log, and a guard test fails the build if interactive prompting ever enters
the execution packages.

## Checklist
- [x] Setup: Open PR Gate (#150 merged), branch, STATUS claim, state files
- [x] T001 decision payload + per-question answer parsing + tests
- [x] T002 approve → write-back → immutability (late answer rejected)
- [x] T003 assumptions.md renderer + CLI + plan.md link
- [x] T004 interactive-input guard test + unattended end-to-end
- [x] Integration gate — no F034-attributable regression (verdict in
      .agent/live_review.md)
- [ ] Closure

## Current Step
Integration-gate handback — both full-suite runs recorded raw, all 7
branch-only failures attributed to pre-existing flake with serial-rerun
and base-repeat evidence, canary green. Awaiting the reviewer.

## Next Steps
Closure (evidence job, review zip, STATUS line) after the gate verdict.

## Risks
- Suite nondeterminism is pre-existing: tests/cli/ shows 27 failures on both
  base and branch (25 identical; the 2+2 differences pass on serial re-run).
  Backlog F135/F052.
- Conditional-answer predicates skipped as OPTIONAL scope (see
  .agent/decisions.md). Nothing in F034's DONE criteria depends on them.
- The guard only covers packages/; apps/cli deliberately stays interactive-
  capable, so a prompt added under apps/ that the runner calls would evade
  it. Runner entry points live in packages/, which is what is guarded.
