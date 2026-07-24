# Plan — F013 Job intake

## Goal
A free-text mission becomes a structured, validated JobIntake —
goal, context refs, constraints, acceptance hints, clarifications —
persisted on the job before planning. Schema-gated, never raw LLM
text; deterministic labeled heuristic fallback without a provider.

## Checklist
- [ ] T001 — JobIntake schema + validation round-trip tests + job
      field + backward-compat fixture
- [ ] T002 — intake module + prompt builder + shared single-shot
      call + fake-provider tests
- [ ] T003 — do-path integration + job show rendering + golden-path
      smoke update

## Current Step
T001.
