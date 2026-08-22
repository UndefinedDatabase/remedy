# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

NON-EMPTY. One candidate, raised by the reviewer during the F009 closure review
and recorded here without an id because the closure protocol reserves ids for
the next session's first reviewed round.

- THE CLOSURE PRECONDITION THAT IS SUPPOSED TO BLOCK ON OPEN HIGH FINDINGS
  CANNOT SEE THIS REPOSITORY'S FINDING LEDGER, SO IT PASSES VACUOUSLY · F009
  R34 · 2026-08-22. `_check_high_blockers_open` in
  `packages/orchestration/integrity_gate.py` parses `.agent/live_review.md` for
  findings shaped `### R-XXXX:` with `- **Status**:` and `- **Severity**:`
  lines beneath them, and reports PASS with "no open blocker/high findings"
  when it matches none. Measured at `06aeb749`, that file contains 0 of those
  headings, 0 `- **Status**:` lines and 0 `- **Severity**:` lines against 213
  real entries in the form `- R-XXXX — <Severity> — <headline>`, and two of
  those entries — R-0495 and R-0574 — are High and carry no `Done:` line. So
  the check answers PASS for a ledger holding exactly what it exists to catch,
  and closure precondition 3 has been satisfied by a reading that cannot fail.
  This is the R-0438 vacuous-gate class in PRODUCTION code rather than in a
  reviewer block, which is why it is worth more than the two that preceded it:
  a reviewer block is read by a human every round, and this parser is not.
  Nothing about the F009 closure is unsound because of it — the reviewer read
  the severities directly, found both Highs inherited from the closed features
  F085 and F086, and the verdict is PASS_WITH_RISKS on that basis — but the
  automated guard contributed nothing to that finding. Candidate
  counter-measure for the round that registers this: teach the parser the
  `- R-XXXX — <Severity> —` form the ledger actually uses with `Done:` as the
  resolution marker, and give it a test whose fixture is a ledger in the REAL
  format holding one open High, so the check goes red where today it is blind.
