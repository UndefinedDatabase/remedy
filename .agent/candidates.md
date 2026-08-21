# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- A UNIQUENESS GATE OVER `.agent/live_review.md` MUST SAY LINE-ANCHORED, BECAUSE
  THAT FILE LEGITIMATELY QUOTES ITS OWN GATE HEADERS. · source F008, raised by
  the reviewer during the R35 gate · 2026-08-21. The R35 block's G6 ordered "the
  R35 pair occurs EXACTLY ONCE" for the entry `Gate: R35 — the R34 entry.` The
  worker read it line-anchored over `^Gate: ` lines, reported 1, and was right:
  measured by the reviewer at `c5ebf179`, that byte string occurs TWICE in the
  file, the second inside finding R-0600, which quotes the F086 record's
  identically-worded round-35 header. Header strings repeat across features by
  construction, so any round whose header a finding has quoted inherits an
  unmeetable gate the moment the count is read as a substring. Nothing false
  landed and the ledger is healthy — 35 `Gate: ` lines under 35 distinct keys at
  that commit. Counter-measure, beside §3 item 26 which produced this gate class:
  a uniqueness or count gate over a file that quotes its own record format states
  the anchor it is read under, and a block ordering such a count orders BOTH
  readings and labels each — as R-0586 already requires backtick-quoted spans to
  be deleted before a token is counted. The fix edits
  `docs/agents/planner_reviewer_prompt.md`, which F008 does not own, so it routes
  to the paydown branch carrying the reviewer-text findings.
