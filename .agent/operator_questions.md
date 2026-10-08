# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q11 — Please delete three practice records (2026-10-08, F253, round 7)

**What needs deciding.** You asked that everything stay clean, and that the three practice
records an early test draft left in your data folder on 8 October 2026 be removed. The loop could
not remove them itself. The settings file of this repository forbids the loop to read your data
folder, and the loop's permissions refused even to list it, so it could not see what it would be
deleting. Remedy also has no command that removes a project, a mission or a job. The records are
one project whose id is 6762bb1d-c63e-4074-a74c-fed41a6e9154, one mission whose id is
2ecf8a2357e44968adf6b6e410c15787, and one job whose id is 7aceeefff16a489b. All three were
created at 13:51 UTC and are about the practice order "Add a line saying hello to README.md".

**Why it matters.** The records show up in Remedy's overview as one more project with one stopped
job. They do no harm, but they are the clutter you asked to be rid of. The loop has now made sure
the same mistake cannot happen again: while the tests start up, they now point every copy of the
settings at a temporary folder that is removed when the tests end, so a test can no longer reach
your data folder by accident.

**My recommendation.** Delete the records yourself, which takes a minute. In the data folder of
this checkout, which is the hidden folder named data at the top of the repository, remove every
file or folder whose name begins with one of the three ids above, in these four folders: the
project in the projects folder, the mission in the missions folder, and the job in the jobs folder
and in the job logs folder. If you would rather have the loop do it, say so and allow it to read
the data folder for that one task, and the next session will remove exactly those entries and
report each one.

**What happens if you say nothing.** The three records stay where they are, nothing reads them as
real work, and the loop does not touch your data folder. The protection against a repeat is
already in place and stands on its own.
