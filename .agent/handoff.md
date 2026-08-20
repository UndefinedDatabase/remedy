# Handback — F255 R7 (teacher role: T001 conventions half)

## Range
Review of eb8aa9ae..HEAD on `feature/f255-teacher-role`.

## Commits

### db54b5f2 chore(state): save the F255 R7 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r7.md | 445/0 | C0a — the R7 block COPIED verbatim, never retyped |

### b208d57d chore(state): mirror the F255 R7 block to last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 361/200 | C0b — the same bytes mirrored |

### cd2bc66c chore(plan): advance the plan to F255 R7
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 14/14 | C1 — the plan, the FIRST substantive commit of the round (constraint 3; the counter-measure R-0377, R-0491 and R-0548 all rule) |

### 5f0ae785 docs(review): record the R6 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORDR6 appended after exactly one blank line |

### 349a458c feat(orchestration): add the teacher conventions role, document and pins
| Path | +/- | Reason |
|---|---|---|
| docs/agents/teacher_conventions.md | 46/0 | C3 — CREATED, holding exactly TEACHERDOC |
| packages/orchestration/role_conventions.py | 5/2 | C3 — the TEACHER member, its document path and its segment name |
| tests/orchestration/test_role_conventions.py | 7/1 | C3 — helper docstring, the two literal pins, the rule anchors |

### 3bffaaab docs(index): register the teacher conventions document
| Path | +/- | Reason |
|---|---|---|
| docs/README.md | 5/4 | C4 — the quick-find row and the Agent Conventions table row |

### C5 docs(state): write the F255 R7 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C5 — a handoff cannot table the commit that writes it (R-0149); its own cell and the complete change set are in the round report, as G13 routes them |

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
`git push` after C5 — real output in the round report. No pull request created and no CI run awaited (constraint 13). No worktree created (constraint 12); `git worktree list` reports the primary checkout alone, and every non-current reading was taken with `git show <sha>:<path>`.

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; `git worktree list` = the primary checkout alone.
G2 `.remedy-wt/f255-r7.md`, `.agent/authored/f255-r7.md` at C0a and `.agent/last_block.md` at C0b are each sha256 326180ada7d1cb7e65e5c19fc845ef7f77b8a37135dfdb1eb88265ca42414b6c over 29581 B and 445 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 TWENTY-THREE slices, a count taken from my own ordered extraction of the COMMITTED `.agent/authored/f255-r7.md` at db54b5f2 rather than written beside it: PLAN255R7, RECORDR6, MODDOCFROM/TO, ENUMFROM/TO, PATHFROM/TO, NAMEFROM/TO, HELPFROM/TO, SEGPINFROM/TO, PATHPINFROM/TO, ANCHORFROM/TO, IDXQUICKFROM/TO, IDXTABLEFROM/TO, TEACHERDOC. Newline convention NEWLINE-INCLUDED (each slice ends with exactly one newline; marker lines excluded). Per-slice sha256, byte and line counts in the round report.
G4 `.agent/plan.md` at C1 byte-equals PLAN255R7: sha256 6a5548d7a831748738fb707abe5396f856795cda9772dd5a95c35668faf42c8a, 2353 B, 42 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and the roadmap F-id F255 present. C1 is the FIRST commit of the round other than C0a and C0b.
G5 C2 is PREFIX-clean: the eb8aa9ae blob is a byte-exact prefix of the C2 blob, remainder sha256 0904c208b35dcccdfd3e6f243e8c3bd1528b1906d69676b2a039047fd603057a at 5720 B / 2 lines, byte-equal to one newline followed by RECORDR6, so the single blank-line separator is present. An INDEPENDENT paragraph split of the C2 blob yields 194 units whose LAST unit is RECORDR6 — newline-excluded sha256 ddd71954b95d37fb76c37440143911c1c2bc4ea76a26f081eabdf956df9bdb6d at 5719 B, newline-included 62b9c57317434f72cccedbf63d86f267bcf26fe4c3db7e48b075e4be8f11dbb2 at 5720 B — and a one-byte mutant of the expected remainder at offset 2859 is REJECTED by BOTH readings and by the prefix reading. Sets: 180 registered / 3 resolved / 177 open / 0 line-anchored `Landed:` at eb8aa9ae AND the same four at C2. `Gate: R7 — the R6 entry.` occurs 1x, is the LAST of the 7 lines beginning `Gate: R`, and all 7 header keys are distinct.
G6 Each of the ten FROM texts occurs exactly 1x in its target file at eb8aa9ae, and each was applied by a count-checked replacement asserting 1 occurrence BEFORE replacing; none was 0 or 2, so the round did not stop.
G7 The nine REWRITE pairs each read FROM 1x at the base and 0x after their commit, with TO 0x then 1x: MODDOC, PATH, NAME, HELP, SEGPIN, PATHPIN and ANCHOR at C3, IDXQUICK and IDXTABLE at C4. The APPEND-shaped ENUMFROM→ENUMTO reads FROM 1x at BOTH ends with TO 0x then 1x, its single TO-ONLY line `    TEACHER = "teacher"` occurs exactly 1x among the lines C3's diff ADDS, and NO FROM-zero count is reported for it because that count is unreachable by construction (§4.9, R-0207). Numstat at C3: 46/0, 5/2, 7/1. At C4: 5/4.
G8 `docs/agents/teacher_conventions.md` is ABSENT at eb8aa9ae (`git ls-tree` empty) and PRESENT at C3, byte-equal to TEACHERDOC at sha256 f172231301d701fb7865bb320244668fa35c411a2d11fadf823beffee181e682 — 1982 bytes, 1972 characters, 46 lines. From a `python3 -c` I ran myself: `estimate_text_tokens(role_conventions_text(ConventionsRole.TEACHER))` is 493 against `CONVENTIONS_TOKEN_CAP` 800 — at or under the cap, matching the reviewer's measurement exactly.
G9 `python3 -m pytest tests/orchestration/test_role_conventions.py -q -rf` at C3: exit 0, `35 passed in 0.24s` — the reviewer's predicted 35. No mutation red-proof was run and no worktree created.
G10 `python3 -m ruff check packages/orchestration/role_conventions.py tests/orchestration/test_role_conventions.py` at C3: exit 0, `All checks passed!`. The SAME two paths at the base read `All checks passed!` too, measured by piping each base blob through `ruff check --stdin-filename <real path> -` so the per-file-ignores of the real path still applied — worktrees being forbidden by constraint 12 — with a red control proving that probe evaluates (a two-unused-import stdin returns exit 1 and 2x F401).
G11 `python3 -m pytest tests/docs/ -q -rf` at C4: exit 0, `295 passed in 0.51s`. A REGRESSION CHECK ONLY: that suite reads feature filenames and the primary docs' own claims and is blind to the body of anything under `docs/agents/`, so the proof for C3's document is G8 and G9.
G12 Serially in the primary checkout, never two pytest processes at once: the four state-reader files exit 0 at `160 passed in 21.11s`, and `tests/cli/test_golden_path.py` exit 0 at `42 passed in 22.56s`.
G13 `git diff --name-only eb8aa9ae..HEAD` equals the Change list with NO path on either side alone (extra: none; missing: none). Each of the ten paths named untouched is PRESENT at the base and ABSENT from the range. Every commit in the range has exactly one parent. Per-commit insertions 445, 361, 14, 2, 58 (46+5+7 across C3's three files) and 5, every one under 500, with C5's own cell in the round report; each per-file `+/-` cell above is byte-identical to `git diff --numstat`. Reflog, as TWO measured claims read from the operation prefix before the first colon (R-0601): entries of this round reading exactly `commit` = 6, equal to the 6 commits the round makes; entries whose PREFIX contains amend, reset, rebase or cherry = 0.
G14 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, 0 in `packages/orchestration/role_conventions.py`, `docs/agents/teacher_conventions.md` and `tests/orchestration/test_role_conventions.py` at C3, 0 in `docs/README.md` at C4, 0 in `.agent/handoff.md` at C5.
G15 `git push` run after C5; its real output is in the round report. No pull request created, no CI run awaited.

## Authored-text proofs
All twenty-three slices were extracted programmatically by their `<<<SLICE`/`<<<END` markers from the COMMITTED `.agent/authored/f255-r7.md` at db54b5f2 — never retyped, never re-wrapped, never edited — and applied byte for byte. Disk-to-disk transport equality is G2. The ten pair applications are proven by G6 and G7, the ledger append by G5's prefix, remainder and paragraph equalities, the plan by G4's byte-equality and the created document by G8's byte-equality.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 ran in exactly that order — none added, none dropped, none reordered. No slice was edited, so no slice is declared wrong. Two readings are worth the reviewer's attention. (1) The base half of G10 could not be taken in a worktree, constraint 12 forbidding one, so it was taken through `ruff check --stdin-filename` at the real repo-relative path, which preserves the `tests/**` per-file-ignore; the red control is reported with it rather than the probe being assumed to run. (2) C3 deliberately changes three files in one commit per constraint 5 — the R-0151 rule, not a deviation. The block states no slice numeral of its own by design (R-0604), so G3's twenty-three contradicts nothing in it.

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: R8, the `teacher.model` config key modelled on the existing `orchestrator.model` spec, with its pin in the SAME commit. R7 awaits review. There is no open pull request.
Fortschritt: ~28 % (F086 merged · F255 claimed · six DECISIONs ruled · the spec written · T001's vocabulary half BUILT at R6 · T001's conventions half BUILT here: the teacher has a role name, a reviewed conventions document and a capped prompt segment) — Schätzung
