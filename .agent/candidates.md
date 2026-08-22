# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

NON-EMPTY. Two candidates, both REVIEWER-BLOCK DEFECTS in the F009 R30 block
saved at `e46e5d0c`, both found and declared by the WORKER in its handback and
both confirmed by the reviewer by measuring the named file. They are recorded
here rather than registered because the session reached its stated round cap
after the R30 verdict was issued; the FIRST reviewed round of the next session
registers each (next free id R-0646) or resolves it inline as a
docs/agents/planner_reviewer_prompt.md §4.7 DECISION, and empties this file in
that same round. Writing them to disk rather than to a round report is finding
R-0494's rule applied: under self-drive, a reading routed to the round report
dies with the session.

- A GATE COUNTED A MARKDOWN CONSTRUCT THE FILE IT NAMES DOES NOT CONTAIN, so the
  clause could not fail for any round · F009 R30 · 2026-08-22. G8 ordered that
  the line-anchored `^## ` headings of `docs/agents/integration_gate.md` read the
  same count at the round base and at C4. That file carries ONE `# ` title and a
  numbered list, and ZERO `^## ` headings, so the reviewer measured 0 at both
  commits and "the same count" is true of every possible round. This is the
  R-0438 vacuous-gate class arriving through a document's STRUCTURE rather than
  through a missing path: checklist item 24 makes a reviewer resolve every PATH a
  gate names, and nothing makes it resolve the CONSTRUCT a gate counts, which is
  why R-0438's own clause does not reach it — the path here is real and only the
  heading level is absent. Candidate counter-measure for the round that registers
  this: before ordering a count of a markup construct, read that construct's
  count in the target at the base, and where it is 0 either drop the clause or
  count the construct the file actually uses.

- A GUARD-TEST CONTROL THAT DOES NOT DISCRIMINATE IN THE ROUND THAT RUNS IT ·
  F009 R30 · 2026-08-22. G6 ordered the max REGISTERED id read line-anchored and
  cited R-0630, whose warning is that an unanchored scan "reports a maximum that
  was never registered". Because R-0645 is minted by that same round and is the
  highest id in the file, the anchored and the unanchored maxima are BOTH R-0645
  and the reading demonstrates nothing. The discriminating readings exist and the
  worker reported them without being asked — 211 anchored ids against 271
  unanchored strings, 60 of which were never registered and which reach R-0627,
  and 30 anchored `Gate: R` keys against 78 unanchored — but the block ordered
  the one reading that is blind precisely when the round's own new id is the
  ceiling. Candidate counter-measure for the round that registers this: a control
  that exists to show an anchoring matters is ordered as the DIFFERENCE between
  the anchored and unanchored populations, never as a maximum, because the
  maximum coincides whenever the newest id is the reviewer's own.
