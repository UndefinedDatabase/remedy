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
R42 landed. T001, T002 and T003 are DONE and gated: every builder composes via
the registry and one composition now feeds both the provider and the trace at
all three CLI sites. R41 is GATED PASS; `LAST_REVIEWED_SHA` is 87ef21d9.
R-0256, R-0263 and R-0264 are RESOLVED with reviewer-authored `Done:` text.
Open findings: R-0221, R-0239, R-0247, R-0262.
T004 is the only slice left; `.agent/t004_inventory.md` is its ground truth.
No PR; one is created at CLOSURE.

## Next Steps
- T004 slice 1, scoped from the inventory: `remedy stats cache` over actuals,
  cache-read share per role, `unmeasured` and never `0` where no provider
  reported — the discipline `remedy stats cost` already applies.
- Then the before/after comparison note in the feature's evidence, with honest
  numbers whatever they are (the feature file's T004 line).
- Then the integration gate (docs/agents/integration_gate.md); R-0221 will
  attribute phantom base-only failures there and that is expected, not new.
- Then closure (docs/roadmap/STATUS_closure_protocol.md), where the evidence
  job, the FRESH review zip, the STATUS line and the PR all land.

## Risks
- T004 may find no join key between a trace's `role` and a ledger row. If so
  the honest first slice reports per-role only where the join exists and says
  "not reported" elsewhere — it never invents a role for a call.
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262 stays OPEN and out of scope: it needs the composition moved inside the
  `try` in `plan_job_llm` AND at the CLI sites, pinned by a raising composer.
