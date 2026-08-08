# Plan — F103 Token ledger (SQLite)

Branch: feature/f103-token-ledger · claimed `[~]` in
docs/roadmap/STATUS.md. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
R1-R5 PASSed; LAST_REVIEWED_SHA af91d57b. Open findings 1 (R-0220,
Medium); next free ID R-0222.

## Goal
Token and cost actuals become queryable: every provider call lands as a
row in a per-project SQLite ledger at
`<data_root>/projects/<uuid>/ledger.sqlite`, and `remedy stats cost`
answers per-job, per-role and per-period questions from it. The file
evidence stays the source of truth; the database is a mirror, and a
writer failure never fails the run. Per DECISION D16 a row is one
finalized TASK RUN, keyed `"<job_id>:<task_id>"`. T001, T002 and T003
are built and reviewer-gated, and the R5 integration gate passed on the
reviewer's own full-suite run.

## Current Step
R6 — arm the live mirror (finding R-0220, DECISION D17). Today the four
`ledger_*` arguments of `write_evidence_bundle` are passed by TESTS
only, so a real job writes zero rows and the feature's acceptance
criterion is unmet. This round wires the task-run seam in
`job_evidence.py` to supply them, keeps the hook inert when no project
resolves so no test starts writing into the user's data root, and pins
the behaviour with a test that drives the PRODUCTION path and passes no
`ledger_*` argument by hand.

## Next Steps
- R7 — closure per docs/roadmap/STATUS_closure_protocol.md: the
  evidence job, a FRESH review zip (a zip failure is a closure
  blocker), the reviewer-authored STATUS `[~]`->`[x]` line and the
  README capability sync in the SAME commit, last on the branch, then
  `gh pr create`. That PR is NOT merged by the session that creates
  it — it merges at the next feature's Open PR Gate, which is the
  operator's manual-review window.

## Risks
- The wiring is the one place this feature can slow a real run. R5
  measured the cost at +1.4 ms per finalized task run; a change that
  moves that number materially is a finding, and tuning it is not this
  round's licence.
- Arming the mirror must not give tests a route into the real data
  root. Inertness without a resolved project is a guarantee to pin with
  a test, not a comment.
- R-0221 is carried in `.agent/candidates.md` and belongs to the owning
  feature. Closure must register or resolve it, never silently drop it.
