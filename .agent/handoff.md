# Handoff — F105 R40 (SESSION CLOSE)

Branch: feature/f105-cache-optimal-prompt-ordering. Base c44a582c.
Commits: 4149021f (C1a), 0dd0b104 (C1b), 7f3b0ba5 (C2), C3 = HEAD.
`.agent/STOP` is present (untracked, empty, operator-owned). It was NOT deleted
or moved. This round is state-only: no production code, no tests, no docs.
The session ENDS here — no further rounds were started and no PR was created.

## Changed files
| Path | Commit | +/- |
|---|---|---|
| .agent/authored/f105-r40-1.md | C1a 4149021f | +220/-0 |
| .agent/last_block.md | C1b 0dd0b104 | +145/-272 |
| .agent/live_review.md | C2 7f3b0ba5 | +59/-4 |
| .agent/plan.md, .agent/handoff.md | C3 HEAD | full rewrites |

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | block copied to .agent/authored/f105-r40-1.md, committed alone |
| C1b | done | same bytes mirrored to .agent/last_block.md, separate commit |
| C2 | done | PAIR_ID, PAIR_F and PAIR_S in ONE commit on ONE path |
| C3 | done | PAIR_P_PLAN byte-for-byte + this handoff |

## Gates
| Gate | Command | Exit | Result |
|---|---|---|---|
| A | sha256sum block/authored/last_block | 0 | all three EQUAL, digest below |
| A | cmp block vs authored; cmp block vs last_block | 0, 0 | both silent |
| B | wc -l .agent/authored/f105-r40-1.md | 0 | 220 vs D5 cap 400 |
| C | pair shapes, measured (table below) | 0 | declared == measured, all 4 |
| C | cmp .agent/plan.md vs PAIR_P_PLAN slice | 0 | silent — byte-for-byte |
| C | wc -l .agent/plan.md | 0 | 41 vs cap 50 |
| D | git show -U0 7f3b0ba5 -- .agent/live_review.md | 0 | +59/-4; strays 0 added, 0 removed |
| E | grep -c '^<<<' live_review / plan / handoff | 0 | 0, 0, 0 |
| F | pytest tests/docs/ -q | 0 | 294 passed in 0.32s |
| F | pytest tests/ui_server/test_dashboard_contract.py -q | 0 | 70 passed in 4.57s |
| F | plan `## Goal` 1x, `Steps` 1x; live_review `## Steps` 1x | 0 | 1, 1, 1 |
| G | git diff --name-only c44a582c..HEAD | 0 | 5 paths, ALL under .agent/ (below) |
| H | pytest tests/cli/test_golden_path.py -q | 0 | 42 passed in 21.88s |
| I | git status --porcelain | 0 | `?? .agent/STOP` and nothing else |
| I | git worktree list | 0 | primary alone |
| I | insertions per commit (git show --numstat) | 0 | 220, 145, 59, 82 — all under 500 |

Paths in range c44a582c..HEAD: `.agent/authored/f105-r40-1.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/handoff.md`. Nothing under `packages/`, `apps/`, `tests/` or `docs/`.

## Transport proof
`.remedy-wt/f105-r40-1.block.md`, `.agent/authored/f105-r40-1.md` and
`.agent/last_block.md` all three hash to
`dd655c7b424259199977a4b402e2a52ea40e2ca4dd78f31f083c554e6995376e`
at 220 lines; both `cmp` runs silent. PRIMARY shape, not the §4.9 fallback.

## Pair proof
Every pair SLICED from the COMMITTED authored file by a whole-line marker reader
(`.remedy-wt/r40_slice.py`, gitignored); nothing retyped. Every FROM verified 1x
in its target BEFORE its write; reconciliation by `.remedy-wt/r40_reconcile.py`.
| Pair | Declared | Measured | Before | After |
|---|---|---|---|---|
| PAIR_ID | REWRITE | REWRITE | FROM 1x | FROM 0x / TO 1x |
| PAIR_F | CONTAINS-FROM | CONTAINS-FROM | FROM 1x | FROM 1x / TO 1x |
| PAIR_S | REWRITE | REWRITE | FROM 1x | FROM 0x / TO 1x |
| PAIR_P_PLAN | FULL REPLACEMENT | FULL REPLACEMENT | n/a | cmp silent, 41 lines |

No mutation red-proof was ordered and none was run: nothing executable changed,
so there is no branch to mutate (D8 item 5, DECISION F105 D10).

## Deviations, declared
1. This file is 97 lines, over the 60-line cap (DECISION D15 stated-cause
   overage). Cause: the mandated gate table (17 rows), the item-status table,
   the transport proof and the pair-shape table. No section dropped.
2. None other. Every C item landed as specified; no block instruction was
   unsatisfiable this round.

## Open findings
6 — R-0221, R-0239, R-0247, R-0256, R-0262, R-0263 (registered this round).
`LAST_REVIEWED_SHA` is c44a582c: R39 is GATED PASS. R40's own four commits are
deliberately ungated on disk — by §4.13 the last round of a session carries its
verdict in this handoff and in the session completion report, not in
`.agent/live_review.md`.

## Next action for whoever resumes this branch
1. Do NOT treat this as a fresh feature: F105 is mid-flight, T001/T002 DONE and
   gated, T003's six migration sites all migrated.
2. First change: land R39's two tests (`tests/orchestration/test_intake.py` and
   `test_flight_plan.py`) with `assert seen[0].startswith(composed.text)` — NOT
   `== composed.text`, which is R-0263 and cannot pass. Proved at R39 in a
   worktree: 68 passed; reverting either `composed`-ternary red-proofs its own
   test. That closes R-0263.
3. Then finish R-0256: pass `composed=` at the three
   `apps/cli/commands/do_cmd.py` sites (intake, flight-plan, replan). The new
   keyword goes on its OWN line — `tests/orchestration/test_prompt_trace.py`
   counts `on_call=make_flight_plan_call_recorder(` over the whole file (== 2).
4. Then T004 (`remedy stats cache` over actuals), the integration gate, then
   closure, where the PR is created. `.agent/STOP` must be cleared by the
   OPERATOR before any of this starts.
