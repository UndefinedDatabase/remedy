STEP F027 R8 — T003 SECOND HALF: the veto reaches the page's surfaces — the unreachable set fades on the canvas, hover text carries the reason, the detail popover shows the veto and links across it, and a "Veto task" form sends it — and R-1068's resolution

GOAL
Book round 7's verdict, resolve R-1068, add one prose-slip line, record DECISION F027 D8, and land
it: the live canvas fades the unreachable set by the vetoed treatment's own downstream alpha, a
vetoed or unreachable node's hover text names the reason or the vetoing task as plain text, the
detail popover shows a Veto or Unreachable section with buttons that open the task on the other
side, and a "Veto task" form sends `job.veto-task` through a new `vetoSend.ts` — with tests, two
assumption-log rows, and a mutation tool proving the tests bite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records travel as
payloads. Read DECISION F027 D8 in `records.diff` before you write code: it is the design, and
`docs/ui/design_reference/` binds every visual and wording choice S1 to S6 leave open.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f027-r8-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f027-r8/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f027-r8-dry/`, `.remedy-wt/f027-r8-drafts/`, `.remedy-wt/f027-review/` and every
                                  older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r8-worker/`    YOURS for logs, scripts and scratch configs; create it if
                                  absent. All are gitignored. You may copy round 7's
                                  `.remedy-wt/f027-r7-worker/` helpers into it.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx; the one Node binary you may run is
`/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest`, and only as G5 orders it. The
TypeScript compiler, the lint and the whole vitest suite run for you inside G4's own tests.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f027-task-veto`, and `git log --oneline -1` must read `b9b16909`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f027-r8/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f027-r8-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 30 | 1097 | ae20aa227eb0d0c616b85d8d52d28af63c01ed7edfca37dd58e58e03b05d2f60 |
| records.diff | 83 | 12242 | c8f465100b12ecff26840d5eebf7e0b00238ddf3a5ea0379644238c783c0bb82 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `b9b16909`. It appends to `.agent/live_review.md`
round 7's gate entry and R-1068's `Done:` line, one line to `.agent/prose_slips.md`, and to
`.agent/decisions.md` DECISION F027 D8.

THE SPECIFICATION
S1 THE VIEW, a NEW pure module `apps/ui/src/api/vetoView.ts` (no `fetch(`, no DOM, no clock):
   `taskVetoEntry(vetoes, taskId)` → the `RemedyVetoEntry` for that task or `null`;
   `vetoingEntriesOf(vetoes, taskId)` → the entries whose `unreachableTaskIds` name it, in section
   order; `taskTitleOf(dashboard, taskId)` → that task's `label` in `dashboard.tasks`, else the id;
   `taskVetoAction(dashboard, taskId)` → `{ taskId }` only when `dashboard.vetoes.error` is `""`
   and `vetoableTaskIds` names the task, else `null`; `vetoHoverText(dashboard, taskId)` →
   `Vetoed: <reason>` (reason verbatim) for a vetoed task, `Unreachable due to veto of <title>`
   (titles joined by `, `, section order) for an unreachable one, a vetoed task's text winning,
   else `null`; `vetoAnswerSentence(answer)` → `""` "A replan proposal is waiting in the decision
   inbox.", `replan_follow_up` "Answered: replan the remaining work as a new job.",
   `accept_reduced_scope` "Answered: accept the smaller scope.", any other value "Answered.".
S2 THE GRAPH'S HELPERS, in `apps/ui/src/components/graph/brainView.ts`: `vetoFadedNodeIds(vetoes)`
   → a `ReadonlySet` of `task:<id>` for every id in `vetoes.unreachableTaskIds`; and
   `vetoHoverTexts(dashboard)` → a `ReadonlyMap` from `task:<id>` to `vetoHoverText`'s text for
   every task of `dashboard.tasks` that has one.
S3 THE CANVAS: `BrainGraphStage.tsx` memoizes both over `dashboard` and passes them to
   `ForceBrainGraph` as new props `vetoFaded` and `vetoHover`. In `ForceBrainGraph.tsx`: a module
   constant `VETO_DOWNSTREAM_ALPHA = NODE_STATE_TREATMENTS.vetoed.downstreamAlpha`; in
   `handleNodeCanvasObject` the line `const dim = emphasis.dimmed.has(n.id) ? ZOOM_DIM_ALPHA : 1;`
   stays byte for byte, a line `const vetoFade = vetoFaded.has(n.id) ? VETO_DOWNSTREAM_ALPHA : 1;`
   follows it, the paint's alpha becomes `birth.alpha * dim * vetoFade`, and the label's
   `ctx.globalAlpha = dim;` becomes `ctx.globalAlpha = dim * vetoFade;`; in
   `handleLinkCanvasObject` the substring `(emphasis.dimmed.has(target.id) ? ZOOM_DIM_ALPHA : 1)`
   stays and the alpha also multiplies by `(vetoFaded.has(target.id) ? VETO_DOWNSTREAM_ALPHA : 1)`;
   both callbacks' dependency lists gain the new props. `ForceGraph2D` gains
   `nodeLabel={handleNodeLabel}`, which returns `null` for a node `vetoHover` does not name and
   otherwise a `span` made with `document.createElement`, its class `styles.vetoTooltip` and its
   text set by `.textContent` — never `innerHTML`, anywhere in the file. The shim
   `apps/ui/src/types/react-force-graph-2d.d.ts` declares
   `nodeLabel?: (node: object) => string | HTMLElement | null;`. `ForceBrainGraph.module.css`
   styles `.vetoTooltip` and, through `:global(...)` under `.container`, the library's tooltip
   container `.float-tooltip-kap`, with existing `--remedy-*` tokens and NO colour literal (the
   raw-colour ratchet pins this file at 2).
S4 THE POPOVER, `apps/ui/src/components/detail/DetailPopover.tsx`: a new optional prop
   `onSelectTask?: (taskId: string) => void`, which `RemedyShell.tsx` passes as
   `(taskId) => onSelectNode(shellSelectionIdOf(dashboard.tasks, taskId))`. For a task
   `taskVetoEntry` names: the status row's label reads `Vetoed`, the Result paragraph reads
   `Vetoed. This task will not run.`, and a section `data-ui="veto-section"` headed `Veto` shows
   the reason verbatim as text, a line `Vetoed by <actor>` with ` · <formatTime(requestedAt)>`
   when there is a time, `Will not run because of this veto:` and one button per unreachable task
   (its title) or `No other task depended on it.`, then `vetoAnswerSentence(answer)`. For a task
   `vetoingEntriesOf` names: a section `data-ui="unreachable-section"` headed `Unreachable`
   reading `Unreachable due to veto of ` and one button per vetoing task (its title), joined by
   `, `. Every such button is `type="button"`, calls `onSelectTask(<that task's id>)`, and renders
   as plain text when no `onSelectTask` is passed. Both sections sit after the Blocker section.
   New classes in `DetailPopover.module.css` use existing tokens and NO colour literal (pinned at
   15); `DetailPopover.tsx` gains no colour literal (pinned at 4), and its lower-cased source
   still holds none of the words
   `tests/ui_contracts/test_ux_quality.py::TestTimelineDetailLayerComponents::test_detail_popover`
   forbids (`rank`, `importance`, `zone` among them).
S5 THE FORM, a NEW `apps/ui/src/components/detail/TaskVetoForm.tsx`, mounted in the popover after
   `TaskEditForm` as `{task && serverToken && vetoAction && (<TaskVetoForm key={task.id} ... />)}`
   with `const vetoAction = task ? taskVetoAction(dashboard, task.id) : null;`. Closed: a ghost
   button `Veto task`. Open: a form `aria-label="Veto task"` `data-ui="task-veto-form"` with one
   labelled single-line text input `Reason (required)`, `maxLength={500}`; the note `A veto cannot
   be undone. Tasks that depend on this one will not run, and a replan proposal goes to the
   decision inbox.`; a primary pill `Veto` disabled while the trimmed reason is empty or a send is
   under way; a ghost `Cancel` that closes it; and the result sentence in an `aria-live="polite"`
   paragraph. It reuses the popover's `ghostButton`, `savePill`, `editForm`, `editField`,
   `editNote`, `editActions` and `editResult` classes and calls `sendVetoTask`; no `fetch(` in it.
S6 THE SEND, a NEW `apps/ui/src/api/vetoSend.ts`, composed from `taskEditSend.ts`'s pattern:
   `JOB_VETO_TASK_COMMAND_ID = "job.veto-task"`; `buildVetoTaskRequest(target, taskId, reason,
   clientNonce)` → body `{ command, client_nonce, args: { task_id, reason } }` with the reason
   unchanged, `null` for an empty task id, a reason blank after trimming, or an unusable nonce;
   `submitVetoTaskRequest`; `describeVetoTaskResult(result)`: a 200 whose `outcome` is `vetoed`
   reads `Vetoed. No other task depended on it. A replan proposal is waiting in the decision
   inbox.` for an empty `unreachable` list, `Vetoed. 1 task that depends on it will not run. A
   replan proposal is waiting in the decision inbox.` for one, and `Vetoed. <n> tasks that depend
   on it will not run. A replan proposal is waiting in the decision inbox.` for more, tone `ok`;
   a 200 with any other outcome reads `The job answered, but did not confirm the veto.` tone
   `warn`; a 409 whose `error` begins `<code>: ` reads, tone `warn`, `Not vetoed: this job has
   already finished.` for `job_not_vetoable`, `Not vetoed: this task is already vetoed.` for
   `task_already_vetoed`, `Not vetoed: this task can no longer be vetoed.` for
   `task_not_vetoable`, `Not vetoed: this job has no such task.` for `unknown_task`, and `Not
   vetoed: <error>.` for any other string `error`; a 400 whose `field` is `reason` and whose
   `error` is a string reads `Not vetoed: <error>.` tone `warn`; everything else reads as
   `describePauseSendResult` does. `sendVetoTask(target, taskId, reason, deps = {})` races the
   send against a 20000 ms deadline and answers `This veto cannot be sent as it stands.` tone
   `warn` when nothing can be built.

THE TESTS — vitest files beside each new or changed `.ts`: `vetoView.test.ts` (each function, the
reason verbatim with `<b>` and `&` in it, both hover forms, the vetoed text winning, every answer
sentence, an error section refusing the action), `vetoSend.test.ts` (the body, each `null` case,
every sentence above, the deadline), and `brainView.test.ts` (both helpers). A NEW
`tests/ui_contracts/test_veto_controls_contract.py`, modelled on
`tests/ui_contracts/test_task_edit_controls_contract.py`: `vetoSend.ts`'s command id equals
`ui_server.JOB_VETO_TASK_COMMAND_ID`; no `fetch(` in `TaskVetoForm.tsx`, `vetoView.ts`,
`DetailPopover.tsx` or `ForceBrainGraph.tsx` with comments stripped; the popover computes
`taskVetoAction(dashboard, task.id)` and mounts `<TaskVetoForm` with `key={task.id}` inside the
`{task && serverToken && vetoAction` gate; `RemedyShell.tsx` passes `onSelectTask=`; the popover
calls `onSelectTask(`; `ForceBrainGraph.tsx` holds `nodeLabel={handleNodeLabel}`, `.textContent =`,
`NODE_STATE_TREATMENTS.vetoed.downstreamAlpha`, the `vetoFade` line of S3 and no `innerHTML`; and
`docs/ui/design_reference/assumption_log.md` names `DECISION F027 D8` in exactly two rows.

BUNDLE — the commits are C1 to C7, in this order.

C1 — copy this block and the payloads: `.agent/authored/f027-r8-block.md`,
  `.agent/authored/f027-r8-plan.md` and `.agent/authored/f027-r8-records.diff`, by
  `shutil.copyfile`. Subject: `F027 R8 C1: copy round 8 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 113. STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F027 R8 C2: book round 7, resolve R-1068, record D8`
  Expected by `git show --numstat`: 54/0 decisions.md, 4/0 live_review.md, 10/11 plan.md,
  1/0 prose_slips.md.
C3 — THE VIEW AND THE SEND: S1, S2's helpers and S6, with their vitest tests.
  Subject: `F027 R8 C3: the veto's view helpers and its send module`
C4 — THE CANVAS: S3, with the one pin update constraint 3 allows.
  Subject: `F027 R8 C4: fade the unreachable set and show the veto on hover`
C5 — THE POPOVER AND THE FORM: S4, S5, the contract test and the two assumption-log rows.
  Subject: `F027 R8 C5: the popover's veto sections, its task links and the veto form`
C6 — THE MUTATION TOOL: `.agent/authored/f027-r8-mutations.py`.
  Subject: `F027 R8 C6: the round's red-proof mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F027 R8 C7: rewrite handoff for round 8`. Then `git push`, and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f027-r8-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
   `.agent/handoff.md`, `apps/ui/src/api/vetoView.ts`, `apps/ui/src/api/vetoView.test.ts`,
   `apps/ui/src/api/vetoSend.ts`, `apps/ui/src/api/vetoSend.test.ts`,
   `apps/ui/src/components/graph/brainView.ts`, `apps/ui/src/components/graph/brainView.test.ts`,
   `apps/ui/src/components/graph/BrainGraphStage.tsx`,
   `apps/ui/src/components/graph/ForceBrainGraph.tsx`,
   `apps/ui/src/components/graph/ForceBrainGraph.module.css`,
   `apps/ui/src/types/react-force-graph-2d.d.ts`,
   `apps/ui/src/components/detail/DetailPopover.tsx`,
   `apps/ui/src/components/detail/DetailPopover.module.css`,
   `apps/ui/src/components/detail/TaskVetoForm.tsx`,
   `apps/ui/src/components/shell/RemedyShell.tsx`,
   `tests/ui_contracts/test_veto_controls_contract.py`,
   `tests/ui_contracts/test_semantic_zoom_wiring.py` and
   `docs/ui/design_reference/assumption_log.md`. The one edit allowed in
   `test_semantic_zoom_wiring.py` is its pin `"ctx.globalAlpha = dim;"` becoming
   `"ctx.globalAlpha = dim * vetoFade;"`; declare it. Report the list
   `git diff --name-only b9b16909` measures after C7. Do NOT touch `packages/`, `apps/cli/`,
   `nodeStates.ts` or any other file under `renderers/`, `BrainGraphCanvas.tsx`,
   `apps/ui/package.json`, `.agent/context.md`, `.agent/candidates.md` or
   `.agent/operator_questions.md`.
4. If a gate goes red on a test this round did not write, STOP, commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back with the tree clean: a draft
   you cannot verify is saved as a patch under your own directory and removed from the tree. A
   test this round itself wrote that is wrong may be corrected inside the path set, in its own
   commit, and declared. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave every worktree `git worktree list` showed at your step 4, and every stash, alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F027 exactly one, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload the line count, byte count and sha256 you measured against the
 table; then each `.agent/authored/f027-r8-*` payload copy compared byte for byte with its source
 (the block copy against `.remedy-wt/f027-r8/block.md`), read back with `git show <C1>:<path>`.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 318158 | da171d6b300f84effdf2531c655047d895acfaa03df23a3bc641378af9b6bdd9 |
 | .agent/decisions.md | 2189106 | 550f72c4007e12d629608ca7cfd24e9a3f8cf703b412362dfcb449fa9c4b59b5 |
 | .agent/prose_slips.md | 369428 | 2c66e3617f67dfb4fe6f06977c7d53034d817fd5ab8410bd60778210b460c9ef |
 | .agent/plan.md | 1097 | ae20aa227eb0d0c616b85d8d52d28af63c01ed7edfca37dd58e58e03b05d2f60 |
 Also the open set by distinct id, with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's text at C2 (the reviewer read `[]`).

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_veto_controls_contract.py
 tests/ui_contracts/test_semantic_zoom_wiring.py` at the last code commit, and the `SKIPPED` lines
 of G4, which must name no TypeScript, lint or vitest node.

G4 THE TESTS — in the primary checkout at the last code commit, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_dashboard_vetoes.py tests/ui_server/test_command_channel.py tests/regression/test_named_bugs.py tests/orchestration/test_project_brain.py tests/orchestration/test_test_runner.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 It must read no failure. The toolchain's own tests are in it and must each be named PASSED by
 `-rA` in a second, narrower run over `tests/ui_server/test_dashboard_contract.py`,
 `tests/ui_contracts/test_ui_lint.py` and `tests/orchestration/test_test_runner.py`:
 `test_typescript_compiles`, both tests of `test_ui_lint.py`, and `test_vitest_passes`. The reviewer
 read this selection green at `b9b16909` in two parts, serially. Report every `SKIPPED` line
 and the nodes each new test file contributes (`--collect-only -q`). Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f027-r8-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs the named tests, restores the bytes, and prints one line per mutation: its
 label, the exit code, the failed count and the failing test names. It runs an unmutated control
 first and last for each runner and ends with `restored byte-identical: True` per file and a final
 line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Python mutations run
 `python3 -B -m pytest -q -p no:cacheprovider tests/ui_contracts/test_veto_controls_contract.py`
 from the worktree's root after purging its `__pycache__` directories. TypeScript mutations run
 `/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest run --config <scratch config>` from
 `/home/decodeux/Repos/remedy/apps/ui`, the scratch config under your own directory a PLAIN OBJECT
 with `root` the primary `apps/ui`, `cacheDir` under `.remedy-wt/`, and `test: { environment:
 "node", include: [<the worktree's vetoView, vetoSend and brainView .test.ts files by absolute
 path>] }` — round 7's route; before the mutations, prove the route reads the worktree's sources
 by a top-level `throw` in one of them, and report it. The mutations:
  m1 `vetoHoverText` drops the reason from the vetoed text;
  m2 `vetoHoverText` names an unreachable task's vetoing task by id instead of title;
  m3 `taskVetoAction` ignores `vetoableTaskIds`;
  m4 `taskVetoAction` ignores the section's `error`;
  m5 `vetoAnswerSentence("")` reads as answered;
  m6 `vetoFadedNodeIds` drops the `task:` prefix;
  m7 `buildVetoTaskRequest` sends the task as `task` instead of `task_id`;
  m8 `buildVetoTaskRequest` accepts a blank reason;
  m9 `describeVetoTaskResult` reads a 409 `task_already_vetoed` as the generic refusal;
  m10 the accepted sentence ignores the size of `unreachable`;
  m11 `ForceBrainGraph.tsx` sets the tooltip's text through `innerHTML`;
  m12 `ForceBrainGraph.tsx`'s node fade reads `1` instead of `VETO_DOWNSTREAM_ALPHA`;
  m13 the popover mounts `TaskVetoForm` without the `vetoAction` gate;
  m14 `RemedyShell.tsx` stops passing `onSelectTask`.
 Run it in `git worktree add --detach .remedy-wt/f027-r8-mut <last code commit>` and report its
 whole output. EVERY mutation must be red; a green one is reported as green, never papered over:
 you then say whether a test can see the behaviour at all, add the test that catches it if one
 can, and re-run the tool. Then `git worktree remove --force .remedy-wt/f027-r8-mut`,
 `git worktree prune`, and `git worktree list`; and `git status --porcelain` must be empty, a
 stray `.vite/` included.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty; `git log --oneline`
 from `b9b16909` to the tip; `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected, every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 2
of feature F027, round 8, and says in one sentence how much context you had left. Where S1 to S6
leave a choice open, make it, say so in the deviations, and never widen the path set for it.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 8, then the diamond end-to-end through the door and the runner. State the open-findings
count, 0, and the operator-questions count, 5.
