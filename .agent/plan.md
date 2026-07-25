# Plan — Gap: short-ID resolver + protocol + hygiene

## Goal
Central short-ID resolver, completion-report protocol, hygiene fixes.

## Checklist
- [x] Central `resolve_job_id` in data_paths.py
- [x] Wire into all 22+ command sites (job, decision, change, patch)
- [x] Delete duplicate resolvers (job_stop_cmd, project)
- [x] Tests: short-ID resolution + verbatim Next-line
- [x] AGENTS.md: item-status-table rule in completion reports
- [x] Hygiene: 2 job_stop_integration failures + ruff --fix

## Current Step
All items done. Commit hygiene, push, create PR.

## Notes
- Catalog/doc test failures (31 tests in test_product_spine + test_do_cmd_summary) are pre-existing on main — missing docs/autocoder-usage.md and docs/core-product-spine-v0.md.
- ruff 10 remaining violations all suppressed with noqa (E402 after bootstrap, F821 forward ref, F722 quirky annotation).
- job_stop_integration fix: runner now acknowledges pending stop signal when job already stopped with matching request_id (crash-at-step-6 recovery path).
