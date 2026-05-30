# Plan — Steps 122-126

## Goal
Job-focused origin fix, view-model hardening, worker unload schema, autocoder calc.py fixture, smoke closure.

## Current Step
All steps complete. Final review and commit.

## Steps
- [x] Step 122: Job-focused origin — only focus_job_id gets is_origin=true, child jobs demoted to zoom>=5, flow_role="continuation"
- [x] Step 123: View-model hardening — 39 behavioral tests covering all field contracts, zoom/subset monotonicity, version=4
- [x] Step 124: Worker unload JSON — flat stopped/skipped/errors/unavailable fields, unavailable=true when ollama missing
- [x] Step 125: Autocoder calc.py fixture — calc.py + tests/test_calc.py + Makefile, --no-ui flag in catalog/do_cmd
- [x] Step 126: Smoke closure — brain-view-model origin check, version 4 check, REMEDY_SMOKE_UNLOAD_MODELS section

## Tests
- 39 new tests in test_steps_122_126.py
- 3141 total tests passing
