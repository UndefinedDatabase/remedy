# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q12 — A resent order runs twice (2026-10-09, F253, round 22)

**What needs deciding.** When a program sends Remedy the same order twice through the web
interface, Remedy starts it twice. On the command line, Remedy refuses to start an order file
again while the first run of that same file is still going, but over the web interface a program
sends the text of an order, not a file, so there is nothing for that check to recognise. A program
that sends an order again because it never received the first answer, which is what a program
does after a dropped connection, therefore starts the same work a second time.

**Why it matters.** The second run is not harmful: it gets its own spending limits and its own
record, and nothing written by the first one is damaged. It does cost the work twice, in time and
in model usage, and a program cannot tell from the answer that it has just repeated itself.

**My recommendation.** Leave it as it is for this feature, and solve it properly later: a program
gives each order a name of its own choosing, and Remedy refuses a second order with the same name
while the first one is still going, answering with the first one's record instead. I recorded it
as a known problem for the next clean-up feature, and the web interface's page will say plainly
that a resent order runs again.

**What happens if you say nothing.** The recommendation is already in effect and stands until you
say otherwise: a resent order runs again, and the fix waits for the next clean-up feature.

### Q13 — The installed command runs old code (2026-10-09, F253, round 23)

**What needs deciding.** The `remedy` command installed for your user on this computer does not
run the code in your main Remedy folder. Python's list of installed packages points it at a
working copy that one of Remedy's own jobs made on October 7, the job that raised the version pins
and regenerated the constraints file, and that copy has not changed since. Anything you start with
the plain `remedy` command, the supervisor included, therefore runs that older code, not today's.

**Why it matters.** Features built since October 7, among them the web interface for programs that
this work is building, are missing from the command you type, so trying them by hand would show
old behaviour and could look like a fault. The loop's own tests are not affected, because they
always run the code of the main folder. It is also worth knowing how the pointer moved: either a
job's work installed Remedy from inside its own copy, which a job should never be able to do to
your user's settings, or it was done by hand.

**My recommendation.** Open a terminal in your main Remedy folder and install it again for your
user in editable form, the same way it was installed before, for example with
`python3 -m pip install --user -e .`, so the command follows the main folder again. If you did not
make that change yourself, tell the loop, and a later feature will look into whether a job can
change your installed packages and stop it.

**What happens if you say nothing.** Nothing changes: the installed command keeps running the old
copy until you reinstall it, and the loop keeps working from the main folder as it does now.
