# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 6 books round 5's PASS, records DECISION F279 D6, and lands T004's
report half: `remedy doctor toolchain` shows each pinned tool's installed,
pinned and newest version, and a test holds the CI matrix to exactly two
Python versions. T001, T002 and T003 are complete.

## Next Steps

1. T004's order half: `docs/orders/toolchain-refresh.md`, a docs test
   pinning its section headings, and the self-use generator minting an item
   from it no more than once every 14 days.
2. The closure sequence, with the one full-suite run.

## Risks

`constraints.txt` (round 1) is F279's one declared oversize commit; no
second may follow. Hosted CI first runs the new install steps at the
closure's pull request. Under `pytest -n 6` in a fresh worktree the UI
server tests fail at the base as well; serially they pass.
