
## DECISION F269 D6 (2026-09-18, reviewer, round 5) — whole-mission checks are reported, not blocking, in a job's DoD; `do`'s job is gated before its worktree goes
CONTEXT: DECISION F269 D3 (2) puts every whole-mission criterion in every job's slice, and D4 (3)
merges each slice check into the job's DoD with the criterion's own `blocking`. Read at `09d7641f`
in `packages/orchestration/orchestrator_loop.py`: `evaluate_milestone_done` refuses a milestone
whose job's gate did not release. A whole-mission criterion describes the mission's end state, so a
mission with two or more milestones would hold its first milestone on a criterion only its last
job can meet, and never reach the last. Also read at `09d7641f`: no `remedy do` job stores a DoD or
runs a gate; `pingpong_job.run_job` removes a completed job's worktree in its `finally` block, so a
gate run after `run_job` returns has no tree; `do`'s jobs record no milestone.
CHOSEN: (1) AMENDING D4 (3). A whole-mission criterion's check enters a job's DoD with `blocking`
false — a reported check the gate evaluates and never holds on — and a milestone-scoped criterion's
check keeps the criterion's `blocking`. D4 (4) is unchanged: the criterion's status follows the
evidence either way, so the mission gate of D4 (5) still holds the achieve move until the latest
evaluation reads it met. (2) THE GATE IN `run_job`. When every task has passed and the job has a
stored DoD, `run_job` runs `dod_gate.run_job_gate` in the job's workspace before the workspace is
finalized; a gate that does not release blocks the job with the gate's `dod_blocking_red:<ids>`
reason (F061's rule that a job ends green only when all blocking checks pass), and then, for a job
that belongs to a mission, `record_contract_results` reads the result onto the job's slice. (3)
`do`. The shape step merges each job's slice into its DoD as it links the job to the mission;
`do`'s jobs serve no milestone, so their slice is the whole-mission criteria. (4) `do`'s result
names the contract's state after the walk: `--json` carries `unmet_blocking_criteria`, the
blockers of D4 (5) in contract order, and the text output carries one line counting the met
criteria against all of them and naming each blocking criterion not met with its status, `open`
or `unmet`.
ALTERNATIVES: blocking whole-mission checks only in the mission's last job, rejected because a plan
may end in more than one milestone and "last" is then not one job; a mission-level evaluation,
rejected in D4 already; recording on each `do` job the milestone its outline came from, rejected
for now because the planner criteria it would put in `do`'s jobs are judged by the test suite and
would block every `do` job in a repository with no tests — they stay the orchestrator's to evaluate.
REVERSE: restore the criterion's own `blocking` in the merge, delete the gate call in `run_job`,
the merge call in `do`'s shape step and the result lines, and delete this paragraph.
