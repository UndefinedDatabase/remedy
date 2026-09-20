STEP R5 T001 — F277 Machine contracts: event vocabulary, JSON envelope, exit codes
Session 2 of F277 · round 5 · base `fa448bef` (the tip of `feature/f277-machine-contracts`,
round 4's C5). This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 4's PASS verdict and FINISH T001. The two names left in `READ_ONLY_EVENT_NAMES` are
not accidents: a dated decision removed each one's writer and kept its readers on purpose, so
that run logs already on disk keep rendering. The set is therefore renamed
`RETIRED_EVENT_NAMES` and its contract restated — every entry cites the decision that retired
it and names a module that still reads it, both asserted from the source by a new guard — and
`docs/roadmap/features/T2_F277.md` is amended to match, which
docs/agents/planner_reviewer_prompt.md §4 item 7 requires the reviewer to author rather than
re-plan silently.

Read first, completely: AGENTS.md; `docs/roadmap/features/T2_F277.md`; and the payload
`decisions.md`, which is DECISION F277 D5 and is this round's spec — where this block is
terser, D5 rules. D5 cites two prior rulings by id; you do not need to read them, because D5
quotes what they said.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f277-r5-payloads/`. Verify each
line count and sha256 BEFORE use and report both readings; any mismatch stops the round. Apply
byte-exact, never by retyping.
  ledger.md        lines 2   sha256 ae24d8d97a9706e655002410ff914bd866bfa06fdfbfe1060aa74b75796f06d5
  decisions.md     lines 53  sha256 c1ee0ff9ce51b74ff10c49f5ea05282d9da3db1798de2c01cf9f5c180ddf073a
  prose_slips.md   lines 1   sha256 4183bbd735e85ff64e2faf1713f15f3c6de9ffdb1bd10590263e3cb6220ca114
  plan.md          lines 44  sha256 e8bb27bbef78e3de9f1d2eae8ae204814553363d7fc788d22924b0e845098766
  block.md         this block; save it and report its line count and digest (R-0954)
CODE — ONE diff the reviewer produced in its own dry-run worktree at `fa448bef`, applied there,
tested there and red-proved there. Verify its digest, then apply it in TWO disjoint slices with
the `--include` lists below, always from its scratch path. Do not retype a hunk, do not edit
one, do not copy the diff into the repository, and never apply it whole.
  `.remedy-wt/f277-r5-payloads/f277-r5.diff`
    lines 315  sha256 41f3fe25b096fdcad22e9f5593617c480041ea417fe825e59d4c11efaed3452b

WHY C2 CARRIES TWO FILES, which is a departure from this feature's habit of one production
commit and one test commit, and is measured rather than assumed. `RETIRED_EVENT_NAMES` is a
rename of `READ_ONLY_EVENT_NAMES`, and the symbol's only importer anywhere under `packages/`,
`apps/` or `tests/` is `tests/orchestration/test_event_names.py`. The reviewer applied the
production half alone in its dry-run worktree at `fa448bef` and ran the selection: it ends
`ImportError: cannot import name 'READ_ONLY_EVENT_NAMES'` at COLLECTION, `1 error in 0.12s`.
Splitting the rename would therefore push a red tip, so the symbol and its importer land
together in one commit of 120 insertions, well under the cap.

SHAPE OF EACH STATE PAYLOAD, tested mechanically by the reviewer at `fa448bef`, one reading per
pair, the label derived from that reading's own output on the same line (item 15):
  `.agent/live_review.md` contains ledger.md — false, so APPEND
  `.agent/decisions.md` contains decisions.md — false, so APPEND
  `.agent/prose_slips.md` contains prose_slips.md — false, so APPEND
  `.agent/plan.md` contains plan.md — false, so REWRITE
Every pair reads false, so all are NEW bytes and NO FROM-count proof is owed on any of them.
ledger.md and decisions.md each begin with a newline, the blank separator their targets use
between entries; prose_slips.md does not, because that file is one line per slip. There is no
resolution payload this round, because this round registers no finding.

Bundle, in commit order
C1a the payload copies, ONE commit whose whole change set is new files under `.agent/authored/`:
   a byte copy of each payload listed above, `block.md` included, as
   `.agent/authored/f277-r5-<name>` — keeping each payload's own file name after the prefix. The
   code diff is NOT copied and is NOT part of this or any commit; G2's blob-id gate is its
   fidelity proof, which pins the applied RESULT rather than the instructions. This block states
   no expected insertion count here, because the commit copies THIS BLOCK and the count
   therefore moves with every edit to it (item 16, R-0656). Report the number YOU read with
   `git show --numstat`, and stop only if yours reaches 500.
C1b the booking, ONE commit: `.agent/plan.md` := plan.md; `.agent/live_review.md` := its
   `fa448bef` bytes + ledger.md; `.agent/decisions.md` := its `fa448bef` bytes + decisions.md;
   `.agent/prose_slips.md` := its `fa448bef` bytes + prose_slips.md. Expected insertions 80 —
   2 plus 53 plus 1 for the three appends and 24 for the plan REWRITE, which is the numstat of
   the rewrite and not the payload's 44 lines. Every one of those four numbers was computed by
   the reviewer's preflight script from the payload files this block ships, which is the rule
   the prose-slip line in this round's own payload leaves behind. Report the number YOU read.
C2 the rename, the restated contract and the new guard —
   `git apply --include=packages/orchestration/event_names.py
    --include=tests/orchestration/test_event_names.py
    .remedy-wt/f277-r5-payloads/f277-r5.diff`
   then commit. Expected insertions 120; report the number YOU read.
C3 the feature-file amendment —
   `git apply --include=docs/roadmap/features/T2_F277.md
    .remedy-wt/f277-r5-payloads/f277-r5.diff`
   then commit. Expected insertions 26; report the number YOU read. This is the only
   `docs/roadmap/**` path this round touches and it is why G3 carries `tests/docs/`.
C4 handoff — rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the Session
   section reading "SESSION 2 of feature F277 · round 5 · rounds so far 5" plus ONE sentence of
   context self-assessment; the per-commit table with `git show --numstat` insertion counts for
   C1a, C1b, C2 and C3; every gate below with its real output and exit code, one line per gate;
   the open-findings count by distinct id; the item-status table; the deviations; and `## Next`
   naming Phase 1 rule 1 first, then the review of round 5, then T002 — the JSON envelope and
   the error boundary — and "Operator questions open: <the count of `### Q` headings you read
   from `.agent/operator_questions.md`>". Then
   `git push -u origin feature/f277-machine-contracts`. Open NO pull request.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as a deviation and
   applied anyway; it is never edited and no slice is retyped.
2. Change set: the paths the Bundle names, and nothing else. In particular do NOT edit
   `docs/roadmap/STATUS.md` or `README.md` — no feature is registered or accepted this round, so
   no ledger count moves and no `tests/docs/` pin changes with it.
3. The commit sequence is C1a, C1b, C2, C3, C4: no extra commit, none dropped, none reordered.
   C1b precedes C2 so `.agent/plan.md` is current before the first product commit (item 23), and
   so DECISION F277 D5 is on disk before the code that applies it (amend0917 rule 3 requires the
   DECISION and its patch in the SAME round; this orders them within it).
4. An insertion count is read with `git show --numstat`, whose `+` column is the reading DECISION
   F104 D1 fixes for the 500-line cap; `git commit`'s own terminal summary applies rename
   detection and is NOT that reading — rounds 3 and 4 measured the two at 23 against 48 and at
   130 against 198, so report which you used. Read it for EVERY commit. If any commit reaches
   500 insertions by that reading, STOP and report — no oversize exception is declared for this
   feature. The three expected values above are the reviewer's arithmetic; where yours differs,
   report YOURS and say so, and stop only if yours reaches 500.
5. Never force-push, never rewrite history, never delete a branch, never merge. Run NO `gh`
   command at all this round.
6. Read `.agent/STOP` from disk before the first commit. If it exists, write the handoff and end,
   doing nothing else.
7. The shell may deny `VAR=x cmd`, `cp` and some compound commands; copy bytes and read exit
   codes with small python scripts under `.remedy-wt/f277-r5-payloads/`. Prefer `git -C <path>`
   over `cd <path> && git`.
8. `.remedy-wt/` is gitignored scratch. Never run `git clean -x`. The directories whose names
   begin `f277-` under `.remedy-wt/` are the reviewer's and are not yours to delete;
   `f277-r5-dry` is a registered worktree of this repository and removing it is a
   history-touching act this block does not order.
9. Never weaken an assertion or delete a test. A red gate, or an ambiguity DECISION F277 D5 does
   not settle, stops the round: commit nothing half-done and report.
10. The full suite does NOT run this round (amend0917-throughput rule 1). It runs once per
    feature, in the closure sequence's integration-gate round.
11. Commit messages "F277 R5 C<n>: <summary>", a blank line, then
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when — the six gates below, each EXECUTED, each reporting its REAL output and exit code.
"Green" as a word is a finding. G1 to G5 run at C3, before C4.

G1 TRANSPORT AND STATE. One python check printing an explicit True or False per reading.
   (a) Each `.agent/authored/f277-r5-*` file equals its payload on disk byte for byte. Report
       the number of such files YOU measured rather than taking a count from this block.
   (b) THE RECORD APPENDS, in full byte forensics, which the gate budget reserves for
       `.agent/live_review.md` and `.agent/decisions.md`. For each at C1b — the ledger file
       against its `fa448bef` bytes plus ledger.md, and the decisions file against its
       `fa448bef` bytes plus decisions.md — take reading (a), byte equality of pre plus payload
       against post; reading (b), an INDEPENDENT structural reader that splits the post file on
       blank lines and compares its LAST N units, in order, against the payload's N paragraphs,
       where N is a number the script COUNTS from the payload and never one this block states;
       and a NEGATIVE CONTROL that flips one byte inside the FIRST appended paragraph and
       confirms BOTH readings reject it. Each payload's leading newline is the blank SEPARATOR
       between entries and not a paragraph of its own. Decode with `errors="replace"` for the
       structural reading only; reading (a) stays on raw bytes.
   (c) Byte equality only: `.agent/plan.md` at C1b equals plan.md's bytes;
       `.agent/prose_slips.md` at C1b equals its `fa448bef` bytes plus prose_slips.md's bytes.
   (d) THE OPEN SET BY DISTINCT ID, counted as the distinct ids matching `^- R-\d+ — ` minus
       those matching `^Done: R-\d+ — `, at `fa448bef` and at C1b. Report both numbers. This
       round registers and resolves nothing, so the two must be equal; report them even so.
   Report the number of readings taken and that every one is True. SEPARATELY, report the SAVED
   BLOCK's own line count and sha256 beside the line count and digest this block's PAYLOADS
   section gives for `block.md` (R-0954).

G2 CODE TRANSPORT — the committed tree is the tree the reviewer tested, and this gate is the
   ONLY proof the diff arrived intact, since no copy of it is committed. At C3, `git rev-parse`
   over the three paths below must print exactly these three blob ids in this order:
     packages/orchestration/event_names.py     e8db6fb63f898ce37802a61dcf34e2b06dcc50ed
     tests/orchestration/test_event_names.py   4826c76e49802e24018069da0fc5c0932278afe9
     docs/roadmap/features/T2_F277.md          511041c4c1a1919678213467e73883b118e8e8c3
   Also report `git diff --name-only <C1b> <C3>` in full: it must name exactly those three paths
   and no other. Report that list and its length.

G3 THE TARGETED SUITE, in the primary checkout, serial (no `-n`), at C3:
     python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_event_names.py
       tests/test_run_log.py tests/docs tests/orchestration/test_roadmap_index.py
       tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py
       tests/cli/test_golden_path.py
   Report the summary line and the exit code. It must read 0 failed at exit 0. `tests/docs` and
   `tests/orchestration/test_roadmap_index.py` are here because C3 edits a `docs/roadmap/**`
   path; `tests/test_run_log.py` is the file nearest the only production module that imports the
   renamed symbol's module; `tests/cli/test_golden_path.py` is the canary.

G4 LINT, at C3:
     python3 -m ruff check packages/orchestration/event_names.py
       tests/orchestration/test_event_names.py
   must print "All checks passed!". Pass ONLY these two paths — the third changed path is
   markdown and ruff would parse it as Python.

G5 MUTATION RED-PROOFS, in ONE disposable worktree under `.remedy-wt/` created at C3 and removed
   as this gate's last action. Name it `.remedy-wt/f277-r5-g5` and do NOT reuse any existing
   directory there. Run every command from the worktree root with
     python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_event_names.py
   Take the UNMUTATED CONTROL FIRST and report its exit code: it must be 0. Then apply each
   mutation below, one at a time, each restored byte-identically before the next; before each,
   COUNT the occurrences of the exact bytes the recipe replaces in the named file and report the
   count, which must be 1, because that uniqueness is what makes the restore safe. Report each
   run's exit code and its failing node ids, and report a mutation that stays green AS GREEN.
   Mutation (c) touches `packages/orchestration/autonomy_loop.py`, which is NOT in this round's
   change set; it is mutated only inside the disposable worktree and restored there, and the
   primary checkout is never touched by this gate.
   (a) A RETIRED ENTRY LOSES ITS CITATION. In `packages/orchestration/event_names.py`, replace
       the single line
       `        # Retired by DECISION F031 D2 and D9, which retired the blocker addend` with
       `        # Retired a while ago by somebody, which retired the blocker addend`.
       Expected: FAIL, naming
       `test_the_entry_names_a_dated_decision[stop_reason_recorded]`.
   (b) A RETIRED ENTRY LOSES EVERY READING-MODULE NAME. In the same file, replace the whole
       six-line comment block that opens `        # Retired by DECISION F031 D2 and D9,` and
       ends `        # the event to exercise them.` with these four lines:
       `        # Retired by DECISION F031 D2 and D9, which retired the blocker addend`,
       `        # and the scan that read this name.  Three modules still render stop`,
       `        # reasons from run logs already on disk, and five test files plant the`,
       `        # event to exercise them.`
       Expected: FAIL, naming
       `test_the_entry_names_at_least_one_reading_module[stop_reason_recorded]`. The reviewer's
       FIRST attempt at this control removed only the last three of those six lines and the
       gate stayed GREEN, because `ui_server.py` survived in the lines above — a guard over a
       comment block is exactly the kind that passes by being blind, so the control that proves
       it must strip every match, and this one does.
   (c) A RETIRED NAME GAINS A WRITER. In `packages/orchestration/autonomy_loop.py`, insert
       directly above the single line
       `def _emit_token_policy_applied(job: JobPlan) -> None:` a function
       `def _writer_for_a_retired_name(log) -> None:` whose body is
       `    log.log("stop_reason_recorded")`, followed by two blank lines. Expected: FAIL,
       naming `test_a_retired_name_that_gains_a_writer_joins_the_vocabulary` and
       `test_every_written_event_name_is_declared`.
   (d) A RETIRED NAME LOSES ITS LAST READER. In `packages/orchestration/event_names.py`, replace
       the single line `        "patch_intent_reverted",` with
       `        "patch_intent_reverted_with_no_reader_at_all",`. Expected: FAIL, naming
       `test_every_retired_name_really_has_a_reader` and
       `test_every_read_event_name_is_declared`.
   After the four, show that each of the two touched files is byte-identical to before (report a
   sha256 per file), run the UNMUTATED selection once more and report that it is exit 0 again,
   remove the worktree, and report `git worktree list` in full.

G6 PUSH AND TREE. `git push -u origin feature/f277-machine-contracts` after C4; then
   `git status --porcelain`, which must be EMPTY; then `ls .agent/STOP`, which must be absent;
   then `git worktree list` in full, which must show the primary checkout, the two
   `remedy/job-*` worktrees, and the reviewer's `.remedy-wt/f277-r5-dry`, and no other. These
   readings necessarily POSTDATE the commit that writes the handback, so they belong to your
   final report and not to the handoff's own text (item 31).

Handback
Rewrite `.agent/handoff.md` as C4 describes, then report. The handback names every gate with one
line of its real output, declares every deviation, and carries the item-status table. If any gate
is red, say so plainly WITH the output: a red gate honestly reported ends the round cleanly and
is worth far more than a green word.
