# Handoff — F109 Semantic dedupe, SESSION 3, round 12

## Session

`SESSION 3 of feature F109 · round 12 · rounds so far 12`

Soft limit is 25 rounds / 7 sessions (self-drive protocol G7, amend0827 rule 6).
At 12 rounds and 3 sessions the limit is NOT reached, so no scope report is due.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

## THE ROUND ENDS GREEN

Round 11's red tip is repaired. All fifteen suites the block names are exit 0,
including the two that were red at `906532ef`, at the same totals: 125 and 46.
No file under `packages/` or `apps/` was touched — `git diff --name-only
906532ef..HEAD -- packages apps` is empty. Round 11's C4 stands unchanged and
is now guarded by a strictly stronger test than existed before it.

## Range

Review of `906532ef`..`ecd2a2d1` (plus the C5 handoff commit that carries this
file).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block verbatim to `.agent/authored/f109-r12.md` | done | `cp` from `.remedy-wt/f109-r12.md`, never retyped |
| C0b mirror it to `.agent/last_block.md` | done | `cp` from the saved copy |
| C1 apply SLICE PLAN to `.agent/plan.md` | done | mechanically extracted, `cmp` clean |
| C2 append SLICE RECORD to `.agent/live_review.md` | done | four paragraphs, append-only |
| C3 apply SPEC A to `tests/orchestration/test_semantic_dedupe.py` | done | first-Builder-trace selection + comment |
| C4 apply SPEC B to `tests/orchestration/test_prompt_trace.py` | done | role-declared site selection + both docstrings |
| C5 rewrite `.agent/handoff.md` | done | this file |

Every ordered item is present exactly once. No item was skipped, added,
dropped or reordered.

## Commits

### 79f629bb F109 R12 C0a: save the round 12 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f109-r12.md` | +319 / -0 | the block, copied byte for byte from `.remedy-wt/f109-r12.md` |

### bdeae810 F109 R12 C0b: mirror the round 12 block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +217 / -263 | mirror of the saved copy; single `.agent/` state file rewrite |

### fd7b8cb6 F109 R12 C1: plan for round 12 — repair the two positional selectors
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +10 / -10 | SLICE PLAN applied byte for byte |

### f15ec620 F109 R12 C2: book round 11 FAIL, register R-0775 and R-0776, correct R-0774
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +9 / -1 | SLICE RECORD appended: the R11 gate entry, the `R-0774` correction, `R-0775`, `R-0776` |

### 115fa15f F109 R12 C3: R-0775 (1) select the first Builder trace of the round, not the last
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_semantic_dedupe.py` | +23 / -11 | SPEC A: collect each round's Builder traces in order and take index 0; comment restated |

### ecd2a2d1 F109 R12 C4: R-0775 (2) guard the trace append sites by the role they declare
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_prompt_trace.py` | +34 / -10 | SPEC B: split into ALL append sites, select by declared `role=`, assert arity 2 / 1; both docstrings restated |

### C5 handoff commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | — | this handback; a handoff cannot table the commit that writes it |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f109-r12-redproof ecd2a2d1` | created, detached at `ecd2a2d1` |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f109-r12-redproof` | removed, exit 0 |
| `git worktree prune` | exit 0 |
| `ls .remedy-wt/f109-r12-redproof` | exit 2, "No such file or directory" — absence confirmed |
| `rm -f .remedy-wt/f109-r12-live-review-negctl.md` then `ls` | exit 2, absence confirmed |
| `rm -f .remedy-wt/f109-r12-mutate.py` / `rm -f .remedy-wt/f109-r12-suites.py` then `ls` | deleted by exact path, absence confirmed |
| `rm -f .remedy-wt/f109-r12-sliceplan.expected` | deleted by exact path |
| `git push -u origin feature/f109-semantic-dedupe` | see Push below |

No PR created. Nothing merged. No force-push. Branch stayed
`feature/f109-semantic-dedupe` throughout.

## Verification — eight gates, every one executed

### G1 TRANSPORT — PASS, exit 0

    $ sha256sum .remedy-wt/f109-r12.md .agent/authored/f109-r12.md .agent/last_block.md
    35e36b1c3db77b15f10f254993cc9e548eef1e224997e4292fca357c44eb4879  .remedy-wt/f109-r12.md
    35e36b1c3db77b15f10f254993cc9e548eef1e224997e4292fca357c44eb4879  .agent/authored/f109-r12.md
    35e36b1c3db77b15f10f254993cc9e548eef1e224997e4292fca357c44eb4879  .agent/last_block.md

ONE digest three times: `35e36b1c3db77b15f10f254993cc9e548eef1e224997e4292fca357c44eb4879`.
The pre-action verification against the digest the order stated also matched.
This chain compares the scratch original, the saved copy and its mirror; it
claims nothing about any earlier bytes.

### G2 THE PLAN — PASS, exit 0

Mechanical extraction: opening `<<<SLICE PLAN` at 0-based line index 190,
closing `SLICE PLAN` at 233; everything between = 1923 bytes.

    $ cmp <extracted> .agent/plan.md
    (no output)                      exit 0
    $ wc -l .agent/plan.md
    42 .agent/plan.md                 42 < 50
    $ grep -c '^## Goal' .agent/plan.md
    1
    $ grep -c '^## Next Steps' .agent/plan.md
    1

### G3 THE RECORD APPEND — PASS, four readings

(a) ARITHMETIC.

    BASE size: 2079735  sha256: 6efe5b0613b4308224f94c397653ab2c5d6efa1f41f563133bd520fe83d56918
    APPENDED length S: 10725      (payload trailing newlines stripped; separator is the blank-line boundary)
    NEW size: 2090460   expected base+S: 2090460   equal: True
    NEW sha256: c03e51ff891b68b9adb6290ca1754b52d7b28a468f6ee768aea1822069992a7a
    ends without trailing newline: True

(b) SECOND, STRUCTURALLY DIFFERENT READER — counts no byte, splits the WHOLE
file on blank-line boundaries and compares units:

    N counted from the payload itself: 4
    total units in whole file: 872
    LAST N units equal appended paragraphs IN ORDER: True
      unit -4  'Gate: F109 R11 — the round 11 entry. VERDICT FAIL, AND T'   match=True
      unit -3  'Note: R-0774 — CORRECTION, appended rather than rewritte'   match=True
      unit -2  '- R-0775 — High, THE BRANCH TIP SHIPS A RED SUITE: TWO T'   match=True
      unit -1  '- R-0776 — Low, A GATE OVER PRODUCTION CODE WAS UNMEETAB'   match=True

(c) NEGATIVE CONTROL, on the scratch copy
`/home/decodeux/Repos/remedy/.remedy-wt/f109-r12-live-review-negctl.md` only:

    TRACKED sha256 BEFORE: c03e51ff891b68b9adb6290ca1754b52d7b28a468f6ee768aea1822069992a7a
    reader (b) on TRACKED file: True
    flip offset 2070355, char ' ', confirmed identical to paras[0][10] -> INSIDE the first appended paragraph
    reader (b) on SCRATCH COPY: False        <- REJECTED
    TRACKED sha256 AFTER:  c03e51ff891b68b9adb6290ca1754b52d7b28a468f6ee768aea1822069992a7a

The tracked digest did not move. The copy was then deleted by exact path and
`ls` on that path returned exit 2, "No such file or directory".

(d) COUNTS. Base counts read from `git show 906532ef:.agent/live_review.md`,
never by rewinding the tracked file:

    grep -c '^Gate: F109 R11 — '        -> 1     (ordered 1)
    grep -c '^- R-0775 — '              -> 1     (ordered 1)
    grep -c '^- R-0776 — '              -> 1     (ordered 1)
    grep -c '^Note: R-0774 — '          -> 1     (ordered 1)
    grep -c '^- R-[0-9]\{4\} — '        -> 337   (base at 906532ef: 335)
    grep -c '^Done: R-[0-9]\{4\} — '    -> 65    (base at 906532ef: 65, UNCHANGED)

`R-0775` and `R-0776` are REGISTERED and NOT resolved — machine-checked:
`R-0775 resolved? False`, `R-0776 resolved? False`, `R-0774 resolved? False`.

### G4 THE EDIT SHAPE — PASS, no test lost

Blobs read with `git show <sha>:<path>`; nothing was written over the tracked
files. `difflib.SequenceMatcher(None, before, after, autojunk=False)` over
LINE sequences. These are REPLACE-shaped edits, so non-zero deletion counts
are expected and are not a defect.

    C3 115fa15f tests/orchestration/test_semantic_dedupe.py   before 2048 lines, after 2060
      opcodes: ['equal','replace','equal','insert','equal','replace','equal']
        ('replace', 1493, 1501, 1493, 1507)
        ('insert',  1511, 1511, 1517, 1521)
        ('replace', 1512, 1515, 1522, 1527)
      grep -c '    def test_' :  before 99  after 99   IDENTICAL

    C4 ecd2a2d1 tests/orchestration/test_prompt_trace.py      before 568 lines, after 592
      opcodes: ['equal','insert','equal','replace','equal','replace','equal','replace','equal']
        ('insert',   398, 398, 398, 409)
        ('replace',  410, 415, 421, 430)
        ('replace',  477, 479, 492, 499)
        ('replace',  492, 495, 512, 519)
      grep -c '    def test_' :  before 46  after 46   IDENTICAL

### G5 THE COLOUR — PASS, three red-proofs, each with its unmutated control

Disposable worktree at the exact path
`/home/decodeux/Repos/remedy/.remedy-wt/f109-r12-redproof`, detached at
`ecd2a2d1`.

IMPORT PROBE FIRST, worktree as cwd:

    $ python3 -B -c "import packages.orchestration.pingpong_loop as m; print(m.__file__)"
    /home/decodeux/Repos/remedy/.remedy-wt/f109-r12-redproof/packages/orchestration/pingpong_loop.py

Resolves INSIDE the worktree — no editable install is shadowing it, so the
gate is not void.

CACHE: `find <worktree> -name __pycache__ -type d | wc -l` -> 0 before the
first run; every process below is `python3 -B` with `-p no:cacheprovider`, so
none was ever created.

UNMUTATED CONTROL for all three cases, at `ecd2a2d1` unmodified:

    $ python3 -B -m pytest <the three node ids> -q -p no:cacheprovider
    3 passed in 0.51s                exit 0

(a) Deleted `composed_prompt=reviewer_composed,` from the Reviewer append.
Byte count before the write: the needle with its 24-space indentation occurs
**1** time in the file, so no disambiguation was needed. Delta -59 bytes.

    $ python3 -B -m pytest ...::test_the_reviewer_call_site_hands_its_composition_down -q -p no:cacheprovider
    >       assert "composed_prompt=reviewer_composed," in site
    E       assert 'composed_prompt=reviewer_composed,' in '...role="reviewer",...'
    1 failed in 0.33s                exit 1   <- RED as required

(b) Deleted `composed_prompt=builder_composed,` from the BUILDER FALLBACK
append. Byte counts before the write, both reported: the bare string
`composed_prompt=builder_composed,` occurs **2** times in the file, so I
quoted a longer unique string anchored on the fallback's own comment —
`                # differ only by being the REBOUND full-content pair.\n` —
which occurs **1** time, and took the FIRST needle occurrence after it, i.e.
the SECOND occurrence in the file, the fallback append. (With its 20-space
indentation the fallback line is in fact already unique at 1; the primary is
indented 16. Both readings are reported.) Delta -54 bytes.

    $ python3 -B -m pytest ...::test_the_builder_call_site_hands_its_composition_down -q -p no:cacheprovider
    >           assert "composed_prompt=builder_composed," in site
    E           assert 'composed_prompt=builder_composed,' in '...role="builder",...'
    1 failed in 0.33s                exit 1   <- RED as required

DISCRIMINATOR, run in addition to the ordered proofs and declared as an
addition below: with mutation (b) still applied, the OLD pre-C4 guard (blob
`115fa15f:tests/orchestration/test_prompt_trace.py`, the fixed-index `[1]`
version) was written into the worktree and run:

    1 passed in 0.32s                exit 0

So the old positional guard is BLIND to the fallback append and the repaired
one is not. The repair is a strict strengthening, measured rather than
asserted.

(c) Deleted the Builder fallback's recomposition statement
`builder_composed = compose_builder_prompt(effective_goal, context, **builder_compose_args)`.
Byte count before the write: **1** occurrence. Delta -107 bytes.

    $ python3 -B -m pytest ...::test_the_recorded_builder_row_describes_the_bytes_that_were_sent -q -p no:cacheprovider
    >           assert _sha256_of_marker(name) not in recorded, name
    E           AssertionError: builder_system
    1 failed in 0.45s                exit 1   <- RED as required

Restored from the `ecd2a2d1` blob by exact path between every mutation and
after the last (231824 bytes each time); the pre-C4 test file was restored
with `git checkout --`. `git -C <worktree> status --porcelain` was then EMPTY.

    $ git worktree list
    /home/decodeux/Repos/remedy                                  ecd2a2d1 [feature/f109-semantic-dedupe]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]

Only the primary checkout and the four pre-existing `remedy/job-*` worktrees.

### G6 THE SUITES — PASS, ALL FIFTEEN EXIT 0

Run SERIALLY: one `python3 -B -m pytest … -q -p no:cacheprovider` process
started, finished, and only then the next.

    EXIT 0 | tests/orchestration/test_semantic_dedupe.py                | 125 passed in 1.08s  | base: 125 total, 124 passed 1 FAILED
    EXIT 0 | tests/orchestration/test_prompt_trace.py                   |  46 passed in 0.31s  | base:  46 total,  45 passed 1 FAILED
    EXIT 0 | tests/orchestration/test_pingpong_cli.py                   | 173 passed in 2.45s  | base: 173 passed
    EXIT 0 | tests/orchestration/test_pingpong.py                       |  34 passed in 0.63s  | base:  34 passed
    EXIT 0 | tests/orchestration/test_session_resume.py                 |  27 passed in 0.55s  | base:  27 passed
    EXIT 0 | tests/orchestration/test_token_ledger.py                   | 120 passed in 10.91s | base: 120 passed
    EXIT 0 | tests/orchestration/test_token_truth.py                    |  37 passed in 0.23s  | base:  37 passed
    EXIT 0 | tests/orchestration/test_token_truth_v1_contract.py        | 101 passed in 0.32s  | base: 101 passed
    EXIT 0 | tests/orchestration/test_job_evidence.py                   |  93 passed in 18.21s | base:  93 passed
    EXIT 0 | tests/orchestration/test_provider_evidence_integration.py  |  64 passed in 0.81s  | base:  64 passed
    EXIT 0 | tests/orchestration/test_cost_report.py                    |  22 passed in 0.25s  | base:  22 passed
    EXIT 0 | tests/ui_server/test_prompt_trace_payload.py               |  20 passed in 0.18s  | base:  20 passed
    EXIT 0 | tests/ui_server/test_prompt_trace_lens.py                  |  13 passed in 0.18s  | base:  13 passed
    EXIT 0 | tests/test_observability_index.py                          |  14 passed in 0.72s  | base:  14 passed
    EXIT 0 | tests/cli/test_golden_path.py                              |  42 passed in 20.62s | base:  42 passed
    SUITES WITH NON-ZERO EXIT: 0

WHICH ONES MOVED: exactly the two the block named as the round's target, and
only in their failure count. `test_semantic_dedupe.py` went 124 passed / 1
failed -> 125 passed at the SAME total of 125. `test_prompt_trace.py` went 45
passed / 1 failed -> 46 passed at the SAME total of 46. The other thirteen are
identical to their base readings, name for name and number for number.

### G7 THE TREE — PASS

    $ git status --porcelain
    (no output)                      EMPTY
    $ git ls-files .remedy-wt
    (no output)                      nothing tracked

INSERTION COUNTS, `+` column only, per AGENTS.md DECISION F104 D1:

    79f629bb C0a  +319   .agent/authored/f109-r12.md                     < 500
    bdeae810 C0b  +217   .agent/last_block.md                            < 500
    fd7b8cb6 C1   +10    .agent/plan.md                                  < 500
    f15ec620 C2   +9     .agent/live_review.md                           < 500
    115fa15f C3   +23    tests/orchestration/test_semantic_dedupe.py     < 500
    ecd2a2d1 C4   +34    tests/orchestration/test_prompt_trace.py        < 500

Each is under 500. (C0b would additionally be exempt as the verbatim rewrite
of a single `.agent/**` state file, but it does not need the exemption.)

    $ git log --format="%h parents=%p" -7
    ecd2a2d1 parents=115fa15f
    115fa15f parents=f15ec620
    f15ec620 parents=fd7b8cb6
    fd7b8cb6 parents=bdeae810
    bdeae810 parents=79f629bb
    79f629bb parents=906532ef
    906532ef parents=d70d9b6a

Every commit is single-parent; no merge, no rewrite.

I RAN THE CELL-BY-CELL COMPARISON: I compared each `git show --numstat` pair
above against the `+/-` cell of the matching row in my own `## Commits` table,
one cell at a time — 319/0, 217/263, 10/10, 9/1, 23/11, 34/10 — and every cell
agrees. I state plainly that I ran that comparison.

### G8 THE STALENESS SWEEP — RUN, one new staleness FOUND and DECLARED

`R-0417`'s standing counter-measure. Per file this round touched:

**`tests/orchestration/test_semantic_dedupe.py`** — swept by joining every
wrapped `#` block into 108 whole comment blocks and reading each.

- REPAIRED THIS ROUND (known, ordered by SPEC A), L1485-1503: the case's own
  comment no longer says "the round 2 Builder trace records the manifest of
  the composition the fallback ABANDONED" as though there were one. It now
  states that round 2 records TWO Builder traces, that the FIRST is read, that
  `R-0774` added the second and `R-0775` is the finding closed. HOLDS.
- **NEW, NOT REPAIRED, L1881-1884** (SPEC W case 4): "the round 2 Builder
  trace describes the composition the fallback ABANDONED, not the bytes that
  left the loop." This is the SAME stale singular that SPEC A repaired
  fourteen hundred lines earlier, in a second comment the block did not name.
  It DOES NOT HOLD: round 2 now records two Builder traces and the second one
  does describe the bytes that left. No assertion depends on it — that case
  reads the CALLS, and it is green — so this is stale prose, not a wrong test.
  SPEC A says "Change nothing else in the file", so I did NOT repair it and
  declare it below instead of silently correcting the reviewer.
- L1908-1925 (the `R-0774` block header): "Until this round the Builder wrote
  its trace two statements BEFORE that recomposition and never wrote another,
  so the only Builder trace of a fallback round described the composition the
  loop had just ABANDONED." Past tense about the pre-round-11 state. HOLDS.
- L1919-1922: "SPEC O asserts what LEFT the loop and deliberately refuses to
  trust the traces." Loose rather than stale: SPEC O cases 1, 2 and 4 read the
  calls, but case 3 does read `segment_manifest` to learn WHICH names were
  replaced before it checks the calls. Pre-existing wording, unchanged by this
  round, not repaired.
- L1972 "(b) TWO INVOCATIONS, TWO TRACES", L2036 the unconditional-append
  discriminator, L2049 "one trace per role per round" as a claim about a chain
  with the opportunity to record a second — all round-11 text, all asserted by
  green cases. HOLD.
- L74/129/171/210/238/287 section round maps, L731-735 and L750-775 the
  fallback/discriminator comments, L971 "Ranks 5, 0, 2 in REGISTRATION order",
  L1204-1355 the SPEC L case map — all covered by green assertions. HOLD.

**`tests/orchestration/test_prompt_trace.py`** — swept end to end.

- REPAIRED THIS ROUND (known, ordered by SPEC B): the reviewer docstring's
  "Index [2] is the reviewer's `build_trace_entry` append; [1] is the
  builder's" is gone, replaced by the arity property the case now asserts.
  HOLDS. The builder docstring now carries the matching property paragraph.
  See deviation 1 — the builder docstring never carried an index sentence.
- L410-413 and L501-504, "The count is 2 because F109 `R-0771` added a SECOND
  composition inside the resume-fallback branch": still asserted, at L418 and
  L509, both green. HOLD.
- L334 `assert source.count("on_call=make_flight_plan_call_recorder(") == 2` —
  a count over production source, green. HOLDS.
- L353-355, the `2*(N-1)` delimiter accounting identity: asserted at L388-390,
  green. HOLDS.
- L157-159 `total_prompts == 3`, `builder_prompts == 2`, `reviewer_prompts ==
  1`: assertions over a constructed fixture, not claims about the loop. HOLD.

**`.agent/plan.md`** — 42 lines, all of it read.

- "cut from `main` at `5e18a8536afa086b591b5a2e13009d68d6227432` (pull request
  231 merged)": `git merge-base main HEAD` -> `5e18a8536afa086b591b5a2e13009d68d6227432`. HOLDS, measured.
- "Round 12, session 3, a REPAIR round … No production file changes.":
  `git diff --name-only 906532ef..HEAD -- packages apps` is empty. HOLDS, measured.
- "`R-0769` is registered, not fixed": machine-checked, `R-0769 resolved? False`. HOLDS.
- Next Steps' claim that "`token_ledger.py`'s `call_segments` table mirrors
  them column for column, so widening a row is a token-ledger change": a
  forward-looking design claim about a module this round did not touch. NOT
  RE-MEASURED this round; declared below rather than asserted.

**`.agent/authored/f109-r12.md` and `.agent/last_block.md`** — byte-identical
to the reviewer's block; every count they carry was tested this round.

- "335 at `906532ef`" and "UNCHANGED at 65": measured, both correct.
- The fifteen base suite readings: all fifteen reproduced (the two targets at
  their stated totals, the thirteen others number for number). HOLD.
- "the four pre-existing `remedy/job-*` worktrees": exactly four, listed above. HOLDS.
- SPEC B's "Each currently explains the index it used": DOES NOT HOLD for the
  builder docstring. Declared as deviation 1. These two files are the block
  itself and are copied verbatim by construction, so the sentence stays as the
  reviewer wrote it.

**`.agent/live_review.md`** — see deviation 3 for the scope of this reading.
The four appended units were read in full:

- Gate paragraph's thirteen unchanged-suite numbers "173, 34, 27, 120, 37,
  101, 93, 64, 22, 20, 13, 14, 42": all thirteen reproduced this round,
  number for number, in G6. HOLDS.
- Gate paragraph's "`- R-` rose 333 to 335, `Done: R-` unchanged at 65": the
  335 and the 65 are measured and correct at `906532ef`. The 333 at
  `c22818f5` was not re-measured this round; declared.
- `Note: R-0774`'s "line 3695 defines a closure `_rev_trace`": read at
  `packages/orchestration/pingpong_loop.py:3695`, `def _rev_trace(...)`. HOLDS, measured.
- `R-0775`'s "exit 1 at 2 failed, 169 passed" at `906532ef`: consistent with
  124 + 45 = 169. Its claim that the builder guard "takes index 1, still
  resolves, and is GREEN" is independently CONFIRMED by the G5(b)
  discriminator above. HOLDS.
- `R-0776`'s `ast.dump` reasoning: not re-measured this round; declared.
- RECORD PROPERTY FOUND BY THE SWEEP, PRE-EXISTING: `Done: R-` counts 65 LINES
  but only 63 DISTINCT ids — `R-0721` and `R-0725` each carry two `Done:`
  lines. Identical at `906532ef`, so this round neither caused nor changed it.
  The record is append-only; not repaired. Consequence for the arithmetic
  below: open findings are counted from the SETS, not the line counts.

**`.agent/handoff.md`** — this file, written last and self-consistent with
every reading above.

NOTHING WAS REPAIRED OUTSIDE THE CHANGE SET.

## Authored-text proofs

| Text | Proof | Result |
|---|---|---|
| the block itself | `sha256sum` of `.remedy-wt/f109-r12.md`, `.agent/authored/f109-r12.md`, `.agent/last_block.md` | one digest three times (G1) |
| SLICE PLAN | mechanical extraction by opening/closing line index, then `cmp` against `.agent/plan.md` | no output, exit 0 (G2) |
| SLICE RECORD | append arithmetic + independent blank-line-unit reader + negative control | base+S == new size; last 4 units match in order; mutated copy rejected (G3 a/b/c) |
| SPEC A, SPEC B | specifications, not slices — implemented in the repository's idiom, proved by G4, G5 and G6 | no test lost; three red-proofs; fifteen suites exit 0 |

## Open findings

337 distinct registered ids, 63 distinct resolved ids, **274 OPEN**.
(`grep -c '^Done: R-[0-9]\{4\} — '` reads 65 lines because two ids are
resolved twice — see the G8 sweep. The open count is a set difference, not
`337 - 65`.)

`R-0775` and `R-0776` were REGISTERED this round and are deliberately NOT
resolved, per the block's constraint 3, however green the suite ended.
`R-0774` also remains open; its own resolution clause is now satisfiable,
because the named test the clause depends on is green again and the G5(b)
red-proof demonstrates it goes red on deleting the fallback append.

## Deviations & assumptions

No departure from the block's ordered commit sequence. C0a, C0b, C1, C2, C3,
C4, C5 were committed in exactly that order, one commit each, none added, none
dropped, none reordered.

1. **SPEC B's premise about the builder docstring is false, and I applied the
   spec's intent rather than its sentence.** SPEC B says of the two cases
   "Each currently explains the index it used — 'Index [2] is the reviewer's
   `build_trace_entry` append; [1] is the builder's'". Measured at `906532ef`:
   ONLY the reviewer docstring contained that sentence. The builder docstring
   contained no index sentence at all — its second paragraph read "Same
   `inspect.getsource` pattern as the CLI guards above." I therefore could not
   "replace that sentence" in the builder docstring; I added the property
   paragraph SPEC B orders ("naming `R-0774` … and `R-0775` …") and left every
   other sentence of both docstrings, including the `R-0771` paragraph,
   untouched, as SPEC B requires. Declared rather than silently corrected.

2. **G8 found a second stale sentence that the round's own constraints forbid
   repairing.** `tests/orchestration/test_semantic_dedupe.py:1881-1884` says
   "the round 2 Builder trace describes the composition the fallback
   ABANDONED, not the bytes that left the loop" — the same singular SPEC A
   repaired at L1485-1503. It no longer holds. SPEC A's closing line is
   "Change nothing else in the file", so I did not touch it. It is prose only:
   the case it sits in reads the CALLS, asserts nothing about traces, and is
   green. It needs one comment edit in a later round. This is the `R-0775`
   class recurring in prose rather than in a selector, and it is exactly the
   kind of thing a §3 item 7 grep of the file's own comments would have caught
   when SPEC A was authored.

3. **G8's "re-read it end to end" was scoped for `.agent/live_review.md`.**
   The file is 2,090,460 bytes in 872 blank-line units; a literal end-to-end
   prose reading of 868 units of append-only history is not something I can
   honestly claim to have done. What I DID do: read all four newly appended
   units in full, and run machine sweeps over the WHOLE file for the count
   claims that could have moved (registered-id set, resolved-id set, duplicate
   `Done:` ids, the four `grep -c` patterns the block names). Declared so the
   reviewer can judge the reading rather than trust the word "swept".

4. **Three claims inside the appended record were NOT re-measured by me** and
   are reported as the reviewer's readings, not as mine: the "333 at
   `c22818f5`" base count, `R-0773`'s `grep -c 'config plumbing that supplies'`
   readings at `c22818f5`, and `R-0776`'s `ast.dump` reasoning. Each concerns a
   commit outside this round's range.

5. **One reading was run that the block did not order**, added beside the
   ordered proofs and never in place of one: under mutation G5(b), the OLD
   pre-C4 builder guard (blob `115fa15f`) was written into the disposable
   worktree and run, and it PASSED (exit 0) where the repaired guard FAILED.
   The block asserts "the old positional guard could not see this site at
   all"; this measures it. Both files were restored from their blobs
   afterwards and the worktree's `git status --porcelain` was EMPTY before
   removal.

6. **G5(b)'s byte count has two honest readings and I report both.** The bare
   string `composed_prompt=builder_composed,` occurs 2 times in
   `pingpong_loop.py`; with its 20-space fallback indentation the line occurs
   1 time, because the primary append is indented 16. Since the plain count is
   not 1, I followed the block's instruction anyway and anchored on a longer
   unique string containing part of the fallback's own comment, taking the
   second occurrence in the file.

7. **`.agent/plan.md`'s `call_segments` "column for column" claim was not
   re-measured.** It is a forward-looking design constraint about
   `token_ledger.py`, which this round did not touch and is not in the change
   set.

Assumption: the block's "`base + S` equals the new size exactly" reading of S
is the length of the bytes actually appended — the blank-line separator plus
the newline-stripped payload — since the base file ends without a trailing
newline. Under that reading the arithmetic closes exactly at 10725.

## Push

    $ git push -u origin feature/f109-semantic-dedupe

See the session output for the real result; the branch is pushed after the C5
commit and nothing else follows it. No PR was created, nothing was merged, and
no push used `--force` or `--force-with-lease`.

## Next

Review round 12 over `906532ef..HEAD`. The branch is green on all fifteen
named suites, so the next authored round is the one the plan's Next Steps
already names — surface `deduped_segment_names` on `PromptTraceEntry` at the
`segment_manifest` seam — and it should carry, as a small rider, the one-line
comment repair at `tests/orchestration/test_semantic_dedupe.py:1881-1884` that
deviation 2 declares and this round had no authority to make. Phase 1 rule 1
first: re-read `.agent/STOP` from disk before anything else.
