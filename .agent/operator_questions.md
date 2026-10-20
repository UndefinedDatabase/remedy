# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q20 — Closing beside foreign open findings (2026-10-20, F310, round 5)

**What needs deciding.** Remedy's own health check before a feature closes refuses while any serious
finding is open. Today it refuses because of thirteen serious findings that this feature never
touched: twelve that earlier work already repaired but never marked as repaired, and one that the
next feature in line is meant to repair. I closed this feature anyway, and marked it as closed with
a risk, rather than make it wait.

**Why it matters.** Until the twelve repaired findings are marked with their proof, every feature
that closes will meet the same refusal, and each would have to make the same choice I made.

**My recommendation.** Keep the close, and let the next round of finding repairs, which is already
on the list, mark the twelve with their proof. That work is registered so it is not forgotten.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise.
