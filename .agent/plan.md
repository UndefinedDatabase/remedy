# Plan — F045 Loop definitions (CLOSED)

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f after the
F115 closure PR #195 merged. Accepted HEAD:
1c84c81805668e1d0f1e04370d5366389c8a8b20 — the head the evidence job and the
review package cover, i.e. after C3 and before this closure commit. Last
reviewed SHA c6b0aeb7 (R15 PASS); feature verdict PASS_WITH_RISKS. Next free
finding ID: R-0359. Open findings: 3 — R-0350, R-0354, R-0358 — all Low,
carried as documented risks. The closure PR opens directly after this commit
and stays UNMERGED by design; its number and URL are in the handback, because
a PR cannot exist before the commit it must contain (F115 closure 57a24947).

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` materializes one as a completely normal job/mission with
loop provenance in evidence (docs/roadmap/features/T2_F045.md). DONE.

## Current Step
Closed. T001–T003 complete and gated; the Built State section of
docs/roadmap/features/T2_F045.md is current (aa5e66f5, every claim re-verified
against the source before commit); the integration gate in
`.agent/gate_f045_r15/` shows an EMPTY `comm -13`, zero branch-only failures;
`integrity check --json` is `"passed": true`; the evidence job is
`f045-closure` and `remedy-review-20260814-032227-READY_FOR_REVIEW.zip` is
READY_FOR_REVIEW; STATUS.md carries `[x]` and README.md the matching count.

## Next Steps
1. The closure PR merges at the NEXT feature's start via the AGENTS.md Open
   PR Gate — that gap is the operator's manual-review window. The operator
   may also merge it manually at any time.
2. Next feature per Rule A5 and STATUS order: F057 — Rate-limit-aware
   scheduler. New session, new branch, nothing carried over but
   `.agent/candidates.md`.
3. That first reviewed round MUST register or resolve BOTH entries in
   `.agent/candidates.md` and empty the file
   (docs/roadmap/STATUS_closure_protocol.md).

## Risks
- The suite is RED at the merge base with five known `reviewer_conventions`
  token-cap ids, unrelated to F045 and unfixed here on purpose
  (DECISION F045 D8; candidate 1).
- README's Tier 2 `Done` cell was 6 while the ledger derived 7; this closure
  writes 8 — pre-existing off-by-one from `98a49b5c`, unpinned (candidate 2).
- Schedule and event triggers are validated but INERT until the scheduler.
- `report_path` resolves through `jobs_dir()`, honouring no `root=`; report
  tests isolate through the environment (R-0351/R-0352).

Fortschritt: 100 % (T001 ✅ · T002 ✅ · T003 ✅ · Integrationsgate ✅ · Closure ✅) — gemessen
