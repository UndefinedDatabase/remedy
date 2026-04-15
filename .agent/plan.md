# Plan

## Goal
Step 1.5: Foundation Hardening — strengthen core contracts and models so Step 2 can be built without immediate breaking changes.

## Current Step
In progress: applying hardening changes to models, interfaces, docs.

## Next Steps
1. Improve LLMWorker: task-oriented interface
2. Tighten Verifier: use AcceptanceCheck instead of list[Any]
3. Clarify architecture boundaries in docs/architecture.md
4. Update README.md
5. Update tests to cover hardened interfaces
6. Push, create PR

## Risks
- contracts/interfaces.py will import from core/models.py — intentional and acceptable.
