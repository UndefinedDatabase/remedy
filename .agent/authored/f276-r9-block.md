STEP closure part three — F276 Data-root hygiene & disk budget, ROUND 9

This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 8's verdict, register R-1007 from the self-use run the closure
consumed, and perform the three closure steps that must happen before the
evidence package: the one §3 checklist consolidation pass this feature is
allowed, the ledger rotation, and the re-assignment of every still-open
finding to F282. This round does NOT flip STATUS, does not touch README, does
not build the evidence package and does not open a pull request; those are
round 10's.

Bundle, in commit order
C1 the bookkeeping, in ONE commit: the four payload copies under
   `.agent/authored/`, the ledger append, the decisions append, the plan
   rewrite.
C2 the §3 checklist consolidation.
C3 the ledger rotation, run by its own script, as its own commit.
C4 the finding re-assignment to F282.
C5 the handoff.

Payloads on disk
Every authored text of this round is a FILE the worker reads from disk. Nothing
is retyped. Each is named with its line count and its sha256; the worker
verifies the digest BEFORE using the file and reports both readings.

P1 `.remedy-wt/f276-r9/block.md` — this block.
   lines 221; the digest is in the delegation message that names this file.
P2 `.remedy-wt/f276-r9/ledger.md`
   lines 4; sha256 a31d4ed98536531608bd5700d4498484c2a7543eae38f5bfb70f06eae4784e2a
P3 `.remedy-wt/f276-r9/decisions.md`
   lines 74; sha256 fdcaa54f5151413f5bf851bb85cd443dc68aea188f0daa0be3a4788573e82055
P4 `.remedy-wt/f276-r9/plan.md`
   lines 44; sha256 f3602a4de443a74a5fc53a620e8ca18b822ae6907db3aa336ea5c2214854f5fa
P5 `.remedy-wt/f276-r9/f276-r9.diff`
   lines 77; sha256 1bc99001c5e36b975905499ebc9ced1d01a787646a454db5480ab0d3bd0eb3c4

P2 and P3 are APPEND-shaped: each begins with a newline and is concatenated
onto the end of its target, whose current bytes end with a newline, so the
result is the target's bytes followed by the payload's bytes and nothing else.
P4 is a REWRITE: `.agent/plan.md` becomes exactly P4's bytes. Containment test,
run mechanically before emission, one reading per pair:
`.agent/live_review.md` contains P2 — false; `.agent/decisions.md` contains P3
— false; `.agent/plan.md` contains P4 — false. All three are NEW bytes and no
FROM-count proof is owed. P5 is a unified diff against `8da83220`, produced by
the reviewer's own dry run and applied with `git apply`, never retyped; it
touches ONE file.

Change set — exactly these paths, and nothing else this round
  .agent/authored/f276-r9-block.md        (new, C1)
  .agent/authored/f276-r9-ledger.md       (new, C1)
  .agent/authored/f276-r9-decisions.md    (new, C1)
  .agent/authored/f276-r9-plan.md         (new, C1)
  .agent/live_review.md                   (C1 append, C3 rotation, C4 appends)
  .agent/decisions.md                     (C1 append)
  .agent/plan.md                          (C1 rewrite)
  docs/agents/planner_reviewer_prompt.md  (C2, from P5)
  .agent/live_review_archive.md           (C3, rotation)
  .agent/handoff.md                       (C5)

C1 — the bookkeeping
Copy P1 to `.agent/authored/f276-r9-block.md`, P2 to `-ledger.md`, P3 to
`-decisions.md`, P4 to `-plan.md`, each with `shutil.copyfile`, never by
retyping. Append P2's bytes to `.agent/live_review.md`; append P3's bytes to
`.agent/decisions.md`; write P4's bytes over `.agent/plan.md`. Commit.

What P2 books: round 8's verdict, PASS, and the registration of R-1007, the
one finding the self-use run of closure precondition 6 produced. What P3
appends: DECISION F276 D10, which rules the consolidation's direction and the
form and place of the re-assignment.

C2 — the §3 checklist consolidation
Apply P5:

  git apply --check .remedy-wt/f276-r9/f276-r9.diff
  git apply .remedy-wt/f276-r9/f276-r9.diff

It merges item 17 into item 15 in `docs/agents/planner_reviewer_prompt.md`,
retires the number 17, repoints the one surviving cross-reference to it inside
item 35, and amends the consolidation bookkeeping paragraph to record the pass,
the measured direction and the new target of 34. This is the ONE consolidation
pass operator amendment amend0827-process-diet rule 4 allows this feature, and
it is spent here. Commit.

C3 — the ledger rotation
Run the repository's own script from the repository root:

  python3 scripts/rotate_live_review.py

Report every line it prints. It moves, byte-verbatim, every `Gate:` record of a
feature that is `[x]` in `docs/roadmap/STATUS.md` and every resolved finding
pair into the append-only archive, verifying each moved record's sha256 before
and after and refusing on any mismatch. Do not pass it arguments and do not
edit either file by hand. Its whole change set is `.agent/live_review.md` and
`.agent/live_review_archive.md`; commit exactly those two. F276's own `Gate:`
records stay, because F276 is still `[~]` at this commit.

C4 — the finding re-assignment to F282
Closure protocol step 5 clause (i), placed here rather than in C1 and performed
as an APPEND rather than as a rewrite, both per DECISION F276 D10.

Compute the open set from `.agent/live_review.md` AS IT STANDS AFTER C3: every
paragraph beginning `- R-` whose id has no matching line beginning
`Done: R-` followed by that id. For each such finding whose paragraph does NOT
already contain the exact string

Owner: F282 — Findings paydown v2

append, as a NEW LINE at the very end of that paragraph — immediately before
the blank line that terminates it — exactly this line:

Owner: F282 — Findings paydown v2 (re-assigned at F276's closure, 2026-09-20; this line supersedes any earlier Owner line in this paragraph).

MODIFY NO EXISTING LINE and REMOVE NONE. A finding whose paragraph already
holds the exact string above is left completely untouched. Report the list of
ids you appended to and its length, and the list of ids you skipped. Commit.

C5 — the handoff
Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the SESSION
NUMBER (this is SESSION 2 of F276), the round, the branch, the per-commit
tables with `git show --numstat` insertion counts for C1 to C4, every gate
below with its real output and exit code, the open-findings count by both
readings, the item-status table, the deviations, and the next expected action.
One sentence of context self-assessment. No length cap. Its own insertion count
belongs in its own text, not in a gate.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as
   a deviation and applied anyway; it is never edited and no slice is retyped.
2. Touch no path outside the change set above. In particular: do not edit
   `docs/roadmap/STATUS.md`, `README.md`, `docs/roadmap/features/T2_F276.md`,
   `scripts/self_use_queue.json`, `.agent/candidates.md` or
   `.agent/prose_slips.md` — every one of those is round 10's or is finished.
3. The commit sequence is C1, C2, C3, C4, C5, in that order, no extra commit,
   none dropped, none reordered. Report any deviation.
4. Every commit's insertion count, by `git show --numstat`, stays under 500,
   EXCEPT C3, whose whole diff is a mechanical move of records between two
   files performed by the repository's own script. C3 is the rewrite of
   `.agent/live_review.md` plus its archive and is therefore an indivisible
   artifact of the kind AGENTS.md's counting rule exempts; report its numbers
   and say which exemption you are reading it under. Report C1, C2 and C4's
   counts; C5's own belongs in its own text.
5. No destructive verification is ordered this round, so create no disposable
   worktree. The self-use job's worktree from round 8 is the job's; leave it.
6. Never force-push, never rewrite history, never delete a branch, never merge,
   never open or edit a pull request, never run any `gh` command. Work only on
   `feature/f276-data-root-hygiene`.
7. Read `.agent/STOP` from disk before the first commit. If it exists, write the
   handoff and end, doing nothing else.
8. The full suite does NOT run this round. It ran once as rule 1 requires and
   once more as rule 2's repair, and its green transcript is committed at
   `fd23710f`.

Done when — six gates, each executed, each reporting its REAL output and exit
code. "Green" as a word is a finding.

G1 TRANSPORT AND STATE, at C1. One python check printing an explicit True or
   False per reading: each of the four `.agent/authored/f276-r9-*` files equals
   its payload on disk byte for byte; `.agent/live_review.md` at C1 equals its
   `8da83220` bytes plus P2's bytes; `.agent/decisions.md` at C1 equals its
   `8da83220` bytes plus P3's bytes; `.agent/plan.md` at C1 equals P4's bytes.
   Report the number of readings and that every one is True. SEPARATELY, report
   the SAVED BLOCK's own line count and sha256 beside the line count and digest
   the delegation message gave for P1, as two readings side by side (R-0954).

G2 THE CONSOLIDATION, at C2. Report three readings.
   (a) `git rev-parse C2:docs/agents/planner_reviewer_prompt.md` must read
       EXACTLY 073486a24b07721fa6364368cc573f8313c1ed52, the object of the
       reviewer's own dry run, so the committed file is byte-identical to the
       tree the reviewer applied and tested before authoring.
   (b) The checklist's own numbering, counted MECHANICALLY over the file at C2
       by matching every line of the form two spaces, a number, a full stop, a
       space and two asterisks, within the pre-emission checklist: report the
       full list of numbers it yields, its length, and whether 17 is among them.
       The length must be 34 and 17 must be absent.
   (c) `git diff --name-only C1 C2` must name that one path and no other.

G3 THE ROTATION, at C3. Report every line `scripts/rotate_live_review.py`
   printed, including the gate records moved, the finding pairs moved, both
   file sizes before and after, and the open-findings count before and after,
   which must be IDENTICAL — that identity is the rotation's own safety
   property and the reason the script prints it. Then report
   `git diff --name-only C2 C3`, which must name exactly the two ledger paths.

G4 THE RE-ASSIGNMENT, at C4. Report four readings.
   (a) `git show --numstat C4 -- .agent/live_review.md`: the deletions column
       must be ZERO. That is the measurement that no landed byte was modified,
       and it is the gate DECISION F276 D10 names.
   (b) The list of ids you appended an Owner line to, and its length; and the
       list you skipped, with the reason each was skipped.
   (c) Recomputed over the file at C4: every open finding's paragraph contains
       the string `Owner: F282 — Findings paydown v2` AT LEAST ONCE. Report the
       count of open findings and the count that satisfy this; they must be
       equal, and report both numbers rather than the word "all".
   (d) The set of ids registered and the set resolved are UNCHANGED from C3 to
       C4: report both counts at both commits, four numbers.

G5 THE CANARY, after C4, in the primary checkout:

  python3 -m pytest tests/cli/test_golden_path.py -q

   and, because this round edits a file under `docs/`:

  python3 -m pytest tests/docs -q

   Report each summary line and each exit code.

G6 PUSH AND TREE, after C5. `git push origin feature/f276-data-root-hygiene`;
   then `git status --porcelain` in the primary checkout, which must be EMPTY;
   then `ls .agent/STOP`, which must be absent; then `git worktree list` in
   full, reported as a measurement — the two job worktrees are jobs' and are
   expected.

Handback
Rewrite `.agent/handoff.md` as C5 describes, then report. The handback names
every gate with one line of its real output, declares every deviation, and
carries the item-status table with one row per bundle item and per gate. If any
gate is red, say so plainly with the output — a red gate honestly reported ends
the round cleanly.
