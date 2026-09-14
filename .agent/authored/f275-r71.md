── STEP T003 / round 71 — F275 ────────────────────────────────
Goal:        Build finding `R-0880`'s SECOND obligation at the reach its method actually has,
             and record why it cannot be built as written. Taken literally the finding stops a
             run on every ruled site whose owner verdict cannot be CONFIRMED, and the static
             method cannot confirm 999 of 2198 — a guard that stops every run it is ever
             given, which item 33 of §3 names as the same defect as one that cannot fail.
             DECISION F275 D45 narrows it to sites the code CONTRADICTS. The owner-check stage
             lands beside the re-key stage, finds FOUR, names each with both classes and exits
             5; given the same set with those four removed it exits 0, the confirmed count
             reading 1195 in both as the control. `R-0880` STAYS OPEN and D45 makes the 999 a
             precondition on the flip round. The round 70 verdict and its prose slip are
             booked. NO LINE UNDER `packages/`, `apps/`, `tests/`, `docs/` OR `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r71.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r71-artefact.md`
             C0c  save the owner-check stage verbatim as
                  `.agent/authored/f275-r71-owner-stage.py.md`
             C0d  save this round's instrument verbatim as
                  `.agent/authored/f275-r71-instrument.py.md`
             C0e  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN71, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD71 appended
             C3   `.agent/prose_slips.md` <- slice SLIPS71 appended
             C4   `.agent/decisions.md` <- slice DEC71 appended
             C5   `.agent/f275_t003_owner_guard_r71.md` <- a copy of the C0b blob
             C6   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r71.md                    NEW
               .agent/authored/f275-r71-artefact.md           NEW
               .agent/authored/f275-r71-owner-stage.py.md     NEW
               .agent/authored/f275-r71-instrument.py.md      NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               .agent/decisions.md
               .agent/f275_t003_owner_guard_r71.md            NEW
               .agent/handoff.md
             The five paths marked NEW do not exist at the base: `git ls-tree 3c59e51b --`
             over all five prints nothing at exit 0.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r71.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. A slice's BODY is the bytes from the start of the line after
     its BEGIN marker to the first byte of its END marker line, INCLUDING the terminal
     newline of the body's last line. Each BEGIN marker carries its slice's own sha256;
     check it. The artefact and the two `.py.md` carriers are WHOLE FILES: copy each with
     `shutil.copyfile` and never open any of them in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 70 across
     C0a through C0e and becomes current at C1, which is the first SUBSTANTIVE commit and
     is what item 23 of §3 of `docs/agents/planner_reviewer_prompt.md` requires of a round
     that touches the finding ledger.
  4. THIS ROUND'S G5 CREATES A DISPOSABLE WORKTREE AND THE INSTRUMENT REMOVES IT ITSELF.
     It lives under the gitignored `.remedy-wt/`, and the instrument's last banner reads
     `git worktree list` and `git status --porcelain` back after pruning. That is the only
     destructive verification this round runs and it never touches the primary checkout,
     which is what `docs/agents/self_drive_protocol.md` G5 requires. The reviewer's runs
     were taken and cleaned up before this block was written, and `git worktree list` shows
     the primary checkout alone at the base.
  5. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  6. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  7. Re-read `.agent/STOP` FROM DISK before the first commit and again before C6, and
     report both readings literally. It does not exist at the reviewer's base reading.
  8. This block is 348 lines TOTAL and 274 PROSE, measured on its final bytes.
  9. NO finding id is registered this round and NONE is resolved. The open set is 87 by
     distinct id at the base and must read 87 at C5, with the registered set, the resolved
     set and the de-registered set ALL EMPTY. The COUNT alone is not the gate; the
     membership is. `R-0880` STAYS OPEN and DEC71 says why at length — do not read the
     landing of its guard as a resolution. The prose slip SLIPS71 books is NOT an id, per
     amend0827-process-diet rule 2.
 10. BOTH `.py.md` CARRIERS ARE `.md` AND THE EXTENSION IS LOAD-BEARING: a `.py` file
     anywhere `ruff check .` scans is counted by
     `tests/orchestration/test_ci_budgets.py`, whose ceiling G6(c) reads. Do not rename
     either, and do not land a runnable copy of either in the tree. G5 extracts into
     `.remedy-wt/`, which is outside the tree and which G6(c) measures separately.
 11. A pipe into `tail` MASKS the real exit code. Redirect to a file and read the file
     instead, for every gate whose exit code you report.
 12. The instrument reads files under `.remedy-wt/` that this round does not create and
     must not rebuild — among them the re-keyed ruled set and its owner table. If any is
     missing, STOP and report which, rather than regenerating it. This block states no
     count of them, because the count is the instrument's to report and not the author's to
     recall. It installs nothing, runs no test, and prints nothing on stderr.
 13. THE OWNER-CHECK STAGE EXITS NON-ZERO BY DESIGN ON THE SET THE PIPELINE HOLDS. G5's
     first banner therefore reports exit 5 and that is the PASS reading for that banner; the
     gate's own exit code is the instrument's, which is 0. Do not treat the stage's 5 as a
     failure and do not "fix" the ruled set to make it 0 — the refusal is the deliverable.
 14. AN f-STRING EXPRESSION CANNOT CONTAIN A BACKSLASH ON THIS INTERPRETER, WHICH IS CPython
     3.10. Bind such a value to a name first. Two previous workers spent a retry on this
     writing gate scripts, and it is stated here so a third does not.

Done when:   the seven gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C6.

  G1 TRANSPORT. For each of the four authored blobs, compare the COMMITTED blob against the
     reviewer's scratch original by size and sha256, the scratch name being the committed
     basename under `.remedy-wt/` except for the block, which is `f275-r71.block.md`:
       .agent/authored/f275-r71.md                  @C0a
       .agent/authored/f275-r71-artefact.md         @C0b
       .agent/authored/f275-r71-owner-stage.py.md   @C0c
       .agent/authored/f275-r71-instrument.py.md    @C0d
     Then `.agent/last_block.md` @C0e against the C0a blob. Report all five EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of every slice's
     BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report both
     numerals beside constraint 8's and say whether they agree. The block states no count
     of its own slices: the extraction is the sweep and its cardinality is your output.
     ADDITIONALLY, as round 70's G1 established: for each `.py.md` carrier, extract its
     single ```python fence and report whether re-wrapping that extracted source in the
     carrier's own header and fence reproduces the committed blob byte for byte.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN71: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. THREE appends in three commits, each proved by TWO readers and a negative
     control: C2 appends RECORD71 to `.agent/live_review.md`, C3 appends SLIPS71 to
     `.agent/prose_slips.md` and C4 appends DEC71 to `.agent/decisions.md`.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline and the slice's body. All three target files end with a
          single newline and no trailing blank line at the base, and all three separate
          their entries by a blank line, which is why the inserted newline is the same for
          each.
            .agent/live_review.md   pre 1040150 at the base, slice RECORD71
            .agent/prose_slips.md   pre  265750 at C2,       slice SLIPS71
            .agent/decisions.md     pre 1175806 at C3,       slice DEC71
          Report each pre size, each post size and each delta. The slice body sizes are
          NOT stated here: each is the length of what you extracted.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N for each of the three.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter — a byte b with
          `b < 128 and chr(b).isalpha()` — inside the FIRST appended paragraph, and report
          that BOTH readers reject it. Report ALSO that both readers ACCEPT the unmutated
          region, because a reader that rejects everything proves nothing by rejecting.
     (iv) RESERVED PREFIXES, scoped by a property rather than by an adjective. Over every
          line of RECORD71 EXCEPT ITS FIRST — the first being the entry header, which
          begins `Gate: ` by the format it joins — count the lines beginning `Gate: `,
          `- R-`, `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; that count
          must be 0. Report the count of `^- R-` and of `^Done: R-` lines C2 ADDS, both of
          which must be 0.
     (v)  Report RECORD71's first line beside the count of lines in `.agent/live_review.md`
          at `3c59e51b` already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.`,
          and whether the new first line matches that pattern and duplicates none of them.
          Report the number your script counted; this block states none.
     (vi) DEC71 must begin `## DECISION F275 D45 ` and `.agent/decisions.md` at the base
          must contain NO line matching `^## DECISION F275 D45`. Report both readings, and
          report the highest existing `^## DECISION F275 D\d+` heading at the base.
     (vii) Every paragraph SLIPS71 adds must begin `2026-09-12 · F275 R70 · `. Report the
          count your script measured, the count of lines in `.agent/prose_slips.md` at
          `3c59e51b` already beginning with that exact prefix, and the count C3 adds.

  G4 THE ARTEFACT. `.agent/f275_t003_owner_guard_r71.md` at C5 must be byte-identical to the
     `.agent/authored/f275-r71-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show 3c59e51b:.agent/f275_t003_owner_guard_r71.md`, which must be non-zero. Report
     the line count of every blob this round lands, each against the DECISION F104 D1 cap of
     500 insertions, and say for each whether it is under.

  G5 THE ARTEFACT'S NUMBERS AND ITS QUOTED TRANSCRIPT ARE RE-DERIVED FROM THE COMMITTED
     INSTRUMENT. The instrument is committed at `.agent/authored/f275-r71-instrument.py.md`
     at C0d, inside a ```python fence. Report the number of fences found, extract that
     source into `.remedy-wt/` and RUN it, REDIRECTED to a file per constraint 11, as
       python3 -B <extracted> . 3c59e51b
     Report every line of every banner it prints. Constraint 13 governs how to read the
     stage's own exit code inside banner 1.
     (a) THE FIGURES. Sweep the artefact's PROSE — its lines that do NOT begin with
         whitespace — for every maximal run of digits, and report which of those runs does
         not occur anywhere in the instrument's output. This block enumerates no figure:
         the enumeration is the sweep's output. Three standing exceptions apply and each is
         reported rather than waved: digits inside an IDENTIFIER such as a SHA, a path or a
         `line:col` citation, digits inside a CITATION of a named prior decision, round,
         finding, slice or feature, and digits inside a backtick-quoted span, which is a
         token the artefact QUOTES rather than one it USES. A citation's quotation marks
         may OPEN on an earlier line than the digits they enclose; read the artefact as a
         whole rather than line by line, and say which reading you used.
     (b) THE TRANSCRIPT, OVER EVERY QUOTED LINE AND NOT A LIST OF THEM. The artefact
         carries its tool output in MARKDOWN INDENTED blocks and NOT in fenced blocks;
         report the count of lines in it that consist of three backticks, which is 0. Then
         take EVERY line of the artefact that begins with whitespace and is not blank —
         all of them, with no prefix list to go stale — and report that its STRIPPED form
         appears as a stripped line of the instrument's output. Report the count checked
         and the count that failed; the second must be 0. This is a CONTENT comparison
         after stripping on BOTH sides, never a byte comparison.
     (c) THE ORDER PROPERTY, AS A MONOTONE MATCHING. The instrument reprints the same field
         names under more than one banner, so resolving each quoted line to its FIRST
         occurrence in the output is the wrong test and reports a false inversion. Match
         each quoted line, in artefact order, to the first output occurrence AT OR AFTER
         the previous match, and report whether every quoted line is matched and whether
         the matched indices strictly increase. Report the count matched and the count
         unmatchable in order; the second must be 0.
     (d) DETERMINISM. Run the SAME extracted file twice more and report whether all three
         outputs are byte-identical, and report the stderr byte count of each.
     A figure the instrument prints that DISAGREES with the artefact is reported as it
     read and is a finding; do not reconcile it in either direction. A figure the artefact
     states that the instrument does NOT print is reported as absent rather than supplied
     from elsewhere.

  G6 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `3c59e51b` and at C5, and whether all five are EQUAL.
     (b) THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`, REDIRECTED to a
         file per constraint 11. It reads 42 passed at exit 0 at the base.
     (c) `python3 -m ruff check . --output-format concise`. Its exit code is 1 whenever
         any finding remains, so the GATE IS THE COUNT: report the number of rows matching
         `^\S+:\d+:\d+: `, which is 26 at the base and is the ceiling
         `tests/orchestration/test_ci_budgets.py` freezes. Report rows under `.remedy-wt/`
         separately, and report rows whose path ends `.py` under `.agent/`, which
         constraint 10 is the reason to expect at zero. Do not use `grep -c` for a count
         you expect to be zero. Run this AFTER G5 has removed its worktree, so no worktree
         checkout is inside the scan.

  G7 NOTHING ELSE MOVED.
     (a) Report whether `.agent/STOP` exists on disk, the literal output of
         `git status --porcelain` piped through `cat -A`, and the literal output of
         `git worktree list`. The first must be absent, the second the empty string and
         the third the primary checkout alone — constraint 4 fixes G5's worktree as
         created and removed WITHIN that gate, so any worktree surviving here is a finding.
     (b) The changed-path set over `3c59e51b`..C5 must be exactly the Change section's
         paths other than `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `docs/`, `scripts/`, `packages/`,
         `apps/` or `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `3c59e51b` and at C5. Report both, the ids registered,
         the ids resolved and the ids de-registered, all three of which must be empty.
         Report the highest id at each end, and whether `R-0880` is open at both.
     (d) Per-commit insertions from `git show --numstat <sha>` for C0a through C5, each
         against the AGENTS.md DECISION F104 D1 cap of 500, and the maximum over them.
         C6's own numbers are NOT ordered here: they cannot exist while C6 is being
         written, and the reviewer records them at the next gate. Where C6 exceeds the cap
         it is exempt by that same decision, which excludes entirely a commit whose diff
         is the verbatim rewrite of a SINGLE `.agent/**` state file; report the PATH COUNT
         of C6's own `--numstat` in the handback so the exemption is measured rather than
         asserted.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 25 of F275 and
             round 71, the one-sentence context self-assessment amend0905-throughput
             requires, the changed-files table with every `+/-` taken from
             `git show --numstat` and no other source, one line per gate with its REAL
             exit code, the item-status table covering every C and every G exactly once,
             and the authored-text proofs. State the SCOPE REPORT position: F275 stands
             past the soft limit amend0908-f275-finish rule 1 names, the report written in
             round 51's handback STANDS and is not restated, rule 2 forbids the
             split-and-close default BY NAME, and this round closes nothing, registers no
             feature and does not touch `docs/roadmap/STATUS.md`. Carry the operator
             banner exactly as `docs/agents/self_drive_protocol.md` spells it. Then push.
──────────────────────────────────────────────────────────────

The three separators in this block carry runs of the box-drawing character U+2500, whose
lengths are stated here because a run of one character has no length a reader recovers by
eye. The STEP line that opens the frame is 63 characters holding 34 of them, in two runs
either side of its text. The rule that closes the frame, directly above this paragraph, is
62 of them and nothing else. The slice rule below is 10, the word SLICES between single
spaces, and 10 more.

────────── SLICES ──────────

BEGIN-PLAN71 sha256=28f5c15bb44aafacfbaf913f391f2ca5a1ba270a924864904e743211918bd287
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

ROUND 71 BUILDS `R-0880`'s SECOND OBLIGATION AT THE REACH ITS METHOD HAS, AND RECORDS WHY IT
CANNOT BE BUILT AS WRITTEN. Taken literally the finding stops a run on every site whose owner
verdict cannot be CONFIRMED, and the static method cannot confirm 999 of 2198 — a guard that
stops every run it is given. DECISION F275 D45 narrows it to sites the code CONTRADICTS. The
owner-check stage lands beside the re-key stage, finds FOUR such sites, names each with both
classes and exits 5; given the same set with those four removed it exits 0, with the confirmed
count reading 1195 in both as the control. `R-0880` STAYS OPEN: the 999 are a real residual
and D45 makes them a precondition on the flip round rather than a silent inheritance. The
round 70 verdict and its prose slip are booked. No production line moves.

## Next Steps

1. SHRINK THE REFUSAL SET, the route D45 names for the flip round: 787 of the 999 are
   receivers no binding in scope resolves, so the gain is there and not in a new rule family.
2. Re-run the flip's dry run against the corrected inputs of rounds 67 and 69 together — the
   plain re-derivation and the re-keyed set — which is the first reading of what both
   corrections cost in FAILURES rather than in sites.
3. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
4. THE FLIP, which D45 now forbids until the residual is shrunk or ruled on the record, then
   the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- THE REVIEWER'S ERROR RATE IS THE LIVE RISK: four authoring slips across rounds 68 to 70,
  one a shipped artefact-and-instrument mismatch that cost a full repair round, every one
  caught by a worker rather than by the reviewer's own pre-emission sweep.
- Two refusal stages now stand between the measured set and the transform and NEITHER has a
  test behind it, because the flip is unlanded and there is no production surface to pin one to.
- The open set is 87 by distinct id, with `R-0880` open. Four are High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN71

BEGIN-RECORD71 sha256=c646ecc2be125fd0808abe8bfbcd8bfeaa1b46ff763fe1a28776a576a31f7f4f
Gate: F275 R70 — the F275 round 70 entry. VERDICT PASS. Written by the planner and reviewer of session 25 after reading the committed range `aa200600`..`3c59e51b` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 71, per operator amendment amend0827-process-diet rule 1. The round repaired round 69's red gate and carried finding `R-0880`'s first obligation beside it, and the decision recorded at C4 of round 70 rules both.

G1 IS THE PRIMARY CMP-AGAINST-SCRATCHPAD PROOF AND NOT THE §4.9 DIGEST FALLBACK: all five authored blobs are byte-identical to the reviewer's own scratch originals — the block at 35910 bytes, the artefact at 8174, the corrected round 69 instrument at 8018, this round's instrument at 5560 and the bound probe at 9572 — and `.agent/last_block.md` equals the block blob. Four slices matched the sha256 on their own BEGIN markers, and the block re-measures at 361 lines TOTAL and 285 PROSE, agreeing with its own constraint 8. THE CHECK ROUND 69 LACKED WAS ADDED AND HELD: all three `.py.md` carriers round-trip through their own fence, and re-wrapping each extracted source reproduces the committed blob byte for byte. G2: `.agent/plan.md` byte-identical to PLAN70 at 3034 bytes over 49 lines against the cap of 50, both mandated headings exactly once.

G3: `.agent/live_review.md` goes 1035516 to 1040150, `.agent/prose_slips.md` 264262 to 265750 and `.agent/decisions.md` 1170195 to 1175806, every one exact under reader A, with reader B holding at N counted from the slice as 6, 1 and 8, and all three of the reviewer's own negative controls — each placed on the FIRST appended paragraph, per item 36 of §3 — REJECTED by both readers while every unmutated region is ACCEPTED. Zero reserved-prefix lines after the entry header, the new header duplicating none of the 68 already matching the neighbours' pattern, and `## DECISION F275 D44` reading 0 at the base against a highest existing D43. G4: the artefact at C5 byte-identical to the C0b blob at 8174 bytes and the path absent at the base. G6: five top-level trees byte-identical, canary 42 passed at exit 0, `ruff check .` 26 rows at the frozen ceiling. G7: eleven changed paths with MISSING and EXTRA empty and zero production paths; constraint 13 held, so neither the stale round 69 blob nor the round 69 artefact is in the change set; the open set 87 at both ends with IDENTICAL MEMBERSHIP and all three id sets empty, `R-0880` open and `R-0879` resolved at each end; per-commit insertions peak at 361 and the handback commit is 343 insertions over ONE path.

G5 CARRIED THE ROUND AND ITS DECISIVE READING IS A PAIR. The instrument extracted from one fence at 4889 bytes and ran to byte-identical 2692-byte captures with ZERO stderr at exit 0. Run against the blob round 69 landed, the round 69 artefact has FIVE quoted lines the blob cannot produce; run against the corrected blob, it has NONE — five absent against zero, over the same artefact and the same sweep. That is the repair demonstrated rather than asserted, and it is why the round ran the stale blob on purpose instead of deleting it. Over this round's OWN artefact the sweep reads 37 quoted lines checked, 0 failed, 0 unmatchable in order and the matched indices strictly increasing, with zero three-backtick lines.

THE SUBSTANCE OF THE REPAIR IS THAT THE ARTEFACT WAS RIGHT AND THE CARRIER WAS STALE, which is the least visible shape this defect has: the stale blob runs at exit 0 with an empty stderr and prints a perfectly good report of five banners where seven were needed, so nothing fails and the only symptom is an absence. The counter-measure DECISION F275 D44 rules is not a procedure but a tool — the carrier is regenerated by the same script that verifies its round-trip, in one step, and the instrument's own source was changed to build its fence marker from a character code so that regeneration can never again be blocked by a literal fence in the file being wrapped.

BESIDE THE REPAIR, `R-0880`'s FIRST OBLIGATION HAS A RESULT. Over 994 tracked files the static pass finds 71 classes carrying `id`, `name` or `description`, of which 69 are neither a job nor a task record; it CONFIRMS 1010 ruled sites as job reads agreeing with their owner verdict and 157 as task reads, finds FOUR statically confirmed over-selected in two classes already on the finding's own list, and REFUSES 973. The blind spot is the reading rather than a caveat on it: a static pass that refuses 44 percent of its input undercounts in a different direction from a dry run, so what it produces is a CONFIRMATION by an independent route and not an upper bound, and the round records it as that and nothing more.

THE WORKER DECLARED NINE DEVIATIONS AND RAISED ONE OBSERVATION THAT IS THE REVIEWER'S TO OWN. The round 70 artefact's provenance sentence reads "Every figure in sections 2 through 4 is re-derived by the committed instrument", and four figures in section 4's PROSE — 33, 25, 12 and 18 — come from `R-0880`'s own registration and from the bound probe's discarded first run rather than from the instrument. The worker reported all eight unresolved digit runs rather than supplying any from elsewhere, applied the wider reading of the citation exception and declared the narrower one, and did not edit the artefact. It is the same class as round 69's defect and milder, because the artefact names the other source in the same sentences; it is booked as a dated line by this same commit's round and is not an id, per amend0827-process-diet rule 2.
END-RECORD71

BEGIN-SLIPS71 sha256=2624d0de7ae86ad75a4a8902ff7ce5746dc4dd03b38b414f3e846bc224085d9b
2026-09-12 · F275 R70 · The round 70 artefact's provenance paragraph reads "Every figure in sections 2 through 4 is re-derived by the committed instrument", and four figures in section 4's PROSE are not: 33 and 25 come from finding `R-0880`'s own registration, which recorded `Mission.job_id` and `Artifact.job_id` at those counts from its dry run, 12 comes from that finding's "12 located frames", and 18 is the class count from the bound probe's discarded first run, which the same section reports as an error it made. Every INDENTED line in the range is instrument output and all 37 verify, so nothing measured is wrong and the artefact names the other sources in the very sentences that use them; what over-reaches is the universal quantifier in the provenance clause. It is the same class as the round 69 defect the same round was repairing — a provenance claim reaching past its evidence — which is why it is worth a line despite being mild. THE RULE THAT FOLLOWS: a provenance clause quantifies over a SHAPE, not over a RANGE. "Every indented line in sections 2 through 5 is a verbatim excerpt of the instrument's output" is checkable by a script and stays true when prose is added; "every figure in sections 2 through 4" quantifies over a region whose prose will always attract citations, so it is false as soon as the document does its job of attributing anything to a second source.
END-SLIPS71

BEGIN-DEC71 sha256=1c7bdea3ceb3ed5341a3c6d2e43ad3d59d7859d8eadab99cef34c873ec979812
## DECISION F275 D45 (2026-09-12, F275 round 71) — `R-0880`'s second obligation is unmeetable as written, the guard is built at the reach its method has, and the residual becomes a precondition on the flip

CONTEXT. Finding `R-0880`'s fix clause binds two obligations. Round 70 discharged the first. The second reads: "give the transform the same shape of refusal `R-0879` gave it, so that a ruled site whose owner verdict CANNOT BE CONFIRMED against the receiver's own record STOPS the run and is named, rather than being renamed quietly." Taken literally that stops the run on every site the method cannot decide, and the method cannot decide 999 of the 2198 — 787 whose receiver no annotation, construction or loop binding in scope resolves, 113 whose receiver is not a bare name at all, and 99 annotated with something carrying no class identity, `Any` above all. A guard that fires on all 999 stops every run it is ever given. That is a guard that CANNOT PASS, which is the same defect as a guard that cannot fail wearing the other face; item 33 of `docs/agents/planner_reviewer_prompt.md` §3 names both, and this is the first time this feature has met the first face.

CHOSEN, and this is a §4 item 7 re-plan recorded rather than a silent narrowing. (1) THE OBLIGATION IS NARROWED FROM "CANNOT BE CONFIRMED" TO "IS CONTRADICTED". The owner-check stage landed by this round stops on a ruled site whose receiver statically resolves to a record class that the site's owner verdict does not name, prints that site with its file, line, column, receiver and both classes, and exits non-zero. On the set the pipeline holds it finds FOUR — one `Mission` and three `Artifact`, both classes already on `R-0880`'s own list from its dry run — and refuses to run. (2) THE STAGE PRINTS WHAT IT REFUSES TO DECIDE, AS A COUNT, ON EVERY RUN. A guard whose reach is smaller than its subject must say so where it is used, not only where it was ruled, so the blind spot travels with the tool. (3) IT IS DEMONSTRATED BESIDE THE CASE THAT MUST FAIL. The same stage over the same tree, given the same set with exactly those four sites removed, exits 0 — and the confirmed count reads 1195 in BOTH runs, which is the control: removing four contradicted sites must not change what the method confirms, and it does not. The cleaned set is built by the instrument from the stage's own report rather than by hand, so the two runs cannot disagree about which sites the difference is. (4) `R-0880` STAYS OPEN. Its literal second obligation is not met and this decision does not pretend it is.

ALTERNATIVES CONSIDERED. Resolving `R-0880` on the narrowed reading was rejected, and it was the closest call: the two obligations would then both be discharged against a recorded ruling, which is a defensible bookkeeping position. It was rejected because the defect the finding names — a wrong rename inside the one commit this feature cannot split — remains reachable among the 999, and a resolved finding is invisible while an open one is not. Making the guard fire on all 999 was rejected under item 33 as above. Improving the static method until its refusal set is small was rejected as this round's work rather than as a bad idea: it is real work, it is the obvious way to make the guard's reach match its subject, and it is named below as the route the flip round may take.

CONSEQUENCE, AND IT IS A PRECONDITION RATHER THAN A TASK. The flip is one commit that AGENTS.md's Commit Discipline lets this feature land oversize exactly once, so a wrong rename inside it has no cheap second chance. THE ROUND THAT TAKES THE FLIP MAY NOT TAKE IT UNTIL ONE OF TWO THINGS IS TRUE ON THE RECORD: either the refusal set has been shrunk far enough that the guard's reach is a fair approximation of the ruled set, or the residual has been RULED ACCEPTABLE in a dated decision that states the count it is accepting. Carrying the number forward silently is the one route this decision closes. Nothing here touches the id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse, which is production work no round has started.

HOW TO REVERSE. Delete this paragraph block. The owner-check stage stays landed and no figure changes, because every figure above is re-derivable by the committed instrument at this round's base. Reversing the narrowing specifically means reading `R-0880`'s second obligation literally again, which makes it unmeetable again; reversing the precondition in the consequence means the flip round inherits the 999 with nothing on the record about them.
END-DEC71
