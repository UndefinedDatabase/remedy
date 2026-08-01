# Integration gate evidence — F062 R2

Procedure: `docs/agents/integration_gate.md`. Only the reviewer issues the
gate verdict; this directory is the worker's raw evidence for it.

- Branch: `feature/f062-product-smoke` @ `76042efe`
- Merge base: `b836d364` (`git merge-base HEAD main`)
- Date: 2026-08-01

## Runs

Identical command both sides: `python3 -m pytest -n auto -q`.

| side | result | wall | exit |
| --- | --- | --- | --- |
| branch @ `76042efe` | 14969 passed, 19 skipped | 136.39s | 0 |
| base @ `b836d364` | 14900 passed, 19 skipped | 165.15s | 0 |

The +69 test delta is exactly `tests/orchestration/test_product_smoke.py`:
the base predates F062 entirely and has none of them; the branch has all 69
(27 from R1, 42 added by R2's T002 and T003). No other test count moved.

## Comparison

Both failure sets are EMPTY, so both comparisons are empty:

- `branch_failed.txt` — 0 lines
- `base_failed.txt` — 0 lines
- `branch_only.txt` (`comm -13 base_failed.txt branch_failed.txt`) — 0 lines.
  **The branch introduces no failure**, so step 4's per-id attribution has
  nothing to attribute and no flake class arises.
- `base_only.txt` (`comm -23`) — 0 lines. No environment-class attribution is
  needed either: parity was restored BEFORE the base run rather than
  attributed after it, which is the first of the two options the gate doc
  allows.

## Base parity (R-0155 amendment / R-0158 path correction)

The throwaway worktree was created ON a throwaway branch
(`git worktree add -b tmp/f062-base-gate <path> b836d364`) — a detached HEAD
fails the self-dogfood branch guard by design (DECISION D3).

`apps/ui/node_modules` and `apps/ui/dist` were COPIED in from the primary
checkout — never symlinked, because the UI auto-build runs npm install and
writes THROUGH a symlink into the primary checkout (F053 R3 evidence). The
base run also carried `REMEDY_UI_NO_AUTO_BUILD=1`.

## Teardown

```
$ git worktree remove --force <path>
$ git worktree prune
$ git branch -D tmp/f062-base-gate
Deleted branch tmp/f062-base-gate (was b836d364).
$ git worktree list
/home/decodeux/Repos/remedy  76042efe [feature/f062-product-smoke]
```

Neither run crosses the gate doc's ~5 min note threshold.
