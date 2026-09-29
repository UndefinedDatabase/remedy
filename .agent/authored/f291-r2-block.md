STEP F291 R2 — T003'S RUN HALF, THE TWO SOURCES DOCUMENTED, AND THE CLOSURE SEQUENCE'S FIRST ROUND: book round 1, consolidate the checklist, write the Built State, and run the closure's self-use item

GOAL
Round 1 passed. Book it, record DECISION F291 D2 and the checklist consolidation, land the
reviewer's runner test for the run half of T003, document the two new sources, drop the clause
label `S0` from two generator comments, write F291's Built State (closure precondition 4), and meet
closure precondition 6 by generating and running the closure's self-use item on the `self_use`
role. The one full suite runs in the next round, after the self-use item's diff is landed or
recorded.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` or `Landed:` line. Every change this round
makes travels as a payload or is produced by a payload script. Read first
`docs/roadmap/STATUS_closure_protocol.md` preconditions 4 and 6, and DECISION F291 D2 in
records.diff.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f291-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f291-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f291-r2-selfuse/`   Where the self-use run writes its job file; the payload names it.
  `.remedy-wt/f291-r2-jobtree/`   The self-use script adds and removes it; never touch it.
  every other `.remedy-wt/f291-*` path: the reviewer's; do not touch.
  `.remedy-wt/f291-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace is refused: write such a script to a file under your own
directory and run the file. Set environment variables for a child process inside a Python script
(`subprocess.run(..., env=...)`), never on a command line. Never run npm or npx. Never `pkill -f`.
The `remedy` command may be denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f291-self-use-sources-v2`, and `git log --oneline -1` must read `045de81f5`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f291-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and the count of `git branch --list 'remedy/*'` as found.

PAYLOADS — under `.remedy-wt/f291-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 71 | 10124 | bcc6ea6659eda98aa5f0a313d3a3707ebe93f47acd18044c5a713bfbe8e4d1cc |
| docs.diff | 96 | 6521 | dc06ebb7acd565c570e930856bf64ed9a5c0c49c27c58af8a0872262bd424b12 |
| code.diff | 22 | 1354 | 03bdff1807268cbd524b14631ab50cfb78fa94eb58cc55da162fd85d342d3a45 |
| tests.diff | 126 | 6217 | 43a85a7c78d42cfd616644a528a1dbe93b337e954e5d1380567008b400eb188f |
| plan.md | 28 | 896 | a59330b4d49e9b584a6542f126c227f8387b3b765fc82ac0ad284ed4c3513301 |
| selfuse.py | 122 | 6488 | be69f7b61e980b8667bfc1fc44aafc32de9a0710c717ff66bbda14cef9c9d81c |

`plan.md` is a REWRITE of `.agent/plan.md`. Every `.diff` goes on with `git apply`, in the order the
commits below name; the reviewer generated them with `git diff HEAD` from a tree at `045de81f5`.
`records.diff` appends round 1's gate entry to `.agent/live_review.md`, DECISION F291 D2 to
`.agent/decisions.md`, and the closure's consolidation paragraph above the line
`  The next consolidation measures against 34.` of `docs/agents/planner_reviewer_prompt.md`.
`docs.diff` appends `## Built State (F291, 2026-09-29)` to `docs/roadmap/features/T5_F291.md` and
describes the two sources in `docs/system/self-use-track-v1.md` and in precondition 6 of
`docs/roadmap/STATUS_closure_protocol.md`. `code.diff` drops the label `S0` from two comments of
`packages/orchestration/self_use_generator.py` and changes nothing else. `tests.diff` imports
`TASK_APPLIED` and appends the class `TestAnExcusedHandlerItemRunsToTheApprovalGate` to
`tests/orchestration/test_self_use_runner.py`. `selfuse.py` is the self-use run, copied and run
from its copy.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6 and C7, in this order.

C1a — `.agent/authored/f291-r2-block.md` := this block, and `.agent/authored/f291-r2-plan.md`,
  `.agent/authored/f291-r2-records.diff` and `.agent/authored/f291-r2-docs.diff` := those payloads,
  by `shutil.copyfile`. Subject: `F291 R2 C1a: copy round 2 block, plan, records and docs diffs`
  Its insertions are this block's line count plus 195; STOP rather than commit at 500.
C1b — `.agent/authored/f291-r2-code.diff`, `.agent/authored/f291-r2-tests.diff` and
  `.agent/authored/f291-r2-selfuse.py` := those payloads.
  Subject: `F291 R2 C1b: copy round 2 code and tests diffs and the self-use script`.
  Expected insertions: 270.
C2 — THE RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md.
  Subject: `F291 R2 C2: book F291 R1, record D2, consolidate the checklist`
  Expected by `git show --numstat`: 35/0 .agent/decisions.md, 2/0 .agent/live_review.md, 9/10 .agent/plan.md, 7/0 docs/agents/planner_reviewer_prompt.md.
C3 — THE DOCUMENTATION: `git apply` docs.diff, then `git apply` code.diff.
  Subject: `F291 R2 C3: document the two new self-use sources and write F291's Built State`
  Expected by `git show --numstat`: 4/2 docs/roadmap/STATUS_closure_protocol.md, 35/0 docs/roadmap/features/T5_F291.md, 17/1 docs/system/self-use-track-v1.md, 2/2 packages/orchestration/self_use_generator.py.
C4 — THE TEST: `git apply` tests.diff.
  Subject: `F291 R2 C4: add the reviewer's test that a Tier 4 item runs to the approval gate`
  Expected by `git show --numstat`: 110/1 tests/orchestration/test_self_use_runner.py.
C5 — THE TOOL: your mutation tool (G3) saved as `.agent/authored/f291-r2-mutations.py`.
  Subject: `F291 R2 C5: add the round 2 mutation tool`
C6 — THE SELF-USE ITEM (closure precondition 6), AFTER G1 to G3: run
  `bash -c 'python3 .agent/authored/f291-r2-selfuse.py 2>&1 | tee .remedy-wt/f291-r2-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  in the primary checkout with a Bash timeout of 3600000 milliseconds: the run makes real provider
  calls, each allowed ten minutes, and may take most of an hour. It appends the generated item to
  `scripts/self_use_queue.json`, runs it on the `self_use` role's configured provider, and writes
  `.agent/selfuse_f291/`. The reviewer's reading of the real tree read the item as `SU-037`, from
  Tier 4, titled "Narrow the excused handler at apps/cli/commands/brain.py:132"; report what the
  run reads. A job that ends blocked or stopped is an OUTCOME to record, never a reason to stop
  or to re-run; only a Python exception before the job exists is a STOP. Commit
  `scripts/self_use_queue.json` and `.agent/selfuse_f291/**`, and nothing else.
  Subject: `F291 R2 C6: generate and run the closure's self-use item, record its readings`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F291 R2 C7: rewrite handoff for round 2`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. If one would reach
   500, split it into lettered parts before committing and declare the split.
3. The round's whole tracked path set is: the `.agent/authored/f291-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/STATUS_closure_protocol.md`,
   `docs/roadmap/features/T5_F291.md`, `docs/system/self-use-track-v1.md`,
   `packages/orchestration/self_use_generator.py`, `tests/orchestration/test_self_use_runner.py`,
   `scripts/self_use_queue.json`, `.agent/selfuse_f291/**` and `.agent/handoff.md`. Report the
   list you measure with `git diff --name-only 045de81f5` after C7. No `consumed_by` is set this
   round, because the closure commit sets it.
4. The self-use job is NEVER applied: no `job apply`, no `--approve`, no copying of its files into
   the checkout. It may leave a `remedy/job-*` branch or an evidence directory behind; report each,
   and delete nothing you did not create as scratch.
5. If a gate other than the self-use outcome goes red, STOP, commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back. An EXISTING test that goes
   red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch switch, no branch deletion,
   no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash alone.
   The worktree G3 adds goes under `.remedy-wt/`, is removed as that gate's last action, and
   `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: it runs once, in the next round.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G3 run before C6, and G4 and G5 before C7.

G1 TRANSPORT AND RECORDS — each payload's measured lines, bytes and sha256 against the table; each
 `.agent/authored/f291-r2-*` copy byte-equal to its source (the block against
 `.remedy-wt/f291-r2/block.md`) by `git show <commit>:<path>` from the commit that added it; and the
 bytes and sha256 of each file below, read with `git show <commit>:<path>` at the commit named,
 equal to the reviewer's reading printed from its simulation tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2509720 | bed852cb4a5682ec88fe8f44460666a7100bfc5c75bc4e66e2faf08b7e4ed6c1 |
 | C2 | .agent/live_review.md | 136370 | f8dcd5c2f986c4a54fe3b021bf00f490a6807054bedf70a7e6e83938c145df13 |
 | C2 | .agent/plan.md | 896 | a59330b4d49e9b584a6542f126c227f8387b3b765fc82ac0ad284ed4c3513301 |
 | C2 | docs/agents/planner_reviewer_prompt.md | 112994 | 20ca744ddadaba51190c6982aefc3c4fde7183d0e222c4bddde1a2a172612ba8 |
 | C3 | docs/roadmap/STATUS_closure_protocol.md | 21138 | 4515afe3df81a4e6ec359ee8254fd8ead3a344a41fc27cd171dc675c1d106a73 |
 | C3 | docs/roadmap/features/T5_F291.md | 6238 | 6f4a3148026d4f9f48763ae90b25c6d09ac4268a5414f4888617b5d89c4e8049 |
 | C3 | docs/system/self-use-track-v1.md | 9881 | 3281eac09df2dea9fda188ba606528c35f853b39098d45c09de33f1f2dba3b7d |
 | C3 | packages/orchestration/self_use_generator.py | 42319 | 555cd1151eb90986ae347967fc606cedfb4bea22dc9508613f16f2159c51143f |
 | C4 | tests/orchestration/test_self_use_runner.py | 42873 | 4f6b3bc6b0ba2ca22fd52d866bbab16a3b495a562ebbf1159f8f3f4375da0f35 |
 Also `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2 (the reviewer read `[]` and `PASS`), and `live_checklist_items` of
 `packages/orchestration/block_lint.py` over the planner prompt at C2 (the reviewer read 34 items).

G2 THE TESTS, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_job.py tests/orchestration/test_doc_staleness.py tests/test_ble001_ratchet.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it in its simulation tree carrying C2 to C4 but no `.agent/authored/f291-r2-*`
 copy and read `685 passed, 1 skipped` at real exit code 0, the skip the D12 quarantine; report the
 counts and every SKIPPED line. `python3 -m ruff check tests/orchestration/test_self_use_runner.py
 packages/orchestration/self_use_generator.py .agent/authored/f291-r2-mutations.py
 .agent/authored/f291-r2-selfuse.py`, its real exit code. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks with status
 `pass` at `fail_count` 0.

G3 THE RED PROOFS — your tool `.agent/authored/f291-r2-mutations.py` takes a worktree path, and for
 each mutation below edits the named production file INSIDE that worktree (asserting its FROM text
 occurs exactly once there), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_self_use_runner.py` with the worktree as the working directory and first
 on `PYTHONPATH` (set through `subprocess.run(..., env=...)`), restores the bytes, and prints one
 line per mutation: its label, the exit code and the failed count. It runs an unmutated control
 first and last, reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  r1 the Tier 4 job's markdown loses its `## Task 1` heading
     (`packages/orchestration/self_use_generator.py`);
  r2 `generate_and_append_if_empty` no longer passes `source_root` on to
     `generate_self_use_item` (same file);
  r3 `_MAX_PROVIDER_CALLS` reads 1 (`packages/orchestration/self_use_runner.py`).
 Run it: `git worktree add --detach .remedy-wt/f291-r2-mut <C5>`, then
 `python3 -B .agent/authored/f291-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f291-r2-mut`
 and report its whole output. The reviewer's own probe, run against the tree at C4, turned every
 one red with both controls passing. EVERY mutation must exit non-zero; one that stays green is
 reported as green, never papered over, and you then STOP and report it. Then
 `git worktree remove --force .remedy-wt/f291-r2-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G4 THE SELF-USE READINGS — the whole output of C6's command and its real exit code; the item's id,
 title and provenance; the job's id and state; the builder and reviewer provider and model from
 `.agent/selfuse_f291/execution_config.txt`, which must name the `self_use` role's provider and
 never `fake`; the budgets and the budget actuals; every task's status, verdict and final status;
 `.agent/selfuse_f291/changed_paths.txt`, `staleness_after.txt`, `job_diff.txt` and
 `run_defects.txt` verbatim; and `git worktree list | wc -l` and the count of
 `git branch --list 'remedy/*'` after the run.

G5 SIZES, TREE AND PUSH — `git show --numstat --format= <commit>` for C1a to C6, each beside the
 expected insertions of its entry where one is stated and placed in the handback's `## Commits`
 table exactly as the tool printed it; and after C7, in your reply only: `git status --porcelain`
 empty, `git log --oneline -n 9` showing C7, C6, C5, C4, C3, C2, C1b, C1a and `045de81f5` in that
 order, the push's real outcome, and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the self-use readings, the authored-text proofs,
the item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Report what you ran, not what you expected to find. Your Session section
reads SESSION 1 of feature F291, round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2 and of the self-use run's diff, then the integration gate (the one full suite). State the
open-findings count, 0, and the operator-questions count, 0.
