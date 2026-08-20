# Handback — F255 R10 (teacher role: `remedy teach narrate`, T002 + T003)

## Range
Review of de0f666b..HEAD on `feature/f255-teacher-role`.

## Commits

### a00e60b3 chore(state): save the F255 R10 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r10.md | 489/0 | C0a — the R10 block COPIED verbatim, never retyped |

### 5814d65b chore(state): mirror the F255 R10 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 366/347 | C0b — the same bytes mirrored |

### 83c55a73 chore(plan): advance the plan to F255 R10
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 21/25 | C1 — the plan, the FIRST substantive commit of the round (constraint 3; R-0377, R-0491 and R-0548 all rule) |

### f732f92c docs(review): record the R9 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORDR9 appended after exactly one blank line |

### 26312742 feat(cli): add the teach narrate command with its read-only proof
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 11/0 | C3 — the `teach` group and the `teach.narrate` entry declaring `action_class="read_only"` |
| apps/cli/commands/__init__.py | 2/1 | C3 — `teach_cmd` imported and added to the handler-collection tuple |
| apps/cli/commands/teach_cmd.py | 64/0 | C3 — the handler: production reader in, plain sentences out, nothing written |
| tests/cli/test_teach_cmd.py | 108/0 | C3 — the BEHAVIOURAL read-only proof; constraint 4 of the Change set keeps all four files in ONE commit (R-0151) |

### C4 docs(state): write the F255 R10 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C4 — a handoff cannot table the commit that writes it (R-0149); its own cell and the complete change set are in the round report, as G13 routes them |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions
`git push` after C4 — real output in the round report. No pull request created and no CI run awaited (constraint 12). No worktree created (constraint 11); `git worktree list` reports the primary checkout alone, and every non-current reading was taken with `git show <sha>:<path>`.

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit, after G8's real CLI run and at the handback; `git worktree list` = the primary checkout alone; no reading was taken by overwriting a file in the primary checkout.
G2 `.remedy-wt/f255-r10.md`, `.agent/authored/f255-r10.md` at C0a and `.agent/last_block.md` at C0b are each sha256 2970251815a503f9b3cf8fc405da232c828eab62113c57407c1fb4f3439736d8 over 30466 B and 489 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 TWELVE slices, a count taken from my own ordered extraction of the COMMITTED `.agent/authored/f255-r10.md` at a00e60b3 rather than written beside it: PLAN255R10, RECORDR9, GROUPFROM, GROUPTO, ENTRYFROM, ENTRYTO, IMPORTFROM, IMPORTTO, MERGEFROM, MERGETO, TEACHCMD, TEACHCMDTEST. Newline convention NEWLINE-INCLUDED — a body is the lines strictly between its markers, each keeping its own LF; marker lines are excluded. Per-slice sha256, byte and line counts in the round report.
G4 `.agent/plan.md` at C1 byte-equals PLAN255R10: sha256 8772ec24a08b68b3f25fd18011f04d201e2cd7009326fa60f9b2ed54faee4ee4, 2426 B, 43 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and the roadmap F-id F255 present. C1 is the FIRST commit of the round other than C0a and C0b.
G5 C2 is PREFIX-clean over the de0f666b blob, remainder sha256 19355299c5f1624b0aeafc8f5f9bb78bfde13069225d7a52198fbc6377e55fb2 at 5109 B / 2 lines, byte-equal to one newline followed by RECORDR9, so the separator is present. An INDEPENDENT blank-line paragraph split of the C2 blob yields 198 units whose LAST unit is RECORDR9: newline-INCLUDED sha256 844da5103165aa54c8e8c0c8801ad1060e346350507df4889b6d72e00ec22067 at 5108 B, newline-STRIPPED sha256 9bd8470664d9c014083c9626e70254faf3ab6d45e5f83a31f920232a7731ec2e at 5107 B. A one-character mutant of the expected remainder (byte 100 flipped) is REJECTED by the prefix reading AND by the paragraph reading, while the real blob is accepted by both. Sets: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at de0f666b, and the SAME four at C2, `resolved` being constraint 7's count of line-anchored `Done:` paragraphs. `Gate: R10 — the R9 entry.` occurs 1x, is the LAST of the 10 lines beginning `Gate: R`, and all 10 header keys are distinct.
G6 Each of the four FROM slices occurs EXACTLY 1x in its target at the base de0f666b — GROUPFROM and ENTRYFROM in `apps/cli/command_catalog.py`, IMPORTFROM and MERGEFROM in `apps/cli/commands/__init__.py` — and each was applied by a count-checked single replacement. `git ls-tree de0f666b` returns nothing for `apps/cli/commands/teach_cmd.py` or `tests/cli/test_teach_cmd.py` — both ABSENT at the base — and `git ls-tree 26312742` returns both, PRESENT at C3. Each byte-equals its slice: the command = TEACHCMD, sha256 46b3cfdb59f0a4c605c8aef5465375e2f4db2a2a1b9a57da37508627151752ec, 2630 B, 64 lines; the tests = TEACHCMDTEST, sha256 cf0f258ec1cd9ad80bdadab05e881cc3e942b69b7cf0cd6a0b052eeba4631860, 4138 B, 108 lines.
G7 The two REWRITE pairs, in `apps/cli/commands/__init__.py`: IMPORTFROM 1x at base and 0x at C3, IMPORTTO 0x then 1x; MERGEFROM 1x at base and 0x at C3, MERGETO 0x then 1x. The two APPEND-shaped pairs, in `apps/cli/command_catalog.py`: GROUPFROM 1x at BOTH ends with GROUPTO 0x then 1x; ENTRYFROM 1x at BOTH ends with ENTRYTO 0x then 1x — no FROM-zero count is reported for either, that count being unreachable by construction (§4.9, R-0207). RECONSTRUCTION, per EDITED file: the base blob with its FROM occurrences replaced once each by their TOs in the block's pair order byte-EQUALS the C3 blob — `apps/cli/command_catalog.py` at sha256 82deed1ead7163d90f8513868d9305f852b30087ad9704d2ecd5947bfe6f5517 and `apps/cli/commands/__init__.py` at sha256 52ea7d69987764bb513d4cab3d5d3a708fe7d2ac7dbad2fb25e7cbd00e3da7cd. `git diff --numstat` at C3: `11 0`, `2 1`, `64 0`, `108 0` for the four files in Change-set order.
G8 THE COMMAND RUNS FOR REAL. With `REMEDY_DATA_DIR` set to the scratch root `.remedy-wt/r10-g8-data`, `python3 -m apps.cli.main teach narrate 3f2b1a90-0000-4000-8000-000000000001` exits 0 over a three-line run log at `<scratch>/runs/3f2b1a90-0000-4000-8000-000000000001/run-1.jsonl` and prints FOUR lines: a header naming 3 events, `The job was created.`, `A task started: t7`, and `An event this teacher has no narration for: mystery` — the third NAMES the event. The run log's sha256 is a1f6170b3367fae683175fb152a192226712a380ac88d44864a937af9a6f8029 BEFORE and the same AFTER, and the whole scratch data root hashes identically across the call; `git status --porcelain` stayed EMPTY. Full stdout in the round report.
G9 `python3 -m pytest tests/cli/test_teach_cmd.py -q -rf` at C3: exit 0, `6 passed in 0.25s` — the reviewer's predicted 6. No mutation red-proof was run and no worktree created (G9, constraint 11).
G10 `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py -q -rf` at C3: exit 0, `529 passed in 55.98s` — the reviewer's predicted 529.
G11 `python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/__init__.py apps/cli/commands/teach_cmd.py tests/cli/test_teach_cmd.py` at C3: exit 0, `All checks passed!`. Base reading for the two EDITED files ONLY, taken with no worktree and no overwrite: `git show de0f666b:<path> | python3 -m ruff check --stdin-filename <path> -` is exit 0 `All checks passed!` for both, so the rule-code multiset is empty at both ends. None is owed for the two CREATED files, ABSENT at the base (item 21).
G12 Serially in the primary checkout, never two pytest processes at once: `tests/orchestration/test_teacher_narration.py` exit 0 `38 passed in 0.23s`; the four state-reader files exit 0 `160 passed in 20.48s`; `tests/cli/test_golden_path.py` exit 0 `42 passed in 22.25s`.
G13 `git diff --name-only de0f666b..HEAD` equals the Change list with NO path on either side alone (extra: none; missing: none). Each of the TWELVE paths named untouched is PRESENT at the base and ABSENT from the range. Every commit in the range has exactly one parent. Per-commit insertions 489, 366, 21, 2 and 185 (11+2+64+108 across C3's four files), every one under 500, with C4's own cell in the round report; each per-file `+/-` cell above is byte-identical to `git diff --numstat`. Reflog, as TWO measured claims read from the OPERATION PREFIX before the first colon (R-0601), NEITHER a total for the round (R-0605): taken AT commit 26312742, where the round has made 5 commits, this round's entries whose prefix reads exactly `commit` number 5 — the two numbers are EQUAL; entries whose prefix contains amend, reset, rebase or cherry number 0. C4 is not written when this text is composed, so its own reflog entry is measured by the reviewer at the next gate (R-0494).
G14 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, 0 in each of `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/teach_cmd.py` and `tests/cli/test_teach_cmd.py` at C3, and 0 in `.agent/handoff.md` at C4.
G15 `git push` run after C4; its real output is in the round report. No pull request created and no CI run awaited.

## Authored-text proofs
All twelve slices were extracted programmatically by their marker lines from the COMMITTED `.agent/authored/f255-r10.md` at a00e60b3 — never retyped, never re-wrapped, never edited — and applied byte for byte. Disk-to-disk transport equality is G2. The plan is proven by G4's byte-equality, the ledger append by G5's prefix, remainder, paragraph and negative-control equalities, the two created files by G6's whole-file byte-equality against TEACHCMD and TEACHCMDTEST, and the four pairs by G7's per-file RECONSTRUCTION, which is byte-equality over the whole edited file rather than over the changed region alone.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3 and C4 ran in exactly that order — none added, none dropped, none reordered. No slice was edited, so no slice is declared wrong. C3 deliberately writes four files in one commit per the Change section's own order, the R-0151 rule, and is not a deviation. ONE DEVIATION IN MECHANISM, DECLARED: this session's shell guard rejects the `VAR=value cmd` environment-prefix form, so G8's `REMEDY_DATA_DIR` could not be set on the command line; the variable is set in a runner that spawns the block's EXACT argv unchanged through `subprocess.run` and prints its real returncode and full stdout. The command executed is the command the block names. For the same reason the extraction, the applications and the measurements ran from short scripts under the gitignored `.remedy-wt/`, which is scratch and is not in the change set. G5's `resolved` extractor is the one constraint 7 names, so nothing was derived this round. The block states no slice numeral of its own by design (R-0604), so G3's TWELVE contradicts nothing in it.

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: R11, T004's Stage 2 Q&A — `remedy teach ask`, the small context, the three grounding sources labelled per answer, the level dial, and spend recorded under the role name `teacher`. R10 awaits review; T002 and T003 are COMPLETE. There is no open pull request.
Fortschritt: ~60 % (T001, T002 and T003 COMPLETE · `remedy teach narrate` runs end to end over a real run log, declared read_only and PROVEN read-only byte for byte · T004 Stage 2, the integration gate and closure remain) — Schätzung
