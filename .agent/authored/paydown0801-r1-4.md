<<<FROM docs/agents/planner_reviewer_prompt.md (exact block, occurs once)
3. .agent/handoff.md (latest worker state), .agent/plan.md,
   .agent/live_review.md → locate the exact round and what is awaited.
4. Only on demand: AGENTS.md sections, docs/agents/* conventions,
FROM>>>
<<<TO
3. .agent/handoff.md (latest worker state), .agent/plan.md,
   .agent/live_review.md → locate the exact round and what is awaited.
4. .agent/candidates.md (operator ruling 2026-08-01, F056-candidate
   loss): if non-empty, the FIRST reviewed round registers each
   entry (next free ID) or resolves it inline as a §4.7 DECISION,
   and empties the file in that same round. A non-empty candidates
   file at feature-claim time is itself a block condition
   (STATUS_closure_protocol.md, "Closure-candidate findings").
5. Only on demand: AGENTS.md sections, docs/agents/* conventions,
TO>>>
