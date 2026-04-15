# Plan

## Goal
Step 1.5: Foundation Hardening — strengthen core contracts and models so Step 2 can be built without immediate breaking changes.

## Current Step
In progress: applying hardening changes to models, interfaces, docs.

## Next Steps
1. Harden models: Task lifecycle + artifact linkage, Artifact provenance
2. Improve LLMWorker: task-oriented interface
3. Tighten Verifier: use AcceptanceCheck instead of list[Any]
4. Clarify architecture boundaries in docs/architecture.md
5. Update README.md
6. Update tests to cover hardened interfaces
7. Commit in small scoped steps, push, create PR

## Risks
- contracts/interfaces.py will import from core/models.py — intentional and acceptable.
