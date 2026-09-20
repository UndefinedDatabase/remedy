STEP closure part six — F276 Data-root hygiene & disk budget, ROUND 13

This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 12's verdict, register `R-1010`, REPAIR it, resolve it, and then
build the closure evidence round 12 could not: the integrity check, the
evidence job, and a fresh review package from a clean tree at this round's own
handback commit. Report the package's filename, its SHA-256 and its archived
path. This round writes NO STATUS line, NO README edit, NO `consumed_by` and
opens NO pull request — those belong to the closure round.

WHY THIS ROUND IS A REPAIR ROUND. Round 12's evidence job raised
`ValueError: T002: safe-diff path set does not match the task partition`.
The reviewer reproduced it and traced it to one cause, registered as `R-1010`
in payload P2: `parse_safe_diff_paths` recovers a path only from a `+++ b/<path>`
line, and git writes no `+++` line for a diff entry with no hunks. The operator's
merge at `512ba69c` brought in `packages/providers/claude_planner/__init__.py`,
an EMPTY added file, so the producer wrote a path into a task's `changed_files`
that its own reader could not read back. Until that reader is widened, NO review
package can be built for this branch, and the closure protocol calls a failing
package build a closure BLOCKER. The repair is P5; the tests that prove it are
P6; the reviewer has already applied and run both, and what it measured is in
the gates below as the numbers YOUR run must reproduce.

Bundle, in commit order
C1 the bookkeeping, in ONE commit: the payload copies under `.agent/authored/`,
   the ledger append that books round 12 and registers `R-1010`, the prose-slip
   append and the plan rewrite.
C2 the repair, in ONE commit: `packages/orchestration/repair_attest.py` and
   `tests/orchestration/test_repair_attest.py`, and nothing else.
C3 the resolution: the `Done: R-1010` append, which states what C2 landed and
   is therefore committed AFTER C2 and never before it.
C4 the handoff.
Then, AFTER C4 and with the tree clean, and committing nothing: the integrity
check, the evidence job and the review package.

Payloads on disk
Every authored text of this round is a FILE the worker reads from disk. Nothing
is retyped. Each is named with its line count and its sha256; the worker
verifies BOTH readings BEFORE using the file and reports them.

P1 `.remedy-wt/f276-r13/block.md` — this block.
   the line count and digest are in the delegation message that names this file.
P2 `.remedy-wt/f276-r13/ledger.md`
   lines 4; sha256 77774dbee01fc24d35869ee7c96d0d30cfc0de65d058d19ebc474057b76a0c41
P3 `.remedy-wt/f276-r13/plan.md`
   lines 49; sha256 7adab1f8aab9a688cb6758c2d63c0070c2652c7ef2b84017d1a363dc6024609c
P4 `.remedy-wt/f276-r13/prose_slips.md`
   lines 1; sha256 7beaa26d2add5c290e94ee9fd91f081a5a23ed8527dee1e93339a45025770e7e
P5 `.remedy-wt/f276-r13/repair_attest.py`
   lines 156; sha256 7811676fd35f45d1885cbc2739cf7c9d73001ef919ccd17be657bbedee85750d
P6 `.remedy-wt/f276-r13/test_repair_attest.py`
   lines 279; sha256 29b69d42eb2bf94d54a369826da23c756b8876c08861ed31bbed9dd4ae089418
P7 `.remedy-wt/f276-r13/ledger_done.md`
   lines 2; sha256 017e406ae83eb4390cdbe086d57930a344aae0ecebc0a2f3fe054a5ea7f98669
P8 `.remedy-wt/f276-r13/create_f276_evidence.py`
   lines 147; sha256 37e1660e41ed8beb8b89247b77b2140f8d56ca232598bb56a6faa578cc14d378

P2, P4 and P7 are APPEND-shaped: each is concatenated onto the end of its
target, whose current bytes end with a newline, so the result is the target's
bytes followed by the payload's bytes and nothing else. P2 and P7 each begin
with a newline, the blank separator `.agent/live_review.md` uses between
entries; P4 does not, because `.agent/prose_slips.md` is one line per slip. P3,
P5 and P6 are REWRITES: each target becomes exactly its payload's bytes.

Containment test, run mechanically by the reviewer at `b8ecbb7a`, one reading
per pair, the label derived from the output on the same line (item 15):
  `.agent/live_review.md` contains P2 — false, so APPEND
  `.agent/live_review.md` contains P7 — false, so APPEND
  `.agent/prose_slips.md` contains P4 — false, so APPEND
  `.agent/plan.md` contains P3 — false, so REWRITE
  `packages/orchestration/repair_attest.py` contains P5 — false, so REWRITE
  `tests/orchestration/test_repair_attest.py` contains P6 — false, so REWRITE
Every pair above reads false, so all are NEW bytes and no FROM-count proof is
owed on any of them.

P5 AND P6 ARE WHOLE-FILE REWRITES OF PRODUCTION AND TEST FILES, and that is
deliberate: a whole file cannot be mis-anchored, and the gate below proves the
change is confined by reading the DIFF rather than by trusting the write. The
reviewer measured both diffs against `b8ecbb7a`: P5 adds 54 lines and deletes
none, P6 adds 78 lines and deletes none, and P6's addition is one contiguous
block at the end of its file. Neither payload removes an existing test.

P5 AND P6 GET NO COPY UNDER `.agent/authored/`, and this is a reasoned
departure from the other payloads rather than an omission. Those two land
BYTE-IDENTICAL in the work tree at C2, so the committed target file IS the
saved copy: the comparison a copy would license — reviewer's scratch original
against a committed artefact — is exactly what G1(c) runs against the target
itself, and a second copy would prove the same equality twice while adding 435
lines to C1. The AGENTS.md oversize exception is already spent by `c6a519d1`
and constraint 4 forbids a second, so the duplicate is not merely redundant
here, it is unaffordable.

P8 is a SCRIPT, not a slice bound for a tracked file. It is run from the
repository root and it writes only under `.remedy-wt/`, which is gitignored. It
is NEVER committed, never copied into `.agent/authored/` and never edited.

Change set — exactly these paths, and nothing else this round
  .agent/authored/f276-r13-block.md          (new, C1)
  .agent/authored/f276-r13-ledger.md         (new, C1)
  .agent/authored/f276-r13-plan.md           (new, C1)
  .agent/authored/f276-r13-prose-slips.md    (new, C1)
  .agent/authored/f276-r13-ledger-done.md    (new, C1)
  .agent/live_review.md                      (C1 append, C3 append)
  .agent/prose_slips.md                      (C1 append)
  .agent/plan.md                             (C1 rewrite)
  packages/orchestration/repair_attest.py    (C2 rewrite)
  tests/orchestration/test_repair_attest.py  (C2 rewrite)
  .agent/handoff.md                          (C4)

C1 — the bookkeeping
Copy P1 to `.agent/authored/f276-r13-block.md`, P2 to `-ledger.md`, P3 to
`-plan.md`, P4 to `-prose-slips.md` and P7 to `-ledger-done.md`, each with
`shutil.copyfile`, never by retyping. Append P2's bytes to
`.agent/live_review.md`; append P4's bytes to `.agent/prose_slips.md`; write
P3's bytes over `.agent/plan.md`. Commit. P7 is COPIED here and APPLIED at C3 —
copying it now is what lets C3 be a single-purpose commit.

C2 — the repair
Write P5's bytes over `packages/orchestration/repair_attest.py` and P6's bytes
over `tests/orchestration/test_repair_attest.py`. Those two paths are the whole
change set of this commit. Commit.

C3 — the resolution
Append P7's bytes to `.agent/live_review.md`. That path is the whole change set
of this commit. Commit. P7 states what C2 landed, so it may not be committed
before C2 — this is the ordering constraint P7's own text names.

C4 — the handoff
Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the SESSION
NUMBER (this is SESSION 3 of F276), the round, the branch, the per-commit table
with `git show --numstat` insertions for C1, C2 and C3, every gate below with
its real output and exit code, the open-findings count by both readings, the
item-status table, the deviations, and the next expected action. One sentence of
context self-assessment. No length cap.

IT CANNOT CARRY THE PACKAGE'S NAME OR HASH, because the package is built after
it by construction, and it says so in one sentence rather than leaving the
absence to be read as an omission. The package's readings go to the reviewer in
this round's report and to `.remedy-wt/f276-r13/package.txt` on disk.

After C4, the tree is clean and the branch is pushed. Everything below commits
nothing.

THE INTEGRITY CHECK — closure precondition 3

  python3 -m apps.cli.main integrity check --json

Report the WHOLE JSON and its exit code. `passed` must be true. It runs AFTER
C3 for a reason the round can see: `R-1010` is registered High, and
`high_blockers_open` counts OPEN high findings, so the check can only read
`pass` once C3 has resolved it. A `fail` on any check, or a non-empty
`relevant_untracked`, stops the round and is reported rather than repaired.

THE EVIDENCE JOB — closure protocol step 1

  python3 .remedy-wt/f276-r13/create_f276_evidence.py

It resolves the committed review subject between the FORK POINT
`43d148177efd145f179ba2d9875eaa675b1595b7` and the tree at C4, collects its node
ids with `--collect-only`, runs those six test files, and writes the full
closed-schema gate set into `.remedy-wt/f276_evidence_closure/`. The reviewer
collected those same six files at `512ba69c` and read 112 node ids, and ran this
same producer over a repaired tree in a disposable worktree, where it reported
`is_valid_current_run: True` and `validation_errors: []` over an authority set
of 59 files in three tasks. Report the script's stderr in full — the collected
node-id count, the test result line, the `is_valid_current_run` reading and the
`validation_errors` list — and the summary dict it prints on stdout.
`validation_errors` must be EMPTY. If it is not, STOP: do not edit the script,
do not hand-write a gate file, do not proceed to the package. Report the errors
verbatim; repairing them is the reviewer's to author.

THE REVIEW PACKAGE — closure protocol step 2, MANDATORY and never skipped

  git status --porcelain
  bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f276_evidence_closure

The tree must be clean before the build; report that reading first. Then report
the package's FILENAME, its SHA-256 exactly as the script prints them, the
script's exit code, and the manifest's `committed_review_subject` base and head
commits, which must be that same fork point and the sha of C4. Finally report
the package's ARCHIVED PATH per DECISION amend0827 D1: the absolute directory it
ended up in, or the literal `NOT ARCHIVED` when it was left where it was built.
Do not move it; just say where it is.

Write those four readings — filename, SHA-256, archived path, accepted HEAD —
into `.remedy-wt/f276-r13/package.txt`, one per line, and quote the file in your
report. A FAILING PACKAGE BUILD IS A CLOSURE BLOCKER: report the raw error and
stop, never a partial or hand-assembled package.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as
   a deviation and applied anyway; it is never edited and no slice is retyped.
   This binds P5 and P6 exactly as it binds the prose.
2. Touch no path outside the change set above. In particular: do not edit
   `docs/roadmap/STATUS.md`, `README.md`, `docs/roadmap/features/T2_F276.md`,
   `scripts/self_use_queue.json`, `.agent/candidates.md`,
   `packages/orchestration/job_evidence.py` or
   `scripts/build_review_manifest.py` — the last two are the READERS the repair
   serves and they need no edit, which is the point of repairing the one
   function both of them call.
3. The commit sequence is C1, C2, C3, C4, no extra commit, none dropped, none
   reordered. C3 states C2's result and must follow it. Nothing after C4 commits
   anything; if any step after C4 leaves a tracked file modified, that is a
   finding and is reported rather than committed away.
4. An insertion count is read with `git show --numstat`, whose `+` column is the
   reading DECISION F104 D1 fixes for the 500-line cap; `git commit`'s own
   terminal summary applies rename detection and is NOT that reading, so where
   the two differ report the `--numstat` one and do not spend a deviation on the
   difference. The AGENTS.md oversize exception is ALREADY SPENT by `c6a519d1`
   and is NOT available to this round: if any commit here reaches 500 insertions
   by that reading, STOP and report rather than committing.
5. Destructive verification IS ordered this round, at G3. It runs in a
   disposable worktree under `.remedy-wt/`, never in the primary checkout, and
   that worktree is removed as G3's last action with `git worktree list`
   reported afterwards. The two job worktrees under `.remedy-wt/` are jobs';
   leave them.
6. Never force-push, never rewrite history, never delete a branch, never merge,
   never open or edit a pull request, never run any `gh` command. Work only on
   `feature/f276-data-root-hygiene`.
7. Read `.agent/STOP` from disk before the first commit. If it exists, write the
   handoff and end, doing nothing else.
8. The full suite does NOT run this round. It ran once on the merged tree in
   round 11 and its green transcript is committed at `3359296e`. This round
   edits two files; G2 runs the suites that guard them and their neighbours,
   which is what the verification tiers ask of a round.
9. `.remedy-wt/` is gitignored scratch holding this round's payloads and earlier
   rounds'. Never run `git clean -x`.

Done when — the gates below, each executed, each reporting its REAL output and
exit code. "Green" as a word is a finding.

G1 TRANSPORT AND STATE. One python check printing an explicit True or False per
   reading.
   (a) Each `.agent/authored/f276-r13-*` file the change set names equals its
       payload on disk byte for byte. Report the number of such files YOU
       measured rather than taking a count from this block.
   (b) THE RECORD APPENDS, in full byte forensics, which the gate budget
       reserves for this file. For `.agent/live_review.md` at C1: reading (a),
       the file equals its `b8ecbb7a` bytes plus P2's bytes; reading (b), an
       INDEPENDENT structural reader that splits the file on blank lines and
       compares its LAST N units, in order, against P2's N paragraphs, where N
       is a number the script COUNTS from the payload and never one this block
       states; and a NEGATIVE CONTROL that flips one byte inside the FIRST
       appended paragraph and confirms BOTH readings reject it. Then the SAME
       three readings for `.agent/live_review.md` at C3 against its C1 bytes
       plus P7's bytes.
   (c) `.agent/prose_slips.md` at C1 equals its `b8ecbb7a` bytes plus P4's
       bytes; `.agent/plan.md` at C1 equals P3's bytes;
       `packages/orchestration/repair_attest.py` at C2 equals P5's bytes;
       `tests/orchestration/test_repair_attest.py` at C2 equals P6's bytes.
       THE LAST TWO ARE THIS ROUND'S SAVED-COPY PROOF for P5 and P6, which get
       no `.agent/authored/` duplicate: read the two paths OUT OF THE COMMIT
       with `git show <C2>:<path>` rather than off the working tree, so the
       equality is asserted of the committed bytes and not of a file that
       merely still happens to sit on disk.
   Report the number of readings taken and that every one is True.
   SEPARATELY, report the SAVED BLOCK's own line count and sha256 beside the
   line count and digest the delegation message gave for P1 (R-0954).

G2 THE REPAIR IS CONFINED AND GREEN. At C2, report `git show --numstat c2` in
   full: it must name those two paths and no third. Then run, and report the
   real summary line and exit code of each:
     python3 -m pytest -q tests/orchestration/test_repair_attest.py
     python3 -m pytest -q tests/orchestration/test_diff_parser.py tests/orchestration/test_round13_evidence_alignment.py tests/orchestration/test_review_package_status.py tests/orchestration/test_review_authoritative_e2e.py tests/orchestration/test_development_artifact_boundary.py tests/cli/test_golden_path.py
     python3 -m ruff check packages/orchestration/repair_attest.py tests/orchestration/test_repair_attest.py
   The reviewer measured 9 passed, 153 passed and `All checks passed!` for these
   three over a tree carrying P5 and P6. Report YOUR numbers; where one differs
   from the reviewer's, report yours and say so rather than adjusting it.

G3 THE MUTATION RED-PROOF, in a disposable worktree and never in the primary
   checkout. Add a worktree under `.remedy-wt/` at C2. In it, purge every
   `__pycache__` directory and run with `python3 -B`. Report, in this order:
   (i) the CONTROL — `python3 -B -m pytest -q tests/orchestration/test_repair_attest.py`
   in the unmutated worktree, whose exit code and summary must be reported
   before any mutation; (ii) the MUTATION — restore ONE file by exact path,
   `git checkout b8ecbb7a -- packages/orchestration/repair_attest.py`, touching
   no other path and no test; (iii) the same pytest command again. THE ORDERED
   PROPERTY IS THE COLOUR AND ITS SHAPE, not a count: the control must be GREEN,
   the mutated run must be RED, and the mutated run must leave at least one node
   of `TestHunklessDiffEntriesAreVisible` PASSING — the deleted-entry and
   ordinary-modified nodes are discriminators, and a mutation that reddens every
   node of the class would mean the tests do not distinguish the repair from a
   reader that simply returns more paths. Report the named node ids that failed.
   Remove the worktree as this gate's last action and report `git worktree list`
   afterwards.

G4 THE INTEGRITY CHECK. Report the whole JSON and its exit code, and state
   `passed` and the per-check status list explicitly. State the open-findings
   count by distinct id at C3 and confirm `R-1010` is not among the open.

G5 THE EVIDENCE JOB AND THE BASE. First, at the commit C4 creates, report
   `git merge-base main <that commit>`; the first commit of
   `git rev-list --first-parent <that commit>` that `git rev-list main` also
   holds; and the LENGTHS of `git rev-list --ancestry-path <base>..<that commit>`
   and `git rev-list <base>..<that commit>`. The first is EXPECTED to answer
   main's tip `8f129d71e311ccd58bdb01d63c78bb75dffbd382` and NOT the base; the
   second must answer `43d148177efd145f179ba2d9875eaa675b1595b7`; the two
   lengths must be EQUAL. Then run the evidence job and report the collected
   node-id count, the test result line and exit code, `is_valid_current_run`,
   and `validation_errors`, which must be an empty list, and the summary dict's
   verdict field.

G6 THE PACKAGE, PUSH AND TREE. Report `git status --porcelain` before the build
   (empty), the script's exit code, the package filename, its SHA-256, the
   manifest's `committed_review_subject` base and head, the archived path, and
   `git status --porcelain` after the build, still empty because
   `remedy-review-*` is gitignored. Quote `.remedy-wt/f276-r13/package.txt`.
   Then `git push origin feature/f276-data-root-hygiene`, `ls .agent/STOP` which
   must be absent, and `git worktree list` in full.

Handback
Rewrite `.agent/handoff.md` as C4 describes, then report. The handback names
every gate with one line of its real output, declares every deviation, and
carries the item-status table. The package's four readings go in your REPORT to
the reviewer and in `.remedy-wt/f276-r13/package.txt`; the handoff says they
exist and where, and does not invent them. If any gate is red, say so plainly
with the output — a red gate honestly reported ends the round cleanly.
