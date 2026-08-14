# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- A resolved finding still carries its `Landed:` line beside its `Done:` line, so the record shows a signal that means "unreviewed fix" on a fix that was reviewed. `planner_reviewer_prompt.md` §4.4 says the reviewer "replace[s] the `Landed:` line with the authored `Done:` text at the next gate" and that "a surviving `Landed:` line is an unreviewed fix". In `.agent/live_review.md` on this branch, R-0370 has BOTH: a `Landed: R-0370 — …` line from R5 and a `Done: R-0370 — Fixed at a01e8a97…` line from R6. Nothing broke, because the mechanical open-set computation subtracts `^Done:` and ignores `^Landed:`, so R-0370 is correctly absent from every open set this feature computed. The conflict is between two rules that both live on disk: §4.4 says REPLACE, while this record is append-only by the convention every F057 block states and every round applied. Under the append-only reading, appending the `Done:` line IS the replacement, and deleting the `Landed:` line would rewrite a history the file exists to preserve; under the §4.4 reading, the stale line should be gone. The cheapest fix is one clause in §4.4 saying that in an append-only record a later `Done:` supersedes an earlier `Landed:` for the same id, and that the `Landed:` line is left in place — which is what every round here already did. Raised as a candidate rather than a finding because the amendment edits `docs/agents/planner_reviewer_prompt.md`, outside F057's change set, and F057 will not open a doc it never owned in order to close it. · source F057 · 2026-08-14
