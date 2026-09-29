STEP F042 R6 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 5, consolidate the checklist, write the Built State, land the end-to-end test, take the live run, and run the closure's self-use item

GOAL
Round 5 passed. Book it with R-1110's resolution and R-1111's registration, record DECISION F042
D6 and the checklist consolidation, write F042's Built State (closure precondition 4), land the
reviewer's end-to-end test over the real CLI and a real UI server with R-1111's test, take the live
browser run over the real stack, and meet closure precondition 6 by generating and running the
closure's self-use item on the `self_use` role. No production file changes this round. The one full
suite runs in the next round, after the self-use item's diff is landed or recorded.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` or `Landed:` line. Every change this round
makes travels as a payload or is produced by a payload script. Read first
`docs/roadmap/STATUS_closure_protocol.md` preconditions 4 and 6.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f042-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f042-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f042-r6-selfuse/`   Where the self-use run writes its job file; the payload names it.
  `.remedy-wt/f042-r6-jobtree/` and `.remedy-wt/f042-r6-live-run/`
                                  The payload scripts add and remove them; never touch them.
  every other `.remedy-wt/f042-*` path: the reviewer's; do not touch.
  `.remedy-wt/f042-r6-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace is refused: write such a script to a file under your own
directory and run the file. Set environment variables for a child process inside a Python script
(`subprocess.run(..., env=...)`), never on a command line. Never run npm or npx yourself. Never
`pkill -f`; the scripts stop what they started by pid. The `remedy` command may be denied; use
`python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f042-multi-project-cockpit`, and `git log --oneline -1` must read `79a2e7809`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f042-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and the count of `git branch --list 'remedy/*'` as found.

PAYLOADS — under `.remedy-wt/f042-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 78 | 10997 | 4ba9deb66edf4bba3370bf71fe06b81d0e88604ad0f01c0e61843c78c13c3d52 |
| built_state.diff | 54 | 4160 | 2d0f83a721c1e350ad4c37aa8436f94b69154d93b2b07683a982e5511cfb384b |
| tests.diff | 161 | 7191 | abe9b7d7e9b5b25858f6a44bc6e91c1f01e5cc97d6f02361d27dfbd297ca3690 |
| plan.md | 31 | 1128 | ca8f1c8f0a62bdc3223c4dbb9ca6fd2a730569716307abb62d98bc16233ab7dc |
| live_measure.py | 176 | 7791 | 86888bd4290027a6d51036a7865d10c8ec8619a9a669898c277286713dc6c502 |
| live_drive.mjs | 179 | 9383 | 230beb461c4df2e435ec69c8839f69dba49d53e633014d0daaefc4c74eca9109 |
| selfuse.py | 122 | 6492 | c7ffad0515cbde860f03adeb36ba5240623e6a078dcced0af131cb19fd8edf52 |

`plan.md` is a REWRITE of `.agent/plan.md`. The three `.diff` files go on with `git apply`, in the
order C2, C3 and C4 name; the reviewer generated them with `git diff HEAD` from a simulation tree at
`79a2e7809`. `records.diff` appends round 5's gate entry, R-1110's `Done:` resolution and R-1111's
registration to `.agent/live_review.md`, DECISION F042 D6 to `.agent/decisions.md`, and the
closure's consolidation paragraph above the line `  The next consolidation measures against 34.`
of `docs/agents/planner_reviewer_prompt.md`. `built_state.diff` appends `## Built State (F042,
2026-09-29)` to `docs/roadmap/features/T5_F042.md`. `tests.diff` adds the NEW FILE at
`tests/ui_server/test_multi_project_live.py` and one test to `tests/ui_server/test_projects_route.py`.
`live_measure.py` with `live_drive.mjs` is the live browser run and `selfuse.py` the self-use run;
all three are copied and run from their copies.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5, C6 and C7, in this order.

C1a — `.agent/authored/f042-r6-block.md` := this block, and `.agent/authored/f042-r6-plan.md`,
  `.agent/authored/f042-r6-records.diff` and `.agent/authored/f042-r6-built_state.diff` := those
  payloads, by `shutil.copyfile`. Subject: `F042 R6 C1a: copy round 6 block, plan and record diffs`
  Its insertions are this block's line count plus 163; STOP rather than commit at 500.
C1b — `.agent/authored/f042-r6-tests.diff` and `.agent/authored/f042-r6-selfuse.py` := those payloads.
  Subject: `F042 R6 C1b: copy round 6 tests diff and self-use script`. Expected insertions: 283.
C1c — `.agent/authored/f042-r6-live_measure.py` and `.agent/authored/f042-r6-live_drive.mjs` :=
  those payloads. Subject: `F042 R6 C1c: copy the round 6 live run`. Expected insertions: 355.
C2 — THE RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md.
  Subject: `F042 R6 C2: book F042 R5, resolve R-1110, register R-1111, record D6, consolidate the checklist`
  Expected by `git show --numstat`: 37/0 .agent/decisions.md, 6/0 .agent/live_review.md, 12/8 .agent/plan.md, 8/0 docs/agents/planner_reviewer_prompt.md.
C3 — THE BUILT STATE: `git apply` built_state.diff.
  Subject: `F042 R6 C3: write F042's Built State`. Expected by `git show --numstat`: 46/0 docs/roadmap/features/T5_F042.md.
C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F042 R6 C4: add the reviewer's end-to-end test and R-1111's test`
  Expected by `git show --numstat`: 135/0 tests/ui_server/test_multi_project_live.py, 12/0 tests/ui_server/test_projects_route.py.
C5 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f042-r6-mutations.py`.
  Subject: `F042 R6 C5: add the round 6 mutation tool`
C6 — THE SELF-USE ITEM (closure precondition 6), AFTER G1 to G4: run
  `bash -c 'python3 .agent/authored/f042-r6-selfuse.py 2>&1 | tee .remedy-wt/f042-r6-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  in the primary checkout with a Bash timeout of 3600000 milliseconds: the run makes real provider
  calls, each allowed ten minutes, and may take most of an hour. It appends the generated item to
  `scripts/self_use_queue.json`, runs it on the `self_use` role's configured provider, and writes
  `.agent/selfuse_f042/`. The reviewer's simulation of the tree at C4 read the item as `SU-036`, from Tier 1 of the generator, titled "Address ledger finding R-1107", whose task is R-1107's FIX in `tests/ui_server/test_story_export_file_live.py`;
  report what the run reads. A job that ends blocked or stopped is an OUTCOME to record, never a
  reason to stop or to re-run; only a Python exception before the job exists is a STOP. Commit
  `scripts/self_use_queue.json` and `.agent/selfuse_f042/**`, and nothing else.
  Subject: `F042 R6 C6: generate and run the closure's self-use item, record its readings`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F042 R6 C7: rewrite handoff for round 6`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. If one would reach
   500, split it into lettered parts before committing and declare the split.
3. The round's whole tracked path set is: the `.agent/authored/f042-r6-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/features/T5_F042.md`,
   `tests/ui_server/test_multi_project_live.py`, `tests/ui_server/test_projects_route.py`,
   `scripts/self_use_queue.json`, `.agent/selfuse_f042/**` and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only 79a2e7809` after C7. No file under `packages/` or `apps/`
   changes; no `consumed_by` is set this round, because the closure commit sets it.
4. The self-use job is NEVER applied: no `job apply`, no `--approve`, no copying of its files into
   the checkout. It may leave a `remedy/job-*` branch or an evidence directory behind; report each,
   and delete nothing you did not create as scratch.
5. If a gate other than the self-use outcome goes red, STOP, commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back. An EXISTING test that goes
   red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch switch, no branch deletion,
   no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash alone.
   The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action, and
   `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: it runs once, in the next round.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before C6, and G5 before C7.

G1 TRANSPORT AND RECORDS — each payload's measured lines, bytes and sha256 against the table; each
 `.agent/authored/f042-r6-*` copy byte-equal to its source (the block against
 `.remedy-wt/f042-r6/block.md`) by `git show <commit>:<path>` from the commit that added it; and the
 bytes and sha256 of each file below, read with `git show <commit>:<path>` at the commit named,
 equal to the reviewer's reading printed from its simulation tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2493168 | bd1e31bc213e3da6d8a336165989caa873b1a59612b2eacc59ca7f5ce43ac022 |
 | C2 | .agent/live_review.md | 326064 | 7a08df4d069a2e5be07893cb173e300ab05ea2f3299d9c1b8c0e86fbfba64eec |
 | C2 | .agent/plan.md | 1128 | ca8f1c8f0a62bdc3223c4dbb9ca6fd2a730569716307abb62d98bc16233ab7dc |
 | C2 | docs/agents/planner_reviewer_prompt.md | 112056 | 2d8b6758a3ac312970af3933756dd51d64c331edd47dbd38cc574bd731ec8908 |
 | C3 | docs/roadmap/features/T5_F042.md | 8352 | d99fd5b7c89dffe6d6982945f72125cfcd6fe284adaefbf8ed060faba1cbd03a |
 | C4 | tests/ui_server/test_multi_project_live.py | 5665 | f47fd9b83c7a94dc5b6b88363c9c9767a0ac830a0544e141750aa508b52bdfa4 |
 | C4 | tests/ui_server/test_projects_route.py | 7308 | 3e71aa6d484277e1539b0c5129766953604a28687d7f9119e3711bd6213c0bd4 |
 Also `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2 (the reviewer read `['R-1107', 'R-1111']` and `PASS`), and
 `live_checklist_items` of `packages/orchestration/block_lint.py` over the planner prompt at C2
 (the reviewer read 34 items).

G2 THE TESTS, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_multi_project_live.py tests/ui_server/test_projects_route.py tests/ui_server/test_pipeline_contract.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_job.py tests/orchestration/test_doc_staleness.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it in its simulation tree carrying C2 to C4 but no `.agent/authored/f042-r6-*`
 copy and read `674 passed, 1 skipped` at real exit code 0, the skip the D12 quarantine; report the counts
 and every SKIPPED line. `python3 -m ruff check tests/ui_server/test_multi_project_live.py
 tests/ui_server/test_projects_route.py .agent/authored/f042-r6-mutations.py
 .agent/authored/f042-r6-live_measure.py .agent/authored/f042-r6-selfuse.py`, its real exit code.
 Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks with
 status `pass` at `fail_count` 0.

G3 THE LIVE RUN — at C5, in the primary checkout:
 `python3 -B .agent/authored/f042-r6-live_measure.py /home/decodeux/Repos/remedy`. It registers two
 projects in a data root of its own, plans jobs and runs one on the fake providers, builds the
 cockpit with the primary's `vite` binary into `apps/ui/dist` (gitignored), serves it from a real
 UI server on 127.0.0.1 port 9010, drives Chrome at 1440 by 900 over CDP port 9372, stops both by
 pid and removes its work dir. Report its whole output from `jobs:` on and its exit code; it must
 print `LIVE: 7 of 7 checks pass` and exit 0. Read both screenshots,
 `/home/decodeux/Repos/remedy/.remedy-wt/f042-r6-live-home.png` and
 `/home/decodeux/Repos/remedy/.remedy-wt/f042-r6-live-cockpit.png`, and say in one sentence each
 what it shows. Then `git status --porcelain`, still empty.

G4 THE RED PROOFS — your tool `.agent/authored/f042-r6-mutations.py` takes a worktree path, and for
 each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once there), runs the named check, restores the bytes, and prints one line per mutation:
 its label, the exit code, and the failed count or the live run's `LIVE: <n> of 7` reading with
 the names of its failing checks. Pytest runs as `python3 -B -m pytest -q -p no:cacheprovider
 <file>` with the worktree as the working directory and first on `PYTHONPATH`; the live run as
 `python3 -B <worktree>/.agent/authored/f042-r6-live_measure.py <worktree>`. The tool runs an
 unmutated control of each check first and last, reports `restored byte-identical: True` after
 each restore, and ends with `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  m1 `project_summary` builds its scope with `all_projects=True`
     (`packages/orchestration/project_cockpit.py`, `tests/ui_server/test_multi_project_live.py`);
  m2 R-1111: `_build_project_summary_section` reads the legacy metadata key before the job's own
     `project_id` (`packages/orchestration/ui_server.py`, `tests/ui_server/test_projects_route.py`);
  m3 `_build_project_summary_section` counts every project's jobs, `all_projects=True` in its
     scope (same file, `tests/ui_server/test_multi_project_live.py`);
  l1 `RemedyApp.tsx` loses BOTH the shell's `key` and `openAddress`'s `setDashboard(null)`, the
     two mechanisms that each unmount the old shell on a switch (the live run, whose L-g must fail;
     either one alone keeps L-g passing, which the reviewer measured).
 Run it: `git worktree add --detach .remedy-wt/f042-r6-mut <C5>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f042-r6-mut/apps/ui/node_modules",
 target_is_directory=True)` unless that path already exists, then
 `python3 -B .agent/authored/f042-r6-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f042-r6-mut`
 and report its whole output. The reviewer's own probe turned every one red with every control
 passing, l1 failing L-g alone. EVERY mutation must exit non-zero; one that stays green is
 reported as green, never papered over, and you then STOP and report it. Then remove the link or
 directory at `apps/ui/node_modules` inside that worktree only (`os.unlink` for a link,
 `shutil.rmtree` for a directory, checking which with `os.path.islink` first), `git worktree remove
 --force .remedy-wt/f042-r6-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G5 THE SELF-USE READINGS — the whole output of C6's command and its real exit code; the item's id,
 title and provenance; the job's id and state; the builder and reviewer provider and model from
 `.agent/selfuse_f042/execution_config.txt`, which must name the `self_use` role's provider and
 never `fake`; the budgets and the budget actuals; every task's status, verdict and final status;
 `.agent/selfuse_f042/changed_paths.txt`, `staleness_after.txt`, `job_diff.txt` and
 `run_defects.txt` verbatim; and `git worktree list | wc -l` and the count of
 `git branch --list 'remedy/*'` after the run.

G6 SIZES, TREE AND PUSH — `git show --numstat --format= <commit>` for C1a to C6, each beside the
 expected insertions of its entry where one is stated and placed in the handback's `## Commits`
 table exactly as the tool printed it; and after C7, in your reply only: `git status --porcelain`
 empty, `git log --oneline -n 10` showing C7, C6, C5, C4, C3, C2, C1c, C1b, C1a and `79a2e7809` in
 that order, the push's real outcome, and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the self-use readings, the authored-text proofs,
the item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Report what you ran, not what you expected to find. Your Session section
reads SESSION 1 of feature F042, round 6, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6 and of the self-use run's diff, then the integration gate (the one full suite).
State the open-findings count, 2, and the operator-questions count, 1.
