STEP F027 R11 — THE CLOSURE'S REPAIR ROUND: book round 10, register and repair R-1071, and take the one full suite again on the repaired tree

GOAL
Round 10 passed, and the feature's full suite read one bad node, an exact-set pin of the completed
episode's tight expectation sets that DECISION F027 D4 (5) widened, which is finding R-1071. Book
round 10, register R-1071, repair it in its test file, and take the feature's one full suite again on
the repaired tree, replacing the transcript at the same path (operator amendment
amend0921-operator-feedback rule 1: the one run belongs to the tree that ships). The evidence bundle
and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue a
verdict, never merge, and never write a `Done:` line: when R-1071's repair lands you append a blank
line and ONE line, `Landed: R-1071 — <one line: what changed>, at this round's C3.`, to
`.agent/live_review.md`.

THE DIRECTORIES
  `.remedy-wt/f027-r11-payloads/` and `.remedy-wt/f027-r11/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f027-r11-drafts/`, `.remedy-wt/f027-r8-dry/`, `.remedy-wt/f027-review/` and every
  older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r11-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, `for` loops, and one-liners chained
with `;` or `&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
read `${PIPESTATUS[0]}` when you pipe. Use `git -C <path>`; never `cd` into a worktree. The ONE npm
command this round may run is C5's `npm --prefix apps/ui run build`; never `npm install`, `npm ci` or
`npx`. Never `git stash`, `git commit --amend`, `pkill -f` or `git worktree prune`.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f027-task-veto`, `git log --oneline -1` `2425626a`.
3. Measure this block's line count and sha256 (`.remedy-wt/f027-r11/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*'` as found.

PAYLOADS — under `.remedy-wt/f027-r11-payloads/`; verify each BEFORE use and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 29 | 1039 | b3e9e2e2aa28f70720b555ef8b42680d629d32808459eb6bc1b6752e2bc583c6 |
| records.diff | 12 | 5070 | 412c10e61b096ad09ecb199e0d96a4009c06d0c138aafbae547c8edc84b5c01c |

`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `2425626a`)
appends round 10's gate entry and R-1071's registration to `.agent/live_review.md`.

THE SPECIFICATION OF THE REPAIR
S1 R-1071, in `tests/orchestration/test_task_expectation_episode_context.py` alone, as its FIX says:
   `test_the_context_helper_is_tight_for_completed_worked` asserts that `_allowed_statuses_for`
   answers exactly `{"passed", "applied_to_job_workspace", "vetoed"}` for both `EXPECT_EXECUTED` and
   `EXPECT_PRIOR_EPISODE`, with a one-line comment naming DECISION F027 D4 (5) and R-1071; and the
   parametrization of `test_a_completed_executed_task_that_actually_completed_passes` gains
   `"vetoed"`. The reviewer measured at `2425626a` that `TestCompletedWorkedIsNarrow._forge("vetoed")`
   returns `[]`. `packages/orchestration/run_manifest.py` does not change.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f027-r11-block.md` := this block and each payload as
   `.agent/authored/f027-r11-<name>`, by `shutil.copyfile`. Subject `F027 R11 C1: copy round 11 block
   and payloads`. Its insertions are this block's line count plus 41.
C2 RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject
   `F027 R11 C2: book round 10, register R-1071`. Expected by `git show --numstat`:
   4/0 .agent/live_review.md, 8/9 .agent/plan.md.
C3 THE REPAIR: S1 and the `Landed: R-1071 — ` line. Subject
   `F027 R11 C3: the completed episode's tight-set pin reads the vetoed status D4 rules (R-1071)`.
C4 THE MUTATION TOOL `.agent/authored/f027-r11-mutations.py` (G4). Subject `F027 R11 C4: the round's
   red-proof mutation tool`.
C5 THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C4: (a) `bash -c 'npm
   --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — a failing build is
   a STOP — then `git status --porcelain`, still empty. (b) `python3 -m pytest -n auto -q`, its log
   under `.remedy-wt/f027-r11-worker/`; measure its wall time. REWRITE
   `.agent/authored/f027-closure-suite.txt` whole, in round 10's format: the command, the real exit
   code, the wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the
   literal `NONE`, and one line naming the tree it ran on (C4's SHA) and saying it replaces round
   10's run at `02890eaf` under amend0921-operator-feedback rule 1. (c) Rewrite `.agent/handoff.md`
   per `docs/agents/handback_template.md` and commit it TOGETHER with the transcript. Subject
   `F027 R11 C5: record the closure suite on the repaired tree and rewrite handoff for round 11`.
   Then `git push origin feature/f027-task-veto`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set: the `.agent/authored/f027-r11-*` copies and tool,
   `.agent/live_review.md`, `.agent/plan.md`,
   `tests/orchestration/test_task_expectation_episode_context.py`,
   `.agent/authored/f027-closure-suite.txt` and `.agent/handoff.md`. No edit to `packages/`, `apps/`,
   any other test, `README.md`, `docs/`, `scripts/`, `.agent/decisions.md`, `.agent/candidates.md`
   or `.agent/operator_questions.md`.
4. The repair must STRICTLY SHRINK the bad set with NO node newly bad (amend0917-throughput rule 2):
   round 10's set is the one pin node. If C5's suite is red, commit the transcript exactly as
   measured, report every bad node id, and hand back; never weaken an assertion, delete a test or
   mark anything xfail.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip.
6. Leave every existing worktree, branch and stash alone. The G4 worktree goes under `.remedy-wt/`
   and is removed after.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
C5 is written; G5 is C5's suite.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f027-r11-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE RECORDS: `git show <C2>:<path>` of each file below hashes to the reviewer's simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 331521 | eb8b293299b3f82a2cc3786fe08922a89caa61ce00bdabbb4aa5f96fa7819d1f |
   | C2 | .agent/plan.md | 1039 | b3e9e2e2aa28f70720b555ef8b42680d629d32808459eb6bc1b6752e2bc583c6 |
   and `open_finding_ids` over the ledger reads `['R-1071']` at C2 and at C4; the ledger's last line
   at C3 begins `Landed: R-1071 — `.
G3 THE CODE: `python3 -m ruff check tests/orchestration/test_task_expectation_episode_context.py` at
   C3, and `git diff 2425626a <C3> -- tests/orchestration/test_task_expectation_episode_context.py`,
   whole.
G4 THE TESTS AND THE RED PROOFS, in the primary checkout at C4, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_task_expectation_episode_context.py
   tests/orchestration/test_task_expectation_status_truth.py tests/orchestration/test_task_veto_runner.py
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
   tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — exit 0. Then
   `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count` 0. Then your tool,
   run in `git worktree add --detach .remedy-wt/f027-r11-mut <C4>` (pytest under `python3 -B` after
   purging `__pycache__`, over the worktree's
   `tests/orchestration/test_task_expectation_episode_context.py`): m1 `vetoed` leaves the completed
   worked `EXPECT_EXECUTED` tight set in `packages/orchestration/run_manifest.py` — the new `vetoed`
   case and the pin must go red; m2 `vetoed` leaves its `EXPECT_PRIOR_EPISODE` tight set — the pin
   must go red. Assert each FROM occurs exactly once in the file. Control first and last, every
   mutation red, the last line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`, whole output
   reported; then `git worktree remove --force .remedy-wt/f027-r11-mut` and `git worktree list`.
G5 THE INTEGRATION GATE: the UI build's last line and real exit code, `git status --porcelain` after
   it, the full suite's real exit code, wall time, summary line and every bad node id, all in the
   rewritten `.agent/authored/f027-closure-suite.txt`; whether round 10's bad node passes; and whether
   any node is newly bad.
G6 AFTER C5 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f027-task-veto`, `git log --oneline -n 6`, `git worktree list`,
   `git branch --list 'remedy/job-*'`, the push's real outcome, and `gh pr list --state open --json
   number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the full suite's summary line and bad node ids, the authored-text
proofs, the item-status table AGENTS.md requires (one row per commit, per gate and per S-item), the
deviations, and the next action. Session section: SESSION 2 of feature F027, round 11, plus one
sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of round 11, then
the closure's evidence round — the booking of round 11, the Built State's note on R-1071, the
evidence bundle and the review package — and then the closing round. State the open-findings count
as the script reads it at C4, and "Operator questions open: 5".
