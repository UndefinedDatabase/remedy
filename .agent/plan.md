# Plan — Steps 4820-4826: Evidence CLI JSON Redaction Closure v2

## Goal
Fix CLI --json stdout leaking secrets from export_evidence return payload.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- Step 4820: export_evidence() return wrapped in _redact_json_value()
- Step 4821: CLI handler inherits redaction from export_evidence (no separate fix needed)
- Step 4822: CLI stdout JSON leak regression test
- Step 4823: Export return-value regression tests (3 tests)
- Step 4824: Extended full-output scanner (files + API return)
- Step 4825: All existing tests preserved — 65 evidence, 131 repair, 109×2 job fulfillment
- Step 4826: Architecture guard clean, full suite 7742 passed
- Lint: ruff clean, mypy clean
