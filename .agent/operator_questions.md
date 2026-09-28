# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q6 — Empty paydown waits one feature (2026-09-28, F036, round 1)

**What needs deciding.** The next item on the roadmap was a clean-up feature whose only job is to
repair known defects that earlier reviews wrote down. Right now no such defect is open, so that
feature would have nothing to repair. I have moved it one place down the list, behind the next
real feature, the guided result tour, which walks you through a finished job in a few short steps.
The session is building the tour now. When the tour is finished, the clean-up feature comes up
again, and it starts as soon as there is at least one open defect to repair.

**Why it matters.** Starting and finishing a feature costs a full test run, an evidence package
and several review rounds. Spending that on a feature with nothing to do would use up about one
session and change nothing in the product.

**My recommendation.** Keep the clean-up feature waiting while there is nothing for it to repair,
and build the next real feature instead. One clean-up feature still always waits on the list, as
your rule asks.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise. The tour is built first, and the clean-up feature is offered again when the tour is
finished.
