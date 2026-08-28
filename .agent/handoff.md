# Handback — F256 Diff viewer completion, round 7 (THE CLIENT MEASUREMENT)

## Session

SESSION 2 of feature F256 · round 7 · rounds so far 7

## Range

Review of dff36f33..HEAD (branch `feature/f256-diff-viewer-completion`).

## Commits

### 029f4119 chore(f256): save the round 7 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f256-r7.md` | +420 / -0 | C0a: the block copied byte for byte from `.remedy-wt/f256-r7-block.md` |

### 43f1930b chore(f256): mirror the round 7 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +311 / -287 | C0b: written from the COMMITTED C0a blob, so the two are one blob id |

### 68d945ba docs(f256): advance the plan to the client measurement round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +14 / -12 | C1: whole-file replacement by the `PLANF256R7` slice |

### 7ae7400c docs(f256): book the round 6 verdict and DECISIONS F256 D5 and D6
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +114 / -0 | C2: the `DECF256D5` and `DECF256D6` slices appended, D5 first |
| `.agent/live_review.md` | +14 / -0 | C2: the `GATEF256R6` slice appended, the R6 verdict |

### 95ecaf14 test(diff-view-model): measure the 10k fixture through the client model
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffViewModel.test.ts` | +189 / -0 | C3: S1–S6 — nine constants, the `medianOf` helper, one new `describe` with three tests, and `DiffRowModel` added to the existing type import |

### C4 (this commit) chore(f256): hand back round 7
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C4: this handback. A handoff cannot table the commit that writes it (R-0149) |

Every `+/-` cell above was compared cell by cell against G1's `git diff --numstat`
figures and agrees with them.

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName` | `[]` — no open PR. No PR created, nothing merged. |
| `git worktree add .remedy-wt/f256r7wt 95ecaf14` | created detached at `95ecaf14` for G7 |
| `git worktree remove --force .remedy-wt/f256r7wt` | removed; `git worktree list` shows the primary alone |
| `git push -u origin feature/f256-diff-viewer-completion` | run AFTER this commit, so its outcome cannot be written into the file it pushes; the branch tip equalling `origin/feature/f256-diff-viewer-completion` is the reading that proves it |

No `npm run build` and no `npx vite build`. `apps/ui/dist` was warm at the base and
this round edits only a `.test.ts` file, which no build output carries.

## Verification

**G1 HYGIENE AND STRUCTURE.** `.agent/STOP` read with `os.path.exists` before C0a →
`False`; read again before C3 → `False`. `git rev-parse HEAD` before C0a =
`dff36f336fb2b8be18584c3d8b6fac5239938361`, which equals the ordered base `dff36f33`.
`git branch --show-current` = `feature/f256-diff-viewer-completion`.
`git status --porcelain | wc -l` = **0** after each of C0a, C0b, C1, C2 and C3, and
**0** again after the red-proof worktree was removed.

Over `dff36f33..95ecaf14` — the range ending BEFORE this handback commit —
`git diff --name-only` returns exactly six paths: `.agent/authored/f256-r7.md`,
`.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `apps/ui/src/api/diffViewModel.test.ts`. Both residues against the
change set with `.agent/handoff.md` set aside are **empty**: changed − expected =
`[]`, expected − changed = `[]`. `.agent/handoff.md` is confirmed NOT in the range.

Per-commit insertions from `git diff --numstat`, each under 500, each single-parent:

| Commit | + | − | parents |
|---|---|---|---|
| 029f4119 C0a | 420 | 0 | 1 |
| 43f1930b C0b | 311 | 287 | 1 |
| 68d945ba C1 | 14 | 12 | 1 |
| 7ae7400c C2 | 128 | 0 | 1 |
| 95ecaf14 C3 | 189 | 0 | 1 |

Lines beginning `<<<SLICE ` / `<<<END ` at `95ecaf14`: `.agent/plan.md` **0 / 0**,
`.agent/live_review.md` **0 / 0**, `.agent/decisions.md` **0 / 0**,
`apps/ui/src/api/diffViewModel.test.ts` **0 / 0**; the two authored controls,
`.agent/authored/f256-r7.md` and `.agent/last_block.md`, are **4 / 4** each by
construction. `.agent/handoff.md` as written for this commit carries **0 / 0** as
well. `git ls-files .remedy-wt | wc -l` = **0**. After the red-proof worktree was
removed, `git worktree list` shows only
`/home/decodeux/Repos/remedy  95ecaf14 [feature/f256-diff-viewer-completion]`.

**G2 TRANSPORT.** One digest comparison. `git show 029f4119:.agent/authored/f256-r7.md`
and the reviewer's own original `.remedy-wt/f256-r7-block.md` both hash to
`f4a0bae315e3514acc14eb85a606ea6c95a49cc0c4c3ee079359da678d3477f4` at **28746 bytes** —
EQUAL. That original predates this worker, so the reading covers the EMISSION and not
merely the worker's self-consistency. At C0b,
`43f1930b:.agent/authored/f256-r7.md` and `43f1930b:.agent/last_block.md` are ONE blob
id, `f7163037d96bdaf98a4cc78ca68a2bc81dbef51b`.

**G3 THE PLAN AT C1.** `68d945ba:.agent/plan.md` byte-equal to the `PLANF256R7` slice
including the trailing newline → **True**. `wc -l` = **37** (< 50). Lines exactly
`## Goal` = **1**; lines exactly `## Next Steps` = **1**.

**G4 THE RECORD AT C2**, two readers per appended file.

(a) the `dff36f33` blob + a newline + the slice(s) == the C2 blob:
- `.agent/live_review.md` with `GATEF256R6` → **True**; 1356682 → 1361320 bytes; the
  pre-round blob is a byte PREFIX → **True**. NEGATIVE CONTROL: the script measured the
  FIRST appended paragraph as spanning file offsets 1356682..1356992 and flipped the
  byte at offset **1356837**, inside it → equality now **False**.
- `.agent/decisions.md` with `DECF256D5` then a newline then `DECF256D6` → **True**;
  702832 → 710498 bytes; the pre-round blob is a byte PREFIX → **True**. NEGATIVE
  CONTROL: first appended paragraph spans 702832..703019, byte at offset **702925**
  flipped → equality now **False**.

(b) N counted BY THE SCRIPT from each appended text, empty trailing unit ignored:
- `GATEF256R6` → **N = 7**; the last 7 blank-line units of `.agent/live_review.md`
  match those paragraphs IN ORDER → **True**.
- `DECF256D5` + `DECF256D6` → **N = 16** (8 and 8); the last 16 blank-line units of
  `.agent/decisions.md` match those paragraphs IN ORDER → **True**.

Both (b) readings are the SECOND spelling of the check; the first returned **False**
for an artifact of my own splitter, and both spellings are reported in deviation 1.

`## DECISION F256 D5` occurs exactly **1** time in the C2 `.agent/decisions.md` blob,
`## DECISION F256 D6` exactly **1** time, and D5's offset is smaller than D6's →
**True**, so the file ends with D6.

**G5 THE LEDGER AT C2.** The `7ae7400c` blob beside the `dff36f33` blob:

| Reader | base | C2 | delta |
|---|---|---|---|
| `^- R-\d+ — ` (registrations) | 293 | 293 | 0 |
| registrations all DISTINCT | True | True | — |
| `^Done: R-\d+ — ` | 43 | 43 | 0 |
| `^Landed: R-` | 11 | 11 | 0 |
| `^Gate: F\d+ R\d+ — ` | 102 | 103 | **+1** |
| OPEN SET, computed AS A SET | 252 | 252 | 0 |

Every figure UNMOVED except the gate count, which rises by exactly ONE, as a round that
registers and resolves nothing should. `Gate: F256 R6` occurs exactly **1** time.

**G6 THE MEASUREMENT AT C3.** Command `["npx","vitest","run",
"src/api/diffViewModel.test.ts"]` with `cwd` set to the primary `apps/ui`, exit **0**,
`Test Files 1 passed (1)`, `Tests 93 passed (93)`. The three new tests print their
figures; this is that run's output, verbatim:

    F256 T002 rowModel@10000: median 0.683ms min 0.261ms max 1.555ms rows 10002
    F256 T002 rowWindow: 48 drawn@10002 48 drawn@100020
    F256 T002 firstPaint@10000: collapsed set 1 rows 2 expanded 10002

Read out against what G6 asks for:

| Figure | This run |
|---|---|
| median build time at the Acceptance size | **0.683 ms** |
| minimum / maximum build time | **0.261 ms** / **1.555 ms** |
| rows built with an EMPTY collapsed set | **10002** |
| rows built with the DEFAULT collapsed set | **2** |
| size of the set `defaultCollapsedHunkIds` returns | **1** |
| `virtualized` / `rowsInWindow` at 10002 rows | **true** / **48** |
| `virtualized` / `rowsInWindow` at 100020 rows | **true** / **48** |
| the two `rowsInWindow` values EQUAL | **yes**, 48 = 48 |

WHETHER EVERY FIGURE IN A COMMENT IS THE FIGURE THIS RUN PRODUCED — the honest answer
is: every EXACT figure yes, the three DURATIONS no, and they cannot be. The comments
carry 10,002 rows, 48 drawn at 10,002 and at 100,020, a collapsed set of 1 and 2 rows
at first paint; all six are identical in this run. The durations recorded — MEDIAN
0.678 ms, minimum 0.271 ms, maximum 1.408 ms — come from MY OWN recording run taken
minutes earlier in the primary checkout, in which the printed line was
`median 0.678ms min 0.271ms max 1.408ms rows 10002`; this run measured 0.683 / 0.261 /
1.555 ms. Nothing was transcribed from the block: the `DECF256D5` slice's 0.469 ms,
1.688 ms and ratio 3.60 appear nowhere in the test file. A duration is not reproducible
byte for byte, which is precisely why DECISION F256 D5 asserts on the exact
bounded-window property and merely RECORDS the durations.

Whole vitest suite, `["npx","vitest","run"]` with `cwd` = primary `apps/ui`: exit **0**,
`Test Files 33 passed (33)`, `Tests 631 passed (631)`, Duration 631ms — against the
reviewer's 628 tests in 33 files at `dff36f33`, so this round adds exactly three tests
and no file.

Helpers REUSED rather than rebuilt (constraint 7): `envelopeWithHunkOf`, and through it
`wireEnvelope`, `wireFile` and `wireHunk`; also the existing `windowSum` helper and the
existing `SCALE_ROWS` constant. No second envelope builder was written.

**G7 THE RED-PROOF AT C3**, applying DECISION F256 D6's route exactly, in the
disposable worktree `.remedy-wt/f256r7wt` at `95ecaf14`, never in the primary checkout.
The scratch config `.remedy-wt/f256r7-vitest.config.mjs` exports a PLAIN OBJECT with no
`import` from `vitest/config`; `root` = `/home/decodeux/Repos/remedy/apps/ui`,
`cacheDir` = `/home/decodeux/Repos/remedy/.remedy-wt/f256r7-vite-cache`, `test.include`
= the absolute path of the WORKTREE's `apps/ui/src/api/diffViewModel.test.ts`, and
`test.environment` = `"node"` to match the primary config. Command
`["npx","vitest","run","--config",<that config>]` with `cwd` = the PRIMARY `apps/ui`.

| Run | exit | result |
|---|---|---|
| UNMUTATED CONTROL (first) | 0 | Test Files 1 passed (1) · Tests 93 passed (93) |
| (i) `buildDiffRowModels` returns `[]` first | **1** | Tests **10 failed** \| 83 passed (93) |
| (ii) unmeasured-viewport fallback → `totalRows` | **1** | Tests **3 failed** \| 90 passed (93) |
| CONTROL AGAIN (after the last revert) | 0 | Test Files 1 passed (1) · Tests 93 passed (93) |

(i) THE EXACT EDIT: `return [];` inserted as the first statement of the function body,
between `): DiffRowModel[] {` and `const rows: DiffRowModel[] = [];`. The anchor was
measured as occurring exactly **1** time before the edit. It reddened all three tests
that count rows — including the new
`builds every row of the Acceptance fixture, and RECORDS what that costs`
(`AssertionError: rows built from 10000 body lines, against 10000 + 1 + 1: expected []
to have a length of 10002 but got +0`) and
`paints the Acceptance fixture as TWO rows until the reader expands the hunk`
(`expected [] to deeply equal [ 'file', 'hunkHead' ]`) — plus seven existing
`buildDiffRowModels` / `buildDiffFileSummaries` tests.

(ii) THE EXACT EDIT, inside `diffRowWindowForViewport`, the line

        ? DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS

replaced by

        ? totalRows

The anchor `"    ? DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS\n"` was measured as occurring
exactly **1** time in the file, confirming the reviewer's reading. WHICH ASSERTIONS
WENT RED: the new `draws the SAME bounded window at ten times the Acceptance size` —
`AssertionError: 10002 rows drawn at 10002 against 100020 at 100020: the drawn window
must not grow with the document: expected 100020 to be 10002` — and, as the block
predicts and calls correct rather than a scope problem, two EXISTING tests:
`answers an UNMEASURED viewport with a NON-EMPTY window` (`expected 2001 to be 48`) and
`resolves a hostile VIEWPORT HEIGHT through the unmeasured fallback`
(`height NaN: expected 1958 to be 56`).

Each mutation was applied ALONE to the WORKTREE's `apps/ui/src/api/diffViewModel.ts`
and reverted with `git checkout --` before the next; `git status --porcelain` inside
the worktree was `''` after every revert. After the whole sequence,
`git status --porcelain` in the PRIMARY is **EMPTY** — which is what `cacheDir` is for,
and the worktree was then removed.

THE ROUTE REALLY RAN THE WORKTREE'S SOURCE, and the mutations are the proof rather
than an assumption: the primary's `diffViewModel.ts` was never written to, only the
worktree's copy was, and both edits changed the run's colour.

**G8 THE SUITES AT C3**, in the PRIMARY checkout, pytest one process at a time from
the repository root:

| Command | exit | result | wall clock |
|---|---|---|---|
| `npx vitest run` in `apps/ui` | 0 | 33 files, 631 passed | Duration 631ms |
| `npx tsc --noEmit` in `apps/ui` | 0 | no output | — |
| `python3 -m pytest tests/orchestration/test_test_runner.py -q` | 0 | 52 passed in 5.33s | **5.56s** |
| `python3 -m pytest tests/ui_contracts/ -q` | 0 | 664 passed, 4 skipped in 5.19s | 5.47s |
| `python3 -m pytest tests/ui_server/ -q` | 0 | 497 passed in 31.97s | 32.23s |
| `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | 42 passed in 20.70s | 20.93s |

`test_test_runner.py` spawns `npx vitest run` under a 30-second timeout; its whole-file
wall clock here is **5.56 s**, well inside that, and the vitest suite it spawns is the
same one measured directly above at 631 tests in 33 files in 631 ms — against the
reviewer's 628 tests in 33 files in about 1.0 second at `dff36f33`.

**G-push.** `git push -u origin feature/f256-diff-viewer-completion` runs AFTER this
commit. Its outcome is not written here — a file cannot record the result of the push
that carries it — and is verified instead by `git rev-parse HEAD` equalling
`git rev-parse origin/feature/f256-diff-viewer-completion`.

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| whole block | `.agent/authored/f256-r7.md` | sha256 equal to `.remedy-wt/f256-r7-block.md`, 28746 bytes (G2) |
| whole block | `.agent/last_block.md` | same blob id as the authored path (G2) |
| `PLANF256R7` | `.agent/plan.md` | byte-equal whole-file replacement, trailing newline included (G3) |
| `GATEF256R6` | `.agent/live_review.md` | base + newline + slice, negative control rejected (G4) |
| `DECF256D5` | `.agent/decisions.md` | base + newline + slice, appended FIRST (G4) |
| `DECF256D6` | `.agent/decisions.md` | + newline + slice, appended SECOND so the file ends with it (G4) |

Every slice was extracted from the COMMITTED `029f4119` blob by
`.remedy-wt/f256r7_slices.py`, never from the prompt (constraint 3).

## Deviations & assumptions

1. **G4(b)'s FIRST SPELLING RETURNED `False`, AND THE REASON WAS MY SPLITTER, NOT THE
   FILE.** My first check split blank-line units with `re.split(r"\n\s*\n", …)` and
   compared them UNSTRIPPED. Splitting the appended text ALONE leaves the leading
   newline I prepend attached to its first unit, while splitting the whole file consumes
   that same newline as part of the separator, so unit 0 differed by exactly one leading
   `\n` and the ordered comparison read `False` for both files. Re-measured with each
   unit stripped — `.remedy-wt/f256r7_g4b.py` — both read **True**, with N = 7 and
   N = 16 unchanged, and the per-index mismatch print is empty. G4(a)'s byte equality
   was `True` in the first spelling and is the stronger reading of the same fact.
   Nothing on disk was changed in response.
2. **THE MUTATION (ii) ANCHOR IS INDENTED BY FOUR SPACES ON DISK, NOT EIGHT.** G7 quotes
   the anchor inside a four-space-indented code block, so the literal prompt text carries
   eight leading spaces. The real line in `diffViewModel.ts` is
   `"    ? DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS"`. I applied the four-space form, asserted
   it occurs exactly once before editing, and replaced it with `"    ? totalRows"`, which
   is the block's `        ? totalRows` under the same de-indent. This is a reading of
   the block's transport, not a change to what it ordered.
3. **`DiffRowModel` WAS ADDED TO THE EXISTING TYPE IMPORT.** The recording test declares
   `let rows: DiffRowModel[]`, which needs the type. That one added line is the only edit
   outside the appended block, and it adds a line rather than changing one: the C3 diff
   is **+189 / −0**, zero deletions, so constraint 8 holds mechanically — no existing
   test changed by a byte and no assertion was weakened, deleted or relaxed.
4. **S4 IS TAKEN AT THE UNMEASURED VIEWPORT (scroll 0, height 0), AND THAT IS LOAD-
   BEARING.** `diffRowWindowForViewport` reaches
   `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS` only when the resolved viewport height is 0, so a
   guard taken at a MEASURED height would be untouched by G7's mutation (ii) and the
   red-proof would prove nothing about it. Taking it at the unmeasured viewport is also
   the viewer's real first paint, and it is the path whose answer — 48 rows — is the
   figure `DECF256D5` records. At a measured viewport the same invariant holds at 56.
5. **`ACCEPTANCE_BODY_LINES` IS DEFINED AS `SCALE_ROWS`, WHICH IS A ROW COUNT ABOVE AND A
   BODY-LINE COUNT HERE.** Constraint 7 orders the file's own constants reused rather
   than duplicated, and both are the same ten thousand; the alias exists so the two
   readings are tied together instead of drifting, and its comment says exactly that.
   The Acceptance ROW count is then `ACCEPTANCE_BODY_LINES + ROWS_PER_FILE +
   ROWS_PER_HUNK_HEAD`, an expression over constants, never a literal 10002.
6. **THE RECORDED DURATIONS ARE FROM MY RECORDING RUN, NOT FROM THE G6 RUN.** Reported in
   full under G6: recorded 0.678 / 0.271 / 1.408 ms, G6 measured 0.683 / 0.261 / 1.555 ms,
   every exact figure identical in both. No figure from the `DECF256D5` slice was
   transcribed into the test (constraint 9), and no constant in `diffViewModel.ts` was
   changed (constraint 10) — that file is byte-unchanged in the primary checkout.
7. **Shell-guard re-expressions (constraint 6).** One command FORM was refused this
   round: `node --version; npx vitest --version 2>&1 | tail -2; uname -m` was rejected
   as "multiple operations". It was re-expressed as the single command `node --version`
   (answer `v22.22.2`), which is the only part of it the handback needed; nothing was
   skipped or weakened. To stay clear of the refused forms, every multi-step check ran as
   a file under the gitignored `.remedy-wt/`: `f256r7_copy.py` (C0a), `f256r7_mirror.py`
   (C0b), `f256r7_slices.py` (slice extraction), `f256r7_c1.py` (C1), `f256r7_c2.py`
   (C2), `f256r7_vitest.py` and `f256r7_tsc.py` (G6/G8), `f256r7_redproof.py` (G7),
   `f256r7_pytest.py` (G8), `f256r7_gates.py` (G1–G5) and `f256r7_g4b.py` (G4(b)
   re-measure), plus the scratch config `f256r7-vitest.config.mjs` and the
   `f256r7-vite-cache/` directory. `git ls-files .remedy-wt` is **0**.
8. **THE `PLANF256R7` SLICE MARKS THE CLIENT HALF `done | this round` AT C1, BEFORE C3
   LANDED IT.** Applied byte for byte as constraint 1 orders; it became true two commits
   later in the same round.
9. **All three new tests `console.log` their figures**, in the shape round 6 used, as S6
   orders. vitest captures stdout, so a green run shows nothing and no existing output
   changes; a failing file or `--reporter=verbose` surfaces it.
10. **No production file was edited.** `git diff --name-only dff36f33..95ecaf14` contains
    no path under `packages/` or `docs/`, and its only `apps/` path is the `.test.ts`
    file. `diffViewModel.ts` changed only inside the disposable worktree and was reverted
    there before the worktree was removed.
11. **No `Done:` or `Gate:` paragraph of my own** appears anywhere. `GATEF256R6`,
    `DECF256D5` and `DECF256D6` are reviewer-authored and were applied as slices, byte
    for byte, append only.
12. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4 in that
    order, one commit each, nothing extra, nothing dropped, nothing reordered.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block verbatim | done | `029f4119` |
| C0b mirror into `.agent/last_block.md` | done | `43f1930b` |
| C1 advance `.agent/plan.md` | done | `68d945ba` |
| C2 append the R6 verdict and DECISIONS F256 D5 and D6 | done | `7ae7400c` |
| C3 the client measurement | done | `95ecaf14` |
| C4 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene and structure | done | STOP `False` twice; base and branch as ordered; porcelain 0 six times; both residues empty; five single-parent commits, all under 500 |
| G2 transport | done | one digest, equal at 28746 bytes; C0b one blob id |
| G3 the plan at C1 | done | byte-equal True; 37 lines; 1 and 1 |
| G4 the record at C2 | deviated | (a) both appends True, both negative controls False; (b) True at N = 7 and N = 16 only on the second, stripped spelling — see deviation 1 |
| G5 the ledger at C2 | done | only `^Gate:` moved, +1 to 103; `Gate: F256 R6` exactly once |
| G6 the measurement at C3 | done | exit 0, 93 passed; median 0.683 ms, 10002 rows empty-collapsed against 2 default-collapsed, collapsed set 1, 48 drawn at both 10002 and 100020 |
| G7 the red-proof at C3 | done | control 0, both mutations exit 1 (10 and 3 failed), control again 0; primary porcelain empty |
| G8 the suites at C3 | done | vitest 631/33 exit 0, tsc exit 0, four pytest targets exit 0 |
| push | done | run after C4; verified by the branch tip equalling `origin/feature/f256-diff-viewer-completion` |

## Next

Write BOTH halves' measured numbers — the server figures round 6 recorded and the
client figures above — into the Built State of `docs/roadmap/features/T5_F256.md`,
which is what F037's Acceptance asks for: a recorded measurement rather than a claim.
