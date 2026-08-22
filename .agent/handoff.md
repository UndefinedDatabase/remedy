# Handback — F009 R24 (T003: test what R23 shipped untested)

Round base: `46189950838679a8bfc86db41e0ec935ba806cd1`

Fortschritt: ~90 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             Kommandos dispatchen und sind jetzt beidseitig wirkungsgeprüft;
             offen bleiben das SSE-Event, der Import-Guard und die
             405-Routenprobe) — Schätzung

## Range

Review of `46189950..689e57b0`; C4 adds this file on top.

## Items

| Item | Status | Reason      |
|------|--------|-------------|
| C0a  | done   |             |
| C0b  | done   |             |
| C1   | done   |             |
| C2   | done   |             |
| C3   | done   |             |
| C4   | done   | this commit |

## Commits

### 7a349543 docs(state): save the F009 R24 test block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f009-r24.md` | +283/-0 | C0a saves the received block |

### ac255fd0 docs(state): mirror the F009 R24 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +192/-373 | C0b mirrors the committed C0a blob |

### cf407fc0 docs(state): set the plan to the F009 R24 test round
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +12/-16 | C1 applies PLANF009R24 |

### 2be1e945 docs(review): record the R23 verdict as Gate R24
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2/-0 | C2 appends LEDGER24 |

### 689e57b0 test(ui-server): reach the decision.resolve 200 path and the 501 guard
| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_server/test_command_channel.py` | +76/-0 | C3 applies the TESTS pair |

### C4 docs(state): write the F009 R24 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | self-reference | a handoff cannot table its own commit (R-0149) |

## External actions

`git worktree add --detach .remedy-wt/r24-red 689e57b0` exit 0 and `git worktree remove --force .remedy-wt/r24-red` exit 0, for G10 only. `git push` after C4; its outcome is in the round report. No PR created or edited, no `gh` command run.

## Verification

- G1 PASS — `.agent/STOP` absent before C0a and before C4; branch reads `feature/f009-single-write-channel`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3; round base `46189950838679a8bfc86db41e0ec935ba806cd1`. Transcripts are in the round report, not here (R-0582), and that holds for every line below.
- G2 PASS — `.agent/authored/f009-r24.md` at C0a, `.agent/last_block.md` at C0b and the received bytes are all sha256 `fe07f2c3…` over 21814 bytes and 283 lines; C0b was written from the committed C0a blob.
- G3 PASS — the script extracted and printed 4 slices from the C0a blob: PLANF009R24 `5565a9ff…`/2025 B/37 L, LEDGER24 `655507b9…`/4814 B/1 L, TESTS_FROM `7c9ceb98…`/153 B/2 L, TESTS_TO `7ac5e8b1…`/4023 B/78 L, summing 118 CONTENT lines; re-measured TOTAL 283 and PROSE 165, under D6's 490 and D5's 400.
- G4 PASS — `cmp` exits 0 and both sha256 read `5565a9ff…`; the negative control against the TESTS_TO slice exits 1 at byte 1; `wc -l` 37 under the 50-line cap; `^## Goal$` and `^## Next Steps$` each read 1.
- G5 PASS — (a) the base blob is a byte-exact prefix and the remainder is exactly a newline plus LEDGER24, sha256 `d39271e7…`, 4815 bytes, 2 lines; (b) N counted at 1 and the last blank-line unit equals the slice's paragraph. A `G`→`X` flip at equal length in the FIRST appended paragraph is REJECTED by both readers while both ACCEPT the true file. 520130→524945 bytes, 1114→1116 lines.
- G6 PASS — base then C2: leading `- R-` 207 and 207 with every captured id DISTINCT at each; `Done: R-` 3 and 3; `Landed: ` 0 and 0; `Gate: R` 23 and 24 over that many DISTINCT keys; `Gate: R24` 0 and 1; `- R-0642` 0 and 0. Max REGISTERED id R-0641 at both; open by DECISION F009 D10's rule, measured at C2 `2be1e945`, 204.
- G7 PASS — `.agent/decisions.md` is sha256 `25f2d750fe6afd51f6c35f5a07d16f4cc61ef33a736702be6ec6211056a001d5` at the round base and the identical digest at C4.
- G8 PASS — whole-line and indent-agnostic AGREE at every count. Before C3 TESTS_FROM 1 and TESTS_TO 0; after C3 BOTH read 1, which is the after-state constraint 3 ordered for an APPEND-SHAPED pair. The script printed TO-contains-FROM as a contiguous line block = 1 under both readings, so the after-state is the authored append rather than a failed application.
- G9 PASS — run serially in the primary checkout: ruff exit 0 at "All checks passed!"; `test_command_channel.py` exit 0 at the 86 it printed; `test_golden_path.py` exit 0 at the 42 it printed; the four-path group exit 0 at the 513 it printed.
- G10 PASS — in the disposable worktree `git diff HEAD --numstat` reads 9/93 on `packages/orchestration/ui_server.py` alone and the file is byte-equal to the `9a47166c` blob; under that mutation the suite EXITS 1, and both tests this round adds are among the failures it named. Worktree removed; `git worktree list` back at 1 line.
- G11 PASS — the range lists exactly the declared paths, set difference EMPTY in both directions, 0 beginning `packages/`, `apps/` or `docs/`; every commit has ONE parent; `git show --numstat` (no `--` before the SHA) and `git diff --numstat` AGREE on every cell and every cell equals this file's `+/-` column; insertions 283, 192, 12, 2 and 76, each under the 500 cap; leading `<<<SLICE ` and `<<<END ` read 0 LINES in both slice targets; `git ls-files .remedy-wt` 0; this round's reflog rows all classify as `commit`, with `amend`, `rebase` and `cherry` each 0 and no whole-reflog total asserted.
- G12 PASS — every mandated section is present, an item row exists for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA is stated, each gate has one line, and the block's `Fortschritt:` line is repeated verbatim across all four of its lines. `wc -l` reads 86 against the 100-line cap, whose stated cause is the six per-commit tables the template mandates for a bundle of more than five commits.

## Authored-text proofs

All four slices were extracted programmatically from the COMMITTED C0a blob by their marker lines and applied byte for byte; `cmp` on `.agent/plan.md` exits 0 against PLANF009R24, and the LEDGER24 and TESTS applications are proved by G5 and G8. No marker line reached any target file.

## Deviations & assumptions

None. The commit sequence executed is exactly C0a, C0b, C1, C2, C3, C4 — no extra commit, no dropped commit, no reordering. No id was minted and none resolved; the next free id is R-0642. No file under `packages/`, `apps/` or `docs/` was touched, and `.agent/decisions.md` was not touched.

## Next

Reviewer verdict on R24, then the `command.accepted` SSE event on the F008 stream.
