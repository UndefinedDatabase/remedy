Target: .agent/live_review.md
Operation: replace FROM with TO. FROM occurs exactly 1x (verify first).
Shape: APPEND — the TO contains the FROM verbatim. Proof obligation is
FROM 1x plus the TO-only line 1x. Do NOT claim FROM 0x.
Apply this ONLY after the planner_reviewer_prompt.md edit is in place.

FROM
<<<FROM
  Fix: write the two proof shapes into
  docs/agents/planner_reviewer_prompt.md §4 item 9, so the rule
  lives on disk instead of in reviewer session memory (the A1 trap
  §0 names).
FROM>>>

TO
<<<TO
  Fix: write the two proof shapes into
  docs/agents/planner_reviewer_prompt.md §4 item 9, so the rule
  lives on disk instead of in reviewer session memory (the A1 trap
  §0 names).
  Done: R-0207 — applied in R2; §4 item 9 now names the rewrite and
  the append shape and the proof each one owes.
TO>>>
