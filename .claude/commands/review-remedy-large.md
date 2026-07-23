Read docs/agents/planner_reviewer_prompt.md and act accordingly.
A worker handback is awaiting review — do NOT plan new work first.
Bootstrap from disk: .agent/handoff.md (review range = its "review of
<sha..sha>" line), .agent/plan.md, .agent/live_review.md, then run the
full review loop: real diff bottom-up, independently re-run the step's
verification yourself, apply the block conditions, issue the verdict.
If information you need exists only in the worker's chat report, author
a paste block requesting it — never guess.
LARGE-mode override on the NEXT block only — every review rule is
unchanged:
- After a PASS: the next paste block targets the WHOLE remaining
  feature (largest safe bundle, per-slice verification, stop-on-red),
  not just the next step.
- After a FAIL: the repair block may ADDITIONALLY carry the next
  outstanding feature work, in this strict order: persist the authored
  findings (own commit) -> fix finding by finding -> re-run the failed
  verification — if it is not green now, STOP the block here, hand
  back -> only then continue with the next T-slices.
- NEVER include closure in these bundles; closure is its own round.
- On momentum warning, author normal-sized rounds instead and say so in
  the brief.
