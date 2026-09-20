# Live Review — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

> Round-by-round review record, re-headed at the F277 claim per
> docs/agents/planner_reviewer_prompt.md §1. The heading this replaces named F276, whose STATUS
> line went `[x]` and whose pull request 262 merged into `main` at the reviewer's Open PR Gate
> under docs/agents/self_drive_protocol.md, as `f2494c02`. F276's round 15 has no gate entry
> written by its own round, by construction (§4 item 13 of
> docs/agents/planner_reviewer_prompt.md); its verdict is booked at the end of this file by F277's
> first commit. Only the heading, this paragraph and the `## Steps` section below are rewritten.
> Everything from the `## Findings` line to the end of the file is carried forward
> BYTE-IDENTICAL, and finding ids continue the monotonic R-XXXX series across the re-head.
> Measured by the reviewer on the committed record at `f2494c02`: 24 DISTINCT ids matching
> `^- R-\d+ — ` against 5 DISTINCT ids matching `^Done: R-\d+ — `, so 19 findings are open BY
> DISTINCT ID. Every one of the nineteen is owned by F282 — Findings paydown v2 — under the
> OWNERSHIP AT CLOSE paragraph F276's closure wrote; F277 owns only what it registers itself.

## Steps

THE ORDER BELOW IS T2_F277.md's Orchestrator brief: T001 first and independent, then T002 before
T003 because the groups migrate onto a helper that has to exist, and T004 last because its sweep
is the acceptance evidence for the two before it. R1 claims F277, re-heads this record, books
F276 round 15's verdict, and builds T001: the declaration module
`packages/orchestration/event_names.py`, the AST test that reads the code rather than the prose,
and the opt-in strict check in `RunLogWriter.log`. Every round's handback states the open set by
distinct id.
