# STEP T003 — F275 ROUND 79 — carry the surviving over-selection frames back to the ruled sites

## Goal

Discharge the second obligation `R-0880` still names. Round 77 partitioned the 60 dropped sites
by the owner check's verdict, which is a property of the SET, and left the surviving
over-selection frames unattributed to the sites that produce them, which is a property of the
RUN. Rebuild the corrected arm's tree under a reproduction control, re-run the selection that
carries those frames with FULL tracebacks, and carry each frame back to the ruled site at its
deepest in-tree location. Book the round 78 PASS verdict and its two prose slips. NO PRODUCTION
LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r79.md`
- C0b mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 79 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 78 reviewer verdict — `.agent/live_review.md`
- C3 append the round 78 prose slips — `.agent/prose_slips.md`
- C4 land the attribution artefact — `.agent/f275_t003_frame_attribution_r79.md`
- C5 record DECISION F275 D53 — `.agent/decisions.md`
- C6 the round 79 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r79.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/f275_t003_frame_attribution_r79.md
    .agent/decisions.md
    .agent/handoff.md

NOTHING under `packages/`, `apps/`, `tests/` or `docs/` is touched. Every tree this round builds
and every transcript it takes lives under `.remedy-wt/`, which is gitignored, so the primary
checkout satisfies `git status --porcelain` == empty at every commit.

## What the reviewer measured before authoring this, and why the cheap route is not ordered

THE SAVED TRANSCRIPT CANNOT ANSWER THE QUESTION. Round 77's artefact says the probe that would
carry the frames back "was written and works", and the reviewer tested that claim against the
bytes on disk at `.remedy-wt/r77_suite_corr.out` before writing this block. Three readings, all
taken at `e262f420`:

- The transcript holds 24 location frames whose message is an `AttributeError` naming a unified
  attribute. Nineteen of them are on a NAMED class and five are on `NoneType`, which is the
  difference between the artefact's 19 and the raw 24, and it is the instrument's class filter
  rather than a discrepancy.
- Those 19 resolve to only FIVE distinct locations, and the location carrying TWELVE of them is
  `pydantic/main.py:1042` — a library frame, outside this repository entirely. The summary line
  names the frame the error was RAISED in, not the repository site that reached it.
- Of the five locations, two resolve directly to a ruled site in the corrected set and three do
  not. The short summary is additionally TRUNCATED — its lines end in `- Attribu...` — so the
  failing node ids cannot be selected by error class out of it either.

So the attribution needs full tracebacks, which that transcript does not carry for the largest
class, and this block orders a fresh capture rather than a re-analysis. The frames must be
attributed by the DEEPEST frame lying inside the built tree, never by the last frame.

## The capture, and the control that makes it a rebuild rather than a new measurement

A rebuild whose predecessor's figures it cannot reproduce is measuring two things at once, so
the transform is re-run FIRST and required to reproduce round 77's own output before the suite
is touched. All four inputs are on disk and none is regenerated:

    .remedy-wt/r77_corrected.json          the ruled site set DECISION F275 D51 rules
    .remedy-wt/r77_corrected_owners.json   its owner verdicts
    .remedy-wt/r69_flip_transform_guarded.py   the transform DECISION F275 D43 landed
    .remedy-wt/r77_tf_corr.out             round 77's transform output, the control

The tree is built at `ef75e213`, the commit round 76 and round 77 both ran at, and the transform
is invoked over it with the ruled set and the owners file. THE CONTROL: the transform's own
summary must reproduce `.remedy-wt/r77_tf_corr.out` — 2185 ruled keys all resolving with none
NOT resolving, 263 files rewritten, 0 skipped unparsable, 0 left alone as would-break, 6078
total rewrites, and the per-rule table equal ROW FOR ROW. If it does not reproduce, STOP and
hand back with the difference: do not proceed to the suite on a tree that is not round 77's.

The transform takes an optional fourth argument. Round 77's output reports 9 rewrites under
`T8 status value read`, so a status input was supplied and this block does not name which: run
the invocation that REPRODUCES the control, reporting the exact argument vector you used, and
if no vector reproduces it, STOP and report the closest and its difference.

## Constraints

1. EVERY SLICE IS APPLIED BYTE FOR BYTE. A slice is never edited, reflowed, re-wrapped or
   corrected, not even where it is wrong. A discrepancy is DECLARED in the handback with the
   measurement that shows it, and the slice still lands as written.
2. THE ARTEFACT AT C4 IS WRITTEN BY YOU, FROM YOUR OWN RUN. This block ships no slice for it and
   states none of its figures, because the figures do not exist until the run happens. It states
   the artefact's required SECTIONS below, and G5 gates every quoted line of it against the
   instrument's own output rather than against any numeral written here.
3. NO `.py` FILE IS CREATED ANYWHERE UNDER `.agent/` OR ANYWHERE INSIDE THE PRIMARY CHECKOUT'S
   TRACKED TREE. The attribution script lives under `.remedy-wt/` and is never committed. A `.py`
   file inside the tree is counted by the ruff ceiling `tests/orchestration/test_ci_budgets.py`
   freezes, and a clean one produces no ruff row, so a gate reading ruff's output cannot see it:
   G6(d) reads the FILESYSTEM.
4. THE SUITE RUN IS TAKEN IN THE BUILT TREE UNDER `.remedy-wt/`, NEVER IN THE PRIMARY CHECKOUT,
   and it is the only expensive step in this round. Run it once. It carries the same missing
   `apps/ui/node_modules` every previous arm carried; that is a property of the environment, it
   is shared with the transcript this round compares against, and it is not argued away.
5. NO GATE BELOW DEMANDS A GREEN SUITE, and no reading this round turns on the suite's colour.
   The round reads TRACEBACKS out of a failing run. A gate that demanded green could not pass
   and would prove nothing if it did.
6. C1 IS THE FIRST SUBSTANTIVE COMMIT, per item 23 of §3: this round touches the finding ledger,
   so the plan advances before the ledger does.
7. NO COMMIT EXCEEDS 500 INSERTIONS, measured per commit with `git show --numstat`.
8. NO `gh` COMMAND AND NO `remedy` CLI COMMAND IS RUN. No pull request is created, edited or
   merged. No branch is created or deleted. No merge. No force-push. No history rewrite.
9. READ `.agent/STOP` BEFORE C0a AND AGAIN BEFORE C6. It does not exist at this round's base.
   If it appears, finish the commit in hand, write the handback recording both readings with
   their timestamps, push, and stop — do not stage it, do not delete it.
10. THE BLOCK'S OWN SIZE: this block is 371 lines TOTAL and 294 of them are PROSE, against the
    caps DECISION F085 D6 and D5 set at 490 and 400. Report both numbers as measured.
11. GATES RUN AT C5, STRICTLY BEFORE C6, so the handback can quote every one of them. Each gate
    writes its transcript to a file under `.remedy-wt/` and the handback reports the REAL exit
    code read back out of that file, one line per gate.
12. EVERY TREE AND TRANSCRIPT THIS ROUND PRODUCES IS LEFT ON DISK UNDER `.remedy-wt/` AND PINNED
    BY SHA256 IN THE ARTEFACT, because the next round re-analyses them and a transcript that is
    deleted cannot be re-taken inside a round.

## The attribution rule, stated exactly

For every `AttributeError` in the fresh transcript whose message names an attribute in
`job_id`, `job_title`, `task_id` or `title`:

(a) Take the traceback the error belongs to, and select the DEEPEST frame whose file path lies
inside the built tree. A frame in `site-packages`, in the standard library, or in pytest's own
machinery is NOT in the tree and is skipped. If no frame of the traceback is in the tree, the
error is reported as UNATTRIBUTABLE with its class and its raising frame, and it is counted.

(b) Reduce that frame's path to a path relative to the built tree's root, and pair it with the
frame's line number.

(c) Report whether `.remedy-wt/r77_corrected.json` holds a ruled site at that exact
`(relative path, line)`, and if it does, report every `(column, attribute)` it holds there.

(d) Report the source line at that `(relative path, line)` read from `ef75e213` — not from the
built tree — so the reader sees the code BEFORE the flip, which is the text the ruled site was
keyed against.

(e) Group the result by receiver class and attribute, and report the group sizes you MEASURED.
The block states no count for any group.

THE ONE READING THIS ROUND EXISTS TO PRODUCE is the answer to (c) summed over the frames: how
many of the surviving over-selection frames land on a ruled site the corrected set holds, and
how many do not. A frame that lands on a held site names a site the flip's input could drop; a
frame that lands nowhere in the set is a different defect and is reported as such rather than
folded in.

## The artefact's required sections

`.agent/f275_t003_frame_attribution_r79.md` carries, in this order and under headings of your
own wording: the inputs with their sha256 digests and byte sizes; the transform control, stated
as reproduced or not with the per-rule comparison; the suite run's selection, its bad-node total
and how that total compares with round 77's; the attribution table, one row per frame group,
carrying the columns the attribution rule names; the UNATTRIBUTABLE set with its count; and a
closing section naming what the reading does NOT settle. Every FIGURE in it is a figure the
instrument printed. QUOTE NO WALL-CLOCK DURATION anywhere in it — the suite's summary line
carries one and round 73 failed on exactly that.

## Done when — the gates

### G1 — transport, the block budget, the insertion cap

(a) `.agent/authored/f275-r79.md` at C0a is byte-identical to the reviewer's scratch original at
`.remedy-wt/r79_block.md`, by `cmp`. This is the PRIMARY proof and not the §4.9 digest fallback.
(b) `.agent/last_block.md` at C0b is byte-identical to the COMMITTED C0a blob, not to any
working copy.
(c) Extract every BEGIN/END slice from the committed C0a blob, report the CARDINALITY YOU
MEASURED — this block states no numeral for it — and for each slice report its byte size, its
line count, and whether its content matches the sha256 on its own BEGIN marker, computed over
the bytes strictly between the BEGIN line and the END line with the trailing newline kept.
(d) Re-measure TOTAL and PROSE as constraint 10 defines them and report both.
(e) Report the number of block lines outside a slice that are a run of a single repeated
character. The expected number is zero, per item 37 of §3.

### G2 — the plan

`.agent/plan.md` at C1 is byte-identical to slice PLAN79; it is at most 50 lines; it carries
exactly one `## Goal` and exactly one `## Next Steps`.

### G3 — the record, with full forensics

For each of the record appends — RECORD79 at C2 and DEC79 at C5, which are the appends into the
two files amend0827 rule 5 reserves full byte forensics for:
(i) READER A, bytes: the pre-commit blob of that path is a byte-exact PREFIX of the post-commit
file, and the slice is a byte-exact SUFFIX of it.
(ii) READER B, structure: the LAST N blank-line-separated units of the post-commit file equal
the slice's N paragraphs IN ORDER, where N is COUNTED by your script from the slice and is never
a number this block asserts.
(iii) NEGATIVE CONTROL: flip one byte inside the FIRST appended paragraph, in the ASCII letter
range `A`-`Z` or `a`-`z` so the flip cannot land inside a multi-byte sequence, and require BOTH
readers to REJECT. Not the last paragraph — a control there leaves reader B unexercised.
(iv) The DELETION column of both commits is ZERO, so no landed paragraph is rewritten.
(vi) `.agent/prose_slips.md` at C3 is the pre-commit blob followed by exactly slice SLIPS79 and
nothing else — a byte-equality check and no arithmetic, which is all amend0827 rule 5 allows a
`.agent/` prose file. Report its insertion and deletion columns; the deletion column is ZERO.
(v) RECORD79's `Gate:` header is compared as a pattern against the headers already in
`.agent/live_review.md`. Derive the pattern from that corpus rather than asserting one, report
how many of the prior headers it matches, and require that RECORD79's header matches it and
duplicates none of them byte for byte.

### G4 — the capture and its control

(a) The built tree's tracked `.py` files are byte-identical to `ef75e213`'s before the transform
runs. Report the count compared and the count differing; the second must be zero.
(b) The transform's summary reproduces `.remedy-wt/r77_tf_corr.out`. Report the comparison as a
per-line diff of the two summaries, which must be empty, and report the argument vector used.
(c) The fresh suite transcript's bad-node total is reported beside round 77's, with the
difference. A difference is NOT a failure of this gate — the gate is that both numbers are
reported and the difference is stated — but a difference over 5 per cent is declared in the
handback with what you believe caused it.
(d) Every tree and transcript this round produced is listed with its path, byte size and sha256,
and each still exists on disk at C5.

### G5 — the artefact

(a) `.agent/f275_t003_frame_attribution_r79.md` at C4 is byte-identical to the file your run
produced, and it did not exist at this round's base — report the base lookup's exit code.
(b) Every line of the artefact that is INDENTED as a quoted instrument line appears verbatim in
the instrument's own saved output, the matching is MONOTONE with indices strictly increasing,
and the count of unmatchable lines is ZERO.
(c) The count of artefact lines carrying a wall-clock duration is ZERO, and so is the count of
three-backtick lines.
(d) The artefact carries every section the block's artefact list names. Report the section
headings you found, in order.

### G6 — the tree, the colours and the path set

(a) `git status --porcelain` is the EMPTY STRING at C5.
(b) `git worktree list` shows the primary checkout alone, and every tree this round built has
been left in place under `.remedy-wt/` per constraint 12 — report both facts, which are not in
tension because those trees are copies rather than registered worktrees. If you built a
registered worktree instead, remove and prune it and say so.
(c) THE CANARY: `python3 -B -m pytest tests/cli/test_golden_path.py -q` in the PRIMARY checkout
at C5. The reviewer measured 42 passed at this round's base.
(d) `ruff check .` at C5 reports 26 rows against the frozen ceiling of 26; and a filesystem
sweep reports ZERO `.py` files anywhere under `.agent/`.

### G7 — the path set and the open set

(a) The changed-path set of the range from this round's base to C6 equals the path set the
Change section names, with MISSING and EXTRA both empty, and the count of changed paths under
`packages/`, `apps/`, `tests/` or `docs/` is ZERO. Run this reading AFTER C6 exists and report
it in the handback. This reading is deliberately taken AFTER C6, unlike every other gate of this
round, which constraint 11 fixes at C5, because its subject includes a path C6 alone creates.
(b) The open set BY DISTINCT ID — registered `- R-xxxx — ` ids minus ids carrying at least one
`Done: R-xxxx — ` line — is reported at this round's base and at C5, together with the
membership difference, which must be empty. `R-0880` is OPEN at both readings.

### G8 — the per-commit insertion counts

`git show --numstat` for each of C0a through C5, reported one line per commit, each under 500.
The handback commit C6 is NOT covered: its own numbers cannot exist while its text is written
(item 14), and the reviewer measures them at the next gate (item 31).

## Handback

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the state block with the
SESSION NUMBER, which is 28, and the round, which is 79; the range; the per-commit table whose
`+/-` cells are read from `git show --numstat` and compared CELL BY CELL against G8's numbers,
with the comparison printed; external actions; one line per gate with the REAL exit code read
back out of its transcript file; the item-status table; deviations; next steps.

NO SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED: amendment amend0911-f275-to-scope, restored
to `docs/agents/self_drive_protocol.md` by round 78, lifts this feature's limit without a
replacement number. State the operator-questions count in `## Next` as restored rule C requires,
read from `.agent/operator_questions.md`.

## SLICE PLAN79 — replaces `.agent/plan.md` at C1

BEGIN PLAN79 sha256=f2339a78afe413d254cf6f29150638c282f8d83470983486b2d1fead684235c2
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

ROUND 79 CARRIES THE SURVIVING OVER-SELECTION FRAMES BACK TO THE RULED SITES THAT PRODUCE THEM,
which is the second obligation `R-0880` names and the one thing round 77 left open. The reviewer
measured before authoring that the saved transcript cannot answer it: the frames on the largest
class resolve to a library frame rather than to a repository site, and the short summary is
truncated. So the round rebuilds the corrected arm's tree under a control that must reproduce
round 77's transform output exactly, re-runs it with full tracebacks, and attributes each frame
by the deepest frame lying inside the tree. The round 78 verdict and its two prose slips are
booked.

## Next Steps

1. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as the
   home of the id-SHAPE seam behind the three largest residue classes. Production code, so a
   SPLIT round with mutation red-proofs.
2. THE FLIP, on the corrected set DECISION F275 D51 rules, less whatever sites round 79's
   attribution shows the surviving frames land on, carrying DECISION F275 D48's obligations: the
   full suite is the backstop, and the thin set is re-derived before the flip with any site
   fallen to zero witnesses treated as a stop.
3. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20 sessions
  and 60 rounds without a replacement, so this feature closes only at full scope and owes no
  scope report. Round 78 restored that paragraph to the protocol after a merge dropped it.
- THE ATTRIBUTION MAY NOT REACH EVERY FRAME. A traceback with no frame inside the tree is
  unattributable by the rule this round uses, and the round reports that set rather than
  forcing it into a site.
- THE CORRECTED SET IS BETTER, NOT RIGHT, and 1204 bad nodes is the best reading this chain has
  taken and is not near green.
- The open set is 87 by distinct id at this round's base, with `R-0880` open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN79

## SLICE RECORD79 — appended to `.agent/live_review.md` at C2

BEGIN RECORD79 sha256=959bf44bded880b286f5f5fbb5d28cb71a01e4cb6090afff2526a51991a25290

Gate: F275 R78 — the F275 round 78 entry. VERDICT PASS. Written by the planner and reviewer of session 28 after reading the committed range `e262f420`..`d3610730` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs and against its own scratch originals; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 79, per operator amendment amend0827-process-diet rule 1. THE ROUND REPAIRED A LOST OPERATOR ORDER. The operator's merge `e262f420` brought eleven of amendment amend0911-feedback's twelve files onto this branch and resolved the twelfth, `docs/agents/self_drive_protocol.md`, in favour of the branch, dropping the four paragraphs `main` added at `d0aa833b` — finding ownership, rolling paydown, the operator questions file, and the lifting of this feature's session and round limit. The branch therefore held DECISIONs amend0911-feedback D8 and D9 naming that document as their home while the document said nothing about them, and the merge base now including `d0aa833b` meant a later merge of this branch would have deleted the four paragraphs from `main`. `R-0881` records it and round 78 resolved it.

THE REPAIR WAS DERIVED RATHER THAN AUTHORED AND THE PROOF IS TWO ROUND TRIPS. No slice carried the restored text: the bytes were computed from the path's blobs at `d0aa833b` and at the round's base, and the reviewer re-derived the same expression independently at `e262f420` — leading agreement 246 lines, trailing agreement 13, a main-only block of 65 lines and a branch-only block of 20. The committed file is 345 lines, `git show --numstat` reads 66 insertions and 0 deletions, the inserted region equals the derived slice, the file with that region removed equals the base blob byte for byte, and the file with the amend0908 paragraph and its trailing blank removed equals `main`'s blob byte for byte. NEITHER IDENTITY IS SUFFICIENT ALONE and the reviewer measured that before ordering the conjunction: a letter flipped inside the inserted region leaves the second identity TRUE, and a line deleted from the shared tail leaves the slice identity TRUE. Four mutations were run against the conjunction and all four were rejected, with the unmutated control accepted by all three readings.

EVERY OTHER GATE HOLDS AND THE REVIEWER RE-RAN ALL EIGHT. The block was byte-identical to the reviewer's scratch original at 30875 bytes, `.agent/last_block.md` equalled the committed block blob, all four slices matched the sha256 on their own BEGIN markers, and the block re-measured at 347 lines TOTAL and 275 PROSE with zero repeated-character lines. `.agent/plan.md` was byte-identical to its slice at 48 lines. The three appends were exact under reader A, reader B held over the whole appended region at N counted from the slice as 3, 8 and 1, all three negative controls on the FIRST appended paragraph were rejected by both readers, and every deletion column was ZERO. The prose-slip lines were extracted from the committed handback rather than retyped, and the append was exactly the four lines composed from them. `tests/test_agent_tooling.py` was green at the base and at the restoring commit, `tests/docs/` green at 306, the canary at 42, `ruff check .` at 26 rows against the frozen ceiling of 26. The open set read 87 at the base, 88 at the registration and 87 at the resolution, with membership identical at the two ends and `R-0880` open at each.

TWO DEFECTS OF THIS ROUND'S BLOCK WERE THE REVIEWER'S AND THE WORKER FOUND BOTH. G1(c) said "the three authored slices" over a block carrying four, and G7(c) ordered the changed-path set of the whole range measured at a commit strictly before the one that creates the last of those paths, so it was unmeetable as written at the time it was ordered. Neither damaged anything on disk: all four digests were verified anyway, and the reviewer's own re-run of G7(c) over the whole range including the handback commit reads the full path set with MISSING and EXTRA both empty. Two dated lines in `.agent/prose_slips.md` and no id, per amend0827-process-diet rule 2 — nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong, and neither gate is over production code.

`R-0881` STAYS RESOLVED BY ROUND 78's OWN RESOLUTION AND THIS ENTRY ADDS NO SECOND ONE. The resolution paragraph round 78 committed at its own final ledger commit is the record, and this entry deliberately carries no line beginning with the resolution keyword: a second such line for one id is subtracted twice by the canonical line-count reader in `scripts/rotate_live_review.py` while the distinct-id reader subtracts it once, and that gap is a measurement nuisance this record does not need. The reviewer re-derived the fix independently at `d3610730` and every reading holds.
END RECORD79

## SLICE SLIPS79 — appended to `.agent/prose_slips.md` at C3

BEGIN SLIPS79 sha256=cc0134f8d461e241edbfae9a958ad41dfbefc301dd10de6f76d295d4a0c70435

2026-09-12 · F275 R78 · The round 78 block's G1(c) ordered "each of the three authored slices below" over a block carrying four, and the worker's gate script counted four mechanically and declared the gap. This is item 16's widened rule — a gate that names a CATEGORY of the block's own slices names the category and gives NO numeral for it, because the numeral is hand-counted while the extraction beside it is measured. The reviewer had applied exactly that rule twice in the same block before emission, deleting "Eight paths over nine commits" from the Change section and "four of them" from G4(vi), and then left the same defect standing in G1(c). THE RULE THAT FOLLOWS: a pre-emission sweep for a class of defect is run over EVERY instance of that class in the block and never over the instances the author happens to remember writing, because the one that survives is by construction the one the author was not thinking about — and the sweep is mechanical, since "count the nouns that quantify my own slices" is a grep and reading it back is not.

2026-09-12 · F275 R78 · The round 78 block's G7(c) ordered the changed-path set of "the whole range" to equal the eight paths of its Change section, while constraint 9 ordered every gate to run at C6 — and one of those eight, `.agent/handoff.md`, is created by C7 alone. The gate was therefore unmeetable at the moment it was ordered, it exited red on a correct measurement of seven paths, and the worker declared it rather than adjusting the recipe. This is item 14's class reaching a PATH SET rather than a per-commit numeral: the block already knew that the handback commit cannot be covered by a gate that runs before it, said so explicitly in G8, and then wrote a different gate whose subject silently included that commit. THE RULE THAT FOLLOWS: when a block states a rule about which commits its gates can reach, every gate is read back against that rule by subject and not only by command — a gate naming a SET is covered by the rule exactly when one member of the set is written by the uncovered commit, and that membership is the thing to check.
END SLIPS79

## SLICE DEC79 — appended to `.agent/decisions.md` at C5

BEGIN DEC79 sha256=f117f403c850379ae8170bab684c563dd2d55264aee69be3bc1cd277a9260b53

## DECISION F275 D53 (2026-09-12, F275 round 79) — the surviving over-selection frames are attributed by the DEEPEST IN-TREE FRAME of a fresh full-traceback run, because the saved transcript names a library frame for the largest class

CONTEXT. `R-0880`'s second obligation asks the transform to refuse a site whose owner verdict cannot be confirmed, and DECISION F275 D51 left 19 over-selection frames surviving the corrected set on classes the shipped owner check refuses rather than decides. Round 77's artefact recorded that those 19 were not carried back to the sites producing them and that the probe which would do it "was written and works". Before this round was authored the reviewer tested that against the bytes at `.remedy-wt/r77_suite_corr.out`, measured at `e262f420`.

THE MEASUREMENT THAT FIXES THE METHOD. The transcript holds 24 location frames whose message is an `AttributeError` on a unified attribute; 19 are on a named class and 5 on `NoneType`, which is the instrument's class filter and not a discrepancy. Those 19 resolve to five distinct locations, and the location carrying twelve of them is inside `pydantic`, not this repository — the summary names the frame the error was RAISED in, not the site that reached it. Two of the five resolve to a ruled site in the corrected set and three do not, and the short summary is truncated at `- Attribu...`, so the failing nodes cannot be selected by error class out of it either.

CHOSEN, FIRST: THE ATTRIBUTION IS BY THE DEEPEST FRAME INSIDE THE BUILT TREE, never by the last frame of the traceback. A frame in `site-packages`, in the standard library or in pytest's own machinery is skipped, and a traceback with no in-tree frame at all is reported as UNATTRIBUTABLE with its class and its raising frame rather than forced onto a site. ALTERNATIVE: attribute by the summary line, which is what the cheap route would have done; rejected on the measurement above, because it attributes twelve of nineteen frames to a library file and would have reported a correct-looking table that names no site this feature can act on.

CHOSEN, SECOND: THE CAPTURE IS A REBUILD UNDER A CONTROL, NOT A NEW MEASUREMENT. The tree is built at `ef75e213`, the commit both previous arms ran at, and the transform is re-run over it with the ruled set and owners file round 77 used, and its summary must reproduce `.remedy-wt/r77_tf_corr.out` row for row before the suite is touched — 2185 ruled keys, 263 files rewritten, 6078 total rewrites. ALTERNATIVE: re-run the suite without reproducing the transform first, rejected because a rebuild whose predecessor's figures it cannot reproduce moves two variables at once and the resulting frames would not be the frames DECISION F275 D51 counted.

CHOSEN, THIRD: WHAT THE READING IS FOR. A frame landing on a ruled site the corrected set holds names a site the flip's input can drop, which is a concrete narrowing of the one commit this feature cannot split. A frame landing nowhere in the set is a DIFFERENT defect — the rewrite that produced it came from somewhere other than a held site — and it is reported separately rather than folded into the first count. The round rules nothing about the flip's input set itself; that stays DECISION F275 D51's until a later round has the attribution in hand.

CONSEQUENCE. `R-0880` is not resolved by this round and is not expected to be: the round produces the attribution its second obligation needs, and whether the transform gains a refusal is a later decision with the table in front of it. Nothing about the id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse is touched, no production line moved, and the tree and transcript this round builds are left on disk and pinned by sha256 so the next round re-analyses the same bytes rather than re-taking a twenty-minute pass.

HOW TO REVERSE. Delete this paragraph block and the artefact it names. The 19 frames then stand unattributed as round 77 left them, DECISION F275 D51's ruling on the flip's input is untouched either way, and the next round re-reads the count out of `.agent/f275_t003_flip_residue_r77.md`.
END DEC79
