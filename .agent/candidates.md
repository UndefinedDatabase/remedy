# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

F085's rounds raised no candidate of their own: everything its reviews found was
registered as an R-id in `.agent/live_review.md` while the round that found it was
still open, which is where a finding belongs. The three the closure-prep round
registered — R-0567, R-0568 and R-0569 — are findings and not candidates, and they
close as documented risks under precondition 1 rather than riding here.

One candidate, raised by the reviewer's closure review of R74 · source F085 ·
2026-08-19. The root `README.md` names five accepted Tier 2 features in its
"Accepted in Tier 2 so far" list while its own tier table records thirteen, and
nothing catches the gap: `test_the_readme_reports_the_accepted_foundation_and_no_later_feature`
in `tests/docs/test_docs_consistency.py` checks only that every feature the README
LISTS is accepted in the ledger, never the converse, so an incomplete list passes.
The count pin and the tier-table pin are both one-directional in the same way. This
is not F085's defect — the same list was already incomplete when F082 and F083
closed, neither of which added itself — which is exactly why it needs a carrier
rather than a repair inside this feature.

If the reviewer's gate of this round raises a further candidate after this file is
committed, that candidate rides in the round report and in `.agent/handoff.md`, and
the next feature's first reviewed round registers it — the path F082's three
closure candidates took to become R-0448, R-0449 and R-0450 at F083 R1.
