# Live Review — F268 remedy do: the one-command start

> Round-by-round review record, re-headed at the F268 claim per
> docs/agents/planner_reviewer_prompt.md §1. The heading this replaces named F266, whose STATUS
> line went `[x]` and whose pull request 255 merged into `main` at the reviewer's Open PR Gate
> under docs/agents/self_drive_protocol.md, as `8e075bbe`, after its round 12 repaired the
> hosted-CI red recorded as R-0962. F266's round 12 has no gate entry here by construction (§4
> item 13 of docs/agents/planner_reviewer_prompt.md): the reviewer re-ran its gates at `750af12a`
> and read PASS, hosted CI run 35314590748 on that commit read success, and that verdict lives in
> the merged PR and in `.agent/handoff.md`'s git history. Only the heading, this paragraph and the
> `## Steps` section below are rewritten. Everything from the `## Findings` line to the end of the
> file is carried forward BYTE-IDENTICAL, and finding ids continue the monotonic R-XXXX series
> across the re-head.
> Measured by the reviewer at `8e075bbe`: 132 DISTINCT ids matching `^- R-\d+ — ` against 4
> DISTINCT ids matching `^Done: R-\d+ — `, so 128 findings are open BY DISTINCT ID.

## Steps

THE ORDER BELOW IS T2_F268.md's Orchestrator brief: T001 first and alone, because it is the
acceptance skeleton — the sequence as data, walked end to end on the fake provider, init → study
→ plan → shape → run → stop before apply, one test per step boundary. T002 (the shape decision
and the force flags) and T003 (step-by-step and plan-only) follow in either order; T004 (cockpit
auto-open and the apply pass-through) reads F270's state on the day; T005 (the quick start) is
written last, against the shipped catalog.
R1 claims F268, re-heads this record, lands DECISIONs F268 D1 to D4, and builds T001.

