# Handback — F037 R12

## Session

SESSION 3 of feature F037 · round 12 · rounds so far 12

## Range

Review of `f676f419`..`HEAD` (branch `feature/f037-rendered-diff-viewer`).

## Commits

### b53f4928 docs(agent): save the F037 R12 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r12.md` | +439 | C0a: the block file's bytes saved verbatim |

### ed7154e8 docs(agent): mirror the F037 R12 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +319/−206 | C0b: mirror; one git blob with the saved copy |

### 8b1ee6a2 docs(agent): point the plan at the F037 R12 ceiling round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +19/−18 | C1: PLANF037R12 applied byte for byte |

### 5c1c624b docs(agent): book the R11 gate verdict and the timing slip
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 | C2: appends GATER11; nothing registered, nothing resolved |
| `.agent/prose_slips.md` | +13 | C2: appends SLIPR12, the `tracemalloc` timing slip |

### 1683c765 feat(orchestration): bound the parsed diff with DECISION F037 D5
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +63 | C3: appends DECISION5 |
| `packages/orchestration/diff_parser.py` | +22 | C3: SPEC S1–S6; constant, counter, guard, WHY comment |

### c9525027 test(orchestration): pin the parse ceiling and its exact boundary
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_diff_parser.py` | +117 | C4: SPEC S7–S12; one import line and one new END section, additions only |

### 21fc04eb docs(agent): resolve R-0721
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 | C5: appends DONE0721; `R-0721` resolved IN PART |

### C6 (this commit) docs(agent): hand back F037 R12
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C6: this handback; a handoff cannot table the commit that writes it |

## External actions

- `git worktree add --detach .remedy-wt/r12-mut c9525027` — exit 0 (G6).
- `git worktree remove .remedy-wt/r12-mut` — exit 0; `git worktree prune` exit 0.
- `git worktree add --detach .remedy-wt/r12-base f676f419` — exit 0 (G7 base timing).
- `git worktree remove .remedy-wt/r12-base` — exit 0; `git worktree prune` exit 0.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, stdout `[]`.
- `git push` of `feature/f037-rendered-diff-viewer` after this commit.
- No PR created, nothing merged.

## Verification

**G1 hygiene.** `.agent/STOP` read from disk before C0a: DOES NOT EXIST. Read again
before C6: DOES NOT EXIST. `git rev-parse HEAD` before C0a =
`f676f41981d83613ab4b216b75e372151881bd83`, which EQUALS the block's base.
`git branch --show-current` = `feature/f037-rendered-diff-viewer`.
`git status --porcelain` line count after C0a 0, after C0b 0, after C1 0, after C2 0,
after C3 0, after C4 0, after C5 0.

**G2 transport, one digest comparison.** `git rev-parse HEAD:.agent/authored/f037-r12.md`
= `dab1d123bf1dace73fa89323a671c1cdafa69528`; `git rev-parse HEAD:.agent/last_block.md`
= `dab1d123bf1dace73fa89323a671c1cdafa69528`; SAME BLOB HASH: True. Working copy of
`.agent/authored/f037-r12.md`: sha256
`29c103ae837cbf96b80f39377f514531ddcc89956d1fc19486a6dfe127e38bb3`, 32012 bytes,
439 lines — identical to the sha256 measured on `.remedy-wt/f037-r12-block.md` before
C0a. THE CHAIN COVERS: the saved copy and its mirror. It does not certify how the
block's bytes reached that scratch path.

**G3 extraction and caps** — measured on the COMMITTED C0a blob (`git show
b53f4928:.agent/authored/f037-r12.md`, exit 0, 32012 bytes, byte-identical to the
working copy). No figure carried from the block's prose.

| Slice | content lines |
|---|---|
| PLANF037R12 | 47 |
| GATER11 | 1 |
| SLIPR12 | 12 |
| DECISION5 | 62 |
| DONE0721 | 1 |
| CONTENT | 123 |
| TOTAL | 439 |
| PROSE = TOTAL − CONTENT | 316 |

TOTAL at most 490: True. PROSE at most 400: True.

**G4 the plan at C1.** `.agent/plan.md` byte-equal to PLANF037R12 including the
trailing newline: True. NEGATIVE CONTROL against the slice minus its trailing newline:
False. Lines exactly `## Goal`: 1. Lines exactly `## Next Steps`: 1. `wc -l` exit 0 =
47; STRICTLY under 50: True.

**G5 the record at C2, C3 and C5.**

| Append | file | before (bytes) | after (bytes) | reader (a) | reader (b) | NEG CONTROL (a)/(b) |
|---|---|---|---|---|---|---|
| GATER11 | `.agent/live_review.md` | 1193281 | 1198371 | True | True, N=1 | False / False |
| SLIPR12 | `.agent/prose_slips.md` | 9696 | 10681 | True | True, N=1 | False / False |
| DECISION5 | `.agent/decisions.md` | 659752 | 663863 | True | True, N=10 | False / False |
| DONE0721 | `.agent/live_review.md` | 1198371 | 1200063 | True | True, N=1 | False / False |

Reader (a) is `result == before + b"\n" + slice` re-read from disk. Reader (b) counts
the N blank-line-separated units of the slice and compares the LAST N units of the file
against them IN ORDER. The negative control flips ONE byte inside the FIRST appended
paragraph; both readers come back False for all four appends. The PRE-ROUND (base
`f676f419`) blob of each file is a byte PREFIX of its result: `.agent/live_review.md`
True (1193281 → 1200063), `.agent/prose_slips.md` True (9696 → 10681),
`.agent/decisions.md` True (659752 → 663863).

Line-anchored counts over `.agent/live_review.md` after C5, with the base figures beside
them: `^- R-\d+ — ` 282, UNMOVED from 282; `^Done: R-\d+ — ` 30, from 29;
`^Landed: R-` 1, UNMOVED; `^Gate: F\d+ R\d+ — ` 82, from 81. Open set size 252, from
253. Every registered id distinct: True. `R-0721` occurs ZERO times as a NEW
registration this round (its single registration is R11's, still the only one) and
EXACTLY ONCE as a resolution; it is no longer in the open set. Over
`.agent/decisions.md`: `^## DECISION ` 171, and the count of `F037 D5` is exactly 1.

**G6 the red-proofs of the ceiling.** All runs inside the disposable worktree
`.remedy-wt/r12-mut` at the C4 tree `c9525027`, never in the primary checkout.
`__pycache__` purged before EVERY run (0 directories found each time — `python3 -B`
writes none) and `python3 -B` used for every run. The parser was restored between runs
and each restore verified byte-identical, by both a full-bytes comparison and a sha256
comparison, against the unmutated file — sha256
`a5b40fe9243f63f9ad8a3aa139ac19d8c7aa14aefcd1f764f42989dd9c49b7f0` over 30204 bytes,
measured on the C4 blob `git show c9525027:packages/orchestration/diff_parser.py`.
RESTORE byte-identical: True after every one of the four mutations, and True again at
the end of the run.

UNMUTATED CONTROL — `python3 -B -m pytest tests/orchestration/test_diff_parser.py -q`:
REAL exit code 0, `37 passed in 2.19s`.

**(a) the bound removed.** Exact string replaced (deleted): the three lines
`if body_lines_appended >= DIFF_VIEW_MAX_BODY_LINES:` / `truncated = True` / `break`
at their own indentation; occurrences BEFORE the edit: 1. REAL exit code 1,
`4 failed, 33 passed in 2.48s`. Node ids that FAIL as measured:
`::test_a_diff_far_above_the_ceiling_stops_at_exactly_the_ceiling`,
`::test_the_ceiling_boundary_holds_on_both_of_its_sides`,
`::test_many_small_files_are_bounded_by_the_same_total_counter`,
`::test_every_file_stats_still_recount_its_own_lines_under_truncation`. COLOUR: RED.

**(b) the flag not set.** Same three lines replaced by the guard and `break` alone,
without `truncated = True`; occurrences BEFORE the edit: 1. REAL exit code 1,
`4 failed, 33 passed in 2.25s`. The SAME four node ids fail as under (a), but on the
`truncated is True` assertion rather than on the line count — which is exactly the
separation this mutation exists to make. COLOUR: RED.

**(c) the counter scoped to one hunk instead of the whole diff.** Exact string
replaced: `                if body_lines_appended >= DIFF_VIEW_MAX_BODY_LINES:`;
occurrences BEFORE the edit: 1. Replaced by
`                if len(hunk["lines"]) >= DIFF_VIEW_MAX_BODY_LINES:`, so the guard
reads the CURRENT HUNK's own length. REAL exit code 1, `2 failed, 35 passed in 2.23s`.
Node ids that FAIL as measured:
`::test_many_small_files_are_bounded_by_the_same_total_counter`,
`::test_every_file_stats_still_recount_its_own_lines_under_truncation`. COLOUR: RED.
The two single-file tests survive it because one file's single hunk holds the whole
body there, so hunk-scope and diff-scope coincide; the many-files shape is the only
one that can see the wrong scope, which is what SPEC S9 says it is for. The
`open_region` spelling the block warns against was NOT substituted.

**(d) the ceiling lowered below the Acceptance fixture.** Exact string replaced:
`DIFF_VIEW_MAX_BODY_LINES = 20_000` → `DIFF_VIEW_MAX_BODY_LINES = 9_000`; occurrences
BEFORE the edit: 1. REAL exit code 1, `4 failed, 33 passed in 1.26s`. Node ids that
FAIL as measured: `::test_the_huge_single_file_diff_parses_to_one_complete_file`,
`::test_line_numbering_survives_the_whole_huge_file`,
`::test_the_huge_diff_parses_inside_the_recorded_perf_budget` — THREE of the four tests
R11 added, untouched by this round — plus this round's
`::test_the_acceptance_fixture_stays_below_the_ceiling_and_is_not_truncated`. COLOUR:
RED. Constraint 9 is therefore proved rather than asserted: a ceiling below the 10,000
-line fixture Acceptance names is caught by the R11 regression guard. The fourth R11
test, `::test_the_many_file_diff_keeps_every_file_distinct_and_in_input_order`, stays
green under (d) because its 400 files carry 800 body lines in total, far below even the
lowered 9,000 — reported because the block's own gate is the COLOUR and not a predicted
name or count.

No mutation came back GREEN. Afterwards: `git worktree remove` exit 0, `git worktree
prune` exit 0, `git worktree list` line count 1, `git status --porcelain` in the primary
checkout 0 lines. `git status --porcelain` INSIDE the worktree read 0 lines before
removal.

**G7 suite, lint and canary at C4.** One pytest process at a time throughout; no two
pytest runs overlapped.

- `python3 -m pytest tests/orchestration/ -q` — THE WHOLE DIRECTORY. REAL exit code 0,
  `11502 passed, 7 skipped in 669.08s (0:11:09)`. Count of lines matching `^FAILED`
  over the COMPLETE captured output (162 lines, 12845 bytes): 0. EXTRACTOR-BLINDNESS
  CONTROL: the same counter over that output plus one control line that does begin with
  `FAILED` returns 1, so the 0 above is a measurement. This gate was run twice — see
  Deviations 2.
- `python3 -m pytest tests/ui_server/test_diff_endpoint.py -q` — REAL exit code 0,
  `6 passed in 2.59s`; lines matching `^FAILED`: 0.
- `python3 -m ruff check packages/orchestration/diff_parser.py
  tests/orchestration/test_diff_parser.py` under the repository's own configuration,
  NO `--isolated` — REAL exit code 0, `All checks passed!`.
- Canary `python3 -m pytest tests/cli/test_golden_path.py -q` — REAL exit code 0,
  `42 passed in 20.58s`. Base figure `42 passed`; measured `42 passed`; NO DIFFERENCE.
- Parser suite `in <n>s` figure: at the base `f676f419`, measured in the disposable
  worktree `.remedy-wt/r12-base`, exit 0, `32 passed in 0.59s`; at C4, exit 0,
  `37 passed in 2.14s`. DIFFERENCE +1.55 s for +5 tests. The cost is the five new
  fixtures: S7 generates 40,000 body lines, S8 generates 20,000 and 20,002, S9 and S11
  each generate 10,400 files carrying 20,800 body lines. At the measured ~10 µs per
  body line that is the whole of the increase; the suite is still comfortably under
  three seconds and the whole `tests/orchestration/` directory is green.

**G8 structure, artifacts and the Open PR Gate at C5.**
`git diff --name-only f676f419..21fc04eb` exit 0, returning exactly:
`.agent/authored/f037-r12.md`, `.agent/decisions.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`packages/orchestration/diff_parser.py`, `tests/orchestration/test_diff_parser.py`.
RESIDUE actual minus expected: `[]`. RESIDUE expected minus actual: `[]`.
`git diff --stat` restricted to `docs/`: EMPTY. To `apps/`: EMPTY. To `packages/`:
holds ONLY `packages/orchestration/diff_parser.py | 22 ++++`, and that single-path
reading is what proves constraint 3 — `diff_view_source.py` and `ui_server.py` are
untouched.

| Commit | insertions | under 500 | parents |
|---|---|---|---|
| C0a b53f4928 | 439 | True | 1 |
| C0b ed7154e8 | 319 | True | 1 |
| C1 8b1ee6a2 | 19 | True | 1 |
| C2 5c1c624b | 15 | True | 1 |
| C3 1683c765 | 85 | True | 1 |
| C4 c9525027 | 117 | True | 1 |
| C5 21fc04eb | 2 | True | 1 |

Marker sweep `^<<<SLICE ` / `^<<<END `: `.agent/plan.md` at C1 — 0 / 0.
`.agent/live_review.md` at C5 — 0 / 0. `packages/orchestration/diff_parser.py` at C3 —
0 / 0. `tests/orchestration/test_diff_parser.py` at C4 — 0 / 0. The SAME counter over
the C0a blob — 5 / 5, both greater than zero, so the zeros above are a measurement and
not a blind counter. `git ls-files .remedy-wt` line count: 0.
Open PR Gate, verbatim: `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` exit 0, stdout `[]` — no open PRs. Nothing
merged, nothing created.

## Authored-text proofs

- `.agent/authored/f037-r12.md` vs the reviewer's scratch original
  `.remedy-wt/f037-r12-block.md`: sha256 equal
  (`29c103ae837cbf96b80f39377f514531ddcc89956d1fc19486a6dfe127e38bb3`), 32012 bytes,
  439 lines. Not edited in transit.
- `.agent/plan.md` vs the PLANF037R12 slice extracted from the COMMITTED C0a blob:
  byte-equal True, trailing-newline negative control False.
- `.agent/live_review.md` vs GATER11 and DONE0721, `.agent/prose_slips.md` vs SLIPR12,
  `.agent/decisions.md` vs DECISION5, all extracted from the committed C0a blob: byte
  identity True for all four appends, negative controls False for both readers.
- Production code was DESCRIBED by SPEC S1–S12 and written by me, not sliced, as
  constraint 2 orders. No authored text was applied to
  `packages/orchestration/diff_parser.py` or `tests/orchestration/test_diff_parser.py`.

## Deviations & assumptions

1. **SPEC S4's "one-line WHY comment" is six lines.** S4 requires the comment to state
   three separate facts — that `truncated` is the contract's own field, that the stop is
   deliberate rather than an error, and that the last file of a truncated view may hold a
   partial hunk or none. Those do not fit one line at this file's 88-column prose width,
   so the comment is a block whose FIRST line is the WHY line and which sits directly
   above the guard, which is where a search lands. S5's deliberate-absence note went into
   the CONSTANT's comment, which S5 permits explicitly.
2. **G7's whole-directory gate was RUN TWICE, both times exit 0.** The first run's stdout
   was piped through `tail -15`, which cannot carry the `^FAILED` completeness sweep the
   gate also orders, so the gate was re-run with the output captured entire. First run:
   exit 0, `11502 passed, 7 skipped in 721.93s (0:12:01)`. Second run, the one reported
   above: exit 0, `11502 passed, 7 skipped in 669.08s (0:11:09)`, `^FAILED` count 0 over
   all 162 output lines. The two runs agree on pass count and on colour; only the
   wall-clock differs.
3. **One unordered worktree.** `.remedy-wt/r12-base` at `f676f419` was created to take
   G7's ordered base timing figure, which cannot be measured in the primary checkout
   because the parser and its tests differ there. It was removed and pruned; nothing in
   the primary checkout was touched.
4. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4, C5, C6 in
   that order, one commit each, no extra commit, none dropped, none reordered.
5. **Mutation (c) and (d) fired on fewer / different tests than a reader might predict.**
   (c) kills 2 rather than 4; (d) kills 3 of R11's 4 rather than all 4. Both are reported
   as measured above with the reason, per the block's own instruction that the ordered
   property is the COLOUR and not a predicted name or count.
6. **Scratch scripts.** Five throwaway measurement scripts and three log files were
   written under the gitignored `.remedy-wt/` and removed BY EXACT PATH after use;
   `git ls-files .remedy-wt` reads 0. `.remedy-wt/f037-r12-block.md`, the reviewer's own
   scratch original, was left in place.
7. **No measurement disagreed with a numeral in the block's prose.** The module is 652
   lines at the base as the SPEC states, the four R11 tests are untouched and all four
   still pass in the unmutated control, and every cap the block names held on the bytes
   actually committed.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into last_block | done | one blob with the saved copy |
| C1 the plan | done | byte-equal to PLANF037R12, 47 lines |
| C2 the R11 verdict and the timing slip | done | GATER11 + SLIPR12; nothing registered |
| C3 DECISION F037 D5 and the ceiling | done | SPEC S1–S6; +22 lines in the parser |
| C4 the boundary tests | done | SPEC S7–S12; 5 tests, both sides of the boundary |
| C5 the resolution | done | `R-0721` resolved IN PART; open set 253 → 252 |
| C6 the handback | done | this file |
| G1 hygiene | PASS | STOP absent twice; HEAD == base; porcelain 0 after every commit |
| G2 transport | PASS | one blob `dab1d123`; sha256 matches the scratch original |
| G3 extraction and caps | PASS | TOTAL 439 ≤ 490, PROSE 316 ≤ 400 |
| G4 the plan | PASS | byte-equal, 47 lines, control False |
| G5 the record | PASS | 4 appends, both readers True, all controls False, prefixes True |
| G6 red-proofs | PASS | control exit 0; (a) (b) (c) (d) all exit 1 — four REDs |
| G7 suite, lint, canary | PASS | exits 0/0/0/0; 11502 passed; canary 42 passed, unchanged |
| G8 structure and Open PR Gate | PASS | both residues empty; `packages/` holds one path |
| R-0721 | resolved in part | parser half repaired; the `read_text` half is R13 |

## Next

Review this round at `f676f419..HEAD`, then order R13: the other half of `R-0721` —
`packages/orchestration/diff_view_source.py` still reads the artifact whole with
`read_text` before the parser ever sees it, so the INPUT is unbounded even though the
OUTPUT no longer is. T002's rendering core and all of T003 stay BLOCKED while the
frontend test runner is refused here. Phase 1 rule 1 first: re-read `.agent/STOP` from
disk before authoring.
