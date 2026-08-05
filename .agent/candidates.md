# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- F070 was accepted with a specified execution step unbuilt (the
  multi-cycle executor call named in T1_F070.md Design): its
  zero-provider evidence never ran a job, so no test could notice.
  Review-practice/gate-tooling class: how closure evidence can
  prove a specified verb is actually CALLED, not merely present.
  Source: F075 R4 diagnosis · 2026-08-04.
- The move schema has no resume kind: a paused job's only forward
  path is re-dispatch, and a job that ended max_cycles_reached
  cannot be continued. Roadmap F045/F106 territory.
  Source: F075 R5/R6 · 2026-08-04.
- R-0199 (registered, deferred): the attempt-03 campaign read
  ~872 GB while writing ~2 MB. Reviewer hypothesis, unverified:
  gauntlet_runner.data_root_digest full-scans the operator's real
  data root before and after every run — cost scales with operator
  history. Needs a measured diagnosis + fix order (manifest-based
  digest or scoped root). Source: F075 R11 · 2026-08-05.
  Operator priority: HIGH — the scan class is the likely root of
  multi-hour campaign wall-clock on this machine (2026-08-05); order
  the measured diagnosis early in the F079 R1 candidate sweep.
- The mid-run UI rebuild recurs: REMEDY_UI_NO_AUTO_BUILD=1 did not
  prevent a rebuild inside the R12 base gate run (6 base-only ids,
  identical dist content hash, mtimes inside the run) — the same
  class as the F069 R2 candidate. Suspect: a spawned server/build
  path not honoring the env var. Gate tooling, not F075 code.
  Source: F075 R12 gate · 2026-08-05.
