# STEP T003 — F275 ROUND 73 — rule the owner check's residual, and unblock the flip

## Goal

Discharge DECISION F275 D45's precondition by its SECOND route. Land RULE H, which widens the
owner check to receiver EXPRESSIONS and carries refusals from 324 to 277; establish by the same
per-site control round 72 used that it finds ZERO new contradictions, which is the evidence
that the resolver route is spent; then measure the residual as a RISK — split by tree, read
against suite coverage, and probed by mutation — and record DECISION F275 D47, which rules it
acceptable at the count it stands and lets the flip proceed. Book the round 72 verdict and its
three prose slips. NO PRODUCTION LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r73.md`
- C0b save the artefact as authored text — `.agent/authored/f275-r73-artefact.md`
- C0c save the owner-check stage carrier — `.agent/authored/f275-r73-owner-stage.py.md`
- C0d save the instrument A carrier — `.agent/authored/f275-r73-instrument.py.md`
- C0e save the instrument B carrier — `.agent/authored/f275-r73-risk.py.md`
- C0f mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 73 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 72 reviewer verdict — `.agent/live_review.md`
- C3 append the round 72 prose slips — `.agent/prose_slips.md`
- C4 record DECISION F275 D47 — `.agent/decisions.md`
- C5 land the residual artefact — `.agent/f275_t003_owner_residual_r73.md`
- C6 the round 73 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r73.md
    .agent/authored/f275-r73-artefact.md
    .agent/authored/f275-r73-owner-stage.py.md
    .agent/authored/f275-r73-instrument.py.md
    .agent/authored/f275-r73-risk.py.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/decisions.md
    .agent/f275_t003_owner_residual_r73.md
    .agent/handoff.md

No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` is touched. This is not a
deletion round and no file is removed.

## The reviewer's texts on disk, and how they travel

Every reviewer-authored text of this round exists as a file under the gitignored `.remedy-wt/`
at this round's base, and each is of one of two kinds. A SLICE is carried verbatim in this
block between a BEGIN and an END marker, the BEGIN marker stating the sha256 of the bytes
between them; the slices are PLAN73, RECORD73, SLIPS73 and DEC73, each under its own heading
below. A WHOLE TEXT is too long to retype and is never retyped: it is transported with
`shutil.copyfile` and never opened in an editor. The whole texts, with their scratch paths and
digests:

    .remedy-wt/f275-r73-artefact.md          12291 bytes  f91e6c7a336baf0925e60e9d422ad04dad38c7b4afaa354b2c62abaf4c99fe72
    .remedy-wt/f275-r73-owner-stage.py.md    24929 bytes  23a4d972d4cd614da20173c2c5b36b79c54736e7639295a59d32eebdad851068
    .remedy-wt/f275-r73-instrument.py.md      8095 bytes  37fb502088f69e8ba3eb7477ca799c0a9c25ced528400e5b2bc407cf552ede84
    .remedy-wt/f275-r73-risk.py.md            8661 bytes  dd04e076e522b23c88dd26db330a72e4418f325de7604484303d828d4ab11dd0

The block travels the same way: read `.remedy-wt/f275-r73.block.md` from disk, verify its
sha256 against the one the delegation wrapper states, and copy it to `.agent/authored/f275-r73.md`
at C0a and to `.agent/last_block.md` at C0f. A slice is applied BYTE FOR BYTE: nothing is
reflowed, re-wrapped, re-indented or corrected, and a slice that looks wrong is APPLIED AS
WRITTEN and declared in the handback.

## Constraints

1. APPLY EVERY SLICE VERBATIM. Extract each by its BEGIN and END marker prefixes, markers
   EXCLUDED, from the COMMITTED C0a blob — never from the delegation prompt and never from
   memory — and check each against the sha256 its own BEGIN marker carries before applying it.
2. PLAN73 is a WHOLE-FILE REPLACEMENT of `.agent/plan.md`. RECORD73, SLIPS73 and DEC73 are
   APPENDS: the pre-commit blob is a byte-exact PREFIX of the post-commit file and the slice
   is an exact SUFFIX of it, separated by exactly one newline.
3. ONE PATH PER COMMIT, in the Bundle's order. Run the AGENTS.md self-review loop before every
   commit: `git diff --cached --stat`, `--numstat` and the full `git diff --cached`. Where a
   commit's diff is a single large blob, the decisive check is BYTE-EQUALITY of the resulting
   blob against its scratch original by sha256, and that is what the handback reports; a hunk
   count is not ordered and proves nothing, because it depends on how much of the old file the
   new one happens to share — C0f REPLACES `.agent/last_block.md` and will carry more than one
   hunk.
4. NO PRODUCTION PATH MOVES. If any gate below would require editing a file under `packages/`,
   `apps/`, `tests/`, `docs/` or `scripts/`, STOP and hand back instead. The mutations G6
   orders happen inside a worktree and are reverted by the instrument itself.
5. DESTRUCTIVE AND SCRATCH WORK IS ISOLATED. Every worktree this round creates lives under the
   gitignored `.remedy-wt/` and is removed and pruned by the instrument that made it.
   `git status --porcelain` is the empty string at every commit and at the handback.
6. NO `gh` COMMAND AND NO `remedy` CLI COMMAND IS RUN. No pull request is created, edited or
   merged. No branch is created. No merge. No force-push. Push the branch after C6.
7. READ `.agent/STOP` FROM DISK before the first commit and again before C6, by BOTH
   `os.path.exists` and `glob`, and report both readings literally in the handback. If it
   exists, finish the commit in hand, write the handback and stop.
8. THIS BLOCK'S OWN SIZE. Measured by the reviewer on the FINAL bytes of
   `.remedy-wt/f275-r73.block.md`: TOTAL 362 lines, PROSE 286 lines, where PROSE is TOTAL
   minus the lines lying between BEGIN and END markers, markers themselves counted as PROSE.
   This clause is the ONLY place either numeral appears; G1 names this clause rather than
   restating them.
9. `R-0880` STAYS OPEN. No finding id is registered, resolved or de-registered this round. Do
   not write a `Done:` or a `Landed:` paragraph of your own; `Done:` is reviewer-authored text
   only. The SLIPS73 lines are not ids, per amend0827-process-diet rule 2.
10. NO `.py` FILE IS CREATED ANYWHERE UNDER `.agent/`. All three python sources ship as `.py.md`
    carriers, because a `.py` file inside the tree is counted by the `ruff` ceiling that
    `tests/orchestration/test_ci_budgets.py` freezes and G7(c) reads.
11. EVERY GATE IS RUN AS `bash -c '<cmd> > <out> 2>&1; echo "REAL_EXIT=$?" >> <out>'` AND THE
    EXIT CODE IS READ BACK OUT OF THE FILE. Write transcripts under `.remedy-wt/`. "Green" as
    a word is a finding; the recorded number is the evidence.
12. THE INSTRUMENTS' INPUTS ARE CHECKED FOR EXISTENCE BEFORE THEY ARE RUN AND NONE IS
    REGENERATED. `.remedy-wt/r69_rekeyed.json` (121516 bytes, sha256
    489fdf8eeb9c4e66b452510de5d362e5d701b4cfe2de79d1d69b768f526d301f) and
    `.remedy-wt/r69_rekeyed_owners.json` (121858 bytes, sha256
    747e8f08c7e3dfc207510a0071d1fd196907ca34667d97baec7ab5028145f57f) must exist with those
    digests. If either is missing or differs, STOP and hand back; do not rebuild it.
13. G5 RUNS BEFORE G6, AND THIS IS AN ORDERING THE ROUND CANNOT SATISFY BY ACCIDENT.
    Instrument A writes `.remedy-wt/r73_map72.json`, the per-site decision map of the shipped
    round 72 stage, and instrument B reads that file to know which sites are refused. Run them
    in that order and say so in the handback.
14. G6 IS THE EXPENSIVE GATE AND ITS COST IS EXPECTED. It runs the full suite FOUR times — a
    warm-up, a control, and one per mutated site — at roughly three to four minutes each under
    coverage. That is the gate, not an overrun. Do not shorten it, do not deselect, and do not
    substitute a scoped run.
15. THIS BLOCK CONTAINS NO LINE THAT IS A RUN OF A SINGLE REPEATED CHARACTER. G1 counts them
    and the expected count is zero, per item 37 of `docs/agents/planner_reviewer_prompt.md` §3.

## Done when — the gates below, all run at C5 before C6 exists

Every gate runs at C5, which is strictly earlier than the commit that writes the handback, so
the handback can quote every reading it states. The handback commit's own numbers are NOT a
gate of this round: the reviewer measures them at the next gate.

**G1 TRANSPORT AND THE BLOCK BUDGET.** For each of the six blobs C0a through C0f commits,
compare the committed bytes against the reviewer's scratch original by size and sha256 and
report EQUAL or not, naming the commit. `.agent/last_block.md` at C0f is compared against the
COMMITTED C0a blob. Then, over the committed C0a blob: extract every BEGIN/END slice, report
the CARDINALITY YOU MEASURED — the block states no numeral for it — and for each slice its
byte size, its line count and whether its content matches the sha256 on its own BEGIN marker.
Then re-measure TOTAL and PROSE as constraint 8 defines them, report both numbers you
measured, and report whether each equals the numeral constraint 8 states for it. Then report
the count of lines in the committed C0a blob that consist of a single character repeated,
which constraint 15 fixes at zero. Finally, for each of the three `.py.md` carriers: report the
number of ```python fence lines and of bare ``` lines, both of which must be 1; extract the
source between them; and confirm that re-wrapping that source in the carrier's own header and
fence reproduces the committed blob BYTE FOR BYTE.

**G2 THE PLAN.** `.agent/plan.md` at C1 is byte-identical to slice PLAN73 — report both sizes
and both sha256 values. Report its line count against the AGENTS.md cap of 50, and the count of
lines matching `^## Goal$` and of lines matching `^## Next Steps$`, both of which are 1.

**G3 THE RECORD.** Three appends, three commits, and for each one TWO INDEPENDENT READERS and
a NEGATIVE CONTROL. Wherever a reading below is taken AT THE BASE, read those bytes with
`git show f8fbe3b6:<path>` into scratch or into memory; nothing is written over a tracked file
to take a base reading.

  (i)  READER A, the byte stream: post == pre + one newline + the slice body. Report pre, post,
       the delta and the body size for each of `.agent/live_review.md`, `.agent/prose_slips.md`
       and `.agent/decisions.md`, and ACCEPT or REJECT.
  (ii) READER B, structural and covering the WHOLE appended region: split the post-commit file
       into blank-line-separated units and compare its LAST N units against the slice's N
       paragraphs IN ORDER, where N is a value your script COUNTS from the slice. Report the N
       you counted for each file and ACCEPT or REJECT.
  (iii) NEGATIVE CONTROL: inside a disposable worktree, flip one ASCII letter inside the FIRST
       appended paragraph of each file and confirm BOTH readers REJECT; then confirm both
       readers ACCEPT the unmutated region. Report the byte offset and the letter for each.
       Choose an ASCII letter, so the flip cannot land inside a multi-byte sequence.
  (iv) Over RECORD73: report its line count, the number of lines AFTER THE FIRST carrying a
       reserved prefix (`- R-`, `Done: R-`, `Landed: R-`, `Gate: `), which is 0, and the number
       of lines C2 ADDS matching `^- R-` and matching `^Done: R-`, both of which are 0.
  (v)  RECORD73's first line joins a repeating record format, so compare it MECHANICALLY
       against its neighbours: report how many lines at the base already match
       `^Gate: F275 R\d+ — the F275 round \d+ entry\.`, whether the new first line matches that
       same pattern, and whether it duplicates any of them.
  (vi) Over DEC73: confirm it begins `## DECISION F275 D47 `, report how many lines at the base
       match `^## DECISION F275 D47` (which is 0), and report the highest existing
       `^## DECISION F275 D\d+` at the base.
  (vii) Over SLIPS73: report the number of paragraphs it adds, how many begin
       `2026-09-12 · F275 R72 · `, and how many lines at the base already begin with that exact
       prefix.

**G4 THE ARTEFACT.** `.agent/f275_t003_owner_residual_r73.md` at C5 is byte-identical to the
C0b blob — report both sizes and both sha256 values. Confirm the path does not resolve at the
base with `git show f8fbe3b6:.agent/f275_t003_owner_residual_r73.md`, whose non-zero exit is
the expected reading. Then report, for EVERY commit C0a through C5, the INSERTION count from
`git show --numstat <sha>` — the `+` column, which is the quantity DECISION F104 D1 caps at
500 — together with the number of paths that commit stages, which is 1 for each.

**G5 INSTRUMENT A — THE WIDENING.**

  (a) Extract the single fence of the COMMITTED C0c carrier to
      `.remedy-wt/f275-r73-owner-stage.py` and of the COMMITTED C0d carrier to
      `.remedy-wt/f275-r73-instrument.py`, reporting each extracted size and sha256.
  (b) Run `python3 -B .remedy-wt/f275-r73-instrument.py . f8fbe3b6` and REPRODUCE EVERY LINE OF
      EVERY BANNER in the handback. The instrument extracts the round 72 stage from its own
      committed carrier, so the comparison is anchored to git and not to scratch.
  (c) THE READINGS THIS GATE TURNS ON, each reported with whether it holds: in section 2, that
      `--narrow` still equals the round 71 figures in every class; in section 4, that of the
      shipped stage's decisions the number now undecided and the number now DIFFERENT are BOTH
      ZERO; and in section 5, that the contradicted SITE LISTS are identical. A non-zero value
      in either of section 4's two numbers is a RED gate: stop and hand back.
  (d) DETERMINISM: run it three times, reporting the byte size of its stdout and of its stderr
      for each run and whether all three stdout captures are byte-identical.

**G6 INSTRUMENT B — THE RESIDUAL AS A RISK.** Read constraint 14 before starting this one.

  (a) Extract the single fence of the COMMITTED C0e carrier to `.remedy-wt/f275-r73-risk.py`,
      reporting the extracted size and sha256, then run
      `python3 -B .remedy-wt/f275-r73-risk.py . f8fbe3b6` ONCE and reproduce EVERY LINE OF
      EVERY BANNER in the handback. It runs the full suite four times; that is expected.
  (b) THE READINGS THIS GATE TURNS ON, each reported with whether it holds: in section 3, that
      the CONTROL's exit code is 0 and its failure count is 0 — if the control is not green,
      the subtraction in section 5 means nothing, so a non-green control is a RED gate and you
      stop and hand back; in section 4, that the number of refused production sites NOT
      executed is 0; and in section 5, that each mutated run exits non-zero and that each
      reverted file is byte-identical to what it was.
  (c) Report `git status --porcelain` and `git worktree list` AFTER this gate, since it is the
      gate that creates and removes the most scratch.

**G7 THE TREE DID NOT MOVE.**

  (a) Report the `git rev-parse` object id of `packages`, `apps`, `tests`, `docs` and `scripts`
      at the base `f8fbe3b6` and at C5, and whether each pair is EQUAL. This is the gate that
      proves G6's mutations left nothing behind.
  (b) THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`, reporting the tail of
      its output and its real exit code.
  (c) `python3 -m ruff check . --output-format concise`. Its exit is 1 whenever any finding
      remains, so THE GATE IS THE COUNT: report the number of rows matching `^\S+:\d+:\d+: `,
      which must equal the ceiling `tests/orchestration/test_ci_budgets.py` freezes; the number
      of rows whose path lies under `.remedy-wt/`, counted rather than grepped; and the number
      of rows whose path ends `.py` under `.agent/`, which constraint 10 fixes at 0. Run it
      AFTER G6 has removed and pruned its worktree.

**G8 NOTHING ELSE MOVED.**

  (a) `.agent/STOP` exists on disk: report the boolean. `git status --porcelain | cat -A`:
      report it literally. `git worktree list`: report every entry and their number, which is
      1, the primary checkout alone.
  (b) The changed paths over `f8fbe3b6`..C5: report how many, and report MISSING and EXTRA
      against the Change section's path set MINUS `.agent/handoff.md`, both of which are empty.
      `.agent/handoff.md` is excluded by construction and not by choice: every gate of this
      round runs at C5 and C6 is the commit that writes that file, so a comparison including it
      is unmeetable for every possible round — the item 14 class, which cost round 72 a declared
      deviation. The reviewer measures that path at the next gate. Report the number of changed
      paths lying under `docs/`, `scripts/`, `packages/`, `apps/` or `tests/`, which is 0.
  (c) THE OPEN SET BY DISTINCT ID: every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
      line, computed at the base and at C5. Report registered, resolved and open at each end;
      the ids REGISTERED, RESOLVED and DE-REGISTERED, all three of which are empty; whether the
      open membership is IDENTICAL at both ends; the highest open id at each end; and whether
      `R-0880` is open at each end, which constraint 9 requires.

## Handback

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`. It carries the SESSION
NUMBER of the running feature, which is 26, and the round, which is 73. One line per gate with
its REAL_EXIT read out of its transcript file. A per-commit table in the `## Commits` section
docs/agents/handback_template.md mandates, whose `+/-` column is read from
`git show --numstat <sha>` and from no other source — that column is an INSERTION and DELETION
count, never a file's line count — and whose insertion cell for each of C0a through C5 is
compared against the number G4 reports for that same commit, cell by cell, with the comparison
stated. The item-status table covers every C and every G exactly once. State the context
self-assessment amend0905-throughput requires, in one sentence. Declare every deviation. F275
stands past the soft limit amend0908-f275-finish rule 1 names, so the handback carries the line
`SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE`, and the SCOPE REPORT that rule
obliges was written in round 51's handback and STANDS — do not restate it. Push after C6.

## SLICE PLAN73 — whole-file replacement of `.agent/plan.md`, applied at C1

BEGIN PLAN73 sha256=066674ceb976a34c83aac0b3465db174357b97b46c9c09c9c7ae92d8bc7c0320
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

ROUND 73 DISCHARGES DECISION F275 D45's PRECONDITION BY ITS SECOND ROUTE. RULE H widens the
owner check to receiver EXPRESSIONS and carries refusals 324 to 277, and the reading that
decides the round is that it finds ZERO new contradictions where round 72 found nine — the
resolver route is spent. So the residual is measured as a RISK instead: of the 324, 148 sit in
tests that break themselves, and all 176 production sites are EXECUTED by the suite, so the
unexecuted set is zero. A wrong rename at two of them reddens 46 and 1 tests, attributed by
name. DECISION F275 D47 rules the residual acceptable at that count and lets the flip proceed.

## Next Steps

1. Re-run the flip's dry run against the corrected inputs of rounds 67 and 69 together — the
   plain re-derivation and the re-keyed set — the first reading of what both corrections
   cost in FAILURES rather than in sites.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
3. THE FLIP, which D47 now permits, carrying D47's one obligation: the full suite is the
   backstop for the 277 the guard cannot decide, so it runs and is read.
4. Then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- THE FLIP'S BACKSTOP IS THE SUITE, AND ITS MARGIN VARIES. One probed site reddens 46 tests
  and another reddens 1; a residual site whose only witness is a single test is one deletion
  away from unguarded. Stated as a limitation inside D47, not absorbed and not given an id:
  nothing on disk is wrong, so amend0827-process-diet rule 2 spends none.
- A fresh worktree is NOT green: no `apps/ui/node_modules`, no built dist, ten failures
  before anything is mutated. Every colour taken there is a set difference against that.
- The open set is 87 by distinct id, with `R-0880` open. Four are High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN73

## SLICE RECORD73 — appended to `.agent/live_review.md` at C2

BEGIN RECORD73 sha256=38ed46b409d11853004b92f6a35fea0a80036d6078bc56cf2b824f3aebd16294
Gate: F275 R72 — the F275 round 72 entry. VERDICT PASS. Written by the planner and reviewer of session 26 after reading the committed range `ae84d89c`..`f8fbe3b6` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 73, per operator amendment amend0827-process-diet rule 1. The round shrank the owner check's refusal set from 999 to 324 and gated that widening by a per-site decision-map diff, which is the SHRINK half of the precondition DECISION F275 D45 put on the flip round.

WHAT THE TRANSPORT PROOF COVERS, STATED BEFORE THE FIGURES, per item 37 of §3. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback, and the chain it walks is the reviewer's own scratch original, the committed `.agent/authored/` blob and the working copy — three artefacts, of which the first is the reviewer's and the other two the worker's. It does not and cannot establish what bytes the worker RECEIVED, and no claim in this entry reaches that far. All four authored blobs are byte-identical to the reviewer's originals — the block at 34189 bytes, the artefact at 11207, the owner-check stage carrier at 19931 and the instrument carrier at 9089 — and `.agent/last_block.md` equals the block blob. Four slices matched the sha256 on their own BEGIN markers. Re-measured on the committed blob the block is 349 lines TOTAL and 277 PROSE, agreeing with its own constraint 8, and it carries zero lines that are a run of a single repeated character, which is item 37's other half. Both `.py.md` carriers round-trip through their own fence and re-wrapping each extracted source reproduces the committed blob byte for byte.

G2: `.agent/plan.md` byte-identical to PLAN72 at 3032 bytes over 49 lines against the cap of 50, both mandated headings exactly once. G3: `.agent/live_review.md` goes 1045796 to 1051368, `.agent/prose_slips.md` 267150 to 268101 and `.agent/decisions.md` 1180370 to 1186351, every one exact under reader A with the slice an exact suffix separated by one newline, reader B holding at N counted from the slice as 6, 1 and 6, and all three of the reviewer's own negative controls — each placed on the FIRST appended paragraph, per item 36 of §3 — REJECTED by both readers. Zero reserved-prefix lines after the entry header; the new header duplicates none of the 70 already matching the neighbours' pattern; `## DECISION F275 D46` reads 0 at the base against a highest existing D45. G4: the artefact at C5 is byte-identical to the C0b blob at 11207 bytes, the path does not resolve at the base, and every commit C0a through C5 stages exactly ONE path with insertions peaking at 431, under the DECISION F104 D1 cap of 500. G6: five top-level trees byte-identical, canary 42 passed at exit 0, `ruff check .` 26 rows at the frozen ceiling with zero rows under `.remedy-wt/` and zero `.py` rows under `.agent/`. G7: ten changed paths over the base with MISSING and EXTRA empty and zero production paths; the open set 87 at the base, at C5 and at the tip with IDENTICAL MEMBERSHIP, registered, resolved and de-registered ALL EMPTY, and `R-0880` open at each.

G5 CARRIED THE ROUND AND ITS DECISIVE READING IS A PAIR OF ZEROES. The instrument was re-run from the COMMITTED carriers, three times, to byte-identical 3957-byte captures with ZERO stderr at exit 0. Its anchor holds: the stage's `--narrow` mode reproduces the COMMITTED round 71 stage class for class and names the same four contradicted sites, so the comparison is against the artefact round 71 shipped. Against that anchor the widened stage carries CONFIRMED from 1195 to 1861 and REFUSED from 999 to 324, and the per-site decision maps say that of the 1199 sites round 71 DECIDED, the number round 72 no longer decides is ZERO and the number it decides DIFFERENTLY is ZERO, with the 675 that moved coming out of the refusal set alone. NINE contradicted sites the narrow method could not see are named, each REFUSED and never CONFIRMED by round 71, and the reviewer read all nine against the source: eight are `mission.id` standing in the mission argument of `link_job_to_mission` and one is `entry.id` on a `QueueEntry`. The artefact's 34 quoted lines verify with 0 failed and 0 unmatchable under the monotone matching, indices strictly increasing, and zero three-backtick lines.

THE SUBSTANCE IS THAT THE ROUND GATED ITS OWN IMPROVEMENT BY SOMETHING ITS IMPROVEMENT COULD NOT FAKE. A smaller refusal set is what the round was for, and is therefore the number least able to judge the round: two banners of counts cannot tell a site that changed its mind from two sites that swapped. The block ordered a PER-SITE map diff instead, and the round's own record shows why that mattered — a discarded draft passed every count-shaped check while destroying 327 correct decisions to buy 585 new ones, and only the per-site reading saw it. DECISION F275 D46 records both discarded drafts, including the one whose refusal set of 297 was the best-looking figure any version produced and the least sound.

THREE WORDING SLIPS OF THE REVIEWER'S, ALL SURFACED BY THE WORKER WITH MEASUREMENTS AND NONE OF THEM WRONG ON DISK. G7(b) ordered MISSING empty against the Change section's path set while every gate runs at C5 and C6 is the commit that writes `.agent/handoff.md`, so the literal reading has MISSING holding that one path — the item 14 class, a gate whose range cannot reach the handback commit, recurring one round after the same class cost round 71's G4. The artefact's provenance clause enumerated two kinds of non-instrument figure and the artefact carries a third and a fourth, a backtick-quoted COMMIT SHA and a SOURCE LINE, both correct and both outside the list that was written to cover them. And constraint 3's structural-review recipe said "one hunk header", which is true of a commit that CREATES a file and false of C0e, which replaces `.agent/last_block.md`. Three dated lines in `.agent/prose_slips.md` and no id, per amend0827-process-diet rule 2.
END RECORD73

## SLICE SLIPS73 — appended to `.agent/prose_slips.md` at C3

BEGIN SLIPS73 sha256=e95371d1bf688022f6e5c7065bce9cd175b72b045ba70e890711c8fe69f00023
2026-09-12 · F275 R72 · The round 72 block's G7(b) ordered the changed-path set compared against the Change section's list with "MISSING and EXTRA both empty", while every gate of that block runs at C5 and C6 is the commit that writes `.agent/handoff.md` — so the literal reading has MISSING holding exactly that path, for every possible round. This is item 14 of `docs/agents/planner_reviewer_prompt.md` §3 recurring one round after the same class cost round 71's G4: a gate whose RANGE cannot reach the handback commit. The worker reported both readings and reconciled neither, which is right, and nothing on disk is wrong. THE RULE THAT FOLLOWS: a gate that compares a measured path set against the block's own Change section names the paths the gate's own commit range can contain, and the handback path is excluded there and re-measured by the reviewer at the next gate — the same route item 31 already fixes for the handback commit's insertion counts.

2026-09-12 · F275 R72 · The round 72 artefact's provenance clause declared that every prose figure the instrument does not print is "a CITATION of a named decision, finding, section or specification" or "a figure of one of the TWO DISCARDED DRAFTS", and the artefact then correctly carried two figures of neither kind: the digits of a backtick-quoted COMMIT SHA (`ae84d89c`), and a SOURCE LINE number (`proposed_tasks.py` line 721). Both are sourced in the sentences that use them and the reviewer re-verified the second against the shipped stage, which does refuse that site — so nothing on disk is wrong and no figure is unexplained. The defect is that the clause enumerated the kinds it covers and got the enumeration short, which makes an honest gate report unexplained figures that are in fact explained. THE RULE THAT FOLLOWS: a provenance clause that enumerates KINDS is checked by running the round's own figure sweep against it before emission and widening the list until the sweep's residue is empty — the enumeration is a claim about the document and is measured like every other one, per item 11.

2026-09-12 · F275 R72 · The round 72 block's constraint 3 told the worker to review a large transport commit structurally, by "one path, one hunk header, every content line an addition, and the resulting blob byte-equal to its scratch original by sha256". That recipe describes a commit that CREATES a file. C0e replaces `.agent/last_block.md`, so its diff carries two hunk headers and removal lines, and the worker met the decisive half — byte-equality against the authored original — while declaring that the shape half did not describe its commit. Nothing on disk is wrong. THE RULE THAT FOLLOWS: a structural review recipe states the property that holds for the commit it is ordered over, and a whole-file REPLACEMENT is proved by byte-equality of the result alone, never by a hunk count, because the hunk count depends on how much of the old file the new one happens to share.
END SLIPS73

## SLICE DEC73 — appended to `.agent/decisions.md` at C4

BEGIN DEC73 sha256=a2933aadba0e6c14d014d49f58466c71e266979f5f9ecb913dcc06e5d834cfb9
## DECISION F275 D47 (2026-09-12, F275 round 73) — the owner check's residual is RULED ACCEPTABLE at the count it stands, because every site in it is reached by the suite, and the flip round is unblocked with the suite named as its backstop

CONTEXT. DECISION F275 D45 forbade the flip round to proceed until one of two things was true on the record: either the refusal set had been shrunk far enough that the guard's reach fairly approximates the ruled set, or the residual had been RULED ACCEPTABLE in a dated decision stating the count it accepts. Round 72 took the first route and carried the refusal set from 999 to 324 by seven ambiguity-refusing rules, finding nine contradicted sites on the way. This round establishes that the first route is spent and then takes the second.

CHOSEN. (1) RULE H SHIPS AND IT IS THE LAST RESOLVER RULE THIS FEATURE ADDS. Rules A through G all resolve a NAME, so the round 72 stage refused outright any receiver that was not a bare name — `job.tasks[0].id`, `result.job.id`, `load_job(...).id`. Rule H walks the receiver expression instead: an attribute against its owner's field annotation, a subscript against its container's element type, a call against the return table, refusing on ambiguity and bounding its recursion at a fixed depth. It carries refusals from 324 to 277 and is sound under the same per-site control round 72 used, diffed against the COMMITTED round 72 carrier: of the 1874 sites that stage decided, ZERO are now undecided and ZERO are decided differently. (2) THE READING THAT ENDS THE RESOLVER ROUTE IS THAT RULE H FINDS NOTHING. All 47 sites it newly decides are CONFIRMATIONS and the contradicted list is identical site for site, where round 72's widening found nine. A method whose additional reach returns only agreement has stopped being a defect detector, and a third resolver round would be cheap to write with no remaining reason to believe it would find anything. (3) THE RESIDUAL IS MEASURED AS A RISK RATHER THAN COUNTED AS A BLIND SPOT. Of the 324 the shipped guard refused, 148 are in test files, where a wrong rename breaks the very test containing it. The other 176 are production lines, and an instrumented run of the whole suite executes ALL 176 — the unexecuted set, which is the only set a ruling has to fear, measures ZERO. (4) IT IS DEMONSTRATED, NOT ARGUED. At two refused production sites, in a disposable worktree and against a control run under the same instrumentation, the attribute was renamed to one nothing defines — what a wrong guess by the flip looks like — and the suite produced 46 and 1 failures absent from the control, whose test ids name the mutated module in each case. (5) THE RESIDUAL IS THEREFORE RULED ACCEPTABLE AT 277 SITES UNDER RULE H, out of 2198 ruled. D45's precondition is DISCHARGED by its second route and the flip round may proceed.

THE LIMITATION THIS RULING STATES RATHER THAN HIDES. The margin varies by more than an order of magnitude: one probed site reddens 46 tests, the other exactly 1. A residual site whose only witness is a single test is one test deletion away from unguarded, and nothing in this decision prevents that deletion. It spends no finding id — nothing on disk is wrong and amend0827-process-diet rule 2 reserves an id for a defect with product effect — but the flip round inherits it as a reason to read the suite's result rather than only its exit code. `R-0880` STAYS OPEN: a ruling that the residual is survivable is not a claim that it is empty.

ALTERNATIVES CONSIDERED. A third resolver round was the obvious alternative and is what (2) rejects on its own measurement rather than on cost. Withholding the ruling until the guard decides every site was rejected because the remaining classes cannot be reached by binding rules at all — 113 receivers the shipped stage could not name and 104 annotated with something carrying no class identity, `Any` above all — so that condition is unreachable and would leave the flip blocked forever, which is the gate that cannot pass D45 itself warned about. Ruling the residual WITHOUT the coverage and mutation readings was rejected as the thing D45 was written to prevent: carrying the number forward silently is the one route D45 closed, and a ruling that states a count without stating what the count risks is that route wearing a date.

CONSEQUENCE. The flip round may take the flip, carrying one obligation: THE FULL SUITE IS THE BACKSTOP FOR THE 277 SITES THE GUARD CANNOT DECIDE, so the flip round runs it and reads its failures, not merely its exit code. That obligation is not new work — the integration gate already requires the suite twice per feature — but it is now load-bearing rather than routine, and a flip round that skipped it would be relying on a guard this decision has measured as silent on 277 sites. A fresh worktree is not green, so any colour taken in one is a set difference against a control run in that same worktree; ten failures were the baseline here, from absent `apps/ui/node_modules` and an unbuilt dist. Nothing here touches the id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse, which is production work no round has started.

HOW TO REVERSE. Delete this paragraph block; the flip is then blocked again by D45's precondition, which no other decision discharges. The round 72 stage remains recoverable from `.agent/authored/f275-r72-owner-stage.py.md` at commit `d60a0cd4`, and reversing Rule H specifically returns the refusal set to 324 without changing a single decision the round 72 stage made, which is what this round's own soundness control measures. Every figure above is re-derivable by the two committed instruments at this round's base.
END DEC73
