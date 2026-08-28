# Handoff — F037 Rendered diff viewer, round 21

## Session

SESSION 6 of feature F037 · round 21 · rounds so far 21.

Round 21 of the 25-round soft limit and session 6 of 7 — approaching both, past
neither, so no scope report is owed yet. Two named pieces remain after this
round: the lazy language bundles, and the 10k-line perf fixture measured END TO
END. If both do not fit in session 7, that session owes the scope report.

## Range

Review of `6d13fae4..HEAD`.

## Commits

### c2878dc1 chore(agent): save the F037 R21 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r21.md` | +490/-0 | C0a, the block saved byte for byte |

### c475172a chore(agent): mirror the F037 R21 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +435/-320 | C0b, the same bytes at the mirror path |

### 68d29e36 docs(agent): set the plan to F037 R21
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +25/-24 | C1, full rewrite from the PLANF037R21 slice |

### cebca097 docs(review): record the F037 R20 verdict and its two resolutions
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +14/-0 | C2, GATER20 + DONE727 + DONE728 appended in Bundle order |
| `.agent/prose_slips.md` | +9/-0 | C2, PROSESLIP appended; append-only, nothing renumbered |

### f2b96d03 docs(agent): record DECISION F037 D10 on typescript red-proofs
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +37/-0 | C3, DECISIOND10 appended |

### 28238993 docs(ui): repair the five stale mount claims
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | S6, the one `Landed: R-0727` line, same commit as C4 |
| `apps/ui/src/api/diffViewModel.ts` | +5/-4 | C4 site 5, the threshold comment put in the present tense |
| `tests/ui_contracts/test_diff_viewer_mount.py` | +15/-13 | C4 sites 1-4, comment and message text only |

### 7d7c1fd0 feat(ui): turn a scrolled viewport into a diff row window
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffViewModel.test.ts` | +149/-0 | C5, SPEC S3, the new `diffRowWindowForViewport` describe |
| `apps/ui/src/api/diffViewModel.ts` | +109/-0 | C5, SPEC S2, three constants, one interface, one function |

### ff85e39f feat(ui): draw only the diff rows a viewport can hold
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/diff/DiffView.tsx` | +72/-6 | C6, SPEC S4, the wiring |

### 835ba84b test(ui-contracts): pin that the diff viewer really draws a window
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_diff_view_render.py` | +245/-5 | C7, SPEC S5, the guards over the wiring |

### C8 — this handoff (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C8, the handback; a handoff cannot table the commit that writes it |

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f037-r21-redproof HEAD`
  — created at `835ba84b` for G6.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f037-r21-redproof`
  — removed by exact path; `git worktree list` afterwards is one line:
  `/home/decodeux/Repos/remedy  835ba84b [feature/f037-rendered-diff-viewer]`.
  Reported BEFORE any pytest gate ran in the primary checkout.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
  No PR created, nothing merged, no history rewritten, no force push.
- `git push -u origin feature/f037-rendered-diff-viewer` after C8.
- Artifact builds (evidence bundle, review zip): NONE attempted this round.

## Verification

One line per gate, real exit codes, no summarized "green".

- **G1 HYGIENE** — exit 0. `.agent/STOP` absent read from disk before C0a and
  again before C8 (`ls` exit 2, "No such file or directory" both times).
  `git rev-parse HEAD` before C0a = `6d13fae4f35dbb24a42ff983d29e8f33d6b2487b`
  = BASE. Branch `feature/f037-rendered-diff-viewer`.
  `git status --porcelain | wc -l` = 0 after every one of the nine commits.
- **G2 TRANSPORT** — exit 0. Committed C0a blob: 38781 bytes, 490 lines, sha256
  `212f83b8a43a0bfe07fb1e5b2f55fa1142a5e7b9bece95c3eb02b26d207f7252` (identical
  to `.remedy-wt/f037-r21-block.md` on disk). At C0b
  `git rev-parse c475172a:.agent/authored/f037-r21.md` and
  `c475172a:.agent/last_block.md` are ONE blob `3d1f37a3e7b5df7b13f0646c7213da951f67217e`.
- **G3 THE PLAN AT C1** — exit 0. PLANF037R21 extracted from the COMMITTED C0a
  blob vs `git show 68d29e36:.agent/plan.md`: byte equality True, including the
  trailing newline. Negative control (slice minus trailing newline): False.
  `wc -l` 48, strictly under 50: True. Lines exactly `## Goal`: 1. Lines exactly
  `## Next Steps`: 1.
- **G4 THE RECORD AT C2 AND C3** — exit 0. `live_review.md`: pre-round blob +
  one newline before each of GATER20, DONE727, DONE728 in Bundle order == C2
  blob: True; negative control (one byte flipped inside GATER20's FIRST
  paragraph): False; pre-round blob is a byte PREFIX: True, 1265615 → 1277380.
  `prose_slips.md`: reader True, negative control False, prefix True,
  12164 → 12776, `^- 2026-` 19 → 20 (rose by exactly one; nothing rewritten or
  renumbered). `decisions.md`: reader True, negative control False, prefix True,
  682310 → 684609, `^## DECISION ` 175 → 176, `F037 D10` 0 → 1 (exactly once).
- **G5 THE LEDGER** — exit 0, line-anchored over the C2 blob, base figures from
  `6d13fae4` (identical to the block's `b2658466` figures):
  `^- R-\d+ — ` 289 → 289; `^Done: R-\d+ — ` 37 → 39; `^Landed: R-` 6 → 6;
  `^Gate: F\d+ R\d+ — ` 90 → 91. Every registered id DISTINCT (289 of 289) at
  base and at C2. OPEN SET computed AS A SET (registered minus ids named by a
  `Done:` line): 254 → 252 — a fall of exactly two, `R-0727` and `R-0728`. No
  figure disagreed with the block.
- **G6 THE RED-PROOFS** — all six RED, exit 1 each. Disposable worktree at the
  C7 tree (`835ba84b`), `__pycache__` purged before every python run, `python3
  -B` throughout, each replaced string counted at exactly 1 BEFORE its edit,
  every file restored to its pre-mutation sha256 after every run (restore
  verified True each time). TypeScript driven per constraint 9 / DECISION F037
  D10: `npx vitest run --root <WT>/apps/ui --config <PRIMARY>/apps/ui/vitest.config.ts
  src/api/diffViewModel.test.ts --reporter=basic`, `cwd=<PRIMARY>/apps/ui`,
  spawned from a `python3` script under `.remedy-wt/`.
  - UNMUTATED CONTROL FIRST: vitest exit 0, 69 passed (1 file); pytest exit 0,
    19 passed.
  - (a) unmeasured-viewport fallback removed → exit 1, 2 failed | 67 passed,
    killing `answers an UNMEASURED viewport with a NON-EMPTY window` and
    `resolves a hostile VIEWPORT HEIGHT through the unmeasured fallback`.
    Restore True, sha256 `711cd58bc6e7fe45…`.
  - (b1) scroll division `Math.floor` → `Math.ceil` → exit 1, 1 failed | 68
    passed, killing `takes the first visible row as the FLOOR of the scroll
    division`. Restore True.
  - (b2) height division `Math.ceil` → `Math.floor` → exit 1, 1 failed | 68
    passed, killing `takes the visible count as the CEILING of the height
    division`. Restore True.
  - (c) `rowsAfterPx` returned as 0 → exit 1, 2 failed | 67 passed, killing
    `sizes both spacers as their row count times the row height` and `draws a
    BOUNDED window of a ten-thousand-row diff and accounts for all of it`.
    Restore True.
  - (d) `diffRowWindowForViewport` call in `DiffView.tsx` replaced by a direct
    `computeDiffRowWindow` call doing the division in the component → pytest
    exit 1, 3 failed 16 passed, killing the NEW delegation guard
    `TestTheComponentReallyVirtualizes::test_the_component_asks_the_model_for_a_window`
    plus `test_the_component_calls_every_rule_it_must_not_carry` and
    `test_the_component_reimplements_no_rule_of_the_model`. Restore True.
  - (e) `DIFF_VIRTUAL_ROW_HEIGHT_PX` 20 → 24 → pytest exit 1, 1 failed 18
    passed, killing exactly
    `TestTheComponentReallyVirtualizes::test_the_row_height_agrees_with_the_stylesheets_own_line_box`
    — the discriminator proving that test really parses the stylesheet.
    Restore True.
  - UNMUTATED CONTROL LAST: vitest exit 0, 69 passed; pytest exit 0, 19 passed.
    Worktree `git status --porcelain` empty at the end.
- **G7 SUITES, TYPES AND LINT AT C7** — primary checkout, ONE pytest process at
  a time, worktree already removed and `git worktree list` reported above as one
  line. Base figures in brackets.
  - `python3 -m pytest tests/ui_contracts/ -q` → exit 0, **648 passed, 4
    skipped** in 5.88s [642 passed, 4 skipped] — +6 from C7's new class.
  - `python3 -m pytest tests/ui_server/ -q` → exit 0, **495 passed** in 33.00s
    [495 passed].
  - `python3 -m pytest tests/orchestration/test_test_runner.py tests/docs/ -q`
    → exit 0, **347 passed** in 5.73s [347 passed].
  - `python3 -m ruff check tests/ui_contracts/test_diff_view_render.py
    tests/ui_contracts/test_diff_viewer_mount.py` → exit 0, `All checks passed!`.
  - `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k "typescript
    or tsc or noEmit" -q -rs` → exit 0, **1 passed, 73 deselected** in 2.15s
    [1 passed, 73 deselected]. PASSED, not skipped: no `s` in the progress line
    and `-rs` printed no skip reason. `tsc --noEmit` was not red at any point.
  - `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, **42 passed**
    in 22.38s [42 passed].
  - vitest TOTAL, driven per DECISION F037 D10 with `--reporter=verbose` against
    the PRIMARY tree → exit 0, **32 test files passed, 592 tests passed**
    [32 files, 584 tests] — +8, the new `describe`'s eight cases, each printed
    as executed and green: `answers an UNMEASURED viewport with a NON-EMPTY
    window`, `does not virtualize below the threshold: no spacers, every row
    drawn`, `takes the first visible row as the FLOOR of the scroll division`,
    `takes the visible count as the CEILING of the height division`, `sizes both
    spacers as their row count times the row height`, `resolves a hostile SCROLL
    OFFSET to the top rather than propagating it`, `resolves a hostile VIEWPORT
    HEIGHT through the unmeasured fallback`, `draws a BOUNDED window of a
    ten-thousand-row diff and accounts for all of it`.
- **G8 STRUCTURE AND THE OPEN PR GATE AT C7** — exit 0.
  `git diff --name-only 6d13fae4..835ba84b` vs the Change set minus
  `.agent/handoff.md`: ACTUAL MINUS EXPECTED empty, EXPECTED MINUS ACTUAL empty
  (11 paths both ways). `git diff --stat` restricted to `packages/` is EMPTY;
  restricted to `apps/ui/src/components/` it names `DiffView.tsx` alone, 72
  insertions and 6 deletions. Per-commit insertions from `git show --numstat`,
  in order: 490, 435, 25, 23, 37, 22, 258, 72, 245 — every one under 500, every
  one single-parent, every one matching the `+/-` column of the tables above
  cell by cell. Lines matching `^<<<SLICE ` or `^<<<END ` are **0** in all nine
  edited targets, with the C0a blob and its C0b mirror as the NON-ZERO controls
  at **12** each. `git ls-files .remedy-wt | wc -l` = 0.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the COMMITTED C0a blob
(`git show HEAD:.agent/authored/f037-r21.md`), never retyped, and applied byte
for byte. Disk-to-disk comparisons, all against committed blobs:

- C0a vs `.remedy-wt/f037-r21-block.md`: 38781 bytes / 490 lines / sha256
  `212f83b8…7252` on both sides. Pre-flight check of all three passed before any
  commit.
- PLANF037R21 vs `68d29e36:.agent/plan.md` — byte equal (G3), negative control
  False.
- GATER20 + DONE727 + DONE728 vs `cebca097:.agent/live_review.md` — byte equal
  under the Bundle-order reader (G4), negative control False.
- PROSESLIP vs `cebca097:.agent/prose_slips.md` — byte equal, negative control
  False. Applied verbatim; the slice's two-space continuation indent and blank
  separator were NOT re-wrapped.
- DECISIOND10 vs `f2b96d03:.agent/decisions.md` — byte equal, negative control
  False.

## Deviations & assumptions

1. **DEVIATION — one comment outside SPEC S1 was repaired, in C6.** The header
   of `DiffView.tsx` read "the T003 pieces still outstanding — the virtual
   scrolling and the lazy language bundles — arrive at this component". C6 lands
   the virtual scrolling, so that sentence would have been falsified by the very
   commit that carried it. Constraint 11 orders OTHER stale claims reported and
   left alone; I read that as binding on claims already stale at the sweep, not
   on a sentence this round's own code makes false, and repairing a false
   comment I would otherwise be shipping is the same defect `R-0727` records.
   The repair is two lines and names no round. Every other stale claim found is
   reported below and left untouched.
2. **ASSUMPTION — the `Landed:` line names its commit by ROLE, not by SHA.**
   SPEC S6 asks it to name "the commit that repaired them", and that commit's
   SHA cannot exist while the line is being written into the same commit. It
   therefore reads "landed by C4 of F037 R21", which is the form every other
   `Landed:` line in the record already uses (`R-0725`, `R-0726`, `R-0727`,
   `R-0728` all name `C<n> of F037 R<r>`).
3. **NO OTHER DEPARTURE FROM THE ORDERED COMMIT SEQUENCE.** The nine commits are
   C0a, C0b, C1, C2, C3, C4, C5, C6, C7 in exactly that order, plus C8 for this
   handback. Nothing added, nothing dropped, nothing reordered. C5 precedes C6
   and C7 follows C6, as constraints 6 and 7 require; `tsc --noEmit` was run at
   C6 and again at C7 and was green at both.
4. **ASSUMPTION — the `Landed:` line rides in C4.** SPEC S6 says "In the SAME
   commit as C4", so `28238993` carries both the five staleness repairs and that
   one line. G5's ledger figures are measured at the C2 blob, where the
   `Landed:` count is still 6, so the two do not conflict.
5. **G5 base figures were re-measured at `6d13fae4`, not taken from the block.**
   They agreed with the block's `b2658466` figures exactly (289 / 37 / 6 / 90 /
   254), so no adjustment was needed and none was made.
6. `.remedy-wt/r21/` holds this round's scratch scripts (slice extractor, the
   three gate readers, the vitest driver, the red-proof driver). `.remedy-wt/`
   is gitignored and `git ls-files .remedy-wt` is 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f037-r21.md` | done | `c2878dc1` |
| C0b mirror it into `.agent/last_block.md` | done | `c475172a`, one blob with C0a |
| C1 rewrite `.agent/plan.md` from PLANF037R21 | done | `68d29e36` |
| C2 append GATER20 + DONE727 + DONE728 and PROSESLIP | done | `cebca097`, one commit |
| C3 append DECISIOND10 to `.agent/decisions.md` | done | `f2b96d03` |
| C4 the staleness repairs (SPEC S1) + the S6 `Landed:` line | deviated | `28238993`; one comment beyond S1's five was repaired in C6 — deviation 1 |
| C5 the viewport rule and its vitest tests (S2, S3) | done | `7d7c1fd0`, before its caller |
| C6 the wiring (S4) | done | `ff85e39f`, after C5 |
| C7 the guards over the wiring (S5) | done | `835ba84b`, after C6 |
| C8 rewrite `.agent/handoff.md` | done | this commit |
| G1 HYGIENE | done | STOP absent twice, HEAD = BASE, branch correct, porcelain 0 after all nine commits |
| G2 TRANSPORT | done | 38781 bytes / 490 lines / sha256 `212f83b8…7252`; one blob `3d1f37a3` |
| G3 THE PLAN AT C1 | done | byte equal True, negative control False, 48 lines, 1 + 1 headings |
| G4 THE RECORD AT C2 AND C3 | done | three readers True, three negative controls False, three prefixes True |
| G5 THE LEDGER | done | 289 / 39 / 6 / 91, all ids distinct, open set 254 → 252 |
| G6 THE RED-PROOFS | done | six runs, all exit 1; controls exit 0 first and last; all restores True |
| G7 SUITES, TYPES AND LINT AT C7 | done | 648+4s / 495 / 347 / ruff clean / 1 passed 73 deselected / 42 / 32 files 592 tests |
| G8 STRUCTURE AND THE OPEN PR GATE | done | both residues empty, markers 0 vs 12 control, `.remedy-wt` 0 files, `gh pr list` `[]` |

## Staleness sweep (constraint 11)

Every WHY comment in each edited file was re-read. The five sites SPEC S1 names
were repaired in C4. What else was found, REPORTED AND LEFT ALONE:

1. `apps/ui/src/api/diffViewModel.ts`, the `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS`
   comment: "Every other site — the function below, **the component that will
   consume it**, and the vitest suite — names this constant". Same future tense
   as S1's site 5, one constant further down, and not in S1's list of five. The
   component now consumes the threshold indirectly through
   `diffRowWindowForViewport`; it still never names the constant, so the clause
   is arguable rather than plainly false. Left byte-identical.
2. `apps/ui/src/api/diffViewModel.ts`, the `computeDiffRowWindow` header:
   "the caller does the one division it owns (scroll offset by row height) …
   **That division is the only untestable part of virtual scrolling**". The
   first half is still exactly true — `diffRowWindowForViewport` is that caller
   and does that division. The second half stopped being true at C5: the
   division moved into this module and vitest now executes it, so the only
   untestable part left is the DOM read of `scrollTop` and `clientHeight`.
   Left byte-identical.
3. NOT a file this round edits, but falsified by this round's own C3:
   `tests/ui_contracts/test_diff_view_model.py`, module docstring, "the same
   decision records that a mutation red-proof of TypeScript is not orderable in
   this repository — `apps/ui/node_modules` is gitignored, so it is absent from
   the disposable worktree". DECISION F037 D10 (landed at `f2b96d03`) measures
   the opposite, and G6 of this round took four TypeScript red-proofs through
   that route. Left untouched; a future round owns it.
4. A note rather than a stale claim: `test_diff_view_render.py`'s docstring says
   "Every assertion runs over COMMENT-STRIPPED source". C7's
   `declared_row_height_px` reads the model module RAW, anchored on
   `^export const DIFF_VIRTUAL_ROW_HEIGHT_PX = (\d+);`, which no JSDoc line in
   this repository's style can satisfy; the CSS side goes through
   `strip_css_comments`. Red-proof (e) shows the test discriminates.

## Next

Review this round: `git diff 6d13fae4..HEAD`, re-run G1 through G8. Before
authoring the next block, re-read `.agent/STOP` from disk (Phase 1 rule 1) and
then run the Open PR Gate (rule 2). The next work order is the lazy language
bundles — unknown languages rendering plain with no bundle fetch — and the
10k-line perf fixture measured END TO END with its numbers recorded; S3 of this
round bounds the window's row count but times nothing.
