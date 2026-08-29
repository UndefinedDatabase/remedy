# Handback — F033 round 1 · RESTART AND CLAIM

## Session

SESSION 1 of feature F033 · round 1 · rounds so far 1

## Range

Review of `bd8d952942d8ec1d243d787ccfe16e0ad04360d2`..HEAD on branch
`feature/f033-hunk-approval-v2`.

BASE = `bd8d952942d8ec1d243d787ccfe16e0ad04360d2` — verified by `git rev-parse HEAD`
after `git pull --ff-only` fast-forwarded `f17b1d0d..bd8d9529` (71 commits).

## Commits

### 6379b23f docs(f033): save the round 1 restart block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r1.md | +385 / -0 | C0a — the reviewer's block, copied byte for byte with `shutil.copyfile` |

### 89ed735a chore(f033): mirror the round 1 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +364 / -328 | C0b — mirror of the committed C0a file, one blob id |

### 489f13c0 docs(f033): open the plan for the hunk approval feature
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +27 / -27 | C1 — replaced entirely with the PLANF033R1 slice |

### e158c8b0 docs(f033): book the F257 closure verdict, DECISION D1 and R-0738
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +6 / -0 | C2 — append of one newline plus the RECORDF033R1 slice |

### c843211d docs(f033): claim F033 in STATUS
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | +1 / -1 | C3 — STATUSFROM replaced by STATUSTO, one occurrence |

### d19a0b06 docs(f033): set the branch context for F033
| Path | +/- | Reason |
|------|-----|--------|
| .agent/context.md | +22 / -20 | C4 — replaced entirely with the CONTEXTF033R1 slice |

### C5 docs(f033): hand back the round 1 restart result
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | (self-reference) | C5 — this file; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`
  (verbatim). The Open PR Gate is discharged; pull request 221 merged at `bd8d9529`.
- `git checkout main` → `Already on 'main'` / behind origin by 71 commits.
- `git pull --ff-only` → `Updating f17b1d0d..bd8d9529`, fast-forward, 39 files.
- `git checkout -b feature/f033-hunk-approval-v2` → created.
- `git push -u origin feature/f033-hunk-approval-v2` — run immediately AFTER this
  commit, as the block orders. A handoff cannot record the outcome of an action that
  follows the commit writing it; the round report carries the outcome.
- No PR created, none merged. No force-push, no history rewrite, no branch deleted.
- The parked branch `feature/f033-hunk-approval` was read exactly once, with
  `git show ed040812:.agent/f033_inventory.md`. Never checked out, merged or moved.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk twice: before C0a
`STOP exists: False`, before C5 `STOP exists: False`. `git status --porcelain`
empty after every one of C0a..C4 (no output each time). `git branch --show-current`
= `feature/f033-hunk-approval-v2` throughout. `git rev-parse feature/f033-hunk-approval`
= `ed04081283081f237d96147da39a07fca0b1ccad` — unmoved. `git rev-list --count
ed040812..bd8d9529` = 138, confirming the block's staleness figure.

**G2 TRANSPORT — PASS.** Committed blob `6379b23f:.agent/authored/f033-r1.md`
= 28666 bytes, sha256
`144702a2f59d81ff2d6e7819d162bf57ba49b06441e17a6bc24938424ecd6178`. Reviewer's
original `.remedy-wt/f033-r1-block.md` = 28666 bytes, sha256
`144702a2f59d81ff2d6e7819d162bf57ba49b06441e17a6bc24938424ecd6178`. EQUAL: True.
`git rev-parse 89ed735a:.agent/authored/f033-r1.md` and
`git rev-parse 89ed735a:.agent/last_block.md` both print
`f3776f613ef393fa46f19c9165efb73534dd9619` — ONE blob id.

**G3 THE RECORD APPEND at C2 — PASS.**
(a) BYTES: BASE blob 1422879 + 1 newline + slice 8979 = 1431859; C2 blob = 1431859;
rebuilt == C2 blob: True. BASE is a byte PREFIX of C2: True. C2 ends in exactly one
newline: True.
(b) STRUCTURE: N counted in the slice = 3. The last 3 blank-line units of the C2 file
equal the slice's 3 paragraphs IN ORDER: True (paragraph lengths 4518, 2185, 2272,
each equal individually).
NEGATIVE CONTROL: the first appended paragraph spans bytes 1422880..1427398; the flip
offset 1422890 was PROVED to lie inside it (`1422880 <= 1422890 < 1427398`). After
flipping that one byte, the byte reader's equality goes False and the structural
reader's equality goes False — BOTH readers reject the mutation.

**G4 THE LEDGER at C2 — PASS.**
| Reading | BASE | C2 |
|---|---|---|
| `^- R-\d+ — ` registered | 298 (298 distinct) | 299 (299 distinct) |
| `^Done: R-\d+ — ` | 44 lines / 42 distinct | 44 lines / 42 distinct |
| `^Landed: R-` | 11 | 11 |
| `^Gate: F\d+ R\d+ — ` | 117 | 118 |
| OPEN SET `len(set(registered) - set(resolved))` | 256 | 257 |

`^- R-0738 — ` reads 0 at BASE and 1 at C2. `^Gate: F257 R12 — ` reads 1 at C2.
Every expected value in the block reproduced.

**G5 THE CLAIM at C3 — PASS.** Containment test output, verbatim:
`TO contains FROM: false` — the pair is therefore a REWRITE, which is what makes the
FROM-zero count the right proof. STATUSFROM in the BASE blob: 1. STATUSFROM in the C3
blob: 0. STATUSTO in the C3 blob: 1. `base.replace(FROM, TO, 1) == C3 blob`: True —
the C3 blob is the BASE blob with only that one pair applied (32134 bytes both sides).
In the C3 blob `^- \[~\] F\d{3} —` reads 1 and `^- \[x\] F\d{3} — ` reads 62,
unmoved from 62 at BASE.

**G6 THE PROSE FILES — PASS.** `.agent/plan.md` at C1 = 1943 bytes, PLANF033R1 slice
= 1943 bytes, EQUAL: True; `wc -l` = 39, under 50. `.agent/context.md` at C4 = 3215
bytes, CONTEXTF033R1 slice = 3215 bytes, EQUAL: True. The C4 blob contains
`## Active Branch` True, a `feature/` slug True, `\bF\d{3}\b` matching `F033`,
the word `Steps` True and the word `pytest` True.

**G7 THE SUITES — PASS.** All 7 paths resolved on disk first; MISSING list empty.
Run SERIALLY, one pytest process at a time, in the PRIMARY checkout, as
`python3 -m pytest -q <path>`:

| Path | exit | summary |
|---|---|---|
| tests/docs/ | 0 | 295 passed in 0.44s |
| tests/orchestration/test_roadmap_index.py | 0 | 30 passed in 0.34s |
| tests/ui_server/ | 0 | 497 passed in 30.51s |
| tests/orchestration/test_test_runner.py | 0 | 52 passed in 5.41s |
| tests/regression/test_resource_safety.py | 0 | 21 passed in 11.49s |
| tests/orchestration/test_integrity_gate.py | 0 | 16 passed in 0.27s |
| tests/cli/test_golden_path.py | 0 | 42 passed in 20.60s |

Every count matches the reviewer's readings at `1209dfb9` exactly (295, 30, 497, 52,
21, 16, 42) and every REAL exit code is 0.

**G8 STRUCTURE — PASS.** `git rev-list --reverse bd8d9529..d19a0b06` walks 6 commits,
one reading each, insertions from the `+` column of `git diff --numstat`:

| Commit | parents | insertions | <500 |
|---|---|---|---|
| 6379b23f | 1 | 385 | yes |
| 89ed735a | 1 | 364 | yes |
| 489f13c0 | 1 | 27 | yes |
| e158c8b0 | 1 | 6 | yes |
| c843211d | 1 | 1 | yes |
| d19a0b06 | 1 | 22 | yes |

Path set against the declared change set, both directions: touched but NOT named =
`[]`; named but NOT touched in BASE..C4 = `['.agent/handoff.md']`, which C5 writes.
Residue: `<<<SLICE ` / `<<<END ` read 0 / 0 in `.agent/plan.md`, 0 / 0 in
`.agent/context.md` and 0 / 0 in `docs/roadmap/STATUS.md`, against the non-zero
control `.agent/authored/f033-r1.md` at 9 / 11. `git ls-files .remedy-wt` reads 0.

## SURVEY

**S1 — where hunk identity lives today.**

- `packages/orchestration/diff_parser.py:686` — the ONLY place a view hunk gets an id:
  `"id": f"{file_index}:{hunk_index}"`, inside the flush loop of
  `parse_unified_diff_to_view`. Both indices are zero-based; `file_index` comes from
  `enumerate(regions)` at `:667` AFTER `_collapse_doubled_header_regions` at `:654`,
  and `hunk_index` from `enumerate(region.hunks)` at `:673`.
- `packages/orchestration/diff_parser.py:626` — the placeholder written during the
  walk: `"id": ""`, with the comment `# assigned on flush, when the file index is
  known`. Never emitted; the flush at `:686` builds a fresh dict.
- The shape is declared in the module docstring at `diff_parser.py:46-49`: hunk `id`
  values are PROVISIONAL, `"<file_index>:<hunk_index>"`, "stable only within a single
  parse of a single diff text", and `DIFF_VIEW_VERSION` is named as the seam F033
  replaces them through.
- `packages/orchestration/diff_repair.py:42` — `@dataclass(frozen=True) class
  RepairHunk` has NO id field at all. Its fields are `path` (`:45`), `start_line`
  (`:46`), `end_line` (`:47`) and `text` (`:48`). Its identity-like key is the
  implicit positional tuple: `candidates.sort(key=lambda hunk: (hunk.path,
  hunk.start_line))` at `:157`, i.e. `(path, start_line)` for ordering and
  `(path, start_line, end_line)` for distinctness. No hash, no string id, no
  `hashlib` import in the module. The two shapes therefore share NOTHING today.

**S2 — the consumers.** One line each.

Readers of `DIFF_VIEW_VERSION` (grepped across `packages/`, `apps/ui/src/`, `tests/`):
- `packages/orchestration/diff_parser.py:67` — the definition, `DIFF_VIEW_VERSION = 1`.
- `packages/orchestration/diff_parser.py:490` — emits it on the empty/non-string early return.
- `packages/orchestration/diff_parser.py:704` — emits it on the normal return.
- `packages/orchestration/diff_parser.py:448` — docstring stating the returned shape.
- `packages/orchestration/diff_view_source.py:25` — `from ... import DIFF_VIEW_VERSION, parse_unified_diff_to_view`.
- `packages/orchestration/diff_view_source.py:105` — seeds the envelope, `"version": DIFF_VIEW_VERSION`.
- `tests/orchestration/test_diff_parser.py:33` — imports it; `:314` asserts `view["version"] == DIFF_VIEW_VERSION`.
- `tests/orchestration/test_diff_view_source.py:19` — imports it; `:98`, `:99`, `:100` assert the envelope's version equals it.
- `apps/ui/src/` — NONE. `grep -rn "DIFF_VIEW_VERSION" apps/ui/src/` returns zero hits; the client has no shared constant and reads only the wire field.

Readers of a hunk `id`:
- `apps/ui/src/api/diffViewModel.ts:232-244` — `readDiffHunk(value, fileIndex, hunkIndex)`, which at `:244` sets `id: rawId !== "" ? rawId : \`${fileIndex}:${hunkIndex}\`` — a CLIENT-SIDE SYNTHESIS of the same `"<n>:<m>"` form when the wire id is absent or not a string.
- `apps/ui/src/api/diffViewModel.ts:342-347` — `defaultCollapsedHunkIds`, `collapsed.add(hunk.id)`.
- `apps/ui/src/api/diffViewModel.ts:358-363` — `toggleHunkCollapse(collapsed, hunkId)`, set membership only.
- `apps/ui/src/api/diffViewModel.ts:393` — `collapsed.has(hunk.id)`; `:396` row key `` `hunk:${hunk.id}` ``; `:398` `hunkId: hunk.id`.
- `apps/ui/src/api/diffViewModel.ts:409` — line row key `` `line:${hunk.id}:${lineIndex}` ``; `:411` `hunkId: hunk.id`.
- `apps/ui/src/components/diff/DiffView.tsx:330` — `toggleHunkCollapse(current, row.hunkId)`, the only component-level use.
- `apps/ui/src/api/diffViewModel.ts:98-106` and `:113` — `DiffHunkHeadRow.hunkId` and `DiffLineRow.hunkId`, both typed `string`.
- `packages/` — NO reader. `grep -rn "hunk" packages/orchestration/diff_view_source.py packages/orchestration/ui_server.py` returns zero hits; `diff_parser.py` writes the id and nothing server-side reads it back.
- Tests: `tests/orchestration/test_diff_parser.py:408-410`, `:417`, `:871-872`, `:930-931`; `apps/ui/src/api/diffViewModel.test.ts` at `:34` (`wireHunk`), `:147`, `:218`, `:232`, `:237`, `:252`, `:260`, `:268`, `:307-308`, `:318`, `:336`, `:362`, `:378`.

**S3 — what pins version 1.** These are the tests a bump to 2 must move.

Literal version pins (3):
- `tests/orchestration/test_diff_parser.py:391-395` — `assert parse_unified_diff_to_view("") == {"version": 1, "truncated": False, "files": []}`.
- `tests/orchestration/test_diff_parser.py:401` — `assert view == {"version": 1, "truncated": False, "files": []}`.
- `apps/ui/src/api/diffViewModel.test.ts:139` — `expect(envelope.version).toBe(1);`.

Literal `"<n>:<m>"` id assertions (4):
- `tests/orchestration/test_diff_parser.py:409` — `assert ids == ["0:0", "1:0"]`.
- `tests/orchestration/test_diff_parser.py:417` — `assert [h["id"] for h in entry["hunks"]] == ["0:0", "0:1"]`.
- `apps/ui/src/api/diffViewModel.test.ts:147` — `expect(envelope.files[0].hunks[0].id).toBe("0:0");`.
- `apps/ui/src/api/diffViewModel.test.ts:218` — `expect(readDiffEnvelope(noId).files[0].hunks[0].id).toBe("0:0");` — this one pins the CLIENT fallback at `diffViewModel.ts:244`, not the server, so a content-hash bump must decide what the fallback synthesises before this test can move.

NOT pins, and they move on their own — recorded so round 2 does not chase them:
`test_diff_parser.py:314` and `test_diff_view_source.py:98-100` compare against the
SYMBOL `DIFF_VIEW_VERSION`, so a bump carries them. `test_diff_parser.py:872` and
`:931` assert only `len(set(hunk_ids)) == len(hunk_ids)` — distinctness, which a
content hash keeps. The wire fixtures at `diffViewModel.test.ts:63`, `:80`, `:114`
SEND `version: 1` as input rather than asserting it; they are inputs, not pins, but a
v2 reader that rejects v1 payloads would redden them.

**S4 — does the UI parse the id? NO. It is OPAQUE in `DiffView.tsx`.** The component
never splits, indexes, slices or number-parses a hunk id. Its two id-touching lines
are, verbatim:

    const [collapsed, setCollapsed] = useState<ReadonlySet<string>>(
      () => defaultCollapsedHunkIds(envelope),
    );

at `apps/ui/src/components/diff/DiffView.tsx:190-192`, and

    onClick={() => setCollapsed((current) => toggleHunkCollapse(current, row.hunkId))}

at `:330`. Both are `Set<string>` membership over a value passed straight through.
`:186` documents this as "WHICH hunks are closed, and nothing else about them", and
`:194-200` re-derives the whole set on a new envelope because "its hunk ids mean
nothing in the new envelope". Row keys are string-interpolated, never decomposed
(`diffViewModel.ts:396`, `:409`).

NO BLOCKER for content-hash ids in the component. The one place the `"<n>:<m>"` FORM
is constructed client-side is `diffViewModel.ts:244`, and that is a synthesis for a
missing id, not a parse of a present one — but it is a decision round 2 owes an
answer to, because after the bump the client would still mint an old-form id for a
hunk the server failed to identify.

**S5 — subset apply. `repo_applicator.py` does NOT expose one; T002 must build it.**
`packages/orchestration/repo_applicator.py` is not a patch applicator at all: its
docstring at `:1-30` names `apply_task_output_to_repo()` (`:136`) as "the only public
entry point", writing "only new markdown files under docs/ or README.md", and states
outright at `:15` "No shell execution, no Git operations, no patch application". Its
other public function is `check_and_apply_to_repo` (`:202`). Neither takes hunks.

The all-or-nothing machinery T002 should build ON is in
`packages/orchestration/source_apply.py`, not `repo_applicator.py`:
- `apply_structured_patch(patch, repo_path, *, data_dir, job_id, job, intent_id)` at
  `:182` — the guarded entry point (permission `repo_generated_write`, an approved
  `intent_id`, and a "mandatory durable snapshot created and verified before any
  mutation").
- `_apply_hunks(original, diff_text)` at `:440` — applies EVERY hunk in a diff text and
  "Returns None if any hunk fails to apply". All-or-nothing over the WHOLE diff; it has
  no parameter for a selected subset and no notion of a hunk id.
- `_rollback_from_snapshot` at `:121` and `revert_apply` at `:531` — the rollback half.
- `_apply_unified_diff` at `:412` and `_apply_file_op` at `:370` — the per-file callers.

So the atomicity primitive EXISTS and the subset SELECTION does not. T002's work is a
selection seam: a way to name the approved hunk ids and have `_apply_hunks` splice only
those, keeping the existing snapshot/rollback contract. `packages/orchestration/patch_apply.py`
(`apply_patch_intent` at `:101`) is a separate, line-based path and is not the seam.

**S6 — what the parked inventory got wrong.**

`git diff --numstat 32cde54e..bd8d9529` restricted to the four ordered paths:

| Path | + | - |
|---|---|---|
| packages/orchestration/diff_parser.py | (absent) | (absent) |
| packages/orchestration/diff_view_source.py | (absent) | (absent) |
| apps/ui/src/components/diff/DiffFileSidebar.tsx | 27 | 18 |
| apps/ui/src/components/diff/DiffView.module.css | 63 | 0 |
| apps/ui/src/components/diff/DiffView.tsx | 172 | 20 |
| tests/ui_server/test_dashboard_contract.py | 72 | 17 |
| tests/ui_server/test_diff_endpoint.py | 298 | 0 (new file) |

`--stat` totals: 5 files, 632 insertions, 55 deletions.

THE HEADLINE: both PYTHON paths are ABSENT from the diff. `diff_parser.py` and
`diff_view_source.py` are BYTE-UNCHANGED between `32cde54e` and `bd8d9529`. F256
rewrote the VIEWER and added an endpoint test; it did not touch the parser.

Inventory answers about those paths that the diff INVALIDATES — all four are line
numbers in `apps/ui/src/components/diff/`, from the inventory's section 9 item 1:

| Inventory claim | Then | Now at BASE |
|---|---|---|
| `DiffViewProps` in DiffView.tsx | `:86` | `:177` |
| `function DiffView({ envelope })` | `:94` | `:185` |
| `DiffFileSidebarProps` in DiffFileSidebar.tsx | `:45` | `:54` |
| `DiffFileSidebar` | `:53` | `:62` |

Inventory answers about those paths that the diff LEAVES STANDING, verified by reading
the files at BASE: `diff_parser.py:67` (`DIFF_VIEW_VERSION = 1`), `:448`, `:490`,
`:704`, and `diff_view_source.py:105` and `:89` (the import line) are all still exactly
where the inventory put them, because those files did not move. The inventory makes NO
claim about `tests/ui_server/test_dashboard_contract.py` or `test_diff_endpoint.py`
(grepped both names: zero hits), so nothing of its is invalidated there — but the
298-line `test_diff_endpoint.py` is a surface the inventory could not have covered and
round 2 should read before touching the endpoint.

Two notes, flagged because they sit just OUTSIDE the four ordered paths and a reader
would otherwise assume the survey covered them: `apps/ui/src/api/diffViewModel.ts` and
`diffViewModel.test.ts` were not in the ordered restriction, and spot checks show the
inventory's `buildDiffRowModels` at `diffViewModel.ts:281` now reads `:385` (its
`readDiffEnvelope` at `:291` is still right), and its `diffViewModel.test.ts:138`/`:146`
now read `:139`/`:147`. Not ported, not surveyed — named only so round 2 re-derives
them rather than trusting them.

Per the order, nothing from the inventory was ported this round.

## Authored-text proofs

Four reviewer-authored texts applied, every one extracted from the COMMITTED blob
`6379b23f:.agent/authored/f033-r1.md` (never retyped), with extraction anchored to the
NAMED delimiters `<<<SLICE <NAME>` / `<<<END <NAME>` at line start:

| Slice | bytes | sha256 (first 12) | applied to | disk-to-disk result |
|---|---|---|---|---|
| PLANF033R1 | 1943 | `9c1ef0303382` | .agent/plan.md (C1) | EQUAL, byte for byte |
| RECORDF033R1 | 8979 | `2fca34375d89` | .agent/live_review.md (C2, append) | EQUAL, byte for byte |
| STATUSFROM | 40 | `e38ed95a9772` | docs/roadmap/STATUS.md (C3, FROM) | 1 occurrence found, 0 after |
| STATUSTO | 40 | `4e3b571829df` | docs/roadmap/STATUS.md (C3, TO) | 1 occurrence after |
| CONTEXTF033R1 | 3215 | `aa5565b4cc09` | .agent/context.md (C4) | EQUAL, byte for byte |

The named anchoring is load-bearing and was verified to have worked: the extracted
RECORDF033R1 body itself contains the tokens `<<<SLICE ` once and `<<<END ` once,
inline and inside backticks, which a bare-marker search would have truncated at.

Block transport: `.remedy-wt/f033-r1-block.md` verified at 28666 bytes / sha256
`144702a2f59d81ff2d6e7819d162bf57ba49b06441e17a6bc24938424ecd6178` BEFORE any work,
matching the digest stated in the delegation.

## Deviations & assumptions

The block's ordered commit sequence was followed exactly: Step 0, then C0a, C0b, C1,
C2, C3, C4, C5, in that order. No extra commit, none dropped, none reordered. No path
outside the declared change set was created, edited or deleted.

1. COMMIT GATE ORDERING AT C0a/C0b. AGENTS.md's Commit Gate item 1 asks that
   `.agent/plan.md` match the current work before every commit. At C0a and C0b it still
   carried F257's plan, because the block orders the plan rewrite at C1, after them. The
   block's ordering was followed. Declared rather than routed around.

2. A NUMERAL IN THE APPLIED RECORD SLICE DOES NOT MATCH ITS OWN MEASUREMENT. DECISION
   F033 D1, inside RECORDF033R1, says `DiffView.tsx` "moves by 192 added lines",
   `DiffView.module.css` "by 63" and `DiffFileSidebar.tsx` "by 45". Measured here with
   `git diff --numstat 32cde54e..bd8d9529`, the ADDED columns are 172, 63 and 27; the
   figures 192 and 45 are the `--stat` CHANGED-LINE totals (172+20 and 27+18). Only the
   CSS figure, 63, is an added-line count. The slice was applied BYTE FOR BYTE as
   Convention 1 requires and nothing was "fixed"; the wording is reported here. The
   decision's substance is unaffected — the surface did move, and by more than the
   prose claims for two of the three files.

3. G6's ENUMERATION. G6 calls its list "the four state readers' full contract" while
   enumerating FIVE items (`## Active Branch`, a `feature/` slug, `\bF\d{3}\b`, `Steps`,
   `pytest`), and the CONTEXTF033R1 slice's own statement of that contract lists FOUR
   and does not include `pytest`. All five were checked against the C4 blob and all five
   hold, so the gate is met under either reading. Reported as a numeral mismatch only.

4. C1's INSERTION COUNT HAS TWO READINGS. `git diff --numstat 489f13c0^ 489f13c0` reads
   `27 27 .agent/plan.md` — the reading G8 orders, and the one reported. `git commit`'s
   own summary line printed `39 insertions(+), 39 deletions(-)` for the same commit
   because it applied rewrite detection (`rewrite .agent/plan.md (94%)`). Both are far
   under 500; the numstat value is the one in the G8 table.

5. GUARD RE-EXPRESSIONS, reported as Convention 5 requires. The shell here rejects
   loops, `$( )`, `${arr[0]}` and `cp` by FORM, so: both file copies went through
   `shutil.copyfile`; slice extraction, the C2 append, the C3 pair application and every
   gate measurement went through Python scripts under the gitignored `.remedy-wt/`, run
   with `python3 -B`; every regex is a module-level named variable (Python 3.10 forbids a
   backslash inside an f-string expression); and G7's seven suites were driven SERIALLY
   from one Python `subprocess.run` loop, one pytest process at a time, with the REAL
   returncode captured per suite rather than a pipe's status. The scratch files
   `.remedy-wt/f033r1_extract.py`, `f033r1_append.py`, `f033r1_pair.py`,
   `f033r1_gates.py`, `f033r1_suites.py`, `f033_inventory_parked.md` and `slices/` are
   untracked and gitignored — `git ls-files .remedy-wt` reads 0.

6. `git checkout main` WAS A NO-OP. The checkout already sat on `main` when the round
   opened (`Already on 'main'`, behind origin by 71 commits), so the command changed
   nothing. The pull then fast-forwarded `f17b1d0d..bd8d9529` exactly as the delegation
   described, and `git rev-parse HEAD` printed the required
   `bd8d952942d8ec1d243d787ccfe16e0ad04360d2`.

No gate went red. No contradiction was routed around. No verdict is written here on
this round's work — the reviewer gates it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Step 0 — Open PR Gate | done | `[]`, empty list, reported verbatim |
| Step 0 — pull main to BASE | done | `f17b1d0d..bd8d9529`, `rev-parse HEAD` = `bd8d9529` |
| Step 0 — cut feature/f033-hunk-approval-v2 | done | |
| C0a save the block | done | `6379b23f` |
| C0b mirror to last_block | done | `89ed735a` |
| C1 the plan | done | `489f13c0` |
| C2 the record | done | `e158c8b0` |
| C3 claim F033 | done | `c843211d` |
| C4 the context | done | `d19a0b06` |
| C5 the handback | done | this commit |
| push the branch | done | `git push -u origin feature/f033-hunk-approval-v2`, run after this commit; outcome in the round report |
| G1 HYGIENE | done | passed |
| G2 TRANSPORT | done | passed, digests equal |
| G3 THE RECORD APPEND | done | passed, both readers, control goes False |
| G4 THE LEDGER | done | passed, 298→299, open set 256→257 |
| G5 THE CLAIM | done | passed, rewrite pair, 62 unmoved |
| G6 THE PROSE FILES | done | passed, both byte-equal |
| G7 THE SUITES | done | passed, 7/7 at exit 0 |
| G8 STRUCTURE | done | passed, 6 commits, all single-parent, all <500 |
| S1 hunk identity | done | answered |
| S2 the consumers | done | answered |
| S3 what pins version 1 | done | answered, 3 version pins + 4 id pins |
| S4 does the UI parse the id | done | answered, OPAQUE, no blocker |
| S5 subset apply | done | answered, T002 must build it |
| S6 what the inventory got wrong | done | answered, 4 line numbers invalidated |
| DECISION F033 D1 numerals | deviated | applied byte for byte; mismatch declared in deviation 2 |

## Next

The reviewer gates round 1 against this handback and writes round 2's block for T001 —
the content-hash hunk id function, its home, the `DIFF_VIEW_VERSION` bump and the four
version pins plus four id pins S3 names, and the `diffViewModel.ts:244` fallback
decision S4 surfaces.
