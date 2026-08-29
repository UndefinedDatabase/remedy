# Handback — F033 round 3 · THE PARSER SEAM

## Session

SESSION 1 of feature F033 · round 3 · rounds so far 3

## Range

Review of `fa745748ba960d13e4230fa34c3d95936522cb70`..HEAD on branch
`feature/f033-hunk-approval-v2`.

BASE = `fa745748ba960d13e4230fa34c3d95936522cb70` — the round 2 handback commit,
confirmed by `git rev-parse HEAD` before C0a. Every base number the block stated
reproduced against it: `.agent/live_review.md` 1435760 bytes, registered 299,
`Done:` 44 over 42 distinct, `Landed:` 11, `Gate:` 119, open set 257, and
`tests/orchestration/test_diff_parser.py` 43 passed (measured at BASE in the
disposable worktree, not taken from the block).

## Commits

### 1a0a7fd6 chore(f033): save the round 3 parser-seam block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r3.md | +286 / -0 | C0a — the reviewer's block, copied byte for byte with `shutil.copyfile` |

### 3b184554 chore(f033): mirror the round 3 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +221 / -266 | C0b — mirror of the COMMITTED C0a blob, one blob id |

### 3fd9ea10 docs(f033): plan the round 3 parser seam
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +18 / -19 | C1 — replaced ENTIRELY with the PLANF033R3 slice (1960 bytes, 40 lines, under the 50-line cap) |

### 236de0f5 docs(f033): book the round 2 identity verdict
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 / -0 | C2 — append of one newline plus the RECORDF033R3 slice (4340 bytes, one paragraph) |

### 919f84a8 feat(f033): derive hunk ids from content and bump the diff view to 2
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/diff_parser.py | +47 / -16 | C3 — the version bump, the `hunk_identity` wiring in the flush loop, and the two corrected contract-note bullets |
| tests/orchestration/test_diff_parser.py | +292 / -4 | C3 — four moved assertions, eight new fixtures, seven new tests |

### C4 (this commit) docs(f033): hand back the round 3 parser seam
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | +313 / -241 | C4 — this file, measured with `git diff --numstat` before committing; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f033-r3-wt fa745748…` | created, detached HEAD at `fa745748` — used to MEASURE the base test count |
| `git -C /home/decodeux/Repos/remedy/.remedy-wt/f033-r3-wt checkout --detach 919f84a8…` | same worktree moved to C3 for the control and the three mutations |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f033-r3-wt` | removed BY EXACT PATH, exit 0, no `--force` needed (worktree clean) |
| `git worktree prune` | exit 0; `git worktree list` then shows only `/home/decodeux/Repos/remedy` |
| `git push` | after C4 — see the push line at the end of Verification |

No pull request created, none edited, nothing merged. No `gh` command run. No
force-push, no history rewrite, no branch deletion.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk with `os.path.exists` before C0a
and again before C4 — `False` BOTH times, absent. `git status --porcelain` printed
nothing after every one of the five commits in the range. `git branch --show-current`
read `feature/f033-hunk-approval-v2` at C0a and again before C4. No force-push, no
history rewrite, no branch deletion. `git rev-parse feature/f033-hunk-approval` reads
`ed04081283081f237d96147da39a07fca0b1ccad` before C4 — the parked branch is
UNDISTURBED and was not checked out, read or touched this round.

**G2 TRANSPORT — PASS, EQUAL.**

    .remedy-wt/f033-r3-block.md           20035 bytes  sha256=bb621ceb62c248e6b5220e65e4c315c1efaa948915cc0936806dbe5c5b6a74b1
    1a0a7fd6:.agent/authored/f033-r3.md   20035 bytes  sha256=bb621ceb62c248e6b5220e65e4c315c1efaa948915cc0936806dbe5c5b6a74b1
    EQUAL: True (byte length and digest both)

    git rev-parse 3b184554:.agent/authored/f033-r3.md -> 08a5532c7ad4efa1370fdf91e33a75ecac58522d
    git rev-parse 3b184554:.agent/last_block.md       -> 08a5532c7ad4efa1370fdf91e33a75ecac58522d
    ONE blob id: yes

The digest also matches the one the delegation message stated over 20035 bytes, so
the reading covers delivery and not only my own self-consistency.

**G3 THE RECORD APPEND at C2 — PASS.** `.remedy-wt/g3_append.py`, real exit 0:

    READER A — byte reconstruction
      base bytes=1435760 slice bytes=4340 head bytes=1440101
      base is byte PREFIX of head: True
      base + one newline + slice == head: True
      head ends in exactly one newline: True
    READER B — structural paragraph reader
      N counted in slice = 1
      head paragraph units = 669
      last 1 head units == slice paragraphs IN ORDER: True
      unit 0: equal=True bytes=4340 opens=b'Gate: F033 R2 \xe2\x80\x94 THE HUNK IDENTITY FUNCTION'
    NEGATIVE CONTROL
      first appended paragraph spans [1435761, 1440101) in head
      chosen offset 1437931 lies inside: True
      head[offset-30:offset+30] = b'UNIQUE before replacement and reverted after: the UNMUTATED '
      mutated byte 114 -> b'R'
      reader A on corrupt: base+newline+slice == head: False
      reader B on corrupt: last 1 head units == slice paragraphs: False
      BOTH readers REJECT the corrupt file: True
    G3 RESULT: PASS

1435760 + 1 + 4340 = 1440101, the C2 blob exactly. The control offset was PROVED
inside the FIRST appended paragraph by the span arithmetic printed above, not
asserted.

**G4 THE LEDGER at C2 — PASS, every ordered number reproduced.**
`.remedy-wt/ledger_counts.py`, real exit 0 at both revisions:

| Reading | BASE `fa745748` | C2 `236de0f5` | Ordered |
|---------|-----------------|---------------|---------|
| `^- R-\d+ — ` lines / distinct | 299 / 299 | 299 / 299 | 299 UNMOVED |
| `^Done: R-\d+ — ` lines / distinct | 44 / 42 | 44 / 42 | 44 over 42 UNMOVED |
| `^Landed: R-` | 11 | 11 | 11 UNMOVED |
| `^Gate: F\d+ R\d+ — ` | 119 | 120 | 119 -> 120 |
| `^Gate: F033 R2 — ` | 0 | 1 | exactly 1 |
| OPEN SET (distinct registered − distinct Done) | 257 | 257 | 257 UNMOVED |

This round registered no id and resolved none, as ordered.

**G5 THE PARSER AGAINST THE SPEC — PASS.** Taken at C3.

    python3 -m ruff check packages/orchestration/diff_parser.py tests/orchestration/test_diff_parser.py
    exit 0
    All checks passed!

`.remedy-wt/g5_parser.py`, real exit 0:

    DIFF_VIEW_VERSION = 2  is 2: True
      occurrences of 'import os' in the module: 0
      occurrences of 'import subprocess' in the module: 0
      occurrences of 'import logging' in the module: 0
      occurrences of 'open(' in the module: 0
      module imports hunk_identity: True
      occurrences of 'there is no endpoint yet': 0
    view['version'] = 2
      first.txt  '@@ -1,2 +1,2 @@'  id='539a25e12e224190'  16-lowercase-hex=True
      second.txt '@@ -1,2 +1,2 @@'  id='a0ce1fbdf10a827e'  16-lowercase-hex=True
      second.txt '@@ -40,2 +40,2 @@' id='99e3eb14901dadd8'  16-lowercase-hex=True
    ids counted=3 distinct=3 all_hex16=True

The multi-file probe is deliberately hostile: the two hunks of `second.txt` carry
BYTE-IDENTICAL old sides (`ctx-two`, `b`) and differ only in their added lines, so
they are separated by the occurrence rank alone and by nothing else.

**G6 THE SUITES — PASS. Run SERIALLY, one pytest process at a time, in the PRIMARY
checkout, real exit codes.**

    python3 -m pytest tests/orchestration/test_diff_parser.py -q
    exit 0    50 passed in 2.37s      (BASE 43 -> 50; seven tests ADDED, none deleted)

    python3 -m pytest tests/orchestration/test_diff_view_source.py -q
    exit 0    15 passed in 0.27s

    python3 -m pytest tests/orchestration/test_hunk_identity.py -q
    exit 0    10 passed in 0.25s      (ordered at 10 — 10, unmoved)

    python3 -m pytest tests/ui_server/ -q
    exit 0    497 passed in 32.21s    (ordered at 497 — 497, unmoved by the bump)

    python3 -m pytest tests/cli/test_golden_path.py -q
    exit 0    42 passed in 20.60s     (the canary, ordered at 42 — 42)

The BASE figure of 43 is MEASURED, not transcribed: `python3 -B -m pytest
tests/orchestration/test_diff_parser.py -q` run with the CWD inside the worktree at
`fa745748` gave `43 passed`, exit 0. That run's import path was proved first —
`packages.orchestration.diff_parser.__file__` printed
`/home/decodeux/Repos/remedy/.remedy-wt/f033-r3-wt/packages/orchestration/diff_parser.py`
with `DIFF_VIEW_VERSION: 1`, so it read the worktree's module and not the primary
checkout's.

**G7 THE MUTATION RED-PROOFS — PASS, all three RED.** In the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/f033-r3-wt` at `919f84a8`, never in the
primary checkout, every run with `python3 -B` and with `__pycache__` purged before
each run so stale bytecode could not mask a mutation. Each anchor was asserted UNIQUE
in `diff_parser.py` (count 1) BEFORE replacement, and each mutation was reverted to
the pristine bytes before the next (file-identity check `True` after every revert).

| Run | Real exit | Result | Failing test |
|-----|-----------|--------|--------------|
| CONTROL (unmutated) | 0 | 50 passed, 0 failed | — |
| M1 `DIFF_LINE_ADDED` included in the old side | 1 | 1 failed, 49 passed | `tests/orchestration/test_diff_parser.py::test_added_lines_do_not_enter_the_hunk_id` |
| M2 constant `0` passed as `occurrence` | 1 | 1 failed, 49 passed | `tests/orchestration/test_diff_parser.py::test_two_identical_hunks_in_one_file_get_distinct_ids_by_occurrence` |
| M3 `DIFF_VIEW_VERSION` set back to `1` | 1 | 1 failed, 49 passed | `tests/orchestration/test_diff_parser.py::test_diff_view_version_is_two_for_the_content_derived_hunk_ids` |
| POST-REVERT CONTROL | 0 | 50 passed, 0 failed | — |

Anchor uniqueness, as the runner printed it: M1 `1 (UNIQUE: True)`, M2
`1 (UNIQUE: True)`, M3 `1 (UNIQUE: True)`. Each mutation reddened EXACTLY the one
test that names its property and no other, which is what makes the fifty green tests
mean something. No mutation came back green, so there is nothing to report under the
green-mutation rule. Worktree removed BY EXACT PATH, then `git worktree prune`;
`git worktree list` afterwards shows only `/home/decodeux/Repos/remedy`, and
`git status --porcelain` in the primary checkout was empty before, during and after.

**G8 STRUCTURE — PASS.** `.remedy-wt/g8_structure.py` over
`git rev-list --reverse fa745748..919f84a8`, real exit 0. Five commits, each with
exactly ONE parent, each under 500 INSERTIONS (the `+` column of
`git diff --numstat`, never insertions plus deletions):

| Commit | Parents | Insertions | Paths |
|--------|---------|-----------|-------|
| 1a0a7fd6 | 1 | 286 | `.agent/authored/f033-r3.md` |
| 3b184554 | 1 | 221 | `.agent/last_block.md` |
| 3fd9ea10 | 1 | 18 | `.agent/plan.md` |
| 236de0f5 | 1 | 2 | `.agent/live_review.md` |
| 919f84a8 | 1 | 339 | `packages/orchestration/diff_parser.py`, `tests/orchestration/test_diff_parser.py` |

Path set, BOTH directions: touched but NOT in the declared change set — none.
In the change set but NOT touched — `.agent/handoff.md` only, which C4 writes and
which is therefore expected to be absent from the `BASE..C3` range. Nothing outside
the change set was created, edited or deleted; `packages/orchestration/hunk_identity.py`,
`diff_view_source.py`, `diff_repair.py`, `ui_server.py`, `apps/ui/**` and
`docs/roadmap/STATUS.md` are untouched.

Delimiter residue, with the saved block as a NON-ZERO control:

    target  .agent/plan.md                              '<<<SLICE ' = 0, '<<<END ' = 0
    target  packages/orchestration/diff_parser.py       '<<<SLICE ' = 0, '<<<END ' = 0
    target  tests/orchestration/test_diff_parser.py     '<<<SLICE ' = 0, '<<<END ' = 0
    CONTROL .agent/authored/f033-r3.md                  '<<<SLICE ' = 4, '<<<END ' = 5

    git ls-files .remedy-wt = 0

    git push -u origin feature/f033-hunk-approval-v2 -> see the push line below

## What shipped — the corrected contract-note bullets, verbatim

The two CONTRACT NOTES bullets of `packages/orchestration/diff_parser.py`'s module
docstring now read, in full and exactly as committed at `919f84a8`:

    * ``intraline`` joined the per-line shape while version 1 was still PRIVATE — nothing
      outside this repository could observe it — so it completed v1 rather than changing a
      shipped shape. Version 1 stopped being private when F256 landed the diff endpoint:
      ``packages/orchestration/ui_server.py`` builds the envelope through
      ``packages/orchestration/diff_view_source.py``'s ``build_diff_view``, which carries
      ``DIFF_VIEW_VERSION`` straight out to a consumer. Version 1 WAS served. That is why
      F033's id change took a real bump to 2 rather than riding in unversioned, and any
      later shape change must take one too — the private-shape argument is spent.
    * Hunk ``id`` values are CONTENT-DERIVED and carry no position at all. The identity is
      computed by ``hunk_identity`` in ``packages/orchestration/hunk_identity.py`` over the
      file's resolved ``path``, the hunk's normalised OLD side — its ``ctx`` and ``del``
      lines in order, never its ``add`` lines — and the hunk's occurrence rank among
      byte-identical old sides within the SAME file. An id is ``HUNK_ID_LENGTH`` lowercase
      hex characters. THE STABILITY PROPERTY a reader may rely on: a hunk keeps its id when
      anything else in its file moves — another hunk gains, loses or rewrites lines, or
      hunks appear before it — and when its OWN added lines change, because a second
      proposed fix for the same original text is the same hunk. It changes only when the
      path changes or when the hunk's own old side does. This shape arrived with
      ``DIFF_VIEW_VERSION`` 2.

The `DIFF_VIEW_VERSION` comment now records that the bump HAS happened and what
changed in it:

    #: Bumped whenever the returned shape changes; consumers gate on this rather than on key
    #: sniffing. Version 2 IS F033's bump, and it happened: a hunk's ``id`` is now derived
    #: from that hunk's own content by ``packages/orchestration/hunk_identity.py`` instead of
    #: from its position in the diff. No other key of the view moved with it.
    DIFF_VIEW_VERSION = 2

## What shipped — the tests

SEVEN tests ADDED, none deleted, none renamed. The four assertions the block named
were MOVED inside the tests that already carried them; those four test names are
unchanged, so no consumer of a node id breaks.

| Test | Status | Property |
|------|--------|----------|
| `test_diff_view_version_is_two_for_the_content_derived_hunk_ids` | ADDED | pins the version LITERAL — the only place `2` is written out |
| `test_a_hunk_keeps_its_id_when_an_earlier_hunk_gains_an_added_line` | ADDED | SPEC test 1 — the stability property, at the parser |
| `test_a_hunk_keeps_its_id_when_a_whole_new_hunk_is_inserted_before_it` | ADDED | the shape a positional id CANNOT survive (deviation 2) |
| `test_added_lines_do_not_enter_the_hunk_id` | ADDED | SPEC test 2 |
| `test_two_identical_hunks_in_one_file_get_distinct_ids_by_occurrence` | ADDED | SPEC test 3 — the occurrence rank |
| `test_every_hunk_id_is_sixteen_lowercase_hex_characters_and_distinct` | ADDED | SPEC test 4 — the id's shape |
| `test_the_same_hunk_content_at_a_different_path_gets_a_different_id` | ADDED | SPEC test 5 |
| `test_parse_unified_diff_to_view_reads_empty_input_as_no_files` | MOVED | `"version": 1` -> `DIFF_VIEW_VERSION` |
| `test_parse_unified_diff_to_view_reads_non_diff_text_as_no_files` | MOVED | `"version": 1` -> `DIFF_VIEW_VERSION` |
| `test_parse_unified_diff_to_view_keeps_input_order_and_distinct_hunk_ids` | MOVED | `ids == ["0:0", "1:0"]` -> count 2, all 16-hex, all distinct; path ordering untouched |
| `test_parse_unified_diff_to_view_seeds_each_hunk_from_its_own_header` | MOVED | `== ["0:0", "0:1"]` -> the same property; both `old_start`/`new_start` pairs and both `_tuples` lists untouched |

Eight new inline fixtures carry the inputs: `STABLE_ID_BASE_DIFF`,
`STABLE_ID_EARLIER_HUNK_GREW_DIFF`, `STABLE_ID_NEW_FIRST_HUNK_DIFF`,
`REPAIR_FIRST_ATTEMPT_DIFF`, `REPAIR_SECOND_ATTEMPT_DIFF`,
`TWIN_HUNKS_IN_ONE_FILE_DIFF`, `SHARED_BODY_AT_ONE_PATH_DIFF` and
`SHARED_BODY_AT_ANOTHER_PATH_DIFF`. All eight end in `_DIFF`, so the existing
whole-corpus sweep `test_every_intraline_span_lies_inside_its_own_content` picks them
up automatically. Three module-level helpers were added — `_HUNK_ID_RE`
(`^[0-9a-f]{16}$`, written out rather than derived from `HUNK_ID_LENGTH`), `_old_side`
and `_added_side` — each spelled out in the test file rather than imported from the
module under test, following the precedent `_significant_tokens` already sets there.

THE VERSION-LITERAL CHOICE the SPEC asks me to state: I took the SECOND branch. The
two named tests now assert against `DIFF_VIEW_VERSION`, and EXACTLY ONE test pins the
literal — the new `test_diff_view_version_is_two_for_the_content_derived_hunk_ids`.
The first branch alone is unmeetable against G7: if every test read the constant, M3
(`DIFF_VIEW_VERSION` back to `1`) would leave the whole file GREEN and the ordered
red-proof could not exist.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `1a0a7fd6`, `shutil.copyfile`, byte-identical |
| C0b mirror it | done | `3b184554`, one blob id `08a5532c7ad4efa1370fdf91e33a75ecac58522d` |
| C1 `.agent/plan.md` | done | `3fd9ea10`, PLANF033R3 applied whole, byte-equal to the slice |
| C2 round 2 verdict into `.agent/live_review.md` | done | `236de0f5`, two readers plus a rejected negative control |
| C3 the parser, the version bump and the tests | done | `919f84a8`, all three in ONE commit as ordered, 339 insertions |
| C4 the handback | done | this commit |
| SPEC §1 the version | done | `DIFF_VIEW_VERSION = 2`, comment records the bump has happened |
| SPEC §2 the id in the flush loop | done | `hunk_identity(path, old_side_lines, occurrence)`; `file_index` gone |
| SPEC §3 the contract note | done | both bullets rewritten; `there is no endpoint yet` reads 0 |
| SPEC §4 what must not change | done | pure, total, no new raising call; only `"id"` values moved |
| SPEC tests: four moved assertions | done | four test names unchanged, literals replaced by the property |
| SPEC tests: five new properties | deviated | six shipped, not five — deviation 2 |
| G1 HYGIENE | done | pass |
| G2 TRANSPORT | done | pass, EQUAL, one blob id |
| G3 THE RECORD APPEND at C2 | done | pass, N=1, control rejected by both readers |
| G4 THE LEDGER at C2 | done | pass, every ordered number reproduced |
| G5 THE PARSER AGAINST THE SPEC | done | pass, ruff exit 0, version 2, stale claim 0 |
| G6 THE SUITES | done | pass, 50/15/10/497/42, all exit 0, run serially |
| G7 THE MUTATION RED-PROOFS | done | pass, control green then M1/M2/M3 all RED, one named test each |
| G8 STRUCTURE | done | pass, 5 single-parent commits, max 339 insertions |

## Authored-text proofs

| Text | Proof |
|------|-------|
| the block itself | `.remedy-wt/f033-r3-block.md` and `1a0a7fd6:.agent/authored/f033-r3.md` are both 20035 bytes at sha256 `bb621ceb…a74b1` — EQUAL |
| PLANF033R3 | extracted from the COMMITTED blob `1a0a7fd6:.agent/authored/f033-r3.md` by `.remedy-wt/extract_slice.py`, 1960 bytes / 40 lines, written whole to `.agent/plan.md`, which ends in exactly one newline and carries 0 delimiter tokens |
| RECORDF033R3 | extracted from the same committed blob, 4340 bytes, one paragraph; appended verbatim after one newline, reconstructing the C2 blob byte for byte |

Every slice's named delimiter (`<<<SLICE NAME` / `<<<END NAME`, anchored at line
start) was asserted to occur EXACTLY ONCE before extraction — the extractor raises
otherwise — and no slice was retyped. The PRODUCTION code was written from the SPEC,
not applied from a slice, as convention 5 requires.

## Deviations & assumptions

The block's ordered commit sequence was followed exactly: C0a, C0b, C1, C2, C3, C4,
in that order, no extra commit, none dropped, none reordered.

1. **`hunk_index` was dropped, against a sentence of SPEC §2.** §2 says "`hunk_index`
   is still needed as the loop variable". After the id stops being
   `f"{file_index}:{hunk_index}"` NOTHING in the function reads `hunk_index` — I
   checked the whole flush loop and the whole module. Keeping
   `for hunk_index, raw in enumerate(region.hunks)` would have shipped a loop variable
   with no reader (ruff would not catch it: `select = ["E","F","W","I","UP"]`, and
   flake8-bugbear's B007 is not enabled). The loop is now `for raw in region.hunks:`.
   The binding half of the sentence — that `hunk_index` no longer contributes to the
   id — is honoured; the aside about it still being needed is not true of the code
   after the change, so I did not invent a reader for it.

2. **SIX new tests, not the five the SPEC lists.** The extra one is
   `test_a_hunk_keeps_its_id_when_a_whole_new_hunk_is_inserted_before_it`, and the
   reason is a claim in the SPEC that does not hold. SPEC test 1 orders a diff whose
   EARLIER hunk "has one more ADDED line" and says "Positional ids fail this and
   content ids pass it". A positional `"<file_index>:<hunk_index>"` id does NOT fail
   that shape: adding a line inside an earlier hunk does not change any hunk's INDEX,
   so the later hunk reads `0:1` before and after and the old ids would have passed
   the ordered test unchanged. I shipped SPEC test 1 exactly as ordered anyway — it
   pins a real property, that a neighbour's growth and the resulting new-side slide
   are both outside the id — and added one more test carrying the shape that IS a
   discriminator: a whole new hunk inserted ahead of the others, which moves the
   observed hunk from index 1 to index 2 while its own old side does not move. That
   is the assertion that shows ids stopped being positional. Declared rather than
   silently folded into the ordered test.

3. **Two comments beyond the two ordered bullets were corrected in the same file.**
   Both stated the positional-id fact this round removes, so leaving them would have
   left the module contradicting itself: `"id": ""  # assigned on flush, when the file
   index is known` became `# assigned on flush, from this hunk's own old side`, and the
   R-0716 comment's clause "so file indices — and therefore hunk ids — are numbered
   over the real files" became "so the view carries one entry per real file rather than
   a phantom beside each of them" (the collapse still matters for FILE ENTRIES; it no
   longer has anything to do with ids). No behaviour changed with either.

4. **One stale-looking docstring sentence was deliberately LEFT.** The second CONTRACT
   NOTES bullet still ends "a consumer pinning version 1 gets these two keys". It is a
   true historical statement about what version 1 carried, `truncated` and `note` are
   both still present at version 2, and SPEC §3 names only two bullets. I flag it
   because a reader sweeping for "version 1" in this file will land on it, and because
   deciding it was out of scope was my judgement rather than the block's.

5. **C1's plan slice books C3's work as "done" one commit before C3 lands it.** The
   PLANF033R3 slice's row `| wire the parser, bump DIFF_VIEW_VERSION to 2 | done | this
   round |` was applied BYTE FOR BYTE as convention 1 requires, at C1. Between
   `3fd9ea10` and `919f84a8` the plan therefore claims something the tree does not yet
   hold. This is the block's own ordering, not a change of mine; recorded because
   AGENTS.md's Commit Gate asks that `.agent/plan.md` match the current work at every
   commit. Identical to round 2's deviation 5.

6. **G8 does not cover C4.** The block explicitly excludes C4's own numbers from G8
   and hands them to the reviewer at the next gate, so this handback's own commit is
   tabled above but not gated here.

Nothing was routed around, no gate went red, and no ordered number failed to
reproduce. No part of the SPEC turned out impossible; the two inaccuracies I found in
it are deviations 1 and 2, and both are declared rather than worked around.

Assumptions: none beyond the above. `.agent/context.md` and `.agent/decisions.md`
needed no update — the change set forbids them and no new durable decision was taken.
`docs/` needed none either: `DIFF_VIEW_VERSION` and the id shape are documented in the
parser's own module docstring, which is where the block's SPEC put them, and no
`docs/` page states the id format. The client-side fallback at
`apps/ui/src/api/diffViewModel.ts`, which still synthesises a POSITIONAL id when the
server sends an empty one, is untouched by design — the block assigns it to the next
round — so the content-hash contract can still be violated silently on the client
until that round rules it.

## Next

Reviewer gates round 3 at `fa745748..HEAD` on `feature/f033-hunk-approval-v2`. I
wrote no verdict on my own work. Round 4, per the plan, rules the client fallback at
`apps/ui/src/api/diffViewModel.ts` and moves the TypeScript pins on version 1 and on
the `"<n>:<m>"` id form.
