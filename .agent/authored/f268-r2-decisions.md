
## DECISION F268 D5 (2026-09-18, reviewer, round 2) — the shape is read from the mission plan, and the force flags override it
CONTEXT: measured at `f0210593`, `mission_compiler.plan_mission` returns a plan whose milestones each
carry `jobs_draft` outlines, the deterministic plan holds exactly one milestone with one outline, and
nothing turns an outline into a job.
CHOSEN: the plan step keeps the plan it produced on the walk's context, and one pure function in
`packages/orchestration/do_sequence.py` reads the shape from it: `"milestones"` when the plan's
outlines number two or more across all milestones, otherwise `"one job"`. `--force-job` makes the
shape `"one job"` whatever the plan says; `--force-mission` makes it `"milestones"`; both together
exit 2. Under `"milestones"` the shape step plans one job per outline, the outline's goal being that
job's order; when fewer than two outlines exist (the deterministic plan, and every forced mission
over it), the jobs are one per deliverable of DECISION D6, and when the order has a single
deliverable the second job is its check — one task whose deliverable is the named check that the
first job's deliverable meets the order. The first job is linked `initial` and every later one
`follow_up`, each with `repo_path` set; the run step runs them in order and stops at the first that
does not complete; the apply step prints one real apply command per job. `--json` carries `shape`
and `shape_source` (`planner`, `--force-job` or `--force-mission`).
ALTERNATIVES: add a shape field to `MissionPlanDraft`, rejected because the planner's internals are
this feature's Do-not-touch and the outline count already is the planner's structured answer;
build the follow-up jobs through `mission_state.continue_mission`, rejected because it sets no
`repo_path` and builds verify-first tasks from a previous job's DoD, which a job that has not yet
run does not have. REVERSE: delete the shape function, the two flags and the multi-job branch;
delete this paragraph.

## DECISION F268 D6 (2026-09-18, reviewer, round 2) — tasks are bounded by deliverables, and one validator enforces it
CONTEXT: measured at `f0210593`, `job_runner.plan_job` (the deterministic skeleton `do` falls back
to) makes the same three tasks for every order — `analyze_requirements`,
`define_acceptance_checks`, `prepare_implementation_plan` — none naming a deliverable and the first
an inspection task, which R-0808 and DECISION amend0911-feedback D3 forbid; no task model has a
deliverable field; the only task-count cap is `_MAX_TASK_PLAN_TASKS = 25`, which rejects a plan
rather than truncating it.
CHOSEN: a new pure module `packages/orchestration/task_deliverables.py` holds (a) the deterministic
deliverable extractor — the file-path-like tokens of the order in order of first appearance,
deduplicated, and the order itself as the single deliverable when it names none; (b) the
deterministic job plan `do` uses in place of `job_runner.plan_job`: one task per deliverable, its
deliverable recorded in the task's `inputs["deliverable"]`, one acceptance item each (so every
`planning.granularity.*` ceiling holds), and more deliverables than `_MAX_TASK_PLAN_TASKS` become
several jobs rather than a truncated one; (c) one validator, run by `plan_order_job` on every job it
plans, deterministic or LLM, that rejects a job holding a task with no deliverable or a task whose
title begins with an inspection verb, the reject surfacing as the existing `OrderJobPlanError`. An
LLM task's deliverable is its first `files_hint` entry, else its first acceptance line.
`job_runner.plan_job` and its own tests stay as they are; `do` no longer calls it.
ALTERNATIVES: a required `deliverable` field on `PlannedTask`, rejected as a planner-internals change
that would re-shape every `task_plan_v1` payload the suite builds; rewriting `job_runner.plan_job`,
rejected because its tests pin it as a standalone planner and `do` is its only production caller.
REVERSE: route `plan_order_job` back to `job_runner.plan_job`, delete the module and the validator
call; delete this paragraph.

## DECISION F268 D7 (2026-09-18, reviewer, round 2) — a surviving hint names a real command or nothing
CHOSEN: when the deletion of `--fixture-builder` leaves a surface naming it (R-0964), the surface
drops the flag where the rest of its invocation still parses, and otherwise names a real command
carrying the real job id; `_pipeline_next_command`'s prose-only and malformed-output stop reasons
return `remedy job show <job id> --full --json`, which the parser accepts and which shows the
output the provider returned. ALTERNATIVES: point those stop reasons at `remedy do` with a fake
provider, rejected because a fake run is not a diagnosis of a real provider's malformed output.
REVERSE: restore the old strings from git history; delete this paragraph.
