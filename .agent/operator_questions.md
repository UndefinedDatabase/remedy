# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q19 — Order caps stay the client's (2026-10-20, F310, round 1)

**What needs deciding.** When an order arrives with its own time or token limit, Remedy now keeps
that limit for the whole order, and fills only the limits the order leaves out from the new
default for local models, which is eight hours, two hundred calls and one and a half million
tokens per job. Your lab order of the twentieth of October carried a limit of twelve minutes for
the whole order, written by the Orb, so even with the new defaults that order would still have
stopped after twelve minutes.

**Why it matters.** The new defaults only help in the lab once the Orb stops writing twelve
minutes into every order. Remedy now tells every client the two sets of defaults, so the Orb can
show them and send the right numbers, but the Orb has to do that itself.

**My recommendation.** Keep the order's own limit as the ceiling. A limit a person or a client
chose should never be raised by a default, and the Orb can read the local defaults from Remedy and
send them.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise.
