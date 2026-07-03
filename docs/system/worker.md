# Worker Guide

## What The Worker Does

The local worker picks jobs from a queue and processes them one at a time. It does not run in the background permanently — you start it, it processes jobs, and it stops.

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

## Running The Worker

### One job

```sh
remedy worker run --once
```

### One job with a specific provider

```sh
remedy worker run --once --provider fixture
```

### Bounded loop

```sh
remedy worker run --max-jobs 3 --max-seconds 120
```

The worker stops when it reaches the job limit, time limit, or has nothing to do.

### Check worker status

```sh
remedy worker status
remedy worker status --json
```

## Queue Commands

```sh
# Add a job to the queue
remedy job enqueue <job_id>

# Pause a job (worker will skip it)
remedy job pause <job_id>

# Cancel a job
remedy job cancel <job_id>
```

## Approval

When the worker reaches a point that needs human approval (like applying a patch), it stops and tells you what to do next:

```
Why stopped: approval_required
Next: remedy patch approve <job_id> <intent_id>
```

The worker does not apply patches without approval. It does not spin waiting.

## CPU Safety

- The worker processes one job at a time.
- It does not run multiple test suites in parallel.
- It respects test timeouts.
- It does not run pytest in the background.
- Two workers cannot process the same job (lease-based locking).

## Stale Worker Recovery

If a worker crashes or disappears:

- The job lease expires after 5 minutes.
- The job becomes "stale."
- Another worker can reclaim it.
- If the job was mid-apply, it requires proof/checkpoint check before resume.

## Dashboard

The dashboard shows worker status in the right panel:

- Whether a worker is active
- Current job
- Queue count
- Why it stopped
- Copyable next command

The dashboard is read-only — no start/pause/cancel buttons.

## What This Is Not

- Not overnight autonomy
- Not a cloud service
- Not a browser-controlled worker
- Not multi-machine
- Not unlimited — always has job and time limits
