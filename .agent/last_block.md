# STEP T003 — F275 ROUND 77 — the flip's input set, constructed and ruled

## Goal

Turn DECISION F275 D50's inference into a construction. The shipped owner check names the ruled
sites whose receiver holds another record; every one of them is among the sites the plain
re-derivation drops, and the rest of that drop is what made round 76's plain arm worse. The
corrected set is the round 53 re-keyed set minus exactly those contradicted sites. It passes the
owner check at zero where the round 53 set exits non-zero, and run as a third arm at the same
commit against the same control it FIXES 23 test nodes and BREAKS NONE. DECISION F275 D51 rules
it the flip's input. Book the round 76 PASS verdict and its three prose slips. NO PRODUCTION
LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r77.md`
- C0b save the artefact as authored text — `.agent/authored/f275-r77-artefact.md`
- C0c save the instrument carrier as authored text — `.agent/authored/f275-r77-instrument.py.md`
- C0d mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 77 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 76 reviewer verdict — `.agent/live_review.md`
- C3 append the round 76 prose slips — `.agent/prose_slips.md`
- C4 record DECISION F275 D51 — `.agent/decisions.md`
- C5 land the partition artefact — `.agent/f275_t003_flip_residue_r77.md`
- C6 the round 77 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r77.md
    .agent/authored/f275-r77-artefact.md
    .agent/authored/f275-r77-instrument.py.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/decisions.md
    .agent/f275_t003_flip_residue_r77.md
    .agent/handoff.md

No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` is touched. This is not a
deletion round and no file is removed. NOTHING LANDED BY AN EARLIER ROUND IS REWRITTEN OR
REVERTED: DECISION F275 D50 stays exactly as it is on disk, and D51 is an append beside it
rather than an edit of it.

## The reviewer's texts on disk, and how they travel

Every reviewer-authored text of this round exists as a file under the gitignored `.remedy-wt/`
at this round's base, and each is of one of two kinds. A SLICE is carried verbatim in this
block between a BEGIN and an END marker, the BEGIN marker stating the sha256 of the bytes
between them; the slices are PLAN77, RECORD77, SLIPS77 and DEC77, each under its own heading
below. A WHOLE TEXT is too long to retype and is never retyped: it is transported with
`shutil.copyfile` and never opened in an editor. The whole texts, with their scratch paths and
digests:

    .remedy-wt/f275-r77-artefact.md         11738 bytes  bc4abd74d806b9b36f4b413782fe9c3e0bd5c87438aebdb41e2c44a23d2f1303
    .remedy-wt/f275-r77-instrument.py.md    15578 bytes  bb8c33256d936593639daa756dc3f9025eb22b69b9bbafc79b1255bc35f1e1bf

The block travels the same way: read `.remedy-wt/f275-r77.block.md` from disk, verify its
sha256 against the one the delegation wrapper states, and copy it to
`.agent/authored/f275-r77.md` at C0a and to `.agent/last_block.md` at C0d. A slice is applied
BYTE FOR BYTE: nothing is reflowed, re-wrapped, re-indented or corrected, and a slice that
looks wrong is APPLIED AS WRITTEN and declared in the handback.

## Constraints

1. APPLY EVERY SLICE VERBATIM. Extract each by its BEGIN and END marker prefixes, markers
   EXCLUDED, from the COMMITTED C0a blob — never from the delegation prompt and never from
   memory — and check each against the sha256 its own BEGIN marker carries before applying it.
2. PLAN77 is a WHOLE-FILE REPLACEMENT of `.agent/plan.md`. RECORD77, SLIPS77 and DEC77 are
   APPENDS: the pre-commit blob is a byte-exact PREFIX of the post-commit file and the slice
   is an exact SUFFIX of it, separated by exactly one newline.
3. ONE PATH PER COMMIT, in the Bundle's order. Run the AGENTS.md self-review loop before every
   commit: `git diff --cached --stat`, `--numstat` and the full `git diff --cached`. Where a
   commit's diff is a single large blob, the decisive check is BYTE-EQUALITY of the resulting
   blob against its scratch original by sha256, and that is what the handback reports; no hunk
   count is ordered, because it depends on how much of the old file the new one shares and
   C0d REPLACES `.agent/last_block.md`.
4. NO PRODUCTION PATH MOVES. If any gate would require editing a tracked file under
   `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`, STOP and hand back instead.
5. THIS ROUND'S INSTRUMENT NEEDS NO WORKTREE AND RUNS NO TEST. It re-analyses SAVED transcripts
   and SAVED site sets and is therefore deterministic. The reviewer's four suite passes and the
   worktrees that produced those transcripts are already done, and every one of those worktrees
   was removed and pruned before this block was authored. The ONLY disposable worktree this
   round needs is the one G3(iii) creates for its negative control, and that worktree is removed
   and pruned by the same script. `git status --porcelain` is the empty string at every commit
   and at the handback.
6. NO `gh` COMMAND AND NO `remedy` CLI COMMAND IS RUN. No pull request is created, edited or
   merged. No branch is created. No merge. No force-push. Push the branch after C6.
7. READ `.agent/STOP` FROM DISK before the first commit and again before C6, by BOTH
   `os.path.exists` and `glob`, and report both readings literally in the handback. If it
   exists, finish the commit in hand, write the handback and stop.
8. THIS BLOCK'S OWN SIZE. Measured by the reviewer on the FINAL bytes of
   `.remedy-wt/f275-r77.block.md`: TOTAL 397 lines, PROSE 316 lines, where PROSE is
   TOTAL minus the lines lying between BEGIN and END markers, markers themselves counted as
   PROSE. This clause is the ONLY place either numeral appears; G1 names this clause rather
   than restating them.
9. `R-0880` STAYS OPEN. No finding id is registered, resolved or de-registered this round. Do
   not write a `Done:` or a `Landed:` paragraph of your own; `Done:` is reviewer-authored text
   only. The SLIPS77 lines are not ids, per amend0827-process-diet rule 2.
10. NO `.py` FILE IS CREATED ANYWHERE UNDER `.agent/`, and G6(d) reads the FILESYSTEM for that
    rather than a linter's findings. A `.py` file inside the tree is counted by the `ruff`
    ceiling that `tests/orchestration/test_ci_budgets.py` freezes, which is why the instrument
    ships as a `.py.md` carrier; but a clean `.py` file produces no ruff row at all, so a gate
    reading ruff's output is blind to exactly the file this constraint forbids. That is a
    defect in the gate this round's predecessor carried, and G6(d) is its repair.
11. EVERY GATE IS RUN AS `bash -c '<cmd> > <out> 2>&1; echo "REAL_EXIT=$?" >> <out>'` AND THE
    EXIT CODE IS READ BACK OUT OF THE FILE. Write transcripts under `.remedy-wt/`. "Green" as
    a word is a finding; the recorded number is the evidence.
12. THE INSTRUMENT'S INPUTS ARE THE SCRATCH FILES IT NAMES IN ITS OWN SECTION 0, WITH THEIR
    SIZES AND DIGESTS, AND NONE OF THEM IS REGENERATED. Before running it, check every file
    that section names against the digest printed for it; if any is missing or differs, STOP
    and hand back, and do not rebuild it. Four of them are pytest transcripts of roughly twenty
    minutes each and cannot be re-taken inside this round. The block states no count of those
    inputs: G5(d) orders the number MEASURED.
13. NO GATE BELOW DEMANDS THAT A WHOLE-SUITE RUN BE GREEN, and no gate below runs the suite at
    all. The readings this round turns on are DIFFERENCES between runs of the same selection,
    taken by the reviewer before this block existed and fixed in the transcripts constraint 12
    pins.
14. THE SUITE SUMMARY LINES THE INSTRUMENT READS CARRY WALL-CLOCK DURATIONS AND THE ARTEFACT
    QUOTES NONE OF THEM. That is why G4(e) can still demand zero: the artefact takes its
    failure counts from the instrument's node-id lines instead, which carry no duration.
    Round 73 failed on a quoted duration and the gate that caught it is carried here unweakened.
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
constraint 15 fixes at zero, under BOTH the length-two and the length-one reading. REPORT THE
LINE COUNT OF EVERY BLOB THIS ROUND CREATES against 500, the DECISION F104 D1 insertion cap —
for a file the commit CREATES the two are the same number. Finally, for the `.py.md` carrier:
report the number of ```python fence lines and of bare ``` lines, both of which must be 1;
extract the source; and confirm that re-wrapping it in the carrier's own header and fence
reproduces the committed blob BYTE FOR BYTE.

**G2 THE PLAN.** `.agent/plan.md` at C1 is byte-identical to slice PLAN77 — report both sizes
and both sha256 values. Report its line count against the AGENTS.md cap of 50, and the count of
lines matching `^## Goal$` and of lines matching `^## Next Steps$`, both of which are 1.

**G3 THE RECORD.** Three appends, three commits, and for each one TWO INDEPENDENT READERS and
a NEGATIVE CONTROL. Wherever a reading below is taken AT THE BASE, read those bytes with
`git show 75cc221e:<path>` into scratch or into memory; nothing is written over a tracked file
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
       AN ASCII LETTER IS A BYTE IN 0x41 TO 0x5A OR 0x61 TO 0x7A, TESTED AS A BYTE: every
       paragraph of `.agent/prose_slips.md` opens with a U+00B7 separator whose lead byte
       passes a naive latin-1 letter test, and a flip landing there corrupts the encoding
       instead of the content. Remove and prune that worktree in the same script and report
       `git worktree list` afterwards.
  (iv) Over RECORD77: report its line count, the number of lines AFTER THE FIRST carrying a
       reserved prefix (`- R-`, `Done: R-`, `Landed: R-`, `Gate: `), which is 0, and the number
       of lines C2 ADDS matching `^- R-` and matching `^Done: R-`, both of which are 0.
  (v)  RECORD77's first line joins a repeating record format, so compare it MECHANICALLY
       against its neighbours: report how many lines at the base already match
       `^Gate: F275 R\d+ — the F275 round \d+ entry\.`, whether the new first line matches that
       same pattern, and whether it duplicates any of them.
  (vi) Over DEC77: confirm it begins `## DECISION F275 D51 `, report how many lines at the base
       match `^## DECISION F275 D51` (which is 0), and report the highest existing
       `^## DECISION F275 D\d+` at the base. Then confirm that C4 REMOVES NO LINE — that its
       `git show --numstat` deletion column is 0.
  (vii) Over SLIPS77: report the number of paragraphs it adds, how many begin
       `2026-09-12 · F275 R76 · `, and how many lines at the base already begin with that exact
       prefix.

**G4 THE ARTEFACT AND ITS TRANSCRIPT.**

  (a) `.agent/f275_t003_flip_residue_r77.md` at C5 is byte-identical to the C0b blob — report
      both sizes and both sha256 values — and the path does not resolve at the base with
      `git show 75cc221e:.agent/f275_t003_flip_residue_r77.md`, whose non-zero exit is the
      expected reading; report the exit code literally rather than as "non-zero".
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
      and how many do not. For each that does not, report it with the line that uses it and
      classify it against THE ARTEFACT'S OWN PROVENANCE CLAUSE, whose words are authoritative
      over this gate's: that clause declares exactly two kinds and says so, and where this
      gate's wording and that clause differ, the clause rules. Report the count you could not
      place under it, which must be 0.
  (e) NO LINE QUOTED IN THE ARTEFACT CARRIES A WALL-CLOCK DURATION: report the count of quoted
      lines matching `in \d+\.\d+s`, which is 0. Constraint 14 states why that is attainable.
  (f) Report, for EVERY commit C0a through C5, the INSERTION count from `git show --numstat
      <sha>` — the `+` column DECISION F104 D1 caps at 500 — with the number of paths that
      commit stages, which is 1 for each, and whether each insertion count is under 500.

**G5 THE INSTRUMENT.** Read constraints 12 and 13 before starting this one.

  (a) Extract the single fence of the COMMITTED C0c carrier to
      `.remedy-wt/f275-r77-instrument.py` and report the extracted size and sha256.
  (b) Run `python3 -B .remedy-wt/f275-r77-instrument.py .remedy-wt` and REPRODUCE EVERY LINE OF
      EVERY SECTION in the handback.
  (c) DETERMINISM: run it THREE times and report the sha256 of stdout for each run and whether
      all three are identical. A reading this round turns on that is not byte-stable is a RED
      gate, because the artefact quotes it line by line.
  (d) THE READINGS THIS GATE TURNS ON, each reported with whether it holds. The instrument
      labels its own arithmetic in two kinds and the difference is the point: a CROSS-CHECK
      compares two numbers reached by different routes and CAN fail, a PARTITION adds a set's
      own parts back to the set and cannot. Report the number of lines containing `MISMATCH`,
      which must be 0. Report the number of records whose line BEGINS with `CROSS-CHECK ` and
      the number whose line BEGINS with `PARTITION `, both of which you MEASURE rather than
      take from this block, and note that section 8's own explanatory prose opens with one of
      those two words, so a prefix count exceeds the summary's count by one and the two
      readings are reported side by side rather than reconciled. Report section 8's `FAILING`
      counts, both of which must be 0, and its `EVERY CHECK HOLDS` line, which must read True.
      Then, by section: in section 0, that each input file named is present at the size and
      sha256 printed for it — constraint 12; in section 2, that
      `EVERY SITE THE OWNER CHECK CONTRADICTS IS ONE THE PLAIN SET DROPS: True` and that
      `the corrected set IS that difference, as a set: True`; in section 3, that the owner
      check's CONTRADICTED count is non-zero over the round 53 set and zero over the corrected
      one, which is the discriminator the guard needs at both ends; in section 6, that the
      BREAKS cell of the CORRECTED-against-round-53 line reads 0. On any red here, stop and
      hand back.

  (e) Report `git status --porcelain` and `git worktree list` AFTER this gate.

**G6 THE TREE DID NOT MOVE.**

  (a) Report the `git rev-parse` object id of `packages`, `apps`, `tests`, `docs` and `scripts`
      at the base `75cc221e` and at C5, and whether each pair is EQUAL.
  (b) THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`, reporting the tail of
      its output and its real exit code.
  (c) `python3 -m ruff check . --output-format concise`. Its exit is 1 whenever any finding
      remains, so THE GATE IS THE COUNT: report the number of rows matching `^\S+:\d+:\d+: `,
      which must equal the ceiling `tests/orchestration/test_ci_budgets.py` freezes, and the
      number of rows whose path lies under `.remedy-wt/`, counted rather than grepped. Run it
      AFTER G3(iii) has removed and pruned its worktree.
  (d) CONSTRAINT 10, READ OFF THE FILESYSTEM RATHER THAN OFF RUFF. Report the number of paths
      matching `.agent/**/*.py` that exist on disk, and the number that `git ls-files .agent`
      returns ending in `.py`. Both are 0. This gate replaces the ruff-row count that stood
      here in earlier rounds, which could not see a clean `.py` file at all.

**G7 NOTHING ELSE MOVED.**

  (a) `.agent/STOP` exists on disk: report the boolean. `git status --porcelain | cat -A`:
      report it literally. `git worktree list`: report every entry and their number, which is
      1, the primary checkout alone.
  (b) The changed paths over `75cc221e`..C5: report how many, and report MISSING and EXTRA
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
NUMBER of the running feature, which is 27, and the round, which is 77. One line per gate with
its REAL_EXIT read out of its transcript file. A per-commit table in the `## Commits` section
`docs/agents/handback_template.md` mandates, whose `+/-` column is read from
`git show --numstat <sha>` and from no other source — that column is an INSERTION and DELETION
count, never a file's line count — and whose insertion cell for each of C0a through C5 is
compared against the number G4(f) reports for that same commit, cell by cell, with the
comparison stated. The item-status table covers every C and every G exactly once. State the
context self-assessment amend0905-throughput requires, in one sentence. Declare every
deviation. F275 stands past the soft limit amend0908-f275-finish rule 1 names, so the handback
carries the line `SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE`, and the SCOPE
REPORT that rule obliges was written in round 51's handback and STANDS — do not restate it.
Push after C6.

## SLICE PLAN77 — whole-file replacement of `.agent/plan.md`, applied at C1

BEGIN PLAN77 sha256=15263f85ce972fe61289fc920ff83ff97132ba696d03ae871dad2aff2475eea9
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

ROUND 77 CONSTRUCTS THE FLIP'S INPUT SET, which DECISION F275 D50 could only infer. The shipped
owner check names 13 ruled sites whose receiver holds another record, every one of them is
among the 60 the plain re-derivation drops, and the other 47 are the wrongly dropped ones.
The corrected set is the round 53 re-keyed set minus those 13, at 2185 sites; it passes the
owner check at zero contradictions where the round 53 set exits at 13. Run as a third arm at
the same commit against the same control it FIXES 23 test nodes and BREAKS NONE, and
`Mission.job_id` and `QueueEntry.job_id` leave the residue entirely. DECISION F275 D51 rules
that set the flip's input. The round 76 verdict and its three prose slips are booked.

## Next Steps

1. Carry the 19 surviving over-selection frames back to the ruled sites that produce them,
   which the corrected set does not remove because the owner check REFUSES rather than
   decides on their receivers. That is the residue `R-0880`'s second obligation still names.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
3. THE FLIP, on the corrected set, carrying DECISION F275 D48's obligations: the full suite
   is the backstop, and the thin set is re-derived before the flip with any site fallen to
   zero witnesses treated as a stop.
4. Then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- THE CORRECTED SET IS BETTER, NOT RIGHT. 19 over-selection frames survive it on classes the
  owner check refuses to decide, and 1204 bad nodes is the best reading this chain has taken
  and is not near green.
- THE 47 ARE UNCONTRADICTED, WHICH IS WEAKER THAN CORRECT. The owner check refuses 277 sites,
  and a site can sit in that refusal set and still be wrong.
- The open set is 87 by distinct id, with `R-0880` open. Four are High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN77

## SLICE RECORD77 — appended to `.agent/live_review.md` at C2

BEGIN RECORD77 sha256=0853581168ed5e74bc1cc5ac884643fd64749e71da46ff1f113f62f0e0dd4b54
Gate: F275 R76 — the F275 round 76 entry. VERDICT PASS. Written by the planner and reviewer of session 27 after reading the committed range `ef75e213`..`75cc221e` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below, and the reviewer's own script recomputed every figure from git objects and from its own scratch originals rather than from any transcript the worker wrote. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 77, per operator amendment amend0827-process-diet rule 1.

WHAT THE TRANSPORT PROOF COVERS, STATED BEFORE THE FIGURES, per item 37 of `docs/agents/planner_reviewer_prompt.md` §3. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: the chain it walks is the reviewer's own scratch original, the committed `.agent/authored/` blob and the working copy. It does not and cannot establish what bytes the worker RECEIVED. All three authored blobs are byte-identical to the reviewer's originals — the block at 36689 bytes, the artefact at 16247 and the instrument carrier at 18628 — and `.agent/last_block.md` equals the committed block blob. Four slices matched the sha256 on their own BEGIN markers, the block re-measures at 385 lines TOTAL and 308 PROSE as its constraint 8 states, and it carries zero lines that are a single repeated character under either the length-two or the length-one reading.

EVERY GATE HOLDS AND THE REVIEWER RE-RAN ALL SEVEN. G2: `.agent/plan.md` byte-identical to PLAN77's predecessor PLAN76 at 48 lines against the cap of 50, with one `## Goal` and one `## Next Steps`. G3: the three appends exact under reader A, reader B holding over the WHOLE appended region at N counted from the slice as 5, 2 and 9, and all three negative controls placed on the FIRST appended paragraph REJECTED by both readers; C4's deletion column is ZERO, so DECISION F275 D48 and D49 are corrected by APPEND and not rewritten, and RECORD76's header matches the ledger's repeating format and duplicates none of the 74 already there. G4: the artefact byte-identical to the C0b blob, absent at the base at exit 128, its 83 quoted lines all present in the instrument's output with the matching monotone and nothing unmatchable, zero quoted lines carrying a wall-clock duration and zero three-backtick lines. G6 and G7: five top-level tree object ids byte-identical at the base and at C5, the canary 42 passed, `ruff check .` 26 rows against the frozen ceiling of 26, `git status --porcelain` the empty string, one worktree, nine changed paths with MISSING and EXTRA both empty and zero production paths, and the open set 87 by distinct id with identical membership at the base, at C5 and at the tip and `R-0880` open at each.

THE PER-COMMIT INSERTION COUNTS WERE RE-DERIVED AND THE HANDBACK'S OWN TABLE COMPARED AGAINST THEM CELL BY CELL, which is the obligation item 28 of §3 carries for a value the worker writes twice. All nine cells agree with `git show --numstat`. The handback commit's own numbers, which no gate of that round could reach, are 636 insertions and 809 deletions over `.agent/handoff.md` alone, and they are exempt entirely under AGENTS.md DECISION F104 D1 as the verbatim rewrite of a single `.agent/**` state file rather than an invocation of the once-per-feature oversize clause.

THE ROUND'S SUBSTANCE, AND IT IS A RESULT RATHER THAN A REPAIR. The dry run three decisions had deferred was taken, against the corrected inputs of rounds 67 and 69 together, in three suite passes at one commit differing in the ruled site set alone. The plain re-derivation costs 134 additional bad test nodes: it breaks 172 and fixes 38. The cause is measured — it removes every production record class `R-0880` names from the residue, 59 over-selection frames falling to 1, and introduces 231 under-selection frames where the round 53 set has none. So the two sets are wrong in opposite directions and DECISION F275 D50 rules the flip's input to be neither. The controls carry the claim: the five tree object ids are identical at round 59's base and at this one, the re-key stage reproduces `.remedy-wt/r69_rekeyed.json` byte for byte, the round 53 arm reproduces round 69's own 263 files and 6091 rewrites, and the unflipped control reproduces round 59's summary to the unit.

AND THE ROUND REPAIRED A GATE OF ITS OWN THAT COULD NOT FAIL, WHICH IS WORTH MORE THAN THE READING IT PROTECTS. An earlier edition of the instrument printed only partitions — sums of a set's own parts against that set — and a control that deleted one `FAILED` line from a transcript left every one of them reading MATCH. Cross-checks between independently derived numbers were added, the instrument now labels the two kinds apart, and the first run of them found a real defect in the instrument's own parser: the transform's rule table was being split at a two-space gap that three of the longest rule names do not have, so three rows worth 19 rewrites were dropped and only the comparison against the transform's own printed total saw it. The gate the worker re-ran reports 14 cross-checks and 12 partitions, all holding, and the reviewer's own count of the verdict-bearing records agrees.
END RECORD77

## SLICE SLIPS77 — appended to `.agent/prose_slips.md` at C3

BEGIN SLIPS77 sha256=eabbd72b978175ee4b1e893553b2669a243ef8a8864a995c76b9ce16bccf3a2a
2026-09-12 · F275 R76 · The round 76 block's G6(c) ordered "the number of rows whose path ends `.py` under `.agent/`, which constraint 10 fixes at 0", and that clause is BLIND to the thing constraint 10 forbids. `ruff check` emits a row only for a file that HAS a finding, so a clean `.py` file created under `.agent/` produces no row and the gate reads 0 whether or not the file exists — it measures the shape of ruff's output rather than the truth constraint 10 states. The reading happened to be honest this round because the reviewer checked the filesystem directly at the verdict and found zero `.py` files anywhere under `.agent/`, tracked or untracked, but that check was not the one the block ordered. The clause has been carried forward unexamined since well before this round. THE RULE THAT FOLLOWS: a gate asserting the ABSENCE of a file kind reads the FILESYSTEM or the index for it, never a linter's findings, because a tool that reports problems is silent about a file with no problems and its silence is indistinguishable from the file not being there.

2026-09-12 · F275 R76 · The round 76 instrument's section 8 opens with a prose line beginning "PARTITION adds a set's own parts back to the set and cannot", and its own records are keyed by the prefixes `CROSS-CHECK ` and `PARTITION `. A gate counting those records by line prefix therefore reads 13 partitions where the tool's own summary reports 12, and both the worker and the reviewer measured the 13 independently and had to explain it. Nothing was wrong on disk and no reading the round turned on moved. THE RULE THAT FOLLOWS: a tool that keys its records by a leading token does not open a sentence with that token, because its own explanatory prose then answers the sweep that counts its records — the collision is invisible in the output and shows up only as a count that disagrees with the summary printed beside it.

2026-09-12 · F275 R76 · The round 76 block's G3(iii) ordered the negative control to "Choose an ASCII letter, so the flip cannot land inside a multi-byte sequence", and the worker implemented it correctly while the REVIEWER's own re-derivation script did not: it picked the first byte satisfying `chr(b).isalpha()`, which is True for `0xB7`, the lead byte of the U+00B7 separator that opens every line of `.agent/prose_slips.md`. The script crashed decoding the mutated bytes rather than producing a false pass, so the defect announced itself, and the fix made the reviewer's control test the byte range the block's own words name. THE RULE THAT FOLLOWS: a reviewer's re-derivation is written against the block's words as literally as the worker's implementation is, and `chr(byte).isalpha()` is not a test for an ASCII letter — it is a test for a latin-1 letter, which is exactly the class the instruction was written to exclude.
END SLIPS77

## SLICE DEC77 — appended to `.agent/decisions.md` at C4

BEGIN DEC77 sha256=18a6167dfb2dfef2c04dc84a2104bbc18c914537ad2116be0b87567b0afbc41e
## DECISION F275 D51 (2026-09-12, F275 round 77) — the flip's input set is CONSTRUCTED and ruled: the round 53 re-keyed set minus the sites the shipped owner check contradicts, which is strictly better than the set the transform consumes today

CONTEXT. DECISION F275 D50 measured that the round 53 committed set over-selects and the round 67 plain re-derivation under-selects, ruled that the flip's input is neither, and named the set between them. It was careful to call that set an inference: its own "what this reading does NOT settle" paragraph says the partition of the 60 dropped sites into correctly and wrongly dropped "is an inference rather than a measurement", because nothing had carried an over-selected frame back to the ruled site that produced it. This round takes the measurement, builds the set, and runs it. The measurement is in `.agent/f275_t003_flip_residue_r77.md` and the instrument is committed at `.agent/authored/f275-r77-instrument.py.md`; every figure below is re-derivable by that instrument from the transcripts its own section 0 pins by sha256.

CHOSEN, PART ONE: THE PARTITION IS MEASURED, AND BY A CHEAPER ROUTE THAN D50 IMAGINED. D50 described carrying each over-selection frame back through the re-key into the ruled set's coordinates. That route works and was probed — all thirteen distinct frames in this repository resolve to a base line carrying a ruled site — but it was not spent, because the SHIPPED owner check of DECISION F275 D47 already names the sites directly, by path, line, column and attribute, with no suite run and no coordinate arithmetic. Over the round 53 re-keyed set it decides 1921 sites, refuses 277 and CONTRADICTS 13, on receivers holding `Mission` at 9, `Artifact` at 3 and `QueueEntry` at 1. All 13 are among the 60 the plain re-derivation drops and NONE survives in the plain set, which is exactly the containment D50 inferred. The other 47 are the wrongly dropped ones and they are what cost round 76's plain arm its 231 under-selection frames.

CHOSEN, PART TWO: THE CORRECTED SET IS THE ROUND 53 RE-KEYED SET MINUS THOSE 13, AT 2185 SITES, and it is that difference as a set rather than merely at that count. The three sets nest — the plain set inside the corrected set inside the round 53 set — so the comparison is a line and not a triangle. The same owner check, at the same commit, exits with 13 contradictions over the round 53 set and ZERO over the corrected one, which is the discriminator a guard needs: a guard seen only to pass is not evidence, and one that can only fail is the same defect from the other side. The 277 refusals do not move, and that is stated rather than smoothed over — the corrected set removes what the check DECIDES against and never what it declines to decide.

CHOSEN, PART THREE, AND IT IS THE RULING: THE CORRECTED SET IS THE FLIP'S INPUT. Run as a third arm through the same guarded transform of DECISION F275 D43, at `ef75e213`, against the same unflipped control as round 76's two arms and differing from them in the ruled site set alone, it reads 1174 failed and 31 errors for 1204 bad nodes, against 1227 for the round 53 set and 1361 for the plain set. AGAINST THE SET THE TRANSFORM CONSUMES TODAY IT FIXES 23 TEST NODES AND BREAKS NOT ONE, and that is a set difference rather than a smaller total: every node bad under the corrected arm is also bad under the round 53 arm, so nothing is being traded. In the residue `Mission.job_id` goes from 22 location frames to none and `QueueEntry.job_id` from 5 to none, `Artifact.job_id` falls from 25 to 12, and the under-selection class stays empty where the plain set put 231 frames in it.

CHOSEN, PART FOUR: `R-0880` IS NOT RESOLVED AND THE REASON IS THE NINETEEN. The finding's first obligation — bound the over-selection statically — is now discharged twice, by DECISION F275 D44's static bound and behaviourally here. Its second asks the transform to REFUSE a site whose owner verdict cannot be confirmed, and 19 over-selection frames survive the corrected set, on `Artifact` at 12, `BrainNode` at 6 and the `_FakeJob` test double at 1. Those are classes the owner check refuses rather than decides, which is the 277-site blind spot DECISION F275 D45 ruled acceptable showing through exactly where it said it would. A finding whose defect is still reachable is OPEN, and no id is minted for the 19: item 30 of `docs/agents/planner_reviewer_prompt.md` §3 requires the open set to be searched for the DEFECT before an id is spent, and that search returns `R-0880` itself.

ALTERNATIVES CONSIDERED. Flipping on the round 53 set as it stands was rejected on this round's own numbers: it carries 59 over-selection frames into the one commit this feature cannot split, and a strictly better input now exists at the cost of one set subtraction. Widening the owner check until it decides the 19 was rejected, and rejected on the reasoning DECISION F275 D45 already recorded rather than freshly: a method that refuses 277 sites cannot be made to decide them by being asked more firmly, and a guard keyed on its refusals would stop every run it is given. Carrying the 19 back to their sites inside this round was rejected as scope — it is a second instrument and a second proof, and the owner check answered the question this round asked without it. Resolving `R-0880` was rejected because its second obligation is unbuilt and its defect is still reachable. Minting a new id for the 19 was rejected under item 30.

CONSEQUENCE. The flip round's input is fixed and on disk, and the flip's obligations are unchanged: DECISION F275 D48 as corrected by D49 keeps the full suite as the backstop, read for its failures rather than its exit code, and the thin set is re-derived before the flip with any site fallen to zero witnesses treated as a stop. The 19 are the next round's work and they are the residue `R-0880`'s second obligation names. Nothing here touches the id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse, which is production work no round has started, and no production line moved in the round that recorded this.

HOW TO REVERSE. Delete this paragraph block. DECISION F275 D50 then stands with its partition still an inference and the flip has no ruled input, the corrected set and the artefact stay on disk, and the next session re-reads the 23-fixes-and-0-breaks result out of the artefact rather than re-measuring it in a further suite pass. Every figure above is re-derivable by the committed instrument against `ef75e213`, except the three this decision quotes from round 76 in order to compare against them.
END DEC77
