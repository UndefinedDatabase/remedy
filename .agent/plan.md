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
R41 landed. T001 and T002 are DONE and gated; T003's six migration sites are
all migrated. R40 is GATED PASS; `LAST_REVIEWED_SHA` is 7f622b7f. R-0256 and
R-0263 are FIXED and marked `Landed:`, awaiting the reviewer's `Done:` text at
the R41 gate: one composition now feeds both the provider and the trace at all
three CLI sites, pinned by two orchestration tests and one wiring guard.
Open findings: R-0221, R-0239, R-0247, R-0262, R-0264.
No PR; one is created at CLOSURE.

## Next Steps
- Await the R41 gate, which resolves R-0256, R-0263 and R-0264.
- Then T004: `remedy stats cache` over actuals — the cache-read share per role
  read from recorded calls, not from an estimate.
- Then the integration gate (docs/agents/integration_gate.md); R-0221 will
  attribute phantom base-only failures there and that is expected, not new.
- Then closure (docs/roadmap/STATUS_closure_protocol.md), where the evidence
  job, the FRESH review zip, the STATUS line and the PR all land.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262 stays OPEN and out of scope: it needs the composition moved inside the
  `try` in `plan_job_llm` AND at the CLI sites, pinned by a raising composer.
