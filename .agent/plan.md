# Plan — F103 Token ledger (SQLite)

Branch: feature/f103-token-ledger · claimed `[~]` in
docs/roadmap/STATUS.md. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
R1-R6 PASSed; LAST_REVIEWED_SHA 7f32dae9. Open findings 0; next free
ID R-0222. R-0221 is carried in `.agent/candidates.md`.

## Goal
Token and cost actuals become queryable: every provider call lands as a
row in a per-project SQLite ledger at
`<data_root>/projects/<uuid>/ledger.sqlite`, and `remedy stats cost`
answers per-job, per-role and per-period questions from it. The file
evidence stays the source of truth; the database is a mirror, and a
writer failure never fails the run. Per DECISION D16 a row is one
finalized TASK RUN, keyed `"<job_id>:<task_id>"`. T001, T002 and T003
are built and reviewer-gated, the R5 integration gate passed on the
reviewer's own full-suite run, and R6 armed the live mirror so a real
job yields rows.

## Current Step
R7 — closure per docs/roadmap/STATUS_closure_protocol.md: the evidence
job, a FRESH review zip (a zip failure is a closure blocker), the
full-suite confirmation run, and the reviewer-authored STATUS
`[~]`->`[x]` line together with the README capability sync in the SAME
commit, last on the branch, then `gh pr create`. That PR is NOT merged
by the session that creates it — it merges at the next feature's Open
PR Gate, which is the operator's manual-review window.

## Next Steps
- After the PR: the feature-done banner and the session ends. The
  operator may review and merge manually at any time.

## Risks
- The closure full-suite confirmation is LOAD-BEARING, not a
  formality: R6 landed production code AFTER the R5 integration gate,
  so the confirmation run is the only full-suite evidence covering the
  live-mirror wiring.
- R-0221 sits in `.agent/candidates.md` and is a block condition at the
  next feature's claim time. Closure must register or resolve it, never
  silently drop it.
- The closure commit must carry the STATUS line and the README
  capability sync TOGETHER, and the README may claim only what is
  merged and verified.
