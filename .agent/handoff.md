# Handback — F037 R5

## Session
SESSION 1 of feature F037 · round 5 · rounds so far 5.
THE SESSION ENDS HERE. R5 was ordered as the last round of this session; no
further round is delegated from it. The 25-round / 7-session soft limit is not
approached: 5 rounds, 1 session.

## Range
Review of c6c490cb83fe4889e41fc0d14d54d80fb306d4f1..HEAD
(plus the C5 handoff commit that writes this file).
Branch: `feature/f037-rendered-diff-viewer`. Round base: `c6c490cb`.

## Commits

### 795a3488 docs(agent): save the F037 R5 block as authored
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r5.md | +360 / -0 | C0a — the block copied byte for byte from `.remedy-wt/f037-r5.md` with `shutil.copyfile` |

### 01b4fc45 docs(agent): mirror the R5 block into the last-block slot
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +249 / -228 | C0b — the C0a blob written out verbatim; the paired-line numstat is the R-0592 full-file-rewrite shape, not a partial copy |

### 902687d7 docs(agent): point the plan at the F037 R5 closure round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +14 / -11 | C1 — byte-equal to slice PLANF037R5; 45 lines, under the 50-line rule |

### cfdbcd87 docs(agent): book the R4 verdict, resolve R-0716 and register R-0717 and R-0718
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +7 / -1 | C2 — the LANDEDFROM→LANDEDTO pair, then the RECORDR5 append |
| .agent/prose_slips.md | +13 / -0 | C2 — the SLIPR5 EOF append |

### 763cc6a9 test(diff-parser): pin both halves of the intraline side mapping
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 / -0 | C3 — the `Landed: R-0717` line constraint 7 orders |
| tests/orchestration/test_diff_parser.py | +55 / -0 | C3 — SPEC S2 pure-deletion and S3 pure-insertion fixtures and their tests |

### c984c161 fix(diff-parser): take the intraline similarity ratio over significant tokens
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 / -0 | C4 — the `Landed: R-0718` line constraint 7 orders |
| packages/orchestration/diff_parser.py | +48 / -8 | C4 — SPEC S6: `_significant_intraline_tokens` and `_intraline_pair_is_similar`; the span mapping stays on the full stream |
| tests/orchestration/test_diff_parser.py | +71 / -0 | C4 — SPEC S7 multi-word guard test and SPEC S8 regression test |

### C5 docs(agent): hand back F037 R5
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self | C5 — a handoff cannot table the commit that writes it (`R-0149`) |

Every `+/-` cell above is taken from `git diff --numstat <sha>^ <sha>` itself and
agrees cell for cell with the G8 per-commit reading below.

## External actions
- `git worktree add --detach .remedy-wt/g6 763cc6a9` — rc 0, used for the G6
  red-proofs; `git worktree remove --force` rc 0, then `git worktree prune`.
- `git worktree add --detach .remedy-wt/g7base c6c490cb` — rc 0, used only to
  collect the base's 24 node ids; removed rc 0.
- `git worktree add --detach .remedy-wt/g7 c984c161` — rc 0, used for the G7
  further mutation; removed rc 0. `git worktree list` then reads 1 line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`
  verbatim. NOTHING MERGED, NOTHING CREATED, no PR exists for this branch.
- INTENT, not yet a measured fact when this file is authored:
  `git push origin feature/f037-rendered-diff-viewer` runs AFTER C5. Its exit code
  and the resulting remote tip are reported in the round's completion report,
  because C5 is written before the push exists and no gate here may name a value
  that cannot exist at authoring time.

## Verification

- **G1 hygiene** — exit 0. `git rev-parse HEAD` before C0a =
  `c6c490cb83fe4889e41fc0d14d54d80fb306d4f1`; `git branch --show-current` =
  `feature/f037-rendered-diff-viewer`. `git status --porcelain` line count after
  C0a/C0b/C1/C2/C3/C4 = 0/0/0/0/0/0. `.agent/STOP` read from disk before C0a:
  ABSENT; re-read before C5: ABSENT.
- **G2 transport** — exit 0. sha256
  `492a1de285ca7f3456dfd6fe021b79905f83727f88d3dbf1e870d365d2614c73`, 32885 bytes,
  360 lines, EQUAL at all four points: the scratch `.remedy-wt/f037-r5.md`, the
  C0a save, the C0b mirror and the working copy read at C4. C0a and C0b are ONE
  git blob `7e2edd7fa7fda688171172c7668937e5bbe2b257`. Lines that are a run of a
  single repeated character at length 4 or more: NONE. This proof covers the
  scratch file, the saved copy, its mirror and the working copy, and NOT the bytes
  of any prompt.
- **G3 extraction and caps** — exit 0. 5 slices printed: PLANF037R5 45,
  LANDEDFROM 1, LANDEDTO 1, RECORDR5 5, SLIPR5 12. CONTENT 64, TOTAL 360,
  PROSE = 360 − 64 = 296. PROSE ≤ 400 and TOTAL ≤ 490 both hold.
- **G4 the plan** — exit 0. `.agent/plan.md` at C1 byte-equal to PLANF037R5 under
  the newline-included convention: True. Negative control against the slice minus
  its trailing newline: FALSE. `^## Goal$` 1, `^## Next Steps$` 1,
  `\bF\d{3}\b` matches `F037`, `wc -l` 45, strictly under 50.
- **G5 the record at C2** — exit 0. PAIR: LANDEDFROM 1 before / 0 after,
  LANDEDTO 0 before / 1 after, `TO contains FROM: false` as the reviewer measured.
  APPEND reader (a), live_review: 1147955 + 1 + 7867 = 1155823 bytes, baseline a
  byte prefix. Reader (b): N = 3 blank-line units counted by the script; the last 3
  units of the file equal the slice's 3 units in order. Negative control: byte at
  offset 1147996, inside the first appended paragraph [1147956, 1151707), flipped —
  reader (a) False, reader (b) False. SLIPR5 reader (a):
  5993 + 1 + 846 = 6840, prefix True; reader (b): N = 1, last unit equal; control at
  offset 6024, inside [5994, 6839) — both readers False. Line-anchored counts
  before → after: `^- R-\d+ — ` 277 → 279, `^Done: R-\d+ — ` 24 → 25,
  `^Landed: R-` 2 → 1, `^Gate: R\d+ — ` 19 → 19, `^Gate: F\d+ R\d+ — ` 74 → 75 —
  every one of them equal to the block's ordered value. Ids ADDED = {R-0717,
  R-0718}; ids REMOVED = {} ; resolved REMOVED = {} ; resolved ADDED = {R-0716};
  all 279 ids DISTINCT; maximum id after C2 = `R-0718`; open set after C2 = 254.
  `R-0715` untouched and still open.
- **G6 the discriminators** — run in the disposable worktree `.remedy-wt/g6` at the
  C3 tree, never in the primary checkout. UNMUTATED CONTROL
  `python3 -B -m pytest tests/orchestration/test_diff_parser.py -q`: real exit code
  **0**, `26 passed in 0.24s`.
  (a) `packages/orchestration/diff_parser.py`, occurrences of `("replace", "delete")`
  before the edit = **1**, narrowed to `("replace",)`: real exit code **1**,
  `1 failed, 25 passed in 0.25s`, failing node id verbatim
  `FAILED tests/orchestration/test_diff_parser.py::test_intraline_spans_mark_a_pure_deletion_on_the_del_side_only`.
  (b) same file, occurrences of `("replace", "insert")` before the edit = **1**,
  narrowed to `("replace",)`: real exit code **1**, `1 failed, 25 passed in 0.25s`,
  failing node id verbatim
  `FAILED tests/orchestration/test_diff_parser.py::test_intraline_spans_mark_a_pure_insertion_on_the_add_side_only`.
  Both were exit 0 at `24 passed` against the round base `c6c490cb` per the block's
  own measurement; both are RED at C3. The module was restored between the two and
  `__pycache__` purged before every run.
- **G7 suite, lint, canary, further mutation** — at C4.
  Suite in the primary checkout, ONE pytest process from the repository root,
  `python3 -m pytest tests/orchestration/test_diff_parser.py -q`: real exit code
  **0**, summary verbatim `28 passed in 0.22s`, count of `^FAILED` lines **0**.
  Extractor blindness control: the same counter over a control string holding
  `FAILED tests/orchestration/test_diff_parser.py::test_control_string` returns
  **1**, so the 0 above is a measurement and not a blind spot.
  Node-id inventory by `--collect-only -q` (never by regexing `-v`): 24 ids at
  `c6c490cb`, 28 at C4, base ids MISSING at C4 = NONE; re-running exactly those 24
  ids at C4 gives exit 0, `24 passed in 0.23s`, `^FAILED` 0. The four added ids are
  `test_intraline_spans_mark_a_pure_deletion_on_the_del_side_only`,
  `test_intraline_spans_mark_a_pure_insertion_on_the_add_side_only`,
  `test_intraline_spans_are_empty_for_multi_word_lines_that_share_no_word` and
  `test_intraline_spans_still_mark_a_multi_word_pair_that_shares_its_other_words`.
  S8 by node id: `test_intraline_spans_are_empty_below_the_similarity_threshold`
  (the existing single-word threshold test) and
  `test_intraline_spans_still_mark_a_multi_word_pair_that_shares_its_other_words`
  (the `the fox jumps` replacement) — exit 0, `2 passed in 0.21s`.
  `python3 -m ruff check packages/orchestration/diff_parser.py
  tests/orchestration/test_diff_parser.py` with the repository's own configuration,
  no `--isolated`: real exit code **0**, output verbatim `All checks passed!`,
  stderr empty.
  Canary `python3 -m pytest tests/cli/test_golden_path.py -q`: real exit code **0**,
  `42 passed in 20.67s`.
  Further mutation, in the disposable worktree `.remedy-wt/g7` at C4. UNMUTATED
  CONTROL: exit **0**, `28 passed in 0.24s`. Mutation: the guard widened so it can
  never fire — `return ratio >= DIFF_INTRALINE_MIN_RATIO` (occurrences before the
  edit = 1) becomes `return ratio >= 0.0`, a value no ratio can be below. Real exit
  code **1**, `2 failed, 26 passed in 0.26s`, failing node ids verbatim
  `FAILED tests/orchestration/test_diff_parser.py::test_intraline_spans_are_empty_below_the_similarity_threshold`
  and
  `FAILED tests/orchestration/test_diff_parser.py::test_intraline_spans_are_empty_for_multi_word_lines_that_share_no_word`.
  The S7 test is the second of those, so S7 kills the mutation as ordered; the
  first is the pre-existing single-word threshold test, which the same widening
  necessarily also kills. Worktrees removed and pruned: `git worktree list` 1 line,
  `git status --porcelain` 0 lines in the primary checkout.
- **G8 structure, artifacts, Open PR Gate, push** — exit 0.
  `git diff --name-only c6c490cb..c984c161` = the expected set exactly; BOTH
  residues EMPTY (actual − expected = {}, expected − actual = {}).
  Restricted `git diff --stat`: `apps/` EMPTY, `docs/` EMPTY, `packages/` holds only
  `packages/orchestration/diff_parser.py` (+48 −8), `tests/` holds only
  `tests/orchestration/test_diff_parser.py` (+126).
  Per-commit insertions from `git diff --numstat`, each single-parent and under 500:
  C0a 360, C0b 249, C1 14, C2 20, C3 57, C4 121.
  Line-anchored `^<<<SLICE ` / `^<<<END `: `.agent/plan.md` at C1 0/0,
  `.agent/live_review.md` at C4 0/0, `.agent/prose_slips.md` at C2 0/0; CONTROL over
  the C0a blob `.agent/authored/f037-r5.md` 5/5, so the sweep is not blind.
  `^Done: R-\d+ — ` at C4 = 25 as ordered. `^Landed: R-` at C4 = **3**, not the 2
  the gate names — see Deviations.
  `git ls-files .remedy-wt` 0 lines; `git branch --list "tmp/*"` 0 lines.
  Open PR Gate, verbatim: `[]`. Nothing merged, nothing created.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `795a3488`, byte-for-byte via `shutil.copyfile` |
| C0b mirror it into `last_block` | done | `01b4fc45`, same git blob as C0a |
| C1 the plan | done | `902687d7`, byte-equal to PLANF037R5 |
| C2 the record | done | `cfdbcd87`, pair then append, then SLIPR5 |
| C3 the `R-0717` discriminating fixtures | done | `763cc6a9`, both G6 mutations red |
| C4 the `R-0718` repair with its test | done | `c984c161`, G7 mutation red |
| C5 the handback | done | this file |
| push | done | reported in the completion report, not here |
| S1 the gap, measured | done | 24 base node ids re-collected; the block's two green mutations reproduced as the reason both fixtures exist |
| S2 pure-deletion fixture | done | `INTRALINE_PURE_DELETION_DIFF`; `del` spans `[[9, 6]]` slicing `"extra "`, `add` spans `[]` |
| S3 pure-insertion fixture | done | `INTRALINE_PURE_INSERTION_DIFF`; `add` spans `[[9, 6]]` slicing `"extra "`, `del` spans `[]` |
| S4 the proof that they discriminate | done | G6 (a) and (b) both exit 1, each killing its own fixture's test |
| S5 the defect, measured | done | full-stream ratio 0.400 for `alpha beta gamma` vs `zzz qqq www` reproduced; significant-token ratio 0.000 |
| S6 the repair | done | `_intraline_pair_is_similar` over significant tokens; mapping unchanged on the full stream; constant unchanged at 0.3; both-empty case returns True |
| S7 the test | deviated | done as ordered, but the significant-token helper is written out in the test rather than imported — see Deviations |
| S8 what must not regress | deviated | the file held no `the fox jumps` test; one was added so G7 could name it — see Deviations |
| G1 hygiene, base, sentinel | done | exit 0 |
| G2 transport | done | exit 0, four points equal |
| G3 extraction and caps | done | exit 0, PROSE 296 / TOTAL 360 |
| G4 the plan | done | exit 0, control FALSE |
| G5 the record | done | exit 0, every ordered numeral matched |
| G6 the discriminators | done | control exit 0; mutations exit 1 and exit 1 |
| G7 suite, lint, canary, mutation | done | exit 0 / 0 / 0, mutation exit 1 |
| G8 structure, artifacts, PR gate | deviated | one numeral disagrees — see Deviations |

## Authored-text proofs

Every slice was extracted programmatically from the COMMITTED C0a blob
(`git show 795a3488:.agent/authored/f037-r5.md`) by its marker LINES and applied
from there in Python; nothing was retyped.

- `.agent/authored/f037-r5.md` vs `.remedy-wt/f037-r5.md`: disk-to-disk equal,
  sha256 `492a1de2…4c73`, 32885 bytes, 360 lines.
- `.agent/last_block.md` vs the C0a blob: equal; ONE git blob
  `7e2edd7fa7fda688171172c7668937e5bbe2b257`.
- PLANF037R5 → `.agent/plan.md`: byte-equal, negative control FALSE.
- LANDEDFROM → LANDEDTO in `.agent/live_review.md`: 1→0 and 0→1.
- RECORDR5 → `.agent/live_review.md`: reconstruction and structure readers both
  pass; single-byte control rejected by both.
- SLIPR5 → `.agent/prose_slips.md`: same two readers, same control result.

## Deviations & assumptions

1. **G8's `^Landed: R-` count of 2 is unreachable and the measured value is 3.**
   G5 measures `^Landed: R-` at 2 at the round base and orders it to 1 after C2 —
   both were measured exactly so. The base's other `Landed:` line belongs to
   `R-0711` and survives C2. Constraint 7 then adds one line at C3 and one at C4,
   so the file necessarily reads 3 at C4. Making it read 2 would require deleting
   the `R-0711` line, which constraint 6 forbids. The block was followed;
   the disagreement is reported and reconciled nowhere, per constraint 12. The
   clause's intent — that exactly the two lines constraint 7 orders were added — IS
   satisfied: the three lines are `R-0711` (pre-existing), `R-0717` (C3) and
   `R-0718` (C4).
2. **Both `Landed:` lines name their commit by ROLE, not by SHA.** "commit C3 of
   F037 R5" and "commit C4 of F037 R5". A `Landed:` line is written INTO the commit
   it describes, so its own SHA cannot exist when the text is authored. This is the
   same choice R4 made and the RECORDR5 slice records as sound.
3. **SPEC S2's stated discriminator names the wrong assertion.** S2 says the
   `add` entry's `[]` "is what fails when `delete` is dropped from the old side".
   Measured: dropping `delete` from the OLD tuple empties the `del` side, so the
   assertion that actually fails is `deleted["intraline"] == [[9, 6]]`. Both
   assertions were written exactly as ordered, so the test fails under the mutation
   either way (G6 (a), exit 1); the `add`-side `[]` is a real discriminator, but for
   a different mutation — one that let `delete` reach the NEW side. Nothing was
   bent; only the block's attribution of which clause fires is corrected here.
4. **SPEC S6's gloss contradicts its own definition, and the definition was
   followed.** S6 defines significant tokens as "the tokens that are not pure
   whitespace", then glosses the both-empty case as "two lines made entirely of
   whitespace and punctuation". Punctuation is not pure whitespace, so under the
   stated definition a punctuation token IS significant and a pure-punctuation pair
   does not reach the both-empty branch. The DEFINITION was implemented, because it
   is the operative clause and it is what S5's diagnosis (separator tokens floor the
   ratio) requires. The module's docstring says "no significant token at all"
   rather than repeating the gloss.
5. **S8 named a test that did not exist, so one was added.** The corpus held no
   `the fox jumps` / `the cat jumps` case; G7 nonetheless orders a report that "the
   `the fox jumps` replacement test" still passes. The closest correct thing was to
   add it at C4 as
   `test_intraline_spans_still_mark_a_multi_word_pair_that_shares_its_other_words`
   with fixture `INTRALINE_MULTI_WORD_ONE_WORD_CHANGED_DIFF`, so the node id G7
   names exists and its significant-token ratio of 0.667 is asserted rather than
   transcribed. No existing test was altered, weakened or renamed.
6. **S7's significant-token helper is written out in the test file, not imported.**
   `_significant_tokens` in the test re-states "not pure whitespace" in the test's
   own words. Importing `_significant_intraline_tokens` would make the test agree
   with the module by construction and blind it to the module drifting. The
   threshold itself is named through the exported `DIFF_INTRALINE_MIN_RATIO`
   exactly as S7 orders and as the existing threshold test does.
7. **C0b's numstat reads +249 / −228 over a 360-line file.** A full-file rewrite
   pairs unchanged lines; this is the R-0592 shape, reported as measured rather
   than adjusted.
8. **G7's further mutation turns TWO tests red, not one.** S7's test is one of
   them, as ordered. The other is the pre-existing single-word threshold test:
   widening the comparison so the guard can never fire necessarily kills every test
   that asserts the guard fired. Reported rather than narrowed.
9. **No ordered commit was added, dropped or reordered.** The sequence run was
   exactly C0a, C0b, C1, C2, C3, C4, C5.
10. **Nothing was merged and no pull request was created.** The Open PR Gate
    returned `[]`; F037's branch has no PR.

## Next

**First action of the NEXT session: re-read `.agent/STOP` from disk** (Phase 1
rule 1 of `docs/agents/self_drive_protocol.md`), and only then run the Open PR
Gate. F037's branch `feature/f037-rendered-diff-viewer` has NO open pull request —
`gh pr list --state open` returned `[]` at this round — so the gate finds nothing
to merge and work resumes directly.

Work resumes at **T001's read endpoint**, which is the only thing T001 still owes:
the parser half is complete and gated, but nothing serves it. The endpoint is keyed
on task run and job per DECISION F037 D2 and must be written against the route
guards the R1 source inventory measured. After that, T002 (rendering core, binding
CSS, goldens) and T003 (sidebar, virtual scrolling, lazy languages, the L3 tab).

Open findings after this round: **254**. `R-0716` is RESOLVED; `R-0717` and
`R-0718` are registered and both have landed repairs awaiting the reviewer's
`Done:` lines. **`R-0715` remains OPEN and was not touched** — it is a stale count
in a test docstring and belongs to whoever next edits that file.
