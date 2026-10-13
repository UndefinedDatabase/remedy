# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q18 — Cockpit logs view moves later (2026-10-13, F203, round 5)

**What needs deciding.** The plan for Remedy's new operations log, the private file where Remedy
now writes what it does with the job, the task and the run named on every line, included a
button in the cockpit, the browser view of a job, that would show those lines. That button is
not being built now. A person can already read one job's lines with a command, and a program
can read them over Remedy's local web interface. The button is moved to the later piece of work
that rebuilds the cockpit on that same web interface.

**Why it matters.** Building the button now would mean changing the largest and oldest part of
the cockpit's server first, and adding a private connection that the later piece of work exists
to remove again. Moving it means the cockpit shows no log lines until that later work is done.

**My recommendation.** Keep the button with the later cockpit work, as already decided. Nothing
is lost, because the command and the web interface show the same lines today.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise: the button is written down as part of the later cockpit work, and this piece of
work closes without it.
