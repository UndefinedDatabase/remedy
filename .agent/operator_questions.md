# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q21 — What the insight cannot see (2026-10-21, F311, round 1)

**What needs deciding.** Remedy is getting two new answers for the Orb: one that lists what runs
right now, and one that looks into a single job's worker and says why it hangs. Remedy can only
report what it can measure, so I made four choices. The worker's latest lines and the time of its
last output are recorded only for the local worker that runs your lab model, not yet for the paid
command-line worker, so a job on that worker says plainly that its silence is not measured. Remedy
has no fixed number of worker slots, so the number of free workers reads empty. The local model
server never tells anyone how many requests wait, so that number reads empty too. And the two
commands are named after the other client reads, as "remedy client now" and "remedy client
insight", rather than "remedy now" and "remedy job insight".

**Why it matters.** The Orb will show an empty value or the word for "not measured" in these
places, instead of a number. If the paid worker matters to you in the lab, it needs a later step.

**My recommendation.** Keep all four choices. An honest empty value is better than a guess, and
the local worker is the one your lab runs use.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise.

### Q22 — Mission runs start one job (2026-10-14, F078, round 2)

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

### Q23 — What Remedy may do, by level (2026-10-21, F141, round 1)

**What needs deciding.** Remedy is getting a table that says, for each autonomy level, what work it
starts may then do: read your project, write a job's result into your files, commit, push, change a
dependency, delete files or run a migration, spend above your cost threshold, and reach the network.
Each place in the table says one of three things: Remedy may do it, it must ask you first for this
one case, or it may not do it at all. I chose the table myself. At the default level Remedy may only
read and reach the network for the builds it already does; writing into your files, committing,
pushing, changing a dependency, deleting and spending above the threshold all need your approval of
that one case, and the flags you already type, such as the approve, commit, push and yes flags, count
as that approval. At the highest level Remedy may commit, change dependencies and spend on its own,
but pushing and deleting still always ask you. I also departed from the plan in two places. The plan
said deleting should be forbidden outright at the default level; I made it ask instead, so that your
own command to merge a job's branch keeps working. The plan assumed Remedy never pushes; it does, on
your push flag, so pushing asks at every level, and a new setting, which is on by default, lets you
switch pushing off completely.

**Why it matters.** Every later step of this feature enforces this table. From then on, applying a job
whose change touches a dependency file or deletes a file will stop and ask you, even at the default
level, until you approve that case.

**My recommendation.** Keep the table as it is. It changes nothing you do today with your usual
flags, and it adds a question only where a change reaches your dependencies or deletes something.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise.
