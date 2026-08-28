# Handback — F037 R14

## Session

SESSION 4 of feature F037 · round 14 · rounds so far 14

## Range

Review of `922f3223`..`HEAD` (branch `feature/f037-rendered-diff-viewer`).

## Commits

### 735a0860 docs(agent): save the F037 R14 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r14.md` | +419/-0 | C0a: the block file's bytes saved verbatim |

### 1c4034dc docs(agent): mirror the F037 R14 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +333/-353 | C0b: same bytes, one git blob with the saved copy |

### d353c697 docs(agent): set the F037 R14 plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +23/-23 | C1: PLANF037R14 applied byte for byte |

### 33cce53b docs(agent): book the F037 R13 gate verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C2: GATER13 appended |

### 6be5b573 feat(orchestration): bound the diff artifact read with DECISION F037 D7
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +76/-0 | C3: DECISION7 appended |
| `packages/orchestration/diff_view_source.py` | +40/-3 | C3: SPEC S1–S4 — the ceiling, the bounded read, the newline cut, the OR flag |

### c9e7a866 test(orchestration): pin the read ceiling and both of its cut hazards
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_diff_view_source.py` | +202/-1 | C4: SPEC S5–S11 — six tests and two helpers, appended |

### 48da5345 docs(agent): resolve the remaining half of R-0721
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C5: DONE0721B appended, after C3 and C4 as constraint 9 requires |

### C6 (this commit) docs(agent): hand back F037 R14
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C6: this handback. A handoff cannot table the commit that writes it (R-0149 pattern). |

## External actions

- `git worktree add --detach .remedy-wt/f037-r14-redproof c9e7a866` — created, HEAD `c9e7a866bdf8b4052851bbbd1d3be38dff2cf1f2`; every G6 mutation ran there.
- `git worktree remove --force .remedy-wt/f037-r14-redproof` — removed; `git worktree list` holds only the primary checkout afterwards.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, stdout `[]`. No open PR, so the Open PR Gate is passed with nothing to merge.
- `git push` of `feature/f037-rendered-diff-viewer` after C6. No PR created, nothing merged.

## Verification

**G1 HYGIENE.** `.agent/STOP` read from disk before C0a: ABSENT. Read again before C6:
ABSENT. `git rev-parse HEAD` before C0a: `922f3223d16ca2b317d8e910b38d893d6e45e4e5`,
which EQUALS the block's base `922f3223`. `git branch --show-current`:
`feature/f037-rendered-diff-viewer`. `git status --porcelain` line count after each of
C0a, C0b, C1, C2, C3, C4, C5: `0`, `0`, `0`, `0`, `0`, `0`, `0`.

**G2 TRANSPORT, ONE DIGEST COMPARISON.** Committed `.agent/authored/f037-r14.md` at
`HEAD:` — sha256 `19ac258925457ddf3b82dcd29751ae49e72854b8ba10cdf03c572025df09e6fc`,
32272 bytes, 419 lines. The reviewer's scratch original `.remedy-wt/f037-r14-block.md`
reads sha256 `19ac2589…e6fc`, 32272 bytes, 419 lines: ALL THREE READINGS EQUAL, compared
disk to disk as whole byte strings (`committed == scratch == on-disk copy` is True), not
merely digest to digest. `git rev-parse 1c4034dc:.agent/authored/f037-r14.md` and
`git rev-parse 1c4034dc:.agent/last_block.md` are BOTH `af7b2387e3c27925a085f7e1737e6b4a77c5d44b`
— ONE blob. WHAT THE CHAIN COVERS: the bytes the reviewer measured before delegating are
the bytes on disk and in both committed copies, so nothing was lost, reflowed or repaired
between the scratch file and the commit. WHAT IT DOES NOT COVER: it says nothing about the
bytes of the delegation message itself, and nothing about whether the SPEC was read
correctly — only S-by-S review of the code can say that.

**G3 EXTRACTION AND CAPS**, measured on the COMMITTED C0a blob, never on prose.
Content lines: PLANF037R14 **49**, GATER13 **1**, DECISION7 **75**, DONE0721B **1**.
TOTAL 419 · CONTENT 126 · PROSE 293. TOTAL ≤ 490: **True**. PROSE ≤ 400: **True**.

**G4 THE PLAN AT C1.** `.agent/plan.md` is byte-equal to the PLANF037R14 slice extracted
from the committed C0a blob, trailing newline included: **True**. Negative control against
that slice minus its trailing newline: **False**. Lines exactly `## Goal`: 1. Lines exactly
`## Next Steps`: 1. `wc -l` 49, strictly under 50: **True**.

**G5 THE RECORD AT C2 AND C5.**

| Append | reader (a) `before + b"\n" + slice` | reader (b) units | reader (b) last-N in order | neg (a) | neg (b) |
|---|---|---|---|---|---|
| GATER13 → `.agent/live_review.md` | True | 1 | True | False | False |
| DECISION7 → `.agent/decisions.md` | True | 10 | True | False | False |
| DONE0721B → `.agent/live_review.md` | True | 1 | True | False | False |

Both negative controls flip ONE byte inside the FIRST appended paragraph and both readers
turn False for all three appends. Pre-round blobs read with `git show 922f3223:<path>` into
memory, never over the tracked file: `.agent/live_review.md` 1209025 → 1216213 and
`.agent/decisions.md` 668900 → 673728, each base a byte PREFIX of its result — **True**
for both, so nothing landed was rewritten.

Line-anchored over `.agent/live_review.md` after C5, base figure first:
`^- R-\d+ — ` **283 → 283** (this round registers nothing); `^Done: R-\d+ — ` **31 → 32**;
`^Landed: R-` **1 → 1**, unmoved; `^Gate: F\d+ R\d+ — ` **83 → 84**; OPEN SET **252 → 252**,
unmoved — and that is the arithmetic's own point: `R-0721` already counted as resolved, which
is exactly why the remaining half survived in prose only. Every REGISTERED id is distinct:
283 ids, 283 distinct, **True**. The RESOLUTION lines are NOT distinct and are not expected
to be: **32** `^Done: R-\d+ — ` lines carrying **31** distinct ids; the repeating id is
**`R-0721`**, DONE0721B being its second resolution paragraph by design, and constraint 1
forbids repairing that by editing either paragraph. Over `.agent/decisions.md`:
`^## DECISION ` **173** headings, and `F037 D7` appears **exactly once**.

**G6 THE RED-PROOFS OF THE READ BOUND.** All runs inside the disposable worktree
`.remedy-wt/f037-r14-redproof` at the C4 tree `c9e7a866`, never in the primary checkout,
with `__pycache__` purged before every run and `python3 -B` throughout. Unmutated module
sha256 `35ee01c1c8acf21b1b142cff8a2065ab39db4c4ed4ec51f088d7c7a5e97b6644`; the module was
restored after every mutation and re-hashed to that same digest each time, and the
worktree's own `git status --porcelain` was 0 lines at the end. The ordered property is the
COLOUR; the names and counts below are measured, not predicted.

| Run | occurrences before the edit | REAL exit | summary |
|---|---|---|---|
| CONTROL (unmutated) | — | **0** | `15 passed in 0.27s` |
| (a) bounded read → `artifact.read_text(encoding="utf-8")`, `read_truncated` dropped from the flag | 1 and 1 | **1** RED | `4 failed, 11 passed in 0.30s` |
| (b) `>` → `>=`, so exactly the ceiling counts as truncated | 1 | **1** RED | `1 failed, 14 passed in 0.29s` |
| (c) the cut back to the last newline dropped, the cut at the ceiling kept | 1 | **1** RED | `2 failed, 13 passed in 0.30s` |
| (d) `parsed["truncated"] or read_truncated` → `parsed["truncated"]` | 1 | **1** RED | `4 failed, 11 passed in 0.30s` |
| (e) the same → `read_truncated` alone | 1 | **1** RED | `1 failed, 14 passed in 0.29s` |

Failing node ids, all under `tests/orchestration/test_diff_view_source.py`:

- (a) 4: `test_the_read_ceiling_boundary_holds_on_both_of_its_sides`,
  `test_the_cut_never_hands_the_parser_a_partial_line`,
  `test_the_cut_never_splits_a_multi_byte_character`,
  `test_one_enormous_line_is_bounded_though_it_reaches_neither_parser_ceiling`.
- (b) 1: `test_the_read_ceiling_boundary_holds_on_both_of_its_sides` — exactly the boundary test.
- (c) 2: `test_the_cut_never_hands_the_parser_a_partial_line`,
  `test_the_cut_never_splits_a_multi_byte_character` — exactly the two cut hazards.
- (d) 4: the same four as (a), which is expected because (a) contains (d)'s edit.
- (e) 1: `test_the_parsers_own_truncation_still_reaches_the_envelope` — exactly the OR
  discriminator, and the only mutation it can see.

**G7 SUITE, LINT AND CANARY AT C4.** One pytest process at a time; the four ran serially.

| Command | REAL exit | summary | base at `922f3223` |
|---|---|---|---|
| `python3 -m pytest tests/orchestration/test_diff_view_source.py -q` | **0** | `15 passed in 0.26s` | `9 passed in 0.21s` |
| `python3 -m pytest tests/orchestration/test_diff_parser.py tests/ui_server/test_diff_endpoint.py -q` | **0** | `49 passed in 3.01s` | `49 passed` — UNMOVED |
| `python3 -m ruff check packages/orchestration/diff_view_source.py tests/orchestration/test_diff_view_source.py` | **0** | `All checks passed!` | — |
| `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | **0** | `42 passed in 20.62s` | `42 passed` — UNMOVED |

The view-source suite's `in <n>s` figure moved `0.21s` → `0.26s`. Measured with
`--durations=8`, the whole of that rise is one test:
`test_an_artifact_above_the_read_ceiling_is_cut_and_the_envelope_says_so` at **0.04s call**,
which is S6 writing and reading its 8,040,304-byte artifact (39,803 body lines). Every other test added this
round is below the 0.005s reporting floor. This is a cost, not a defect: the parser stops at
`DIFF_VIEW_MAX_BODY_LINES` 20,000 lines into that text, so what is paid is the read and the
split rather than a full parse.

**G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C5.**
`git diff --name-only 922f3223..48da5345` → `.agent/authored/f037-r14.md`,
`.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`packages/orchestration/diff_view_source.py`, `tests/orchestration/test_diff_view_source.py`.
Residue ACTUAL minus EXPECTED: **empty**. Residue EXPECTED minus ACTUAL:
**`.agent/handoff.md`** and nothing else, which is the expected member because C6 writes it.
`git diff --stat` restricted to `docs/`: **empty**; to `apps/`: **empty**; to `packages/`:
`packages/orchestration/diff_view_source.py | 43 +++---`, `1 file changed, 40 insertions(+),
3 deletions(-)` — that ONE file and nothing else, which is what proves constraints 3 and 4.

| Commit | insertions | < 500 | parents |
|---|---|---|---|
| C0a `735a0860` | 419 | True | 1 |
| C0b `1c4034dc` | 333 | True | 1 |
| C1 `d353c697` | 23 | True | 1 |
| C2 `33cce53b` | 2 | True | 1 |
| C3 `6be5b573` | 116 | True | 1 |
| C4 `c9e7a866` | 202 | True | 1 |
| C5 `48da5345` | 2 | True | 1 |

Checked cell by cell against the `+/-` column of the `## Commits` table above: C0a +419;
C0b +333/−353; C1 +23/−23; C2 +2/−0; C3 +76/−0 and +40/−3, summing to 116; C4 +202/−1;
C5 +2/−0. Every cell agrees.

Marker sweep, `^<<<SLICE ` / `^<<<END `: `.agent/plan.md` **0 / 0**;
`.agent/live_review.md` **0 / 0**; `packages/orchestration/diff_view_source.py` **0 / 0**;
`tests/orchestration/test_diff_view_source.py` **0 / 0**. CONTROL over the C0a blob:
**4 / 4** — the counter is not blind. `git ls-files .remedy-wt` line count: **0**.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit **0**,
stdout `[]`.

## Authored-text proofs

| Slice | Target | Proof |
|---|---|---|
| the block itself | `.agent/authored/f037-r14.md`, `.agent/last_block.md` | disk-to-disk byte equality against `.remedy-wt/f037-r14-block.md`: True; both committed copies are one blob `af7b2387` |
| PLANF037R14 | `.agent/plan.md` | byte-equal to the slice extracted from the committed C0a blob, trailing newline included; negative control against the slice minus that newline is False |
| GATER13 | `.agent/live_review.md` (C2) | reader (a) True, reader (b) 1 unit in order True, both negative controls False |
| DECISION7 | `.agent/decisions.md` (C3) | reader (a) True, reader (b) 10 units in order True, both negative controls False |
| DONE0721B | `.agent/live_review.md` (C5) | reader (a) True, reader (b) 1 unit in order True, both negative controls False |

Every slice was applied BYTE FOR BYTE. Nothing in any slice was edited, reflowed or
corrected, and no slice looked wrong.

## Deviations & assumptions

The ordered commit sequence C0a → C0b → C1 → C2 → C3 → C4 → C5 → C6 was followed exactly:
no extra commit, none dropped, none reordered.

1. **The import block of the test module was edited, which is the one line of existing text
   this round did not leave alone.** Constraint 6 binds every existing TEST to be
   byte-identical, and all nine are: the base file's 5665 bytes from
   `# The two fixtures name DIFFERENT paths on purpose` to end-of-file survive as ONE
   contiguous byte substring of the new file, verified mechanically. What changed above that
   is the import block only — `import pytest` added, `DIFF_TRUNCATED_SENTINEL` added to the
   `diff_parser` import, `DIFF_VIEW_MAX_ARTIFACT_BYTES` added to the `diff_view_source`
   import, and `from packages.orchestration import diff_view_source` added for the
   `monkeypatch.setattr` target S7 names. No test body was touched.
2. **The parser appends one trailing EMPTY body line whenever a cut hunk still has lines
   outstanding in its header, and S9's and S10's assertions name it.** `parse_unified_diff_to_view`
   splits on `"\n"`, so the text's own terminating newline yields a final `""`, and while
   `old_left`/`new_left` are still positive that `""` is classified as a context line with
   content `""`. This is pre-existing parser behaviour on ANY short hunk, is nothing the cut
   produced, and constraint 3 forbids touching `diff_parser.py`. The assertions are therefore
   `_contents(view) == body[:6] + [""]` and `== ["→" * 12] * 3 + [""]` — exact rather than
   filtered, so a real half-line still reddens them, which mutation (c) confirms.
3. **S8's boundary is exercised by moving the CEILING, not by sizing two artifacts to the
   real one.** Two artifacts of exactly 512 and exactly 513 bytes are built against a
   monkeypatched ceiling of 512, with both byte lengths asserted in the test. "An artifact of
   exactly the ceiling" and "one of exactly one byte more" are both present as the SPEC asks;
   only the ceiling they are measured against is small, which is what S7 authorises.
4. **S11's second test also runs under a monkeypatched ceiling (4096), not the real one.**
   The SPEC says only "SMALLER than the ceiling". The small ceiling makes "the read did
   nothing" checkable in the test itself — `assert len(text.encode("utf-8")) < ceiling` —
   rather than left to the reader.
5. **Mutation (a)'s replaced string is the whole bounded-read block, from
   `with artifact.open("rb") as handle:` through `diff_text = raw.decode("utf-8")`.** That is
   what "replace the bounded read with `artifact.read_text(encoding="utf-8")`" has to mean
   for the result to compile; it counted 1 before the edit, as G6 requires.
6. **Mutations (a) and (d) kill the same four tests.** (a) contains (d)'s edit, so this is
   arithmetic, not a weakness. Note also that S6 — the real-ceiling test — survives BOTH:
   its 39,803-line fixture saturates `DIFF_VIEW_MAX_BODY_LINES` as well, so the parser sets
   `truncated` on its own. S6 proves the shipped constant is in the read path; it is
   deliberately not the discriminator for the flag, and (b), (c) and (e) each isolate exactly
   one property.
7. **`packages/orchestration/ui_server.py` was NOT touched, per constraint 4, and needs no
   change.** It builds its diff JSON by returning `build_diff_view`'s envelope whole, so the
   `truncated` field reaches the client already; this round changed what SETS that field, not
   what carries it. `tests/ui_server/test_diff_endpoint.py` is unmoved at 49 passed together
   with the parser suite, which is the measurement behind that claim.
8. **`packages/orchestration/diff_parser.py` and `tests/orchestration/test_diff_parser.py`
   were NOT touched, per constraint 3.** Two DELIBERATE-ABSENCE comments in `diff_parser.py`
   now read slightly stale — they say `diff_view_source.py` "still reads the artifact WHOLE"
   and that the input bound "belongs" there. The bound now exists. Repairing them means
   editing that module, which constraint 3 forbids, so this is REPORTED rather than fixed and
   is offered as the next round's smallest possible cleanup.
9. **No measurement of mine disagreed with SPEC S1.** The reviewer's figures — 1,423,907
   bytes, 397,907 and 1,026,000 — were applied as given and not re-derived, per constraint 10.
10. **One ruff finding was fixed during authoring, before C4:** UP012 on
    `len(" \n".encode("utf-8"))`, rewritten as `len(b" \n")`. It never reached a commit.
11. **Scratch cleaned by exact path, never by glob:** `.remedy-wt/f037-r14-redproof.py`,
    `.remedy-wt/f037-r14-g5.py`, `.remedy-wt/f037-r14-g8.py`,
    `.remedy-wt/slice_PLANF037R14.bin`, `.remedy-wt/slice_GATER13.bin`,
    `.remedy-wt/slice_DECISION7.bin`, `.remedy-wt/slice_DONE0721B.bin`,
    `.remedy-wt/live_review_before_c2.bin`, and the worktree
    `.remedy-wt/f037-r14-redproof`. `.remedy-wt/f037-r14-block.md` is the reviewer's own file
    and was left in place. `git ls-files .remedy-wt` is 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `735a0860` |
| C0b mirror the block | done | `1c4034dc`, one blob with C0a |
| C1 PLANF037R14 → `.agent/plan.md` | done | `d353c697` |
| C2 GATER13 → `.agent/live_review.md` | done | `33cce53b` |
| C3 DECISION7 + SPEC S1–S4 | done | `6be5b573` |
| C4 SPEC S5–S11 | done | `c9e7a866` |
| C5 DONE0721B → `.agent/live_review.md` | done | `48da5345`, after C3 and C4 |
| C6 the handback | done | this commit |
| G1 hygiene | done | STOP absent twice, base matched, tree 0 after every commit |
| G2 transport | done | one digest comparison, three readings equal, one blob |
| G3 extraction and caps | done | TOTAL 419 ≤ 490, PROSE 293 ≤ 400 |
| G4 the plan | done | byte-equal, negative control False, 49 lines |
| G5 the record | done | all three appends proved, ledger arithmetic as expected |
| G6 red-proofs | done | control exit 0; (a)–(e) all RED at real exit 1 |
| G7 suite, lint, canary | done | 15 passed, 49 passed, `All checks passed!`, 42 passed — all exit 0 |
| G8 structure and Open PR Gate | done | residues clean, `packages/` one file, `gh` exit 0 stdout `[]` |
| `R-0721` | done | remaining half resolved by C3 and C4, booked by C5 |

## Next

Review this round at `922f3223..HEAD` and issue the verdict; then start T002, the rendering
core, which `.agent/plan.md` "Next Steps" item 1 already scopes to `apps/ui/src/api/` with
markup pinned from `tests/ui_contracts/`. Phase 1 rule 1 first: re-read `.agent/STOP` from
disk before authoring. The feature stands at 14 rounds against the soft limit of 25 with T002
and T003 still to build — the R14 plan's own Risks entry says that if the rendering core has
not started within two rounds, the next handback carries a scope report instead of a step.
