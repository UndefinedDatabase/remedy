── STEP T003 / round 62 — F275 ────────────────────────────────
Goal:        Land the dry run that builds DECISION F275 D32's THIRD retype rule family
             against the nine sites DECISION F275 D35 names, and the scope-keyed site
             generator it consumes. The rule closes the class it was built for exactly.
             The artefact and the generator are reviewer texts transported as whole files.
             The round 61 verdict is booked. NO LINE UNDER `packages/`, `apps/`, `tests/`,
             `docs/` OR `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r62.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r62-artefact.md`
             C0c  save the bound instrument verbatim as
                  `.agent/authored/f275-r62-bound.py.md`
             C0d  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN62, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD62 appended
             C3   `.agent/decisions.md` <- slice DEC62 appended
             C4   `.agent/f275_t003_flip_residue_r62.md` <- a copy of the C0b blob
             C5   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r62.md                NEW
               .agent/authored/f275-r62-artefact.md       NEW
               .agent/authored/f275-r62-bound.py.md       NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/decisions.md
               .agent/f275_t003_flip_residue_r62.md       NEW
               .agent/handoff.md
             The four paths marked NEW do not exist at the base: `git ls-tree 7910aa7d --`
             over all four prints nothing at exit 0, so each is an ADDITION and not a
             rewrite. `.agent/prose_slips.md` is NOT in this set: the reviewer spent no
             slip on round 61, which makes three rounds in a row, and RECORD62 states that
             and names the counter-measure in its own text.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r62.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. A slice's BODY is the bytes from the start of the line after
     its BEGIN marker to the first byte of its END marker line, INCLUDING the terminal
     newline of the body's last line. Each BEGIN marker carries its slice's own sha256;
     check it. The artefact and the generator are WHOLE FILES: copy each with
     `shutil.copyfile` and never open either in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 61 across
     C0a, C0b, C0c and C0d and becomes current at C1, which is the first SUBSTANTIVE
     commit and is what item 23 of §3 of `docs/agents/planner_reviewer_prompt.md` requires
     of a round that touches the finding ledger.
  4. This round creates NO `git worktree` and runs nothing destructive. The reviewer's own
     two worktrees were created, used and removed BEFORE this block was written, and
     `git worktree list` shows the primary checkout alone at the base.
  5. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  6. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  7. Re-read `.agent/STOP` FROM DISK before the first commit and again before C5, and
     report both readings literally. It does not exist at the reviewer's base reading.
  8. This block is 289 lines TOTAL and 212 PROSE, measured on its final bytes.
  9. NO finding id is registered this round and NONE is resolved. `R-0880` is BOUNDED
     here, not resolved: its second obligation is unbuilt and DEC62 says so. The open set
     is 88 by distinct id at the base and must read 88 at C4, with the registered set, the
     resolved set and the de-registered set ALL EMPTY. The COUNT alone is not the gate;
     the membership is.
 10. `.agent/authored/f275-r62-bound.py.md` is a `.md` and its extension is load-bearing:
     a `.py` file anywhere `ruff check .` scans is counted by
     `tests/orchestration/test_ci_budgets.py`, whose ceiling G6(c) reads. Do not rename it,
     and do not land a runnable copy of it anywhere in the tree.
 11. A pipe into `tail` MASKS the real exit code. Round 60's worker hit this on the canary
     and had to re-run it. Redirect to a file and read the file instead, for every gate
     whose exit code you report.

Done when:   the seven gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C5.

  G1 TRANSPORT. For each of the three authored blobs, compare the COMMITTED blob against
     the reviewer's scratch original by size and sha256:
       .agent/authored/f275-r62.md           @C0a  vs  .remedy-wt/f275-r62.block.md
       .agent/authored/f275-r62-artefact.md  @C0b  vs  .remedy-wt/f275-r62-artefact.md
       .agent/authored/f275-r62-bound.py.md  @C0c  vs  .remedy-wt/f275-r62-bound.py.md
     Then `.agent/last_block.md` @C0d against the C0a blob. Report all four EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of every slice's
     BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report both
     numerals beside constraint 8's and say whether they agree. The block states no count
     of its own slices: the extraction is the sweep and its cardinality is your output.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN62: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. Two appends in two commits, each proved by TWO readers and a negative
     control: C2 appends RECORD62 to `.agent/live_review.md` and C3 appends DEC62 to
     `.agent/decisions.md`.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline and the slice's body.
            .agent/live_review.md   pre  990200 at the base, slice RECORD62
            .agent/decisions.md     pre 1124939 at C2,       slice DEC62
          Report each pre size, each post size and each delta. The slice body sizes are
          NOT stated here: each is the length of what you extracted.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N for each.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter — a byte b with
          `b < 128 and chr(b).isalpha()` — inside the FIRST appended paragraph, and report
          that BOTH readers reject it. Report ALSO that both readers ACCEPT the unmutated
          region, because a reader that rejects everything proves nothing by rejecting.
     (iv) RECORD62 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0. Report the count of `^- R-` and of `^Done: R-` lines that C2
          ADDS, both of which must be 0.
     (v)  Report RECORD62's first line beside the count of lines in `.agent/live_review.md`
          at `7910aa7d` already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.`,
          and whether the new first line matches that pattern and duplicates none of them.
          Report the number your script counted; this block states none.
     (vi) DEC62 must begin `## DECISION F275 D36 ` and `.agent/decisions.md` at the base
          must contain NO line matching `^## DECISION F275 D36`. Report both readings, and
          report the highest existing `^## DECISION F275 D\d+` heading at the base.

  G4 THE ARTEFACT AND THE GENERATOR ARE THE AUTHORED BLOBS AND NOTHING ELSE.
     `.agent/f275_t003_flip_residue_r62.md` at C4 must be byte-identical to the
     `.agent/authored/f275-r62-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show 7910aa7d:.agent/f275_t003_flip_residue_r62.md`, which must be non-zero.
     Report the artefact's line count and the generator blob's line count, each against
     the DECISION F104 D1 cap of 500 insertions.

  G5 THE ARTEFACT'S NUMBERS ARE RE-DERIVED FROM THE COMMITTED INSTRUMENT.
     The instrument is committed at `.agent/authored/f275-r62-bound.py.md` at C0c, inside a
     ```python fence. Extract that fenced source into `.remedy-wt/` and RUN it with
     `python3 -B`. It reads only `.remedy-wt/r53_R.json` and `.remedy-wt/r55_owners.json`,
     both of which are already on disk, and it creates nothing and writes nothing.
     (a) Report its six headline figures literally: the ruled-site count, the distinct
         `(path, line)` count, the number of lines carrying more than one ruled site, the
         number of ruled sites on such a line, the number of AT-RISK lines, and the number
         of ruled sites on those. The artefact states 2198, 2080, 104, 222, 39 and 78.
         Report what the instrument printed and say whether each agrees.
     (b) Report the two rows the instrument prints for
         `packages/orchestration/loop_run.py:285` — their columns, receivers, owner
         verdicts and `static` values. The artefact's section 2 rests on those two rows
         being one line, two receivers, ONE owner verdict and `static=None` on both.
     (c) Report the instrument's cross-check block: for each of `loop_run.py:285`,
         `long_run_executor.py:504`, `brain_detail.py:345` and `mission_state.py:1074`,
         whether it is in the static bound. The artefact states all four are, and a FALSE
         on any of them is a real finding rather than a formality — it would mean the
         bound does not contain the instances already observed.
     A figure the instrument prints that DISAGREES with the artefact is reported as it
     read and is a finding; do not reconcile it in either direction.

  G6 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `7910aa7d` and at C4, and whether all five are EQUAL.
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
     (b) The changed-path set over `7910aa7d`..C4 must be exactly the Change section's
         paths other than `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `docs/`, `scripts/`, `packages/`,
         `apps/` or `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `7910aa7d` and at C4. Report both, the ids registered,
         the ids resolved and the ids de-registered, all three of which must be empty.
         Report the highest id in the record at each end.
     (d) Per-commit insertions from `git show --numstat <sha>` for C0a through C4, each
         against the AGENTS.md DECISION F104 D1 cap of 500, and the maximum over them.
         C5's own numbers are NOT ordered here: they cannot exist while C5 is being
         written, and the reviewer records them at the next gate.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 23 of F275 and
             round 61, the one-sentence context self-assessment amend0905-throughput
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

BEGIN-PLAN62 sha256=dfff2924be5ec7e43291bcb32a35fd0bc357e22a7207ac3cc667cf23dd4337cb
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

ROUND 62 bounds finding `R-0880` STATICALLY, which is the first of the two obligations its
own fix clause binds, and DECISION F275 D36 rules the result. The class is 39 ruled sites
and the bound is exact: the descriptor probe records a LINE and no COLUMN, so on 39 lines
one proof ruled two receivers. All four frames the previous run reached are inside the
bound. The artefact is `.agent/f275_t003_flip_residue_r62.md`. The round 61 verdict is
booked here. No worktree was created and no suite was run.

## Next Steps

1. Diagnose the three largest residue classes, which are reads of an id whose SHAPE
   changed rather than renames: `SystemExit` at `data_paths.py:324`, `unsupported operand`
   at `data_paths.py:200` and the hexadecimal-UUID parse. Rule whether they are a fourth
   rule family or a consequence of records written to disk under the classic shape.
2. Build `R-0880`'s second obligation, the transform's refusal to rename a site whose
   owner verdict cannot be confirmed, and resolve the 39 pairs or re-derive the site set
   with a column in its key. DECISION F275 D36 forbids the flip commit until one of those
   two lands.
3. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, registering
   the `acceptance_checks` finding DECISION F275 D22 places with it.
4. The resolver collapse DECISION F260 D5 places in T003, with the classic store, then the
   closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- 1186 failures is not a landable state, and no rule family of D32's kind is left to build.
- The 42 errors have not moved across three runs and are still undiagnosed.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN62

BEGIN-RECORD62 sha256=00485631154749f0f16817e626d088fa957390a4f99388fae925667ba14ea1dd
Gate: F275 R61 — the F275 round 61 entry. VERDICT PASS. Written by the planner and reviewer of session 23 after reading the committed range `5dfeeae6`..`7910aa7d` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 62, per operator amendment amend0827-process-diet rule 1. The round built DECISION F275 D32's THIRD retype rule family against the nine sites DECISION F275 D35 names, and the class that family was built for went to ZERO.

G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: all three authored blobs are byte-identical to the reviewer's own scratch originals — the block at 23106 bytes and sha256 `969758a16521e5f72775d0f70f6ae80ce0b0ae6745e259dc7568afed88930391`, the artefact at 8109 and the site generator at 4675 — and `.agent/last_block.md` equals the block blob. Both slices matched the sha256 on their own BEGIN markers, re-derived by the reviewer from the committed C0a blob. Re-measured there the block is 258 lines TOTAL and 200 PROSE, agreeing with its own constraint 8. G2: `.agent/plan.md` is byte-identical to PLAN61 at 2444 bytes over 43 lines, both mandated headings exactly once.

G3: `.agent/live_review.md` goes 983710 to 990200, a delta of 6490 which is the slice body plus one newline, exact under reader A, with reader B holding at N counted from the slice as 8. The reviewer ran its own negative control: one ASCII letter flipped in the FIRST appended paragraph is REJECTED by both readers while the UNMUTATED region is ACCEPTED by both. C2 adds no line beginning `- R-` and none beginning `Done: R-`. G4: the artefact at C3 is byte-identical to the C0b blob at 8109 bytes, the path does not resolve at the base, and the artefact and the generator are 141 and 100 lines against the 500 cap.

G5 IS THE GATE THAT CARRIED THIS ROUND AND THE REVIEWER RE-TOOK ALL THREE READINGS. All nine sites resolve and every one still contains `.status.value`, 9 of 9 with no miss, so no `R-0879` recurrence arrived in a new artefact. Line 380 of `packages/orchestration/brain_detail.py` reads 2 `.status` attribute nodes and 1 `.status.value` chain, counted with `ast` — which is the measured form of why the generator REFUSED on its first keying and why the unit had to become the chain. And `packages`, `apps` and `tests` are the same tree objects at `bf692757` and at `5dfeeae6`, which is what licenses the artefact's reuse of round 59's control run rather than spending twenty-one minutes to reproduce a reading the tree identity already fixes. That reuse is gated rather than asserted, and the gate is the reason it is legitimate.

G6: all five of `packages`, `apps`, `tests`, `docs` and `scripts` are byte-identical trees at the base and at C3, the canary reads 42 passed at exit 0, and `ruff check .` reads 26 finding rows at the frozen ceiling with ZERO under `.remedy-wt/` and ZERO `.py` rows under `.agent/`. G7: seven changed paths with MISSING and EXTRA both empty and ZERO production paths; the open set reads 88 at both ends with the registered, resolved and de-registered sets ALL EMPTY; per-commit insertions are 258, 141, 100, 145, 12, 14 and 141, every one under the cap, so F275's one declared-oversize allowance is STILL UNSPENT at 61 rounds. The handback commit's own numbers, which no gate of that round could reach, are 371 insertions and 366 deletions.

THE SUBSTANCE OF THE ROUND, RE-DERIVED RATHER THAN ACCEPTED: rule T8 fired exactly nine times and no other rule count moved, the one newly touched file being `trust_report.py`; total failures fell from 1240 to 1186; and the class the rule was built for — a `.value` read on a `str` — went from 61 located exception frames to ZERO. The three largest residue classes did not move by a single line, which is what a rule family built against a named site set should look like, and it is the reason this round's reading is a difference of one variable rather than a new measurement.

THE WORKER DECLARED FIVE DEVIATIONS AND THEN VOLUNTEERED A SIXTH AGAINST ITSELF, WHICH IS THE ONE WORTH RECORDING. Its handback's External actions section says of the push "see the push transcript below" and no transcript follows, because the push necessarily happens after the commit that writes the file; the wording was inherited from round 60's handback, which carries the same forward reference. The worker reported this rather than trimming a committed file, and it is right that it did: a handback is not edited after the fact. It damages nothing — the real range `5dfeeae6..7910aa7d` is on the record and no gate depends on it — and under operator amendment amend0827-process-diet rule 2 it is a declared deviation and not an id. The remaining five are the standing ones plus one of substance: C3 was copied with `shutil.copyfile` from the working-tree path after that path was asserted byte-equal to the committed C0b blob, which reconciles the Bundle's "a copy of the C0b blob" with constraint 2's copyfile order, and G4 re-checked the landed result independently and read byte-identical.

THE REVIEWER SPENT NO PROSE SLIP THIS ROUND, WHICH MAKES THREE IN A ROW, AND THE COUNTER-MEASURE THAT PRODUCED THEM IS NAMED SO IT CAN BE KEPT. Every numeral the block asserted about its base was measured at that base BEFORE the block was emitted — the live_review size, the Gate-pattern count, the open set, the nine site lines, the two-versus-one node count on line 380, the three tree object ids, the ruff ceiling and the canary — and each came back equal to what the block went on to state. Session 22's close named the reviewer's own error rate as the one thing that had got worse; three rounds is not a trend and is not claimed as one, but the practice behind them is item 12 of `docs/agents/planner_reviewer_prompt.md` §3 and finding `R-0364`, run as a single script over every base reading rather than as a habit of care.
END-RECORD62

BEGIN-DEC62 sha256=f7e9e6dfc50870f20a873204c883ed138ddb5bb319c4491468cc59561fdcbacd
## DECISION F275 D36 (2026-09-11, F275 round 62) — finding `R-0880` is 39 ruled sites, and its cause is that the descriptor probe records a LINE and not a COLUMN

CONTEXT. `R-0880` records that the ruled site set the flip consumes OVER-selects: it rules reads whose receiver is not a job or a task record, and the flip would rename them inside the one commit AGENTS.md's declared-oversize allowance lets this feature land exactly once. It was raised from a RUN, so it named the 12 located frames the suite reached and called that a floor. Its fix clause binds two obligations; this decision discharges the FIRST and rules the shape of the second. The measurement is in `.agent/f275_t003_flip_residue_r62.md` and the instrument that produced it is committed at `.agent/authored/f275-r62-bound.py.md`.

THE CAUSE IS NOT A BAD HEURISTIC; IT IS A KEY THAT IS ONE COLUMN TOO SHORT. The DECISION F272 D7 descriptor probe records `(owner, field, mode, path, LINE, function)` and NO column. Round 53 built the ruled site set by matching each probe row against the attribute nodes of that line. Where a line holds two attribute nodes of the same name on DIFFERENT receivers, one proof ruled BOTH. The instance the finding was raised from is exactly that, and the site set's own data shows it: `packages/orchestration/loop_run.py:285` carries `mission.id` at column 40 and `job.id` at column 56, both ruled `Job`, both carrying `static=None` — so neither came from the static sweep and the probe had proved only one of them. The probe was right about what it saw. The inference drawn from it, that every same-named attribute on the line was the same record, is what was wrong, and it is invisible on the 2080 lines that hold only one such node.

CHOSEN, PART ONE: THE CLASS IS BOUNDED AT 39 SITES, AND THE BOUND IS EXACT RATHER THAN APPROXIMATE. Of 2198 ruled sites on 2080 distinct lines, 104 lines carry more than one ruled site and 222 sites sit on them. A shared line is not by itself a defect — `job.id` and `task.id` on one line are two receivers with two DIFFERENT owner verdicts and two separate proofs — so the at-risk class is the line where two different receiver names carry the SAME owner verdict. There are 39 such lines, carrying 78 ruled sites, and every one of the 39 carries exactly TWO. Exactly one site per line is the proved one and exactly one was ruled for free, so the lower and the upper bound coincide at 39. Four of the 39 lines are in production modules and the rest are in tests.

CHOSEN, PART TWO: THE BOUND IS ACCEPTED BECAUSE IT AGREES WITH THE RUN FROM THE OTHER DIRECTION. Round 61's dry run reached the over-selection at four source frames — `loop_run.py:285`, `long_run_executor.py:504`, `brain_detail.py:345` and `mission_state.py:1074` — and ALL FOUR are inside the static bound. A bound that did not contain the instances already observed would be a different measurement of a different thing; this one contains them, and `brain_detail.py:345` additionally explains a residue class the run could not attribute, its `str(t.id) == node.id` pairing a genuine `Task.id` with a `BrainNode` under one proof.

CHOSEN, PART THREE: THE REMEDY IS THE COLUMN, AND IT IS NOT PERFORMED HERE. The probe's recorded key gains `col_offset`, which makes the match exact and costs a one-line change to a committed instrument plus the two twenty-one-minute runs a re-derivation needs. This decision does NOT order that re-derivation into any particular round, because the flip's remaining blockers are the three id-SHAPE classes and not this one, and a re-derivation taken before those are understood would be paid for twice. What this decision DOES order is that no round may consume the ruled site set for a WRITE to the tree until either the 39 are resolved pair by pair or the set is re-derived with a column in its key. Reading the set, measuring against it and running dry runs on it stay permitted; the flip commit itself does not.

ALTERNATIVES CONSIDERED. (i) Strike all 78 sites on the at-risk lines — rejected: 39 of them are proved and striking them would turn an over-selection into an under-selection, which is finding `R-0879` arriving from the other side and is the worse failure, because a missed rename fails loudly at run time while a wrong one may not fail at all. (ii) Decide each of the 39 pairs by receiver name — rejected by name: that is the heuristic DECISION F275 D29's P1 exists to have killed, and `record`, `entry`, `node` and `art` are exactly the names it decides nothing about. (iii) Re-derive the set now, with the column — not rejected, and explicitly still open; it is the stronger answer and this decision orders only that it happen before the set is used for a write, not that it happen next. (iv) Treat the 12 frames the run reached as the whole class and fix those — rejected on this round's own arithmetic: the class is 39 and a run can only ever show what it executes, which is the reason `R-0880` asked for a static bound in the first place.

WHAT THIS DECISION DOES NOT RULE. It does not say WHICH site of each pair is the unproved one: the probe row that proved the line carries no column to match against, so deciding a pair needs either the re-derivation above or a per-pair reading of the kind round 60 used on the `.status` family. It does not certify the rest of the site set; the other 2159 sites are outside this class, not shown sound by it. And it does not resolve `R-0880`, whose second obligation — the transform's refusal to rename a site whose owner verdict cannot be confirmed — is unbuilt.

HOW TO REVERSE: delete this decision. `R-0880` then stands with its 12 observed frames and no bound, the 39 are unknown again, and the next session re-derives them from the committed site set in about the time this round took, which was one reading and no suite run.
END-DEC62
