STEP R1 T001 — F277 Machine contracts: event vocabulary, JSON envelope, exit codes
Session 1 of F277 · round 1 · base `f2494c02` (main, the merge of pull request 262, F276's closure).

This block contains no horizontal rule and no run of a repeated character, so nothing in its
frame has a length a reader must recover by eye (item 37).

THIS IS THE CORRECTED SECOND EMISSION OF ROUND 1. The first emission ordered a single C1 that
copied the code diff, this block and the decisions payload into `.agent/authored/` beside four
live `.agent/**` rewrites: 1207 insertions by `git show --numstat`, against its own constraint
ordering a STOP at 500. The worker built it, measured it, reset the unpushed commit and reported
the contradiction — the ordered behaviour, and the reason nothing landed. Two things change here
and nothing else does: the bookkeeping is SPLIT into C1a and C1b, and the code diff is NO LONGER
COPIED into the commit — G2's tree-id gate is its fidelity proof, which is stronger than a copy
because it pins the applied result rather than the instructions. The reviewer's slip is recorded
in the `prose_slips.md` payload, which C1b appends.

Goal
Claim F277, re-head `.agent/live_review.md`, book F276 round 15's verdict, and build T001 exactly
as the reviewer's dry run built it: `packages/orchestration/event_names.py` declaring the event
names this repository writes, the names it only reads quarantined beside them, the AST test that
measures both from the source, and an opt-in strict check in `RunLogWriter.log`.

Read first, completely: AGENTS.md; `docs/roadmap/features/T2_F277.md`; the payload `decisions.md`
(DECISIONs F277 D1, D2 and D3 — this round's spec; where this block is terser, they rule).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f277-r1-payloads/`. Verify each
line count and sha256 BEFORE use and report both readings; any mismatch stops the round. Apply
byte-exact, never by retyping.
  context.md            lines 42   sha256 de7b14f23f4d02a1b7f63619825fdc92d9cc2820fb34c5679dc6a9729697cab7
  decisions.md          lines 108  sha256 ff8495431423670d8e252268317ba8bb256f9a72a5ede5ce760fdea874895d0b
  ledger.md             lines 2    sha256 7df1a559e1883a3264368cf207dae9140115152eb1bef56b3a52d179127c870c
  live_review_head.md   lines 25   sha256 f6efff4df96f152de7d9b3ca8499e04b0498ca11447cd66df7903bf0fff73d0c
  plan.md               lines 44   sha256 8d2dee1aef97cbee6cb2305297505aec586e049a0ed6d13742d3704d06810758
  prose_slips.md        lines 1    sha256 d64a8b530e0c17dc134bcac5ad4b50857372e786d7b3ddf85f4a8f942eecbcab
  status_from.txt       lines 1    sha256 c5ee42e702947af43260a7c6e677bc3acd50d330af5e991b2fa54c8e6aa69b29
  status_to.txt         lines 1    sha256 eab31392224047db02b66dac1fb1ee9d918e9b8c9faaae39c5c0ecd9b88842b2
  block.md              this block; save it and report its line count and digest (R-0954)
CODE — ONE diff the reviewer produced in its own dry-run worktree at `f2494c02`, applied there,
tested there and red-proved there. Verify its digest, then apply it in TWO disjoint slices with
the `--include` lists below, always from its scratch path. Do not retype a hunk, do not edit one,
do not copy the diff into the repository, and never apply it whole — it is 557 insertions and the
AGENTS.md cap is 500, which is why the slices exist.
  `.remedy-wt/f277-r1-payloads/f277-r1.diff`
    lines 605  sha256 d57140c5bef3793424cd0276260e263dca39164b847a8be0896603c816dab4f2

SHAPE OF EACH STATE PAYLOAD, tested mechanically by the reviewer at `f2494c02`, one reading per
pair, the label derived from the output on the same line (item 15):
  `.agent/live_review.md` contains live_review_head.md — false, so REWRITE of the head
  `.agent/live_review.md` contains ledger.md — false, so APPEND
  `.agent/decisions.md` contains decisions.md — false, so APPEND
  `.agent/prose_slips.md` contains prose_slips.md — false, so APPEND
  `.agent/plan.md` contains plan.md — false, so REWRITE
  `.agent/context.md` contains context.md — false, so REWRITE
  status_to.txt contains status_from.txt — false, so REWRITE
Every pair reads false, so all are NEW bytes and no FROM-count proof is owed on any of them
beyond the STATUS anchor count below.

ANCHOR UNIQUENESS, measured by the reviewer at `f2494c02`: `status_from.txt`'s line occurs
exactly ONCE in `docs/roadmap/STATUS.md`, and the string `- [~]` occurs ZERO times there. Report
both counts yourself BEFORE replacing; any other reading stops the round.

ledger.md, decisions.md and prose_slips.md are APPEND-shaped. ledger.md and decisions.md each
begin with a newline, the blank separator their targets use between entries; prose_slips.md does
not, because that file is one line per slip. The live_review re-head is NOT an append:
`.agent/live_review.md` becomes live_review_head.md's bytes plus the old file's bytes from the
FIRST line that is exactly `## Findings` (inclusive) to the end, plus ledger.md's bytes. Match
that line as a whole line and take the FIRST such match — the substring `## Findings` also occurs
inside prose, both in the head payload and in the record, so a substring search finds the wrong
offset. Everything from that line onward is carried BYTE-IDENTICAL.

Bundle, in commit order
C1a the payload copies, ONE commit whose whole change set is new files under `.agent/authored/`:
   a byte copy of each payload listed above, `block.md` included, as
   `.agent/authored/f277-r1-<name>` — keeping each payload's own file name after the prefix, so
   `live_review_head.md` becomes `f277-r1-live_review_head.md`. The code diff is NOT copied and
   is NOT part of this or any commit. This block states no expected insertion count for this
   commit, because the commit copies THIS BLOCK and the count therefore moves with every edit to
   it (item 16, R-0656): the reviewer measured 452 insertions here while simulating the round.
   Report the number YOU read, and stop only if yours reaches 500.
C1b the claim and the booking, ONE commit: `.agent/plan.md` := plan.md; `.agent/context.md` :=
   context.md; `.agent/live_review.md` := the re-head described above; `.agent/decisions.md` :=
   its `f2494c02` bytes + decisions.md; `.agent/prose_slips.md` := its `f2494c02` bytes +
   prose_slips.md; `docs/roadmap/STATUS.md`: the line equal to status_from.txt replaced by
   status_to.txt. Expected insertions 178 by `git show --numstat`; report the number YOU read.
C2 the declaration —
   `git apply --include=packages/orchestration/event_names.py
    --include=packages/orchestration/run_log.py .remedy-wt/f277-r1-payloads/f277-r1.diff`
   then commit. Expected insertions 196; report the number YOU read.
C3 the test —
   `git apply --include=tests/orchestration/test_event_names.py
    --include=tests/orchestration/import_reachability_allowlist.txt
    .remedy-wt/f277-r1-payloads/f277-r1.diff`
   then commit. Expected insertions 361; report the number YOU read.
C4 handoff — rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the Session
   section reading "SESSION 1 of feature F277 · round 1 · rounds so far 1" plus ONE sentence of
   context self-assessment; the per-commit table with `git show --numstat` insertion counts for
   C1a, C1b, C2 and C3; every gate below with its real output and exit code, one line per gate;
   the open-findings count by distinct id; the item-status table; the deviations; and `## Next`
   naming Phase 1 rule 1, then the review of round 1, then round 2's disposal of the quarantined
   names, and "Operator questions open: <the count of `### Q` headings you read from
   `.agent/operator_questions.md`>". Then `git push -u origin feature/f277-machine-contracts`.
   Open NO pull request.

THE BRANCH. `feature/f277-machine-contracts` may ALREADY EXIST locally at `f2494c02`, created by
the refused first emission and never pushed. Check it out if it exists and create it from `main`
at `f2494c02` only if it does not; either way verify before C1a that the branch is checked out
and that it points at `f2494c02`. Do not delete it and do not recreate it.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as a deviation and
   applied anyway; it is never edited and no slice is retyped.
2. Change set: the paths the Bundle names, and nothing else. In particular do NOT edit
   `docs/roadmap/features/T2_F277.md` — DECISION F277 D2 amends T001's sequencing and the feature
   file's Built State is updated by round 2, the round that lands the disposal D2 describes.
3. The commit sequence is C1a, C1b, C2, C3, C4: no extra commit, none dropped, none reordered.
   C1b precedes C2 so that `.agent/plan.md` is current before the first product commit (item 23).
   C2 precedes C3, because the test imports the module C2 creates.
4. An insertion count is read with `git show --numstat`, whose `+` column is the reading DECISION
   F104 D1 fixes for the 500-line cap; `git commit`'s own terminal summary applies rename
   detection and is NOT that reading. Read it for EVERY commit, C1a and C1b included. If any
   commit reaches 500 insertions by that reading, STOP and report — no oversize exception is
   declared for this feature. The four expected values above are the reviewer's arithmetic; where
   yours differs, report YOURS and say so, and stop only if yours reaches 500.
5. Never force-push, never rewrite history, never delete a branch, never merge. Run NO `gh`
   command at all this round.
6. Read `.agent/STOP` from disk before the first commit. If it exists, write the handoff and end,
   doing nothing else.
7. The shell may deny `VAR=x cmd`, `cp` and some compound commands; copy bytes and read exit
   codes with small python scripts under `.remedy-wt/f277-r1-payloads/`. Prefer `git -C <path>`
   over `cd <path> && git`.
8. `.remedy-wt/` is gitignored scratch. Never run `git clean -x`.
9. Never weaken an assertion or delete a test. A red gate, or an ambiguity D1, D2 and D3 do not
   settle, stops the round: commit nothing half-done and report.
10. The full suite does NOT run this round (amend0917-throughput rule 1). It runs once per
    feature, in the closure sequence's integration-gate round.
11. Commit messages "F277 R1 C<n>: <summary>", a blank line, then
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when — the gates below, each EXECUTED, each reporting its REAL output and exit code.
"Green" as a word is a finding. G1 to G5 run at C3, before C4.

G1 TRANSPORT AND STATE. One python check printing an explicit True or False per reading.
   (a) Each `.agent/authored/f277-r1-*` file equals its payload on disk byte for byte. Report
       the number of such files YOU measured rather than taking a count from this block.
   (b) THE RECORD APPENDS, in full byte forensics, which the gate budget reserves for this file
       and for `.agent/decisions.md`. For `.agent/live_review.md` at C1b: reading (a), the file
       equals live_review_head.md's bytes plus the `f2494c02` bytes from the line `## Findings`
       inclusive to the end plus ledger.md's bytes; reading (b), an INDEPENDENT structural
       reader that splits the file on blank lines and compares its LAST N units, in order,
       against ledger.md's N paragraphs, where N is a number the script COUNTS from the payload
       and never one this block states; and a NEGATIVE CONTROL that flips one byte inside the
       FIRST appended paragraph and confirms BOTH readings reject it. Then the SAME three
       readings for `.agent/decisions.md` at C1b against its `f2494c02` bytes plus decisions.md.
   (c) Byte equality only: `.agent/plan.md` at C1b equals plan.md's bytes; `.agent/context.md`
       at C1b equals context.md's bytes; `.agent/prose_slips.md` at C1b equals its `f2494c02`
       bytes plus prose_slips.md's bytes; `docs/roadmap/STATUS.md` at C1b equals its `f2494c02`
       bytes with the one pair applied.
   Report the number of readings taken and that every one is True. SEPARATELY, report the SAVED
   BLOCK's own line count and sha256 beside the line count and digest this block's PAYLOADS
   section gives for `block.md` (R-0954).

G2 CODE TRANSPORT — the committed tree is the tree the reviewer tested, and this gate is the
   ONLY proof the diff arrived intact, since no copy of it is committed. At C3:
     git rev-parse <C3>:packages <C3>:tests
   must print exactly
     58f6bbd055c1e25d9dfc32263a14adf93079b45d
     a781a46d213ed4447075a50a9e89fc3823c53bd8
   and
     git rev-parse <C3>:packages/orchestration/event_names.py
                   <C3>:packages/orchestration/run_log.py
                   <C3>:tests/orchestration/test_event_names.py
                   <C3>:tests/orchestration/import_reachability_allowlist.txt
   must print exactly
     3c519bdea8ff4be676541aec2a141d55b4c51fcb
     a17a20f3e93112b4579604cd2efe2d3df0c7005d
     b789385fa3b5ecd83cda4658c7eb46f29e28ea97
     e4791c40af0b95f2f986b812a388ba6bc70bc2e8
   Also report `git diff --name-only <C1b> <C3>` in full: it must name exactly the four paths C2
   and C3 name and no other. Report that list and its length.

G3 THE TARGETED SUITE, in the primary checkout, serial (no `-n`):
     python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_event_names.py
       tests/test_run_log.py tests/orchestration/test_import_reachability.py
       tests/test_no_orphan_modules.py tests/orchestration/test_dead_command_check.py
       tests/test_autonomy_readiness.py tests/test_memory_learn.py tests/docs
       tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py
   Report the summary line and the exit code. It must read 0 failed at exit 0. `tests/docs` and
   `tests/orchestration/test_roadmap_index.py` are in the list because C1b edits
   `docs/roadmap/STATUS.md`; `tests/cli/test_golden_path.py` is the canary.

G4 LINT:
     python3 -m ruff check packages/orchestration/event_names.py
       packages/orchestration/run_log.py tests/orchestration/test_event_names.py
   must print "All checks passed!". Pass ONLY these three paths — the allowlist is a `.txt` file
   and ruff parses it as Python if you hand it over, which reports hundreds of false errors.

G5 MUTATION RED-PROOFS, in ONE disposable worktree under `.remedy-wt/` created at C3 and removed
   as this gate's last action. Run every command from the worktree root with
   `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_event_names.py`.
   Take the UNMUTATED CONTROL FIRST and report its exit code: it must be 0. Then apply each
   mutation below, one at a time, each restored byte-identically before the next; before each,
   COUNT the mutated bytes in the named file and report the count, which must be 1. Report each
   run's exit code and its failing node ids, and report a mutation that stays green AS GREEN.
   (a) In `packages/orchestration/autonomy_loop.py`, insert directly above the line
       `def _emit_token_policy_applied(job: JobPlan) -> None:` a function
       `def _reader_for_a_name_nothing_writes(e: dict) -> bool:` whose body is
       `    return e.get("event") == "f277_red_proof_unwritten_name"`, followed by two blank
       lines. Expected: FAIL, naming `test_every_read_event_name_is_declared`.
   (b) In `packages/orchestration/event_names.py`, delete the single line
       `        "task_run_started",`. Expected: FAIL, naming
       `test_every_written_event_name_is_declared`.
   (c) In `packages/orchestration/run_log.py`, delete the two lines
       `        if os.environ.get(STRICT_EVENT_NAMES_ENV) == "1":` and
       `            assert_declared_event(event)`. Expected: FAIL, naming
       `test_the_writer_rejects_an_undeclared_name_under_the_flag`.
   (d) In `packages/orchestration/autonomy_loop.py`, insert directly above the same
       `def _emit_token_policy_applied(job: JobPlan) -> None:` line a function
       `def _writer_for_a_quarantined_name(log) -> None:` whose body is
       `    log.log("worker_adapters_listed")`, followed by two blank lines. Expected: FAIL,
       naming `test_a_read_only_name_that_gains_a_writer_leaves_the_quarantine`.
   After the four, show that each of the three touched files is byte-identical to before (report
   a sha256 per file), remove the worktree, and report `git worktree list` in full.

G6 PUSH AND TREE. `git push -u origin feature/f277-machine-contracts` after C4; then
   `git status --porcelain`, which must be EMPTY; then `ls .agent/STOP`, which must be absent;
   then `git worktree list` in full. Run no `gh` command. These readings necessarily POSTDATE
   the commit that writes the handback, so they belong to your final report and not to the
   handoff's own text (item 31).

Handback
Rewrite `.agent/handoff.md` as C4 describes, then report. The handback names every gate with one
line of its real output, declares every deviation, and carries the item-status table. If any gate
is red, say so plainly WITH the output: a red gate honestly reported ends the round cleanly and
is worth far more than a green word.
