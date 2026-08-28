# Handback — F037 R4

## Session
SESSION 1 of feature F037 · round 4 · rounds so far 4

## Range
Review of 6dfd27d94374cc1a8940394279a1fee9afeaf549..f2929832e59d7394b90d8b7d7a152812a11f250d
(plus the C5 handoff commit that writes this file).
Branch: `feature/f037-rendered-diff-viewer`. Round base: `6dfd27d9`.

## Commits

### 2de561da chore(agent): save the F037 R4 block as authored
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r4.md | +339 / -0 | C0a — the block copied byte for byte from `.remedy-wt/f037-r4.md` with `shutil.copyfile` |

### 1d9f455d chore(agent): mirror the R4 block into the last-block slot
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +339 / -389 | C0b — same bytes as C0a; git stores both paths as ONE blob `437db60f492af15f9f9fcb2c093c1ee799541aa1`. `git diff --numstat` reports `234 / 284` for this rewrite because it pairs unchanged lines against the R3 block it replaces; the file's own line count is 339 |

### a7937795 docs(agent): point the plan at the F037 R4 repair round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +16 / -20 | C1 — byte-equal to slice `PLANF037R4`; 42 lines, under the 50-line rule |

### cd8eb75a docs(agent): book the F037 R3 verdict and register R-0716
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | C2 — EOF append of slice `RECORDR4`: the R3 gate paragraph and the `R-0716` finding. Baseline read with `git show a7937795:.agent/live_review.md` |

### b2fdbc4e fix(orchestration): collapse the doubled workspace diff header pair
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 / -0 | C3 — the single `Landed: R-0716` line constraint 6 orders, as the file's last line |
| packages/orchestration/diff_parser.py | +55 / -0 | C3 — `_region_is_redundant_header_echo` and `_collapse_doubled_header_regions`, applied at flush time before regions become files |
| tests/orchestration/test_diff_parser.py | +114 / -0 | C3 — the doubled-header regression test proved red first, the three-repeat case, and the same-path/different-headers guard |

### f2929832 feat(orchestration): add intraline spans to the diff view line shape
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/diff_parser.py | +138 / -1 | C4 — `DIFF_INTRALINE_MIN_RATIO`, the token regex, the offset/normalise/pair helpers and the per-hunk application; `DIFF_VIEW_VERSION` unchanged at 1 |
| tests/orchestration/test_diff_parser.py | +130 / -0 | C4 — exact-span word diff, the below-threshold pair, a `ctx` line, a surplus unpaired line, and the in-bounds property over every `*_DIFF` fixture |

### C5 docs(agent): hand back the F037 R4 round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self | C5 — this file; a handoff cannot table the commit that writes it (R-0149) |

## External actions

- `git worktree add --detach .remedy-wt/g6wt b2fdbc4e` — rc 0; the G6 unrepaired red-proof; removed, `git worktree list` back to 1 line.
- `git worktree add --detach .remedy-wt/g7base 6dfd27d9` — rc 0; base node-id inventory; removed.
- `git worktree add --detach .remedy-wt/g7mut f2929832` — rc 0; the G7 mutation red-proofs; removed, `git worktree prune` run.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — output verbatim `[]`. Open PR Gate passes; NOTHING merged, NO pull request created.
- INTENT after this commit: `git push origin feature/f037-rendered-diff-viewer`. Its outcome is reported in the round's completion report, not here — C5 is authored before the push exists.

## Verification

| Gate | Real exit code | Result |
|------|----------------|--------|
| G1 hygiene | 0 | HEAD before C0a `6dfd27d94374cc1a8940394279a1fee9afeaf549`, branch `feature/f037-rendered-diff-viewer`. `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4. `.agent/STOP` ABSENT before C0a and ABSENT before C5. |
| G2 transport | 0 | sha256 `8304eb095e810cedc7266eaf5bacc35d9053fecaae3b2c3a35946eee6076670f`, 28725 bytes, 339 lines — EQUAL at all four points (scratch, C0a, C0b, working copy at C4). C0a and C0b are ONE git blob `437db60f`. No line is a run of a single repeated character at length ≥ 4. The chain covers the scratch file, the saved copy, its mirror and the working copy, and says NOTHING about any prompt's bytes. |
| G3 extraction and caps | 0 | 2 slices printed: `PLANF037R4` 42 content lines, `RECORDR4` 3. CONTENT 45, TOTAL 339, PROSE = 339 − 45 = 294. PROSE ≤ 400 and TOTAL ≤ 490 both hold. |
| G4 the plan | 0 | `.agent/plan.md` at C1 byte-equal to `PLANF037R4` True; negative control against the slice minus its trailing newline False. `^## Goal$` 1, `^## Next Steps$` 1, `\bF\d{3}\b` matches `F037`, `wc -l` 42 < 50. |
| G5 the registration | 0 | Reader (a) reconstruction True with `1140801 + 1 + 5958 = 1146760` and the baseline a byte PREFIX. Reader (b): N = 2 blank-line units in the slice, last 2 units equal in order. Negative control at byte offset 1140842, inside the first appended paragraph — BOTH readers reject. Counts before → after: `^- R-\d+ — ` 276→277, `^Done: R-\d+ — ` 24→24, `^Landed: R-` 1→1, `^Gate: R\d+ — ` 19→19, `^Gate: F\d+ R\d+ — ` 73→74, all matching the reviewer's base reference. Finding ids ADDED `{R-0716}`; ids REMOVED, resolved ADDED and resolved REMOVED all EMPTY; all 277 ids DISTINCT; maximum id `R-0716`; open set 253. |
| G6 the repair's own red | 1 (unrepaired), 0 (repaired) | UNREPAIRED worktree run `python3 -B -m pytest tests/orchestration/test_diff_parser.py -q` → real exit 1, `2 failed, 17 passed in 0.24s`, failing node ids `tests/orchestration/test_diff_parser.py::test_parse_unified_diff_to_view_collapses_the_doubled_workspace_header` and `::test_parse_unified_diff_to_view_collapses_three_repeats_as_cleanly_as_two`. The unrepaired parser returned 2 files for the doubled-header input — matching the reviewer's measurement of 2 at `6dfd27d9` — the first with 0 hunks, `stats {added: 0, deleted: 0}` and `note` None. PRIMARY checkout at C3: real exit 0, `19 passed in 0.23s`. |
| G7 suite, lint, canary, mutations | 0 / 0 / 0, then 0 control, 1 and 0 mutated | Primary `python3 -m pytest tests/orchestration/test_diff_parser.py -q` → exit 0, `24 passed in 0.24s`, `^FAILED` count 0, extractor proved not blind (1 on a control string). Test count 24 at C4 against the 16 the reviewer measured at `6dfd27d9`; all 16 base node ids still present and re-run green — none missing. `python3 -m ruff check` over both paths, repository configuration, no `--isolated` → exit 0, `All checks passed!`. Canary `tests/cli/test_golden_path.py` → exit 0, `42 passed in 20.77s`. Mutation worktree: UNMUTATED CONTROL exit 0, `24 passed in 0.23s`. Mutation (a) `if matcher.ratio() < DIFF_INTRALINE_MIN_RATIO:` → `< -1.0:` in `packages/orchestration/diff_parser.py`, occurrence count 1 before the edit → exit 1, `1 failed, 23 passed`, `FAILED tests/orchestration/test_diff_parser.py::test_intraline_spans_are_empty_below_the_similarity_threshold`. Mutation (b) `if tag in ("replace", "delete"):` → `("replace", "insert")` in the same file, occurrence count 1 before the edit → exit 0, `24 passed`, NO FAILURE — reported plainly, cause under Deviations. Worktree removed and pruned; `git worktree list` 1 line, `git status --porcelain` 0 lines. |
| G8 structure, artifacts, PR gate | 0 | Path set of `git diff --name-only 6dfd27d9..f2929832` compared BOTH WAYS against the Change list minus `.agent/handoff.md`: both residues EMPTY. `git diff --stat` restricted — `apps/` EMPTY, `docs/` EMPTY, `packages/` only `packages/orchestration/diff_parser.py`, `tests/` only `tests/orchestration/test_diff_parser.py`. Insertions C0a 339, C0b 234, C1 16, C2 4, C3 171, C4 268 — each single-parent and under 500. `^<<<SLICE ` / `^<<<END ` are 0/0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2 and C3, against a CONTROL over the C0a blob reading 2/2. `.agent/live_review.md` at C4 ends with the `Landed: R-0716` line and `^Landed: R-` counts 2. `git ls-files .remedy-wt` 0 lines, `git branch --list "tmp/*"` 0 lines. `gh pr list --state open ...` → `[]`. |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it into `last_block` | done | |
| C1 the plan | done | |
| C2 the record — the R3 gate and the registration of `R-0716` | done | |
| C3 the `R-0716` repair with its regression test | done | red proved before the repair landed |
| C4 intraline spans with their tests | done | |
| C5 the handback | done | this file |
| push | done | ordered by G8 after C5; outcome in the completion report |
| S1 the shape | done | measured against `job_evidence._build_workspace_diff`, which appends the `a/`+`b/` pair itself and then hands the same pair to `difflib.unified_diff`; the unrepaired parser returned 2 entries for 1 path |
| S2 collapse at flush time | done | `_collapse_doubled_header_regions` folds a region into its SUCCESSOR on all six conditions; applied repeatedly, so three repeats collapse to one |
| S3 what the repair must not do | done | the comparison is on `(minus_header, plus_header)` and never on the resolved path; a `note`, a binary flag or a rename blocks the fold; order preserved |
| S4 regression test written first and proved red | done | G6: exit 1 on the unrepaired module with the doubled-header node id among the failures; plus the same-path/different-headers guard test |
| S5 the line shape gains one key | done | `intraline` on EVERY line entry, `[]` where nothing is marked; `DIFF_VIEW_VERSION` stays 1 with the one-sentence reason in the module docstring |
| S6 pairing then word diff | done | maximal `del` run immediately followed by a maximal `add` run, paired by position; `re.findall(r"\w+\|\W", s)` tokens with the rejoin identity checked before any offset arithmetic; `difflib.SequenceMatcher` opcodes mapped `replace`/`delete` → OLD, `replace`/`insert` → NEW |
| S7 the similarity guard | done | `DIFF_INTRALINE_MIN_RATIO = 0.3` exported; strictly below it both sides emit `[]` |
| S8 spans are normalised | done | clamped, zero-length dropped, touching/overlapping merged, sorted by `start`; the in-bounds property is asserted over every fixture in the file |
| S9 the tests for intraline | done | exact spans AND the sliced text on both sides, a below-threshold pair, a `ctx` line, a surplus unpaired line, and the corpus-wide in-bounds property |
| S10 nothing else changes | done | no existing test edited, weakened or deleted; all 16 base node ids present and passing |
| G1 … G8 | done | see the Verification table; G7 mutation (b) came back GREEN and is declared below |

## Authored-text proofs

Two slices applied, both extracted programmatically from the COMMITTED C0a blob
via `git show 2de561da:.agent/authored/f037-r4.md` and never retyped:

- `PLANF037R4` → `.agent/plan.md` at C1: byte-equal True; trailing-newline negative control False.
- `RECORDR4` → `.agent/live_review.md` at C2: EOF append, reconstruction `1140801 + 1 + 5958 = 1146760`, baseline a byte PREFIX, and the structural reader agreeing over the slice's 2 blank-line units.

The block itself: sha256 `8304eb095e810cedc7266eaf5bacc35d9053fecaae3b2c3a35946eee6076670f`
equal across the scratch file, `.agent/authored/f037-r4.md` at C0a, `.agent/last_block.md`
at C0b and the working copy at C4; the two committed paths are ONE git blob.

## Deviations & assumptions

1. **G7 mutation (b) produced NO failure, and the cause is that the ordered
   mutation is VACUOUS BY CONSTRUCTION rather than that an assertion is blind.**
   The order was to swap `insert` for `delete` in the OLD side's opcode test.
   `difflib.SequenceMatcher.get_opcodes()` emits every `insert` opcode with
   `i1 == i2` by definition, so the old-side span such an opcode yields is always
   zero length and is dropped by S8's normalisation. No corpus — this one or any
   other — could turn that mutation red. Measured, not inferred: for the pure
   insertion `the fox` → `the quick fox` the opcodes are
   `[('equal', 0, 2, 0, 2), ('insert', 2, 2, 2, 4), ('equal', 2, 3, 4, 5)]`.
   Reported plainly as the block orders; no substitute mutation was run in its
   place.
2. **A residual blind spot, measured while diagnosing (1) and named so the next
   round can order a fix.** Across every `*_DIFF` fixture in
   `tests/orchestration/test_diff_parser.py`, the paired del/add lines that clear
   the ratio guard produce only `equal` (6) and `replace` (4) opcodes — no
   `delete` and no `insert`. S6's side mapping is therefore pinned only for the
   `replace` case: deleting `"delete"` from the OLD side's tuple would leave the
   suite green. Not repaired here, because S9 enumerates the intraline tests and
   a fixture producing a bare `delete` opcode is not among them, and reaching for
   extra surface mid-round is what the single-writer split exists to prevent.
3. **`git diff --numstat` for C0b reads `234 / 284`, not `339 / 389`.** The
   `.agent/last_block.md` rewrite pairs unchanged lines against the R3 block it
   replaces, so numstat's insertion count is lower than the file's 339 lines. The
   commit table above carries the numstat figure in the Reason column and the
   file's real size beside it, so the two readings cannot be confused.
4. **The `Landed: R-0716` line names its commit as "commit C3 of F037 R4" rather
   than by SHA.** The line is written INTO C3, so C3's SHA does not exist when
   the text is authored; naming it any other way would be an invented value.
5. No SPEC item was impossible to implement as written. Assumption recorded: the
   `_intraline_spans_for_pair` rejoin check (`"".join(tokens) == content`) is an
   addition to S6, kept because S6 makes that identity "the property that makes
   the offsets sound" — the check makes the parser refuse rather than emit an
   unsound offset if it ever stops holding. It never fires for `r"\w+|\W"`.
6. No commit was made beyond the ordered sequence C0a, C0b, C1, C2, C3, C4, C5,
   and none was dropped or reordered.

## Open findings

253 open after this round: 277 registered, 24 resolved. `R-0715` untouched and
still OPEN; `R-0716` registered at C2, repaired at C3 and NOT resolved — only
reviewer-authored `Done:` text closes it.

## Next

Reviewer re-runs G1 through G8 at `f2929832` and rules on the round; the next
worker round is the read endpoint, keyed on task run and job per DECISION F037 D2.
