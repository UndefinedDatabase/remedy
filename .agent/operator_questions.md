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

### Q3 — Second test diet stops (2026-10-01, F294, round 14)

**What needs deciding.** This is the follow-up to the question above. The second round of test
savings is finished. One full run of all tests now uses about 865 processor seconds. That is 8
percent less than after the first round of savings, about 941 seconds, and about 31 percent less
than where we started, about 1,246 seconds. Your target was 40 percent, which is about 748
seconds, so about 118 seconds are still missing. I am closing this work below the target. I did
not register another work item for the rest.

**Why it matters.** The tests that cost the most each run a complete job, the way you run one, and
then check what the job left behind. Inside a job, most of the remaining cost is two things the
job does to protect you. First, at every safe point of every task it checks whether you edited the
code yourself in the meantime, so that it never overwrites your edit. Second, before it releases a
job, it runs the project's own tests. The tests could only skip that work by no longer checking a
real job, which would make them weaker. The other way is to change the product: check for your
edits less often, or run the project's tests in a cheaper way. That would save processor time in
every real job too, but your own edits would be noticed later. I do not think that is worth about
118 processor seconds, roughly two minutes of computer time, per full test run.

**My recommendation.** Accept the 31 percent and keep the protective checks as they are.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise. If you want the cheaper job runs anyway, say so, and I will register that change as
its own work item.
