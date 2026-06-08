---
description: Use for Remedy test selection, pytest wrappers, smoke scripts, and safe validation planning.
---

# Remedy Test Triage Skill

## Rules
- Read `AGENTS.md` before planning or running validation.
- Use `scripts/remedy_pytest.sh` for targeted pytest.
- Use `scripts/remedy_test_fast.sh` for fast broad checks.
- Use smoke scripts only when scope requires runtime/smoke validation.
- Do not run direct `pytest`, `python -m pytest`, or background pytest.
- Do not run tests in parallel unless the wrapper or script explicitly does it safely.

## Selection pattern
1. Start with tests nearest the changed files.
2. Add CLI tests when output contracts change.
3. Add security/config tests when agent tooling, MCP, or settings change.
4. Run the fast lane only after targeted tests pass and time allows.

## Reporting
Report exact wrapper commands and whether full pytest was not run.
