# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 1 claims F279, re-heads the finding ledger, records DECISION F279 D1
with the feature file's T002 amendment, and lands T002: upper bounds on
`pydantic` and `psutil`, a generated hash-pinned `constraints.txt`, the
two-step pinned install in CI, and the guards that hold all of it.

## Next Steps

1. T001, the environment-variable registry: `env_registry.py` populated
   from the measured set, with the AST guard over every `REMEDY_` read.
2. T001's second half: `remedy doctor` reporting unknown and unparsable
   variables, and the generated `docs/guides/environment.md` with its
   drift test.
3. T003, `remedy block lint`, unless the operator has dropped it.
4. T004, the toolchain refresh order and `remedy doctor toolchain`.
5. The closure sequence, with the one full-suite run.

## Risks

`constraints.txt` is a generated file of about 650 lines, so its commit is
F279's one declared oversize commit under AGENTS.md. The developer's own
environment stays unpinned; T004 is the slice that reports its drift.
