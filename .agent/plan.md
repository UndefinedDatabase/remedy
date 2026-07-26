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
- [ ] T002 approve → write-back → immutability (late answer rejected)
- [ ] T003 assumptions.md renderer + CLI + plan.md link
- [ ] T004 interactive-input guard test + unattended end-to-end
- [ ] Integration gate
- [ ] Closure

## Current Step
T002 — approve writes answers back (supplied → answered_by "human",
unanswered → default_answer with answered_by "default"), answers become
immutable (late `--answer` rejected with "already resolved"), reject
leaves clarifications untouched.

## Next Steps
T002 write-back/immutability, T003 assumption log, T004 guard + e2e.

## Risks
- Schema changes must be additive: existing fp1 job data must keep loading.
- Question ids must be stable across plan regeneration (intake order).
- Conditional-answer predicates are OPTIONAL scope; skip unless trivially
  cheap and record the skip in the handoff.
