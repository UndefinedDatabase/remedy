# Context — F080 machine-readable roadmap mirror (R2)

## Active Branch
feature/f080-roadmap-mirror — R1 PASS (LAST_REVIEWED_SHA 6787d6cf), cut
from main 1da1b07a. No PR this round; F080's PR is created only at
closure.

## Scope
F080 R2: persist the R1 verdict, T003 feature→mission adapter
(packages/orchestration/feature_mission_adapter.py + tests: detail file
→ PREPARED mission draft, one real feature file compiled end to end),
the docs page for the `plan` CLI group + its docs/README.md index line,
and the integration gate. T001/T002 are landed and unchanged this round.

## Constraints
- The adapter PREPARES and never executes: no job, no run, approval
  left to the standard human path, writes only under the data root.
  Zero jobs started is an acceptance criterion, not a nicety.
- Section mapping must stay traceable to the feature file: "How it
  fits" → context input, "Task slicing" → plan seed, "Acceptance" →
  DoD seed, "Do not touch" → fences.
- One parser only — reuse roadmap_index's feature-file machinery
  instead of a second markdown parser for the same grammar; reuse the
  existing mission/DoD compiler record shapes rather than inventing a
  parallel one.
- STATUS.md semantics and ownership stay human-owned (A4); no
  auto-checking of checkboxes; the generated index stays uncommitted.
- Commits < 500 lines; multiple commits expected.
- Test runner is pytest. Scoped per-file runs during build
  (tests/orchestration/test_feature_mission_adapter.py,
  test_roadmap_index.py, tests/docs/, tests/cli/test_golden_path.py);
  the ONE full `-n auto` run this round is Part D's integration gate
  per docs/agents/integration_gate.md, whose logs are written to the
  session scratchpad OUTSIDE the repo while the suite runs.

## Steps
Verdict persisted (Part A) → adapter (Part B) → adapter tests + real
feature-file e2e → docs page + index line (Part C) → integration gate
(Part D) → push + handoff rewrite.
