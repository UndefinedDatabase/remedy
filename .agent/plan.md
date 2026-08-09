# Plan — F104 Hard budget enforcement

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 was merged at the Open PR Gate. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
Reviewed through R5: **R5 PASS at 549f2bac** (`LAST_REVIEWED_SHA = 549f2bac`).
R6 and R7 are both awaiting review. R-0222 through R-0226 are Done with
reviewer-authored resolution text. Next free ID: R-0228.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check is unchanged — prediction never replaces the backstop.

## Current Step
R7 — COMPLETE, awaiting review. Two things landed. (1) R-0227 was registered
first and then fixed: the F103 ledger read in `_cmd_job_budget` no longer
swallows its failure silently — it logs at ERROR with `exc_info=True` and
surfaces a `cost_read:` text line plus a `cost_read_error` JSON key, so a
broken read is no longer indistinguishable from a job nobody priced.
`spent`/`remaining`/`diagnostic` are unchanged.
(2) The integration gate ran per docs/agents/integration_gate.md, evidence in
`.agent/gate_f104_r7/`: branch exit 0 (16305 passed, 19 skipped, 121 s), base
exit 1 (16125 passed, 6 failed, 19 skipped, 123 s), **zero branch-only
failures**, six base-only ids all attributed by direct evidence to the
pre-existing R-0221 dist-mtime class with a controlled reproduction and
reversal. The base worktree and `tmp/base-gate` are removed. T001-T003 done.

## Next Steps
- R8 — closure per docs/roadmap/STATUS_closure_protocol.md, once the reviewer
  has gated R6 and R7. `docs/roadmap/STATUS.md` still carries F104 as `[~]`;
  the STATUS line is the reviewer's to author at R8.

## Risks
- Cost is NULLABLE by design (P6): the ledger stores NULL for an unpriced call
  and nothing may render that as a measured zero. Every figure keeps the None.
- The band estimate is a FLOOR (DECISION F104 D6): it can only under-predict,
  which is why the reactive backstop must stay exactly as it is.
- R-0221 stays OPEN and unfixed by F104 — not this feature's code. It cost
  this gate six phantom base-only failures: attributed, not chased, and
  carried as a documented LOW risk to closure.
- `remedy job budget` now performs I/O the catalog marks `read_only`: a
  SELECT-only `query_cost` that never creates a ledger, pinned by
  `test_the_command_does_not_mutate_the_persisted_job`. The full suite saw it.
- The manifest budget schema is SHARED F012 surface. R5 widened it by exactly
  one field; any further budget field owes the same run-manifest gate
  (tests/orchestration/test_run_manifest*.py) before it is believed.
