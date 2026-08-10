# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
SESSION ENDED ON `.agent/STOP` at R47 — on the guardrail G6 signal, NOT at a
round cap and NOT on a failure. That file still exists, empty and untracked,
and was deliberately not removed. NO WORK MAY START in the next session while
it exists: per self_drive_protocol Phase 1 rule 1 the next session writes its
handoff and ends. The BRANCH stays open, F105 is NOT closed, no PR exists.
`LAST_REVIEWED_SHA` is aad00eee — R46 was GATED PASS this session and that
record sits in `.agent/live_review.md`. R47 itself carries a step line and NO
gate record, deliberately (the R-0264 distinction).
T001-T003 are DONE and T004's VIEW half is DONE: `remedy stats cache` renders
the human table, and `--json` emits the same share, the same two absence words
and the R-0266 per-role limit. `.agent/t004_inventory.md` stays T004's ground
truth. Open findings: R-0221, R-0239, R-0247, R-0262, R-0265, R-0266 and the
new R-0268 — seven, all OPEN by design, none touched this round.

## Next Steps
Nothing below may begin until the operator removes `.agent/STOP`.
1. The T004 before/after comparison note in the feature's evidence, with honest
   numbers whatever they turn out to be (the feature file's T004 line).
2. The integration gate per `docs/agents/integration_gate.md`; R-0221 will
   attribute phantom base-only failures there — expected, not new.
3. Closure per `docs/roadmap/STATUS_closure_protocol.md`, where the evidence
   job, the FRESH review zip, the STATUS line and the PR all land.
4. PR #189 (`docs/amend0810-clerical` -> `main`), which the OPERATOR must
   resolve before F105's closure PR is cut.

## Risks
- PR #189 is open and is NOT from a `feature/*` branch, so the Open PR Gate
  makes it stop-and-report. It blocks no work here, but it blocks closure.
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262, R-0265, R-0266 and R-0268 stay OPEN and out of scope for F105 by
  design; R-0268 belongs to the self-drive protocol, not prompt composition.
