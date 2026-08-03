# Integration gate evidence — F070 R2

Run of `docs/agents/integration_gate.md` in its HARDENED form (the R-0169
amendments applied earlier this round: `.txt` evidence names only, and the
dist/ hash-before/after verification of the UI auto-build neutralization).
This is that hardening's first live use.

Range: merge base `afbe2639` .. branch head `7fcc3ebc`
(`feature/f070-orchestrator-loop`).

**No verdict is written here.** Only the reviewer issues the gate verdict.

## Result

| Run | Command | Passed | Failed | Exit | Wall |
|---|---|---|---|---|---|
| Branch | `scripts/remedy_pytest_runner.py -n auto -q` | 15274 | 0 | 0 | 161.71s |
| Base   | same, in a throwaway worktree at `afbe2639` | 15094 | 0 | 0 | 184.70s |

`comm -13` (branch-only failures): **empty**.
`comm -23` (failures the branch fixed / base-only): **empty**.
Both failure sets are empty, so there is nothing to attribute per id.

The 180-test delta (15274 − 15094) is this round's additions: the F070 loop,
era-corpus, e2e and CLI tests.

## R-0169 neutralization check (new this round)

`apps/ui/node_modules` and `apps/ui/dist` were COPIED into the base worktree
(never symlinked), `REMEDY_UI_NO_AUTO_BUILD=1` was set for the base run, and
the dist/ tree was hashed before and after it:

    before  5ff2033ab95c45d2802cbe7d9977605abbe009a916236a43aab30f97954ba092
    after   5ff2033ab95c45d2802cbe7d9977605abbe009a916236a43aab30f97954ba092

UNCHANGED — the neutralization held on this run and the parity claim stands.
This is exactly the check F069 R2 lacked when a spawned build path rewrote
dist/ mid-run.

## Suite nondeterminism observed (recorded, not a gate finding)

The SCOPED `tests/orchestration/` slice gate went red twice during Phase D,
with a DIFFERENT failing set each time, all inside
`tests/orchestration/test_product_smoke.py` (port-binding smoke tests):

    run 1  3 failed  TestAppStartsGreen::test_a_clean_app_passes,
                     TestAppStartsGreen::test_the_app_is_always_stopped,
                     TestRetryAndPortConflict::test_a_flaky_start_passes_on_retry_and_says_so
    run 2  1 failed  TestCorePathsRun::test_ok_paths_pass   (run 1's three passed)

Serial re-run of that whole file: 76 passed, exit 0. The full-suite branch run
above: 0 failed. Churning ids that pass serially are the xdist-flake class
(integration_gate.md step 4; F135/F052 backlog; the same pre-existing
nondeterminism the F016 verdict recorded). No F070 file is involved — the
branch touches none of `test_product_smoke.py` or the product-smoke code.

## Files

| File | What |
|---|---|
| `merge_base.txt` | merge base + branch head |
| `branch_run.txt` / `branch_exit.txt` | branch full-suite run, raw + exit code |
| `base_run.txt` / `base_exit.txt` | base full-suite run, raw + exit code |
| `branch_failed.txt` / `base_failed.txt` | sorted FAILED lists (both empty) |
| `branch_only.txt` / `base_only.txt` | `comm -13` / `comm -23` (both empty) |
| `dist_hash_before.txt` / `dist_hash_after.txt` | R-0169 dist/ hashes |
| `dist_parity_verdict.txt` | the before/after comparison result |
| `scoped_slice_run1.txt` / `scoped_slice_run2.txt` | the two red scoped-slice runs |
| `product_smoke_serial.txt` | serial re-run of the churning file (76 passed) |
| `worktree_teardown.txt` | `git worktree list` after removal + prune |
| `README.md` | this file |

Teardown: worktree removed and pruned, `tmp/base-gate-f070` deleted, the
primary checkout is the only entry in `worktree_teardown.txt`.
