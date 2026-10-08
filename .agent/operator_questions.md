# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q10 — Stray test records in data (2026-10-08, F253, round 5)

**What needs deciding.** While the loop was writing a test on 8 October 2026, one early draft of
that test ran Remedy against your real data folder instead of a temporary one. It left one small
project, one mission and one job behind, all created at 13:51 UTC and all about the practice order
"Add a line saying hello to README.md". The project's id begins with 6762bb1d, the mission's with
2ecf8a23, and the job's id is 7aceeefff16a489b. They point at a temporary folder that the test
system has already removed, and they changed nothing in any of your repositories. The draft was
corrected before it was saved, and the saved tests only ever use temporary data.

**Why it matters.** The three records show up in Remedy's overview of your work as one more
project with one stopped job and two open questions. They do no harm, but they are clutter that
you did not create. The loop does not delete anything in your data folder on its own, because a
deletion there cannot be undone.

**My recommendation.** Leave them, or delete them yourself when convenient. In the data folder of
this checkout, each sits in a folder or file named after its id above: the job in the jobs folder
and in the job logs folder, the mission in the missions folder, and the project in the projects
folder.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise: the records stay where they are, nothing reads them as real work, and the loop
does not touch them.
