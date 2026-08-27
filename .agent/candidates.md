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

- A retired clause was reproduced from an OPEN finding's own body into two
  permanent records at closure. `DECISION F031 D27` in `.agent/decisions.md` and
  the Risks section of `.agent/plan.md` both route the `R-0708` repair away
  "because `tests/ui_server/` is outside F031's change set". THAT CLAUSE IS FALSE
  AND WAS ALREADY MEASURED FALSE: the `Gate: F031 R69` entry of
  `.agent/live_review.md` records it as false and narrows it to "the FAILING
  CLASS, ITS HELPER AND THE FAILING TEST are outside F031's change set, even
  though the FILE is not", and five files under `tests/ui_server/` change on this
  branch, `test_live_state.py` among them. The DECISION's substance is
  unaffected: commit `6b68718e` leaves `TestUIServerIntegration`, its
  `_start_server` helper and `test_context_budget_endpoint` untouched at lines
  121, 133 and 317, so only the WIDTH of one supporting sentence is wrong. The
  reviewer read the wide form off the `R-0708` paragraph, which still carries it,
  and never checked whether a LATER gate entry had narrowed it — the worker
  applied both slices byte for byte and declared the contradiction, which is why
  it is recoverable at all. Register the reviewer-side rule this earns: a clause
  quoted from a finding's BODY is re-measured against every later gate entry
  naming that finding, because a correction lands in the gate entry and never in
  the finding it corrects. · source F031 · 2026-08-27

- A candidate raised while GATING the closure commit has no disk carrier left.
  The disk-vehicle rule puts candidates in `.agent/candidates.md` "inside the
  closure commit", while the closure protocol's rendering of Rule A4 makes the
  STATUS edit the last commit on the branch — so a defect the reviewer finds when
  it reviews that very commit can reach no file, and the entry above is exactly
  that case. It is carried here by an EXTRA `.agent/candidates.md`-only commit,
  declared as a deviation from that rendering: Rule A4 as stated in
  `docs/roadmap/ROADMAP.md` requires only "STATUS.md updated in the same PR",
  which holds, and the R-0154 pin the rendering protects is README/STATUS
  agreement, which a candidates-only commit cannot disturb. Decide whether the
  protocol should permit this commit explicitly, or should instead order the
  closure gate to run BEFORE the closure commit so the carrier is still open. ·
  source F031 · 2026-08-27
