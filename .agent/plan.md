# Plan — F013 Job intake

## Goal
A free-text mission becomes a structured, validated JobIntake —
goal, context refs, constraints, acceptance hints, clarifications —
persisted on the job before planning. Schema-gated, never raw LLM
text; deterministic labeled heuristic fallback without a provider.

## Checklist
- [x] T001 — JobIntake schema + validation round-trip tests + job
      field + backward-compat fixture
- [x] T002 — intake module (run_intake + heuristic_intake) using
      run_structured_call + fake-provider tests (31 tests)
- [x] T003 — do-path integration (intake before planning, --no-llm
      flag) + job show rendering + golden-path smoke (36 tests)

- [x] R-0110..R-0117 — reviewer repairs
- [x] Closure — verdict PASS_WITH_RISKS, evidence job,
      STATUS [x], PR

## Current Step
Closure complete.
