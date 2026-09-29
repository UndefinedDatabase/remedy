STEP F042 R7 — THE INTEGRATION GATE: book round 6, land the self-use item's diff, complete the Built State, and take the feature's one full suite

GOAL
Round 6 is reviewed PASS at `19ccafd4c`; its gate entry is carried verbatim in `.agent/handoff.md`,
and the operator has since carried `main` into the branch twice (`edfcf4638`, `c36841c6f`), so the
suite below runs on the tree that ships. Book round 6 with R-1111's resolution, record DECISION F042
D7, land the closure's self-use item `SU-036` as its job's diff with the reviewer's one added
assertion (it repairs R-1107), append the self-use paragraph to F042's Built State, prove the
repair red, then build `apps/ui` and run this feature's ONE full suite on the tree that ships and
commit its transcript. The evidence bundle, the review package, the rotation, the STATUS line and
the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` or `Landed:` line. Every change this round
makes travels as a payload. Read first `docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3
and 7 and `docs/agents/integration_gate.md`, and read `tests/ui_server/test_story_export_file_live.py`
whole before C3.

THE DIRECTORIES
  `.remedy-wt/f042-r7-payloads/` and `.remedy-wt/f042-r7/`  READ-ONLY. The reviewer's.
  every other `.remedy-wt/f042-*` path: the reviewer's; do not touch.
  `.remedy-wt/f042-r7-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, `ln`, `sed`, process and command substitution, `cd <dir> && ...`, `for` loops, and one-liners
chained with `;` or `&&` outside a `bash -c`. Capture exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe. Use
`git -C <path>`; never `cd` into a worktree. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`); write any script holding a dollar-brace or a brace next to a quote to
a file under your own directory and run it; run a program in another directory with
`subprocess.run(..., cwd=...)`. Never run npm or npx. Never `git stash`, never `git commit --amend`,
never `pkill -f`: stop a process only by its own recorded pid. The `remedy` command may be denied;
use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f042-multi-project-cockpit`, `git log --oneline -1`
   `c36841c6f`.
3. Measure this block's line count and sha256 (`.remedy-wt/f042-r7/block.md`) against your
   delegation message's readings; report both beside both, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f042-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 45 | 7630 | 4e2523cc277f49c7f4bb1ef8fea9a74289a731ea87c566ef0028724e8a8fd856 |
| selfuse.diff | 103 | 5091 | 2a2834a75df5734dd400afda29a9beb895375a12aaaeecd3c9a37483848cb2ad |
| built_state.diff | 17 | 1283 | 289ab2578040d8ca6d44f78ac655b4de1c72a75f1fb562332670a2a6d1c95acc |
| plan.md | 29 | 971 | 0d064dc2dc959771f7a557533a04aae4ec48a69c27a5fbe97fbb56858aff0c92 |

`plan.md` REWRITES `.agent/plan.md`. The three diffs were generated with `git diff HEAD` from the
reviewer's simulation tree at `c36841c6f` and go on with `git apply`, in the order C2, C3 and C4
name. `records.diff` appends to `.agent/live_review.md` round 6's gate entry, VERDICT PASS, and
R-1111's `Done:` resolution, and to `.agent/decisions.md` DECISION F042 D7. `selfuse.diff` is the
job `6dad54d0e18348c4`'s own change to `tests/ui_server/test_story_export_file_live.py`, as its
branch `remedy/job-6dad54d0e18348c4` holds it, with the one assertion D7 adds. `built_state.diff`
appends the self-use paragraph to `docs/roadmap/features/T5_F042.md`.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f042-r7-block.md` := this block and each payload as
   `.agent/authored/f042-r7-<name>`, by `shutil.copyfile`. Subject `F042 R7 C1: copy round 7
   block and payloads`. Its insertions are this block's line count plus 194; STOP rather than
   commit at 500 or more.
C2 RECORDS: `git apply --check` then `git apply` records.diff, then `.agent/plan.md` := plan.md.
   Subject `F042 R7 C2: book F042 R6 with R-1111's resolution, record D7`. Expected by
   `git show --numstat`: 25/0 .agent/decisions.md, 4/0 .agent/live_review.md, 9/17 .agent/plan.md.
C3 THE SELF-USE DIFF: `git apply --check` then `git apply` selfuse.diff. Subject `F042 R7 C3: land
   the closure's self-use item SU-036, the repair of R-1107`. Expected by `git show --numstat`:
   42/5 tests/ui_server/test_story_export_file_live.py.
C4 THE BUILT STATE: `git apply --check` then `git apply` built_state.diff. Subject `F042 R7 C4:
   record the self-use item in F042's Built State`. Expected by `git show --numstat`: 9/0 docs/roadmap/features/T5_F042.md.
C5 THE TOOL: your mutation tool (G3) saved as `.agent/authored/f042-r7-mutations.py`. Subject
   `F042 R7 C5: add the round 7 mutation tool`.
C6 THE INTEGRATION GATE, in the PRIMARY checkout, after C5 and after G1 to G3. (a) run
   `apps/ui/node_modules/.bin/vite build` with `cwd` `apps/ui` from a Python script, report its exit
   code and last line — a failing build is a STOP — then `git status --porcelain`, still empty.
   (b) `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f042-r7-worker/`; measure its wall
   time. Write `.agent/authored/f042-closure-suite.txt` holding the command, the real exit code, the
   wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the literal
   `NONE`, and one line naming the tree it ran on (C5's SHA). After the suite, report the processes
   `pgrep -af server.py` lists, which must be none. (c) Rewrite `.agent/handoff.md` per
   `docs/agents/handback_template.md` and commit it TOGETHER with the transcript. Subject `F042 R7
   C6: record the closure suite transcript and rewrite handoff for round 7`. Then `git push`. No
   pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set: the `.agent/authored/f042-r7-*` files, `.agent/live_review.md`,
   `.agent/decisions.md`, `.agent/plan.md`, `tests/ui_server/test_story_export_file_live.py`,
   `docs/roadmap/features/T5_F042.md`, `.agent/authored/f042-closure-suite.txt` and
   `.agent/handoff.md`. Report `git diff --name-only c36841c6f` at the tip. No edit to `README.md`,
   `docs/roadmap/STATUS.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `scripts/self_use_queue.json` or any file under `packages/` or `apps/`. The self-use job is never
   applied and its branch is left as it is.
4. A RED full suite in C6 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to order
   (amend0917-throughput rule 2). Never weaken an assertion, delete a test, skip or mark anything
   xfail. An EXISTING test that goes red before C6 is never edited to pass; report it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no amend; no evidence job; no
   zip; do not run the self-use runner or any job that calls a provider.
6. Leave every existing worktree, branch and stash alone, the reviewer's included. The worktree G3
   adds goes under `.remedy-wt/`, is removed as that gate's last action, and
   `git worktree list | wc -l` is reported afterwards.
7. The full suite runs ONCE, in C6, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding. G1 to G3 run before C6 is written; G4 is C6's suite.
G1 TRANSPORT AND RECORDS: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f042-r7-*` payload copy byte-equal to its source by `git show <C1>:<path>`;
   and `git show <read at>:<path>` of each file below hashes to the reviewer's tree:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/decisions.md | 2501470 | da266e21688c306ad57354025cac3d41efbfb179262ac3ea22026c77f60514b0 |
   | C2 | .agent/live_review.md | 151944 | 9e2fe9424e73c0eba9fd8ef36a40a124244e734265b87a3e76bb35831e62b98c |
   | C2 | .agent/plan.md | 971 | 0d064dc2dc959771f7a557533a04aae4ec48a69c27a5fbe97fbb56858aff0c92 |
   | C3 | tests/ui_server/test_story_export_file_live.py | 14707 | 0c93cb10be7c41b94a7c91d653c467b210ff00964312734c74f6b83c1b29a0df |
   | C4 | docs/roadmap/features/T5_F042.md | 9032 | 7bac54d72b1cd5fe728793b8e399c2ffae01f7780cc71b46b0b13595d99fefdc |
   `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the ledger
   at C2 read `['R-1107']` and `PASS`.
G2 THE TESTS, in the primary checkout at C5, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_story_export_file_live.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — the reviewer read `550 passed, 2 skipped` at exit 0 in its tree carrying C2 to C4 but no `.agent/authored/f042-r7-*`
   copy and no `node_modules`, the skips the D12 quarantine and the story test for want of `vite`,
   which your checkout has, so the story test must run and pass here. Report the summary and every
   SKIPPED line. `python3 -m ruff check tests/ui_server/test_story_export_file_live.py
   .agent/authored/f042-r7-mutations.py`, its real exit code. Then
   `python3 -m apps.cli.main integrity check --json`: six `pass` at `fail_count` 0; then
   `python3 -m apps.cli.main integrity block .remedy-wt/f042-r7/block.md`, real exit code and whole
   output; and `git status --porcelain` empty with no untracked file (closure precondition 3).
G3 THE RED PROOFS OF R-1107'S REPAIR: your tool `.agent/authored/f042-r7-mutations.py` takes a
   worktree path, and for each mutation below edits `tests/ui_server/test_story_export_file_live.py`
   INSIDE that worktree (asserting its FROM text occurs exactly once there), runs
   `python3 -B -m pytest -q -p no:cacheprovider tests/ui_server/test_story_export_file_live.py::test_chrome_timeout_message_names_log`
   with the worktree as the working directory and first on `PYTHONPATH`, restores the bytes, and
   prints its label, exit code and failed count, with an unmutated control first and last,
   `restored byte-identical: True` after each restore, and a last line
   `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
    r1 `ChromePipe._read_message` leaves the log's last lines out of the timeout message;
    r2 it leaves the log's path out of the message;
    r3 `ChromePipe.__init__` sends Chrome's standard error to `subprocess.DEVNULL` again.
   Run it on `git worktree add --detach .remedy-wt/f042-r7-mut <C5>` and report its whole output;
   the reviewer's probe turned all three red with both controls passing. Then
   `git worktree remove --force .remedy-wt/f042-r7-mut`, `git worktree prune`, and report
   `git worktree list | wc -l`.
G4 THE INTEGRATION GATE: the UI build's last line and real exit code; `git status --porcelain`
   after it; then the full suite's real exit code, wall time, summary line and every bad node id,
   all in `.agent/authored/f042-closure-suite.txt`; the `server.py` reading; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
   bad node (closure precondition 7).
G5 AFTER C6 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f042-multi-project-cockpit`, `git log --oneline -n 7`,
   `git worktree list | wc -l`, `git branch --list 'remedy/*' | wc -l`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the full suite's summary line and bad node ids, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next action. Session section: SESSION 2 of feature F042, round 7 (re-delegated after session 1's halt at `.agent/STOP`), rounds so
far 7, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of
round 7 and of its suite transcript, then the closure's evidence round — the booking of round 7,
any repair the suite requires, the evidence bundle and the review package — and then the closing
round. State the open-findings count, 1, and "Operator questions open: 0".
