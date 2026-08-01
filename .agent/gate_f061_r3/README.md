# Integration gate evidence — F061 R3

Procedure: `docs/agents/integration_gate.md`. Only the reviewer issues the
gate verdict; this directory is the worker's raw evidence for it.

- Branch: `feature/f061-dod-compiler` @ `aebc3c11`
- Merge base: `1869d89a` (`git merge-base HEAD main`)
- Date: 2026-08-01

## Runs

Identical command both sides: `python3 -m pytest -n auto -q`.

| side | result | wall | exit |
| --- | --- | --- | --- |
| branch @ `aebc3c11` | 14900 passed, 19 skipped | 140.76s | 0 |
| base @ `1869d89a` | 14744 passed, 19 skipped | 137.49s | 0 |

The +156 test delta is F061's own additions across R1–R3.

## Comparison

Both failure sets are EMPTY, so both comparisons are empty:

- `branch_failed.txt` — 0 lines
- `base_failed.txt` — 0 lines
- `branch_only.txt` (`comm -13 base_failed.txt branch_failed.txt`) — 0 lines.
  **The branch introduces no failure**, so step 4's per-id attribution has
  nothing to attribute.
- `base_only.txt` (`comm -23`) — 0 lines. No environment-class attribution is
  needed either: parity was restored BEFORE the base run rather than
  attributed after it, which is the first of the two options the gate doc
  allows.

## Base parity (R-0155 amendment / R-0158 path correction)

The throwaway worktree was created ON a throwaway branch
(`git worktree add -b tmp/base-gate <path> 1869d89a`) — a detached HEAD fails
the self-dogfood branch guard by design (DECISION D3).

`apps/ui/node_modules` and `apps/ui/dist` were COPIED in from the primary
checkout — never symlinked, because the UI auto-build runs npm install and
writes THROUGH a symlink into the primary checkout (F053 R3 evidence). The
base run also carried `REMEDY_UI_NO_AUTO_BUILD=1` so it could not rebuild.

That parity is why the base run shows zero UI build-artifact failures: the
class the amendment describes did not arise at all this round.

## Teardown

```
$ git worktree remove --force <path>
$ git worktree prune
$ git branch -D tmp/base-gate
Deleted branch tmp/base-gate (was 1869d89a).
$ git worktree list
/home/decodeux/Repos/remedy  aebc3c11 [feature/f061-dod-compiler]
```

Wall clock per side is ~2m20s, over the gate doc's ~5 min note threshold only
when both sides are counted together; neither single run crosses it.
