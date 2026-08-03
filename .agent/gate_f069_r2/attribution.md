# comm -23 attribution — every base-only id, by direct evidence

Class: ENVIRONMENT (UI build artifact in the throwaway base worktree).
integration_gate.md §3 names this class: the base worktree lacks
apps/ui/dist. Parity was attempted per the doc (cp -a, never symlink)
plus REMEDY_UI_NO_AUTO_BUILD=1.

## Direct evidence 1 — the base run named the artifact itself (stderr):
ERROR: React UI not built.

  To fix, run:
    cd apps/ui && npm install && npm run build

  Or check npm is installed and retry.
  Disable auto-build: REMEDY_UI_NO_AUTO_BUILD=1
ERROR: React UI not built.

## Direct evidence 2 — dist state in the base worktree after the run:
total 16
drwxrwxr-x 3 decodeux decodeux 4096 Aug  3 09:05 .
drwxrwxr-x 6 decodeux decodeux 4096 Aug  3 09:05 ..
drwxrwxr-x 2 decodeux decodeux 4096 Aug  3 09:05 assets
-rw-rw-r-- 1 decodeux decodeux  414 Aug  3 09:05 index.html

  Note: index.html carries a mtime LATER than the copy (09:05 vs 09:03).
  A UI auto-build ran inside the base worktree during the run and
  rewrote dist while workers were reading it — the same auto-build
  hazard recorded for F053 R3 in .agent/decisions.md (2026-07-31),
  there via a symlink, here contained to the worktree by the copy.

## Direct evidence 3 — re-run AT BASE with dist present: all pass
  $ cd <base worktree> && REMEDY_UI_NO_AUTO_BUILD=1 \
      python3 -m pytest tests/ui_server/test_live_state.py -q -p no:randomly
..........................................                               [100%]
42 passed in 1.96s
  exit_code=0 — the 8 ids below all pass at the merge base.

## Per-id attribution (all 8 comm -23 ids)
- tests/ui_server/test_live_state.py::TestUIServerIntegration::test_api_invalid_token_403
    missing artifact: apps/ui/dist/index.html (server refuses to start)
    passes at base once dist is present: YES (evidence 3)
- tests/ui_server/test_live_state.py::TestUIServerIntegration::test_api_valid_token_returns_dashboard
    missing artifact: apps/ui/dist/index.html (server refuses to start)
    passes at base once dist is present: YES (evidence 3)
- tests/ui_server/test_live_state.py::TestUIServerIntegration::test_brain_endpoint
    missing artifact: apps/ui/dist/index.html (server refuses to start)
    passes at base once dist is present: YES (evidence 3)
- tests/ui_server/test_live_state.py::TestUIServerIntegration::test_dashboard_no_raw_leaks
    missing artifact: apps/ui/dist/index.html (server refuses to start)
    passes at base once dist is present: YES (evidence 3)
- tests/ui_server/test_live_state.py::TestUIServerIntegration::test_put_rejected
    missing artifact: apps/ui/dist/index.html (server refuses to start)
    passes at base once dist is present: YES (evidence 3)
- tests/ui_server/test_live_state.py::TestUIServerIntegration::test_readiness_endpoint
    missing artifact: apps/ui/dist/index.html (server refuses to start)
    passes at base once dist is present: YES (evidence 3)
- tests/ui_server/test_live_state.py::TestUIServerIntegration::test_server_starts_and_writes_info
    missing artifact: apps/ui/dist/index.html (server refuses to start)
    passes at base once dist is present: YES (evidence 3)
- tests/ui_server/test_live_state.py::TestUIServerIntegration::test_url_is_localhost_only
    missing artifact: apps/ui/dist/index.html (server refuses to start)
    passes at base once dist is present: YES (evidence 3)

## comm -13 (branch-only failures): NONE (0 ids).
