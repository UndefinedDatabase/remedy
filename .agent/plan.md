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
(R-0241). Migration-order steps 1 (`intake.py`), 2 (`mission_compiler.py`),
3 (`flight_plan.py`) and 4 (`orchestrator_loop.py`) are COMPLETE, each with its
own golden; step 4 covers `build_orchestrator_prompt` AND its system half
`build_orchestrator_system_prompt`, and is the only one so far whose golden
asserts BYTE equality rather than equality modulo ordering, because its
pre-migration order was already rank-ordered (R-0249). `LAST_REVIEWED_SHA` is
04a3396d; R20 is ungated. Open findings: R-0221, R-0239, R-0246, R-0247,
R-0249. No PR; one is created at CLOSURE.

## Next Steps

- The next round gates R20 FIRST, then takes migration-order step 5,
  `pingpong_loop.py::_build_builder_prompt` — twelve conditional parts and a
  `"\n".join` whose blank-line runs must be reproduced exactly.
- Then step 6, `pingpong_loop.py::_build_reviewer_prompt`, last and highest
  content-equality risk. One builder per round, each with its own golden.
- BEFORE step 5, decide whether the schema tail from `build_schema_prompt` /
  `native_schema_prompt` becomes a registered rank-4 segment. Until that is
  settled, every manifest for sites 1-4 describes a strict prefix of the bytes
  actually sent.
- ONE later round wires `on_call` for all three sites that lack call evidence —
  `mission_cmd.py:362` (orchestrator, deferred by R20's block),
  `mission_cmd.py:187` + `gauntlet_runner.py:505` (mission), and
  `do_cmd.py:253` + `:2860` (plan) — one recorder pattern, one review.
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Register the Phase-0 gap the R17 gate records: the protocol gives no
  disposition for a tree a dead session left dirty. Not yet a DECISION.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks

- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- Four of the six migrated builders still reach no call evidence, so F105's
  every-role acceptance line is met for intake only until that round lands.
