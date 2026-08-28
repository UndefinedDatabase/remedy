# Handback — F037 R2 (book R1, register R-0715, amend the spec)

## Session

SESSION 1 of feature F037 · round 2 · rounds so far 2

## Range

Review of 69f6478c6c18b7957f3e244b9f121e372f22a99d..HEAD

## Commits

### 1f8d7826 chore(agent): save the F037 R2 block as authored
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r2.md | 416 / 0 | C0a — the block copied byte for byte from `.remedy-wt/f037-r2.md` with `shutil.copyfile` |

### 07d2a3f7 chore(agent): mirror the F037 R2 block into the last-block slot
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | 314 / 356 | C0b — mirror written from the committed C0a blob; same git blob `c0812abbe876801a5ac5c737918400f46ced453b` |

### 9b8cce95 docs(agent): point the plan at the F037 R2 booking round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | 24 / 27 | C1 — byte-equal to slice PLANF037R2 |

### 1d703c57 docs(agent): book the F037 R1 verdict, R-0715 and both DECISIONS
| Path | +/- | Reason |
|------|-----|--------|
| .agent/decisions.md | 84 / 0 | C2 — DECR2 appended; DECISIONS F037 D1 and D2 |
| .agent/live_review.md | 4 / 0 | C2 — RECORDR2 appended; the F037 R1 gate paragraph and finding R-0715 |
| .agent/prose_slips.md | 11 / 0 | C2 — SLIPR2 appended; the reviewer's own authoring slip |

### 390234c1 docs(roadmap): amend the F037 design against the R1 source inventory
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/features/T5_F037.md | 48 / 0 | C3 — DFROM→DTO pointer under the Design heading, then AMENDF037 appended (A1, A2, A3) |

### C4 docs(agent): hand back the F037 R2 round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self | a handoff cannot table the commit that writes it (R-0149) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `.agent/authored/f037-r2.md`, byte-identical to the scratch file |
| C0b mirror it into `last_block` | done | same git blob as C0a |
| C1 the plan | done | byte-equal to PLANF037R2, 44 lines |
| C2 the record — the R1 gate, `R-0715`, the slip and both DECISIONS | done | three EOF appends, each proved two ways |
| C3 the feature-file amendments | done | pair applied, AMENDF037 appended |
| C4 the handback | done | this file |
| push | done | ordered after C4; outcome reported in the round report, not here |

Open findings after this round: **252** (276 registered, 24 resolved, maximum id
`R-0715`). One finding registered this round, `R-0715`; none resolved.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — run
  once, at G8, after C3 and before C4. Output verbatim: `[]`. Nothing merged,
  nothing created, no pull request exists for this branch.
- `git push origin feature/f037-rendered-diff-viewer` is INTENDED immediately
  after this commit. Its exit code and the resulting remote tip do NOT appear
  here: this file is authored before the push exists, so stating either would be
  a value that cannot be true when written. Both are reported in the round
  report instead, per the block's G8.
- No worktree was added or removed. No branch was created or deleted. No merge.
  No `npm`, `npx`, `node` or `vite` was run and nothing was built.

## Verification

- **G1 — hygiene, the base and the sentinel · exit 0.** `git rev-parse HEAD`
  before C0a: `69f6478c6c18b7957f3e244b9f121e372f22a99d`, as ordered.
  `git branch --show-current`: `feature/f037-rendered-diff-viewer`.
  `git status --porcelain` LINE COUNT after C0a, C0b, C1, C2, C3: `0 0 0 0 0`.
  C4's own reading is taken after this commit and reported in the round report,
  as ordered. `.agent/STOP` read from disk before C0a: ABSENT; read again before
  C4: ABSENT.
- **G2 — transport · exit 0.** Four points, ALL EQUAL: sha256
  `e6ef75ba2400c2bc4c3ab30256e85f0a1bf7fb42e9a1ae4f9760763d485fc332`, 31950
  bytes, 416 lines — at `.remedy-wt/f037-r2.md`, at the C0a commit blob, at the
  C0b commit blob, and read off disk at C3. C0a and C0b are the SAME git blob,
  `c0812abbe876801a5ac5c737918400f46ced453b`. Lines of the saved block that are
  a run of one repeated character at length 4 or more: NONE. What this proof
  covers, in one sentence: the scratch file, the saved copy, its mirror and the
  working copy — and NOT the bytes of any prompt, which no party to this round
  measured.
- **G3 — extraction and caps · exit 0.** The extractor read the COMMITTED C0a
  blob by its marker LINES and printed 7 slices: PLANF037R2 44, RECORDR2 3,
  SLIPR2 10, DECR2 83, DFROM 1, DTO 3, AMENDF037 45. CONTENT 189, TOTAL 416,
  PROSE = 416 − 189 = 227. Markers counted as prose. PROSE 227 ≤ 400 and TOTAL
  416 ≤ 490; both caps hold.
- **G4 — the plan · exit 0.** `.agent/plan.md` at C1 BYTE-EQUAL to PLANF037R2
  under the newline-included convention: True. Negative control against the
  slice MINUS its trailing newline: False. Contract readings: `^## Goal$` 1,
  `^## Next Steps$` 1, `\bF\d{3}\b` matched (`F037`), `wc -l` 44 — strictly
  under 50.
- **G5 — the three record appends, at C2 · exit 0.** Each baseline was read with
  `git show`, never by reading a tracked working file; see Deviations for the
  baseline SHA. Reader (a), RECONSTRUCTION, and reader (b), STRUCTURE, both hold
  for all three, and every negative control was rejected by BOTH readers:

  | File | Slice | (a) byte-equal | (a) prefix | arithmetic (bytes) | N | (b) last N units | flip offset | (a) rejects | (b) rejects |
  |------|-------|----------------|------------|--------------------|---|------------------|-------------|-------------|-------------|
  | `.agent/live_review.md` | RECORDR2 | True | True | 1130704 + 1 + 5684 = 1136389 | 2 | equal IN ORDER | 1130710, inside the first appended paragraph (1130705…1133955) | True | True |
  | `.agent/prose_slips.md` | SLIPR2 | True | True | 4319 + 1 + 750 = 5070 | 1 | equal IN ORDER | 4325, inside the first appended paragraph (4320…5068) | True | True |
  | `.agent/decisions.md` | DECR2 | True | True | 649977 + 1 + 5442 = 655420 | 12 | equal IN ORDER | 649983, inside the first appended paragraph (649978…650125) | True | True |

  N is counted by the script from the slice itself, never asserted by the block.
  Line-anchored counts for `.agent/live_review.md`, before C2 then after C2:
  `^- R-\d+ — ` 275 → 276, `^Done: R-\d+ — ` 24 → 24, `^Landed: R-` 1 → 1,
  `^Gate: R\d+ — ` 19 → 19, `^Gate: F\d+ R\d+ — ` 71 → 72. All five match the
  block's ordered post-C2 values exactly. Finding ids ADDED as a SET:
  `{R-0715}`. Resolved ids ADDED: `{}`; resolved ids REMOVED: `{}`; finding ids
  REMOVED: `{}` — all three EMPTY. All 276 ids DISTINCT: True. Maximum id after
  C2: `R-0715`. Open set after C2: 252. `.agent/decisions.md`: `^## DECISION `
  166 before, 168 after; literal `## DECISION F037 D1 ` 0 before and EXACTLY 1
  after; literal `## DECISION F037 D2 ` 0 before and EXACTLY 1 after.
- **G6 — the feature file, at C3 · exit 0.** `docs/roadmap/features/T5_F037.md`:
  DFROM occurs EXACTLY 1x BEFORE the edit. After C3, DFROM occurs 1x and DTO
  occurs EXACTLY 1x — the APPEND-shaped obligation constraint 11 assigns this
  pair, `TO contains FROM` re-measured True here, which is why no FROM-zero
  count is ordered or attainable. The 2 TO-ONLY lines of DTO each occur EXACTLY
  1x among the lines C3's diff ADDS to that file: `> Amended below — see "Design
  amendments" at the end of this file. Where an` 1x, and `> amendment conflicts
  with this section, the amendment wins.` 1x. RECONSTRUCTION against the
  baseline with the pair applied in memory first: BYTE-EQUAL True, the paired
  baseline a byte PREFIX of the result True, arithmetic 5110 + 1 + 2870 = 7981
  bytes. `^## Design amendments$` 0 before, EXACTLY 1 after. `^## Do not touch$`
  1 before and 1 after.
- **G7 — the docs gate and the canary · REAL exit 0.** Run as ONE pytest
  process after C3 and before C4, from the repository root:
  `python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py
  tests/cli/test_golden_path.py -q`. Summary line VERBATIM:
  `367 passed in 21.04s`. COUNT of lines matching `^FAILED`: 0. The `^FAILED`
  extractor is NOT blind: run over the control string
  `FAILED tests/x.py::test_y - AssertionError\nok\n` it matched exactly 1 line.
  The reviewer's base reference `367 passed` at a real exit 0 with zero
  `^FAILED` lines is reproduced exactly.
- **G8 — structure, artifacts, the Open PR Gate and the push · exit 0.** Path
  set of `git diff --name-only 69f6478c..390234c1` compared BOTH WAYS against
  the Change list minus `.agent/handoff.md`: residue GOT−WANT `[]`, residue
  WANT−GOT `[]`. `git diff --stat 69f6478c..390234c1` restricted to `apps/`,
  `packages/` and `tests/`: EMPTY, EMPTY, EMPTY; restricted to `docs/` WHOLE:
  `docs/roadmap/features/T5_F037.md | 48 ++++…`, `1 file changed, 48
  insertions(+)` — that file ALONE. Per-commit insertions from
  `git diff --numstat`, each single-parent and under 500: C0a 416, C0b 314,
  C1 24, C2 99, C3 48. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
  `.agent/plan.md` at C1 and in `.agent/live_review.md`, `.agent/prose_slips.md`,
  `.agent/decisions.md` at C2 and in `docs/roadmap/features/T5_F037.md` at C3,
  against a CONTROL over the C0a blob reading 7 and 7 — not 0. `git ls-files
  .remedy-wt` 0 lines, `git worktree list` 1 line, `git branch --list "tmp/*"`
  0 lines. Open PR Gate output VERBATIM: `[]`. Nothing merged, nothing created.

## Authored-text proofs

Every slice applied this round was extracted PROGRAMMATICALLY from the committed
C0a blob via `git show 1f8d7826:.agent/authored/f037-r2.md`, split on its
`<<<SLICE ` / `<<<END ` marker LINES, and applied from there in Python. Nothing
was retyped, reflowed or corrected.

| Slice | Applied to | Disk-to-disk result |
|-------|-----------|---------------------|
| PLANF037R2 | `.agent/plan.md` at C1 | BYTE-EQUAL True; trailing-newline negative control False |
| RECORDR2 | `.agent/live_review.md` at C2 | EOF append; reconstruction BYTE-EQUAL True, structure reader True, both controls reject |
| SLIPR2 | `.agent/prose_slips.md` at C2 | EOF append; reconstruction BYTE-EQUAL True, structure reader True, both controls reject |
| DECR2 | `.agent/decisions.md` at C2 | EOF append; reconstruction BYTE-EQUAL True, structure reader True, both controls reject |
| DFROM → DTO | `docs/roadmap/features/T5_F037.md` at C3 | FROM 1x before; FROM 1x and TO 1x after; both TO-ONLY lines 1x among added lines |
| AMENDF037 | `docs/roadmap/features/T5_F037.md` at C3 | EOF append; reconstruction BYTE-EQUAL True against the paired baseline |

The block itself: `.agent/authored/f037-r2.md` and `.agent/last_block.md` carry
the identical sha256 as `.remedy-wt/f037-r2.md` and are ONE git blob.

## Deviations & assumptions

**Commit sequence.** The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed
exactly, in that order, with the record moving before the feature file as
constraint 4 fixes. No extra commit, no dropped commit, no reordering. ANY
COMMIT MADE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN `## Commits` ROW AND
ITS OWN ITEM-STATUS ROW; none was made, so no such row exists.

**ONE DEVIATION, DECLARED AND NOT SILENTLY CORRECTED: the G5 baseline SHA is
stale for one of the three files.** G5 orders each baseline read with
`git show 89b96df7:<path>`. I measured all three at that commit and at the round
base `69f6478c`:

- `.agent/prose_slips.md` — identical at both, 4319 bytes, sha256 `635bb72a2b75…`.
- `.agent/decisions.md` — identical at both, 649977 bytes, sha256 `b4073db0ecd0…`.
- `.agent/live_review.md` — DIFFERENT: 1126556 bytes at `89b96df7` against
  1130704 bytes at `69f6478c`. `89b96df7` is R1's C1; R1's C3 (`d4aef1db`) later
  reset the live-review header and appended the F032 R19 gate paragraph.

Appending to the `89b96df7` bytes would have DELETED R1's own header reset and
its F032 R19 gate entry from an append-only record, which constraint 5 forbids
outright, and constraint 3 — the block's stated ONLY definition of this
operation — says the baseline is "the target file's bytes as they stood before
the commit". I therefore read that one baseline with `git show
9b8cce95:.agent/live_review.md`, the pre-C2 tip, which is byte-identical to
`git show 69f6478c:.agent/live_review.md`. No tracked file was ever overwritten
to obtain a baseline, which is the property G5's clause exists to secure. The
block's own numbers confirm which reading it intended: `^Gate: F\d+ R\d+ — `
reads 70 at `89b96df7` and 71 at `69f6478c`, and the block states the base as
71. The other two files are unaffected because their bytes are equal at both
commits.

**Every other numeral the block stated about the round base was reproduced
exactly**, so there is nothing further to reconcile: 275 / 24 / 1 / 19 / 71
line-anchored counts before C2, `TO contains FROM: true` for the DFROM/DTO pair,
`367 passed` at a real exit 0 with zero `^FAILED` lines, and the Open PR Gate
reading `[]`.

**No defect was observed in the slices themselves.** Every slice applied cleanly
and every gate the block ordered came back green at a real exit code. I minted
no finding id, wrote no `Gate:` or `Done:` line and authored no DECISION, per
constraint 6.

**Assumptions.** (1) A slice's TEXT is its content lines joined with a newline
plus ONE trailing newline, per constraint 2, and that single definition was used
for every extraction, every reconstruction and every negative control. (2) A
"blank-line unit" in G5 reader (b) is a maximal run of non-empty lines, so runs
of consecutive blank lines separate the same units; under that reading the last
N units of each file equal the slice's N units in order. (3) The round base
`69f6478c` and the pre-C2 tip `9b8cce95` carry identical bytes for all three
record files, since C0a, C0b and C1 touch none of them.

## Next

The reviewer books the R2 verdict as a `Gate:` paragraph and plans T001 — the
unified-to-JSON parser as a NEW module with its corpus tests, then the read
endpoint — against the now-amended spec in
`docs/roadmap/features/T5_F037.md`.
