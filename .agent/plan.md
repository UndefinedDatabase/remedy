# Plan — Steps 3216-3275: First Perfect Job Demo + Core Truth Closure v0

## Goal
Fix `do` vs `do run` command shape mismatch, enrich `job status` and `job report`
with artifact/patch_intent/approval truth, create first demo guide, investigate
runtime nested-lock, add comprehensive tests.

## Current Step
Running test lanes (fast + runtime). All code changes complete.

## Completed
- Steps 3216-3220: Gate + baselines captured
- Steps 3221-3224: Fixed Happy Path `do "<goal>"` → `do run "<goal>"` in help + all docs
- Steps 3225-3228: Added `_extract_job_truth()` helper, enriched `_cmd_job_status` and `_cmd_job_report`
- Steps 3229-3237: Added 14 new tests (truth extraction, truth fields, no-provider/no-apply proofs, help alignment)
- Steps 3238-3244: Created demo guide (`docs/first-perfect-job-demo-v0.md`), all docs updated
- Steps 3245-3249: Runtime nested-lock investigation — no issue found (sequential lock, no nesting)
- Steps 3250-3260: Running test lanes

## Next Steps
- Complete test lanes
- Self-review, lint, commit
- PR + handoff

## Risks
- Hook revert pattern: all file edits must use `python3 pathlib.write_text()`
