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

## Raised after the closure commit

One further candidate, raised by the reviewer's gate of R74 · source F085 · 2026-08-19, and written
here rather than only into the round report because this file is the carrier of record and a
brief-only candidate is exactly what the F056 closure lost. A branch's LAST round has no on-disk gate
entry by construction (docs/agents/planner_reviewer_prompt.md §4 item 13), so on disk a last round
whose verdict was issued and a last round whose verdict was never written are INDISTINGUISHABLE: both
show a handback with no `Gate:` paragraph naming it and no verdict anywhere. This session found
exactly that state at e950e8af — R74's handback present, `.agent/live_review.md` correctly silent
about R74, no verdict in `.agent/handoff.md`, and no comment on PR #204 when this gate began — and had
to re-run the entire round gate to establish which of the two states it was looking at. Item 13 tells
the reviewer to write the verdict into the handoff and the PR, but nothing on disk goes red when that
write does not happen, and the closure protocol's preconditions do not check for it either. Two
obvious counter-measures, for whoever takes this: have the closure round's own block order the verdict
slice as a named unit the way every other authored text is ordered, or give `.agent/handoff.md` a
terminator marker the integrity gate can look for. This is not F085's defect — it is a hole in the
terminator rule itself, which is why it needs a carrier rather than a repair inside this feature.
