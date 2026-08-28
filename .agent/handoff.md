# Handback — F037 R13

## Session

SESSION 4 of feature F037 · round 13 · rounds so far 13

## Range

Review of `327c1333`..`HEAD` (branch `feature/f037-rendered-diff-viewer`).

## Commits

### e3cb2607 docs(agent): save the F037 R13 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r13.md` | +439 | C0a: the block file's bytes saved verbatim |

### cbc4ae87 docs(agent): mirror the F037 R13 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +416/−416 | C0b: mirror; one git blob with the saved copy |

### f3411900 docs(agent): set the plan for F037 R13
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +26/−24 | C1: PLANF037R13 applied byte for byte |

### 4cf51bdb docs(agent): book the R12 verdict and register R-0722
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 | C2: appends GATER12 then FIND0722 |
| `.agent/prose_slips.md` | +10 | C2: appends SLIPR13, the partial-resolution slip |

### 3d161c6c feat(orchestration): bound the file entries with DECISION F037 D6
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +80 | C3: appends DECISION6 |
| `packages/orchestration/diff_parser.py` | +29/−1 | C3: SPEC S1–S3; constant, cut, WHY comment, `Returns` sentence |

### b5ec4315 test(orchestration): pin the file ceiling and the payload budget
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_diff_parser.py` | +296/−14 | C4: SPEC S4–S11; 6 new tests, 4 new builders, the re-based fixture |

### 8f2f3000 docs(agent): resolve R-0722
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 | C5: appends DONE0722, after C3 and C4 as constraint 8 orders |

### C6 (this commit) docs(agent): hand back F037 R13
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C6: this handback; a handoff cannot table the commit that writes it |

## External actions

- `git worktree add .remedy-wt/f037-r13-gate b5ec4315 --detach` — exit 0 (G6).
- `git worktree remove .remedy-wt/f037-r13-gate` — exit 0; `git worktree list` then
  reads 1 line, the primary checkout.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0,
  stdout `[]`.
- `git push` of `feature/f037-rendered-diff-viewer` after this commit.
- No PR created, nothing merged, no branch created or switched.

## Verification

**G1 hygiene.** `.agent/STOP` read from disk before C0a: DOES NOT EXIST (`ls` exit 2,
"No such file or directory"). Read again before C6: DOES NOT EXIST, same reading.
`git rev-parse HEAD` before C0a = `327c1333a60b4293f44240781586fd7c757542b4`, which
EQUALS the block's base `327c1333`. `git branch --show-current` =
`feature/f037-rendered-diff-viewer`. `git status --porcelain` line count after C0a 0,
after C0b 0, after C1 0, after C2 0, after C3 0, after C4 0, after C5 0.

**G2 transport, one digest comparison.**
`git rev-parse cbc4ae87:.agent/authored/f037-r13.md` =
`2f9c30ae910007b4e7301b72d361ca347a3202b3`;
`git rev-parse cbc4ae87:.agent/last_block.md` =
`2f9c30ae910007b4e7301b72d361ca347a3202b3`; SAME BLOB: True. The committed C0a blob,
read with `git show`, measures sha256
`39a60cc6aa9423c9b7bfa3ed76e4e00b9597706efed9a0ccd8e6e79aac161260`, 34679 bytes,
439 lines; the reviewer's scratch original `.remedy-wt/f037-r13-block.md` measures the
same three readings, and a direct disk-to-disk byte comparison of the two returns True.
THE CHAIN COVERS: the scratch original, the saved copy and its mirror. It says NOTHING
about the bytes the reviewer emitted, which is unmeasurable from here.

**G3 extraction and caps** — measured on the COMMITTED C0a blob
(`git show e3cb2607:.agent/authored/f037-r13.md`), never on the block's prose.

| Slice | content lines |
|---|---|
| PLANF037R13 | 49 |
| GATER12 | 1 |
| FIND0722 | 1 |
| SLIPR13 | 9 |
| DECISION6 | 79 |
| DONE0722 | 1 |
| CONTENT | 140 |
| TOTAL | 439 |
| PROSE = TOTAL − CONTENT | 299 |

TOTAL at most 490: True. PROSE at most 400: True.

**G4 the plan at C1.** `.agent/plan.md` byte-equal to the PLANF037R13 slice extracted
from the committed C0a blob, INCLUDING the trailing newline: True. NEGATIVE CONTROL
against that slice minus its trailing newline: False. Lines exactly `## Goal`: 1. Lines
exactly `## Next Steps`: 1. `wc -l` = 49; STRICTLY under 50: True.

**G5 the record at C2 and C5.**

| Append | file | reader (a) | reader (b) | NEG CONTROL (a)/(b) | base blob a PREFIX |
|---|---|---|---|---|---|
| GATER12 | `.agent/live_review.md` | True | True, N=1 | False / False | True |
| FIND0722 | `.agent/live_review.md` | True | True, N=1 | False / False | True |
| SLIPR13 | `.agent/prose_slips.md` | True | True, N=1 | False / False | True |
| DONE0722 | `.agent/live_review.md` | True | True, N=1 | False / False | True |

Reader (a) is `result == before + b"\n" + slice` RE-READ from disk. Reader (b) counts the
N blank-line-separated units of the slice and compares the LAST N units of the file
against them IN ORDER; N measured as 1 for all four slices. The negative control flips
ONE byte inside the FIRST appended paragraph; both readers return False for all four
appends. Each file's PRE-ROUND blob was read with `git show 327c1333:<path>` INTO MEMORY,
never over the tracked file, and is a byte PREFIX of the result in all four cases.

Line-anchored counts over `.agent/live_review.md` after C5, base figure beside each:
`^- R-\d+ — ` 283, from 282; `^Done: R-\d+ — ` 31, from 30; `^Landed: R-` 1, UNMOVED;
`^Gate: F\d+ R\d+ — ` 83, from 82. Open set size 252, UNMOVED from 252 — R-0722 was
registered and resolved in the same round, so the set gains one and loses one; the
computed symmetric difference of the two open sets is EMPTY in both directions. Every
registered id distinct: True (283 registrations, 283 distinct). `R-0722` occurs EXACTLY
ONCE as a registration and EXACTLY ONCE as a resolution. Over `.agent/decisions.md`:
`^## DECISION ` 172, and the count of `F037 D6` is exactly 1.

**G6 the red-proofs of the file ceiling.** All runs inside the disposable worktree
`.remedy-wt/f037-r13-gate` at the C4 tree `b5ec4315`, never in the primary checkout.
`__pycache__` purged before EVERY run (0 directories found each time — `python3 -B`
writes none) and `python3 -B` used for every run. The parser was restored from the
unmutated C4 bytes after every mutation and each restore verified byte-identical by
sha256 against `b66d3164b74a23c3d5fe1b7fdef8496f079fd0002a2c2c5d68a435fd56b56027`
(32117 bytes): True after all five. `git status --porcelain` inside the worktree read 0
lines before removal.

UNMUTATED CONTROL — `python3 -B -m pytest tests/orchestration/test_diff_parser.py -q`:
REAL exit code 0, `43 passed in 2.37s`.

The five mutation runs used `python3 -B -m pytest tests/orchestration/test_diff_parser.py
-q --tb=no -rf`, the `-rf` being what makes the ordered NODE IDS readable — see
Deviations 2. The ordered property is the COLOUR; every name and count below is MEASURED,
not predicted.

**(a) the three S2 lines deleted.** Replaced string: the block
`if len(regions) > DIFF_VIEW_MAX_FILES:` / `truncated = True` /
`regions = regions[:DIFF_VIEW_MAX_FILES]` at its own indentation; occurrences BEFORE the
edit: 1. REAL exit code 1, `5 failed, 38 passed in 2.35s`. COLOUR: RED. Node ids that
FAIL: `::test_a_diff_of_files_with_no_body_lines_is_cut_to_the_file_ceiling`,
`::test_the_file_ceiling_boundary_holds_on_both_of_its_sides`,
`::test_binary_marker_files_are_bounded_by_the_file_ceiling_too`,
`::test_the_file_ceiling_counts_files_after_the_doubled_header_collapse`,
`::test_the_worst_case_payload_stays_inside_the_recorded_budget`.

**(b) S2's `>` changed to `>=`.** Replaced string:
`    if len(regions) > DIFF_VIEW_MAX_FILES:`; occurrences BEFORE the edit: 1. REAL exit
code 1, `1 failed, 42 passed in 2.37s`. COLOUR: RED. Node id that FAILS:
`::test_the_file_ceiling_boundary_holds_on_both_of_its_sides` — its at-ceiling half, on
`truncated is False`, which is exactly the half that exists for this off-by-one.

**(c) the three S2 lines moved ABOVE the collapse.** Anchor string
`    regions = _collapse_doubled_header_regions(regions)`; occurrences BEFORE the edit:
1. The three lines were removed from below it and re-inserted directly above it, so the
cut reads the UNCOLLAPSED region list. REAL exit code 1, `1 failed, 42 passed in 2.35s`.
COLOUR: RED. Node id that FAILS:
`::test_the_file_ceiling_counts_files_after_the_doubled_header_collapse` — the only
fixture in the file whose headers are doubled, and therefore the only one that can see
the placement at all. The other four file-ceiling tests survive it because their fixtures
carry no header echo, so collapsed and uncollapsed counts coincide there.

**(d) `DIFF_VIEW_MAX_FILES` raised tenfold.** Replaced string
`DIFF_VIEW_MAX_FILES = 2_000` → `DIFF_VIEW_MAX_FILES = 20_000`; occurrences BEFORE the
edit: 1. REAL exit code 1, `2 failed, 41 passed in 3.65s`. COLOUR: RED. Node ids that
FAIL: `::test_the_file_ceiling_counts_files_after_the_doubled_header_collapse`,
`::test_the_worst_case_payload_stays_inside_the_recorded_budget`.

**(e) `DIFF_VIEW_MAX_BODY_LINES` raised tenfold.** Replaced string
`DIFF_VIEW_MAX_BODY_LINES = 20_000` → `DIFF_VIEW_MAX_BODY_LINES = 200_000`; occurrences
BEFORE the edit: 1. REAL exit code 1, `3 failed, 40 passed in 11.02s`. COLOUR: RED. Node
ids that FAIL: `::test_many_small_files_are_bounded_by_the_same_total_counter`,
`::test_every_file_stats_still_recount_its_own_lines_under_truncation`,
`::test_the_worst_case_payload_stays_inside_the_recorded_budget`. THIS IS THE ONE THAT
MATTERS: the same mutation is exit 0 at `327c1333`, and it is the whole of `R-0722`'s
second half. The payload-budget test is the assertion that catches it, exactly as SPEC
S11 says it should; the two re-based tests catch it as well, because their fixture is now
sized against `DIFF_VIEW_MAX_FILES` and so no longer follows the body constant upward.

No mutation came back GREEN. `git status --porcelain` in the primary checkout: 0 lines
after the worktree was removed.

**G7 suite, lint and canary at C4.** One pytest process at a time throughout; no two
pytest runs overlapped. Every exit code below is the process's real return code, read
from `subprocess.run(...).returncode` — see Deviations 1.

- `python3 -m pytest tests/orchestration/test_diff_parser.py -q` — REAL exit code 0,
  `43 passed in 2.31s`.
- `python3 -m pytest tests/orchestration/test_diff_view_source.py
  tests/ui_server/test_diff_endpoint.py -q` — REAL exit code 0, `15 passed in 0.91s`.
  Base figure at `327c1333` is `15 passed`; measured `15 passed`; NO DIFFERENCE, which is
  the reading that shows constraint 3 held on behaviour and not only on the diff.
- `python3 -m ruff check packages/orchestration/diff_parser.py
  tests/orchestration/test_diff_parser.py` under the repository's own configuration, NO
  `--isolated` — REAL exit code 0, `All checks passed!`.
- Canary `python3 -m pytest tests/cli/test_golden_path.py -q` — REAL exit code 0,
  `42 passed in 20.72s`. Base figure `42 passed`; measured `42 passed`; NO DIFFERENCE.
- Parser suite `in <n>s` at C4: `2.31s` (and `2.37s`/`2.38s` on the two other runs of it
  this round), against the base figure `37 passed in 2.14s`. DIFFERENCE +0.17 s for +6
  tests, well under the two seconds that would oblige naming fixtures. The six new
  fixtures are cheap by construction: four of them carry NO body line at all, and the
  re-based S5 shape generates 40,000 body lines where the shape it replaced generated
  20,800.

**G8 structure, artifacts and the Open PR Gate at C5.**
`git diff --name-only 327c1333..8f2f3000` returns exactly, in this order:
`.agent/authored/f037-r13.md`, `.agent/decisions.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`packages/orchestration/diff_parser.py`, `tests/orchestration/test_diff_parser.py`.
RESIDUE actual minus expected: `[]`. RESIDUE expected minus actual: `[.agent/handoff.md]`
— the block's change set includes it and C6 is the commit that writes it, so it cannot
appear in a range ending at C5.

`git diff --stat 327c1333..8f2f3000` restricted to `docs/`: EMPTY. To `apps/`: EMPTY. To
`packages/`: holds ONLY `packages/orchestration/diff_parser.py | 30 +++-` (29 insertions,
1 deletion), and that single-path reading is what proves constraint 3 —
`diff_view_source.py` and `ui_server.py` are untouched.

| Commit | insertions | deletions | under 500 |
|---|---|---|---|
| C0a e3cb2607 | 439 | 0 | True |
| C0b cbc4ae87 | 416 | 416 | True |
| C1 f3411900 | 26 | 24 | True |
| C2 4cf51bdb | 14 | 0 | True |
| C3 3d161c6c | 109 | 1 | True |
| C4 b5ec4315 | 296 | 14 | True |
| C5 8f2f3000 | 2 | 0 | True |

Those `git show --numstat` figures were checked cell by cell against the `+/-` column of
the `## Commits` table above and agree in every cell.

Marker sweep `^<<<SLICE ` / `^<<<END `: `.agent/plan.md` 0 / 0; `.agent/live_review.md`
0 / 0; `packages/orchestration/diff_parser.py` 0 / 0;
`tests/orchestration/test_diff_parser.py` 0 / 0. The SAME counter over the C0a blob reads
6 / 6, both greater than zero, so the zeros above are a measurement and not a blind
counter. `git ls-files .remedy-wt` line count: 0.

Open PR Gate, run verbatim: `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` — exit 0, stdout `[]`. No open PRs; nothing
merged, nothing created.

## Authored-text proofs

- `.agent/authored/f037-r13.md` vs the reviewer's scratch original
  `.remedy-wt/f037-r13-block.md`, compared disk to disk: BYTE-EQUAL True, sha256
  `39a60cc6aa9423c9b7bfa3ed76e4e00b9597706efed9a0ccd8e6e79aac161260`, 34679 bytes,
  439 lines — the three readings the block ordered verified BEFORE C0a and again on the
  committed blob. Not edited in transit.
- `.agent/plan.md` vs the PLANF037R13 slice extracted from the COMMITTED C0a blob:
  byte-equal True, trailing-newline negative control False.
- `.agent/live_review.md` vs GATER12, FIND0722 and DONE0722; `.agent/prose_slips.md` vs
  SLIPR13; `.agent/decisions.md` vs DECISION6 — all extracted from the committed C0a
  blob: reader (a) True for every append, reader (b) True for every append, both negative
  controls False for every append.
- Production code and test code were DESCRIBED by SPEC S1–S11 and written by me, not
  sliced, as constraint 2 orders. No authored text was applied to
  `packages/orchestration/diff_parser.py` or `tests/orchestration/test_diff_parser.py`.

## Deviations & assumptions

1. **Exit codes were captured through `subprocess`, not `echo $?`.** This session's
   command guard REFUSES `$?` — `python3 -m pytest ... ; echo "REAL_EXIT=$?"` was denied
   outright, as were two other compound forms. Every gate was therefore run inside a
   `python3` process that reports `subprocess.run(...).returncode`, which is the same real
   exit code by a different reader. No gate's colour was inferred from output text.
2. **The mutation runs added `--tb=no -rf` to the ordered `-q`.** G6 orders "the node ids
   that fail" to be reported, and plain `-q` prints no such list. The unmutated control was
   run with plain `-q`. The flags change neither the colour nor the summary line; the
   control and the five mutations agree with the plain-`-q` runs of G7 on pass count.
3. **My measurement of SPEC S11's FILE-dimension figure disagrees with the recorded one.**
   The constant's comment carries the reviewer's 1.269 MB, as constraint 9 orders. I
   measure **1.233 MB** on the fixture I wrote. The BODY-dimension figure matches exactly
   at 2.096 MB (2,095,849 bytes). The gap is path length: SPEC S11 requires "at least
   sixty characters" and `_LONG_PATH_TEMPLATE` renders 73, evidently shorter than the
   reviewer's own fixture. Both figures are far inside the 4,000,000-byte budget and the
   SPEC value was applied unchanged.
4. **S5 adds an assertion to a test constraint 5 restricts to "the fixture and the
   docstring".** SPEC S5 explicitly orders the first test to assert that the surviving
   file count is STRICTLY BELOW `DIFF_VIEW_MAX_FILES`; constraint 5 says only the fixture
   and the docstrings change in those two tests. I applied S5, since it is the specific
   order. I also added `assert TRUNCATING_MANY_FILE_COUNT < DIFF_VIEW_MAX_FILES` beside
   the existing `generated_body_lines > DIFF_VIEW_MAX_BODY_LINES` line, because S5 states
   the fixture's defining property as a conjunction and only one half of it was pinned.
   That second assertion is my reading, not a literal order. Both tests' assertions about
   the body ceiling are unchanged.
5. **S4's "keeps its current behaviour" was read as BYTE-IDENTITY and proved.** The pair
   TEXT deliberately does NOT carry the pair index, so at the default of one pair the new
   builder emits exactly what the old one emitted. Verified by exec-ing the base builder
   out of `git show 327c1333:tests/orchestration/test_diff_parser.py` and comparing its
   output against the new builder's at 1, 3 and 400 files: byte-identical in all three.
   The cost is that at `pairs_per_file > 1` the repeated pairs carry identical text; no
   assertion in the file reads it, and the docstring says so.
6. **S11's long-path fixture is a SEPARATE builder.** `_generated_long_path_many_file_diff`
   is written out rather than added as a third parameter to `_generated_many_file_diff`,
   because S4 orders exactly one new parameter there and the byte-identity in 4 above
   depends on that builder's short path staying the default.
7. **G6's runs (d) and (e) were not slow.** The block warns they would take several
   minutes; measured they took 3.65 s and 11.02 s. The reason is this round's own change:
   the re-based S5 fixture is expressed in `DIFF_VIEW_MAX_FILES`, so raising
   `DIFF_VIEW_MAX_BODY_LINES` no longer multiplies it. Reported because a gate's real
   figure is the evidence and the block's prediction is not.
8. **Mutation fault counts are reported as MEASURED, not as predicted.** (b) and (c) kill
   one test each rather than several; (d) kills two; (e) kills three. Each is explained
   above beside its measurement, per the block's own instruction that the ordered property
   is the COLOUR.
9. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4, C5, C6 in
   that order, one commit each, no extra commit, none dropped, none reordered. C5 ran
   after both C3 and C4, as constraint 8 requires.
10. **Scratch.** Two throwaway measurement scripts were written under the gitignored
    `.remedy-wt/` — `f037_r13_ledger.py` and `f037_r13_g8.py` — and removed BY EXACT PATH
    after use; both paths now read "No such file or directory" and `git ls-files
    .remedy-wt` is 0. `.remedy-wt/f037-r13-block.md`, the reviewer's own scratch original,
    was left in place. The disposable worktree `.remedy-wt/f037-r13-gate` was removed with
    `git worktree remove`.
11. **No slice was edited.** Every slice was applied byte for byte out of the COMMITTED
    C0a blob, never retyped. Nothing in the six slices looked wrong.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | 439 lines, 34679 bytes, sha256 verified before and after |
| C0b mirror into last_block | done | one blob `2f9c30ae` with the saved copy |
| C1 the plan | done | byte-equal to PLANF037R13, 49 lines, under 50 |
| C2 the R12 verdict, `R-0722`, the slip | done | GATER12 + FIND0722 + SLIPR13 |
| C3 DECISION F037 D6 and the file ceiling | done | SPEC S1–S3; +29 lines in the parser |
| C4 the file-ceiling tests and the budget | done | SPEC S4–S11; 6 tests, 4 builders, 2 re-based |
| C5 the resolution | done | DONE0722, written after C3 and C4 |
| C6 the handback | done | this file |
| G1 hygiene | PASS | STOP absent twice; HEAD == base; porcelain 0 after every commit |
| G2 transport | PASS | one blob `2f9c30ae`; disk-to-disk equal to the scratch original |
| G3 extraction and caps | PASS | TOTAL 439 ≤ 490, PROSE 299 ≤ 400 |
| G4 the plan | PASS | byte-equal, 49 lines, negative control False |
| G5 the record | PASS | 4 appends, both readers True, all controls False, prefixes True |
| G6 red-proofs | PASS | control exit 0; (a)–(e) all exit 1 — five REDs, no green |
| G7 suite, lint, canary | PASS | exits 0/0/0/0; 43 passed; 15 passed; canary 42 passed |
| G8 structure and Open PR Gate | PASS | `packages/` holds one path; `docs/` and `apps/` empty |
| R-0722 | resolved | file ceiling + payload budget landed; registered and resolved this round |

## Next

Review this round at `327c1333..HEAD`, then order R14: the remaining half of `R-0721` —
`packages/orchestration/diff_view_source.py` still reads the artifact WHOLE with
`read_text` before the parser is called, so the INPUT is unbounded even though the OUTPUT
is now bounded in both dimensions. That half survives in prose only, in this handback and
in the plan's Next Steps, which is the slip SLIPR13 records; a round that resolves it
should also make the remainder visible to the open-set arithmetic. The round after that
carries the plan's claim that T002 and T003 are NOT blocked by the refused runner. Phase 1
rule 1 first: re-read `.agent/STOP` from disk before authoring.
