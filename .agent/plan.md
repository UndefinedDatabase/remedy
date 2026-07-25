# Plan — F014 Flight Plan

## Goal
LLM-generated, schema-validated Flight Plan (DAG of tasks with
goals, acceptance, depends_on, token bands) carrying budgets and
fences; rendered plan.md; human approval gate before execution;
deterministic planner stays as --no-llm/provider-down fallback.

## Checklist
- [ ] T001 — schemas + DAG validator + tests + deprecation notes
- [ ] T002 — plan_job_llm + task mapping + budget/fence
      precedence + fake-provider tests
- [ ] T003 — plan.md renderer (golden file) + replan versioning
- [ ] T004 — approval gate + --yes audit + execution refusal +
      golden-path label flip + smoke update

## Current Step
T001 in progress.
