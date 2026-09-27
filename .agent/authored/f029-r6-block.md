STEP F029 R6 — BOOK R5, RECORD D6 AND ITS ASSUMPTION-LOG ROW, AND LAND T003's CONTROL HALF: the Rerun control in the run detail, its send module and sentences, and the report's attempt clause

GOAL
Round 5 passed. Book its gate entry, record DECISION F029 D6 with its assumption-log row, and make
the run detail's Rerun button real: it sends `job.rerun-subtree` for the run's task, shows a cost
the preview would ask about as one sentence with "Rerun anyway" and "Cancel", takes an optional
model, and answers a prepared rerun with the command that runs it. The final report names a task's
attempt and its override. The end-to-end proof is round 7.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
code and tests against S1 to S5. Read DECISION F029 D6 (it arrives with C2) and, whole:
`apps/ui/src/api/injectSend.ts` with its test, `apps/ui/src/api/vetoSend.ts`,
`apps/ui/src/api/pauseSend.ts`, `apps/ui/src/api/decisionAnswer.ts`,
`apps/ui/src/api/decisionSend.ts`, `apps/ui/src/components/graph/RunDetailPopover.tsx` with its
style sheet, `tests/ui_contracts/test_run_detail_wiring.py`,
`tests/ui_contracts/test_attempt_fan_contract.py`, and in
`packages/orchestration/run_report.py` the `TaskOutcome` model, `_origin_clause`, `_task_lines` and
`_task_origin` with the builder that calls it, and the origin tests of
`tests/orchestration/test_run_report.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f029-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f029-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f029-r6-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f029-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f029-r6-worker/`    YOURS for logs, scripts and the G5 scratch config; create it
                                  if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx from the shell; vitest, tsc and eslint run through the pytest nodes of
G4, and G5's tool spawns the primary checkout's own vitest binary as a subprocess.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f029-subtree-rerun`, and `git log --oneline -1` must read `4295d0dc`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f029-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f029-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 68 | 14189 | 442bd4114c85bf67e26e5eae73b07b93e1fd6cca6580a3682c9e03550b39d517 |
| plan.md | 33 | 1171 | c217f215fe46dc18f1bd3526f3c48b37aca41be563bbba139c701363bc3e5652 |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer generated
it with `git diff HEAD` from a tree at `4295d0dc`. It appends round 5's gate entry to
`.agent/live_review.md`, DECISION F029 D6 to `.agent/decisions.md`, and one row naming DECISION
F029 D6 to `docs/ui/design_reference/assumption_log.md`.

THE SPECIFICATION
S1 THE SEND, a NEW file `apps/ui/src/api/rerunSend.ts`, composed exactly as `injectSend.ts` is
   and reusing its composed helpers rather than retyping them: `JOB_RERUN_SUBTREE_COMMAND_ID =
   "job.rerun-subtree"` (the door's own spelling), `RERUN_DEADLINE_MS = 60000`,
   `buildRerunSubtreeRequest(target, taskId, { model, confirmCost })` whose `args` hold `task_id`
   always, `model` only when `model.trim()` is not empty (the trimmed value), and `confirm_cost:
   true` only when `confirmCost` is true; a submit reading the body as `submitInjectRequest` does,
   with `accepted`, `refused` and `unreachable`; `rerunAnswerOf(result)` answering the 200 body
   or null; `describeRerunResult(result)` whose refusal sentence is the 409 text after its first
   `": "`, verbatim, and whose `unreachable` sentence is `pauseSend.ts`'s; and
   `sendRerunSubtree(deps, taskId, { model, confirmCost })` as `sendInjectDraft` is shaped.
S2 THE WORDS, a NEW file `apps/ui/src/api/rerunView.ts`: `rerunAnswerView(answer)` answers null
   unless `answer.outcome` is `needs_confirmation` or `prepared`, else `{ kind, sentence,
   runCommand }`, reading defensively. For `needs_confirmation` with `n` = the subtree's length
   minus one and `root` its first id: an estimate whose `band_usd_high` is a number reads
   `` `Rerunning task ${root} and ${n} task${n === 1 ? "" : "s"} after it is estimated at
   $${low.toFixed(2)} to $${high.toFixed(2)}, above the $${threshold.toFixed(2)} you asked to
   confirm.` ``, and otherwise `` `The cost of rerunning task ${root} and ${n} task${n === 1 ? "" :
   "s"} after it cannot be estimated in advance.` ``; `runCommand` is "". For `prepared`:
   `` `Task ${root} and ${n} task${n === 1 ? "" : "s"} after it were reset to run again.` `` with
   `root` the answer's `root_task_id` and `n` its subtree's length minus one, and `runCommand` the
   answer's `run_command`.
S3 THE CONTROL, in `RunDetailPopover.tsx`: the Rerun button is enabled whenever `token` is not
   empty, else disabled with the title and the visible reason "Rerunning needs the live page's
   server token.", `aria-describedby` naming that reason; before the actions, a labelled
   `<input type="text">` "Model for the rerun (optional)" with `maxLength={128}`; a click sends
   `sendRerunSubtree` for the run's task (the id the popover already derives) with the field's
   value and no `confirmCost`; a `needs_confirmation` view shows its sentence with the buttons
   "Rerun anyway" (sends again with `confirmCost: true`) and "Cancel" (clears the view); a
   `prepared` view shows its sentence and then `` `Run it with: ${runCommand}` ``; a refusal or an
   unreachable server shows `describeRerunResult`'s sentence. Every sentence goes into ONE
   `<p aria-live="polite">`; the buttons are disabled while a send is in flight. The detail stays
   a panel: no `role="dialog"`. `RERUN_NOT_YET` and the disabled button's reason line are DELETED.
   New style rules, if any, use existing `--remedy-*` tokens and the existing `.action` rules.
S4 THE REPORT, in `run_report.py`: `TaskOutcome` gains `attempt: int = 1` and `model_override:
   str = ""`, filled where `origin` is filled from the task entry's `attempt` and
   `model_override`, read defensively as `_task_origin` reads `origin`; `_attempt_clause(task)`
   answers "" for an attempt below 2, else `` f" — attempt {task.attempt}" `` followed by
   `` f", run on {task.model_override}" `` when the override is not empty; `_task_lines` appends it
   after `_origin_clause`. A job with no rerun renders byte-identical.
S5 THE PINS. In `tests/ui_contracts/test_run_detail_wiring.py`,
   `test_rerun_is_disabled_with_its_reason_visible_and_the_detail_is_not_a_dialog` — the ONLY edit
   this round makes to a test it did not write — is renamed
   `test_rerun_sends_the_subtree_rerun_and_the_detail_is_not_a_dialog` and asserts
   `sendRerunSubtree(` and `rerunAnswerView(` in the source, `RERUN_NOT_YET` absent, `role="dialog"`
   absent, `aria-live="polite"` present, and keeps its `.action:disabled { opacity: 0.45;` line;
   its comment names DECISION F029 D6. `tests/ui_contracts/test_attempt_fan_contract.py` gains:
   `RunDetailPopover.tsx` holds no `fetch(`, and exactly one line of the assumption log names
   DECISION F029 D6.

THE TESTS — vitest, beside their modules: `rerunSend.test.ts` for the request's `args` in every
combination of model and confirmation (a blank model sends none), a 200, a 409 whose sentence is the
detail after the prefix, and an unreachable server; `rerunView.test.ts` for both estimate sentences
with one and with three tasks, the prepared sentence and its command, and null for any other
outcome, a null body and a body with every field missing. Python, appended to
`tests/orchestration/test_run_report.py`: the clause for attempt 2 without and with an override,
none for attempt 1, and a report of a job with no rerun equal to the one rendered without the new
fields.

BUNDLE — the commits are C1 to C7, in this order.
C1 — `.agent/authored/f029-r6-block.md` := this block, `.agent/authored/f029-r6-booking.diff` and
  `.agent/authored/f029-r6-plan.md` := the payloads, by `shutil.copyfile`.
  Subject: `F029 R6 C1: copy round 6 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 101. Report the number you measure.
C2 — `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F029 R6 C2: book round 5, record D6 and its assumption-log row`
  Expected by `git show --numstat`: 41/0 decisions.md, 2/0 live_review.md, 9/11 plan.md,
  1/0 assumption_log.md.
C3 — S1 and S2 with their tests. Subject: `F029 R6 C3: send a subtree rerun from the browser and read its answer as sentences`
C4 — S3 and S5. Subject: `F029 R6 C4: make the run detail's Rerun button send the rerun behind its cost`
C5 — S4 with its tests. Subject: `F029 R6 C5: the final report names a task's attempt and its override`
C6 — `.agent/authored/f029-r6-mutations.py` (G5). Subject: `F029 R6 C6: add the round 6 mutation tool`
C7 — `.agent/handoff.md` per `docs/agents/handback_template.md`. Subject: `F029 R6 C7: rewrite handoff for round 6`
  Then `git push origin feature/f029-subtree-rerun` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C3, C4 and C5 before
   you commit them; a commit that would reach 500 is split into parts with their own subjects,
   each part leaving G4's selection green, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f029-r6-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `docs/ui/design_reference/assumption_log.md`, the files S1 to S5 and THE TESTS name, and
   `.agent/handoff.md`. Report `git diff --name-only 4295d0dc` after C7. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test THIS round wrote that is wrong may be corrected
   before C7, and the correction is declared. An existing test goes red and is edited only where
   S5 orders it; any other is reported, and you stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F029 one full-suite run, at its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table; then
 each `.agent/authored/f029-r6-*` copy read back with `git show <C1>:<path>` compared byte for byte
 with its source (the block copy against `.remedy-wt/f029-r6/block.md`). One reading per copy.
G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2302631 | 6437bdd35357ecbb20b50dfa3abee6843dae8ad113e949271f097876a26ea8d3 |
 | .agent/live_review.md | 326313 | efc0988d0611e6fade0a03ad8e0d62ccfcc3d2368169df342c4884e47b242209 |
 | .agent/plan.md | 1171 | c217f215fe46dc18f1bd3526f3c48b37aca41be563bbba139c701363bc3e5652 |
 | docs/ui/design_reference/assumption_log.md | 20869 | 6f2a0c0795b29b31ab692c9e21ded4689eb83669b435b58a2fae60a0b110c031 |
 Also `open_finding_ids` over the ledger's text at `4295d0dc` and at C2 (the reviewer read `[]` at
 both), and `git diff --name-only <C1> <C2>`, which must name exactly the paths of the table.
G3 THE CODE — `python3 -m ruff check packages/orchestration/run_report.py
 tests/orchestration/test_run_report.py tests/ui_contracts/test_run_detail_wiring.py
 tests/ui_contracts/test_attempt_fan_contract.py` at C6 with its real exit code; then quote from
 the diff `buildRerunSubtreeRequest`, `rerunAnswerView`, the Rerun control's JSX, and
 `_attempt_clause`.
G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/orchestration/test_run_report.py tests/ui_server/test_rerun_subtree_door.py tests/ui_server/test_dashboard_task_attempts.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -16; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `4295d0dc` and read
 `1690 passed, 11 skipped` at real exit code 0; the eleven skips are F252 quarantines. Report
 every `SKIPPED` line and account for any difference from 1690 beyond the Python nodes the round
 adds. Then `python3 -m apps.cli.main integrity check --json`: every check's status and
 `fail_count`.
G5 THE RED PROOFS — your tool `.agent/authored/f029-r6-mutations.py` takes a worktree path. For a
 TypeScript mutation it runs the PRIMARY checkout's `apps/ui/node_modules/.bin/vitest run --config
 <scratch>` with the primary's `apps/ui` as its working directory, `<scratch>` a PLAIN-OBJECT
 config it writes under `.remedy-wt/f029-r6-worker/` with `root` the primary's `apps/ui`,
 `cacheDir` under `.remedy-wt/`, `test.environment` `"node"` and `test.include` the worktree's
 `rerunSend.test.ts` and `rerunView.test.ts` by absolute path; for a Python mutation it runs
 `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_run_report.py
 tests/ui_contracts/test_run_detail_wiring.py tests/ui_contracts/test_attempt_fan_contract.py`
 from the worktree's root after purging its `__pycache__` directories. Each mutation edits the
 named file INSIDE the worktree (its FROM text asserted to occur exactly once) and is restored.
 Unmutated controls of both kinds run first and last. It prints one line per mutation (label,
 exit code, failed count, the failing tests' names) and ends with `restored byte-identical: True`
 per file, the PRIMARY checkout's `git status --porcelain` (which must be empty) and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 the request always sends `confirm_cost: true` (rerunSend.ts);
  m2 the request never sends `model` (rerunSend.ts);
  m3 a refusal's sentence keeps the code's prefix (rerunSend.ts);
  m4 an unavailable estimate reads as the priced sentence (rerunView.ts);
  m5 the prepared view's `runCommand` is "" (rerunView.ts);
  m6 `_attempt_clause` answers a clause for attempt 1 (run_report.py);
  m7 `_attempt_clause` leaves out the override (run_report.py);
  m8 `RunDetailPopover.tsx` keeps a `role="dialog"` on its panel (RunDetailPopover.tsx).
 Run it: `git worktree add --detach .remedy-wt/f029-r6-mut <C6>`, then
 `python3 -B .agent/authored/f029-r6-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f029-r6-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, then you add the test that catches it before C7 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f029-r6-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.
G6 TREE AND PUSH — after C7: `git status --porcelain`, empty; `git log --oneline -n 9`;
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected, every gate's real output and exit code, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate and
per S-item), the deviations, and the next expected action. Your Session section reads SESSION 1
of feature F029, round 6, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6 with the reviewer's headless render of the Rerun control, then T003's end-to-end proof —
run, rerun a middle task with an override, the subtree runs again, both attempts in the evidence
and the report — then the closure sequence. State the open-findings count, 0, and the
operator-questions count, 0.
