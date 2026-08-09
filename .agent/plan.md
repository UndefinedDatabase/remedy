# Plan — F104 Hard budget enforcement — CLOSED AND REVIEWER-GATED

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 was merged at the Open PR Gate. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
R1-R9 executed; R-0222 through R-0227 all Resolved with reviewer-authored text.
Next free ID: R-0228.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check is unchanged — prediction never replaces the backstop.

## Current Step
R9 — DONE. The reviewer's gate on R6, R7 and R8 is now recorded in
`.agent/live_review.md`: those three rounds read **PASS** rather than "Awaiting
review", and a `Reviewer gate on R6+R7+R8` entry holds the evidence
(range `549f2bac..b5a241c3` read as a real diff, gates A-D re-run with real
exit codes, the closure zip re-hashed on disk, the R7 integration-gate evidence
checked directly, one independent mutation red-proof). `LAST_REVIEWED_SHA`
advances 549f2bac -> b5a241c3. The stale "seven phantom base-only failures"
count inside the carried finding R-0221 now reads "six or seven" with both
measurements attributed. No code, test, doc or `docs/roadmap/STATUS.md` byte
changed this round — F104 stays accepted `[x]`.

## Next Steps
- F104 is CLOSED and reviewer-gated through b5a241c3. Nothing further is owed
  on this branch.
- The closure PR **#188** is open and MUST NOT be merged in this session. It
  merges at the next feature's start via the Open PR Gate — the operator's
  manual-review window (closure protocol step 6).
- Next feature per Rule A5: F105 — Cache-optimal prompt ordering, in a fresh
  session, after PR #188 is merged.

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
