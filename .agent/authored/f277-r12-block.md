STEP R12 — F277: the scope report lands, F283 is registered, F277's Built State is written

GOAL
Book round 11's PASS and two reviewer slips, record DECISION F277 D10 and the operator
question it owes, register F283 in ONE ledger-atomic commit, and give
`docs/roadmap/features/T2_F277.md` the Built State its closure precondition 4 requires.
F277 reached the standing seven-session soft limit at round 11 of 25, so by operator
amendment amend0905-throughput the session writes the scope report and EXECUTES the
split-and-close default: F277 closes on T001 and T002 complete and T003 in part, and the
rest becomes F283, placed directly after its parent under amend0906-split-placement.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep `.agent/plan.md` current, keep the tree
clean, push at the end, rewrite `.agent/handoff.md`. You never issue a verdict.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r12-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r12-scratch/`   YOURS. Every log, exit-code capture, temporary script
      and note goes here. Both are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR — do not spend turns rediscovering them.
Denied outright: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`, `cp`, process
substitution `<(...)`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. The Bash tool does not surface a non-zero exit on its own, so capture every
gate's REAL code as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. For anything involving
counting, hashing, byte arithmetic or copying, use `python3 -c` or `python3 - <<'PY'` —
`shutil.copyfile` is how you copy. That route is the reliable one; reach for it first.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty and `git branch --show-current` must read
   `feature/f277-machine-contracts` at `67b0972d`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r12-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all eleven under `.remedy-wt/f277-r12-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| context.md | 49 | 2621 | c40f9910340ca109fa07c7963e0fe9dd58a71c0c6054b218cc182c200b96c69e |
| decisions.md | 65 | 4708 | ce012695e0bebf539b6c9db2a9e8fcf00734d6288d4611e4901ac54a6d494a17 |
| f277-file.diff | 92 | 6665 | 99c570b0f69a313e9c792d5d9a007c7d444af33eb6d048fc8ed1b1c5e4fa43b2 |
| f283.md | 90 | 5472 | 2b6ff2b34cf82b9452be409ef6cf4da7c63ec379e42431edc2f43c76777fee39 |
| ledger.md | 2 | 7273 | 0c34a0770d977a17a9ed56c9f23a126f235a0ac506bf72da8deda48208d729fd |
| pin.diff | 17 | 836 | 37241db16f88a34a44c367d775313bbd764a66f2972b683e22268b648b1d39b6 |
| plan.md | 46 | 2425 | ce8fe437a82fb00cc24fcfc5a50ded844cfc4605aa579e9a0d562704a5d46396 |
| questions.md | 39 | 2789 | ade37891181ba543edeaa808c17ba4ea7fe6a477b0db5fedda9694305d99a97c |
| readme.diff | 19 | 655 | e207d8e0fce50336115a14f66a1901d01cb5f8f87e8325803da0b1de0f4fdbaa |
| slips.md | 2 | 2365 | 0ea03bac3f8c11ccb03e4c1f7b7156c87d59f469d486d09c01a620d37990b604 |
| status.diff | 11 | 1371 | 5881978ca6ec288ff1677ad1416c581509b873ff886e838fb7e20bb228e63b2a |

APPENDS, each beginning with a single newline that is the record separator:
`ledger.md`, `decisions.md` and `questions.md`. `slips.md` is an APPEND of TWO LINES with
NO leading newline, because `.agent/prose_slips.md` holds one line per entry and no blank
line between them. REWRITES: `plan.md` and `context.md`. `f283.md` is a WHOLE NEW FILE and
is written to `docs/roadmap/features/T2_F283.md`; it is not a diff and there is nothing to
apply. The four `.diff` files go on with `git apply`; every one was generated from the tree
at `67b0972d` and every one was dry-run with `git apply --check` by the reviewer at exit 0.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order

C1a — copy this block and all eleven payloads into `.agent/authored/`
  `.agent/authored/f277-r12-block.md` := this block, byte-for-byte, and one
  `.agent/authored/f277-r12-<name>` per payload, keeping each payload's own file name
  (so `f277-r12-context.md`, `f277-r12-f277-file.diff`, and so on for all eleven).
  Subject: `F277 R12 C1a: copy round 12 payloads into .agent/authored/`
  Expected insertions: this block's own line count plus 432. No fixed number is stated,
  because the block's count moves with every edit to the block itself. Report what you
  measure; it is far under 500 either way.

C1b — book round 11's PASS, the two slips, the DECISION and the operator question, and
      rewrite the plan and the context
  `.agent/live_review.md`       += ledger.md     (append, +2)
  `.agent/prose_slips.md`       += slips.md      (append, +2)
  `.agent/decisions.md`         += decisions.md  (append, +65)
  `.agent/operator_questions.md` += questions.md (append, +39)
  `.agent/plan.md`              := plan.md       (rewrite, +46/-49)
  `.agent/context.md`           := context.md    (rewrite, +49/-42)
  Subject: `F277 R12 C1b: book round 11's PASS, DECISION D10 and the split scope report`
  EXPECTED INSERTIONS: 203 by `git show --numstat` — 2+2+65+39+46+49. That is the reading
  DECISION F104 D1 fixes; `git commit`'s terminal summary applies rename detection and may
  print a different pair. If your measurement differs from 203, report the number you
  measured and say so — do not adjust the payloads to reach it.
  WHY THE OPERATOR QUESTION IS HERE AND NOT IN THE HANDBACK COMMIT: amend0911-feedback
  rule C says the session writes that file "in its handback commit through the worker",
  and amend0917-throughput rule 4 says the handback is its own commit and that a round's
  DECISION lands in the one bookkeeping commit. The entry is this round's DECISION in
  question form, so it travels with it; the rule C obligation the two share is that the
  WORKER writes it and the reviewer stays read-only, which this satisfies. Declare the
  reading in your deviations so the next gate sees it was chosen and not missed.

C2 — REGISTER F283, ledger-atomically: this commit carries all four edits or none
  `docs/roadmap/features/T2_F283.md` := f283.md    (new file, +90; `git add` it)
  `docs/roadmap/STATUS.md`           += status.diff (the F283 line, directly after F277's)
  `README.md`                        += readme.diff (the ledger total and the Tier 2 cell)
  `tests/docs/test_docs_consistency.py` += pin.diff (`TOTAL_FEATURES` and its comment)
  Subject: `F277 R12 C2: register F283 — machine contracts part two: feature file, STATUS
  line, pin 283, README counters`
  Expected insertions: 99 — 90 for the new file, 1 for the STATUS line, 2 for README, 6
  for the pin and its comment.
  The atomicity is not style: `tests/docs/test_docs_consistency.py` pins the feature count,
  the README total and the STATUS ledger against each other, so any THREE of these four
  edits committed alone leaves the tree red. Commit them together.

C3 — F277's own feature file: strike what moved, write the Built State
  `git apply .remedy-wt/f277-r12-payloads/f277-file.diff`, touching only
  `docs/roadmap/features/T2_F277.md`.
  Subject: `F277 R12 C3: strike the moved Acceptance bullets and write F277's Built State`
  Expected insertions: 71.

C4 — the handback
  Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, then
  `git push -u origin feature/f277-machine-contracts`.
  Subject: `F277 R12 C4: rewrite handoff for round 12`

CONSTRAINTS
1. Never edit a payload and never retype one. Each `.diff` goes on with `git apply`; run
   `git apply --check` first for each and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. Do not touch any file this block does not name. In particular: NO file under
   `packages/` or `apps/`, no test file other than
   `tests/docs/test_docs_consistency.py`, and no command-group migration — the remaining
   groups belong to F283 now and are not this round's to spend.
4. If a gate goes red, STOP. Do not repair the reviewer's slice and do not guess which
   half of a disagreement is wrong. Commit and push what is verified, write an honest
   handoff under AGENTS.md "If Blocked", and hand back. Round 8 did exactly that.
5. `.agent/plan.md` must read 46 lines after C1b, under the 50-line rule of AGENTS.md.
6. There is NO mutation red-proof this round and that is deliberate, not an omission:
   the round's change set holds no production code, so §3's standing red-proof obligation
   has nothing to bite on. G3's two red controls are the reviewer's, already run, and
   their readings are stated in G3 so you can compare rather than repeat them.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the eleven payload files, report the line count, byte count and sha256
     you measured against the PAYLOADS table above. Thirty-three readings, all equal.
 (b) For each of the twelve `.agent/authored/f277-r12-*` copies at C1a — the eleven
     payload copies and the block copy — compare it byte-for-byte with its source under
     `.remedy-wt/f277-r12-payloads/` (the block copy against
     `.remedy-wt/f277-r12-block.md`). Report one reading per copy; all True.
 (c) The four appends at C1b. For each of `.agent/live_review.md`, `.agent/prose_slips.md`,
     `.agent/decisions.md` and `.agent/operator_questions.md`: the file's bytes at
     `67b0972d` plus the payload's bytes equal the file's bytes at C1b. Report pre, payload,
     post and post-minus-pre for each; all True. The reviewer measured the four pre values
     at `67b0972d` as 439654, 342200, 1787112 and 2572 in that order — report yours beside
     them. Then ONE negative control, on `.agent/live_review.md` only: flip a single bit
     inside the appended region and show the reading returns False.
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte at 46 lines, and
     `.agent/context.md` at C1b equals `context.md` byte-for-byte at 49 lines. Report both
     sha256 pairs and both line counts.
 (e) The open set by distinct id in `.agent/live_review.md` — ids matching `^- R-\d+ — `
     minus ids matching `^Done: R-\d+ — ` — is 20 at `67b0972d` and 20 at C1b. Report both
     numbers, not a claim that they match. Round 12 registers and resolves nothing.

G2 THE REGISTRATION IS LEDGER-ATOMIC
 `git diff --name-only <C1b> <C2>` must name exactly these four paths and no fifth:
 `README.md`, `docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F283.md` and
 `tests/docs/test_docs_consistency.py`. Report the list and its length. If
 `docs/roadmap/features/T2_F283.md` is missing from it you forgot to `git add` the new
 file — that is the failure mode this gate is shaped to catch. Then report, from the tree
 at C2: the value of `TOTAL_FEATURES`, the `N of M registered items accepted` line from
 `README.md`, the README Tier 2 table row, and the two STATUS lines for F277 and F283 with
 F283's immediately following F277's and both under the same `## Tier 2` heading.

G3 THE DOCS AND STATE-CONTRACT GATE — in the primary checkout, at C3:
```
python3 -m pytest -q -p no:cacheprovider tests/docs/ \
  tests/orchestration/test_roadmap_index.py tests/orchestration/test_test_runner.py \
  tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py
```
 The selection is the docs ledger, the roadmap index, and every test file that reads
 `.agent/plan.md` or `.agent/context.md` and asserts on their contents — which is what
 makes a state rewrite safe to ship (§4 item 11). The reviewer's dry run, taken in a
 disposable worktree with every slice of this round applied, read `479 passed, 2 skipped`
 at exit 0; with the pin left at 282 it read `3 failed, 476 passed, 2 skipped` at exit 1,
 and with the README total left at 282 `1 failed, 478 passed, 2 skipped` at exit 1, so the
 gate can fail and its green means something. Report the summary line and the exit code.
 Do not run the full suite — amend0917 rule 1 reserves it for the closure round, which is
 the next one.

G4 LINT AND CANARY — `python3 -m ruff check tests/docs/test_docs_consistency.py`, the
 round's only touched Python file, and then `python3 -m pytest tests/cli/test_golden_path.py
 -q`, the standing canary. Report both outputs and both exit codes.

G5 THE ROUND'S WHOLE PATH SET
 `git diff --name-only 67b0972d <C3>` must name exactly these eleven paths: the six
 `.agent/` state files C1b writes, the four C2 paths G2 lists, and
 `docs/roadmap/features/T2_F277.md`, plus the twelve `.agent/authored/f277-r12-*` files
 C1a adds — report the full list and its length, and state for each entry which commit
 introduced it. No path under `packages/` or `apps/` may appear; report that reading as a
 count you measured, not as an assertion.

G6 PUSH AND TREE — after C4: `git push -u origin feature/f277-machine-contracts` and
 report its outcome, then `git status --porcelain` (must be empty) and `git worktree list`
 (must show the primary checkout and the two pre-existing `remedy/job-*` worktrees and
 nothing else).

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find.

THE SESSION NUMBER, WHICH THIS ROUND CORRECTS. Your handback's Session section reads
SESSION 7 of feature F277, round 12. The `Gate:` entries in `.agent/live_review.md` for
rounds 1 to 10 label their reviewing sessions FIRST, SECOND and THIRD; the handoff chain
across the eleven handback commits that carry the field runs SESSION 1 through SESSION 6
continuously, and AGENTS.md makes that field the mandated carrier, so the handoff chain is
right and the ledger's labels undercount by three. Round 12's ledger entry and the second
prose-slip line both record that reconciliation; do not re-derive it, and do not
retroactively edit any landed entry.

AND THIS IS THE SCOPE-REPORT ROUND. Your handback's `## Next` names, in order: Phase 1
rule 1 (read `.agent/STOP` from disk), then the review of round 12, then the closure
sequence of `docs/roadmap/STATUS_closure_protocol.md` — precondition 6's self-use item
planned and run to the approval gate with its defect strings registered, `integrity check`,
then the integration-gate round running the full suite ONCE with its transcript committed
as `.agent/authored/f277-closure-suite.txt`. State the open-findings count and the
operator-questions count, which are 20 and 2.
