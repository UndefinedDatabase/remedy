# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 2 books round 1's PASS, records DECISION F279 D2 with the feature
file's T001 amendment, and lands T001's registry half: the fifteen
`REMEDY_` names production code spelled without a spec are registered as
env-only keys in `packages/orchestration/config.py`, and
`tests/orchestration/test_env_registry.py` holds every name to the registry.
T002 landed in round 1.

## Next Steps

1. T001's doctor and docs half: `remedy doctor core` names an unknown
   `REMEDY_*` variable with its closest registered match and a registered
   one whose value does not parse; a generated `docs/guides/environment.md`
   with its drift test and its `docs/README.md` index line.
2. T001's reader half: the direct `REMEDY_` reads move onto one registry
   reader, so each type and default lives in its spec alone.
3. T003, `remedy block lint`, unless the operator has dropped it.
4. T004, the toolchain refresh order and `remedy doctor toolchain`.
5. The closure sequence, with the one full-suite run.

## Risks

`constraints.txt` (round 1) is F279's one declared oversize commit; no
second may follow. Hosted CI first runs the new install steps at the
closure's pull request.
