
### Q3 — no planner provider flag (2026-09-18, F268, round 8)

What needs deciding: the one-command start was designed with a flag to choose which service does the planning, beside the flags that choose the builder and the reviewer. Today the planner can only use the local model server, so that flag would accept exactly one value. The session decided not to create it, and to create only the flag that picks which planning model to use.

Why it matters: a flag that accepts one value tells a user there is a choice when there is none, and it would have to be changed again the day a second planning service exists. Leaving it out keeps the help text honest, but it means the command's flag list differs from the design by one flag.

My recommendation: leave the flag out until a second planning service exists, and add it in the same change that adds that service.

What happens if you say nothing: the recommendation is already executed and stands until you say otherwise.
