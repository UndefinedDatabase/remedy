# Handback — F255 R6 (teacher role: T001 first half)

## Range
Review of 9d28d93c..HEAD on `feature/f255-teacher-role`.

## Commits

### e6aa3338 docs(state): save the F255 R6 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r6.md | 284/0 | C0a — the R6 block saved verbatim |

### b83a71a4 docs(state): mirror the F255 R6 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 209/212 | C0b — the same bytes mirrored |

### 033605c8 docs(review): register finding R-0604
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C1 — R0604 appended after one blank line |

### f3ae2244 docs(review): record the R5 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORDR5 appended after one blank line |

### c4866547 feat(orchestration): add the teacher role to KNOWN_ROLES with its pin
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/role_config.py | 5/0 | C3 — `teacher` in the tuple, with its WHY comment |
| tests/orchestration/test_role_config.py | 4/1 | C3 — the pin renamed to eight and extended |

### 94e9c4c2 chore(plan): advance the plan to F255 R6
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 15/15 | C4 — the plan advanced to R6 |

### C5 docs(state): write the F255 R6 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C5 — a handoff cannot table the commit that writes it (R-0149); its own cell and the complete change set are in the round report, as G11 routes them |

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
`git push` after C5 — real output in the round report. No pull request created and
no CI run awaited (constraint 11). No worktree created (constraint 10); `git worktree
list` reports the primary checkout alone.

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; worktree list = primary alone; every reading taken via `git show <sha>:<path>`.
G2 `.remedy-wt/f255-r6.md`, `.agent/authored/f255-r6.md` at C0a and `.agent/last_block.md` at C0b are all sha256 e12761e56c23f6249bd50defe6d91b69cbd3e01f013195604664c16d3cbe024e over 23360 B and 284 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 ELEVEN slices, a count taken from my own ordered listing rather than written beside it: ROLEDOCFROM, ROLEDOCTO, ROLETUPFROM, ROLETUPTO, PINNAMEFROM, PINNAMETO, PINTUPFROM, PINTUPTO, R0604, RECORDR5, PLAN255R6. Newline convention NEWLINE-INCLUDED. Per-slice sha256/bytes/lines in the round report.
G4 C1 and C2 are both PREFIX-clean with exactly one blank-line separator; remainders 1872 B / 2 lines and 4990 B / 2 lines, each byte-equal to newline + its slice. The independent paragraph split of the C2 blob yields 193 units and its LAST unit IS RECORDR5 under BOTH conventions — 087bd125…0cd at 4989 B newline-included, 646cbe2a…537 at 4988 B newline-excluded — and a one-byte mutant at offset 2495 is REJECTED by both readings. Sets: 179/3/176/0 at 9d28d93c, 180/3/177/0 at C1 and 180/3/177/0 at C2. `- R-0604 — ` 1x; `Gate: R6 — the R5 entry.` 1x, the LAST line beginning `Gate: R`, and all six header keys distinct.
G5 Each of the four FROM texts occurs exactly 1x in its target at the base, and each was applied by a count-checked replacement that asserts 1 before replacing.
G6 The three REWRITE pairs each read FROM 1x at base and 0x at C3 — the FROM-zero count — with TO 0x then 1x. The APPEND-shaped ROLEDOCFROM→ROLEDOCTO reads FROM 1x at BOTH ends and TO 0x then 1x, each of its 4 TO-ONLY lines occurs exactly 1x among the 9 lines C3's diff ADDS, and NO FROM-zero count is reported for it because that count is unreachable by construction. C3 numstat: 5/0 and 4/1.
G7 `python3 -m pytest tests/orchestration/test_role_config.py -q -rf` exit 0 at `32 passed` at the base and exit 0 at `33 passed` at C3 — the parametrize over KNOWN_ROLES gains the teacher case. `len(KNOWN_ROLES)` is 8 and `resolve_role_config("teacher")` returns `.role == "teacher"` without raising under `warnings.simplefilter("error")`. No mutation red-proof was run and no worktree created.
G8 `python3 -m ruff check packages/orchestration/role_config.py tests/orchestration/test_role_config.py` exit 0 `All checks passed!` at the base AND at C3, so no pre-existing finding is read as a new one.
G9 `.agent/plan.md` at C4 byte-equals PLAN255R6: sha256 3ca563eadb06bd687be0c6b36a624275b08b5fa60290fe38044639a0f0ae2f55, 2395 B, 42 lines — under 50 — with `## Goal` 1x, `## Next Steps` 1x and the F-id F255 present.
G10 Serially, in the primary checkout: the four state-reader files exit 0 at `160 passed`, and `tests/cli/test_golden_path.py` exit 0 at `42 passed`. Never two pytest processes at once.
G11 `git diff --name-only 9d28d93c..HEAD` equals the Change list with no path on either side alone; each of the eight paths named untouched is PRESENT at the base and ABSENT from the range; every commit in the range has one parent; per-commit insertion totals 284, 209, 2, 2, 9 (5+4 across C3's two files), 15 and C5's own, every one under 500, with the per-file `+/-` cells byte-identical to the tables above. Reflog, as two measured claims read from the operation prefix before the first colon: entries producing a commit and reading `commit` equal the number of commits this round makes; entries whose PREFIX contains amend, reset, rebase or cherry: 0. The retired whole-line reading also returns 0 this round, so it did NOT discriminate — reported as measured, not as a control passing.
G12 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/live_review.md` at C2, 0 in `packages/orchestration/role_config.py` and 0 in `tests/orchestration/test_role_config.py` at C3, 0 in `.agent/plan.md` at C4, 0 in `.agent/handoff.md` at C5.
G13 `git push` run after C5; its real output is in the round report.

## Authored-text proofs
All eleven slices were extracted programmatically, by their markers, from the COMMITTED `.agent/authored/f255-r6.md` at e6aa3338 — never retyped, never rewrapped — and applied byte for byte. Disk-to-disk transport equality is the G2 result above; the four pair applications are proven by G5 and G6, the two ledger appends by G4's prefix and remainder equalities, and the plan by G9's byte-equality.

## Deviations & assumptions
None from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 were executed in that order, none added, none dropped, none reordered. No slice was edited. C3 deliberately changes two files in one commit per constraint 5, which is the R-0151 rule and not a deviation. The block states no slice numeral of its own by design (R-0604), so the eleven in G3 contradicts nothing.

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: R7, T001's second half — `ConventionsRole`, the conventions document and the `teacher.model` config key, in that order. R6 awaits review. There is no open pull request.
Fortschritt: ~20 % (F086 merged · F255 claimed · ground measured · six DECISIONs ruled · the spec written · T001 first half BUILT: the teacher role name resolves) — Schätzung
