# Plan — Steps 4446-4495: Promotion Exactness Closure v2

## Goal
Block unexpected artifacts, enforce exact reviewed artifact set,
normalize paths, bind promotion target to original run repo.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- Unexpected artifact check: manifest entries not in staged_files block
- Duplicate artifact check: same normalized path appearing twice blocks
- Path normalization: _normalize_rel_path strips ./ prefix, backslash, trailing /
- Repo binding: resolved run_data.repo_path must match resolved --repo target
- Missing run repo_path blocks legacy runs (no silent promotion)
- repo_path added to export_pingpong_json for persistence in result.json
- New PromotionResult fields: unexpected_artifacts, duplicate_artifacts,
  run_repo, requested_target_repo, target_repo_mismatch
- export_promotion_json and summarize_promotion updated with new fields
- do_cmd.py report shows unexpected artifacts, duplicates, repo mismatch
- 70 promotion tests (26 new): unexpected artifact regression, extra code artifact,
  exact set promotes, missing still blocks, duplicate blocks, duplicate listed,
  path normalization (3), repo mismatch blocks, mismatch persisted, same repo resolves,
  missing repo_path blocks, empty repo_path blocks, dry-run exact no mutation,
  no-approve exact no mutation, approved new file, approved modify,
  hash still blocks, baseline still blocks, post-test runs, post-test fails,
  report unexpected, report repo mismatch
- Full suite: 7407 passed, 0 failed (1 pre-existing deselected)
- Fast lane: 571 passed
- Runtime lane: 4/4 suites passed
- Lint: all checks passed (ruff + mypy)
- Architecture guard: clean
- Dogfood smoke: 6/6 scenarios pass (run, dry-run, approved, JSON fields,
  repo mismatch, unexpected artifact injection)
- Job fulfillment: 109 passed
