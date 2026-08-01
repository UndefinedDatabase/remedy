# Context — F056 Missions (Tier 1)

## Active Branch
`feature/f056-missions`
Base commit: `78f5f608` (main after PR #170 merge)

## Steps (round map)
R1 (LARGE): STATUS claim `[~]` + state reset → T001 record/store/
link/list/show → T002 intake hint + approval opt-in (default NO) →
T003 continue + injected verify-first + two-job fixture e2e.
Closure is its own later round.

## Scope
`packages/orchestration/mission_state.py` (new), CLI wiring for
`remedy mission start|continue|list|show`, the intake
mission-candidate hint, the plan-approval payload opt-in, plus
`tests/orchestration/test_mission_state.py` and
`tests/cli/test_mission_cmd.py`. Also `docs/roadmap/STATUS.md` and
`.agent/` state. Nothing beyond.

## Gates (round verification, pytest)
python3 -m pytest tests/orchestration/test_mission_state.py \
    tests/cli/test_mission_cmd.py -q     per-slice gate
python3 -m pytest tests/cli/test_golden_path.py -q   canary
python3 -m pytest tests/docs/ -q                     docs gate
Resource safety: everything runs through these pytest wrappers; no
unbounded subprocess fan-out from state-file tooling.

## Constraints
- Missions never auto-create: opt-in defaults to NO; a plain
  do-flow creates none (negative test required).
- Mission goals are immutable — a changed goal is a new mission.
- One job belongs to at most one mission (validator).
- A linked job that no longer exists renders "(missing job)";
  listings never crash, corrupt records are skipped and counted.
- Nothing auto-transitions mission status in this feature.
- Storage like other entities: atomic JSON per record under a
  project-scoped area of the data root.
- Reviewer-authored texts under .agent/authored/ are applied by
  copy and sha256-verified before use; never hand-edited.
- Commits stay under 500-line diffs (AGENTS.md).
- context.md satisfies its FULL test reader list: a "Steps"
  section, "## Active Branch" with a feature/ slug, a roadmap
  F-id, and this pytest/resource line (R-0162; reader rule in
  planner_reviewer_prompt.md §4 item 11).

## Do not touch
The orchestrator loop (later feature), lineage UI, dossier CONTENT
— only reserve the field. docs/roadmap/ROADMAP.md; STATUS entries
other than the F056 line.
