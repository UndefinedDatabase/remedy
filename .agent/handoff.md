# Handback — F009 R21 (T003 record round — the R20 verdict, closing the session)

F009 "The single write channel", round 21, branch `feature/f009-single-write-channel`, round base SHA `a2af1014b660c8b97224d4e3991ce8e2cc09ef79` read at step 0. `.agent/STOP` absent before C0a and again before C3. Open at C2 by DECISION F009 D10's rule: 203. Max id R-0640. This round minted R-0640 and resolved none; the next free id is R-0641.

Fortschritt: ~82 % (T001 gebaut · T002 gebaut · T003 begonnen: der
             `job.stop`-Dispatch steht und ist wirkungsgeprüft; offen bleiben
             `decision.resolve`, das SSE-Event, der Import-Guard und die
             405-Routenprobe) — Schätzung

## Range

Review of a2af1014..HEAD.

## Commits

### bc035156 docs(state): save the F009 R21 record block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r21.md | 181/0 | C0a — the block saved byte for byte from the scratch copy |

### 0c7070de docs(state): mirror the F009 R21 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 91/239 | C0b — written from the committed C0a blob, not from scratch |

### 5ab95500 docs(state): set the plan to the F009 R21 record round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 13/11 | C1 — whole-file replacement by slice PLANF009R21 |

### fcbb0bb3 docs(review): record the R20 verdict and register R-0640
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 4/0 | C2 — slice LEDGER21 appended: the R20 verdict plus R-0640 |

### C3 docs(state): write the F009 R21 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | C3 — this file; a handoff cannot table its own commit (R-0149, checklist item 14) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |

## External actions

- `git push -u origin feature/f009-single-write-channel` after C3 → exit code and output in the round report.
- No worktree added or removed; `git worktree list` printed 1 line throughout. Gate scratch was written under the gitignored `.remedy-wt/worker-r21/`; `git ls-files .remedy-wt` reads 0.
- No PR created, no PR merged, no `gh` command run. F009 opens its PR at its own closure.

## Verification

- G1 `.agent/STOP` absent at both checks; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1 and C2; round base read at step 0 was `a2af1014b660c8b97224d4e3991ce8e2cc09ef79`.
- G2 `.agent/authored/f009-r21.md` at C0a, `.agent/last_block.md` at C0b and the block as received are all sha256 `29bc2a7f4504c137614a74f55b0de69cc5d43f679210554bd51376987858b0b8`, 18556 bytes, 181 lines, and byte-equal to each other; C0b was written from the committed C0a blob, never from the scratch copy again.
- G3 the extractor read the slices out of the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines and printed an aggregate count of 2: PLANF009R21 sha256 `fb70be12…` 2396 bytes 42 lines, LEDGER21 sha256 `1b674523…` 7071 bytes 3 lines. Constraint 6 re-measured from that same blob: TOTAL 181 lines and PROSE 136 — TOTAL minus the 45 summed slice-CONTENT lines, marker lines counted as prose — both agreeing with the block, under DECISION F085 D6's 490 and D5's 400.
- G4 `cmp .agent/plan.md <PLANF009R21>` exit 0, both sha256 `fb70be12…`; negative control `cmp .agent/plan.md .agent/context.md` exit 1, "differ: byte 3, line 1"; `wc -l` 42 against the 50-line cap of AGENTS.md; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 the C2 append is ACCEPTED by reader (a) prefix+remainder and by reader (b) last-N-units: the round-base blob is a byte-exact prefix of `.agent/live_review.md`, the remainder is exactly a newline plus LEDGER21, sha256 `a9aa70b8…`, 7072 bytes, 4 lines; N counted at 2 BY THE SCRIPT and the last 2 blank-line units equal LEDGER21's 2 paragraphs IN ORDER; the base ended in exactly ONE newline, measured on the bytes; the file went 501154 → 508226 bytes and 1104 → 1108 lines; flipping the printable byte at offset 501155 in the FIRST appended paragraph at equal length (`G`→`H`, in memory only) is REJECTED by BOTH readers while both ACCEPT the true file.
- G6 line-anchored at line START over `.agent/live_review.md`, round base → C2: leading `- R-` ids 205 → 206 with every captured id DISTINCT at each; leading `Done: R-` ids 3 → 3; leading `Landed: ` 0 → 0; leading `Gate: R` keys 20 → 21 over that many DISTINCT keys; the `Gate: R21` key 0 → 1; a leading `- R-0640` entry 0 → 1; a leading `- R-0641` entry 0 → 0 at both; max id R-0639 → R-0640; open by DECISION F009 D10's rule 203 at C2.
- G7 `.agent/decisions.md` is sha256 `518e00e02b27c349d85867ae106d766e45cad3377bc5fe44555d56b21337a7ba` over 461478 bytes at the round base AND at C3 — byte-identical, untouched; this round rules nothing.
- G8 run SERIALLY in the primary checkout, never two pytest processes at once and never in a worktree: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` EXIT 0 at 42 passed; `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` EXIT 0 at 511 passed.
- G9 the range base→C2 lists exactly the four declared paths other than `.agent/handoff.md`, the set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/`; each commit has ONE parent; `git show --numstat` (invoked WITHOUT a `--` before the SHA) and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the `## Commits` tables above, compared cell by cell — 181/0, 91/239, 13/11 and 4/0; pre-handback insertions 181, 91, 13 and 4, each under the 500 cap of AGENTS.md DECISION F104 D1; leading `<<<SLICE ` and `<<<END ` read 0 LINES in both files a slice lands in, `.agent/plan.md` and `.agent/live_review.md`; `git ls-files .remedy-wt` reads 0; this round's reflog rows all classify as `commit` before the first `:`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; `git worktree list` printed 1 line throughout and no worktree was created.
- G10 every mandated section of docs/agents/handback_template.md is present in order, the item-status table carries exactly one row for each of C0a, C0b, C1, C2 and C3, the round base SHA is stated above, each gate is one line with the raw transcripts in the round report and not in this file (R-0582), and the block's `Fortschritt:` line is repeated VERBATIM across all FOUR of its lines; this file's `wc -l` is reported in the round report against the cap.

## Authored-text proofs

Both applied texts were extracted programmatically from the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines and applied byte for byte; neither was retyped, rewrapped, reflowed or reindented, and no slice was edited. `.agent/plan.md` = PLANF009R21 by `cmp` exit 0 with a negative control at exit 1 (G4). `.agent/live_review.md` carries LEDGER21 as an exact-prefix remainder under two independent readers, with a rejecting equal-length flip control on the FIRST appended paragraph (G5). This round has NO FROM/TO pair, so no replacement obligation arose and none was performed.

## Deviations & assumptions

The ordered commit sequence C0a, C0b, C1, C2, C3 was executed exactly as the block wrote it: no extra commit, no dropped commit, no reordering, and no file outside the declared change set was touched. No block numeral disagreed with the measurement this round: constraint 6's 181 TOTAL and 136 PROSE both reproduced from the committed C0a blob, and the `Fortschritt:` line was found on FOUR physical lines as constraint 5 states.

Deviations, declared: this handback is 82 lines against the 60-line cap for a bundle of five commits. The cause is mandated content only — five per-commit changed-files tables (25 lines), the six-row item-status table, and G10's one-line-per-gate obligation over ten gates. No section was dropped and no transcript was inlined.

## Next

Next session, FIRST action: Phase 1 rule 1 of docs/agents/self_drive_protocol.md — re-read `.agent/STOP` from disk; if it exists, write the handoff and end. SECOND: Phase 1 rule 2, the AGENTS.md Open PR Gate. Then the work: `decision.resolve` dispatches to `answer_task_decision` followed by `save_job` per DECISION F009 D5, the 501 seam goes entirely, DECISION F009 D18's clause three is re-examined against a non-idempotent effect as D18 requires, and the two pins that still expect 501 migrate.
