# Plan — F104 Hard budget enforcement — CLOSED

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 was merged at the Open PR Gate. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
R1-R8 executed; R-0222 through R-0227 all Resolved with reviewer-authored text.
Next free ID: R-0228.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check is unchanged — prediction never replaces the backstop.

## Current Step
R8 — CLOSURE, complete per docs/roadmap/STATUS_closure_protocol.md. T001-T003
done. `docs/roadmap/features/T2_F104.md` carries a Built State section
(precondition 4); `remedy integrity check --json` PASS (5/5, exit 0); the
evidence bundle `f104-closure` was produced by
`job_evidence.create_manual_completion_bundle(review_feature_id="f104")` into
the gitignored `.remedy-wt/` and evaluates READY (gate matrix ok,
final-verifier and token-truth VERIFIED_EQUAL); the review zip
`remedy-review-20260809-033908-READY_FOR_REVIEW.zip`
(SHA-256 6117b6b0…8bb6a) covers accepted HEAD
`68a7412019e92232a880625b7fce4e48c7198744` and spans BASE..HEAD.
`docs/roadmap/STATUS.md` now reads `[x] F104` and README.md moved to
41 of 255 with Tier 2 at 3; both in the same commit (R-0154).

## Next Steps
- The closure PR is open and MUST NOT be merged in this session. It merges at
  the next feature's start via the Open PR Gate — the operator's manual-review
  window (closure protocol step 6).
- Next feature per Rule A5: F105 — Cache-optimal prompt ordering, in a fresh
  session, after the closure PR is merged.

## Risks
- R-0221 stays OPEN: the UI auto-build test refreshes `apps/ui/dist` mtimes
  mid-suite. Documented LOW, routed to the F252 flake-debt class, not F104's
  code to fix under AGENTS.md Scope Control. It cost the R7 gate six phantom
  base-only failures, each attributed by controlled evidence.
- The band estimate is a FLOOR (DECISION F104 D6): it can only under-predict,
  which is why the reactive backstop must stay exactly as it is.
- Cost is NULLABLE by design (P6): an unpriced call stays None everywhere.
- The manifest budget schema is SHARED F012 surface; any further budget field
  owes the same run-manifest gate before it is believed.
