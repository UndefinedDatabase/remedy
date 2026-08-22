# Handback — F009 R26 (the `command.accepted` SSE event)

## Range

Review of `cd77e969`..HEAD. Round base SHA `cd77e969c97a885325d2b6b31be086750e7f0df0`, branch `feature/f009-single-write-channel`, no pull request created. The block's `Fortschritt:` line follows VERBATIM across all four of its lines:

Fortschritt: ~93 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             Kommandos dispatchen, sind beidseitig wirkungsgeprüft und melden
             sich jetzt auf dem SSE-Strom; offen bleiben der Import-Guard und
             die 405-Routenprobe) — Schätzung

## Commits

### 232e5a6a docs(state): save the F009 R26 block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r26.md | 451/0 | C0a — the received block, copied byte for byte |

### 392a94eb docs(state): mirror the F009 R26 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 366/91 | C0b — written from the committed C0a blob |

### 58b9932a docs(state): set the plan to the F009 R26 event round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 8/8 | C1 — PLANF009R26, byte-equal |

### a573210c docs(review): record the R25 verdict as clean
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — LEDGER26 appended |

### f36f46b2 docs(decisions): rule DECISION F009 D23 for the accepted event
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 16/0 | C3 — DECISION23 appended |

### 69b5f890 feat(ui-server): announce an accepted command on the job event stream
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | 40/0 | C4 — CONST, METH, and PUB at both accepted exits |

### 77114cd4 test(ui-server): pin the accepted event, its frame and its silences
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_channel.py | 112/0 | C5 — TESTS: four tests and two helpers |

### C6 docs(state): write the F009 R26 handback (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see report | C6 — this file; a handback cannot table its own commit, so its numstat is in the round report |

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

## External actions

- `git worktree add .remedy-wt/r26final 77114cd4 --detach` — created for G10's red proof; `git worktree remove --force` then `git worktree prune` removed it and `git worktree list` reads 1 line.
- `git push -u origin feature/f009-single-write-channel` — `cd77e969..77114cd4`, C0a through C5 pushed. C6 is pushed immediately after it is committed; that outcome is in the round report.
- No `gh` command was run. No PR created, edited or merged.

## Verification

- G1 — `.agent/STOP` ABSENT before C0a and again before C6; `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel`; `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5; round base read at step 0 is `cd77e969c97a885325d2b6b31be086750e7f0df0`.
- G2 — the authored blob at C0a and `.agent/last_block.md` at C0b are both sha256 `9db61842f2287d052a03e144b7437d0584fcd3b25aa98b2245a608345bdfa068`, 33832 bytes, 451 lines, and byte-equal to each other and to the block received; C0b was written from the committed C0a blob.
- G3 — the script extracted 11 slices over 218 CONTENT lines from the committed C0a blob; constraint 9 re-measures to TOTAL 451 and PROSE 233, both the block's own numerals.
- G4 — `cmp .agent/plan.md <PLANF009R26>` exits 0, both sha256 `05884bfa0fa6e8835e90ae2c68d0f7ab593d893378b8b7fafe65563722a97d35`; the negative control against `.agent/last_block.md` exits 1; `wc -l` 37 against the 50-line cap; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 — both appends pass both readers: (a) the base blob is a byte-exact prefix and the remainder is a newline plus the slice — LEDGER26 remainder `6b5e0603…` 5692 bytes 2 lines, DECISION23 remainder `1f88275c…` 3623 bytes 16 lines; (b) N counted BY THE SCRIPT is 1 and 8 and the last N blank-line units match in order; an equal-length printable-byte flip in the FIRST appended paragraph is REJECTED by both readers while both ACCEPT the true file; live_review 530425→536117 bytes and 1118→1120 lines, decisions 473798→477421 bytes and 6909→6925 lines.
- G6 — line-anchored at line START, round base then C2: leading `- R-` entries 207 and 207 with every id DISTINCT at each, leading `Done: R-` 3 and 3, leading `Landed: ` 0 and 0, leading `Gate: R` keys 25 and 26 over that many DISTINCT keys, the `Gate: R26` key 0 and 1, leading `- R-0642` 0 and 0; max REGISTERED id R-0641 at both; open by DECISION F009 D10's rule (line-anchored entries minus line-anchored `Done:` lines) 204 at C2.
- G7 — base FROM counts CONST 1, PUB 2, METH 1, TESTS 1 with every TO 0, whole-line and indent-agnostic AGREEING on every cell, read via `git show <base>:<path>` and never over the tracked file; after application every TO reads its FROM's base count (1, 2, 1, 1) and the REWRITE pair PUB reads FROM 0; my own script printed `TO contains FROM: true` for CONST, METH and TESTS and `false` for PUB.
- G8 — ordered equality holds: C4's diff adds exactly the 40 lines the CONST, METH and PUB applications introduce, compared as a list in file order, and C5's adds exactly the 112 lines of TESTS; `git show --numstat` reads 40/0 and 112/0, the two numbers the reviewer measured on its own dry run.
- G9 — run serially in the primary checkout: ruff over the two paths exit 0 "All checks passed!"; `tests/ui_server/test_command_channel.py` exit 0, 90 passed; the `tests/cli/test_golden_path.py` canary exit 0, 42 passed; the four-path group exit 0, 517 passed.
- G10 — in the disposable worktree only: the target line reads 2 whole-line and 2 indent-agnostic at C5, both agreeing; mutation (a) deleted both and exactly `test_an_accepted_command_reaches_the_sse_frame_it_announces`, `test_a_replay_announces_nothing_a_second_time` and `test_an_event_writer_that_raises_changes_neither_status_nor_body` failed (exit 1, 3 failed 87 passed); mutation (b) made the 409 clause announce and exactly `test_a_refused_command_announces_nothing` failed (exit 1, 1 failed 89 passed); neither set reaches the other; the worktree was removed and `git worktree list` reads 1 line.
- G11 — the range base→C5 lists exactly the 7 declared paths with the set difference EMPTY in both directions and 0 paths under `apps/` or `docs/`; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree cell by cell and every cell equals the `+/-` column above; pre-handback insertions 451, 366, 8, 2, 16, 40 and 112, each under the 500 cap; leading `<<<SLICE ` and `<<<END ` read 0 LINES in all five slice targets; `git ls-files .remedy-wt` reads 0; this round's 7 reflog rows all classify as `commit`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog.
- G12 — this file, whose own `wc -l` against the 100-line cap is reported with the full gate transcripts in the round report rather than here (R-0582).

## Authored-text proofs

The reviewer's emitted original still exists on disk at `.remedy-wt/f009-r26.md` and was verified at step 0, before C0a, as sha256 `9db61842…` over 33832 bytes and 451 lines — so the primary disk-to-disk proof was available this round. Every slice was extracted from the COMMITTED C0a blob by its `<<<SLICE `/`<<<END ` marker lines and applied by script: `.agent/plan.md` `cmp`s exit 0 against PLANF009R26 with a negative control at exit 1, both appends are byte-exact prefix-plus-remainder under two independent readers, and C4 and C5 pass §4.9 ordered equality against their slices.

## Deviations & assumptions

- G10 mutation (b) — the block orders "that SAME line, with `payload` in place of `accepted_body`, directly BELOW the `rejected_state` audit call". That call sits at 16-space indentation inside `if accepted_body is None:`, so inserting the line at its own 12 spaces is an IndentationError that would redden the whole module instead of the one named id. It was inserted at 16 spaces, matching the clause. Declared rather than silently repaired; the ordered outcome held exactly.
- No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5, C6 in that order, with no extra commit, no dropped commit and no reordering. No id was minted and none resolved; the next free id is R-0642, exactly as at the round start.

## Next

The reviewer reviews `cd77e969`..HEAD and issues the R26 verdict; the round after that lands the queue-only import guard.
