# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

The two entries the F033 closure gate raised were discharged in F040 round 1 and
the reasons are on the record in `.agent/live_review.md`: the first as new
evidence on the OPEN finding `R-0570`, which already describes that defect and
keeps its own routing, and the second as DECISION F040 D1, which measured it and
found no defect to repair. No id was spent on either.

1. THE README'S PER-TIER ACCEPTED LIST IS STILL MISSING F033'S OWN
   PARAGRAPH. · F040 · 2026-08-30. Found during F040's own closure-round
   README audit at C3 (`0ec9bb37`): `README.md` carries a prose block headed
   "Accepted in Tier 5 so far:" and F033's closure did not extend it. What's
   missing: F033's capability paragraph. Where: `README.md`, in the Tier 5
   prose block, between F257's paragraph and F040's own paragraph (the one
   this round's C3 just added) — the slot the list's existing chronological
   convention would put it in. F033 IS counted in both the accepted-count
   pin and the Tier 5 Done cell (both pins pass regardless), and NO TEST
   CATCHES THE OMISSION:
   `tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_reports_the_accepted_foundation_and_no_later_feature`
   asserts only that every feature the README LISTS as accepted IS accepted
   in the ledger, so an accepted feature the README omits stays invisible to
   it. NOT F040's defect to fix inline — recorded here as a closure
   candidate per STATUS_closure_protocol.md, source feature F040, discovered
   during F040's own closure's README audit, dated 2026-08-30.
