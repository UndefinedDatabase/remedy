STEP closure part five — F276 Data-root hygiene & disk budget, ROUND 12

This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 11's verdict, correct one false clause the round 10 entry left in the
ledger, and then BUILD THE CLOSURE EVIDENCE: the integrity check, the evidence
job, and a fresh review package from a clean tree at this round's own handback
commit. Report the package's filename, its SHA-256 and its archived path. This
round writes NO STATUS line, NO README edit, NO `consumed_by` and opens NO pull
request — the reviewer authors the STATUS line from the values this round
measures, and the closure round applies it. DECISION F276 D11 records why the
closure is two rounds.

Bundle, in commit order
C1 the bookkeeping, in ONE commit: the payload copies under `.agent/authored/`,
   the ledger append, the prose-slip append and the plan rewrite.
C2 the handoff.
Then, AFTER C2 and with the tree clean, and committing nothing: the integrity
check, the evidence job and the review package.

Payloads on disk
Every authored text of this round is a FILE the worker reads from disk. Nothing
is retyped. Each is named with its line count and its sha256; the worker
verifies BOTH readings BEFORE using the file and reports them.

P1 `.remedy-wt/f276-r12/block.md` — this block.
   the line count and digest are in the delegation message that names this file.
P2 `.remedy-wt/f276-r12/ledger.md`
   lines 2; sha256 65a1eced7d05643184c4030dd8043b71a5fd7bea022590462cd46e52f8daf05b
P3 `.remedy-wt/f276-r12/plan.md`
   lines 49; sha256 015b73764077a69ae7c7b5e1fb1862af50bfba967a7721bb6387269de0658cdd
P4 `.remedy-wt/f276-r12/prose_slips.md`
   lines 2; sha256 0183f995c9400e366c261db802b25ba7c544b2d95de1dfccffff094e25073ba3
P5 `.remedy-wt/f276-r12/create_f276_evidence.py`
   lines 147; sha256 6c4b1d91a30557a586ac7e4ade05840b07092f80475264392937d61195f46608

P2 and P4 are APPEND-shaped: each is concatenated onto the end of its target,
whose current bytes end with a newline, so the result is the target's bytes
followed by the payload's bytes and nothing else. P2 begins with a newline, the
blank separator its target's entries use; P4 does not, because
`.agent/prose_slips.md` is one line per slip. P3 is a REWRITE: `.agent/plan.md`
becomes exactly P3's bytes.

Containment test, run mechanically by the reviewer at `7625d967`, one reading
per pair, the label derived from the output on the same line (item 15):
  `.agent/live_review.md` contains P2 — false, so APPEND
  `.agent/prose_slips.md` contains P4 — false, so APPEND
  `.agent/plan.md` contains P3 — false, so REWRITE
Every pair above reads false, so all are NEW bytes and no FROM-count proof is
owed on any of them.

P5 is a SCRIPT, not a slice bound for a tracked file. It is run from the
repository root and it writes only under `.remedy-wt/`, which is gitignored. It
is NEVER committed, never copied into `.agent/authored/` and never edited.

Change set — exactly these paths, and nothing else this round
  .agent/authored/f276-r12-block.md        (new, C1)
  .agent/authored/f276-r12-ledger.md       (new, C1)
  .agent/authored/f276-r12-plan.md         (new, C1)
  .agent/authored/f276-r12-prose-slips.md  (new, C1)
  .agent/live_review.md                    (C1 append)
  .agent/prose_slips.md                    (C1 append)
  .agent/plan.md                           (C1 rewrite)
  .agent/handoff.md                        (C2)

C1 — the bookkeeping
Copy P1 to `.agent/authored/f276-r12-block.md`, P2 to `-ledger.md`, P3 to
`-plan.md`, P4 to `-prose-slips.md`, each with `shutil.copyfile`, never by
retyping. Append P2's bytes to `.agent/live_review.md`; append P4's bytes to
`.agent/prose_slips.md`; write P3's bytes over `.agent/plan.md`. Commit.

What P2 books: round 11's verdict, PASS, together with a CORRECTION to the
round 10 entry, appended rather than written over it, because that record is
append-only. What P4 appends: two dated lines for two of the reviewer's own
authoring defects in round 11.

THE INSERTION CAP, computed here rather than asserted, because round 11 spent a
declared deviation on a cap the block had not added up. The copies are P1 plus
P2 at 2, P3 at 49 and P4 at 2; the appends are P2's 2 and P4's 2; the rewrite is
P3's 49. P5 is not copied and not committed, so its 147 lines are not in this
commit at all. The sum is therefore this block's own line count plus 106, and
this block is under 250 lines, so C1 lands comfortably below 500. THE AGENTS.md
OVERSIZE EXCEPTION IS ALREADY SPENT by `c6a519d1` and is NOT available to this
round: a second oversize commit in this feature would be a Medium finding. If
your measured count nevertheless reaches 500, STOP and report rather than
committing.

C2 — the handoff
Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the SESSION
NUMBER (this is SESSION 3 of F276), the round, the branch, the per-commit table
with `git show --numstat` insertions for C1, every gate below with its real
output and exit code, the open-findings count by both readings, the item-status
table, the deviations, and the next expected action. One sentence of context
self-assessment. No length cap.

IT CANNOT CARRY THE PACKAGE'S NAME OR HASH, because the package is built after
it by construction, and it says so in one sentence rather than leaving the
absence to be read as an omission. The package's readings go to the reviewer in
this round's report and to `.remedy-wt/f276-r12/package.txt` on disk; the
closure round records them durably in the STATUS line and in its own handoff.

After C2, the tree is clean and the branch is pushed. Everything below commits
nothing.

THE INTEGRITY CHECK — closure precondition 3

  python3 -m apps.cli.main integrity check --json

Report the WHOLE JSON and its exit code. `passed` must be true. Every one of its
checks is EXPECTED to read `pass`, including `live_review_verdict`: the reviewer
ran this command at `512ba69c` and read `passed: true` with five checks and a
zero fail count. A `fail` on any check, or a non-empty `relevant_untracked`,
stops the round and is reported rather than repaired.

THE EVIDENCE JOB — closure protocol step 1

  python3 .remedy-wt/f276-r12/create_f276_evidence.py

It resolves the committed review subject between the FORK POINT
`43d148177efd145f179ba2d9875eaa675b1595b7` and the tree at C2, collects its node
ids with `--collect-only`, runs those six test files, and writes the full
closed-schema gate set into `.remedy-wt/f276_evidence_closure/`. The reviewer
collected those same six files at `512ba69c` and read 112 node ids. Report the
script's stderr in full — the collected node-id count, the test result line, the
`is_valid_current_run` reading and the `validation_errors` list — and the summary
dict it prints on stdout. `validation_errors` must be EMPTY. If it is not, STOP:
do not edit the script, do not hand-write a gate file, do not proceed to the
package. Report the errors verbatim; repairing them is the reviewer's to author.

THE REVIEW PACKAGE — closure protocol step 2, MANDATORY and never skipped

  git status --porcelain
  bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f276_evidence_closure

The tree must be clean before the build; report that reading first. Then report
the package's FILENAME, its SHA-256 exactly as the script prints them, the
script's exit code, and the manifest's `committed_review_subject` base and head
commits, which must be that same fork point and the sha of C2. Finally report
the package's ARCHIVED PATH per DECISION amend0827 D1: the absolute directory it
ended up in, or the literal `NOT ARCHIVED` when it was left where it was built.
Do not move it; just say where it is.

Write those four readings — filename, SHA-256, archived path, accepted HEAD —
into `.remedy-wt/f276-r12/package.txt`, one per line, and quote the file in your
report. A FAILING PACKAGE BUILD IS A CLOSURE BLOCKER: report the raw error and
stop, never a partial or hand-assembled package.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as
   a deviation and applied anyway; it is never edited and no slice is retyped.
2. Touch no path outside the change set above. In particular: do not edit
   `docs/roadmap/STATUS.md`, `README.md`, `docs/roadmap/features/T2_F276.md`,
   `scripts/self_use_queue.json` or `.agent/candidates.md` — every one of those
   belongs to the closure round.
3. The commit sequence is C1 then C2, no extra commit, none dropped, none
   reordered. Nothing after C2 commits anything; if any step after C2 leaves a
   tracked file modified, that is a finding and is reported rather than
   committed away.
4. No destructive verification is ordered, so create no disposable worktree. The
   two job worktrees under `.remedy-wt/` are jobs'; leave them.
5. Never force-push, never rewrite history, never delete a branch, never merge,
   never open or edit a pull request, never run any `gh` command. Work only on
   `feature/f276-data-root-hygiene`.
6. Read `.agent/STOP` from disk before the first commit. If it exists, write the
   handoff and end, doing nothing else.
7. The full suite does NOT run this round. It ran once on the merged tree in
   round 11 and its green transcript is committed at `3359296e`; re-running it
   here would spend four minutes to learn nothing, and closure precondition 2 is
   satisfied by READING that transcript.
8. `.remedy-wt/` is gitignored scratch holding this round's payloads and round
   10's and round 11's. Never run `git clean -x`.

Done when — the gates below, each executed, each reporting its REAL output and
exit code. "Green" as a word is a finding.

G1 TRANSPORT AND STATE, at C1. One python check printing an explicit True or
   False per reading.
   (a) Each `.agent/authored/f276-r12-*` file the change set names equals its
       payload on disk byte for byte. Report the number of such files YOU
       measured rather than taking a count from this block.
   (b) THE RECORD APPEND, in full byte forensics, which the gate budget reserves
       for this file. For `.agent/live_review.md`: reading (a), the file at C1
       equals its `7625d967` bytes plus P2's bytes; reading (b), an INDEPENDENT
       structural reader that splits the file at C1 on blank lines and compares
       its LAST N units, in order, against P2's N paragraphs, where N is a number
       the script COUNTS from the payload and never one this block states; and a
       NEGATIVE CONTROL that flips one byte inside the FIRST appended paragraph
       and confirms that BOTH readings reject it.
   (c) `.agent/prose_slips.md` at C1 equals its `7625d967` bytes plus P4's
       bytes; `.agent/plan.md` at C1 equals P3's bytes. Byte equality only —
       these are prose files and the gate budget gives them no arithmetic.
   Report the number of readings taken and that every one is True.
   SEPARATELY, report the SAVED BLOCK's own line count and sha256 beside the
   line count and digest the delegation message gave for P1 (R-0954).

G2 THE INTEGRITY CHECK. Report the whole JSON and its exit code, and state
   `passed` and the per-check status list explicitly.

G3 THE BASE COMMIT, before the evidence job — closure pitfall (e), which this
   branch's merge has made live. At the commit C2 creates, report all four
   readings: `git merge-base main <that commit>`; the first commit of
   `git rev-list --first-parent <that commit>` that `git rev-list main` also
   holds; and the LENGTHS of `git rev-list --ancestry-path <base>..<that commit>`
   and `git rev-list <base>..<that commit>`. The FIRST reading is EXPECTED to
   answer main's tip `8f129d71e311ccd58bdb01d63c78bb75dffbd382` and NOT the base.
   The SECOND must answer `43d148177efd145f179ba2d9875eaa675b1595b7`, and the two
   LENGTHS must be EQUAL to each other. State the base at full forty characters
   and confirm it is the sha P5 carries.

G4 THE EVIDENCE JOB. Report the collected node-id count, the test result line
   and exit code, `is_valid_current_run`, and `validation_errors`, which must be
   an empty list. Report the summary dict's final verdict field.

G5 THE PACKAGE. Report `git status --porcelain` before the build (empty), the
   script's exit code, the package filename, its SHA-256, the manifest's
   `committed_review_subject` base and head, the archived path, and
   `git status --porcelain` again AFTER the build, which must still be empty
   because `remedy-review-*` is gitignored. Quote
   `.remedy-wt/f276-r12/package.txt`.

G6 PUSH AND TREE. `git push origin feature/f276-data-root-hygiene` after C2;
   then `git status --porcelain`, which must be EMPTY; then `ls .agent/STOP`,
   which must be absent; then `git worktree list` in full, reported as a
   measurement.

Handback
Rewrite `.agent/handoff.md` as C2 describes, then report. The handback names
every gate with one line of its real output, declares every deviation, and
carries the item-status table. The package's four readings go in your REPORT to
the reviewer and in `.remedy-wt/f276-r12/package.txt`; the handoff says they
exist and where, and does not invent them. If any gate is red, say so plainly
with the output — a red gate honestly reported ends the round cleanly.
