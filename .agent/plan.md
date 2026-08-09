# Plan — F104 Hard budget enforcement — CLOSED AND REVIEWER-GATED

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 was merged at the Open PR Gate. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
R1-R10 executed; F104 is closed and reviewer-gated through 8e651661.
Next free finding ID: R-0229.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check is unchanged — prediction never replaces the backstop.

## Current Step
R10 — DONE. R9 cleared the stale "Awaiting review" markers on R6 and R7 but
missed the same marker on R4, although R-0225 and R-0226 are both recorded as
"found in the R4 review" and R5 was the repair round that fixed them. R10
registered that contradiction as **R-0228** (Low), recorded the reviewer's PASS
gate on R9 (`LAST_REVIEWED_SHA` advances b5a241c3 -> 8e651661), and then, in a
SEPARATE repair commit, corrected the R4 line to PASS and appended the
reviewer-authored `Done:` text. The string `Awaiting review` now occurs ZERO
times in `.agent/live_review.md`. No code, test, doc or `docs/roadmap/STATUS.md`
byte changed this round — F104 stays accepted `[x]`.

## Next Steps
- F104 is CLOSED and reviewer-gated through 8e651661. Nothing further is owed
  on this branch.
- The closure PR **#188** is open and is merged by the REVIEWER at the Open PR
  Gate, not by the worker — the operator's window (closure protocol step 6).
- Next feature per Rule A5: **F105 — Cache-optimal prompt ordering**, in a
  fresh session, after PR #188 is merged.
- `.agent/candidates.md` still carries ONE open F104 closure candidate (a
  worker-authored `Done:` paragraph preceded the reviewer's, F104 R7). The
  first reviewed round of the next feature MUST register or resolve it.

## Risks
- R-0221 stays OPEN: the UI auto-build test refreshes `apps/ui/dist` mtimes
  mid-suite. Documented LOW, routed to the F252 flake-debt class, not F104's
  code to fix under AGENTS.md Scope Control. It cost the R7 gate six phantom
  base-only failures (F103 R5 measured seven), each attributed by controlled
  evidence.
- The band estimate is a FLOOR (DECISION F104 D6): it can only under-predict,
  which is why the reactive backstop must stay exactly as it is.
- Cost is NULLABLE by design (P6): an unpriced call stays None everywhere.
- The manifest budget schema is SHARED F012 surface; any further budget field
  owes the same run-manifest gate before it is believed.
