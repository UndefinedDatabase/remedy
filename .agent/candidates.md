# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

- Job/mission resume-from-persisted-state — a new orchestrator move-schema
  `resume` kind so a paused job, or one that ended `max_cycles_reached`, can
  continue rather than only re-dispatch (F075 R5/R6 evidence, routed via
  F079 R1 as R-0201, scope-noted onto F106 2026-08-06 as in-scope territory
  alongside provider-session resume). F106 closed on its own Task slicing
  (T001-T003, provider-session resume only) without building this half; the
  deferral, and why it is not a dropped promise, is recorded in full as
  DECISION F106 D2 in `.agent/live_review.md`. · source feature: F106 ·
  date: 2026-09-02

The one entry F040's closure gate raised was discharged in F258 round 1 as new
evidence on the already-open finding `R-0570` in `.agent/live_review.md`; no id
was spent. The two entries F033's closure gate raised before it were discharged
the same way in F040 round 1.

> Recorded AFTER the F106 closure commit, per DECISION amend0827 D2 (the
> carrier for a candidate raised at the closure gate itself, where no earlier
> commit remains to hold it). The accepted HEAD
> (82278107ecea9e291d668caa9180f3d847d13e88) and the review package both
> predate this commit and are unaffected.
