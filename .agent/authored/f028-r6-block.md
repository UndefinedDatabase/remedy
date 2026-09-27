STEP F028 R6 — BOOK ROUND 5 AND RESOLVE R-1078, RECORD D6, AND LAND THE TASK ITEM'S `origin`, THE BROWSER'S SEND MODULE FOR THE THREE INJECTION COMMANDS, AND THE "Added by you" PILL IN THE TASK LIST AND THE DETAIL POPOVER

GOAL
Round 5 passed. Book its gate entry and R-1078's resolution, record DECISION F028 D6 and its
assumption-log row. Then carry an injected task's provenance to the browser: every dashboard task
item names its `origin`, a pure view module turns `human_injected` into the words "Added by you",
the task-list row and the detail popover draw them as a pill, and a send module builds, submits
and describes the door's three injection commands for the sheet round 7 builds on it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests against S1 to S6. Read DECISION F028 D6 (it arrives with C2),
`docs/ui/design_reference/tokens_rules.md`, and whole: `apps/ui/src/api/vetoSend.ts` with its
test, `apps/ui/src/components/panels/TaskChecklistCard.tsx`, the status row of
`apps/ui/src/components/detail/DetailPopover.tsx`, and `tests/ui_contracts/test_veto_controls_contract.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r1-sim/` to `.remedy-wt/f028-r6-sim/`  The reviewer's simulation trees.
  `.remedy-wt/f028-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f028-r6-worker/`    YOURS for logs, scripts and the G5 scratch config; create it
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
   `feature/f028-task-injection`, and `git log --oneline -1` must read `d82a407c`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 30 | 1072 | 51d9e9f00ee359684f41633f7d4662ef9488461a60573c7176d5419365252ff2 |
| records.diff | 64 | 13623 | 7c26043f0e7215bf8a39e811d67caaf4203fe035e86b09d1365f8d6a7760a60b |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; it appends
round 5's gate entry and R-1078's `Done:` paragraph to `.agent/live_review.md`, DECISION F028 D6
to `.agent/decisions.md`, and one row naming DECISION F028 D6 to
`docs/ui/design_reference/assumption_log.md`.

THE SPECIFICATION
S1 THE DATA. In `packages/orchestration/ui_server.py`, each dashboard task item (the dict built per
   task before it is placed under `"tasks"`) gains, as its LAST key, `"origin"`: the entry's
   `inputs["plan"]["origin"]` when `inputs["plan"]` is a dict and that value is a non-empty `str`,
   else `""`. In `apps/ui/src/api/types.ts`, `RemedyTaskItem` gains `origin?: string`, and
   `normalizeDashboardPayload` in `apps/ui/src/api/remedyApi.ts` sets it only when the raw value
   is a non-empty string.
S2 THE VIEW, a NEW FILE at `apps/ui/src/api/injectView.ts`: `INJECTED_TASK_ORIGIN =
   "human_injected"`, `ORIGIN_CHIP_TEXT = "Added by you"`, `ORIGIN_CHIP_TITLE = "You added this
   task while the job was running."`, and `taskOriginChip(task: { origin?: string } | null |
   undefined): string | null`, answering `ORIGIN_CHIP_TEXT` exactly when `task?.origin` equals
   `INJECTED_TASK_ORIGIN`, else null.
S3 THE SEND MODULE, a NEW FILE at `apps/ui/src/api/injectSend.ts`, built from `vetoSend.ts`'s
   imports and shapes: `JOB_INJECT_COMMAND_ID = "job.inject"`,
   `JOB_INJECT_CONFIRM_COMMAND_ID = "job.inject-confirm"`,
   `JOB_INJECT_ANSWER_COMMAND_ID = "job.inject-answer"`, `INJECT_SHORTFALL_OPTIONS =
   ["extend_budget", "shrink_task", "drop"] as const`, `INJECT_DRAFT_DEADLINE_MS = 120000` (the
   draft waits on the planner's call) and `INJECT_STEP_DEADLINE_MS = 20000`.
   `buildInjectDraftRequest(target, text, after, clientNonce)` is null for a text blank after
   trimming or an unusable nonce, and sends `args: {text}` plus `after` only when it is a
   non-empty string; `buildInjectConfirmRequest(target, confirmToken, clientNonce)` is null for an
   empty token and sends `{confirm_token}`; `buildInjectAnswerRequest(target, draftId, option,
   clientNonce)` is null for an empty draft id or an option outside `INJECT_SHORTFALL_OPTIONS` and
   sends `{draft_id, option}`; each carries the headers and path `buildVetoTaskRequest` carries.
   `submitInjectRequest(request, send?)` is `submitVetoTaskRequest`'s contract.
   `describeInjectResult(result) -> DecisionOutcomeMessage` words a 200 by its `outcome`
   (`drafted`, `shortfall`, `confirmed`, `dropped`; anything else as unconfirmed), a 409 through a
   table of one complete plain sentence per refusal code the door answers (`job_terminal`,
   `no_task_plan`, `plan_full`, `planner_unavailable`, `budget_unreadable`, `draft_unparseable`,
   `draft_invalid`, `unknown_task`, `draft_unknown`, `draft_expired`, `draft_needs_decision`,
   `already_confirmed`, `draft_stale`, `draft_not_in_shortfall`, `already_answered`,
   `cannot_shrink`) and an unknown code verbatim, a 400 on field `text` through the door's own
   detail, and everything else as `describePauseSendResult` words it. `injectAnswerOf(result)`
   answers the 200 body as an object, else null. `sendInjectDraft(target, text, after, deps)`,
   `sendInjectConfirm(target, confirmToken, deps)` and `sendInjectAnswer(target, draftId, option,
   deps)` each answer `{message, answer}`, never reach the network when the request is null, and
   race the send against their deadline, as `sendVetoTask` does.
S4 THE PILLS. `TaskChecklistCard.tsx` draws, inside each row after the label, `{chip && <span
   className={styles.originChip} title={ORIGIN_CHIP_TITLE}>{chip}</span>}` with
   `chip = taskOriginChip(task)`; `RightLivePanel.module.css` gains `.originChip` with
   `.decisionChip`'s declarations plus `margin-left: 6px; flex: none;`. `DetailPopover.tsx`'s
   status row draws the same pill before the version chip, and `DetailPopover.module.css` gains
   `.originChip` with `.versionChip`'s declarations, its `margin-left: auto` replaced by
   `margin-left: 6px`. No raw colour, no new token, no `fetch(`.
S5 THE TESTS. NEW FILES at `apps/ui/src/api/injectView.test.ts` and
   `apps/ui/src/api/injectSend.test.ts`, covering S2 and S3 as `vetoSend.test.ts` covers its
   module: the three exact requests, each null case, the token never in the path, every refusal
   code's sentence, the unknown code, the 400 on `text`, the pause fallback, each 200 outcome,
   `injectAnswerOf`, and each send function's network, no-network and deadline paths. NEW FILE at
   `tests/ui_server/test_dashboard_task_origin.py`: an injected task's item names
   `human_injected`, a planned task's and a task without plan inputs name `""`. NEW FILE at
   `tests/ui_contracts/test_inject_controls_contract.py`: the three ids of `injectSend.ts` equal
   the door's three constants in `ui_server.py`; `fetch(` absent from `TaskChecklistCard.tsx`,
   `DetailPopover.tsx` and `injectView.ts` after `strip_ts_comments`; `taskOriginChip(` present in
   both components; and exactly one line of the assumption log names DECISION F028 D6.
S6 NOTHING ELSE: no Add Task row, no sheet, no canvas chip this round; the "+ Propose task" button
   stays as it is, because `tests/ui_contracts/test_responsive.py` pins it and round 7 replaces it.

BUNDLE — the commits are C1 to C7, in this order.
C1 — copy this block and the payloads: `.agent/authored/f028-r6-block.md`,
  `.agent/authored/f028-r6-records.diff`, `.agent/authored/f028-r6-plan.md`, by
  `shutil.copyfile`. Subject: `F028 R6 C1: copy round 6 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 94; STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F028 R6 C2: book round 5, resolve R-1078, record D6 and its assumption-log row`
  Expected by `git show --numstat`: 35/0 decisions.md, 4/0 live_review.md, 7/7 plan.md, 1/0 assumption_log.md.
C3 — S1: `ui_server.py`, `types.ts`, `remedyApi.ts`, `tests/ui_server/test_dashboard_task_origin.py`.
  Subject: `F028 R6 C3: carry each task's origin on the dashboard`
C4 — S2, S4 and their contract test: `injectView.ts`, `injectView.test.ts`, the two components,
  the two CSS modules, `tests/ui_contracts/test_inject_controls_contract.py`.
  Subject: `F028 R6 C4: show Added by you on an injected task in the list and the popover`
C5 — S3: `injectSend.ts`, `injectSend.test.ts`.
  Subject: `F028 R6 C5: add the browser's send module for the three injection commands`
C6 — THE TOOL: `.agent/authored/f028-r6-mutations.py`. Subject: `F028 R6 C6: add the round 6 mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F028 R6 C7: rewrite handoff for round 6`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C4 and C5 before you
   commit them; a commit that would reach 500 is split into parts with their own subjects, each
   part leaving the selection of G4 green, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f028-r6-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `docs/ui/design_reference/assumption_log.md`, the paths C3, C4 and C5 name, and
   `.agent/handoff.md`. Report the list `git diff --name-only d82a407c` measures after C7. Touch
   nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test THIS round
   wrote that is wrong may be corrected before C7, and the correction is declared. Any other
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
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table; then compare each `.agent/authored/f028-r6-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f028-r6/block.md`), read back with
 `git show <C1>:<path>`. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 327502 | 5b6ca36fb4bc2e0f57c50f3b32b47dbd5c46a516682cb23ff65bbd01679217dd |
 | .agent/decisions.md | 2269306 | 1ef9f83ef76cdd752f6817397249198e701ff1b5c497abea939fcc41bde5cc0b |
 | docs/ui/design_reference/assumption_log.md | 17173 | 4ed2e280fc62bcb523bac936bb34482497a6759d098ea36a788bcf90d2e40e81 |
 | .agent/plan.md | 1072 | 51d9e9f00ee359684f41633f7d4662ef9488461a60573c7176d5419365252ff2 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at
 `d82a407c` and at C2 (the reviewer read `['R-1078']` and `[]`), and `git diff --name-only <C1>
 <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/ui_server.py
 tests/ui_server/test_dashboard_task_origin.py tests/ui_contracts/test_inject_controls_contract.py`
 at C6, with its real exit code. Then quote from the diff the new task-item key, `taskOriginChip`,
 both pill mounts, both `.originChip` rules, and `describeInjectResult` whole.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_dashboard_task_origin.py tests/ui_contracts/test_inject_controls_contract.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py tests/ui_server/test_dashboard_task_specs.py tests/ui_contracts/test_ux_quality.py tests/ui_contracts/test_responsive.py tests/ui_contracts/test_raw_colour_ratchet.py tests/ui_contracts/test_design_drift.py tests/ui_contracts/test_ui_lint.py tests/ui_contracts/test_pause_controls_contract.py tests/ui_contracts/test_task_version_contract.py tests/ui_contracts/test_veto_controls_contract.py tests/ui_contracts/test_apply_state_partial.py tests/ui_contracts/test_decision_answer_wiring.py tests/ui_contracts/test_humanize_catalog.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_task_injection.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -14; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the two new Python test files, serially, in the primary
 checkout at `d82a407c`, and read `1197 passed, 9 skipped` at real exit code 0. Report every
 `SKIPPED` line, the node counts of the new files by `--collect-only -q`, the vitest test count
 the vitest node's own output prints at `d82a407c` and at C6 if you can read it, and account for
 any difference from 1197 beyond the nodes the round adds. Then
 `python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f028-r6-mutations.py` takes a worktree path. For
 the Python mutation it runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/ui_server/test_dashboard_task_origin.py` from the worktree's root after purging its
 `__pycache__`. For each TypeScript mutation it runs the PRIMARY checkout's
 `apps/ui/node_modules/.bin/vitest run --config <scratch>` with the primary's `apps/ui` as its
 working directory, where `<scratch>` is a config the tool writes under
 `.remedy-wt/f028-r6-worker/` exporting a PLAIN OBJECT (no `defineConfig` import) with `root` the
 primary's `apps/ui`, `cacheDir` a directory under `.remedy-wt/`, `test.environment` `"node"` and
 `test.include` the worktree's two new `.test.ts` files by absolute path. Every mutation edits the
 named file INSIDE the worktree (asserting its FROM text occurs exactly once) and restores its
 bytes; an unmutated control of each runner runs first and last. It prints one line per mutation:
 label, exit code, failed count; and ends with `restored byte-identical: True` per file,
 `git status --porcelain` of the PRIMARY checkout (which must be empty), and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 the task item's `origin` is always `""` (ui_server.py);
  m2 `taskOriginChip` answers the chip for any non-empty origin (injectView.ts);
  m3 `buildInjectDraftRequest` accepts a blank text (injectSend.ts);
  m4 `buildInjectAnswerRequest` accepts an option outside the three (injectSend.ts);
  m5 `INJECT_DRAFT_DEADLINE_MS` is 20000 (injectSend.ts);
  m6 a 409 `draft_expired` is worded by the unknown-code fallback (injectSend.ts);
  m7 `buildInjectConfirmRequest` names `job.inject` as its command (injectSend.ts).
 Run it: `git worktree add --detach .remedy-wt/f028-r6-mut <C6>`, then
 `python3 -B .agent/authored/f028-r6-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f028-r6-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, and you then add the test that catches it before C7 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f028-r6-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, empty; `git log --oneline -n 8`, showing
 C7 back to C1 and `d82a407c` in order (more lines if constraint 2 split a commit);
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Your Session section
reads SESSION 1 of feature F028, round 6, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6, then the Add Task row and its sheet, the canvas chip and the render proof. State the
open-findings count, 0, and the operator-questions count, 0.
