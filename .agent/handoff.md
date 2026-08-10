# Handoff — F105 R39

Branch: feature/f105-cache-optimal-prompt-ordering. Base 5ca4debd.
Commits: 0b3d4a6a (C1a), 9962afe5 (C1b), 4c1b9bac (C2), b2e6194e (C3), C5 = HEAD.
C4 was NOT committed. The block's test assertion is unsatisfiable — see BLOCKER.

## Changed files
| Path | Commit | +/- |
|---|---|---|
| .agent/authored/f105-r39-1.md | C1a 0b3d4a6a | +347/-0 |
| .agent/last_block.md | C1b 9962afe5 | +281/-164 |
| .agent/live_review.md | C2 4c1b9bac | +37/-0 |
| packages/orchestration/intake.py | C3 b2e6194e | +12/-2 |
| packages/orchestration/flight_plan.py | C3 b2e6194e | +9/-1 |
| .agent/plan.md, .agent/handoff.md | C5 HEAD | full rewrites |

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | skipped | PAIR_TI/PAIR_TF assert an unsatisfiable equality — BLOCKER below |
| C5 | deviated | PAIR_P_PLAN applied, then 3 minimal factual corrections |

## BLOCKER — why C4 did not land
PAIR_TI and PAIR_TF both assert `seen == [composed.text]`. That can never hold,
for ANY implementation: `run_structured_call` does not hand the base prompt to
`call_fn`, it hands `build_schema_prompt(model_cls, base_prompt, carry)`, which
appends `\n\n` + the schema instruction — 1489 chars for `JobIntake`. Measured:
`effective == composed.text` False, `effective.startswith(composed.text)` True.
Applied verbatim, the two tests fail: `2 failed, 66 passed in 0.60s` (exit 1),
reproduced identically on HEAD inside the disposable worktree. Committing them
would have left the branch knowingly red, so they were reverted from the primary
checkout (G8: never widen scope to route around a block). C3's production change
is correct and unaffected — `_build_intake_prompt(m) == compose_intake_prompt(m).text`
was verified True, so the default branch is byte-identical to before.

## Diagnostic for R40 (worktree only, nothing landed)
With the single assertion changed to `seen[0].startswith(composed.text)`, both
tests pass: `68 passed in 0.46s`. Red-proofs then work, one mutation at a time:
- intake ternary -> `_build_intake_prompt(mission)`:
  `> assert seen[0].startswith(composed.text)` / `E assert False` — 1 failed, 37 passed.
- flight_plan ternary -> `_build_plan_prompt(intake)`:
  `> assert seen[0].startswith(composed.text)` / `E assert False` — 1 failed, 29 passed.
Worktree removed and pruned; the primary checkout was never mutated (G5).

## Gates
| Gate | Command | Exit | Result |
|---|---|---|---|
| A | cmp block/authored, authored/last_block | 0, 0 | both silent |
| B | wc -l authored | 0 | 347 vs cap 400 |
| C | pair shapes (below) | 0 | declared == measured, all 6 |
| C | cmp plan.md vs PAIR_P_PLAN slice | 1 | DECLARED deviation, see C5 |
| C | wc -l plan.md | 0 | 49 vs cap 50 |
| D | git show -U0 per commit | 0 | C2 +37/-0, C3 +12/-2 and +9/-1; strays 0/0 all three |
| E | grep -c '^<<<' in 5 written targets | 0 | 0 in every one |
| F | pytest tests/docs/ | 0 | 294 passed in 0.25s |
| F | pytest test_dashboard_contract.py | 0 | 70 passed in 4.05s |
| F | plan `## Goal` 1x, `Steps` 1x; live_review `## Steps` 1x | 0 | all hold |
| G | pytest test_intake + test_flight_plan, C4 APPLIED | 1 | 2 failed, 66 passed — RED, the blocker |
| G | same, as LANDED (C4 skipped) | 0 | 66 passed in 0.48s |
| H | compose digests before C3 and after | 0 | EQUAL, both |
| I | red-proofs in .remedy-wt/r39-red | n/a | vacuous as specified; run against the corrected assertion instead, above |
| J | pytest test_golden_path.py | 0 | 42 passed in 20.50s |
| J | git status --porcelain | 0 | only `?? .agent/STOP`, an untracked operator file |
| J | git worktree list | 0 | primary alone |
| J | insertions per commit | 0 | 347, 281, 37, 21 — all under 500 |
| J | git diff --name-only 5ca4debd..HEAD | 0 | the 5 paths below; do_cmd.py ABSENT |

Paths in range: `.agent/authored/f105-r39-1.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `packages/orchestration/flight_plan.py`,
`packages/orchestration/intake.py` (+ `.agent/plan.md`, `.agent/handoff.md` at C5).
The two `tests/orchestration/` paths are absent because C4 was skipped.

## Transport proof
All three of `.remedy-wt/f105-r39-1.block.md`, `.agent/authored/f105-r39-1.md`
and `.agent/last_block.md` hash to
`377d8c5e6ffaa18a7d98f17e6dab2ab630e50132417c4109f199022e28bf345b` at 347 lines;
both `cmp` runs silent. PRIMARY shape, not the §4.9 fallback.

## Pair proof
Every pair sliced from the COMMITTED authored file by a whole-line marker reader
(`.remedy-wt/r39_slice.py`, gitignored); nothing retyped. Every FROM verified 1x
in its target BEFORE its write.
| Pair | Declared | Measured | Before | After |
|---|---|---|---|---|
| PAIR_LR | CONTAINS-FROM | CONTAINS-FROM | FROM 1x | FROM 1x / TO 1x |
| PAIR_INTAKE | REWRITE | REWRITE | FROM 1x | FROM 0x / TO 1x |
| PAIR_FP | REWRITE | REWRITE | FROM 1x | FROM 0x / TO 1x |
| PAIR_FP2 | REWRITE | REWRITE | FROM 1x | FROM 0x / TO 1x |
| PAIR_TI | CONTAINS-FROM | CONTAINS-FROM | FROM 1x | worktree only, NOT landed |
| PAIR_TF | CONTAINS-FROM | CONTAINS-FROM | FROM 1x | worktree only, NOT landed |

## Gate H digests (identical before C3 and after C5)
- `compose_intake_prompt('a fixed mission')`:
  `cde0c0deafe387a7e078f36ca69270c44642e1c542e397221a6c55021b8d80d8`
- `compose_flight_plan_prompt({'goal':'fixed'}, project_facts='pinned')`:
  `9c8d25d8e0db9c9f7328c24ccec21b47dd126cbb269e41e3caa9f764d7f3d7a5`
Neither composer was touched.

## Deviations, declared
1. C4 skipped. Reason in BLOCKER. Consequence: `composed=` ships with no test on
   its new branch until R40; the default branch keeps its existing coverage (66
   passed). R-0256 stays OPEN, as the block already intended.
2. C5 is not byte-for-byte PAIR_P_PLAN. The slice states "one test each, both
   red-proofed", which C4 did not deliver; committing it would have made
   `.agent/plan.md` assert something false, and AGENTS.md requires plan.md to
   reflect the current state and to carry the exact blocker. Applied the slice,
   then three minimal corrections: the Current Step sentence, one Next Steps
   bullet for R40, and a `## BLOCKER` section. 49 lines, under the cap of 50.
   Everything else is byte-identical to the slice. AGENTS.md over the block.
3. Gate I could not run as written — with C4 unlanded there is no committed test
   to red-proof, and with C4 applied the tests fail unmutated, so the mutation
   would prove nothing. Ran the equivalent proof against the corrected assertion
   in the disposable worktree instead and reported the real failure lines.
4. `.agent/STOP` (untracked, empty, 09:15) appeared mid-round. Per G6 no commit
   was half-written, so this handoff commit closes the round. The file is left
   in place — it is the operator's signal, not the round's to remove. It is the
   only entry in `git status --porcelain`.
5. This file is 134 lines, over the 60-line cap (DECISION D15 stated-cause
   overage). Cause: the mandated gate table plus the item-status table, the
   transport and pair proofs, the two H digests and the red-proof lines, and a
   blocker that needs its evidence stated to be actionable. No section dropped.

## Open findings
5 — R-0221, R-0239, R-0247, R-0256, R-0262. R-0256 remains OPEN; R39 landed its
signature half only.

## Next action
Gate R39. Then reissue C4 inside R40 with `seen[0].startswith(composed.text)`
(or `== build_schema_prompt(<model>, composed.text)`), and run R40's three
`apps/cli/commands/do_cmd.py` call sites. No PR — one is created at CLOSURE.
