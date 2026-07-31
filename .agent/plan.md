# Plan — F053 Final & interim report (Tier 1)

## Goal
Every run produces ONE human-readable account: what was attempted, what
succeeded, what is blocked and why, what it cost, what needs answering,
and the single recommended next action. The report is a pure RENDERER
over existing structured sources — it computes nothing new, and a
missing source renders "not recorded", never a guessed value (P6,
docs/roadmap/features/T1_F053.md).

## Current Step
R1 complete, awaiting review. Claim + state reset, source inspection
(STEP 2), and T001 (renderer + next-action rule table + three golden
terminal fixtures) are committed and pushed on
`feature/f053-run-report`. Gates green: test_run_report.py 44 ·
tests/docs 293 · canary 42.

## Next Steps
- Reviewer verdict on R1. The worker writes no verdict and merges
  nothing.
- Open question for the reviewer (STEP 2 finding): no production reader
  of `docs/roadmap/STATUS.md` exists, so the milestone distance and the
  capability lines have no producer. `ReportSources.status_mirror` is
  the input seam; both sections render "not recorded" until a producer
  lands. Needs a routing decision — T002, a new slice, or a feature-file
  amendment.
- T002 (next round): terminal-state hook (every terminal path writes
  exactly one report, regenerated not appended) + interim mode against a
  running fake job + `remedy job report <id>` CLI with `--json` + the
  evidence-area source collection this round deliberately did not wire.

## Risks
- The six terminal statuses in `long_run_executor.TERMINAL_*` are the
  T002 hook surface; `max_cycles_reached` maps to JOB_RUNNING and is NOT
  a terminal report trigger. Enumerated in the handoff.
