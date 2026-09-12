# STEP T003 — F275 ROUND 74 — repair round 73, and rule the residual on a reading that reproduces

## Goal

Repair the round 73 FAIL. Move the coverage reading out of a `git worktree`, where the
`ui_server` suite cannot run, into the PRIMARY CHECKOUT where it can; replace "is the line
executed" with "how many tests witness it"; red-prove every thin site against its own single
witness, mutating the ATTRIBUTE NODE the ruled set records rather than the first textual
match; and correct DECISION F275 D47 by APPENDING DECISION F275 D48, never by rewriting a
landed paragraph. Restore the three artefact gates round 73 dropped. Book the round 73 FAIL
verdict and its four prose slips. NO PRODUCTION LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r74.md`
- C0b save the artefact as authored text — `.agent/authored/f275-r74-artefact.md`
- C0c save the witness-instrument carrier — `.agent/authored/f275-r74-witness.py.md`
- C0d mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 74 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 73 reviewer verdict — `.agent/live_review.md`
- C3 append the round 73 prose slips — `.agent/prose_slips.md`
- C4 record DECISION F275 D48 — `.agent/decisions.md`
- C5 land the witness artefact — `.agent/f275_t003_witness_r74.md`
- C6 the round 74 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r74.md
    .agent/authored/f275-r74-artefact.md
    .agent/authored/f275-r74-witness.py.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/decisions.md
    .agent/f275_t003_witness_r74.md
    .agent/handoff.md

No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` is touched. This is not a
deletion round and no file is removed. NOTHING LANDED BY ROUND 73 IS REWRITTEN OR REVERTED:
DECISION F275 D47 stays exactly as it is on disk and is corrected by the append at C4.

## The reviewer's texts on disk, and how they travel

Every reviewer-authored text of this round exists as a file under the gitignored `.remedy-wt/`
at this round's base, and each is of one of two kinds. A SLICE is carried verbatim in this
block between a BEGIN and an END marker, the BEGIN marker stating the sha256 of the bytes
between them; the slices are PLAN74, RECORD74, SLIPS74 and DEC74, each under its own heading
below. A WHOLE TEXT is too long to retype and is never retyped: it is transported with
`shutil.copyfile` and never opened in an editor. The whole texts, with their scratch paths and
digests:

    .remedy-wt/f275-r74-artefact.md        9578 bytes  c914420ef60576b0429a87a20cfc38d30acbc06c0851c74628dbfa28f23228c2
    .remedy-wt/f275-r74-witness.py.md     12539 bytes  1ae814a0af76fff846f936ebf7844484f7cf039dddf3717ed841eaf4a4297806

The block travels the same way: read `.remedy-wt/f275-r74.block.md` from disk, verify its
sha256 against the one the delegation wrapper states, and copy it to `.agent/authored/f275-r74.md`
at C0a and to `.agent/last_block.md` at C0d. A slice is applied BYTE FOR BYTE: nothing is
reflowed, re-wrapped, re-indented or corrected, and a slice that looks wrong is APPLIED AS
WRITTEN and declared in the handback.

## Constraints

1. APPLY EVERY SLICE VERBATIM. Extract each by its BEGIN and END marker prefixes, markers
   EXCLUDED, from the COMMITTED C0a blob — never from the delegation prompt and never from
   memory — and check each against the sha256 its own BEGIN marker carries before applying it.
2. PLAN74 is a WHOLE-FILE REPLACEMENT of `.agent/plan.md`. RECORD74, SLIPS74 and DEC74 are
   APPENDS: the pre-commit blob is a byte-exact PREFIX of the post-commit file and the slice
   is an exact SUFFIX of it, separated by exactly one newline.
3. ONE PATH PER COMMIT, in the Bundle's order. Run the AGENTS.md self-review loop before every
   commit: `git diff --cached --stat`, `--numstat` and the full `git diff --cached`. Where a
   commit's diff is a single large blob, the decisive check is BYTE-EQUALITY of the resulting
   blob against its scratch original by sha256, and that is what the handback reports; no hunk
   count is ordered, because it depends on how much of the old file the new one shares and
   C0d REPLACES `.agent/last_block.md`.
4. NO PRODUCTION PATH MOVES. The mutations G5 orders happen inside a worktree and are reverted
   by the instrument itself, which reports the byte-equality of every revert. If any gate would
   require editing a tracked file under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`,
   STOP and hand back instead.
5. THE COVERAGE RUN HAPPENS IN THE PRIMARY CHECKOUT AND THAT IS DELIBERATE. It writes no
   tracked file — `.coverage` is gitignored — and the instrument reports
   `git status --porcelain` immediately after it. Every MUTATION still happens inside a
   disposable worktree under the gitignored `.remedy-wt/`, which the instrument creates and
   removes. `git status --porcelain` is the empty string at every commit and at the handback.
6. NO `gh` COMMAND AND NO `remedy` CLI COMMAND IS RUN. No pull request is created, edited or
   merged. No branch is created. No merge. No force-push. Push the branch after C6.
7. READ `.agent/STOP` FROM DISK before the first commit and again before C6, by BOTH
   `os.path.exists` and `glob`, and report both readings literally in the handback. If it
   exists, finish the commit in hand, write the handback and stop.
8. THIS BLOCK'S OWN SIZE. Measured by the reviewer on the FINAL bytes of
   `.remedy-wt/f275-r74.block.md`: TOTAL 382 lines, PROSE 299 lines, where PROSE is TOTAL
   minus the lines lying between BEGIN and END markers, markers themselves counted as PROSE.
   This clause is the ONLY place either numeral appears; G1 names this clause rather than
   restating them.
9. `R-0880` STAYS OPEN. No finding id is registered, resolved or de-registered this round. Do
   not write a `Done:` or a `Landed:` paragraph of your own; `Done:` is reviewer-authored text
   only. The SLIPS74 lines are not ids, per amend0827-process-diet rule 2.
10. NO `.py` FILE IS CREATED ANYWHERE UNDER `.agent/`. The instrument ships as a `.py.md`
    carrier, because a `.py` file inside the tree is counted by the `ruff` ceiling that
    `tests/orchestration/test_ci_budgets.py` freezes and G6(c) reads.
11. EVERY GATE IS RUN AS `bash -c '<cmd> > <out> 2>&1; echo "REAL_EXIT=$?" >> <out>'` AND THE
    EXIT CODE IS READ BACK OUT OF THE FILE. Write transcripts under `.remedy-wt/`. "Green" as
    a word is a finding; the recorded number is the evidence.
12. THE INSTRUMENT'S ONLY SCRATCH INPUTS ARE THE TWO RULED-SET FILES, AND NEITHER IS
    REGENERATED. `.remedy-wt/r69_rekeyed.json` (121516 bytes, sha256
    489fdf8eeb9c4e66b452510de5d362e5d701b4cfe2de79d1d69b768f526d301f) and
    `.remedy-wt/r69_rekeyed_owners.json` (121858 bytes, sha256
    747e8f08c7e3dfc207510a0071d1fd196907ca34667d97baec7ab5028145f57f) must exist with those
    digests; if either is missing or differs, STOP and hand back, and do not rebuild it.
    EVERYTHING ELSE THE INSTRUMENT NEEDS IT DERIVES ITSELF from the committed carrier at
    `78e5c18c:.agent/authored/f275-r73-owner-stage.py.md`, which is the Rule H stage round 73
    landed — it extracts that stage and runs it to obtain the SHIPPED guard's own refusal set,
    rather than reading a decision map an earlier round left in scratch. Section 0 of its
    output reports the extraction and the stage's whole banner.
13. NO GATE BELOW DEMANDS THAT A WHOLE-SUITE RUN BE GREEN, and that is the repair of round
    73's third defect rather than an oversight. This suite carries at least three
    environment-sensitive tests — a wall-clock perf budget and a workspace-identity pair —
    each observed red in one invocation, green in the next, and passing in isolation. The
    readings this round turns on are DIFFERENCES between two runs of the same selection, never
    the colour of one run over everything.
14. G5 RUNS THE FULL SUITE ONCE, UNDER COVERAGE, AND THAT TAKES ROUGHLY FOUR MINUTES. The
    eleven red-proofs after it run ONE TEST each and are fast. That is the gate, not an
    overrun: do not shorten it, do not deselect, and do not substitute a scoped run for the
    coverage pass.
15. THIS BLOCK CONTAINS NO LINE THAT IS A RUN OF A SINGLE REPEATED CHARACTER. G1 counts them
    and the expected count is zero, per item 37 of `docs/agents/planner_reviewer_prompt.md` §3.

## Done when — the gates below, all run at C5 before C6 exists

Every gate runs at C5, which is strictly earlier than the commit that writes the handback, so
the handback can quote every reading it states. The handback commit's own numbers are NOT a
gate of this round: the reviewer measures them at the next gate.

**G1 TRANSPORT, THE BLOCK BUDGET, AND THE INSERTION CAP.** For each of the four blobs C0a
through C0d commits, compare the committed bytes against the reviewer's scratch original by
size and sha256 and report EQUAL or not, naming the commit. `.agent/last_block.md` at C0d is
compared against the COMMITTED C0a blob. Then, over the committed C0a blob: extract every
BEGIN/END slice, report the CARDINALITY YOU MEASURED — the block states no numeral for it —
and for each slice its byte size, its line count and whether its content matches the sha256 on
its own BEGIN marker. Re-measure TOTAL and PROSE as constraint 8 defines them, report both
numbers you measured, and report whether each equals the numeral constraint 8 states for it.
Report the count of lines in that blob that consist of a single character repeated, which
constraint 15 fixes at zero. REPORT THE LINE COUNT OF EVERY BLOB THIS ROUND CREATES against
500, the DECISION F104 D1 insertion cap — for a file the commit CREATES the two are the same
number, and round 73 landed a 529-line carrier because nobody counted one. Finally, for the
`.py.md` carrier: report the number of ```python fence lines and of bare ``` lines, both of
which must be 1; extract the source; and confirm that re-wrapping it in the carrier's own
header and fence reproduces the committed blob BYTE FOR BYTE.

**G2 THE PLAN.** `.agent/plan.md` at C1 is byte-identical to slice PLAN74 — report both sizes
and both sha256 values. Report its line count against the AGENTS.md cap of 50, and the count of
lines matching `^## Goal$` and of lines matching `^## Next Steps$`, both of which are 1.

**G3 THE RECORD.** Three appends, three commits, and for each one TWO INDEPENDENT READERS and
a NEGATIVE CONTROL. Wherever a reading below is taken AT THE BASE, read those bytes with
`git show 0d47205d:<path>` into scratch or into memory; nothing is written over a tracked file
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
  (iv) Over RECORD74: report its line count, the number of lines AFTER THE FIRST carrying a
       reserved prefix (`- R-`, `Done: R-`, `Landed: R-`, `Gate: `), which is 0, and the number
       of lines C2 ADDS matching `^- R-` and matching `^Done: R-`, both of which are 0.
  (v)  RECORD74's first line joins a repeating record format, so compare it MECHANICALLY
       against its neighbours: report how many lines at the base already match
       `^Gate: F275 R\d+ — the F275 round \d+ entry\.`, whether the new first line matches that
       same pattern, and whether it duplicates any of them.
  (vi) Over DEC74: confirm it begins `## DECISION F275 D48 `, report how many lines at the base
       match `^## DECISION F275 D48` (which is 0), and report the highest existing
       `^## DECISION F275 D\d+` at the base. Then confirm that C4 REMOVES NO LINE — that its
       `git show --numstat` deletion column is 0 — which is what makes this a correction by
       append rather than a rewrite of DECISION F275 D47.
  (vii) Over SLIPS74: report the number of paragraphs it adds, how many begin
       `2026-09-12 · F275 R73 · `, and how many lines at the base already begin with that exact
       prefix.

**G4 THE ARTEFACT, AND THE THREE CHECKS ROUND 73 DROPPED.**

  (a) `.agent/f275_t003_witness_r74.md` at C5 is byte-identical to the C0b blob — report both
      sizes and both sha256 values — and the path does not resolve at the base with
      `git show 0d47205d:.agent/f275_t003_witness_r74.md`, whose non-zero exit is the expected
      reading.
  (b) THE TRANSCRIPT. In the C0b artefact blob, report the number of lines consisting of three
      backticks, which is 0; then check EVERY line that begins with whitespace and is not blank
      against the instrument's output from G5, reporting how many you checked and how many have
      no stripped-equal line in that output. Any line with no match is a RED gate.
  (c) THE ORDER PROPERTY as a MONOTONE MATCHING over those same quoted lines: report how many
      matched in order, how many were unmatchable, whether every quoted line matched, and
      whether the matched indices strictly increase.
  (d) THE FIGURES: sweep every maximal digit run over the artefact's PROSE — its lines that do
      NOT begin with whitespace — reading the artefact AS A WHOLE rather than line by line.
      Report how many runs you swept, how many occur as a digit run in the instrument's output,
      and how many do not. For each that does not, report it with the line that uses it and say
      which of the artefact's two declared kinds it is: a CITATION of a named decision, finding,
      round, section, commit or source line, or a READING THE REVIEWER TOOK OUTSIDE THIS
      INSTRUMENT. The artefact's provenance clause declares exactly those two and no third.
  (e) NO LINE QUOTED IN THE ARTEFACT CARRIES A WALL-CLOCK DURATION: report the count of quoted
      lines matching `in \d+\.\d+s`, which is 0. This is the round 73 defect stated as a gate.
  (f) Report, for EVERY commit C0a through C5, the INSERTION count from `git show --numstat
      <sha>` — the `+` column DECISION F104 D1 caps at 500 — with the number of paths that
      commit stages, which is 1 for each, and whether each insertion count is under 500.

**G5 THE INSTRUMENT.** Read constraints 12, 13 and 14 before starting this one.

  (a) Extract the single fence of the COMMITTED C0c carrier to `.remedy-wt/f275-r74-witness.py`
      and report the extracted size and sha256.
  (b) Run `python3 -B .remedy-wt/f275-r74-witness.py . 0d47205d` and REPRODUCE EVERY LINE OF
      EVERY BANNER in the handback.
  (c) THE READINGS THIS GATE TURNS ON, each reported with whether it holds: in section 2, that
      `git status --porcelain` is the empty string AFTER the coverage run, which is what makes
      running it in the primary checkout legal; in section 4, that the risk set — refused sites
      witnessed by NO test — is 0; in section 5, that every thin site's control is green and its
      mutation red, that the summary reads as many proved as the thin set holds, and that every
      mutated file reverted byte-identically. A thin site whose control is not green, or whose
      mutation is not red, or whose revert is not byte-identical, is a RED gate: stop and hand
      back. THE COLOUR OF SECTION 2's OWN SUITE RUN IS NOT A READING and is not a red condition,
      per constraint 13.
  (d) Report `git status --porcelain` and `git worktree list` AFTER this gate.

**G6 THE TREE DID NOT MOVE.**

  (a) Report the `git rev-parse` object id of `packages`, `apps`, `tests`, `docs` and `scripts`
      at the base `0d47205d` and at C5, and whether each pair is EQUAL. This is the gate that
      proves G5's eleven mutations left nothing behind.
  (b) THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`, reporting the tail of
      its output and its real exit code.
  (c) `python3 -m ruff check . --output-format concise`. Its exit is 1 whenever any finding
      remains, so THE GATE IS THE COUNT: report the number of rows matching `^\S+:\d+:\d+: `,
      which must equal the ceiling `tests/orchestration/test_ci_budgets.py` freezes; the number
      of rows whose path lies under `.remedy-wt/`, counted rather than grepped; and the number
      of rows whose path ends `.py` under `.agent/`, which constraint 10 fixes at 0. Run it
      AFTER G5 has removed and pruned its worktree.

**G7 NOTHING ELSE MOVED.**

  (a) `.agent/STOP` exists on disk: report the boolean. `git status --porcelain | cat -A`:
      report it literally. `git worktree list`: report every entry and their number, which is
      1, the primary checkout alone.
  (b) The changed paths over `0d47205d`..C5: report how many, and report MISSING and EXTRA
      against the Change section's path set MINUS `.agent/handoff.md`, both of which are empty.
      That path is excluded by construction: every gate runs at C5 and C6 writes it, so a
      comparison including it is unmeetable for every possible round, and the reviewer measures
      it at the next gate. Report the number of changed paths lying under `docs/`, `scripts/`,
      `packages/`, `apps/` or `tests/`, which is 0.
  (c) THE OPEN SET BY DISTINCT ID: every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
      line, computed at the base and at C5. Report registered, resolved and open at each end;
      the ids REGISTERED, RESOLVED and DE-REGISTERED, all three of which are empty; whether the
      open membership is IDENTICAL at both ends; the highest open id at each end; and whether
      `R-0880` is open at each end, which constraint 9 requires.

## Handback

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`. It carries the SESSION
NUMBER of the running feature, which is 26, and the round, which is 74. One line per gate with
its REAL_EXIT read out of its transcript file. A per-commit table in the `## Commits` section
docs/agents/handback_template.md mandates, whose `+/-` column is read from
`git show --numstat <sha>` and from no other source — that column is an INSERTION and DELETION
count, never a file's line count — and whose insertion cell for each of C0a through C5 is
compared against the number G4(f) reports for that same commit, cell by cell, with the
comparison stated. The item-status table covers every C and every G exactly once. State the
context self-assessment amend0905-throughput requires, in one sentence. Declare every
deviation. F275 stands past the soft limit amend0908-f275-finish rule 1 names, so the handback
carries the line `SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE`, and the SCOPE
REPORT that rule obliges was written in round 51's handback and STANDS — do not restate it.
Push after C6.

## SLICE PLAN74 — whole-file replacement of `.agent/plan.md`, applied at C1

BEGIN PLAN74 sha256=38f8dd5538b9a33806e0119d1f8d7aa069c4a17da7fd2329e7da99054240f23c
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

ROUND 74 REPAIRS ROUND 73, WHICH FAILED. D47 discharged D45's precondition on a coverage
reading taken inside a fresh worktree; re-run there it gives 23 unexecuted rather than 0,
because a worktree has no built UI dist. The reading moves to the PRIMARY CHECKOUT, where the
suite runs, and the question sharpens from "is the line executed" to "how many tests witness
it": zero for none, exactly one for eleven, a median of seventeen, over 7065 site-and-test
pairs. Each of the eleven thin sites is red-proved against its own single witness, mutating
the ATTRIBUTE NODE the ruled set records rather than the first textual match. DECISION F275
D48 corrects D47 by appending, never by rewriting.

## Next Steps

1. Re-run the flip's dry run against the corrected inputs of rounds 67 and 69 together — the
   plain re-derivation and the re-keyed set — the first reading of what both corrections
   cost in FAILURES rather than in sites.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
3. THE FLIP, which D48 permits on D47's corrected footing, carrying D48's obligations: the
   full suite is the backstop, and the eleven thin sites are named rather than averaged.
4. Then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- A MEASUREMENT TAKEN IN A WORKTREE IS A MEASUREMENT OF THAT WORKTREE. The UI dist and
  `node_modules` are absent there, so any suite-wide reading taken in one is about the
  environment. Round 73 shipped a decision on such a reading.
- THE SUITE HAS ENVIRONMENT-SENSITIVE TESTS. A perf budget and a workspace-identity pair go
  red or green by load under coverage, and pass in isolation. No gate may demand a green
  full-suite run as its pass condition.
- The open set is 87 by distinct id, with `R-0880` open. Four are High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN74

## SLICE RECORD74 — appended to `.agent/live_review.md` at C2

BEGIN RECORD74 sha256=33273af4a01f491a2f669cc570660bcb6fddb7f5ffc5a69719b701f0aa553920
Gate: F275 R73 — the F275 round 73 entry. VERDICT FAIL. Written by the planner and reviewer of session 26 after reading the committed range `f8fbe3b6`..`0d47205d` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 74, per operator amendment amend0827-process-diet rule 1. EVERY DEFECT BELOW IS THE REVIEWER'S. The worker followed the block exactly, landed all twelve commits in order, stopped where the block told it to stop, and surfaced four of the five defects itself with measurements; nothing it did contributed to this verdict.

WHAT THE TRANSPORT PROOF COVERS, STATED BEFORE THE FIGURES, per item 37 of §3. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback, and the chain it walks is the reviewer's own scratch original, the committed `.agent/authored/` blob and the working copy — three artefacts, of which the first is the reviewer's and the other two the worker's. It does not and cannot establish what bytes the worker RECEIVED. All five authored blobs are byte-identical to the reviewer's originals — the block at 36880 bytes, the artefact at 12291, the owner-check stage carrier at 24929, instrument A's carrier at 8095 and instrument B's at 8661 — and `.agent/last_block.md` equals the block blob. Four slices matched the sha256 on their own BEGIN markers, the block re-measures at 362 lines TOTAL and 286 PROSE as its constraint 8 states, it carries zero repeated-character lines, and all three `.py.md` carriers round-trip through their own fence byte for byte.

WHAT WAS RIGHT, AND IT IS MOST OF THE ROUND. G2: `.agent/plan.md` byte-identical to PLAN73 at 2837 bytes over 47 lines. G3: the three appends each exact under reader A with the slice an exact suffix after one newline, reader B holding at N counted from the slice as 6, 3 and 7, and all three of the reviewer's negative controls on the FIRST appended paragraph REJECTED by both readers. G4: the artefact byte-identical to the C0b blob and absent at the base. G8: eleven changed paths with MISSING and EXTRA empty and zero production paths, the open set 87 with identical membership at the base, at C5 and at the tip, and `R-0880` open at each. G5 reproduced in full from the committed carriers: `--narrow` still equals the round 71 figures class for class, the shipped stage's 1874 decisions are ZERO undecided and ZERO different under Rule H, the contradicted site lists are identical, and 47 sites move out of the blind spot as confirmations. Every substantive numeral of the round reproduced.

THE FIRST DEFECT IS THAT THE ARTEFACT QUOTES OUTPUT THAT DOES NOT REPRODUCE. Nine of its fifty-one quoted lines have no stripped-equal line in the worker's own run of the same instrument, and one of the nine — `18416 passed, 23 skipped, 1 warning in 222.78s (0:03:42)` — carries a WALL-CLOCK DURATION and therefore cannot reproduce in any run by any worker on any machine. A document whose evidentiary claim is "these are verbatim excerpts" is false for those nine lines. This is the class that cost round 69 a FAIL, arriving through a quoted duration rather than a stale blob.

THE SECOND DEFECT IS WHY NOTHING CAUGHT THE FIRST. Round 72's block ordered the artefact's every indented line checked against the instrument's output, the matching checked as monotone, and every prose figure swept and classified. Round 73's block ordered none of those three. The gate that would have seen the defect was dropped by the reviewer between one round and the next, on the same branch, for an artefact of the same kind.

THE THIRD DEFECT IS A GATE THAT CANNOT RELIABLY PASS. G6(b) made a GREEN control run a pass condition, while the same block's PLAN73 risk bullet, its DEC73 CONSEQUENCE paragraph and instrument B's own docstring all state that a fresh worktree is NOT green and that its failures are SUBTRACTED rather than required to be absent. The control went red on one wall-clock perf test that the round's own artefact names as load-sensitive, so the worker stopped, as ordered, on a gate the block contradicted three times over. Item 33 of §3 names this shape and DECISION F275 D45 named it in this very feature.

THE FOURTH DEFECT IS THAT THE MEASUREMENT ITSELF DOES NOT REPRODUCE, AND IT IS THE ONE THAT MATTERS. Re-run by the reviewer at this round's base, round 73's instrument B read 23 refused production sites UNEXECUTED and 126 control failures, where the round's own run read 0 and 0. A `git worktree` carries no `apps/ui/node_modules` and no built dist, so the `ui_server` suite fails there and never reaches the `ui_server` lines; round 73's worktree had been warmed by an earlier invocation and the next was not. DECISION F275 D47 discharged DECISION F275 D45's precondition on the reading that moved. A measurement taken in an environment the suite cannot run in is a measurement of that environment.

THE FIFTH IS THAT C0c LANDED AT 529 INSERTIONS, over AGENTS.md's 500-line cap, because the reviewer authored a 529-line carrier and never counted it. The worker declared it with an inseparability reason and MEASURED that it is the only such commit in F275 — of 603 commits since the fork point, five exceed 500, two being `main` merges and three being `.agent/handoff.md` rewrites that DECISION F104 D1 exempts entirely — so the once-per-feature exception AGENTS.md's Commit Discipline allows is correctly invoked and is now SPENT for this feature. That is the honest disposition: the commit stands, and no second oversize commit may be declared in F275.

LAST_REVIEWED_SHA DOES NOT ADVANCE. Round 74 is the repair: it moves the coverage reading to the primary checkout, replaces "is the line executed" with "how many tests witness it", red-proves every thin site against its own witness, restores the artefact transcript and figure gates, and corrects D47 by appending DECISION F275 D48 rather than by rewriting a landed paragraph. No finding id is minted: every defect above sits in `.agent/` prose or in a reviewer-authored gate, and amend0827-process-diet rule 2 reserves an id for a defect with product effect on disk.
END RECORD74

## SLICE SLIPS74 — appended to `.agent/prose_slips.md` at C3

BEGIN SLIPS74 sha256=a9caa25d73b203073868cb4b58bbd44031437bbf7d3ed2046bd7cb472d812471
2026-09-12 · F275 R73 · The round 73 artefact quoted a pytest summary line — `18416 passed, 23 skipped, 1 warning in 222.78s (0:03:42)` — into a document whose provenance clause claims every indented line is a verbatim excerpt of an instrument's output. That line carries a WALL-CLOCK DURATION, so it cannot reproduce in any run, on any machine, ever; nine of the artefact's fifty-one quoted lines failed to reproduce in the worker's own execution and this one is unreproducible by construction. THE RULE THAT FOLLOWS: an instrument that feeds a quoted artefact returns the REPRODUCIBLE part of a tool's output and never the tool's own summary line — parse the counts out and print those — because a duration, a timestamp, a temporary path and a process id are all of that class, and a document that quotes one has made a claim no gate can ever satisfy.

2026-09-12 · F275 R73 · The round 72 block ordered three checks over its artefact — every indented line checked against the instrument's output, the matching checked as MONOTONE, and every prose figure swept and classified against a declared list of kinds — and the round 73 block, on the same branch and for an artefact of the same kind, ordered none of them. The defect above was therefore invisible to every gate the round ran, and the worker reported eight deviations without being able to see it. THE RULE THAT FOLLOWS: the gate set of a round that ships an artefact of a kind already shipped is DIFFED against the gate set of the round that shipped the last one, and any gate dropped is either restored or the block says why in its own text. A gate that exists only in a previous block is a gate that protects only a previous round.

2026-09-12 · F275 R73 · The round 73 block's G6(b) made a GREEN full-suite control run a pass condition and a non-green control an explicit RED, while the same block's PLAN73 risk bullet, its DEC73 CONSEQUENCE paragraph and instrument B's own docstring all stated that a fresh worktree is NOT green and that its failures are SUBTRACTED rather than required to be absent. The control went red on a single wall-clock perf test that the round's own artefact names as load-sensitive, and the worker stopped on a gate its own block contradicted three times over. Item 33 of `docs/agents/planner_reviewer_prompt.md` §3 names this shape, and DECISION F275 D45 named it inside this very feature two rounds earlier. THE RULE THAT FOLLOWS: a gate over a whole-suite run asserts a property of the DIFFERENCE between two runs, never the colour of one of them, because a suite with any environment-sensitive test has no colour that a gate can demand — and this suite has at least three, a perf budget and a workspace-identity pair, each observed red in one invocation, green in the next, and passing in isolation.

2026-09-12 · F275 R73 · The round 73 block ordered a carrier the reviewer had authored at 529 lines into a single commit, under AGENTS.md's Commit Discipline cap of 500 INSERTIONS, and the reviewer never counted it: the block's own G4 orders every commit's insertions reported "under 500" and C0c could not meet it. The worker declared the overage with an inseparability reason and measured that it is the only such commit in F275, so the once-per-feature exception is correctly invoked and is now SPENT. THE RULE THAT FOLLOWS: every authored blob a block orders into a commit is counted in LINES against the 500-insertion cap at emission, in the same sweep that counts the block itself, because a new file's line count IS its commit's insertion count and the reviewer already has the bytes on disk.
END SLIPS74

## SLICE DEC74 — appended to `.agent/decisions.md` at C4

BEGIN DEC74 sha256=248674db62844db80efd1cecd635bfb1560fbb11f6b96ee02dbdfad225725482
## DECISION F275 D48 (2026-09-12, F275 round 74) — DECISION F275 D47 rested on a reading that does not reproduce, and is CORRECTED by appending rather than rewritten; the residual is ruled acceptable again, on a witness measurement taken where the suite actually runs

CONTEXT, AND IT IS A CORRECTION. DECISION F275 D47 discharged DECISION F275 D45's precondition on the flip round by measuring that all 176 refused production sites are executed by the suite and that the unexecuted set is zero. That measurement was taken inside a fresh `git worktree`. Re-run by the reviewer at this round's base, the identical instrument in the identical kind of worktree reads 23 sites UNEXECUTED and 126 control failures: a worktree carries no `apps/ui/node_modules` and no built dist, so the `ui_server` suite fails there and never reaches the `ui_server` lines, and round 73's worktree had been warmed by an earlier invocation while the next one was not. D47's central reading is therefore a property of an environment rather than of the tree. D47 IS NOT REWRITTEN — the record is append-only and a dated correction is how it stays honest — and this decision supersedes its CHOSEN paragraph (3) and its discharge of D45.

CHOSEN. (1) THE COVERAGE READING MOVES TO THE PRIMARY CHECKOUT, where the suite actually runs. This is not a guardrail violation: `docs/agents/self_drive_protocol.md` G5 isolates DESTRUCTIVE verification, and a coverage run writes no tracked file — `.coverage` is gitignored and the instrument reports `git status --porcelain` afterwards to prove it. Mutations still happen only inside a disposable worktree. (2) THE QUESTION IS SHARPENED FROM EXECUTION TO WITNESS. "Is the line executed" cannot distinguish a site one test reaches from a site forty tests reach, and D47 could only name that difference as an unmeasured caveat after spot-checking two sites. Coverage records WHICH test executed each line, so the reading is now a distribution over all 176 at once: ZERO sites are witnessed by no test, ELEVEN by exactly one, 58 by two to nine and 98 by ten or more, at a median of seventeen and 7065 site-and-test pairs in total. (3) EVERY THIN SITE IS RED-PROVED INDIVIDUALLY rather than averaged into a reassurance. Each of the eleven has its single witness run unmutated in a worktree and then run again with the flip's own rename applied to that exact site: eleven controls green, eleven mutations red, every file reverted byte-identically. (4) THE PROBE MUTATES THE ATTRIBUTE NODE, NOT THE FIRST TEXTUAL MATCH, and this is recorded because a draft got it wrong: at `packages/orchestration/verifier.py` the first textual `.id` on the ruled line sits inside an f-string LITERAL, so a naive replace edited a message rather than an attribute access, the witness stayed green, and the site read as the one unguarded member of the thin set. Located instead by the line, the byte column and the attribute name the ruled set already records, the reading goes from 10 of 11 to 11 of 11. (5) THE RESIDUAL IS RULED ACCEPTABLE at 277 sites under Rule H, on this footing rather than D47's.

WHAT THIS RULING NOW OBLIGES THE FLIP ROUND TO DO, AND IT IS MORE THAN D47 ASKED. The full suite remains the backstop and must be read for its failures rather than its exit code. In addition, THE ELEVEN THIN SITES ARE CARRIED BY NAME into the flip round rather than as a percentage: a witness set of size one is a fact about today's suite, not a property of the code, so the flip round re-derives the thin set before it flips and treats any site that has dropped to zero witnesses as a stop. Nothing in this decision claims the residual is empty; `R-0880` STAYS OPEN and the guard is still silent on all 277.

ALTERNATIVES CONSIDERED. Rewriting D47 was rejected outright — the record is append-only, item 20 of `docs/agents/planner_reviewer_prompt.md` §3 forbids repairing a landed sentence, and a dated correction beside a wrong paragraph is worth more to a later reader than a clean paragraph with no history. Re-taking the round 73 measurement in a worktree made usable, by copying `apps/ui/node_modules` in with symlinks preserved, was considered and rejected as the more expensive way to a weaker answer: 305 MB and 44839 entries per run, to reproduce an environment the primary checkout already is. Withholding any ruling until the guard decides every site was rejected for the reason D45 itself gave — the remaining classes cannot be reached by binding rules, so that condition is unreachable and would block the flip forever.

HOW TO REVERSE. Delete this paragraph block; D47 then stands alone, and with it the reading this decision has shown does not reproduce, so the flip would be proceeding on an environment's accident. Every figure above is re-derivable by the committed instrument `.agent/authored/f275-r74-witness.py.md` at this round's base, except the two this decision explicitly attributes elsewhere: the 23 and the 126 come from the reviewer's re-run of round 73's own instrument, and the 10 of 11 comes from the discarded draft described in CHOSEN (4).
END DEC74
