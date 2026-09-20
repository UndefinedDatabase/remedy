STEP closure part eight — F276 Data-root hygiene & disk budget, ROUND 15, THE REPAIR THAT COMPLETES THE CLOSURE

This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Make `tests/docs/` green on this branch. Round 14's closure commit moved the
README's Tier 2 prose entry but not the two README counters the docs suite
pins, so `python3 -m pytest tests/docs/ -q` reads `2 failed, 312 passed` at
exit 1 at `b07a2eda` with a pull request open over it. This round books round
14's verdict, registers `R-1011` for that on-disk state, repairs both counters,
resolves the finding, and empties the entry round 14 filed in
`.agent/candidates.md`. It opens NO pull request and MERGES NOTHING; pull
request 262 already exists and stays open and untouched.

WHY COMMITS ON THIS BRANCH ARE ALLOWED AFTER ITS CLOSURE COMMIT. Operator
amendment amend0820-gate-autonomy rules that a check which is RED over an open
pull request is WORK and not a blocker, and that commits on that pull request's
branch are explicitly allowed for the repair. Rule A4's "the STATUS edit is the
last commit" is a rendering rule about the closing PR, and a branch that cannot
be merged green is the condition that rule exists to protect. Repairing it here
is the narrower and safer reading, and it is the one the amendment names.

Bundle, in commit order
C1 the bookkeeping, in ONE commit: the payload copies under `.agent/authored/`,
   the ledger append that books round 14 and registers `R-1011`, the
   `.agent/candidates.md` rewrite, the prose-slip append and the plan rewrite.
C2 the repair: `README.md`, the two counter pairs, and nothing else.
C3 the resolution: the `Done: R-1011` append, committed AFTER C2.
C4 the handoff.

Payloads on disk
Every authored text of this round is a FILE the worker reads from disk. Nothing
is retyped. Each is named with its line count and its sha256; the worker
verifies BOTH readings BEFORE using the file and reports them.

P1 `.remedy-wt/f276-r15/block.md` — this block.
   the line count and digest are in the delegation message that names this file.
P2 `.remedy-wt/f276-r15/ledger.md`
   lines 4; sha256 e176aae18f87910d135a2b90d5c5b73573c33ab251184b00b014a938d9683b62
P3 `.remedy-wt/f276-r15/plan.md`
   lines 40; sha256 e7e24f0cb61c4e7633e7127e3f35be90e852ecbf7f6e94702a98848f328cff84
P4 `.remedy-wt/f276-r15/prose_slips.md`
   lines 1; sha256 2ace9662326e849b58b5ab6cecf5f9e744e46ea05c95532afc395ee69400b85d
P5 `.remedy-wt/f276-r15/candidates.md`
   lines 41; sha256 5f1aebbb0b6986e3aac2f03eba03678dda45e7e425c0b8df2f6fde90e2eefd1f
P6 `.remedy-wt/f276-r15/ledger_done.md`
   lines 2; sha256 a1dc6ca2b12beadd8235f89bec9ba0b506c595d5fd86df77f21389352a9b598f
P7 the two README pairs:
   `.remedy-wt/f276-r15/count_from.txt` and `.remedy-wt/f276-r15/count_to.txt`
   `.remedy-wt/f276-r15/tier_from.txt` and `.remedy-wt/f276-r15/tier_to.txt`
   The COUNT pair's FROM and TO carry NO trailing newline, because the sentence
   they replace continues on its own line; the TIER pair's FROM and TO each end
   with one, because they are whole table rows. Do not add or strip a byte.

P2, P4 and P6 are APPEND-shaped: each is concatenated onto the end of its
target, whose current bytes end with a newline. P2 and P6 each begin with a
newline, the blank separator `.agent/live_review.md` uses between entries; P4
does not, because `.agent/prose_slips.md` is one line per slip. P3 and P5 are
REWRITES: `.agent/plan.md` and `.agent/candidates.md` each become exactly their
payload's bytes.

Containment test, run mechanically by the reviewer at `b07a2eda`, one reading
per pair, the label derived from the output on the same line (item 15):
  `.agent/live_review.md` contains P2 — false, so APPEND
  `.agent/live_review.md` contains P6 — false, so APPEND
  `.agent/prose_slips.md` contains P4 — false, so APPEND
  `.agent/plan.md` contains P3 — false, so REWRITE
  `.agent/candidates.md` contains P5 — false, so REWRITE
  the COUNT pair's TO contains its FROM — false, so REWRITE
  the TIER pair's TO contains its FROM — false, so REWRITE
Every pair above reads false, so all are NEW bytes and no FROM-count proof is
owed on any of them.

ANCHOR UNIQUENESS, measured by the reviewer at `b07a2eda`: each of the two
README FROM texts occurs exactly ONCE in `README.md`. Report both counts
yourself before replacing; a count other than one stops the round.

P5 keeps `.agent/candidates.md`'s header and its other entries byte-for-byte and
replaces only the F276 closure-gate paragraph with the resolved-pointer wording
the file's other retired entries use. The reviewer built it from the file's own
bytes rather than by retyping them.

Change set — exactly these paths, and nothing else this round
  .agent/authored/f276-r15-block.md         (new, C1)
  .agent/authored/f276-r15-ledger.md        (new, C1)
  .agent/authored/f276-r15-plan.md          (new, C1)
  .agent/authored/f276-r15-prose-slips.md   (new, C1)
  .agent/authored/f276-r15-candidates.md    (new, C1)
  .agent/authored/f276-r15-ledger-done.md   (new, C1)
  .agent/live_review.md                     (C1 append, C3 append)
  .agent/candidates.md                      (C1 rewrite)
  .agent/prose_slips.md                     (C1 append)
  .agent/plan.md                            (C1 rewrite)
  README.md                                 (C2, the two P7 pairs)
  .agent/handoff.md                         (C4)

C1 — the bookkeeping
Copy P1 to `.agent/authored/f276-r15-block.md`, P2 to `-ledger.md`, P3 to
`-plan.md`, P4 to `-prose-slips.md`, P5 to `-candidates.md` and P6 to
`-ledger-done.md`, each with `shutil.copyfile`, never by retyping. Append P2's
bytes to `.agent/live_review.md`; append P4's bytes to `.agent/prose_slips.md`;
write P3's bytes over `.agent/plan.md`; write P5's bytes over
`.agent/candidates.md`. Commit.

C2 — the repair
In `README.md`, replace the COUNT pair's FROM with its TO and the TIER pair's
FROM with its TO, each as a single literal string replacement after you have
measured that the FROM occurs exactly once. `README.md` is the whole change set
of this commit. Commit.

C3 — the resolution
Append P6's bytes to `.agent/live_review.md`. That path is the whole change set
of this commit. Commit. P6 states what C2 landed, so it may not be committed
before C2 — this is the ordering constraint P6's own text names.

C4 — the handoff
Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the SESSION
NUMBER (this is SESSION 3 of F276), the round, the branch, the per-commit table
with `git show --numstat` insertions for C1, C2 and C3, every gate below with
its real output and exit code, the open-findings count by both readings, the
item-status table, the deviations, and the next expected action. One sentence of
context self-assessment. No length cap.

Because this completes the closure, the handoff also states: the accepted HEAD
`03e72f77fd74e72d6cdc8b2d2f00e3efe76e0315`, the package
`remedy-review-20260920-150902-READY_FOR_REVIEW.zip` with SHA-256
`b36e23f1e04adf64f953ba9fbc5825ff5a9942af97a8133616646417d6cd01f3` at
`/home/decodeux/Repos/remedy-history/zips`, the evidence job `f276r13e1001`, and
that pull request 262 is OPEN and UNMERGED and is the next session's Open PR
Gate business.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as
   a deviation and applied anyway; it is never edited and no slice is retyped.
2. Touch no path outside the change set above. In particular: do not edit
   `docs/roadmap/STATUS.md`, whose `[x]` line is correct and whose numbers this
   round makes the README agree with rather than the other way round; do not
   edit `scripts/self_use_queue.json`; do not edit
   `docs/roadmap/features/T2_F276.md`.
3. The commit sequence is C1, C2, C3, C4, no extra commit, none dropped, none
   reordered. C3 states C2's result and must follow it.
4. An insertion count is read with `git show --numstat`, whose `+` column is the
   reading DECISION F104 D1 fixes for the 500-line cap; `git commit`'s own
   terminal summary applies rename detection and is NOT that reading. The
   AGENTS.md oversize exception is ALREADY SPENT by `c6a519d1`: if any commit
   here reaches 500 insertions by that reading, STOP and report.
5. No destructive verification is ordered, so create no disposable worktree. The
   two job worktrees under `.remedy-wt/` are jobs'; leave them.
6. Never force-push, never rewrite history, never delete a branch, never merge.
   Run NO `gh` command at all this round: pull request 262 exists, needs no
   edit, and must not be merged — that is the next session's Open PR Gate.
7. Read `.agent/STOP` from disk before the first commit. If it exists, write the
   handoff and end, doing nothing else.
8. The full suite does NOT run this round. It ran once on the merged tree in
   round 11 and its green transcript is committed at `3359296e`. This round
   edits two numerals in `README.md`; G2 runs the suite that pins them.
9. `.remedy-wt/` is gitignored scratch. Never run `git clean -x`.

Done when — the gates below, each executed, each reporting its REAL output and
exit code. "Green" as a word is a finding.

G1 TRANSPORT AND STATE. One python check printing an explicit True or False per
   reading.
   (a) Each `.agent/authored/f276-r15-*` file the change set names equals its
       payload on disk byte for byte. Report the number of such files YOU
       measured rather than taking a count from this block.
   (b) THE RECORD APPENDS, in full byte forensics, which the gate budget
       reserves for this file. For `.agent/live_review.md` at C1: reading (a),
       the file equals its `b07a2eda` bytes plus P2's bytes; reading (b), an
       INDEPENDENT structural reader that splits the file on blank lines and
       compares its LAST N units, in order, against P2's N paragraphs, where N
       is a number the script COUNTS from the payload and never one this block
       states; and a NEGATIVE CONTROL that flips one byte inside the FIRST
       appended paragraph and confirms BOTH readings reject it. Then the SAME
       three readings for `.agent/live_review.md` at C3 against its C1 bytes
       plus P6's bytes.
   (c) `.agent/prose_slips.md` at C1 equals its `b07a2eda` bytes plus P4's
       bytes; `.agent/plan.md` at C1 equals P3's bytes; `.agent/candidates.md`
       at C1 equals P5's bytes.
   Report the number of readings taken and that every one is True.
   SEPARATELY, report the SAVED BLOCK's own line count and sha256 beside the
   line count and digest the delegation message gave for P1 (R-0954).

G2 THE GATE THAT FOUND THE DEFECT, RUN AGAIN.

     python3 -m pytest tests/docs/ -q

   Run it TWICE and report both: once at `b07a2eda`, this round's base, where
   the reviewer measured `2 failed, 312 passed` at exit 1 — take this reading
   BEFORE C1, since it describes the base and no commit of this round changes
   it — and once after C2, where it must be GREEN at exit 0. Name the two
   failing node ids in the base reading. A base run that is already green
   stops the round and is reported: it would mean the defect is not what this
   block says it is.

G3 THE REPAIR IS CONFINED AND EXACT. At C2, report the FROM occurrence count
   you measured in `README.md` for each of the two pairs BEFORE replacing (each
   must be 1). Then, read out of the commit with `git show <C2>:README.md`:
   that it contains each TO exactly once and each FROM zero times. Report
   `git show --numstat <C2>` in full: it must name `README.md` and no second
   path, and its insertion count must be 2.

G4 THE LEDGER AND THE CANDIDATES. Report the open-findings count by DISTINCT ID
   at C1 and at C3 — every `^- R-\d+` registration minus every `^Done: R-\d+`
   resolution — which must be 20 at C1 with `R-1011` among them and 19 at C3
   with `R-1011` no longer among them. Report the count of the 19 carrying the
   string `Owner: F282`, using that SHORTER spelling. Then report, read out of
   the commit with `git show <C1>:.agent/candidates.md`, whether the string
   `went RED against the closure commit` occurs zero times and whether
   `R-1011` occurs at least once — the entry retired and its pointer left.

G5 THE CANARY AND THE INTEGRITY CHECK, after C3.

     python3 -m pytest tests/cli/test_golden_path.py -q
     python3 -m apps.cli.main integrity check --json

   Report each summary line and exit code, and for the integrity check the whole
   JSON with `passed` and the per-check status list stated explicitly.

G6 PUSH AND TREE. `git push origin feature/f276-data-root-hygiene` after C4;
   then `git status --porcelain`, which must be EMPTY; then `ls .agent/STOP`,
   which must be absent; then `git worktree list` in full. Run no `gh` command.
   These readings necessarily POSTDATE the commit that writes the handback, so
   they belong to the round report and not to the handoff's own text; the
   reviewer re-takes them (item 31).

Handback
Rewrite `.agent/handoff.md` as C4 describes, then report. The handback names
every gate with one line of its real output, declares every deviation, and
carries the item-status table. If any gate is red, say so plainly with the
output — a red gate honestly reported ends the round cleanly, which is exactly
what round 14 did and why this round exists.
