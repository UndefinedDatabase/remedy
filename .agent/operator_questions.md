# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q24 — Pull request 381 is not merged: the second hosted run is red on two tests (2026-10-23, fix1022-review-findings)

**What needs deciding.** Your order fix1022-review-findings asked me to repair four findings and merge
the pull request when hosted CI is green. The four repairs are done and every local gate is green.
The first hosted run was red on 166 tests in both Python versions, all because the hosted machine
had no sandbox program, which Remedy has required since 16 October; nobody had started a hosted
run since then, so nobody saw it. I added the sandbox to the workflow (R-1426) and started the
second run, the last one your order allows. That run is almost green: 166 failures fell to two.
One test about splitting a cost cap across a chain of jobs fails on both Python versions with a
missing budget (R-1427), and one sandbox test that searches the whole disk ran out of its 60
seconds on Python 3.12 only (R-1428). Both pass on your machine. Your order says a second red run
is never merged, so pull request 381 stays open and unmerged. Please decide: merge it as it is,
with the two tests left to the next findings paydown (F314), or have a session repair the two
first and start one more hosted run.

**Why it matters.** Pull request 381 carries the four repairs and the sandbox step that makes the
hosted run usable again; until it merges, `main` has neither, and the next session's open pull
request check stops on it.

**My recommendation.** Merge it as it is. Neither red test is in code this branch changed, both pass
on your machine, the branch takes the hosted run from 166 failures to two, and both are registered
for the next findings paydown, F314.

**What happens if you say nothing.** The pull request stays open with a red hosted run, so the next
session reads that red run as its work first, repairs the two tests on this branch and starts one
more hosted run before it begins anything new.
