# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q19 — Mission runs start one job (2026-10-14, F078, round 2)

**What needs deciding.** Remedy now has an autonomy level that says what it may start on its own.
At the lowest level, which is the default, every start must be your own command. A mission run
works through a mission by starting one job after another. From now on, at the default level, one
mission run starts only the first job itself, because you asked for it. When the run wants to start
the next job, it stops instead, keeps a note that a start is waiting, and tells you to run the same
mission command again to start it. At the next level up, which needs the passed test campaign of
ten flawless runs and a short written record of why you raised the level, a mission run starts its
jobs one after another as before. The test campaign itself is not held back by the level, because
it is what proves a level can be raised and you start it yourself.

**Why it matters.** If you run missions today and expect them to finish on their own, they will
now stop after each job until you start the next one or raise the level. Nothing is lost when a run
stops this way: the waiting start is written down and the next run of the same command picks the
mission up.

**My recommendation.** Keep the default at the lowest level, as the feature describes. Raise the
level in your project settings when you want missions to run on their own; the passed campaign
from August already counts as the proof, and you only need to add the written record.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise.
