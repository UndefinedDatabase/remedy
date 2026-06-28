# Plan — Steps 5141-5170: Review Zip Current-Run Contract + Worker/Remedy Starter Prep v1

## Goal
Fix R-4315..R-4320. Make review zip current-run-centered, generate valid JSON
manifest via Python, add command transcript, fix artifact ref sanitization,
add Worker/Remedy starter docs.

## Current Step
Step 5170: Verification complete. Committing and creating PR.

## Completed
- R-4315: Command transcript persisted with safe fields + repo hashes
- R-4316: Python manifest builder (always-valid JSON, bundle v7)
- R-4317: Review zip rewritten for current-run contract (evidence/current/ prefix)
- R-4318: All observability artifacts verified present after persist
- R-4319: Sanitizer preserves artifact names (prefix-only replacement)
- R-4320: Worker/Remedy starter script (scripts/remedy_self_job_flow.sh)
- Detritus check moved before manifest build in make_review_zip.sh
- Tests: 340 focused tests pass, 8255+ full suite pass (1 pre-existing failure)

## Constraints
No auto-approval, no target mutation, no git ops, no UI mutation,
no external providers, no fake events, no hiding missing data, no MemPalace.
