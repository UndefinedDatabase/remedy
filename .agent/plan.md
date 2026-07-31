# Plan — F053 Final & interim report (Tier 1)

## Goal
Every run produces ONE human-readable account: what was attempted,
what succeeded, what is blocked and why, what it cost, what needs
answering, and the single recommended next action. The report is a
pure RENDERER over existing structured sources — it computes nothing
new, and a missing source renders "not recorded", never a guessed
value (P6, docs/roadmap/features/T1_F053.md).

## Current Step
R1 — claim + state reset (this commit), then inspect the report
sources with file:line evidence, then T001: renderer +
next-action rule table + three golden terminal fixtures.

## Next Steps
- STEP 2: name the exact module + accessor for every rendered source;
  confirm or disprove the all-inputs-exist claim; enumerate every
  terminal state the persistence path reaches (T002 input only).
- STEP 3 (T001): packages/orchestration/run_report.py
  `render_report(job, mode=final|interim)` +
  tests/orchestration/test_run_report.py (three goldens, basis on
  every cost line, "not recorded" negative test, interim label,
  deterministic double-render).
- Gates: test_run_report.py green · tests/docs 293 · canary 42.
- Handback per docs/agents/handback_template.md; reviewer writes the
  verdict, not the worker.
- T002 (later round): terminal-state hook + interim mode + CLI.
