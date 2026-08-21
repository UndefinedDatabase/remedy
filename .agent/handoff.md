# Handback — F255 R16 (T004 FINISHED: the teacher's model seam, ruled, built and CALLED)
## Range
Review of 2e5b8299..HEAD on `feature/f255-teacher-role`.
## Commits
### 883b9886 chore(state): save the F255 R16 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r16.md | 478/0 | C0a — the R16 block COPIED verbatim from `.remedy-wt/f255-r16.md`, never retyped |

### 6d137821 chore(state): mirror the F255 R16 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 402/131 | C0b — the same file copied again, not regenerated |

### 9dfbcd4a chore(plan): advance the plan to F255 R16
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 18/20 | C1 — the plan, the FIRST substantive commit (constraint 3; R-0377, R-0491, R-0548) |

### 27941050 docs(review): record the R15 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORDR15 appended after exactly one blank line (R-0578); a `Gate:` paragraph, so it registers and resolves nothing |

### 85ea2d43 docs(decisions): rule the teacher model seam, the refusal and the action class
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 103/0 | C3 — DECISIONS255 appended after exactly one blank line: F255 D8, D9 and D10 |

### cbcc65e1 docs(roadmap): amend F255 for the model seam, the refusal and the action class
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F255.md | 27/0 | C4 — AMEND255 appended after exactly one blank line; the two superseded phrases and the seam |

### c2f31bdb feat(teacher): add the teacher model transport and its ask seam
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/teacher_model.py | 259/0 | C5a — the module half of the split C5 (see Deviations); written by me to the block's spec, not a slice |

### 8120646c test(teacher): pin the model seam, the refusal and the single spend row
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_teacher_model.py | 283/0 | C5b — the test half of the split C5; 18 tests, every one offline |

### 9f656f6d feat(cli): add remedy teach ask and declare it in the catalog
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 20/0 | C6 — ONE entry, `teach.ask`, `write_metadata` per F255 D10 |
| apps/cli/commands/teach_cmd.py | 118/14 | C6 — `_cmd_teach_ask` and its handler; the docstring now covers both commands |
| tests/cli/test_teach_cmd.py | 15/1 | C6 — the pin EXTENDED in the same commit as the entry it guards, still an EQUALITY |

### 9526104b test(cli): prove teach ask writes only the ledger and never bills a refusal
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_teach_cmd.py | 223/9 | C7 — the four behavioural proofs, all with an injected `call` |

### C8 docs(state): write the F255 R16 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C8 — a handoff cannot table the commit that writes it (R-0149); its cell and the complete change set are in the round report |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | deviated | split into c2f31bdb (259 ins) + 8120646c (283 ins): as ONE commit it was 542 insertions, over the 500 cap G13 pins |
| C6 | done | |
| C7 | done | |
| C8 | done | |

## External actions
`git push` after C8 — real output in the round report. No pull request created and no CI run awaited (constraint 12). No worktree created; `git worktree list` reports the primary checkout alone, and every non-current reading was taken with `git show <sha>:<path>`.

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; `git worktree list` = the primary checkout alone.
G2 `.remedy-wt/f255-r16.md`, `.agent/authored/f255-r16.md` at C0a and `.agent/last_block.md` at C0b are each sha256 8e40970251874febe66b0d0b66ea213d8fcf1df902652013fed3ed77f3565a2e over 36286 B and 478 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 FOUR slices, a count taken from my own ordered extraction of the COMMITTED `.agent/authored/f255-r16.md` at 883b9886 rather than written beside it (R-0604): PLAN255R16 a9f93d981010431d2c67c995bbe283846a1a6192aa063223da9aa79c6ceea6e1 2245 B 41 lines; RECORDR15 9ed4d44468e46c7b85204a7a4fc0d7f9410c111fb93216b0f7396928c3ddbbdd 4742 B 1 line; DECISIONS255 02427bbaeb2ef1fd91b810ec6f612622e4dc04981f8c1c7c4a674c554f4ace70 6297 B 102 lines; AMEND255 b201ac7aece30e31a0d9654d4d72e22289ec5e73a4dacaa6471b521a2a46ceb9 1765 B 26 lines. Newline convention NEWLINE-INCLUDED — a body is the lines strictly between its markers, each keeping its own LF; marker lines excluded (R-0600).
G4 `.agent/plan.md` at C1 byte-equals PLAN255R16: sha256 a9f93d981010431d2c67c995bbe283846a1a6192aa063223da9aa79c6ceea6e1, 2245 B, 41 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and the roadmap F-id F255 present 3x. C1 is the FIRST commit of the round other than C0a and C0b: `git log --reverse 2e5b8299..HEAD` opens 883b9886, 6d137821, 9dfbcd4a.
G5 The 2e5b8299 blob of `.agent/live_review.md` is a byte-exact PREFIX of the C2 blob; remainder sha256 899dc2a1d5f3f9b022a0f99fd28e8a9f4699ad341e772320a9da5aed58a4923c at 4743 B / 2 lines, byte-equal to one newline followed by RECORDR15, the byte after that leading newline being `G`, not a newline. SECOND, INDEPENDENT blank-line paragraph split of the C2 blob: 206 units whose LAST unit IS RECORDR15 — newline-INCLUDED 9ed4d44468e46c7b85204a7a4fc0d7f9410c111fb93216b0f7396928c3ddbbdd at 4742 B, newline-EXCLUDED df9005d13738a73b0d02e4097c83d7bf8a60c28d99ce38db1df5a4ccb5f6aa9b at 4741 B. I re-measured constraint 5 rather than trusting it: RECORDR15 holds no interior blank line, so it is exactly 1 unit and the LAST-UNIT reading is exact. Negative control: a one-byte mutant of the expected remainder is REJECTED by BOTH readings while the real blob is accepted by both.
G6 C3 over `.agent/decisions.md`: the 2e5b8299 blob is a byte-exact PREFIX; remainder sha256 953ffffe7c49596e9cbe02bc4abe2097b267052abb7c1d809c8907567c0158fc at 6298 B / 103 lines, byte-equal to one newline followed by DECISIONS255, the byte after that newline being `#`. C4 over `docs/roadmap/features/T5_F255.md`: same prefix reading; remainder sha256 511d83891d9d9112c08481c2a979c5b4b5fbc45c709e869d03f64f029d1d0ee0 at 1766 B / 27 lines, byte-equal to one newline followed by AMEND255, the byte after that newline being `#`. NO paragraph reading is ordered or reported for either: both slices are MULTI-paragraph, so the prefix-and-remainder reading is their whole proof (constraint 5, R-0606). LINE-ANCHORED, `## DECISION F255 D8`, `## DECISION F255 D9` and `## DECISION F255 D10` each occur 0x at 2e5b8299 and 1x at C3.
G7 Sets over `.agent/live_review.md`, registered being lines matching `^- R-\d+ — ` and resolved lines matching `^Done: R-\d+ — `: 183 / 3 / 180 / 0 at 2e5b8299 and the SAME 183 / 3 / 180 / 0 at C2 — a `Gate:` paragraph adds neither kind of line. `Gate: R16 — the R15 entry.` occurs 0x at 2e5b8299 and 1x at C2, is the LAST of the 16 lines beginning `Gate: R`, and all 16 header keys are distinct. Counted LINE-ANCHORED, never as substrings (R-0584).
G8 `python3 -m pytest tests/orchestration/test_teacher_model.py -q -rf` exit 0, `18 passed in 0.32s`. `python3 -m ruff check packages/orchestration/teacher_model.py tests/orchestration/test_teacher_model.py` exit 0, `All checks passed!` on ruff 0.15.17. NO test in that file opens a socket: every `ask_teacher` test injects `call` and every `ollama_teacher_call` test replaces `sys.modules["ollama"]` with an in-process fake — proven, not asserted, by a control run of the same file under a plugin that raises on `socket.connect`, exit 0 at 18 passed, with a deliberately-connecting control test RED under that same plugin. The default seam is pinned by `TestTheInjectedSeam::test_the_default_transport_is_ollama_teacher_call_by_identity`, which asserts the object that ran IS `teacher_model.ollama_teacher_call` and never invokes the real transport.
G9 `python3 -m pytest tests/cli/test_teach_cmd.py tests/test_command_catalog.py -q -rf` exit 0, `33 passed in 0.30s`. `get_command("teach.ask").action_class` is `write_metadata`; `get_commands_for_group("teach")` and `set(COMMAND_HANDLERS)` are both `['teach.ask', 'teach.narrate']` and EQUAL as sets. The pin `test_the_handler_table_covers_every_declared_teach_command` still reads `assert declared == {"teach.narrate", "teach.ask"} == set(COMMAND_HANDLERS)` — an EQUALITY of the two sets, widened by exactly one id in the SAME commit as the entry it guards, never weakened to a subset.
G10 `python3 -m pytest tests/cli/test_teach_cmd.py -q -rf` exit 0, `15 passed in 0.27s`. The four required proofs: `TestTeachAskWritesOnlyTheLedger::test_asking_changes_no_byte_under_the_data_root_except_the_ledger` and its partner `::test_the_excluded_set_is_exactly_the_ledger_and_its_sidecars`; `TestTeachAskWritesExactlyOneRow::test_one_ask_writes_exactly_one_teacher_row` with `::test_the_role_split_reports_teacher_apart_from_the_mission_roles`; `TestTeachAskRefusesWithoutBilling::test_a_provider_with_no_teacher_transport_refuses_and_writes_no_row`; and `::test_a_failing_transport_refuses_and_writes_no_row`. The read-only exclusion filter, verbatim, is `not (excluding is not None and path.name.startswith(excluding))` with `excluding=_LEDGER_NAME_PREFIX` and `_LEDGER_NAME_PREFIX = "ledger.sqlite"`; the partner test asserts the excluded set EQUALS the paths whose file name starts with that prefix and that the set is non-empty.
G11 Serially, in the PRIMARY checkout: `python3 -m pytest tests/docs/ -q -rf` exit 0, `295 passed in 0.52s`; then `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf` exit 0, `30 passed in 0.41s`.
G12 R-0607's own rule obeyed, run SERIALLY in the PRIMARY checkout, never two pytest processes at once: `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` exit 0, `160 passed in 20.06s`; then `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, `42 passed in 21.56s`.
G13 `git diff --name-only 2e5b8299..9526104b` equals the Change list minus `.agent/handoff.md`, which C8 itself adds — no path on either side alone. Each of the FIVE paths named untouched is PRESENT at the base and ABSENT from the range. Every commit in the range has exactly one parent. Per-commit insertions 478, 402, 18, 2, 103, 27, 259, 283, 153 and 223, every one under 500; each per-file `+/-` cell above is byte-identical to `git diff --numstat` (checklist item 28). Reflog, as TWO measured claims read from the OPERATION PREFIX before the first colon (R-0601), NEITHER a total (R-0605): taken AT commit 9526104b, where the round has made 10 commits, this round's entries whose prefix reads exactly `commit` number 10 — the two are EQUAL. Entries whose prefix contains amend, reset, rebase or cherry number ONE, not zero: a single `reset: moving to HEAD` at new-HEAD cbcc65e1 — see Deviations. C8 is unwritten as this is composed, so the reviewer measures its entry at the next gate (R-0494).
G14 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, 0 in `.agent/decisions.md` at C3, 0 in `docs/roadmap/features/T5_F255.md` at C4, and 0 in `.agent/handoff.md` at C8 — the last measured after that commit and reported in the round report. `git push` run after C8; its real output is in the round report. No pull request created and no CI run awaited.

## Authored-text proofs
All FOUR slices were extracted programmatically by their marker lines from the COMMITTED `.agent/authored/f255-r16.md` at 883b9886 — never retyped, never re-wrapped, never edited — and applied byte for byte. Disk-to-disk transport equality is G2. The plan is proven by G4's byte-equality; the three appends by G5's and G6's prefix, remainder, separator and (for RECORDR15 alone) paragraph and negative-control equalities. NO FROM/TO pair exists this round, so no containment reading and no FROM-zero count is owed (constraint 6, §4.9, R-0207). The code of C5, C6 and C7 is NOT authored text: I wrote it to the block's specification and it carries no transport proof.

## Deviations & assumptions
TWO DEVIATIONS, BOTH DECLARED. (1) C5 WAS SPLIT INTO TWO COMMITS. As one commit its two new files were 542 insertions — over the 500-line cap AGENTS.md sets and G13 re-pins — so `packages/orchestration/teacher_model.py` landed at c2f31bdb (259) and `tests/orchestration/test_teacher_model.py` at 8120646c (283). Nothing else changed: same files, same content, same order, and the module is committed before the tests that hold it to its spec. (2) THE REFLOG CARRIES ONE `reset` ENTRY, which G13 demands be 0. It is `reset: moving to HEAD` at new-HEAD cbcc65e1 — the bare `git reset` I ran to UNSTAGE the already-staged C5 pair before splitting it. It moved HEAD nowhere: its new HEAD equals its old HEAD, no commit was created, rewritten, dropped or reordered, and `git log --reverse 2e5b8299..HEAD` still lists the ten commits in the block's order, each with one parent. I report the real 1 rather than a convenient 0. No slice was edited and no slice is declared wrong. ASSUMPTION: this session's shell guard rejects `VAR=value cmd` prefixes, shell loops, `$( )`, `${arr[0]}` and brace literals containing quotes, so every copy, extraction, application and measurement ran through short Python scripts — heredocs and scratch files under the gitignored `.remedy-wt/`, which is scratch and NOT in the change set — with git, pytest and ruff spawned as exact argv through `subprocess.run`, so every exit code above is the real one. SIZE: this handback is 102 lines and the range `2e5b8299..HEAD` holds ELEVEN commits, so the template's >10-commit allowance (≤160) is the bound that applies; no mandated section was dropped to reach it.

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: the INTEGRATION GATE round per docs/agents/integration_gate.md, which follows T004 because T002, T003 and T004 all touch the CLI catalog that the parser and the help renderer both read. R15 PASSED and its verdict is ON DISK at C2. This round registered NO finding and resolved NONE: registered stays 183, resolved stays 3. R-0607 REMAINS OPEN — only a docs round promoting its rule into the docs/agents/planner_reviewer_prompt.md §3 checklist closes it; R16 obeyed the rule at G12 without closing the finding. R16 ITSELF IS THE ROUND WHOSE VERDICT IS NOT ON DISK, so it awaits review. There is no open pull request.
Fortschritt: ~88 % (T001, T002 and T003 COMPLETE · T004 COMPLETE at this round — the model seam is built, ruled and CALLED by `remedy teach ask`, and teacher spend lands as its own ledger role · integration gate and closure remain) — Schätzung
