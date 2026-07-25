# Plan — F014 Flight Plan

## Goal
LLM-generated, schema-validated Flight Plan (DAG of tasks with
goals, acceptance, depends_on, token bands) carrying budgets and
fences; rendered plan.md; human approval gate before execution;
deterministic planner stays as --no-llm/provider-down fallback.

## Checklist
- [x] T001 — schemas + DAG validator + tests + deprecation notes
- [x] T002 — plan_job_llm + task mapping + budget/fence
      precedence + fake-provider tests
- [x] T003 — plan.md renderer (golden file) + replan versioning
- [x] T004 — approval gate + golden-path label flip + smoke update

## Current Step
All tasks complete. Ready for PR.
