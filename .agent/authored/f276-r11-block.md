STEP closure part four — F276 Data-root hygiene & disk budget, ROUND 11

This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book the verdicts of rounds 9 and 10, record DECISIONs F276 D11 and D12 and the
operator question D12 answers, and then RE-RUN THE INTEGRATION GATE ONCE on the
merged tree, committing its transcript over
`.agent/authored/f276-closure-suite.txt` in place. This round writes NO STATUS
line, NO README edit, NO `consumed_by`, builds NO evidence job, builds NO
package and opens NO pull request — those are the two rounds after it.

WHY THIS ROUND EXISTS AT ALL, because it was not in round 10's plan. After round
10 ended on the STOP sentinel the operator merged `origin/main` into this branch
at `512ba69c`. The transcript closure precondition 2 reads by name was committed
at `fd23710f` and records 17659 test outcomes; at `512ba69c` the reviewer's own
`python3 -m pytest -q --collect-only` reads 17740 tests collected. The committed
transcript therefore describes a tree that no longer exists, and 81 tests on the
branch were never in it. DECISION F276 D12, which payload P3 carries, rules the
re-run and gives the full reasoning; this block executes it.

Bundle, in commit order
C1 the bookkeeping, in ONE commit: the five payload copies under
   `.agent/authored/`, the ledger append, the decisions append, the prose-slip
   append, the plan rewrite and the operator-questions rewrite.
C2 the integration-gate transcript, replacing the closure-suite file in place.
C3 the handoff.

Payloads on disk
Every authored text of this round is a FILE the worker reads from disk. Nothing
is retyped. Each is named with its line count and its sha256; the worker
verifies BOTH readings BEFORE using the file and reports them.

P1 `.remedy-wt/f276-r11/block.md` — this block.
   the line count and digest are in the delegation message that names this file.
P2 `.remedy-wt/f276-r11/ledger.md`
   lines 4; sha256 5fa2784e5a201b74e69a938df8ec713d277a9e93f8a69a398a6c475d7cbf5426
P3 `.remedy-wt/f276-r11/decisions.md`
   lines 136; sha256 a9a39be4be5b7fc4ff1f11d19d9a84cec233631e8ea0aab77e8a3aca9f66b404
P4 `.remedy-wt/f276-r11/plan.md`
   lines 47; sha256 672f83d95c5d538e2888c87dbb29d7f599ef6ed08f6e6badf5b829db192bda73
P5 `.remedy-wt/f276-r11/prose_slips.md`
   lines 1; sha256 7ab1117ffe690970bef04e8a34b032143d2dd2d01f581f63886b846f2ef60abe
P6 `.remedy-wt/f276-r11/operator_questions.md`
   lines 39; sha256 25a621db2dfffb974617fa0a04eb5d824410f34b3646cfa87e7602cdce077e4d

P2, P3 and P5 are APPEND-shaped: each is concatenated onto the end of its
target, whose current bytes end with a newline, so the result is the target's
bytes followed by the payload's bytes and nothing else. P2 and P3 each begin
with a newline, the blank separator their targets' entries use; P5 does not,
because `.agent/prose_slips.md` is one line per slip. P4 and P6 are REWRITES:
each target becomes exactly its payload's bytes.

Containment test, run mechanically by the reviewer at `512ba69c`, one reading
per pair, the label derived from the output on the same line (item 15):
  `.agent/live_review.md` contains P2 — false, so APPEND
  `.agent/decisions.md` contains P3 — false, so APPEND
  `.agent/prose_slips.md` contains P5 — false, so APPEND
  `.agent/plan.md` contains P4 — false, so REWRITE
  `.agent/operator_questions.md` contains P6 — false, so REWRITE
Every pair above reads false, so all are NEW bytes and no FROM-count proof is
owed on any of them.

P6 preserves its target's header byte for byte and replaces only the line
reading `EMPTY — nothing is waiting on the operator.` with the Q1 entry; the
reviewer built it from the target's own bytes rather than by retyping the
header.

Change set — exactly these paths, and nothing else this round
  .agent/authored/f276-r11-block.md              (new, C1)
  .agent/authored/f276-r11-ledger.md             (new, C1)
  .agent/authored/f276-r11-decisions.md          (new, C1)
  .agent/authored/f276-r11-plan.md               (new, C1)
  .agent/authored/f276-r11-prose-slips.md        (new, C1)
  .agent/authored/f276-r11-operator-questions.md (new, C1)
  .agent/live_review.md                          (C1 append)
  .agent/decisions.md                            (C1 append)
  .agent/prose_slips.md                          (C1 append)
  .agent/plan.md                                 (C1 rewrite)
  .agent/operator_questions.md                   (C1 rewrite)
  .agent/authored/f276-closure-suite.txt         (C2 rewrite)
  .agent/handoff.md                              (C3)

C1 — the bookkeeping
Copy P1 to `.agent/authored/f276-r11-block.md`, P2 to `-ledger.md`, P3 to
`-decisions.md`, P4 to `-plan.md`, P5 to `-prose-slips.md` and P6 to
`-operator-questions.md`, each with `shutil.copyfile`, never by retyping.
Append P2's bytes to `.agent/live_review.md`; append P3's bytes to
`.agent/decisions.md`; append P5's bytes to `.agent/prose_slips.md`; write P4's
bytes over `.agent/plan.md`; write P6's bytes over `.agent/operator_questions.md`.
Commit.

What P2 books: round 9's verdict PASS, byte-verbatim from the payload round 10
was given and never applied, and round 10's verdict PASS, newly authored. What
P3 appends: DECISION F276 D11, which rules the two-round closure, and DECISION
F276 D12, which rules the integration-gate re-run this round performs. What P5
appends: one dated line for the reviewer's unbounded count gate of round 9. What
P6 writes: operator question Q1, which D12 answers in advance under operator
amendment amend0917-throughput rule 5 — the entry never stalls the round.

C2 — the integration gate, and its transcript

Run in the PRIMARY checkout `/home/decodeux/Repos/remedy`, never a worktree,
which lacks the UI dependencies. BUILD `apps/ui` FIRST and report that build's
exit code and last line: a cold `apps/ui/dist` makes the UI server's start path
auto-build while the xdist workers are already running, and that race is what
reddened three `tests/ui_server/` nodes in round 7. Then, from the repository
root, after C1 is committed and with the tree otherwise clean:

  python3 -m pytest -n auto -q

ONCE. Take the exit code from the process object, never from a pipeline, which
would report the exit code of the last stage instead. Write the transcript over
`.agent/authored/f276-closure-suite.txt` — the same path, replaced in place, as
round 8 did — and commit it as C2 with that one path as its whole change set.

The transcript states, each as a real reading:
  the command, the working directory and the commit C1 created;
  the `apps/ui` build's exit code and last line;
  the summary line verbatim, and the exit code;
  the BAD NODE IDS — failed plus errors — found by searching the captured
    output mechanically for a FAILURES section, an ERRORS section and any line
    beginning FAILED or ERROR, rather than read off the summary; where the set
    is empty it says so and says how it was searched;
  the SUPERSEDED run, so both resolve from this one file: the `fd23710f`
    transcript's summary `17639 passed, 20 skipped` for 17659 outcomes, and its
    empty bad set;
  the RECONCILIATION that is this round's whole reason: the superseded run's
    17659 outcomes against this run's own outcome total, with the difference
    stated and attributed to the merge at `512ba69c`;
  the wall clock measured around the process;
  and the outcome of the golden-path nodes `tests/cli/test_golden_path.py`,
    named explicitly, which is where this round's canary reading lives.

IF THE RUN IS RED, that is not a failure of this round: record the bad set in
the transcript, commit C2 and C3 exactly as ordered, and report it. Do NOT
repair a test, weaken an assertion, mark anything xfail or re-run to get a
different answer. The bad set is the reading the next round is authored from,
under operator amendment amend0917-throughput rule 2, and this feature has two
of its three repair rounds unspent.

C3 — the handoff
Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the SESSION
NUMBER (this is SESSION 3 of F276), the round, the branch, the per-commit table
with `git show --numstat` insertions for C1 and C2, every gate below with its
real output and exit code, the open-findings count by both readings, the
item-status table, the deviations, and the next expected action. One sentence of
context self-assessment. No length cap.

The handback commit's own insertion count and the push that follows it cannot be
quoted by the file being written, so they go nowhere: the reviewer measures them
at the next gate and records them in that round's ledger entry (item 31).

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as
   a deviation and applied anyway; it is never edited and no slice is retyped.
2. Touch no path outside the change set above. In particular: do not edit
   `docs/roadmap/STATUS.md`, `README.md`, `docs/roadmap/features/T2_F276.md`,
   `scripts/self_use_queue.json` or `.agent/candidates.md` — every one of those
   belongs to the closure round.
3. The commit sequence is C1, C2, C3, no extra commit, none dropped, none
   reordered. C2 and C3 write only under `.agent/`, so neither can change a test
   outcome, which is why the transcript names the commit C1 created as the state
   it describes.
4. C1's insertion count, by `git show --numstat`, stays under 500; report it.
   C2's and C3's belong to their own readings.
5. No destructive verification is ordered, so create no disposable worktree. The
   two job worktrees under `.remedy-wt/` are jobs'; leave them.
6. Never force-push, never rewrite history, never delete a branch, never merge,
   never open or edit a pull request, never run any `gh` command. Work only on
   `feature/f276-data-root-hygiene`.
7. Read `.agent/STOP` from disk before the first commit. If it exists, write the
   handoff and end, doing nothing else.
8. `.remedy-wt/` is gitignored scratch that holds round 10's intact payloads as
   well as this round's. Never run `git clean -x`.

Done when — the gates below, each executed, each reporting its REAL output and
exit code. "Green" as a word is a finding.

G1 TRANSPORT AND STATE, at C1. One python check printing an explicit True or
   False per reading.
   (a) Each `.agent/authored/f276-r11-*` file the change set names equals its
       payload on disk byte for byte. Report the number of such files YOU
       measured rather than taking a count from this block.
   (b) THE RECORD APPENDS, in full byte forensics, which the gate budget
       reserves for exactly these two files. For `.agent/live_review.md` and for
       `.agent/decisions.md` separately: reading (a), the file at C1 equals its
       `512ba69c` bytes plus the payload's bytes; reading (b), an INDEPENDENT
       structural reader that splits the file at C1 on blank lines and compares
       its LAST N units, in order, against the payload's N paragraphs, where N
       is a number the script COUNTS from the payload and never one this block
       states; and a NEGATIVE CONTROL that flips one byte inside the FIRST
       appended paragraph and confirms that BOTH readings reject it.
   (c) `.agent/prose_slips.md` at C1 equals its `512ba69c` bytes plus P5's
       bytes; `.agent/plan.md` at C1 equals P4's bytes; `.agent/operator_questions.md`
       at C1 equals P6's bytes. Byte equality only — these are prose files and
       the gate budget gives them no arithmetic.
   Report the number of readings taken and that every one is True.
   SEPARATELY, report the SAVED BLOCK's own line count and sha256 beside the
   line count and digest the delegation message gave for P1 (R-0954).

G2 THE UI BUILD, before the suite starts. Report the command, its exit code and
   its last line, and `git status --porcelain` after it, which must be EMPTY
   because `apps/ui/dist` is gitignored. A non-zero exit stops the round and is
   reported; do not start the suite over a failed build.

G3 THE INTEGRATION GATE. Report the exact command, the exit code taken from the
   process object, the summary line verbatim, the wall clock, and the BAD NODE
   IDS as a list — empty or not — with the method used to search for them. State
   this run's outcome total and the superseded run's 17659 side by side, and the
   difference between them. Report the golden-path nodes' outcome by name.

G4 THE BASE COMMIT AND THE FORK POINT — closure pitfall (e), which this branch's
   merge has made live. At the commit C1 created, report all four readings:
   `git merge-base main <that commit>`; the first commit of
   `git rev-list --first-parent <that commit>` that `git rev-list main` also
   holds; and the LENGTHS of `git rev-list --ancestry-path <base>..<that commit>`
   and `git rev-list <base>..<that commit>`. The FIRST reading is EXPECTED to
   answer main's tip `8f129d71e311ccd58bdb01d63c78bb75dffbd382` and NOT the base
   — that divergence is the whole of pitfall (e) and its absence would be the
   surprise. The SECOND must answer `43d148177efd145f179ba2d9875eaa675b1595b7`,
   and the two LENGTHS must be EQUAL to each other. State the base at full forty
   characters. Report the readings even if one surprises you; do not adjust one
   to match this text.

G5 THE OPEN SET, at C1. Derive it mechanically from `.agent/live_review.md`:
   every `^- R-\d+` registration minus every `^Done: R-\d+` resolution, counted
   BY DISTINCT ID and not by line. Report the count, the ids in ascending order,
   and the count of those ids carrying the string
   `Owner: F282 — Findings paydown v2`. This round registers and resolves
   nothing, so the count must be IDENTICAL at `512ba69c` and at C1; report both
   and state whether they are equal.

G6 PUSH AND TREE. `git push origin feature/f276-data-root-hygiene` after C3;
   then `git status --porcelain`, which must be EMPTY; then `ls .agent/STOP`,
   which must be absent; then `git worktree list` in full, reported as a
   measurement. These readings necessarily POSTDATE the commit that writes the
   handback, so they belong to the round report and not to the handoff's own
   text; the reviewer re-takes them at the next gate (item 31).

Handback
Rewrite `.agent/handoff.md` as C3 describes, then report. The handback names
every gate with one line of its real output, declares every deviation, and
carries the item-status table. If any gate is red, say so plainly with the
output — a red gate honestly reported ends the round cleanly, and for G3 in
particular a red suite is a reading this round is entitled to produce.
