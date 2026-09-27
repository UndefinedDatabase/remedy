STEP F288 R7 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 6, consolidate the checklist, write the Built State, then generate and run the closure's self-use item

GOAL
Round 6 passed and all three T-slices of F288 are built. Book round 6's verdict from the handoff
into the ledger, add the closure's consolidation paragraph to the checklist, write the Built State
of `docs/roadmap/features/T5_F288.md` (closure precondition 4), and meet precondition 6 of
`docs/roadmap/STATUS_closure_protocol.md`: generate the closure's self-use item and run it to its
approval gate on the `self_use` role, recording its readings under `.agent/selfuse_f288/`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. Every change this round makes travels as a payload
or is produced by the payload script; you write no code and no prose outside the handback.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f288-r7-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f288-r7/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f288-r7-selfuse/`   Where the self-use run writes its job file; the payload names it.
  `.remedy-wt/f288-r7-jobtree/`   The payload adds and removes it itself; never touch it.
  `.remedy-wt/f288-r7-sim/`, `.remedy-wt/f288-r7-drafts/` and `.remedy-wt/f288-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f288-r7-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace or a backslash inside an f-string is refused or fails: write
such a script to a file under your own directory and run the file. Never run npm or npx. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f288-event-stream-completeness`, and `git log --oneline -1` must read `2f49da5c`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f288-r7/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and the count of `git branch --list 'remedy/*'` as found.

PAYLOADS — under `.remedy-wt/f288-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 29 | 1078 | 83d89f6f4ada45dfdb44ad46a5689b4ed22a3665096f1d95fa15ea5493a8fd0a |
| records.diff | 29 | 11008 | ec3ec0281e0ccc78f543f524b77f7b9d02050598afe40167b7b11934610f8bbc |
| built_state.diff | 79 | 5968 | 5efb7f4142289d3e399a80e0197a4344bef197366b50f1f8a984c09dffdf527e |
| selfuse.py | 121 | 6420 | f70612e69c39682b41e11168ecbeffb785af00cdcf306d13dd50d541e5ceffce |

`plan.md` is a REWRITE of `.agent/plan.md`. Both diffs go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a simulation tree at `2f49da5c`, `records.diff` first and
`built_state.diff` on top of it. `records.diff` appends round 6's gate entry — the paragraph
between the BEGIN and END GATE ENTRY markers of `.agent/handoff.md` at `2f49da5c`, verbatim, after
one blank line — to `.agent/live_review.md`, and inserts the closure's consolidation paragraph
above the line `  The next consolidation measures against 34.` in
`docs/agents/planner_reviewer_prompt.md`. `built_state.diff` appends a `## Built State (F288,
2026-09-27)` section to `docs/roadmap/features/T5_F288.md`. `selfuse.py` is the reviewer's script
for C4, run from the primary checkout.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f288-r7-block.md` := this block, and `.agent/authored/f288-r7-plan.md`,
  `.agent/authored/f288-r7-records.diff`, `.agent/authored/f288-r7-built_state.diff` and
  `.agent/authored/f288-r7-selfuse.py` := the four payloads, by `shutil.copyfile`.
  Subject: `F288 R7 C1: copy round 7 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 258. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKKEEPING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F288 R7 C2: book round 6, consolidate the checklist, plan round 7`
  Expected by `git show --numstat` (insertions and deletions): 2/0 `.agent/live_review.md`,
  9/9 `.agent/plan.md`, 8/0 `docs/agents/planner_reviewer_prompt.md`.

C3 — THE BUILT STATE: `git apply` built_state.diff.
  Subject: `F288 R7 C3: write the Built State`
  Expected by `git show --numstat`: 71/0 `docs/roadmap/features/T5_F288.md`.

C4 — THE SELF-USE ITEM (closure precondition 6): run
  `bash -c 'python3 .remedy-wt/f288-r7-payloads/selfuse.py 2>&1 | tee .remedy-wt/f288-r7-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  in the primary checkout AFTER C3 is committed, with a Bash timeout of 3600000 milliseconds: the
  run makes real provider calls, each allowed ten minutes, and may take most of an hour. It
  appends the generated item to `scripts/self_use_queue.json`, runs it on the `self_use` role's
  configured provider, and writes `.agent/selfuse_f288/`. The reviewer's simulation of the tree at
  C3 read the item as `SU-034`, from Tier 2, generated from the claim that the CLI commands table of
  `docs/guides/remedy-toml-user-guide.md` never documents the `config` subcommand `show`; report
  what the run reads. A job that ends blocked or stopped is an OUTCOME to record, never a reason to
  stop or to re-run; only a Python exception before the job exists is a STOP. Commit
  `scripts/self_use_queue.json` and `.agent/selfuse_f288/**`, and nothing else.
  Subject: `F288 R7 C4: generate and run the closure's self-use item, record its readings`

C5 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F288 R7 C5: rewrite handoff for round 7`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. If one would reach
   500, split it into lettered parts before committing and declare the split.
3. The round's whole tracked path set is: the `.agent/authored/f288-r7-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`,
   `docs/roadmap/features/T5_F288.md`, `scripts/self_use_queue.json`, `.agent/selfuse_f288/**` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 2f49da5c` after C5.
   No `consumed_by` is set this round: the closure commit sets it.
4. The self-use job is NEVER applied: no `job apply`, no `--approve`, no copying of its files into
   the checkout. It may leave a `remedy/job-*` branch or an evidence directory behind; report
   each, and delete nothing you did not create as scratch.
5. If a gate other than the self-use outcome goes red, STOP, commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
7. DO NOT run the full suite: it runs once, in a later round of this closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f288-r7-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f288-r7/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKKEEPING AND THE BUILT STATE — the byte count and sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equal the reviewer's reading, printed from its
 simulation tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 322392 | 3e122392b3f04cba97655c57d7b9eb5356c51304e8104ab92610bf0488395721 |
 | C2 | docs/agents/planner_reviewer_prompt.md | 105869 | 61fab16e0c8c77c10d1979f2c84ea2de8a98504c6b29dcfaa0c92e72dd1e90a6 |
 | C2 | .agent/plan.md | 1078 | 83d89f6f4ada45dfdb44ad46a5689b4ed22a3665096f1d95fa15ea5493a8fd0a |
 | C3 | docs/roadmap/features/T5_F288.md | 8149 | 464873a969d453a721602df901e02c67dbd364634564177ee76501a740a2f49d |
 Also the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` (import it with `scripts` on `sys.path`) over the ledger's TEXT at
 `2f49da5c` and at C2: the reviewer read empty at both.

G3 THE TESTS, in the primary checkout at C4, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_job.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/orchestration/test_test_runner.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection in its simulation tree at C3 with the generated item appended
 as C4 appends it and read `689 passed, 2 skipped` at real exit code 0. The skips were
 `tests/test_agent_tooling.py:43`, a standing quarantine, and `tests/orchestration/test_test_runner.py:414`,
 skipped only because the simulation tree has no `apps/ui/node_modules`; in the primary checkout
 that second node runs, so report the counts and every skip line you read. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks with status
 `pass` at `fail_count` 0 — the STATUS of each check is the reading, not the exit code, because a
 broken ledger verdict reads `warn` at exit code 0.

G4 THE SELF-USE READINGS — the whole output of C4's command and its real exit code; the item's
 id, title and provenance; the job's id and state; the builder and reviewer provider and model
 from `.agent/selfuse_f288/execution_config.txt`, which must name the `self_use` role's provider
 and never `fake`; the budgets and the budget actuals; every task's status, verdict and final
 status; `.agent/selfuse_f288/changed_paths.txt`, `.agent/selfuse_f288/staleness_after.txt`,
 `.agent/selfuse_f288/job_diff.txt` and `.agent/selfuse_f288/run_defects.txt` verbatim; and
 `git worktree list | wc -l` and the count of `git branch --list 'remedy/*'` after the run.

G5 SIZES — `git show --numstat --format= <commit>` for C1, C2, C3 and C4, each reported beside
 the expected insertions of its entry above where one is stated, and placed in the handback's
 `## Commits` table exactly as the tool printed it.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `2f49da5c` in that order; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the self-use readings, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next expected action. Report what you ran, not what you expected to find.
Your Session section reads SESSION 2 of feature F288, round 7, rounds so far 7, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 7 and of the self-use run's diff, then the rest of the closure sequence. State the
open-findings count, 0, and the operator-questions count, 0.
