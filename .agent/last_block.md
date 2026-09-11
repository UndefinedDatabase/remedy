── STEP T003 / round 64 — F275 ────────────────────────────────
Goal:        Land the measurement that DECISION F275 D36's blocker needs and the decision
             that rules it. D36 part three orders a `col_offset` this interpreter cannot
             supply; `f_lasti` discriminates instead, measured on the real pydantic model
             through the probe's own outward walk, and its coverage over the 39 at-risk
             lines is counted with its refusals enumerated. The artefact and the instrument
             are reviewer texts transported as whole files. The round 63 verdict and its
             prose slip are booked. NO LINE UNDER `packages/`, `apps/`, `tests/`, `docs/`
             OR `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r64.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r64-artefact.md`
             C0c  save the route instrument verbatim as
                  `.agent/authored/f275-r64-route.py.md`
             C0d  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN64, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD64 appended
             C3   `.agent/prose_slips.md` <- slice SLIPS64 appended
             C4   `.agent/decisions.md` <- slice DEC64 appended
             C5   `.agent/f275_t003_flip_residue_r64.md` <- a copy of the C0b blob
             C6   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r64.md                NEW
               .agent/authored/f275-r64-artefact.md       NEW
               .agent/authored/f275-r64-route.py.md       NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               .agent/decisions.md
               .agent/f275_t003_flip_residue_r64.md       NEW
               .agent/handoff.md
             The four paths marked NEW do not exist at the base: `git ls-tree 30072048 --`
             over all four prints nothing at exit 0.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r64.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. A slice's BODY is the bytes from the start of the line after
     its BEGIN marker to the first byte of its END marker line, INCLUDING the terminal
     newline of the body's last line. Each BEGIN marker carries its slice's own sha256;
     check it. The artefact and the instrument are WHOLE FILES: copy each with
     `shutil.copyfile` and never open either in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 63 across
     C0a, C0b, C0c and C0d and becomes current at C1, which is the first SUBSTANTIVE
     commit and is what item 23 of §3 of `docs/agents/planner_reviewer_prompt.md` requires
     of a round that touches the finding ledger.
  4. This round creates NO `git worktree` and runs nothing destructive. `git worktree list`
     shows the primary checkout alone at the base, and the reviewer created none this
     round: its measurement ran in the primary checkout because every probe in it is a
     read, plus one descriptor installed IN ITS OWN PROCESS.
  5. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  6. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  7. Re-read `.agent/STOP` FROM DISK before the first commit and again before C6, and
     report both readings literally. It does not exist at the reviewer's base reading.
  8. This block is 333 lines TOTAL and 255 PROSE, measured on its final bytes.
  9. NO finding id is registered this round and NONE is resolved. The open set is 88 by
     distinct id at the base and must read 88 at C5, with the registered set, the resolved
     set and the de-registered set ALL EMPTY. The COUNT alone is not the gate; the
     membership is. `R-0880` stays OPEN with both obligations where DECISION F275 D36 left
     them, and DEC64 says so in its own closing paragraph. The prose slip SLIPS64 books is
     NOT an id, per operator amendment amend0827-process-diet rule 2.
 10. `.agent/authored/f275-r64-route.py.md` is a `.md` and its extension is load-bearing:
     a `.py` file anywhere `ruff check .` scans is counted by
     `tests/orchestration/test_ci_budgets.py`, whose ceiling G6(c) reads. Do not rename it,
     and do not land a runnable copy of it anywhere in the tree.
 11. A pipe into `tail` MASKS the real exit code. Redirect to a file and read the file
     instead, for every gate whose exit code you report.
 12. The instrument G5 runs INSTALLS a property over `packages.core.models.Job.id` inside
     its own interpreter process. It writes no file anywhere and it does not touch the
     module on disk; G6(a) measures the `packages` tree object and G7(a) the porcelain
     status, and those two together are what prove it.

Done when:   the seven gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C6.

  G1 TRANSPORT. For each of the three authored blobs, compare the COMMITTED blob against
     the reviewer's scratch original by size and sha256:
       .agent/authored/f275-r64.md           @C0a  vs  .remedy-wt/f275-r64.block.md
       .agent/authored/f275-r64-artefact.md  @C0b  vs  .remedy-wt/f275-r64-artefact.md
       .agent/authored/f275-r64-route.py.md  @C0c  vs  .remedy-wt/f275-r64-route.py.md
     Then `.agent/last_block.md` @C0d against the C0a blob. Report all four EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of every slice's
     BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report both
     numerals beside constraint 8's and say whether they agree. The block states no count
     of its own slices: the extraction is the sweep and its cardinality is your output.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN64: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. THREE appends in three commits, each proved by TWO readers and a negative
     control: C2 appends RECORD64 to `.agent/live_review.md`, C3 appends SLIPS64 to
     `.agent/prose_slips.md` and C4 appends DEC64 to `.agent/decisions.md`.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline and the slice's body. All three target files end with a
          single newline and no trailing blank line at the base, and all three separate
          their entries by a blank line, which is why the inserted newline is the same for
          each.
            .agent/live_review.md   pre 1000844 at the base, slice RECORD64
            .agent/prose_slips.md   pre  255085 at C2,       slice SLIPS64
            .agent/decisions.md     pre 1136331 at C3,       slice DEC64
          Report each pre size, each post size and each delta. The slice body sizes are
          NOT stated here: each is the length of what you extracted.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N for each of the three.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter — a byte b with
          `b < 128 and chr(b).isalpha()` — inside the FIRST appended paragraph, and report
          that BOTH readers reject it. Report ALSO that both readers ACCEPT the unmutated
          region, because a reader that rejects everything proves nothing by rejecting.
     (iv) RECORD64 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0. Report the count of `^- R-` and of `^Done: R-` lines that C2
          ADDS, both of which must be 0.
     (v)  Report RECORD64's first line beside the count of lines in `.agent/live_review.md`
          at `30072048` already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.`,
          and whether the new first line matches that pattern and duplicates none of them.
          Report the number your script counted; this block states none.
     (vi) DEC64 must begin `## DECISION F275 D38 ` and `.agent/decisions.md` at the base
          must contain NO line matching `^## DECISION F275 D38`. Report both readings, and
          report the highest existing `^## DECISION F275 D\d+` heading at the base.
     (vii) The paragraph SLIPS64 adds must begin `2026-09-11 · F275 R63 · `. Report the
          count of lines in `.agent/prose_slips.md` at `30072048` already beginning with
          that exact prefix, and the count C3 adds.

  G4 THE ARTEFACT AND THE INSTRUMENT ARE THE AUTHORED BLOBS AND NOTHING ELSE.
     `.agent/f275_t003_flip_residue_r64.md` at C5 must be byte-identical to the
     `.agent/authored/f275-r64-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show 30072048:.agent/f275_t003_flip_residue_r64.md`, which must be non-zero.
     Report the artefact's line count and the instrument blob's line count, each against
     the DECISION F104 D1 cap of 500 insertions.

  G5 THE ARTEFACT'S NUMBERS ARE RE-DERIVED FROM THE COMMITTED INSTRUMENT.
     The instrument is committed at `.agent/authored/f275-r64-route.py.md` at C0c, inside a
     ```python fence. Extract that fenced source into `.remedy-wt/` and RUN it with
     `python3 -B`, REDIRECTED to a file per constraint 11. Report the number of fences
     your script found. It prints four banners; report from its OUTPUT, and where a
     reading below names a token, `grep` the output for that token rather than reading
     around it.
     (a) Banner 1. Report all three of its lines literally. The artefact's section 2
         states `python 3.10.12`, `co_positions` at False, and a frame carrying
         `f_lasti` and `f_lineno`. Say whether each agrees.
     (b) Banner 2. Report every line literally, including the two recorded reads with
         their `f_lasti` values, the three counts, and the line beginning
         `the offset DISCRIMINATES`. The artefact's section 3 states 2 reads, 1 distinct
         `(path, line, func)` key, 2 distinct with `f_lasti`, and True.
     (c) Banner 3. Report both resolution lines and the line beginning
         `receivers resolved in order`. The artefact's section 4 states `'a'` then `'b'`
         and MATCH True.
     (d) Banner 4. Report the at-risk line and the three counts beneath it, every row of
         the receiver-shape table, the line beginning `a bare Name`, every one of the
         lines listing a receiver the route must REFUSE, and the disagreement block at the
         end. The artefact's sections 5 and 6 state 39 at-risk lines carrying 78 ruled
         sites, 39 with more than one receiver name and 7 carrying `(expr)`, the shape
         table as 68 Name, 4 Subscript, 3 Call and 2 Attribute, `68 of 77`, NINE refusal
         lines every one of which is under `tests/`, and exactly one disagreement, at
         `packages/orchestration/long_run_executor.py:504`, reading 2 ruled sites against
         1 ast node with site cols `[19, 40]` and node value cols `[30]`.
     (e) DETERMINISM. Run the SAME extracted file twice more and report whether all three
         outputs are byte-identical. The instrument walks a `set`, so an unsorted listing
         would come out in a different order in every process; the artefact's section 5
         states that it sorts and routes the proof here rather than asserting it. A
         difference between two runs is a finding, and the lines to look at first are the
         nine refusal lines and the receiver-shape table.
     A figure the instrument prints that DISAGREES with the artefact is reported as it
     read and is a finding; do not reconcile it in either direction. A figure the artefact
     states that the instrument does NOT print is likewise reported as absent rather than
     supplied from elsewhere. The artefact's PROVENANCE paragraph claims there is NO
     reviewer-only reading in it, so unlike the round before this one there is no excused
     list: an absent figure is a finding against that claim. The base SHA `30072048` is an
     identifier rather than a measurement and is not owed here.

  G6 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `30072048` and at C5, and whether all five are EQUAL. `packages` is
         the one constraint 12 makes load-bearing: the instrument installs a property over
         a class in `packages/core/models.py` in its own process, and an EQUAL tree object
         is what proves it did not write that module.
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
         reading AFTER G5 has run, because constraint 12 names what the instrument does in
         its own process and this is the reading that proves it left the tree alone.
     (b) The changed-path set over `30072048`..C5 must be exactly the Change section's
         paths other than `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `docs/`, `scripts/`, `packages/`,
         `apps/` or `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `30072048` and at C5. Report both, the ids registered,
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
             round 64, the one-sentence context self-assessment amend0905-throughput
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

BEGIN-PLAN64 sha256=33eff07a813d291164c9726ee9a4e3194471e6dea33ac03443e4f2e05d8157a6
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

ROUND 64 MEASURES THE ROUTE that DECISION F275 D36's blocker needs, and DECISION F275 D38
rules it. D36 part three orders the probe key to gain `col_offset`; this interpreter is
CPython 3.10.12 and has no column on a frame at all, so that remedy is unimplementable as
written. `f_lasti` discriminates instead, measured on the real pydantic model through the
probe's own outward walk, and resolves back to a named receiver by disassembly for 68 of
the 77 attribute nodes on the 39 at-risk lines. The nine it cannot are enumerated and all
are in tests. The artefact is `.agent/f275_t003_flip_residue_r64.md`. The round 63 verdict
and its prose slip are booked here. No production line moves.

## Next Steps

1. SPEND the route: modify the committed descriptor probe to record `f_lasti`, run the
   suite under it twice, rebuild the ruled site set with a receiver-discriminating key, and
   REFUSE the nine sites section 5 of the round 64 artefact names. That discharges DECISION
   F275 D36's binding clause and both halves of `R-0880`'s fix clause at once.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
3. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, registering
   the `acceptance_checks` finding DECISION F275 D22 places with it.
4. The classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- 1186 failures is not a landable state, and the largest classes need PRODUCTION-CODE work
  rather than another transform rule — a bigger step than the rounds before it.
- The 42 errors have not moved across three runs and are still undiagnosed, and the ruled
  set holds two sites over one attribute node at `long_run_executor.py:504`, unattributed.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN64

BEGIN-RECORD64 sha256=b1d5a923496221f3bca45713736b7405098159fe75c8c3afbba8f8c1c7dd307f
Gate: F275 R63 — the F275 round 63 entry. VERDICT PASS. Written by the planner and reviewer of session 24 after reading the committed range `93063ec4`..`30072048` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 64, per operator amendment amend0827-process-diet rule 1. The round diagnosed the three largest residue classes and the decision recorded at `1252140d` ruled them ONE id-SHAPE seam that is neither a fourth transform rule family nor a data migration.

G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: all three authored blobs are byte-identical to the reviewer's own scratch originals — the block at 32200 bytes, the artefact at 10145 and the route instrument at 9733 — and `.agent/last_block.md` equals the block blob. All four slices matched the sha256 on their own BEGIN markers, re-derived by the reviewer from the committed blob. Re-measured there the block is 318 lines TOTAL and 242 PROSE, agreeing with its own constraint 8. G2: `.agent/plan.md` is byte-identical to its slice at 2669 bytes over 45 lines, both mandated headings exactly once.

G3 CARRIED THREE APPENDS RATHER THAN TWO AND ALL THREE HOLD. `.agent/live_review.md` goes 996190 to 1000844, `.agent/prose_slips.md` 253122 to 255085 and `.agent/decisions.md` 1130791 to 1136331, every one exact under reader A, with reader B holding at N counted from the slice as 6, 2 and 9. The reviewer ran its own negative control on each: one ASCII letter flipped inside the FIRST appended paragraph is REJECTED by both readers while the unmutated region is ACCEPTED by both, on all three files. The D37 heading reads 0 at the base and the highest existing is D36; the two slip paragraphs carry a prefix the base holds none of. G4: the artefact at C5 is byte-identical to the C0b blob at 10145 bytes and the path does not resolve at the base.

G6 and G7: all five top-level trees are byte-identical at the base and at C5, the canary reads 42 passed at exit 0, and `ruff check .` reads 26 rows at the frozen ceiling with zero under `.remedy-wt/` and zero `.py` rows under `.agent/`. Nine changed paths with MISSING and EXTRA empty and zero production paths; the open set is 88 at both ends with registered, resolved and de-registered ALL EMPTY. Per-commit insertions peak at 318 over C0a to C5. THE HANDBACK COMMIT IS 515 INSERTIONS AND 594 DELETIONS, which is over the DECISION F104 D1 cap of 500 and is NOT a violation: that decision exempts entirely a commit whose diff is the verbatim rewrite of a SINGLE `.agent/**` state file, and `git show --numstat` on that commit lists `.agent/handoff.md` and nothing else. F275's one declared-oversize allowance is therefore STILL UNSPENT at 63 rounds.

THE SUBSTANCE, RE-DERIVED RATHER THAN ACCEPTED. The reviewer extracted the instrument from the committed blob and ran it: one fence found, and all four banners reproduce. The three classes are 337, 223 and 90 E-lines, with 193 at `data_paths.py:324`, 87 at the stdlib UUID constructor and all 90 at `data_paths.py:200`. All three reproduce by CALLING the shipped functions against a root that does not exist, each beside a control that succeeds, so no record on disk participates and the data-migration reading is answered NO by a probe. The resolver, run against a synthetic store holding both shapes, refuses a unified record by its WHOLE id while the sibling matcher finds it on the same row. And the candidate fourth rule — the narrowest rewrite that could close the seam — was applied and run: against a control at a REAL exit 0 and 1345 passed, it moved 263 failures to 249, fixing 16 and BREAKING 2, and both it broke assert the guard the unwrap deletes.

THE WORKER DECLARED NINE DEVIATIONS AND THE SIXTH IS THE ONE THAT MATTERS, BECAUSE IT IS THE REVIEWER'S AND IT IS THE SAME CLASS AS ROUND 62'S. The block's G5(d) ordered the control reported "at exit 0", and the committed instrument prints no exit code for any of its three runs — its fourth banner reads each log's pass-or-fail line and nothing else. The artefact's section 6 table carries a REAL-exit column whose three values are true readings the reviewer took while running those suites, but the artefact's own PROVENANCE paragraph declares only TWO readings as reviewer-only and this is a third. The worker reported the field as ABSENT rather than supplying it from elsewhere, which is exactly what the gate's own closing sentence orders, and it named that this is not one of the two the provenance paragraph excuses. Nothing on disk is wrong and no id is spent; it is one dated line in `.agent/prose_slips.md`, booked by this same round.

THE COUNTER-MEASURE ROUND 62 PRODUCED WAS RUN THIS ROUND AND WAS STILL NOT ENOUGH, WHICH IS WORTH THE RECORD MORE THAN THE SLIP IS. Before emitting, the reviewer greped the instrument's real output for every token G5 names and counted zero absent — the check that round 62's slip asked for, run as a script. It passed because it was built from the gate's TOKEN LIST, and the exit column lives in the ARTEFACT rather than in the gate's quoted tokens, so the sweep never looked at it. A token sweep proves a gate's words are answerable; it does not prove an artefact's every column is. The narrower rule that follows is in the slip line, and the remaining eight deviations are the standing ones plus the note that the instrument's resolver banner emits two unbuffered stderr lines that land at the top of a redirected capture.
END-RECORD64

BEGIN-SLIPS64 sha256=75ab9ddc86852945917c00096ed248589294e5460775c841762022853e363c05
2026-09-11 · F275 R63 · The round 63 artefact's section 6 table carried a `REAL exit` column reading 0, 1 and 1 for its three scoped runs, and the committed instrument prints no exit code for any of them — its fourth banner reads each log's `\d+ (passed|failed)` line and nothing else. The three values are true readings the reviewer took while running those suites, so nothing on disk is wrong; what is wrong is that the artefact's own PROVENANCE paragraph declared exactly TWO readings as reviewer-only and this was a third. The round 62 counter-measure WAS run before emission — every token the gate names was greped in the instrument's real output, zero absent — and it did not catch this, because it was built from the GATE's token list while the undeclared column lives in the ARTEFACT. THE RULE THAT FOLLOWS: when an artefact declares which of its readings an instrument re-derives, the pre-emission check sweeps the ARTEFACT's own numerals against that instrument's output and the declared exception list, not only the gate's quoted tokens — a provenance paragraph is a claim about the whole document and is measured over the whole document.
END-SLIPS64

BEGIN-DEC64 sha256=78514ed884ef326722278eec23c910b5b88165b2856be18361bff63604ff0080
## DECISION F275 D38 (2026-09-11, F275 round 64) — DECISION F275 D36's part-three remedy is unavailable on this interpreter, and `f_lasti` is the route that replaces it

CONTEXT. DECISION F275 D36 bounded finding `R-0880` at 39 ruled sites and ruled the cause to be a probe key one discriminator short. Its part three names the remedy — "The probe's recorded key gains `col_offset`" — and its binding clause forbids any round to consume the ruled site set for a WRITE until either the 39 are resolved pair by pair or the set is re-derived with a column in its key. This decision corrects the REMEDY and leaves the binding clause standing, in the form the correction gives it. The measurement is in `.agent/f275_t003_flip_residue_r64.md` and the instrument that produced it is committed at `.agent/authored/f275-r64-route.py.md`. D36 itself is NOT edited: the record is append-only and a dated correction is how it stays honest.

CHOSEN, PART ONE: THE REMEDY AS WRITTEN CANNOT BE IMPLEMENTED, AND THAT IS A PROPERTY OF THE INTERPRETER RATHER THAN OF THE PROBE. This machine runs CPython 3.10.12. Column information for a byte-code instruction arrived in 3.11 with PEP 657, as `code.co_positions()`, and `hasattr` on a code object here reads False. A frame carries `f_lineno` and `f_lasti` and no third positional attribute. The F275 R53 descriptor probe takes its line from `frame.f_lineno`; there is no `frame.f_col_offset` beside it to take, and D36 part three read a fix off the STATIC site set — which does carry a column, because `ast` supplies one — and assumed the dynamic side could carry the same value. It cannot.

CHOSEN, PART TWO: `f_lasti` IS THE DISCRIMINATOR, MEASURED ON THE REAL MODEL AND THROUGH THE REAL WALK. A descriptor of the probe's own shape installed over `packages.core.models.Job.id`, with the probe's own outward frame walk, records two reads of one attribute on ONE line with two different receivers as ONE key by `(path, line, function)` and as TWO keys once `f_lasti` joins them. The offsets then resolve back to their NAMED receivers by disassembling the caller's code object and taking the last name-load at or before the offset, and the two receivers came back in source order. The reading is taken through pydantic's dispatch rather than against a toy class, because that dispatch is what made the earlier probe's frame attribution hard in the first place.

CHOSEN, PART THREE: THE BINDING CLAUSE OF D36 IS RE-STATED WITH THE ROUTE IT CAN ACTUALLY NAME. No round may consume the ruled site set for a WRITE to the tree until either the 39 at-risk sites are resolved pair by pair, or the set is re-derived with a key that DISCRIMINATES the receiver — which on this interpreter means `f_lasti` plus the disassembly above, and on 3.11 or later would mean `co_positions`. Reading the set, measuring against it and running dry runs on it stay permitted, exactly as D36 says; the flip commit itself does not. Nothing about the PROHIBITION changes: only the second escape route is now described in terms that exist here.

CHOSEN, PART FOUR: THE ROUTE'S COVERAGE IS STATED AS A NUMBER WITH ITS REFUSALS ENUMERATED, NOT AS A CLAIM OF COMPLETENESS. All 39 at-risk lines carry receiver names that differ, which is the definition of the class rather than a fortunate property, so a receiver-carrying key separates every one of them. Of the attribute nodes on those lines, 68 have a bare `Name` receiver, which one load instruction resolves; the other nine have a `Subscript`, a `Call` or an `Attribute` receiver, which it does not. The artefact names all nine, every one of them is in a test file, and the four production lines D36 named by hand are all in the 68. Those nine are to be REFUSED by the re-derivation rather than guessed at, which is the same obligation `R-0880`'s fix clause already carries as its second half.

ALTERNATIVES CONSIDERED. (i) Upgrade the interpreter to 3.11 to obtain `co_positions` — rejected outright: a runtime change to make one measurement easier is the largest possible blast radius for the smallest possible gain, and it would invalidate every timing and suite reading this feature has taken. (ii) Resolve the 39 pair by pair by hand, which D36's first escape route already permits — not rejected, and still available; it is rejected only as the DEFAULT, because it decides 39 lines by reading and leaves the key wrong for every future round, which is how `R-0879` happened. (iii) Key the probe on the receiver's NAME captured from the descriptor's own `self` — rejected: the descriptor sees the OBJECT, not the expression that reached it, so two locals bound to the same record are indistinguishable and two different records read through one name are wrongly split. (iv) Abandon the re-derivation and strike all 78 sites — rejected for the reason D36 already gave: that turns an over-selection into an under-selection, which is `R-0879` from the other side.

WHAT THIS DECISION DOES NOT RULE. It does not perform the re-derivation; that means modifying the committed probe, running the suite under it twice and rebuilding the site set, and it is the next round. It does not decide the nine refusals. It does not diagnose the one line where the ruled set holds two sites over a single attribute node, `packages/orchestration/long_run_executor.py:504`, which the artefact reports and attributes to nothing. It does not resolve or register any finding id, and `R-0880` stays open with both obligations where D36 left them.

HOW TO REVERSE: delete this decision. D36 part three then stands alone, ordering a `col_offset` this interpreter cannot supply, and the next session re-measures that in the time it takes to run one `hasattr`.
END-DEC64
