# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q4 — Unchanged tasks now stop jobs (2026-10-06, F290, round 4)

**What needs deciding.** When Remedy runs a job, each task in it goes first to a model that
writes the code, the builder, and then to a second model that checks the work, the reviewer.
Until now, when the builder changed no file at all and the reviewer still said the task was fine,
Remedy recorded the task as done and went on. That happened twice when Remedy ran jobs on its own
code: a task asked for one line to be changed, nothing was changed, and the task was still
recorded as passed. From now on, a task inside a job that changed no file is never recorded as
done. The job stops at that task and gives the reason "no file changed", even when the builder
says the code was already correct.

**Why it matters.** A task recorded as done when nothing was done is a false report of finished
work, and you would only notice it by reading the code yourself. The price is that a task whose
work really was finished before the job started now stops the job, and you have to skip or remove
that task yourself. Running a single task on its own, outside a job, is not changed.

**My recommendation.** Keep the stop. A false "done" costs more than a stop you have to look at.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise. If you would rather have such tasks recorded as "already done" while the job goes
on, say so, and I will register that as its own work item.
