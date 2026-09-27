STEP F028 R8 — THE REPAIR OF ROUND 7: BOOK ROUND 7'S FAIL AND REGISTER R-1079 FIRST, RECORD D8 AND TWO PROSE SLIPS, RENDER THE ADD TASK SHEET THROUGH A PORTAL, AND NAME AN INJECTED TASK'S ORIGIN ON ITS LINE OF THE FINAL REPORT

GOAL
Round 7 failed on R-1079: the reviewer's headless render measured the Add Task sheet squeezed into
the tasks card, because the card's glass rule captures fixed positioning. Persist the FAIL and the
finding first, then repair it: the sheet renders through a portal into the document's body. And
give the final report the injected task's provenance: its task line says it was added by the
operator while the job ran.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests against S1 and S2. Read R-1079 and DECISION F028 D8 (both arrive
with C2), `apps/ui/src/components/panels/AddTaskSheet.tsx` whole, and in
`packages/orchestration/run_report.py` `TaskOutcome`, `_task_lines`, `collect_report_sources` and
`_tasks_with_apply_state` whole.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r8-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r8/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r1-sim/` to `.remedy-wt/f028-r8-sim/`  The reviewer's simulation trees.
  `.remedy-wt/f028-review/`       The reviewer's scripts and render harness; do not touch them.
  `.remedy-wt/f028-r8-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx from the shell; vitest, tsc and eslint run through the pytest nodes of
G4.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f028-task-injection`, and `git log --oneline -1` must read `41f591a3`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r8/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r8-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 29 | 1011 | f615125f62041ca38504b5778836abca6f24ec7ce82e20974afbae86e3fc44d8 |
| records.diff | 58 | 11888 | 1944d395635d66c2db78ffbf75bdb8e47e88d76915baf969bb56a4263230aa55 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; it appends
round 7's gate entry, VERDICT FAIL, and R-1079's registration to `.agent/live_review.md`,
DECISION F028 D8 to `.agent/decisions.md`, and two lines to `.agent/prose_slips.md`.

THE SPECIFICATION
S1 R-1079. `AddTaskSheet` in `apps/ui/src/components/panels/AddTaskSheet.tsx` keeps its markup,
   state, effects and props, and returns its `<section>` through
   `createPortal(<section ...>...</section>, document.body)` imported from `react-dom`; a comment
   names R-1079 and says why: the card's `backdrop-filter` makes it the containing block of every
   fixed descendant. Nothing else in the file changes. `TaskChecklistCard.tsx` still mounts it.
S2 THE REPORT, in `packages/orchestration/run_report.py`: `TaskOutcome` gains `origin: str = ""`
   as its last field, with a comment naming DECISION F028 D8; `collect_report_sources` fills it
   with the task entry's `inputs["plan"]["origin"]` when `inputs["plan"]` is a dict and that value
   is a non-empty `str`, else `""`; wherever a `TaskOutcome` is rebuilt from another (read
   `_tasks_with_apply_state`) the origin survives; and `_task_lines` appends
   `" — added by you while the job ran"` to the line of a task whose `origin` is
   `"human_injected"`, after the apply clause and before the evidence link. Every other line is
   byte-identical to today's.

THE TESTS — `tests/ui_contracts/test_inject_controls_contract.py` gains: `AddTaskSheet.tsx`
calls `createPortal(` with `document.body`. `tests/orchestration/test_run_report.py` gains: a job
whose second task's plan inputs carry `origin` `human_injected` renders that task's line ending,
before any evidence link, in ` — added by you while the job ran`, its first task's line
unchanged; a task without plan inputs and one with a non-string origin render no clause; and the
origin survives the apply-state rebuild. `tests/orchestration/test_task_injection_runner.py`
gains: after a run that folds and runs an injected task, `render_report(job)` holds the clause
on that task's line exactly once.

BUNDLE — the commits are C1 to C6, in this order.
C1 — copy this block and the payloads: `.agent/authored/f028-r8-block.md`,
  `.agent/authored/f028-r8-records.diff`, `.agent/authored/f028-r8-plan.md`, by
  `shutil.copyfile`. Subject: `F028 R8 C1: copy round 8 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 87; STOP rather than commit at 500 or more.
C2 — THE FINDING FIRST: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F028 R8 C2: book round 7's FAIL, register R-1079, record D8 and two prose slips`
  Expected by `git show --numstat`: 28/0 decisions.md, 4/0 live_review.md, 8/6 plan.md, 2/0 prose_slips.md.
C3 — S1 with its contract test. Subject: `F028 R8 C3: repair R-1079, render the Add Task sheet through a portal`
C4 — S2 with its two test files. Subject: `F028 R8 C4: name an injected task's origin on its report line`
C5 — THE TOOL: `.agent/authored/f028-r8-mutations.py`. Subject: `F028 R8 C5: add the round 8 mutation tool`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F028 R8 C6: rewrite handoff for round 8`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`; a commit that would reach it
   is split into parts with their own subjects, each leaving the selection of G4 green, and you
   say so.
3. The round's whole tracked path set is: the `.agent/authored/f028-r8-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `apps/ui/src/components/panels/AddTaskSheet.tsx`, `packages/orchestration/run_report.py`,
   `tests/ui_contracts/test_inject_controls_contract.py`, `tests/orchestration/test_run_report.py`,
   `tests/orchestration/test_task_injection_runner.py`, and `.agent/handoff.md`. Report the list
   `git diff --name-only 41f591a3` measures after C6. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test THIS round
   wrote that is wrong may be corrected before C6, and the correction is declared. Any other
   existing test that goes red is never edited; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F028 one full-suite run, at its closure.
8. No `except Exception` in any production line this round writes.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table; then compare each `.agent/authored/f028-r8-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f028-r8/block.md`), read back with
 `git show <C1>:<path>`. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 334238 | 8d78f6edf35e680ddfe2aade3e569b784cc42d56ea3bab411d174cd095d27f14 |
 | .agent/decisions.md | 2274641 | e313b649687b810e7db109ee24d563f7a78955364655d4a98970eb837a6cb525 |
 | .agent/prose_slips.md | 373641 | 8c710f22fe34e758e2b193ffdc190a03e7936d340dbb147c9e63ea868c3b8862 |
 | .agent/plan.md | 1011 | f615125f62041ca38504b5778836abca6f24ec7ce82e20974afbae86e3fc44d8 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at
 `41f591a3` and at C2 (the reviewer read `[]` and `['R-1079']`), and `git diff --name-only <C1>
 <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/run_report.py
 tests/ui_contracts/test_inject_controls_contract.py tests/orchestration/test_run_report.py
 tests/orchestration/test_task_injection_runner.py` at C5, with its real exit code. Then quote
 from the diff the portal's return statement and `_task_lines` whole.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_run_report.py tests/orchestration/test_run_report_hook.py tests/orchestration/test_job_digest.py tests/cli/test_job_report.py tests/orchestration/test_task_injection_runner.py tests/ui_contracts/test_inject_controls_contract.py tests/ui_server/test_dashboard_task_origin.py tests/ui_server/test_dashboard_contract.py tests/ui_contracts/test_ux_quality.py tests/ui_contracts/test_responsive.py tests/ui_contracts/test_raw_colour_ratchet.py tests/ui_contracts/test_design_drift.py tests/ui_contracts/test_ui_lint.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_task_injection.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -14; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `41f591a3` and read
 `1198 passed, 9 skipped` at real exit code 0. Report every `SKIPPED` line and account for any
 difference from 1198 beyond the nodes the round adds. Then
 `python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0 — the
 reviewer read that at C2 in its simulation tree, round 7's FAIL booked.

G5 THE RED PROOFS — your tool `.agent/authored/f028-r8-mutations.py` takes a worktree path and,
 for each mutation below, edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/ui_contracts/test_inject_controls_contract.py tests/orchestration/test_run_report.py
 tests/orchestration/test_task_injection_runner.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: label, exit
 code, failed count, failing node ids. An unmutated control runs first and last; it ends with
 `restored byte-identical: True` per file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 the sheet returns its section directly, without the portal (AddTaskSheet.tsx);
  m2 `_task_lines` appends the clause to every task (run_report.py);
  m3 `collect_report_sources` never fills `origin` (run_report.py);
  m4 the apply-state rebuild drops `origin` (run_report.py).
 Run it: `git worktree add --detach .remedy-wt/f028-r8-mut <C5>`, then
 `python3 -B .agent/authored/f028-r8-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f028-r8-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, and you then add the test that catches it before C6 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f028-r8-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, empty; `git log --oneline -n 7`, showing
 C6 back to C1 and `41f591a3` in order (more lines if constraint 2 split a commit);
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C5), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit, per gate and for R-1079), the deviations, and the next expected action. Name the
commit that lands R-1079's repair; write no `Done:` or `Landed:` line into the ledger. Your
Session section reads SESSION 1 of feature F028, round 8, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 8 with the reviewer's headless render of the sheet measuring its box, then the end-to-end
proof and the closure sequence. State the open-findings count, 1 (R-1079, its repair awaiting
review), and the operator-questions count, 0.
