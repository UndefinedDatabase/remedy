# Integration gate evidence — F069 R2 (2026-08-03)

Procedure: docs/agents/integration_gate.md, followed as written.
The GATE VERDICT is the reviewer's. This directory reports evidence only.

## Runs

| Run | Command | Result | Exit | Wall |
| --- | --- | --- | --- | --- |
| Branch (`b70009cb`+state) | `python3 -m pytest -n auto -q` | 15094 passed, 19 skipped | 0 | 115s |
| Base (`53ac3efa`, worktree on `tmp/base-gate`) | `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` | 8 failed, 14968 passed, 19 skipped | 1 | 163s |

Base worktree created per §2 on a throwaway BRANCH (never detached).
UI parity per §3: `apps/ui/node_modules` and `apps/ui/dist` **copied**
(`cp -a`), never symlinked; `find apps/ui -maxdepth 1 -type l` was empty.

## Comparison (§3, both directions)

- `comm -13 base_failed.txt branch_failed.txt` → **0 branch-only failures**
  (`branch_only.txt` is empty).
- `comm -23 base_failed.txt branch_failed.txt` → 8 base-only ids
  (`base_only.txt`), every one attributed in `attribution.md` to the
  environment class the doc names (the base worktree's `apps/ui/dist`),
  by three pieces of direct evidence including a clean re-run at base.

## Attribution (§4)

No branch-only id exists, so §4's per-id serial re-run has no input and no
id could be classified as a blocker. The `comm -23` ids are attributed in
`attribution.md` as §3 requires.

## Budget (§5)

Both runs are under the ~5 min threshold (115s branch, 163s base), so no
perf pass is flagged.

## Files

| File | Contents |
| --- | --- |
| `branch_run.txt` / `base_run.txt` | full raw pytest output |
| `branch_failed.txt` (empty) / `base_failed.txt` | sorted `^FAILED` lists |
| `branch_only.txt` (empty) / `base_only.txt` | the two `comm` outputs |
| `branch_exit.txt` / `base_exit.txt` | exit code + wall seconds |
| `base_only_rerun.txt` | base re-run of the 8 ids with `dist` present |
| `attribution.md` | per-id attribution for every `comm -23` id |
| `worktree_teardown.txt` | removal + prune + `git worktree list` proof |

> **Extension note (F069 R3).** These three raw-output files were written as
> `*.log` during R2 and were therefore silently excluded from that round's
> commit by `.gitignore:59 (*.log)` — the ordered raw tails never reached the
> repository. They are renamed to `.txt` and committed here, which also clears
> the review-zip packaging guard (it rejects any `.log` member). The bytes are
> the originals from the R2 runs; nothing was re-run to produce them.
