STEP R2 T001 — F277 Machine contracts: event vocabulary, JSON envelope, exit codes
Session 2 of F277 · round 2 · base `9114721f` (the tip of `feature/f277-machine-contracts`,
round 1's C4). This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 1's PASS verdict, register and resolve finding R-1012, and dispose of three of the
six names in `READ_ONLY_EVENT_NAMES` exactly as the reviewer's dry run disposed of them:
`worker_adapters_listed` deleted with its zero-caller reader, `approval_decision`'s reader
repointed at the two names the repository really writes, and `patch_intent_reverted`'s dead
`revert_snapshot` signal removed while the brain's `revert_capable` starts reading the
authoritative `verified_snapshot`. The quarantine goes from six names to four.

Read first, completely: AGENTS.md; `docs/roadmap/features/T2_F277.md`; the payload
`decisions.md`, which is DECISION F277 D4 and is this round's spec — where this block is
terser, D4 rules.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f277-r2-payloads/`. Verify each
line count and sha256 BEFORE use and report both readings; any mismatch stops the round. Apply
byte-exact, never by retyping.
  ledger.md        lines 4   sha256 a65b69929d6db4d5102323292beefc26d72c643f8b51a3843a339b42d8ba4d16
  resolution.md    lines 2   sha256 12fe353cd6aeac3e4b8dba5f2e7e399b4bab23fa2f5e77c2ec6c0a09ebcd0197
  decisions.md     lines 65  sha256 e0e9f0e980c8eb91696a7e2b5d13d840cfb3bbafdbdacae35b3e803a0850790a
  plan.md          lines 47  sha256 1a81c26db4c044236d95c5a24c55e736f4d60b39a67105630d08ad63e7ed7903
  prose_slips.md   lines 1   sha256 e0ddce24d119ad5b638c7a1fa4db0b5e2625b361502c1693422a1f8376570405
  block.md         this block; save it and report its line count and digest (R-0954)
CODE — ONE diff the reviewer produced in its own dry-run worktree at `9114721f`, applied there,
tested there and red-proved there. Verify its digest, then apply it in TWO disjoint slices with
the `--include` lists below, always from its scratch path. Do not retype a hunk, do not edit
one, do not copy the diff into the repository, and never apply it whole — C2 and C3 are separate
commits because the production change and its tests are separate reviewable units.
  `.remedy-wt/f277-r2-payloads/f277-r2.diff`
    lines 260  sha256 fa582c9c173cf64b581cf8b5c98d09b91992a9b1b3d83b95c7bb618706426f96

SHAPE OF EACH STATE PAYLOAD, tested mechanically by the reviewer at `9114721f`, one reading per
pair, the label derived from that reading's own output on the same line (item 15):
  `.agent/live_review.md` contains ledger.md — false, so APPEND
  `.agent/live_review.md` contains resolution.md — false, so APPEND
  `.agent/decisions.md` contains decisions.md — false, so APPEND
  `.agent/prose_slips.md` contains prose_slips.md — false, so APPEND
  `.agent/plan.md` contains plan.md — false, so REWRITE
Every pair reads false, so all are NEW bytes and NO FROM-count proof is owed on any of them.
ledger.md, resolution.md and decisions.md each begin with a newline, the blank separator their
targets use between entries; prose_slips.md does not, because that file is one line per slip.
There is no STATUS.md edit this round and no live_review re-head.

Bundle, in commit order
C1a the payload copies, ONE commit whose whole change set is new files under `.agent/authored/`:
   a byte copy of each payload listed above, `block.md` included, as
   `.agent/authored/f277-r2-<name>` — keeping each payload's own file name after the prefix. The
   code diff is NOT copied and is NOT part of this or any commit; G2's blob-id gate is its
   fidelity proof, which pins the applied RESULT rather than the instructions. This block states
   no expected insertion count here, because the commit copies THIS BLOCK and the count
   therefore moves with every edit to it (item 16, R-0656). Report the number YOU read with
   `git show --numstat`, and stop only if yours reaches 500.
C1b the booking, ONE commit: `.agent/plan.md` := plan.md; `.agent/live_review.md` := its
   `9114721f` bytes + ledger.md; `.agent/decisions.md` := its `9114721f` bytes + decisions.md;
   `.agent/prose_slips.md` := its `9114721f` bytes + prose_slips.md. Expected insertions 117 by
   `git show --numstat`; report the number YOU read.
C2 the three dispositions —
   `git apply --include=packages/orchestration/autonomy_readiness.py
    --include=packages/orchestration/project_brain.py
    --include=packages/orchestration/stop_reasons.py
    --include=packages/orchestration/event_names.py
    .remedy-wt/f277-r2-payloads/f277-r2.diff`
   then commit. Expected insertions 15; report the number YOU read.
C3 the tests, and the R-1012 repair —
   `git apply --include=tests/orchestration/test_event_names.py
    --include=tests/orchestration/test_stop_reasons.py
    --include=tests/test_autonomy_readiness.py
    .remedy-wt/f277-r2-payloads/f277-r2.diff`
   then commit. Expected insertions 125; report the number YOU read.
C4 the resolution, ONE commit whose whole change set is `.agent/live_review.md` := its C1b bytes
   + resolution.md. It comes AFTER C3 because the paragraph it appends states that C3 landed the
   repair, and a `Done:` written before its fix is a false line in a file nothing can correct.
   Expected insertions 2; report the number YOU read.
C5 handoff — rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the Session
   section reading "SESSION 2 of feature F277 · round 2 · rounds so far 2" plus ONE sentence of
   context self-assessment; the per-commit table with `git show --numstat` insertion counts for
   C1a, C1b, C2, C3 and C4; every gate below with its real output and exit code, one line per
   gate; the open-findings count by distinct id; the item-status table; the deviations; and
   `## Next` naming Phase 1 rule 1 first, then the review of round 2, then round 3's writer for
   `command_discovery_completed`, and "Operator questions open: <the count of `### Q` headings
   you read from `.agent/operator_questions.md`>". Then
   `git push -u origin feature/f277-machine-contracts`. Open NO pull request.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as a deviation and
   applied anyway; it is never edited and no slice is retyped.
2. Change set: the paths the Bundle names, and nothing else. In particular do NOT edit
   `docs/roadmap/STATUS.md`, `README.md` or `docs/roadmap/features/T2_F277.md` — the feature
   file's Built State is written by the closure sequence, and no `docs/roadmap/**` path is in
   this round's change set, so `tests/docs/` is not among the gates.
3. The commit sequence is C1a, C1b, C2, C3, C4, C5: no extra commit, none dropped, none
   reordered. C1b precedes C2 so `.agent/plan.md` is current before the first product commit
   (item 23) and so the registration of R-1012 lands before its repair (§4 item 4). C2 precedes
   C3 because the tests assert the behaviour C2 creates. C4 follows C3 for the reason C4 states.
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
   codes with small python scripts under `.remedy-wt/f277-r2-payloads/`. Prefer `git -C <path>`
   over `cd <path> && git`.
8. `.remedy-wt/` is gitignored scratch. Never run `git clean -x`. The directories
   `.remedy-wt/f277-r1-payloads/`, `.remedy-wt/f277-r2-dry/` and `.remedy-wt/f277-s2/` are the
   reviewer's and are not yours to delete; `f277-r2-dry` is a registered worktree of this
   repository and removing it is a history-touching act this block does not order.
9. Never weaken an assertion or delete a test. A red gate, or an ambiguity DECISION F277 D4 does
   not settle, stops the round: commit nothing half-done and report.
10. The full suite does NOT run this round (amend0917-throughput rule 1). It runs once per
    feature, in the closure sequence's integration-gate round.
11. Commit messages "F277 R2 C<n>: <summary>", a blank line, then
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when — the six gates below, each EXECUTED, each reporting its REAL output and exit code.
"Green" as a word is a finding. G1 to G5 run at C4, before C5.

G1 TRANSPORT AND STATE. One python check printing an explicit True or False per reading.
   (a) Each `.agent/authored/f277-r2-*` file equals its payload on disk byte for byte. Report
       the number of such files YOU measured rather than taking a count from this block.
   (b) THE RECORD APPENDS, in full byte forensics, which the gate budget reserves for
       `.agent/live_review.md` and `.agent/decisions.md`. For each of the three appends —
       `.agent/live_review.md` at C1b against its `9114721f` bytes plus ledger.md,
       `.agent/decisions.md` at C1b against its `9114721f` bytes plus decisions.md, and
       `.agent/live_review.md` at C4 against its C1b bytes plus resolution.md — take reading
       (a), byte equality of pre plus payload against post; reading (b), an INDEPENDENT
       structural reader that splits the post file on blank lines and compares its LAST N units,
       in order, against the payload's N paragraphs, where N is a number the script COUNTS from
       the payload and never one this block states; and a NEGATIVE CONTROL that flips one byte
       inside the FIRST appended paragraph and confirms BOTH readings reject it. Decode with
       `errors="replace"` for the structural reading only, so a flip landing on a UTF-8
       continuation byte reports a rejection rather than a traceback; reading (a) stays on raw
       bytes.
   (c) Byte equality only: `.agent/plan.md` at C1b equals plan.md's bytes; `.agent/prose_slips.md`
       at C1b equals its `9114721f` bytes plus prose_slips.md's bytes.
   (d) THE OPEN SET BY DISTINCT ID, counted as the distinct ids matching `^- R-\d+ — ` minus
       those matching `^Done: R-\d+ — `, at three commits: `9114721f`, C1b and C4. Report all
       three numbers and whether `R-1012` is among the open ids at each.
   Report the number of readings taken and that every one is True. SEPARATELY, report the SAVED
   BLOCK's own line count and sha256 beside the line count and digest this block's PAYLOADS
   section gives for `block.md` (R-0954).

G2 CODE TRANSPORT — the committed tree is the tree the reviewer tested, and this gate is the
   ONLY proof the diff arrived intact, since no copy of it is committed. At C3, `git rev-parse`
   over the seven paths below must print exactly these seven blob ids in this order:
     packages/orchestration/autonomy_readiness.py  6bf0866a32ab7afc53b0c62de671abe3ad11533d
     packages/orchestration/event_names.py         c7ea49597a894652e9bbb16d4e806c70776a81da
     packages/orchestration/project_brain.py       e1fc35c8a4de6f34042f5994f6d2ebc2ab905f78
     packages/orchestration/stop_reasons.py        1b56d322a8f8f515965473b64ab26503416522f4
     tests/orchestration/test_event_names.py       f812ba15e101dbfb8e6333e172e3c8e11ca79f64
     tests/orchestration/test_stop_reasons.py      62219863ce4aacf0f052985d549609ec51fef935
     tests/test_autonomy_readiness.py              33926504985c02943e2bb021744d75f2f8045900
   Also report `git diff --name-only <C1b> <C3>` in full: it must name exactly those seven paths
   and no other. Report that list and its length.

G3 THE TARGETED SUITE, in the primary checkout, serial (no `-n`), at C3:
     python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_event_names.py
       tests/orchestration/test_stop_reasons.py tests/test_autonomy_readiness.py
       tests/test_project_brain.py tests/orchestration/test_source_apply.py
       tests/test_memory_learn.py tests/orchestration/test_autonomy.py tests/test_run_log.py
       tests/orchestration/test_change_set.py tests/cli/test_golden_path.py
   Report the summary line and the exit code. It must read 0 failed at exit 0. The list is every
   test file this round touches plus the file nearest each production module it edits
   (`test_project_brain.py`, `test_source_apply.py` and `test_change_set.py` for the three
   surviving readers of `patch_intent_reverted`, `test_memory_learn.py` and `test_autonomy.py`
   for the readiness and stop-reason consumers); `tests/cli/test_golden_path.py` is the canary.

G4 LINT, at C3:
     python3 -m ruff check packages/orchestration/autonomy_readiness.py
       packages/orchestration/project_brain.py packages/orchestration/stop_reasons.py
       packages/orchestration/event_names.py tests/orchestration/test_event_names.py
       tests/orchestration/test_stop_reasons.py tests/test_autonomy_readiness.py
   must print "All checks passed!". Pass ONLY these seven paths.

G5 MUTATION RED-PROOFS, in ONE disposable worktree under `.remedy-wt/` created at C3 and removed
   as this gate's last action. Name it `.remedy-wt/f277-r2-g5` and do NOT reuse any existing
   directory there. Run every command from the worktree root with
     python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_event_names.py
       tests/orchestration/test_stop_reasons.py tests/test_autonomy_readiness.py
   Take the UNMUTATED CONTROL FIRST and report its exit code: it must be 0. Then apply each
   mutation below, one at a time, each restored byte-identically before the next; before each,
   COUNT the occurrences of the exact bytes the recipe replaces in the named file and report the
   count, which must be 1, because that uniqueness is what makes the restore safe. Report each
   run's exit code and its failing node ids, and report a mutation that stays green AS GREEN.
   (a) In `packages/orchestration/stop_reasons.py`, replace the single line
       `                      a.get("event") in _DECIDED` with
       `                      a.get("event") == "approval_decision"`. Expected: FAIL, naming
       `test_an_approved_intent_no_longer_blocks` and
       `test_every_read_event_name_is_declared` among its failures.
   (b) Two edits, applied together as ONE mutation and reverted together. In
       `packages/orchestration/autonomy_readiness.py`, insert directly above the single line
       `        "verified_snapshot": _has_verified_snapshot(job, data_dir),` the three lines
       `        "revert_snapshot": any(`,
       `            e.get("event") == "patch_intent_reverted" for e in events`,
       `        ),`; and in `packages/orchestration/project_brain.py` replace the single line
       `                "revert_capable": sigs.get("verified_snapshot", False),` with
       `                "revert_capable": sigs.get("revert_snapshot", False),`. Expected: FAIL,
       naming `test_a_revert_event_alone_does_not_make_the_brain_revert_capable` and
       `test_the_signal_dict_no_longer_carries_the_phantom`.
   (c) In `packages/orchestration/autonomy_readiness.py`, insert directly above the single line
       `def _has_agent_loop(events: list[dict[str, Any]]) -> bool:` a function
       `def _has_worker_adapters(events: list[dict[str, Any]]) -> bool:` whose body is
       `    return any(e.get("event") == "worker_adapters_listed" for e in events)`, followed by
       two blank lines. Expected: FAIL, naming `test_every_read_event_name_is_declared`.
   After the three, show that each of the three touched files is byte-identical to before
   (report a sha256 per file), run the UNMUTATED selection once more and report that it is exit
   0 again, remove the worktree, and report `git worktree list` in full.

G6 PUSH AND TREE. `git push -u origin feature/f277-machine-contracts` after C5; then
   `git status --porcelain`, which must be EMPTY; then `ls .agent/STOP`, which must be absent;
   then `git worktree list` in full, which must show the primary checkout, the two
   `remedy/job-*` worktrees, and the reviewer's `.remedy-wt/f277-r2-dry`, and no other. These
   readings necessarily POSTDATE the commit that writes the handback, so they belong to your
   final report and not to the handoff's own text (item 31).

Handback
Rewrite `.agent/handoff.md` as C5 describes, then report. The handback names every gate with one
line of its real output, declares every deviation, and carries the item-status table. If any gate
is red, say so plainly WITH the output: a red gate honestly reported ends the round cleanly and
is worth far more than a green word.
