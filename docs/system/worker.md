# Worker Guide (queue and run commands deleted 2026-09-16)

> **Status (2026-09-16):** F261 round 23 deleted the queue words of the `job` group — `enqueue`,
> `pause`, `cancel` and `resume-queue` — and the `run` word of the `worker` group (DECISION
> amend0905-vocab D4 keeps `worker` as `list`, `show`, `resources`, `unload`, `status` and
> `doctor`). Nothing adds a job to the local queue or processes one from it any more. A job is run
> with `remedy job run <job_id>` and stopped at its next safe point with `remedy job stop <job_id>`;
> neither reads the queue below. `remedy worker status` still prints the last status a worker
> wrote, and nothing writes one now. The page is kept as the record of what was built.

## What The Worker Did

The local worker picked jobs from a queue and processed them one at a time. It did not run in the background permanently — it was started, it processed jobs, and it stopped.

## Job States

| State | Meaning |
|-------|---------|
| queued | Waiting for a worker to pick it up |
| claimed | A worker has reserved it |
| running | Work is in progress |
| waiting_for_approval | Stopped — human decision needed |
| blocked | Cannot proceed (permission, provider, etc.) |
| paused | You paused it — worker will skip it |
| cancelling | Cancel requested — worker will stop at next safe point |
| cancelled | Cancelled |
| completed | Done |
| failed | Something went wrong |
| stale | Worker disappeared — job can be reclaimed |

## Running The Worker (deleted 2026-09-16)

The worker was started with a `run` word under `worker`. It took `--once` to process one job,
`--provider` (`none`, `fixture` or `ollama`) and `--job` to name one job, or `--max-jobs` and
`--max-seconds` for a bounded loop, and it stopped when it reached the job limit, the time limit,
or had nothing to do. It skipped a queued job whose proposed tasks were unresolved or approved but
not materialized. No command starts it now.

### Check worker status

```sh
remedy worker status
remedy worker status --json
```

## Queue Commands (deleted 2026-09-16)

A job was added to the queue with an `enqueue` word under `job`, set aside with a `pause` word so
the worker skipped it, put back with a `resume-queue` word, and cancelled with a `cancel` word,
each taking the job id. Stopping a job that is running is `remedy job stop <job_id>`; the queue
itself has no heir.

## Approval

When the worker reached a point that needed human approval (like applying a patch), it stopped and told you what to do next:

```
Why stopped: approval_required
Next: remedy patch approve <job_id> <intent_id>
```

The worker did not apply patches without approval. It did not spin waiting.

## CPU Safety

- The worker processed one job at a time.
- It did not run multiple test suites in parallel.
- It respected test timeouts.
- It did not run pytest in the background.
- Two workers could not process the same job (lease-based locking).

## Stale Worker Recovery

If a worker crashed or disappeared:

- The job lease expired after 5 minutes.
- The job became "stale."
- Another worker could reclaim it.
- If the job was mid-apply, it required a proof/checkpoint check before resume.

## Dashboard

The dashboard shows worker status in the right panel:

- Whether a worker is active
- Current job
- Queue count
- Why it stopped

It reads the last status a worker wrote and the queue files already on disk, and since F261 round
23 nothing writes either, so it shows no active worker. It no longer offers a next command.

The dashboard is read-only — no start/pause/cancel buttons.

## What This Is Not

- Not overnight autonomy
- Not a cloud service
- Not a browser-controlled worker
- Not multi-machine
- Not unlimited — always has job and time limits
