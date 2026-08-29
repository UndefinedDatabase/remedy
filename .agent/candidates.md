# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

Two entries, both raised at the F033 CLOSURE GATE and therefore carrying no
R-id: the protocol rules that a finding raised during a closure review is a
candidate only, and the NEXT session's first reviewed round either registers it
with the next free id or resolves it inline as a §4.7 DECISION, and empties this
file in that same round. They are recorded in the one commit DECISION amend0827
D2 permits after the closure commit, so its path set is exactly this file.

1. THE README'S PER-TIER ACCEPTED LIST IS GUARDED IN ONE DIRECTION ONLY, AND IT
   IS NOW ONE FEATURE SHORT. · F033 · 2026-08-29. Measured by the reviewer at
   `179d4031`: `README.md` carries a prose block headed "Accepted in Tier 5 so
   far:" and the F033 closure did not extend it, so the block names ten DISTINCT
   feature ids while `docs/roadmap/STATUS.md` carries eleven accepted Tier 5
   features and the README's own tier table, which the same commit moved, reads
   11. The missing one is F033 itself. NO TEST CATCHES THIS, and that is the
   candidate rather than the missing paragraph:
   `tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_reports_the_accepted_foundation_and_no_later_feature`
   asserts only that every feature the README LISTS as accepted IS accepted in
   the ledger, so an accepted feature the README omits is invisible to it, in
   the same way the tier-table pin was invisible before R-0360 added it. The
   round-29 worker found this, declared it and correctly declined to write the
   paragraph, because no pair ordered one and the prose is the reviewer's to
   author. Whoever takes this decides two things: whether the paragraph is added
   for F033, and whether the pin is widened to the second direction — every
   accepted id of a tier that the README lists AT ALL must appear in that tier's
   block — which is the half that stops the drift recurring.

2. THE SAME BLIND SPOT ALREADY HIDES A DUPLICATE IN THAT LIST. · F033 ·
   2026-08-29. Measured by the reviewer at `179d4031` while checking entry 1: the
   Tier 5 block names ELEVEN ids of which only TEN are distinct, because `F037`
   occurs twice. Nothing on disk is wrong about F037 — it is genuinely accepted —
   but the list is a hand-maintained inventory whose only guard reads it in the
   direction that cannot see either fault, so the duplicate has stood
   unremarked. It is recorded separately from entry 1 because the fixes differ:
   entry 1 is a missing paragraph plus a widened pin, this one is a deletion, and
   a single entry covering both would let one be repaired while the other is
   read as done.
