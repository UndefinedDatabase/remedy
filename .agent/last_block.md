# STEP T003 — F275 ROUND 80 — the repair: classify by the EXCEPTION, not by the message

## Goal

Round 79 was FAILED. Its instrument selected a record when the record's MESSAGE matched the
`'X' object has no attribute 'Y'` pattern, without requiring the record's exception CLASS to be
`AttributeError`, so six `AssertionError` nodes whose assertion message quotes such an error
were counted as frames of the class `R-0880` names. Re-classify by the exception, re-derive the
attribution over the records that survive, and land the corrected reading as a NEW artefact
beside the landed one. Correct DECISION F275 D53 by APPENDING D54, never by rewriting it. Book
the round 79 FAIL verdict and its prose slips. NO PRODUCTION LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r80.md`
- C0b mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 80 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 79 reviewer verdict — `.agent/live_review.md`
- C3 append the round 79 prose slips — `.agent/prose_slips.md`
- C4 land the corrected attribution artefact — `.agent/f275_t003_frame_attribution_r80.md`
- C5 record DECISION F275 D54 — `.agent/decisions.md`
- C6 the round 80 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r80.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/f275_t003_frame_attribution_r80.md
    .agent/decisions.md
    .agent/handoff.md

`.agent/f275_t003_frame_attribution_r79.md` IS NOT EDITED, NOT DELETED AND NOT STAGED. A landed
artefact is not rewritten when its reading is corrected — the correction is a new document
beside it, and item 20 of `docs/agents/planner_reviewer_prompt.md` §3 is the rule. The same
holds for DECISION F275 D53 inside `.agent/decisions.md`: C5 APPENDS D54 and the deletion column
of that commit is ZERO.

NOTHING under `packages/`, `apps/`, `tests/` or `docs/` is touched. No suite is run, no tree is
built, and no transform is executed: every input this round needs is already on disk.

## What the reviewer measured, and why this round exists

THE DEFECT IS ONE MISSING CONDITION IN A PREDICATE. Round 79's instrument builds its working set
with a search over each record's message alone. A pytest record whose exception is an
`AssertionError` carries the assertion's full text as its message, and six such records in this
capture quote an `AttributeError` on `_FakeJob.job_id` inside that text. They were therefore
admitted to a set defined as "AttributeError records naming a unified attribute", and the label
is wider than the thing it names.

Re-derived by the reviewer at `c7ac5e00`, over `.remedy-wt/r79_frames.jsonl` and without using
the instrument:

    records in the capture                                   1238
    selected by the message rule, as round 79 selected them     30
      whose exception class really is AttributeError            24
        on a NAMED receiver class                               19
        on NoneType                                              5
      whose exception class is AssertionError                    6

THE CORRECTED NAMED-CLASS COUNT IS NINETEEN, WHICH IS EXACTLY WHAT ROUND 77 RECORDED. So the
round 79 artefact's explanation of its own larger number — that the earlier `--tb=line`
transcript could not show six further nodes, and that the difference was the instrument rather
than the population — is FALSE IN BOTH HALVES. The population never grew; the predicate widened.
Round 77's reading needed no explaining away.

WHAT SURVIVES THE CORRECTION, AND IT IS THE HALF THE ROUND EXISTED FOR. All six mis-selected
records sit in `tests/orchestration/test_orchestrator_loop.py`, all six fall in the "lands
nowhere in the corrected set" bucket, and none of them touches the seventeen frames that land ON
a held site. The three sites those seventeen name — and they are the actionable result — are
unaffected by this repair. This round re-derives the split rather than assuming that, and the
block states no numeral for the corrected split: G4 orders it MEASURED.

## Constraints

1. EVERY SLICE IS APPLIED BYTE FOR BYTE. A slice is never edited, reflowed, re-wrapped or
   corrected, not even where it is wrong. A discrepancy is DECLARED in the handback with the
   measurement that shows it, and the slice still lands as written.
2. THE CORRECTED INSTRUMENT IS ROUND 79's WITH ONE CONDITION ADDED, and the handback states the
   diff between the two as a unified diff of the selection predicate alone. Do not rewrite the
   instrument, do not retune anything else in it, and do not change what it prints beyond what
   the added condition and the new sections below require. It lives under `.remedy-wt/` and is
   never committed, per round 79's constraint 3, which stands unchanged here.
3. THE INPUTS ARE PINNED AND NONE IS REGENERATED. Check each against the digest below before
   running anything; if any is missing or differs, STOP and hand back rather than rebuilding it.

    .remedy-wt/r79_frames.jsonl    3638751 bytes  sha256 16d876503e3c790cde16943d802116d305b15921268ed05ab43812ce1842bc43
    .remedy-wt/r79_instrument.py     18750 bytes  sha256 7e8680165949197d61d93532a0e8136a320229a856f2aa8e64c48563b3ad871a
    .remedy-wt/r77_corrected.json   120753 bytes  sha256 765b5ba99f2c92765349c3a013f4074c62ece893cb50b373450927af0290a512
    .remedy-wt/r79_inst.out          18685 bytes  sha256 750b1f6008417721df1d6a4515551695ba53acf77c1693b21011a1f5d35f1f29

4. THE ARTEFACT AT C4 IS WRITTEN BY YOU, FROM YOUR OWN RUN, and this block states none of its
   figures. Its required sections are below and G5 gates its quoted lines against the corrected
   instrument's own output.
5. THE BUILT TREE `.remedy-wt/r79_tree` IS READ, NEVER REBUILT AND NEVER DELETED. The source
   lines the artefact quotes come from `ef75e213` as before, not from that tree.
6. C1 IS THE FIRST SUBSTANTIVE COMMIT, per item 23 of §3.
7. NO COMMIT EXCEEDS 500 INSERTIONS, measured per commit with `git show --numstat`.
8. NO `gh` COMMAND AND NO `remedy` CLI COMMAND IS RUN. No pull request is created, edited or
   merged. No branch is created or deleted. No merge. No force-push. No history rewrite.
9. READ `.agent/STOP` BEFORE C0a AND AGAIN BEFORE C6. It does not exist at this round's base.
   If it appears, finish the commit in hand, write the handback recording both readings with
   their timestamps, push, and stop — do not stage it, do not delete it.
10. THE BLOCK'S OWN SIZE: this block is 353 lines TOTAL and 275 of them are PROSE, against the
    caps DECISION F085 D6 and D5 set at 490 and 400. Report both numbers as measured.
11. GATES RUN AT C5, STRICTLY BEFORE C6, so the handback can quote every one of them. Each gate
    writes its transcript to a file under `.remedy-wt/` and the handback reports the REAL exit
    code read back out of that file, one line per gate.

## The corrected rule, stated exactly

A record enters the working set when BOTH hold: its exception CLASS is `AttributeError`, and its
message names an attribute in `job_id`, `job_title`, `task_id` or `title`. Everything downstream
— the deepest in-tree frame, the reduction to a tree-relative path and line, the lookup into
`.remedy-wt/r77_corrected.json`, the pre-flip source line read from `ef75e213`, and the grouping
— is round 79's, unchanged.

THE CORRECTED INSTRUMENT ALSO REPORTS THE SET IT NOW EXCLUDES, because a repair that silently
drops records is indistinguishable from a repair that loses them: report the count of records
the message rule admits and the class rule rejects, and for each one its exception class, its
node id and the receiver-and-attribute its message names.

AND IT REPORTS THE TWO SPLITS SIDE BY SIDE — the attribution split as round 79 published it and
the split over the corrected set — so a reader of both artefacts can see which rows moved and
which did not, without re-running anything.

## The artefact's required sections

`.agent/f275_t003_frame_attribution_r80.md` carries, in this order and under headings of your
own wording: what round 79 published and what was wrong with it, naming the artefact and the
DECISION by path and id; the inputs with their digests; the corrected selection with the
excluded set enumerated; the corrected attribution table in round 79's own row format; the two
splits side by side with the rows that moved named; and a closing section on what the corrected
reading does NOT settle, which states in its own words that `R-0880` remains open.

Every FIGURE in it is a figure the corrected instrument printed. QUOTE NO WALL-CLOCK DURATION.
The artefact does not restate round 79's table as if it were current, and wherever it gives a
round 79 number it says so in the same sentence.

## Done when — the gates

### G1 — transport, the block budget, the insertion cap

(a) `.agent/authored/f275-r80.md` at C0a is byte-identical to the reviewer's scratch original at
`.remedy-wt/r80_block.md`, by `cmp`. This is the PRIMARY proof and not the §4.9 digest fallback.
(b) `.agent/last_block.md` at C0b is byte-identical to the COMMITTED C0a blob.
(c) Extract every BEGIN/END slice from the committed C0a blob, report the CARDINALITY YOU
MEASURED — this block states no numeral for it — and for each slice its byte size, its line
count, and whether its content matches the sha256 on its own BEGIN marker, computed over the
bytes strictly between the BEGIN line and the END line with the trailing newline kept.
(d) Re-measure TOTAL and PROSE as constraint 10 defines them and report both.
(e) Report the number of block lines outside a slice that are a run of a single repeated
character. The expected number is zero, per item 37 of §3.

### G2 — the plan

`.agent/plan.md` at C1 is byte-identical to slice PLAN80; it is at most 50 lines; it carries
exactly one `## Goal` and exactly one `## Next Steps`.

### G3 — the record, with full forensics

For each of the record appends — RECORD80 at C2 and DEC80 at C5, the appends into the two files
amend0827 rule 5 reserves full byte forensics for:
(i) READER A, bytes: the pre-commit blob is a byte-exact PREFIX of the post-commit file, and the
slice is a byte-exact SUFFIX of it.
(ii) READER B, structure: the LAST N blank-line-separated units of the post-commit file equal
the slice's N paragraphs IN ORDER, where N is COUNTED by your script from the slice and is never
a number this block asserts.
(iii) NEGATIVE CONTROL: flip one byte inside the FIRST appended paragraph, in the ASCII letter
range `A`-`Z` or `a`-`z` so the flip cannot land inside a multi-byte sequence, and require BOTH
readers to REJECT.
(iv) The DELETION column of both commits is ZERO, so neither DECISION F275 D53 nor any landed
ledger paragraph is rewritten.
(v) `.agent/prose_slips.md` at C3 is the pre-commit blob followed by exactly slice SLIPS80 and
nothing else, a byte-equality check with no arithmetic; its deletion column is ZERO.
(vi) RECORD80's `Gate:` header is compared as a pattern DERIVED from the headers already in
`.agent/live_review.md`; report how many prior headers the derived pattern matches, and require
that RECORD80's header matches it and duplicates none of them byte for byte.

### G4 — the corrected reading

(a) Every input of constraint 3 matches its stated digest. Report each comparison.
(b) The selection predicate's change is reported as a unified diff against
`.remedy-wt/r79_instrument.py`, and the diff touches the selection only. Report the number of
changed hunks and the lines added and removed.
(c) Over the pinned records, report: the count the MESSAGE rule admits, the count the CLASS rule
admits, and the count it rejects; and the corrected named-class and NoneType counts. These are
MEASURED and this block states no numeral for any of them.
(d) PARTITION: the message-rule count equals the class-rule count plus the rejected count, and
the corrected count equals the named-class count plus the NoneType count. Both must hold.
(e) CROSS-CHECK against a number nothing in this round produced: the corrected NAMED-CLASS count
is compared against the figure `.agent/f275_t003_flip_residue_r77.md` records for that class,
and the comparison is reported as MATCH or as a difference with its size. A cross-check between
two independently derived numbers can fail; a partition cannot, and both are labelled.
(f) The corrected attribution split — frames landing on a ruled site the corrected set holds
against frames landing nowhere in it — is reported beside round 79's published split, with the
rows that moved named individually.

### G5 — the artefact

(a) `.agent/f275_t003_frame_attribution_r80.md` at C4 is byte-identical to the file your run
produced, and it did not exist at this round's base — report the base lookup's exit code.
(b) Every INDENTED non-blank line of the artefact appears verbatim in the corrected instrument's
saved output, the matching is MONOTONE with indices strictly increasing, and the count of
unmatchable lines is ZERO. Report the number of indented lines you compared and the rule you
used to decide a line is indented.
(c) The count of artefact lines carrying a wall-clock duration is ZERO, and so is the count of
three-backtick lines.
(d) The artefact carries every section the block's artefact list names. Report the headings you
found, in order.
(e) `.agent/f275_t003_frame_attribution_r79.md` is byte-identical at this round's base and at
C5, and it is absent from the round's changed-path set.

### G6 — the tree, the colours and the path set

(a) `git status --porcelain` is the EMPTY STRING at C5.
(b) `git worktree list` shows the primary checkout alone, and `.remedy-wt/r79_tree` still exists
on disk per constraint 5. Report both.
(c) THE CANARY: `python3 -B -m pytest tests/cli/test_golden_path.py -q` in the PRIMARY checkout
at C5. The reviewer measured 42 passed at this round's base.
(d) `ruff check .` at C5 reports 26 rows against the frozen ceiling of 26; and a filesystem
sweep reports ZERO `.py` files anywhere under `.agent/`. The reviewer measured both at the base.

### G7 — the path set and the open set

(a) The changed-path set of the range from this round's base to C6 equals the path set the
Change section names, with MISSING and EXTRA both empty, and the count of changed paths under
`packages/`, `apps/`, `tests/` or `docs/` is ZERO. This reading is taken AFTER C6, unlike every
other gate, because its subject includes a path C6 alone creates.
(b) The open set BY DISTINCT ID is reported at this round's base and at C5 with the membership
difference, which must be empty; `R-0880` is OPEN at both. Report ALSO the canonical line-count
reading of `scripts/rotate_live_review.py` at both, and the gap between the two readings, which
is a pre-existing property of two ids carrying two resolution lines each and must not grow.

### G8 — the per-commit insertion counts

`git show --numstat` for each of C0a through C5, reported one line per commit, each under 500.
The handback commit C6 is NOT covered: its own numbers cannot exist while its text is written
(item 14), and the reviewer measures them at the next gate (item 31).

## Handback

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the state block with the
SESSION NUMBER, which is 28, and the round, which is 80; the range; the per-commit table whose
`+/-` cells are compared CELL BY CELL against G8's numbers with the comparison printed; external
actions; one line per gate with the REAL exit code read back out of its transcript file; the
item-status table; deviations; next steps. No scope report and no session-limit banner is owed.
State the operator-questions count in `## Next` as rule C requires.

## SLICE PLAN80 — replaces `.agent/plan.md` at C1

BEGIN PLAN80 sha256=3e6374ad588ebe885c4f758aea18e4a494ac9adfa15621574ae1cd1a82888e97
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 80 REPAIRS ROUND 79, WHICH WAS FAILED. That round's instrument selected a record by
searching its MESSAGE for an attribute-error pattern without requiring the record's exception
CLASS to be `AttributeError`, so six `AssertionError` nodes whose assertion text quotes such an
error entered a set defined as the class `R-0880` names. Corrected, the named-class count is
nineteen, which is exactly what round 77 recorded, so that round's reading needed no explaining
away and round 79's explanation of its own larger number is false in both halves. The repair
re-classifies, re-derives the attribution over what survives, and lands the corrected reading as
a NEW artefact beside the landed one, correcting DECISION F275 D53 by appending D54 rather than
by rewriting it. The round 79 verdict and its prose slips are booked.

## Next Steps

1. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as the
   home of the id-SHAPE seam behind the three largest residue classes. Production code, so a
   SPLIT round with mutation red-proofs.
2. THE FLIP, on the corrected set DECISION F275 D51 rules, less whatever sites the corrected
   attribution shows the surviving frames land on, carrying DECISION F275 D48's obligations: the
   full suite is the backstop, and the thin set is re-derived before the flip with any site
   fallen to zero witnesses treated as a stop.
3. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20 sessions
  and 60 rounds without a replacement, so this feature closes only at full scope and owes no
  scope report. Round 78 restored that paragraph to the protocol after a merge dropped it.
- A LANDED ARTEFACT AND A LANDED DECISION CARRY THE WRONG READING and stay on disk carrying it.
  The correction is an append beside them, never a rewrite, so a reader who finds the round 79
  artefact first must follow it forward to the round 80 one.
- THE CORRECTED SET IS BETTER, NOT RIGHT, and 1204 bad nodes is the best reading this chain has
  taken and is not near green.
- The open set is 87 by distinct id at this round's base, with `R-0880` open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN80

## SLICE RECORD80 — appended to `.agent/live_review.md` at C2

BEGIN RECORD80 sha256=3fbcd97a7e2341684a0b0fef35f7cec50ca9f6ae6ace09c7500ce4db96b0723b

Gate: F275 R79 — the F275 round 79 entry. VERDICT FAIL. Written by the planner and reviewer of session 28 after reading the committed range `d3610730`..`c7ac5e00` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs and against the capture's own records; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 80, per operator amendment amend0827-process-diet rule 1. THE ROUND EXECUTED FAITHFULLY AND ITS READING IS STILL WRONG, which is the distinction this entry exists to keep: every commit landed in the Bundle's order, every gate ran, the transform control reproduced round 77's output byte for byte from the PRECONDITION line to the last rule row, and the one line by which the two transcripts differ is the gate wrapper's own exit marker.

THE DEFECT IS ONE MISSING CONDITION IN A SELECTION PREDICATE. The instrument admits a record when a regular expression matches the record's MESSAGE, and never asks whether the record's exception CLASS is `AttributeError`. A pytest record for a failing assertion carries the assertion's full text as its message, and six records in the capture quote an `AttributeError` on `_FakeJob.job_id` inside that text. Re-derived by the reviewer at `c7ac5e00` over `.remedy-wt/r79_frames.jsonl`, whose sha256 is `16d876503e3c790cde16943d802116d305b15921268ed05ab43812ce1842bc43`, and without using the instrument: of 1238 records the message rule admits 30, of which 24 carry the class `AttributeError` — 19 on a named receiver class and 5 on `NoneType` — and 6 carry `AssertionError`.

WHAT MAKES IT A FAIL RATHER THAN A SLIP IS THE SENTENCE IT PRODUCED. The round's artefact and DECISION F275 D53 both state that the named-class population is 25 and explain the gap against round 77's 19 as a limitation of the earlier `--tb=line` transcript — "the difference is what the earlier transcript could show and not a different population of failures". The corrected count IS 19, exactly round 77's, so the population never grew and the explanation is false in both halves. That is a load-bearing factual claim landed in the append-only record, which is the one condition AGENTS.md allows a correction round for, and it would have been consumed by the next round as the denominator of the reading `R-0880` turns on.

WHAT SURVIVES, STATED BECAUSE A FAIL IS NOT A DISMISSAL. The actionable half of the round is untouched: seventeen frames land on a ruled site the corrected set holds, and they concentrate in three sites — `tests/cli/test_repair_runtime.py:68`, whose pre-flip source is `return str(job.id), str(art.id), str(data_dir)` and whose ruled columns are 19 and 32, `packages/orchestration/brain_detail.py:345` at columns 45 and 54, and `packages/orchestration/project_registry.py:856` at column 19. All six mis-selected records fall in the other bucket, so none of the seventeen moves. The capture itself is sound and is not re-taken: the round 80 repair re-analyses the same pinned records.

NO ID IS MINTED. Nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong and no gate over production code is blind or unmeetable, so operator amendment amend0827-process-diet rule 2 puts this in `.agent/prose_slips.md` rather than in an id, and the correction lands as DECISION F275 D54 appended beside D53 and as a new artefact beside the landed one. THE REVIEWER OWNS PART OF THIS: the block's attribution rule said "for every `AttributeError` in the fresh transcript whose message names an attribute in" the four names, and it never stated that the record's class must be that exception, so the predicate the worker wrote is a defensible reading of the sentence the reviewer authored. LAST_REVIEWED_SHA DOES NOT ADVANCE.
END RECORD80

## SLICE SLIPS80 — appended to `.agent/prose_slips.md` at C3

BEGIN SLIPS80 sha256=0c0ce3edb31e1291329b3b4da6204feae2fff14a7f2da5d9c90b8ca7084d34a8

2026-09-12 · F275 R79 · The round 79 block's attribution rule read "for every `AttributeError` in the fresh transcript whose message names an attribute in `job_id`, `job_title`, `task_id` or `title`", and the instrument implemented the subordinate clause alone: it matched the message and never tested the exception class, so six `AssertionError` records whose assertion text quotes an attribute error entered the set. THE RULE THAT FOLLOWS: when a block names a set by a TYPE and then qualifies it by a STRING the type's instances carry, the qualifier is the half that gets implemented, because it is the half that looks like a predicate — so state the type as its own condition in its own clause, and where the data carries the type in a field, name that field.

2026-09-12 · F275 R79 · The round 79 artefact explained a count that disagreed with a previous round's by reasoning about the instrument that produced the EARLIER number, and never re-derived the earlier number with the later instrument. Had it done so it would have found the two agree at 19 and that its own 25 was the outlier. THE RULE THAT FOLLOWS: when a fresh measurement disagrees with a landed one, the first move is to reproduce the LANDED number under the NEW method, because a difference explained by a story about the old instrument is the one shape that never has to confront the new one — and where the old number reproduces, the new method is what changed.
END SLIPS80

## SLICE DEC80 — appended to `.agent/decisions.md` at C5

BEGIN DEC80 sha256=6f6537257b6817122fcfeec51eba3b3d88ce78256cadad0c36623796e0a255e3

## DECISION F275 D54 (2026-09-12, F275 round 80) — D53's selection is corrected to require the exception CLASS, the named-class count is nineteen, and D53's explanation of its own larger number is withdrawn

CONTEXT. DECISION F275 D53 ruled that the surviving over-selection frames are attributed by the deepest in-tree frame of a fresh full-traceback run, and round 79 executed it. The instrument it used selects a record by searching the record's MESSAGE for `'X' object has no attribute 'Y'` and never tests the record's exception CLASS, so records whose exception is an `AssertionError` quoting such an error were admitted. This decision corrects that selection. D53 is NOT rewritten: its paragraph block stands where it landed, and this one is read beside it.

THE MEASUREMENT, taken by the reviewer at `c7ac5e00` over `.remedy-wt/r79_frames.jsonl` without using the instrument. Of 1238 captured records the message rule admits 30. Twenty-four of those carry the exception class `AttributeError` — 19 on a named receiver class, 5 on `NoneType` — and six carry `AssertionError`, every one of them a node of `tests/orchestration/test_orchestrator_loop.py` asserting over a local `_FakeJob` double.

CHOSEN, FIRST: A RECORD ENTERS THE SET ONLY WHEN ITS EXCEPTION CLASS IS `AttributeError` AND its message names one of the four unified attributes. Everything downstream of the selection — the deepest in-tree frame, the tree-relative reduction, the lookup into the corrected site set, the pre-flip source line, the grouping — is D53's and is unchanged. ALTERNATIVE: keep the message rule and subtract the six by name, rejected because a set defined by a predicate that admits the wrong members and is then patched by a list is not a set anyone can re-derive, and the next capture would admit a different six.

CHOSEN, SECOND: D53's EXPLANATION OF THE 25 IS WITHDRAWN. That decision and its artefact state that the named-class population is 25 and that round 77's 19 was what a `--tb=line` transcript could show rather than a different population. The corrected count is 19 — the same number, by a different instrument, over a different capture — so round 77's reading required no explanation, and the sentence explaining it is false in both halves. The withdrawal is recorded here and the landed text stays, because appending a correction is how this record stays honest and overwriting landed text is worse than a dated wrong sentence.

CHOSEN, THIRD: THE ACTIONABLE HALF STANDS AND IS RE-DERIVED RATHER THAN ASSUMED. All six mis-selected records fall in the "lands nowhere in the corrected set" bucket, so the frames that land ON a held site do not move; but round 80 re-derives the split from the corrected set rather than reasoning to it, and reports the two splits side by side with the rows that moved named. ALTERNATIVE: declare the actionable half unaffected and re-run nothing, rejected under the rule this very defect illustrates — a reading reasoned to is not a reading measured.

CONSEQUENCE. `R-0880` stays OPEN and its second obligation now has a corrected attribution behind it. The flip's input set is still DECISION F275 D51's and nothing here changes it; the sites the corrected attribution names are candidates for a later round to drop, and that decision is not taken here. No production line moved, no suite was re-run, the capture is not re-taken, and the built tree and the records stay on disk pinned by digest.

HOW TO REVERSE. Delete this paragraph block and the round 80 artefact. DECISION F275 D53 then stands alone with its selection as landed and its count of 25, and a reader comparing it with `.agent/f275_t003_flip_residue_r77.md` finds the disagreement with round 77's 19 unexplained rather than resolved.
END DEC80
