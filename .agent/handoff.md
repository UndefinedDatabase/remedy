# Handback — F009 R19 (T003, round one of DECISION F009 D19 — the `job.stop` dispatch)

Feature F009 "The single write channel", round 19, branch `feature/f009-single-write-channel`.
Round base SHA `aa1e27808b115f79a26ba2ab60a8bd1fdd97a77a`. `.agent/STOP` absent before C0a and before C5.
Open findings at C2 by DECISION F009 D10's rule: 201. Max id R-0638. This round minted R-0638 and resolved none.

Fortschritt: ~78 % (T001 gebaut · T002 gebaut · T003 begonnen: Extraktion,
             Publikations-Bound und Vokabular stehen, der `job.stop`-Dispatch
             wird in dieser Runde gebaut) — Schätzung

## Range

Review of aa1e2780..HEAD.

## Commits

### ed036f14 docs(state): save the F009 R19 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r19.md | 488/0 | C0a — the block saved byte for byte from the scratch copy |

### de716e02 docs(state): mirror the F009 R19 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 426/138 | C0b — written from the committed C0a blob, not from scratch |

### 909d37ee docs(state): set the plan to the F009 R19 dispatch round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 16/20 | C1 — whole-file replacement by slice PLANF009R19 |

### 768eba0f docs(review): record the R18 verdict and finding R-0638
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 4/0 | C2 — slice LEDGER19 appended: the R18 verdict plus R-0638 |

### d2388da2 docs(decisions): rule DECISION F009 D20 for the job stop dispatch
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 10/0 | C3 — slice DECISION20 appended |

### 5d3d1e32 feat(ui-server): dispatch job stop through the command channel
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | 76/13 | C4 — slices U1CONST, U2REPLAY, U3DISPATCH: the dispatch, its two helpers and D20's constants |
| tests/ui_server/test_command_channel.py | 46/38 | C4 — slices P_A..P_J plus the three ordered replacements; kept whole with the door per constraint 3 |

### C5 docs(state): write the F009 R19 handback
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
- No worktree added or removed; `git worktree list` printed 1 line throughout.
- No PR created, no PR merged, no `gh` command run. F009 opens its PR at its own closure.

## Verification

- G1 `.agent/STOP` absent at both checks; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3 and C4; round base read at step 0 was `aa1e27808b115f79a26ba2ab60a8bd1fdd97a77a`.
- G2 `.agent/authored/f009-r19.md` at C0a, `.agent/last_block.md` at C0b and the received block are all sha256 `36b24983aebc1f9e4f92569a7f59c6a1a9015dcf55e51564cfb9d3b627836595`, 36697 bytes, 488 lines, and byte-equal to each other; C0b was written from the committed C0a blob.
- G3 the extractor read 31 slices out of the committed C0a blob by their marker lines; the count 31 and the aggregate 24295 bytes over 253 lines are what the script printed; per-slice digests in the round report. Constraint 9 re-measured from that blob: 488 lines TOTAL, 156 PROSE — both agree with the block.
- G4 `cmp .agent/plan.md <PLANF009R19>` exit 0, both sha256 `7787099a…`; negative control `cmp .agent/context.md <PLANF009R19>` exit 1; `wc -l` 44 against the 50-line cap; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 both appends ACCEPTED by reader (a) prefix+remainder and reader (b) last-N-units: C2 over the round-base blob, remainder sha256 `6708ca1d…`, 6590 bytes, 4 lines, N=2 counted by the script, `.agent/live_review.md` 486398→492988 bytes and 1096→1100 lines; C3 over the C2 blob, remainder sha256 `b94849e6…`, 3316 bytes, 10 lines, N=5, `.agent/decisions.md` 458162→461478 bytes and 6857→6867 lines; flipping byte 0 of the FIRST appended paragraph at equal length (`G`→`!`, `#`→`!`) is REJECTED by both readers in both cases while both ACCEPT the true file.
- G6 line-anchored at line START over `.agent/live_review.md`, round base → C2: leading `- R-` ids 203 → 204 with every captured id DISTINCT at each; leading `Done: R-` ids 3 → 3; leading `Landed: ` 0 → 0; leading `Gate: R` keys 18 → 19 over that many DISTINCT keys; the `Gate: R19` key 0 → 1; a leading `- R-0638` entry 0 → 1; a leading `- R-0639` entry 0 → 0; max id R-0637 → R-0638; open by D10's rule 201 at C2.
- G7 line-anchored at line START over `.agent/decisions.md`, round base → C3: leading `## DECISION F009 D` numbers 19 → 20 with every captured number DISTINCT at each; the `## DECISION ` total 104 → 105; `## DECISION F009 D20` 0 → 1.
- G8 all 14 pairs measured in the file each lands in, whole-line and indent-agnostic, the two readings AGREEING at every count. BEFORE C4 every FROM read 1/1 and every TO 0/0. AFTER C4 every TO reads 1/1, and 13 of 14 FROMs read 0/0 — U1CONST reads 1/1, which is ENTAILED by its own containment reading and is reported, not fixed (see Deviations). Containment `TO contains FROM`: TRUE for U1CONST alone, FALSE for the other 13, matching the block.
- G9 my script changed `[0] == 501`→`[0] == 200` at 9 occurrences, `status == 501`→`status == 200` at 4 and the quoted `not_implemented`→`accepted` at 4, all in `tests/ui_server/test_command_channel.py` only; afterwards that file reads 0, 0 and 0 for the three sources and 1 for the quoted `replayed`, while `packages/orchestration/command_audit.py` still reads 1 for the quoted `not_implemented` and was not touched by this round.
- G10 serially in the primary checkout, never two pytest processes at once and never in a worktree: `ruff check` over the two changed paths exit 0 "All checks passed!"; `tests/ui_server/` exit 0 at 418 passed; `tests/cli/test_golden_path.py` exit 0 at 42 passed; the four-path group exit 0 at 507 passed; `tests/orchestration/test_command_audit.py` exit 0 at 17 passed.
- G11 the range base→C4 lists exactly the seven declared paths other than `.agent/handoff.md`, the set difference EMPTY in both directions, 0 paths beginning `apps/` and 0 beginning `docs/`; six commits each with ONE parent; `git show --numstat` (invoked without a `--` before the SHA) and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the `## Commits` tables above, compared cell by cell — 488/0, 426/138, 16/20, 4/0, 10/0 and 76/13 with 46/38; pre-handback insertions 488, 426, 16, 4, 10 and 122, each under the 500 cap of AGENTS.md DECISION F104 D1; leading `<<<SLICE ` and `<<<END ` read 0 LINES in all five files a slice lands in; `git ls-files .remedy-wt` reads 0; this round's 6 reflog rows all classify as `commit` before the first `:`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; `git worktree list` printed 1 line throughout and no worktree was created.
- G12 every mandated section of docs/agents/handback_template.md is present in order, the item-status table carries exactly one row for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA is stated above, each gate is one line, the block's `Fortschritt:` line is repeated verbatim across all three of its lines, and this file's `wc -l` is reported in the round report against the 100-line cap.

## Authored-text proofs

All applied texts were extracted programmatically from the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines and applied byte for byte; none was retyped, rewrapped, reflowed or reindented, and no slice was edited. `.agent/plan.md` = PLANF009R19 by `cmp` exit 0 with a negative control at exit 1 (G4). `.agent/live_review.md` and `.agent/decisions.md` carry LEDGER19 and DECISION20 as exact-prefix remainders under two independent readers each, with a rejecting equal-length flip control on the FIRST appended paragraph of each (G5). All 14 FROM/TO pairs were applied FIRST and the three ordered replacements of constraint 5 only afterwards, in the block's order (G8, G9).

## Deviations & assumptions

The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was executed exactly as the block wrote it: no extra commit, no dropped commit, no reordering, and no file outside the declared change set was touched.

ONE GATE CLAUSE DOES NOT HOLD, reported rather than repaired. G8 orders "each FROM reads 1 before and 0 after". For U1CONST that is unmeetable by construction, and the SAME gate says so: U1CONST_TO appends three constant blocks AFTER re-quoting U1CONST_FROM verbatim, so `TO contains FROM` is TRUE — the reading G8 itself predicts — and a FROM contained in its own TO necessarily still reads 1 after the pair is applied. Measured: U1CONST FROM 1/1 and TO 1/1 after C4, both readings agreeing; the other 13 pairs read FROM 0/0 and TO 1/1. Nothing was edited to reconcile the two clauses; per the round instruction a disagreement is reported, not fixed. Assumption: the intent of G8's after-clause is that no pair leaves an unconverted site, which holds for all 14.

## Next

Round two of DECISION F009 D19: the effect assertions in a NEW file `tests/ui_server/test_command_dispatch.py` — that the stop request the dispatch published exists and carries the door's source, that the nonce record holds the body the client received, and that a retry of the same nonce is audited `replayed`. Purely additive; it edits no existing test. `rejected_effect` is written from R19 but no shipped test reaches it, and round two owes it a permanent test.
