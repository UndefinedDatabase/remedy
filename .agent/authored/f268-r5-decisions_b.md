
## DECISION F268 D12 (2026-09-18, reviewer, round 5) — D10 amended: a follow-up job waits until its predecessor's output is committed
CONTEXT: D10's `--apply` half cannot hold. Measured by the round 5 worker at `994f045a` and confirmed
by the reviewer's reading of `worktrees.py` and `job_apply.py`: a job's workspace is a git worktree
cut from the target's HEAD commit, and `job_apply.apply_job` writes the target's working tree
without committing, so applying job k leaves job k+1's workspace exactly where it was, and the
second apply is refused by the baseline check (`target_created_since_job` /
`target_changed_since_job`) — the worker's dry run of D10 as written read exit 1 both ways. The
reviewer authored D10 without the dry run docs/agents/self_drive_protocol.md's own practice asks
for; the slip is recorded in `.agent/prose_slips.md`.
CHOSEN: in a walk of two or more jobs, the run step runs job 1 only and reports `done`, naming the
jobs that wait and why; the ui step opens the cockpit for job 1; the apply step, with `--apply`,
applies job 1 and reports `done`, and without it stops before apply with job 1's apply command. For
every waiting job `do` prints, with real ids, that job 1's applied output must be committed first
and then `remedy job run <id>` for the next job, and `--json` lists them as `waiting_job_ids`.
Chaining the jobs inside one `do` needs a commit per applied job, which is F270's `--commit`
family (DECISION amend0911-feedback D4), still refused as not yet available (DECISION F268 D9); it
lands with F270, not here. D10 is superseded wherever it says otherwise; a walk of one job is
unchanged. ALTERNATIVES: cut job k+1's workspace from a commit holding job k's output, rejected
because it changes the runner and the worktree layer every job path shares; have `do` commit each
applied job itself, rejected because committing is F270's and the refusal of `--commit` would then
be false. REVERSE: delete this paragraph and restore D10's run loop.
