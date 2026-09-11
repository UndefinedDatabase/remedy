── STEP T003 / round 65 — F275 ────────────────────────────────
Goal:        Land the RE-DERIVATION of the ruled site set with a receiver in its key, and
             the decision that rules the result. The route DECISION F275 D38 chose was
             spent: the descriptor probe's key gained `lasti` and `recv`, the suite ran
             under it twice, and the set was rebuilt under a control that reproduces round
             53's committed set exactly. DECISION F275 D36's condition on the write falls
             from 39 sites to 3, named. The artefact and BOTH instruments are reviewer
             texts transported as whole files. The round 64 verdict and its two prose slips
             are booked. NO LINE UNDER `packages/`, `apps/`, `tests/`, `docs/` OR
             `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r65.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r65-artefact.md`
             C0c  save the re-keyed probe verbatim as
                  `.agent/authored/f275-r65-probe.py.md`
             C0d  save the re-derivation instrument verbatim as
                  `.agent/authored/f275-r65-rederive.py.md`
             C0e  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN65, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD65 appended
             C3   `.agent/prose_slips.md` <- slice SLIPS65 appended
             C4   `.agent/decisions.md` <- slice DEC65 appended
             C5   `.agent/f275_t003_flip_residue_r65.md` <- a copy of the C0b blob
             C6   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r65.md                NEW
               .agent/authored/f275-r65-artefact.md       NEW
               .agent/authored/f275-r65-probe.py.md       NEW
               .agent/authored/f275-r65-rederive.py.md    NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               .agent/decisions.md
               .agent/f275_t003_flip_residue_r65.md       NEW
               .agent/handoff.md
             The five paths marked NEW do not exist at the base: `git ls-tree 98a67f4f --`
             over all five prints nothing at exit 0.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r65.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. A slice's BODY is the bytes from the start of the line after
     its BEGIN marker to the first byte of its END marker line, INCLUDING the terminal
     newline of the body's last line. Each BEGIN marker carries its slice's own sha256;
     check it. The artefact and BOTH instruments are WHOLE FILES: copy each with
     `shutil.copyfile` and never open any of them in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 64 across
     C0a to C0e and becomes current at C1, which is the first SUBSTANTIVE commit and is
     what item 23 of §3 of `docs/agents/planner_reviewer_prompt.md` requires of a round
     that touches the finding ledger.
  4. This round creates NO `git worktree` and runs nothing destructive. The reviewer's own
     worktree was created, used for the two probe runs and removed BEFORE this block was
     written, and `git worktree list` shows the primary checkout alone at the base.
  5. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  6. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  7. Re-read `.agent/STOP` FROM DISK before the first commit and again before C6, and
     report both readings literally. It does not exist at the reviewer's base reading.
  8. This block is 329 lines TOTAL and 249 PROSE, measured on its final bytes.
  9. NO finding id is registered this round and NONE is resolved. The open set is 88 by
     distinct id at the base and must read 88 at C5, with the registered set, the resolved
     set and the de-registered set ALL EMPTY. The COUNT alone is not the gate; the
     membership is. `R-0880`'s SECOND obligation stays unbuilt and DEC65 says so. The two
     prose slips SLIPS65 books are NOT ids, per amend0827-process-diet rule 2.
 10. BOTH `.agent/authored/f275-r65-probe.py.md` and
     `.agent/authored/f275-r65-rederive.py.md` are `.md` and their extension is
     load-bearing: a `.py` file anywhere `ruff check .` scans is counted by
     `tests/orchestration/test_ci_budgets.py`, whose ceiling G6(c) reads. Do not rename
     either, and do not land a runnable copy of either anywhere in the tree.
 11. A pipe into `tail` MASKS the real exit code. Redirect to a file and read the file
     instead, for every gate whose exit code you report.
 12. THE PROBE IS NOT RUN BY THIS ROUND AND G5 DOES NOT ORDER IT RUN. It installs a
     property over `packages.core.models` and refuses unless it sits at the root of the
     tree it is measuring, which is why the reviewer ran it inside a worktree that no
     longer exists. G5 asks only that its fence extract and COMPILE. Running it here would
     either refuse or take twenty-one minutes, and neither is this round's work.

Done when:   the seven gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C6.

  G1 TRANSPORT. For each of the four authored blobs, compare the COMMITTED blob against
     the reviewer's scratch original by size and sha256:
       .agent/authored/f275-r65.md              @C0a  vs  .remedy-wt/f275-r65.block.md
       .agent/authored/f275-r65-artefact.md     @C0b  vs  .remedy-wt/f275-r65-artefact.md
       .agent/authored/f275-r65-probe.py.md     @C0c  vs  .remedy-wt/f275-r65-probe.py.md
       .agent/authored/f275-r65-rederive.py.md  @C0d  vs  .remedy-wt/f275-r65-rederive.py.md
     Then `.agent/last_block.md` @C0e against the C0a blob. Report all five EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of every slice's
     BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report both
     numerals beside constraint 8's and say whether they agree. The block states no count
     of its own slices: the extraction is the sweep and its cardinality is your output.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN65: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. THREE appends in three commits, each proved by TWO readers and a negative
     control: C2 appends RECORD65 to `.agent/live_review.md`, C3 appends SLIPS65 to
     `.agent/prose_slips.md` and C4 appends DEC65 to `.agent/decisions.md`.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline and the slice's body. All three target files end with a
          single newline and no trailing blank line at the base, and all three separate
          their entries by a blank line, which is why the inserted newline is the same for
          each.
            .agent/live_review.md   pre 1006423 at the base, slice RECORD65
            .agent/prose_slips.md   pre  256246 at C2,       slice SLIPS65
            .agent/decisions.md     pre 1142043 at C3,       slice DEC65
          Report each pre size, each post size and each delta. The slice body sizes are
          NOT stated here: each is the length of what you extracted.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N for each of the three.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter — a byte b with
          `b < 128 and chr(b).isalpha()` — inside the FIRST appended paragraph, and report
          that BOTH readers reject it. Report ALSO that both readers ACCEPT the unmutated
          region, because a reader that rejects everything proves nothing by rejecting.
     (iv) RECORD65 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0. Report the count of `^- R-` and of `^Done: R-` lines that C2
          ADDS, both of which must be 0.
     (v)  Report RECORD65's first line beside the count of lines in `.agent/live_review.md`
          at `98a67f4f` already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.`,
          and whether the new first line matches that pattern and duplicates none of them.
          Report the number your script counted; this block states none.
     (vi) DEC65 must begin `## DECISION F275 D39 ` and `.agent/decisions.md` at the base
          must contain NO line matching `^## DECISION F275 D39`. Report both readings, and
          report the highest existing `^## DECISION F275 D\d+` heading at the base.
     (vii) Both paragraphs SLIPS65 adds must begin `2026-09-11 · F275 R64 · `. Report the
          count of lines in `.agent/prose_slips.md` at `98a67f4f` already beginning with
          that exact prefix, and the count C3 adds.

  G4 THE ARTEFACT AND THE INSTRUMENTS ARE THE AUTHORED BLOBS AND NOTHING ELSE.
     `.agent/f275_t003_flip_residue_r65.md` at C5 must be byte-identical to the
     `.agent/authored/f275-r65-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show 98a67f4f:.agent/f275_t003_flip_residue_r65.md`, which must be non-zero.
     Report the artefact's line count and BOTH instrument blobs' line counts, each against
     the DECISION F104 D1 cap of 500 insertions.

  G5 THE ARTEFACT'S NUMBERS ARE RE-DERIVED FROM THE COMMITTED INSTRUMENTS.
     Both instruments are committed inside a single ```python fence each. Report the number
     of fences found in each blob.
     (a) THE PROBE, at `.agent/authored/f275-r65-probe.py.md` @C0c. Extract its fence and
         COMPILE it with `compile(<source>, <name>, "exec")`, reporting that it compiles.
         DO NOT RUN IT — constraint 12 states why. Report the extracted byte count.
     (b) THE REBUILD, at `.agent/authored/f275-r65-rederive.py.md` @C0d. Extract its fence
         into `.remedy-wt/` and RUN it with `python3 -B`, REDIRECTED to a file per
         constraint 11. It prints banners numbered 1, 2, 3, 4, 5, 5b and 6; report every
         line of all of them.
     (c) THE FIGURES. Say whether each of these agrees with what the instrument printed.
         The artefact's section 2 states 2195 probe rows in each run, and symmetric
         difference 0 under both keys, at 2145 and 2195. Section 3 states 2082 resolved
         against 113 refused, 111 of them with `direct=True` and 2 with `direct=False`.
         Section 4 states TWELVE round 53 keys covering more than one resolved receiver,
         and lists all twelve. Section 5 states the control rebuilding round 53's set at
         2198 and SET-EQUAL True. Section 6 states 2168 under the line join, 2116 under
         the receiver join, a drift of 32, and 52 dropped with 0 added. Section 7 states
         52 dropped as 31 at-risk, 23 with no sweep receiver, 5 both and 3 NEITHER, and
         names those three; it also states 31 dropped and 45 remaining of the 78 sites on
         D36's 39 lines, with 38 lines reached and 1 not.
     (d) DETERMINISM. Run the SAME extracted rebuild twice more and report whether all
         three outputs are byte-identical. The instrument walks sets, and round 64's
         equivalent clause caught a real non-determinism in a tie-broken counter, so this
         is a gate rather than a formality.
     A figure the instrument prints that DISAGREES with the artefact is reported as it
     read and is a finding; do not reconcile it in either direction. A figure the artefact
     states that the instrument does NOT print is likewise reported as absent rather than
     supplied from elsewhere — EXCEPT the readings the artefact's own PROVENANCE paragraph
     lists as the reviewer's, which are the two pytest summary lines of section 2 and the
     four receiver-shape cases of section 3. Those are named there as a LIST and are not
     owed here; anything else absent is a finding against that list.

  G6 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `98a67f4f` and at C5, and whether all five are EQUAL.
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
         removed any worktree, which constraint 4 fixes at neither. Take the porcelain
         reading AFTER G5 has run.
     (b) The changed-path set over `98a67f4f`..C5 must be exactly the Change section's
         paths other than `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `docs/`, `scripts/`, `packages/`,
         `apps/` or `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `98a67f4f` and at C5. Report both, the ids registered,
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
             round 65, the one-sentence context self-assessment amend0905-throughput
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

BEGIN-PLAN65 sha256=8527249b66f13485a2bb9cb8a2b17106836d5fb84947c5bdd6d555d39c4e56ca
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

ROUND 65 SPENDS the route DECISION F275 D38 ruled, and DECISION F275 D39 rules the result.
The descriptor probe's key gains `lasti` and `recv`, the suite ran under it twice with
symmetric difference 0 under both keys, and the ruled site set is re-derived: 2168 under
the line join and 2116 under the receiver join, a one-variable difference of 52 drops and
no adds, with the rebuild controlled against round 53's own committed set. DECISION F275
D36's condition on the write falls from 39 sites to 3, named. The artefact is
`.agent/f275_t003_flip_residue_r65.md`. The round 64 verdict and its two prose slips are
booked here. No production line moves.

## Next Steps

1. RULE THE THREE sites DECISION F275 D39 names — `long_run_executor.py:505`,
   `test_loop_run.py:285` and `test_repair_loop_v1.py:56` — one by one, each with the
   reading that rules it, and diagnose the `long_run_executor.py:504` disagreement round 64
   reported one line above the first of them. That opens the write.
2. Point the transform at the re-derived set and re-run the flip's dry run, which is the
   first reading of what the re-keying costs or saves in failures rather than in sites.
3. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
4. THE FLIP, then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The largest residue classes need PRODUCTION-CODE work rather than another transform rule,
  which is a bigger step than any round since 34 has taken.
- `R-0880`'s SECOND obligation is still unbuilt, and the `long_run_executor.py:504`
  disagreement is still undiagnosed.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN65

BEGIN-RECORD65 sha256=7587940aa8f8386f0bee52c506a42ba6f3fdf9be1d42de0c14b8ac85320bbb0c
Gate: F275 R64 — the F275 round 64 entry. VERDICT PASS. Written by the planner and reviewer of session 24 after reading the committed range `30072048`..`98a67f4f` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 65, per operator amendment amend0827-process-diet rule 1. The round measured that DECISION F275 D36's part-three remedy is unimplementable on this interpreter and the decision recorded at `39dbde28` ruled the route that replaces it.

G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: all three authored blobs are byte-identical to the reviewer's own scratch originals — the block at 33717 bytes, the artefact at 7530 and the route instrument at 7288 — and `.agent/last_block.md` equals the block blob. All four slices matched the sha256 on their own BEGIN markers. Re-measured on the committed blob the block is 333 lines TOTAL and 255 PROSE, agreeing with its own constraint 8. G2: `.agent/plan.md` is byte-identical to its slice at 2837 bytes over 47 lines, both mandated headings exactly once.

G3: `.agent/live_review.md` goes 1000844 to 1006423, `.agent/prose_slips.md` 255085 to 256246 and `.agent/decisions.md` 1136331 to 1142043, every one exact under reader A, with reader B holding at N counted from the slice as 7, 1 and 9. The reviewer ran its own negative control on each and all three are REJECTED by both readers while all three unmutated regions are ACCEPTED. The D38 heading reads 0 at the base against a highest existing D37, and the round 63 slip prefix reads 0 at the base against 1 added. G4: the artefact at C5 is byte-identical to the C0b blob at 7530 bytes and the path does not resolve at the base.

G5 CARRIED A DETERMINISM CLAUSE FOR THE FIRST TIME AND IT HELD. The reviewer extracted the instrument from the committed blob and ran it three times: the three captures are BYTE-IDENTICAL at 2029 bytes. Every figure agrees — Python 3.10.12 with `co_positions` absent, a frame carrying `f_lasti` and `f_lineno`, two reads on one line collapsing to ONE key by line and separating into TWO with the offset, the offsets resolving to `'a'` and `'b'` in source order, and over the 39 at-risk lines a receiver-shape table of 68 Name against 4 Subscript, 3 Call and 2 Attribute, with nine refusals every one under `tests/` and one ruled-site-against-node disagreement at `long_run_executor.py:504`. G6 and G7: all five top-level trees byte-identical including `packages`, which is the tree the instrument installs a property into in its own process; canary 42 passed at exit 0; `ruff check .` 26 rows at the frozen ceiling with zero under `.remedy-wt/` and zero `.py` rows under `.agent/`; nine changed paths with MISSING and EXTRA empty and zero production paths; the open set 88 at both ends with all three sets empty; per-commit insertions peak at 333 and the handback commit is 405, all under the cap.

THE WORKER DECLARED NINE DEVIATIONS AND TWO OF THEM ARE THE REVIEWER'S. The first is the same class as round 63's and is booked as a dated line: the artefact's PROVENANCE paragraph claims there is NO reviewer-only reading in it, and two readings are — the sentence that the four production lines D36 names are all inside the 68, which FOLLOWS from the printed refusals rather than being printed, and the source line quoted at `long_run_executor.py:504`, which the reviewer read off disk. The worker checked that quoted line against the file and found it exact, declared both rather than reconciling either, and that is the right handling of a provenance claim it cannot verify from the instrument alone.

THE SECOND IS IN THE DELEGATION NOTE RATHER THAN IN ANY ARTEFACT, AND IT IS WORTH THE RECORD BECAUSE OF WHERE IT CAME FROM. That note warned the worker that the instrument prints two `Error: no job matches prefix` lines on stderr and that they are not a failure. That was true of ROUND 63's instrument, which called the shipped resolver against a synthetic store; round 64's instrument calls no handler at all and printed nothing of the kind, which the worker measured across three 2031-byte captures and declared. The note was adapted from the previous round's rather than rewritten, which is the identical mechanism as round 62's stale round numeral, one class and two rounds apart. Nothing on disk is wrong and no id is spent.

THE REMAINING SEVEN DEVIATIONS ARE SOUND AND ONE OF THEM IS THE WORKER CATCHING ITSELF. Its first G3 invocation exited 1 on a `SyntaxError` in its OWN gate script, an em dash inside a byte literal; it fixed the script, re-ran to 0, reported both invocations and noted that neither touched a repository file. It also recorded that G5's extraction leaves a real `.py` under `.remedy-wt/`, and that G6(c) independently measures zero ruff rows there, so constraint 10's ceiling is untouched by the very file the gate creates. The rest are the standing ones: the plan naming round 63 across the block-save commits, ruff exiting 1 by design while the gate is the count, the absence probe at 128, and gates written to files because the shell rejects `$?` by form.
END-RECORD65

BEGIN-SLIPS65 sha256=1ba50448c6c866180c0d30aa00b02cf302e5bcacadd1ad1d6da96efbd922de99
2026-09-11 · F275 R64 · The round 64 artefact's PROVENANCE paragraph claimed "There is no reviewer-only reading in this artefact", and two of its readings are: the sentence that the four production lines DECISION F275 D36 names are all inside the 68, which FOLLOWS from the printed refusals but is not itself printed, and the source line quoted at `packages/orchestration/long_run_executor.py:504`, which the reviewer read off disk. The counter-measure written one round earlier WAS run — every numeral in the artefact was swept against the instrument's output and only the base SHA came back absent — and it did not catch these, because both are PROSE rather than numerals and a numeral sweep sees neither. THE RULE THAT FOLLOWS: an absolute provenance claim is the expensive kind, so state the claim as a LIST of what the instrument re-derives rather than as a denial that anything else exists; a denial is measured over every sentence of the document and a list is measured over itself.

2026-09-11 · F275 R64 · The round 64 delegation note warned the worker that the instrument prints two `Error: no job matches prefix` lines on stderr and that they are not a failure. That was true of ROUND 63's instrument, which called the shipped resolver against a synthetic store; round 64's instrument calls no handler and printed nothing of the kind, which the worker measured and declared. The note was adapted from the previous round's rather than rewritten — the identical mechanism as round 62's stale round numeral, one class and two rounds apart, and this time in the one artefact of a round that no gate ever reads. THE RULE THAT FOLLOWS: the delegation note is adapted from the previous round's and therefore gets the same sweep the block gets — every fact it asserts about THIS round's instrument is checked against that instrument's own output before it is sent, and a note that cannot be checked says nothing instead.
END-SLIPS65

BEGIN-DEC65 sha256=7c30fe1bc9ed59e7a8cd07f49424b018a3c2a19541f939120949e0ba35a82fcf
## DECISION F275 D39 (2026-09-11, F275 round 65) — the ruled site set is re-derived with a receiver in its key, and three sites hold the write shut

CONTEXT. DECISION F275 D36 forbade any round to consume the ruled site set for a WRITE until either the 39 at-risk sites were resolved pair by pair or the set was re-derived with a discriminating key, and DECISION F275 D38 replaced its unimplementable `col_offset` remedy with `f_lasti` plus a disassembly. This round SPENDS that route. The measurement is in `.agent/f275_t003_flip_residue_r65.md`, the re-keyed probe is committed at `.agent/authored/f275-r65-probe.py.md`, and the instrument that rebuilds the set is at `.agent/authored/f275-r65-rederive.py.md`.

CHOSEN, PART ONE: THE RE-DERIVATION IS PERFORMED AND IT REPRODUCES. The descriptor probe's key gains `lasti` and `recv`, the suite ran under it twice, and the two runs are set-equal under BOTH the old key at 2145 and the new one at 2195, symmetric difference 0 in each case. The re-keyed probe is therefore exactly as reproducible as the one it replaces, which is the only precondition that mattered: an instrument that measured a different set each run could not be the input to anything.

CHOSEN, PART TWO: THE REBUILD IS CONTROLLED BEFORE IT IS BELIEVED. Fed ROUND 53's OWN probe output under the LINE join, the rebuild reproduces round 53's committed ruled set as a SET at 2198. That control was not decoration: the first attempt at this rebuild did not reproduce it, and the cause was the input rather than the logic — the new probe run against the old committed set, which is a two-variable comparison wearing a one-variable face. Only with the control passing does the next number mean what it says.

CHOSEN, PART THREE: THE RECEIVER JOIN DROPS 52 AND ADDS NONE. Built from ONE probe run and differing only in the join, the line-keyed set is 2168 and the receiver-keyed set is 2116. The drift of 32 between round 53's set and this round's line-keyed set is a SEPARATE quantity, caused by the tree moving across the rounds between them, and it is never added to the 52. Where the probe REFUSED a receiver on a line, every site on that line keeps its old standing, because a refusal is an absence of evidence and turning it into a strike is finding `R-0879` arriving from the other side.

CHOSEN, PART FOUR: THE WRITE STAYS SHUT, ON A SMALLER AND NAMED CONDITION. Of the 52 drops, 31 are on the at-risk lines D36 bounded and 23 are sites for which the static sweep recorded no receiver at all, 5 of them both. THREE are neither: `packages/orchestration/long_run_executor.py:505` with sweep receiver `entry`, `tests/orchestration/test_loop_run.py:285` with `job`, and `tests/orchestration/test_repair_loop_v1.py:56` with `art`. Each is a site the sweep named a receiver for, on a line the probe reached, where the probe named a different one — a correct drop or an under-selection, and nothing measured so far decides which. NO ROUND MAY CONSUME THE RE-DERIVED SET FOR A WRITE UNTIL THOSE THREE ARE RULED, one by one, with the reading that rules each recorded. That is what replaces D36's clause: the prohibition is unchanged in kind and its condition has gone from 39 to 3.

ALTERNATIVES CONSIDERED. (i) Consume the re-derived set now and treat the three as noise — rejected: it is exactly the reasoning that produced `R-0880`, where a set was consumed because its defect looked small. (ii) Strike all three — rejected: two of them name a receiver the sweep and the probe disagree about, and striking on a disagreement is choosing the under-selection without reading either side. (iii) Keep D36's first route and resolve the 39 by hand instead — rejected as redundant: the re-derivation already separates every line the suite reaches, and 31 of the 39's sites are now dropped by measurement rather than by reading. (iv) Re-run the flip's dry run against the new set this round — not rejected, and deliberately not done: a dry run is twenty-one minutes and its value depends on the three rulings above, so it is the round after them and not this one.

WHAT THIS DECISION DOES NOT RULE. It does not rule the three. It does not point any instrument at the re-derived set — the transform still consumes the old one and no round may change that until the three are ruled. It does not diagnose the `long_run_executor.py:504` disagreement round 64 reported, which sits one line above one of the three. It does not touch the 113 refusals, whose sites keep their old standing by design. And it does not resolve `R-0880`, whose SECOND obligation — the transform's refusal to rename a site whose owner verdict cannot be confirmed — is still unbuilt, though the probe's own refusal behaviour is now the model for it.

HOW TO REVERSE: delete this decision. The re-keyed probe, the two runs and the rebuild stay on disk and in the artefact; what returns is DECISION F275 D36's clause with its condition at 39 rather than at 3.
END-DEC65
