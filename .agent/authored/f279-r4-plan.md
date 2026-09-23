# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 4 books round 3's PASS, records DECISION F279 D4 with the feature
file's note, and lands T001's reader half: `env_value` in
`packages/orchestration/config.py` reads a registered variable from the live
environment as its declared type, the eleven typed reads move onto it, and a
guard keeps typed reads on it. T002 landed in round 1; T001's registry,
doctor and guide in rounds 2 and 3.

## Next Steps

1. T003, `remedy block lint`, unless the operator has dropped it.
2. T004, the toolchain refresh order and `remedy doctor toolchain`.
3. The closure sequence, with the one full-suite run.

## Risks

`constraints.txt` (round 1) is F279's one declared oversize commit; no
second may follow. Hosted CI first runs the new install steps at the
closure's pull request. Under `pytest -n 6` in a fresh worktree the UI
server tests show failures at the base as well; serially they pass.
