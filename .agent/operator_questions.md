# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q13 — Toolchain job spending limit raised (2026-10-11, F297, round 8)

**What needs deciding.** Every fourteen days the loop may run a job that checks whether the
pinned versions of its development tools can move forward, and that ends with a pull request for
a person to review. The last time it ran, it used up its spending limit after three of its five
steps and stopped before the two steps that matter most: running the whole test suite on the new
versions and opening the pull request. The loop measured what that run spent on each call to the
model and raised the job's spending limit to a little under three times its old value, which is
enough for all five steps even when every step needs both of its retries.

**Why it matters.** Under the old limit the job spends its whole allowance every fourteen days
and never reaches the pull request, so that spending buys nothing a person can use. Under the new
limit each run may cost up to almost three times as much as before.

**My recommendation.** Keep the higher limit. A run that stops before its pull request produces
nothing, so a limit that cannot reach the end wastes more than a limit that can.

**What happens if you say nothing.** The recommendation is already carried out and stands until
you say otherwise.
