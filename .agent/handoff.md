# Handback — F085 Sandbox hardening (stage 1), R33

Branch: feature/f085-sandbox-hardening · base SHA c2033d6c. No production code
changed: checklist narrowing, record, state only. Open findings: 118.

Fortschritt: ~70 % (T001 gebaut · R13-R32 PASS · T002a KOMPLETT · T002b 9 von 12
Sites auf dem Seam, 3 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

## Range

Review of c2033d6c..HEAD.

## Commits

### d2e0c5ae docs(f085): save the R33 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r33.md | +305/-0 | C0a: block saved byte-for-byte |

### f2f0338b docs(f085): mirror the R33 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +223/-318 | C0b: identical bytes mirrored |

### 74dfa30e docs(review): narrow the slice-fact checklist item to an absolute commit id
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +9/-1 | C1: SHARPF→SHARPT narrows item 20 in place |

### c933b949 docs(review): record the R32 PASS and register and resolve R-0521
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +79/-0 | C2: RECORD1 appended, nothing else |

### e917ac90 docs(f085): advance the plan to R33
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13/-12 | C3: PLANF→PLANT, file stays 47 lines |

### (this commit) docs(f085): rewrite the handback for R33
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4: a handoff cannot table itself (R-0149); own insertions in the round report |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C4 — outcome in the round
report. No PR, no merge, no gh command, no worktree added or removed.

## Verification

G1 STATE — pass. `.agent/STOP` absent, read from disk before C0a and again before C4.
`git status --porcelain` empty at round start and after each of C0a-C3.
`git worktree list` = 1 line throughout.

G2 TRANSPORT — pass. Committed `.agent/authored/f085-r33.md`, committed
`.agent/last_block.md`, both working copies AND the reviewer's scratch original are
all five byte-EQUAL: sha256
a089cc6604b57cfd9c7ee5449742a4651c10c9d7db80af0f8da735bd5b566404, 19296 B,
305 lines, 10 marker lines, regions 2c1d1941 / 84609b00 / f6c3a188 — all measured.

G3 APPEND SHAPE — pass. Pre-commit blob 367484 B is a byte-exact PREFIX of the
373548 B post-commit file; remainder 6064 B = one blank line + RECORD1's 6063 B;
the slice is an exact suffix; RECORD1's first line occurs once among the lines
c933b949 adds; 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the `BEGIN` SUBSTRING
occurs 7× — which is why LINES were counted.
`git show --numstat c933b949 -- .agent/live_review.md` = `79  0`.

G4 ARITHMETIC — pass. Base c2033d6c: 135 registered / 17 done / 0 landed, 118 open,
both maxima R-0520 — reproduces the reviewer's base exactly. HEAD: 136 / 18 / 0,
118 open again, both maxima R-0521. Registered symmetric difference {R-0521}, done
symmetric difference {R-0521}, landed symmetric difference empty, 0 duplicate ids,
0 resolutions naming an unregistered id, maximum id R-0521, next free R-0522.

G5 NARROWING — pass, measured at HEAD after C1. In
`docs/agents/planner_reviewer_prompt.md` the new `identifier that already EXISTS…`
line, the `Why this is on disk and not a habit…` closer and the item-20 opener each
occur exactly once — the pair narrowed item 20 rather than adding an item. 0 marker
lines reached the file. `git show --numstat 74dfa30e` = `9  1`.

G6 SUITES — pass, run in the PRIMARY checkout, never in a worktree (R-0518).
- 4 state readers, `-rf -q`: exit 0, `159 passed in 19.83s` (base 159 passed).
- `python3 -m pytest tests/docs/ -q`: exit 0, `295 passed in 0.43s` (base 295).
- CANARY `tests/cli/test_golden_path.py -q`: exit 0, `42 passed in 20.19s` (base 42).
No ruff run and no red proof were ordered: this round changed no production code.

G7 HYGIENE — pass, measured BEFORE C4. `git diff --name-only c2033d6c..HEAD` holds
exactly the 5 declared paths (change set minus `.agent/handoff.md`), nothing else.
Per-commit insertions 305, 223, 9, 79, 13 — none exceeds 500. All 5 commits have
exactly one parent; `git reflog -10` holds only `commit:` entries.

STALENESS (constraint 8), re-read after C3: `.agent/authored/f085-r33.md`,
`.agent/last_block.md`, `docs/agents/planner_reviewer_prompt.md`,
`.agent/live_review.md`, `.agent/plan.md`. Each commit touches exactly one path and
no commit AFTER C2 touches a file RECORD1 asserts about; C1 precedes C2 as constraint
9 requires, so RECORD1's claim about the sharpened item 20 was true when written. All
four `HEAD` occurrences in RECORD1 QUOTE or name the defect R-0521 registers, none
asserts a reading of its own, so they were applied verbatim and NOT repaired; every
commit id it asserts (16234fbf, 94e70839, c2033d6c, ce69c39a, ed88be4c) resolves.

## Authored-text proofs

SHARPF→SHARPT and PLANF→PLANT: both REWRITE; each FROM matched exactly once before
apply and 0 times after, each TO once after. RECORD1: APPEND, proved by the prefix
and exact-suffix byte equalities under G3. All three were extracted PROGRAMMATICALLY
from the COMMITTED `.agent/authored/f085-r33.md` by marker pair, none retyped, and
0 marker lines reached any target file.

## Deviations & assumptions

No deviation from the block: C0a, C0b, C1, C2, C3, C4 ran in exactly that order, one
commit each — nothing added, dropped, merged or reordered.
Deviations, declared: this handback is 136 lines against the 100-line cap (>5-commit
case). Cause is mandated content, not prose: six per-commit changed-files tables, the
six-row item-status table, the verbatim Fortschritt block and seven gate transcripts
G1-G7 plus the constraint-8 staleness reading. No section was dropped to fit.

## Next

The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk —
BEFORE rule 2, the Open PR Gate
(`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
R33's own verdict is NOT a §4.13 terminator, because this branch continues. The next
reviewed round records R33's gate entry in `.agent/live_review.md`. The next
MIGRATION round takes `mission_state.py`'s spawn, because `builder_bridge.py` cannot
move until the seam can SET an environment value rather than only allowlist a key.
