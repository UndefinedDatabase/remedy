# Handback — F009 R23 (T003 — `decision.resolve` dispatches, the 501 seam is retired)

F009 "The single write channel", round 23, branch `feature/f009-single-write-channel`, round base SHA `9a47166c41dbd3cd1bd4a448a546109eac990a84` read at step 0. `.agent/STOP` absent before C0a and again before C5. Open at C2 by DECISION F009 D10's rule — every line-anchored `^- R-\d+ — ` paragraph minus every line-anchored `^Done: R-\d+ — ` line — 204, measured at `21379c75`. Max id R-0641. This round minted ONE id, R-0641, and resolved none; the next free id is R-0642.

Fortschritt: ~88 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             ausgesetzten Kommandos dispatchen jetzt wirklich, die 501-Naht ist
             weg; offen bleiben das SSE-Event, der Import-Guard und die
             405-Routenprobe) — Schätzung

## Range

Review of 9a47166c..HEAD.

## Commits

### 16904e69 docs(state): save the F009 R23 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r23.md | 464/0 | C0a — the block saved byte for byte from the scratch copy |

### 3f0bf26f docs(state): mirror the F009 R23 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 368/186 | C0b — written from the committed C0a blob, not from scratch |

### 78664c08 docs(state): set the plan to the F009 R23 dispatch round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 16/15 | C1 — whole-file replacement by slice PLANF009R23 |

### 21379c75 docs(review): record the R22 verdict and register R-0641
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 4/0 | C2 — slice LEDGER23 appended: the R22 verdict and finding R-0641 |

### 19f10abf docs(decisions): rule DECISION F009 D22 on answer_source and the 501 guard
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 22/0 | C3 — slice DECISION22 appended, eleven paragraphs |

### 15b8f85f feat(ui-server): dispatch decision.resolve and turn the 501 into a guard
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | 93/9 | C4 — pairs CONST, SEAM and METHOD |
| tests/ui_server/test_command_channel.py | 22/7 | C4 — pairs PINABSENT and PINLOOP |

### C5 docs(state): write the F009 R23 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | C5 — this file; a handoff cannot table its own commit (R-0149, checklist item 14) |

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

## External actions

- `git worktree add --detach .remedy-wt/g11 15b8f85f` for G11's red control, then `git worktree remove --force .remedy-wt/g11`; `git worktree list` printed 1 line before and after. Gate scratch lives under the gitignored `.remedy-wt/`; `git ls-files .remedy-wt` reads 0.
- `git push -u origin feature/f009-single-write-channel` after C5 → exit code and output in the round report.
- No PR created, no PR merged, no `gh` command run. F009 opens its PR at its own closure.

## Verification

- G1 `.agent/STOP` absent at both checks; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3 and C4; round base read at step 0 was `9a47166c41dbd3cd1bd4a448a546109eac990a84`.
- G2 `.agent/authored/f009-r23.md` at C0a, `.agent/last_block.md` at C0b and the block as received are all sha256 `0166cb2cbf86413d8f604b124f52354c498b945269da2c82c830c2a4d00191f5`, 39789 bytes, 464 lines, and byte-equal to one another; C0b was written FROM the committed C0a blob, never from the scratch copy again.
- G3 the extractor read the slices out of the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines and printed an aggregate count of 13: PLANF009R23 `c0c9347b…` 2364 B 41 L, LEDGER23 `3e7430fd…` 7503 B 3 L, DECISION22 `0040cee8…` 6547 B 21 L, CONST_FROM `03194d1d…` 194 B 3 L, CONST_TO `7243f758…` 885 B 16 L, SEAM_FROM `ab597637…` 469 B 8 L, SEAM_TO `e605f8eb…` 2484 B 37 L, METHOD_FROM `7c326f1b…` 190 B 4 L, METHOD_TO `e4085b57…` 2477 B 46 L, PINABSENT_FROM `40ef9bcb…` 394 B 7 L, PINABSENT_TO `aef7fd1c…` 868 B 16 L, PINLOOP_FROM `ff4fb16b…` 931 B 18 L, PINLOOP_TO `c14fe803…` 1270 B 24 L. Constraint 8 re-measured from that same blob: TOTAL 464 lines and PROSE 220 — TOTAL minus the 244 summed slice-CONTENT lines, marker lines counted as prose — both agreeing with the block, under DECISION F085 D6's 490 and D5's 400.
- G4 `cmp .agent/plan.md <PLANF009R23>` exit 0, both sha256 `c0c9347bf870010424dfdce829e992667a4ff51830c1abbf51effce7aeeac135`, 2364 bytes; negative control `cmp .agent/plan.md .agent/last_block.md` exit 1, "differ: byte 1, line 1"; `wc -l` 41 against the 50-line cap of AGENTS.md; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 BOTH appends are ACCEPTED by reader (a) prefix+remainder and by reader (b) last-N-blank-line-units-in-order, and BOTH readers REJECT an equal-length printable-byte flip in the FIRST appended paragraph while accepting the true file. C2 over `.agent/live_review.md`: remainder is exactly a newline plus LEDGER23, sha256 `619b3808…`, 7504 bytes, 4 lines; N counted at 2 BY THE SCRIPT; file 512626 → 520130 bytes, 1110 → 1114 lines; flip at offset 0 of the first appended paragraph, `G`→`g`, in memory only. C3 over `.agent/decisions.md`: remainder is exactly a newline plus DECISION22, sha256 `fc548ef2…`, 6548 bytes, 22 lines; N counted at 11 BY THE SCRIPT; file 467250 → 473798 bytes, 6887 → 6909 lines; flip at offset 3, `D`→`d`, in memory only. Each base blob ended in exactly ONE newline, measured on the bytes.
- G6 line-anchored at line START over `.agent/live_review.md`, round base → C2: `^- R-\d+ — ` entries 206 → 207 with every captured id DISTINCT at each; `^Done: R-\d+ — ` ids 3 → 3; leading `Landed: ` 0 → 0; leading `Gate: R` keys 22 → 23 over that many DISTINCT keys; the `Gate: R23` key 0 → 1; a leading `- R-0641` entry 0 → 1; a leading `- R-0642` entry 0 → 0; max id R-0640 → R-0641; open by DECISION F009 D10's rule 204 at C2.
- G7 line-anchored over `.agent/decisions.md`, round base → C3: the `## DECISION ` total 106 → 107; leading `## DECISION F009 D` numbers 21 → 22 with every captured number DISTINCT at each, max 21 → 22; the `## DECISION F009 D22 ` key 0 → 1.
- G8 each pair counted in its target file BOTH whole-line and indent-agnostic, the two readings AGREEING at every count. Before C4 CONST, SEAM, METHOD, PINABSENT and PINLOOP each read FROM 1 / TO 0; after C4 each reads FROM 0 / TO 1. TO-contains-FROM-as-a-contiguous-line-block, a value the script printed, is FALSE for every one of the five under both readings — none is append-shaped, as constraint 3 classified them.
- G9 line-anchored over `packages/orchestration/ui_server.py`, round base → C4: LINES carrying the quoted `"command channel not yet accepting commands"` 1 → 0; LINES carrying `_dispatch_decision_resolve` 0 → 2, one definition and one call site; LINES carrying the quoted `"not_implemented"` 1 → 1, the writer DECISION F009 D22 keeps as the guard.
- G10 run SERIALLY in the primary checkout, never two pytest processes at once and never in a worktree: `python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_command_channel.py` EXIT 0, "All checks passed!"; `pytest tests/ui_server/test_command_channel.py -q -rf` EXIT 0 at 84 passed; `pytest tests/ui_server/test_command_dispatch.py -q -rf` EXIT 0 at 4 passed; `pytest tests/orchestration/test_command_audit.py -q -rf` EXIT 0 at 17 passed; `pytest tests/cli/test_golden_path.py -q -rf` EXIT 0 at 42 passed; `pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` EXIT 0 at 511 passed.
- G11 RED CONTROL in the disposable worktree `.remedy-wt/g11` at C4 and nowhere else. Unmutated there the suite EXITS 0 at 84 passed. Reverting `packages/orchestration/ui_server.py` ALONE to its round-base bytes is REAL: the file is byte-equal to the base blob, sha256 `4f416712…` over 165494 bytes, and `git diff HEAD --numstat` prints `9	93	packages/orchestration/ui_server.py`. `pytest tests/ui_server/test_command_channel.py -q -rf` then EXITS 1 at 2 failed, 82 passed, and the failures are exactly the two pins this round migrates — `test_absent_args_is_valid_and_reaches_the_effect` and `test_every_exposed_command_reaches_the_answer_its_effect_gives`, both on `assert 501 == 409`. Worktree removed; `git worktree list` back to 1 line.
- G12 the range base→C4 lists exactly the declared paths other than `.agent/handoff.md` — the script printed 7 — with the set difference EMPTY in both directions, 0 paths beginning `apps/`, 0 beginning `docs/` and 0 equal to `packages/orchestration/command_audit.py`; the script counted 6 commits in that range and each has ONE parent; `git show --numstat` (invoked WITHOUT a `--` before the SHA) and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the `## Commits` tables above, compared cell by cell — 464/0, 368/186, 16/15, 4/0, 22/0, and 93/9 with 22/7; pre-handback insertions 464, 368, 16, 4, 22 and 115, each under the 500 cap of AGENTS.md DECISION F104 D1; leading `<<<SLICE ` and `<<<END ` read 0 LINES in each of the 5 files a slice lands in, a set the script enumerated; `git ls-files .remedy-wt` reads 0; this round's reflog rows classify as `{'commit': 6}` by the operation before the first `:`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog.
- G13 every mandated section of docs/agents/handback_template.md is present in order, the item-status table carries exactly one row for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA is stated above, each gate is one line with the raw transcripts in the round report and not in this file (R-0582), and the block's `Fortschritt:` line is repeated VERBATIM across all FOUR of its lines; this file's `wc -l` is reported in the round report against the cap. Every numeral above about this round's own measurements was read out of a script's printed output before it was written (R-0404, R-0641).

## Authored-text proofs

All thirteen applied texts were extracted programmatically from the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines and applied byte for byte; none was retyped, rewrapped, reflowed, reindented or whitespace-adjusted, and no slice was edited. `.agent/plan.md` = PLANF009R23 by `cmp` exit 0 with a negative control at exit 1 (G4). `.agent/live_review.md` carries LEDGER23 and `.agent/decisions.md` carries DECISION22 as exact-prefix remainders under two independent readers each, with a rejecting equal-length flip control on each FIRST appended paragraph (G5). The five FROM/TO pairs were applied as byte replacements of a FROM whose occurrence count the script measured at exactly 1 before each replacement, and their before/after counts are G8.

## Deviations & assumptions

The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was executed exactly as the block wrote it: no extra commit, no dropped commit, no reordering, C4 was not split, and no file outside the declared change set was touched. No block numeral disagreed with the measurement this round: constraint 8's 464 TOTAL and 220 PROSE both reproduced from the committed C0a blob, constraint 2's TWO and ELEVEN paragraphs are the N each reader counted, constraint 3's five not-append-shaped classifications all measured FALSE, and the `Fortschritt:` line was found on FOUR physical lines as constraint 7 states.

Deviations, declared: this handback is 98 lines, over the 60-line base cap and within the ≤100 tier docs/agents/handback_template.md grants a bundle whose per-commit tables exceed five commits. The cause is mandated content only — seven per-commit changed-files tables, the seven-row item-status table, and G13's one-line-per-gate obligation over thirteen gates. No section was dropped and no transcript was inlined.

## Next

Next session, FIRST action: Phase 1 rule 1 of docs/agents/self_drive_protocol.md — re-read `.agent/STOP` from disk; if it exists, write the handoff and end. SECOND: Phase 1 rule 2, the AGENTS.md Open PR Gate. Then the work: R24 adds, purely additively, the tests DECISION F009 D22's fifth clause defers — the 200 acceptance path, the 501 guard reached by monkeypatching `UI_EXPOSED_COMMANDS`, and the disk-level `decision.resolve` effect assertions in `tests/ui_server/test_command_dispatch.py`.
