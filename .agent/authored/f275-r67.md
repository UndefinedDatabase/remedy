── STEP T003 / round 67 — F275 ────────────────────────────────
Goal:        Land the PLAIN re-derivation DECISION F275 D40 ordered, and the decision that
             rules it. The probe is unmodified and only the pytest invocation gained
             `--assert=plain`: the synthetic receivers go 24 to ZERO, the receiver-joined
             set 2116 to 2138, its drop list 52 to 30, with 22 sites recovered and NONE
             newly dropped. Both remaining unexplained drops were already ruled a round
             ago, so the plain set carries no unruled drop. The artefact and the instrument
             are reviewer texts transported as whole files. The round 66 verdict and its
             two prose slips are booked. NO LINE UNDER `packages/`, `apps/`, `tests/`,
             `docs/` OR `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r67.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r67-artefact.md`
             C0c  save the plain-run instrument verbatim as
                  `.agent/authored/f275-r67-plain.py.md`
             C0d  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN67, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD67 appended
             C3   `.agent/prose_slips.md` <- slice SLIPS67 appended
             C4   `.agent/decisions.md` <- slice DEC67 appended
             C5   `.agent/f275_t003_flip_residue_r67.md` <- a copy of the C0b blob
             C6   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r67.md                NEW
               .agent/authored/f275-r67-artefact.md       NEW
               .agent/authored/f275-r67-plain.py.md       NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               .agent/decisions.md
               .agent/f275_t003_flip_residue_r67.md       NEW
               .agent/handoff.md
             The four paths marked NEW do not exist at the base: `git ls-tree 39647827 --`
             over all four prints nothing at exit 0.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r67.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. A slice's BODY is the bytes from the start of the line after
     its BEGIN marker to the first byte of its END marker line, INCLUDING the terminal
     newline of the body's last line. Each BEGIN marker carries its slice's own sha256;
     check it. The artefact and the instrument are WHOLE FILES: copy each with
     `shutil.copyfile` and never open either in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 66 across
     C0a, C0b, C0c and C0d and becomes current at C1, which is the first SUBSTANTIVE
     commit and is what item 23 of §3 of `docs/agents/planner_reviewer_prompt.md` requires
     of a round that touches the finding ledger.
  4. This round creates NO `git worktree` and runs nothing destructive. The reviewer's own
     worktree was created, used for the two plain probe runs and removed BEFORE this block
     was written, and `git worktree list` shows the primary checkout alone at the base.
  5. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  6. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  7. Re-read `.agent/STOP` FROM DISK before the first commit and again before C6, and
     report both readings literally. It does not exist at the reviewer's base reading.
  8. This block is 332 lines TOTAL and 253 PROSE, measured on its final bytes.
  9. NO finding id is registered this round and NONE is resolved. The open set is 88 by
     distinct id at the base and must read 88 at C5, with the registered set, the resolved
     set and the de-registered set ALL EMPTY. The COUNT alone is not the gate; the
     membership is. `R-0880`'s SECOND obligation stays unbuilt and DEC67 says so. The two
     prose slips SLIPS67 books are NOT ids, per amend0827-process-diet rule 2.
 10. `.agent/authored/f275-r67-plain.py.md` is a `.md` and its extension is load-bearing:
     a `.py` file anywhere `ruff check .` scans is counted by
     `tests/orchestration/test_ci_budgets.py`, whose ceiling G6(c) reads. Do not rename it,
     and do not land a runnable copy of it anywhere in the tree.
 11. A pipe into `tail` MASKS the real exit code. Redirect to a file and read the file
     instead, for every gate whose exit code you report.
 12. The instrument reads JSON files under `.remedy-wt/` and nothing else — this block
     states no count of them, because the count is the instrument's to report and not the
     author's to recall. It writes nothing, installs nothing, runs no test and prints
     nothing on stderr.

Done when:   the seven gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C6.

  G1 TRANSPORT. For each of the three authored blobs, compare the COMMITTED blob against
     the reviewer's scratch original by size and sha256:
       .agent/authored/f275-r67.md           @C0a  vs  .remedy-wt/f275-r67.block.md
       .agent/authored/f275-r67-artefact.md  @C0b  vs  .remedy-wt/f275-r67-artefact.md
       .agent/authored/f275-r67-plain.py.md  @C0c  vs  .remedy-wt/f275-r67-plain.py.md
     Then `.agent/last_block.md` @C0d against the C0a blob. Report all four EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of every slice's
     BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report both
     numerals beside constraint 8's and say whether they agree. The block states no count
     of its own slices: the extraction is the sweep and its cardinality is your output.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN67: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. THREE appends in three commits, each proved by TWO readers and a negative
     control: C2 appends RECORD67 to `.agent/live_review.md`, C3 appends SLIPS67 to
     `.agent/prose_slips.md` and C4 appends DEC67 to `.agent/decisions.md`.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline and the slice's body. All three target files end with a
          single newline and no trailing blank line at the base, and all three separate
          their entries by a blank line, which is why the inserted newline is the same for
          each.
            .agent/live_review.md   pre 1016632 at the base, slice RECORD67
            .agent/prose_slips.md   pre  259093 at C2,       slice SLIPS67
            .agent/decisions.md     pre 1152295 at C3,       slice DEC67
          Report each pre size, each post size and each delta. The slice body sizes are
          NOT stated here: each is the length of what you extracted.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N for each of the three.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter — a byte b with
          `b < 128 and chr(b).isalpha()` — inside the FIRST appended paragraph, and report
          that BOTH readers reject it. Report ALSO that both readers ACCEPT the unmutated
          region, because a reader that rejects everything proves nothing by rejecting.
     (iv) RECORD67 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0. Report the count of `^- R-` and of `^Done: R-` lines that C2
          ADDS, both of which must be 0.
     (v)  Report RECORD67's first line beside the count of lines in `.agent/live_review.md`
          at `39647827` already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.`,
          and whether the new first line matches that pattern and duplicates none of them.
          Report the number your script counted; this block states none.
     (vi) DEC67 must begin `## DECISION F275 D41 ` and `.agent/decisions.md` at the base
          must contain NO line matching `^## DECISION F275 D41`. Report both readings, and
          report the highest existing `^## DECISION F275 D\d+` heading at the base.
     (vii) Both paragraphs SLIPS67 adds must begin `2026-09-12 · F275 R66 · `. Report the
          count of lines in `.agent/prose_slips.md` at `39647827` already beginning with
          that exact prefix, and the count C3 adds.

  G4 THE ARTEFACT AND THE INSTRUMENT ARE THE AUTHORED BLOBS AND NOTHING ELSE.
     `.agent/f275_t003_flip_residue_r67.md` at C5 must be byte-identical to the
     `.agent/authored/f275-r67-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show 39647827:.agent/f275_t003_flip_residue_r67.md`, which must be non-zero.
     Report the artefact's line count and the instrument blob's line count, each against
     the DECISION F104 D1 cap of 500 insertions.

  G5 THE ARTEFACT'S NUMBERS AND ITS QUOTED TRANSCRIPT ARE RE-DERIVED FROM THE COMMITTED
     INSTRUMENT. The instrument is committed at `.agent/authored/f275-r67-plain.py.md` at
     C0c, inside a ```python fence. Report the number of fences found, extract that source
     into `.remedy-wt/` and RUN it with `python3 -B`, REDIRECTED to a file per constraint
     11. It prints five banners; report every line of all five.
     (a) THE FIGURES. Say whether each agrees with what the instrument printed. The
         artefact's section 2 states 2195 rows in each plain run and symmetric difference 0
         under both keys at 2145 and 2195. Section 3 states 24 synthetic rows on 24 lines
         in the rewritten CONTROL against 0 in the plain run. Section 4 states 2082 against
         2058 resolved and 113 against 137 refused, and on the 24 lines 24 REFUSED beside 4
         resolved. Section 5 states the control at 2198 and SET-EQUAL True, the rewritten
         probe at LINE 2168 and RECEIVER 2116 for 52 drops, the plain probe at LINE 2168
         and RECEIVER 2138 for 30 drops, the two LINE joins agreeing, 22 sites kept that
         the rewritten join dropped and 0 dropped that it kept. Section 6 states 30 dropped
         as 27 at-risk, 4 with no sweep receiver, 3 both, 0 on a synthetic line and 2
         NEITHER, and names those two.
     (b) THE TRANSCRIPT. The artefact carries its tool output in MARKDOWN INDENTED blocks
         and NOT in fenced blocks; report the count of lines in it that consist of three
         backticks, which is 0. Every line of the artefact that begins with whitespace and
         whose STRIPPED form begins with any of `as the ROUND`, `CONTROL`, `the PLAIN run`,
         `rewritten:`, `plain    :`, `REFUSED:`, `resolved:`, `rewritten probe`,
         `plain probe`, `the two LINE joins`, `sites the PLAIN`, `dropped total`,
         `on one of the 39`, `the sweep recorded`, `both of the above`, `on a line still`,
         `NEITHER` or `packages/orchestration/long_run_executor.py:505` must appear, in its
         STRIPPED form, as a stripped line of the instrument's output. Report the count
         checked and the count that failed; the second must be 0. This is a CONTENT
         comparison after stripping on BOTH sides, never a byte comparison.
     (c) EXCERPTS ARE PERMITTED AND THIS IS WHAT MAKES ONE HONEST. The artefact quotes
         SOME of the instrument's lines and not all of them, which satisfies (b) as
         written. Where a block is an excerpt, the three properties that must hold are:
         every quoted line verbatim after stripping, in the SAME ORDER as the output, and
         no line present in the artefact that the output does not contain. Report whether
         the ORDER property holds over the lines (b) checked.
     (d) DETERMINISM. Run the SAME extracted file twice more and report whether all three
         outputs are byte-identical.
     A figure the instrument prints that DISAGREES with the artefact is reported as it
     read and is a finding; do not reconcile it in either direction. A figure the artefact
     states that the instrument does NOT print is reported as absent rather than supplied
     from elsewhere — EXCEPT the readings the artefact's PROVENANCE list names as the
     reviewer's, which are the two pytest summary lines of section 2 and the probe sha256
     of section 1, and EXCEPT the two standing exceptions any numeral sweep carries:
     digits inside an IDENTIFIER such as a SHA or a path, and numerals inside a CITATION
     of a named prior artefact or decision.

  G6 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `39647827` and at C5, and whether all five are EQUAL.
     (b) THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`, REDIRECTED to a
         file per constraint 11. It reads 42 passed at exit 0 at the base.
     (c) `python3 -m ruff check . --output-format concise`. Its exit code is 1 whenever
         any finding remains, so the GATE IS THE COUNT: report the number of rows matching
         `^\S+:\d+:\d+: `, which is 26 at the base and is the ceiling
         `tests/orchestration/test_ci_budgets.py` freezes. Report rows under `.remedy-wt/`
         separately, and report rows whose path ends `.py` under `.agent/`, which
         constraint 10 is the reason to expect at zero. Do not use `grep -c` for a count
         you expect to be zero.

  G7 NOTHING ELSE MOVED.
     (a) Report whether `.agent/STOP` exists on disk, the literal output of
         `git status --porcelain` piped through `cat -A`, and the literal output of
         `git worktree list`. The first must be absent and the second the empty string.
         The third is REPORTED, not gated: state instead whether THIS ROUND created or
         removed any worktree, which constraint 4 fixes at neither.
     (b) The changed-path set over `39647827`..C5 must be exactly the Change section's
         paths other than `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `docs/`, `scripts/`, `packages/`,
         `apps/` or `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `39647827` and at C5. Report both, the ids registered,
         the ids resolved and the ids de-registered, all three of which must be empty.
         Report the highest id in the record at each end.
     (d) Per-commit insertions from `git show --numstat <sha>` for C0a through C5, each
         against the AGENTS.md DECISION F104 D1 cap of 500, and the maximum over them.
         C6's own numbers are NOT ordered here: they cannot exist while C6 is being
         written, and the reviewer records them at the next gate. Where C6 exceeds the cap
         it is exempt by that same decision, which excludes entirely a commit whose diff
         is the verbatim rewrite of a SINGLE `.agent/**` state file; report the PATH COUNT
         of C6's own `--numstat` in the handback so the exemption is measured rather than
         asserted.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 24 of F275 and
             round 67, the one-sentence context self-assessment amend0905-throughput
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

BEGIN-PLAN67 sha256=ad6d26cbd22452b3a03952045112f3c3cf9584b6652b63ce13a2be25521b5caf
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

ROUND 67 SPENDS the `--assert=plain` route DECISION F275 D40 chose, and DECISION F275 D41
rules the result. The probe was not modified; only the pytest invocation changed. The
synthetic receivers go from 24 to ZERO, the receiver-joined set goes from 2116 to 2138, its
drop list from 52 to 30, and 22 sites come back with NONE newly dropped. Both remaining
unexplained drops were already ruled by D40 a round ago, so the plain set carries no unruled
drop and half of D40's condition is discharged. The artefact is
`.agent/f275_t003_flip_residue_r67.md`. The round 66 verdict and its two prose slips are
booked here. No production line moves.

## Next Steps

1. RULE THE 54 ruled keys that resolve to no `ast` node at their recorded position, and
   answer first whether the transform's own consumption already loses them — which decides
   whether they are a reporting defect or a live under-selection in every dry run so far.
   That is the whole of what DECISION F275 D41 still holds the write shut on.
2. Point the transform at the plain re-derived set and re-run the flip's dry run, which is
   the first reading of what the re-keying costs or saves in failures rather than in sites.
3. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
4. THE FLIP, then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The site set has yielded four distinct position defects in five rounds — the line key, the
  assertion rewriting, the sweep's own columns and the 54 non-resolving keys — and each was
  invisible to the gate that preceded it.
- `R-0880`'s SECOND obligation is still unbuilt, and the largest residue classes still need
  PRODUCTION-CODE work rather than another transform rule.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN67

BEGIN-RECORD67 sha256=9544278ae2614bcd141e4f84b443acc7cc0d4be1248b2542b11d800183a85f5b
Gate: F275 R66 — the F275 round 66 entry. VERDICT PASS. Written by the planner and reviewer of session 24 after reading the committed range `4de28049`..`39647827` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 67, per operator amendment amend0827-process-diet rule 1. The round RULED the three sites DECISION F275 D39 held the write shut on, and the decision recorded at `dc0fb7f1` records the result.

G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: all three authored blobs are byte-identical to the reviewer's own scratch originals — the block at 31424 bytes, the artefact at 8788 and the ruling instrument at 5991 — and `.agent/last_block.md` equals the block blob. All four slices matched the sha256 on their own BEGIN markers. Re-measured on the committed blob the block is 320 lines TOTAL and 241 PROSE, agreeing with its own constraint 8. G2: `.agent/plan.md` is byte-identical to its slice at 2860 bytes over 48 lines, both mandated headings exactly once.

G3: `.agent/live_review.md` goes 1011627 to 1016632, `.agent/prose_slips.md` 258183 to 259093 and `.agent/decisions.md` 1146996 to 1152295, every one exact under reader A, with reader B holding at N counted from the slice as 7, 1 and 9, and all three of the reviewer's own negative controls REJECTED by both readers while all three unmutated regions are ACCEPTED. The D40 heading reads 0 at the base against a highest existing D39. G4: the artefact at C5 is byte-identical to the C0b blob at 8788 bytes and the path does not resolve at the base. G6 and G7: five trees byte-identical; canary 42 passed at exit 0; ruff 26 rows at the frozen ceiling with zero under `.remedy-wt/` and zero `.py` under `.agent/`; nine changed paths with MISSING and EXTRA empty and zero production paths; the open set 88 at both ends with all three sets empty; per-commit insertions peak at 320 and every commit including the handback is under the cap at one path each.

G5 CARRIED A VERBATIM-TRANSCRIPT CLAUSE FOR THE FIRST TIME AND BOTH HALVES HELD. The instrument extracted from one fence and ran three times to byte-identical 5676-byte captures with empty stderr. The reviewer re-ran the same comparison the gate orders — every in-scope quoted line of the landed artefact against the instrument's own output, compared as content after each side's leading whitespace is stripped — and read 29 lines checked with 0 failed. Every figure agrees: 2198 ruled keys with 2144 resolving to an `ast` Attribute at their exact recorded position and 54 not, 24 probe rows carrying a synthetic `@py_assert` receiver on 24 lines every one of which begins `assert ` in the source, and 22 of the 52 drops sitting on such a line.

THE SUBSTANCE, RE-DERIVED RATHER THAN ACCEPTED, IS THAT THE THREE SITES RULE THREE DIFFERENT WAYS AND ONLY ONE IS THE DROP D39 SUPPOSED. `test_repair_loop_v1.py:56` at column 28 is an Artifact's id ruled only by sharing a line with a job's and a task's, so its drop is the over-selection being fixed. `long_run_executor.py:505` reads `RULED False` against round 53's committed set and its recorded column and receiver both disagree with the source, which makes it a defect of the SWEEP rather than a drop at all — and the same defect explains the `:504` disagreement round 64 reported and could not diagnose, where two sites at columns 19 and 40 sit over one attribute node at column 30 inside a call spanning two lines. `test_loop_run.py:285` is a WRONG drop whose cause is pytest rewriting `assert` statements before compiling them, so the name the probe recovers by disassembly is one pytest invented and can match no sweep receiver ever.

THE WORKER DECLARED TEN DEVIATIONS AND THE TWO NEW ONES ARE BOTH THE REVIEWER'S WORDING, BOOKED AS DATED LINES BY THIS SAME ROUND. G5(a) named the artefact's per-site blocks without saying whether a quoted EXCERPT satisfies it, and the artefact quotes six of nine lines for one site; the worker's first implementation demanded block equality, went red, and it then applied the excerpt reading and printed the three unquoted lines in full rather than resolving the ambiguity silently. G5(b) said "the artefact's fenced blocks" while that artefact carries ZERO fence lines and uses the indented form throughout, so the worker scoped the sweep to indented lines and reported that a prose line at column zero fell outside the stated scope. Both are gate text that did not match the artefact it was written about, neither left anything wrong on disk, and the worker's handling of each was to report rather than to reconcile.
END-RECORD67

BEGIN-SLIPS67 sha256=8ea66b70492453fa9729a46817dcf9be22ed020d1a551a5eb76bb48e08901965
2026-09-12 · F275 R66 · The round 66 block's G5(b) ordered a verbatim comparison over "every line inside the artefact's fenced blocks", and that artefact carries ZERO ``` fence lines — every transcript block in it is the markdown INDENTED form. The worker scoped the sweep to indented lines, which is what the clause plainly meant, and reported that one prose line at column zero fell outside the stated scope rather than silently widening it. The clause was written while the reviewer was looking at the instrument's output rather than at the artefact's own markup, one paragraph after adding the clause because a re-wrapped transcript had nearly shipped. THE RULE THAT FOLLOWS: a gate that quantifies over a REGION of an authored document names that region by a property measured in the document itself — count the fence lines, or say "indented block" — because "fenced" and "indented" are the same thing to a reader and different things to a script.

2026-09-12 · F275 R66 · The round 66 block's G5(a) ordered the artefact's per-site blocks reported and said nothing about whether a quoted EXCERPT satisfies it, while the artefact quotes six of the instrument's nine lines for `tests/orchestration/test_repair_loop_v1.py:56`, omitting the three `ast` lines. The worker's first implementation demanded block equality and went red, and it then applied the reading that an excerpt agrees when every quoted line is verbatim and in order with none invented, and printed the three unquoted lines in full. That reading is right and the gate should have stated it. THE RULE THAT FOLLOWS: where an artefact quotes part of a tool's output, the gate says whether it is comparing an EXCERPT or a BLOCK, and for an excerpt it states the three properties that make one honest — every quoted line verbatim, in order, and nothing invented — because a gate that leaves the reader to choose has two possible results and only one of them is a pass.
END-SLIPS67

BEGIN-DEC67 sha256=d850ecccb777681921e629b007fffa4c7f52f97e5927508cb1b74d01f3dcd6e8
## DECISION F275 D41 (2026-09-12, F275 round 67) — the plain re-derivation stands, and the write is shut on the 54 non-resolving keys alone

CONTEXT. DECISION F275 D40 ruled that pytest's assertion rewriting caused 22 of the 52 drops the round 65 re-derivation made, named `--assert=plain` as the route, and held the write shut on that and on 54 ruled keys that resolve to no `ast` node. This round spends the route. The measurement is in `.agent/f275_t003_flip_residue_r67.md` and the instrument is committed at `.agent/authored/f275-r67-plain.py.md`.

CHOSEN, PART ONE: THE ROUTE WORKS AND ITS PREDICTED FIGURE IS MET EXACTLY. The probe was NOT modified — the file run here is byte-identical to the one committed at round 65 — and only the pytest invocation gained `--assert=plain`, so the comparison moves one variable. Both plain runs hold 2195 rows and are set-equal under both keys. The synthetic `@py_assert` receivers go from 24, which is the rewritten run's own figure standing as the control, to ZERO. The plain run resolves 24 fewer receivers and refuses 24 more, which is the whole of the difference and is the direction D40 predicted: a wrong name became an honest absence.

CHOSEN, PART TWO: 22 SITES COME BACK AND NOT ONE IS NEWLY DROPPED. Rebuilt under the same join and the same control that reproduces round 53's committed set at 2198, the receiver join reads 2138 against the rewritten run's 2116, and its drop list is 30 against 52. Twenty-two sites the rewritten run dropped are kept, which is exactly the count D40 attributed to the rewriting arriving from the other direction, and ZERO sites are dropped that the rewritten run kept — so the plain run is strictly better rather than differently wrong. The two LINE joins agreeing at 2168 is the control on that claim: a join that reads no receiver must not move when the receivers change.

CHOSEN, PART THREE: THE PLAIN SET HAS NO UNRULED DROP, SO HALF OF D40's CONDITION IS DISCHARGED. Of its 30 drops, 27 are on the at-risk lines DECISION F275 D36 bounded, 4 are sites the sweep recorded no receiver for, 3 are both, NONE sits on a line still carrying a synthetic name, and 2 are neither — and both of those two were ruled a round ago by D40: `packages/orchestration/long_run_executor.py:505`, which reads `RULED False` against round 53's set and whose recorded column and receiver both disagree with the source, and `tests/orchestration/test_repair_loop_v1.py:56` at column 28, which is an Artifact's id ruled only by sharing a line. The third site DECISION F275 D39 held the write shut on is not in the list at all: the plain run recovered it, which is what D40 predicted for it by name.

CHOSEN, PART FOUR: THE WRITE STAYS SHUT ON THE 54 NON-RESOLVING KEYS AND ON NOTHING ELSE. D40 part three measured that 54 of the 2198 ruled keys resolve to no `ast` Attribute at their recorded line and column, and nothing since has ruled them. A consumer that walks the tree and looks a node up by that triple misses every one of them silently, which is an under-selection. NO ROUND MAY CONSUME THE RE-DERIVED SET FOR A WRITE UNTIL THOSE 54 ARE RULED, and the ruling must answer one question first: whether the transform's own consumption already loses them, which decides whether they are a reporting defect or a live under-selection in every dry run this chain has taken. That is the whole of the remaining condition, and it replaces the two halves D40 carried.

ALTERNATIVES CONSIDERED. (i) Consume the plain set now and rule the 54 afterwards — rejected for the reason the 22 exist: a set that drives a rename is consumed once, and a defect measured but unruled is a defect that ships. (ii) Modify the probe to ignore `@py_assert` names instead of disabling the rewriting — rejected in D40 and re-rejected here on this round's evidence: the plain run recovered four resolutions on the same lines that a prefix filter would have thrown away, so removing the cause was also the more accurate route. (iii) Re-run the flip's dry run against the plain set this round — not rejected and deliberately deferred: it costs twenty-one minutes and its reading is only meaningful once the 54 are ruled, because a dry run over a set with a known under-selection measures the under-selection too. (iv) Rule the 54 in this round — rejected as scope: two suite passes were already spent here, and the 54 need a separate instrument and a separate proof.

WHAT THIS DECISION DOES NOT RULE. It does not rule the 54, and it does not point the transform at the plain set. It does not re-run the dry run. It does not resolve `R-0880`, whose SECOND obligation — the transform's refusal to rename a site whose owner verdict cannot be confirmed — is still unbuilt, though the probe's own refusal behaviour, now at 137 rows, remains the model for it. And it registers no id: nothing measured here is wrong on disk under `packages/`, `apps/`, `tests/` or `docs/`.

HOW TO REVERSE: delete this decision. DECISION F275 D40's condition then stands with both of its halves open, the two plain runs and this artefact stay on disk, and the next session re-reads the 22-and-0 reading out of the artefact rather than re-measuring it in forty-two minutes.
END-DEC67
