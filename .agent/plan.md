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
- [x] Integration gate — no F034-attributable regression (reviewer verdict
      in .agent/live_review.md)
- [x] Repair R-0144 (resolved, reviewer-verified)
- [ ] Closure

## Current Step
Closure — integrity check, evidence job attesting T001–T004, fresh review
zip, Built State in the feature file, authored STATUS line, PR #151
finalized. Do NOT merge: the Open PR Gate handles that at the next
feature start.

## Next Steps
None after closure.

## Risks
- Suite nondeterminism is pre-existing: tests/cli/ shows 27 failures on both
  base and branch (25 identical; the 2+2 differences pass on serial re-run).
  Backlog F135/F052.
- Conditional-answer predicates skipped as OPTIONAL scope (see
  .agent/decisions.md). Nothing in F034's DONE criteria depends on them.
- The guard only covers packages/; apps/cli deliberately stays interactive-
  capable, so a prompt added under apps/ that the runner calls would evade
  it. Runner entry points live in packages/, which is what is guarded.
