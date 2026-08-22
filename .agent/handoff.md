# Handback — F009 R17 (T003, round one of DECISION F009 D18)

Feature F009 "The single write channel", round 17, branch `feature/f009-single-write-channel`.
Round base SHA `e7c621fce35c3247832f1d3f6dd06768a4d37be1`. `.agent/STOP` absent before C0a and before C5.
Open findings at C2 by DECISION F009 D10's rule: 200. Max id R-0637. This round minted no id and resolved none.

Fortschritt: ~72 % (T001 gebaut · T002 gebaut · T003 begonnen: Extraktion,
             Publikations-Bound und das vollständige Vokabular stehen, der
             Dispatch fehlt) — Schätzung

## Range

Review of e7c621fc..HEAD.

## Commits

### 10681377 docs(state): save the F009 R17 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r17.md | 322/0 | C0a — the block saved byte for byte from the scratch copy |

### e92970bf docs(state): mirror the F009 R17 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 253/134 | C0b — written from the committed C0a blob, not from scratch |

### bacc2459 docs(state): set the plan to the F009 R17 round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 17/18 | C1 — whole-file replacement by slice PLANF009R17 |

### d3a3bd27 docs(review): record the R16 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — slice LEDGER17 appended, the R16 verdict |

### 6f140128 docs(decisions): rule DECISION F009 D18
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 18/0 | C3 — slice DECISION18 appended |

### e1850a5b feat(orchestration): add the rejected_effect audit outcome with its pin
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/command_audit.py | 7/1 | C4 — pair AUDIT_FROM → AUDIT_TO |
| tests/orchestration/test_command_audit.py | 3/1 | C4 — pair PIN_FROM → PIN_TO, same commit as the token |

### C5 docs(state): write the F009 R17 handback
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

- `git worktree add --detach .remedy-wt/r17red e1850a5b` → exit 0 (gate G10, guardrail G5).
- `git worktree remove .remedy-wt/r17red` → exit 0; `git worktree prune` → exit 0; `git worktree list` then prints 1 line.
- `git push -u origin feature/f009-single-write-channel` after C5 → exit code and output in the round report.
- No PR created, no PR merged, no `gh` command run. F009 opens its PR at its own closure.

## Verification

One line per gate; the raw transcripts are in the round report (finding R-0582).

- G1 `.agent/STOP` absent at both checks; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3, C4; round base read at step 0 was `e7c621fce35c3247832f1d3f6dd06768a4d37be1`.
- G2 `.agent/authored/f009-r17.md` at C0a, `.agent/last_block.md` at C0b and the received block are all sha256 `a99166a9d66fbd0c67dea646c6dab389707e001559c4978c0eee6d57a14a3196`, 26275 bytes, 322 lines, and byte-equal to each other.
- G3 the extractor read 7 slices out of the committed C0a blob by their marker lines; the count 7 and the aggregate 14216 bytes over 127 lines are what the script printed; per-slice digests in the round report.
- G4 `cmp .agent/plan.md .remedy-wt/r17slices/PLANF009R17` exit 0, both sha256 `50eb380b…`; negative control `cmp .agent/plan.md .agent/last_block.md` exit 1; `wc -l` 45 against the 50-line cap; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 both appends ACCEPTED by reader (a) prefix+remainder and reader (b) last-N-units: C2 remainder sha256 `585973ea…`, 4804 bytes, 2 lines, N=1 counted by the script, `.agent/live_review.md` 476187→480991 bytes and 1092→1094 lines; C3 remainder sha256 `a7fad9c3…`, 4494 bytes, 18 lines, N=9, `.agent/decisions.md` 450056→454550 bytes and 6827→6845 lines; flipping byte 0 of the FIRST appended paragraph at equal length (`G`→`Z`, `#`→`Z`) is REJECTED by both readers in both cases while both ACCEPT the true file.
- G6 at C4 AUDIT_FROM reads 0 whole-line and 0 indent-agnostic and AUDIT_TO 1 and 1; PIN_FROM 0 and 0 and PIN_TO 1 and 1; every pair of readings agrees; each file's C3 blob with its single pair applied is BYTE-EQUAL to what C4 landed (sha256 `8268358d…` and `03b86977…`); `git show --numstat` for C4 reads `7 1` and `3 1`.
- G7 line-anchored at line START over `.agent/live_review.md`, round base → C2: `^- R-\d+ — ` 203 → 203 with every captured id DISTINCT at each; `^Done: R-\d+ — ` 3 → 3; `^Landed: ` 0 → 0; `^Gate: R\d+ — ` 16 → 17 over that many DISTINCT keys; `^Gate: R17 — ` 0 → 1; `^- R-0638 — ` 0 → 0; max id R-0637 at both; open by D10's rule 200 at C2.
- G8 line-anchored over `.agent/decisions.md`, round base → C3: `^## DECISION F009 D\d+ — ` 17 → 18 with every captured number DISTINCT at each; `^## DECISION ` 102 → 103; `^## DECISION F009 D18 — ` 0 → 1.
- G9 serially in the primary checkout: ruff exit 0 "All checks passed!"; `test_command_audit.py test_command_nonce.py` exit 0 at 45 passed; `tests/cli/test_golden_path.py` exit 0 at 42 passed; the four-path group exit 0 at 507 passed — the ui_server half is the constraint-8 proof that the door's guard passes UNEDITED.
- G10 in the disposable worktree `.remedy-wt/r17red` at content byte-identical to C4, deleting the single line `    "rejected_effect",` (1 whole-line, 1 indent-agnostic, agreeing) makes the run exit 1 with `tests/orchestration/test_command_audit.py::test_the_outcome_vocabulary_is_the_closed_set_d14_ruled` the id it printed as FAILED; after restore the same command exits 0; worktree removed and pruned, `git worktree list` prints 1 line.
- G11 the range base→C4 lists exactly the seven declared paths with the set difference EMPTY in both directions, 0 paths equal to `packages/orchestration/ui_server.py` and 0 beginning `tests/ui_server/`; six commits each with ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the `## Commits` tables above, compared cell by cell — 322/0, 253/134, 17/18, 2/0, 18/0, 7/1 and 3/1; pre-handback insertions 322, 253, 17, 2, 18 and 10, each under the 500 cap; `^<<<SLICE ` and `^<<<END ` read 0 LINES in all five files a slice lands in; `git ls-files .remedy-wt` reads 0; this round's 6 reflog rows all classify as `commit` before the first `:`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog.
- G12 every mandated section of docs/agents/handback_template.md is present in order, the item-status table carries exactly one row for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA is stated above, each gate is one line, and this file's `wc -l` is reported in the round report.

## Authored-text proofs

All applied texts were extracted programmatically from the COMMITTED C0a blob by their marker lines and applied byte for byte; none was retyped. `.agent/plan.md` = PLANF009R17 by `cmp` exit 0 with a negative control at exit 1 (G4). `.agent/live_review.md` and `.agent/decisions.md` carry LEDGER17 and DECISION18 as exact-prefix remainders (G5). The two FROM/TO pairs reproduce their C4 blobs byte for byte from the C3 blobs (G6).

## Deviations & assumptions

None. The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was executed exactly as the block wrote it, with no extra commit, no dropped commit and no reordering. No slice was edited. No file outside the declared change set was touched.

## Next

Round two of DECISION F009 D18: dispatch `job.stop` in `packages/orchestration/ui_server.py` under D18's ruled order, migrate the seam pins in `tests/ui_server/test_command_channel.py` and pay R-0636. Read `.agent/STOP` first (Phase 1 rule 1), then the Open PR Gate.
