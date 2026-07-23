Read docs/agents/planner_reviewer_prompt.md and act accordingly, with
this LARGE-mode override on step sizing only — every other rule is
unchanged:
- Default bundle = the LARGEST coherent unit that is still safe: several
  T-slices, up to the whole remaining feature, when the ground is known
  and momentum is forward. "Inspect current shape first" steps stay small.
- Structure the bundle so every T-slice ends with its own verification
  commands; instruct the worker to STOP at the first red verification
  (AGENTS.md If-Blocked) instead of continuing into the next slice.
- NEVER include closure in a forward bundle: the STATUS [x] line, the
  evidence job, the zip and the PR are always their own reviewer-gated
  round after everything else has a PASS.
- On momentum warning (circling), drop back to normal step size until two
  consecutive rounds run forward again.
