# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q1 — How the big rename lands (2026-09-13, F275, round 87)

What needs deciding. The last large step of the current feature renames how every job record is read and written, across about two hundred and sixty files and roughly five thousand added lines. The project allows one commit of more than five hundred added lines per feature, and this feature already used that allowance earlier, on a tooling file. I have decided that the rename will land as a series of smaller commits inside one working round, where the commits in the middle of the series do not pass the test suite on their own and only the last one does. You can overrule that by allowing one more oversized commit for this feature, so the rename lands as a single commit.

Why it matters. A single commit keeps every commit on the branch in a working state, which helps anyone who later searches the history one commit at a time for the moment something broke. The series keeps the size rule intact but leaves around ten commits on the branch that do not work on their own. The main branch receives the finished work as one merge either way.

My recommendation. Keep the series of smaller commits. The size rule exists so that each change stays reviewable, and a mechanical rename split into groups of files is easier to check than one very large commit.

What happens if you say nothing. The rename lands as the series of smaller commits once it is ready. That is several working rounds away: about eight hundred tests still fail against the renamed code, and those failures are removed first.
