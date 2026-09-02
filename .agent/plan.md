# Plan — amend0902-ollama-pingpong

Branch: feature/amend0902-ollama-pingpong, cut from `main` at
`269b5b84` (F108 merge). Operator amendment, boundary-agnostic.

## Goal

Make `role_config.DEFAULT_PROVIDER = "ollama"` constructible and callable on
the ping-pong job path, resolving finding R-0761. Scope is the factory branch
plus the adapter it returns — quality fallback and per-role local routing are
F113 and stay out.

## Current Step

C6 — Part 4 battery, PR, hosted CI, merge. Parts 1-3 are done: the fix and
its 17 tests landed (C1-C3), the real-path proof ran (job `48a379ab5ca44ec5`,
six real ollama provider calls, past `provider_unavailable`), and the record
carries `Done: R-0761` plus the two adjacent gaps it surfaced.

## Next Steps

- C6: run the Part 4 battery (tests/docs/ 295, golden path 42, the provider
  and ping-pong suites, ruff on every changed file), open the PR, wait for the
  HOSTED run to go green, merge it, confirm zero open PRs.

## Risks

- The shipped queue is EXHAUSTED — every item is `consumed_by` a closed
  feature, SU-004 by the F108 closure this session merged at Part 0 — so the
  real-path run pointed `queue_path` at a scratch copy of the real queue with
  SU-004's `consumed_by` cleared. Declared in the `Done: R-0761` text; the real
  queue's sha256 is recorded unchanged before and after.
- R-0767 and R-0768 are registered, not fixed: both sit in the CLI layer,
  outside this amendment's stated scope.
