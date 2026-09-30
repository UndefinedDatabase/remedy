# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q1 — New feature for plan editing (2026-09-30, F044, round 5)

**What needs deciding.** The command palette can reach every command the cockpit's write channel
accepts except seven: the six ways to edit a plan while it waits for approval, and approving or
rejecting single parts of a change. Those seven need screens the cockpit does not have: a view of
the stored plan that shows which version of it you are editing, and approve and reject controls in
the change viewer. I registered a new roadmap item for those screens and placed it directly after
the command palette, so it is built next.

**Why it matters.** Until those screens exist, the seven stay visible in the palette but disabled,
with a sentence saying why. Building them inside the palette instead would make merging, splitting
or reordering planned tasks awkward, and it would still need a new way for the page to read the
plan from the server.

**My recommendation.** Keep the new item where it is, directly after the command palette, and let
the palette open those screens once they exist.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise.
