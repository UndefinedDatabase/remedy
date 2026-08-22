# Handback — F009 R25 (record round: the R24 verdict, closing the session)

Round base: `c20cd5cb9c68bddf1d30c54630e6d06760f989f9`

Fortschritt: ~90 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             Kommandos dispatchen und sind beidseitig wirkungsgeprüft; offen
             bleiben das SSE-Event, der Import-Guard und die 405-Routenprobe) —
             Schätzung

## Range

Review of `c20cd5cb..84f81a31`; C3 adds this file on top.

## Items

| Item | Status | Reason      |
|------|--------|-------------|
| C0a  | done   |             |
| C0b  | done   |             |
| C1   | done   |             |
| C2   | done   |             |
| C3   | done   | this commit |

## Commits

### cf658e26 docs(state): save the F009 R25 record block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f009-r25.md` | +176/-0 | C0a saves the received block |

### 5212f39a docs(state): mirror the F009 R25 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +82/-189 | C0b mirrors the committed C0a blob |

### 7bf5bb21 docs(state): set the plan to the F009 R25 record round
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +4/-4 | C1 applies PLANF009R25 |

### 84f81a31 docs(review): record the R24 verdict as clean
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2/-0 | C2 appends LEDGER25 |

### C3 docs(state): write the F009 R25 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | self-reference | a handoff cannot table its own commit (R-0149); its numbers are in the round report |

## External actions

`git push` after C3; its outcome is in the round report. No worktree added or removed, no PR created or edited, no `gh` command run.

## Verification

- G1 PASS — `.agent/STOP` absent before C0a and before C3; branch reads `feature/f009-single-write-channel`; `git status --porcelain` 0 lines after each of C0a, C0b, C1 and C2; round base `c20cd5cb9c68bddf1d30c54630e6d06760f989f9`. Transcripts are in the round report, not here (R-0582), and that holds for every line below.
- G2 PASS — `.agent/authored/f009-r25.md` at C0a, `.agent/last_block.md` at C0b and the received bytes are all sha256 `0de7a901…` over 16694 bytes and 176 lines; C0b was written from the committed C0a blob, not from the scratch copy.
- G3 PASS — the script extracted and printed an aggregate of 2 slices from the C0a blob: PLANF009R25 `bcda0e23…`/2039 B/37 L and LEDGER25 `4f76e1ab…`/5479 B/1 L, summing 38 CONTENT lines; re-measured from that same blob, TOTAL 176 and PROSE 138, matching constraint 6 and under D6's 490 and D5's 400.
- G4 PASS — `cmp` exits 0 and both sha256 read `bcda0e23…`; the negative control against `.agent/last_block.md` exits 1 at byte 1; `wc -l` 37 under the 50-line cap; `^## Goal$` and `^## Next Steps$` each read 1.
- G5 PASS — (a) the round-base blob is a byte-exact prefix and the remainder is exactly a newline plus LEDGER25, sha256 `590b1061…`, 5480 bytes, 2 lines; (b) N counted at 1 by the script and the last blank-line unit equals the slice's paragraph. A `G`→`X` flip at equal length in the FIRST appended paragraph is REJECTED by both readers while both ACCEPT the true file. 524945→530425 bytes, 1116→1118 lines.
- G6 PASS — line-anchored at line START, base then C2: leading `- R-` 207 and 207 with every captured id DISTINCT at each; `Done: R-` 3 and 3; `Landed: ` 0 and 0; `Gate: R` 24 and 25 over that many DISTINCT keys; `Gate: R25` 0 and 1; `- R-0642` 0 at BOTH, this round having minted no id. Max REGISTERED id R-0641 at both; open by DECISION F009 D10's rule, measured at C2 `84f81a31`, 204. Declared reading: an UNANCHORED `R-\d+` scan returns 642 because LEDGER25's prose quotes that id while reporting its own zero-reading — the max REGISTERED id is R-0641.
- G7 PASS — `.agent/decisions.md` is sha256 `25f2d750fe6afd51f6c35f5a07d16f4cc61ef33a736702be6ec6211056a001d5` at the round base and the identical digest at C3.
- G8 PASS — run serially in the primary checkout, never in a worktree: `test_golden_path.py` exit 0 at the 42 passed it printed; the four-path group exit 0 at the 513 passed it printed.
- G9 PASS — the range base→C2 lists exactly the declared paths other than this file, set difference EMPTY in both directions, 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/`; every commit has ONE parent; `git show --numstat` (no `--` before the SHA) and `git diff --numstat` AGREE on every cell and every cell equals this file's `+/-` column; pre-handback insertions 176, 82, 4 and 2, each under the 500 cap; leading `<<<SLICE ` and `<<<END ` read 0 LINES in both slice targets; `git ls-files .remedy-wt` 0; this round's reflog rows all classify as `commit`, with `amend`, `rebase` and `cherry` each 0 and no whole-reflog total asserted; `git worktree list` 1 line throughout.
- G10 PASS — every mandated section is present, an item row exists for each of C0a, C0b, C1, C2 and C3, the round base SHA is stated, each gate has one line, and the block's `Fortschritt:` line is repeated verbatim across all four of its lines. `wc -l` reads 78 against the 100-line cap, whose stated cause is the five per-commit tables the template mandates plus the ten gate lines; no section was dropped to meet 60.

## Authored-text proofs

Both slices were extracted programmatically from the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines and applied byte for byte; `cmp` on `.agent/plan.md` exits 0 against PLANF009R25 and the LEDGER25 application is proved by G5. No marker line reached any target file.

## Deviations & assumptions

None. The commit sequence executed is exactly C0a, C0b, C1, C2, C3 — no extra commit, no dropped commit, no reordering. No id was minted and none resolved, so the next free id is R-0642 exactly as when the round started. No production code and no test were written; nothing under `packages/`, `apps/`, `tests/` or `docs/` was touched and `.agent/decisions.md` was not touched.

## Next

This is the LAST round of the session. The next session's FIRST action is Phase 1 rule 1 of docs/agents/self_drive_protocol.md — the `.agent/STOP` re-read; its SECOND is the AGENTS.md Open PR Gate. The work that follows is the `command.accepted` SSE event on the F008 stream.
