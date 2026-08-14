# Handback — F082 Self-benchmark, round R8

Deviations, declared: this handback is 190 lines against the 60-line cap, under
AGENTS.md DECISION D15 stated cause — the mandated content is the eighteen-gate
verification table with real values, the nine-slice authored-text proof table,
the six per-commit changed-files tables and the item-status table. No section is
dropped and no prose is padded.

## Range
Review of 20f101b0..da163bc6.

## Commits

### 18a15de7 chore(f082): save the R8 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f082-r8.md | +312 -0 | C0a, block saved byte for byte from the scratchpad |

### b79d2d73 chore(f082): mirror the R8 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +203 -225 | C0b, mirrored from the COMMITTED authored file, not the scratchpad |

### 4e031c8f docs(f082): record the R7 verdict, register R-0415 and R-0416
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +9 -0 | C1, append only: FINDING-R415, FINDING-R416, DECISION-D4, GATE-R7 |

### d81cb921 docs(f082): complete the context sweep and re-sync plan
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +13 -9 | C2a/C2b, the CTXSCOPE and CTXSTEPS2 rewrite pairs |
| .agent/plan.md | +8 -8 | C2c, full replacement with the PLAN slice |

### da163bc6 test(f082): pin the regression threshold and the trailing median
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/fixtures/bench_history/varied.jsonl | +4 -0 | C3, the fourth golden, generated with BenchHistoryEntry.to_json() |
| tests/orchestration/test_bench_history.py | +40 -0 | C3, two new tests, purely additive |

### C4 handback (self-reference, R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | the commit that writes this table cannot table itself |

## External actions
- `git push -u origin feature/f082-self-benchmark` after C0a; `git push` after
  C0b, C1, C2, C3 and C4. All succeeded.
- `git worktree add .remedy-wt/r8-redproof HEAD --detach`, then
  `git worktree remove --force` + `git worktree prune` after gate 15.
- `gh pr list --state open --json number,headRefName` → `[]`. NO PR created:
  F082 is mid-feature and its PR is created at closure.

## Verification (all eighteen gates, real values)
1. `git status --porcelain` EMPTY at handback. `git worktree list` 1 line:
   `/home/decodeux/Repos/remedy da163bc6 [feature/f082-self-benchmark]`.
2. Transport as a PROPERTY (`cmp`/`cp` denied; route = python3 byte compare +
   `sha256sum`): `.remedy-wt/f082-r8-scratchpad.md`, `.agent/authored/f082-r8.md`
   and `.agent/last_block.md` are byte-identical, shared sha256
   `9435c875acdf6ea2671efea0931afc66d61d3bbb61750fc517980c284bee5dd0`,
   30466 bytes, 312 lines — inside the 400-line cap.
3. `.agent/STOP` ABSENT at round start and ABSENT at handback.
4. Append proof: `post == pre + add` byte-wise TRUE, pre an exact prefix, first
   125 lines byte-equal to the pre-C1 file; C1 numstat `9 0`, DELETION 0.
   Physical lines: FINDING-R415 1, FINDING-R416 1, DECISION-D4 2, GATE-R7 1.
5. `^Gate: R7 — PASS` 1; `^- R-0415 — ` 1; `^- R-0416 — ` 1;
   `^## DECISION F082 D4` 1; `^## Steps` 1 (in .agent/context.md);
   `^Landed: ` 0; `^Done: ` 0.
6. Open set recomputed mechanically: 46 paragraphs `^- R-[0-9]+ — `, 0
   `^Done: ` lines, so FORTY-SIX open, no duplicate, max R-0416, next free
   R-0417. Ids: R-0361/62/63/64, R-0367/68/69, R-0371, R-0374/75/76/77/78/79,
   R-0380/81/82, R-0385/86/87, R-0389, R-0391/92/93/94/95/96/97, R-0399,
   R-0400/01/02/03/04/05/06/07/08/09, R-0410/11/12/13/14/15/16.
7. Both pairs as a PROPERTY: `post == pre.replace(SF,ST).replace(TF,TT)` TRUE.
   SCOPE_FROM 1→0, SCOPE_TO 0→1, STEPS_FROM 1→0, STEPS_TO 0→1, measured WITH
   the terminating newline. `wc -l .agent/context.md` = 59. Re-read end to end:
   ONE region still names which modules the feature builds — the Scope
   paragraph's second half, "R2's inventory settled the shape … R3's
   `capability_bench.py`, R4's `bench_orders.py`, R6's `bench_dry_run.py` and
   R7's `bench_history.py`" — and it AGREES with `.agent/plan.md` and with the
   rewritten first half; nothing is stale there. The `## Steps` map now names
   every round R1-R11 and agrees with plan.md's Next Steps (R9 T003, R10
   integration gate, R11 closure). No other region names rounds or counts.
   Nothing repaired outside the two ordered pairs.
8. `wc -l .agent/plan.md` = 36, under 50.
9. Contract readers in `.agent/context.md`: `## Active Branch` present with
   slug `feature/f082-self-benchmark`; substring `Steps` present (1 heading);
   roadmap F-id `F082` present (9 hits); `pytest`/`resource` present (2 hits).
10. `git diff --name-only 20f101b0..HEAD` = 7 paths, counted mechanically:
    .agent/authored/f082-r8.md, .agent/context.md, .agent/last_block.md,
    .agent/live_review.md, .agent/plan.md,
    tests/orchestration/fixtures/bench_history/varied.jsonl,
    tests/orchestration/test_bench_history.py. Every one is in the Change list;
    NO path outside it. `git diff --name-only 20f101b0..HEAD -- packages/` is
    EMPTY. (`.agent/handoff.md` becomes the 8th at the C4 commit, R-0149.)
11. `git diff --numstat 20f101b0..HEAD -- tests/orchestration/test_bench_history.py`
    → `40  0` — DELETION column 0, purely additive.
12. Eleven-file orchestration suite: exit 0, `294 passed`. Arithmetic:
    292 at 20f101b0 + 2 new tests = 294; no pre-existing test lost.
13. Canary + three contract readers: exit 0, `184 passed` (42 + 142).
14. `python3 -m ruff check tests/orchestration/test_bench_history.py` → exit 0,
    `All checks passed!`.
15. Red-proof, disposable worktree `.remedy-wt/r8-redproof` at da163bc6 only.
    Unmutated baseline there: `10 passed`, exit 0 — proving the worktree copy is
    the one imported (cwd was the worktree, R-0337).
    (a) `if latest <= baseline * multiplier:` → `if latest <= baseline:`
        (FROM 1→0, TO 0→1): exit 1, `1 failed, 9 passed`. FAILED
        `test_a_larger_multiplier_silences_the_same_history` at
        `assert bench_regressions(entries, series=SERIES, multiplier=3.0) == ()`
        — "Left contains 2 more items, first extra item: BenchRegression(
        kind='cost_regression', … latest=2000.0, baseline=1000.0,
        multiplier=3.0)". Reverted with `git -C … checkout --`; baseline
        re-run `10 passed` before (b).
    (b) `_median` body → `return float(sum(values)) / float(len(values))`:
        exit 1, `2 failed, 8 passed`. FAILED
        `test_the_trailing_median_ignores_one_catastrophic_run` at
        `cost_warning = next(w for w in found if w.kind == REGRESSION_COST)` →
        `StopIteration`, and
        `test_a_larger_multiplier_silences_the_same_history` at
        `assert bench_regressions(entries, series=SERIES)` → `assert ()`.
    BOTH mutations that left `8 passed` at 20f101b0 now die. R-0415's blindness
    is closed. Worktree removed and pruned; `git worktree list` = 1 line.
16. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`; `high_blockers_open` message:
    "no open blocker/high findings".
17. `gh pr list --state open --json number,headRefName` → `[]`.
18. Insertions per commit: 312, 203, 9, 21, 44. None over 500.

## Authored-text proofs
Every slice was extracted from the COMMITTED `.agent/authored/f082-r8.md`
(`git show HEAD:…`) and applied disk-to-disk; none was retyped and none came
from the scratchpad.

| Slice | lines | bytes | sha256 | applied-region proof |
|---|---|---|---|---|
| FINDING-R415 | 1 | 2343 | 74a7c65f… | in `post == pre + add`, TRUE |
| FINDING-R416 | 1 | 2166 | fe18162c… | in `post == pre + add`, TRUE |
| DECISION-D4 | 2 | 1457 | 7fe0fa38… | in `post == pre + add`, TRUE |
| GATE-R7 | 1 | 5283 | 5a5d74dd… | in `post == pre + add`, TRUE |
| CTXSCOPE-FROM | 7 | 543 | d5752692… | 1x before, 0x after |
| CTXSCOPE-TO | 10 | 711 | bc218e9b… | 0x before, 1x after |
| CTXSTEPS2-FROM | 8 | 634 | 1a7a541b… | 1x before, 0x after |
| CTXSTEPS2-TO | 9 | 724 | c68e6a66… | 0x before, 1x after |
| PLAN | 36 | 1876 | 435b5962… | whole-file equality TRUE, same digest |

Appended live_review region sha256
`2b19ac8680bd0ddd9afe59542f3ffb49eea64105aef386380eb62d530be10482`.
Both context pairs are REWRITES: neither TO contains its own FROM (both False)
and the two FROMs are disjoint (both directions False). Byte lengths are UTF-8
BYTES including each slice's terminating newline.
Marker scan: 0 BEGIN/END lines in all six non-block files (18 in each block
file, as expected). Trailing-whitespace scan: NONE in any of the eight files
touched; every one ends with a newline.

## Item-status table
| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror to last_block | done | |
| C1 R415/R416/D4/GATE-R7 | done | |
| C2a CTXSCOPE pair | done | |
| C2b CTXSTEPS2 pair | done | |
| C2c plan.md replacement | done | |
| C3 varied.jsonl + 2 tests | done | both mutations now die |
| C4 handback | done | |
| Gates 1-18 | done | all eighteen run, real values above |

## Deviations & assumptions
1. Handback length 190 lines against the 60-line cap — DECISION D15 stated
   cause, named at the top; no section dropped.
2. Commit messages carry no trailer, matching this branch's history.
3. `cmp`, `cp`, bare `echo $?` and the `remedy` entry point are denied to this
   session class. Routes used instead: python3 byte comparison plus
   `sha256sum` for every byte-equality and transport property; a python3
   `subprocess` runner for the real pytest exit codes under gate 15;
   `python3 -m apps.cli.main` for gate 16. This is R-0408's counter-measure.
4. NOT repaired, declared instead (R-0406 conduct): the module docstring of
   `tests/orchestration/test_bench_history.py` still opens "The three goldens
   under `fixtures/bench_history/`" while there are now FOUR. Editing it would
   have put a deletion in that file and gate 11 orders the DELETION column at 0,
   so the ordered constraint won. It is the R-0414/R-0416 stale-claim class, one
   sentence, and R9 can retire it in a pair.
5. No file under `packages/` changed, as the block required.

## Next
The next session's FIRST action is `docs/agents/self_drive_protocol.md` Phase 1
rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR Gate. F082 is
MID-FEATURE: no PR exists for `feature/f082-self-benchmark` and none is created
until closure. Next round is R9 — T003: the `stats bench` CLI, model-context
recording, and a fake-provider bench run end to end.
