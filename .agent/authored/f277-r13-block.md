STEP R13 — F277 closure: the self-use precondition, and the one clause round 12 got wrong

GOAL
Book round 12's PASS and three reviewer slips, repair the single Built State clause that
landed inaccurate under `docs/`, and satisfy closure precondition 6: the self-use queue
holds no pending item, so the generator appends one and the runner takes it to the normal
approval gate. This is the closure sequence of `docs/roadmap/STATUS_closure_protocol.md`,
where a round may be bookkeeping — that exception exists for exactly this stretch.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep `.agent/plan.md` current, keep the tree
clean, push at the end, rewrite `.agent/handoff.md`. You never issue a verdict, and you
never author a finding — you REPORT the self-use run's defect strings verbatim and the
reviewer writes them into the ledger next round.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r13-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r13-scratch/`   YOURS. Every log, exit-code capture, driver script,
      the self-use job file and the run's `dest_dir` go here. Both are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR — do not spend turns rediscovering them.
Denied outright: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`, `cp`, process
substitution `<(...)`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. The Bash tool does not surface a non-zero exit on its own, so capture every
gate's REAL code as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. For anything involving
counting, hashing, byte arithmetic or copying, use `python3 -c` or `python3 - <<'PY'` —
`shutil.copyfile` is how you copy. A `python3 -c` script containing a newline followed by
`#` is rejected; use the heredoc form there. Both `remedy` and `claude` ARE on PATH and
ran for the reviewer this session, so do not assume either is denied — try it once.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty and `git branch --show-current` must read
   `feature/f277-machine-contracts` at `4f335b03`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r13-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all four under `.remedy-wt/f277-r13-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| f277-fix.diff | 16 | 1088 | 932b7f5bb90880a6df7b7b256e2faa9635d7d719ae1705c01efda5b168a517e5 |
| ledger.md | 2 | 7938 | 179d9ace9be680b32048f70d0e24d3aec1074a5b4bcba1bf1d7ca3e072e12bb2 |
| plan.md | 49 | 2578 | 0fa5a9978e86dd44f61bee44d403eed7490d8f2212d7d7d5ecfcfec499011b55 |
| slips.md | 3 | 3493 | cf7071e6bd0d81bd77b1b10d9c6e3b1b50cf02730a1036499a5fae79822d3692 |

`ledger.md` is an APPEND beginning with a single newline that is the record separator.
`slips.md` is an APPEND of THREE LINES with NO leading newline, because
`.agent/prose_slips.md` holds one line per entry and no blank line between them.
`plan.md` is a REWRITE. `f277-fix.diff` goes on with `git apply`; it was generated from the
tree at `4f335b03` and dry-run with `git apply --check` by the reviewer at exit 0. Its pair
was tested mechanically for containment: TO contains FROM: false, so it is a REWRITE and
no FROM-zero count is owed — the corrected clause and the wrong one are disjoint text.
There is no decisions payload and no questions payload this round; `.agent/decisions.md`
and `.agent/operator_questions.md` are not touched.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order

C1a — copy this block and all four payloads into `.agent/authored/`
  `.agent/authored/f277-r13-block.md` := this block, byte-for-byte, and one
  `.agent/authored/f277-r13-<name>` per payload, keeping each payload's own file name.
  Subject: `F277 R13 C1a: copy round 13 payloads into .agent/authored/`
  SIZE, AND IT MATTERS THIS ROUND. The payloads total 70 lines, so this commit's
  insertions are 70 plus this block's own line count, and the 500-insertion cap of
  DECISION F104 D1 binds at 430 block lines. Round 12's mirror commit spent this
  FEATURE'S ONE permitted oversize declaration at 661 insertions, so a second one is a
  Medium finding and not a declaration you may make. Compute `500 minus 70 minus <the
  block line count you measured>` and report that number beside your measured insertions;
  if it is negative, STOP and hand back rather than committing.

C1b — book round 12's PASS and three slips, rewrite the plan
  `.agent/live_review.md` += ledger.md (append, +2)
  `.agent/prose_slips.md` += slips.md  (append, +3)
  `.agent/plan.md`        := plan.md   (rewrite)
  Subject: `F277 R13 C1b: book round 12's PASS and three reviewer slips, rewrite plan`
  EXPECTED INSERTIONS: 2 plus 3 plus the plan rewrite's own DIFF insertions, which the
  reviewer measured with `git diff --numstat` in a disposable worktree at `4f335b03` as
  `28 25 .agent/plan.md`, giving 33 by `git show --numstat`. That is the reading DECISION
  F104 D1 fixes, and it is the DIFF's count and not the payload's 49 lines — the
  distinction round 12 got wrong and the second prose-slip line records. If your
  measurement differs from 33, report the number you measured and say so; do not adjust
  the payload to reach it.

C2 — repair the one Built State clause that landed inaccurate
  `git apply .remedy-wt/f277-r13-payloads/f277-fix.diff`, touching only
  `docs/roadmap/features/T2_F277.md`. The clause said F283 was registered "in the same
  commit that struck them from the Acceptance list"; the registration is `90976846` and
  the strike is `3c3ca820`, two adjacent commits of round 12, and the corrected clause
  names both. This is a repair of a REVIEWER slip, ordered by the reviewer — it is not
  you repairing a slice on your own initiative, which constraint 4 still forbids.
  Subject: `F277 R13 C2: name both commits in the Built State clause round 12 got wrong`
  Expected insertions: 3.

C3 — CLOSURE PRECONDITION 6: the self-use item, generated and run
  Write a driver script under `.remedy-wt/f277-r13-scratch/` and run it. In order:
   (i)   Report `len(packages.orchestration.self_use_queue.pending_self_use_items())`
         BEFORE anything — the reviewer measured 0 at `4f335b03`, every one of the 24
         items carrying a `consumed_by`.
   (ii)  Call `packages.orchestration.self_use_generator.generate_and_append_if_empty()`.
         Report the returned entry's `id`, `title` and `provenance`. The reviewer's
         read-only dry run of `generate_self_use_item()` at `4f335b03` answered `SU-025`,
         `Address ledger finding R-0820`, tier 1 ledger scan. If it answers `None`
         instead, the track is genuinely exhausted: record
         `self-use NONE (queue exhausted)` and skip to (v), which the protocol permits
         explicitly.
   (iii) Report `resolve_self_use_role_config()` in full. The reviewer read
         provider `claude-cli`, model `claude-sonnet-4-6`, effort `medium`. Do NOT pass
         `builder_name`/`reviewer_name`: an unflagged run must resolve the configured
         provider, and passing `"fake"` would defeat the precondition.
   (iv)  Call `packages.orchestration.self_use_runner.run_next_self_use_item(dest_dir,
         repo_path=".")` with `dest_dir` under your scratch directory. Report the job id,
         the returned `JobPlan`'s `state`, its `execution_config`'s provider, and the
         wall clock. `JOB_COMPLETED` and `JOB_BLOCKED` are BOTH real outcomes and neither
         is a failure of this gate — the gate is that the run HAPPENED and was reported.
   (v)   Call `packages.orchestration.self_use_findings.describe_self_use_run_defects(
         plan)` and report EVERY string it returns, verbatim and in order, with its
         length. An empty tuple means the run surfaced nothing to register — say that in
         those words; it does not mean nothing was checked.
  Then commit `scripts/self_use_queue.json` — the generator's append and nothing else.
  Subject: `F277 R13 C3: generate and run the closure's self-use item`
  DO NOT set `consumed_by` on the new item. That edit belongs to the closure commit and
  to no other, because a run that can check itself off is not a gate — the queue file's
  own description says so. Leave it the empty string the generator wrote.

C4 — the handback
  Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, then
  `git push -u origin feature/f277-machine-contracts`.
  Subject: `F277 R13 C4: rewrite handoff for round 13`

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the five `.agent/authored/f277-r13-*` copies, `.agent/live_review.md`,
   `.agent/prose_slips.md`, `.agent/plan.md`, `docs/roadmap/features/T2_F277.md`,
   `scripts/self_use_queue.json` and `.agent/handoff.md`. NO file under `packages/`,
   `apps/` or `tests/`.
4. If a gate goes red, STOP. Do not repair the reviewer's slice and do not guess which
   half of a disagreement is wrong. Commit and push what is verified, write an honest
   handoff under AGENTS.md "If Blocked", and hand back. Round 8 did exactly that. The one
   thing that is NOT a red gate is a self-use run ending `JOB_BLOCKED` or hitting its
   budget — that is a run outcome, you report it and continue.
5. The self-use run writes under `.data/`, under `remedy-job-evidence-*/` and under your
   scratch directory, all three gitignored, and it may create a `remedy/job-*` worktree
   and branch of its own. That is expected, not a leak. What is NOT permitted is leaving
   a tracked file dirty: `git status --porcelain` must be empty at C4.
6. There is NO mutation red-proof this round and that is deliberate: the change set holds
   no file under `packages/` or `apps/`, so §3's standing obligation over production code
   has nothing to bite on. The full suite is NOT run this round either — it is round 14's
   integration gate, once, per amend0917 rule 1.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the four payload files, report the line count, byte count and sha256 you
     measured against the PAYLOADS table above. Twelve readings, all equal.
 (b) For each of the five `.agent/authored/f277-r13-*` copies at C1a — the four payload
     copies and the block copy — compare it byte-for-byte with its source under
     `.remedy-wt/f277-r13-payloads/` (the block copy against
     `.remedy-wt/f277-r13-block.md`). One reading per copy; all True.
 (c) The two appends at C1b. For each of `.agent/live_review.md` and
     `.agent/prose_slips.md`: the file's bytes at `4f335b03` plus the payload's bytes equal
     the file's bytes at C1b. Report pre, payload, post and post-minus-pre for each. The
     reviewer measured the two pre values at `4f335b03` as 446927 and 344565 — report yours
     beside them. Then ONE negative control, on `.agent/live_review.md` only: flip a single
     bit inside the FIRST appended paragraph and show the reading returns False.
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte at 49 lines, under the
     50-line rule of AGENTS.md. Report both sha256s and the line count.
 (e) The open set by distinct id in `.agent/live_review.md` — ids matching `^- R-\d+ — `
     minus ids matching `^Done: R-\d+ — ` — is 20 at `4f335b03` and 20 at C1b. Report both
     numbers, not a claim that they match. Round 13 registers and resolves nothing; the
     self-use defect strings are REPORTED to the reviewer, not registered by you.

G2 THE BUILT STATE CLAUSE
 At C2: report the corrected paragraph's first four lines verbatim from
 `docs/roadmap/features/T2_F277.md`, and report the count of the string
 `registered in the same commit` in that file, which must be 0. Then
 `git diff --name-only <C1b> <C2>` must name exactly `docs/roadmap/features/T2_F277.md`
 and nothing else — report the list and its length.

G3 DOCS AND STATE-CONTRACT — in the primary checkout, at C2:
```
python3 -m pytest -q -p no:cacheprovider tests/docs/ \
  tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py \
  tests/regression/test_resource_safety.py
```
 The selection is the docs ledger plus every test file that reads `.agent/plan.md` or
 `.agent/context.md` and asserts on their contents (§4 item 11). The reviewer's dry run,
 taken in a disposable worktree at `4f335b03` with this round's slices applied, read
 `449 passed, 2 skipped` at exit 0, and with the plan's `## Next Steps` heading renamed it
 read `3 failed, 446 passed, 2 skipped` at exit 1 — so the gate can fail and its green
 means something. The primary checkout typically runs the two the worktree skips, so a
 slightly higher passed count with the same total collected is expected rather than a
 discrepancy. Report the summary line and the exit code.

G4 THE SELF-USE PRECONDITION — report, as one block, every reading C3 items (i) to (v)
 name: the pending count before, the generated entry's id, title and provenance, the
 resolved role config, the job id, the run's state, the provider that actually ran, the
 wall clock, and every string `describe_self_use_run_defects` returned with the tuple's
 length. Report the pending count AFTER the run as well, and the value of the new item's
 `consumed_by`, which must be the empty string. If the run raised, report the exception
 type and its full message rather than a summary — a raised `SelfUseRunError` is a
 reportable outcome and this gate is met by reporting it honestly.

G5 CANARY AND TREE HYGIENE — `python3 -m pytest tests/cli/test_golden_path.py -q`, the
 standing canary; report its output and exit code. Then report `git worktree list` and
 `git branch --list 'remedy/job-*'` BOTH before C3 and after it, with the counts. The
 reviewer measured two `remedy/job-*` worktrees at `4f335b03`. A THIRD appearing is
 expected if the run created one — name its job id and say whether it matches the run's;
 an unexplained new worktree or branch is what this gate is shaped to catch.

G6 PUSH AND TREE — after C4: `git push -u origin feature/f277-machine-contracts` and
 report its outcome, then `git status --porcelain`, which must be empty.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 7 of feature F277, round 13.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the
review of round 13, then round 14 — the reviewer registering every self-use defect string
you reported as an R-id finding, `remedy integrity check --json`, and the integration
gate running the full suite ONCE with its transcript committed as
`.agent/authored/f277-closure-suite.txt`. State the open-findings count and the
operator-questions count, which are 20 and 2.
