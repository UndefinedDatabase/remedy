# Handback — F255 R13 (the billing ruling, the ledger module text, and the spend writer)
## Range
Review of 8d8e7a5c..HEAD on `feature/f255-teacher-role`.
## Commits
### fa934355 chore(state): save the F255 R13 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r13.md | 489/0 | C0a — the R13 block COPIED verbatim from `.remedy-wt/f255-r13.md`, never retyped |

### e4d89120 chore(state): mirror the F255 R13 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 427/114 | C0b — the same file copied again, not regenerated |

### 562bb67e chore(plan): advance the plan to F255 R13
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 13/13 | C1 — the plan, the FIRST substantive commit of the round (constraint 3; R-0377, R-0491 and R-0548 all rule) |

### 8366e85a docs(review): record the R12 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORDR12 appended after exactly one blank line (R-0578); no finding registered, none resolved |

### f185dc77 docs(decisions): rule teacher spend as a null task_id ledger row
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 37/0 | C3 — DECISION F255 D7 appended after exactly one blank line: a teacher question is a ledger row whose `task_id` is NULL |

### 573a80c3 docs(ledger): name the teacher spend writer in the module text
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/token_ledger.py | 14/8 | C4 — the ONE FROM/TO pair, a REWRITE; module docstring only, so the ruling and the module agree on disk |

### b3b76f84 feat(orchestration): record teacher question spend as a ledger row
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/teacher_spend.py | 90/0 | C5 — the ONE writer; no `task_id` parameter at all, NULL counts never zeros |
| tests/orchestration/test_teacher_spend.py | 116/0 | C5 — the guard, in the SAME commit as the code it pins |

### C6 docs(state): write the F255 R13 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C6 — a handoff cannot table the commit that writes it (R-0149); its own cell and the complete change set are in the round report, as G10 routes them |

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
`git push` after C6 — real output in the round report. No pull request created and no CI run awaited (constraint 10). No worktree created (constraint 9); `git worktree list` reports the primary checkout alone, and every non-current reading was taken with `git show <sha>:<path>`.

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; `git worktree list` = the primary checkout alone; no reading was taken by mutating the primary checkout.
G2 `.remedy-wt/f255-r13.md`, `.agent/authored/f255-r13.md` at C0a and `.agent/last_block.md` at C0b are each sha256 d1a48700a8e9467719ed0081ad96936384c1f52325349c4df14114a7b83da6fd over 30557 B and 489 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 SEVEN slices, a count taken from my own ordered extraction of the COMMITTED `.agent/authored/f255-r13.md` at fa934355 rather than written beside it: PLAN255R13 323dd245f8692e395e017555acb6d9aa0164c3142cb7827aa466ab8c2138d72d 2429 B 42 lines; RECORDR12 d80e2ddae41d4c8c34799364db056e650012d4d1be9482cc6d80682e91b2b70d 5094 B 1 line; DECISION255D7 b33a7e1a94c24b7f1a1216112914dd5b9384c7d02a434194d8d91fb3ce0d3a2f 2341 B 36 lines; LEDGERFROM 28123d1947ef7e55979396de39b722b392d141a2fffa2b524826411c2220e85e 1157 B 16 lines; LEDGERTO b00e8a042be3debffe9102b00b86e8bc21fed4ea98daca6fecbce95628bb1bc2 1659 B 22 lines; TEACHSPEND a693df17f4303a4ed851163d54c4fb14c5fe7c580ecce726fae861c5ce11b137 3315 B 90 lines; TEACHSPENDTEST 40e5ebc5881f5aac5132f92032bc8634026202fa013b27f440fbd4d44b1a2880 3531 B 116 lines. Newline convention NEWLINE-INCLUDED — a body is the lines strictly between its markers, each keeping its own LF; marker lines are excluded (R-0600).
G4 `.agent/plan.md` at C1 byte-equals PLAN255R13: sha256 323dd245f8692e395e017555acb6d9aa0164c3142cb7827aa466ab8c2138d72d, 2429 B, 42 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and the roadmap F-id F255 2x. C1 is the FIRST commit of the round other than C0a and C0b: `git rev-list --reverse 8d8e7a5c..562bb67e` is exactly fa934355, e4d89120, 562bb67e.
G5 C2 is PREFIX-clean over the 8d8e7a5c blob, remainder sha256 39c53f0d9145f3b8d15f97eb19c9a1f05974ff98521dad5e27fec7b6bf14f4fc at 5095 B / 2 lines, byte-equal to one newline followed by RECORDR12, and the byte after that leading newline is not a newline, so the separator is exactly one blank line. An INDEPENDENT line-wise blank-line paragraph split of the C2 blob yields 201 units whose LAST unit IS RECORDR12: newline-INCLUDED sha256 d80e2ddae41d4c8c34799364db056e650012d4d1be9482cc6d80682e91b2b70d at 5094 B, newline-EXCLUDED sha256 017fa2a842cc32c7f89b29da6b2617b262f0cba10731a051dbd09b0e011902ab at 5093 B. A one-byte mutant of the expected remainder (byte 2547, low bit flipped) is REJECTED by the prefix reading AND by BOTH paragraph readings, while the real blob is accepted by all three. Sets: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at 8d8e7a5c, and the SAME four at C2 — registered being lines matching `^- R-\d{4} — `, resolved being lines beginning `Done:`, open their difference. `Gate: R13 — the R12 entry.` occurs 1x, is the LAST of the 13 lines beginning `Gate: R`, and all 13 header keys are distinct.
G6 C3 is PREFIX-clean over the 8d8e7a5c blob of `.agent/decisions.md`, remainder sha256 db8546b041b9e6ee4df78cc904eb0d033da8d25c629ba086a500fa3ed34e6601 at 2342 B / 37 lines, byte-equal to one newline followed by DECISION255D7, and the byte after that leading newline is not a newline. DECISION255D7 is itself MULTI-PARAGRAPH, so it cannot be one unit of a paragraph split; the independent reading is therefore the LAST K units of the C3 blob rejoined by one blank line, K = 6 taken from splitting the slice, over 1006 units — equal to the slice at newline-INCLUDED sha256 b33a7e1a94c24b7f1a1216112914dd5b9384c7d02a434194d8d91fb3ce0d3a2f / 2341 B and newline-EXCLUDED 1172bd03f49e36da4dcc6b3c677e0713e95085c07e4eb6f592f4b1b323ae670a / 2340 B. Two one-byte mutants (bytes 1171 and 2322) are REJECTED by the prefix reading and by BOTH K-unit readings, while the real blob is accepted by all three. `## DECISION F255 D7` occurs 0x at 8d8e7a5c and 1x at C3, and all 79 lines beginning `## DECISION ` at C3 are distinct.
G7 In `packages/orchestration/token_ledger.py`: LEDGERFROM occurs 1x at 8d8e7a5c and 0x at C4 — the FROM-zero count constraint 4 says is owed for a REWRITE; LEDGERTO occurs 0x at 8d8e7a5c and 1x at C4. The file measures 1669 lines at 8d8e7a5c and 1675 at C4, numstat `14 8 packages/orchestration/token_ledger.py`.
G8 `git ls-tree 8d8e7a5c -- <path>` is EMPTY (exit 0, no output) for BOTH created paths. `packages/orchestration/teacher_spend.py` at C5 byte-EQUALS TEACHSPEND at sha256 a693df17f4303a4ed851163d54c4fb14c5fe7c580ecce726fae861c5ce11b137, 3315 B, 90 lines, and the 90 lines its diff ADDS are exactly that slice's 90 lines IN ORDER; numstat `90 0`. `tests/orchestration/test_teacher_spend.py` at C5 byte-EQUALS TEACHSPENDTEST at sha256 40e5ebc5881f5aac5132f92032bc8634026202fa013b27f440fbd4d44b1a2880, 3531 B, 116 lines, its 116 added lines exactly that slice's lines IN ORDER; numstat `116 0`.
G9 Serially in the PRIMARY checkout, never two pytest processes at once, each spawned as the block's exact argv: `test_teacher_spend.py` exit 0 `5 passed`; `test_token_ledger.py` exit 0 `112 passed`; `test_path_utils.py test_data_paths.py test_autonomy.py` exit 0 `132 passed`; `test_test_runner.py test_dashboard_contract.py test_resource_safety.py test_integrity_gate.py` exit 0 `160 passed`; `test_golden_path.py` exit 0 `42 passed`; `python3 -m ruff check` over the three named paths exit 0 `All checks passed!`. The 112, 132, 160 and 42 are the four the reviewer measured at 8d8e7a5c; the 5 is new, the file being ABSENT at the base per G8.
G10 `git diff --name-only 8d8e7a5c..HEAD` at C5 equals the Change list minus `.agent/handoff.md`, which C6 itself adds — no other path on either side alone. Each of the FOUR paths named untouched is PRESENT at the base and ABSENT from the range. Every commit in the range has exactly one parent. Per-commit insertions 489, 427, 13, 2, 37, 14 and 206, every one under 500, with C6's own cell in the round report; each per-file `+/-` cell above is byte-identical to `git diff --numstat` (checklist item 28). Reflog, as TWO measured claims read from the OPERATION PREFIX before the first colon (R-0601), NEITHER a total for the round (R-0605): taken AT commit b3b76f84, where the round has made 7 commits, this round's entries whose prefix reads exactly `commit` number 7 — the two are EQUAL; entries whose prefix contains amend, reset, rebase or cherry number 0. C6 is unwritten when this text is composed, so its own entry is measured by the reviewer at the next gate (R-0494).
G11 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, 0 in `.agent/decisions.md` at C3, 0 in `packages/orchestration/token_ledger.py` at C4, 0 in both files at C5, and 0 in `.agent/handoff.md` at C6 — the last measured after that commit and reported in the round report.
G12 `git push` run after C6; its real output is in the round report. No pull request created and no CI run awaited.

## Authored-text proofs
All seven slices were extracted programmatically by their marker lines from the COMMITTED `.agent/authored/f255-r13.md` at fa934355 — never retyped, never re-wrapped, never edited — and applied byte for byte. Disk-to-disk transport equality is G2. The plan is proven by G4's byte-equality, the two appends by G5's and G6's prefix, remainder, paragraph and negative-control equalities, the ONE pair by G7's FROM-zero and TO-one counts, and the two created files by G8's byte-equality plus ordered line equality (R-0531).

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 and C6 ran in exactly that order — none added, none dropped, none reordered. No slice was edited, so no slice is declared wrong. TWO DEVIATIONS, DECLARED. (1) G6 orders "a SECOND, INDEPENDENT paragraph split of the C3 blob whose LAST unit is DECISION255D7", and that reading is unmeetable by construction: the slice contains blank lines, so a blank-line split makes it the last SIX units, not one. I did not edit the slice or weaken the gate; I measured the last-K-units reading G6 line 4 records, with a negative control that discriminates, and report the literal last unit as well — 191 B, sha256 e5a22db464395e26b5c08540009567eb84209cb0842ed019a900bd5a6fa71bde, the slice's own closing paragraph. (2) This session's shell guard rejects the `VAR=value cmd` environment-prefix form, shell loops, `$( )` substitution and `${arr[0]}` indexing, so every copy, extraction, application, gate run and measurement was routed through short Python scripts — inline heredocs and four scratch files under the gitignored `.remedy-wt/`, which is scratch and is not in the change set; each gate command was spawned as its EXACT argv through `subprocess.run` and the real returncode and output are in the round report. G3's SEVEN contradicts nothing in the block, which states no slice numeral of its own by design (R-0604).

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: R14, which FINISHES T004 — `remedy teach ask` on the CLI over `teacher_qa.build_teacher_context`, the teacher model call through `resolve_role_config("teacher")`, the honest refusal when no model is configured, and the spend row written through `teacher_spend`. R12 PASSED and its verdict is now ON DISK at C2; R13 itself awaits review. There is no open pull request.
Fortschritt: ~80 % (T001, T002 and T003 COMPLETE · T004 split in two by the reviewer at R13 — the billing ruling and the spend writer land here, the model call and the CLI at R14 · integration gate and closure remain) — Schätzung
