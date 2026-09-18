
## DECISION F268 D8 (2026-09-18, reviewer, round 3) — where `--step-by-step` halts, and what `--plan-only` stops after
CONTEXT: T2_F268.md's Design reuses the safe points where budget and stop are checked
(`packages/orchestration/safe_points.py`); measured at `57ca6293`, `pingpong_job.run_job` checks them
through an internal stop check before the run, before each task, between provider calls and after the
loop, and exposes no hook for a caller to pause there.
CHOSEN: `--step-by-step` halts at the walker's step boundaries — after every step that did work and
before the next — and, inside the run step, before each job; at those points no provider call is in
flight by construction, because a step returns only after its own calls have returned. At each halt
`do` prints what just happened and what comes next and reads one line: an empty line continues, `q`
(or end of input) stops the walk with the halted step's successor unrun and, when a job exists,
records the stop through `safe_points.request_stop` for every job of the walk, so the F011 path
carries it. The line is read through a function the walk's context carries, so a test can supply
it. `--plan-only` ends the walk after the shape step: the run step reports stopped with the reason
`--plan-only`, no job is run, and the output lists the mission plan's path, the contract (null,
DECISION D1) and every job's tasks with their deliverables. Both flags join the bare-route
allow-list. ALTERNATIVES: a pause hook inside `run_job`'s own stop check, rejected because it
changes the runner shared by every job path for a behaviour only `do` asks for. REVERSE: delete the
two flags, the halt function and the `--plan-only` branch; delete this paragraph.
