# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. Build mode: one-session self-drive,
one delegated worker per round. Next finding ID: R-0239.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and reviewer-gated, and R11 landed T003 SITE 1's
composition move under `tests/orchestration/test_intake_prompt_golden.py`. R12
completes site 1 by putting its manifest into call evidence and settles the
schema tail as DECISION F105 D3: the manifest covers the composed BASE prompt,
and `segment_manifest_chars` beside `prompt_chars` makes that coverage visible
instead of implied; D3's ledger entry lands at R13. Open findings: R-0221
(carried) and R-0238. No PR exists; one is created at CLOSURE.

## Next Steps
- Sites 2-6 in `.agent/t003_inventory.md`'s order, ONE builder per round, each
  with its golden.
- Then T004, the `remedy stats cache` view over actuals, reporting "not
  reported" rather than zeros where a provider reports no cache figures.
- Then the integration gate (docs/agents/integration_gate.md), then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- Sites 3, 5 and 6 reach no call evidence today; each must thread `on_call` from
  its CLI caller before a manifest can land anywhere.
- Sites 5 and 6 interpolate caps and repo facts into their rules blocks, so
  those segments are not byte-stable per role without a split.
- R-0221 stays open and will cost the F105 integration gate phantom base-only
  failures.
