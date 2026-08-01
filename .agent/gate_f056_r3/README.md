# F056 R3 — integration gate evidence

Procedure: docs/agents/integration_gate.md. Worker records only; the
reviewer issues the gate verdict.

| Run | Command | Result | Exit | Wall |
|---|---|---|---|---|
| Branch @ c66b9695 | `python3 -m pytest -n auto -q` | 14744 passed, 19 skipped | 0 | 146s |
| Base @ 78f5f608, run 1 | same, `REMEDY_UI_NO_AUTO_BUILD=1` | 8 failed, 14602 passed, 19 skipped | 1 | 151s |
| Base @ 78f5f608, run 2 | identical command and environment | 14610 passed, 19 skipped | 0 | 115s |

Base ran in a throwaway worktree on throwaway branch `tmp/base-gate-f056r3`
at the merge base, with build-artifact parity restored by COPYING (never
symlinking) `apps/ui/node_modules` and `apps/ui/dist` from the primary
checkout. Worktree removed, pruned, branch deleted.

- `branch_failed.txt` — empty (no failures on the branch).
- `base_failed.txt` — run 1's 8 ids. `base_failed_run2.txt` — empty.
- `branch_only.txt` = `comm -13` — EMPTY: the branch introduces no failure.
- `base_only.txt` = `comm -23` against run 1 — the 8 ids below.

## Attribution of every `comm -23` id

All 8 are the same class and the same file
(`tests/ui_server/test_live_state.py::TestUIServerIntegration`):
`test_server_starts_and_writes_info`, `test_api_requires_token`,
`test_app_shell_served_without_token`, `test_api_missing_job_404`,
`test_put_rejected`, `test_dashboard_no_raw_leaks`, `test_brain_endpoint`,
`test_readiness_endpoint`.

Direct evidence (`base_run1_error_evidence.txt`): each failed as
"Server did not start in time" with captured stderr
`ERROR: React UI not built.` — the UI build-artifact class named in
integration_gate.md §3, artifact `apps/ui/dist`.

Three checks, all in the base worktree with parity in place:

1. serial re-run of that class — 16 passed in 1.87s;
2. same class under `-n auto` in isolation — 260 passed in 3.48s;
3. the FULL base suite re-run, identical command and environment —
   14610 passed, exit 0, zero failures (`base_failed_run2.txt`).

So the 8 are transient and non-reproducible, confined to the first
full-suite run in the freshly created worktree (immediately after the
312 MB artifact copy). They are environment/parity-class, not genuine
base failures, and they touch no F056 code.

Against the reproducible base result (run 2) both comparisons are empty:
`comm -13` = none, `comm -23` = none.

Flake debt: branch-only failures = 0, so the >10 threshold in the block
does not apply.
