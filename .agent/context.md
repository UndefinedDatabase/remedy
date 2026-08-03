# Context — F069 Mission compiler (Tier 1)

## Active Branch
`feature/f069-mission-compiler`
Base commit: main after PR #174 merge (F062 closure), `53ac3efa`

## Steps (round map)
R1 (SPLIT, LARGE bundle): claim `[~]` + T001 schema `mission_plan_v1`
+ milestone-DAG validation + compiler + deterministic fallback +
three long-goal golden fixtures; then T002 per-milestone DoD hand-off
through the F061 compiler + additive persistence + mission_plan.md
rendering + the no-autostart guarantee; then T003 CLI
`remedy mission plan <id>` + recompile versioning + in-progress
refusal.
Next: integration gate per docs/agents/integration_gate.md.
Then: closure — its own round.

## Scope
`packages/orchestration/**` (mission_compiler, the MissionPlan
schema, the additive mission-record field, mission_plan rendering),
`apps/cli/commands/mission_cmd.py` (the `plan` subcommand),
`tests/orchestration/test_mission_compiler.py` plus fixtures under
`tests/orchestration/fixtures/`, `tests/cli/test_mission_cmd.py`,
`docs/roadmap/STATUS.md` (claim line only), and `.agent/` state.
Nothing beyond.

## Gates (round verification, pytest)
python3 -m pytest tests/orchestration/test_mission_compiler.py \
    tests/orchestration/test_mission_state.py \
    tests/orchestration/schemas -q                    scoped slice gate
python3 -m pytest tests/cli/test_mission_cmd.py -q    CLI slice gate
python3 -m pytest tests/cli/test_golden_path.py -q    canary
python3 -m pytest tests/docs/ -q                      docs-round gate
Integration gate: full suite with pytest -n auto, branch AND base,
per docs/agents/integration_gate.md.
Resource safety: everything runs through these pytest wrappers; the
compiler starts no process and touches no worktree, so there is no
subprocess fan-out to bound — the no-autostart negative test pins it.

## Constraints
- Milestone DoDs are compiled through the F061 `compile_dod` ONLY —
  no second DoD mechanism (Rule A6).
- The compiler has ZERO execution side effects: no jobs created,
  nothing started, no worktree touched (pinned negative test).
- `jobs_draft[]` entries are outlines, never runnable jobs.
- Provider absence → honest deterministic fallback: ONE milestone
  wrapping the whole goal, labeled deterministic (P6, never silently
  pretending to be a real plan).
- Validator discipline mirrors `FlightPlan._validate_dag`: duplicate
  ids, unknown deps, cycles, hard cap 12 milestones (over-cap =
  parse-class "hallucinated scope").
- Milestone goals must be outcome-phrased; a documented lint-style
  heuristic rejects obvious task-lists-as-milestones.
- Persistence on the mission record is ADDITIVE and OPTIONAL — no
  silent MISSION_SCHEMA_VERSION bump; a required bump is a declared
  deviation.
- Prompt-building/call helpers are REUSED; a copy is extracted into a
  shared helper instead (feature file, Orchestrator brief).
- Reviewer-authored texts under .agent/authored/ are applied by copy
  and sha256-verified before use; never hand-edited.
- Commits stay under 500-line diffs (AGENTS.md).
- Mutation red-proofs only in a disposable git worktree (R-0160); the
  primary checkout is porcelain-clean at handback.
- context.md satisfies its FULL test reader list: a "Steps" section,
  "## Active Branch" with a feature/ slug, a roadmap F-id, and this
  pytest/resource line (R-0162; reader rule in
  planner_reviewer_prompt.md §4 item 11).

## Do not touch
Execution, job creation, dossier maintenance, loop policy. Harness /
process semantics. docs/roadmap/ROADMAP.md; STATUS entries other than
the F069 claim line.
