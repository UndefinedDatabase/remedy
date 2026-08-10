# Handoff — F105 R34: repair the unsatisfiable guard, label the run command

Branch: feature/f105-cache-optimal-prompt-ordering. Review of af35adbc..HEAD.
Commits: b3cd8145 (C1a), 64d6f018 (C1b), a6e660df (C2), 3c651516 (C3),
083a42d3 (C4), f3968dfd (C5), 32d4c78d (C6), plus this C7 commit.

## Commits

### b3cd8145 save the R34 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r34-1.md | +398/-0 | the block, byte-identical to the original |

### 64d6f018 mirror the R34 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +334/-229 | the same 398 lines |

### a6e660df record the R33 gate, findings R-0258 and R-0259, and D12 and D13
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +81/-1 | PAIR_A next free ID; PAIR_B R-0258 + R-0259, both OPEN; PAIR_C the R33 PASS record |
| .agent/decisions.md | +42/-0 | PAIR_D: DECISIONs D12 and D13 |

### 3c651516 add pre-emission checklist item 7 for unnamed source guards
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +12/-0 | PAIR_E: §3 item 7, the R-0258 fix |

### 083a42d3 scope the mission_cmd provider guard to its own call site
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_mission_compiler.py | +7/-1 | PAIR_F: the file-wide `source.count(...) == 1` becomes a window on the plan call |

### f3968dfd name the provider on the mission run loop call
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/mission_cmd.py | +7/-1 | PAIR_G: `provider`/`provider_kind` on the `run_mission` call |
| packages/orchestration/gauntlet_runner.py | +7/-0 | PAIR_H: the deliberate absence of a label (D13) |

### 32d4c78d pin the run command provider label at its call site
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_orchestrator_loop.py | +17/-0 | 4th test of `TestOrchestratorEvidenceSink`, scoped to `result = run_mission(`; nothing asserted about the gauntlet |

### C7, this commit (a handoff cannot table its own commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | replaced | PAIR_I verbatim, 43 lines |
| .agent/handoff.md | rewritten | this file |

## Items
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | |

## Verification (real exit codes, real output)
| Gate | Exit | Output |
|---|---|---|
| A transport | 0 | all three files `6d816a6434c6d98cdaafca3df7654580d2c5985abdef65398c9eccb8fb97c14e`; three `cmp` runs silent |
| B size | 0 | `398 .agent/authored/f105-r34-1.md` — cap 400 (D5) |
| C application | 0 | the proofs below; PAIR_I `cmp` against the sliced text silent, 43 lines < 50 |
| D markers | 1 (no-match) | `0` in live_review.md, decisions.md, plan.md, planner_reviewer_prompt.md |
| E guard alone, AT C4 | 0 | `test_mission_compiler.py` `121 passed in 0.70s` before the label landed |
| F scoped | 0 | compiler + loop + prompt golden `323 passed in 1.63s`; the frozen render still `==` |
| G callers | 0 | mission_cmd + gauntlet_runner + mission_e2e `152 passed in 38.06s` |
| H docs + state | 0 | `tests/docs/` `294 passed in 0.30s`; dashboard contract `70 passed in 4.01s` |
| I canary | 0 | golden path `42 passed in 19.64s` |
| J red-proofs | 0 | baseline, both guards: `2 passed in 0.36s`. M1, dropping the label from the `run_mission` call: `1 failed, 1 passed` — the C6 test RED, `test_the_cli_names_the_provider_it_planned_with` GREEN, so the two guards sit on different call sites. M2, moving the label onto the `plan_mission` call so the file-wide count is 2 either way (measured 2): `1 failed, 1 passed` — the C6 test RED, so the repaired guard is per-call-site and not a disguised count. Neither came back green. Disposable worktree at 32d4c78d, `PYTHONDONTWRITEBYTECODE=1`, each revert proved by empty `git diff --stat` AND `git status --porcelain`, worktree removed and pruned |
| K hygiene | 0 | insertions per commit 398, 334, 123, 12, 7, 14, 17 — each under 500; `git status --porcelain` empty; `git worktree list` the primary alone |
| L scope | 0 | nine paths through C6 plus C7's `plan.md` and `handoff.md` = the eleven the Change line names, nothing else. K and L measured AFTER C6: a commit cannot state its own stat |

## Authored-text proofs
All three transport files carry
`6d816a6434c6d98cdaafca3df7654580d2c5985abdef65398c9eccb8fb97c14e`, every `cmp`
silent, 398 lines. Every pair was sliced from the COMMITTED authored file by
whole-line markers, never retyped. DECLARED vs MEASURED shape, all nine agree:
PAIR_A REWRITE/REWRITE, PAIR_B REWRITE/REWRITE, PAIR_C and PAIR_D
CONTAINS-FROM/CONTAINS-FROM, PAIR_E CONTAINS-FROM/CONTAINS-FROM, PAIR_F and
PAIR_G REWRITE/REWRITE, PAIR_H CONTAINS-FROM/CONTAINS-FROM, PAIR_I a full
replacement proved by `cmp`. Rewrites: FROM 0x and TO 1x after the write.
Appends: FROM exactly 1x after. ADDED-line reconciliation per path over that
path's own commit, both directions, 0 strays each: live_review.md +81/-1 against
PAIR_A + PAIR_B + PAIR_C TOGETHER (1 + 36 + 44 = 81 added, 1 removed);
decisions.md +42/-0 (PAIR_D); planner_reviewer_prompt.md +12/-0 (PAIR_E);
mission_cmd.py +7/-1 (PAIR_G); gauntlet_runner.py +7/-0 (PAIR_H).

## External actions
`git worktree add --detach .remedy-wt/r34-redproof HEAD`, then `remove` and
`prune` — gone, `git worktree list` the primary alone. `git push` after C7. No PR.

## Deviations, declared
One declared-vs-measured mismatch, reported rather than worked around: PAIR_F's
prose says the 200-character window "covers the plan call's own two lines and
nothing after them". MEASURED, it spans FOUR lines — the plan call's two plus the
first `except` clause and part of the next `print`, 71 characters past the call.
The slice was applied BYTE FOR BYTE anyway and the property still holds: the next
`provider_kind="ollama"` lies ~7000 characters later at the `run_mission` call,
so the guard stays scoped to the plan site, and M2 proves it. C6 reuses 200 for
symmetry. No code was adjusted to accommodate the wording.
Length (DECISION D15): 120 lines, over the 100 the 8-commit case allows. Cause,
mandated content only: eight per-commit tables, the twelve-row gate table, the
nine pair proofs with declared-vs-measured shapes, the item-status table and this
mismatch statement.

Open findings: 5 — R-0221, R-0239, R-0247, R-0256, R-0259, exactly as PAIR_I's
plan states. R-0258's live_review entry stays OPEN as the reviewer authored it;
its fix landed here. Landed: R-0258 — §3 checklist item 7 plus the per-call-site
repair of the `test_mission_compiler.py` guard.

## Next
Gate R34 over `af35adbc..HEAD`. Then the R-0259 round: MOVE the misfiled R-0257
block (live_review.md 1528-1554) to the end of `## Findings`, bytes unchanged.
