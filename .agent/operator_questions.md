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

### Q25 — One hosted test run, please (2026-10-24, F314, round 6)

**What needs deciding.** Two of the open problems of this clean-up concern the copy of Remedy's
tests that runs on GitHub's machines rather than on yours. I repaired what I could reproduce here:
one test failed there only because GitHub's machine has no name and e-mail address for git, and
another took too long because it searched a large Python installation that only GitHub's machines
carry. To prove both repairs, and to close the problem that the whole GitHub test run was red, the
test run on GitHub has to be started once on this branch. Your permission settings do not let this
session start it, so it has not run.

**Why it matters.** Until one such run is green, the two problems stay open and move to the next
clean-up. Nothing else waits on it.

**My recommendation.** Start the GitHub test run once for this branch, from the Actions page of the
repository or with the GitHub command line, or allow sessions to start it. The next clean-up then
reads the result and closes both problems when it is green.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise: the two problems are carried to the next clean-up, which asks again.

### Q26 — Let sessions run the claude command (2026-10-24, F152, round 2)

**What needs deciding.** The current work makes sure that a worker run by Remedy never picks up your own personal settings for the Claude command line, such as your instructions file, your extra tool servers or your plugins. To prove this properly, Remedy has to run the real command line twice: once with a planted marker in a fake personal settings folder, and once isolated, and show that the marker only appears the first time. The permission settings of these sessions refuse every run of the command line, even just asking it for its version or its help text, and they also refuse reading the public documentation on the web. So the research is written from a saved copy of the help text, and some points stay marked as unverified.

**Why it matters.** Without one real run, Remedy can prove that it hides your settings from the worker, but not that the command line itself honours the switches it is given. One real run costs one very small paid call.

**My recommendation.** Allow sessions to run the claude command for version and help, allow one small paid call for the proof, and allow reading the public Claude documentation. Until then, the proof runs against a stand-in program and the real run sits behind a switch that is off by default.

**What happens if you say nothing.** The recommendation is already executed and stands until you say otherwise: everything is built and tested with the stand-in, the real run stays switched off, and the work closes with that one point named as an open risk for a later clean-up.
