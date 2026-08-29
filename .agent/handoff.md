# Handback — F033 round 4 · THE CLIENT SEAM

## Session

SESSION 1 of feature F033 · round 4 · rounds so far 4

## Range

Review of `51e04c894658551d3e1775178b8354f8a72a3c28`..HEAD on branch
`feature/f033-hunk-approval-v2`.

BASE = `51e04c894658551d3e1775178b8354f8a72a3c28` — the round 3 handback commit,
confirmed by `git rev-parse HEAD` before C0a. Every base number the block stated
reproduced against it: `.agent/live_review.md` 1440101 bytes, registered 299,
`Done:` 44 over 42 distinct, `Landed:` 11, `Gate:` 120, open set 257, the bare
positional template occurring exactly once in `apps/ui/src/api/diffViewModel.ts`,
and `src/api/diffViewModel.test.ts` at 93 tests (measured in the disposable
worktree at BASE, not taken from the block).

## Commits

### 920c66bc chore(f033): save the round 4 block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r4.md | +249 / -0 | C0a — the reviewer's block, copied byte for byte with `shutil.copyfile` |

### daf2a96e chore(f033): mirror the round 4 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +155 / -192 | C0b — mirror of the COMMITTED C0a blob, one blob id |

### fa745427 docs(f033): retarget the plan on the client seam
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +17 / -17 | C1 — replaced ENTIRELY with the PLANF033R4 slice (1975 bytes, 40 lines, under the 50-line cap) |

### 201823cf docs(f033): book the round 3 verdict and DECISION F033 D2
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | C2 — append of one newline plus the RECORDF033R4 slice (6185 bytes, two paragraphs) |

### 76b6448b fix(f033): stop the client inventing a server-shaped hunk id
| Path | +/- | Reason |
|------|-----|--------|
| apps/ui/src/api/diffViewModel.ts | +15 / -5 | C3 — the exported prefix, the rewritten fallback, the rewritten `readDiffHunk` contract note |
| apps/ui/src/api/diffViewModel.test.ts | +92 / -32 | C3 — v2 fixtures, one renamed test, two new tests |

### C4 (this commit) docs(f033): hand back the round 4 client seam
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | +270 / -303 | C4 — this file, measured with `git diff --numstat` before committing; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f033-r4-wt 76b6448b` | created, detached HEAD at `76b6448b` — G7's control and mutation ran there |
| `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f033-r4-wt` | removed BY EXACT PATH, exit 0; the path no longer exists on disk |
| `git worktree prune` | exit 0; `git worktree list` then shows only `/home/decodeux/Repos/remedy` |
| `git push` | after C4 — see the push line at the end of Verification |

No pull request created, none edited, nothing merged. No `gh` command run. No
force-push, no history rewrite, no branch deletion.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a and again before C4 —
ABSENT both times (`ls` reports "No such file or directory"). `git status --porcelain`
printed nothing after every one of the five commits in the range. The branch was
`feature/f033-hunk-approval-v2` throughout (`git rev-parse --abbrev-ref HEAD`). No
force-push, no history rewrite, no branch deletion.
`git rev-parse feature/f033-hunk-approval` reads
`ed04081283081f237d96147da39a07fca0b1ccad` before C4 — the parked branch is
UNDISTURBED and was not checked out, read or touched this round.

**G2 TRANSPORT — PASS, EQUAL.** No expected digest was stated in the block, as it
cannot carry its own; the delegation message stated one and it reproduced.

    .remedy-wt/f033-r4-block.md           19163 bytes  sha256=f92ac6a1e3a5710101a71244b3af9f3a26906453926aa68b9a63990a28318aff
    920c66bc:.agent/authored/f033-r4.md   19163 bytes  sha256=f92ac6a1e3a5710101a71244b3af9f3a26906453926aa68b9a63990a28318aff
    EQUAL: True (byte length and digest both)

    git rev-parse daf2a96e:.agent/authored/f033-r4.md -> 15eae1e894271325284f28a3cfea1734fecea46a
    git rev-parse daf2a96e:.agent/last_block.md       -> 15eae1e894271325284f28a3cfea1734fecea46a
    ONE blob id: yes

**G3 THE RECORD APPEND at C2 — PASS.** `.remedy-wt/f033r4_g3.py`, real exit 0:

    READER A — byte reconstruction
      base bytes=1440101 slice bytes=6185 C2 bytes=1446287
      1440101 + 1 + 6185 = 1446287, the C2 blob exactly
      base is a byte PREFIX of C2: True
      C2 ends in exactly one newline: True
    READER B — structural paragraph reader
      N paragraphs COUNTED in the slice = 2
      last 2 blank-line units of C2 == the slice's paragraphs IN ORDER: True
    NEGATIVE CONTROL
      first appended paragraph spans [1440102, 1444310) in C2
      chosen offset 1440202 lies inside: True (proved by the span arithmetic, not asserted)
      one byte flipped, exactly one byte differs from C2
      READER A rejects the control: True
      READER B rejects the control: True

**G4 THE LEDGER at C2 — PASS, every ordered number reproduced.**
`.remedy-wt/f033r4_g4.py`, real exit 0 at both revisions:

| Reading | BASE `51e04c89` | C2 `201823cf` | Ordered |
|---------|-----------------|---------------|---------|
| `^- R-\d+ — ` lines / distinct | 299 / 299 | 299 / 299 | 299 UNMOVED |
| `^Done: R-\d+ — ` lines / distinct | 44 / 42 | 44 / 42 | 44 over 42 UNMOVED |
| `^Landed: R-` | 11 | 11 | 11 UNMOVED |
| `^Gate: F\d+ R\d+ — ` | 120 | 121 | 120 -> 121 |
| `^Gate: F033 R3 — ` | 0 | 1 | exactly 1 |
| OPEN SET (distinct registered − distinct Done) | 257 | 257 | 257 UNMOVED |

This round registers no id and resolves none, as ordered.

**G5 THE CLIENT AGAINST THE SPEC — PASS.** Taken at C3,
`.remedy-wt/f033r4_g5.py`, real exit 0:

    UNIDENTIFIED_HUNK_ID_PREFIX exported: True   (matched on `^export const … = "…";`)
    its value: 'unidentified:'
    BASE  bare template `${fileIndex}:${hunkIndex}` (WITH backticks) count: 1
    HEAD  bare template `${fileIndex}:${hunkIndex}` (WITH backticks) count: 0
    BASE  bare substring  ${fileIndex}:${hunkIndex}  (no backticks)  count: 1
    HEAD  bare substring  ${fileIndex}:${hunkIndex}  (no backticks)  count: 0
    npx tsc --noEmit (cwd apps/ui, invoked through subprocess.run): REAL exit 0, no output

Both readings are reported because the gate's wording admits both and a prefixed
template would have satisfied only the first. See deviation 1.

**G6 VITEST AND THE PYTHON SUITES — PASS.** In the PRIMARY checkout, `npx` invoked
through `subprocess.run`, pytest run SERIALLY, one process at a time, real exit codes:

    npx vitest run --reporter=basic src/api/diffViewModel.test.ts   (cwd apps/ui)
    exit 0    95 passed (95), 1 file       BASE 93 -> 95: one test RENAMED, two ADDED

    python3 -B -m pytest tests/ui_server/ -q
    exit 0    497 passed in 32.05s         (ordered at 497 — unmoved)

    python3 -B -m pytest tests/cli/test_golden_path.py -q
    exit 0    42 passed in 20.50s          (the canary, ordered at 42 — 42)

    python3 -B -m pytest tests/ui_contracts/ -q                     NOT ordered; run anyway
    exit 0    664 passed, 4 skipped in 5.66s

`tests/ui_contracts/` is not in the block's gate list but reads BOTH edited files as
text — `test_every_exported_name_is_named_by_the_vitest_suite` fails any export the
vitest suite does not NAME in comment-stripped source, which the new
`UNIDENTIFIED_HUNK_ID_PREFIX` would have tripped had it only appeared in a comment.
Run as part of the self-review loop, not as a substitute for an ordered gate.

**G7 THE VITEST RED-PROOF — PASS, the mutation went RED.** In the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/f033-r4-wt` at `76b6448b`, never in the primary
checkout, by the exact route the block gives: cwd `apps/ui` of the PRIMARY checkout,
`--config <PRIMARY>/apps/ui/vitest.config.ts`, `--root <WORKTREE>/apps/ui`. No
`node_modules` was installed, copied or symlinked into the worktree.

The anchor was asserted UNIQUE before replacement — the fallback line occurs exactly
1 time in the worktree's `diffViewModel.ts` — and the file was reverted to the
pristine bytes afterwards (identity check `True`).

| Run | Real exit | Result |
|-----|-----------|--------|
| UNMUTATED CONTROL | 0 | 95 passed (95) |
| MUTANT — fallback returns the bare positional id again | 1 | 2 failed, 93 passed (95) |

The mutation applied, verbatim:

    -    id: rawId !== "" ? rawId : `${UNIDENTIFIED_HUNK_ID_PREFIX}file${fileIndex}:hunk${hunkIndex}`,
    +    id: rawId !== "" ? rawId : `${fileIndex}:${hunkIndex}`,

The two tests it reddened, by NAME:

    × readDiffEnvelope > marks a hunk with no usable id UNIDENTIFIED instead of inventing a server-shaped one
      → expected false to be true // Object.is equality
    × readDiffEnvelope > gives two id-less hunks in ONE file DISTINCT ids, so the collapse set still sees two
      → 0:0: expected false to be true // Object.is equality

Two rather than one, because both tests assert the PREFIX and only the second also
asserts distinctness — which a bare positional id still satisfies, so distinctness
alone would not have caught the mutation. Nothing came back green, so the
green-mutation rule has nothing to report. Worktree removed BY EXACT PATH, then
`git worktree prune`; `git worktree list` afterwards shows only
`/home/decodeux/Repos/remedy`, and `git status --porcelain` in the primary checkout
was empty before, during and after.

**G8 STRUCTURE — PASS.** `.remedy-wt/f033r4_g8.py` over
`git rev-list --reverse 51e04c89..76b6448b`, real exit 0. Five commits, each with
exactly ONE parent, each under 500 INSERTIONS (the `+` column of
`git diff --numstat`, never insertions plus deletions):

| Commit | Parents | Insertions | Paths |
|--------|---------|-----------|-------|
| 920c66bc | 1 | 249 | `.agent/authored/f033-r4.md` |
| daf2a96e | 1 | 155 | `.agent/last_block.md` |
| fa745427 | 1 | 17 | `.agent/plan.md` |
| 201823cf | 1 | 4 | `.agent/live_review.md` |
| 76b6448b | 1 | 107 | `apps/ui/src/api/diffViewModel.ts`, `apps/ui/src/api/diffViewModel.test.ts` |

Path set, BOTH directions: touched but NOT in the declared change set — none.
In the change set but NOT touched — `.agent/handoff.md` only, which C4 writes and
which is therefore expected to be absent from the `BASE..C3` range. Nothing outside
the change set was created, edited or deleted; `packages/orchestration/diff_parser.py`,
`packages/orchestration/hunk_identity.py`,
`apps/ui/src/components/diff/DiffView.tsx` and `docs/roadmap/STATUS.md` are untouched.

Delimiter residue, with the saved block as a NON-ZERO control:

    target  .agent/plan.md                          '<<<SLICE ' = 0, '<<<END ' = 0
    target  apps/ui/src/api/diffViewModel.ts        '<<<SLICE ' = 0, '<<<END ' = 0
    target  apps/ui/src/api/diffViewModel.test.ts   '<<<SLICE ' = 0, '<<<END ' = 0
    CONTROL .agent/authored/f033-r4.md              '<<<SLICE ' = 4, '<<<END ' = 5

    git ls-files .remedy-wt = 0

    git push -u origin feature/f033-hunk-approval-v2 -> see the push line below

## What shipped — the fallback, verbatim

The final expression, exactly as committed at `76b6448b`:

    id: rawId !== "" ? rawId : `${UNIDENTIFIED_HUNK_ID_PREFIX}file${fileIndex}:hunk${hunkIndex}`,

so an id-less hunk in the first file becomes `unidentified:file0:hunk0`. The
constant and its WHY comment, also verbatim:

    /** WHY THE PREFIX: a server hunk id is sixteen lowercase hex characters, so a
     *  string carrying this prefix cannot be mistaken for one by any consumer, which
     *  is the whole point of it (DECISION F033 D2). */
    export const UNIDENTIFIED_HUNK_ID_PREFIX = "unidentified:";

`readDiffHunk`'s contract note was rewritten in place: it no longer says a hunk with
no usable id is "given the `\"<fileIndex>:<hunkIndex>\"` the parser would have
assigned", and now states why an id must exist, why it must not look like the
server's, and that a real id passes through untouched and unvalidated. A real id is
neither validated nor reformatted anywhere in the module. `readDiffEnvelope` still
never throws, no other envelope field moved, and no signature changed.

## What shipped — the fixture values I chose

| Fixture | BASE | Now |
|---------|------|-----|
| `wireEnvelope`, `camelPayload`, `snakePayload` `version` | `1` | `WIRE_DIFF_VIEW_VERSION` = `2` |
| the hunk id of `camelPayload`, `snakePayload`, `envelopeWithHunkOf` and the two inline hunk fixtures | `"0:0"` | `SERVER_HUNK_ID` = `"3f5a9c1e0b7d2481"` |
| the second hunk of the multi-hunk fixtures | `"0:1"` | `SECOND_SERVER_HUNK_ID` = `"a41d0c7e93b6f582"` |
| the second file's hunk | `"1:0"` | `THIRD_SERVER_HUNK_ID` = `"b0e27d4a1c9f6835"` |

All three ids are sixteen lowercase hex characters and mutually distinct; they are
written out rather than recomputed, because what a client fixture owes the server is
the SHAPE of an id and never the hash behind it. Every other assertion in those tests
is untouched: the snake/camel equivalence, `stats {added: 2, deleted: 1}`, both line
counts, `oldStart` 1, `newLn` 1, and the never-throws test.

## What shipped — the tests

| Test | Status | Property |
|------|--------|----------|
| `marks a hunk with no usable id UNIDENTIFIED instead of inventing a server-shaped one` | RENAMED + rewritten | was `gives a hunk with no usable id the position the parser would have given it`, which asserted `"0:0"`; now asserts the prefix, a non-empty tail and `not.toBe("0:0")` |
| `gives two id-less hunks in ONE file DISTINCT ids, so the collapse set still sees two` | ADDED | two id-less hunks in one file get distinct prefixed ids, and `toggleHunkCollapse` keeps them as two entries of its `Set<string>` |
| `passes a well-formed SERVER hunk id through unchanged, prefixing nothing` | ADDED | `SERVER_HUNK_ID` arrives back identical, wears no prefix, and matches `^[0-9a-f]{16}$` |

93 tests at BASE, 95 now: two added, one renamed, none deleted.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `920c66bc`, `shutil.copyfile`, byte-identical |
| C0b mirror it | done | `daf2a96e`, one blob id `15eae1e894271325284f28a3cfea1734fecea46a` |
| C1 `.agent/plan.md` | done | `fa745427`, PLANF033R4 applied whole, byte-equal to the slice |
| C2 round 3 verdict and DECISION F033 D2 into `.agent/live_review.md` | done | `201823cf`, two readers plus a rejected negative control |
| C3 the client model and its tests, together | done | `76b6448b`, both files in ONE commit as ordered, 107 insertions |
| C4 the handback | done | this commit |
| SPEC §1 a reserved prefix, exported | done | `UNIDENTIFIED_HUNK_ID_PREFIX = "unidentified:"`, WHY comment directly above |
| SPEC §2 the fallback stops manufacturing a plausible id | deviated | prefix applied and the position kept, but spelled `file<i>:hunk<j>` — deviation 1 |
| SPEC §2 a real id passes through UNTOUCHED | done | not validated, not reformatted, no length check; pinned by a new test |
| SPEC §3 what must NOT change | done | `readDiffEnvelope` still never throws, no field moved, no signature changed |
| SPEC tests: rename the `"0:0"` test to the new contract | done | renamed and rewritten |
| SPEC tests: two id-less hunks get DISTINCT ids | done | added |
| SPEC tests: a well-formed server id passes through | done | added, sixteen-hex id |
| SPEC tests: move the fixtures to v2 | deviated | done, and slightly wider than the wording — deviation 2 |
| G1 HYGIENE | done | pass |
| G2 TRANSPORT | done | pass, EQUAL, one blob id |
| G3 THE RECORD APPEND at C2 | done | pass, N=2, control rejected by both readers |
| G4 THE LEDGER at C2 | done | pass, every ordered number reproduced |
| G5 THE CLIENT AGAINST THE SPEC | done | pass, exported at `unidentified:`, 1 -> 0 under both readings, tsc exit 0 |
| G6 VITEST | done | pass, 93 -> 95 vitest, 497 ui_server, 42 golden path, all exit 0 |
| G7 THE VITEST RED-PROOF | done | pass, control green then RED at 2 failed |
| G8 STRUCTURE | done | pass, 5 single-parent commits, max 249 insertions |

## Authored-text proofs

| Text | Proof |
|------|-------|
| the block itself | `.remedy-wt/f033-r4-block.md` and `920c66bc:.agent/authored/f033-r4.md` are both 19163 bytes at sha256 `f92ac6a1…18aff` — EQUAL |
| PLANF033R4 | extracted from the COMMITTED blob `920c66bc:.agent/authored/f033-r4.md` by `.remedy-wt/f033r4_slice.py`, 1975 bytes / 40 lines, written whole to `.agent/plan.md`, which ends in exactly one newline and carries 0 delimiter tokens |
| RECORDF033R4 | extracted from the same committed blob, 6185 bytes, two paragraphs; appended verbatim after one newline, reconstructing the C2 blob byte for byte |

Each slice's named delimiter (`<<<SLICE NAME` / `<<<END NAME`, anchored at line
start) was asserted to occur EXACTLY ONCE before extraction — the extractor raises
otherwise — and no slice was retyped. The PRODUCTION code was written from the SPEC,
not applied from a slice, as convention 5 requires.

## Deviations & assumptions

The block's ordered commit sequence was followed exactly: C0a, C0b, C1, C2, C3, C4,
in that order, no extra commit, none dropped, none reordered.

1. **The invented id's positional part is spelled `file<fileIndex>:hunk<hunkIndex>`,
   not the bare `<fileIndex>:<hunkIndex>`.** SPEC §2 fixes the prefix and says "the
   positional part stays: it is what makes the invented ids distinct from each
   other"; it fixes no separator. G5 forbids "the bare template
   `` `${fileIndex}:${hunkIndex}` ``" at ZERO occurrences, and that wording admits
   two readings — with the backticks, or the inner substring alone. A prefixed
   template of the form `` `${UNIDENTIFIED_HUNK_ID_PREFIX}${fileIndex}:${hunkIndex}` ``
   satisfies the first reading and READS 1 UNDER THE SECOND, so it would have looked
   red to a reviewer grepping the substring. Interposing the two words removes the
   byte sequence entirely: both readings now measure BASE 1 -> HEAD 0, both reported
   above. The property the SPEC asks for is unchanged — the ids stay distinct per
   `(fileIndex, hunkIndex)` and the pinning test asserts distinctness directly.

2. **Every v1-shaped id literal moved, which is slightly wider than "the fixture
   payload builders".** The block names the builders that "assert `version` 1 and a
   hunk id `\"0:0\"`". I also moved the ids in the `toggleHunkCollapse` block, which
   builds no payload and merely uses `"0:0"`/`"1:0"` as arbitrary `Set<string>`
   members. Reason: after the ordered change those three lines would have been the
   only v1-shaped hunk ids left in the file, and a reader sweeping the suite for the
   old shape would land on them. No assertion changed — the same set operations are
   asserted over renamed constants. The two DELIBERATE survivals are in the renamed
   test, which names `"0:0"` on purpose: once in a comment and once in
   `expect(id).not.toBe("0:0")`, the value the client no longer invents.

3. **A stale comment two functions away was found and deliberately LEFT.**
   `buildDiffRowModels`' doc comment still reads: "The hunk-derived keys are built
   from the server's own hunk `id`, which `diff_parser.py` assigns as
   `\"<fileIndex>:<hunkIndex>\"`, both zero-based and unique within one parse. Those
   ids are PROVISIONAL: F033 replaces them with content-hash ids…". Round 3 already
   made them content-derived, so the first sentence is false at BASE and the second
   is in the wrong tense. SPEC §3 says "nothing outside these two functions is
   edited", and the change set names these two files but the SPEC narrows the module
   to `readDiffHunk` and `readDiffEnvelope`, so repairing it would have widened
   scope against an explicit instruction. Reported rather than fixed; it is a
   candidate for the next round that touches this module.

4. **C1's plan slice books C3's work as "done" one commit before C3 lands it.** The
   PLANF033R4 slice's row `| rule the client's invented id | done | this round,
   DECISION F033 D2 |` was applied BYTE FOR BYTE as convention 1 requires, at C1.
   Between `fa745427` and `76b6448b` the plan therefore claims something the tree
   does not yet hold. This is the block's own ordering, not a change of mine;
   recorded because AGENTS.md's Commit Gate asks that `.agent/plan.md` match the
   current work at every commit. Identical to rounds 2 and 3.

5. **G7 reddened TWO tests, not one.** The block asks for "the NAME of each failing
   test" and does not fix a count, so this is a reading rather than a departure, but
   it is worth stating: both new prefix assertions catch the mutation. Distinctness
   alone does not — a bare `0:0`/`0:1` pair is still distinct — which is why the
   distinctness test also asserts the prefix.

6. **The WHY comment is one SENTENCE wrapped over three physical lines.** SPEC §1
   asks for "a one-line WHY comment"; the sentence it dictates does not fit in one
   line at this file's width, and every other declaration in the module carries a
   wrapped JSDoc block. Wrapped rather than truncated.

7. **The commit messages carry no `Co-Authored-By` trailer.** Every commit on this
   branch and on `main` before it is written without one, and AGENTS.md prefers
   repository state over session convention; flagged because my own default is to
   add one.

8. **G8 does not cover C4.** The block explicitly excludes C4's own numbers from G8
   and hands them to the reviewer at the next gate, so this handback's own commit is
   tabled above but not gated here.

Nothing was routed around, no gate went red, and no ordered number failed to
reproduce. No part of the SPEC turned out impossible.

Assumptions: none beyond the above. `.agent/context.md` and `.agent/decisions.md`
needed no update — the change set forbids them, and DECISION F033 D2 is recorded in
`.agent/live_review.md` by C2. `docs/` needed none either: no page under `docs/`
states the client's id fallback, the rule lives in the module's own contract note
where a reader searching for it lands, and `tests/ui_contracts/test_diff_view_model.py`
already forces every export of this module to be named by the vitest suite.

## Next

Reviewer gates round 4 at `51e04c89..HEAD` on `feature/f033-hunk-approval-v2`. I
wrote no verdict on my own work. Round 5, per the plan, retires the local hunk helper
in `packages/orchestration/diff_repair.py` onto `hunk_identity`, which closes T001.
