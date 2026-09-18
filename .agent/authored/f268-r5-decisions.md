
## DECISION F268 D10 (2026-09-18, reviewer, round 5) — a follow-up job runs only on top of its predecessor's applied output
CONTEXT: R-0968. Measured at `994f045a`, every job's workspace is cut from the target's HEAD when
the job runs, and `pingpong_job.run_job` takes no base other than the target.
CHOSEN: in a walk of two or more jobs, job k+1 runs only after job k is APPLIED to the target. With
`--apply`, the run step applies each job through the apply step's own function right after it
completes and before the next job runs, stopping at the first job that is not applied; the apply
step then reports the jobs already applied and applies nothing twice. Without `--apply`, the run
step runs job 1 only and reports `stopped`, naming why the rest wait and printing, with real ids,
the apply command for job 1 and the `remedy job run` command for job 2; the walk's `--json`
carries every planned job in `job_ids` as before. A walk of one job is unchanged. DECISION F268 D5
is amended accordingly: its sentence "the run step runs them in order and stops at the first that
does not complete" now reads through this decision. ALTERNATIVES: cut job k+1's workspace from job
k's result branch, rejected because it changes the runner every job path shares and leaves the
target and the branches disagreeing about what was delivered; run every job and apply them all
afterwards, rejected by R-0968. REVERSE: restore the run step's loop over every job; delete this
paragraph.

## DECISION F268 D11 (2026-09-18, reviewer, round 5) — `do`'s cost summary reads the ledger, and the builder's context size is evidence
CONTEXT: R-0807's F268 half. Measured at `994f045a`, `remedy job run` mirrors a finished job into the
F103 token ledger through `job_evidence.mirror_job_run_into_ledger` and `do`'s run step does not;
`token_ledger.query_cost(..., job_id=..., by="role")` aggregates the ledger by role; the
`context_strategy.json` that `job_evidence` writes names the strategy and carries no size.
CHOSEN: after each job completes, the run step mirrors it into the ledger exactly as `job run`
does; at the end of the walk `do` prints one line per role with the measured input, output and
cache-read tokens and one line with the measured cost, read through `query_cost` for the walk's
jobs, and `--json` carries the same numbers under `cost`; a job whose mirror failed is named, never
counted as zero. `context_strategy.json` gains the context size sent to the builder per round — the
builder call's reported input and cache-read tokens for each task and round, read from the run's
own evidence — written by `job_evidence`'s existing writer. ALTERNATIVES: sum tokens from the run
logs inside `do`, rejected because the ledger is the one cost truth and a second sum is a second
answer. REVERSE: delete the summary, the mirror call and the new field; delete this paragraph.
