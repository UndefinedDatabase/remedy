# F040 round 17 — integration gate attribution

## Comparison result

`branch_only.txt` (comm -13 base_failed.txt branch_failed.txt): **0 lines.**
`base_only.txt` (comm -23 base_failed.txt branch_failed.txt): **0 lines.**

Both `branch_failed.txt` and `base_failed.txt` are empty (0 lines) — the
branch run and the corrected base run each exited 0 with zero FAILED lines.
There is no branch-only id to classify under constraint 8's per-id
procedure, and no base-only id needing the environment-parity attribution
integration_gate.md step 3 would otherwise require.

## The base run required one parity correction before it produced this result

The FIRST base-run attempt, made after the constraint-6 `shutil.copytree(...,
symlinks=True)` of `apps/ui/node_modules` and `apps/ui/dist` from the primary
checkout into `.remedy-wt/wt-r17-base` and with `REMEDY_UI_NO_AUTO_BUILD=1`
set, failed 119 of 18467 collected tests (18328 passed, 20 skipped), every
one of them a `tests/ui_server/*` id dying on `ERROR: React UI not built.`
in captured stderr. This reproduces the environment class already on
record as **finding R-0736** (Medium, OPEN, confirmed independently at the
F033 R27 integration gate, 2026-08-29): `shutil.copytree` preserves the
PRIMARY checkout's source mtimes, but `git worktree add` stamps every
checked-out file in the WORKTREE with the checkout time, so after the copy
every file under the worktree's `apps/ui/src/` reads newer than the copied
`apps/ui/dist/index.html`. `_get_frontend_dist()` /
`_frontend_is_stale()` in `packages/orchestration/ui_server.py` (around
line 3162) then reports the dist stale, `REMEDY_UI_NO_AUTO_BUILD=1` correctly
suppresses the rebuild that would otherwise fix it, and every test that
starts the UI server dies loud instead.

Measured directly in this worktree before the first base run: max mtime
under `apps/ui/src/` = `1788050552.36` (2026-08-30 02:42:32); `dist/index.html`
mtime = `1788050071.91` (2026-08-30 02:34:31, carried from the primary
checkout by the copy) — src newer than dist, confirming the stale reading
that produced the 119 failures.

Per R-0736's own documented fix and per integration_gate.md step 3's
"restore parity before the base run" option: `os.utime` was applied to
every file and directory under the worktree's `apps/ui/dist` (content
untouched, sha256 unchanged), advancing their mtime to
`1788051304.657` (2026-08-30 02:55:04), strictly after the max
`apps/ui/src/` mtime. Re-checked: `_frontend_is_stale()`'s own inputs now
read `is_stale == False`. The base suite was re-run under the same
`REMEDY_UI_NO_AUTO_BUILD=1` and this corrected artifact state; result:
**exit 0, 18447 passed, 20 skipped, 0 failed, 113.83s.** This second run's
output is what `.agent/gate_f040_r17/base_run.txt` and `base_failed.txt`
hold — it is "the base run" this gate's comparison is built from.

Constraint 6's own mtime-window instrument was applied to THIS (corrected,
authoritative) base run: `apps/ui/dist` mtimes recorded immediately before
and immediately after — both readings identical, all four files at
`1788051304.6574283` before and after. No mtime falls inside the run
window; the parity claim holds for the run whose evidence is reported.

This is a fresh, independent reproduction of an already-registered
Medium/OPEN environment finding (R-0736), not a new finding — no new id is
minted here, per checklist item 30 (retire/avoid duplicate ids) and the
reviewer-only minting rule (per §4 item 30 the reviewer, not this round,
would mint any new R-id; none is warranted since R-0736 already exists and
already names this exact mechanism). R-0736 itself remains OPEN and is not
F040's to fix (F040's plan.md already routes it, alongside R-0570, R-0752
and R-0755, to the paydown branch).

## Conclusion

No branch-only failure exists to attribute. No base-only failure survives
the parity correction. The gate's raw evidence is clean; per
docs/agents/integration_gate.md step 5, only the reviewer issues the gate
verdict.
