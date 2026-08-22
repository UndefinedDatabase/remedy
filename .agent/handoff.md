# Handback — F009 R22 (T003 — DECISION F009 D21 ruled, the `rejected_state` token landed)

F009 "The single write channel", round 22, branch `feature/f009-single-write-channel`, round base SHA `09d473d658bac0a715d63be2e0b334b071d5cd81` read at step 0. `.agent/STOP` absent before C0a and again before C5. Open at C2 by DECISION F009 D10's rule — every line-anchored `^- R-\d+ — ` paragraph minus every line-anchored `^Done: R-\d+ — ` line — 203, measured at `a68d1693`. Max id R-0640. This round minted NO id and resolved none; the next free id is R-0641, exactly as when the round started. No door was touched.

Fortschritt: ~84 % (T001 gebaut · T002 gebaut · T003 begonnen: der
             `job.stop`-Dispatch steht und ist wirkungsgeprüft, die
             `decision.resolve`-Wirkung ist geregelt; offen bleiben der Dispatch
             selbst, das SSE-Event, der Import-Guard und die 405-Routenprobe) —
             Schätzung

## Range

Review of 09d473d6..HEAD.

## Commits

### 9d23eb4a docs(state): save the F009 R22 block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r22.md | 282/0 | C0a — the block saved byte for byte from the scratch copy |

### 76c1a3fb docs(state): mirror the F009 R22 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 212/111 | C0b — written from the committed C0a blob, not from scratch |

### bd5c3d9c docs(state): set the plan to the F009 R22 ruling round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 13/15 | C1 — whole-file replacement by slice PLANF009R22 |

### a68d1693 docs(review): record the R21 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — slice LEDGER22 appended: the R21 verdict, no finding under it |

### 9d154d00 docs(decisions): rule DECISION F009 D21
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 20/0 | C3 — slice DECISION21 appended, ten paragraphs |

### 3fc8e98d feat(orchestration): land the rejected_state audit token
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/command_audit.py | 7/0 | C4 — pairs AUDITDOC and AUDITSET |
| tests/orchestration/test_command_audit.py | 3/1 | C4 — pairs PINDOC and PINSET |

### C5 docs(state): write the F009 R22 handback
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

- `git push -u origin feature/f009-single-write-channel` after C5 → exit code and output in the round report.
- No worktree added or removed; `git worktree list` printed 1 line throughout. Gate scratch was written under the gitignored `.remedy-wt/`; `git ls-files .remedy-wt` reads 0.
- No PR created, no PR merged, no `gh` command run. F009 opens its PR at its own closure.

## Verification

- G1 `.agent/STOP` absent at both checks; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3 and C4; round base read at step 0 was `09d473d658bac0a715d63be2e0b334b071d5cd81`.
- G2 `.agent/authored/f009-r22.md` at C0a, `.agent/last_block.md` at C0b and the block as received are all sha256 `11f2023104c32675429f9dc91afcd268bd9657f4539b6d1f860af16232f4b2c4`, 25633 bytes, 282 lines, byte-equal by `cmp` exit 0 with a negative control at exit 1; C0b was written from the committed C0a blob, never from the scratch copy again.
- G3 the extractor read the slices out of the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines and printed an aggregate count of 11: PLANF009R22 `faa5b439…` 2270 B 40 L, LEDGER22 `575d4d9d…` 4399 B 1 L, DECISION21 `5719d830…` 5771 B 19 L, AUDITDOC_FROM `5c3524d5…` 87 B 2 L, AUDITDOC_TO `1ac35b15…` 605 B 8 L, AUDITSET_FROM `985934eb…` 25 B 2 L, AUDITSET_TO `6c8c825b…` 47 B 3 L, PINDOC_FROM `0d58d648…` 88 B 1 L, PINDOC_TO `bb87226f…` 87 B 1 L, PINSET_FROM `b5007e68…` 259 B 5 L, PINSET_TO `0f43ec84…` 378 B 7 L. Constraint 7 re-measured from that same blob: TOTAL 282 lines and PROSE 193 — TOTAL minus the 89 summed slice-CONTENT lines, marker lines counted as prose — both agreeing with the block, under DECISION F085 D6's 490 and D5's 400.
- G4 `cmp .agent/plan.md <PLANF009R22>` exit 0, both sha256 `faa5b4391003168979fafd578846f5664f2a2d7b1990c782ec2075fbe09fa35c`; negative control `cmp .agent/plan.md .agent/context.md` exit 1, "differ: byte 3, line 1"; `wc -l` 40 against the 50-line cap of AGENTS.md; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 BOTH appends are ACCEPTED by reader (a) prefix+remainder and by reader (b) last-N-units, and BOTH readers REJECT an equal-length printable-byte flip in the FIRST appended paragraph while accepting the true file. C2 over `.agent/live_review.md`: remainder is exactly a newline plus LEDGER22, sha256 `69dda8a4…`, 4400 bytes, 2 lines; N counted at 1 BY THE SCRIPT; file 508226 → 512626 bytes, 1108 → 1110 lines; flip at offset 508227 `G`→`H`, in memory only. C3 over `.agent/decisions.md`: remainder is exactly a newline plus DECISION21, sha256 `19ccc8d5…`, 5772 bytes, 20 lines; N counted at 10 BY THE SCRIPT; file 461478 → 467250 bytes, 6867 → 6887 lines; flip at offset 461479 `#`→`$`, in memory only. Each base blob ended in exactly ONE newline, measured on the bytes.
- G6 line-anchored at line START over `.agent/live_review.md`, round base → C2: leading `- R-` entries 206 → 206 with every captured id DISTINCT at each; leading `Done: R-` ids 3 → 3; leading `Landed: ` 0 → 0; leading `Gate: R` keys 21 → 22 over that many DISTINCT keys; the `Gate: R22` key 0 → 1; a leading `- R-0641` entry 0 → 0; max id R-0640 → R-0640; open by DECISION F009 D10's rule 203 at C2.
- G7 line-anchored over `.agent/decisions.md`, round base → C3: the `## DECISION ` total 105 → 106; leading `## DECISION F009 D` numbers 20 → 21 with every captured number DISTINCT at each, max 20 → 21; the `## DECISION F009 D21 ` key 0 → 1.
- G8 each pair counted in its target file BOTH whole-line and indent-agnostic, the two readings AGREEING at every count. Before C4 AUDITDOC, AUDITSET, PINDOC and PINSET each read FROM 1 / TO 0; after C4 each reads FROM 0 / TO 1. TO-contains-FROM-as-a-contiguous-line-block, a value the script printed, is FALSE for all four — none is append-shaped, as constraint 3 classified them.
- G9 run SERIALLY in the primary checkout, never two pytest processes at once and never in a worktree: `python3 -m ruff check packages/orchestration/command_audit.py tests/orchestration/test_command_audit.py` EXIT 0, "All checks passed!"; `python3 -m pytest tests/orchestration/test_command_audit.py -q -rf` EXIT 0 at 17 passed; `python3 -m pytest tests/cli/test_golden_path.py -q -rf` EXIT 0 at 42 passed; `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` EXIT 0 at 511 passed.
- G10 the range base→C4 lists exactly the six declared paths other than `.agent/handoff.md`, the set difference EMPTY in both directions, 0 paths beginning `apps/`, 0 beginning `docs/` and 0 equal to `packages/orchestration/ui_server.py`; each commit has ONE parent; `git show --numstat` (invoked WITHOUT a `--` before the SHA) and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the `## Commits` tables above, compared cell by cell — 282/0, 212/111, 13/15, 2/0, 20/0, 7/0 and 3/1; pre-handback insertions 282, 212, 13, 2, 20 and 10, each under the 500 cap of AGENTS.md DECISION F104 D1; leading `<<<SLICE ` and `<<<END ` read 0 LINES in each of the five files a slice lands in; `git ls-files .remedy-wt` reads 0; this round's six reflog rows all classify as `commit` before the first `:`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; `git worktree list` printed 1 line throughout and no worktree was created.
- G11 every mandated section of docs/agents/handback_template.md is present in order, the item-status table carries exactly one row for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA is stated above, each gate is one line with the raw transcripts in the round report and not in this file (R-0582), and the block's `Fortschritt:` line is repeated VERBATIM across all FIVE of its lines; this file's `wc -l` is reported in the round report against the cap.

## Authored-text proofs

All eleven applied texts were extracted programmatically from the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines and applied byte for byte; none was retyped, rewrapped, reflowed, reindented or whitespace-adjusted, and no slice was edited. `.agent/plan.md` = PLANF009R22 by `cmp` exit 0 with a negative control at exit 1 (G4). `.agent/live_review.md` carries LEDGER22 and `.agent/decisions.md` carries DECISION21 as exact-prefix remainders under two independent readers each, with a rejecting equal-length flip control on each FIRST appended paragraph (G5). The four FROM/TO pairs were applied as byte replacements of a FROM whose occurrence count the script measured at exactly 1 before each replacement, and their before/after counts are G8.

## Deviations & assumptions

The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was executed exactly as the block wrote it: no extra commit, no dropped commit, no reordering, and no file outside the declared change set was touched. No block numeral disagreed with the measurement this round: constraint 7's 282 TOTAL and 193 PROSE both reproduced from the committed C0a blob, constraint 2's ONE and TEN paragraphs are the N each reader counted, constraint 3's four not-append-shaped classifications all measured FALSE, and the `Fortschritt:` line was found on FIVE physical lines as constraint 6 states.

Deviations, declared: this handback is 97 lines, over the 60-line base cap and within the ≤100 tier docs/agents/handback_template.md grants a bundle whose per-commit tables exceed five commits. The cause is mandated content only — seven per-commit changed-files tables, the eight-row item-status table, and G11's one-line-per-gate obligation over eleven gates. No section was dropped and no transcript was inlined.

## Next

Next session, FIRST action: Phase 1 rule 1 of docs/agents/self_drive_protocol.md — re-read `.agent/STOP` from disk; if it exists, write the handoff and end. SECOND: Phase 1 rule 2, the AGENTS.md Open PR Gate. Then the work: R23 edits `packages/orchestration/ui_server.py` alone — `decision.resolve` dispatches to `answer_task_decision` followed by `save_job` under DECISION F009 D21, the 501 seam and its `not_implemented` writer go, and the two pins that still expect 501 migrate.
