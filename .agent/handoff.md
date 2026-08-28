# Handoff — F037 Rendered diff viewer, round 22

## Session

SESSION 6 of feature F037 · round 22 · rounds so far 22.

Round 22 of the 25-round soft limit and session 6 of 7 — approaching both, past
neither, so no scope report is owed yet. After this round the named pieces that
remain are the WIRING of highlighting into `DiffView`, and the 10k-line perf
fixture measured END TO END with its numbers recorded. If they do not fit by
round 25, the session that reaches the limit owes the scope report rather than
more work.

## Range

Review of `665be6ef..HEAD` (`HEAD` = `b94a4bc9`).

## Commits

### f3d00153 docs(agent): save the F037 R22 block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r22.md` | +384/-0 | C0a, the block saved byte for byte |

### 03053837 docs(agent): mirror the F037 R22 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +287/-393 | C0b, the same bytes at the mirror path |

### 62aca836 docs(agent): retarget the plan at the lazy language bundles
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +24/-25 | C1, the PLANF037R22 slice applied byte for byte |

### b634b8d6 docs(agent): book the R21 verdict and two staleness findings
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +16/-0 | C2, GATER21 + FINDING729 + FINDING730 appended in Bundle order |

### 335d1a68 docs(ui): repair three comments this feature falsified
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | S5, the two `Landed:` lines |
| `apps/ui/src/api/diffViewModel.ts` | +13/-6 | S1.2 and S1.3, `R-0730`'s two sites |
| `tests/ui_contracts/test_diff_view_model.py` | +11/-5 | S1.1, `R-0729`'s module docstring |

### 5328d0de feat(ui): decide a diff file's language from its path alone
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffViewModel.ts` | +75/-0 | S2, `DIFF_SUPPORTED_LANGUAGES` and `diffLanguageForPath`, appended |
| `apps/ui/src/api/diffViewModel.test.ts` | +77/-0 | S4, nine cases for the language rule |

### 6213af93 feat(ui): load a language bundle only when there is one to load
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffViewModel.ts` | +82/-0 | S3, the importer type, the answer type, the cache, the loader |
| `apps/ui/src/api/diffViewModel.test.ts` | +120/-1 | S4, eight cases including the zero-call Acceptance test |

### 69be112f test(ui-contracts): hold the lazy bundle to its three structural promises
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_diff_view_model.py` | +168/-2 | S6, three new guards, two new scopers, the export scan widened to `async function`, the docstring's blind-spot list extended |

### b94a4bc9 docs(ui): correct a location this round own appends falsified
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffViewModel.ts` | +1/-1 | UNORDERED, see Deviations: C3 wrote "at the foot of this file" of `diffRowWindowForViewport`, and C4/C5 appended past it in the same round |

### The C7 handoff commit
`.agent/handoff.md` is rewritten by the commit that carries this text; a handoff
cannot table the commit that writes it (R-0149 pattern). It is the only path in
that commit.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f037-r22-wt HEAD` | created at `69be112f` |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f037-r22-wt` + `git worktree prune` | removed by exact path; `git worktree list` then reported ONE line, the primary checkout, BEFORE any pytest gate ran there |
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — no open PR |
| `git push -u origin feature/f037-rendered-diff-viewer` | run after C7; see the note below the table |

No PR was created, nothing was merged, nothing was force-pushed and no history
was rewritten.

## Verification

One line per gate, with the real exit code.

**G1 HYGIENE — PASS.** `.agent/STOP` absent, read from disk before C0a
(`ls: cannot access '.agent/STOP': No such file or directory`) and again before
C7 (same output). `git rev-parse HEAD` before C0a was
`665be6efbd9be93121845cb4dcc8248e143e8edc`, equal to BASE. Branch
`feature/f037-rendered-diff-viewer`. `git status --porcelain | wc -l` was `0`
after every one of the nine commits.

**G2 TRANSPORT — PASS.** The committed C0a blob is 33754 bytes, 384 lines,
sha256 `0e2cf6475dc53bfea5d7509bf7fc31693a0559e5af060b967ced3f47db15075e`, which
is byte-identical to the reviewer's own scratch original
`.remedy-wt/f037-r22-block.md` measured before any commit. At C0b
`git rev-parse 03053837:.agent/authored/f037-r22.md` and
`03053837:.agent/last_block.md` are ONE blob,
`16d14a50923cb0b97ee5896321c17002ca0299b9`.

**G3 THE PLAN AT C1 — PASS.** PLANF037R22 extracted from the COMMITTED C0a blob
equals `git show 62aca836:.agent/plan.md` byte for byte including the trailing
newline: `True`. Negative control, the same slice minus its trailing newline:
`False`. `wc -l` 47, strictly under 50: `True`. Lines exactly `## Goal`: 1.
Lines exactly `## Next Steps`: 1.

**G4 THE RECORD AT C2 — PASS.** The `665be6ef` blob joined to GATER21,
FINDING729 and FINDING730 in Bundle order with exactly one newline before each
equals the C2 blob: `True`. Negative control, one byte flipped inside GATER21's
FIRST paragraph (offset 200 XOR 0x01): `False`. The pre-round blob is a byte
PREFIX of the committed one: `True`.

**G5 THE LEDGER — PASS, every figure as predicted.** Line-anchored over the C2
blob, base figure from `665be6ef` in brackets: `^- R-\d+ — ` 291 [289],
`^Done: R-\d+ — ` 39 [39], `^Landed: R-` 7 [7], `^Gate: F\d+ R\d+ — ` 92 [91],
OPEN SET computed AS A SET (registered ids minus ids named by a `Done:` line)
254 [252]. Every registered id is distinct: `True` (291 ids, 291 unique).
Registrations ROSE BY TWO to 291 and the open set ROSE BY TWO to 254; `Done:` is
UNMOVED at 39; `Gate:` rose by one to 92. At C3, `^Landed: R-` rose by two to 9
per SPEC S5. No figure disagreed.

**G6 THE RED-PROOFS — PASS, all seven RED on exactly the named tests.** Run in
the disposable worktree `.remedy-wt/f037-r22-wt` at the C6 tree `69be112f`,
`__pycache__` purged and `python3 -B` used for every pytest run, TypeScript
driven per constraint 8 and DECISION F037 D10 (vitest spawned FROM the primary
checkout, `--root` at the worktree, `--config` at the primary). Every replaced
string counted at exactly 1 BEFORE its edit; every file restored from its saved
bytes and its sha256 re-checked equal.

| Mutation | Exit | Test(s) that went red |
|---|---|---|
| control FIRST, unmutated | vitest 0 (86 passed), pytest 0 (6 passed) | — |
| (a) plain-language early return removed | 1 | `NEVER asks for a bundle when the language is plain` — `expected 1 to be +0`; and `asks for no bundle for ANY kind of plain path` |
| (b) cache lookup removed | 1 | `imports ONE bundle per language however many files ask for it` — `expected 2 to be 1`; and `really forgets what it loaded when the cache is reset` |
| (c) `try`/`catch` around `importBundle` removed | 1 | `degrades a REJECTING import to plain…`, `degrades a THROWING import to plain…`, `RETRIES a language whose import failed…` |
| (d) extension taken from the FIRST dot | 1 | `reads the LAST dot, and reads it inside the BASENAME` — `expected null to be 'typescript'` |
| (e) dotfile guard removed (`dot <= 0` to `dot < 0`) | 1 | `renders a DOTFILE plain, including one named after a supported extension` — `expected 'typescript' to be null` |
| (f) one entry deleted from `DIFF_SUPPORTED_LANGUAGES` (`md: "markdown"`) | 1 | `names every language id it claims to support` — the id set lost one member |
| (g) a `vi.fn()` inserted into the vitest suite | 1 | `test_the_vitest_suite_counts_calls_without_a_mocking_library` — `assert ['vi.fn'] == []` |
| control LAST, every file restored | vitest 0 (86 passed), pytest 0 (6 passed) | — |

Restoration was verified per mutation: `restored: True` with the module back at
sha256 `1a5db12c…` for (a) through (f) and the suite back at `3b4c440a…` for (g).

**G7 SUITES, TYPES AND LINT — PASS.** Primary checkout, ONE pytest process at a
time, worktree removed first and `git worktree list` reported as one line
(`/home/decodeux/Repos/remedy  69be112f [feature/f037-rendered-diff-viewer]`)
BEFORE any pytest ran there. Base figure in brackets.

| Gate | Exit | Result |
|---|---|---|
| `python3 -m pytest tests/ui_contracts/ -q` | 0 | 651 passed, 4 skipped [648, 4] |
| `python3 -m pytest tests/ui_server/ -q` | 0 | 495 passed [495] |
| `python3 -m pytest tests/orchestration/test_test_runner.py tests/docs/ -q` | 0 | 347 passed [347] |
| `python3 -m ruff check tests/ui_contracts/test_diff_view_model.py` | 0 | `All checks passed!` |
| `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k "typescript or tsc or noEmit" -q -rs` | 0 | 1 passed, 73 deselected [1, 73] — PASSED, not skipped |
| `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | 42 passed [42] |
| vitest TOTAL, D10 route, `--reporter=verbose`, primary tree | 0 | 32 files passed, 609 passed [32 files, 592] |

The 17 new cases were all printed by name as EXECUTED: nine under
`diffLanguageForPath` (`resolves EVERY entry of the supported set…`, `names every
language id it claims to support`, `folds an UPPER-CASE extension…`, `reads the
LAST dot, and reads it inside the BASENAME`, `renders a DOTFILE plain…`, `renders
a path with NO dot plain`, `renders the EMPTY path plain`, `renders a path ENDING
in a dot plain`, `renders an UNSUPPORTED extension plain`) and eight under
`loadDiffLanguageBundle` (`NEVER asks for a bundle when the language is plain`,
`asks for no bundle for ANY kind of plain path`, `imports a supported language
EXACTLY once and answers its bundle`, `imports ONE bundle per language however
many files ask for it`, `degrades a REJECTING import to plain, still reporting the
language`, `degrades a THROWING import to plain in the same way`, `RETRIES a
language whose import failed rather than caching the failure`, `really forgets
what it loaded when the cache is reset`). 592 + 17 = 609.

G7 was run at C6 `69be112f` and the three gates the unordered C6b could touch
were RE-RUN at `b94a4bc9`: `tests/ui_contracts/` exit 0 at 651 passed 4 skipped,
the vitest total exit 0 at 32 files and 609 tests, and the typescript node exit 0
at 1 passed 73 deselected.

**G8 STRUCTURE AND THE OPEN PR GATE — PASS.** `git diff --name-only 665be6ef..69be112f`
equals the Change set minus `.agent/handoff.md`: ACTUAL MINUS EXPECTED `[]`,
EXPECTED MINUS ACTUAL `[]`. The same holds at `b94a4bc9`, since C6b edits a path
already in the set. `git diff --stat` restricted to `packages/`,
`apps/ui/src/components/` and `apps/ui/src/styles/` is EMPTY for all three, at
both `69be112f` and `b94a4bc9`. Per-commit insertions from `git show --numstat`,
each under 500 and each matching the tables above: 384, 287, 24, 16, 28, 152,
202, 168, 1. Lines matching `^<<<SLICE ` or `^<<<END ` are 0 in every edited
target that is not a block mirror — `.agent/live_review.md` 0, `.agent/plan.md`
0, `apps/ui/src/api/diffViewModel.ts` 0, `apps/ui/src/api/diffViewModel.test.ts`
0, `tests/ui_contracts/test_diff_view_model.py` 0 — with 8 in the C0a blob as the
NON-ZERO control and 8 in `.agent/last_block.md`, which is that blob mirrored
byte for byte by C0b and is therefore the second control rather than a leak.
`git ls-files .remedy-wt | wc -l` is 0.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned
`[]`.

## Authored-text proofs

| Authored text | Comparison | Result |
|---|---|---|
| the whole block | `.agent/authored/f037-r22.md` at C0a vs the reviewer's scratch original `.remedy-wt/f037-r22-block.md` | byte-equal, sha256 `0e2cf647…`, 33754 bytes, 384 lines |
| the whole block | `.agent/last_block.md` at C0b vs `.agent/authored/f037-r22.md` at C0b | ONE git blob, `16d14a50…` |
| PLANF037R22 | slice extracted from the COMMITTED C0a blob vs `62aca836:.agent/plan.md` | equal `True`, negative control `False` |
| GATER21 + FINDING729 + FINDING730 | base blob + one newline before each vs `b634b8d6:.agent/live_review.md` | equal `True`, negative control `False`, base a byte prefix `True` |

Every slice was extracted PROGRAMMATICALLY from the file on disk; none was
retyped. The two `Landed:` lines of SPEC S5 are the worker's own text, as
constraint 9 requires, and no `Done:` or `Gate:` paragraph was authored.

## Staleness sweep (constraint 10)

The three sites SPEC S1 names were repaired at C3 and nothing else was changed in
them: comment, docstring and message text only, no executable line. Re-reading
every WHY comment in each edited file turned up three OTHER stale claims. Two are
reported and LEFT ALONE per constraint 10; the third is the one this round's own
appends broke, and it was repaired under the reading the reviewer recorded in
GATER21.

1. LEFT ALONE, and it is the strongest of the three. `apps/ui/src/api/diffViewModel.ts`
   line 327, in the `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` comment: "Every other
   site — `defaultCollapsedHunkIds`, `DiffView.tsx`, which renders these rows and
   has been mounted by `RemedyShell` since F037 R18, and both test files — names
   this constant rather than repeating the number." `DiffView.tsx` does NOT name
   that constant: `grep -rn DIFF_HUNK_COLLAPSE_THRESHOLD_LINES apps/ui/src/components/`
   is empty, and the component imports `splitLineIntoIntralineSegments` and its
   siblings but no threshold at all. This is the SAME defect as `R-0730`'s first
   site, one constant along, and the block named only the virtual-scroll one.
   It was already false at `665be6ef`.
2. LEFT ALONE. `apps/ui/src/api/diffViewModel.ts` line 13, in the module header:
   "The segments `splitLineIntoIntralineSegments` returns at the foot of this
   file". That function sits at line 476 of an 883-line module; the foot has been
   something else since F037 R20 appended `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS`
   past it. Already false at `665be6ef`. Line 6 of the same header, "the component
   that will draw it", carries the future tense `R-0730` was raised for, in a
   sentence the block did not name.
3. REPAIRED at `b94a4bc9`, and declared below. C3's own replacement text called
   `diffRowWindowForViewport` "at the foot of this file", which was true when C3
   wrote it and false one commit later, because C4 and C5 append past it. It now
   reads "below in this same module".

## Deviations & assumptions

1. DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. The block orders C0a, C0b, C1
   through C7. I committed ONE extra commit, `b94a4bc9`, between C6 and C7. Its
   whole content is a one-line comment correction in
   `apps/ui/src/api/diffViewModel.ts`: C3's repair of `R-0730` located
   `diffRowWindowForViewport` "at the foot of this file", and C4 and C5 then
   appended past it, so my own round falsified a sentence my own round wrote.
   Constraint 10 says to leave OTHER stale claims alone, and I read that — as
   GATER21 records the R21 worker reading it, and as the reviewer there ruled
   correct — as binding on claims already stale at the sweep rather than on one
   the round's own code breaks. Leaving it would have shipped a false sentence in
   the very commit chain that falsified it. The three gates it could touch were
   re-run at the new tip and are recorded under G7.
2. The subject line of that extra commit reads "this round own appends" where it
   should read "this round's own appends". It is a typo in a commit subject.
   Amending it would rewrite history, which G2 forbids, so it stands.
3. FORWARD REFERENCES INSIDE THE ROUND. Two comments name a symbol that arrives
   one commit later: the S2 comment at C4 names `loadDiffLanguageBundle` (lands at
   C5), and the C5 test-helper comment names
   `tests/ui_contracts/test_diff_view_model.py`'s mocking guard (lands at C6).
   Both are true at the round's tip. They are declared rather than left for a
   reader to trip over.
4. DESIGN CHOICES SPEC S3 ASKED ME TO STATE AND PIN.
   - `importBundle` is REQUIRED, with no default. A default that threw only when
     called would be swallowed by this function's own degrade-to-plain rule and
     reach the operator as "that language is not supported"; required makes the
     same mistake a compile error. Stated in the comment, and consistent with the
     S6 guard, which forbids the module any module specifier at all.
   - A FAILED IMPORT IS RETRIED, not cached. The rejected promise is dropped from
     the cache, so a later call tries again; caching the failure would make one
     lost chunk request permanent for the life of the page. Pinned by
     `RETRIES a language whose import failed rather than caching the failure`.
   - The cache holds the PROMISE rather than the resolved bundle, so two files of
     one language asking at the same moment share one import.
5. TWO ADDITIONS INSIDE C6 BEYOND S6'S FOUR BULLETS, both to keep an existing
   guard from going blind on this round's own code.
   - `exported_names` matched `^export (?:function|const)` only, so
     `export async function loadDiffLanguageBundle` would have been the one export
     `test_every_exported_name_is_named_by_the_vitest_suite` could not see. The
     pattern now also matches `async function`; the scan finds 17 names, the new
     one among them.
   - The module docstring listed THREE things vitest is blind to and said "any of
     the three below". C6 adds three guards of new classes, so the numeral was
     about to be false: it now reads "any of the classes below" and carries three
     more bullets, one per new guard. This is the same class of repair as item 3
     of the staleness sweep — a claim the round's own change breaks.
6. THE MOCKING-TOKEN GUARD READS RAW TEXT, comments included, unlike S6's first
   bullet which is explicitly comment-stripped. That is deliberate and stated in
   the guard's docstring: constraint 5 forbids those three spellings ANYWHERE, and
   a comment reaching for one is drift toward the arrangement the guard prevents.
   The C5 test-helper comment was therefore written without naming the tokens.
   Each new scoper carries its own vacuity assertion, and both new text scanners
   additionally carry a planted-control assertion proving they are not blind.
7. `.agent/plan.md` still carries the item-status table the PLANF037R22 slice
   ordered, in which every item reads `ordered`. It was applied byte for byte at
   C1 and the block does not order a second write of it, so the round's real
   item status is the table below rather than the plan's.
8. G8's marker sweep says "0 in every edited target". `.agent/last_block.md` is an
   edited target AND a byte-for-byte mirror of the block, so it necessarily
   carries the block's 8 marker lines. It is reported as a second NON-ZERO control
   beside the C0a blob, which is how F037 R21's own sweep read it. This is a
   wording tension in the gate, not a leak, and no marker reached any of the five
   real targets.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C6b | deviated | not ordered; the one-line repair of a comment C4/C5 falsified, see Deviations 1 |
| C7 | done | this file |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | |
| G7 | done | re-run at `b94a4bc9` for the three gates C6b could touch |
| G8 | done | marker sweep reported with `.agent/last_block.md` as a control, see Deviations 8 |

## Next

Review `665be6ef..b94a4bc9`: the language rule and the lazy bundle loader in
`apps/ui/src/api/diffViewModel.ts`, their 17 vitest cases, the three new guards
in `tests/ui_contracts/test_diff_view_model.py`, and the unordered comment
commit `b94a4bc9`. `R-0729` and `R-0730` are registered and their repairs have
landed, so both are candidates for a `Done:` line once the repaired text has been
read. The next round's work is the WIRING of highlighting into `DiffView` plus
the 10k-line perf fixture measured end to end; the sidebar's visual treatment is
still owed a ruling. Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
