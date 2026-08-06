# Context — F080 machine-readable roadmap mirror (R1)

## Active Branch
feature/f080-roadmap-mirror — cut from main 1da1b07a after the Open PR
Gate merged PR #182 (plan0806 registration). No PR this round; F080's
PR is created only at closure.

## Scope
F080 R1: candidate sweep + claim + T001 (pure parser
packages/orchestration/roadmap_index.py, strict grammar validation with
`<file>:<line>: <what>` errors, JSON index writer under the data root,
CLI group `plan` with `status` / `next`) + T002 (report-only
consistency checks). T003 (feature→mission adapter) is R2, not here.

## Constraints
- STATUS.md semantics and ownership stay human-owned (A4); no
  auto-checking of checkboxes; the generated index is never committed
  (one-way mirror under REMEDY_DATA_DIR, regenerated on every read).
- `plan status` / `plan next` PROPOSE only — they never start a job.
  Per STATUS Rule A5 an in-progress `[~]` line is the active feature;
  otherwise the first `[ ]` line is next.
- Grammar violations are the only hard failures; consistency findings
  are reported, never fatal. Duplicate feature ids: hard error.
- Commits < 500 lines; multiple commits expected.
- Test runner is pytest, invoked per-file (tests/orchestration/
  test_roadmap_index.py, tests/cli/test_plan_cli.py, tests/docs/,
  tests/cli/test_golden_path.py) — no full-suite or xdist runs from
  the worker window (resource safety).

## Steps
Sweep committed (6f529456) → claim (STATUS [~], live_review reset) →
T001 parser+tests → T001 CLI+tests → T002 checks+tests → push +
handoff rewrite.
