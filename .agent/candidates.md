# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

NON-EMPTY. One candidate, raised by the reviewer during the F022 closure review
and recorded here without an id because the closure protocol reserves ids for
the next session's first reviewed round. It was MEASURED by the reviewer at
`9a1e677f`, not read back out of a handback.

- FIVE HISTORICAL REVIEW PACKAGES WERE CREATED AT ONE INSTANT DURING THIS
  SESSION AND NOTHING IN THE SESSION'S RECORD ACCOUNTS FOR IT · F022 R19 ·
  2026-08-23. `stat` reports that `remedy-review-20260726-001936-`,
  `-20260726-165629-`, `-20260726-202004-`, `-20260726-215057-` and
  `-20260727-101857-READY_FOR_REVIEW.zip` each carry an mtime EQUAL to their
  ctime at 2026-08-23 13:29:18, all five within 44 milliseconds of each other,
  while their filenames date them to 2026-07-26 and 2026-07-27. Equal mtime and
  ctime means the bytes were WRITTEN at that instant rather than merely touched,
  so five packages named for July were created during this August session by a
  step no round ordered and no handback records. Nothing about F022's closure
  rests on them: this feature's package is
  `remedy-review-20260823-135731-READY_FOR_REVIEW.zip`, the reviewer recomputed
  its SHA-256 over the published file and read its manifest, and all five of
  these are outside the review subject and gitignored. The reason to record it
  anyway is R-0662: a glob in the F021 R40 closure destroyed roughly 78
  historical review packages on this machine, so packages APPEARING
  unaccountably is the same blind spot from the other side, and a restore nobody
  can name is not better than a deletion nobody intended. Candidate
  counter-measure: identify what writes those files — a recovery path in the
  packaging pipeline, a worktree operation, or an operator action — and either
  make it say so, or establish that the five are byte-identical to what the
  filenames claim and record where the originals were kept.
