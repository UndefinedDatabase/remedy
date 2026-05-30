# Plan — Steps 111-116

## Goal
UI CLI contract fix, resource cleanup, semantic zoom v4, forward flow v3, task ribbon v2, autocoder E2E.

## Current Step
All steps complete. Final review and commit.

## Steps
- [x] Step 111: `remedy ui <job_id>` direct form (default-command rewrite in grouped.py)
- [x] Step 112: `worker resources` + `worker unload` commands (no shell=True)
- [x] Step 113: visible_node_ids_by_zoom, label_counts_by_zoom, subset monotonicity, wheel max level 5
- [x] Step 114: flow_role, lane, source_rank/target_rank/primary_path on edges, low-zoom edge filtering
- [x] Step 115: Task progress v2 with proof_status, test_status, is_current, is_future, is_reviewer_suggested
- [x] Step 116: Fixture builder E2E slice — source context, structured patch, apply, test, proof

## Tests
- 54 new tests in test_steps_111_116.py
- 3102 total tests passing
- Frontend builds clean (Vite)
