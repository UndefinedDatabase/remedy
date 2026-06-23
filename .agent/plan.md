# Plan — Steps 3916-3995: Real Claude Builder/Reviewer Ping-Pong v0

## Goal
Build the core ping-pong Builder ↔ Reviewer loop: one task in, staged
result out, with real Claude provider path and fake provider for tests.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- pingpong_provider.py: FakeProvider + ClaudeProvider + provider protocol
- pingpong_loop.py: Core ping-pong orchestrator with staging, context, prompts
- Context pack v0: safe bounded repo context (no .env, no secrets, capped)
- CLI wired: remedy do run --builder fake --reviewer fake --max-rounds 3 --mode staged
- 33 E2E tests covering all 17 required test cases
- Fulfillment wrapper: 109 passed × 2 runs
- Runtime lane: 4/4 suites
- Fast lane: 571 passed
- Full suite: 7213 passed, 0 failed, 8 skipped
- Lint: ruff clean, mypy clean (196 files)
- Architecture guard: clean (0 violations across 13 categories)
- No stale processes, lock not held

## Risks
- Real Claude smoke not run (ANTHROPIC_API_KEY not configured in this env)
