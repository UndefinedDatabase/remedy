STEP F043 R6 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 5, consolidate the checklist, write the Built State, and run the closure's self-use item

GOAL
Book round 5's PASS, add F043's consolidation paragraph to the reviewer's checklist, write the
feature file's Built State, and meet closure precondition 6 by generating and running the
closure's self-use item on the `self_use` role. The one full suite runs in the next round, after
the self-use item's diff is landed or declined there.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THIS ROUND CHANGES NO PRODUCTION CODE: every edit is a
payload you apply, and the self-use run is a command you run and record. You never edit a payload;
if one looks wrong to you, STOP and report it. Read `docs/roadmap/STATUS_closure_protocol.md`
precondition 6 before C5.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f043-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f043-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f043-r6-selfuse/`   Where the self-use run writes its job file; the script names it.
  `.remedy-wt/f043-r6-jobtree/`   The self-use script adds and removes it; never touch it.
  `.remedy-wt/f043-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f043-r6-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace or a brace beside a quote is refused: write such a script to a
file under your own directory and run the file. Never run npm or npx yourself. Never stop a
process with `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f043-explanation-layer`, and `git log --oneline -1` must read `2660444a9`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f043-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and the count of `git branch --list 'remedy/*'` as found.

PAYLOADS — under `.remedy-wt/f043-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 10 | 4364 | 5326d29dafcf736270fbaaa190dd6dd7742cacfeffc173ac0ff99c028eb157e0 |
| docs.diff | 66 | 4659 | 471fb8e62ba4c1a5de827b37dc84b270166fee4057d76eafa6935489d3ec1da1 |
| plan.md | 30 | 1114 | d8736bf3d9115a6f9221e9f4ec0dfabcc765af4b0ad154137c6686cd0a6bb6aa |
| selfuse.py | 122 | 6488 | 3a1bae0b8755823f8502d964859291d7f7ae9e9dc6d13875ca5078bd6e137775 |

`plan.md` is a REWRITE of `.agent/plan.md`. The two `.diff` files go on with `git apply`; the
reviewer generated them with `git diff HEAD` from a tree at `2660444a9`. `records.diff` appends
round 5's gate entry to `.agent/live_review.md`. `docs.diff` adds F043's consolidation paragraph to
`docs/agents/planner_reviewer_prompt.md` and the Built State section to
`docs/roadmap/features/T5_F043.md`. `selfuse.py` is the self-use run, copied and run from its copy.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the plan
  `.agent/authored/f043-r6-block.md` := this block and `.agent/authored/f043-r6-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F043 R6 C1a: copy round 6 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 30. Report the number you measure.

C1b — copy the two diffs and the self-use script
  `.agent/authored/f043-r6-records.diff`, `.agent/authored/f043-r6-docs.diff` and
  `.agent/authored/f043-r6-selfuse.py` := their payloads.
  Subject: `F043 R6 C1b: copy round 6 records and docs diffs and the self-use script`
  Expected insertions: 198.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F043 R6 C2: book F043 R5, advance the plan to the closure`
  Expected by `git show --numstat` (insertions and deletions): 2/0 .agent/live_review.md, 9/10 .agent/plan.md.

C3 — THE CONSOLIDATION AND THE BUILT STATE: `git apply` docs.diff.
  Subject: `F043 R6 C3: consolidate the checklist for F043 and write its Built State`
  Expected: 6/0 docs/agents/planner_reviewer_prompt.md, 41/0 docs/roadmap/features/T5_F043.md.

C4 — nothing is committed here: RUN G1 to G3 now, before C5, and record their readings for the
  handback.

C5 — THE SELF-USE ITEM (closure precondition 6), AFTER G1 to G3: run
  `bash -c 'python3 .agent/authored/f043-r6-selfuse.py 2>&1 | tee .remedy-wt/f043-r6-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  in the primary checkout with a Bash timeout of 3600000 milliseconds: the run makes real provider
  calls, each allowed ten minutes. It appends the generated item to `scripts/self_use_queue.json`,
  runs it on the `self_use` role's configured provider, and writes `.agent/selfuse_f043/`. The
  reviewer's reading of the real tree read the item as `SU-038`, from Tier 4, titled "Narrow the
  excused handler at apps/cli/commands/brain.py:182"; report what the run reads. A job that ends
  blocked or stopped is an OUTCOME to record, never a reason to stop or to re-run; only a Python
  exception before the job exists is a STOP. Commit `scripts/self_use_queue.json` and
  `.agent/selfuse_f043/**`, and nothing else.
  Subject: `F043 R6 C5: generate and run the closure's self-use item, record its readings`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F043 R6 C6: rewrite handoff for round 6`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading, except C5, whose
   `.agent/selfuse_f043/` record is the run's own output and is reported with its real count.
3. The round's whole tracked path set is: the `.agent/authored/f043-r6-*` copies, the paths the two
   diffs edit, `.agent/plan.md`, `scripts/self_use_queue.json`, `.agent/selfuse_f043/**` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 2660444a9` at the
   branch tip after C6. No file under `apps/`, `packages/` or `tests/` changes in this round.
4. The self-use job is NEVER applied: no `job apply`, no `--approve`, no copying of its files into
   the checkout. Its diff is read in the next round.
5. If a gate other than the self-use outcome goes red, STOP, commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch switch, no branch deletion,
   no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, every branch and every existing stash
   alone; the script removes the one worktree it adds.
8. DO NOT run the full suite: F043's one full suite belongs to the next round.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G3 run before C5; G4 after C5; all
before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f043-r6-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f043-r6/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE DOCS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, printed from its simulation tree:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/live_review.md | C2 | 131634 | c6844fb11a9e4366dfd28fea91f3444e17bca646cf0725b13dda5e2198751ae0 |
 | .agent/plan.md | C2 | 1114 | d8736bf3d9115a6f9221e9f4ec0dfabcc765af4b0ad154137c6686cd0a6bb6aa |
 | docs/agents/planner_reviewer_prompt.md | C3 | 113549 | 6a233d9f38412f39061c397c4fabab2a9f4ead341f6d1dc5f71289cbf6f38a91 |
 | docs/roadmap/features/T5_F043.md | C3 | 7699 | 0f17c419ee836051feeb1bbabc240640c34856d30738c399e3c826c91c80f433 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT at C2 (the reviewer read `[]`), and the
 ledger's last non-empty line at C2, which begins `Gate: F043 R5 — the F043 round 5 entry`.

G3 THE TESTS — in the primary checkout at C3, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_findings.py tests/test_ble001_ratchet.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it serially in its dry tree, which carries C2 and C3 but no
 `.agent/authored/f043-r6-*` copy, and read `636 passed, 1 skipped` at real exit code 0, the skip
 the D12 quarantine; your count may differ by what the round's copies hold. Report every `SKIPPED`
 line. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass` at `fail_count` 0.

G4 THE SELF-USE READINGS — the whole output of C5's command and its real exit code; the item's id,
 title and provenance; the job's id and state; the builder and reviewer provider and model from
 `.agent/selfuse_f043/execution_config.txt`, which must name the `self_use` role's provider and
 never `fake`; the budgets and the budget actuals; every task's status, verdict and final status;
 `.agent/selfuse_f043/changed_paths.txt`, `staleness_after.txt`, `job_diff.txt` and
 `run_defects.txt` verbatim; and `git worktree list | wc -l` and the count of
 `git branch --list 'remedy/*'` after the run.

G5 SIZES, TREE AND PUSH — `git show --numstat --format= <commit>` for C1a to C5, each beside the
 expected insertions of its entry where one is stated and placed in the handback's `## Commits`
 table exactly as the tool printed it; and after C6, in your reply only: `git status --porcelain`
 empty, `git log --oneline -n 7` showing C6, C5, C3, C2, C1b, C1a and `2660444a9` in that order,
 the push's real outcome, and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
 EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected, every gate's real output and exit code, the
self-use readings, the authored-text proofs, the item-status table AGENTS.md requires (one row per
commit and per gate), the deviations, and the next expected action. Report what you ran, not what
you expected to find. Your Session section reads SESSION 1 of feature F043, round 6, and says in
one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6 and of the self-use run's diff, then the integration gate (the one full suite). State the
open-findings count, 0, and the operator-questions count, 0.
