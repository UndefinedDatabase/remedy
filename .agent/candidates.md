# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

- The closure package a STATUS line names is absent from disk at closure time.
  `remedy-review-20260827-122441-READY_FOR_REVIEW.zip` was built and verified at
  F031 CLOSURE 2 — 20155047 bytes over 3596 members, SHA-256 recomputed
  independently by the reviewer — and no copy of it exists anywhere under the
  repository at the closure round, while the F022 package from four days earlier
  still sits in the repository root. `.gitignore` excludes the archive by design
  and the durable pointer is the STATUS line, so this is not a failed build and
  not a protocol breach; what is unexplained is the ASYMMETRY, and the operator's
  review window for F031 cannot be reopened from this machine without a rebuild.
  Decide whether closure should verify the package still exists, or state
  plainly that it is handed over and expected to vanish. · source F031 ·
  2026-08-27
