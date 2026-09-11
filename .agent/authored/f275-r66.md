── STEP T003 / round 66 — F275 ────────────────────────────────
Goal:        Land the RULING on the three sites DECISION F275 D39 held the write shut on,
             and the decision that records it. They rule three different ways, and the
             third of them has a systematic cause — pytest's assertion rewriting — that
             reaches 22 of the 52 drops, so the re-derived set is NOT safe to consume. A
             second and independent defect is measured beside it: 54 ruled keys resolve to
             no `ast` node at their recorded position. The artefact and the instrument are
             reviewer texts transported as whole files. The round 65 verdict and its prose
             slip are booked. NO LINE UNDER `packages/`, `apps/`, `tests/`, `docs/` OR
             `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r66.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r66-artefact.md`
             C0c  save the ruling instrument verbatim as
                  `.agent/authored/f275-r66-rule.py.md`
             C0d  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN66, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD66 appended
             C3   `.agent/prose_slips.md` <- slice SLIPS66 appended
             C4   `.agent/decisions.md` <- slice DEC66 appended
             C5   `.agent/f275_t003_flip_residue_r66.md` <- a copy of the C0b blob
             C6   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r66.md                NEW
               .agent/authored/f275-r66-artefact.md       NEW
               .agent/authored/f275-r66-rule.py.md        NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               .agent/decisions.md
               .agent/f275_t003_flip_residue_r66.md       NEW
               .agent/handoff.md
             The four paths marked NEW do not exist at the base: `git ls-tree 4de28049 --`
             over all four prints nothing at exit 0.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r66.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. A slice's BODY is the bytes from the start of the line after
     its BEGIN marker to the first byte of its END marker line, INCLUDING the terminal
     newline of the body's last line. Each BEGIN marker carries its slice's own sha256;
     check it. The artefact and the instrument are WHOLE FILES: copy each with
     `shutil.copyfile` and never open either in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 65 across
     C0a, C0b, C0c and C0d and becomes current at C1, which is the first SUBSTANTIVE
     commit and is what item 23 of §3 of `docs/agents/planner_reviewer_prompt.md` requires
     of a round that touches the finding ledger.
  4. This round creates NO `git worktree` and runs nothing destructive. The reviewer's own
     worktree was created, used for the paired probe run of the artefact's section 7 and
     removed BEFORE this block was written, and `git worktree list` shows the primary
     checkout alone at the base.
  5. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  6. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  7. Re-read `.agent/STOP` FROM DISK before the first commit and again before C6, and
     report both readings literally. It does not exist at the reviewer's base reading.
  8. This block is 320 lines TOTAL and 241 PROSE, measured on its final bytes.
  9. NO finding id is registered this round and NONE is resolved. The open set is 88 by
     distinct id at the base and must read 88 at C5, with the registered set, the resolved
     set and the de-registered set ALL EMPTY. The COUNT alone is not the gate; the
     membership is. `R-0880`'s SECOND obligation stays unbuilt and DEC66 says so. The
     prose slip SLIPS66 books is NOT an id, per amend0827-process-diet rule 2.
 10. `.agent/authored/f275-r66-rule.py.md` is a `.md` and its extension is load-bearing:
     a `.py` file anywhere `ruff check .` scans is counted by
     `tests/orchestration/test_ci_budgets.py`, whose ceiling G6(c) reads. Do not rename it,
     and do not land a runnable copy of it anywhere in the tree.
 11. A pipe into `tail` MASKS the real exit code. Redirect to a file and read the file
     instead, for every gate whose exit code you report.
 12. The instrument reads only `.remedy-wt/r53_R.json`, `.remedy-wt/r65_probe1.json` and
     the tracked source files it parses. It writes nothing and installs nothing.

Done when:   the seven gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C6.

  G1 TRANSPORT. For each of the three authored blobs, compare the COMMITTED blob against
     the reviewer's scratch original by size and sha256:
       .agent/authored/f275-r66.md           @C0a  vs  .remedy-wt/f275-r66.block.md
       .agent/authored/f275-r66-artefact.md  @C0b  vs  .remedy-wt/f275-r66-artefact.md
       .agent/authored/f275-r66-rule.py.md   @C0c  vs  .remedy-wt/f275-r66-rule.py.md
     Then `.agent/last_block.md` @C0d against the C0a blob. Report all four EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of every slice's
     BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report both
     numerals beside constraint 8's and say whether they agree. The block states no count
     of its own slices: the extraction is the sweep and its cardinality is your output.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN66: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. THREE appends in three commits, each proved by TWO readers and a negative
     control: C2 appends RECORD66 to `.agent/live_review.md`, C3 appends SLIPS66 to
     `.agent/prose_slips.md` and C4 appends DEC66 to `.agent/decisions.md`.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline and the slice's body. All three target files end with a
          single newline and no trailing blank line at the base, and all three separate
          their entries by a blank line, which is why the inserted newline is the same for
          each.
            .agent/live_review.md   pre 1011627 at the base, slice RECORD66
            .agent/prose_slips.md   pre  258183 at C2,       slice SLIPS66
            .agent/decisions.md     pre 1146996 at C3,       slice DEC66
          Report each pre size, each post size and each delta. The slice body sizes are
          NOT stated here: each is the length of what you extracted.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N for each of the three.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter — a byte b with
          `b < 128 and chr(b).isalpha()` — inside the FIRST appended paragraph, and report
          that BOTH readers reject it. Report ALSO that both readers ACCEPT the unmutated
          region, because a reader that rejects everything proves nothing by rejecting.
     (iv) RECORD66 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0. Report the count of `^- R-` and of `^Done: R-` lines that C2
          ADDS, both of which must be 0.
     (v)  Report RECORD66's first line beside the count of lines in `.agent/live_review.md`
          at `4de28049` already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.`,
          and whether the new first line matches that pattern and duplicates none of them.
          Report the number your script counted; this block states none.
     (vi) DEC66 must begin `## DECISION F275 D40 ` and `.agent/decisions.md` at the base
          must contain NO line matching `^## DECISION F275 D40`. Report both readings, and
          report the highest existing `^## DECISION F275 D\d+` heading at the base.
     (vii) The paragraph SLIPS66 adds must begin `2026-09-11 · F275 R65 · `. Report the
          count of lines in `.agent/prose_slips.md` at `4de28049` already beginning with
          that exact prefix, and the count C3 adds.

  G4 THE ARTEFACT AND THE INSTRUMENT ARE THE AUTHORED BLOBS AND NOTHING ELSE.
     `.agent/f275_t003_flip_residue_r66.md` at C5 must be byte-identical to the
     `.agent/authored/f275-r66-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show 4de28049:.agent/f275_t003_flip_residue_r66.md`, which must be non-zero.
     Report the artefact's line count and the instrument blob's line count, each against
     the DECISION F104 D1 cap of 500 insertions.

  G5 THE ARTEFACT'S NUMBERS AND ITS QUOTED TRANSCRIPT ARE RE-DERIVED FROM THE COMMITTED
     INSTRUMENT. The instrument is committed at `.agent/authored/f275-r66-rule.py.md` at
     C0c, inside a ```python fence. Report the number of fences found, extract that source
     into `.remedy-wt/` and RUN it with `python3 -B`, REDIRECTED to a file per constraint
     11. It prints four banners; report every line of all four.
     (a) THE FIGURES. Say whether each of these agrees with what the instrument printed.
         The artefact's section 4 states 2198 ruled keys, 2144 resolving to an `ast`
         Attribute at that exact position and 54 not. Section 6 states 24 probe rows with
         a synthetic receiver, on 24 distinct lines, all 24 of which begin `assert ` in the
         source, and 22 of the 52 drops sitting on such a line. Sections 2, 3 and 5 state
         the per-site blocks for `test_repair_loop_v1.py:56`, `long_run_executor.py:505`
         and `test_loop_run.py:285`, and section 4 the block for
         `long_run_executor.py:504`.
     (b) THE TRANSCRIPT, VERBATIM. Every line inside the artefact's fenced blocks that
         begins — after its leading whitespace is stripped — with any of `sweep `, `probe `,
         `ast `, `source:`, `ruled keys`, `resolving `, `NOT resolving`, `probe rows whose`,
         `distinct synthetic`, `distinct lines`, `of those lines`, `dropped sites` or
         `of them on a line` must appear, with ITS OWN leading whitespace stripped, as a
         line of the instrument's output. Report the count checked and the count that
         failed; the second must be 0. This is a CONTENT comparison after stripping, not a
         byte comparison, because a fenced block is indented and the instrument's own lines
         are not — and it exists because a transcript re-wrapped to fit a page is a
         transcript that no longer says what the tool said.
     (c) DETERMINISM. Run the SAME extracted file twice more and report whether all three
         outputs are byte-identical.
     A figure the instrument prints that DISAGREES with the artefact is reported as it
     read and is a finding; do not reconcile it in either direction. A figure the artefact
     states that the instrument does NOT print is likewise reported as absent rather than
     supplied from elsewhere — EXCEPT the reading the artefact's PROVENANCE list names as
     the reviewer's, which is the paired probe run of section 7. Two standing exceptions
     apply to any numeral sweep you run: digits inside an IDENTIFIER such as a SHA or a
     path, and numerals inside a CITATION of a named prior artefact, are not readings.

  G6 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `4de28049` and at C5, and whether all five are EQUAL.
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
     (b) The changed-path set over `4de28049`..C5 must be exactly the Change section's
         paths other than `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `docs/`, `scripts/`, `packages/`,
         `apps/` or `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `4de28049` and at C5. Report both, the ids registered,
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
             round 66, the one-sentence context self-assessment amend0905-throughput
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

BEGIN-PLAN66 sha256=0bb5e779029f581c41ebde2433fafe71d81d251a1cbc84c68c794b5bb9ba0374
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

ROUND 66 RULES the three sites DECISION F275 D39 held the write shut on, and DECISION F275
D40 records the result. They rule three ways: one correct drop, one site that was never in
the committed set, and one wrong drop whose cause is pytest's assertion rewriting — which
reaches 22 of the 52 drops, so the re-derived set is NOT safe to consume. A second and
independent defect is measured beside it: 54 of the 2198 ruled keys resolve to no `ast`
node at their recorded position, which is what the `long_run_executor.py:504` disagreement
round 64 reported turns out to be. The artefact is `.agent/f275_t003_flip_residue_r66.md`.
The round 65 verdict and its prose slip are booked here. No production line moves.

## Next Steps

1. RE-DERIVE from a PLAIN run: two suite passes under the committed probe with
   `--assert=plain`, rebuild the set, and confirm the 22 rewriting drops become refusals
   that the join keeps. That is the first half of what DECISION F275 D40 holds shut.
2. RULE THE 54 ruled keys that resolve to no `ast` node, and measure whether the
   transform's own consumption already loses them — which decides whether they are a
   reporting defect or a live under-selection in every dry run taken so far.
3. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
4. THE FLIP, then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The site set has now yielded three distinct position defects in four rounds — the line
  key, the rewriting and the sweep's own columns — and each was invisible to the gate that
  preceded it.
- `R-0880`'s SECOND obligation is still unbuilt, and the largest residue classes still need
  PRODUCTION-CODE work rather than another transform rule.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN66

BEGIN-RECORD66 sha256=73de51b131a365cae3188f0d9216b53a53333195f69ce081be01935c28c12b22
Gate: F275 R65 — the F275 round 65 entry. VERDICT PASS. Written by the planner and reviewer of session 24 after reading the committed range `98a67f4f`..`4de28049` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 66, per operator amendment amend0827-process-diet rule 1. The round SPENT the route DECISION F275 D38 ruled: the descriptor probe was re-keyed, the suite ran under it twice, and the ruled site set was re-derived, which the decision recorded at `95990d1e` rules.

G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: all four authored blobs are byte-identical to the reviewer's own scratch originals — the block at 32736 bytes, the artefact at 8531, the re-keyed probe at 6684 and the re-derivation instrument at 8499 — and `.agent/last_block.md` equals the block blob. All four slices matched the sha256 on their own BEGIN markers. Re-measured on the committed blob the block is 329 lines TOTAL and 249 PROSE, agreeing with its own constraint 8. G2: `.agent/plan.md` is byte-identical to its slice at 2728 bytes over 47 lines, both mandated headings exactly once.

G3: `.agent/live_review.md` goes 1006423 to 1011627, `.agent/prose_slips.md` 256246 to 258183 and `.agent/decisions.md` 1142043 to 1146996, every one exact under reader A, with reader B holding at N counted from the slice as 7, 2 and 9, and all three of the reviewer's own negative controls REJECTED by both readers while all three unmutated regions are ACCEPTED. The D39 heading reads 0 at the base against a highest existing D38. G4: the artefact at C5 is byte-identical to the C0b blob at 8531 bytes and the path does not resolve at the base. G6 and G7: five trees byte-identical; canary 42 passed at exit 0; ruff 26 rows at the frozen ceiling with zero under `.remedy-wt/` and zero `.py` under `.agent/`; ten changed paths with MISSING and EXTRA empty and zero production paths; the open set 88 at both ends with all three sets empty; per-commit insertions peak at 329 and every commit including the handback is under the cap, each touching exactly one path.

G5 CARRIED TWO INSTRUMENTS WITH DIFFERENT ORDERS AND BOTH HELD. The probe's fence was extracted and COMPILED and deliberately not run, at 6398 bytes; the re-derivation instrument was extracted and run THREE times to byte-identical 3606-byte captures. Every figure the block named agrees: 2195 probe rows in each run with symmetric difference 0 under both keys, 2082 receivers resolved against 113 refused, TWELVE round 53 keys covering more than one resolved receiver, the control rebuilding round 53's committed set SET-EQUAL at 2198, and the re-derivation reading 2168 under the line join against 2116 under the receiver join for 52 drops and no adds.

THE CONTROL IS THE PART OF THAT ROUND WORTH RECORDING, BECAUSE IT WAS ADDED AFTER A FAILURE RATHER THAN BY FORESIGHT. The reviewer's first rebuild did not reproduce round 53's set and read 2168 against 2198, and the cause was the INPUT rather than the logic — the new probe run compared against the old committed set, which is a two-variable comparison wearing a one-variable face. Feeding the rebuild round 53's OWN probe output makes it reproduce that set exactly, and only with that reading does the 2168-against-2116 comparison mean what it says. A rebuild that cannot reproduce the set it claims to re-derive is not a re-derivation, and this one could not until it was made to.

THE WORKER DECLARED TEN DEVIATIONS AND THE TWO SUBSTANTIVE ONES ARE SWEEP ARTEFACTS RATHER THAN PROVENANCE FAILURES, WHICH IT JUDGED CORRECTLY. Running the artefact's numerals against the instrument's output it found two survivors: the digits `98` and `67`, which are fragments of the base SHA in the header banner, and `504`, which the artefact cites in two places and attributes in both to the round 64 artefact and to round 64 by name. Neither is an undeclared reviewer reading — one is an identifier and the other a citation of a prior committed artefact — and the worker reported both as absent rather than supplying them from elsewhere, which is what the gate orders. The lesson is the sweep's rather than the artefact's and is booked as a dated line: a numeral sweep over prose flags digit-substrings of identifiers and numerals inside citations, so it needs an exception list of those two kinds or it will spend a deviation every round.

THE PROVENANCE PARAGRAPH WAS WRITTEN AS A LIST THIS ROUND AND THE LIST HELD, which is the rule the round before it booked being applied on its first opportunity and surviving contact with the sweep that broke its predecessor. The remaining eight deviations are the standing ones plus the probe's compiled-not-run asymmetry, which the block's constraint 12 orders and explains, and the note that G5's extraction leaves a real `.py` under `.remedy-wt/` which G6(c) independently measures at zero ruff rows.
END-RECORD66

BEGIN-SLIPS66 sha256=d7bd91dac885db97d945816894bafb6185a0ba30d88a41efbcbdb4b4e3ef9192
2026-09-11 · F275 R65 · The round 65 block's G5 ordered every figure the artefact states to be re-derived from the instrument, and the worker's numeral sweep over the artefact returned two survivors that are not readings at all: `98` and `67`, which are digit fragments of the base SHA `98a67f4f` in the header banner, and `504`, which the artefact cites twice and attributes in both places to `.agent/f275_t003_flip_residue_r64.md` and to round 64 by name. The round 64 block had excused the base SHA explicitly and the round 65 block, adapted from it, dropped that clause while keeping the sweep. THE RULE THAT FOLLOWS: a numeral sweep over prose is a tokeniser and not a reader, so the gate that orders one names its two standing exceptions — digits inside an IDENTIFIER such as a SHA or a path, and numerals inside a CITATION of a named prior artefact — and anything outside those two is a finding.
END-SLIPS66

BEGIN-DEC66 sha256=eef61db96891071a9a43339b0a218588a12873bfff92169ae13defc66a5eb7c5
## DECISION F275 D40 (2026-09-11, F275 round 66) — the three sites are ruled, the re-derived set is NOT safe to consume, and two independent defects hold the write shut

CONTEXT. DECISION F275 D39 re-derived the ruled site set with a receiver in its key and held the write shut on three sites its own evidence could not justify. This round rules them. The measurement is in `.agent/f275_t003_flip_residue_r66.md` and the instrument that produced it is committed at `.agent/authored/f275-r66-rule.py.md`.

CHOSEN, PART ONE: THE THREE RULE THREE DIFFERENT WAYS, AND ONLY ONE OF THEM IS THE DROP D39 THOUGHT IT WAS. `tests/orchestration/test_repair_loop_v1.py:56` is a CORRECT drop: three `.id` reads share the line, the probe resolves `job` and `task`, and `art` is an Artifact the probe never installs a descriptor on, so the third site was ruled only by sharing a line — which is finding `R-0880`'s over-selection being fixed exactly as designed. `packages/orchestration/long_run_executor.py:505` is NOT A DROP AT ALL: its site reads `RULED False` against round 53's committed set, and it reached the drop list only because this round's rebuild recomputes from the sweep's raw sites. `tests/orchestration/test_loop_run.py:285` is a WRONG drop, and its cause is not local.

CHOSEN, PART TWO: PYTEST'S ASSERTION REWRITING MAKES THE PROBE RESOLVE A NAME THAT DOES NOT EXIST, AND IT REACHES 22 OF THE 52 DROPS. Pytest rewrites `assert` statements into temporaries before compiling them, and the re-keyed probe reads the frame of that rewritten code, so the name its disassembly recovers is one pytest invented. Twenty-four probe rows resolve to a synthetic `@py_assert<n>` name, every one of the twenty-four on a line beginning `assert ` in the source, and twenty-two of the fifty-two drops sit on such a line. Those twenty-two are UNDER-selections, which is finding `R-0879`'s class arriving through the new key rather than through the old one. THE RE-DERIVED SET OF D39 IS THEREFORE NOT SAFE TO CONSUME, and this decision says so before any round spends it.

CHOSEN, PART THREE: A SECOND AND INDEPENDENT DEFECT IS MEASURED IN THE SWEEP'S OWN POSITIONS. Of 2198 ruled keys, 2144 resolve to an `ast` Attribute node at their exact recorded line and column and 54 DO NOT. `long_run_executor.py:504` is the instance round 64 reported and could not diagnose: the sweep placed two sites on that line, at columns 19 and 40, over ONE attribute node at column 30, and gave the second of them a receiver belonging to the NEXT line inside the same multi-line call. A key that resolves to no node is missed silently by any consumer that walks the tree, because a lookup finding nothing is indistinguishable from a site that was never ruled. This defect is independent of the receiver key and of the rewriting, and it is an under-selection too.

CHOSEN, PART FOUR: THE ROUTE IS `--assert=plain`, AND WHAT IT BUYS IS AN HONEST REFUSAL RATHER THAN A RECOVERED NAME. Run over one file twice, the same committed probe resolves four synthetic receivers as round 65 ran it and FOUR NONES with rewriting disabled, at an unchanged row count. That is the right direction and the reason is worth stating: the receiver in those asserts is a subscript, so the correct answer was always a refusal, and under the join a refusal keeps the site's old standing. A wrong name became an honest absence, which cannot cause an under-selection. THE WRITE STAYS SHUT until the set is re-derived from a plain run AND the 54 non-resolving keys are ruled.

ALTERNATIVES CONSIDERED. (i) Consume the D39 set and repair the 22 afterwards — rejected: 22 under-selections in a set that drives a rename are 22 renames that silently do not happen, and a missed rename fails at run time in a place that does not name the cause. (ii) Special-case the `@py_assert` prefix in the resolution and treat it as a refusal — not rejected on correctness and rejected on honesty: it patches the symptom in the instrument while the probe still measures rewritten code, and the next rewriting pytest invents would be invisible. `--assert=plain` removes the cause. (iii) Rule only the three D39 named and leave the class — rejected on this round's own arithmetic: the third of the three is one of twenty-two, and ruling it without its class would have closed the decision on a number known to be wrong. (iv) Repair the sweep's 54 positions in the same round — rejected as scope: it is a separate instrument with a separate proof, and DECISION F275 D39's write is already shut for the other reason.

WHAT THIS DECISION DOES NOT RULE. It does not re-derive anything; the plain run is the next round and costs two more suite passes. It does not repair the 54 non-resolving keys, and it does not ask whether the transform's own consumption already loses them — that question is now on the plan and nothing has measured it. It does not resolve `R-0880`, whose second obligation is still unbuilt, and it registers no id: nothing measured here is wrong on disk under `packages/`, `apps/`, `tests/` or `docs/`.

HOW TO REVERSE: delete this decision. DECISION F275 D39's condition then stands at its three named sites with no ruling on any of them, and the 22 rewriting drops and the 54 non-resolving keys go back to being unmeasured rather than untouched.
END-DEC66
