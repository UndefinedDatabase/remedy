STEP F026 R6 — THE CLOSURE'S REPAIR ROUND: book round 5, repair R-1063, make R-1062's flag read a changed acceptance, and take the one full suite again on the repaired tree

GOAL
Round 5 passed, and the feature's full suite read one bad node, the write door's transitive import
guard, which is finding R-1063. Book round 5, resolve R-1061, register R-1063, repair it by moving
the DoD file's name into `packages/orchestration/data_paths.py`, correct R-1062's flag so it reads a
CHANGED acceptance, and take the feature's one full suite again on the repaired tree, replacing the
transcript at the same path (operator amendment amend0921-operator-feedback rule 1: the one run
belongs to the tree that ships). The evidence bundle and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue a
verdict, never merge, and never write a `Done:` line: when R-1063's repair lands you append ONE line,
`Landed: R-1063 — <one line: what changed, which commit>`, to `.agent/live_review.md`.

THE DIRECTORIES
  `.remedy-wt/f026-r6-payloads/` and `.remedy-wt/f026-r6/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f026-r6-sim/`, `.remedy-wt/f026-r6-dry/`, `.remedy-wt/f026-r6-drafts/`  The reviewer's.
  `.remedy-wt/f026-r6-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

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
   `git branch --show-current` `feature/f026-task-edit-runtime`, `git log --oneline -1` `40b94e02`.
3. Measure this block's line count and sha256 (`.remedy-wt/f026-r6/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*'` as found.

PAYLOADS — under `.remedy-wt/f026-r6-payloads/`; verify each BEFORE use and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1112 | 9cd57eb83f1b961f30113263f2bd1badaac8ebe8cf2cae1652a4a5fa4c84142b |
| records.diff | 23 | 7733 | bd6a5e4148e7a8a9775516fbc462fb83e9c7d7f8cdc2f0faf14cbcd3d9b24696 |

`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `40b94e02`)
appends round 5's gate entry, R-1061's `Done:` paragraph and R-1063's registration to
`.agent/live_review.md`, and one line to `.agent/prose_slips.md`.

THE SPECIFICATION OF THE REPAIR
S1 R-1063. `packages/orchestration/data_paths.py` gains, directly after `job_evidence_dir`, the
   constant `DOD_FILENAME = "dod.json"` and `job_dod_path(job_id, root=None) -> Path`, returning
   `job_evidence_dir(job_id, root) / DOD_FILENAME`, each with a one-line comment naming R-1063 and
   DECISION F260 D1. `packages/orchestration/dod_gate.py` no longer defines `DOD_FILENAME`: it
   imports it from `data_paths` inside its sorted import block (ruff's `I001` refuses it elsewhere),
   so `dod_gate.DOD_FILENAME` still resolves for every caller; nothing else there changes.
   `packages/orchestration/task_edit_runtime.py` imports `job_dod_path` from `data_paths`, reads the
   stored DoD as `job_dod_path(job_id, root).is_file()`, and no longer imports `dod_gate` at all.
   `ACCEPTED_TRANSITIVE_FORBIDDEN` and every other set in `tests/ui_server/test_command_channel.py`
   stay unchanged. The reviewer applied exactly this in a scratch tree at `40b94e02` and read the
   door's guard, `tests/orchestration/test_dod_gate.py` and `tests/orchestration/test_task_edit_runtime.py`
   green. `tests/test_data_paths.py` gains a test that `job_dod_path` is `dod.json` in
   `job_evidence_dir` under a given root, and that `dod_gate.dod_path(job_id)` equals
   `data_paths.job_dod_path(job_id)` under the process data root.
S2 R-1062's FLAG. `dod_resync_pending` is true only when the edited plan task's `acceptance`
   DIFFERS from the plan task's `acceptance` before the edit and the job has a stored DoD; passing an
   unchanged acceptance beside another changed field reads false. `TestDodResyncPending` in
   `tests/orchestration/test_task_edit_runtime.py` gains that case.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f026-r6-block.md` := this block and each payload as
   `.agent/authored/f026-r6-<name>`, by `shutil.copyfile`. Subject `F026 R6 C1: copy round 6 block and
   payloads`. Its insertions are this block's line count plus 54.
C2 RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject
   `F026 R6 C2: book round 5, resolve R-1061, register R-1063`. Expected by `git show --numstat`:
   6/0 .agent/live_review.md, 8/10 .agent/plan.md, 1/0 .agent/prose_slips.md.
C3 THE REPAIR: S1 and S2 with their tests and the `Landed: R-1063 — ` line. Subject
   `F026 R6 C3: the DoD file's name lives with the job layout, and the edit reads it without the gate (R-1063)`.
C4 THE MUTATION TOOL `.agent/authored/f026-r6-mutations.py` (G4). Subject `F026 R6 C4: the round's
   red-proof mutation tool`.
C5 THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C4: (a) `bash -c 'npm
   --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — a failing build is
   a STOP — then `git status --porcelain`, still empty. (b) `python3 -m pytest -n auto -q`, its log
   under `.remedy-wt/f026-r6-worker/`; measure its wall time. REWRITE
   `.agent/authored/f026-closure-suite.txt` whole, in round 5's format: the command, the real exit
   code, the wall time, the summary line and the FULL list of bad node ids (failed plus errors), or
   the literal `NONE`, plus one line naming the tree it ran on (C4's SHA) and saying it replaces round
   5's run at `40b94e02` under amend0921-operator-feedback rule 1. (c) Rewrite `.agent/handoff.md` per
   `docs/agents/handback_template.md` and commit it TOGETHER with the transcript. Subject
   `F026 R6 C5: record the closure suite on the repaired tree and rewrite handoff for round 6`. Then
   `git push origin feature/f026-task-edit-runtime`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set: the `.agent/authored/f026-r6-*` copies and tool,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `packages/orchestration/data_paths.py`, `packages/orchestration/dod_gate.py`,
   `packages/orchestration/task_edit_runtime.py`, `tests/test_data_paths.py`,
   `tests/orchestration/test_task_edit_runtime.py`, `.agent/authored/f026-closure-suite.txt` and
   `.agent/handoff.md`. No edit to `tests/ui_server/test_command_channel.py`, `README.md`,
   `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`, `.agent/decisions.md`,
   `.agent/candidates.md` or `.agent/operator_questions.md`.
4. The repair must STRICTLY SHRINK the bad set with NO node newly bad (amend0917-throughput rule 2):
   round 5's set is the one guard node. If C5's suite is red, commit the transcript exactly as
   measured, report every bad node id, and hand back; never weaken an assertion, delete a test or
   mark anything xfail.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip.
6. Leave every existing worktree, branch and stash alone, including the self-use job's
   `remedy/job-fd57a5d1dfe245b0`. The G4 worktree goes under `.remedy-wt/` and is removed after.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
C5 is written; G5 is C5's suite.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f026-r6-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE RECORDS: `git show <C2>:<path>` of each file below hashes to the reviewer's simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 338125 | 3082dd8e3b1e06d6aaa80ce1aa76d3bc541a8befb39d2f1aefd27d98cc1062e4 |
   | C2 | .agent/prose_slips.md | 368585 | 37eb9109526e55f498313086ffc0b51fa9a8786ba75dfb979fc94fceb4cd97a0 |
   | C2 | .agent/plan.md | 1112 | 9cd57eb83f1b961f30113263f2bd1badaac8ebe8cf2cae1652a4a5fa4c84142b |
   and `open_finding_ids` over the ledger reads R-1008, R-1055, R-1057, R-1058, R-1062 and R-1063 at
   C2 and at C4; the ledger's last line at C3 begins `Landed: R-1063 — `.
G3 THE CODE: `python3 -m ruff check packages/orchestration/data_paths.py
   packages/orchestration/dod_gate.py packages/orchestration/task_edit_runtime.py tests/test_data_paths.py
   tests/orchestration/test_task_edit_runtime.py` at C3; a python `ast` reading at C3 of every
   `Import` and `ImportFrom` node of `packages/orchestration/task_edit_runtime.py`, which must name
   no `dod_gate`; and `git diff -U0 40b94e02 <C3> -- packages/orchestration/dod_gate.py`, whole.
G4 THE TESTS AND THE RED PROOFS, in the primary checkout at C4, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_command_channel.py
   tests/ui_server/test_command_dispatch.py tests/orchestration/test_dod_gate.py
   tests/orchestration/test_task_edit_runtime.py tests/test_data_paths.py
   tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/docs
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
   tests/orchestration/test_block_lint.py tests/orchestration/test_roadmap_index.py
   tests/cli/test_golden_path.py 2>&1 | tail -5; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — exit 0. The
   reviewer ran it without `tests/test_data_paths.py` and the golden path in a tree at `40b94e02`
   carrying C2's records and read `1 failed, 610 passed`, the one failure being R-1063's guard node, which must
   PASS in your run. Then `python3 -m apps.cli.main integrity check --json`, six `pass` at
   `fail_count` 0. Then your tool, run in `git worktree add --detach .remedy-wt/f026-r6-mut <C4>`
   (pytest under `python3 -B` after purging `__pycache__`, over the worktree's
   `tests/ui_server/test_command_channel.py`, `tests/orchestration/test_task_edit_runtime.py` and
   `tests/test_data_paths.py`): m1 `task_edit_runtime.py` imports `dod_gate` again (one added import
   line — the door's guard must go red); m2 `job_dod_path` returns the path without `DOD_FILENAME`;
   m3 `dod_resync_pending` reads `"acceptance" in fields` again. Controls first and last, every
   mutation red, the last line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`, whole output
   reported; then `git worktree remove --force .remedy-wt/f026-r6-mut`.
G5 THE INTEGRATION GATE: the UI build's last line and real exit code, `git status --porcelain` after
   it, the full suite's real exit code, wall time, summary line and every bad node id, all in the
   rewritten `.agent/authored/f026-closure-suite.txt`; whether round 5's bad node passes; and whether
   any node is newly bad.
G6 AFTER C5 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f026-task-edit-runtime`, `git log --oneline -n 7`, `git worktree list`,
   `git branch --list 'remedy/job-*'`, the push's real outcome, and `gh pr list --state open --json
   number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the full suite's summary line and bad node ids, the authored-text
proofs, the item-status table AGENTS.md requires (one row per commit, per gate and per S-item), the
deviations, and the next action. Session section: SESSION 1 of feature F026, round 6, plus one
sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of round 6, then the
closure's evidence round — the booking of round 6, the evidence bundle and the review package — and
then the closing round. State the open-findings count as the script reads it at C4, and "Operator
questions open: <the count of `### Q` headings in the file at C2>".
