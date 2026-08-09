# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003 counts in the MIGRATION ORDER of
`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings
(R-0241). Migration-order steps 1-5 are COMPLETE and GATED, each with its own
golden; `LAST_REVIEWED_SHA` is b35d9d56. R23 is the session terminator: it
records the R22 gate, registers and fixes R-0251 and R-0252, and starts no
migration. Open findings: R-0221, R-0239, R-0246, R-0247. No PR; one is
created at CLOSURE.

## Next Steps
- R24 gates R23 (state, docs and one test file — a red-proof IS owed, on the
  new pin), then takes migration-order step 6,
  `pingpong_loop.py::_build_reviewer_prompt`, last of the six.
- Step 6 gets a FRESH session on purpose. Before authoring its block, prove the
  decomposition byte-exact in pre-migration order over every combination of its
  optional arguments, as R22 did for step 5 — that proof is what made step 5
  land without a repair round. Its two mutually exclusive branches and its
  three reviewer-role strings (base, effective, parse-retry) all reach
  evidence.
- ONE later round wires `on_call` for the three sites lacking call evidence:
  `mission_cmd.py:362` (orchestrator), `mission_cmd.py:187` +
  `gauntlet_runner.py:505` (mission), `do_cmd.py:253` + `:2860` (plan).
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The builder prompt's cacheable prefix now dies 24 characters into
  `builder_staged_state` (R22 gate H measured 467). T004's before/after number
  should quote that, not the rank order alone.
