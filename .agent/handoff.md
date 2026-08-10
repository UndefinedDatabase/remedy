# Handoff — F105 R41

Branch: feature/f105-cache-optimal-prompt-ordering. Base 7f622b7f.
Commits: ab16abf0 (C1a), 68722d66 (C1b), 3682dac9 (C2), 398c7752 (C3),
3e2fa6bc (C4), C5 = HEAD (this commit).
`.agent/STOP` is ABSENT and was not created. No PR was created; no merge; no
force-push; `main` untouched. Every red-proof ran in a disposable worktree only.

## Changed files
| Path | Commit | +/- |
|---|---|---|
| .agent/authored/f105-r41-1.md | C1a ab16abf0 | +383/-0 |
| .agent/last_block.md | C1b 68722d66 | +299/-136 |
| .agent/live_review.md | C2 3682dac9, C5 HEAD | +43/-1, then +2/-0 |
| tests/orchestration/test_intake.py | C3 398c7752 | +21/-0 |
| tests/orchestration/test_flight_plan.py | C3 398c7752 | +23/-0 |
| apps/cli/commands/do_cmd.py | C4 3e2fa6bc | +7/-5 |
| tests/orchestration/test_prompt_trace.py | C4 3e2fa6bc | +9/-0 |
| .agent/plan.md | C5 HEAD | full replacement (PAIR_P_PLAN) |
| .agent/handoff.md | C5 HEAD | full rewrite |

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | block copied to .agent/authored/f105-r41-1.md, committed alone |
| C1b | done | same bytes mirrored to .agent/last_block.md, separate commit |
| C2 | done | PAIR_ID, PAIR_F, PAIR_S — one path, one commit, reconciled together |
| C3 | done | PAIR_TI + PAIR_TF, the corrected `startswith` form (R-0263) |
| C4 | done | PAIR_DO1/DO2/DO3 + PAIR_GUARD; recorder count still 2 |
| C5 | done | two worker-authored `Landed:` lines, PAIR_P_PLAN, this handoff |

## Gates — real exit codes
| Gate | Command | Exit | Result |
|---|---|---|---|
| A | sha256sum block/authored/last_block | 0 | all three EQUAL (digest below) |
| A | cmp block↔authored; cmp authored↔last_block | 0, 0 | both silent |
| B | wc -l .agent/authored/f105-r41-1.md | 0 | 383 vs D5 cap 400 |
| C | pair shapes, measured (table below) | 0 | declared == measured, all 9 |
| C | cmp .agent/plan.md vs PAIR_P_PLAN slice | 0 | silent — byte-for-byte |
| C | wc -l .agent/plan.md | 0 | 37 vs cap 50 |
| D | git show -U0 for 3682dac9, 398c7752, 3e2fa6bc | 0 | strays 0/0 in all three |
| E | grep '^<<<' over the 7 touched text files | 0 counts | 0,0,0,0,0,0,0 |
| F | pytest tests/docs/ -q | 0 | 294 passed in 0.26s |
| F | pytest tests/ui_server/test_dashboard_contract.py -q | 0 | 70 passed in 3.91s |
| F | plan `## Goal` 1x, `Steps` 1x; live_review `## Steps` 1x | 0 | 1, 1, 1 |
| G | git diff --name-only 7f622b7f..HEAD | 0 | 9 paths (below), 0 under packages/ or docs/ |
| H | pytest intake+flight_plan+prompt_trace+do_cmd_cli_path -q | 0 | 119 passed in 0.95s |
| I | pytest tests/cli/test_golden_path.py -q | 0 | 42 passed in 19.79s |
| J | three mutation red-proofs in a disposable worktree | 1, 1, 1 | all three RED (below) |
| K | git status --porcelain | 0 | EMPTY |
| K | git worktree list | 0 | primary ALONE; `.agent/STOP` absent |
| K | insertions per commit (git show --numstat) | 0 | 383, 299, 43, 44, 16, C5 — all < 500 |

Gate E note: `grep -c` exits 1 when a pattern is absent, which is the PASS
condition here; the recorded numbers are the counts, all zero.
Paths in 7f622b7f..HEAD: `.agent/authored/f105-r41-1.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
`tests/orchestration/test_intake.py`, `tests/orchestration/test_flight_plan.py`,
`tests/orchestration/test_prompt_trace.py`, `apps/cli/commands/do_cmd.py`.

## Transport proof
`.remedy-wt/f105-r41-1.block.md`, `.agent/authored/f105-r41-1.md` and
`.agent/last_block.md` all three hash to
`58b153128ab2711982bfed1163a80f6286ab2f9c0716d060390594b155773baf`
at 383 lines; both `cmp` runs silent. PRIMARY shape, not the §4.9 fallback.

## Pair proof
Every pair SLICED from the COMMITTED authored file by a whole-line marker reader
(`.remedy-wt/r41_slice.py`, gitignored); nothing retyped. Every FROM verified 1x
in its target BEFORE its write (`.remedy-wt/r41_precheck.py`); reconciliation by
`.remedy-wt/r41_reconcile.py`.
| Pair | Declared | Measured | Before | After |
|---|---|---|---|---|
| PAIR_ID | REWRITE | REWRITE | FROM 1x | FROM 0x / TO 1x |
| PAIR_F | CONTAINS-FROM | CONTAINS-FROM | FROM 1x | FROM 1x / TO 1x at C2 (see note) |
| PAIR_S | CONTAINS-FROM | CONTAINS-FROM | FROM 1x | FROM 1x / TO 1x |
| PAIR_TI | CONTAINS-FROM | CONTAINS-FROM | FROM 1x | FROM 1x / TO 1x |
| PAIR_TF | CONTAINS-FROM | CONTAINS-FROM | FROM 1x | FROM 1x / TO 1x |
| PAIR_DO1 | REWRITE | REWRITE | FROM 1x | FROM 0x / TO 1x |
| PAIR_DO2 | REWRITE | REWRITE | FROM 1x | FROM 0x / TO 1x |
| PAIR_DO3 | REWRITE | REWRITE | FROM 1x | FROM 0x / TO 1x |
| PAIR_GUARD | CONTAINS-FROM | CONTAINS-FROM | FROM 1x | FROM 1x / TO 1x |
| PAIR_P_PLAN | FULL REPLACEMENT | FULL REPLACEMENT | n/a | cmp silent, 37 lines |

PAIR_F note, measured not assumed: at C2 the whole TO occurred 1x. At C5 the
block's own instruction put `Landed: R-0263` directly below the last line of the
R-0263 entry — which IS PAIR_F's FROM and PAIR_F's first TO line — so the TO is
no longer one contiguous run in the final file: the FROM line occurs 1x, the
remaining 14 TO lines occur 1x, and the whole-block count is 0. The R-0264 entry
itself is byte-intact; only contiguity was broken, by design. Every other pair
still measures its declared shape in the FINAL committed files
(`.remedy-wt/r41_postcheck.py`).

## Red-proofs (gate J) — worktree `.remedy-wt/r41-red` at 3e2fa6bc, since removed
| # | Mutation | Outcome |
|---|---|---|
| J1 | `intake.py`: ternary → `_build_intake_prompt(mission),` | RED — `test_intake.py::TestRunIntakeAcceptsAComposedPrompt::test_composed_text_is_the_prefix_the_provider_sees`, 1 failed 67 passed |
| J2 | `flight_plan.py`: ternary → `prompt = _build_plan_prompt(intake)` | RED — `test_flight_plan.py::TestPlanJobLlmAcceptsAComposedPrompt::test_composed_text_is_the_prefix_the_provider_sees`, 1 failed 67 passed |
| J3 | `do_cmd.py`: delete `composed=plan_composed,` | RED — `test_prompt_trace.py::TestSegmentManifest::test_every_cli_call_site_hands_its_composition_down`, 1 failed 41 passed |
Each mutation was reverted before the next; the worktree was removed with
`git worktree remove --force` and `git worktree prune`. The primary checkout was
never mutated and is `git status --porcelain` EMPTY.

## Deviations, declared
1. This file is 127 lines, over the 60-line cap (DECISION D15 stated-cause
   overage). Cause: the mandated content — the nine-row changed-files table, the
   six-row item-status table, the eighteen-row gate table with real exit codes,
   the ten-row pair-shape proof, the transport proof and the three red-proof
   rows. No section was dropped and no prose was added to pad it.
2. None other. Every C item landed as specified; no block instruction turned out
   unsatisfiable and no gate came back a colour the block did not expect.

## Open findings
5 — R-0221, R-0239, R-0247, R-0262, R-0264 (registered this round).
R-0256 and R-0263 carry worker `Landed:` lines only; per §4.4 only the reviewer's
`Done:` text resolves them. `LAST_REVIEWED_SHA` is 7f622b7f — R40 is GATED PASS
and that gate is now on disk in `.agent/live_review.md`.

## Next expected action
1. Reviewer gates R41 over `git diff 7f622b7f..HEAD` and re-runs gates A-K
   itself; on PASS `LAST_REVIEWED_SHA` advances 7f622b7f -> HEAD and R-0256,
   R-0263 and R-0264 get their `Done:` text.
2. Then T004: `remedy stats cache` over actuals.
3. Then the integration gate (docs/agents/integration_gate.md) — R-0221 will
   attribute phantom base-only failures there, expected, not new.
4. Then closure (docs/roadmap/STATUS_closure_protocol.md), where the evidence
   job, the FRESH review zip, the STATUS line and the PR all land.
