# Plan — Gap: short-ID resolver + protocol + hygiene

## Goal
Central short-ID resolver, completion-report protocol, hygiene fixes.

## Checklist
- [ ] Central `resolve_job_id` in data_paths.py
- [ ] Wire into all 22+ command sites (job, decision, change, patch)
- [ ] Delete duplicate resolvers (job_stop_cmd, project)
- [ ] Tests: short-ID resolution + verbatim Next-line
- [ ] AGENTS.md: item-status-table rule in completion reports
- [ ] Hygiene: 2 job_stop_integration failures + ruff --fix

## Current Step
Central resolver function.
