# Plan — F306 Findings paydown v8

## Goal
Pay down the four findings open at the claim — R-1235, R-1246, R-1251 and R-1252 — each by the
repair its own text names, after the structural steps the structure ledger owes for the files they
touch, or carry it by name to the next paydown (docs/roadmap/features/T2_F306.md; DECISION F306 D1).

## Current Step
Round 3 on `feature/f306-findings-paydown-v8`, session 1: book round 2 and R-1251's resolution,
then T004, the first step of `run_manifest.py`: the probes, the workspace identity record and the
verified read of untracked files move to `packages/orchestration/workspace_identity.py`; the git
reads tests replace on `run_manifest` stay there with their callers.

## Next Steps
1. T005 — R-1252: a run that splits a task writes the run manifest.
2. T006 to T008 — R-1235's three steps.
3. The closure, carrying R-1246 by name to the next paydown.

## Risks
- A name a test replaces on `run_manifest` must stay there with every function that calls it.
- R-1252 reaches the manifest's validation, which requires every call's task in the frozen task
  list, so its repair may need a decision on how a split is recorded.
