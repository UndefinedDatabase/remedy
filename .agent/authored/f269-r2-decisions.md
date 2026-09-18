
## DECISION F269 D4 (2026-09-18, reviewer, round 2) — the contract is compiled by F061's compiler, gated inside each job's own DoD, and holds the loop's achieve move
CONTEXT: T2_F269.md T002 rules "F061's compiler over the criteria; the mission gate that holds a
mission open on a red blocking criterion", reusing `dod_gate.py` and never a second mechanism, and
its Acceptance wants an amendment to change "the DoD of the next round". Measured at `17edb194`:
`dod_compiler.compile_dod` turns a `TaskPlan`'s acceptance lines into `DoDCheck`s whose
`acceptance_refs` name `<task id>:<index>`, and with no provider it falls back to one pytest check
per distinct selector; `dod_gate.run_job_gate` evaluates a job's stored DoD in the job's workspace
inside `execute_dispatched_job` and persists the result by job id; `evaluate_move` refuses
`declare_mission_achieved` only for a missing plan or an open milestone; `remedy mission achieve`
calls `set_mission_status` with no guard, and its catalog entry calls it an explicit human
judgement; `plan_mission` writes no contract.
CHOSEN: (1) COMPILE. `mission_contract.py` gains a compiler that builds a `TaskPlan` with one task
per criterion (task id = criterion id, `acceptance` = [the criterion text]), calls
`dod_compiler.compile_dod`, and gives each criterion the FIRST check whose `acceptance_refs` holds
`<criterion id>:0`, stored as that check's `model_dump(mode="json")` with `id` set to
`ctr-<criterion id>`, `acceptance_refs` set to [`<criterion id>:0`] and `blocking` set to the
criterion's own. (2) PLANNER CRITERIA. `plan_mission`, after the milestone DoDs are attached,
writes the mission's contract: every criterion whose origin is not `planner` is kept with its id,
and the planner criteria are replaced by one per milestone of the compiled plan — text = the
milestone's goal, `milestones` = [its id], blocking — with fresh ids after the highest kept one,
all compiled by (1) with no provider (`call_fn=None`, F061's own deterministic path). (3) THE JOB'S
DoD CARRIES ITS SLICE. At dispatch, after `attach_milestone_dod`, the orchestrator merges the
job's slice checks into that job's stored DoD through `dod_gate.load_dod` and `store_dod`, adding a
criterion's check only when no check already in the DoD has the same `kind` and `spec`, and
creating a DoD from the slice checks when the job has none. (4) RESULTS. After the dispatched job
has executed, the orchestrator reads that job's stored DoD and gate result and sets each slice
criterion whose check's `kind` and `spec` match a DoD check to `met` when that check's evidence
passed and `unmet` otherwise, with `evidence_ref` = `<job id>:<check id>`; a job with no gate
result changes nothing. (5) THE GATE. A contract's blockers are its blocking criteria whose status
is not `met`. `evaluate_move` refuses `declare_mission_achieved` while any exist, naming their ids,
after the existing plan and milestone refusals; a contract body that breaks a D2 rule refuses with
the rule. `remedy mission achieve` stays the human's explicit judgement and is NOT refused: it
prints one line naming the unmet blocking criteria before its status line (text) and carries them as
`unmet_blocking_criteria` (`--json`). (6) `remedy do --json` reports the mission's contract body,
or null when it has none, in place of DECISION F268 D1's fixed null.
ALTERNATIVES: a mission-level evaluation of the criteria's checks, rejected because it needs a
tree the job gate already has and would run the same checks a second time — the second mechanism
T002 forbids; refusing `mission achieve` too, rejected for now because the catalog defines it as
the operator's override, and recorded as an operator question instead; passing the planner's
structured call function to the contract compiler, rejected because that function is built for the
mission-plan schema, not the DoD draft schema. REVERSE: drop the calls from `plan_mission` and
`execute_move`, delete the compiler, merge and result functions with their tests, restore
`do`'s null, and delete this paragraph.
