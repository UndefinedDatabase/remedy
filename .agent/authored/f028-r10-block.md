STEP F028 R10 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 9, write the Built State, consolidate the checklist, ask the self-use generator for the closure's item, and take the feature's one full suite

GOAL
Book round 9's PASS, append the Built State to `docs/roadmap/features/T5_F028.md`, run the checklist
consolidation pass (it joins nothing and keeps `docs/agents/planner_reviewer_prompt.md` §3 at 34
items), ask the self-use generator for the closure's item (closure precondition 6), and run this
feature's ONE full suite on the tree that ships, committing its transcript. The evidence bundle, the
review package, the ledger rotation, the STATUS line and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue a
verdict, never merge, and never write a `Done:` line. Read first:
`docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3, 6 and 7, and
`docs/agents/integration_gate.md`.

THE DIRECTORIES
  `.remedy-wt/f028-r10-payloads/` and `.remedy-wt/f028-r10/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f028-r10-drafts/`, `.remedy-wt/f028-r10-sim/`, `.remedy-wt/f028-review/` and every
  older `f028-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f028-r10-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, `for` loops, and one-liners chained
with `;` or `&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
read `${PIPESTATUS[0]}` when you pipe. Use `git -C <path>`; never `cd` into a worktree. Write any
script holding a dollar-brace or a brace-quote shape to a file under your own directory and run it.
The ONE npm command this round may run is C4's `npm --prefix apps/ui run build`; never `npm install`,
`npm ci` or `npx`. Never `git stash`, never `pkill -f`, never `git worktree prune`. The `remedy`
command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f028-task-injection`, `git log --oneline -1` `969c6b5e`.
3. Measure this block's line count and sha256 (`.remedy-wt/f028-r10/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r10-payloads/`; verify each one's line count, byte count and sha256
BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| closure_docs.diff | 130 | 10442 | 9b2ace7316f8ab2a91d5f708aef06feedf0462fdceaae1eb50ec527ecb13d4ad |
| plan.md | 30 | 1069 | 7619d7d2d61de0b44c2e0b4ad5c807ea13978c17dfd92d95d72d2814d6da9e8b |
| records.diff | 10 | 5162 | eb83ce157268501b9ba88e8b24bc40f5a3012f1197fbed6c1f498641b7ebd19a |

`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `969c6b5e`)
appends round 9's gate entry to `.agent/live_review.md`, after one blank line. `closure_docs.diff`,
generated in the same tree on top of it, appends the Built State to
`docs/roadmap/features/T5_F028.md` and replaces, in `docs/agents/planner_reviewer_prompt.md`, the line
`  The next consolidation measures against 34.` with the consolidation paragraph that ends with it
(containment test: TO contains FROM: true — an APPEND; the line occurs once before and once after).

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f028-r10-block.md` := this block and each payload as
   `.agent/authored/f028-r10-<name>`, by `shutil.copyfile`. Subject `F028 R10 C1: copy round 10 block
   and payloads`. Its insertions are this block's line count plus 170.
C2 RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject
   `F028 R10 C2: book round 9`. Expected by `git show --numstat`: 2/0 .agent/live_review.md, 10/8
   .agent/plan.md.
C3 THE BUILT STATE AND THE CONSOLIDATION: `git apply` closure_docs.diff. Subject
   `F028 R10 C3: write the Built State and consolidate the checklist`. Expected by
   `git show --numstat`: 10/0 docs/agents/planner_reviewer_prompt.md, 101/0
   docs/roadmap/features/T5_F028.md.
C4 THE SELF-USE ITEM AND THE INTEGRATION GATE, in the PRIMARY checkout, after C3. (a) From a scratch
   Python file of yours: `packages.orchestration.self_use_generator.generate_and_append_if_empty()`
   with no arguments, then `packages.orchestration.self_use_queue.next_self_use_item()`; report both
   return values verbatim. The reviewer's dry run on a tree byte-equal to C3's read `None` for both,
   because the queue holds no pending item, the ledger no open finding, and neither the staleness
   catalog nor `doctor core` offers a claim. If yours reads `None` too, nothing is written and closure
   precondition 6 reads `self-use NONE (queue exhausted)`; if it appends an item instead, STOP after
   this step, commit `scripts/self_use_queue.json` alone with subject `F028 R10 C4a: the generator
   appended a self-use item`, and hand back without running it.
   (b) `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` —
   a failing build is a STOP — then `git status --porcelain`, still empty. (c)
   `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f028-r10-worker/`; measure its wall
   time. Write `.agent/authored/f028-closure-suite.txt` holding the command, the real exit code, the
   wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the literal
   `NONE`, and one line naming the tree it ran on (C3's SHA). (d) Rewrite `.agent/handoff.md` per
   `docs/agents/handback_template.md` and commit it TOGETHER with the transcript. Subject
   `F028 R10 C4: record the closure suite transcript and rewrite handoff for round 10`. Then
   `git push origin feature/f028-task-injection`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; `git apply --check` before each `git apply`, exit codes reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set: the `.agent/authored/f028-r10-*` copies, `.agent/live_review.md`,
   `.agent/plan.md`, `docs/roadmap/features/T5_F028.md`, `docs/agents/planner_reviewer_prompt.md`,
   `.agent/authored/f028-closure-suite.txt` and `.agent/handoff.md`, and `scripts/self_use_queue.json`
   only in C4(a)'s stop case. No edit to `README.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or any file under `packages/`, `apps/` or
   `tests/`.
4. A RED full suite in C4 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to order
   (amend0917-throughput rule 2). Never weaken an assertion, delete a test or mark anything xfail.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip.
6. Leave every existing worktree, branch and stash alone.
7. The full suite runs ONCE, in C4, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
C4 is written; G5 is C4's suite.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f028-r10-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE RECORDS: `git show <read at>:<path>` of each file below hashes to the reviewer's simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 339147 | d607d6739d94295005ef8d61a5fa4e0d5608a3be416b6ac9c9467ecf8e8d7fda |
   | C2 | .agent/plan.md | 1069 | 7619d7d2d61de0b44c2e0b4ad5c807ea13978c17dfd92d95d72d2814d6da9e8b |
   | C3 | docs/roadmap/features/T5_F028.md | 13131 | 1be63e3198cde648777f04624bb87fa744e2062e4653f2b0f74487d0ff2b852d |
   | C3 | docs/agents/planner_reviewer_prompt.md | 106796 | 76037d336f5065d7a08db99a764cbf483e6b58468d7fdefc578b4e99c259a5d8 |
   `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger reads `[]` at C2; and
   `live_checklist_items` of `packages/orchestration/block_lint.py` over the planner prompt reads the
   same 34 numbers at `969c6b5e` and at C3.
G3 THE LINTER: `python3 -m apps.cli.main integrity block .remedy-wt/f028-r10/block.md` at C3, real
   exit code 0, whole output.
G4 THE TESTS AND THE TREE, in the primary checkout at C3, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs/ tests/orchestration/test_block_lint.py
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
   tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py
   tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — exit 0, the summary line and every SKIPPED line reported (the reviewer read the same selection
   at 595 passed and 1 skipped on its simulated tree, which has no `apps/ui/node_modules`); then
   `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count` 0 — the status of
   each check is the reading, not the exit code; and `git status --porcelain` empty with no
   untracked file (closure precondition 3).
G5 THE INTEGRATION GATE: C4(a)'s two return values; the UI build's last line and real exit code;
   `git status --porcelain` after it; then the full suite's real exit code, wall time, summary line
   and every bad node id, all in `.agent/authored/f028-closure-suite.txt`; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a bad
   node (closure precondition 7).
G6 AFTER C4 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip equal
   to `origin/feature/f028-task-injection`, `git log --oneline -n 5`, `git worktree list | wc -l`,
   `git branch --list 'remedy/job-*' | wc -l`, the push's real outcome, and `gh pr list --state open
   --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the self-use readings, the full suite's summary line and bad node
ids, the authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per
gate), the deviations, and the next action. Session section: SESSION 2 of feature F028, round 10,
rounds so far 10, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the
review of round 10, then the closure's evidence round — the booking of round 10, any repair the
suite requires, the evidence bundle and the review package — and then the closing round. State the
open-findings count, 0, and "Operator questions open: 0".
