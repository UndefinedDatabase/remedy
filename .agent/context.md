# Context — F053 Final & interim report

## Active Branch
`feature/f053-run-report`
Base commit: `15105dbe` (main after PR #168 merge)

## Scope
T001 only this round: `packages/orchestration/run_report.py` as a pure
renderer plus `tests/orchestration/test_run_report.py`. The inspect
step (STEP 2) is read-only evidence gathering; it wires nothing.

## Constraints
- Pure renderer (P6): every number names its basis; a missing source
  renders "not recorded"; the renderer never computes or guesses a
  value that is not already structured data.
- Deterministic ordering — double render must be byte-identical.
- Milestone distance comes from the STATUS mirror, never
  hand-maintained. Momentum flag uses the mechanical definition in
  T1_F053.md. "can now" capability lines cite ONLY accepted `[x]`
  state.
- Reports are English regardless of mission language; mission text is
  quoted as-is. Per-task lines cap with an "and N more" line (A9).
- Reviewer-authored texts under `.agent/authored/` are applied by copy
  and sha256-verified before use; STATUS.md and live_review.md are
  such texts this round and are never hand-edited.
- Commits stay under 500-line diffs (AGENTS.md); multiple commits per
  round are expected.

## Gates
`python3 -m pytest tests/orchestration/test_run_report.py -q` green ·
`tests/docs/` 293 · canary `tests/cli/test_golden_path.py` 42. Round
touches docs/roadmap/** → the docs gate applies
(docs/agents/planner_reviewer_prompt.md §3 item 5).

## Do not touch
Notification delivery, UI rendering, cost calibration (feature file
Do-not-touch). No CLI and no terminal-state hook — both are T002.
`docs/roadmap/ROADMAP.md`; STATUS entries other than the F053 line.
