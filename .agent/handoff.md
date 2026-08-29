# Handback — F033 round 2 · THE HUNK IDENTITY FUNCTION

## Session

SESSION 1 of feature F033 · round 2 · rounds so far 2

## Range

Review of `8dc4721a92c96a4e153a1f079c467a60e7f4ae04`..HEAD on branch
`feature/f033-hunk-approval-v2`.

BASE = `8dc4721a92c96a4e153a1f079c467a60e7f4ae04` — the round 1 handback commit,
confirmed by `git rev-parse HEAD` before C0a. Every base number the block stated
reproduced against it: `.agent/live_review.md` 1431859 bytes,
`.agent/prose_slips.md` 17728 bytes, registered 299, `Done:` 44 over 42 distinct,
`Landed:` 11, `Gate:` 118, open set 257.

## Commits

### 749316a2 docs(f033): save the round 2 identity block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r2.md | +331 / -0 | C0a — the reviewer's block, copied byte for byte with `shutil.copyfile` |

### 1198698c chore(f033): mirror the round 2 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +251 / -305 | C0b — mirror of the COMMITTED C0a blob, one blob id |

### 3cb1914c docs(f033): advance the plan to the identity round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +16 / -14 | C1 — replaced ENTIRELY with the PLANF033R2 slice (2137 bytes, 41 lines, under the 50-line cap) |

### 879b084d docs(f033): book the round 1 verdict
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 / -0 | C2 — append of one newline plus the RECORDF033R2 slice (3900 bytes, one paragraph) |

### 0cb69c59 docs(f033): record two reviewer prose slips from round 1
| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +4 / -0 | C3 — append of one newline plus the SLIPF033R2 slice (952 bytes, two slip lines) |

### 05168c05 feat(f033): add the stable hunk identity function
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/hunk_identity.py | +132 / -0 | C4 — the new module, written from the block's SPEC |
| tests/orchestration/test_hunk_identity.py | +216 / -0 | C4 — ten property tests, named for the property |

### C5 (this commit) docs(f033): hand back the round 2 identity result
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | +301 / -387 | C5 — this file, measured with `git diff --numstat` before committing; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/f033-g7-wt 05168c05 --detach` | created, detached HEAD at `05168c05` |
| `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f033-g7-wt` | removed BY EXACT PATH, exit 0 |
| `git worktree prune` | exit 0; `git worktree list` then shows only the primary checkout |
| `git push` | after C5 — see the push line at the end of Verification |

No pull request created, none edited, nothing merged. No `gh` command run. No
force-push, no history rewrite, no branch deletion.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a (directory listing
of `.agent/`, absent) and again before C5 (`ls -a .agent/ | grep -x "STOP"` printed
nothing, then the sentinel line `STOP-listing-done`) — absent BOTH times.
`git status --porcelain` printed nothing after every one of the six commits.
`git branch --show-current` read `feature/f033-hunk-approval-v2` at C0a, at C0b, at
C4 and at C5. No force-push, no history rewrite, no branch deletion.
`git rev-parse feature/f033-hunk-approval` reads
`ed04081283081f237d96147da39a07fca0b1ccad` at C5 — the parked branch is UNDISTURBED
and was not checked out, read or touched this round.

**G2 TRANSPORT — PASS, EQUAL.**

    .remedy-wt/f033-r2-block.md      22433 bytes  sha256=4ee838f6dd706077033192557770d6a1ae5728dcede851ce7c87269fd97e9190
    749316a2:.agent/authored/f033-r2.md  22433 bytes  sha256=4ee838f6dd706077033192557770d6a1ae5728dcede851ce7c87269fd97e9190
    EQUAL: yes (byte length and digest both)

    git rev-parse 1198698c:.agent/authored/f033-r2.md -> 371866589a53d37f16457ac93a4e885c773c17da
    git rev-parse 1198698c:.agent/last_block.md       -> 371866589a53d37f16457ac93a4e885c773c17da
    ONE blob id: yes

The digest also matches the one the delegation message stated over 22433 bytes, so
the reading covers delivery and not only my own self-consistency.

**G3 THE TWO APPENDS — PASS.** `.remedy-wt/f033r2_g3.py`, real exit 0:

    BASE blob bytes = 1431859 (block states 1431859: True)
    C2   blob bytes = 1435760      slice bytes = 3900
    N (paragraphs COUNTED in the slice) = 1
    reader (a) BYTE       on C2: True  (equal, prefix, one-trailing-newline) = (True, True, True)
    reader (b) STRUCTURAL on C2: True  (file paragraph count 668, tail match True)
    first appended paragraph spans bytes 1431860..1435759 (len 3899)
    negative control offset 1433809 lies inside it: True
    byte at control offset before mutation: b'O'   after: b'Z'
    reader (a) on CONTROL: False   detail=(equal False, prefix True, newline True)
    reader (b) on CONTROL: False   detail=(668, False)
    G3 live_review VERDICT: True

BOTH readers rejected the control, and the control offset was PROVED inside the
FIRST appended paragraph rather than asserted — 1431860 <= 1433809 < 1435759.
1431859 + 1 + 3900 = 1435760, the C2 blob exactly.

`.remedy-wt/f033r2_g3b.py` over `.agent/prose_slips.md`, real exit 0:

    BASE blob bytes = 17728 (block states 17728: True)
    C3   blob bytes = 18681      slice bytes = 952
    base + one newline + slice == C3 blob: True
    base is a byte PREFIX of C3: True        C3 ends in exactly one newline: True
    lines beginning '- R-' in C3: 0 (must be 0)
    lines matching '^2026-\d\d-\d\d · F033 R1 · ': base=0 C3=2 (added 2, must be 2)
    non-blank lines in the slice: 2   every added line matches the slip pattern: True
    G3 prose_slips VERDICT: True

**G4 THE LEDGER at C2 — PASS, every ordered number reproduced.**
`.remedy-wt/f033r2_ledger.py`, real exit 0 at both revisions:

| Reading | BASE `8dc4721a` | C2 `879b084d` | Ordered |
|---------|-----------------|---------------|---------|
| `^- R-\d+ — ` lines / distinct | 299 / 299 | 299 / 299 | 299 UNMOVED |
| `^Done: R-\d+ — ` lines / distinct | 44 / 42 | 44 / 42 | 44 over 42 UNMOVED |
| `^Landed: R-` | 11 | 11 | 11 UNMOVED |
| `^Gate: F\d+ R\d+ — ` | 118 | 119 | 118 -> 119 |
| `^Gate: F033 R1 — ` | 0 | 1 | exactly 1 |
| `^- R-0738 — ` | 1 | 1 | (unchanged; registered in round 1) |
| OPEN SET (distinct registered − distinct Done) | 257 | 257 | 257 UNMOVED |

This round registered no id and resolved none, as ordered.

**G5 THE MODULE AGAINST THE SPEC — PASS.** Taken at C4, before C5.

    python3 -m ruff check packages/orchestration/hunk_identity.py tests/orchestration/test_hunk_identity.py
    exit 0
    All checks passed!

`.remedy-wt/f033r2_g5.py` (AST predicate over the top-level definitions, not a text
grep), real exit 0:

    exported names DEFINED by the module (AST, top level, no leading _):
        ['HUNK_ID_LENGTH', 'hunk_identity', 'normalise_old_side']
    equals the SPEC's three names: True
    HUNK_ID_LENGTH = 16 (SPEC says 16: True)
    occurrences of the builtin call 'hash(' in the source: 0
    occurrences of 'hash(' by naive substring:            0
    forbidden imports found: []          occurrences of 'open(': 0
    hunk_identity('a.py', ['x']) = 'fbbbcf6d501305b0'  len=16  lowercase hex of length 16: True
    G5 VERDICT: True

Both the regex reading (word-boundary `hash(`) and the naive substring reading are
reported, because the two can disagree and the gate should not turn on which one I
happened to pick. Both are 0 — see deviation 3.

**G6 THE TESTS — PASS. Run SERIALLY, one pytest process at a time, in the PRIMARY
checkout.**

    python3 -m pytest -q tests/orchestration/test_hunk_identity.py
    exit 0    10 passed in 0.25s

    python3 -m pytest -q tests/cli/test_golden_path.py
    exit 0    42 passed in 20.71s      (the canary, ordered at 42 — 42)

**G7 THE MUTATION RED-PROOFS — PASS, all three RED.** In the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/f033-g7-wt` at `05168c05`, never in the
primary checkout, every run with `python3 -B`. The worktree was created fresh so no
`__pycache__` existed, and `-B` kept one from being written; the subprocess the
cross-process test spawns also runs `-B`. Each mutation anchor was asserted UNIQUE
(FROM occurs exactly 1 time) before replacement, so a silent no-op could not pass as
a colour. Each was reverted to the pristine bytes before the next
(sha256=cd95eeb96dc94d372c7e434bccdea86948141e620f05bf327c5c76de46ab148a, 7203 bytes,
confirmed identical after every revert).

| Run | Command | Real exit | Result | Failing test |
|-----|---------|-----------|--------|--------------|
| CONTROL (unmutated) | `python3 -B -m pytest -q tests/orchestration/test_hunk_identity.py` | 0 | 10 passed | — |
| M1 `path` removed from the digest input | same | 1 | 1 failed, 9 passed | `test_the_same_content_at_a_different_path_gets_a_different_id` |
| M2 `occurrence` removed from the digest input | same | 1 | 1 failed, 9 passed | `test_two_identical_hunks_in_one_file_are_separated_by_occurrence` |
| M3 `normalise_old_side` joins with no trailing strip | same | 1 | 1 failed, 9 passed | `test_trailing_whitespace_does_not_change_the_id` |

The decisive assertion lines, as the runner printed them:

    M1: assert '174cb98d6a42ce3d' != '174cb98d6a42ce3d'          (two paths collapsed to one id)
    M2: assert 1 == 3  +  where 1 = len({'87b82be450daf28b'})    (three occurrences collapsed to one id)
    M3: assert 'c77faf41034001ff' == '6481bdf440a1300b'          (padded and bare no longer agree)

No mutation came back green, so there is nothing to report under the green-mutation
rule. Worktree removed BY EXACT PATH with `--force`, then `git worktree prune`;
`git worktree list` afterwards shows only `/home/decodeux/Repos/remedy`, and
`git status --porcelain` in the primary checkout was empty before, during and after.

**G8 STRUCTURE — PASS.** `.remedy-wt/f033r2_g8.py` over
`git rev-list --reverse 8dc4721a..05168c05`, real exit 0. Six commits, each with
exactly ONE parent, each under 500 INSERTIONS (the `+` column of
`git diff --numstat`, never insertions plus deletions):

| Commit | Parents | Insertions | Paths |
|--------|---------|-----------|-------|
| 749316a2 | 1 | 331 | `.agent/authored/f033-r2.md` |
| 1198698c | 1 | 251 | `.agent/last_block.md` |
| 3cb1914c | 1 | 16 | `.agent/plan.md` |
| 879b084d | 1 | 2 | `.agent/live_review.md` |
| 0cb69c59 | 1 | 4 | `.agent/prose_slips.md` |
| 05168c05 | 1 | 348 | `packages/orchestration/hunk_identity.py`, `tests/orchestration/test_hunk_identity.py` |

Path set, BOTH directions: touched but NOT in the declared change set — none.
In the change set but NOT touched — `.agent/handoff.md` only, which C5 writes and
which is therefore expected to be absent from the `BASE..C4` range. Nothing outside
the change set was created, edited or deleted; `packages/orchestration/diff_parser.py`,
`diff_view_source.py`, `diff_repair.py`, `apps/ui/**` and `docs/roadmap/STATUS.md`
are untouched.

Delimiter residue, with the saved block as a NON-ZERO control:

    target  .agent/plan.md                             '<<<SLICE ' = 0, '<<<END ' = 0
    target  packages/orchestration/hunk_identity.py    '<<<SLICE ' = 0, '<<<END ' = 0
    target  tests/orchestration/test_hunk_identity.py  '<<<SLICE ' = 0, '<<<END ' = 0
    CONTROL .agent/authored/f033-r2.md                 '<<<SLICE ' = 6, '<<<END ' = 8

    git ls-files .remedy-wt = 0

## What shipped — the two public signatures and the test names

`packages/orchestration/hunk_identity.py`, 132 lines:

    HUNK_ID_LENGTH = 16

    def normalise_old_side(lines: Iterable[str]) -> str

    def hunk_identity(path: str, old_side_lines: Iterable[str], occurrence: int = 0) -> str

`Iterable` is imported from `collections.abc` (ruff's UP rules reject the `typing`
spelling). The digest material is
`path + "\x00" + normalise_old_side(old_side_lines) + "\x00" + str(occurrence)`,
encoded `utf-8` with `errors="replace"`, hashed with `hashlib.sha256`, truncated to
`HUNK_ID_LENGTH` hex characters. Private helpers `_total_text`, `_occurrence_text`
and the constant `_FIELD_SEPARATOR` carry the totality guards.

`tests/orchestration/test_hunk_identity.py`, 216 lines, ten tests:

| # | Test | Property |
|---|------|----------|
| 1 | `test_the_same_hunk_re_emitted_keeps_its_id` | SPEC 1 — determinism in one process |
| 2 | `test_an_edit_elsewhere_leaves_other_hunk_ids_unchanged` | SPEC 2 — THE stability property |
| 3 | `test_trailing_whitespace_does_not_change_the_id` | SPEC 3 |
| 4 | `test_leading_whitespace_does_change_the_id` | SPEC 4 — the negative of 3 |
| 5 | `test_the_same_content_at_a_different_path_gets_a_different_id` | SPEC 5 |
| 6 | `test_two_identical_hunks_in_one_file_are_separated_by_occurrence` | SPEC 6 |
| 7 | `test_the_id_is_stable_across_processes` | SPEC 7 — `PYTHONHASHSEED` 1 and 424242 |
| 8 | `test_a_lone_surrogate_cannot_be_encoded_strictly` | ADDED — pins the encoding clause (deviation 1) |
| 9 | `test_hostile_input_never_raises_and_still_returns_an_id` | SPEC 8 — totality |
| 10 | `test_the_id_shape_is_lowercase_hex_of_the_declared_length` | SPEC 9 |

Test 2 carries a DISCRIMINATOR: it asserts the EDITED hunk's id really did change
before asserting the other hunk's id did not, so the unchanged reading is evidence
about stability rather than about a function that ignores its input. Test 7 compares
both children against each other AND against the in-process call, and asserts each
child's real exit code. Test 9 asserts a WELL-FORMED id in every hostile case — type,
length and lowercase-hex — rather than merely that nothing raised.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `749316a2`, `shutil.copyfile`, byte-identical |
| C0b mirror it | done | `1198698c`, one blob id `371866589a53d37f16457ac93a4e885c773c17da` |
| C1 `.agent/plan.md` | done | `3cb1914c`, PLANF033R2 applied whole, byte-equal to the slice |
| C2 round 1 verdict into `.agent/live_review.md` | done | `879b084d`, two readers plus a rejected negative control |
| C3 two reviewer slips into `.agent/prose_slips.md` | done | `0cb69c59`, byte check, 0 lines beginning `- R-` |
| C4 the new module and its tests | done | `05168c05`, written from the SPEC, both files in one commit |
| C5 the handback | done | this commit |
| G1 HYGIENE | done | pass |
| G2 TRANSPORT | done | pass, EQUAL, one blob id |
| G3 THE TWO APPENDS | done | pass, N=1, control rejected by both readers |
| G4 THE LEDGER at C2 | done | pass, every ordered number reproduced |
| G5 THE MODULE AGAINST THE SPEC | done | pass, ruff exit 0, three exported names, id `fbbbcf6d501305b0` |
| G6 THE TESTS | done | pass, 10 and 42, both exit 0, run serially |
| G7 THE MUTATION RED-PROOFS | done | pass, control green then M1/M2/M3 all RED |
| G8 STRUCTURE | done | pass, 6 single-parent commits, max 348 insertions |

## Authored-text proofs

| Text | Proof |
|------|-------|
| the block itself | `.remedy-wt/f033-r2-block.md` and `749316a2:.agent/authored/f033-r2.md` are both 22433 bytes at sha256 `4ee838f6…9190` — EQUAL |
| PLANF033R2 | extracted from the COMMITTED blob `749316a2:.agent/authored/f033-r2.md` (saved to `.remedy-wt/c0a_blob.md`), 2137 bytes sha256 `e2f9dd3a…e621`; `.agent/plan.md` on disk carries the identical digest |
| RECORDF033R2 | extracted from the same committed blob, 3900 bytes sha256 `85529a4f…43fc`, one paragraph; appended verbatim |
| SLIPF033R2 | extracted from the same committed blob, 952 bytes sha256 `c6e19b95…d3fc`, two slip lines; appended verbatim |

Every slice's named delimiter (`<<<SLICE NAME` / `<<<END NAME`, anchored at line
start) was asserted to occur EXACTLY ONCE before extraction, and every slice was
confirmed to end in exactly one trailing newline. No slice was retyped.

## Deviations & assumptions

The block's ordered commit sequence was followed exactly: C0a, C0b, C1, C2, C3, C4,
C5, in that order, no extra commit, none dropped, none reordered.

1. **One test beyond the SPEC's nine.** `test_a_lone_surrogate_cannot_be_encoded_strictly`
   is an ADDITION. The SPEC says "Cover at least these properties" and states that the
   reviewer measured `"\ud800".encode("utf-8")` raising while `errors="replace"` yields
   `b"?"`; I re-measured both before writing the module (they hold) and pinned them in a
   test, so the load-bearing encoding clause is asserted rather than only asserted-about.
   The count reported everywhere in this handback is therefore 10, not 9.
2. **A totality guard the SPEC did not enumerate.** `normalise_old_side` wraps
   `list(lines)` in a `try`, and treats a NON-iterable argument as a single line rather
   than raising `TypeError`. The SPEC's binding property is that the module "NEVER raises
   on any input", and a non-iterable is an input; the SPEC's hostile-input list does not
   name that case, so this is my judgement about internal structure, declared here rather
   than left for the reviewer to find. It is exercised only indirectly.
3. **The module names the forbidden builtin without its parentheses.** G5 forbids the
   SOURCE containing `hash(`, and the SPEC separately requires the module to explain why
   the builtin is not used. Written naturally the docstring would contain the literal
   substring `hash(` and G5 would go red on prose rather than on code. I resolved it by
   writing "the builtin ``hash``" in the docstring instead of "``hash()``". The
   explanation is intact, the gate reads 0, and I am flagging the tension because a
   future round widening that gate should know the two clauses can collide.
4. **`_occurrence_text` is annotated `Any`, not `object`.** `int(x)` where `x: object` is
   a mypy `arg-type` error, and `warn_unused_ignores = true` in `pyproject.toml` makes a
   speculative `# type: ignore` an error in its own right, so `Any` was the only spelling
   that is clean under both tools. mypy was not an ordered gate this round; ruff was, and
   it passes.
5. **C1's plan slice books C4's work as "done" one commit before C4 lands it.** The
   PLANF033R2 slice's row `| the shared identity function and its tests | done | this
   round |` was applied BYTE FOR BYTE as convention 1 requires, at C1. Between `3cb1914c`
   and `05168c05` the plan therefore claims something the tree does not yet hold. This is
   the block's own ordering, not a change of mine; recorded because AGENTS.md's Commit
   Gate asks that `.agent/plan.md` match the current work at every commit.
6. **The block's own gate arithmetic is fine; nothing in it contradicted itself.** No
   ordered number failed to reproduce, no gate went red, and no part of the SPEC turned
   out impossible. Nothing was routed around and no scope was widened.

Assumptions: none beyond the above. `.agent/context.md`, `.agent/decisions.md` and
`docs/` needed no update this round — the change set forbids them, the module is
internal and unwired, and the durable documentation belongs with round 3's parser
wiring and `DIFF_VIEW_VERSION` bump, where the behaviour becomes visible.

## Next

Reviewer gates round 2 at `8dc4721a..HEAD` on `feature/f033-hunk-approval-v2`. I
wrote no verdict on my own work. Round 3, per the plan, wires `hunk_identity` into
`packages/orchestration/diff_parser.py`, bumps `DIFF_VIEW_VERSION` to 2, moves the
tests that pin version 1, and rules the client fallback at
`apps/ui/src/api/diffViewModel.ts`.
