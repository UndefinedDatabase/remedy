# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q1 — Post-task lessons start switched off (2026-09-24, F265, round 1)

**What needs deciding.** Remedy can now write a short lesson after each finished task of a
job. The lesson explains the change that task really made to the code: what was built, which
functions and language features it uses, what they do, why they fit there, and whether that is
good practice, stated as the teacher's opinion. Writing one lesson costs one call to the
teacher's model for every finished task. I have made lessons switched off unless you turn them
on, with the setting named `teacher.lessons` in your project's settings file or the environment
variable named `REMEDY_TEACHER_LESSONS`. You can tell me they should be on unless switched off.

**Why it matters.** With lessons on, every finished task makes one extra model call, and a large
job has many tasks. I also set a spending limit for these calls in each job: at most thirty
calls, and at most three hundred thousand tokens, which are the units a model counts its reading
and writing in. When a job reaches either limit, the tasks after it get an empty lesson that says
the limit was reached, never a shortened one.

**My recommendation.** Keep lessons off until you switch them on. A run should never spend money
on something the person running it did not ask for, and the optional written summary of a failed
run already follows that same rule. Switching lessons on is a single setting.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise. Lessons stay off until you switch them on, and the spending limit for each job
applies from the first lesson.
