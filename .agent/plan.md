# Plan — Steps 725-734: Runtime Tests Process-Isolated

## Goal
Make runtime CLI tests process-isolated so pytest exits cleanly.

## Current Step
734 — Final handoff (complete)

## Steps
- [x] 725: Correct handoff — pytest exit contamination from many subprocess calls
- [x] 726: Standalone smoke script (scripts/remedy_runtime_cli_smoke.py)
- [x] 727: Propose/worker test files → thin wrappers (1 test each, 1 subprocess)
- [x] 728: Runtime helper unit tests kept separate (test_runtime_helpers.py)
- [x] 729: Smoke runs standalone script + thin pytest tests
- [x] 730: Propose runtime — 1 passed, 0.71s, clean exit
- [x] 731: Worker runtime — 1 passed, 0.87s, clean exit
- [x] 732: Smoke — standalone PASS + 168 pytest passed, 2.86s, clean exit
- [x] 733: Completion table — runtime 100% after proof
- [x] 734: Final handoff
