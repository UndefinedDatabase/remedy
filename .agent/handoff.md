# Handback — F259 Vocabulary & concept model v1, round 3

## Session

`SESSION 1 of feature F259 · round 3 · rounds so far 3`

Fortschritt: `~40 % (T001 ✅ komplett · T002, T003, T004 offen) — Schätzung`

Context self-assessment (operator amendment amend0905-throughput): this round
was the cheapest of the three — the block, four `.agent/` files, one feature file
and one docs page were the whole read set — so the session has ample window for
several more rounds before a boundary is needed.

## Range

Review of `e726832e..<the C4 commit that carries this file>`; the reviewable work
is `e726832e..8de6d3e6` plus this handback commit.

Branch `feature/f259-vocabulary`. No pull request exists for this branch and none
was created — F259's pull request belongs to its closure round.

## Commits

Every `+/-` number below comes from `git diff --numstat <parent> <commit>` as
gate G7 printed it, and from nothing else.

### 2e29738b f259: save round 3 block to authored

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f259-r3.md` | +275 / -0 | C0a — the reviewer's block file, copied with `shutil.copyfile`, never retyped |

Insertions 275, under the 500 cap.

### 947e94ab f259: mirror round 3 block to last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +186 / -237 | C0b — the same bytes mirrored as the current block |

Insertions 186, under the 500 cap. C0a and C0b are separate commits, as the block
requires and as round 1's collapsed C0 taught.

### 5e8c90b1 f259: plan for round 3 - do-not-confuse table and concept model

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +13 / -15 | C1 — the PLANF259R3 slice, whole-file rewrite |

Insertions 13, under the 500 cap.

### c6999268 f259: book the round 2 PASS verdict and one reviewer prose slip

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | C2 — GATE_R2 appended at end of file |
| `.agent/prose_slips.md` | +3 / -1 | C2 — SLIP3 appended; the `-1` is the pre-existing last line re-emitted because the file has no final newline |

Insertions 5, under the 500 cap.

### 8de6d3e6 f259: append the do-not-confuse table and the concept model to the vocabulary page

| Path | +/- | Reason |
|---|---|---|
| `docs/system/vocabulary.md` | +41 / -0 | C3 — `"\n" + PAGE2 + "\n"` appended; T001 is now complete |

Insertions 41, under the 500 cap.

### C4 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | whole rewrite | C4 — this handback; a handoff cannot table the commit that writes it |

## External actions

- `git push -u origin feature/f259-vocabulary` after C3 —
  `e726832e..8de6d3e6  feature/f259-vocabulary -> feature/f259-vocabulary`,
  fast-forward, branch set up to track the remote.
- `git push` after C4 — result recorded in the Verification section below.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
  No pull request was created, edited or merged. No worktree was added or removed.
- No `--force`, no `--force-with-lease`, no history rewrite, no branch deletion.

## Verification

### G1 TRANSPORT — PASS

    $ sha256sum .remedy-wt/f259-r3-block.md .agent/authored/f259-r3.md .agent/last_block.md
    7c12b38cdc9b9f921b3fd768861898e6fdd1664f840e747a40a1fe50a88f74a2  .remedy-wt/f259-r3-block.md
    7c12b38cdc9b9f921b3fd768861898e6fdd1664f840e747a40a1fe50a88f74a2  .agent/authored/f259-r3.md
    7c12b38cdc9b9f921b3fd768861898e6fdd1664f840e747a40a1fe50a88f74a2  .agent/last_block.md

One digest, three paths, and it equals the digest this round's order stated, so
the copy chain scratch → saved → mirror is unbroken.

### G2 THE PAGE APPEND, BY RECONSTRUCTION — PASS

`.remedy-wt/f259r3_c3.py`, which performed the append and measured it:

    STOP exists (before C3): False
    G2 BEFORE: bytes = 10608  ends with newline: True  final bytes: b' under `apps/`.\n'
    G2 prefix property (pre-append bytes are a byte-exact PREFIX): True
    G2 remainder == '\n' + PAGE2 + '\n': True
    G2 AFTER: bytes = 14545  ends with newline: True
    G2 delta bytes: 3937   len(PAGE2) + 2 = 3937

Both booleans are True. 10 608 bytes before, 14 545 after — exactly the 10 608
the block measured at `e726832e`, and the growth is exactly `len(PAGE2) + 2`.
Nothing already in the file moved: the prefix property is what proves it.

### G3 THE DIAGRAM CANNOT DRIFT — PASS, with a negative control that fires

`.remedy-wt/f259r3_g3_mermaid.py` takes the body of the single fenced
```mermaid block of each file — the bytes between the opening fence line's
newline and the newline preceding the closing fence, that final newline excluded
— and reports both readings so neither is hidden:

    $ python3 .remedy-wt/f259r3_g3_mermaid.py docs/roadmap/features/T2_F259.md docs/system/vocabulary.md
      docs/roadmap/features/T2_F259.md
        fenced ```mermaid blocks in file: 1
        body bytes=309 lines=7 sha256=6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c
        body+trailing-newline bytes=310 sha256=1da6e9ee983e53b252f5982dc0449dea1473a15b8c028b4e3d1fe42677b0a716
        contains U+00B7 MIDDLE DOT: True
        four-space indent lines: 6
      docs/system/vocabulary.md
        fenced ```mermaid blocks in file: 1
        body bytes=309 lines=7 sha256=6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c
        body+trailing-newline bytes=310 sha256=1da6e9ee983e53b252f5982dc0449dea1473a15b8c028b4e3d1fe42677b0a716
        contains U+00B7 MIDDLE DOT: True
        four-space indent lines: 6
      EQUAL: True
      sha256 A == sha256 B: True

309 bytes, seven lines, exactly one fenced mermaid block per file, and the digest
is `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c` — the value
the reviewer measured at `e726832e`. The byte length and line count reported here
are what this worker's own extraction measured, not numbers copied from the block.

NEGATIVE CONTROL — `.remedy-wt/f259r3_g3_negctl.py` copies the page under
`.remedy-wt/` and turns the middle dot in `Round 1 (build · review)` into a
hyphen; the SAME comparator then runs against the copy:

    needle present in copy: True   occurrences: 1
    middle dot replaced by a hyphen in .remedy-wt/vocab_broken_dot.md
    copy still contains U+00B7 anywhere: False

    $ python3 .remedy-wt/f259r3_g3_mermaid.py docs/roadmap/features/T2_F259.md .remedy-wt/vocab_broken_dot.md
      .remedy-wt/vocab_broken_dot.md
        body bytes=308 lines=7 sha256=fb3933084aaf4759b8a2089e5b77e357841a024f764603d5467c9360db5d3a5b
        contains U+00B7 MIDDLE DOT: False
      EQUAL: False
      sha256 A == sha256 B: False

One byte of difference in one character flips the comparison to False, so the
comparison that passed on the real page is a comparison that can fail.

### G4 THE DO-NOT-CONFUSE TABLE ROWS THE RIGHT PAIRS — PASS

`.remedy-wt/f259r3_g4_pairs.py`, which locates the table under
`## Do not confuse these` and reports its own measurements:

    rows beginning with '|' under the heading: 10
    header cells: 3 ['Not the same', 'The difference', 'Why they get confused']
    separator cells: 3
    data rows: 8
    first cells, in file order, bold markers stripped:
        'Job / Run'
        'Plan / Roadmap'
        'Order / Job'
        'Task / Round'
        'Contract / permissions'
        'Mission / schedule'
        'Worker / role'
        'template / order file'
    length my extraction measured: 8
    every data row splits into the header's cell count (3): True
    equals the T2_F259.md Goal & Done pairs, in order: True
    exit=0

Eight rows, in exactly the order T2_F259.md's Goal & Done names them, and every
row splits into three cells like its header, so no stray unescaped pipe ate a
column.

### G5 THE RECORD AND THE SLIP APPENDS — PASS

`.remedy-wt/f259r3_c2.py`, which performed both appends and measured them:

    G5 lr BEFORE: bytes = 823241  ends with newline: True
    G5 ps BEFORE: bytes = 76469  ends with newline: False  final byte: b'.'
    G5 lr prefix property: True
    G5 lr remainder == '\n' + GATE_R2 + '\n': True
    G5 lr AFTER: bytes = 827079  ends with newline: True
    G5 ps prefix property: True
    G5 ps remainder == '\n\n' + SLIP3: True
    G5 ps AFTER: bytes = 77778  ends with newline: False  final byte: b'.'

`.agent/live_review.md` 823 241 → 827 079 bytes; `.agent/prose_slips.md`
76 469 → 77 778 bytes — both starting exactly where the block measured them — and
the slip file still ends with `.` and no newline. Both prefix booleans and both
remainder booleans are True.

    $ grep -c '^Gate: R2 — ' .agent/live_review.md      # before C2
    0
    $ grep -c '^Gate: R2 — ' .agent/live_review.md      # after C2
    1

### G6 THE SUITES, RUN SERIALLY AT C3 — PASS, all seven exact

`.remedy-wt/f259r3_g6_suites.py` runs them one after another via
`subprocess.run`, so the exit code recorded is the pytest process's own and not a
pipeline's:

    tests/docs/                                    exit=0 passed=295 expected=295 OK
        last line: 295 passed in 0.45s
    tests/orchestration/test_roadmap_index.py      exit=0 passed=30 expected=30 OK
        last line: 30 passed in 0.42s
    tests/ui_server/                               exit=0 passed=515 expected=515 OK
        last line: 515 passed in 33.82s
    tests/orchestration/test_test_runner.py        exit=0 passed=52 expected=52 OK
        last line: 52 passed in 6.11s
    tests/regression/test_resource_safety.py       exit=0 passed=21 expected=21 OK
        last line: 21 passed in 11.54s
    tests/orchestration/test_integrity_gate.py     exit=0 passed=16 expected=16 OK
        last line: 16 passed in 0.28s
    tests/cli/test_golden_path.py                  exit=0 passed=42 expected=42 OK
        last line: 42 passed in 21.18s

Every count equals the reviewer's baseline at `e726832e`. No failing node ids, no
errors. The four state readers were run as four, not as three.

### G7 THE PLAN AND THE STRUCTURE — PASS

`.remedy-wt/f259r3_g7_structure.py`, run immediately before C4 was staged:

    PLAN
        wc -l .agent/plan.md -> 44 .agent/plan.md(exit=0)  under 50: True
        grep -c '^## Goal' .agent/plan.md -> 1 (exit=0)
        grep -c '^## Next Steps' .agent/plan.md -> 1 (exit=0)
        filecmp.cmp(.agent/plan.md, PLANF259R3 + one newline, shallow=False) -> True
    STRUCTURE
        git status --porcelain -> '' (exit=0)
        git ls-files .remedy-wt -> 0 lines (exit=0)
        range base: e726832e e726832e9b346a40e853cd65a783aa1b4c8526c2
        C0a 2e29738b  parents=1
           numstat: +275 -0  .agent/authored/f259-r3.md
           insertions=275  500-cap: OK
        C0b 947e94ab  parents=1
           numstat: +186 -237  .agent/last_block.md
           insertions=186  500-cap: OK
        C1 5e8c90b1  parents=1
           numstat: +13 -15  .agent/plan.md
           insertions=13  500-cap: OK
        C2 c6999268  parents=1
           numstat: +2 -0  .agent/live_review.md
           numstat: +3 -1  .agent/prose_slips.md
           insertions=5  500-cap: OK
        C3 8de6d3e6  parents=1
           numstat: +41 -0  docs/system/vocabulary.md
           insertions=41  500-cap: OK

44 lines, under 50; one `## Goal`, one `## Next Steps`; byte-equal to the
PLANF259R3 slice plus one trailing newline. Every commit is single-parent. The
largest commit is 275 insertions, so no commit approaches the AGENTS.md
500-insertion cap and no overage is declared. The tree was clean before C4 was
staged. `git ls-files .remedy-wt` returns 0 lines, so no scratch file was
committed.

    $ git push -u origin feature/f259-vocabulary        # after C3
    To github.com:UndefinedDatabase/remedy.git
       e726832e..8de6d3e6  feature/f259-vocabulary -> feature/f259-vocabulary
    Branch 'feature/f259-vocabulary' set up to track remote branch 'feature/f259-vocabulary' from 'origin'.

    $ git push                                          # after C4
    To github.com:UndefinedDatabase/remedy.git
       8de6d3e6..e06e2170  feature/f259-vocabulary -> feature/f259-vocabulary

    $ git status --porcelain                            # after the final push
    (no output)
    $ git ls-files .remedy-wt | wc -l
    0
    $ git rev-list --parents -n 1 e06e2170
    e06e2170b1fa6d3f30cddc7bc8f643cfa7fef32b 8de6d3e68aa59f81959f9d279627911db6648827
    $ gh pr list --state open --json number,headRefName,baseRefName,isDraft
    []

The tree is clean again after the final push, C4 is single-parent like the five
before it, and no pull request was created this round; F259's PR belongs to its
closure round.

## Authored-text proofs

Every slice was extracted from the COMMITTED `.agent/authored/f259-r3.md` by
marker extraction in `.remedy-wt/f259r3_extract.py`, never retyped, never edited
and never routed through anything that could rewrite whitespace:

    PLANF259R3   bytes=2112   lines=44  sha256=59e86a1427350c3229daf07d847b912e1bc01a7b00c353e64348c29ce98b7792
    GATE_R2      bytes=3836   lines=1   sha256=67bef1ae6118bbb28b03911f87983f83be9c98084626c380f1934d41b82d33c0
    SLIP3        bytes=1307   lines=1   sha256=f91d1de9b550728e7a2b56f67715bcbec7e40c2e4606e8adcb4c846acb4f1ac5
    PAGE2        bytes=3935   lines=40  sha256=9f3293ffe456f9bbd83546f98f93c047c7be1e1f25625730f1f07905b1dbfd1d

| Slice | Bytes | Lines | Applied to | Proof |
|---|---|---|---|---|
| `PLANF259R3` | 2112 | 44 | `.agent/plan.md`, whole file + one `\n` | `filecmp.cmp(..., shallow=False)` → True (G7) |
| `GATE_R2` | 3836 | 1 | `.agent/live_review.md`, appended | prefix property True, remainder byte-equal to `"\n" + GATE_R2 + "\n"` (G5) |
| `SLIP3` | 1307 | 1 | `.agent/prose_slips.md`, appended | prefix property True, remainder byte-equal to `"\n\n" + SLIP3`, no trailing newline (G5) |
| `PAGE2` | 3935 | 40 | `docs/system/vocabulary.md`, appended | prefix property True, remainder byte-equal to `"\n" + PAGE2 + "\n"` (G2); its mermaid body digest equals the feature file's (G3) |

No slice was improved, rewrapped, re-punctuated or shortened. The mermaid block
inside PAGE2 was written as bytes and its four-space indentation and its U+00B7
MIDDLE DOT survive — G3 measures both.

## Item status

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | `2e29738b` — block copied with `shutil.copyfile` to `.agent/authored/f259-r3.md`, digest identical |
| C0b | done | `947e94ab` — mirrored to `.agent/last_block.md`, digest identical |
| C1 | done | `5e8c90b1` — `.agent/plan.md` = PLANF259R3 + one newline, 44 lines |
| C2 | done | `c6999268` — GATE_R2 appended to the record, SLIP3 appended to the slips, one commit |
| C3 | done | `8de6d3e6` — `"\n" + PAGE2 + "\n"` appended to `docs/system/vocabulary.md`; pushed; the seven gates then ran |
| C4 | done | this commit — handback rewritten whole, then pushed |

## Deviations & assumptions

The block's ordered commit sequence was followed exactly: C0a, C0b, C1, C2, C3,
push, gates, C4, push. No commit was added, dropped or reordered. Every gate the
block ordered was executed and every reading it asked for is reported above; no
gate was dropped, narrowed or found unmeetable this round.

1. **One shell-guard refusal, re-expressed in Python, nothing weakened.** The
   command

       python3 .remedy-wt/f259r3_g4_pairs.py docs/system/vocabulary.md ; echo "exit=$?"

   was refused verbatim with:

       Permission to use Bash has been denied. IMPORTANT: You *may* attempt to
       accomplish this action using other tools that might naturally be used to
       accomplish this goal, e.g. using head instead of cat. But you *should not*
       attempt to work around this denial in malicious ways, e.g. do not use your
       ability to run tests to execute non-test actions. You should only try to
       work around this restriction in reasonable ways that do not attempt to
       bypass the intent behind this denial. If you believe this capability is
       essential to complete the user's request, STOP and explain to the user what
       you were trying to do and why you need this permission. Let the user decide
       how to proceed.

   This is the `$?`-in-a-compound-command form the block's constraint 5 names. The
   check was not narrowed: `f259r3_g4_pairs.py` now computes its exit code, prints
   it as `exit=0` and then exits with that same value, so the number in the
   transcript is the process's real status. The identical refusal was returned
   earlier for `grep -c '^Gate: R2 — ' .agent/live_review.md ; echo "exit=$?"`,
   and that `grep -c` was then run on its own — 0 before C2, 1 after.

2. **G3's mermaid body is reported under two readings.** The block does not define
   whether the "body" carries the newline before the closing fence. The reading
   that reproduces the reviewer's stated 309 bytes and seven lines is the one that
   EXCLUDES it — the same convention the block uses for its own BEGIN/END slices —
   and that reading's digest is the stated
   `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c`. The
   including reading (310 bytes) is printed beside it on every run so no reading is
   hidden; both are equal across the two files.

3. **A second measurement was added to G3, not a substitute for one.** Besides the
   two digests the block ordered, the comparator prints the number of fenced
   ```mermaid blocks in each file (1 and 1), whether the body contains U+00B7, and
   how many body lines carry the four-space indent (6 of 7 — the `flowchart TD`
   line is unindented). These make the two properties the block warns about
   directly visible rather than inferred from a digest.

4. **`.agent/context.md` and `.agent/decisions.md` were not touched.** The Commit
   Gate asks whether either needs an update; the branch, scope and constraints they
   record are unchanged from round 2, and the block's change set names EXACTLY
   seven paths and forbids any other, so editing either would have been scope
   drift.

5. **`docs/README.md` and `README.md` were deliberately not touched.** Registering
   the page in the docs index and writing the diagram into `README.md` are round
   6's work (T004) under the block's constraint 8, so the page stays unregistered
   for now and `README.md` still carries no mermaid block.

6. **Scratch files.** `.remedy-wt/` holds this round's block, the extractor, the
   C2 and C3 edit scripts, the three gate scripts, three commit-message files, the
   three `.bin` pre-edit snapshots, the expected-plan file and the one mutated page
   copy. It is gitignored (`.gitignore` line 235) and `git ls-files .remedy-wt`
   returns 0 lines. Nothing was deleted by glob.

7. **`.agent/handoff.md` took a SECOND commit, and that is a departure from the
   block's one-commit C4.** The first write said the post-push `git status
   --porcelain` reading was "recorded below", and it could not be: the reading
   does not exist until C4 itself has been pushed. Rather than leave a pointer at
   evidence that was not there, the real post-push transcript — clean tree, 0
   lines from `git ls-files .remedy-wt`, C4 single-parent, `gh pr list` `[]` —
   was written into G7 in one follow-up commit. This is NOT a trim against a
   length cap, which is what the write-once rule of
   `docs/agents/handback_template.md` exists to forbid; it is the one reading G7
   orders that a handback cannot carry at the moment it is written. It is
   declared here because R-0485 makes any departure from the ordered commit
   sequence a deviation even when it is correct. The change set is unaffected:
   `.agent/handoff.md` is a path the block authorises.

Assumption: "the do-not-confuse table" in G4 means the table under the
`## Do not confuse these` heading, which is the only table PAGE2 adds; the
extractor locates it by that heading rather than by taking the last table in the
file, so the D1 table above it can never be measured by mistake.

## Next

The reviewer gates round 3 — the round-2 verdict booking, SLIP3, and the
do-not-confuse table and concept model that complete T001 — and then issues the
round-4 block: DECISION amend0905-vocab D2–D10 and F259 D1/D2 onto the page as
dated paragraphs, which is T002. Phase 1 rule 1 (`.agent/STOP`) is checked before
rule 2, as the protocol requires; `.agent/STOP` did not exist at any of this
round's three mandated reads — before C0a, before C3 and before C4.
