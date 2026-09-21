STEP R4 T001 — F277 Machine contracts: event vocabulary, JSON envelope, exit codes
Session 2 of F277 · round 4 · base `f9cb2f62` (the tip of `feature/f277-machine-contracts`,
round 3's C4). This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 3's PASS verdict, register and resolve finding R-1013, and dispose of
`snapshot_created` exactly as the reviewer's dry run disposed of it. `autonomy_loop._decide`
gated autonomy level 5 on that event name, which nothing in this repository writes, so the gate
answered "no snapshot for revert" for every job that ever reached it however good the snapshot
was. The gate now reads the `verified_snapshot` signal — the durable `build_snapshot_truth`
check of Step 1159, which `autonomy_readiness` already gates its own level 5 on and which
`run_autonomy_loop` computes one statement before it calls `_decide`. The branch had no test at
all and gains four. The quarantine goes from three names to two.

Read first, completely: AGENTS.md; `docs/roadmap/features/T2_F277.md`; and DECISION F277 D4 in
`.agent/decisions.md`, which is this round's spec and which named this disposition and rejected
the rename when it was written — where this block is terser, D4 rules. This round registers NO
new DECISION, because D4 already fixed both the route and the reason.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f277-r4-payloads/`. Verify each
line count and sha256 BEFORE use and report both readings; any mismatch stops the round. Apply
byte-exact, never by retyping.
  ledger.md      lines 4   sha256 e00f07a6df47ec9776db0e976c6e55d3df0b2b35abe9f84a3675ab2044940729
  resolution.md  lines 2   sha256 1910b346308e83bea0f658ec3c1183e15ded67a67b13760e9aedf7696d89dc38
  plan.md        lines 46  sha256 2bc6639f7e721044b962f049996b5c0ce599512c971072c9e56978bfd6b70bc4
  block.md       this block; save it and report its line count and digest (R-0954)
CODE — ONE diff the reviewer produced in its own dry-run worktree at `f9cb2f62`, applied there,
tested there and red-proved there. Verify its digest, then apply it in TWO disjoint slices with
the `--include` lists below, always from its scratch path. Do not retype a hunk, do not edit
one, do not copy the diff into the repository, and never apply it whole — C2 and C3 are separate
commits because the production change and its tests are separate reviewable units.
  `.remedy-wt/f277-r4-payloads/f277-r4.diff`
    lines 162  sha256 f9d548add63cb39ab3c0a6e95c1b8f34771cb38824f01c5879a5d90d874d1e31

SHAPE OF EACH STATE PAYLOAD, tested mechanically by the reviewer at `f9cb2f62`, one reading per
pair, the label derived from that reading's own output on the same line (item 15):
  `.agent/live_review.md` contains ledger.md — false, so APPEND
  `.agent/live_review.md` contains resolution.md — false, so APPEND
  `.agent/plan.md` contains plan.md — false, so REWRITE
Every pair reads false, so all are NEW bytes and NO FROM-count proof is owed on any of them.
ledger.md and resolution.md each begin with a newline, the blank separator their target uses
between entries. There is no `.agent/decisions.md` payload and no `.agent/prose_slips.md`
payload this round — round 3's block arithmetic held, so there is no slip to append — and no
`docs/roadmap/**` edit and no live_review re-head.

Bundle, in commit order
C1a the payload copies, ONE commit whose whole change set is new files under `.agent/authored/`:
   a byte copy of each payload listed above, `block.md` included, as
   `.agent/authored/f277-r4-<name>` — keeping each payload's own file name after the prefix. The
   code diff is NOT copied and is NOT part of this or any commit; G2's blob-id gate is its
   fidelity proof, which pins the applied RESULT rather than the instructions. This block states
   no expected insertion count here, because the commit copies THIS BLOCK and the count
   therefore moves with every edit to it (item 16, R-0656). Report the number YOU read with
   `git show --numstat`, and stop only if yours reaches 500.
C1b the booking, ONE commit: `.agent/plan.md` := plan.md; `.agent/live_review.md` := its
   `f9cb2f62` bytes + ledger.md. The reviewer's arithmetic is 18 insertions — 2 for the ledger
   append and 16 for the plan REWRITE, which is the numstat of the rewrite and not the payload's
   46 lines, because the new plan and the one it replaces share lines. Report the number YOU
   read and say so where it differs.
C2 the disposition —
   `git apply --include=packages/orchestration/autonomy_loop.py
    --include=packages/orchestration/event_names.py
    .remedy-wt/f277-r4-payloads/f277-r4.diff`
   then commit. Expected insertions 14; report the number YOU read.
C3 the tests, and the R-1013 repair —
   `git apply --include=tests/orchestration/test_autonomy.py
    --include=tests/orchestration/test_event_names.py
    .remedy-wt/f277-r4-payloads/f277-r4.diff`
   then commit. Expected insertions 83; report the number YOU read.
C4 the resolution, ONE commit whose whole change set is `.agent/live_review.md` := its C1b bytes
   + resolution.md. It comes AFTER C3 because the paragraph it appends states that C3 landed the
   repair, and a `Done:` written before its fix is a false line in a file nothing can correct.
   Expected insertions 2; report the number YOU read.
C5 handoff — rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the Session
   section reading "SESSION 2 of feature F277 · round 4 · rounds so far 4" plus ONE sentence of
   context self-assessment; the per-commit table with `git show --numstat` insertion counts for
   C1a, C1b, C2, C3 and C4; every gate below with its real output and exit code, one line per
   gate; the open-findings count by distinct id; the item-status table; the deviations; and
   `## Next` naming Phase 1 rule 1 first, then the review of round 4, then round 5's disposal of
   `patch_intent_reverted`, and "Operator questions open: <the count of `### Q` headings you read
   from `.agent/operator_questions.md`>". Then
   `git push -u origin feature/f277-machine-contracts`. Open NO pull request.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as a deviation and
   applied anyway; it is never edited and no slice is retyped.
2. Change set: the paths the Bundle names, and nothing else. In particular do NOT edit
   `docs/roadmap/STATUS.md`, `README.md`, `docs/roadmap/features/T2_F277.md`,
   `.agent/decisions.md` or `.agent/prose_slips.md` — the feature file's Built State is written
   by the closure sequence, and no `docs/roadmap/**` path is in this round's change set, so
   `tests/docs/` is not among the gates.
3. The commit sequence is C1a, C1b, C2, C3, C4, C5: no extra commit, none dropped, none
   reordered. C1b precedes C2 so `.agent/plan.md` is current before the first product commit
   (item 23) and so the registration of R-1013 lands before its repair (§4 item 4). C2 precedes
   C3 because the tests exercise the gate C2 changes. C4 follows C3 for the reason C4 states.
4. An insertion count is read with `git show --numstat`, whose `+` column is the reading DECISION
   F104 D1 fixes for the 500-line cap; `git commit`'s own terminal summary applies rename
   detection and is NOT that reading — round 3 measured the two at 23 and 48 for one commit, so
   report which you used. Read it for EVERY commit, C1a and C1b included. If any commit reaches
   500 insertions by that reading, STOP and report — no oversize exception is declared for this
   feature. The four expected values above are the reviewer's arithmetic; where yours differs,
   report YOURS and say so, and stop only if yours reaches 500.
5. Never force-push, never rewrite history, never delete a branch, never merge. Run NO `gh`
   command at all this round.
6. Read `.agent/STOP` from disk before the first commit. If it exists, write the handoff and end,
   doing nothing else.
7. The shell may deny `VAR=x cmd`, `cp` and some compound commands; copy bytes and read exit
   codes with small python scripts under `.remedy-wt/f277-r4-payloads/`. Prefer `git -C <path>`
   over `cd <path> && git`.
8. `.remedy-wt/` is gitignored scratch. Never run `git clean -x`. The directories whose names
   begin `f277-` under `.remedy-wt/` are the reviewer's and are not yours to delete;
   `f277-r4-dry` is a registered worktree of this repository and removing it is a
   history-touching act this block does not order.
9. Never weaken an assertion or delete a test. A red gate, or an ambiguity DECISION F277 D4 does
   not settle, stops the round: commit nothing half-done and report.
10. The full suite does NOT run this round (amend0917-throughput rule 1). It runs once per
    feature, in the closure sequence's integration-gate round.
11. Commit messages "F277 R4 C<n>: <summary>", a blank line, then
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when — the six gates below, each EXECUTED, each reporting its REAL output and exit code.
"Green" as a word is a finding. G1 to G5 run at C4, before C5.

G1 TRANSPORT AND STATE. One python check printing an explicit True or False per reading.
   (a) Each `.agent/authored/f277-r4-*` file equals its payload on disk byte for byte. Report
       the number of such files YOU measured rather than taking a count from this block.
   (b) THE RECORD APPENDS, in full byte forensics, which the gate budget reserves for
       `.agent/live_review.md`. For each of the two appends — the file at C1b against its
       `f9cb2f62` bytes plus ledger.md, and the file at C4 against its C1b bytes plus
       resolution.md — take reading (a), byte equality of pre plus payload against post; reading
       (b), an INDEPENDENT structural reader that splits the post file on blank lines and
       compares its LAST N units, in order, against the payload's N paragraphs, where N is a
       number the script COUNTS from the payload and never one this block states; and a NEGATIVE
       CONTROL that flips one byte inside the FIRST appended paragraph and confirms BOTH readings
       reject it. Each payload's leading newline is the blank SEPARATOR between record entries
       and not a paragraph of its own; a structural reader that counts it as content reads False
       against a file that is byte-for-byte correct, which is the script bug round 3 declared.
       Decode with `errors="replace"` for the structural reading only, so a flip landing on a
       UTF-8 continuation byte reports a rejection rather than a traceback; reading (a) stays on
       raw bytes.
   (c) Byte equality only: `.agent/plan.md` at C1b equals plan.md's bytes.
   (d) THE OPEN SET BY DISTINCT ID, counted as the distinct ids matching `^- R-\d+ — ` minus
       those matching `^Done: R-\d+ — `, at three commits: `f9cb2f62`, C1b and C4. Report all
       three numbers and whether `R-1013` is among the open ids at each.
   Report the number of readings taken and that every one is True. SEPARATELY, report the SAVED
   BLOCK's own line count and sha256 beside the line count and digest this block's PAYLOADS
   section gives for `block.md` (R-0954).

G2 CODE TRANSPORT — the committed tree is the tree the reviewer tested, and this gate is the
   ONLY proof the diff arrived intact, since no copy of it is committed. At C3, `git rev-parse`
   over the four paths below must print exactly these four blob ids in this order:
     packages/orchestration/autonomy_loop.py     30fda566147ad93ce50b2401096e343947baa286
     packages/orchestration/event_names.py       ccebb8ec4eaa61a78a3539a9fd21a1d9da5b2cd4
     tests/orchestration/test_autonomy.py        78a296da3d49ba1bc27f014b4804a6ad00fa1371
     tests/orchestration/test_event_names.py     8489ba8c18dde542e0f072cbd64604cd3cacc5ca
   Also report `git diff --name-only <C1b> <C3>` in full: it must name exactly those four paths
   and no other. Report that list and its length.

G3 THE TARGETED SUITE, in the primary checkout, serial (no `-n`), at C3:
     python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_autonomy.py
       tests/orchestration/test_event_names.py tests/test_autonomy_readiness.py
       tests/storage/test_persistence.py tests/orchestration/test_repository_snapshot.py
       tests/orchestration/test_stop_reasons.py tests/test_no_orphan_modules.py
       tests/cli/test_golden_path.py
   Report the summary line and the exit code. It must read 0 failed at exit 0. The list is the
   two test files this round touches plus the files nearest the two production modules it edits —
   `test_persistence.py` is the only other caller of `run_autonomy_loop`,
   `test_repository_snapshot.py` owns `build_snapshot_truth`, `test_autonomy_readiness.py` owns
   the signal the gate now reads, `test_stop_reasons.py` owns the blockers the same loop derives,
   and `test_no_orphan_modules.py` is the import-reachability guard; `tests/cli/test_golden_path.py`
   is the canary.

G4 LINT, at C3:
     python3 -m ruff check packages/orchestration/autonomy_loop.py
       packages/orchestration/event_names.py tests/orchestration/test_autonomy.py
       tests/orchestration/test_event_names.py
   must print "All checks passed!". Pass ONLY these four paths.

G5 MUTATION RED-PROOFS, in ONE disposable worktree under `.remedy-wt/` created at C3 and removed
   as this gate's last action. Name it `.remedy-wt/f277-r4-g5` and do NOT reuse any existing
   directory there. Run every command from the worktree root with
     python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_autonomy.py
       tests/orchestration/test_event_names.py
   Take the UNMUTATED CONTROL FIRST and report its exit code: it must be 0. Then apply each
   mutation below, one at a time, each restored byte-identically before the next; before each,
   COUNT the occurrences of the exact bytes the recipe replaces in the named file and report the
   count, which must be 1, because that uniqueness is what makes the restore safe. Report each
   run's exit code and its failing node ids, and report a mutation that stays green AS GREEN.
   (a) THE GATE READS THE PHANTOM EVENT AGAIN. In `packages/orchestration/autonomy_loop.py`,
       replace the single line
       `        if not (signals or {}).get("verified_snapshot", False):` with
       `        if not any(e.get("event") == "snapshot_created" for e in events):`.
       Expected: FAIL, naming `test_a_durably_verified_snapshot_unblocks_the_level`,
       `test_the_retired_event_no_longer_decides_anything` and
       `test_every_read_event_name_is_declared`.
   (b) THE LOOP STOPS HANDING THE GATE THE SIGNALS IT COMPUTED. In the same file, delete the
       single line `            report.signals,` from the `_decide` call in
       `run_autonomy_loop`. This is the wiring half: the parameter defaults to None, so the gate
       blocks forever and looks on the page exactly like the defect this round removes.
       Expected: FAIL, naming `test_the_loop_hands_the_gate_the_signals_it_computed`.
   After the two, show that the touched file is byte-identical to before (report its sha256),
   run the UNMUTATED selection once more and report that it is exit 0 again, remove the worktree,
   and report `git worktree list` in full.

G6 PUSH AND TREE. `git push -u origin feature/f277-machine-contracts` after C5; then
   `git status --porcelain`, which must be EMPTY; then `ls .agent/STOP`, which must be absent;
   then `git worktree list` in full, which must show the primary checkout, the two
   `remedy/job-*` worktrees, and the reviewer's `.remedy-wt/f277-r4-dry`, and no other. These
   readings necessarily POSTDATE the commit that writes the handback, so they belong to your
   final report and not to the handoff's own text (item 31).

Handback
Rewrite `.agent/handoff.md` as C5 describes, then report. The handback names every gate with one
line of its real output, declares every deviation, and carries the item-status table. If any gate
is red, say so plainly WITH the output: a red gate honestly reported ends the round cleanly and
is worth far more than a green word.
