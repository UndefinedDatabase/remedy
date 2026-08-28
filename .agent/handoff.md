# Handoff — F037 Rendered diff viewer, round 23

## Session

SESSION 6 of feature F037 · round 23 · rounds so far 23.

THIS IS EXPECTED TO BE THE LAST DELEGATED ROUND OF SESSION 6. The next session
begins at ROUND 24 of a 25-round soft limit, session 7 of 7, with THREE named
pieces outstanding:

1. the WIRING of highlighting into `DiffView` through `loadDiffLanguageBundle`;
2. the 10k-line perf fixture measured END TO END with its numbers recorded,
   which Acceptance requires and which nothing has yet measured;
3. a ruling on the sidebar's visual treatment, still owed.

Three pieces and two rounds inside the limit, so the session that reaches ROUND
25 owes a SCOPE REPORT rather than more work — most likely proposing that the
highlighting wiring and the perf fixture become their own STATUS line. No scope
report is owed yet: round 23 is past neither limit.

## Range

Review of `815f7a30..HEAD` (`HEAD` = `4f8a9088` at C5; the handoff commit is C6).

## Commits

### bed572bd chore(agent): save the F037 R23 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r23.md` | +353/-0 | C0a: the block saved byte for byte |

### ce7f54ce chore(agent): mirror the F037 R23 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +241/-272 | C0b: the same bytes, read back from the committed C0a blob |

### ab85ce02 docs(agent): set the plan for F037 R23
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +24/-24 | C1: the PLANF037R23 slice, extracted from the committed C0a blob |

### b9fb06ec docs(review): record the R22 verdict, two resolutions and one finding
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +16/-0 | C2: GATER22, DONE729, DONE730, FINDING731 appended in Bundle order |

### 8bb2ab6a fix(ui): stop the language lookup falling through to the prototype
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffViewModel.ts` | +50/-20 | S1: null-prototype mapping and own-property read, with the WHY on both halves |
| `apps/ui/src/api/diffViewModel.test.ts` | +52/-0 | S2: four new cases, no existing case edited |
| `tests/ui_contracts/test_diff_view_model.py` | +36/-12 | the existing `DIFF_SUPPORTED_LANGUAGES` scoper, re-anchored — see Deviations 1 |
| `.agent/live_review.md` | +2/-0 | S5: the `Landed: R-0731` line |

(140 insertions, 32 deletions across the four paths.)

### 4406640f test(ui-contracts): pin the shape the prototype-safe lookup rests on
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_diff_view_model.py` | +129/-6 | S3: `TestLanguageLookupIsSafeForArbitraryKeys`, the lookup-body scoper, two named spellings, and the module docstring's overlap sentence |

### 4f8a9088 docs(ui): name only the sites that really name the collapse threshold
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffViewModel.ts` | +19/-15 | S4: the three comment repairs, comment text only |
| `.agent/live_review.md` | +2/-0 | S5: the `Landed: R-0730` line |

### C6 — this commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | the handback a handoff cannot table for itself |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/f037-r23-redproof 4406640f --detach` | created at `4406640f` |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f037-r23-redproof --force` + `git worktree prune` | removed by exact path; `git worktree list` is ONE line, the primary checkout |
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — no open PR |
| `git push -u origin feature/f037-rendered-diff-viewer` | run after C6; see Verification |

No PR created, nothing merged, no force-push, no history rewrite.

## Verification

One line per gate, real exit codes.

**G1 HYGIENE** — `.agent/STOP` absent, read from disk before C0a and again before
C6 (`ls` exit 2 both times, "No such file or directory"). `git rev-parse HEAD`
before C0a = `815f7a30fa8ba83842f63c189b3e7e8b9935bf46` = BASE. Branch
`feature/f037-rendered-diff-viewer`. `git status --porcelain | wc -l` = 0 after
every one of C0a, C0b, C1, C2, C3, C4, C5.

**G2 TRANSPORT** — the committed C0a blob is 32100 bytes, 353 lines, sha256
`2793ac9e5c51c397364f1fd75b5bf6b4759ccdd6d003b6645eabc21b49fad185`, which is the
block file's own reading before any commit. At C0b `git rev-parse
HEAD:.agent/authored/f037-r23.md` and `HEAD:.agent/last_block.md` are ONE blob,
`190eb058387b0dc0bf9574f91e33ecd12952866c`.

**G3 THE PLAN AT C1** — PLANF037R23 re-extracted from the COMMITTED C0a blob and
compared to `git show ab85ce02:.agent/plan.md`: byte equality **True**, including
the trailing newline. Negative control, the same slice minus its trailing
newline: **False**. `wc -l` = 47, strictly under 50 = True. Lines exactly
`## Goal` = 1; lines exactly `## Next Steps` = 1.

**G4 THE RECORD AT C2** — pre-round blob (`ab85ce02`, 1292757 bytes) joined to
GATER22, DONE729, DONE730, FINDING731 in Bundle order with exactly one newline
before each equals the C2 blob (1306220 bytes): **True**. Negative control, one
byte flipped at offset 1030 inside GATER22's FIRST paragraph (that paragraph is
2060 bytes): **False**. The pre-round blob is a byte PREFIX of the C2 blob:
**True**.

**G5 THE LEDGER** — line-anchored, base figures from `815f7a30` in brackets, all
four base figures matched the block's brackets exactly.

| Pattern | base | C2 | ordered | met |
|---|---|---|---|---|
| `^- R-\d+ — ` | 291 [291] | 292 | rise by one to 292 | yes |
| `^Done: R-\d+ — ` | 39 [39] | 41 | rise by two to 41 | yes |
| `^Gate: F\d+ R\d+ — ` | 92 [92] | 93 | rise by one to 93 | yes |
| OPEN SET, computed AS A SET | 254 [254] | 253 | FALL by one to 253 | yes |
| `^Landed: R-` | 9 [9] | 9 → 10 at C3 → 11 at C5 | rise by two to 11 | yes |

Every registered id distinct: 292 of 292 at C2 (291 of 291 at base).

**G6 THE RED-PROOFS** — disposable worktree at the C4 tree (`4406640f`), removed
afterwards. TypeScript driven per constraint 8 and DECISION F037 D10: vitest
spawned FROM the primary checkout, `--root` at the worktree, `--config` at the
primary. `__pycache__` purged and `python3 -B` for every pytest run. Pre-mutation
sha256 of `diffViewModel.ts` = `0a2ec9c286d4b0cab8277b7da358990ebb72add4bc4c490f467a066f9b682343`.

| Gate | count of replaced string | exit | result |
|---|---|---|---|
| control FIRST | — | vitest 0 (90 passed), pytest 0 (8 passed) | green |
| (a) null prototype removed, own-property read STAYS | 1 | **1 — RED** | `builds the supported set with NO prototype to inherit from` |
| (b) own-property read replaced by an `undefined` comparison, null prototype STAYS | 1 | **0 — GREEN, EXPECTED** | 90 passed; not a gate failure, see below |
| (c) BOTH halves removed, the exact `815f7a30` shape | 1 + 1 | **1 — RED on 4** | the three inherited-key tests AND `asks for NO bundle for an extension naming an INHERITED property` |
| (d) one entry (`toml: "toml"`) deleted from the mapping | 1 | **1 — RED** | `names every language id it claims to support` |
| (e) `Object.create(null)` removed from the DECLARATION | 1 | **1 — RED** | `TestLanguageLookupIsSafeForArbitraryKeys::test_the_supported_set_is_built_on_a_null_prototype` |
| control LAST | — | vitest 0 (90 passed), pytest 0 (8 passed) | green |

Every file restored to sha256
`0a2ec9c286d4b0cab8277b7da358990ebb72add4bc4c490f467a066f9b682343` after every
mutation, shown each time, and at the end of the run.

(b) IS GREEN AND THAT IS THE ORDERED READING, not a red gate: a null-prototype
map has nothing to inherit, so an `undefined` comparison over it is correct
today. That is the measurement showing the two halves are belt and braces rather
than one fix written twice, which is why S1 calls both load-bearing and why the
S3 guard pins the own-property spelling separately.

(c) IS THE DISCRIMINATOR AND IT TURNS OVER: restoring the exact shipped shape
reddens the zero-call Acceptance test, so S2 really reproduces `R-0731` rather
than merely describing it.

**G7 SUITES, TYPES AND LINT AT C5** — worktree removed first;
`git worktree list` is ONE line: `/home/decodeux/Repos/remedy  4f8a9088
[feature/f037-rendered-diff-viewer]`. One pytest process at a time, serially.

| Gate | exit | result [base] |
|---|---|---|
| `python3 -m pytest tests/ui_contracts/ -q` | 0 | 653 passed, 4 skipped [651, 4] |
| `python3 -m pytest tests/ui_server/ -q` | 0 | 495 passed [495] |
| `python3 -m pytest tests/orchestration/test_test_runner.py tests/docs/ -q` | 0 | 347 passed [347] |
| `python3 -m ruff check tests/ui_contracts/test_diff_view_model.py` | 0 | `All checks passed!` |
| the typescript node, `-k "typescript or tsc or noEmit" -q -rs` | 0 | 1 passed, 73 deselected [1, 73] — PASSED, not skipped |
| the canary `tests/cli/test_golden_path.py -q` | 0 | 42 passed [42] |
| the vitest TOTAL, D10 route, `--reporter=verbose`, primary tree | 0 | 32 files passed, 613 passed [32 files, 609] |

`tests/ui_contracts/` rose by 2 (the two methods of the new S3 class) and vitest
by 4 (the four new S2 cases). All four ran and are named as executed:

- `diffLanguageForPath > renders an extension naming an INHERITED property plain`
- `diffLanguageForPath > never answers a FUNCTION for an inherited extension`
- `diffLanguageForPath > builds the supported set with NO prototype to inherit from`
- `loadDiffLanguageBundle > asks for NO bundle for an extension naming an INHERITED property`

**G8 STRUCTURE AND THE OPEN PR GATE AT C5** — `git diff --name-only
815f7a30..4f8a9088` equals the Change set minus `.agent/handoff.md` EXACTLY:
residue in the diff but not in the change set = `[]`; residue in the change set
but not in the diff = `[]`. `git diff --stat 815f7a30..4f8a9088` restricted to
`packages/`, to `apps/ui/src/components/` and to `apps/ui/src/styles/` is EMPTY
in all three (empty string, measured, not asserted). Every commit is
single-parent. Per-commit insertions, each under 500 and each matching the
tables above: 353, 241, 24, 16, 140, 129, 21. Lines matching `^<<<SLICE ` or
`^<<<END ` at the C5 tree: `.agent/plan.md` 0, `.agent/live_review.md` 0,
`diffViewModel.ts` 0, `diffViewModel.test.ts` 0, `test_diff_view_model.py` 0,
against `.agent/last_block.md` 10 and `.agent/authored/f037-r23.md` 10 as the
NON-ZERO control. `git ls-files .remedy-wt | wc -l` = 0. `gh pr list --state
open` = `[]`.

## Authored-text proofs

`.agent/authored/f037-r23.md` is the block itself, byte for byte:
`.remedy-wt/f037-r23-block.md` and the committed blob agree at 32100 bytes, 353
lines, sha256 `2793ac9e…d185` — the same three readings the prompt named before
the file was opened. Both slices applied this round (PLANF037R23 at C1, the
four-slice append at C2) were extracted PROGRAMMATICALLY from the COMMITTED C0a
blob, never retyped, and both were proved by byte equality (G3, G4).

## Staleness sweep (constraint 10)

Every WHY comment in each edited file was re-read.

REPAIRED — the three sites S4 names, all in `apps/ui/src/api/diffViewModel.ts`,
comment text only, no executable line moved:

1. The `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` paragraph no longer lists
   `DiffView.tsx` among the sites naming the constant. `git grep -n
   DIFF_HUNK_COLLAPSE_THRESHOLD_LINES -- apps/ui/src/components/` exits 1 with no
   output. Every site now named was grepped first, with its hit count:
   `diffViewModel.ts` 4, `diffViewModel.test.ts` 5, `test_diff_view_model.py` 2,
   `test_diff_view_render.py` 1 (line 313). The paragraph now states in so many
   words that the component is NOT among them.
2. "`splitLineIntoIntralineSegments` returns at the foot of this file" — the
   location claim is DROPPED, not re-pointed. It sits at line 476 of 916.
3. "the component that will draw it" is now present tense and names
   `DiffView.tsx`.

REPAIRED — falsified by THIS ROUND'S OWN CODE, which is the carve-out constraint
10 names and the one R21 and R22 both used:

4. `apps/ui/src/api/diffViewModel.ts`, the `diffLanguageForPath` body comment:
   "`Record<string, string>` claims every key resolves … so the absent case can
   be compared for" described the `undefined` comparison C3 removes. Replaced.
5. `tests/ui_contracts/test_diff_view_model.py`, the module docstring: "there is
   no overlap between the two: a green vitest run says nothing about any of the
   classes below" is falsified by C4's own class, which deliberately overlaps
   with the S2 vitest cases. Rewritten to name the class as the ONE exception and
   to say which guard is the stronger.

VERIFIED RATHER THAN ASSUMED while editing the sentence beside it:
`DiffView.tsx:228` really does call `splitLineIntoIntralineSegments` and wrap
each segment in `<mark className={styles.intraline}>` at line 230.

REPORTED AND LEFT ALONE — no other stale claim was found in either edited file.
The remaining relational comments were re-checked and all hold at `4f8a9088`:
`DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS`'s "ONE consumer is `computeDiffRowWindow`",
the `defaultCollapsedHunkIds` "below", and the two "above" references in the new
S1 text.

## Deviations & assumptions

1. **ONE EXTRA FILE IN C3, DECLARED.** The block bundles
   `tests/ui_contracts/test_diff_view_model.py` under C4. C3 also touches it,
   for one reason: the existing scoper `supported_languages_block` matched
   `= Object\.freeze\(\{` LITERALLY, so S1's ordered shape change turned
   `test_every_supported_language_id_is_named_by_the_vitest_suite` RED — measured
   before the repair, `1 failed, 5 passed`. Leaving it to C4 would have made C3 a
   commit at which that guard was red, which is exactly what constraint 6 exists
   to prevent, so the minimal repair travelled with the change that forced it.
   The repair re-anchors the scoper on the DECLARATION'S OWN boundaries rather
   than on one way of writing the initialiser, and `supported_languages_block`
   now reads the entries between that region's first `{` and last `}`. No
   assertion was weakened: the same function still returns the entry body, the
   same ids, and the same "declared exactly once, by name" promise, and (e) of G6
   proves the new region scoper is not vacuous.
2. **THE COMMIT ORDER ITSELF IS UNCHANGED** — C0a, C0b, C1, C2, C3, C4, C5, C6,
   nothing reordered, nothing dropped, no extra commit.
3. **G6 (e) IS SCOPED TO THE DECLARATION.** The block orders "the
   `Object.create(null)` spelling removed from the declaration" and orders each
   replaced string counted at exactly 1. The raw file names that spelling TWICE —
   once in the WHY comment and once in the code — so a bare replacement counted 2
   and the run stopped rather than proceeding. The mutation was then scoped to
   the declaration's own occurrence,
   `Object.create(null) as Record<string, string>`, which counts 1. This is the
   STRONGER reading of the gate, not a weaker one: the comment goes on naming the
   spelling, so a guard satisfied by the comment rather than by comment-stripped
   code would have stayed GREEN. It went red, and its assertion message shows it
   read the stripped declaration.
4. **THE WORKTREE VITEST RUN IS SCOPED TO THE MODULE UNDER TEST.** A full
   `--root`-at-the-worktree run cannot be green there:
   `src/components/prompt/promptTraceLens.test.ts` transitively loads a `.tsx`
   needing `react/jsx-dev-runtime`, and the worktree has no `node_modules`
   (`ERR_MODULE_NOT_FOUND`, measured). The red-proofs therefore run
   `src/api/diffViewModel.test.ts`, the file every mutation touches. That is R22's
   own precedent — its worktree control was 86 tests, and ours is 90, being those
   86 plus this round's 4. The vitest TOTAL of G7 is the unscoped run, in the
   primary checkout, at 32 files and 613 tests.
5. **`--config` IS THE SECOND OF CONSTRAINT 8'S TWO FLAGS.** `--root` alone fails
   in the worktree, because the worktree's own `vitest.config.ts` imports
   `vitest/config` and node resolves it from the worktree, which has no
   `node_modules`. Pointing `--config` at the PRIMARY config while `--root` stays
   at the worktree resolves the package from the primary and still collects and
   executes the WORKTREE's tree — proved, not assumed, by (a), (c), (d) and (e)
   all going red on worktree-only mutations while the primary checkout was
   untouched throughout.
6. **`.remedy-wt/` SCRATCH LEFT IN PLACE.** Two files were written this round,
   `.remedy-wt/r23_vitest.py` and `.remedy-wt/r23_redproof.py`, plus
   `.remedy-wt/r23_vitest_verbose.txt`. The directory is gitignored and
   `git ls-files .remedy-wt` is 0, so nothing is tracked; they are left alongside
   earlier rounds' scratch rather than deleted, and they are named here by exact
   path.
7. **NO `Done:` OR `Gate:` PARAGRAPH WAS AUTHORED.** The only lines written into
   `.agent/live_review.md` by this worker are the two `Landed:` lines SPEC S5
   asks for. Everything else in C2 is the block's own slices, applied byte for
   byte.
8. **ASSUMPTION.** The plan file's item table reads `ordered` for every item at
   this handback, as it did at R22: the plan is written byte for byte at C1 from
   the block's slice and the block orders no second write. It records the round's
   intent, not its outcome; this table is the outcome.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into `last_block.md` | done | |
| C1 the plan | done | |
| C2 the record append | done | |
| C3 the `R-0731` fix and its tests | deviated | also carried the forced one-function repair of the existing scoper — Deviations 1 |
| C4 the structural guard | done | |
| C5 the three comment repairs | done | |
| C6 the handback | done | this commit |
| G1 hygiene | done | STOP absent twice, HEAD = BASE, branch right, clean after every commit |
| G2 transport | done | 32100 / 353 / `2793ac9e…d185`; ONE blob `190eb058` at C0b |
| G3 the plan at C1 | done | byte equality True, negative control False, 47 lines |
| G4 the record at C2 | done | join True, flipped-byte control False, prefix True |
| G5 the ledger | done | 292 / 41 / 93 / open set 253 / Landed 11, all as ordered |
| G6 the red-proofs | done | (a) RED, (b) GREEN as ordered, (c) RED on 4, (d) RED, (e) RED; controls green first and last |
| G7 suites, types and lint | done | all seven exit 0; worktree list reported first |
| G8 structure and Open PR Gate | done | residue empty both ways, three trees empty, markers 0/10, `[]` |

No gate marked MUST be RED came back green. No slice failed to apply. Nothing in
the block contradicted itself.

## Next

Review this round at `815f7a30..HEAD` and issue the verdict. Before authoring the
next round, re-read `.agent/STOP` from disk (Phase 1 rule 1 BEFORE rule 2), then
the Open PR Gate. Round 24 of 25 begins a new session, session 7 of 7, with the
three pieces named at the top of this file outstanding and a SCOPE REPORT owed by
the session that reaches round 25.
