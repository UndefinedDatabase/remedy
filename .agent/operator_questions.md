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
