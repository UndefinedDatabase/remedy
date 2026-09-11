── STEP T003 / round 63 — F275 ────────────────────────────────
Goal:        Land the DIAGNOSIS of the three largest residue classes and the decision that
             rules them. They are ONE id-SHAPE seam — not a fourth rule family and not a
             data migration — and the candidate fourth rule was built, applied and RUN
             before this block was written. The artefact and the instrument are reviewer
             texts transported as whole files. The round 62 verdict and its two prose
             slips are booked. NO LINE UNDER `packages/`, `apps/`, `tests/`, `docs/` OR
             `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r63.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r63-artefact.md`
             C0c  save the diagnosis instrument verbatim as
                  `.agent/authored/f275-r63-diag.py.md`
             C0d  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN63, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD63 appended
             C3   `.agent/prose_slips.md` <- slice SLIPS63 appended
             C4   `.agent/decisions.md` <- slice DEC63 appended
             C5   `.agent/f275_t003_flip_residue_r63.md` <- a copy of the C0b blob
             C6   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r63.md                NEW
               .agent/authored/f275-r63-artefact.md       NEW
               .agent/authored/f275-r63-diag.py.md        NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               .agent/decisions.md
               .agent/f275_t003_flip_residue_r63.md       NEW
               .agent/handoff.md
             The four paths marked NEW do not exist at the base: `git ls-tree 93063ec4 --`
             over all four prints nothing at exit 0. `.agent/prose_slips.md` IS in this set
             this round, unlike the last three, because the round 62 verdict spent two
             slips and SLIPS63 is their booking.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r63.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. A slice's BODY is the bytes from the start of the line after
     its BEGIN marker to the first byte of its END marker line, INCLUDING the terminal
     newline of the body's last line. Each BEGIN marker carries its slice's own sha256;
     check it. The artefact and the instrument are WHOLE FILES: copy each with
     `shutil.copyfile` and never open either in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 62 across
     C0a, C0b, C0c and C0d and becomes current at C1, which is the first SUBSTANTIVE
     commit and is what item 23 of §3 of `docs/agents/planner_reviewer_prompt.md` requires
     of a round that touches the finding ledger.
  4. This round creates NO `git worktree` and runs nothing destructive. The reviewer's own
     two worktrees were created, used and removed BEFORE this block was written, and
     `git worktree list` shows the primary checkout alone at the base.
  5. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  6. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  7. Re-read `.agent/STOP` FROM DISK before the first commit and again before C6, and
     report both readings literally. It does not exist at the reviewer's base reading.
  8. This block is 318 lines TOTAL and 242 PROSE, measured on its final bytes.
  9. NO finding id is registered this round and NONE is resolved. The open set is 88 by
     distinct id at the base and must read 88 at C5, with the registered set, the resolved
     set and the de-registered set ALL EMPTY. The COUNT alone is not the gate; the
     membership is. The two prose slips SLIPS63 books are NOT ids, per operator amendment
     amend0827-process-diet rule 2.
 10. `.agent/authored/f275-r63-diag.py.md` is a `.md` and its extension is load-bearing:
     a `.py` file anywhere `ruff check .` scans is counted by
     `tests/orchestration/test_ci_budgets.py`, whose ceiling G6(c) reads. Do not rename it,
     and do not land a runnable copy of it anywhere in the tree.
 11. A pipe into `tail` MASKS the real exit code. Redirect to a file and read the file
     instead, for every gate whose exit code you report.
 12. The instrument G5 runs CREATES a synthetic store under `.remedy-wt/r63_store` and
     REMOVES it again, and it sets `REMEDY_DATA_DIR` inside its own process only. That is
     the one thing in this round that writes anything, it writes only under the gitignored
     scratch directory, and G7(a)'s `git status --porcelain` reading is what proves it left
     the tree alone.

Done when:   the seven gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C6.

  G1 TRANSPORT. For each of the three authored blobs, compare the COMMITTED blob against
     the reviewer's scratch original by size and sha256:
       .agent/authored/f275-r63.md           @C0a  vs  .remedy-wt/f275-r63.block.md
       .agent/authored/f275-r63-artefact.md  @C0b  vs  .remedy-wt/f275-r63-artefact.md
       .agent/authored/f275-r63-diag.py.md   @C0c  vs  .remedy-wt/f275-r63-diag.py.md
     Then `.agent/last_block.md` @C0d against the C0a blob. Report all four EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of every slice's
     BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report both
     numerals beside constraint 8's and say whether they agree. The block states no count
     of its own slices: the extraction is the sweep and its cardinality is your output.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN63: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. THREE appends in three commits, each proved by TWO readers and a negative
     control: C2 appends RECORD63 to `.agent/live_review.md`, C3 appends SLIPS63 to
     `.agent/prose_slips.md` and C4 appends DEC63 to `.agent/decisions.md`.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline and the slice's body. All three target files end with a
          single newline and no trailing blank line at the base, and all three separate
          their entries by a blank line, which is why the inserted newline is the same for
          each.
            .agent/live_review.md   pre  996190 at the base, slice RECORD63
            .agent/prose_slips.md   pre  253122 at C2,       slice SLIPS63
            .agent/decisions.md     pre 1130791 at C3,       slice DEC63
          Report each pre size, each post size and each delta. The slice body sizes are
          NOT stated here: each is the length of what you extracted.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N for each of the three.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter — a byte b with
          `b < 128 and chr(b).isalpha()` — inside the FIRST appended paragraph, and report
          that BOTH readers reject it. Report ALSO that both readers ACCEPT the unmutated
          region, because a reader that rejects everything proves nothing by rejecting.
     (iv) RECORD63 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0. Report the count of `^- R-` and of `^Done: R-` lines that C2
          ADDS, both of which must be 0.
     (v)  Report RECORD63's first line beside the count of lines in `.agent/live_review.md`
          at `93063ec4` already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.`,
          and whether the new first line matches that pattern and duplicates none of them.
          Report the number your script counted; this block states none.
     (vi) DEC63 must begin `## DECISION F275 D37 ` and `.agent/decisions.md` at the base
          must contain NO line matching `^## DECISION F275 D37`. Report both readings, and
          report the highest existing `^## DECISION F275 D\d+` heading at the base.
     (vii) Both paragraphs SLIPS63 adds must begin `2026-09-11 · F275 R62 · `. Report the
          count of lines in `.agent/prose_slips.md` at `93063ec4` already beginning with
          that exact prefix, which this block states none of, and the count C3 adds.

  G4 THE ARTEFACT AND THE INSTRUMENT ARE THE AUTHORED BLOBS AND NOTHING ELSE.
     `.agent/f275_t003_flip_residue_r63.md` at C5 must be byte-identical to the
     `.agent/authored/f275-r63-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show 93063ec4:.agent/f275_t003_flip_residue_r63.md`, which must be non-zero.
     Report the artefact's line count and the instrument blob's line count, each against
     the DECISION F104 D1 cap of 500 insertions.

  G5 THE ARTEFACT'S NUMBERS ARE RE-DERIVED FROM THE COMMITTED INSTRUMENT.
     The instrument is committed at `.agent/authored/f275-r63-diag.py.md` at C0c, inside a
     ```python fence. Extract that fenced source into `.remedy-wt/` and RUN it with
     `python3 -B`, REDIRECTED to a file per constraint 11. Report the number of fences
     your script found. It prints four banners; report from its OUTPUT, and where a
     reading below names a token, `grep` the output for that token rather than reading
     around it.
     (a) Banner 1. Report the three `E-lines` counts and, for each class, every line
         beginning `frame ` and every line beginning `stderr ` that the banner prints
         beneath it. The artefact's section 2 states 337, 223 and 90, with 193 at
         `data_paths.py:324`, 87 at `uuid.py:177` and 90 at `data_paths.py:200`, and the
         three stderr rows 180, 123 and 13. Say whether each agrees.
     (b) Banner 2 and banner 2b. Report every line of both literally. The artefact's
         sections 3 and 4 rest on four of them: that `UUID(mint_job_id())` raises
         `badly formed hexadecimal UUID string`, that `job_dir` and `load_job_plan` each
         raise `unsupported operand type(s) for /: 'PosixPath' and 'UUID'`, that the
         CONTROL lines beneath them SUCCEED, and that the unified record's WHOLE id still
         reads `resolve_job_id -> SystemExit: 1` while `task finds it` on the same row.
         The two CONTROL lines carry a freshly minted id and therefore differ run to run;
         do not compare them byte for byte, compare that they returned rather than raised.
     (c) Banner 3. Report `every \`UUID(...)\` call`, the `sites that BIND a UUID and pass
         it on` line with its scope and file counts, the `under apps/cli/` line, and every
         `callee ` line. The artefact's section 7 states 105, 75 over 39 scopes in 18
         files, 58 and 17, and `load_job` at 29.
     (d) Banner 4. Report the three run rows and the `the candidate rule FIXED` line and
         both `BROKE ` lines. The artefact's section 6 states the control at exit 0 and
         1345 passed, the flipped run at 263 failed, the candidate run at 249 failed, and
         FIXED 16 / BROKE 2 / 247 surviving.
     A figure the instrument prints that DISAGREES with the artefact is reported as it
     read and is a finding; do not reconcile it in either direction. A figure the artefact
     states that the instrument does NOT print is likewise reported as absent rather than
     supplied from elsewhere — except the two the artefact's own PROVENANCE paragraph
     already declares are not in it, which are not owed here.

  G6 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `93063ec4` and at C5, and whether all five are EQUAL.
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
         reading AFTER G5 has run, because constraint 12 names the one thing this round
         writes and this is the reading that proves it wrote nothing tracked.
     (b) The changed-path set over `93063ec4`..C5 must be exactly the Change section's
         paths other than `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `docs/`, `scripts/`, `packages/`,
         `apps/` or `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `93063ec4` and at C5. Report both, the ids registered,
         the ids resolved and the ids de-registered, all three of which must be empty.
         Report the highest id in the record at each end.
     (d) Per-commit insertions from `git show --numstat <sha>` for C0a through C5, each
         against the AGENTS.md DECISION F104 D1 cap of 500, and the maximum over them.
         C6's own numbers are NOT ordered here: they cannot exist while C6 is being
         written, and the reviewer records them at the next gate.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 24 of F275 and
             round 63, the one-sentence context self-assessment amend0905-throughput
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

BEGIN-PLAN63 sha256=af9865be58706c0d668c9b81de0a260f14474ce871de5ada5844baee17e8fc11
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

ROUND 63 DIAGNOSES the three largest residue classes and DECISION F275 D37 rules them. They
are ONE id-SHAPE seam, not a fourth rule family and not a data migration: a resolver that
searches only the classic store, and a handler layer that parses its argument into a
`uuid.UUID` and hands the OBJECT to the store. The candidate fourth rule was built, applied
and run; it fixed 16 and BROKE 2, and 247 of 263 survived. The artefact is
`.agent/f275_t003_flip_residue_r63.md`. The round 62 verdict and its two prose slips are
booked here. No line under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moves.

## Next Steps

1. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 now names
   as the home of both halves of the seam: one resolver reaching both stores, and the
   handler layer routed through it instead of through `UUID(...)`. Production code, so a
   SPLIT round with mutation red-proofs.
2. Build `R-0880`'s second obligation, the transform's refusal to rename a site whose owner
   verdict cannot be confirmed, and resolve the 39 pairs or re-derive the site set with a
   column in its key. DECISION F275 D36 forbids the flip commit until one of those lands.
3. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, registering
   the `acceptance_checks` finding DECISION F275 D22 places with it.
4. The classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- 1186 failures is not a landable state, and the largest classes are now understood to need
  PRODUCTION-CODE work rather than another transform rule — a bigger step, not a smaller one.
- The 42 errors have not moved across three runs and are still undiagnosed.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN63

BEGIN-RECORD63 sha256=67b689f55731e882f417a01d778fb0de33baeeb6e2b49ba78d90b3ae4aa05f83
Gate: F275 R62 — the F275 round 62 entry. VERDICT PASS. Written by the planner and reviewer of session 23 after reading the committed range `7910aa7d`..`79129f58` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 63, per operator amendment amend0827-process-diet rule 1. The round bounded finding `R-0880` STATICALLY at 39 ruled sites and ruled the result as the decision recorded at `549dc58b`.

G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: all three authored blobs are byte-identical to the reviewer's own scratch originals — the block at 29515 bytes, the artefact at 6473 and the bound instrument at 3770 — and `.agent/last_block.md` equals the block blob. All three slices matched the sha256 on their own BEGIN markers. Re-measured on the committed blob the block is 289 lines TOTAL and 212 PROSE, agreeing with its own constraint 8. G2: `.agent/plan.md` is byte-identical to its slice at 2576 bytes over 45 lines, both mandated headings exactly once.

G3: `.agent/live_review.md` goes 990200 to 996190 and `.agent/decisions.md` 1124939 to 1130791, both exact under reader A, reader B holding at N counted as 8 and 9; the reviewer ran its own negative controls and both are REJECTED by both readers while both unmutated regions are ACCEPTED. The D36 heading reads 0 at the base and 1 at C3. G4: the artefact at C4 is byte-identical to the C0b blob and the path does not resolve at the base. G6: all five top-level trees are byte-identical at the base and at C4, the canary reads 42 passed at exit 0, and `ruff check .` reads 26 rows at the frozen ceiling with zero under `.remedy-wt/` and zero `.py` rows under `.agent/`. G7: eight changed paths with MISSING and EXTRA empty and zero production paths; the open set is 88 at both ends with registered, resolved and de-registered ALL EMPTY; per-commit insertions peak at 289, so F275's one declared-oversize allowance is STILL UNSPENT at 62 rounds. The handback commit's own numbers, which no gate of that round could reach, are 489 insertions and 391 deletions.

THE WORKER REPORTED TWO DEFECTS IN THE BLOCK AND BOTH WERE THE REVIEWER'S. Neither is an id, because neither left anything wrong on disk — operator amendment amend0827-process-diet rule 2 — and both are booked as dated lines in `.agent/prose_slips.md` by this same round. The first and more serious is a gate that could not be met as written: G5(b) ordered "the two rows the instrument prints for `packages/orchestration/loop_run.py:285` — their columns, receivers, owner verdicts and `static` values", while the committed instrument aggregates per at-risk LINE and prints ONE row per line with no column and no `static` value anywhere in its output. The reviewer confirmed this independently by extracting the fenced source from the committed blob and running it. The rows the artefact's section 2 quotes are real measurements, but they were taken with a DIFFERENT script during the reviewer's own dry run.

THE WORKER'S HANDLING OF THAT GATE IS THE RIGHT ONE AND IS WORTH NAMING: it ran the instrument UNMODIFIED, reported the one row it actually prints, refused to reconcile the difference in either direction, and then ran a SEPARATE and CLEARLY LABELLED probe over the same two inputs which returned `col=40 recv=mission owner=Job static=None` and `col=56 recv=job owner=Job static=None`. So the artefact's section 2 substance HOLDS and only the gate's premise about where those numbers live was wrong. A worker that had quietly edited the instrument to print what the gate wanted would have destroyed the evidence that round existed to produce.

The second defect is a stale numeral: the block's Handback section ordered the worker to carry "SESSION 23 of F275 and round 61" while every other sentence in the block says 62. It is a carry from round 61's block, which the reviewer adapted rather than rewrote, and the two-line wrap is why the correction missed it. The worker labelled its handback round 62, which is right: obeying the numeral literally would have put two consecutive handbacks both claiming to be round 61, and `.agent/handoff.md` is the file AGENTS.md's Session Resume tells the next session to read. The remaining deviations are sustained and standing — the plan named round 61 across the block-save commits as constraint 3 requires, ruff exits 1 by design while the gate is the count, the absence probe exits 128, and C4 was copied with `shutil.copyfile` from a working-tree path first asserted byte-equal to the committed blob.
END-RECORD63

BEGIN-SLIPS63 sha256=586a5703242a9cbb368408df8c56536c0e697d9328c16f358e73255059f620c0
2026-09-11 · F275 R62 · The round 62 block's G5(b) ordered a reading the committed instrument cannot produce: "the two rows the instrument prints for `packages/orchestration/loop_run.py:285` — their columns, receivers, owner verdicts and `static` values", where that instrument aggregates per at-risk LINE, prints ONE row per line, and emits no `col=` and no `static=` anywhere. The rows the artefact quotes are real but were taken with a DIFFERENT script during the reviewer's own dry run. The reviewer DID run the instrument at the base before emitting, and that is exactly why this is worth a line: running it is not the same as reading its OUTPUT against the words of the gate, and the base run's transcript was checked for its headline figures and its cross-check block while the clause about columns was never compared to anything. THE RULE THAT FOLLOWS: where a gate orders a specific READING from a named artefact, the pre-emission check greps that artefact's actual output for the tokens the gate names, and a gate may not order a field that the output does not contain.

2026-09-11 · F275 R62 · The round 62 block's Handback section ordered the worker to carry "SESSION 23 of F275 and round 61" while the block is round 62 and every other sentence in it — the STEP header, the Bundle, the changed-path filenames, PLAN62 and DEC62's dateline — says 62. It is a stale carry from round 61's block, which was adapted rather than rewritten, and the correction missed it because the numeral sits on the second line of a two-line wrap where the search pattern matched neither half alone. The worker labelled its handback round 62 and declared the contradiction, so nothing on disk is wrong. THE RULE THAT FOLLOWS: when a block is adapted from the previous round's, the ROUND NUMERAL is re-checked by a sweep over the whole block for the previous round's number, run after the last edit — not by replacing the strings the author remembers writing.
END-SLIPS63

BEGIN-DEC63 sha256=c16b1a0da684d6ebafba62a6eadcd4b3f8adc746a52397c39ed2b4ae4aff688a
## DECISION F275 D37 (2026-09-11, F275 round 63) — the three largest residue classes are ONE id-SHAPE seam, and it is production-code work in T003 rather than a fourth transform rule

CONTEXT. `.agent/plan.md` at `93063ec4` set this round one question: the three largest residue classes of the flip's dry run — `SystemExit` at `data_paths.py:324`, `unsupported operand` at `data_paths.py:200` and the hexadecimal-UUID parse — are reads of an id whose SHAPE changed rather than renames, so are they a FOURTH rule family of DECISION F275 D32's kind, or a consequence of records already written to disk under the classic shape? The measurement is in `.agent/f275_t003_flip_residue_r63.md` and the instrument that produced it is committed at `.agent/authored/f275-r63-diag.py.md`.

CHOSEN, PART ONE: THEY ARE ONE SEAM AND NOT THREE CLASSES. The unified store mints a job id as the sixteen hex characters `mint_job_id` returns; the classic store's id is a `uuid.UUID`. The handler layer parses its argument with `UUID(job_id_str)` and passes the resulting OBJECT to the store. After the flip that store is the unified one, so three things happen at once and each is one of the three classes: the parse REFUSES a sixteen-hex id and the handler exits, which is the `badly formed hexadecimal UUID string` line and the `invalid job ID` exit; a `UUID` object that does get through reaches `jobs_dir(root) / job_id`, which has no `__truediv__` for it, which is every one of the 90 `unsupported operand` lines at `data_paths.py:200`; and `resolve_job_id` searches the CLASSIC store alone, so a unified record it is standing next to is unresolvable, which is the `no job matches prefix` exit at `data_paths.py:324`.

CHOSEN, PART TWO: IT IS NOT A DATA MIGRATION, AND THAT HALF IS ANSWERED BY A PROBE. All three failures reproduce by CALLING the shipped functions against a root that does not exist, before any file is opened, each beside a control on the shape the unified store mints that succeeds. No record on disk participates. `JobPlan` is a dataclass and not a pydantic model, so its `job_id: str` annotation validates nothing and a `UUID` handed to that keyword is stored unchanged — which is the whole of the coercion that does not happen.

CHOSEN, PART THREE: A FOURTH RULE FAMILY WAS BUILT, APPLIED AND RUN, AND IT DOES NOT CLOSE THEM. The narrowest rewrite that could — T7's `UUID(...)` unwrap widened from a constructor keyword to any call position, under `apps/cli/` — was applied to the flipped worktree and the same scoped selection run three times. The control is a REAL exit 0 at 1345 passed, the flipped run is 263 failed, and the flipped run with the candidate rule is 249 failed: it FIXED 16 and BROKE 2, leaving 247 of 263. The two it broke are the ruling, and they are named in the artefact: both assert the `invalid job ID` guard that the unwrap deletes. A parse in a handler is a VALIDATION, not a coercion, so no rewrite removes it without changing behaviour — and a rule family of D32's kind renames a field and changes no behaviour. The thing that would close these classes is therefore not a member of the category the question offered.

CHOSEN, PART FOUR: THE WORK HAS A HOME ALREADY, AND THIS DECISION PLACES IT THERE RATHER THAN MINTING A NEW SLICE. Both halves of the seam are the resolver collapse DECISION F260 D5 places in T003 and that `docs/roadmap/features/T2_F275.md` carries verbatim: one resolver that reaches both stores, and a handler layer routed through it instead of through `UUID(...)`. That is production code, so it is a SPLIT round with mutation red-proofs, and it is ordered BEFORE the flip rather than after it — the flip's dry run cannot be read as converging while its largest classes are a seam the transform provably cannot reach.

ALTERNATIVES CONSIDERED. (i) Ship the unwrap anyway as a partial win — rejected on this round's own measurement: it clears 16 of 263 and breaks two guards, so it buys a worse tree for a rounding error. (ii) Migrate the on-disk records to the classic shape — rejected: the probe shows the failures need no record at all, so the migration would leave every one of them standing. (iii) Widen the unwrap beyond `apps/cli/` to the 17 sites outside it — not rejected on principle and still worthless on its own, because it addresses only the `unsupported operand` half and leaves the resolver untouched; it is subsumed by the collapse, which removes the parse rather than unwrapping it. (iv) Declare the classes out of scope and flip anyway — rejected by name: 1186 failures is not a landable state and DECISION F275 D36 independently forbids the flip commit until its own condition is met.

WHAT THIS DECISION DOES NOT RULE. It does not design the collapse; it names where the work belongs and what it must reach. It does not claim the three classes are the whole residue — the artefact's own section 8 states that the 650 is a count of E-LINES rather than of distinct failures, that a `--tb=line` run prints no per-test header and so cannot attribute one to the other, and that the one distinct-failure count measured here is 263 over `tests/cli/` alone. It does not touch the 42 errors, which have now not moved across three runs. And it does not resolve or register any finding id.

HOW TO REVERSE: delete this decision. The three classes then stand as an open question, the candidate rule's negative result stays on the record in the artefact, and the next session re-derives the ruling from that artefact in the time it takes to read it.
END-DEC63
