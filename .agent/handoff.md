# Handback — F037 R3

## Session
SESSION 1 of feature F037 · round 3 · rounds so far 3

## Range
Review of 09cbe24c2723b2aacb62e355fe5e03f9c8e46fe7..b8b832d3730a3bad51cd4cd3f6073b9f243a0b70
(plus the C5 handoff commit that writes this file).
Branch: `feature/f037-rendered-diff-viewer`. Round base: `09cbe24c`.

## Commits

### 69fb2d2f chore(agent): save the F037 R3 block as authored
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r3.md | +389 / -0 | C0a — the block copied byte for byte from `.remedy-wt/f037-r3.md` with `shutil.copyfile` |

### 40f9cf74 chore(agent): mirror the R3 block into the last-block slot
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +318 / -345 | C0b — mirror of the committed C0a blob; same git blob `b26bbb83` |

### 685611a2 docs(agent): point the plan at the F037 parser round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +21 / -19 | C1 — byte-equal to slice PLANF037R3 |

### ea7a3a67 docs(agent): book the R2 verdict and the authoring slip
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 / -0 | C2 — EOF append of slice RECORDR3 onto the C1 baseline |
| .agent/prose_slips.md | +13 / -0 | C2 — EOF append of slice SLIPR3 onto the C1 baseline |

### ba4e6f32 feat(orchestration): add the F037 unified-diff view parser
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/diff_parser.py | +420 / -0 | C3 — the parser, implemented from SPEC S1–S11; stdlib only |

### b8b832d3 test(orchestration): pin the F037 diff-parser corpus
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_diff_parser.py | +393 / -0 | C4 — the corpus, implemented from SPEC S12–S15 |

### C5 docs(agent): hand back F037 R3
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self | C5 — a handoff cannot table the commit that writes it (R-0149) |

## External actions
- `git worktree add .remedy-wt/g7 b8b832d3 --detach` — added for G7. Outcome: created at detached `b8b832d3`.
- `git worktree remove --force .remedy-wt/g7` then `git worktree prune` — outcome: `git worktree list` back to 1 line, primary `git status --porcelain` 0 lines.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, stdout `[]`. Nothing merged, nothing created.
- INTENT after C5: `git push origin feature/f037-rendered-diff-viewer`. Its outcome cannot be a value of this file — C5 is authored before the push exists — so it is reported in the round's completion report instead.
- No PR created. Nothing merged. No `npm`/`npx`/`node`/`vite` run.

## Verification

- **G1** exit 0. `git rev-parse HEAD` before C0a = `09cbe24c2723b2aacb62e355fe5e03f9c8e46fe7`; `git branch --show-current` = `feature/f037-rendered-diff-viewer`. `git status --porcelain` line count after C0a/C0b/C1/C2/C3/C4 = 0/0/0/0/0/0. `.agent/STOP` read from disk before C0a: ABSENT (`ls` exit 2, "No such file or directory"); read again before C5: ABSENT.
- **G2** exit 0. sha256 `e5bd63a70b28652d86c6f76eaebd16fc0da95f11ddb46d9c7758d4607721f61a`, 30544 bytes, 389 lines — identical at all FOUR points: the scratch `.remedy-wt/f037-r3.md`, the C0a blob, the C0b blob and the working copy read off disk at C4. ALL FOUR EQUAL: True. C0a and C0b are the SAME git blob, `b26bbb839cc26ef523c328f974d741e678310b7a`. Lines that are a run of one repeated character at length ≥ 4: 0. What this proof covers: the scratch file, the saved copy, its mirror and the working copy — and NOT the bytes of any prompt.
- **G3** exit 0. Extractor printed 3 slices from the committed C0a blob by marker lines: PLANF037R3 46 content lines, RECORDR3 1, SLIPR3 12. CONTENT 59, TOTAL 389, PROSE = 389 − 59 = 330. PROSE ≤ 400 True; TOTAL ≤ 490 True.
- **G4** exit 0. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF037R3 (2357 bytes both sides). Negative control against the slice MINUS its trailing newline: FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `\bF\d{3}\b` matched `F037`, `wc -l` 46 (strictly under 50).
- **G5** exit 0. Both appends built by the constraint-3 operation with baselines read from C1 (`685611a2`).
  - `.agent/live_review.md` — reader (a): 1136389 + 1 + 4411 = 1140801, file at C2 = 1140801, BYTE-EQUAL True, baseline is a byte PREFIX True. Reader (b): N = 1 blank-line unit counted from the slice by the script; the LAST 1 unit of the file equals the slice's unit in order: True. Negative control: byte flipped at offset 1136395, inside the FIRST appended paragraph `[1136390, 1140801)` (`' '` → `'!'`) — reader (a) rejects True, reader (b) rejects True.
  - `.agent/prose_slips.md` — reader (a): 5070 + 1 + 922 = 5993, file at C2 = 5993, BYTE-EQUAL True, PREFIX True. Reader (b): N = 1, last 1 unit equals the slice in order True. Negative control: byte flipped at offset 5076, inside `[5071, 5993)` (`'6'` → `'7'`) — both readers reject True.
  - Line-anchored counts in `.agent/live_review.md`, before C2 → after C2: `^- R-\d+ — ` 276 → 276; `^Done: R-\d+ — ` 24 → 24; `^Landed: R-` 1 → 1; `^Gate: R\d+ — ` 19 → 19; `^Gate: F\d+ R\d+ — ` 72 → 73. All five match the block's ordered readings.
  - Finding ids ADDED `[]`, REMOVED `[]`; resolved ids ADDED `[]`, REMOVED `[]` — all four EMPTY. Maximum id `R-0715` at both points. Open set 252 at both points. `R-0715` still ends with the word `OPEN.` at both points.
- **G6** all three commands exit 0, at C4, from the repository root.
  - `python3 -m pytest tests/orchestration/test_diff_parser.py -q` — REAL exit 0, summary VERBATIM `16 passed in 0.22s`, `^FAILED` count 0. Extractor blindness proof: the same `^FAILED` regex over a control string holding two such lines reports 2, so it is not blind.
  - `python3 -m ruff check packages/orchestration/diff_parser.py tests/orchestration/test_diff_parser.py` — REAL exit 0, stdout VERBATIM `All checks passed!`, stderr empty. Repository configuration, no `--isolated`, no `--line-length`. Both paths are added by this branch, so no baseline reading at an earlier commit exists.
  - Canary `python3 -m pytest tests/cli/test_golden_path.py -q` — REAL exit 0, summary VERBATIM `42 passed in 22.13s`.
- **G7** exit 0 for the control, exit 1 for each of the three mutations. All of it inside the disposable worktree `.remedy-wt/g7` at detached `b8b832d3`; the primary checkout was never mutated. Every mutation was applied in `packages/orchestration/diff_parser.py` INSIDE that worktree, `__pycache__` purged and `python3 -B` used each time, the file restored between mutations.
  - UNMUTATED CONTROL: `python3 -B -m pytest tests/orchestration/test_diff_parser.py -q`, REAL exit 0, `16 passed in 0.26s`, `^FAILED` 0.
  - (a) old-side counter never advances — replaced text `                    old_ln += 1\n`, occurrences before the edit 1. REAL exit 1, `5 failed, 11 passed in 0.25s`, `^FAILED` 5: `test_parse_unified_diff_to_view_reads_a_deletion`, `test_parse_unified_diff_to_view_seeds_each_hunk_from_its_own_header`, `test_parse_unified_diff_to_view_numbers_both_sides_of_every_line`, `test_parse_unified_diff_to_view_drops_the_no_newline_marker`, `test_parse_unified_diff_to_view_reads_real_difflib_output`. S13's full-tuple node is among them, as ordered.
  - (b) `[binary file]` literal made unreachable — replaced text `DIFF_BINARY_SENTINEL = "[binary file]"`, occurrences before the edit 1. REAL exit 1, `1 failed, 15 passed in 0.23s`, `^FAILED` 1: `test_parse_unified_diff_to_view_reads_the_binary_sentinel`. S12's binary node, as ordered.
  - (c) `stats["deleted"]` forced to 0 — replaced text `"deleted": deleted`, occurrences before the edit 1. REAL exit 1, `4 failed, 12 passed in 0.24s`, `^FAILED` 4: `test_parse_unified_diff_to_view_reads_a_plain_modification`, `test_parse_unified_diff_to_view_reads_a_deletion`, `test_parse_unified_diff_to_view_reads_a_git_rename_and_keeps_the_old_path`, `test_every_file_stats_equal_a_recount_of_its_own_parsed_lines`. S14's stats-property node is among them, as ordered.
  - After removal and prune: `git worktree list` 1 line, primary `git status --porcelain` 0 lines.
- **G8** exit 0 on every command. Path set of `git diff --name-only 09cbe24c..b8b832d3` compared BOTH WAYS against the Change list minus `.agent/handoff.md`: residue actual−expected `[]`, residue expected−actual `[]`. `git diff --stat 09cbe24c..b8b832d3` restricted by area: `apps/` EMPTY, `docs/` EMPTY, `packages/` holds ONLY `packages/orchestration/diff_parser.py` (+420), `tests/` holds ONLY `tests/orchestration/test_diff_parser.py` (+393). Per-commit insertions from `git diff --numstat`, each single-parent and under 500: C0a 389, C0b 318, C1 21, C2 15, C3 420, C4 393. Line-anchored `^<<<SLICE ` / `^<<<END `: `.agent/plan.md` at C1 0/0, `.agent/live_review.md` at C2 0/0, `.agent/prose_slips.md` at C2 0/0, against the CONTROL over the C0a blob which reads 3/3. `git ls-files .remedy-wt` 0 lines; `git branch --list "tmp/*"` 0 lines. Open PR Gate VERBATIM: `[]` at exit 0 — nothing merged, nothing created.

## Authored-text proofs

Three reviewer-authored slices applied, every one of them extracted programmatically
from the COMMITTED C0a blob (`git show 69fb2d2f:.agent/authored/f037-r3.md`) by its
marker LINES and applied from there in Python. None was retyped.

| Slice | Target | Result |
|-------|--------|--------|
| PLANF037R3 | `.agent/plan.md` at C1 | BYTE-EQUAL, 2357 = 2357; negative control (slice minus trailing newline) FALSE |
| RECORDR3 | `.agent/live_review.md` at C2 | reconstruction 1136389 + 1 + 4411 = 1140801 BYTE-EQUAL, baseline a PREFIX; structure reader last-1-unit equal; both negative controls reject |
| SLIPR3 | `.agent/prose_slips.md` at C2 | reconstruction 5070 + 1 + 922 = 5993 BYTE-EQUAL, baseline a PREFIX; structure reader last-1-unit equal; both negative controls reject |

The block asserts no digest of its own; the four-point equality under G2 is the
transport proof, and the reviewer holds the scratch value.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror into last_block | done | |
| C1 the plan | done | |
| C2 the record | done | |
| C3 the parser module | done | |
| C4 the corpus tests | done | |
| C5 the handback | done | this commit |
| push | done | ordered by G8 after C5; outcome reported in the round report, not here |
| S1 module header / three shapes / A1 absence | done | docstring names shapes (a) difflib, (b) git hunks, (c) `--- /dev/null` untracked markers, with their producers, and the deliberate absence of `review_subject.py`'s vocabulary pointing at amendment A1 |
| S2 public names | done | `DIFF_VIEW_VERSION`, the five `DIFF_STATUS_*`, `DIFF_VIEW_STATUSES`, `parse_unified_diff_to_view(diff_text: str) -> dict` |
| S3 return shape | done | shape as specified; the `stats {+,-}` shorthand and the `truncated`/`note` additions are stated in the docstring |
| S4 file splitting | deviated | implemented AS WRITTEN; see Deviations D1 — the real `workspace.diff` shape emits its header pair twice and therefore yields one extra empty file entry |
| S5 status derivation | done | order renamed → binary → added → deleted → modified; a hunkless file with no other signal is `modified` |
| S6 hunk headers | done | both sides captured, absent count = 1, header kept VERBATIM incl. section heading; a non-matching `@@` line is recorded as a `note` rather than treated as a hunk |
| S7 line numbering | done | two counters seeded from the header's two starts; `\ No newline` dropped |
| S8 sentinels | done | `[binary file]`, `[unsafe staged artifact skipped:`, `[DIFF TRUNCATED]`, `#` comments; see Deviations D2 for `[FOCUSED DIFF TRUNCATED]` |
| S9 provisional hunk ids | done | `f"{file_index}:{hunk_index}"`; the F033 note and the `DIFF_VIEW_VERSION` seam are in the docstring |
| S10 stats | done | counted from the parsed entries only |
| S11 empty and malformed | done | both return the empty-files shape; nothing raises |
| S12 one test per shape | done | 9 ordered shapes plus a real-`difflib` generator test |
| S13 both-sided full-tuple test | done | `test_parse_unified_diff_to_view_numbers_both_sides_of_every_line`; red-proof (a) confirms it fails when the old side stops advancing |
| S14 further pins | done | statuses frozenset, truncated flag, `\ No newline`, and the stats-recount PROPERTY over the whole corpus |
| S15 nothing else touched | done | the only two `packages/`/`tests/` paths in the range are the two new files |

## Deviations & assumptions

**D1 — the real `workspace.diff` shape disagrees with S4, and S4 was followed as
written.** `packages/orchestration/job_evidence.py` writes `--- a/<rel>` and
`+++ b/<rel>` itself (lines 1212–1213) and then appends the output of
`difflib.unified_diff(..., fromfile="a/<rel>", tofile="b/<rel>")` (lines 1242–1251),
which carries the SAME header pair again. S4 says a `--- ` line outside a hunk body
starts a new file entry, so that shape parses to TWO file entries for one file: a
first with the right path, no hunks, no note, status `modified`, and a second
carrying the actual hunks. Measured on a reconstruction of that emitter, not
reasoned about. I implemented S4 exactly as written and did NOT add a
same-path merge rule, because the block orders the contradiction declared rather
than silently corrected. The fix, if the reviewer wants one, is one condition:
reuse the current region when it is hunkless, note-less and its `+++` path equals
the incoming pair's. No test pins the duplicate behaviour either way, so a repair
next round breaks nothing.

**D2 — `[FOCUSED DIFF TRUNCATED]` exists and S8 does not name it.**
`pingpong_loop.py` line 1365 appends `[FOCUSED DIFF TRUNCATED]` on the
reviewer-scoped path, alongside the `[DIFF TRUNCATED]` of lines 1378 and 1813. S8
orders the stripped form `[DIFF TRUNCATED]` and only that, so the focused variant
does NOT set `truncated`; it falls through to the unrecognized-line branch and is
dropped. Implemented as ordered. Widening the sentinel to a prefix or to both
literals is a one-line change for a later round.

**D3 — the parser trusts the hunk header's declared counts to bound the body.** S6
orders both counts captured and S7 orders the body walked; it does not say how the
body ends. Ending it on "the first line that is not ` `/`+`/`-`" is wrong for this
repository, because a deleted line reading `-- foo` arrives as `--- foo` and a
`rstrip`-ed blank context line arrives as the empty string, both of which are
indistinguishable from structure by shape alone. Counting down from the header's
declared counts resolves both. Consequence to be aware of: after `[DIFF TRUNCATED]`
the counts are meaningless by construction, which is why the truncation sentinel is
tested BEFORE the body and closes the file cleanly.

**D4 — `note` is first-come, with two forced exceptions.** S8 gives four different
things that can set `note` and does not order a precedence. A file region keeps the
FIRST marker it sees, because every producer in this repository puts the marker
immediately after the file's own header; `[binary file]` and
`[unsafe staged artifact skipped:` overwrite it, because S8 states outright what
each of those two sets `note` to.

**D5 — `parse_unified_diff_to_view` also tolerates a non-`str` argument**, returning
the empty-files shape rather than raising. The signature is `str` as S2 orders; this
is constraint 8's totality carried one step further, and it is three lines.

**D6 — no departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4,
C5 were made in that order and nothing else was committed. No extra commit, none
dropped, none reordered.

**D7 — one scratch artifact note.** The G7 worktree and the gate scripts live under
the gitignored `.remedy-wt/`; `git ls-files .remedy-wt` reads 0 lines, and the
worktree itself was removed and pruned before this commit.

## Next

Reviewer rules on D1 and D2 — whether the duplicated `workspace.diff` header pair
gets a same-path merge rule and whether `[FOCUSED DIFF TRUNCATED]` joins the
truncation sentinel — and then orders R4: the intraline spans over the parsed
lines, with the word-diff fixture the feature file's Acceptance names.

Open findings after this round: 252.
