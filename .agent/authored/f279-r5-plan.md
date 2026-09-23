# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 5 books round 4's PASS, records DECISION F279 D5 with the feature
file's amendment, and lands T003: `remedy integrity block <path>` lints a
step block against items 1, 3, 10, 24, 30, 31 and 37 of the reviewer's
checklist, and a guard holds every rule to a live item and to a sentence
that item contains. T001 and T002 are complete.

## Next Steps

1. T004, the toolchain refresh order and `remedy doctor toolchain`.
2. The closure sequence, with the one full-suite run.

## Risks

`constraints.txt` (round 1) is F279's one declared oversize commit; no
second may follow. Hosted CI first runs the new install steps at the
closure's pull request. Under `pytest -n 6` in a fresh worktree the UI
server tests fail at the base as well; serially they pass.
