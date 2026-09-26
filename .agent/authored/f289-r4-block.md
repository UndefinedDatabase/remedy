STEP F289 R4 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 3 and R-1074's resolution, consolidate the checklist, then generate and run the closure's self-use item

GOAL
Round 3 passed and all three T-slices of F289 are built. Book round 3's verdict and R-1074's
resolution, add the closure's consolidation paragraph to the checklist, and meet precondition 6
of `docs/roadmap/STATUS_closure_protocol.md`: generate the closure's self-use item, which F289's
own Tier 2 now supplies, and run it to its approval gate on the `self_use` role, recording its
readings and its defects under `.agent/selfuse_f289/`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. Every change this round makes travels as a payload
or is produced by the payload script; you write no code.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f289-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f289-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f289-r4-selfuse/`   Where the self-use run writes its job file; the payload names it.
  `.remedy-wt/f289-r4-dry/`, `.remedy-wt/f289-r4-sim/`, `.remedy-wt/f289-r4-drafts/` and
  `.remedy-wt/f289-review/`       The reviewer's; do not touch them.
  `.remedy-wt/f289-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace is refused: write such a script to a file under your own
directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f289-self-use-sources`, and `git log --oneline -1` must read `ad7f57ad`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f289-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and the count of `git branch --list 'remedy/*'` as found.

PAYLOADS — under `.remedy-wt/f289-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 29 | 1010 | 99e98ff09a0a2f63a18e77d0710fbd3e298a72759e255d71f32882eda1694b9b |
| records.diff | 30 | 6319 | fcbc4cde7b7cfe18a23d7c3464db1ab3dc6e2eebbd97899b7645efa285b9ae14 |
| selfuse.py | 99 | 5245 | 18b3c38fd76b65d65f456b4861c43c98f17a79463243babbffdabc5f3a9a3138 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `ad7f57ad`. It replaces the `Landed: R-1074` line
of `.agent/live_review.md` with the reviewer's `Done: R-1074` paragraph, appends round 3's gate
entry, and inserts the consolidation paragraph above the line
`  The next consolidation measures against 34.` in `docs/agents/planner_reviewer_prompt.md`.
`selfuse.py` is the reviewer's script for C3, run from the primary checkout.

BUNDLE — the commits are C1, C2, C3 and C4, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f289-r4-block.md` := this block, and `.agent/authored/f289-r4-plan.md`,
  `.agent/authored/f289-r4-records.diff` and `.agent/authored/f289-r4-selfuse.py` := plan.md,
  records.diff and selfuse.py, by `shutil.copyfile`.
  Subject: `F289 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 158. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKKEEPING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F289 R4 C2: book round 3 and R-1074's resolution, consolidate the checklist`
  Expected by `git show --numstat` (insertions and deletions): 3/1 live_review.md, 9/8 plan.md, 7/0 planner_reviewer_prompt.md.

C3 — THE SELF-USE ITEM (closure precondition 6): run
  `bash -c 'python3 .remedy-wt/f289-r4-payloads/selfuse.py 2>&1 | tee .remedy-wt/f289-r4-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  in the primary checkout AFTER C2 is committed, with a Bash timeout of 3600000 milliseconds: the
  run makes real provider calls, each allowed ten minutes, and may take most of an hour. It
  appends the generated item to `scripts/self_use_queue.json`, runs it on the `self_use` role's
  configured provider, and writes `.agent/selfuse_f289/`. The reviewer's simulation of the tree at
  C2 read the item as `SU-033`, from Tier 2, generated from the Quick-Find Table's missing link to
  `guides/real-test-execution-snapshot-rollback-user-guide-v1.md`; report what the run reads. A job
  that ends blocked or stopped is an OUTCOME to record, never a reason to stop or to re-run; only a
  Python exception before the job exists is a STOP. Commit `scripts/self_use_queue.json` and
  `.agent/selfuse_f289/**`, and nothing else.
  Subject: `F289 R4 C3: generate and run the closure's self-use item, record its readings`

C4 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F289 R4 C4: rewrite handoff for round 4`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f289-r4-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`,
   `scripts/self_use_queue.json`, `.agent/selfuse_f289/**` and `.agent/handoff.md`. Report the
   list you measure with `git diff --name-only ad7f57ad` after C4. No `consumed_by` is set this
   round: the closure commit sets it.
4. The self-use job is NEVER applied: no `remedy job apply`, no `--approve`, no copying of its
   files into the checkout. It may leave a `remedy/job-*` branch, a worktree or an evidence
   directory behind; report each, and delete nothing you did not create as scratch.
5. If a gate other than the self-use outcome goes red, STOP, commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
7. DO NOT run the full suite: it runs once, in a later round of this closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f289-r4-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f289-r4/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 328714 | fca56d616c4fceab480ab606c18e2ea3054f6ab699d843ffe5d4ba5a4616cbd6 |
 | docs/agents/planner_reviewer_prompt.md | 105183 | 275042a5df5bd03a740327a7b7fb68601175a6d4a35fa9ca66cfa4f20022231f |
 | .agent/plan.md | 1010 | 99e98ff09a0a2f63a18e77d0710fbd3e298a72759e255d71f32882eda1694b9b |
 Also the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT at `ad7f57ad` and at C2: the reviewer read
 `R-1074` alone, then empty.

G3 THE TESTS, in the primary checkout at C3, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection in its simulation tree with the generated item appended as
 C3 appends it and read `585 passed` at real exit code 0, the `-rs` summary printing none. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE SELF-USE READINGS — the whole output of C3's command and its real exit code; the item's
 id, title and provenance; the job's id and state; the builder and reviewer provider and model
 from `.agent/selfuse_f289/execution_config.txt`, which must name the `self_use` role's provider
 and never `fake`; the budgets and the budget actuals; every task's status, verdict and final
 status; `.agent/selfuse_f289/changed_paths.txt`, `.agent/selfuse_f289/staleness_after.txt` and
 `.agent/selfuse_f289/run_defects.txt` verbatim; the diff the job left in its workspace
 (`git -C <Job Workspace> diff HEAD` and its untracked files, reported whole); and
 `git worktree list` and the count of `git branch --list 'remedy/*'` after the run.

G5 SIZES — `git show --numstat --format= <commit>` for C1, C2 and C3, each reported beside the
 expected insertions of its entry above where one is stated, and placed in the handback's
 `## Commits` table exactly as the tool printed it.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 5`, which must show C4, C3, C2, C1 and `ad7f57ad` in that order; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the self-use readings, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next expected action. Report what you ran, not what you expected to find.
Your Session section reads SESSION 1 of feature F289, round 4, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4 and of the self-use run's diff, then the rest of the closure sequence. State the
open-findings count, 0, and the operator-questions count, 0.
