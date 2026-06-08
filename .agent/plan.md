# Plan — Steps 795-809: Test Suite Triage

## Goal
Make test suite understandable and fast. Clear categories. Fast/integration/provider commands.

## Current Step
805-809 — Proof and handoff

## Steps
- [x] 795: Handoff — backend basis closed, focus on test triage
- [x] 796: 9 pytest markers in pyproject.toml
- [x] 797: Auto-marking via tests/conftest.py (no per-file decorators)
- [x] 798: remedy_test_fast.sh — excludes subprocess/ollama/ui/smoke (~2820 tests, ~34s)
- [x] 799: remedy_test_integration.sh — smokes + full minus ollama/slow
- [x] 800: remedy_test_real_providers.sh — opt-in via REMEDY_RUN_REAL_OLLAMA=1
- [x] 801: test_test_categories.py — 10 enforcement tests
- [x] 802: test_autorun.py checked — no subprocess, no split needed
- [x] 803: tests/README.md rewritten with commands and marker table
- [ ] 804: Context update
- [ ] 805: Run fast command
- [ ] 806: Run integration command
- [ ] 807: Optional full pytest
- [ ] 808: Next block recommendation
- [ ] 809: Final handoff
