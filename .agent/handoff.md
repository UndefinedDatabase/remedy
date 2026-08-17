# Handback — F085 Sandbox hardening (stage 1), R34

Branch: feature/f085-sandbox-hardening · base SHA 7480d880. No production code
changed: checklist narrowing, record, state only. Open findings: 118.

Fortschritt: ~70 % (T001 gebaut · R13-R32 PASS · R33 FAIL, hier repariert · T002a
KOMPLETT · T002b 9 von 12 Sites auf dem Seam, 3 offen · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Range

Review of 7480d880..HEAD.

## Commits

### 56f0bcb7 docs(f085): save the R34 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r34.md | +373/-0 | C0a: block saved byte-for-byte |

### b928de97 docs(f085): mirror the R34 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +304/-236 | C0b: identical bytes mirrored |

### c15798a8 docs(review): narrow checklist items 15 and 20
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +24/-0 | C1: P15F→P15T, P20F→P20T |

### 2342ed97 docs(review): record the R33 FAIL and register and resolve R-0522 to R-0524
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +104/-0 | C2: RECORD2 appended, nothing else |

### 942ecbf1 docs(f085): advance the plan to R34
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +3/-3 | C3: PLANF2→PLANT2, file stays 47 lines |

### (this commit) docs(f085): rewrite the handback for R34
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
`git worktree list` = 1 line throughout; this round created none.

G2 TRANSPORT — pass. Committed `.agent/authored/f085-r34.md`, committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL: sha256
42bf5eeb4bd3725848d7f824912827a9bff4948a18dd2f6cf13bc6caec46835b, 24167 B,
373 lines, 14 marker lines, regions 1-100 / 101-200 / 201-373 = 2764ed2a / 6fe4a6ca
/ 2b83c685 (trailing newlines included) — every value measured, none computed by hand.

G3 APPEND SHAPE — pass. Pre-commit blob 373548 B is a byte-exact PREFIX of the
381289 B post-commit file; remainder 7741 B = one blank line + RECORD2's 7740 B;
RECORD2 is an exact suffix; its first line occurs once among the 104 lines 2342ed97
adds; 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the `BEGIN` SUBSTRING occurs 9×
— which is why LINES were counted.
`git show --numstat 2342ed97 -- .agent/live_review.md` = `104  0`.

G4 ARITHMETIC — pass. Base 7480d880: 136 registered / 18 done / 0 landed, 118 open,
both maxima R-0521 — reproduces the reviewer's base exactly. HEAD: 139 / 21 / 0,
118 open again, both maxima R-0524. Registered symmetric difference
{R-0522, R-0523, R-0524}, done symmetric difference the same three, landed symmetric
difference empty, 0 duplicate ids, 0 resolutions naming an unregistered id, maximum
id R-0524, next free R-0525.

G5 NARROWINGS + APPEND OBLIGATION — pass, measured at HEAD after C1, in
`docs/agents/planner_reviewer_prompt.md`. The P15F text still occurs exactly once and
the P20F text still occurs exactly once — both pairs are APPEND-shaped, so their FROMs
survive by construction. The item-15, item-16 and item-20 openers and the `Why this is
on disk and not a habit…` closer each occur exactly once: two items narrowed, none
added, removed or renumbered. §4.9 append obligation: P15T contributes 12 TO-only
lines and P20T 12, and each of those 24 occurs exactly once among the 24 lines C1's
diff ADDS. 0 marker lines reached the file. `git show --numstat c15798a8` = `24  0`.

G6 SUITES — pass, run in the PRIMARY checkout, never in a worktree (R-0518).
- 4 state readers, `-rf -q`: exit 0, `159 passed in 21.14s` (base 159 passed).
- `python3 -m pytest tests/docs/ -q`: exit 0, `295 passed in 0.51s` (base 295). Not
  read as evidence about C1: no test under `tests/docs/` reads that file.
- CANARY `tests/cli/test_golden_path.py -q`: exit 0, `42 passed in 21.85s` (base 42).
No ruff run and no red proof were ordered: this round changed no production code.

G7 HYGIENE — pass, measured BEFORE C4. `git diff --name-only 7480d880..HEAD` holds
exactly the 5 declared paths (change set minus `.agent/handoff.md`), nothing else.
Per-commit insertions 373, 304, 24, 104, 3 — none exceeds 500. All 5 commits have
exactly one parent; `git reflog -10` holds only `commit:` entries.

STALENESS (constraint 8), re-read after C3: `.agent/authored/f085-r34.md`,
`.agent/last_block.md`, `docs/agents/planner_reviewer_prompt.md`,
`.agent/live_review.md`, `.agent/plan.md`. Each commit touches exactly one path and no
commit after C2 touches a file RECORD2 asserts about; C1 precedes C2 as constraint 9
requires, so RECORD2's claims about the narrowed items 15 and 20 were true when
written. `HEAD` appears nowhere in RECORD2; every commit id it asserts (c2033d6c,
7480d880, 74dfa30e, c933b949) resolves, and the R-0522 and R-0524 resolutions name
constraint 9 under the item-20 carve-out C1 landed.

## Authored-text proofs

All four slices were extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f085-r34.md` by marker pair, none retyped, 0 marker lines reaching
any target file.
- P15F→P15T — TO contains FROM: true — APPEND. FROM matched exactly once before
  apply; the §4.9 append obligation is the reading reported under G5, and no
  FROM-zero count is claimed, because for an append pair none exists.
- P20F→P20T — TO contains FROM: true — APPEND. Same obligation, same G5 reading.
- PLANF2→PLANT2 — TO contains FROM: false — REWRITE. FROM matched exactly once
  before apply and 0 times after; the TO occurs exactly once after.
- RECORD2 — APPEND to `.agent/live_review.md`, proved by the prefix, remainder and
  exact-suffix byte equalities under G3.

## Deviations & assumptions

No deviation from the block: C0a, C0b, C1, C2, C3, C4 ran in exactly that order, one
commit each — nothing added, dropped, merged or reordered.
Observation, not a repair: RECORD2's R-0523 resolution says the false sentence "stays
in `.agent/handoff.md` where it landed". C4 rewrites that file per constraint 10, so
the sentence stays in the commit 7480d880 where it landed and not in the file's
current content. The slice was applied byte-verbatim and nothing was edited.
Deviations, declared: this handback is 152 lines against the 100-line cap (>5-commit
case). Cause is mandated content, not prose: six per-commit changed-files tables, the
six-row item-status table, the verbatim Fortschritt block, seven gate transcripts
G1-G7, the constraint-8 staleness reading and the four-pair proof list. No section was
dropped to fit.

## Next

The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk —
BEFORE rule 2, the Open PR Gate
(`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
R34's own verdict is NOT a §4.13 terminator, because this branch continues. The next
reviewed round records R34's gate entry in `.agent/live_review.md`. The next
MIGRATION round takes `mission_state.py`'s spawn, because `builder_bridge.py` cannot
move until the seam can SET an environment value rather than only allowlist a key.
