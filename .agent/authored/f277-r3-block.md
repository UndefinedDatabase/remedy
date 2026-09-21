STEP R3 T001 — F277 Machine contracts: event vocabulary, JSON envelope, exit codes
Session 2 of F277 · round 3 · base `69b7c729` (the tip of `feature/f277-machine-contracts`,
round 2's C5). This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 2's PASS verdict and give `command_discovery_completed` its writer, exactly as the
reviewer's dry run built it. `remedy test discover <job>` records itself in the run ledger with
the two metadata keys `memory_learn` already indexes, so the `command_discovery` readiness
signal becomes reachable and autonomy level 3 stops being ineligible for every job that has ever
existed. The name then moves out of `READ_ONLY_EVENT_NAMES` into `EVENT_NAMES`, and the
quarantine goes from four names to three.

Read first, completely: AGENTS.md; `docs/roadmap/features/T2_F277.md`; and DECISION F277 D4 in
`.agent/decisions.md`, which is this round's spec and which named this disposition when it was
written — where this block is terser, D4 rules. This round registers NO new DECISION, because
D4 already fixed both the site and the metadata keys.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f277-r3-payloads/`. Verify each
line count and sha256 BEFORE use and report both readings; any mismatch stops the round. Apply
byte-exact, never by retyping.
  ledger.md        lines 2   sha256 e222251d49b68709de22147ba3f340e266af6ea7d552ebdeb7c1cb7cf58d8751
  plan.md          lines 45  sha256 1695246a0aee8b325b18808361070f58d85570fe32a66fb8ea4b8f5b0f4659a3
  prose_slips.md   lines 1   sha256 4c1f26be532c94d2437dcab3eb5f566fd459a44e52c578e364d68be5b35e7849
  block.md         this block; save it and report its line count and digest (R-0954)
CODE — ONE diff the reviewer produced in its own dry-run worktree at `69b7c729`, applied there,
tested there and red-proved there. Verify its digest, then apply it in TWO disjoint slices with
the `--include` lists below, always from its scratch path. Do not retype a hunk, do not edit
one, do not copy the diff into the repository, and never apply it whole — C2 and C3 are separate
commits because the production change and its tests are separate reviewable units.
  `.remedy-wt/f277-r3-payloads/f277-r3.diff`
    lines 143  sha256 bccefe4eb873bcdf1c21409ba6ba7e94c14966121f54d7a32c884456462f918d

SHAPE OF EACH STATE PAYLOAD, tested mechanically by the reviewer at `69b7c729`, one reading per
pair, the label derived from that reading's own output on the same line (item 15):
  `.agent/live_review.md` contains ledger.md — false, so APPEND
  `.agent/prose_slips.md` contains prose_slips.md — false, so APPEND
  `.agent/plan.md` contains plan.md — false, so REWRITE
Every pair reads false, so all are NEW bytes and NO FROM-count proof is owed on any of them.
ledger.md begins with a newline, the blank separator its target uses between entries;
prose_slips.md does not, because that file is one line per slip. There is no
`.agent/decisions.md` payload this round, no `docs/roadmap/**` edit and no live_review re-head.

Bundle, in commit order
C1a the payload copies, ONE commit whose whole change set is new files under `.agent/authored/`:
   a byte copy of each payload listed above, `block.md` included, as
   `.agent/authored/f277-r3-<name>` — keeping each payload's own file name after the prefix. The
   code diff is NOT copied and is NOT part of this or any commit; G2's blob-id gate is its
   fidelity proof, which pins the applied RESULT rather than the instructions. This block states
   no expected insertion count here, because the commit copies THIS BLOCK and the count
   therefore moves with every edit to it (item 16, R-0656). Report the number YOU read with
   `git show --numstat`, and stop only if yours reaches 500.
C1b the booking, ONE commit: `.agent/plan.md` := plan.md; `.agent/live_review.md` := its
   `69b7c729` bytes + ledger.md; `.agent/prose_slips.md` := its `69b7c729` bytes +
   prose_slips.md. The reviewer's arithmetic is 23 insertions — 2 for the ledger append, 1 for
   the prose-slip line, and 20 for the plan REWRITE, which is the numstat of the rewrite and not
   the payload's 45 lines, because the new plan and the one it replaces share lines. That
   distinction is the round 2 slip this very round books; report the number YOU read and say so
   where it differs.
C2 the writer and the declaration —
   `git apply --include=apps/cli/commands/test_cmds.py
    --include=packages/orchestration/event_names.py
    .remedy-wt/f277-r3-payloads/f277-r3.diff`
   then commit. Expected insertions 24; report the number YOU read.
C3 the tests —
   `git apply --include=tests/test_command_discovery.py
    .remedy-wt/f277-r3-payloads/f277-r3.diff`
   then commit. Expected insertions 79; report the number YOU read.
C4 handoff — rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the Session
   section reading "SESSION 2 of feature F277 · round 3 · rounds so far 3" plus ONE sentence of
   context self-assessment; the per-commit table with `git show --numstat` insertion counts for
   C1a, C1b, C2 and C3; every gate below with its real output and exit code, one line per gate;
   the open-findings count by distinct id; the item-status table; the deviations; and `## Next`
   naming Phase 1 rule 1 first, then the review of round 3, then round 4's disposal of
   `snapshot_created` and the remainder of `patch_intent_reverted`, and "Operator questions
   open: <the count of `### Q` headings you read from `.agent/operator_questions.md`>". Then
   `git push -u origin feature/f277-machine-contracts`. Open NO pull request.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as a deviation and
   applied anyway; it is never edited and no slice is retyped.
2. Change set: the paths the Bundle names, and nothing else. In particular do NOT edit
   `docs/roadmap/STATUS.md`, `README.md`, `docs/roadmap/features/T2_F277.md` or
   `.agent/decisions.md` — the feature file's Built State is written by the closure sequence,
   and no `docs/roadmap/**` path is in this round's change set, so `tests/docs/` is not among
   the gates.
3. The commit sequence is C1a, C1b, C2, C3, C4: no extra commit, none dropped, none reordered.
   C1b precedes C2 so `.agent/plan.md` is current before the first product commit (item 23). C2
   precedes C3 because the tests exercise the handler C2 changes.
4. An insertion count is read with `git show --numstat`, whose `+` column is the reading DECISION
   F104 D1 fixes for the 500-line cap; `git commit`'s own terminal summary applies rename
   detection and is NOT that reading. Read it for EVERY commit, C1a and C1b included. If any
   commit reaches 500 insertions by that reading, STOP and report — no oversize exception is
   declared for this feature. The three expected values above are the reviewer's arithmetic;
   where yours differs, report YOURS and say so, and stop only if yours reaches 500.
5. Never force-push, never rewrite history, never delete a branch, never merge. Run NO `gh`
   command at all this round.
6. Read `.agent/STOP` from disk before the first commit. If it exists, write the handoff and end,
   doing nothing else.
7. The shell may deny `VAR=x cmd`, `cp` and some compound commands; copy bytes and read exit
   codes with small python scripts under `.remedy-wt/f277-r3-payloads/`. Prefer `git -C <path>`
   over `cd <path> && git`.
8. `.remedy-wt/` is gitignored scratch. Never run `git clean -x`. The directories
   `.remedy-wt/f277-r1-payloads/`, `.remedy-wt/f277-r2-payloads/`, `.remedy-wt/f277-r3-dry/` and
   `.remedy-wt/f277-s2/` are the reviewer's and are not yours to delete; `f277-r3-dry` is a
   registered worktree of this repository and removing it is a history-touching act this block
   does not order.
9. Never weaken an assertion or delete a test. A red gate, or an ambiguity DECISION F277 D4 does
   not settle, stops the round: commit nothing half-done and report.
10. The full suite does NOT run this round (amend0917-throughput rule 1). It runs once per
    feature, in the closure sequence's integration-gate round.
11. Commit messages "F277 R3 C<n>: <summary>", a blank line, then
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when — the six gates below, each EXECUTED, each reporting its REAL output and exit code.
"Green" as a word is a finding. G1 to G5 run at C3, before C4.

G1 TRANSPORT AND STATE. One python check printing an explicit True or False per reading.
   (a) Each `.agent/authored/f277-r3-*` file equals its payload on disk byte for byte. Report
       the number of such files YOU measured rather than taking a count from this block.
   (b) THE RECORD APPEND, in full byte forensics, which the gate budget reserves for
       `.agent/live_review.md`: at C1b the file equals its `69b7c729` bytes plus ledger.md.
       Reading (a), byte equality of pre plus payload against post; reading (b), an INDEPENDENT
       structural reader that splits the post file on blank lines and compares its LAST N units,
       in order, against ledger.md's N paragraphs, where N is a number the script COUNTS from the
       payload and never one this block states; and a NEGATIVE CONTROL that flips one byte inside
       the FIRST appended paragraph and confirms BOTH readings reject it. Decode with
       `errors="replace"` for the structural reading only, so a flip landing on a UTF-8
       continuation byte reports a rejection rather than a traceback; reading (a) stays on raw
       bytes.
   (c) Byte equality only: `.agent/plan.md` at C1b equals plan.md's bytes; `.agent/prose_slips.md`
       at C1b equals its `69b7c729` bytes plus prose_slips.md's bytes.
   (d) THE OPEN SET BY DISTINCT ID, counted as the distinct ids matching `^- R-\d+ — ` minus
       those matching `^Done: R-\d+ — `, at `69b7c729` and at C1b. Report both numbers. This
       round registers and resolves nothing, so the two must be equal; report them even so.
   Report the number of readings taken and that every one is True. SEPARATELY, report the SAVED
   BLOCK's own line count and sha256 beside the line count and digest this block's PAYLOADS
   section gives for `block.md` (R-0954).

G2 CODE TRANSPORT — the committed tree is the tree the reviewer tested, and this gate is the
   ONLY proof the diff arrived intact, since no copy of it is committed. At C3, `git rev-parse`
   over the three paths below must print exactly these three blob ids in this order:
     apps/cli/commands/test_cmds.py            b0f66911245a5708a679bc6d970e26a59788c749
     packages/orchestration/event_names.py     b82893659bfc8ca12cabb93ffebbbec60d41a2ec
     tests/test_command_discovery.py           4c1ef7d37ceddf3649799f05f0ec4fa68079af91
   Also report `git diff --name-only <C1b> <C3>` in full: it must name exactly those three paths
   and no other. Report that list and its length.

G3 THE TARGETED SUITE, in the primary checkout, serial (no `-n`), at C3:
     python3 -m pytest -q -p no:cacheprovider tests/test_command_discovery.py
       tests/orchestration/test_event_names.py tests/test_autonomy_readiness.py
       tests/test_memory_learn.py tests/test_grouped_cli.py tests/test_command_catalog.py
       tests/cli/test_test_run_runtime.py tests/orchestration/test_test_execution_service.py
       tests/orchestration/test_command_discovery.py tests/cli/test_golden_path.py
   Report the summary line and the exit code. It must read 0 failed at exit 0. The list is the
   test file this round touches plus the files nearest the two production modules it edits —
   `test_grouped_cli.py` and `test_command_catalog.py` for the CLI handler and its catalog entry,
   `test_autonomy_readiness.py` and `test_memory_learn.py` for the two readers the writer
   revives, and `test_test_run_runtime.py`, `test_test_execution_service.py` and
   `tests/orchestration/test_command_discovery.py` for the rest of the discovery path;
   `tests/cli/test_golden_path.py` is the canary.

G4 LINT, at C3:
     python3 -m ruff check apps/cli/commands/test_cmds.py
       packages/orchestration/event_names.py tests/test_command_discovery.py
   must print "All checks passed!". Pass ONLY these three paths.

G5 MUTATION RED-PROOFS, in ONE disposable worktree under `.remedy-wt/` created at C3 and removed
   as this gate's last action. Name it `.remedy-wt/f277-r3-g5` and do NOT reuse any existing
   directory there. Run every command from the worktree root with
     python3 -B -m pytest -q -p no:cacheprovider tests/test_command_discovery.py
       tests/orchestration/test_event_names.py
   Take the UNMUTATED CONTROL FIRST and report its exit code: it must be 0. Then apply each
   mutation below, one at a time, each restored byte-identically before the next; before each,
   COUNT the occurrences of the exact bytes the recipe replaces in the named file and report the
   count, which must be 1, because that uniqueness is what makes the restore safe. Report each
   run's exit code and its failing node ids, and report a mutation that stays green AS GREEN.
   (a) THE WRITER IS TAKEN AWAY AGAIN. In `apps/cli/commands/test_cmds.py`, replace the single
       line `            event="command_discovery_completed",` with
       `            event="agent_loop_inspected",` — another declared name, so the declaration
       tests stay green and only the four new tests can speak. Expected: FAIL, naming all four
       of `test_the_event_carries_the_keys_memory_learn_reads`,
       `test_the_json_mode_records_the_same_fact`,
       `test_the_readiness_signal_is_now_reachable` and
       `test_memory_learn_stores_the_two_entries`.
   (b) THE NAME IS PUT BACK IN THE QUARANTINE IT HAS OUTGROWN. Two edits, applied together as
       ONE mutation and reverted together, both in `packages/orchestration/event_names.py`:
       delete the single line `        "command_discovery_completed",` that sits directly below
       `        "command.accepted",`, and insert that same line directly above the unique
       comment line whose text, after eight leading spaces, is
       the two words "# Read" followed by " by " and then the backtick-quoted module name
       autonomy_loop.py, then a semicolon and the words "the writer spells it". That comment
       opens the `snapshot_created` entry of the quarantine and occurs exactly once in the file.
       Expected: FAIL, naming
       `test_a_read_only_name_that_gains_a_writer_leaves_the_quarantine` and
       `test_every_written_event_name_is_declared`.
   After the two, show that each of the two touched files is byte-identical to before (report a
   sha256 per file), run the UNMUTATED selection once more and report that it is exit 0 again,
   remove the worktree, and report `git worktree list` in full.

G6 PUSH AND TREE. `git push -u origin feature/f277-machine-contracts` after C4; then
   `git status --porcelain`, which must be EMPTY; then `ls .agent/STOP`, which must be absent;
   then `git worktree list` in full, which must show the primary checkout, the two
   `remedy/job-*` worktrees, and the reviewer's `.remedy-wt/f277-r3-dry`, and no other. These
   readings necessarily POSTDATE the commit that writes the handback, so they belong to your
   final report and not to the handoff's own text (item 31).

Handback
Rewrite `.agent/handoff.md` as C4 describes, then report. The handback names every gate with one
line of its real output, declares every deviation, and carries the item-status table. If any gate
is red, say so plainly WITH the output: a red gate honestly reported ends the round cleanly and
is worth far more than a green word.
