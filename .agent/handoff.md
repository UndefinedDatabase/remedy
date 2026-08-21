# Handback — F255 R11 (teacher role: Stage 2's deterministic half, T004)

## Range
Review of c6c6fb08..HEAD on `feature/f255-teacher-role`.

## Commits

### 153b78fd chore(state): save the F255 R11 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r11.md | 490/0 | C0a — the R11 block COPIED verbatim, never retyped |

### b9b1ce9d chore(state): mirror the F255 R11 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 366/365 | C0b — the same bytes mirrored |

### 948f57de chore(plan): advance the plan to F255 R11
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 15/16 | C1 — the plan, the FIRST substantive commit of the round (constraint 3; R-0377, R-0491 and R-0548 all rule) |

### 8271d828 docs(review): record the R10 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORDR10 appended after exactly one blank line |

### 18083ea7 feat(orchestration): add teacher Q&A grounding for Stage 2
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/teacher_qa.py | 151/0 | C3 — the pure module: three labelled grounding sources, the level dial, the small-context assembly, the honest no-model refusal |
| tests/orchestration/test_teacher_qa.py | 113/0 | C3 — the tests that make those honesty rules falsifiable; the Change set keeps both files in ONE commit (R-0151) |

### C4 docs(state): write the F255 R11 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C4 — a handoff cannot table the commit that writes it (R-0149); its own cell and the complete change set are in the round report, as G11 routes them |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions
`git push` after C4 — real output in the round report. No pull request created and no CI run awaited (constraint 11). No worktree created (constraint 10); `git worktree list` reports the primary checkout alone, and every non-current reading was taken with `git show <sha>:<path>`.

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; `git worktree list` = the primary checkout alone; no reading was taken by overwriting a file in the primary checkout.
G2 `.remedy-wt/f255-r11.md`, `.agent/authored/f255-r11.md` at C0a and `.agent/last_block.md` at C0b are each sha256 d4e511dd4060b29e26f1331ee6eeb0c888abec01e04fe7f3681aea4fae07f5de over 31058 B and 490 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 FOUR slices, a count taken from my own ordered extraction of the COMMITTED `.agent/authored/f255-r11.md` at 153b78fd rather than written beside it: PLAN255R11, RECORDR10, TEACHQA, TEACHQATEST. Newline convention NEWLINE-INCLUDED — a body is the lines strictly between its markers, each keeping its own LF; marker lines are excluded (R-0600). Per-slice sha256, byte and line counts in the round report.
G4 `.agent/plan.md` at C1 byte-equals PLAN255R11: sha256 a8d22168cfc33e52a9f488082670cb24348bb203802b2aaef1fa84313057fda5, 2350 B, 42 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and the roadmap F-id F255 present. C1 is the FIRST commit of the round other than C0a and C0b.
G5 C2 is PREFIX-clean over the c6c6fb08 blob, remainder sha256 f92e0f4ddae2be63076fd072fe4d6e49bcd1441714b3f6462ecedc0e5feea23a at 5659 B / 2 lines, byte-equal to one newline followed by RECORDR10, so the separator is present and is exactly one blank line. An INDEPENDENT blank-line paragraph split of the C2 blob yields 199 units whose LAST unit is RECORDR10: newline-INCLUDED sha256 98999ada6035883610f0e52c99835ce7c0446602b5f95b7248d0049b9c8a3d73 at 5658 B, newline-EXCLUDED sha256 cf9e5c517b2643978a81b74e3fd3324ee82266c2c87fffc307f4f46ac60cfcf7 at 5657 B. A one-character mutant of the expected remainder (byte 2829, `6` flipped to `X`) is REJECTED by the prefix reading AND by the paragraph reading, while the real blob is accepted by both. Sets: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at c6c6fb08, and the SAME four at C2, the registered count being lines matching `^- R-\d+ — ` and the resolved count lines matching `^Done: R-\d+ — `. `Gate: R11 — the R10 entry.` occurs 1x, is the LAST of the 11 lines beginning `Gate: R`, and all 11 header keys are distinct.
G6 `git ls-tree c6c6fb08` returns nothing for `packages/orchestration/teacher_qa.py` or `tests/orchestration/test_teacher_qa.py` — both ABSENT at the base — and `git ls-tree 18083ea7` returns both, PRESENT at C3. Each byte-equals its slice: the module = TEACHQA, sha256 abe69cac625362f6067a2e491ced9b6a613cab7c293d2ce0831e905adc126d09, 5969 B, 151 lines; the tests = TEACHQATEST, sha256 208a9417619372ca27d1d07fa1aa0b034c99eb3ad87a15809f06f6c34c00f063, 4567 B, 113 lines. `git diff --numstat` at C3: `151 0` and `113 0`. This round contains NO FROM/TO pair, so no containment reading and no FROM-zero count is owed (§4.9, R-0207).
G7 `python3 -m pytest tests/orchestration/test_teacher_qa.py -q -rf` at C3: exit 0, `19 passed in 0.26s` — the 19 the reviewer measured. I ran NO mutation red-proof and created no worktree, as G7 and constraint 10 order; the five red-proof results quoted in the block are the reviewer's own measurements, not mine.
G8 `python3 -m pytest tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_autonomy.py -q -rf` at C3: exit 0, `132 passed in 3.29s` — the same 132 the reviewer measured at c6c6fb08, so the new file under `packages/` trips no glob sweep.
G9 `python3 -m ruff check packages/orchestration/teacher_qa.py tests/orchestration/test_teacher_qa.py` at C3: exit 0, `All checks passed!`. No base rule-code multiset is owed: both files are ABSENT at c6c6fb08 (item 21).
G10 Serially in the primary checkout, never two pytest processes at once: `tests/orchestration/test_teacher_narration.py` exit 0 `38 passed in 0.28s`; the four state-reader files exit 0 `160 passed in 20.44s`; `tests/cli/test_golden_path.py` exit 0 `42 passed in 20.50s`.
G11 `git diff --name-only c6c6fb08..HEAD` equals the Change list with NO path on either side alone (extra: none; missing: none). Each of the SIX paths named untouched is PRESENT at the base and ABSENT from the range. Every commit in the range has exactly one parent. Per-commit insertions 490, 366, 15, 2 and 264 (151+113 across C3's two files), every one under 500, with C4's own cell in the round report; each per-file `+/-` cell above is byte-identical to `git diff --numstat`. Reflog, as TWO measured claims read from the OPERATION PREFIX before the first colon (R-0601), NEITHER a total for the round (R-0605): taken AT commit 18083ea7, where the round has made 5 commits, this round's entries whose prefix reads exactly `commit` number 5 — the two numbers are EQUAL; entries whose prefix contains amend, reset, rebase or cherry number 0. C4 is not written when this text is composed, so its own reflog entry is measured by the reviewer at the next gate (R-0494).
G12 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, 0 in each of `packages/orchestration/teacher_qa.py` and `tests/orchestration/test_teacher_qa.py` at C3, and 0 in `.agent/handoff.md` at C4.
G13 `git push` run after C4; its real output is in the round report. No pull request created and no CI run awaited.

## Authored-text proofs
All four slices were extracted programmatically by their marker lines from the COMMITTED `.agent/authored/f255-r11.md` at 153b78fd — never retyped, never re-wrapped, never edited — and applied byte for byte. Disk-to-disk transport equality is G2. The plan is proven by G4's byte-equality, the ledger append by G5's prefix, remainder, paragraph and negative-control equalities, and the two created files by G6's whole-file byte-equality against TEACHQA and TEACHQATEST.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3 and C4 ran in exactly that order — none added, none dropped, none reordered. No slice was edited, so no slice is declared wrong. C3 deliberately writes two files in one commit per the Change section's own order, the R-0151 rule, and is not a deviation. ONE DEVIATION IN MECHANISM, DECLARED: this session's shell guard rejects the `VAR=value cmd` environment-prefix form, shell loops, `$( )` substitution and `${arr[0]}` indexing, so every extraction, application, gate run and measurement was routed through short Python scripts under the gitignored `.remedy-wt/`, which is scratch and is not in the change set; each gate's command was spawned as the block's EXACT argv through `subprocess.run`, and the real returncode and output are in the round report. No environment variable was needed this round. G3's FOUR contradicts nothing in the block, which states no slice numeral of its own by design (R-0604).

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: R12, which FINISHES T004 — `remedy teach ask` on the CLI, the teacher model call through the role's own config, the honest refusal when no model is configured, and spend recorded under the role name `teacher`. R11 awaits review; T004's DETERMINISTIC half is complete and its MODEL half is not. There is no open pull request.
Fortschritt: ~70 % (T001, T002 and T003 COMPLETE · T004 half done — the grounding sources, the level dial and the small context are built and red-proofed, zero tokens · the teacher model call, the integration gate and closure remain) — Schätzung
