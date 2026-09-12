# STEP T003 — F275 ROUND 81 — the frames name a FALLBACK, and the class it puts at risk

## Goal

Round 80's corrected attribution sends seventeen frames to three ruled sites. Read those sites
against the SHIPPED owner check and against their own source, measure the class they belong to
across the whole corrected set, and rule which sites come out of the flip's input. Book the
round 80 PASS verdict and its prose slips. NO PRODUCTION LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r81.md`
- C0b mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 81 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 80 reviewer verdict — `.agent/live_review.md`
- C3 append the round 80 prose slips — `.agent/prose_slips.md`
- C4 land the fallback-class artefact — `.agent/f275_t003_owner_fallback_r81.md`
- C5 record DECISION F275 D55 — `.agent/decisions.md`
- C6 the round 81 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r81.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/f275_t003_owner_fallback_r81.md
    .agent/decisions.md
    .agent/handoff.md

The round 79 and round 80 artefacts are NOT edited, NOT deleted and NOT staged, and no landed
DECISION is rewritten: C5 APPENDS D55 and its deletion column is ZERO.

NOTHING under `packages/`, `apps/`, `tests/` or `docs/` is touched. No suite is run and no
transform is executed. The only tree this round builds is a read-only copy of `ef75e213` used to
run a static check, and it is built by the recipe below.

## What the reviewer measured before authoring this

Round 80's corrected set is 24 records — 19 on a named receiver class and 5 on `NoneType` — and
17 of them land on a ruled site the corrected set holds, at three sites carrying five ruled
columns between them. The reviewer read all five at `ef75e213` and ran the SHIPPED owner check
of DECISION F275 D47 over them, at `89d4772a`:

    tests/cli/test_repair_runtime.py:68    return str(job.id), str(art.id), str(data_dir)
      col 19  receiver job    CONFIRMED Job
      col 32  receiver art    REFUSED — absent from the decided set
    packages/orchestration/brain_detail.py:345
                              task = next((t for t in job.tasks if str(t.id) == node.id), None)
      col 45  receiver t      CONFIRMED Task
      col 54  receiver node   REFUSED — absent from the decided set
    packages/orchestration/project_registry.py:856   job_map = {str(j.id): j for j in jobs}
      col 19  receiver j      REFUSED — absent from the decided set

THE OWNER CHECK IS NOT WRONG ANYWHERE HERE; IT DECLINES, AND THE TRANSFORM RENAMES ANYWAY. Every
column the frames blame is a column the check REFUSES, and the rename happens on the fallback
the transform's P1 rule describes — the owner comes from the static verdict where there is one,
else from the probe's line, else from the receiver name. On these two lines the line carries one
verdict and both columns take it, so `art` is renamed as a Job and `node` as a Task. That is the
277-site blind spot DECISION F275 D45 ruled acceptable, and these seventeen frames are the first
BEHAVIOURAL measurement of what it costs.

THE THIRD SITE IS DIFFERENT AND MUST NOT BE SWEPT IN WITH THE OTHER TWO. At
`project_registry.py:856` the receiver `j` iterates `jobs`, so the rename is right for the
production record and the single frame comes from a `_FakeJob` double in the test that lacks the
unified field. A site whose rename is correct and whose test double is stale is a test to update
with the flip, not a site to drop.

THE CLASS, MEASURED ACROSS THE WHOLE CORRECTED SET rather than at these three sites: of 2185
ruled sites over 2080 distinct lines, 91 lines carry more than one ruled site, and on 26 of
those a single shared owner verdict spans sites whose receivers are DIFFERENT NAMES. Both lines
behind sixteen of the seventeen frames are in that 26. The block states these figures because
the reviewer measured them; G4 orders every one of them MEASURED AGAIN and reports the
comparison, and a difference is declared rather than reconciled.

A SHARED VERDICT OVER DIFFERING RECEIVERS IS NOT AUTOMATICALLY WRONG — `job_one` and `job_two`
on one line are both Jobs — so 26 is an upper bound on the suspect set and this round does not
treat it as a defect count. What it is, is the population the fallback can reach.

## The base tree, and the control that proves the recipe

The static check needs the UNFLIPPED tree and it enumerates its files with `git ls-files`, so a
plain extraction is not enough: build it as an archive of `ef75e213` extracted into a scratch
directory, then `git init` and `git add -A -f` inside it so the index exists. The reviewer
measured that without the index the check reports every site as unreadable and decides nothing,
which is a gate that cannot fail wearing the face of a gate that cannot pass.

THE CONTROL: run the shipped stage over that tree with the corrected set and its owners file and
require its summary to reproduce `.remedy-wt/r77_stage_corrected.out` — 2185 ruled sites, 71
live record classes, 1908 CONFIRMED, 277 REFUSED across the three stated reasons, and 0
CONTRADICTED. If it does not reproduce, STOP and hand back with the difference rather than
proceeding on a tree that is not round 77's.

## Constraints

1. EVERY SLICE IS APPLIED BYTE FOR BYTE. A slice is never edited, reflowed, re-wrapped or
   corrected, not even where it is wrong. A discrepancy is DECLARED in the handback with the
   measurement that shows it, and the slice still lands as written.
2. THE INPUTS ARE PINNED AND NONE IS REGENERATED. Check each against its digest before running
   anything; if any is missing or differs, STOP and hand back rather than rebuilding it.

    .remedy-wt/f275-r73-owner-stage.py      24253 bytes  sha256 7be3437450d1f183d241e8a5161a6ae182652d0aecd674ea10e8f870407eddb8
    .remedy-wt/r77_corrected.json          120753 bytes  sha256 765b5ba99f2c92765349c3a013f4074c62ece893cb50b373450927af0290a512
    .remedy-wt/r77_corrected_owners.json   121095 bytes  sha256 670c6e952667b7c52b6c5a9ffd832dcc9f096aedfba114b83bc28ca061591b44
    .remedy-wt/r77_stage_corrected.out        447 bytes  sha256 86ecf97aa7c6a522427e2f137782594546a2f330d7a87f2242ec37bee2e56fc6
    .remedy-wt/r79_frames.jsonl           3638751 bytes  sha256 16d876503e3c790cde16943d802116d305b15921268ed05ab43812ce1842bc43

3. THE ARTEFACT AT C4 IS WRITTEN BY YOU, FROM YOUR OWN RUN. This block states figures the
   reviewer measured; the artefact states the figures YOUR run produced, and where the two
   differ the artefact carries yours and the handback declares the difference.
4. AN `ast` COLUMN IS A BYTE OFFSET INTO ITS LINE, and the receiver is the identifier that
   STARTS at that offset — not the text before it. The reviewer's first extraction read
   backwards from the column and found nothing, which is how a real class came within one
   measurement of being reported as empty.
5. NO `.py` FILE IS CREATED UNDER `.agent/` OR ANYWHERE INSIDE THE PRIMARY CHECKOUT'S TRACKED
   TREE. Scripts live under `.remedy-wt/` and are never committed. G6(d) reads the FILESYSTEM.
6. C1 IS THE FIRST SUBSTANTIVE COMMIT, per item 23 of §3.
7. NO COMMIT EXCEEDS 500 INSERTIONS, measured per commit with `git show --numstat`.
8. NO `gh` COMMAND AND NO `remedy` CLI COMMAND IS RUN. No pull request is created, edited or
   merged. No branch is created or deleted. No merge. No force-push. No history rewrite.
9. READ `.agent/STOP` BEFORE C0a AND AGAIN BEFORE C6. It does not exist at this round's base.
   If it appears, finish the commit in hand, write the handback recording both readings with
   their timestamps, push, and stop — do not stage it, do not delete it.
10. THE BLOCK'S OWN SIZE: this block is 343 lines TOTAL and 267 of them are PROSE, against the
    caps DECISION F085 D6 and D5 set at 490 and 400. Report both numbers as measured.
11. EVERY GATE EXCEPT G7(a) RUNS AT C5, STRICTLY BEFORE C6. G7(a)'s subject includes a path C6
    alone creates, so it runs after C6 and the handback says so. Each gate writes its transcript
    under `.remedy-wt/` and the handback reports the REAL exit code read back out of that file.

## Done when — the gates

### G1 — transport, the block budget, the insertion cap

(a) `.agent/authored/f275-r81.md` at C0a is byte-identical to the reviewer's scratch original at
`.remedy-wt/r81_block.md`, by `cmp`. This is the PRIMARY proof, not the §4.9 digest fallback.
(b) `.agent/last_block.md` at C0b is byte-identical to the COMMITTED C0a blob.
(c) Extract every BEGIN/END slice from the committed C0a blob, report the CARDINALITY YOU
MEASURED — this block states no numeral for it — and for each slice its byte size, its line
count and whether its content matches the sha256 on its own BEGIN marker, computed over the
bytes strictly between the BEGIN line and the END line with the trailing newline kept.
(d) Re-measure TOTAL and PROSE as constraint 10 defines them and report both.
(e) Report the number of block lines outside a slice that are a run of a single repeated
character. The expected number is zero, per item 37 of §3.

### G2 — the plan

`.agent/plan.md` at C1 is byte-identical to slice PLAN81; it is at most 50 lines; it carries
exactly one `## Goal` and exactly one `## Next Steps`.

### G3 — the record, with full forensics

For each of the record appends — RECORD81 at C2 and DEC81 at C5:
(i) READER A: the pre-commit blob is a byte-exact PREFIX of the post-commit file and the slice
is a byte-exact SUFFIX of it.
(ii) READER B: the LAST N blank-line-separated units of the post-commit file equal the slice's N
paragraphs IN ORDER, where N is COUNTED by your script and is never a number this block asserts.
(iii) NEGATIVE CONTROL: flip one byte inside the FIRST appended paragraph, in the ASCII letter
range `A`-`Z` or `a`-`z`, and require BOTH readers to REJECT.
(iv) The DELETION column of both commits is ZERO.
(v) `.agent/prose_slips.md` at C3 is the pre-commit blob followed by exactly slice SLIPS81 and
nothing else, a byte-equality check with no arithmetic; its deletion column is ZERO.
(vi) RECORD81's `Gate:` header is compared against a pattern DERIVED from the headers already in
`.agent/live_review.md`; report how many prior headers that pattern matches, and require that
RECORD81's header matches it and duplicates none of them byte for byte.

### G4 — the control, the five columns and the class

(a) Every input of constraint 2 matches its stated digest. Report each comparison.
(b) THE CONTROL: the shipped stage's summary over the rebuilt base tree reproduces
`.remedy-wt/r77_stage_corrected.out`. Report the comparison as a per-line diff of the two
summaries, ignoring any wrapper line your own harness adds, and report the argument vector used.
If it does not reproduce, STOP.
(c) THE NEGATIVE CONTROL ON THE RECIPE: run the same stage over a copy of the tree with NO git
index and report what it decides. The reviewer measured that it decides nothing and calls every
site unreadable; report what you measure. This exists so the control in (b) is known to be
capable of failing.
(d) For each of the five ruled columns the reviewer lists above, report: the receiver identifier
read at that byte offset, the owner verdict the shipped stage gives it or REFUSED if the site is
absent from the decided set, and the pre-flip source line read from `ef75e213`. Report also how
many of the five are CONFIRMED and how many REFUSED — MEASURED, not taken from this block.
(e) THE CLASS: over the corrected set report the number of ruled sites, the number of distinct
lines, the number of lines carrying more than one ruled site, and among those the number on
which one shared owner verdict spans sites whose receiver identifiers differ. PARTITION the
multi-site lines by whether their sites' verdicts agree, and report the parts and the total.
(f) CROSS-CHECK, against numbers nothing in this round produced: the counts in (e) are compared
against the figures this block states, and the two lines behind the frames are checked for
membership in the class set. Report each as MATCH or as a difference with its size. A cross-check
between independently derived numbers can fail; a partition cannot, and both are labelled.

### G5 — the artefact

(a) `.agent/f275_t003_owner_fallback_r81.md` at C4 is byte-identical to the file your run
produced, and it did not exist at this round's base — report the base lookup's exit code.
(b) Every INDENTED non-blank line of the artefact appears verbatim in your instrument's saved
output, the matching is MONOTONE with strictly increasing indices, and the count of unmatchable
lines is ZERO. Report the number of lines compared and the rule you used to decide a line is
indented.
(c) The count of artefact lines carrying a wall-clock duration is ZERO, and so is the count of
three-backtick lines.
(d) The artefact carries, in order and under headings of your own wording: what round 80 handed
it; the control and its negative control; the five columns with their verdicts; the class with
its partition; the ruling and which sites it names; and a closing section on what the reading
does NOT settle, stating in its own words that `R-0880` remains open. Report the headings found.
(e) The round 79 and round 80 artefacts are byte-identical at this round's base and at C5, and
neither appears in the round's changed-path set.

### G6 — the tree, the colours and the path set

(a) `git status --porcelain` is the EMPTY STRING at C5.
(b) `git worktree list` shows the primary checkout alone. The trees under `.remedy-wt/` are
copies rather than registered worktrees; report that both facts hold together.
(c) THE CANARY: `python3 -B -m pytest tests/cli/test_golden_path.py -q` in the PRIMARY checkout
at C5. The reviewer measured 42 passed at this round's base.
(d) `ruff check .` at C5 reports 26 rows against the frozen ceiling of 26 — count the rows
yourself and cross-check your count against the tool's own `Found <n> errors.` line — and a
filesystem sweep reports ZERO `.py` files anywhere under `.agent/`.

### G7 — the path set and the open set

(a) The changed-path set of the range from this round's base to C6 equals the path set the
Change section names, with MISSING and EXTRA both empty, and the count of changed paths under
`packages/`, `apps/`, `tests/` or `docs/` is ZERO. Taken after C6 per constraint 11.
(b) The open set BY DISTINCT ID is reported at this round's base and at C5 with the membership
difference, which must be empty; `R-0880` is OPEN at both. Report also the canonical line-count
reading of `scripts/rotate_live_review.py` at both and the gap between the two readings, which
is a pre-existing property of two ids carrying two resolution lines each and must not grow.

### G8 — the per-commit insertion counts

`git show --numstat` for each of C0a through C5, one line per commit, each under 500. The
handback commit C6 is NOT covered: its own numbers cannot exist while its text is written
(item 14), and the reviewer measures them at the next gate (item 31).

## Handback

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the state block with the
SESSION NUMBER, which is 28, and the round, which is 81; the range; the per-commit table whose
`+/-` cells are compared CELL BY CELL against G8's numbers with the comparison printed; external
actions; one line per gate with the REAL exit code read back out of its transcript; the
item-status table; deviations; next steps. No scope report and no session-limit banner is owed.
State the operator-questions count in `## Next` as rule C requires.

## SLICE PLAN81 — replaces `.agent/plan.md` at C1

BEGIN PLAN81 sha256=8a6d653acecb3343f262b6b6c8a8d1269c5c055a37783dc0aed874beccd248e4
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

ROUND 81 READS THE THREE SITES ROUND 80's ATTRIBUTION NAMES AND FINDS A FALLBACK BEHIND THEM.
Every ruled column the seventeen frames blame is a column the shipped owner check REFUSES rather
than decides, and the transform renames it anyway on the fallback its P1 rule describes, so on a
line carrying one owner verdict both columns take it and a receiver of another record is renamed
with the record the line names. Two of the three sites are that shape; the third is a correct
rename whose test double is stale. The class those two belong to is the lines where one shared
verdict spans differing receivers, and the round measures it across the whole corrected set. The
round 80 verdict and its prose slips are booked.

## Next Steps

1. Drop the sites DECISION F275 D55 names from the flip's input and re-derive the corrected set,
   which is a set subtraction and a re-key, not a new measurement.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as the
   home of the id-SHAPE seam behind the three largest residue classes. Production code, so a
   SPLIT round with mutation red-proofs.
3. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, and the
   thin set is re-derived before the flip with any site fallen to zero witnesses treated as a
   stop. The stale test double at `project_registry.py:856` is updated in the flip's own commit.
4. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20 sessions
  and 60 rounds without a replacement, so this feature closes only at full scope.
- THE CLASS IS AN UPPER BOUND, NOT A DEFECT COUNT. A shared verdict over differing receivers can
  be right for both, and only the two sites with behavioural evidence are ruled out.
- ONLY WHAT A TEST EXERCISES PRODUCED A FRAME. The fallback reaches sites no test reaches, and
  those are invisible to every reading this chain has taken.
- The open set is 87 by distinct id at this round's base, with `R-0880` open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN81

## SLICE RECORD81 — appended to `.agent/live_review.md` at C2

BEGIN RECORD81 sha256=a81e402d0acb759914e07664f51d68cf59c81c569d66d9ca2db111e48c82a9ae

Gate: F275 R80 — the F275 round 80 entry. VERDICT PASS. Written by the planner and reviewer of session 28 after reading the committed range `c7ac5e00`..`89d4772a` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs and against the capture's own records; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 81, per operator amendment amend0827-process-diet rule 1. The round repaired the round 79 FAIL and it repaired it at the predicate rather than at the number: the selection now requires the record's exception CLASS to be `AttributeError` as well as its message to name a unified attribute, and everything downstream is round 79's, unchanged.

THE CORRECTED READING REPRODUCES UNDER THE REVIEWER'S OWN DERIVATION, taken over `.remedy-wt/r79_frames.jsonl` without using the instrument. Of the records the message rule admits, 24 carry the class `AttributeError` — 19 on a named receiver class and 5 on `NoneType` — and 6 carry `AssertionError`, every one of them a node of `tests/orchestration/test_orchestrator_loop.py` naming `_FakeJob.job_id` inside assertion text. The named-class count of 19 matches what `.agent/f275_t003_flip_residue_r77.md` records for that class, and it matches PER KIND as well: `Artifact.job_id` 12, `BrainNode.task_id` 5, `BrainNode.job_id` 1, `_FakeJob.job_id` 1. The attribution split re-derives at 17 frames landing on a ruled site the corrected set holds and 7 landing nowhere, against round 79's published 17 and 13, so the six rows that moved are exactly the six mis-selected records and the actionable half did not move.

EVERY GATE HOLDS AND THE REVIEWER RE-RAN ALL EIGHT. The block was byte-identical to the reviewer's scratch original, `.agent/last_block.md` equalled the committed block blob, all four slices matched the sha256 on their own BEGIN markers, and the block re-measured at 353 lines TOTAL and 275 PROSE. `.agent/plan.md` was byte-identical to its slice at 48 lines. The two record appends were exact under reader A, reader B held over the whole appended region at N counted from the slice as 5 and 8, both negative controls on the FIRST appended paragraph were rejected by both readers, and every deletion column was ZERO. THE LANDED TEXTS WERE NOT REWRITTEN, which is the property this round was built around: the round 79 artefact is byte-identical at the base and at the tip and absent from the changed-path set, and the DECISION F275 D53 paragraph block is byte-identical after the commit that appends D54. The canary read 42, `ruff check .` 26 rows against the frozen ceiling of 26, zero `.py` files under `.agent/`, and the open set 87 by distinct id at both ends with identical membership and `R-0880` open.

THE ONE JUDGEMENT CALL WAS THE WORKER'S AND IT WAS THE RIGHT ONE. Constraint 2 ordered the instrument changed no further than the added condition requires, and the worker also removed five hard-coded lines that printed round 79's false explanation of its own larger count — replacing them with a check that PARSES round 77's artefact for the number it recorded and compares against it. Leaving those lines would have put a false paragraph into the very file the artefact gate quotes against, and replacing a hard-coded narrative with a measurement against an independent document is strictly stronger than the sentence it removed. The worker declared it as the deviation to look at hardest rather than letting it pass, which is how a constraint should be stretched when it is stretched at all.
END RECORD81

## SLICE SLIPS81 — appended to `.agent/prose_slips.md` at C3

BEGIN SLIPS81 sha256=19ae53c395b461ede352f1f4e8bd0e3e2c45ccb54106bfac6114cf3b737706c1

2026-09-12 · F275 R80 · The round 80 block's slices RECORD80 and DEC80 both say "of 1238 captured records", and the capture file holds 1238 JSON lines of which 1237 are per-node records and one is a session-level record, so the rule the sentence describes runs over 1237 of them. Every figure downstream is unaffected and the worker declared the nuance rather than adjusting a slice constraint 1 forbids it to touch. THE RULE THAT FOLLOWS: a count of "records" in a file of newline-delimited JSON names which KIND of record it counts, because a capture format that carries one summary line among its per-item lines makes the file's line count and the population's size differ by exactly the amount nobody checks.

2026-09-12 · F275 R80 · The round 80 block put every gate at C5 in constraint 11 and then wrote G7(a) to measure a path set whose subject includes a path C6 alone creates, saying inside the gate that the reading is taken after C6. Both sentences are true and they contradict each other's scope, and the worker split the gate to satisfy them. THE RULE THAT FOLLOWS: an exception to a blanket ordering constraint belongs IN that constraint, not only in the gate that needs it — a reader checking the constraint never reaches the gate, and this is the second round running in which the same path set forced the same split.
END SLIPS81

## SLICE DEC81 — appended to `.agent/decisions.md` at C5

BEGIN DEC81 sha256=da7da8c8c19f913f441fd0ebd4dfaa15cc0c9f010c67558ce5e7fa9b2be556bf

## DECISION F275 D55 (2026-09-12, F275 round 81) — the seventeen attributed frames blame a FALLBACK rather than a wrong verdict, two ruled sites come out of the flip's input by name, and the third is a stale test double

CONTEXT. DECISION F275 D54 corrected round 79's selection and left a reading its own round did not act on: 17 of the 24 records land on a ruled site the corrected set holds, at three sites. DECISION F275 D45 ruled the owner check's 277 refusals an acceptable blind spot, and DECISION F275 D51 ruled the corrected set the flip's input while leaving `R-0880` open on exactly this residue. This decision reads those three sites and rules on them.

THE MEASUREMENT. The five ruled columns at the three sites were read at `ef75e213` and put through the SHIPPED owner check of DECISION F275 D47. Two are CONFIRMED — `job` at `tests/cli/test_repair_runtime.py:68` column 19, and `t` at `packages/orchestration/brain_detail.py:345` column 45. Three are REFUSED, absent from the decided set entirely: `art` at column 32 of the first line, `node` at column 54 of the second, and `j` at `packages/orchestration/project_registry.py:856` column 19. The check is wrong at none of the five; it declines at three, and the transform renames all five because the ruled set holds them.

CHOSEN, FIRST: THE DEFECT IS NAMED AS A FALLBACK, NOT AS A WRONG VERDICT. The transform's P1 rule takes the owner from the static verdict where there is one, else from the probe's line, else from the receiver name. On both of the first two lines the line carries a single verdict, so a refused column takes the verdict of the column beside it — `art` is renamed as a Job because `job` shares its line, and `node` as a Task because `t` shares its line. Calling this an owner-check error would send the next round to repair a component that is behaving exactly as specified.

CHOSEN, SECOND: TWO SITES COME OUT OF THE FLIP'S INPUT BY NAME — `tests/cli/test_repair_runtime.py` line 68 column 32 attribute `id`, and `packages/orchestration/brain_detail.py` line 345 column 54 attribute `id`. Both carry behavioural evidence: a rename at each produces failing nodes whose exception is an `AttributeError` naming a unified attribute on a receiver of another record. ALTERNATIVE: drop every site the check refuses, all 277 of them, rejected because refusal is not evidence of error and DECISION F275 D45 already weighed and accepted that set; dropping it wholesale trades a measured defect for an unmeasured one.

CHOSEN, THIRD: THE THIRD SITE STAYS AND ITS TEST DOUBLE MOVES INSTEAD. At `project_registry.py:856` the receiver `j` iterates `jobs` and the rename is right for the production record; the single frame comes from a `_FakeJob` double in the test that lacks the unified field. The site stays in the input and the double is updated in the flip's own commit, per the rule that a deletion or a rename never leaves a stub — the test follows the record, not the other way round.

CHOSEN, FOURTH: THE CLASS IS RECORDED AS AN UPPER BOUND AND NOT AS A DEFECT COUNT. Across the corrected set, lines carrying more than one ruled site on which a single shared verdict spans differing receiver identifiers are the population the fallback can reach, and both lines behind sixteen of the seventeen frames are in it. A shared verdict over differing receivers can be right for both — two locals both holding Jobs is the ordinary case — so no site is dropped on membership alone, and the artefact reports the class with its partition rather than a verdict on it.

CONSEQUENCE. `R-0880` stays OPEN. Its second obligation asks the transform to REFUSE a site whose owner verdict cannot be confirmed, and this round neither builds that refusal nor closes the case for it: what it adds is the first behavioural measurement of what the fallback costs, and two sites removed by name. ONLY WHAT A TEST EXERCISES PRODUCED A FRAME, so the fallback certainly reaches sites no reading here can see. No production line moved, no suite was run and no transform was executed.

HOW TO REVERSE. Delete this paragraph block. The flip's input is then DECISION F275 D51's corrected set with both named sites still in it, the two renames land inside the one commit this feature cannot split, and the seventeen frames stand measured in `.agent/f275_t003_frame_attribution_r80.md` with nothing ruled about them.
END DEC81
