# Handoff — F105 R33: the orchestrator prompt's call evidence

Branch: feature/f105-cache-optimal-prompt-ordering. Review of cab89962..HEAD.
Commits: cd499612 (C1a), cb6ae21a (C1b), c35a7c05 (C2), d7645f08 (C3),
d2ba6a21 (C4), fbc01401 (C5), plus this C6 commit.

## Commits

### cd499612 save the R33 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r33-1.md | +293/-0 | the block, byte-identical to the original |

### cb6ae21a mirror the R33 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +232/-135 | the same 293 lines |

### c35a7c05 record the R32 gate and DECISION D11
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +46/-0 | PAIR_A: R32 round line + PASS record |
| .agent/decisions.md | +33/-0 | PAIR_B: DECISION D11 |

### d7645f08 record the orchestrator prompt manifest per iteration
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/orchestrator_loop.py | +77/-2 | `make_orchestrator_call_recorder`; compose ONCE per iteration; `run_mission` gains `provider`/`provider_kind`; `on_call` CHAINED, not replaced |

### d2ba6a21 append orchestrator call traces to the mission evidence dir
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/orchestrator_loop.py | +27/-7 | per-iteration `append_trace_jsonl` in a `finally`, so a RAISED call still leaves evidence; no call, no file |

### fbc01401 pin the orchestrator evidence sink and its append rule
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_orchestrator_loop.py | +55/-0 | `TestOrchestratorEvidenceSink`, three tests |

### C6, this commit (a handoff cannot table its own commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | replaced | PAIR_C verbatim, 43 lines |
| .agent/handoff.md | rewritten | this file |

## Items
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | deviated | items 1-2 landed; item 3, the CLI label, unapplied — see Deviations |
| C5 | deviated | tests 1-3 landed; test 4 would guard an unapplied line |
| C6 | done | |

## Verification (real exit codes, real output)
| Gate | Exit | Output |
|---|---|---|
| A transport | 0 | all three `d6d9d2a8e0d03d646021ed101d7c5b83dacce65b66dc75c74e5ea92306f40d80`; three `cmp` runs silent |
| B size | 0 | `293 .agent/authored/f105-r33-1.md` — cap 400 (D5) |
| C application | 0 | the proofs below |
| D markers | 1 (no-match) | `0` in live_review.md, decisions.md, plan.md |
| E scoped | 0 | loop + prompt golden `201 passed in 1.17s`; the frozen render still `==` |
| F callers | 0 | mission_cmd + gauntlet_runner + mission_e2e `152 passed in 41.26s` |
| G state files | 0 | `tests/docs/` `294 passed in 0.29s`; dashboard `70 passed in 4.37s` |
| H canary | 0 | golden path `42 passed in 20.57s` |
| I red-proofs | 0 | M1 `2 failed, 1 passed` (tests 1+2 RED, as ordered); M2 `1 failed, 2 passed` (test 2 RED, test 1 GREEN, as ordered); M3 NOT runnable — `provider="ollama"` was never added. Worker substitute, not ordered: dropping the label inside `run_mission` gives `1 failed, 2 passed`, test 1 RED, so the label is pinned — the CLI's passing of it is not. Disposable worktree at HEAD, `PYTHONDONTWRITEBYTECODE=1`, each revert proved by an empty `git diff --stat`, worktree removed and pruned |
| J hygiene | 0 | insertions 293, 232, 79, 27, 55, 105 — each under 500; `git status --porcelain` empty; `git worktree list` the primary alone |
| K scope | 0 | eight paths, all on the Change line; `mission_cmd.py` absent by declared deviation. J and K re-measured AFTER C6: a commit cannot state its own stat |

## Authored-text proofs
All three transport files carry
`d6d9d2a8e0d03d646021ed101d7c5b83dacce65b66dc75c74e5ea92306f40d80`, every `cmp`
silent, 293 lines. PAIR_A and PAIR_B sliced from the COMMITTED authored file by
whole-line markers: declared APPEND, MEASURED APPEND — each TO opens with its
FROM verbatim; FROM 1x before and after, TO 0x before and 1x after, in its own
target. TO-only lines 46 and 33; c35a7c05 is +46/-0 over live_review.md and
+33/-0 over decisions.md, so strays are 0 both directions on both paths. PAIR_C:
`cmp` against the applied `.agent/plan.md` silent, 43 lines < 50.

## External actions
`git worktree add --detach .remedy-wt/r33-redproof HEAD`, then `remove` and
`prune` — gone. `git push` after C6. No PR.

## Deviations, declared
C4 item 3 and C5 test 4 are unapplied: the block contradicts the existing suite.
`tests/orchestration/test_mission_compiler.py:1210` asserts
`source.count('provider_kind="ollama"') == 1` over the WHOLE of `mission_cmd.py`;
the second label makes it `assert 2 == 1` — measured with the edit applied, not
predicted. The repair belongs in that test file, which the Change line forbids,
so the CLI edit was reverted rather than landed red. Consequence: BOTH
`run_mission` callers now write UNLABELLED rows, so D11's consequence paragraph
understates the gap by one caller and PAIR_C's Next Steps names only the
gauntlet. Both are reviewer-authored and were applied verbatim; this is the
correction. Pre-existing, untouched: `ruff check
tests/orchestration/test_orchestrator_loop.py` reports I001 at HEAD too.
Length (DECISION D15): 107 lines, over the 100 the 7-commit case allows. Cause,
mandated content only: seven per-commit tables, the eleven-row gate table, the
pair proofs, the item-status table and this contradiction statement.

Open findings: 4 — R-0221, R-0239, R-0247, R-0256. None resolved this round.

## Next
Gate R33 over `cab89962..HEAD`. Then ONE round naming the provider at both
`mission_cmd.py:366` and `gauntlet_runner.py:514`, repairing the
`test_mission_compiler.py` guard into a per-call-site assertion.
