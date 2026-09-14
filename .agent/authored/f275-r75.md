# STEP T003 — F275 ROUND 75 — a SITE is not a LINE, and DECISION F275 D48 is corrected

## Goal

Correct the three descriptive numerals DECISION F275 D48 carries and the unit confusion behind
them, which the round 74 worker found by adding a banner's own buckets up. Coverage resolves a
context per LINE; the ruled set is keyed per SITE, and nine refused production sites share a
line with another, so round 74's instrument counted sites in one section and lines in the next
under the same word. This edition prints the unit on every count and prints both bucket sums
beside the totals they partition. DECISION F275 D49 records the corrected figures by
APPENDING; D48 is not rewritten and its ruling is unchanged, because the two readings it rests
on — an empty risk set and a thin set of eleven — are the same in both units. Book the round 74
PASS verdict and its two prose slips. NO PRODUCTION LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r75.md`
- C0b save the artefact as authored text — `.agent/authored/f275-r75-artefact.md`
- C0c save the witness-instrument carrier — `.agent/authored/f275-r75-witness.py.md`
- C0d mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 75 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 74 reviewer verdict — `.agent/live_review.md`
- C3 append the round 74 prose slips — `.agent/prose_slips.md`
- C4 record DECISION F275 D49 — `.agent/decisions.md`
- C5 land the units artefact — `.agent/f275_t003_units_r75.md`
- C6 the round 75 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r75.md
    .agent/authored/f275-r75-artefact.md
    .agent/authored/f275-r75-witness.py.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/decisions.md
    .agent/f275_t003_units_r75.md
    .agent/handoff.md

No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` is touched. This is not a
deletion round and no file is removed. NOTHING LANDED BY ROUND 74 IS REWRITTEN OR REVERTED:
DECISION F275 D48 stays exactly as it is on disk and is corrected by the append at C4.

## The reviewer's texts on disk, and how they travel

Every reviewer-authored text of this round exists as a file under the gitignored `.remedy-wt/`
at this round's base, and each is of one of two kinds. A SLICE is carried verbatim in this
block between a BEGIN and an END marker, the BEGIN marker stating the sha256 of the bytes
between them; the slices are PLAN75, RECORD75, SLIPS75 and DEC75, each under its own heading
below. A WHOLE TEXT is too long to retype and is never retyped: it is transported with
`shutil.copyfile` and never opened in an editor. The whole texts, with their scratch paths and
digests:

    .remedy-wt/f275-r75-artefact.md         4739 bytes  0e2078f5c5e7907bc39149d968d0b35c0186ba4b819f0819795958eaa619852e
    .remedy-wt/f275-r75-witness.py.md     14692 bytes  fa7a54de28e31875c13bac66f7308596f18bfb73d0d11bbaad164bd918d73529

The block travels the same way: read `.remedy-wt/f275-r75.block.md` from disk, verify its
sha256 against the one the delegation wrapper states, and copy it to `.agent/authored/f275-r75.md`
at C0a and to `.agent/last_block.md` at C0d. A slice is applied BYTE FOR BYTE: nothing is
reflowed, re-wrapped, re-indented or corrected, and a slice that looks wrong is APPLIED AS
WRITTEN and declared in the handback.

## Constraints

1. APPLY EVERY SLICE VERBATIM. Extract each by its BEGIN and END marker prefixes, markers
   EXCLUDED, from the COMMITTED C0a blob — never from the delegation prompt and never from
   memory — and check each against the sha256 its own BEGIN marker carries before applying it.
2. PLAN75 is a WHOLE-FILE REPLACEMENT of `.agent/plan.md`. RECORD75, SLIPS75 and DEC75 are
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
   `.remedy-wt/f275-r75.block.md`: TOTAL 378 lines, PROSE 305 lines, where PROSE is TOTAL
   minus the lines lying between BEGIN and END markers, markers themselves counted as PROSE.
   This clause is the ONLY place either numeral appears; G1 names this clause rather than
   restating them.
9. `R-0880` STAYS OPEN. No finding id is registered, resolved or de-registered this round. Do
   not write a `Done:` or a `Landed:` paragraph of your own; `Done:` is reviewer-authored text
   only. The SLIPS75 lines are not ids, per amend0827-process-diet rule 2.
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

**G2 THE PLAN.** `.agent/plan.md` at C1 is byte-identical to slice PLAN75 — report both sizes
and both sha256 values. Report its line count against the AGENTS.md cap of 50, and the count of
lines matching `^## Goal$` and of lines matching `^## Next Steps$`, both of which are 1.

**G3 THE RECORD.** Three appends, three commits, and for each one TWO INDEPENDENT READERS and
a NEGATIVE CONTROL. Wherever a reading below is taken AT THE BASE, read those bytes with
`git show dac50bcd:<path>` into scratch or into memory; nothing is written over a tracked file
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
  (iv) Over RECORD75: report its line count, the number of lines AFTER THE FIRST carrying a
       reserved prefix (`- R-`, `Done: R-`, `Landed: R-`, `Gate: `), which is 0, and the number
       of lines C2 ADDS matching `^- R-` and matching `^Done: R-`, both of which are 0.
  (v)  RECORD75's first line joins a repeating record format, so compare it MECHANICALLY
       against its neighbours: report how many lines at the base already match
       `^Gate: F275 R\d+ — the F275 round \d+ entry\.`, whether the new first line matches that
       same pattern, and whether it duplicates any of them.
  (vi) Over DEC75: confirm it begins `## DECISION F275 D49 `, report how many lines at the base
       match `^## DECISION F275 D49` (which is 0), and report the highest existing
       `^## DECISION F275 D\d+` at the base. Then confirm that C4 REMOVES NO LINE — that its
       `git show --numstat` deletion column is 0 — which is what makes this a correction by
       append rather than a rewrite of DECISION F275 D48.
  (vii) Over SLIPS75: report the number of paragraphs it adds, how many begin
       `2026-09-12 · F275 R74 · `, and how many lines at the base already begin with that exact
       prefix.

**G4 THE ARTEFACT AND ITS TRANSCRIPT.**

  (a) `.agent/f275_t003_units_r75.md` at C5 is byte-identical to the C0b blob — report both
      sizes and both sha256 values — and the path does not resolve at the base with
      `git show dac50bcd:.agent/f275_t003_units_r75.md`, whose non-zero exit is the expected
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

  (a) Extract the single fence of the COMMITTED C0c carrier to `.remedy-wt/f275-r75-witness.py`
      and report the extracted size and sha256.
  (b) Run `python3 -B .remedy-wt/f275-r75-witness.py . dac50bcd` and REPRODUCE EVERY LINE OF
      EVERY BANNER in the handback.
  (c) THE READINGS THIS GATE TURNS ON, each reported with whether it holds. In section 2, that
      `git status --porcelain` is the empty string AFTER the coverage run, which is what makes
      running it in the primary checkout legal. In section 3, THE ARITHMETIC THIS ROUND EXISTS
      FOR: that the bucket LINE counts sum to the distinct-line total the same section states,
      and that the bucket SITE counts sum to the production-site total, both reported as the
      numbers you measured rather than as numbers this block names. A sum that does not match
      its stated total is a RED gate — it is the defect round 74 shipped, and it is invisible to
      every digest and byte-equality gate this workflow has. In section 4, that the risk set is
      0 in BOTH units. In section 5, that every thin site's control is green and its mutation
      red, that the summary reads as many proved as the thin set holds, and that every mutated
      file reverted byte-identically; any one of those failing is a RED gate. On any red here,
      stop and hand back. THE COLOUR OF SECTION 2's OWN SUITE RUN IS NOT A READING and is not a
      red condition, per constraint 13.
  (d) Report `git status --porcelain` and `git worktree list` AFTER this gate.

**G6 THE TREE DID NOT MOVE.**

  (a) Report the `git rev-parse` object id of `packages`, `apps`, `tests`, `docs` and `scripts`
      at the base `dac50bcd` and at C5, and whether each pair is EQUAL. This is the gate that
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
  (b) The changed paths over `dac50bcd`..C5: report how many, and report MISSING and EXTRA
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

## SLICE PLAN75 — whole-file replacement of `.agent/plan.md`, applied at C1

BEGIN PLAN75 sha256=262030673090ba31f14b401c7066fa2dc8b07440c29a0fa4fa1ec26117928816
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

ROUND 75 CORRECTS DECISION F275 D48's THREE NUMERALS AND THE UNIT CONFUSION BEHIND THEM.
Coverage resolves a context per LINE; the ruled set is keyed per SITE. Round 74's instrument
printed a site count in one section and a line distribution in the next without naming either,
so its buckets summed to fewer than its own site total. Both units are now printed with both
sums visible: 175 sites on 166 lines, 9 sharing. D48's two load-bearing readings are the same
in both units — the risk set is empty and the thin set is eleven lines carrying eleven sites,
all eleven still red-proved — so the ruling stands and DECISION F275 D49 records the
correction by appending. The round 74 verdict and its prose slips are booked.

## Next Steps

1. Re-run the flip's dry run against the corrected inputs of rounds 67 and 69 together — the
   plain re-derivation and the re-keyed set — the first reading of what both corrections
   cost in FAILURES rather than in sites.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
3. THE FLIP, which D48 permits, carrying its obligations: the full suite is the backstop, and
   the thin set is re-derived before the flip and any site that has dropped to zero witnesses
   is a stop.
4. Then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- THE REVIEWER'S ERROR RATE IS THE LIVE RISK AND IT ROSE THIS SESSION: round 73 FAILED on
  five reviewer defects, and rounds 72, 73 and 74 each landed stale or mis-united numerals a
  WORKER found. Ten dated lines went into `.agent/prose_slips.md` across four rounds.
- A UNIT IS PART OF A NUMBER. Coverage counts lines, the ruled set counts sites, and a
  document that prints one and names the other is wrong even when its arithmetic is right.
- The open set is 87 by distinct id, with `R-0880` open. Four are High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN75

## SLICE RECORD75 — appended to `.agent/live_review.md` at C2

BEGIN RECORD75 sha256=94ccfc769116de12326463b8375618c3f8d7dd300e0361ebe1df2db1d8d868ec
Gate: F275 R74 — the F275 round 74 entry. VERDICT PASS. Written by the planner and reviewer of session 26 after reading the committed range `0d47205d`..`dac50bcd` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 75, per operator amendment amend0827-process-diet rule 1. The round repaired the round 73 FAIL and it repaired it in the right place: not by re-taking a reading in a better mood, but by moving the measurement to where the suite actually runs and sharpening the question it answers.

WHAT THE TRANSPORT PROOF COVERS, STATED BEFORE THE FIGURES, per item 37 of §3. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback, and the chain it walks is the reviewer's own scratch original, the committed `.agent/authored/` blob and the working copy. It does not and cannot establish what bytes the worker RECEIVED. All three authored blobs are byte-identical to the reviewer's originals — the block at 38127 bytes, the artefact at 9578 and the witness-instrument carrier at 12539 — and `.agent/last_block.md` equals the block blob. Four slices matched the sha256 on their own BEGIN markers, the block re-measures at 382 lines TOTAL and 299 PROSE as its constraint 8 states, it carries zero repeated-character lines, and the carrier round-trips through its own fence byte for byte.

THE THREE GATES ROUND 73 DROPPED WERE RESTORED AND ALL THREE HOLD, which is the half of this round that answers the previous verdict directly. The artefact's 24 quoted lines all appear in the instrument's output, the matching is monotone with indices strictly increasing, zero lines are unmatchable, and the count of quoted lines carrying a wall-clock duration is ZERO — the defect that made round 73 a FAIL, now stated as a gate and measured at nothing. G2: `.agent/plan.md` byte-identical to PLAN74 at 48 lines against the cap of 50. G3: the three appends each exact under reader A with the slice an exact suffix after one newline, reader B holding at N counted from the slice as 9, 4 and 6, and all three of the reviewer's negative controls on the FIRST appended paragraph REJECTED by both readers; C4's deletion column is 0, so DECISION F275 D47 is corrected by APPEND and not rewritten, which is the property the round was built around. G4: the artefact byte-identical to the C0b blob, absent at the base, every commit staging exactly ONE path with insertions peaking at 382 and none at or over the 500 cap — the round 73 overage is not repeated. G6 and G7: five top-level trees byte-identical across the round's eleven mutations, `git status --porcelain` the empty string, one worktree, nine changed paths with MISSING and EXTRA empty and zero production paths, and the open set 87 with identical membership at the base, at C5 and at the tip with `R-0880` open at each.

G5 CARRIED THE ROUND. The measurement moved into the PRIMARY CHECKOUT, where `apps/ui/node_modules` and a built dist exist and the `ui_server` suite can run at all, and `git status --porcelain` reads empty immediately after the coverage pass, which is what makes that legal under G5 of the protocol: a coverage run writes no tracked file. The question moved from "is the line executed" to "how many tests witness it", which is answerable for every refused site at once instead of by spot-check. The risk set — refused and witnessed by nothing — is EMPTY. The thin set is ELEVEN, and every one of the eleven is red-proved individually against its own single witness: eleven controls green, eleven mutations red, every file reverted byte-identically. The probe mutates the ATTRIBUTE NODE the ruled set records rather than the first textual match, which a draft of the same instrument got wrong at `packages/orchestration/verifier.py`, where the first textual `.id` sits inside an f-string literal and a naive replace edited a message instead of an attribute access — that draft read 10 of 11 and the defect was the instrument's, not the repository's.

AND THE ROUND'S OWN GATE SET NOW REFUSES TO DEMAND A COLOUR IT CANNOT GUARANTEE. Round 73 made a green full-suite control a pass condition and went red on a load-sensitive perf test. This block states in its own text that no gate demands a green whole-suite run, names why — this suite has at least three environment-sensitive tests, a wall-clock perf budget and a workspace-identity pair, each observed red in one invocation and green in the next and passing in isolation — and states the bias that makes the colour unnecessary: a failing test executes FEWER lines, so it can only UNDERSTATE a witness count, which makes the risk and thin sets too large rather than too small.

THREE NUMERALS OF THE REVIEWER'S DID NOT REPRODUCE, AND THE WORKER FOUND THEM BY ARITHMETIC RATHER THAN BY READING. DEC74 says the distribution runs "over all 176 at once", gives "98 by ten or more" and totals "7065 site-and-test pairs"; PLAN74 repeats the last. The instrument reports 175 production sites, 97 in that bucket and 6966 pairs. The cause is a unit the reviewer never named: coverage resolves a context per LINE while the ruled set is keyed per SITE, and nine of the 175 sites share a line with another, so round 74's banner counted sites in one section and lines in the next and its buckets summed to 166. The worker applied both slices as written, as constraint 1 requires, and declared the discrepancy with the arithmetic that shows it. THE READINGS DECISION F275 D48 ACTUALLY RESTS ON ARE THE SAME IN BOTH UNITS — the risk set is empty either way, and the eleven thin LINES carry exactly eleven SITES — so the ruling stands and round 75 corrects the numerals by appending DECISION F275 D49 rather than by rewriting a landed paragraph. Two dated lines in `.agent/prose_slips.md` and no id, per amend0827-process-diet rule 2: nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong.
END RECORD75

## SLICE SLIPS75 — appended to `.agent/prose_slips.md` at C3

BEGIN SLIPS75 sha256=5b80d81a839e0313d36f4e7189c6150d70937220f6fb1086074f0500449a37f9
2026-09-12 · F275 R74 · The round 74 DEC74 slice states that the witness distribution runs "over all 176 at once", gives "98 by ten or more" and totals "7065 site-and-test pairs", and PLAN74 repeats the last; the committed instrument reports 175 production sites, 97 in that bucket and 6966 pairs. The three numerals are the reviewer's stale copies from a DISCARDED draft of that instrument, which derived its refusal set from round 72's decision map rather than from the shipped Rule H stage. The artefact was corrected to the shipped guard's figures and the decision and the plan were not, so the round landed a document that reproduces beside two that do not. THE RULE THAT FOLLOWS: when an instrument is re-pointed at a different input, every authored text of that round is re-swept against its NEW output before emission, not only the one the gate checks — a figure sweep that covers the gated artefact and nothing else leaves the decision, which is the append-only half, unprotected.

2026-09-12 · F275 R74 · The deeper cause of the numerals above is a UNIT the round 74 instrument never named. Coverage resolves a context per LINE; the ruled set is keyed per SITE — path, line, column and attribute — and nine of the 175 refused production sites share a line with another. The instrument printed a site count in its first section and a line distribution in its third, calling both by the same word, so its buckets summed to 166 against a stated total of 175, and DECISION F275 D48 restated the two as one number. The worker found it by adding the buckets up, which is a check the prose could not pass by accident. Nothing on disk is wrong beyond the numerals, because the two readings D48 rests on are identical in both units: the risk set is empty either way, and the eleven thin LINES carry exactly eleven SITES. THE RULE THAT FOLLOWS: a banner that reports a distribution prints the SUM of its own buckets beside the total it claims to partition, and every count states the unit it is in, because a wrong unit is invisible to every digest, byte-equality and transcript gate this workflow has — only arithmetic sees it.
END SLIPS75

## SLICE DEC75 — appended to `.agent/decisions.md` at C4

BEGIN DEC75 sha256=ea708b73fc634b90043b1a12a79bdf6b3e46fcc4052ee7bd95765d87918f38c9
## DECISION F275 D49 (2026-09-12, F275 round 75) — DECISION F275 D48's three descriptive numerals are CORRECTED by appending, the SITE-versus-LINE unit is now printed by the instrument, and D48's ruling is unchanged because the readings it rests on are the same in both units

CONTEXT. DECISION F275 D48 discharged DECISION F275 D45's precondition on a witness measurement and described it as "a distribution over all 176 at once", with "98 by ten or more" and "7065 site-and-test pairs". The committed instrument reports 175 production sites, 97 lines in that bucket and 6966 pairs. Two things went wrong and only one of them is a numeral. The three figures were stale copies from a DISCARDED draft of that instrument, which derived its refusal set from round 72's decision map rather than from the shipped Rule H stage; the artefact was corrected to the shipped guard and the decision was not. Underneath that sits a UNIT the instrument never named: coverage resolves a context per LINE, the ruled set is keyed per SITE — path, line, column and attribute — and nine of the 175 refused production sites share a line with another, so one banner counted sites and the next counted lines under the same word, and the buckets summed to 166 against a stated 175.

CHOSEN. (1) THE CORRECTED FIGURES, measured by this round's instrument at its own base and stated here once: the shipped guard refuses 277 ruled sites, of which 102 are in test files and 175 are production sites; those 175 sit on 166 DISTINCT LINES, with 9 sites sharing a line with another; the witness buckets are 0 lines carrying 0 sites, 11 lines carrying 11 sites, 58 lines carrying 60 sites, and 97 lines carrying 104 sites; the bucket sums are 166 lines and 175 sites, both printed; the median is 17 witnesses per LINE; and the total is 6966 LINE-and-test pairs, which is what the instrument has always computed and D48 called site-and-test pairs. (2) THE INSTRUMENT NOW PRINTS THE UNIT ON EVERY COUNT and prints both bucket sums beside the totals they partition, so the arithmetic that exposed this is visible in the output rather than left to a reader. (3) D48 IS NOT REWRITTEN. The record is append-only, item 20 of `docs/agents/planner_reviewer_prompt.md` §3 forbids repairing a landed sentence, and a dated correction beside a wrong paragraph is worth more to a later reader than a clean paragraph with no history. (4) D48's RULING IS UNCHANGED, and this is a measurement rather than a concession: the risk set is empty in BOTH units, and the eleven thin LINES carry exactly eleven SITES, so "the eleven thin sites" was right as written and all eleven remain red-proved against their own single witnesses. The discharge of D45's precondition therefore stands on the readings it actually rests on, and the corrected numerals were descriptive throughout.

ALTERNATIVES CONSIDERED. Retracting D48 and re-ruling from scratch was rejected: nothing it rests on moved, and a retraction would tell a later reader that the ruling was unsound when only its scenery was. Leaving the numerals uncorrected as a prose slip was rejected for the opposite reason — a slip line is the right vehicle for a miscount that damaged nothing, and these numerals sit in the append-only record where the next reader will take them as measured. Both are recorded: the slip lines carry the lesson, this decision carries the figures.

CONSEQUENCE, AND IT IS SMALL BY DESIGN. Nothing about the flip round's obligations changes: the full suite remains the backstop, and the thin set is still re-derived before the flip with any site fallen to zero witnesses treated as a stop. What changes is that the thin set is now expressed in both units wherever it is stated, because a set of lines and a set of sites can diverge even when they do not happen to here. `R-0880` STAYS OPEN and the guard is still silent on 277 sites. Nothing here touches the id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse, which is production work no round has started.

HOW TO REVERSE. Delete this paragraph block; D48 then stands alone with three numerals that its own instrument contradicts, and the unit distinction returns to being invisible. Every figure above is re-derivable by the committed instrument `.agent/authored/f275-r75-witness.py.md` at this round's base, except the three this decision QUOTES from D48 in order to correct them, which come from D48 itself.
END DEC75
