# STEP T003 — F275 ROUND 76 — the flip's dry run against the corrected inputs, and neither set is its input

## Goal

Take the flip's dry run that DECISIONs F275 D41, D42 and D44 each deferred by name, against the
corrected inputs of rounds 67 and 69 together, and read what they cost in FAILURES rather than
in sites. The answer is that the round 67 plain re-derivation is a strict subset of the round
53 committed set which costs 134 additional bad test nodes, because it removes every production
record class `R-0880` names from the residue and introduces a larger under-selection class in
their place. The two sets are wrong in opposite directions and the flip's input is neither.
DECISION F275 D50 records that. Book the round 75 PASS verdict and its two prose slips. NO
PRODUCTION LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r76.md`
- C0b save the artefact as authored text — `.agent/authored/f275-r76-artefact.md`
- C0c save the instrument carrier as authored text — `.agent/authored/f275-r76-instrument.py.md`
- C0d mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 76 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 75 reviewer verdict — `.agent/live_review.md`
- C3 append the round 75 prose slips — `.agent/prose_slips.md`
- C4 record DECISION F275 D50 — `.agent/decisions.md`
- C5 land the residue artefact — `.agent/f275_t003_flip_residue_r76.md`
- C6 the round 76 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r76.md
    .agent/authored/f275-r76-artefact.md
    .agent/authored/f275-r76-instrument.py.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/decisions.md
    .agent/f275_t003_flip_residue_r76.md
    .agent/handoff.md

No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` is touched. This is not a
deletion round and no file is removed. NOTHING LANDED BY AN EARLIER ROUND IS REWRITTEN OR
REVERTED: DECISION F275 D48 and DECISION F275 D49 stay exactly as they are on disk, and D50 is
an append beside them rather than an edit of either.

## The reviewer's texts on disk, and how they travel

Every reviewer-authored text of this round exists as a file under the gitignored `.remedy-wt/`
at this round's base, and each is of one of two kinds. A SLICE is carried verbatim in this
block between a BEGIN and an END marker, the BEGIN marker stating the sha256 of the bytes
between them; the slices are PLAN76, RECORD76, SLIPS76 and DEC76, each under its own heading
below. A WHOLE TEXT is too long to retype and is never retyped: it is transported with
`shutil.copyfile` and never opened in an editor. The whole texts, with their scratch paths and
digests:

    .remedy-wt/f275-r76-artefact.md         16247 bytes  b4744c01a8342863f4770541239cac4796432eb9593da1ee9734c81b38ce6dc7
    .remedy-wt/f275-r76-instrument.py.md    18628 bytes  9c1c1f4f1c3f84ff681b8867d443689715883083a81c7f7f3e38f8f0197d6e08

The block travels the same way: read `.remedy-wt/f275-r76.block.md` from disk, verify its
sha256 against the one the delegation wrapper states, and copy it to
`.agent/authored/f275-r76.md` at C0a and to `.agent/last_block.md` at C0d. A slice is applied
BYTE FOR BYTE: nothing is reflowed, re-wrapped, re-indented or corrected, and a slice that
looks wrong is APPLIED AS WRITTEN and declared in the handback.

## Constraints

1. APPLY EVERY SLICE VERBATIM. Extract each by its BEGIN and END marker prefixes, markers
   EXCLUDED, from the COMMITTED C0a blob — never from the delegation prompt and never from
   memory — and check each against the sha256 its own BEGIN marker carries before applying it.
2. PLAN76 is a WHOLE-FILE REPLACEMENT of `.agent/plan.md`. RECORD76, SLIPS76 and DEC76 are
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
5. THIS ROUND'S INSTRUMENT NEEDS NO WORKTREE AND RUNS NO TEST, which is a difference from the
   last several rounds and is deliberate: it re-analyses SAVED transcripts and SAVED site sets
   and is therefore deterministic. The reviewer's three pytest passes and four worktrees that
   produced those transcripts are already done, and their worktrees were removed and pruned
   before this block was authored. The ONLY disposable worktree this round needs is the one
   G3(iii) creates for its negative control, and that worktree is removed and pruned by the
   same script. `git status --porcelain` is the empty string at every commit and at the
   handback.
6. NO `gh` COMMAND AND NO `remedy` CLI COMMAND IS RUN. No pull request is created, edited or
   merged. No branch is created. No merge. No force-push. Push the branch after C6.
7. READ `.agent/STOP` FROM DISK before the first commit and again before C6, by BOTH
   `os.path.exists` and `glob`, and report both readings literally in the handback. If it
   exists, finish the commit in hand, write the handback and stop.
8. THIS BLOCK'S OWN SIZE. Measured by the reviewer on the FINAL bytes of
   `.remedy-wt/f275-r76.block.md`: TOTAL 385 lines, PROSE 308 lines, where PROSE is
   TOTAL minus the lines lying between BEGIN and END markers, markers themselves counted as
   PROSE. This clause is the ONLY place either numeral appears; G1 names this clause rather
   than restating them.
9. `R-0880` STAYS OPEN. No finding id is registered, resolved or de-registered this round. Do
   not write a `Done:` or a `Landed:` paragraph of your own; `Done:` is reviewer-authored text
   only. The SLIPS76 lines are not ids, per amend0827-process-diet rule 2.
10. NO `.py` FILE IS CREATED ANYWHERE UNDER `.agent/`. The instrument ships as a `.py.md`
    carrier, because a `.py` file inside the tree is counted by the `ruff` ceiling that
    `tests/orchestration/test_ci_budgets.py` freezes and G6(c) reads.
11. EVERY GATE IS RUN AS `bash -c '<cmd> > <out> 2>&1; echo "REAL_EXIT=$?" >> <out>'` AND THE
    EXIT CODE IS READ BACK OUT OF THE FILE. Write transcripts under `.remedy-wt/`. "Green" as
    a word is a finding; the recorded number is the evidence.
12. THE INSTRUMENT'S INPUTS ARE NINE SCRATCH FILES AND NONE OF THEM IS REGENERATED. The
    instrument names them itself, with their sizes and sha256 values, in its own section 0.
    Before running it, check every one of those nine against the digest the instrument prints
    for it; if any file is missing or differs, STOP and hand back, and do not rebuild it. Three
    of them are pytest transcripts of roughly twenty minutes each and cannot be re-taken inside
    this round.
13. NO GATE BELOW DEMANDS THAT A WHOLE-SUITE RUN BE GREEN, and no gate below runs the suite at
    all. The readings this round turns on are DIFFERENCES between two runs of the same
    selection, taken by the reviewer before this block existed and fixed in the transcripts
    constraint 12 pins.
14. THE THREE SUITE SUMMARY LINES THE INSTRUMENT PRINTS CARRY WALL-CLOCK DURATIONS AND THE
    ARTEFACT QUOTES NONE OF THEM. That is why G4(e) can still demand zero: the artefact takes
    its failure counts from the instrument's node-id lines instead, which carry no duration.
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
constraint 15 fixes at zero. REPORT THE LINE COUNT OF EVERY BLOB THIS ROUND CREATES against
500, the DECISION F104 D1 insertion cap — for a file the commit CREATES the two are the same
number. Finally, for the `.py.md` carrier: report the number of ```python fence lines and of
bare ``` lines, both of which must be 1; extract the source; and confirm that re-wrapping it in
the carrier's own header and fence reproduces the committed blob BYTE FOR BYTE.

**G2 THE PLAN.** `.agent/plan.md` at C1 is byte-identical to slice PLAN76 — report both sizes
and both sha256 values. Report its line count against the AGENTS.md cap of 50, and the count of
lines matching `^## Goal$` and of lines matching `^## Next Steps$`, both of which are 1.

**G3 THE RECORD.** Three appends, three commits, and for each one TWO INDEPENDENT READERS and
a NEGATIVE CONTROL. Wherever a reading below is taken AT THE BASE, read those bytes with
`git show ef75e213:<path>` into scratch or into memory; nothing is written over a tracked file
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
       Choose an ASCII letter, so the flip cannot land inside a multi-byte sequence. Remove and
       prune that worktree in the same script and report `git worktree list` afterwards.
  (iv) Over RECORD76: report its line count, the number of lines AFTER THE FIRST carrying a
       reserved prefix (`- R-`, `Done: R-`, `Landed: R-`, `Gate: `), which is 0, and the number
       of lines C2 ADDS matching `^- R-` and matching `^Done: R-`, both of which are 0.
  (v)  RECORD76's first line joins a repeating record format, so compare it MECHANICALLY
       against its neighbours: report how many lines at the base already match
       `^Gate: F275 R\d+ — the F275 round \d+ entry\.`, whether the new first line matches that
       same pattern, and whether it duplicates any of them.
  (vi) Over DEC76: confirm it begins `## DECISION F275 D50 `, report how many lines at the base
       match `^## DECISION F275 D50` (which is 0), and report the highest existing
       `^## DECISION F275 D\d+` at the base. Then confirm that C4 REMOVES NO LINE — that its
       `git show --numstat` deletion column is 0.
  (vii) Over SLIPS76: report the number of paragraphs it adds, how many begin
       `2026-09-12 · F275 R75 · `, and how many lines at the base already begin with that exact
       prefix.

**G4 THE ARTEFACT AND ITS TRANSCRIPT.**

  (a) `.agent/f275_t003_flip_residue_r76.md` at C5 is byte-identical to the C0b blob — report
      both sizes and both sha256 values — and the path does not resolve at the base with
      `git show ef75e213:.agent/f275_t003_flip_residue_r76.md`, whose non-zero exit is the
      expected reading.
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
      lines matching `in \d+\.\d+s`, which is 0. Constraint 14 states why that is attainable
      this round even though the instrument prints three such lines.
  (f) Report, for EVERY commit C0a through C5, the INSERTION count from `git show --numstat
      <sha>` — the `+` column DECISION F104 D1 caps at 500 — with the number of paths that
      commit stages, which is 1 for each, and whether each insertion count is under 500.

**G5 THE INSTRUMENT.** Read constraints 12 and 13 before starting this one.

  (a) Extract the single fence of the COMMITTED C0c carrier to
      `.remedy-wt/f275-r76-instrument.py` and report the extracted size and sha256.
  (b) Run `python3 -B .remedy-wt/f275-r76-instrument.py .remedy-wt` and REPRODUCE EVERY LINE OF
      EVERY SECTION in the handback.
  (c) DETERMINISM: run it THREE times and report the sha256 of stdout for each run and whether
      all three are identical. A reading this round turns on that is not byte-stable is a RED
      gate, because the artefact quotes it line by line.
  (d) THE READINGS THIS GATE TURNS ON, each reported with whether it holds. The instrument
      labels its own arithmetic in two kinds and the difference is the point: a CROSS-CHECK
      compares two numbers reached by different routes and CAN fail, a PARTITION adds a set's
      own parts back to the set and cannot. Report the number of lines containing `MISMATCH`,
      which must be 0. Report the number of `CROSS-CHECK` lines and the number of `PARTITION`
      lines, both of which you MEASURE rather than take from this block, and report section
      8's own `FAILING` counts, both of which must be 0, and its `EVERY CHECK HOLDS` line,
      which must read True. Then, by section: in section 0, that each input file named is
      present at the size and sha256 printed for it — constraint 12; in section 3, that the
      CONTROL reads 1 failed node and 0 error nodes; in section 5, that
      `every one of them is named by R-0880: True` appears TWICE, once per arm. On any red
      here, stop and hand back.
      A NOTE ON WHY THIS GATE IS WORDED THAT WAY, because it is the repair of a defect this
      block's own author shipped and caught. An earlier edition of the instrument printed only
      partitions, and a control that deleted a single `FAILED` line from one transcript left
      every one of them reading MATCH — a gate that could not fail. The cross-checks were added
      for that reason and the first run of them found a real defect in the instrument's own
      parser. A gate that turns on `MISMATCH` alone would still pass an instrument that checks
      nothing, which is why the COUNT of cross-checks is reported too.
  (e) Report `git status --porcelain` and `git worktree list` AFTER this gate.

**G6 THE TREE DID NOT MOVE.**

  (a) Report the `git rev-parse` object id of `packages`, `apps`, `tests`, `docs` and `scripts`
      at the base `ef75e213` and at C5, and whether each pair is EQUAL.
  (b) THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`, reporting the tail of
      its output and its real exit code.
  (c) `python3 -m ruff check . --output-format concise`. Its exit is 1 whenever any finding
      remains, so THE GATE IS THE COUNT: report the number of rows matching `^\S+:\d+:\d+: `,
      which must equal the ceiling `tests/orchestration/test_ci_budgets.py` freezes; the number
      of rows whose path lies under `.remedy-wt/`, counted rather than grepped; and the number
      of rows whose path ends `.py` under `.agent/`, which constraint 10 fixes at 0. Run it
      AFTER G3(iii) has removed and pruned its worktree.

**G7 NOTHING ELSE MOVED.**

  (a) `.agent/STOP` exists on disk: report the boolean. `git status --porcelain | cat -A`:
      report it literally. `git worktree list`: report every entry and their number, which is
      1, the primary checkout alone.
  (b) The changed paths over `ef75e213`..C5: report how many, and report MISSING and EXTRA
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
NUMBER of the running feature, which is 27, and the round, which is 76. One line per gate with
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

## SLICE PLAN76 — whole-file replacement of `.agent/plan.md`, applied at C1

BEGIN PLAN76 sha256=1d9ed208a90e8b244d3fd57f180fc5c0428680b8d904d533daa128088bd3f7e4
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

ROUND 76 TAKES THE FLIP'S DRY RUN AGAINST THE CORRECTED INPUTS OF ROUNDS 67 AND 69 TOGETHER,
which DECISIONs F275 D41, D42 and D44 each deferred by name, and the answer is that NEITHER
SET IS THE FLIP'S INPUT. The two arms differ in the ruled site set alone. The round 67 plain
re-derivation is a strict subset of the round 53 committed set, 60 sites smaller, and it costs
134 additional bad test nodes: it breaks 172 and fixes 38. The cause is measured rather than
inferred — it removes every production record class `R-0880` names from the residue, 59
over-selection frames falling to 1, and introduces 231 under-selection frames where the round
53 set has none. DECISION F275 D50 records the route. The round 75 verdict and its two prose
slips are booked.

## Next Steps

1. Partition the 60 dropped sites into correctly and wrongly dropped, by carrying each
   over-selection frame back through the re-key to the ruled site that produced it. That
   partition IS the flip's input set, and this round establishes that such a set exists.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
3. THE FLIP, on the partitioned set, carrying DECISION F275 D48's obligations: the full suite
   is the backstop, and the thin set is re-derived before the flip with any site fallen to
   zero witnesses treated as a stop.
4. Then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- THE FLIP'S INPUT SET IS WRONG IN BOTH DIRECTIONS and this round is the first to measure
  both in one pass. Neither arm is near green: 1227 bad nodes under the better of the two.
- A UNIT IS PART OF A NUMBER. This round counts LOCATION FRAMES where `R-0880` counts
  `E <Exc>` lines, and says so rather than comparing the two figure for figure.
- The open set is 87 by distinct id, with `R-0880` open. Four are High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN76

## SLICE RECORD76 — appended to `.agent/live_review.md` at C2

BEGIN RECORD76 sha256=b761ef7d9bfbad2e0f0d1084e286c7572d4e885cbe4bbdc39264ccc88c4096bc
Gate: F275 R75 — the F275 round 75 entry. VERDICT PASS. Written by the planner and reviewer of session 26 after reading the committed range `dac50bcd`..`90c81f42` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 76, per operator amendment amend0827-process-diet rule 1, from `.agent/handoff.md` at `ef75e213` as the durable carrier that rule names.

WHAT THE TRANSPORT PROOF COVERS, STATED BEFORE THE FIGURES, per item 37 of `docs/agents/planner_reviewer_prompt.md` §3. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: the chain it walks is the reviewer's own scratch original, the committed `.agent/authored/` blob and the working copy — three artefacts, of which the first is the reviewer's and the other two the worker's. It does not and cannot establish what bytes the worker RECEIVED. All three authored blobs are byte-identical to the reviewer's originals — the block at 36374 bytes, the artefact at 4739 and the instrument carrier at 14692 — and `.agent/last_block.md` equals the block blob. Four slices matched the sha256 on their own BEGIN markers, the block re-measures at 378 lines TOTAL and 305 PROSE as its constraint 8 states, it carries zero repeated-character lines, and the carrier round-trips through its own fence byte for byte.

G2: `.agent/plan.md` byte-identical to PLAN75 at 48 lines against the cap of 50. G3: the three appends exact under reader A with the slice an exact suffix after one newline, reader B holding at N counted from the slice as 6, 2 and 6, all three of the reviewer's negative controls on the FIRST appended paragraph REJECTED by both readers, and C4's deletion column ZERO — so DECISION F275 D48 is corrected by APPEND and not rewritten, which is the property this round was built around. G4: the artefact byte-identical to the C0b blob and absent at the base, its 15 quoted lines all present in the instrument's output, the matching monotone with indices strictly increasing, zero unmatchable, zero lines carrying a wall-clock duration, zero three-backtick lines; every commit stages exactly ONE path with insertions peaking at 378 and none at or over the 500 cap. G6 and G7: five top-level trees byte-identical across the round's eleven mutations, `git status --porcelain` the empty string, one worktree, nine changed paths with MISSING and EXTRA empty and zero production paths, the open set 87 with identical membership at the base, at C5 and at the tip, and `R-0880` open at each.

THE READING THE ROUND EXISTS FOR IS ARITHMETIC AND IT HOLDS IN BOTH UNITS. The witness buckets sum to 166 against a stated distinct-LINE total of 166, and to 175 against a stated production-SITE total of 175, with the difference of 9 matching the separately printed count of sites sharing a line. That is the check nothing else in this workflow can make: a wrong unit is invisible to every digest, byte-equality and transcript gate, and only adding the numbers up sees it. The risk set is 0 in both units, the thin set is 11 lines carrying 11 sites, and all eleven are still red-proved against their own single witnesses.

TWO SLIPS OF THE REVIEWER'S, BOTH FOUND BY THE WORKER, and both are dated lines in `.agent/prose_slips.md` rather than ids, per amend0827-process-diet rule 2: nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong. The block's Handback section said "the round, which is 74" while the block's own title, its C6 bundle line and its PLAN75 slice all say 75 and the round's base commit is itself round 74's handback; the worker wrote 75, which is right, and declared the block's numeral with the measurements that show it rather than fixing it silently. And G4(d) listed the artefact's citation kinds as "section, commit or source line" while the artefact's own provenance clause says "round or section", so the gate was wider than the document it checked — one digit run was affected, `50`, out of the commit id `dac50bcd`.
END RECORD76

## SLICE SLIPS76 — appended to `.agent/prose_slips.md` at C3

BEGIN SLIPS76 sha256=85d0b30210dd4dbbe896ce10d4be261c2ec84ccb220789c9b5c3ad2c53804fbf
2026-09-12 · F275 R75 · The round 75 block was retargeted from the round 74 block by textual substitution, and its Handback section kept "the round, which is 74" because that numeral is bare — the substitution matched the phrase "round 74" and a lone "74" after a comma is not that phrase. The block's title, its C6 bundle line and its own PLAN75 slice all said 75, and the round's base commit is itself the round 74 handback, so three independent readings contradicted the fourth. The worker wrote 75 and declared the block's numeral rather than fixing it silently, which is right. THE RULE THAT FOLLOWS: a block derived from a previous block by substitution is swept for EVERY BARE NUMERAL of the old round before emission, not only for the phrases that name it — the retarget's own diff against its source is the sweep, read hunk by hunk, because a substitution's misses are exactly the places the diff stays unchanged.

2026-09-12 · F275 R75 · The round 75 block's G4(d) ordered every unresolved prose figure classified as "a CITATION of a named decision, finding, round, section, commit or source line", while the artefact's own provenance clause names only "a named decision, finding, round or section". The gate is therefore WIDER than the document it checks, and a figure the gate would accept as a commit citation is one the artefact never licensed itself to carry; one digit run was affected, `50` out of `dac50bcd`. This is the third round in four whose defect is a provenance enumeration disagreeing with something — twice the artefact's list was short of its own contents, and now the gate's list is long of the artefact's. THE RULE THAT FOLLOWS: the gate that checks a provenance clause QUOTES that clause's own words for its list of kinds rather than restating them, so the two cannot drift; where the gate must paraphrase, the block says which document is authoritative.
END SLIPS76

## SLICE DEC76 — appended to `.agent/decisions.md` at C4

BEGIN DEC76 sha256=25d69af1f1248fc1384a4a7c8b24fc3c6fc3eb2f4061651dc7cfc5f150126a71
## DECISION F275 D50 (2026-09-12, F275 round 76) — the flip's input is NEITHER the round 53 committed set nor the round 67 plain re-derivation, because the two are wrong in opposite directions, and the set the flip needs lies between them

CONTEXT. DECISION F275 D41's alternative (iii) deferred re-running the flip's dry run against the plain re-derived set, on the ground that its reading was only meaningful once the 54 non-resolving keys were ruled. DECISION F275 D42 ruled them and closed by recording that the run had still not been taken. DECISION F275 D44's consequence paragraph repeated the same sentence for the corrected inputs of rounds 67 and 69 together, and `.agent/plan.md` has carried it as item 1 ever since. This round takes it. The measurement is in `.agent/f275_t003_flip_residue_r76.md` and the instrument is committed at `.agent/authored/f275-r76-instrument.py.md`; every figure below is re-derivable by that instrument from the transcripts its own section 0 pins by sha256.

CHOSEN, PART ONE: THE COMPARISON IS ONE-VARIABLE AND ITS CONTROLS REPRODUCE. Both arms ran the guarded transform DECISION F275 D43 landed, at `ef75e213`, over the same 994 tracked `.py` files, with the same status input, differing in the RULED SITE SET alone. Three controls hold and they were taken because a rebuild whose predecessor's figures it cannot reproduce is measuring two things at once. The `packages`, `apps`, `tests`, `docs` and `scripts` tree object ids are identical at `bf692757`, round 59's base, and at `ef75e213`, and the 994 tracked `.py` files are identical between them, so round 59's run is comparable to this one at all. The re-key stage run here against the round 53 set reproduces `.remedy-wt/r69_rekeyed.json` BYTE FOR BYTE. And the round 53 arm's transform reproduces round 69's own figures exactly, at 263 files rewritten and 6091 rewrites. The unflipped control reproduces round 59's to the unit, at one failure, and that one failure is the node needing the gitignored `apps/ui/node_modules`, which is subtracted from both arms rather than argued away.

CHOSEN, PART TWO: THE PLAIN SET IS A STRICT SUBSET AND IT COSTS FAILURES. It holds 2138 sites against the round 53 set's 2198, drops 60 and adds none; 35 of the 60 are in production files and 25 in test files. Sixty fewer ruled sites buy 59 fewer renames and 59 more undecided sites, the missing one being the single site carrying no owner verdict, which the transform leaves alone whether or not the set holds it. In the suite the plain arm reads 1361 bad nodes against the round 53 arm's 1227 — it BREAKS 172 nodes and FIXES 38, for a net cost of 134.

CHOSEN, PART THREE, AND IT IS THE RULING: THE TWO SETS ARE WRONG IN OPPOSITE DIRECTIONS AND BOTH ERRORS ARE NOW MEASURED IN ONE PASS. Under the round 53 set the under-selection class is EMPTY and the over-selection class on a named receiver class stands at 59 location frames over six kinds — `Artifact.job_id` 25, `Mission.job_id` 22, `BrainNode.task_id` 5, `QueueEntry.job_id` 5, `BrainNode.job_id` 1 and `_FakeJob.job_id` 1 — every one of them a class finding `R-0880` names, which the instrument checks as a set containment rather than by eye. Under the plain set that class falls to a single frame, on the test double `_FakeJob`, and every production record class disappears; in the same run the under-selection class rises from nothing to 231 frames, `TaskEntry.id` at 224 and `JobPlan.id` at 7, each one a classic field read left standing on a record whose field the flip has already renamed. SO THE FLIP'S INPUT IS THE ROUND 53 SET MINUS THE SITES THE PLAIN RE-DERIVATION IDENTIFIES AS OVER-SELECTED — a set strictly between the two — and the plain re-derivation is the first mechanism this chain has found that locates those sites at all. It is a DIAGNOSTIC for `R-0880`, not a replacement input.

CHOSEN, PART FOUR: THE UNIT IS NAMED BECAUSE THE LAST TWO ROUNDS WERE SPENT ON EXACTLY THAT MISTAKE. The figures above are LOCATION FRAMES of a `--tb=line` report. `R-0880`'s own measurement counts `E <Exc>: <msg>` lines, and section 8 of `.agent/f275_t003_flip_residue_r59.md` already recorded that those two readings disagree to the unit even within one run. No claim is made here that the counts are comparable figure for figure with the ones on `R-0880`'s record; what is compared, and mechanically, is the SET OF CLASSES.

ALTERNATIVES CONSIDERED. Pointing the transform at the plain set and proceeding to the flip was rejected on this round's own numbers: it would land 231 half-flipped reads inside the one commit this feature cannot split, which is a worse outcome than the 59 wrong renames it removes, and it trades a bounded known defect for a larger one. Keeping the round 53 set and treating `R-0880` as accepted risk was rejected because the diagnostic now exists and is cheap: a finding that can be fixed is not accepted. Building the partition inside this round was rejected as scope rather than as unnecessary — it needs each over-selection frame carried back through the re-key into the ruled set's own coordinates, which is a separate instrument and a separate proof, and this round had already spent three full suite passes. Resolving `R-0880` here was rejected because nothing on disk changed: the over-selection is still in the set the transform consumes.

CONSEQUENCE. `R-0880` stays OPEN and its first obligation now has a second, independent line of evidence beside the static bound DECISION F275 D44 recorded: the plain re-derivation removes the class behaviourally, which the static pass could only bound. The next round partitions the 60 and that partition is the flip's input. No new finding id is minted, per item 30 of `docs/agents/planner_reviewer_prompt.md` §3, whose search over the open set was run before this decision was written and returned `R-0880` for the over-selection and nothing for the under-selection, which is not a defect on disk but a property of a set no round has consumed. Nothing here touches the id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse, which is production work no round has started, and no production line moved in the round that recorded this.

HOW TO REVERSE. Delete this paragraph block. DECISION F275 D44's consequence sentence then stands as the record's last word on the dry run, the artefact and the instrument stay on disk, and the next session re-reads the 172-and-38 reading out of the artefact rather than re-measuring it in three suite passes. Every figure above is re-derivable by the committed instrument against `ef75e213`, except the three this decision quotes from round 69 in order to state that they reproduced.
END DEC76
