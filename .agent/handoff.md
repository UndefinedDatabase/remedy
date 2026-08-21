# Handback — F255 R17 (R16's verdict recorded; grounding source (2) given a production caller)
## Range
Review of 8f885b4f..HEAD on `feature/f255-teacher-role`.
## Commits
### f0287557 chore(state): save the F255 R17 block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r17.md | 284/0 | C0a — the R17 block COPIED verbatim from `.remedy-wt/f255-r17.md`, never retyped |

### cbe83001 chore(state): mirror the F255 R17 block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 190/384 | C0b — the same file copied again, not regenerated |

### 0f2b3968 chore(plan): advance the plan to F255 R17
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 14/17 | C1 — the plan, the FIRST substantive commit (constraint 3; R-0377, R-0491, R-0548) |

### 76d2d941 docs(review): register findings R-0608, R-0609 and R-0610
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 6/0 | C2 — FINDINGS3 appended after exactly one blank line (R-0578); THREE registrations, blank-separated from each other |

### 8729b4d4 docs(review): record the R16 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C3 — RECORDR16 appended after exactly one blank line; a `Gate:` paragraph, so it registers and resolves nothing |

### da0ed2d9 feat(cli): ground teach ask in a workspace file with --file
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 4/0 | C4 — ONE new `ArgDef("--file", ...)` on `teach.ask`; the entry stays `write_metadata` (F255 D10) |
| apps/cli/commands/teach_cmd.py | 55/1 | C4 — `_read_grounding_file` plus the `file` parameter; the SAME `code`/`code_path` reach both contexts |

### aa3a47c9 test(cli): pin teach ask --file to grounding source 2
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_teach_cmd.py | 104/0 | C5 — the four required proofs and a prompt-capturing seam; ordered as its own commit per R-0609 |

### C6 docs(state): write the F255 R17 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C6 — a handoff cannot table the commit that writes it (R-0149); its cell and the complete change set are in the round report |

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
`git push` after C6 — real output in the round report. No pull request created and no CI run awaited (constraint 12). No worktree created; `git worktree list` reports the primary checkout alone, and every non-current reading was taken with `git show <sha>:<path>`.

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; `git worktree list` = the primary checkout alone.
G2 `.remedy-wt/f255-r17.md`, `.agent/authored/f255-r17.md` at C0a and `.agent/last_block.md` at C0b are each sha256 45fedbdf8ed39f04a92e08678161cb83fe2eb46e39d3bb7dfc4f30c58ca615a4 over 31242 B and 284 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 THREE slices, a count taken from my own ordered extraction of the COMMITTED `.agent/authored/f255-r17.md` at f0287557 rather than written beside it (R-0604): PLAN255R17 7f7d6271e0d09f130fabb8b2a8c74a850424614d1263fd43958436bcbb6c09eb 2125 B 38 lines; FINDINGS3 2811b7b659491067cb99b4f427c305268859dbfea8589a679b3de93fc8c2e6ba 6444 B 5 lines; RECORDR16 4bfca993fc0d86e43febcfae5248ce2c8bd0c71e84c9714641b4f38b3814714e 5940 B 1 line. Newline convention NEWLINE-INCLUDED — a body is the lines strictly between its markers, each keeping its own LF; marker lines excluded (R-0600).
G4 `.agent/plan.md` at C1 byte-equals PLAN255R17: sha256 7f7d6271e0d09f130fabb8b2a8c74a850424614d1263fd43958436bcbb6c09eb, 2125 B, 38 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and the roadmap F-id F255 present. C1 is the FIRST commit of the round other than C0a and C0b: `git log --reverse 8f885b4f..0f2b3968` opens f0287557, cbe83001, 0f2b3968.
G5 The 8f885b4f blob of `.agent/live_review.md` is a byte-exact PREFIX of the C2 blob; remainder sha256 e9594e8e6445b6bfb2bf163fe2d33732f2238b86492522c52827d2239d172a08 at 6445 B / 6 lines, byte-equal to one newline followed by FINDINGS3, the byte after that leading newline being `-`, not a newline. TWO INDEPENDENT EXTRACTIONS AGREE (R-0578): the blank-line split of FINDINGS3 gives 3 units, ids R-0608, R-0609, R-0610; collecting the C2 blob's `^- R-\d+ — ` lines absent at the base gives 3 lines, the same ids in the same order.
G6 C3 over the C2 blob: byte-exact PREFIX; remainder sha256 06f49656fae03c3cad56fabb94f8fa69dfa4ef80e84edf1bab8a2a4f6a49fc03 at 5941 B / 2 lines, byte-equal to one newline followed by RECORDR16, the byte after that newline being `G`. SECOND, INDEPENDENT blank-line paragraph split of the C3 blob: 210 units whose LAST unit IS RECORDR16 — newline-INCLUDED 4bfca993fc0d86e43febcfae5248ce2c8bd0c71e84c9714641b4f38b3814714e at 5940 B, newline-EXCLUDED 36ae312ce7b6b6d67cf438993740dc1c50a73ec44812868585d1e0111463a099 at 5939 B. I re-measured constraint 6 rather than trusting it: RECORDR16 holds no interior blank line, so it is exactly 1 unit and the LAST-UNIT reading is exact. NO paragraph reading is ordered or reported for FINDINGS3, which is MULTI-paragraph. Negative controls: for EACH of C2 and C3 a one-byte mutant of the expected remainder is REJECTED by the prefix-and-remainder reading while the real blob is accepted.
G7 Sets over `.agent/live_review.md`, registered being lines matching `^- R-\d+ — ` and resolved lines matching `^Done: R-\d+ — `: 183 / 3 / 180 / 0 at 8f885b4f; 186 / 3 / 183 / 0 at C2, the three new registered lines; and the SAME 186 / 3 / 183 / 0 at C3, a `Gate:` paragraph adding neither kind of line. Each of R-0608, R-0609 and R-0610 occurs 0x at 8f885b4f. `Gate: R17 — the R16 entry.` occurs 1x at C3, is the LAST of the 17 lines beginning `Gate: R`, and all 17 header keys are distinct. Counted LINE-ANCHORED, never as substrings (R-0584).
G8 `python3 -m pytest tests/cli/test_teach_cmd.py tests/test_command_catalog.py -q -rf` exit 0, `37 passed in 0.37s`. The four required proofs, all in `TestTeachAskGroundsInAWorkspaceFile`: `test_the_file_reaches_the_prompt_and_the_grounding_sources`, `test_without_the_option_no_code_reaches_the_prompt`, `test_an_unreadable_path_is_said_out_loud_and_the_answer_still_comes`, `test_reading_a_file_writes_nothing_and_leaves_it_untouched`. CALLER MEASUREMENT, taken by parsing every tracked `.py` outside `tests/` at each commit and reading each `ask_teacher` call's keywords from the AST rather than from a grep: at 8f885b4f exactly ONE caller, `_cmd_teach_ask` in `apps/cli/commands/teach_cmd.py`, passing NEITHER `code` nor `code_path` — the defect R-0610 names; at C5 exactly ONE caller, the same `_cmd_teach_ask`, now passing BOTH.
G9 `python3 -m ruff check apps/cli/commands/teach_cmd.py apps/cli/command_catalog.py tests/cli/test_teach_cmd.py` on ruff 0.15.17 exit 0, `All checks passed!` — no rule code appears at all, so none is new against the base reading. `python3 -m pytest tests/orchestration/test_teacher_model.py -q -rf` exit 0, `18 passed in 0.27s`, run serially in the PRIMARY checkout.
G10 R-0607's own rule obeyed unconditionally, run SERIALLY in the PRIMARY checkout, never two pytest processes at once: `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` exit 0, `160 passed in 19.97s`; then `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, `42 passed in 20.50s`.
G11 `git diff --name-only 8f885b4f..aa3a47c9` equals the Change list minus `.agent/handoff.md`, which C6 itself adds — no path on either side alone. Each of the SIX paths named untouched is PRESENT at the base and ABSENT from the range. Every commit in the range has exactly one parent. Per-commit insertions 284, 190, 14, 6, 2, 59 and 104, every one under 500; each per-file `+/-` cell above is byte-identical to `git diff --numstat` (checklist item 28). Reflog, read from the OPERATION PREFIX before the first colon and NEITHER claim a total (R-0601, R-0605): taken AT commit aa3a47c9, where the round has made 7 commits, this round's entries whose prefix reads exactly `commit` number 7 — the two are EQUAL. Entries of this round whose prefix contains `amend`, `rebase` or `cherry` number 0, as R-0608 rules the clause should be written; and this round produced NO `reset` entry at all, so none is owed a destination demonstration. C6 is unwritten as this is composed, so the reviewer measures its entry at the next gate (R-0494).
G12 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C3, and 0 in `.agent/handoff.md` at C6 — the last measured after that commit and reported in the round report. `git push` run after C6; its real output is in the round report. No pull request created and no CI run awaited.

## Authored-text proofs
All THREE slices were extracted programmatically by their marker lines from the COMMITTED `.agent/authored/f255-r17.md` at f0287557 — never retyped, never re-wrapped, never edited — and applied byte for byte. Disk-to-disk transport equality is G2. The plan is proven by G4's byte-equality; the two appends by G5's and G6's prefix, remainder, separator, dual-extraction and negative-control equalities, plus the paragraph reading for RECORDR16 alone. NO FROM/TO pair exists this round, so no containment reading and no FROM-zero count is owed (constraint 7, §4.9, R-0207). The code of C4 and C5 is NOT authored text: I wrote it to the block's specification and it carries no transport proof.

## Deviations & assumptions
NO DEVIATIONS. The ordered bundle C0a..C6 was executed in order, one commit each, with no extra commit, no dropped commit and no reordering; no slice was edited and no slice is declared wrong. ASSUMPTION: this session's shell guard rejects `VAR=value cmd` prefixes, shell loops, `$( )`, `${arr[0]}` and brace literals containing quotes, so every copy, extraction, application and measurement ran through short Python scripts — heredocs and one scratch file under the gitignored `.remedy-wt/`, which is scratch and NOT in the change set — with git, pytest and ruff spawned as exact argv through `subprocess.run`, so every exit code above is the real one. ASSUMPTION on the reflog reading: this round's entries are those newer than the entry recording the base 8f885b4f, taken positionally from `git reflog` rather than by SHA membership, which is the stricter of the two readings.

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: the INTEGRATION GATE round per docs/agents/integration_gate.md, the full suite, because T002, T003 and T004 all touch the CLI catalog that the parser and the help renderer both read. R16 PASSED; its verdict is ON DISK at C3 and its three findings at C2. R-0610's CODE half is fixed this round — `remedy teach ask --file` is grounding source (2)'s first production caller — but only the reviewer's own text at the next gate may RESOLVE it, and this block authored no resolution for it. R-0607, R-0608 and R-0609 REMAIN OPEN: R-0607 needs a docs round promoting its rule into the docs/agents/planner_reviewer_prompt.md §3 checklist, and R-0608 and R-0609 bind future blocks rather than this code. R17 ITSELF IS THE ROUND WHOSE VERDICT IS NOT ON DISK, so it awaits review. There is no open pull request.
Fortschritt: ~90 % (T001, T002 and T003 COMPLETE · T004 COMPLETE now that grounding source (2) has a production caller — at R16 it did not, which is R-0610 · integration gate and closure remain) — Schätzung
