<<<FROM docs/roadmap/STATUS_closure_protocol.md (exact block, occurs once)
## Closure-candidate findings

Operator ruling 2026-07-30 (F050→amend0730 precedent): findings
raised DURING a closure review are recorded in the closure brief as
CANDIDATES only — no R-id is spent, nothing is registered in the
already-final live_review. The NEXT session's first reviewed round
then either registers each candidate (spending the next free ID) or
resolves it inline as a DECISION per planner_reviewer_prompt.md §4
item 7. This keeps the ledger monotonic across the session boundary
and keeps the operator-facing narrative in agreement with the disk.
FROM>>>
<<<TO
## Closure-candidate findings

Operator ruling 2026-07-30 (F050→amend0730 precedent): findings
raised DURING a closure review are recorded in the closure brief as
CANDIDATES only — no R-id is spent, nothing is registered in the
already-final live_review. The NEXT session's first reviewed round
then either registers each candidate (spending the next free ID) or
resolves it inline as a DECISION per planner_reviewer_prompt.md §4
item 7. This keeps the ledger monotonic across the session boundary
and keeps the operator-facing narrative in agreement with the disk.

Disk vehicle (operator ruling 2026-08-01, F056-candidate loss): at
closure, any candidate findings are ALSO written to
`.agent/candidates.md` — one entry each: description, source
feature, date — inside the closure commit. `.agent/**` is already
within the closure commit's allowed path set, so the R-0154
exact-paths rule is unchanged. The chat brief keeps listing
candidates as before, but the FILE, not the brief, is the carrier
of record: a brief-only candidate is exactly what the F056 closure
lost. The Window-1 session bootstrap reads `.agent/candidates.md`;
if it is non-empty, the FIRST reviewed round registers each entry
(next free ID) or resolves it inline as a §4.7 DECISION, and
empties the file in that same round. A non-empty candidates file at
feature-claim time is itself a block condition
(planner_reviewer_prompt.md §1).
TO>>>
