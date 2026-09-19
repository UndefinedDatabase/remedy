
## DECISION F273 D18 (2026-09-19, reviewer, round 18) — a check writes no bytecode, each `do` job serves its milestone without being held on it, and the memory-candidate store goes
CONTEXT: DECISION F273 D16 (6) held R-0977 because its FIX as written blocks every `do` job in a
repository with no tests, which DECISION F269 D6 measured, and because the non-blocking variant exposed
R-0993. D17 (3) took R-0992 into the same round. A research helper prototyped all three on the tree of
`f445a2c0`, and the reviewer re-ran them in its own dry run.
CHOSEN: (1) R-0993. `dod_process_exec_policy` gives every process check `PYTHONDONTWRITEBYTECODE=1`
beside the scrubbed environment, and the pytest check runs with `-p no:cacheprovider`, so a check
writes nothing into the worktree it judges; handoff coverage is unchanged, because a task may not write
under `__pycache__` in the first place. (2) R-0977. `do`'s shape step records on each job the milestone
whose `jobs_draft` it came from, or the plan's milestone when the plan has exactly one, and merges that
milestone's slice with `hold_on_milestone=False`: the job's gate evaluates the planner's criterion and
reads it `met` or `unmet` onto the contract, and never holds the job on it. This amends DECISION F269 D6
(1) and (3) for `do` only; `mission run` keeps holding its jobs on their milestone. A job made with
`--force-job` from a plan of several milestones serves none, so their criteria stay `open`. As a
consequence of DECISION F270 D4 (6), which lets only an unmet blocking criterion hold a push back, a
`do --push` in a repository with no passing suite is now refused after its commits land; operator
question Q4 carries this as its third ruling. (3) R-0992. The memory-candidate store, the
`memory candidates`, `memory approve-candidate` and `memory reject-candidate` words, the cockpit's
candidate count and checklist items, the `dev status` key and the smoke section are deleted with
their tests. `approve_candidate` imported a module this repository does not hold, swallowed the error
and still reported `memory_created` true, so it goes rather than being given a writer.
ALTERNATIVES: R-0977's FIX as written, rejected for D6's reason; hiding bytecode paths from handoff
coverage, rejected because it treats a symptom and would also hide a real write; giving the memory
candidates a writer, rejected because no surviving path proposes one.
REVERSE: restore the touched files from `f445a2c0`, restore Q4 of `.agent/operator_questions.md`, and
delete this paragraph.
