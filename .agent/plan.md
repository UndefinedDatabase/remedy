# Plan — Steps 4807-4811: Run Evidence Bundle v0

## Goal
Export a self-contained, safe proof bundle for any Remedy run.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- Step 4807: Evidence bundle builder (pingpong_evidence.py)
- Step 4808: CLI command `remedy do evidence <run_id> --out <dir> --json`
- Step 4809: Redaction rules (API keys, env vars, staging paths, path traversal)
- Step 4810: 35 tests covering bundle, CLI, redaction, safety
- Step 4811: Architecture guard clean, full suite 7712 passed
- Lint: ruff clean, mypy clean
- No provider calls, no target mutation, no task body dump
