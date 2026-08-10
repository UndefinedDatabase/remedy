# Handoff — F105 R44 (T004 slice 0/2)

Branch: feature/f105-cache-optimal-prompt-ordering. Base b0b2d12f.
Commits: 9ecccec8 (C1a), d56c11da (C1b), a24b8fa0 (C2), 90ac7adb (C3),
C4 = HEAD (this commit).
SPLIT round: production code landed in C3 and in C3 alone. No test module, no
catalog entry, no `docs/`. `.agent/STOP` is ABSENT and was not created. No PR
was created, nothing was merged, `main` was not touched, no force-push.

## Changed files
| Path | Commit | +/- |
|---|---|---|
| .agent/authored/f105-r44-1.md | C1a 9ecccec8 | +233/-0 (new file) |
| .agent/last_block.md | C1b d56c11da | +226/-290 |
| .agent/live_review.md | C2 a24b8fa0 | +37/-0 |
| apps/cli/commands/stats_ledger_cmd.py | C3 90ac7adb | +24/-6 |
| .agent/plan.md | C4 HEAD | full rewrite, 48 lines |
| .agent/handoff.md | C4 HEAD | full rewrite |

Counts from `git log --numstat b0b2d12f..HEAD` at write time.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | block written to .agent/authored/f105-r44-1.md, committed alone |
| C1b | done | same bytes copied to .agent/last_block.md, separate commit |
| C2 | done | PAIR_LR applied CONTAINS-FROM; R43 gate record + R44 step line |
| C3 | done | PAIR_COST applied as a REWRITE; `_load_ledger_reports` extracted |
| C4 | done | plan.md rewritten (48 lines) + this handoff, then push |

## Gates — real exit codes
| Gate | Command | Exit | Result |
|---|---|---|---|
| A | sha256sum block/authored/last_block | 0 | all three EQUAL (digest below) |
| A | cmp block↔authored; cmp block↔last_block | 0, 0 | both silent |
| B | wc -l .agent/authored/f105-r44-1.md | 0 | 233 vs D5 cap 400 |
| C | pair shapes, measured (table below) | 0 | declared == measured, both |
| D | stray reconcile a24b8fa0 live_review.md | 0 | +37 added, 0 strays |
| D | stray reconcile 90ac7adb stats_ledger_cmd.py | 0 | +24 added, 0 strays |
| E | grep -c '^<<<' over the 4 touched files | 1,1,1,1 | counts 0, 0, 0, 0 |
| F | pytest tests/cli/test_stats_cost.py -q | 0 | 33 passed in 0.34s |
| G | pytest test_command_catalog.py x2 -q | 0 | 41 passed in 0.50s |
| H | pytest tests/cli/test_golden_path.py -q | 0 | 42 passed in 19.98s |
| I | PROBE in disposable worktree, then removed | 1 | 19 failed, 14 passed in 0.62s |
| J | git status --porcelain | 0 | EMPTY |
| J | git worktree list | 0 | primary ALONE (probe removed + pruned) |
| J | insertions per commit | 0 | 233, 226, 37, 24, C4 — all < 500 |
| K | git diff --name-only b0b2d12f..HEAD | 0 | exactly the 6 named paths |

Gate E note: `grep -c` exits 1 when the pattern is absent, which is the PASS
condition; the recorded numbers are the counts, all zero. Files checked for
`^<<<`: live_review.md, plan.md, handoff.md, stats_ledger_cmd.py.
Also run before C3's commit: `python3 -m py_compile` on the edited module, exit 0.

## Gate I — the probe, reported as a number and not a colour
A disposable worktree at HEAD under `.remedy-wt/r44probe` had the whole body of
`_load_ledger_reports` replaced by `raise RuntimeError("probe")`. Against that
mutation `tests/cli/test_stats_cost.py` reports `19 failed, 14 passed in 0.62s`:
19 of 33 tests reach the extracted helper, so it is not dead code. The worktree
was removed with `git worktree remove --force` and `git worktree prune`; the
primary checkout is alone at verdict time. The primary was never mutated.

## Transport proof
`.remedy-wt/f105-r44-1.block.md`, `.agent/authored/f105-r44-1.md` and
`.agent/last_block.md` all three hash to
`8944f6e563a74b11d104dc671b702b46ef49397f2b29227cf5fec48b6b987c24`,
233 lines. Both `cmp` runs silent. Both pairs were SLICED from the COMMITTED
`.agent/authored/f105-r44-1.md` by `.remedy-wt/r44_slice.py`, a whole-line marker
reader that refuses any marker not present exactly 1x, and applied by
`.remedy-wt/r44_apply.py`, which refuses to write unless FROM==1 and TO==0.
Nothing was retyped. Scratch lives in the gitignored `.remedy-wt/`, never `/tmp`.

## Pair proof — declared vs MEASURED
| Pair | Declared | FROM before | FROM after | TO after |
|---|---|---|---|---|
| PAIR_LR | CONTAINS-FROM | 1 | 1 | 1 |
| PAIR_COST | REWRITE | 1 | 0 | 1 |

Both FROMs were counted in their targets BEFORE the first write — each 1x, each
TO 0x. The PAIR_COST FROM was counted as the WHOLE contiguous 38-line text, not
by its first line: the `def _cmd_stats_cost` signature survives inside the TO.

## Behaviour proof for the extraction
Only the READ moved; both renderers keep the same three values. The proof is
`tests/cli/test_stats_cost.py` at 33 passed, not a reading of the diff. One
comment moved with its code: the "an unreadable ledger is not zero cost" note is
now the helper docstring's third paragraph (authored text, 0 strays).

## Open findings: 6
R-0221, R-0239, R-0247, R-0262, R-0265, R-0266 — all six OPEN by design and
untouched this round. No finding was resolved, and no `Done:` paragraph was
authored by this worker (planner_reviewer_prompt.md §4.4).

## PR #189 — untouched, stop-and-report
`docs/amend0810-clerical` -> `main`, open, not a draft, NOT from a `feature/*`
branch, so the AGENTS.md Open PR Gate makes it stop-and-report. This round did
not merge, comment on, or modify it. It blocks no work on THIS branch but must
be resolved by the operator before any NEW branch is cut.

## Next expected action
Gate R44 as an ordinary handback: `git diff b0b2d12f..HEAD`, re-run every gate
above, advance `LAST_REVIEWED_SHA` from b0b2d12f, and write the R44 gate record
into `.agent/live_review.md` under `## Steps`. The next WORK action is R45 =
T004 slice 1/2 exactly as `.agent/plan.md` "Next Steps" scopes it: the
`stats cache` command reading through `_load_ledger_reports`, its catalog entry,
and its own test module, under DECISION F105 D14 with `.agent/t004_inventory.md`
as ground truth.

Deviations, declared (DECISION D15): this handoff is 114 lines against the
60-line cap. The cause is mandated content only — the 15-row gate table with its
real exit codes, the changed-files table, the item-status table, the transport
and pair proofs, the ordered gate-I probe report, the behaviour proof for the
extraction, and the PR #189 state. No section was dropped and no prose was added
to reach that length.
