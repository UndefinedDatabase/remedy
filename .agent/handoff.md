# Handback — F031 Decision inbox, Round R51

Feature/round: F031 R51 — the SERVER half of the clarification form.
Branch: `feature/f031-decision-inbox`. Tip before C6: `dac7a471`.

## Range

Review of `242144ff..HEAD`.

## Commits

### 0cb63fd6 docs(agent): save the F031 R51 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r51.md | +441/-0 | C0a — the block saved verbatim |

### 2b12be4a docs(agent): mirror the F031 R51 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +317/-222 | C0b — same bytes, same blob `516c218a` |

### 596ff616 docs(agent): advance the plan to the F031 R51 form round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +14/-16 | C1 — PLANF031R51 |

### 024f3730 docs(agent): record the F031 R50 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2 — LEDGER51 appended |

### 8fb2b0de docs(agent): rule DECISION F031 D26 on the clarification form
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +30/-0 | C3 — DECISION26 appended |

### 1ff29dda feat(ui-server): accept validated clarification answers on flight-plan approval
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +49/-9 | C4 — S1 helper, S2 call site, S3 docstring |
| packages/orchestration/decision_inbox.py | +6/-2 | C4 — S4, the door's third refusal |

### dac7a471 test(ui-server): pin the operator answer reaching the stored record
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_dispatch.py | +27/-2 | C5 — S5 optional `answers`, S6 effect test |

### C6 docs(agent): write the F031 R51 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C6 — this file; a handback cannot table its own commit (R-0149) |

Every `+/-` cell above is read from `git diff --numstat` itself and agrees cell for cell with G7.

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

## External actions

`git worktree add --detach .remedy-wt/f031-r51-probe dac7a471` — created for G6(d).
`git worktree remove --force .remedy-wt/f031-r51-probe` — removed by exact path; list back to 1 line.
`git push origin feature/f031-decision-inbox` — run after C6. No `gh` command, no PR action.

## Verification — one line per gate, REAL exit codes

- G1 exit 0 — branch correct; `git status --porcelain` 0 lines after C0a, C0b, C1, C2, C3, C4, C5; `.agent/STOP` read off disk before C0a and before C6, ABSENT both times; the block is sha256 `fe15be6b…a92825f0`, 30931 bytes, 441 lines at C0a, at C0b and as read off disk at C5 — all three EQUAL — and C0a and C0b are the SAME git blob `516c218a`.
- G2 exit 0 — extractor printed 13 slices from the COMMITTED C0a blob; CONTENT 178, TOTAL 441, PROSE 263. PROSE 263 ≤ 400 and TOTAL 441 ≤ 490.
- G3 exit 0 — `.agent/plan.md` at C1 byte-equal to PLANF031R51 TRUE; minus-trailing-newline control FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 45 (<50).
- G4 exit 0 — live_review base read 893819 as the block named: 893819 + 1 + 4236 = 898056 = post. N counted by my script = 1, so paragraph 1 IS also the last; units 366→367; reader 2 matches. decisions base read 613277 as named: 613277 + 1 + 1957 = 615235 = post; N = 4; units 1478→1482; reader 2 matches. The byte flipped in memory inside paragraph 1 of each slice is REJECTED by BOTH readers on BOTH appends. No tracked file was mutated; past blobs read via `git show`.
- G5 exit 0 — before C2 / after C2 / after C5: `^- R-\d+ — ` 263/263/263, `^Done: R-\d+ — ` 8/8/8, `^Landed: R-` 0/0/0, `^Gate: R\d+ — ` 19/19/19, `^Gate: F\d+ R\d+ — ` 31/32/32 with gate keys ADDED {F031 R50} and REMOVED {} at C2 and both empty at C5; no id added or removed anywhere; all ids DISTINCT, maximum `R-0702`; open set 255 before C2 and 255 after C5. `^## DECISION F031 D\d+ ` 25 before C3 and 26 after, ADDED {D26}, REMOVED {}.
- G6 exit 0 — (a) at C4 ui_server.py: S1HELPER 1x, S2FROM 0x, S2TO 1x, S3FROM 0x, S3TO 1x, `answers={}` 0x over the whole file; decision_inbox.py: S4FROM 0x, S4TO 1x, `exactly two conditions` 0x; `git diff --name-only C3..C4` is exactly those two paths. (b) at C5: S5FROM 0x, S5TO 1x, S6NEW 1x; `git diff --name-only C4..C5` is that one path only. (c) `python3 -m ruff check` over the three files at C5 REAL exit 0. (d) the three-line sequence counted 1 in the worktree copy; after replacing it, pytest in that worktree returned a REAL exit code of 1 — non-zero, as required; worktree removed by exact path, `git worktree list` back to 1 line.
- G7 exit 0 — path set of `242144ff..dac7a471` both residues EMPTY against the expected eight paths; `git diff --stat` restricted to `apps/` and to `docs/` both EMPTY; `^<<<SLICE ` and `^<<<END ` are 0 and 0 in plan.md at C1, live_review.md at C2, decisions.md at C3, ui_server.py at C4 and test_command_dispatch.py at C5, against a CONTROL of 13 and 13 over the C0a blob; insertions 441, 317, 14, 2, 30, 55, 27, each commit single-parent and under 500; `git ls-files .remedy-wt` 0 lines; `git worktree list` 1 line at C5; the reflog entries for THIS round's seven commits all read prefix `commit`, with `amend`, `rebase` and `cherry` 0 each among them.
- G8 exit 0 — all eight suites REAL exit 0, run serially: canary 42, `tests/ui_server/` 487, test_test_runner.py 52, test_resource_safety.py 21, test_integrity_gate.py 16, test_decision_inbox.py 35, test_plan_approval.py 27, test_decision_answers.py 29.

THE BRANCH TIP IS GREEN. G6's PROBE RETURNED A REAL EXIT CODE OF 1 — non-zero, so reverting the feature turns the effect test red and the door carries the answers rather than dropping them. THE THREE MUST-NOT-MOVE SUITES DID NOT MOVE: 35, 27 and 29, exactly as measured at `242144ff`. `tests/ui_server/` reads 487 against the reviewer's 486 — one higher, the one test S6 adds, and no other test under that path changed.

## Authored-text proofs

All 13 slices were extracted from the COMMITTED C0a blob, never from the prompt, and applied byte for byte by exact-substring replacement with a pre-count assertion of 1 on every FROM and anchor. Post-application counts are in G6. Base counts at `242144ff` matched the block's claims exactly: S2FROM 1x, S3FROM 1x, S4FROM 1x, S5FROM 1x, both anchors 1x, and `TO contains FROM` false for all four pairs.

## Deviations & assumptions

None. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was followed exactly, with no extra, dropped or reordered commit. No finding was registered or resolved. Open findings: 255.

## Next

1. Re-read `.agent/STOP` from disk. 2. Run the Open PR Gate. 3. Review this round's handback. 4. R52 — the BROWSER half of the form plus the tests pinning DECISION F031 D26's two refusals.
