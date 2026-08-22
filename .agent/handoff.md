# Handback — F009 R20 (T003, round two of DECISION F009 D19 — the dispatch effects)

Feature F009 "The single write channel", round 20, branch `feature/f009-single-write-channel`.
Round base SHA `7ac8d98c24e7b76b4f684ec6e6a95de99b98da2f`. `.agent/STOP` absent before C0a and before C4.
Open findings at C2 by DECISION F009 D10's rule: 202. Max id R-0639. This round minted R-0639 and resolved none.

Fortschritt: ~82 % (T001 gebaut · T002 gebaut · T003 begonnen: der
             `job.stop`-Dispatch steht und ist wirkungsgeprüft; offen bleiben
             `decision.resolve`, das SSE-Event, der Import-Guard und die
             405-Routenprobe) — Schätzung

## Range

Review of 7ac8d98c..HEAD.

## Commits

### dbca3df0 docs(state): save the F009 R20 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r20.md | 329/0 | C0a — the block saved byte for byte from the scratch copy |

### 54120f8a docs(state): mirror the F009 R20 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 251/410 | C0b — written from the committed C0a blob, not from scratch |

### 58c1227e docs(state): set the plan to the F009 R20 effects round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 16/20 | C1 — whole-file replacement by slice PLANF009R20 |

### 33d6edd1 docs(review): record the R19 verdict and register R-0639
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 4/0 | C2 — slice LEDGER20 appended: the R19 verdict plus R-0639 |

### 5788b393 test(ui-server): pin the job.stop dispatch effects
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_dispatch.py | 143/0 | C3 — NEW file created from slice DISPATCHTESTS; no other path touched |

### C4 docs(state): write the F009 R20 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | C4 — this file; a handoff cannot table its own commit (R-0149, checklist item 14) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions

- `git push -u origin feature/f009-single-write-channel` after C4 → exit code and output in the round report.
- No worktree added or removed; `git worktree list` printed 1 line throughout.
- No PR created, no PR merged, no `gh` command run. F009 opens its PR at its own closure.

## Verification

- G1 `.agent/STOP` absent at both checks; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2 and C3; round base read at step 0 was `7ac8d98c24e7b76b4f684ec6e6a95de99b98da2f`.
- G2 `.agent/authored/f009-r20.md` at C0a, `.agent/last_block.md` at C0b and the received block are all sha256 `f10ccb1c506164779c7cd8ac164b59587753fe7bc3f7828568cb34a07de53718`, 25976 bytes, 329 lines, and byte-equal to each other; C0b was written from the committed C0a blob.
- G3 the extractor read 3 slices out of the committed C0a blob by their marker lines; the count 3 and the aggregate 16398 bytes over 186 lines are what the script printed; per-slice digests in the round report. Constraint 7 re-measured from that blob: 329 lines TOTAL agrees with the block; PROSE reads 143, not the 134 the block states — reported, not repaired (see Deviations).
- G4 `cmp <PLANF009R20> .agent/plan.md` exit 0, both sha256 `13cee13d…`; negative control `cmp <PLANF009R20> .agent/last_block.md` exit 1 at byte 1; `wc -l` 40 against the 50-line cap; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 the C2 append is ACCEPTED by reader (a) prefix+remainder and reader (b) last-N-units: the round-base blob is a byte-exact prefix, the remainder is exactly a newline plus LEDGER20, sha256 `560fd38c…`, 8166 bytes, 4 lines, N counted at 2 by the script, `.agent/live_review.md` 492988→501154 bytes and 1100→1104 lines; the base ended in exactly ONE newline, measured on the bytes; flipping byte 0 of the FIRST appended paragraph at equal length (`G`→`F`, in memory only) is REJECTED by BOTH readers while both ACCEPT the true file.
- G6 line-anchored at line START over `.agent/live_review.md`, round base → C2: leading `- R-` ids 204 → 205 with every captured id DISTINCT at each; leading `Done: R-` ids 3 → 3; leading `Landed: ` 0 → 0; leading `Gate: R` keys 19 → 20 over that many DISTINCT keys; the `Gate: R20` key 0 → 1; a leading `- R-0639` entry 0 → 1; a leading `- R-0640` entry 0 → 0; max id R-0638 → R-0639; open by D10's rule 202 at C2.
- G7 `.agent/decisions.md` is sha256 `518e00e02b27c349d85867ae106d766e45cad3377bc5fe44555d56b21337a7ba` over 461478 bytes at the round base AND at C4 — byte-identical, untouched; this round rules nothing.
- G8 `tests/ui_server/test_command_dispatch.py` did NOT exist at the round base: `git cat-file -e HEAD:tests/ui_server/test_command_dispatch.py` exited 128 "Not a valid object name" and the working tree had no such file. At C3 `cmp <DISPATCHTESTS> tests/ui_server/test_command_dispatch.py` exits 0, both sha256 `f58fafdb…`; negative control `cmp <DISPATCHTESTS> .agent/plan.md` exits 1 at byte 1.
- G9 serially in the primary checkout, never two pytest processes at once and never in a worktree: `ruff check tests/ui_server/test_command_dispatch.py` exit 0 "All checks passed!"; that file alone exit 0 at 4 passed; `tests/ui_server/` exit 0 at 422 passed; `tests/cli/test_golden_path.py` exit 0 at 42 passed; the four-path state-reader group exit 0 at 511 passed.
- G10 the range base→C3 lists exactly the five declared paths other than `.agent/handoff.md`, the set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/` or `docs/`; five commits each with ONE parent; `git show --numstat` (invoked WITHOUT a `--` before the SHA) and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the `## Commits` tables above, compared cell by cell — 329/0, 251/410, 16/20, 4/0 and 143/0; pre-handback insertions 329, 251, 16, 4 and 143, each under the 500 cap of AGENTS.md DECISION F104 D1; leading `<<<SLICE ` and `<<<END ` read 0 LINES in all three files a slice lands in, `.agent/plan.md`, `.agent/live_review.md` and the new test file; `git ls-files .remedy-wt` reads 0; this round's 5 reflog rows all classify as `commit` before the first `:`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; `git worktree list` printed 1 line throughout and no worktree was created.
- G11 every mandated section of docs/agents/handback_template.md is present in order, the item-status table carries exactly one row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA is stated above, each gate is one line with the transcripts in the round report and not in this file, and the block's `Fortschritt:` line is repeated verbatim; this file's `wc -l` is reported in the round report against the 100-line cap.

## Authored-text proofs

All three applied texts were extracted programmatically from the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines and applied byte for byte; none was retyped, rewrapped, reflowed or reindented, and no slice was edited. `.agent/plan.md` = PLANF009R20 by `cmp` exit 0 with a negative control at exit 1 (G4). `tests/ui_server/test_command_dispatch.py` = DISPATCHTESTS by `cmp` exit 0 with a negative control at exit 1 (G8). `.agent/live_review.md` carries LEDGER20 as an exact-prefix remainder under two independent readers, with a rejecting equal-length flip control on the FIRST appended paragraph (G5). This round has NO FROM/TO pair, so no replacement obligation arose and none was performed.

## Deviations & assumptions

The ordered commit sequence C0a, C0b, C1, C2, C3, C4 was executed exactly as the block wrote it: no extra commit, no dropped commit, no reordering, and no file outside the declared change set was touched.

TWO BLOCK NUMERALS DISAGREE WITH THE MEASUREMENT, reported rather than repaired. (a) Constraint 7 states "134 of them PROSE"; measured from the committed C0a blob, TOTAL is 329 as stated but PROSE is 143 — TOTAL minus the 186 slice-content lines, markers counted as prose. 134 is the count of lines from the top through the `─────` rule, which excludes the 3 blank separator lines and the 6 marker lines. Under either reading the figure is far under DECISION F085 D5's 400 cap. (b) Constraint 6 and G11 say the `Fortschritt:` line is repeated "across all three of its lines"; in the block it occupies FOUR lines (12–15). It is reproduced above verbatim across all four. Nothing was edited to reconcile either numeral. Assumption: the binding obligation is the verbatim text and the cap, not the count naming it.

## Next

Round three of DECISION F009 D19: `decision.resolve` dispatches to `answer_task_decision` followed by `save_job` per DECISION F009 D5 and the 501 seam is gone entirely; that round re-examines D18's clause three against a non-idempotent effect, as D18 requires of it, and migrates the two pins that still expect 501.
