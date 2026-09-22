STEP F283 R22 — the closure sequence's first half: the built state, the one checklist pass, the self-use item and the feature's one full suite

GOAL
Book round 21's PASS and resolve R-1033, write the feature file's Built State, fold this feature's
one prose lesson into the reviewer checklist without lengthening it, run the closure's self-use
item to its approval gate, and run this feature's ONE full suite, committing its transcript.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors the RECORD payloads and the checklist
pair; the feature file's Built State prose is yours, written to the SPEC in C3. This round closes
nothing: the STATUS line, the evidence job, the review zip and the pull request are the NEXT
round's, and no commit of this round may touch `docs/roadmap/STATUS.md`, `README.md` or
`scripts/self_use_queue.json`'s `consumed_by` fields.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r22-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r22-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file the
      reviewer put there before C1, which is read-only to you. `probe_selfuse.py` is the
      reviewer's dry run of C5's generation step, run in a throwaway worktree at `0838fc12`.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`, a
`grep` pattern holding `$`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`; put multi-step code in a scratch file. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <dir>` for a worktree. NEVER USE `git stash` IN
ANY FORM, and never check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `0838fc12`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r22-block.md` against the two readings your delegation message states. Report
   both beside both, and stop if either differs.
4. Record, before anything runs: `git branch --list 'remedy/job-*'` count and `git worktree list`.

PAYLOADS — under `.remedy-wt/f283-r22-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 4583 | d75ddba3d479d010ebc8c7f99bed397263e071247f81d8f74d0d67ddb3df0f58 |
| plan.md | 34 | 1525 | 8f1606f409ab07a9920b784d632029cc4fc08ae236859e706fea0d6fa803659b |
| checklist_from.txt | 1 | 164 | 3cb6b93c27fcf9c9fd138fbd9d93bed635d590fa292e6dfe40e11f64a78cdcea |
| checklist_to.txt | 13 | 1118 | 69a245325f2ea03ea8f2de476c5a5b925299d266370c1aa58b9d20be3718d40e |

`ledger.md` is an APPEND beginning with the single newline that separates records: the round 21
`Gate:` entry and R-1033's `Done:` paragraph. `plan.md` is a REWRITE. `checklist_from.txt` and
`checklist_to.txt` are ONE replacement pair for `docs/agents/planner_reviewer_prompt.md`; the
reviewer's containment test printed `TO contains FROM: true`, so the pair is an APPEND and no
FROM-zero count is owed — FROM stays at exactly one occurrence, and each line only the TO holds
appears exactly once among that commit's ADDED lines. Never retype or edit a payload.

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f283-r22-block.md` := this block; `.agent/authored/f283-r22-<name>` for each
  payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R22 C1: copy round 22 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md
  Subject: `F283 R22 C2: book round 21's PASS and resolve R-1033`

C3 — THE BUILT STATE, in `docs/roadmap/features/T2_F283.md`: a `## Built State` section, written
  in plain complete sentences, that states for each Acceptance line what meets it and where —
  the envelope on success and on an invalid argument (the sweep and the per-module tests), the
  empty read-only-without-`supports_json` set and its ratchet, the exit-code taxonomy with its
  module, guide and test, and R-1019 and R-1020 with the round that resolved each. Name the
  DECISIONS this feature recorded (F283 D1 to D13) as a list of ids with one clause each, and
  name `apps/cli/exit_codes.py` and `tests/cli/test_json_contract.py` as the files it added, since
  a closure precondition asks the feature file to name a new module. Correct nothing else in the
  file and remove nothing from it.
  Subject: `F283 R22 C3: write the feature file's Built State`

C4 — THE ONE CHECKLIST PASS (operator amendment amend0827 rule 4), applying the payload pair to
  `docs/agents/planner_reviewer_prompt.md`: the clause joins ITEM 34 and the list does not grow.
  Apply the pair byte-for-byte; edit nothing else in that file.
  Subject: `F283 R22 C4: fold F283's prose lesson into checklist item 34`

C5 — THE SELF-USE ITEM (closure precondition 6):
  (a) `packages.orchestration.self_use_generator.generate_and_append_if_empty()` FIRST. The
      reviewer's dry run at `0838fc12` appended `SU-026`, "Address ledger finding R-0950"; report
      what yours does, and report `next_self_use_item()`'s answer afterwards.
  (b) RUN it with `packages.orchestration.self_use_runner.run_next_self_use_item`, whose
      `dest_dir` is a path under `.remedy-wt/` and never a tracked one. Pass no
      `builder_name`/`reviewer_name`, so both resolve from the one `self_use` role configuration
      (DECISION amend0920-selfuse-real D2); report the `execution_config` the returned `JobPlan`
      carries, which is the proof of which provider actually ran. It is run to the approval gate
      and NEVER applied.
  (c) Save under `.agent/selfuse_f283/`, mirroring `.agent/selfuse_f281/`'s file names: the item
      markdown, the entry and job-file path, the execution config, the result state, the timing,
      the transcript, and `run_defects.txt` holding every string
      `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the
      run's own `JobPlan` — verbatim, and the literal `NONE` if it returns an empty tuple.
  (d) Then `python3 -m pytest tests/docs/ -q`. The generated item's text lands in the tracked
      `scripts/self_use_queue.json`, and `tests/docs/test_retired_promote_word.py` reads it
      (finding R-1015). If that guard goes red on the text the generator wrote, repair its
      `KEPT_BY_SENSE` entry for `scripts/self_use_queue.json` — the tokens the NEW text carries,
      or the entry removed when it carries none — IN THIS COMMIT, and report both readings. The
      reviewer's dry run read `315 passed` at exit 0 with the generated item in place.
  This commit's paths: `scripts/self_use_queue.json`, `.agent/selfuse_f283/**`, and
  `tests/docs/test_retired_promote_word.py` only if (d) requires it. You do not register findings:
  the reviewer authors every registration from `run_defects.txt` at the next round.
  Subject: `F283 R22 C5: generate and run the closure's self-use item, record its defects`

C6 — THE INTEGRATION GATE, this feature's ONE full suite (operator amendment amend0917-throughput
  rule 1, and amend0921-operator-feedback rule 1: the run belongs to the shipped tree, which is
  this branch with `main` already merged in): `python3 -m pytest -n auto -q` in the PRIMARY
  checkout, after C5. Commit the summary line and the FULL list of bad node ids as
  `.agent/authored/f283-closure-suite.txt`, together with the handback.
  `.agent/handoff.md` is rewritten per `docs/agents/handback_template.md` in this same commit.
  Subject: `F283 R22 C6: record the closure suite transcript and rewrite handoff for round 22`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the `.agent/authored/f283-r22-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `.agent/authored/f283-closure-suite.txt`, `.agent/selfuse_f283/**`,
   `docs/roadmap/features/T2_F283.md`, `docs/agents/planner_reviewer_prompt.md`,
   `scripts/self_use_queue.json`, and `tests/docs/test_retired_promote_word.py` under C5 (d).
   Report the set you measure. Nothing under `packages/`, nothing under `apps/`, no
   `docs/roadmap/STATUS.md`, no root `README.md`, nothing else under `scripts/`, and none of
   `.agent/candidates.md`, `.agent/context.md`, `.agent/operator_questions.md`,
   `.agent/decisions.md`, `.agent/prose_slips.md`.
4. If the full suite in C6 is RED, that is this feature's work and not a reason to stop: commit
   the transcript exactly as measured, report every bad node id, and hand back. The repair rounds
   and their rules are the reviewer's to order (amend0917-throughput rule 2). Never weaken an
   assertion, delete a test or mark anything xfail on your own initiative.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no STATUS edit, no `consumed_by` edit, no review zip, no evidence job.
7. The self-use run may leave `remedy/job-*` branches, worktrees or evidence directories behind.
   Report them; delete NOTHING you did not create as scratch, and never delete a branch.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6's handback text is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f283-r22-*` blob, read with `git show <C1>:<path>`, compared
 byte-for-byte with its source (the block copy against `.remedy-wt/f283-r22-block.md`). One
 reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, `.agent/live_review.md` read at `0838fc12` (555322) plus
     ledger.md, the reviewer composed 559905.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R21 — ` 1 and `^Done: R-1033 — ` 1. Open
     set by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` at `0838fc12`
     and at C2: the reviewer measured 26 and 25, REMOVED `R-1033`, ADDED none.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE DOCS — at C4: `checklist_from.txt`'s text occurs exactly ONCE in
 `docs/agents/planner_reviewer_prompt.md` both before and after (the pair is an APPEND), and each
 line only `checklist_to.txt` holds occurs exactly once among the lines C4's diff ADDS. The
 numbered items of the pre-emission checklist count 34 before and 34 after, read mechanically —
 the reviewer read `1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37`
 at `0838fc12` — and the same numbers in the same order. Then `python3 -m pytest tests/docs/ -q`
 after C3 and again after C4, since C3 writes a roadmap file.

G4 THE SELF-USE ITEM — at C5: the generator's answer and `next_self_use_item()`'s afterwards; the
 runner's returned entry id, job file path and job state; the `execution_config`'s builder and
 reviewer names and models, which must be the `self_use` role's configured provider and never a
 raw fallback; the `describe_self_use_run_defects` output verbatim; `python3 -m pytest tests/docs/
 -q` after the queue file is written, with its exit code; and `git branch --list 'remedy/job-*'`
 counted before C1 and after C5 with `git worktree list` beside each.

G5 THE INTEGRATION GATE — at C6: `python3 -m pytest -n auto -q` in the primary checkout, its real
 exit code, its summary line and every bad node id, all of it in
 `.agent/authored/f283-closure-suite.txt`. Report whether
 `tests/orchestration/test_import_reachability.py` and `tests/test_no_orphan_modules.py` are among
 the bad nodes (closure precondition 7). Then `python3 -m apps.cli.main integrity check --json`,
 all five checks `pass`, and `git status --porcelain`, which must be empty with no relevant
 untracked file (closure precondition 3).

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline -n 8`; `git
 worktree list`; `git stash list`'s first line unchanged from its reading before C1; the push's
 real outcome; `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit changed-files
table with the insertions git MEASURED, every gate's real output and exit code, the self-use run's
entry id, provider, state and defect list, the full suite's summary line and bad node ids, the
item-status table with one row per C-item and gate, the deviations, and the next action. Your
Session section reads SESSION 5 of feature F283, round 22, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
22, then the closure sequence's second half — the registrations the self-use defects ask for, the
evidence job, the review zip, the ledger rotation, the STATUS line with the README counters in the
same commit, and the pull request. State the open-findings count, 25 after this round, and the
operator-questions count, 0.
