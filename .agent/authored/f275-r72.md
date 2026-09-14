# STEP T003 — F275 ROUND 72 — shrink the owner check's refusal set

## Goal

Discharge the SHRINK half of the precondition DECISION F275 D45 put on the flip round: widen
the owner check's static resolver so the guard's reach approaches the ruled set it guards,
and gate that widening by a per-site comparison against the method it replaces rather than by
its own counts. Land the widened stage, the instrument that reads it against round 71's, the
artefact recording the measurement, and DECISION F275 D46. Book the round 71 verdict and its
prose slip. NO PRODUCTION LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r72.md`
- C0b save the artefact as authored text — `.agent/authored/f275-r72-artefact.md`
- C0c save the owner-check stage carrier — `.agent/authored/f275-r72-owner-stage.py.md`
- C0d save the instrument carrier — `.agent/authored/f275-r72-instrument.py.md`
- C0e mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 72 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 71 reviewer verdict — `.agent/live_review.md`
- C3 append the round 71 prose slip — `.agent/prose_slips.md`
- C4 record DECISION F275 D46 — `.agent/decisions.md`
- C5 land the owner-widening artefact — `.agent/f275_t003_owner_widening_r72.md`
- C6 the round 72 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r72.md
    .agent/authored/f275-r72-artefact.md
    .agent/authored/f275-r72-owner-stage.py.md
    .agent/authored/f275-r72-instrument.py.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/decisions.md
    .agent/f275_t003_owner_widening_r72.md
    .agent/handoff.md

No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` is touched. This is not a
deletion round and no file is removed.

## The reviewer's texts on disk, and how they travel

Every reviewer-authored text of this round exists as a file under the gitignored `.remedy-wt/`
at this round's base, and each is of one of two kinds. A SLICE is carried verbatim in this
block between a BEGIN and an END marker, the BEGIN marker stating the sha256 of the bytes
between them; the slices are PLAN72, RECORD72, SLIPS72 and DEC72, each under its own heading
below. A WHOLE TEXT is too long to retype and is never retyped: it is transported with
`shutil.copyfile` and never opened in an editor. The whole texts, with their scratch paths and
digests:

    .remedy-wt/f275-r72-artefact.md          11207 bytes  c30b23bb8d794ece0ffadfdb3ea06615bdbe3cf46357488228481667957c5bd2
    .remedy-wt/f275-r72-owner-stage.py.md    19931 bytes  f876cc405d4d8af0abcc0f7d2e31073c88bc7c2df1757d6233addbcac0089aab
    .remedy-wt/f275-r72-instrument.py.md      9089 bytes  1f81ad4cc969e6ee7743897340dc55dabcba4b762f6f2a6885d6e0792eab3894
    .remedy-wt/f275-r72.block.md                          this block itself, digest in the delegation wrapper

The block travels the same way: read `.remedy-wt/f275-r72.block.md` from disk, verify its
sha256 against the one the delegation wrapper states, and copy it to `.agent/authored/f275-r72.md`
at C0a and to `.agent/last_block.md` at C0e. A slice is applied BYTE FOR BYTE: nothing is
reflowed, re-wrapped, re-indented or corrected, and a slice that looks wrong is APPLIED AS
WRITTEN and declared in the handback.

## Constraints

1. APPLY EVERY SLICE VERBATIM. Extract each by its BEGIN and END marker prefixes, markers
   EXCLUDED, from the COMMITTED C0a blob — never from the delegation prompt and never from
   memory — and check each against the sha256 its own BEGIN marker carries before applying it.
2. PLAN72 is a WHOLE-FILE REPLACEMENT of `.agent/plan.md`. RECORD72, SLIPS72 and DEC72 are
   APPENDS: the pre-commit blob is a byte-exact PREFIX of the post-commit file and the slice
   is an exact SUFFIX of it, separated by exactly one newline.
3. ONE PATH PER COMMIT, in the Bundle's order. Run the AGENTS.md self-review loop before every
   commit: `git diff --cached --stat`, `--numstat` and the full `git diff --cached`. For a
   transport commit whose diff is a single large blob, review it structurally — one path, one
   hunk header, every content line an addition, and the resulting blob byte-equal to its
   scratch original by sha256 — and say so in the handback rather than printing the blob.
4. NO PRODUCTION PATH MOVES. If any gate below would require editing a file under `packages/`,
   `apps/`, `tests/`, `docs/` or `scripts/`, STOP and hand back instead.
5. DESTRUCTIVE AND SCRATCH WORK IS ISOLATED. Every worktree this round creates lives under the
   gitignored `.remedy-wt/` and is removed and pruned by the instrument that made it.
   `git status --porcelain` is the empty string at every commit and at the handback.
6. NO `gh` COMMAND AND NO `remedy` CLI COMMAND IS RUN. No pull request is created, edited or
   merged. No branch is created. No merge. No force-push. Push the branch after C6.
7. READ `.agent/STOP` FROM DISK before the first commit and again before C6, by BOTH
   `os.path.exists` and `glob`, and report both readings literally in the handback. If it
   exists, finish the commit in hand, write the handback and stop.
8. THIS BLOCK'S OWN SIZE. Measured by the reviewer on the FINAL bytes of
   `.remedy-wt/f275-r72.block.md`: TOTAL 349 lines, PROSE 277 lines, where PROSE is TOTAL
   minus the lines lying between BEGIN and END markers, markers themselves counted as PROSE.
   This clause is the ONLY place either numeral appears; G1 names this clause rather than
   restating them.
9. `R-0880` STAYS OPEN. No finding id is registered, resolved or de-registered this round. Do
   not write a `Done:` or a `Landed:` paragraph of your own; `Done:` is reviewer-authored text
   only. The SLIPS72 line is not an id, per amend0827-process-diet rule 2.
10. NO `.py` FILE IS CREATED ANYWHERE UNDER `.agent/`. Both python sources ship as `.py.md`
    carriers, because a `.py` file inside the tree is counted by the `ruff` ceiling that
    `tests/orchestration/test_ci_budgets.py` freezes and G6(c) reads.
11. EVERY GATE IS RUN AS `bash -c '<cmd> > <out> 2>&1; echo "REAL_EXIT=$?" >> <out>'` AND THE
    EXIT CODE IS READ BACK OUT OF THE FILE. Write transcripts under `.remedy-wt/`. "Green" as
    a word is a finding; the recorded number is the evidence.
12. THE INSTRUMENT'S INPUTS ARE CHECKED FOR EXISTENCE BEFORE IT IS RUN AND NONE IS
    REGENERATED. `.remedy-wt/r69_rekeyed.json` (121516 bytes, sha256
    489fdf8eeb9c4e66b452510de5d362e5d701b4cfe2de79d1d69b768f526d301f) and
    `.remedy-wt/r69_rekeyed_owners.json` (121858 bytes, sha256
    747e8f08c7e3dfc207510a0071d1fd196907ca34667d97baec7ab5028145f57f) must exist with those
    digests. If either is missing or differs, STOP and hand back; do not rebuild it.
13. THE ROUND 71 STAGE THE INSTRUMENT COMPARES AGAINST IS EXTRACTED FROM ITS COMMITTED
    CARRIER, not trusted from scratch. G5(a) orders that extraction and the comparison; the
    instrument reads `.remedy-wt/f275-r71-owner-stage.py`, so write the extraction there.
14. THE STAGE'S EXIT 5 IN THE REFUSE CASE IS THE PASS READING, NOT A RED GATE. The refusal is
    the deliverable. The GATE's exit code is the INSTRUMENT's, which is 0. Do not alter any
    ruled set to make the stage exit 0; the cleaned set is built by the instrument from the
    stage's own report.
15. THIS BLOCK CONTAINS NO LINE THAT IS A RUN OF A SINGLE REPEATED CHARACTER. G1 counts them
    and the expected count is zero, per item 37 of `docs/agents/planner_reviewer_prompt.md` §3.

## Done when — the gates below, all run at C5 before C6 exists

Every gate runs at C5, which is strictly earlier than the commit that writes the handback, so
the handback can quote every reading it states. The handback commit's own numbers are NOT a
gate of this round: the reviewer measures them at the next gate.

**G1 TRANSPORT AND THE BLOCK BUDGET.** For each of the five blobs C0a through C0e commits,
compare the committed bytes against the reviewer's scratch original by size and sha256 and
report EQUAL or not, naming the commit. `.agent/last_block.md` at C0e is compared against the
COMMITTED C0a blob. Then, over the committed C0a blob: extract every BEGIN/END slice, report
the CARDINALITY YOU MEASURED — the block states no numeral for it — and for each slice its
byte size, its line count and whether its content matches the sha256 on its own BEGIN marker.
Then re-measure TOTAL and PROSE as constraint 8 defines them, report both numbers you
measured, and report whether each equals the numeral constraint 8 states for it. Then report
the count of lines in the committed C0a blob
that consist of a single character repeated, which constraint 15 fixes at zero. Finally, for
each `.py.md` carrier: report the number of ```python fence lines and of bare ``` lines, both
of which must be 1; extract the source between them; and confirm that re-wrapping that source
in the carrier's own header and fence reproduces the committed blob BYTE FOR BYTE.

**G2 THE PLAN.** `.agent/plan.md` at C1 is byte-identical to slice PLAN72 — report both sizes
and both sha256 values. Report its line count against the AGENTS.md cap of 50, and the count of
lines matching `^## Goal$` and of lines matching `^## Next Steps$`, both of which are 1.

**G3 THE RECORD.** Three appends, three commits, and for each one TWO INDEPENDENT READERS and
a NEGATIVE CONTROL. Wherever a reading below is taken AT THE BASE, read those bytes with
`git show ae84d89c:<path>` into scratch or into memory; nothing is written over a tracked
file to take a base reading.

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
  (iv) Over RECORD72: report its line count, the number of lines AFTER THE FIRST carrying a
       reserved prefix (`- R-`, `Done: R-`, `Landed: R-`, `Gate: `), which is 0, and the number
       of lines C2 ADDS matching `^- R-` and matching `^Done: R-`, both of which are 0.
  (v)  RECORD72's first line joins a repeating record format, so compare it MECHANICALLY
       against its neighbours: report how many lines at the base `ae84d89c` already match
       `^Gate: F275 R\d+ — the F275 round \d+ entry\.`, whether the new first line matches that
       same pattern, and whether it duplicates any of them.
  (vi) Over DEC72: confirm it begins `## DECISION F275 D46 `, report how many lines at the base
       match `^## DECISION F275 D46` (which is 0), and report the highest existing
       `^## DECISION F275 D\d+` at the base.
  (vii) Over SLIPS72: report the number of paragraphs it adds, how many begin
       `2026-09-12 · F275 R71 · `, and how many lines at the base already begin with that exact
       prefix.

**G4 THE ARTEFACT.** `.agent/f275_t003_owner_widening_r72.md` at C5 is byte-identical to the
C0b blob — report both sizes and both sha256 values. Confirm the path does not resolve at the
base with `git show ae84d89c:.agent/f275_t003_owner_widening_r72.md`, whose non-zero exit is
the expected reading. Then report, for EVERY commit C0a through C5, the INSERTION count from
`git show --numstat <sha>` — the `+` column, which is the quantity DECISION F104 D1 caps at
500 — together with the number of paths that commit stages, which is 1 for each.

**G5 THE INSTRUMENT — THIS ROUND'S MEASUREMENT.**

  (a) FIRST, anchor the comparison. Extract the single fence of the COMMITTED round 71 carrier
      at `ac7fa202:.agent/authored/f275-r71-owner-stage.py.md` to
      `.remedy-wt/f275-r71-owner-stage.py`, and report the extracted size and sha256. It is
      8134 bytes with sha256
      dabbdf6657c1fe444eacb1f41d22aa33bd1e290560422eaacf0d0bb341079d81.
  (b) Extract the single fence of the COMMITTED C0d carrier to
      `.remedy-wt/f275-r72-instrument.py`, report its size and sha256, and likewise extract the
      COMMITTED C0c carrier to `.remedy-wt/f275-r72-owner-stage.py`. Then run
      `python3 -B .remedy-wt/f275-r72-instrument.py . ae84d89c` and REPRODUCE EVERY LINE OF
      EVERY BANNER in the handback.
  (c) THE READING THE ROUND TURNS ON is section 3 of that output: of the sites the round 71
      method DECIDED, the number round 72 no longer decides and the number it decides
      DIFFERENTLY are BOTH ZERO, and the number of sites round 72 decides that round 71 refused
      equals the fall in the refusal count. Report those four lines and say whether each holds.
      A non-zero value in either of the first two is a RED gate: stop and hand back.
  (d) THE TRANSCRIPT. In the C0b artefact blob, report the number of lines consisting of three
      backticks, which is 0; then check EVERY line that begins with whitespace and is not blank
      against the instrument's output, reporting how many you checked and how many have no
      stripped-equal line in that output.
  (e) THE ORDER PROPERTY as a MONOTONE MATCHING over those same quoted lines: report how many
      matched in order, how many were unmatchable, whether every quoted line matched, and
      whether the matched indices strictly increase.
  (f) DETERMINISM: run the instrument three times, reporting the byte size of its stdout and of
      its stderr for each run and whether all three stdout captures are byte-identical.
  (g) THE FIGURES: sweep every maximal digit run over the artefact's PROSE — its lines that do
      NOT begin with whitespace — reading the artefact AS A WHOLE rather than line by line, so
      a backtick span or a citation may open on an earlier line than the digits it encloses.
      Report how many runs you swept, how many occur as a digit run in the instrument's output,
      and how many do not. For each that does not, report it with the line that uses it and say
      which of the artefact's two declared kinds it is — a CITATION of a named decision,
      finding, section or specification, or a figure of one of the TWO DISCARDED DRAFTS. The
      artefact's provenance clause declares exactly those two kinds and no third.

**G6 THE TREE DID NOT MOVE.**

  (a) Report the `git rev-parse` object id of `packages`, `apps`, `tests`, `docs` and `scripts`
      at the base `ae84d89c` and at C5, and whether each pair is EQUAL.
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
  (b) The changed paths over `ae84d89c`..C5: report how many, and report MISSING and EXTRA
      against the Change section's path set, both of which are empty. Report the number of
      those paths lying under `docs/`, `scripts/`, `packages/`, `apps/` or `tests/`, which is 0.
  (c) THE OPEN SET BY DISTINCT ID: every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
      line, computed at the base and at C5. Report registered, resolved and open at each end;
      the ids REGISTERED, RESOLVED and DE-REGISTERED, all three of which are empty; whether the
      open membership is IDENTICAL at both ends; the highest open id at each end; and whether
      `R-0880` is open at each end, which constraint 9 requires.

## Handback

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`. It carries the SESSION
NUMBER of the running feature, which is 26, and the round, which is 72. One line per gate with
its REAL_EXIT read out of its transcript file. A per-commit table in the `## Commits` section
docs/agents/handback_template.md mandates, whose `+/-` column is read from
`git show --numstat <sha>` and from no other source — that column is an INSERTION and DELETION
count, never a file's line count — and whose insertion cell for each of C0a through C5 is
compared against the number G4 reports for that same commit, cell by cell, with the comparison
stated. The item-status table covers every C and every G exactly once. State the context self-assessment amend0905-throughput requires, in one sentence.
Declare every deviation. F275 stands past the soft limit amend0908-f275-finish rule 1 names, so
the handback carries the line `SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE`, and
the SCOPE REPORT that rule obliges was written in round 51's handback and STANDS — do not
restate it. Push after C6.

## SLICE PLAN72 — whole-file replacement of `.agent/plan.md`, applied at C1

BEGIN PLAN72 sha256=56bf032d7de0034c1c0e7d5a9c59816763f827d0a51c89c4238854d3f8ddc060
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

ROUND 72 SHRINKS THE OWNER CHECK'S REFUSAL SET, which DECISION F275 D45 made a precondition
on the flip. Seven resolution rules join the static method — return types across files, the
single-constructor return, container field element types, PEP 604 and mapping annotations,
`with`/walrus, aliases, file-wide agreement — each refusing on ambiguity rather than
guessing. Refusals go 999 to 324, confirmations 1195 to 1861. The widening is gated by a
PER-SITE decision-map diff and not by its own counts: every site round 71 DECIDED, round 72
decides the SAME WAY, none dropped. It finds NINE contradicted sites round 71 could not see,
all real. `R-0880` stays open, the residual is 324, and D45's precondition is not discharged.

## Next Steps

1. RULE THE RESIDUAL OR SHRINK IT AGAIN, the two routes D45 leaves open for the flip round.
   The largest remaining class is 113 receivers that are not a bare name, which no binding
   rule reaches, so the route from here is a different method rather than another rule.
2. Re-run the flip's dry run against the corrected inputs of rounds 67 and 69 together — the
   plain re-derivation and the re-keyed set — the first reading of what both corrections
   cost in FAILURES rather than in sites.
3. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
4. THE FLIP, which D45 forbids until the residual is shrunk or ruled on the record, then
   the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- A WIDER RESOLVER CAN BE WRONG WHERE A NARROW ONE WAS ONLY SILENT, AND ITS OWN COUNTS
  CANNOT SEE IT. Two drafts of this round's stage were discarded; the second passed every
  count-shaped check while destroying 327 correct decisions. Only a per-site diff caught it.
- Two refusal stages stand between the measured set and the transform and NEITHER has a test
  behind it: the flip is unlanded, so there is no production surface to pin one to.
- The open set is 87 by distinct id, with `R-0880` open. Four are High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN72

## SLICE RECORD72 — appended to `.agent/live_review.md` at C2

BEGIN RECORD72 sha256=c3efee670b7e3c718d9f3461d2699762bd9c592febdb33d76076d63cf91ab949
Gate: F275 R71 — the F275 round 71 entry. VERDICT PASS. Written by the planner and reviewer of session 25 after reading the committed range `3c59e51b`..`5e7114e6` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 72, per operator amendment amend0827-process-diet rule 1. The round built finding `R-0880`'s second obligation at the reach its method has and recorded, as DECISION F275 D45, why the literal obligation cannot be built at all.

WHAT THE TRANSPORT PROOF COVERS, STATED BEFORE THE FIGURES, per item 37 of §3. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback, and the chain it walks is the reviewer's own scratch original, the committed `.agent/authored/` blob and the working copy — three artefacts, of which the first is the reviewer's and the other two the worker's. It does not and cannot establish what bytes the worker RECEIVED, and no claim in this entry reaches that far. All four authored blobs are byte-identical to the reviewer's originals — the block at 34906 bytes, the artefact at 6699, the owner-check stage carrier at 8812 and the instrument carrier at 5234 — and `.agent/last_block.md` equals the block blob. Four slices matched the sha256 on their own BEGIN markers. Re-measured on the committed blob the block is 348 lines TOTAL and 274 PROSE, agreeing with its own constraint 8. Both `.py.md` carriers round-trip through their own fence, and re-wrapping each extracted source reproduces the committed blob byte for byte — the check round 69 lacked, held for a second round.

G2: `.agent/plan.md` byte-identical to PLAN71 at 3039 bytes over 49 lines against the cap of 50, both mandated headings exactly once. G3: `.agent/live_review.md` goes 1040150 to 1045796, `.agent/prose_slips.md` 265750 to 267150 and `.agent/decisions.md` 1175806 to 1180370, every one exact under reader A, with reader B holding at N counted from the slice as 7, 1 and 6, and all three of the reviewer's own negative controls — each placed on the FIRST appended paragraph, per item 36 of §3 — REJECTED by both readers while every unmutated region is ACCEPTED. Zero reserved-prefix lines after the entry header; the new header duplicates none of the 69 already matching the neighbours' pattern; `## DECISION F275 D45` reads 0 at the base against a highest existing D44. G4: the artefact at C5 is byte-identical to the C0b blob at 6699 bytes and the path does not resolve at the base. G6: five top-level trees byte-identical, canary 42 passed at exit 0, `ruff check .` 26 rows at the frozen ceiling. G7: ten changed paths with MISSING and EXTRA empty and zero production paths; the open set 87 at both ends with IDENTICAL MEMBERSHIP and registered, resolved and de-registered ALL EMPTY, `R-0880` open and `R-0879` resolved at each end; per-commit insertions peak at 348. The handback commit's own numbers, which no gate of that round could reach, are 377 insertions over ONE path, so DECISION F104 D1's exclusion applies by that decision's own wording.

G5 CARRIED THE ROUND AND ITS DECISIVE READING IS A PAIR OF EXIT CODES. The instrument extracted from one fence at 4563 bytes and ran to byte-identical 2533-byte captures with ZERO stderr at exit 0. The owner-check stage, over the set the pipeline holds, names FOUR ruled sites whose receiver statically resolves to a record its owner verdict does not name — one `Mission` and three `Artifact` — and exits 5. Over the same tree and the same stage, given that set with exactly those four removed, it exits 0. THE CONTROL THAT MAKES THAT A READING IS THAT CONFIRMED IS 1195 IN BOTH RUNS: removing four contradicted sites must not change what the method confirms, and it does not. The artefact's 25 quoted lines verify with 0 failed and 0 unmatchable under the monotone matching, indices strictly increasing, and zero three-backtick lines.

THE SUBSTANCE IS THAT A FINDING'S OWN FIX CLAUSE WAS MEASURED AND FOUND UNMEETABLE, AND THE ROUND SAID SO INSTEAD OF QUIETLY SHRINKING IT. `R-0880` asks for a run to stop on any ruled site whose owner verdict CANNOT BE CONFIRMED; the static method cannot confirm 999 of 2198, so that guard stops every run it is ever given — the gate that cannot pass, which item 33 of §3 names as the twin of the gate that cannot fail. DECISION F275 D45 narrows the obligation to sites the code CONTRADICTS, records what the narrowing costs, and makes the 999 a PRECONDITION ON THE FLIP ROUND rather than a silent inheritance: the flip may not be taken until the refusal set is shrunk or the residual is ruled acceptable in a dated decision that states the count it accepts. `R-0880` STAYS OPEN, which is the right disk state — the defect it names remains reachable among the 999, and a resolved finding is invisible while an open one is not.

ONE WORDING SLIP OF THE REVIEWER'S, WHICH THE WORKER REPORTED RATHER THAN RESOLVED. G4 ordered "the line count of every blob this round lands, each against the DECISION F104 D1 cap of 500 insertions". For the five NEW files a line count and an insertion count coincide; for the three ledger files this round APPENDS to they do not, and read widely the clause compares whole-file line counts of 1128, 891 and 13009 against a cap on insertions that are 14, 2 and 12. The worker reported both readings and reconciled neither, which is right. It is one dated line in `.agent/prose_slips.md` and not an id, per amend0827-process-diet rule 2: nothing on disk is wrong.
END RECORD72

## SLICE SLIPS72 — appended to `.agent/prose_slips.md` at C3

BEGIN SLIPS72 sha256=70224833de6843931ba5a908eae227e50bc0af7cd332fbe141c136e0c14e757c
2026-09-12 · F275 R71 · The round 71 block's G4 ordered "the line count of every blob this round lands, each against the DECISION F104 D1 cap of 500 insertions", and for the three ledger files the round APPENDS to, a blob's line count is not that commit's insertion count: read widely the clause sets 1128, 891 and 13009 against a cap whose real subject is 14, 2 and 12. For the five NEW files the two coincide, which is why the clause reads correctly for most of what it names and wrongly for the rest. The worker reported both readings and reconciled neither, and nothing on disk is wrong. THE RULE THAT FOLLOWS: a clause that bounds a COMMIT names the quantity the commit produces — insertions, from `git show --numstat` — and never a property of the FILE the commit touched, because the two coincide only for a file the commit creates, and a cap stated against the wrong quantity is unmeetable exactly where the file is oldest and largest.
END SLIPS72

## SLICE DEC72 — appended to `.agent/decisions.md` at C4

BEGIN DEC72 sha256=71e595e5d0f0aaf38056ae50a2fa2dd91d2309d484a1aec4a79c106a73cc4940
## DECISION F275 D46 (2026-09-12, F275 round 72) — the owner check's refusal set is shrunk from 999 to 324 by resolution rules that refuse on ambiguity, the widening is gated by a PER-SITE decision-map diff rather than by its own counts, and contradicted sites the narrow method could not see are now named

CONTEXT. DECISION F275 D45 made the owner check's refusal set a PRECONDITION on the flip round: the flip may not be taken until that set is shrunk far enough that the guard's reach fairly approximates the ruled set, or the residual is ruled acceptable in a dated decision that states the count it accepts. D45 named the route as well — 787 of the 999 were receivers no binding in scope resolved, so the gain was there and not in a new rule family. This round takes that route. It is the SHRINK half of D45's precondition and it does not discharge it.

CHOSEN. (1) SEVEN RESOLUTION RULES JOIN THE STATIC METHOD, AND EVERY ONE REFUSES ON AMBIGUITY. A cross-file table of functions whose return annotation names a live record class; a function with no return annotation whose every `return` returns one live constructor; container field element types, so `for t in job.tasks` resolves against `Job.tasks` on the RECEIVER'S OWN class and never by field name globally; PEP 604 unions and mapping subscripts, which carry a class identity the round 71 reader dropped; `with ... as` and the walrus; aliases, to a fixed point; and FILE-WIDE AGREEMENT, which resolves a receiver no enclosing scope binds only when every scope in the file that binds that name binds it identically. Wherever a rule can yield two different live record classes for one name it yields NOTHING and the site stays refused. That is the design constraint and not an implementation detail: a resolver that guesses converts a counted blind spot into an uncounted wrong answer, which is strictly worse, because the blind spot is printed on every run and the wrong answer is not. (2) THE WIDENING IS GATED BY A PER-SITE DECISION-MAP DIFF, NOT BY ITS OWN COUNTS. The stage carries a `--dump` writing its per-site decision map and a `--narrow` restoring the round 71 reader exactly; the instrument proves `--narrow` reproduces the COMMITTED round 71 stage class for class and site for site, then diffs the two maps site by site and asserts that EVERY SITE THE ROUND 71 METHOD DECIDED, THE ROUND 72 METHOD DECIDES THE SAME WAY. Nothing is dropped and nothing is decided differently. (3) THE RESULT. The refusal set goes from 999 to 324 and the confirmed set from 1195 to 1861; the class D45 named goes from 787 to 107. NINE contradicted sites the narrow method could not see are now named, eight of them `mission.id` standing in the mission argument of `link_job_to_mission` and one an `entry.id` on a `QueueEntry` — every one a site the flip would have renamed to `job_id` against the code's own reading. (4) `R-0880` STAYS OPEN and D45's precondition is NOT discharged. 324 sites remain undecided and this decision does not rule them acceptable.

ALTERNATIVES CONSIDERED. Ruling the residual acceptable now, which is D45's other route, was rejected as premature: a ruling costs nothing to write and is worth writing only once the cheap reach has been taken, and this round shows the cheap reach was worth 675 sites and nine real defects. TWO DRAFTS OF THIS ROUND'S OWN STAGE WERE DISCARDED AND BOTH ARE RECORDED, because each produced a better-looking number than the one that shipped. The first let every scope walk its nested definitions, so the module scope — whose span covers every line of a file — republished each function's locals as file-wide bindings; it reported a refusal set of 297 and ten contradictions, three of them its own artefacts, the clearest a `for t in job.tasks` resolved against a `for t in load_proposed_tasks(...)` four hundred lines away in another function. The second repaired the scoping and reported 741, and its defect is the one worth keeping: sound scoping destroyed 327 sites the round 71 reader had decided correctly, and because it also decided 585 new ones, every count-shaped check passed — DECIDED grew by exactly what REFUSED lost. Only the per-site diff showed the 327. Rule G is the answer to that and is why the shipped figure is 324 rather than 741. Making the guard fire on the residual was rejected again under item 33 of `docs/agents/planner_reviewer_prompt.md` §3, for the reason D45 gives.

CONSEQUENCE. The flip round's precondition is now one of two things rather than one of two plus an obvious unspent option: either a further shrink of the 324 — whose largest class is now 113 receivers that are not a bare name at all, which no binding rule reaches, so the route from here is a different method rather than another rule — or a dated decision ruling that residual acceptable and stating the count. A SECOND CONSEQUENCE IS METHODOLOGICAL AND BINDS THE NEXT ROUND THAT WIDENS A MEASUREMENT: the quantity a round exists to reduce is the quantity least able to judge its own reduction, so a widening ships with a per-item comparison against the method it replaces, never with two totals. The owner-check stage is REPLACED rather than kept beside its predecessor, per AGENTS.md Scope Control: the round 71 stage is an authored blob in git history and no second copy of it stays live. Nothing here touches the id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse, which is production work no round has started.

HOW TO REVERSE. Delete this paragraph block and stop running the round 72 stage; the round 71 stage is recoverable from `.agent/authored/f275-r71-owner-stage.py.md` at commit `ac7fa202`, and running the round 72 stage with `--narrow` reproduces it without recovering anything. Every figure above except the two discarded drafts' is re-derivable by the committed instrument at this round's base. Reversing the widening specifically means returning the refusal set to 999 and the nine named contradictions to silence.
END DEC72
