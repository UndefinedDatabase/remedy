# Mission upkeep v1: every fifth job cleans up

> Status (F301, 2026-10-10): being built. DECISIONs F301 D1 to D3 in `.agent/decisions.md` hold the
> rules this page states; the feature is `docs/roadmap/features/T7_F301.md`. Built so far: the
> upkeep ledger, the cadence, the planned step and `remedy mission continue`. The orchestrator's
> own dispatch and the views of `remedy mission show` and the client digest come next.

A mission that runs for many jobs leaves things behind: problems a reviewer still saw when a job
ended, code that grew past the size limits, and files that a newer file replaced and nobody
deleted. Mission upkeep collects them in a ledger per project, and after every fifth completed job
of a mission the next job is an upkeep job that Remedy plans from that ledger by fixed rules. The
code is `packages/orchestration/mission_upkeep.py`.

## The ledger
Each project has one append-only file, `upkeep_ledger.jsonl`, in its folder under the data root's
`projects/`. A line is written and never changed. When a job of a mission has ended — completed,
failed or cancelled — its `job_closed` line records the findings it left open and the files it
replaced and did not delete. The ledger also records each upkeep job Remedy planned, each upkeep
job the operator skipped with its reason, and each time upkeep was due and nothing was left.

A job's open findings are the findings of its final job review, and the findings the reviewer
still named in the last round of each task that stayed blocked. Finding ids are chosen anew in
every run, so a finding is known by its job, its task and its id together. It stays open until an
upkeep job that carried it ends completed.

## The cadence
The setting `mission.upkeep_every`, five unless set, is a whole number of at least 1; any other
value is refused. Remedy counts the mission's completed jobs since the last upkeep job, skip or
not-needed line, and upkeep is due when the count reaches the setting. The count is in jobs, never
in time.

## What an upkeep job carries
The rules, in the order the job's step lists them:
1. The oldest findings the mission's jobs left open, at most five; the others wait for the next
   upkeep job.
2. The longest Python function above 100 lines and the longest code file above 1,000 lines in the
   project's repository, measured as `remedy integrity structure` measures, each to be shortened
   without a change of behaviour. A code file is one whose name ends in `.py`, `.js`, `.jsx`, `.ts`
   or `.tsx`, so a lockfile or a data file is never picked.
3. Every file that sits beside the file it replaces, found in the repository or recorded by a job,
   while both still exist, with the replaced one to be deleted.

When none of these holds anything, no job is made and the ledger says so.

An upkeep job is an ordinary job of the mission: it begins with the task that checks the previous
job, runs under the ordinary budgets, and waits at the ordinary approval. It is known by the key
`mission_upkeep` in its job's metadata, which holds what it was planned to carry.

## The command line
`remedy mission continue <mission> "<step>"` records the jobs that have ended first. When upkeep is
due, it makes the upkeep job in place of the step, says so, and the step can be given again once
that job has run. `--skip-upkeep "<reason>"` skips the upkeep job that is due and records the
reason; a skip without a reason, or with nothing due, exits 2 and changes nothing. There is no
other way to skip one. Under `--json` the answer's `upkeep` key holds the ledger line this call
wrote, or `null`.
