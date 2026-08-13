# Plan — F115 Prompt breakdown & cost report (CLOSED)

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after PR
#194 merged. Accepted HEAD: 705feeb19c871db6313828d76ad4e1d9e0cc4d58. Last
reviewed SHA 7bc57cd1 (R21 PASS, integration gate); feature verdict
PASS_WITH_RISKS. Next free finding ID: R-0344. Open findings: 15 — R-0320,
R-0322, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333, R-0334, R-0336,
R-0337, R-0339, R-0341, R-0342, R-0343 — all Medium/Low, carried as
documented risks. The closure PR is opened directly after this commit and
stays UNMERGED by design; its URL is in the handback.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE tokens go
— by segment kind, by role, by task class — plus a cost curve and a
prior-period comparison, as markdown and json, every number traceable to a
ledger row, missing data reported as missing
(docs/roadmap/features/T2_F115.md). DONE.

## Current Step
Closed. T001, T002 and T003 are complete and gated; the Built State section
of docs/roadmap/features/T2_F115.md is current (0fc9c051, 30/30 claims
verified); the integration gate in `.agent/gate_f115_r20/` and
`.agent/gate_f115_r21/` shows zero branch-only failures against the merge
base; `remedy integrity check --json` is PASS; the evidence job is
`f115-closure` and the package
`remedy-review-20260813-142842-READY_FOR_REVIEW.zip` is READY; STATUS.md
carries the `[x]` line and README.md the matching count.

## Next Steps
1. The closure PR merges at the NEXT feature's start via the AGENTS.md Open
   PR Gate — that gap is the operator's manual-review window. The operator
   may also merge it manually at any time.
2. Next feature per Rule A5 and STATUS order: F045 — Loop definitions. New
   session, new branch, nothing carried over but `.agent/candidates.md`.
3. That first reviewed round MUST register or resolve every entry in
   `.agent/candidates.md` and empty the file
   (docs/roadmap/STATUS_closure_protocol.md). The file is `(empty)` today.

## Risks
- The suite is RED at the merge base with five known `reviewer_conventions`
  token-cap ids (R-0322), unrelated to F115 and unfixed here on purpose.
- `scripts/make_review_zip.sh` carries the operator's uncommitted prune-list
  edit. Per DECISION F115 D7 it is STASHED, not committed and not discarded:
  `stash@{0}` "f115-closure: operator's make_review_zip.sh prune-list edit".
  It was never popped; reversing it is the operator's call.
- A per-role breakdown has one bucket and a per-task-class breakdown has no
  source; both limits are documented, not faked, and own their own features.

Fortschritt: 100 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration-Gate ✅ · Closure ✅) — gemessen
