# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q24 — Two self-use sources go quiet (2026-10-23, F314, round 1)

**What needs deciding.** Remedy refills its own practice queue from several sources when the queue
runs empty. I switched two of them off in effect. The first is the fortnightly job that raises the
versions of the tools Remedy is built with: it must read the newest versions and their release
notes from the internet, and the model that does the work runs in a locked box with no internet at
all, so every such job could only stop half way and waste its budget. That job is no longer queued
automatically; its description stays in the repository, now saying that a person runs it from a
session that can reach the internet. The second source picks code that catches every possible
error and asks the model to narrow it. Every one of those places in Remedy already explains why it
must catch everything, so the model's reviewer had to refuse each one. That source now only picks
a place whose explanation calls itself a debt, and today no place does, so the queue moves on to
the next source, which asks for first tests of a module that has none.

**Why it matters.** The tool versions now move only when someone starts that job by hand, and the
practice runs will no longer spend money on changes that cannot be made.

**My recommendation.** Keep both changes. A job that cannot succeed teaches nothing, and the tool
versions are better raised in a session that can actually read the release notes.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise.
