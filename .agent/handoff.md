# Handback — F109 Semantic dedupe, round 18 — CLOSURE PREPARATION

## Session

SESSION 4 of feature F109 · round 18 · rounds so far 18

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 18 rounds and 4 sessions it is NOT reached, so no scope report is due.
`.agent/STOP` was read from disk before the first commit and does not exist; it
was re-read before this handback and still does not exist.

## State

| Feld | Wert |
|------|------|
| **Feature** | F109 Semantic dedupe (T3) |
| **Branch** | `feature/f109-semantic-dedupe` |
| **Runde** | 18 (Session 4) |
| **Vorheriger Stand** | `50526376` |
| **Fortschritt** | ~97 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration Gate ✅ · Closure offen) — Schätzung |
| **Gates** | G1-G8 alle GRÜN, echte Exit-Codes unten |
| **Offene Findings** | 277 (Mengendifferenz, nicht Subtraktion) |

The `Fortschritt` row above is the block's SLICE FORTSCHRITT, applied verbatim
as its own line — constraint 5 and finding `R-0418`'s standing form for
self-drive, where a worker never sees the reviewer's operator brief.

## Range

Review of `50526376..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `a5fb260b` | done | block copied verbatim with `shutil.copyfile`; G1 `cmp` exit 0 against the reviewer's own `.remedy-wt/f109-r18.md` |
| C0b `9284e364` | done | mirrored to `.agent/last_block.md`; one sha256 for both copies |
| C1 `ce1b9227` | done | PLAN18 extracted by delimiter index from the COMMITTED authored copy and applied; G2 `cmp` exit 0, 44 lines |
| C2 `18f0c9c6` | done | RECORD18 appended as the two bytes `\n\n` + slice; G3 (a)(b)(c)(d) all pass |
| C3 `b89456a6` | done | PAIR F applied byte for byte; FROM 1→0, TO 0→1, 130 cases collected before and after, AST profile unchanged |
| C4 `b2814f5d` | done | BUILTSTATE appended as the one byte `\n` + slice; one `## Built State` heading, exactly one trailing newline |
| C5 (this commit) | done | handback rewritten per handback_template.md, then pushed |

No item was skipped and none deviated. The block's ordered commit sequence was
followed exactly — no extra commit, no dropped commit, no reordering. The
DEVIATIONS section below records observations made while running the gates;
none of them changed the commit sequence and none of them altered a slice.

## Commits

### a5fb260b F109 R18 C0a: save the round 18 block verbatim as authored text
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f109-r18.md` | +316 / -0 | the reviewer's block saved verbatim; transport proof's first link |

### 9284e364 F109 R18 C0b: mirror the round 18 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +200 / -173 | round 17's block replaced by round 18's; same sha256 as the authored copy |

### ce1b9227 F109 R18 C1: plan for round 18 - closure preparation
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +15 / -14 | PLAN18 applied whole; current step is round 18 closure preparation |

### 18f0c9c6 F109 R18 C2: book round 17 PASS, resolve R-0782, register R-0783
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +7 / -1 | RECORD18's three paragraphs appended: round 17 PASS verdict, `Done: R-0782`, registration of `R-0783` |

### b89456a6 F109 R18 C3: repair R-0783 - the comment names the object, not a false reason
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_semantic_dedupe.py` | +4 / -2 | ONE comment rewritten (PAIR F); no executable line moved, no case added or removed |

### b2814f5d F109 R18 C4: the feature file states its built state, scope limit first
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T3_F109.md` | +47 / -0 | the Built State section closure precondition 4 requires; pure append, nothing edited |

### C5 (this commit) F109 R18 C5: handback for round 18
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | (self-referential) | this file; its own insertion count cannot exist while the text stating it is written (constraint 7, §3 checklist item 14) |

## External actions

| Command | Outcome |
|---------|---------|
| `git push -u origin feature/f109-semantic-dedupe` | run after C5; result reported in the round report |

No worktree was added or removed this round: nothing this round ordered was
destructive, so G5's isolation requirement was never triggered. No `gh` command
was run. No PR was created, edited or merged.

## Verification — the eight gates, real commands and real exit codes

### G1 TRANSPORT

    $ cmp .remedy-wt/f109-r18.md .agent/authored/f109-r18.md
    REAL_EXIT=0        (no output)

    $ sha256sum .agent/authored/f109-r18.md .agent/last_block.md
    e31bfdc9296f19b6ebe861ae61b66c11f5575d10a51031e40c1c3687614ecb83  .agent/authored/f109-r18.md
    e31bfdc9296f19b6ebe861ae61b66c11f5575d10a51031e40c1c3687614ecb83  .agent/last_block.md

ONE DIGEST TWICE. The left-hand file of the `cmp` is the REVIEWER'S OWN
original, so this is real transport and not self-consistency. Block size 23307
bytes.

### G2 THE PLAN

PLAN18 extracted by delimiter index (BEGIN/END lines excluded) from the
COMMITTED authored copy, 1995 bytes, written to `.agent/plan.md`.

    $ cmp <extracted PLAN18> .agent/plan.md
    REAL_EXIT=0        (no output)
    $ wc -l .agent/plan.md            ->  44        (< 50, AGENTS.md)
    $ grep -c '^## Goal' .agent/plan.md        ->  1
    $ grep -c '^## Next Steps' .agent/plan.md  ->  1

### G3 THE RECORD APPEND — four readings

**(a) ARITHMETIC.**

    base_size                 2119546
    base_sha256               f934a2a18754767ab3428c1db06b86d83ced20c058b2a70532685ca504e9222d
    appended length S         6324      ( = 2 bytes '\n\n' + 6322 bytes of RECORD18 )
    new_size                  2125870
    base + S == new_size      True
    new_sha256                4bd7f5df5ff80b225f3fe813255e96c463256f3bd2e87f526a4a067d9f1f3028
    ends WITHOUT trailing newline   True
    bytes[0:base_size] identical to base   True

The base sha256 was also read from the untouched file at `50526376` before any
commit of this round and is the same value, so the arithmetic starts from the
state the block names.

**(b) A SECOND READER THAT COUNTS NO BYTE.** The WHOLE file was split on
blank-line boundaries into 889 units. N was counted BY THE SCRIPT from the slice,
not taken from the block: `N_from_slice = 3`. The LAST 3 units equal RECORD18's
3 paragraphs IN ORDER:

    tracked_file_accepted = True
    unit[-3] opening60 = 'Gate: F109 R17 — the round 17 entry. VERDICT PASS, over th'
    unit[-2] opening60 = 'Done: R-0782 — RESOLVED at `cce5f9d7` and verified by the '
    unit[-1] opening60 = '- R-0783 — Low, A COMMENT IN THE SAME SUITE STILL GIVES TH'

**(c) A NEGATIVE CONTROL ON THE FIRST APPENDED PARAGRAPH.** The file was copied
to `.remedy-wt/live_review_negative_control_r18.md` and byte offset 2119558 —
inside the FIRST appended paragraph, 10 bytes into `Gate: F109 R17 …` — was
flipped from `' '` to `'!'`.

    control_copy_accepted        False    (reader (b) REJECTS it)
    tracked_file_accepted_again  True     (reader (b) still ACCEPTS the tracked file)
    tracked sha256 before        4bd7f5df5ff80b225f3fe813255e96c463256f3bd2e87f526a4a067d9f1f3028
    tracked sha256 after         4bd7f5df5ff80b225f3fe813255e96c463256f3bd2e87f526a4a067d9f1f3028
    tracked sha unmoved          True

The scratch file was deleted BY ITS EXACT PATH (never by glob), and

    os.path.exists('.remedy-wt/live_review_negative_control_r18.md')  ->  False

**(d) COUNTS, AS A SET DIFFERENCE.** Base read from
`git show 35c0b03f:.agent/live_review.md`, never by rewinding the tracked file.

    reading                                   BASE 35c0b03f    NEW
    registered id lines                              342       344
    DISTINCT registered ids                          342       344
    'Done:' lines                                     66        69
    DISTINCT resolved ids                             64        67
    |set(registered) - set(resolved)|  = OPEN        278       277

    newly registered over the range:  R-0782, R-0783
    newly resolved  over the range:   R-0780, R-0781, R-0782

`R-0721` and `R-0725` each carry two `Done:` lines (measured, not recalled), so
344 − 69 = 275 is the WRONG reading; 277 is the set difference. That is `R-0778`.

    $ grep -c '^Gate: F109 R17 — ' .agent/live_review.md  ->  1
    $ grep -c '^Done: R-0782 — '   .agent/live_review.md  ->  1
    $ grep -c '^- R-0783 — '       .agent/live_review.md  ->  1

### G4 PAIR F AND THE PROOF THAT NO CODE MOVED

    FROM count BEFORE C3   1
    TO   count BEFORE C3   0
    TO contains FROM       False       (so the rewrite proof is FROM 0x / TO 1x)
    FROM count AFTER  C3   0
    TO   count AFTER  C3   1
    file size 107569 -> 107737, delta 168 == len(TO) - len(FROM) = 601 - 433

AST profile parsed from `git show <sha>:<path>` BLOBS ONLY, before = `18f0c9c6`
(C2, the commit immediately preceding C3), after = `b89456a6` (C3):

    definition NAMES identical                       True
    names only in before / only in after             [] / []
    every definition's executable statement count, docstring EXCLUDED, identical
                                                     True   (no diffs at all)
    total executable statements                      816 -> 816
    qualified-name definition count                  155 -> 155
    DISTINCT flat definition names                   154 -> 154

    $ python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q --collect-only
      BEFORE C3:  130 tests collected   REAL_EXIT=0
      AFTER  C3:  130 tests collected   REAL_EXIT=0

Counting-convention note, not a divergence in substance: the reviewer's dry-run
reported "154 definition names". My walker's qualified-name convention counts
155 definitions; the DISTINCT flat-name convention counts 154 and reproduces the
reviewer's figure exactly. Both conventions read IDENTICAL before and after, so
the claim "the repair moved no code" holds under either.

### G5 THE BUILT STATE APPEND

    before_size    3268     before_sha256  01f06901ec601c578b5f511231b12204a8d390a724eaab0c3ec0498abcdde16c
    appended len   2802     ( = 1 byte '\n' + 2801 bytes of BUILTSTATE )
    after_size     6070     after_sha256   9a31f8382a54dae6e1882da71b22aa6b1c440963d07f931382a974412f717fea
    arithmetic closes (3268 + 2802 == 6070)                       True
    bytes BEFORE the appended region byte-identical to the whole pre-C4 file  True
    ends with EXACTLY ONE trailing newline                        True
    $ grep -c '^## Built State' docs/roadmap/features/T3_F109.md   ->  1
    $ git diff --stat  ->  47 insertions(+), 0 deletions(-)        (an append edits nothing)

The two append targets' opposite newline conventions were honoured separately:
`.agent/live_review.md` still ends WITHOUT a trailing newline (G3a), and
`docs/roadmap/features/T3_F109.md` ends WITH exactly one.

### G6 THE BUILT STATE IS TRUE — re-measured, not trusted

**(a) `supports_resume` returns literal False**, read by `ast` over
`packages/orchestration/pingpong_provider.py` (body with any docstring removed,
a single `Return` of the literal constant `False`):

    ClaudeProvider.supports_resume          line 443   returns_literal_False=True   'return False'
    ClaudeCliProvider.supports_resume       line 1084  returns_literal_False=True   'return False'
    OllamaPingPongProvider.supports_resume  line 1657  returns_literal_False=True   'return False'

**(b) every cited SHA exists**, `git cat-file -e <sha>^{commit}`:

    7451e9c7 exit 0 · 24352750 exit 0 · 60343048 exit 0
    b245e1c9 exit 0 · 78d2b7b5 exit 0 · d52a5371 exit 0

**(c) the marker string and the field resolve**, verified by RUNNING the shipped
code rather than by grep alone:

    from packages.orchestration.pingpong_loop import dedupe_marker_for_segment
    dedupe_marker_for_segment('repo_map')  ->  '[unchanged: repo_map, previously provided]'
    '[unchanged: ' in that result          ->  True

    dataclasses.fields(PromptTraceEntry)   ->  contains 'deduped_segment_names'   True
    'unmeasured_segment_names' is a field of DedupeSavingsMeasurement in
    packages/orchestration/prompt_trace.py, the return type of
    measure_dedupe_savings_from_traces (which resolves and is callable)
    fields = chars_avoided, chars_spent_on_markers, net_chars_saved,
             deduped_occurrences_counted, unmeasured_segment_names

TEXTUAL SUB-READING, DECLARED (see Deviations): the LITERAL `[unchanged: ` occurs
0 times in `packages/orchestration/pingpong_loop.py` and 1 time in
`packages/orchestration/session_sent_index.py:295`. `_dedupe_resumed_segments`
does live in `pingpong_loop.py` (line 882) and does replace the segment text with
that marker (line 939, `dedupe_marker_for_segment(segment.name)`, imported at
line 75), so the Built State's SENTENCE is true; only the string LITERAL sits in
the other module the slice already names. The slice was applied unchanged.

**(d) the doc exists and does not disagree.**
`docs/system/semantic-dedupe-v1.md` exists; its savings table reads:

    | Segments withheld           | 2 (`builder_system`, `reviewer_system`) | 0 |
    | Characters avoided          | 556 | 0 |
    | Characters spent on markers |  97 | 0 |
    | Net characters saved        | 459 | 0 |

All four figures — 556, 97, 459 and 2 — match the Built State's
"556 characters avoided against 97 spent on markers, 459 net over 2 withheld
segments". No contradiction between slice and doc.

### G7 THE SUITES — run SERIALLY, one process finished before the next started

    $ python3 -m pytest tests/docs/ -q
      295 passed in 0.53s                     REAL_EXIT=0
    $ python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q
      130 passed in 1.04s                     REAL_EXIT=0
    $ python3 -m pytest tests/orchestration/test_prompt_trace.py -q
      54 passed in 0.37s                      REAL_EXIT=0
    $ python3 -m pytest tests/cli/test_golden_path.py -q
      42 passed in 22.66s                     REAL_EXIT=0

NO COUNT MOVED IN EITHER DIRECTION: 295 / 130 / 54 / 42 are exactly the four
figures the reviewer measured at `50526376`, and no count rose either. Zero
failures, zero errors, four exit codes of 0. `tests/docs/` ran FIRST and was
mandatory because this round's change set includes `docs/roadmap/**`
(planner_reviewer_prompt.md §3, verification tier 5). `tests/cli/test_golden_path.py`
is the mandatory canary.

### G8 THE TREE AND THE SWEEP

    $ git status --porcelain          ->  0 bytes, EMPTY = True
    $ git ls-files .remedy-wt         ->  0 bytes, EMPTY = True

Insertion counts from `git show --numstat`, the `+` column ONLY (AGENTS.md
DECISION F104 D1), for every commit of this round EXCEPT C5, compared CELL BY
CELL against the `## Commits` table above:

    a5fb260b  .agent/authored/f109-r18.md                    316   table says +316   MATCH
    9284e364  .agent/last_block.md                           200   table says +200   MATCH
    ce1b9227  .agent/plan.md                                  15   table says  +15   MATCH
    18f0c9c6  .agent/live_review.md                            7   table says   +7   MATCH
    b89456a6  tests/orchestration/test_semantic_dedupe.py      4   table says   +4   MATCH
    b2814f5d  docs/roadmap/features/T3_F109.md                47   table says  +47   MATCH

Every commit is far under the 500-insertion cap; C0b is additionally the verbatim
rewrite of a single `.agent/**` state file, which AGENTS.md exempts outright.

THE STALENESS SWEEP over every file this round touched:

    $ grep -rn "report never reaches|no consumer|has no production consumer" \
        tests/orchestration/test_semantic_dedupe.py \
        docs/roadmap/features/T3_F109.md .agent/plan.md \
        docs/system/semantic-dedupe-v1.md
      REAL_EXIT=1   (zero hits)

`R-0783`'s stated resolution condition — "no comment or docstring in that file
gives 'the report never reaches `PingPongResult`' as a reason for anything" — is
therefore MET ON DISK. `R-0782`'s condition, the string `no consumer for the
report` at ZERO in that file, is still met.

Sentences found stale, including those NOT repaired: NONE in the change set. Two
observations that are NOT staleness and were NOT repaired are recorded under
Deviations below.

## Authored-text proofs

| Authored text | Proof | Result |
|---------------|-------|--------|
| the round 18 block | `cmp .remedy-wt/f109-r18.md .agent/authored/f109-r18.md` | exit 0 — the left file is the REVIEWER'S OWN original |
| the block, mirrored | `sha256sum` of authored copy and `.agent/last_block.md` | one digest twice: `e31bfdc9…4ecb83` |
| SLICE PLAN18 | delimiter-index extraction `cmp`'d against `.agent/plan.md` | exit 0, no output |
| SLICE RECORD18 | G3 (a) arithmetic, (b) whole-region paragraph reader, (c) negative control, (d) counts | all four pass |
| PAIR F FROM/TO | occurrence counts + AST profile over the two git blobs | FROM 1→0, TO 0→1, profile identical |
| SLICE BUILTSTATE | G5 append arithmetic + prefix identity + heading count + newline count | all pass |
| SLICE FORTSCHRITT | extracted by delimiter index and pasted as the `Fortschritt` row of the State block | applied verbatim |

Every slice was extracted BY DELIMITER INDEX from the COMMITTED authored copy and
written with `shutil.copyfile` or a byte-level `replace`. No slice was retyped.
`BEGIN`/`END` marker lines never reached any file.

## Deviations & assumptions

**No deviation from the block's ordered commit sequence.** C0a, C0b, C1, C2, C3,
C4, C5 ran in that order, one commit each, none extra, none dropped, none
reordered.

**No slice was altered.** Every slice was applied byte for byte. Where a gate
reading did not sit flush against the block's wording, the slice was applied
UNCHANGED and the reading is declared here, per constraint 1.

1. **DECLARED, not repaired — the `[unchanged: ` literal lives in a different
   module than a literal reading of G6(c) expects.** G6(c) asks that the marker
   string "resolve in the modules named". It occurs 0 times in
   `packages/orchestration/pingpong_loop.py` and 1 time in
   `packages/orchestration/session_sent_index.py:295`. The Built State's sentence
   is nevertheless TRUE: `_dedupe_resumed_segments` is at `pingpong_loop.py:882`,
   it writes the marker at line 939 via `dedupe_marker_for_segment`, imported at
   line 75, and running that function through `pingpong_loop` returns
   `[unchanged: repo_map, previously provided]`. The slice names BOTH modules, so
   nothing on disk is wrong; only a grep-only reading of the gate would fail.
   Reported so the reviewer sees the reading rather than a bare "green".

2. **DECLARED, not repaired — `unmeasured_segment_names` is not a
   `PromptTraceEntry` field.** It is a field of `DedupeSavingsMeasurement`, the
   return type of `measure_dedupe_savings_from_traces`, in the same module
   `prompt_trace.py`. The Built State's "Its `unmeasured_segment_names` field"
   takes the MEASUREMENT function as its antecedent, not the entry, so the slice
   reads correctly; a reader who binds "Its" to `PromptTraceEntry` would be
   misled. Not repaired, because only reviewer-authored text may change a slice.

3. **OBSERVATION outside the change set, declared and NOT repaired (constraint
   6).** `docs/roadmap/features/T3_F109.md` "Edge cases" proposes a
   "minimum-size threshold (config)". It IS built —
   `should_dedupe_segment(..., min_chars=DEDUPE_MIN_SEGMENT_CHARS)` at
   `packages/orchestration/session_sent_index.py:304-331` — but the BUILTSTATE
   slice does not mention it. That is an omission from the slice, not a false
   statement in it, and the slice is the reviewer's to widen.

4. **OBSERVATION on the stale-prose class enumeration, declared only.** RECORD18
   calls `R-0783` "the sixth site of one class … after `R-0749`, `R-0773`,
   `R-0779`, `R-0780` and `R-0781`", and `.agent/plan.md` agrees at six. `R-0782`
   — a docstring that said the dedupe report has no production consumer — reads
   to me as the same class but is excluded from that enumeration. The block's two
   texts are consistent WITH EACH OTHER, so nothing was corrected; the closure
   consolidation may want to settle whether the class has six members or seven.

5. **Method, not scope: no worktree was created.** G5 of the protocol isolates
   DESTRUCTIVE verification. Nothing this round ordered was destructive — the
   only mutation was the G3(c) negative control, which was performed on a COPY
   under the gitignored `.remedy-wt/` and never on a tracked file, with the
   tracked sha256 shown unmoved before and after. The primary checkout satisfies
   `git status --porcelain` == EMPTY.

6. **Sandbox routes used, as the block's constraint 8 anticipated.** `cp` and
   env-var assignment were not used at all; copying went through
   `python3 -c "import shutil; shutil.copyfile(a, b)"`, and every multi-step
   proof was written to a scratch `.py` under `.remedy-wt/`, run with
   `python3 -B`, and deleted BY EXACT PATH. Real exit codes were obtained with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` because the tool does not surface them.
   Thirteen scratch paths were created and all thirteen were deleted individually;
   `git ls-files .remedy-wt` returns nothing and the tree is clean.

7. **Constraint 7 honoured.** This handback commit's own insertion count is not
   quoted anywhere; it cannot exist while the text stating it is being written
   (§3 checklist item 14). Its row in the `## Commits` table says so explicitly.

**No `Done:` paragraph and no `Landed:` line was written for `R-0783`**, per the
order. Only reviewer-authored text sets a resolution.

## Open findings

Recomputed as a SET DIFFERENCE, never a subtraction (`R-0778`), after C2:

    registered id lines             344
    DISTINCT registered ids         344
    'Done:' lines                    69
    DISTINCT resolved ids            67
    OPEN = |registered - resolved|  277

`R-0721` and `R-0725` each carry two `Done:` lines — measured this round, not
recalled — which is why 344 − 69 = 275 would be the wrong reading.

**PENDING RESOLUTION.** `R-0783` is REPAIRED ON DISK at `b89456a6` and its stated
resolution condition is MET (the sweep in G8 returns zero hits), but it is NOT
RESOLVED: it still counts among the 277 open. Only reviewer-authored text sets
`Done:`, so its resolution line is the reviewer's to write in the first commit of
the next round. `R-0782` was booked resolved this round in C2 and is no longer
pending.

## Next

The single expected next action: the reviewer re-runs these eight gates over
`50526376..HEAD`, issues the round 18 verdict and books `R-0783`'s resolution.
Then the closure sequence's remaining precondition that is not yet met — the
SELF-USE ITEM of closure precondition 6: the queue holds no pending item, so
`generate_and_append_if_empty` supplies one from the ledger, and that item is
planned, RUN to the normal approval gate, and its defects registered before the
close. Only after that do the closure sequence proper's steps run — the evidence
job, a FRESH review zip, the authored STATUS line with the `docs/README.md` sync
in the SAME commit, and the PR. Phase 1 rule 1 first — re-read `.agent/STOP` from
disk before anything else.
