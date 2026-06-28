# Plan — Steps 5231-5260: Valid Latest Evidence Selection + Reviewer-Ready Bundle Gate v1

## Goal
Implement strict evidence candidate validation, reviewer-ready bundle gate,
manifest validation section, path sanitizer hardening, and comprehensive tests.

## Current Step
Step 5231: Add evidence validation to build_review_manifest.py

## Next Steps
- Step 5232: Update make_review_zip.sh with strict validation + candidate table
- Step 5233: Add --allow-incomplete-evidence flag for explicit override
- Step 5234: Harden path sanitizer for .data/job_workspaces and /mnt paths
- Step 5235: Add comprehensive tests
- Step 5236: Full verification + handoff

## Constraints
No auto-approval, no target mutation, no git ops, no UI mutation,
no filename pattern changes, no external providers.
