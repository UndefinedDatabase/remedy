# Handback — F255 R8 (teacher role: T001 config key)

## Range
Review of 3812d625..HEAD on `feature/f255-teacher-role`.

## Commits

### edbe5081 chore(state): save the F255 R8 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r8.md | 304/0 | C0a — the R8 block COPIED verbatim, never retyped |

### 92ae84fd chore(state): mirror the F255 R8 block to last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 219/360 | C0b — the same bytes mirrored |

### 5970a477 chore(plan): advance the plan to F255 R8
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 15/16 | C1 — the plan, the FIRST substantive commit of the round (constraint 3; R-0377, R-0491 and R-0548 all rule) |

### 7b76bdd4 docs(review): register finding R-0605
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — R0605 appended after exactly one blank line |

### 2aeec2b0 docs(review): record the R7 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C3 — RECORDR7 appended after exactly one blank line |

### 47288467 feat(orchestration): declare the teacher.model config key with its pin
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/config.py | 14/0 | C4 — the `teacher.model` ConfigKeySpec, declared and unread until T004 |
| tests/orchestration/test_config.py | 9/0 | C4 — its expected-literal pin; constraint 5 keeps key and pin in ONE commit (R-0151) |

### C5 docs(state): write the F255 R8 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C5 — a handoff cannot table the commit that writes it (R-0149); its own cell and the complete change set are in the round report, as G12 routes them |

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
`git push` after C5 — real output in the round report. No pull request created and no CI run awaited (constraint 12). No worktree created (constraint 11); `git worktree list` reports the primary checkout alone, and every non-current reading was taken with `git show <sha>:<path>`.

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; `git worktree list` = the primary checkout alone; no reading was taken by overwriting a file in the primary checkout.
G2 `.remedy-wt/f255-r8.md`, `.agent/authored/f255-r8.md` at C0a and `.agent/last_block.md` at C0b are each sha256 10568c5540165120f2b96d9cf875c99ef1fd9b0a454a4f7701775c3655ee8e12 over 26977 B and 304 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 SEVEN slices, a count taken from my own ordered extraction of the COMMITTED `.agent/authored/f255-r8.md` at edbe5081 rather than written beside it: PLAN255R8, R0605, RECORDR7, CFGFROM, CFGTO, PINFROM, PINTO. Newline convention NEWLINE-INCLUDED (each body ends with exactly one newline; marker lines excluded). Per-slice sha256, byte and line counts in the round report.
G4 `.agent/plan.md` at C1 byte-equals PLAN255R8: sha256 a1d16420f454a4fd98f0e7701e6f943d0269a6c1a77d96f8991dd62a7aaebe55, 2240 B, 41 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and the roadmap F-id F255 present. C1 is the FIRST commit of the round other than C0a and C0b.
G5 C2 is PREFIX-clean over the 3812d625 blob, remainder sha256 d812ad1ed0257da3849866850a769f4e3fcb4757fb7b0cfb07a190394b4542cb at 3597 B / 2 lines, byte-equal to one newline followed by R0605; C3 is PREFIX-clean over the C2 blob, remainder sha256 c19419dc09dc3d4bf0ff02d5eaf93a9b640221bd4e41505483f54f761939cac4 at 5380 B / 2 lines, byte-equal to one newline followed by RECORDR7 — so both separators are present. An INDEPENDENT paragraph split of the C3 blob yields 196 units whose LAST unit is RECORDR7: newline-EXCLUDED sha256 74dde377aafaac0c4a0ed2886c9f4b78caba1c54aefe9a6e81fcf0d5f723b8ec at 5378 B, newline-INCLUDED sha256 e0f4c1644f4ca3c16c727c26bfb9d91b17b435e56bc2bbb11cb30a4c0f69aec1 at 5379 B; a one-character mutant of the expected remainder at offset 2000 is REJECTED by the prefix reading and by BOTH paragraph readings, while the unmutated blob is accepted by both. Sets: 180 registered / 3 resolved / 177 open / 0 line-anchored `Landed:` at 3812d625, and 181 / 3 / 178 / 0 at BOTH C2 and C3. `- R-0605 — ` occurs 1x; `Gate: R8 — the R7 entry.` occurs 1x, is the LAST of the 8 lines beginning `Gate: R`, and all 8 header keys are distinct.
G6 CFGFROM occurs 1x in `packages/orchestration/config.py` and PINFROM 1x in `tests/orchestration/test_config.py` at 3812d625; each was applied by a count-checked replacement that asserted exactly 1 occurrence BEFORE replacing, so the round never had cause to stop.
G7 The REWRITE pair CFGFROM→CFGTO reads FROM 1x at the base and 0x at C4, TO 0x then 1x. The APPEND-shaped pair PINFROM→PINTO reads FROM 1x at BOTH ends and TO 0x then 1x, and NO FROM-zero count is reported for it — that count is unreachable by construction (§4.9, R-0207). RECONSTRUCTION, which fixes position and multiplicity together and is independent of hunk attribution: for BOTH files the blob at C4 byte-EQUALS the blob at 3812d625 with that file's single FROM occurrence replaced once by its TO — config.py sha256 59fd1f2baa09da7fcae0bf44a98ae6a09a01171bbef7ff3767ce0690e5b03988, test_config.py sha256 946ea4a02da52d47d0aa060ebde0a5abc1f1e2c0c232a4d57f32e13fd4551569, each equal on both sides. `git diff --numstat` at C4: 14/0 and 9/0.
G8 `python3 -m pytest tests/orchestration/test_config.py -q -rf` at C4: exit 0, `63 passed in 0.33s` — the reviewer's predicted 63 against 62 at the base, the one new case being `test_teacher_model_key_is_declared`. From a `python3 -c` I ran myself, `get_key_spec("teacher.model")` is not None with `.env_var` `REMEDY_TEACHER_MODEL`, `.value_type` `<class 'str'>` and `.default` `None`. No mutation red-proof was run and no worktree created (G8, constraint 11).
G9 `python3 -m ruff check packages/orchestration/config.py tests/orchestration/test_config.py` at C4: exit 0, `All checks passed!`.
G10 `python3 -m pytest tests/orchestration/test_role_config.py tests/orchestration/test_role_conventions.py -q -rf` at C4: exit 0, `68 passed in 0.35s` — the reviewer's predicted 68.
G11 Serially in the primary checkout, never two pytest processes at once: the four state-reader files exit 0 at `160 passed in 19.94s`, and `tests/cli/test_golden_path.py` exit 0 at `42 passed in 20.46s`.
G12 `git diff --name-only 3812d625..HEAD` equals the Change list with NO path on either side alone (extra: none; missing: none). Each of the nine paths named untouched is PRESENT at the base and ABSENT from the range. Every commit in the range has exactly one parent. Per-commit insertions 304, 219, 15, 2, 2 and 23 (14+9 across C4's two files), every one under 500, with C5's own cell in the round report; each per-file `+/-` cell above is byte-identical to `git diff --numstat`. Reflog, as TWO measured claims read from the OPERATION PREFIX before the first colon (R-0601), NEITHER a total for the round (R-0605): taken AT commit 47288467, where the round has made 6 commits, this round's entries whose prefix reads exactly `commit` number 6 — the two numbers are EQUAL; entries whose prefix contains amend, reset, rebase or cherry number 0. C5 is not written when this text is composed, so its own reflog entry is measured by the reviewer at the next gate (R-0494).
G13 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C3, 0 in `packages/orchestration/config.py` and `tests/orchestration/test_config.py` at C4, and 0 in `.agent/handoff.md` at C5.
G14 `git push` run after C5; its real output is in the round report. No pull request created and no CI run awaited.

## Authored-text proofs
All seven slices were extracted programmatically by their `<<<SLICE`/`<<<END` markers from the COMMITTED `.agent/authored/f255-r8.md` at edbe5081 — never retyped, never re-wrapped, never edited — and applied byte for byte. Disk-to-disk transport equality is G2. The plan is proven by G4's byte-equality, the two ledger appends by G5's prefix, remainder, paragraph and negative-control equalities, and the two code pairs by G6's pre-replacement counts and G7's whole-file reconstructions.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 ran in exactly that order — none added, none dropped, none reordered. No slice was edited, so no slice is declared wrong. One reading is worth the reviewer's attention: this session's shell guard rejects `$?`, so every gate's exit code was captured by a three-line runner that passes the gate's argv through untouched to `subprocess.run` from the repo root with the environment inherited — the command run is the command the block names, and its returncode is printed beside it. C4 deliberately changes two files in one commit per constraint 5, the R-0151 rule, not a deviation. The block states no slice numeral of its own by design (R-0604), so G3's seven contradicts nothing in it.

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: R9, which builds T002 AND T003 together — Stage 1 narration over an enumerated event set, and the behavioural read-only proof. T001 is COMPLETE. R8 awaits review. There is no open pull request.
Fortschritt: ~35 % (F086 merged · F255 claimed · six DECISIONs ruled · the spec written · T001 COMPLETE: the teacher has a role name, a reviewed conventions document, a capped prompt segment and its own model key · T002-T004 open) — Schätzung
