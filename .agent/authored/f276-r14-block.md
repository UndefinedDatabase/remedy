STEP closure part seven — F276 Data-root hygiene & disk budget, ROUND 14, THE CLOSING ROUND

This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Close F276. Book round 13's verdict, then land the closure commit — the LAST
commit on this branch — carrying the STATUS `[x]` line, the README Tier 2
entry, SU-024's `consumed_by` and the final `.agent/` state, and then open the
pull request into `main`. The pull request is NOT merged this session.

Every closure precondition is already met and none is re-measured by guesswork
here: T001 to T004 are built; the integration gate ran once on the merged tree
and its green transcript is committed at `3359296e`; the integrity check reads
`passed: true`; the feature file's Built State is current; the self-use item was
consumed in round 8; `R-1010` is repaired and resolved; and the package is built
and archived. What remains is the ledger edit and the pull request.

Bundle, in commit order
C1 the bookkeeping, in ONE commit: the payload copies under `.agent/authored/`,
   the ledger append that books round 13, the prose-slip append and the plan
   rewrite.
C2 THE CLOSURE COMMIT, the LAST on this branch: the STATUS line, the README
   entry, `scripts/self_use_queue.json` and the final `.agent/handoff.md`.
Then, AFTER C2 and committing nothing further: the pull request.

Payloads on disk
Every authored text of this round is a FILE the worker reads from disk. Nothing
is retyped. Each is named with its line count and its sha256; the worker
verifies BOTH readings BEFORE using the file and reports them.

P1 `.remedy-wt/f276-r14/block.md` — this block.
   the line count and digest are in the delegation message that names this file.
P2 `.remedy-wt/f276-r14/ledger.md`
   lines 2; sha256 20fe134c152516e2fd5b933634eb409eff3db959884580abe971c8b8cd627acc
P3 `.remedy-wt/f276-r14/plan.md`
   lines 43; sha256 607dd750ff17c96a363513030fd061cc088abe56d41ddaaab4f2480cf42ddd56
P4 `.remedy-wt/f276-r14/prose_slips.md`
   lines 1; sha256 2176701a7502aa673c0a1727546ad0a1cbc862de53e09bc11fb0c428f9584b85
P5 `.remedy-wt/f276-r14/status_from.txt` and `.remedy-wt/f276-r14/status_to.txt`
   the STATUS pair. FROM lines 1; TO lines 1.
P6 `.remedy-wt/f276-r14/readme_from.txt` and `.remedy-wt/f276-r14/readme_to.txt`
   the README pair. FROM lines 2; TO lines 8.

P2 and P4 are APPEND-shaped: each is concatenated onto the end of its target,
whose current bytes end with a newline. P2 begins with a newline, the blank
separator `.agent/live_review.md` uses between entries; P4 does not, because
`.agent/prose_slips.md` is one line per slip. P3 is a REWRITE: `.agent/plan.md`
becomes exactly P3's bytes.

P5 and P6 are FROM/TO PAIRS, applied by replacing the FROM's exact bytes with
the TO's exact bytes in the named file. Neither FROM is retyped and neither is
matched loosely: read both files and use a single literal string replacement.

Containment test, run mechanically by the reviewer at `03e72f77`, one reading
per pair, the label derived from the output on the same line (item 15):
  `.agent/live_review.md` contains P2 — false, so APPEND
  `.agent/prose_slips.md` contains P4 — false, so APPEND
  `.agent/plan.md` contains P3 — false, so REWRITE
  P5's TO contains P5's FROM — false, so REWRITE
  P6's TO contains P6's FROM — false, so REWRITE
Every pair above reads false, so all are NEW bytes and no FROM-count proof is
owed on any of them.

ANCHOR UNIQUENESS, measured by the reviewer at `03e72f77`: P5's FROM occurs
exactly ONCE in `docs/roadmap/STATUS.md` and P6's FROM occurs exactly ONCE in
`README.md`. Report both counts yourself before replacing; a count other than
one stops the round.

Change set — exactly these paths, and nothing else this round
  .agent/authored/f276-r14-block.md         (new, C1)
  .agent/authored/f276-r14-ledger.md        (new, C1)
  .agent/authored/f276-r14-plan.md          (new, C1)
  .agent/authored/f276-r14-prose-slips.md   (new, C1)
  .agent/authored/f276-r14-status-to.txt    (new, C1)
  .agent/authored/f276-r14-readme-to.txt    (new, C1)
  .agent/live_review.md                     (C1 append)
  .agent/prose_slips.md                     (C1 append)
  .agent/plan.md                            (C1 rewrite)
  docs/roadmap/STATUS.md                    (C2, the P5 pair)
  README.md                                 (C2, the P6 pair)
  scripts/self_use_queue.json               (C2, one field)
  .agent/handoff.md                         (C2)

C1 — the bookkeeping
Copy P1 to `.agent/authored/f276-r14-block.md`, P2 to `-ledger.md`, P3 to
`-plan.md`, P4 to `-prose-slips.md`, the STATUS TO to `-status-to.txt` and the
README TO to `-readme-to.txt`, each with `shutil.copyfile`, never by retyping.
Append P2's bytes to `.agent/live_review.md`; append P4's bytes to
`.agent/prose_slips.md`; write P3's bytes over `.agent/plan.md`. Commit.

The two TO texts are copied HERE, in the bookkeeping commit, so that the closure
commit's own path set stays exactly the four paths the protocol allows it. What
C1 saves is the reviewer-authored text; what C2 applies is the same bytes.

C2 — the closure commit, and it is the LAST commit on this branch
Apply P5 to `docs/roadmap/STATUS.md` and P6 to `README.md`. In
`scripts/self_use_queue.json`, set the `consumed_by` field of the item whose
`id` is `SU-024` from its current empty string to `f276`, changing no other
field of that item and no other item — load the file, set the one value, and
write it back with the file's own existing formatting preserved. Rewrite
`.agent/handoff.md`. Commit all four paths TOGETHER: the README entry and the
STATUS line may never disagree in any committed state, which is the R-0154
ledger cross-check and the reason they share a commit.

THE PULL REQUEST, after C2 and committing nothing
Push, then open it with `gh pr create` against `main` from
`feature/f276-data-root-hygiene`. The description carries what changed, why,
the key decisions, how to review, a changed-files summary, the latest verdict,
the open-findings count and the runtime actuals. DO NOT MERGE IT, do not mark it
ready-for-review-by-merging, and run no `gh pr merge`. Report its number and URL.

Its title and body must contain no leading-slash token, no absolute path and no
secret-like string — the evidence metadata scanner rejects such subjects. The
same rule binds your commit subjects.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as
   a deviation and applied anyway; it is never edited and no slice is retyped.
2. Touch no path outside the change set above. In particular: do not edit
   `docs/roadmap/features/T2_F276.md`, whose Built State is already current, and
   do not edit `.agent/candidates.md`, which reads EMPTY and stays so unless the
   closure itself raises a candidate — if it does, that file is the ONE path a
   commit after C2 may carry, alone, declared as such.
3. The commit sequence is C1 then C2, no extra commit, none dropped, none
   reordered. C2 is the last commit on the branch.
4. An insertion count is read with `git show --numstat`, whose `+` column is the
   reading DECISION F104 D1 fixes for the 500-line cap; `git commit`'s own
   terminal summary applies rename detection and is NOT that reading. The
   AGENTS.md oversize exception is ALREADY SPENT by `c6a519d1` and is NOT
   available: if any commit here reaches 500 insertions by that reading, STOP.
5. No destructive verification is ordered, so create no disposable worktree. The
   two job worktrees under `.remedy-wt/` are jobs'; leave them.
6. Never force-push, never rewrite history, never delete a branch, never merge.
   Work only on `feature/f276-data-root-hygiene`.
7. Read `.agent/STOP` from disk before the first commit. If it exists, write the
   handoff and end, doing nothing else.
8. The full suite does NOT run this round. It ran once on the merged tree in
   round 11 and its green transcript is committed at `3359296e`; closure
   precondition 2 is satisfied by READING that transcript, never by re-running.
9. `.remedy-wt/` is gitignored scratch. Never run `git clean -x`.

Done when — the gates below, each executed, each reporting its REAL output and
exit code. "Green" as a word is a finding.

G1 TRANSPORT AND STATE, at C1. One python check printing an explicit True or
   False per reading.
   (a) Each `.agent/authored/f276-r14-*` file the change set names equals its
       payload on disk byte for byte. Report the number of such files YOU
       measured rather than taking a count from this block.
   (b) THE RECORD APPEND, in full byte forensics, which the gate budget reserves
       for this file. For `.agent/live_review.md` at C1: reading (a), the file
       equals its `03e72f77` bytes plus P2's bytes; reading (b), an INDEPENDENT
       structural reader that splits the file on blank lines and compares its
       LAST N units, in order, against P2's N paragraphs, where N is a number
       the script COUNTS from the payload and never one this block states; and a
       NEGATIVE CONTROL that flips one byte inside the FIRST appended paragraph
       and confirms BOTH readings reject it.
   (c) `.agent/prose_slips.md` at C1 equals its `03e72f77` bytes plus P4's
       bytes; `.agent/plan.md` at C1 equals P3's bytes.
   Report the number of readings taken and that every one is True.
   SEPARATELY, report the SAVED BLOCK's own line count and sha256 beside the
   line count and digest the delegation message gave for P1 (R-0954).

G2 THE CLOSURE EDIT IS EXACT. At C2, report the FROM occurrence count you
   measured in each target BEFORE replacing (each must be 1), and then, read out
   of the commit with `git show <C2>:<path>`: that `docs/roadmap/STATUS.md`
   contains P5's TO bytes exactly once and P5's FROM bytes zero times, and that
   `README.md` contains P6's TO bytes exactly once and P6's FROM bytes zero
   times. Report `git show --numstat <C2>` in full: it must name exactly the
   four paths C2 is allowed and no fifth.

G3 THE LEDGER PINS, which are the reason STATUS and README share a commit.

     python3 -m pytest tests/docs/ -q

   Report the summary line and the exit code. This is the docs-round gate: the
   round's change set includes `docs/roadmap/**`, so it is owed in addition to
   the canary, and it is the gate that reads the README accepted list against
   the STATUS ledger in both directions.

G4 THE CANARY AND THE QUEUE.

     python3 -m pytest tests/cli/test_golden_path.py -q

   Report its summary line and exit code. Then report, read out of the commit
   with `git show <C2>:scripts/self_use_queue.json`: the `consumed_by` value of
   the item whose `id` is `SU-024`, which must read exactly `f276`; the NUMBER
   of items in the file before and after C2, which must be equal; and the number
   of items whose `consumed_by` is non-empty before and after, which must differ
   by exactly one.

G5 THE INTEGRITY CHECK AND THE OPEN SET, after C2.

     python3 -m apps.cli.main integrity check --json

   Report the whole JSON and its exit code; `passed` must be true. Then report
   the open-findings count at C2 by DISTINCT ID — every `^- R-\d+` registration
   minus every `^Done: R-\d+` resolution — together with the count of those
   carrying the string `Owner: F282`, using that SHORTER spelling and not the
   longer one, because two spellings of the same owner tag are in the file and
   counting the long one reports an absence wherever the short one was written.

G6 PUSH, PULL REQUEST AND TREE. `git push origin feature/f276-data-root-hygiene`
   after C2; then `gh pr create` as described; then `git status --porcelain`,
   which must be EMPTY; then `ls .agent/STOP`, which must be absent; then
   `git worktree list` in full. Report the pull request's NUMBER and URL, and
   state plainly that you did not merge it. These readings necessarily POSTDATE
   the commit that writes the handback, so they belong to the round report and
   not to the handoff's own text; the reviewer re-takes them (item 31).

Handback
Rewrite `.agent/handoff.md` as part of C2, then report. The handback names every
gate with one line of its real output, declares every deviation, and carries the
item-status table. Because this is the closing round, the handoff additionally
states: the accepted HEAD `03e72f77fd74e72d6cdc8b2d2f00e3efe76e0315`, the
package name and its SHA-256 and its archived path, the evidence job id
`f276r13e1001`, the open-findings count, and that the pull request is OPEN and
UNMERGED. If any gate is red, say so plainly with the output — a red gate
honestly reported ends the round cleanly, and a closure that cannot be completed
is reported as unfinished rather than declared done.
