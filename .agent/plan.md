# Plan — F104 Hard budget enforcement — CLOSED AND REVIEWER-GATED

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 was merged at the Open PR Gate. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
R1-R11 executed; F104 closed, reviewer-gated through 16f1c375; next ID R-0229.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach it, recording the arithmetic. The reactive backstop is unchanged.

## Current Step
R11 — DONE, and it is the LAST round on this branch. R10 recorded the gate on
R9 but nothing recorded the gate on R10, and each further round would inherit
that gap. R11 appended the reviewer's PASS gate on R10 (`LAST_REVIEWED_SHA`
advances 8e651661 -> 16f1c375), stated the TERMINATING CONVENTION inline — an
on-disk round log cannot record the gate on the commit that writes it, so the
final round's verdict is carried by `.agent/handoff.md`, the reviewer's report
and PR #188 instead, a terminator and not a second R-0228 — narrowed one
over-broad sentence in the `Done: R-0228` text, and registered the convention
as the SECOND closure candidate. No code, test, doc or `docs/roadmap/STATUS.md`
byte changed — F104 stays accepted `[x]`.

## Next Steps
- F104 is CLOSED and reviewer-gated through 16f1c375. Nothing further is owed
  on this branch, and no further round belongs here. R11's own gate is carried
  by `.agent/handoff.md`, the reviewer's completion report and PR **#188** — by
  construction, not by omission.
- PR **#188** is merged by the REVIEWER at the Open PR Gate, never by the
  worker — the operator's window (closure protocol step 6).
- Next feature per Rule A5: **F105 — Cache-optimal prompt ordering**, in a
  fresh session, after PR #188 is merged. Its first reviewed round MUST
  register or resolve BOTH entries now in `.agent/candidates.md` — the
  worker-authored `Done:` text that preceded the reviewer's (F104 R7) and the
  terminating convention above — and empty the file.

## Risks
- R-0221 stays OPEN: the UI auto-build test refreshes `apps/ui/dist` mtimes
  mid-suite. Documented LOW, F252 flake-debt class, not F104's code to fix
  (Scope Control). It cost the R7 gate six phantom base-only failures, each
  attributed by controlled evidence.
- The band estimate is a FLOOR (DECISION F104 D6): it can only under-predict,
  which is why the reactive backstop must stay exactly as it is.
- Cost is NULLABLE by design (P6): an unpriced call stays None everywhere.
- The manifest budget schema is SHARED F012 surface; any further budget field
  owes the same run-manifest gate before it is believed.
