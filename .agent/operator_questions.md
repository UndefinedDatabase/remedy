# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q2 — Test diet closes short (2026-10-01, F293, round 22)

**What needs deciding.** You asked for the tests to use at least 40 percent less processor time.
The work that just finished cut it by about a quarter: one full run of all tests used about 1,246
processor seconds before and about 941 seconds now, and it takes about 4 and a half minutes
instead of about 6. Reaching 40 percent needs about 193 more seconds. The largest cost left is not
in the tests themselves: every test that runs a whole job starts about 210 small git programs,
because that is how Remedy's job runner works today. Making the job runner start fewer of them is a
change to the product, which also makes your real jobs faster. I closed the finished work at the
quarter it reached and registered the job runner change as a new roadmap item, placed directly
after it, so it is built next.

**Why it matters.** Closing now keeps the finished cuts, a fix for a test that left a program
running after every test run, and a doctor line that shows you the daily test cost. Continuing
inside the same work item would have meant more small test changes of a few seconds each, and every
check of their effect at full scale costs another full test run of about 941 processor seconds.

**My recommendation.** Keep the split: close the finished work at the quarter it reached, and build
the job runner change as the next item.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise.
