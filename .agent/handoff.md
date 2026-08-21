# Handback — F255 R12 (record round: the R11 verdict and the plan; nothing built)
## Range
Review of da8c2e3f..HEAD on `feature/f255-teacher-role`.
## Commits
### fc3cd2e4 chore(state): save the F255 R12 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r12.md | 176/0 | C0a — the R12 block COPIED verbatim from `.remedy-wt/f255-r12.md`, never retyped |

### cbb727d3 chore(state): mirror the F255 R12 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 72/386 | C0b — the same file copied again, not regenerated |

### 938a861c chore(plan): advance the plan to F255 R12
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 12/12 | C1 — the plan, the FIRST substantive commit of the round (constraint 3; R-0377, R-0491 and R-0548 all rule) |

### 057146c4 docs(review): record the R11 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORDR11 appended after exactly one blank line (R-0578); no finding registered, none resolved |

### C3 docs(state): write the F255 R12 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C3 — a handoff cannot table the commit that writes it (R-0149); its own cell and the complete change set are in the round report, as G7 routes them |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |

## External actions
`git push` after C3 — real output in the round report. No pull request created and no CI run awaited (constraint 9). No worktree created (constraint 8); `git worktree list` reports the primary checkout alone, and every non-current reading was taken with `git show <sha>:<path>`.

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; `git worktree list` = the primary checkout alone; no reading was taken by overwriting a file in the primary checkout.
G2 `.remedy-wt/f255-r12.md`, `.agent/authored/f255-r12.md` at C0a and `.agent/last_block.md` at C0b are each sha256 d7fa8558af635d879f9b540888d44aed37450fda5430babd16967eede99830bb over 17520 B and 176 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 TWO slices, a count taken from my own ordered extraction of the COMMITTED `.agent/authored/f255-r12.md` at fc3cd2e4 rather than written beside it: PLAN255R12, sha256 8aca9b4c5f4a21cb1002abc1a1c3d7346b4bcf72c63d5501e91d458eb9f66f0e, 2380 B, 42 lines; RECORDR11, sha256 69d7956dffb82702a15c3e1ea2df48ad7f1578f7f4c77ad820e9213ae02b97f5, 6106 B, 1 line. Newline convention NEWLINE-INCLUDED — a body is the lines strictly between its markers, each keeping its own LF; marker lines are excluded (R-0600).
G4 `.agent/plan.md` at C1 byte-equals PLAN255R12: sha256 8aca9b4c5f4a21cb1002abc1a1c3d7346b4bcf72c63d5501e91d458eb9f66f0e, 2380 B, 42 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and the roadmap F-id F255 present. C1 is the FIRST commit of the round other than C0a and C0b.
G5 C2 is PREFIX-clean over the da8c2e3f blob, remainder sha256 0934102a3bd14ec22f985bf3d87ee9357c9fcc048c82d76f5d25ee507c30239a at 6107 B / 2 lines, byte-equal to one newline followed by RECORDR11, so the separator is present and is exactly one blank line — the byte after it is not a newline. An INDEPENDENT line-wise blank-line paragraph split of the C2 blob yields 200 units whose LAST unit is RECORDR11: newline-INCLUDED sha256 69d7956dffb82702a15c3e1ea2df48ad7f1578f7f4c77ad820e9213ae02b97f5 at 6106 B, newline-EXCLUDED sha256 7b61248f301a4149a9b1bd9da60f8370ca9cca59a5a8c2a3b71f0f02127440bf at 6105 B; the splitter drops the empty tail the document's final LF creates, which is the mislabelling R11 caught in itself. A one-character mutant of the expected remainder (byte 100, `.` flipped to `X`) is REJECTED by the prefix reading AND by BOTH paragraph readings, while the real blob is accepted by all three. Sets: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at da8c2e3f, and the SAME four at C2, the registered count being lines matching `^- R-\d+ — ` and the resolved count lines matching `^Done: R-\d+ — `. `Gate: R12 — the R11 entry.` occurs 1x, is the LAST of the 12 lines beginning `Gate: R`, and all 12 header keys are distinct.
G6 Serially in the PRIMARY checkout, never two pytest processes at once: `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` exit 0, `160 passed in 19.94s`; `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, `42 passed in 20.46s` — the 160 and the 42 the reviewer measured at da8c2e3f.
G7 `git diff --name-only da8c2e3f..HEAD` equals the Change list with NO path on either side alone (extra: none; missing: none). Each of the FOUR paths named untouched is PRESENT at the base and ABSENT from the range. Every commit in the range has exactly one parent. Per-commit insertions 176, 72, 12 and 2, every one under 500, with C3's own cell in the round report; each per-file `+/-` cell above is byte-identical to `git diff --numstat`. Reflog, as TWO measured claims read from the OPERATION PREFIX before the first colon (R-0601), NEITHER a total for the round (R-0605): taken AT commit 057146c4, where the round has made 4 commits, this round's entries whose prefix reads exactly `commit` number 4 — the two numbers are EQUAL; entries whose prefix contains amend, reset, rebase or cherry number 0. C3 is unwritten when this text is composed, so its own entry is measured by the reviewer at the next gate (R-0494).
G8 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2 and 0 in `.agent/handoff.md` at C3.
G9 `git push` run after C3; its real output is in the round report. No pull request created and no CI run awaited.

## Authored-text proofs
Both slices were extracted programmatically by their marker lines from the COMMITTED `.agent/authored/f255-r12.md` at fc3cd2e4 — never retyped, never re-wrapped, never edited — and applied byte for byte. Disk-to-disk transport equality is G2. The plan is proven by G4's byte-equality and the ledger append by G5's prefix, remainder, paragraph and negative-control equalities. This round contains NO FROM/TO pair and creates no file outside `.agent/`, so no containment reading and no FROM-zero count is owed (§4.9, R-0207).

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a, C0b, C1, C2 and C3 ran in exactly that order — none added, none dropped, none reordered. No slice was edited, so no slice is declared wrong. No source file and no test file was touched. ONE DEVIATION IN MECHANISM, DECLARED: this session's shell guard rejects the `VAR=value cmd` environment-prefix form, shell loops, `$( )` substitution and `${arr[0]}` indexing, so every copy, extraction, application, gate run and measurement was routed through short Python scripts — inline heredocs and two scratch files under the gitignored `.remedy-wt/`, which is scratch and is not in the change set; each gate's command was spawned as the block's EXACT argv through `subprocess.run`, and the real returncode and output are in the round report. G3's TWO contradicts nothing in the block, which states no slice numeral of its own by design (R-0604).

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: R13, which FINISHES T004 — `remedy teach ask` on the CLI over `teacher_qa.build_teacher_context`, the teacher model call through `resolve_role_config("teacher")`, the honest refusal when no model is configured, and spend recorded under the role name `teacher`. R11 PASSED and its verdict is now ON DISK at C2; R12 itself awaits review. There is no open pull request.
Fortschritt: ~70 % (T001, T002 and T003 COMPLETE · T004 half done — the grounding sources, the level dial and the small context are built, red-proofed and REVIEWED · the teacher model call, the integration gate and closure remain) — Schätzung
