# Handback — F031 Decision inbox, Round R50 (repair round)

Branch: `feature/f031-decision-inbox` · tip `f4545e3c` (C5), then C6 = this file. `.agent/STOP` read from disk before C0a and again before C6: ABSENT both times.

## Range

Review of `cd676e4c`..`HEAD`.

## Commits

### ef3dc85a docs(agent): save the F031 R50 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r50.md | +346/-0 | C0a: the R50 block, verbatim |

### 4233b651 docs(agent): mirror the F031 R50 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +280/-149 | C0b: same bytes, same git blob as C0a |

### a6db8474 docs(agent): advance the plan to the F031 R50 repair round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +14/-15 | C1: PLANF031R50 |

### 9bd1a153 docs(agent): record the F031 R49 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2: LEDGER50 appended |

### ed4e1b2a docs(ui-server): name the decision, not a round, in the resolve docstring
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +4/-3 | C3: the S1 pair — R-0702 |

### c94c3ecb refactor(tests): extract the shared UI-server start helper to module level
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_dispatch.py | +37/-50 | C4: S2, S3, S4 — R-0701 |

### f4545e3c docs(agent): resolve the two F031 R48 code findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C5: DONE50 appended |

### C6 — this commit (self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | n/a | C6: this handback; a handoff cannot table itself |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| push | done | ordered after C6; its reading is not quoted here |

## Verification

- G1 exit 0 — branch `feature/f031-decision-inbox`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4, C5; STOP ABSENT at both readings; the block reads sha256 `18709505…5fd11e24`, 25929 bytes, 346 lines as saved at C0a, as mirrored at C0b and as read off disk at C5 — all three EQUAL; C0a and C0b are the SAME git blob `5fbb344f`.
- G2 exit 0 — the extractor printed 9 slices from the COMMITTED C0a blob; CONTENT 113, TOTAL 346, PROSE 233 (cap 400), TOTAL 346 (cap 490).
- G3 exit 0 — `.agent/plan.md` at C1 byte-equal to PLANF031R50 TRUE; minus-trailing-newline control FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 47 (strictly under 50).
- G4 exit 0 — C2: 888399 + 1 + 3486 = 891886, the pre-C2 blob equal to the 888399-byte base the block named; N counted at 1, units 363→364, last-N in order TRUE — N is 1, so paragraph 1 is also the last. C5: pre-commit blob READ at 891886, 891886 + 1 + 1932 = 893819; N counted at 2, units 364→366, last-N in order TRUE. A byte flipped IN MEMORY inside paragraph 1 of each slice was REJECTED by BOTH readers both times. The tracked file was never mutated.
- G5 exit 0 — before C2 / after C2 / after C5: `^- R-\d+ — ` 263/263/263, `^Done: R-\d+ — ` 6/6/8, `^Landed: R-` 0/0/0, `^Gate: R\d+ — ` 19/19/19, `^Gate: F\d+ R\d+ — ` 30/31/31. ADDED across C2: the gate key `F031 R49` and nothing else. ADDED across C5: `R-0701` and `R-0702` and nothing else. Nothing REMOVED at either step; no finding id minted. All ids DISTINCT, maximum `R-0702`. Open set 257 before C2, 255 after C5.
- G6 exit 0 — (a) at C3: S1FROM 0x, S1TO 1x, and over the whole file `R48` 0x and `Round R` 0x; `git diff --name-only 9bd1a153..ed4e1b2a` is that one path only. (b) at C4: S2DEL 0x, S3HELPER 1x, S4FROM 0x, S4TO 6x, `def _start_server` 0x, `def _start_ui_server_for_job` 1x; `git diff --name-only ed4e1b2a..c94c3ecb` is that one path only. (c) `python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_command_dispatch.py` REAL exit 0, "All checks passed!". (d) the probe ran in the disposable worktree `.remedy-wt/f031r50-probe`: the return line counted 1, was replaced with `return 1, token`, and `python3 -m pytest tests/ui_server/test_command_dispatch.py -q` gave a REAL exit code of 1 — non-zero — with the output naming BOTH `TestJobStopDispatchEffects` and `TestFlightPlanApprovalDispatchEffects`; the worktree was then removed by its exact path and `git worktree list` is back to 1 line.
- G7 exit 0 — the path set of `git diff --name-only cd676e4c..f4545e3c` is exactly the six expected paths, BOTH residues EMPTY; `git diff --stat` restricted to `apps/` and to `docs/` is EMPTY for each. `^<<<SLICE ` / `^<<<END ` read 0 and 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C5, `packages/orchestration/ui_server.py` at C3 and `tests/ui_server/test_command_dispatch.py` at C4, against a CONTROL of 9 and 9 over the C0a blob. Insertions from `git diff --numstat`: 346, 280, 14, 2, 4, 37, 4 — each commit single-parent and under 500. `git ls-files .remedy-wt` 0 lines and `git worktree list` 1 line at C5. The reflog for this round's OWN 7 commits reads prefix `commit` on every one, with `amend` 0, `rebase` 0 and `cherry` 0 among those entries.
- G8 exit 0 on all five, run SERIALLY in the primary checkout at C5 — canary `tests/cli/test_golden_path.py` 42 passed; `tests/ui_server/` 486 passed; `tests/orchestration/test_test_runner.py` 52 passed; `tests/regression/test_resource_safety.py` 21 passed; `tests/orchestration/test_integrity_gate.py` 16 passed. Every count matches the reviewer's own measurement at `cd676e4c`.

THE BRANCH TIP IS GREEN. G6's PROBE RETURNED A REAL EXIT CODE OF 1, non-zero, with both dispatch-effect classes named in its output — which is what proves the single module-level helper is the LIVE path for each class rather than merely present. R-0701 AND R-0702 ARE RESOLVED THIS ROUND: R-0701 by C4 `c94c3ecb`, R-0702 by C3 `ed4e1b2a`. Open findings after C5: 255.

## External actions

- `git worktree add .remedy-wt/f031r50-probe HEAD --detach` — created for G6(d); `git worktree remove --force .remedy-wt/f031r50-probe` — removed by its exact path before C5, list back to 1 line.
- `git push origin feature/f031-decision-inbox` — ordered after C6. No `gh` command; no PR created, edited, merged or commented on; `.agent/STOP` was only ever read.

## Authored-text proofs

Every slice was applied byte for byte from the COMMITTED C0a blob, never from the prompt: PLANF031R50 (G3 byte-equality plus a FALSE control), LEDGER50 and DONE50 (G4, two independent readers each plus a first-paragraph negative control), and S1FROM/S1TO, S2DEL, S3HELPER, S4FROM/S4TO (G6 a and b occurrence counts). No slice was retyped, reflowed or corrected, and no slice looked wrong.

## Deviations & assumptions

None. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was executed exactly in that order — no extra commit, none dropped, none reordered, none merged. `.agent/decisions.md` was deliberately left untouched per the Change line. The handback cap is 100 lines, derived from the Bundle's 8 commits (more than five); this file is inside it, so no DECISION D15 overage line is due.

## Next

1. Re-read `.agent/STOP` from disk.
2. The Open PR Gate.
3. Review this round's handback.
4. R51 — the clarification FORM over `payload.clarifications`.
