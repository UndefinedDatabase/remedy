---
name: remedy-test-triage
description: Use for selecting safe Remedy test commands, pytest wrappers, smoke scripts, and fast-lane validation.
---

# Remedy Test Triage

## Rules
- Read `AGENTS.md` before planning or running validation.
- Use `scripts/remedy_pytest.sh` for targeted pytest.
- Use `scripts/remedy_test_fast.sh` only after targeted tests pass when broad fast validation is needed.
- Use smoke scripts only for smoke/runtime scope.
- Do not run background pytest.
- Do not run direct pytest.

## Selection
1. Run tests nearest changed code.
2. Add CLI tests when command output changes.
3. Add security/config tests for tooling and MCP changes.
4. Report full pytest as run/not run.
