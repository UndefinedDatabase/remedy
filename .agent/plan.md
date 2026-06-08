# Plan — Steps 905-924: remedy do v1 Cohesive Flow

## Goal
Build `remedy do "prompt" --repo . --autonomy-level 3 --json` as cohesive phased flow.

## Current Step
924 — Final handoff

## Steps
- [x] 905: Handoff setup
- [x] 906-907: Run phase model + result contract (do_run.py)
- [x] 908: CLI wiring (catalog + do_cmd.py update)
- [x] 909-915: Flow phases (init/plan/context/build/intent/approval/proof)
- [x] 916-918: Continue placeholder + run contract + events
- [x] 919: Runtime subprocess tests (tests/cli/test_do_runtime.py — 10 tests)
- [x] 920-921: Safety + alignment tests (tests/orchestration/test_do_run.py — 34 tests)
- [x] 922: Docs (docs/do-run-v1.md)
- [x] 923: Targeted + fast lane tests (44 new pass, 778 total pass, 1 pre-existing fail)
- [x] 924: Final handoff — commit, push, PR

## Pre-existing Issue
`test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.
