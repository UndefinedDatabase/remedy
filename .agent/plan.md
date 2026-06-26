# Plan — Steps 4927-4936: Job Evidence Symlink Containment Closure v2

## Goal
Close symlink escape vulnerability in nested task evidence paths.

## Current Step
All steps complete. Awaiting 5-minute quiet window.

## Steps
- Step 4927: Fix _task_evidence_dir to use _validate_output_path (resolve follows symlinks)
- Step 4928: Verify all nested writes use resolved-contained task dirs
- Step 4929: Unavailable-evidence symlink escape regression test
- Step 4930: Run_id-evidence symlink escape regression test
- Step 4931: Symlink file mapping containment tests
- Step 4932: Preserve malicious task ID traversal tests
- Step 4933: Preserve normal job evidence behavior
- Step 4934: Preserve redaction and read-only guarantees
- Step 4935: Preserve existing job and orchestration safety
- Step 4936: Final architecture guard and handoff
