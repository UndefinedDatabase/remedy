# Handoff — F105 R45 (T004 slice 1/2)

Branch: feature/f105-cache-optimal-prompt-ordering. Base ae1756f8.
Commits: 788a529c (C1a), dfa9fdde (C1b), d39dad4a (C2), 422a01cc (C3),
e1f503f5 (C4), 8d497bc2 (C5), a2f1bc3b (C6), C7 = HEAD (this commit).
SPLIT round: production code landed in C4 and C5, tests in C6. No new test
module, no `docs/`, no `packages/`. `.agent/STOP` is ABSENT and was not created.
No PR was created, nothing was merged, `main` was not touched, no force-push.

## Changed files
| Path | Commit | +/- |
|---|---|---|
| .agent/authored/f105-r45-1.md | C1a 788a529c | +399/-0 (new file) |
| .agent/last_block.md | C1b dfa9fdde | +363/-197 |
| .agent/live_review.md | C2 d39dad4a | +47/-1 |
| .agent/decisions.md | C3 422a01cc | +17/-0 |
| apps/cli/commands/stats_ledger_cmd.py | C4 e1f503f5 | +109/-0 |
| apps/cli/command_catalog.py | C5 8d497bc2 | +22/-0 |
| tests/cli/test_stats_cost.py | C6 a2f1bc3b | +54/-0 |
| .agent/plan.md | C7 HEAD | full rewrite, 45 lines |
| .agent/handoff.md | C7 HEAD | full rewrite |

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | block written to .agent/authored/f105-r45-1.md, committed alone |
| C1b | done | same bytes copied to .agent/last_block.md, separate commit |
| C2 | done | PAIR_ID rewrite + PAIR_LR contains-from, R44 gate + R-0267 + R45 |
| C3 | done | PAIR_DEC contains-from; DECISION F105 D15 appended at the END |
| C4 | done | PAIR_VIEW + PAIR_HANDLER, one commit |
| C5 | done | PAIR_CAT; supports_json=False and no --json arg, as ordered |
| C6 | done | PAIR_TDOC + PAIR_TEST, one commit, six new tests |
| C7 | done | plan.md rewritten (45 lines) + this handoff, then push |

## Gates — real exit codes
| Gate | Command | Exit | Result |
|---|---|---|---|
| A | sha256sum block/authored/last_block | 0 | all three EQUAL (digest below) |
| A | cmp block vs authored; cmp block vs last_block | 0, 0 | both silent |
| B | wc -l .agent/authored/f105-r45-1.md | 0 | 399 vs D5 cap 400 |
| C | pair shapes, measured (table below) | 0 | declared == measured, all 8 |
| D | stray reconcile, 5 commits (table below) | 0 | 249 added, 0 strays |
| E | grep -c '^<<<' over the 7 touched text files | 1 x7 | counts all 0 |
| F | pytest tests/cli/test_stats_cost.py -q | 0 | 39 passed in 0.38s |
| G | pytest the 3 catalog/spine suites -q | 0 | 113 passed in 0.56s |
| H | pytest tests/cli/test_golden_path.py -q | 0 | 42 passed in 19.85s |
| I | py_compile both changed production files | 0 | no output |
| J | git status --porcelain | 0 | EMPTY |
| J | git worktree list | 0 | primary ALONE |
| J | insertions per commit | 0 | 399,363,47,17,109,22,54 — all < 500 |
| K | git diff --name-only ae1756f8..HEAD | 0 | exactly the 9 named paths |

Gate E note: `grep -c` exits 1 when the pattern is absent, which is the PASS
condition; the recorded numbers are the counts, all zero. Files checked:
live_review.md, decisions.md, plan.md, handoff.md, stats_ledger_cmd.py,
command_catalog.py, test_stats_cost.py.

## Transport proof
`.remedy-wt/f105-r45-1.block.md`, `.agent/authored/f105-r45-1.md` and
`.agent/last_block.md` all three hash to
`87f65221d35d613fdb70265fd670060ccc174c77c84fa4640eefa288a6058ad8`,
399 lines. Both `cmp` runs silent. All 16 pair bodies were SLICED from the
COMMITTED `.agent/authored/f105-r45-1.md` by `.remedy-wt/r45_slice.py`, a
whole-line marker reader that refuses any marker not present exactly 1x, and
applied by `.remedy-wt/r44_apply.py`, which refuses to write unless FROM==1 and
TO==0. Nothing was retyped. Scratch lives in the gitignored `.remedy-wt/`.

## Pair proof — declared vs MEASURED
| Pair | Declared | FROM before | FROM after | TO after |
|---|---|---|---|---|
| PAIR_ID | REWRITE | 1 | 0 | 1 |
| PAIR_LR | CONTAINS-FROM | 1 | 1 | 1 |
| PAIR_DEC | CONTAINS-FROM | 1 | 1 | 1 |
| PAIR_VIEW | CONTAINS-FROM | 1 | 1 | 1 |
| PAIR_HANDLER | CONTAINS-FROM | 1 | 1 | 1 |
| PAIR_CAT | CONTAINS-FROM | 1 | 1 | 1 |
| PAIR_TDOC | CONTAINS-FROM | 1 | 1 | 1 |
| PAIR_TEST | CONTAINS-FROM | 1 | 1 | 1 |

Every FROM was counted in its target BEFORE the first write: each 1x, each TO 0x.

## Gate D — stray reconcile per commit
| Commit | Path | Added | Removed | Strays |
|---|---|---|---|---|
| d39dad4a C2 | .agent/live_review.md | 47 | 1 | 0 |
| 422a01cc C3 | .agent/decisions.md | 17 | 0 | 0 |
| e1f503f5 C4 | apps/cli/commands/stats_ledger_cmd.py | 109 | 0 | 0 |
| 8d497bc2 C5 | apps/cli/command_catalog.py | 22 | 0 | 0 |
| a2f1bc3b C6 | tests/cli/test_stats_cost.py | 54 | 0 | 0 |

The single C2 removal is the PAIR_ID FROM line, which that REWRITE replaces.

## Open findings: 7
R-0221, R-0239, R-0247, R-0262, R-0265 and R-0266 — all six OPEN by design and
untouched this round. `Landed: R-0267` — the fix is
`TestStatsCacheView.test_an_unreadable_ledger_exits_instead_of_reporting_zero`
in C6, which drives the `sqlite3.Error` branch of `_load_ledger_reports` and
asserts EXIT_ERROR plus the stderr text. No `Done:` paragraph was authored by
this worker; only reviewer-authored text sets a resolution
(planner_reviewer_prompt.md §4.4).

## PR #189 — untouched, stop-and-report
`docs/amend0810-clerical` -> `main`, open, not a draft, NOT from a `feature/*`
branch, so the AGENTS.md Open PR Gate makes it stop-and-report. This round did
not merge, comment on, or modify it.

## Next expected action
Gate R45 as an ordinary handback: `git diff ae1756f8..HEAD`, re-run every gate
above, advance `LAST_REVIEWED_SHA` from ae1756f8, and write the R45 gate record
into `.agent/live_review.md` under `## Steps`, resolving or keeping R-0267. The
next WORK action is R46 = T004 slice 2/2 as `.agent/plan.md` "Next Steps" scopes
it: the `--json` mode for `stats cache` and the before/after comparison note.

Deviations, declared (DECISION D15): this handoff is 119 lines against the
60-line cap. The cause is mandated content only — the 14-row gate table with its
real exit codes, the changed-files table, the item-status table, the transport
proof, the 8-row pair proof, the 5-row stray reconcile, the finding state and
the PR #189 state. No section was dropped and no prose was added to reach that
length.
