# Plan — Tiered Verification Gates (operator decision 2026-07-26)

## Goal
Encode tiered verification gates in the planner/reviewer protocol and set
up pytest-xdist for full-suite runs.

## Checklist
- [x] F014 closure PR #148 merged via Open PR Gate
- [x] planner_reviewer_prompt.md §3: verification tiers (round gate scoped
      only · golden-path canary per handback · full suite 2× per feature ·
      xdist + ~5 min budget note)
- [x] planner_reviewer_prompt.md §4.6: verdict semantics (round PASS =
      scoped green + clean diff; only integration gate claims full green)
- [x] STATUS_closure_protocol.md precondition 2: integration-gate round
      reference
- [x] pyproject dev deps: pytest-xdist; markers slow/integration existed
- [x] Verified: canary 42 passed in ~19 s; full suite `-n auto` 3m11s

## Current Step
Commit + PR.

## Risks
- Full suite currently RED on main: 159 failed / 13827 passed (spot-check
  serial: pre-existing, e.g. dev_server missing `_ABS_PATH_RE`). Expected
  target of the first integration-gate round; out of scope here.
