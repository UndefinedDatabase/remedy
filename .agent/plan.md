# Plan — amend0902-ollama-pingpong

Branch: feature/amend0902-ollama-pingpong, cut from `main` at
`269b5b84` (F108 merge). Operator amendment, boundary-agnostic.

## Goal

Make `role_config.DEFAULT_PROVIDER = "ollama"` constructible and callable on
the ping-pong job path, resolving finding R-0761. Scope is the factory branch
plus the adapter it returns — quality fallback and per-role local routing are
F113 and stay out.

## Current Step

C4 — Part 4 battery, PR, hosted CI, merge.

## Next Steps

- C1: extract the builder file-list parser into one named helper (pure
  refactor, no behaviour change).
- C2: add `OllamaPingPongProvider` + the `"ollama"` factory branch; update the
  factory's error string.
- C3: hermetic tests (factory, default model, build + review round trip over a
  mocked ollama boundary, `provider_error:` prefix on transport failure) and
  the disposable-worktree red proof.
- C4: append `Done: R-0761` to `.agent/live_review.md`; run SU-004 through the
  real job path; operator note in `docs/roadmap/features/T3_F113.md`; battery,
  PR, hosted CI, merge.

## Risks

- The real SU-004 run may block on a NEW defect behind the old one. That is
  registered honestly as the next finding, never forced green.
