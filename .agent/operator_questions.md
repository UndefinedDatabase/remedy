# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q4 — Background service built smaller (2026-10-01, F200, round 1)

**What needs deciding.** The next item on the roadmap is a background service for Remedy. You
start it once, it keeps running, and the remedy command hands its work to it instead of doing the
work itself. The plan for this item was written months ago, and three things it relied on are
gone or were never built. The waiting line of jobs it was meant to work through was removed on
purpose, together with the command that worked through it, and nothing replaced them. Running
several jobs at once from such a line was never built. And the two helpers it was meant to host,
one for notifications and one for exporting the audit trail, do not exist. So I rewrote the item
to what can be built today. The service listens on a private connection that only your user
account on this machine can open. It accepts exactly the commands the cockpit page already
accepts, and it checks them in exactly the same way. While the service runs, those commands from
the command line go through it and print the same output as before. It also runs the jobs you
hand it, and if it is killed, it starts those jobs again when it comes back. It ships with a file
for the system's service manager and a start script for containers. I left out the waiting line,
running several jobs at once from one list, the two helpers, and serving the cockpit page from
the service.

**Why it matters.** Building the old plan as written would bring back the waiting line you
removed. Leaving the item untouched would also hold up the remote access item, which needs this
service. One part of the old promise is not kept in full. Commands that the cockpit page does not
accept, such as applying a finished change to your project, still run directly even while the
service runs, so the service is not the only program that writes a job's records. I chose this
so that the command line keeps working completely. Letting every command go through one door is
a separate roadmap item that builds a complete programming interface.

**My recommendation.** Build the smaller service as described, and leave the waiting line
removed.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise. If you want the waiting line back, say so, and I will register it as its own
roadmap item.
